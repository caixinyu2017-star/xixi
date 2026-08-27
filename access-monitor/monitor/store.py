"""本地状态存储（SQLite）。

存三样东西：
1. 已经见过的访问记录（去重 + 窗口统计的数据源）
2. 已经发过的告警（做冷却和限流）
3. IP 画像缓存（省 API 配额，也让离线时仍有历史信息）

用 SQLite 而不是 JSON，是因为要按时间窗口做范围查询，而且断电/强杀不会把文件写坏。
"""
from __future__ import annotations

import json
import sqlite3
import threading
from contextlib import closing
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .models import IpProfile, VisitRecord

SCHEMA = """
CREATE TABLE IF NOT EXISTS seen_records (
    key           TEXT PRIMARY KEY,
    ip            TEXT NOT NULL,
    visited_at    TEXT,
    visited_ts    REAL,
    page          TEXT,
    page_title    TEXT,
    referer       TEXT,
    user_agent    TEXT,
    site          TEXT,
    raw_json      TEXT,
    first_seen_at TEXT NOT NULL,
    first_seen_ts REAL NOT NULL,
    alerted       INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_seen_visited_ts ON seen_records(visited_ts);
CREATE INDEX IF NOT EXISTS idx_seen_first_seen_ts ON seen_records(first_seen_ts);
CREATE INDEX IF NOT EXISTS idx_seen_ip ON seen_records(ip);

CREATE TABLE IF NOT EXISTS alerts (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    rule         TEXT NOT NULL,
    dedup_key    TEXT,
    severity     TEXT,
    title        TEXT,
    triggered_at TEXT NOT NULL,
    triggered_ts REAL NOT NULL,
    payload_json TEXT,
    delivered    TEXT
);
CREATE INDEX IF NOT EXISTS idx_alerts_ts ON alerts(triggered_ts);
CREATE INDEX IF NOT EXISTS idx_alerts_rule ON alerts(rule, triggered_ts);

CREATE TABLE IF NOT EXISTS ip_cache (
    ip           TEXT PRIMARY KEY,
    profile_json TEXT NOT NULL,
    updated_at   TEXT NOT NULL,
    updated_ts   REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS kv (
    k TEXT PRIMARY KEY,
    v TEXT
);
"""


class Store:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(str(self.path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        with self._lock:
            self._conn.executescript(SCHEMA)
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.commit()

    def close(self) -> None:
        with self._lock:
            self._conn.close()

    # ------------------------------------------------------------------ #
    # 通用 KV（记住自动发现出来的记录页 URL 之类）
    # ------------------------------------------------------------------ #
    def get(self, key: str, default: str = "") -> str:
        with self._lock:
            row = self._conn.execute("SELECT v FROM kv WHERE k=?", (key,)).fetchone()
        return row["v"] if row else default

    def set(self, key: str, value: str) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT INTO kv(k, v) VALUES(?,?) ON CONFLICT(k) DO UPDATE SET v=excluded.v",
                (key, value),
            )
            self._conn.commit()

    # ------------------------------------------------------------------ #
    # 访问记录
    # ------------------------------------------------------------------ #
    def is_empty(self) -> bool:
        with self._lock:
            row = self._conn.execute("SELECT COUNT(*) AS c FROM seen_records").fetchone()
        return int(row["c"]) == 0

    def filter_new(self, records: Iterable[VisitRecord]) -> List[VisitRecord]:
        """返回还没入库过的记录（保持原顺序）。"""
        records = list(records)
        if not records:
            return []
        keys = [r.key for r in records]
        placeholders = ",".join("?" * len(keys))
        with self._lock:
            rows = self._conn.execute(
                f"SELECT key FROM seen_records WHERE key IN ({placeholders})", keys
            ).fetchall()
        known = {r["key"] for r in rows}
        return [r for r in records if r.key not in known]

    def add_records(self, records: Iterable[VisitRecord], now: Optional[datetime] = None) -> int:
        now = now or datetime.now()
        rows: List[Tuple[Any, ...]] = []
        for r in records:
            r.first_seen_at = r.first_seen_at or now
            rows.append((
                r.key, r.ip,
                r.visited_at.isoformat() if r.visited_at else None,
                r.visited_at.timestamp() if r.visited_at else None,
                r.page, r.page_title, r.referer, r.user_agent, r.site,
                json.dumps(r.raw, ensure_ascii=False),
                r.first_seen_at.isoformat(), r.first_seen_at.timestamp(),
            ))
        if not rows:
            return 0
        with self._lock:
            cur = self._conn.executemany(
                "INSERT OR IGNORE INTO seen_records"
                "(key, ip, visited_at, visited_ts, page, page_title, referer, user_agent, site,"
                " raw_json, first_seen_at, first_seen_ts) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                rows,
            )
            self._conn.commit()
        return cur.rowcount if cur.rowcount and cur.rowcount > 0 else 0

    def records_since(self, since: datetime, use_visit_time: bool = True) -> List[VisitRecord]:
        """取窗口内的记录。

        ``use_visit_time=True`` 用后台标注的访问时间；如果后台没给时间（解析不出来），
        自动回落到「我们第一次看到它的时间」。
        """
        col = "visited_ts" if use_visit_time else "first_seen_ts"
        ts = since.timestamp()
        with self._lock:
            rows = self._conn.execute(
                f"SELECT * FROM seen_records WHERE COALESCE({col}, first_seen_ts) >= ? "
                f"ORDER BY COALESCE({col}, first_seen_ts) ASC",
                (ts,),
            ).fetchall()
        return [self._row_to_record(r) for r in rows]

    def all_known_ips(self) -> set:
        with self._lock:
            rows = self._conn.execute("SELECT DISTINCT ip FROM seen_records").fetchall()
        return {r["ip"] for r in rows}

    def prune(self, older_than_days: int = 30) -> int:
        cutoff = (datetime.now() - timedelta(days=older_than_days)).timestamp()
        with self._lock:
            cur = self._conn.execute("DELETE FROM seen_records WHERE first_seen_ts < ?", (cutoff,))
            self._conn.execute("DELETE FROM alerts WHERE triggered_ts < ?", (cutoff,))
            self._conn.commit()
        return cur.rowcount or 0

    @staticmethod
    def _row_to_record(row: sqlite3.Row) -> VisitRecord:
        rec = VisitRecord(
            ip=row["ip"],
            visited_at=datetime.fromisoformat(row["visited_at"]) if row["visited_at"] else None,
            page=row["page"] or "",
            page_title=row["page_title"] or "",
            referer=row["referer"] or "",
            user_agent=row["user_agent"] or "",
            site=row["site"] or "",
            raw=json.loads(row["raw_json"]) if row["raw_json"] else {},
            first_seen_at=datetime.fromisoformat(row["first_seen_at"]),
        )
        return rec

    # ------------------------------------------------------------------ #
    # 告警
    # ------------------------------------------------------------------ #
    def last_alert_ts(self, rule: Optional[str] = None, dedup_key: Optional[str] = None) -> Optional[float]:
        sql = "SELECT MAX(triggered_ts) AS ts FROM alerts WHERE 1=1"
        params: List[Any] = []
        if rule:
            sql += " AND rule = ?"
            params.append(rule)
        if dedup_key:
            sql += " AND dedup_key = ?"
            params.append(dedup_key)
        with self._lock:
            row = self._conn.execute(sql, params).fetchone()
        return row["ts"] if row and row["ts"] is not None else None

    def alerts_since(self, since: datetime) -> int:
        with self._lock:
            row = self._conn.execute(
                "SELECT COUNT(*) AS c FROM alerts WHERE triggered_ts >= ?", (since.timestamp(),)
            ).fetchone()
        return int(row["c"])

    def record_alert(self, alert, delivered: Optional[Dict[str, Any]] = None) -> int:
        with self._lock:
            cur = self._conn.execute(
                "INSERT INTO alerts(rule, dedup_key, severity, title, triggered_at, triggered_ts,"
                " payload_json, delivered) VALUES (?,?,?,?,?,?,?,?)",
                (
                    alert.rule, alert.dedup_key, alert.severity, alert.title,
                    alert.triggered_at.isoformat(), alert.triggered_at.timestamp(),
                    json.dumps(alert.to_dict(), ensure_ascii=False),
                    json.dumps(delivered or {}, ensure_ascii=False),
                ),
            )
            keys = [r.key for r in alert.records]
            if keys:
                self._conn.executemany(
                    "UPDATE seen_records SET alerted=1 WHERE key=?", [(k,) for k in keys]
                )
            self._conn.commit()
        return int(cur.lastrowid or 0)

    # ------------------------------------------------------------------ #
    # IP 画像缓存
    # ------------------------------------------------------------------ #
    def get_ip_profile(self, ip: str, max_age_days: int = 7) -> Optional[IpProfile]:
        with self._lock:
            row = self._conn.execute("SELECT * FROM ip_cache WHERE ip=?", (ip,)).fetchone()
        if not row:
            return None
        age = datetime.now().timestamp() - float(row["updated_ts"])
        if age > max_age_days * 86400:
            return None
        try:
            data = json.loads(row["profile_json"])
        except json.JSONDecodeError:
            return None
        data.pop("location_text", None)
        data.pop("network_text", None)
        data.pop("labels", None)
        looked = data.pop("looked_up_at", None)
        prof = IpProfile(**{k: v for k, v in data.items() if k in IpProfile.__dataclass_fields__})
        if looked:
            try:
                prof.looked_up_at = datetime.fromisoformat(looked)
            except ValueError:
                pass
        return prof

    def put_ip_profile(self, profile: IpProfile) -> None:
        now = datetime.now()
        with self._lock:
            self._conn.execute(
                "INSERT INTO ip_cache(ip, profile_json, updated_at, updated_ts) VALUES(?,?,?,?) "
                "ON CONFLICT(ip) DO UPDATE SET profile_json=excluded.profile_json,"
                " updated_at=excluded.updated_at, updated_ts=excluded.updated_ts",
                (profile.ip, json.dumps(profile.to_dict(), ensure_ascii=False),
                 now.isoformat(), now.timestamp()),
            )
            self._conn.commit()

    # ------------------------------------------------------------------ #
    def stats(self) -> Dict[str, int]:
        with self._lock:
            with closing(self._conn.cursor()) as cur:
                records = cur.execute("SELECT COUNT(*) FROM seen_records").fetchone()[0]
                ips = cur.execute("SELECT COUNT(DISTINCT ip) FROM seen_records").fetchone()[0]
                alerts = cur.execute("SELECT COUNT(*) FROM alerts").fetchone()[0]
                cached = cur.execute("SELECT COUNT(*) FROM ip_cache").fetchone()[0]
        return {"records": records, "ips": ips, "alerts": alerts, "ip_cache": cached}
