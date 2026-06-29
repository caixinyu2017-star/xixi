#!/usr/bin/env python3
"""数据卡新鲜度检查（warn-only，R8.6/G6）。

扫 databases/ 下所有数据卡的最近核查日期，列出超过阈值（默认 90 天）未复查的卡，
按库分组统计。**纯警告**：本地与 CI 都不因此变红（CI 用 continue-on-error 或纯输出接入）。
README 的"每月/每季度更新"承诺据此落地为可执行流程：每月跑一次本脚本，按清单更新。

新鲜度信号来源（两类）：
  1. db01 venues.csv 的 `last_checked_date` 列（每行一个 venue）。
  2. db03–db08 等 md 卡里的日期标头：`last_checked_date:` 字段，或散文式
     `核实日期 YYYY-MM-DD` / `研究日期 YYYY-MM` 标注（取每文件最早的一处，最保守）。

用法：
  python check_freshness.py                 # 用今天的系统日期
  python check_freshness.py --today 2026-09-20   # 指定基准日（CI/可复现）
  python check_freshness.py --threshold-days 90  # 调阈值
  python check_freshness.py --selftest           # 离线自测（内置 fixture，不读真实库）
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import io
import pathlib
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATABASES = ROOT / "databases"

DEFAULT_THRESHOLD_DAYS = 90

# 散文式日期标注：核实日期 / 核验日期 / 研究日期 / 核查日期，后接 YYYY-MM(-DD)。
PROSE_DATE_RE = re.compile(r"(?:核实日期|核验日期|研究日期|核查日期|核实于|更新于)\s*[:：]?\s*(\d{4})-(\d{2})(?:-(\d{2}))?")
# 字段式：last_checked_date: YYYY-MM(-DD)
FIELD_DATE_RE = re.compile(r"last_checked_date\s*[:：]\s*[\"']?(\d{4})-(\d{2})(?:-(\d{2}))?")


def parse_ymd(year: str, month: str, day: str | None) -> _dt.date:
    """把 YYYY-MM(-DD) 解析为 date；缺日按当月 1 号（最保守，偏老）。"""
    return _dt.date(int(year), int(month), int(day) if day else 1)


def db_key_for(path: pathlib.Path) -> str:
    rel = path.relative_to(DATABASES)
    return rel.parts[0] if rel.parts else "?"


def scan_venues_csv(csv_path: pathlib.Path) -> list[tuple[str, _dt.date]]:
    """返回 venues.csv 每行的 (标签, 日期)。多行字段安全：用 csv 模块逐行读。"""
    out: list[tuple[str, _dt.date]] = []
    if not csv_path.exists():
        return out
    with csv_path.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for i, row in enumerate(reader, 1):
            raw = (row.get("last_checked_date") or "").strip()
            m = re.fullmatch(r"(\d{4})-(\d{2})(?:-(\d{2}))?", raw)
            if not m:
                continue
            label = (row.get("venue_name") or f"row{i}").strip()[:40]
            out.append((label, parse_ymd(*m.groups())))
    return out


def scan_md_cards(db_root: pathlib.Path) -> list[tuple[str, _dt.date]]:
    """扫 md 卡，取每文件最早的一个日期标注作为该文件的新鲜度。"""
    out: list[tuple[str, _dt.date]] = []
    for md in sorted(db_root.rglob("*.md")):
        if md.name == "README.md":
            continue
        text = md.read_text(encoding="utf-8")
        dates: list[_dt.date] = []
        for m in PROSE_DATE_RE.finditer(text):
            dates.append(parse_ymd(*m.groups()))
        for m in FIELD_DATE_RE.finditer(text):
            dates.append(parse_ymd(*m.groups()))
        if dates:
            out.append((md.relative_to(ROOT).as_posix(), min(dates)))
    return out


def collect(today: _dt.date, threshold_days: int, db_root: pathlib.Path) -> dict[str, list[tuple[str, _dt.date, int]]]:
    """按库分组收集所有卡的新鲜度，返回 {db_key: [(label, date, age_days), ...]}。"""
    by_db: dict[str, list[tuple[str, _dt.date, int]]] = {}
    venues = db_root / "db01-venues-templates" / "venues.csv"
    for label, date in scan_venues_csv(venues):
        age = (today - date).days
        by_db.setdefault("db01-venues-templates", []).append((label, date, age))
    for db_dir in sorted(p for p in db_root.glob("db*") if p.is_dir()):
        for label, date in scan_md_cards(db_dir):
            age = (today - date).days
            by_db.setdefault(db_dir.name, []).append((label, date, age))
    return by_db


def report(today: _dt.date, threshold_days: int, by_db: dict) -> int:
    total = stale = 0
    print(f"数据卡新鲜度（基准日 {today.isoformat()}，阈值 {threshold_days} 天，warn-only）")
    for db_key in sorted(by_db):
        entries = by_db[db_key]
        total += len(entries)
        stale_entries = [e for e in entries if e[2] > threshold_days]
        stale += len(stale_entries)
        flag = f"{len(stale_entries)} 超期" if stale_entries else "全部新鲜"
        print(f"  {db_key}: {len(entries)} 张卡, {flag}")
        for label, date, age in sorted(stale_entries, key=lambda x: -x[2])[:20]:
            print(f"      ! {label} — {date.isoformat()}（{age} 天）")
    print(f"合计 {total} 张卡，{stale} 张 > {threshold_days} 天需复查。")
    if stale:
        print("提示：按上表逐条复查并更新 last_checked_date / 核实日期。本检查不影响 CI。")
    return 0  # warn-only：永远返回 0


def selftest() -> int:
    """离线自测：用内置 fixture 验证阈值判定，不触碰真实库、不联网。"""
    today = _dt.date(2026, 9, 20)
    by_db = {
        "db-fixture": [
            ("fresh-card", _dt.date(2026, 9, 1), (today - _dt.date(2026, 9, 1)).days),   # 19 天，新鲜
            ("stale-card", _dt.date(2026, 1, 1), (today - _dt.date(2026, 1, 1)).days),   # 262 天，超期
        ]
    }
    stale = [e for e in by_db["db-fixture"] if e[2] > DEFAULT_THRESHOLD_DAYS]
    assert len(stale) == 1 and stale[0][0] == "stale-card", "阈值判定错误"
    # 日期解析与缺日补 1 号
    assert parse_ymd("2026", "06", None) == _dt.date(2026, 6, 1)
    assert parse_ymd("2026", "06", "12") == _dt.date(2026, 6, 12)
    # 正则覆盖两类标注
    assert PROSE_DATE_RE.search("核实日期 2026-06-06") is not None
    assert PROSE_DATE_RE.search("核验日期：2026-06-12") is not None
    assert FIELD_DATE_RE.search("last_checked_date: 2026-06") is not None
    print("✓ check_freshness selftest 通过（阈值判定/日期解析/标注正则）")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="数据卡新鲜度检查（warn-only）")
    parser.add_argument("--today", help="基准日 YYYY-MM-DD（默认系统今天）")
    parser.add_argument("--threshold-days", type=int, default=DEFAULT_THRESHOLD_DAYS)
    parser.add_argument("--selftest", action="store_true", help="离线自测，不读真实库")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.today:
        today = _dt.date.fromisoformat(args.today)
    else:
        today = _dt.date.today()
    by_db = collect(today, args.threshold_days, DATABASES)
    return report(today, args.threshold_days, by_db)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
