#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tracker.py — 文献定期追踪的 SQLite 持久化（借 paper-tracker，升级"已读库 txt"）。

literature-search 原有"定期追踪协议"用一个 known_dois.txt 记已读 DOI、每次重跑 diff。
本脚本把它升级成 **SQLite 持久库**（标准库 sqlite3，零外部依赖）：
  - 把检索结果 upsert 进库，按 DOI（无 DOI 回退 规范化标题+年）去重
  - 记 first_seen_run / last_seen_run / status（new/seen/read）/ 被引快照随轮次变化
  - 增量：每轮重跑只把"库里没见过的"标 new，已见的更新 last_seen + 被引
  - 导出 JSON / Markdown / 仅新增清单，状态可留存可查历史

诚实纪律（与 search_normalize 一致）：被引数标来源库不跨库比；不臆造；DOI 缺失如实回退标题键；
本脚本只做"持久化去重与状态管理"，检索本身仍由 search_normalize/pipeline 产出 records 喂入。

用法：
  # 把一次检索的 JSON（search_normalize --json-out 的产物）灌进追踪库
  python tracker.py --db goats.db --ingest search.json --run 2026-06-13
  python tracker.py --db goats.db --new            # 列本轮新增
  python tracker.py --db goats.db --export md --out tracked.md
  python tracker.py --selftest
"""
from __future__ import annotations
import argparse
import json
import re
import sqlite3
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

SCHEMA = """
CREATE TABLE IF NOT EXISTS papers (
    key            TEXT PRIMARY KEY,   -- DOI（小写）或 t:<规范化标题>+<年>
    doi            TEXT,
    title          TEXT,
    year           INTEGER,
    venue          TEXT,
    cited_by       INTEGER,
    cited_by_src   TEXT,
    status         TEXT DEFAULT 'new', -- new / seen / read
    first_seen_run TEXT,
    last_seen_run  TEXT,
    times_seen     INTEGER DEFAULT 1
);
"""


def _norm_doi(doi: str | None) -> str:
    if not doi:
        return ""
    d = (doi or "").lower().strip()
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", d)


def _norm_title(t: str) -> str:
    return re.sub(r"[^a-z0-9一-鿿]+", "", (t or "").lower())


def _rec_key(rec: dict) -> str:
    """去重键：优先 DOI，无 DOI 回退 t:<规范化标题>+<年>（与 search_normalize 同口径）。"""
    doi = _norm_doi(rec.get("doi"))
    if doi:
        return doi
    return "t:" + _norm_title(rec.get("title", "")) + str(rec.get("year") or "")


def connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def ingest(conn: sqlite3.Connection, records: list[dict], run: str) -> dict:
    """把一轮检索结果 upsert 进库。返回 {new, updated, total} 统计。"""
    new = updated = 0
    cur = conn.cursor()
    for r in records:
        key = _rec_key(r)
        if not key or key == "t:":
            continue
        row = cur.execute("SELECT key, times_seen FROM papers WHERE key=?", (key,)).fetchone()
        if row is None:
            cur.execute(
                "INSERT INTO papers (key,doi,title,year,venue,cited_by,cited_by_src,"
                "status,first_seen_run,last_seen_run,times_seen) "
                "VALUES (?,?,?,?,?,?,?,'new',?,?,1)",
                (key, _norm_doi(r.get("doi")), r.get("title"), r.get("year"),
                 r.get("venue"), r.get("cited_by"), r.get("cited_by_src"), run, run))
            new += 1
        else:
            # 已见过：更新被引快照 + last_seen + times_seen，status 从 new 转 seen
            cur.execute(
                "UPDATE papers SET cited_by=?, cited_by_src=?, last_seen_run=?, "
                "times_seen=times_seen+1, status=CASE WHEN status='new' THEN 'seen' ELSE status END "
                "WHERE key=?",
                (r.get("cited_by"), r.get("cited_by_src"), run, key))
            updated += 1
    conn.commit()
    return {"new": new, "updated": updated, "total": new + updated, "run": run}


def list_papers(conn: sqlite3.Connection, status: str = "") -> list[dict]:
    q = "SELECT * FROM papers"
    args = ()
    if status:
        q += " WHERE status=?"
        args = (status,)
    q += " ORDER BY (cited_by IS NULL), cited_by DESC"
    return [dict(r) for r in conn.execute(q, args).fetchall()]


def mark_read(conn: sqlite3.Connection, doi: str) -> bool:
    cur = conn.execute("UPDATE papers SET status='read' WHERE key=? OR doi=?",
                       (_norm_doi(doi), _norm_doi(doi)))
    conn.commit()
    return cur.rowcount > 0


def export_md(rows: list[dict], title: str = "追踪文献") -> str:
    lines = [f"# {title}（共 {len(rows)} 条）", "",
             "> SQLite 持久追踪；被引为快照标来源库不可跨库比；status: new(本轮新增)/seen/read。", "",
             "| # | 状态 | 标题 | 年 | 被引(来源) | 首见轮 | DOI |",
             "|---|------|------|----|-----------|--------|-----|"]
    for i, r in enumerate(rows, 1):
        lines.append(f"| {i} | {r['status']} | {(r.get('title') or '')[:60].replace('|','/')} | "
                     f"{r.get('year') or ''} | {r.get('cited_by')}({r.get('cited_by_src') or '?'}) | "
                     f"{r.get('first_seen_run') or ''} | {r.get('doi') or ''} |")
    return "\n".join(lines)


def _selftest() -> int:
    print("### tracker 离线自测", file=sys.stderr)
    conn = connect(":memory:")  # 内存库，不落盘

    r1 = [{"doi": "10.1/a", "title": "Goat A", "year": 2022, "cited_by": 10, "cited_by_src": "OpenAlex"},
          {"doi": "", "title": "No DOI paper", "year": 2021, "cited_by": 5, "cited_by_src": "Crossref"}]
    s1 = ingest(conn, r1, run="2026-06-01")
    assert s1["new"] == 2 and s1["updated"] == 0, s1
    # 全是 new
    assert len(list_papers(conn, status="new")) == 2

    # 第二轮：a 重现（被引涨到 15）+ 新增 b
    r2 = [{"doi": "10.1/a", "title": "Goat A", "year": 2022, "cited_by": 15, "cited_by_src": "OpenAlex"},
          {"doi": "10.1/b", "title": "Goat B", "year": 2023, "cited_by": 3, "cited_by_src": "OpenAlex"}]
    s2 = ingest(conn, r2, run="2026-06-08")
    assert s2["new"] == 1 and s2["updated"] == 1, s2
    # a 被引快照更新为 15、status 转 seen、times_seen=2
    a = conn.execute("SELECT * FROM papers WHERE key='10.1/a'").fetchone()
    assert a["cited_by"] == 15 and a["status"] == "seen" and a["times_seen"] == 2, dict(a)
    # b 是本轮新增
    new_rows = list_papers(conn, status="new")
    assert any(r["key"] == "10.1/b" for r in new_rows), new_rows

    # 无 DOI 走标题键，不与有 DOI 的混
    nod = conn.execute("SELECT key FROM papers WHERE doi=''").fetchone()
    assert nod["key"].startswith("t:"), dict(nod)

    # mark_read
    assert mark_read(conn, "10.1/a") is True
    assert conn.execute("SELECT status FROM papers WHERE key='10.1/a'").fetchone()["status"] == "read"

    # 导出
    md = export_md(list_papers(conn))
    assert "追踪文献" in md and "10.1/b" in md, md
    conn.close()
    print("[selftest] PASS tracker offline")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="文献定期追踪 SQLite 持久化")
    ap.add_argument("--db", default="tracked_papers.db", help="SQLite 库路径")
    ap.add_argument("--ingest", help="灌入的检索结果 JSON（含 records 数组，或直接是数组）")
    ap.add_argument("--run", default="", help="本轮标识（如日期 2026-06-13）")
    ap.add_argument("--new", action="store_true", help="列本轮 status=new 的新增")
    ap.add_argument("--export", choices=["json", "md"], help="导出全部追踪文献")
    ap.add_argument("--mark-read", help="把某 DOI 标为 read")
    ap.add_argument("--out", default="")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return _selftest()

    conn = connect(args.db)
    if args.ingest:
        with open(args.ingest, encoding="utf-8") as f:
            data = json.load(f)
        records = data.get("records", data) if isinstance(data, dict) else data
        run = args.run or "unspecified-run"
        stat = ingest(conn, records, run)
        print(f"[INGEST] run={run} new={stat['new']} updated={stat['updated']}", file=sys.stderr)
    if args.mark_read:
        ok = mark_read(conn, args.mark_read)
        print(f"[MARK-READ] {args.mark_read} -> {'ok' if ok else '未命中'}", file=sys.stderr)
    if args.new:
        rows = list_papers(conn, status="new")
        print(export_md(rows, "本轮新增文献"))
    if args.export:
        rows = list_papers(conn)
        out = json.dumps(rows, ensure_ascii=False, indent=2) if args.export == "json" else export_md(rows)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as f:
                f.write(out)
            print(f"已导出 {len(rows)} 条 -> {args.out}", file=sys.stderr)
        else:
            print(out)
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
