#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cn_journal_probe.py — 读 ISSN 清单批量探 OpenAlex source 体量。

读 assets/cn_core_issn.csv（或 --csv 指定），逐刊 GET
  https://api.openalex.org/sources/issn:{ISSN}
取 OpenAlex source id / display_name / works_count / cited_by_count / country_code，
输出体量表（JSON + Markdown），并记录每次请求 HTTP 码。

诚实约定：
- OpenAlex 常把中文刊名/标题存成拼音或英译（如"计算机学报"->"Chinese Journal of
  Computers"），故按 ISSN 检索比按 language:zh 更可靠（见 SKILL.md）。
- ISSN 解析失败（404）如实标 NOT_FOUND，不脑补。
- 无网络时回退合成体量，打印 [OFFLINE]。
- 礼貌池邮箱经环境变量 OPENALEX_MAILTO / CROSSREF_MAILTO 或 --mailto 传入；不传则匿名（不伪造）。
- OpenAlex key 经环境变量 OPENALEX_API_KEY 或 --api-key 传入（2026 起需 key，口径见 references）。

用法：
    python scripts/cn_journal_probe.py --mailto you@inst.edu
    python scripts/cn_journal_probe.py --csv assets/cn_core_issn.csv --sleep 0.2
"""
from __future__ import annotations
import argparse
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request

_MAILTO = (os.environ.get("OPENALEX_MAILTO") or os.environ.get("CROSSREF_MAILTO") or "").strip()
_API_KEY = os.environ.get("OPENALEX_API_KEY", "").strip()
TIMEOUT = 30
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = os.path.join(HERE, "..", "assets", "cn_core_issn.csv")
# 限速/临时故障指数退避重试（零依赖、零费用）：OpenAlex 匿名走共享池高峰常 429。
_RETRY_CODES = {429, 502, 503, 504}
_MAX_RETRIES = 2
_BACKOFF_BASE = 0.5
_sleep = time.sleep


def _retry_after(e, attempt: int) -> float:
    ra = e.headers.get("Retry-After") if getattr(e, "headers", None) else None
    if ra:
        try:
            return min(float(ra), 8.0)
        except ValueError:
            pass
    return min(_BACKOFF_BASE * (2 ** attempt), 8.0)


def _user_agent() -> str:
    if _MAILTO:
        return "Light-literature-search/1.0 (mailto:%s)" % _MAILTO
    return "Light-literature-search/1.0"


def probe_issn(issn: str) -> dict:
    params = {"select": "id,display_name,works_count,cited_by_count,country_code"}
    if _MAILTO:
        params["mailto"] = _MAILTO
    if _API_KEY:
        params["api_key"] = _API_KEY
    url = f"https://api.openalex.org/sources/issn:{issn}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": _user_agent(), "Accept": "application/json"})
    for attempt in range(_MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                d = json.loads(resp.read().decode("utf-8", "replace"))
                return {"issn": issn, "http": resp.getcode(), "status": "OK",
                        "openalex_id": (d.get("id") or "").rsplit("/", 1)[-1],
                        "display_name": d.get("display_name"),
                        "works_count": d.get("works_count"),
                        "cited_by_count": d.get("cited_by_count"),
                        "country_code": d.get("country_code")}
        except urllib.error.HTTPError as e:  # noqa
            if e.code in _RETRY_CODES and attempt < _MAX_RETRIES:
                _sleep(_retry_after(e, attempt))
                continue
            return {"issn": issn, "http": e.code,
                    "status": "NOT_FOUND" if e.code == 404 else "HTTP_ERROR"}
        except Exception as e:  # noqa
            return {"issn": issn, "http": 0, "status": "NETWORK_ERROR", "err": str(e)}


def load_issns(csv_path: str) -> list[dict]:
    rows = []
    with open(csv_path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def to_markdown(results: list[dict]) -> str:
    lines = ["# 中文核心刊 OpenAlex 体量探测", "",
             "按 ISSN 检索（比 language:zh 更可靠；OpenAlex 刊名多为英译/拼音）。", "",
             "| ISSN | 中文刊名 | OpenAlex display_name | OA_id | works | cited_by | 国别 | 状态 |",
             "|------|---------|----------------------|-------|-------|----------|------|------|"]
    for r in results:
        lines.append(f"| {r.get('issn','')} | {r.get('journal_cn','')} | "
                     f"{r.get('display_name') or ''} | {r.get('openalex_id') or ''} | "
                     f"{r.get('works_count') if r.get('works_count') is not None else ''} | "
                     f"{r.get('cited_by_count') if r.get('cited_by_count') is not None else ''} | "
                     f"{r.get('country_code') or ''} | {r.get('status','')}(HTTP{r.get('http','')}) |")
    return "\n".join(lines)


_SYNTHETIC = [{"issn": "0254-4164", "http": 200, "status": "OK",
               "openalex_id": "S4210175330", "display_name": "Chinese Journal of Computers",
               "works_count": 1264, "cited_by_count": 6374, "country_code": "CN",
               "journal_cn": "计算机学报"}]


def run(csv_path: str, sleep: float = 0.2, offline: bool = False) -> dict:
    rows = load_issns(csv_path)
    results = []
    net_dead = False
    for row in rows:
        if offline or net_dead:
            break
        pr = probe_issn(row["issn"])
        pr["journal_cn"] = row.get("journal_cn", "")
        results.append(pr)
        print(f"[HTTP] {row['issn']} -> {pr['http']} {pr['status']}", file=sys.stderr)
        if pr["status"] == "NETWORK_ERROR":
            net_dead = True
        time.sleep(sleep)
    if offline or net_dead or not results:
        print("[OFFLINE] 网络不可达，使用内置合成体量样本。", file=sys.stderr)
        results = [dict(_SYNTHETIC[0])]
        offline = True
    ok = sum(1 for r in results if r["status"] == "OK")
    return {"offline": offline, "total": len(results), "ok": ok, "results": results}



def _selftest() -> int:
    import tempfile
    fd, csv_path = tempfile.mkstemp(prefix="cn_journal_probe_", suffix=".csv")
    os.close(fd)
    try:
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            f.write("issn,journal_cn\n0254-4164,计算机学报\n")
        out = run(csv_path, sleep=0, offline=True)
    finally:
        try:
            os.unlink(csv_path)
        except OSError:
            pass
    assert out["offline"] is True, out
    assert out["total"] == 1 and out["ok"] == 1, out
    md = to_markdown(out["results"])
    assert "计算机学报" in md and "Chinese Journal of Computers" in md, md
    print("[selftest] PASS cn_journal_probe")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="批量探中文核心刊 OpenAlex 体量")
    ap.add_argument("--csv", default=DEFAULT_CSV)
    ap.add_argument("--sleep", type=float, default=0.2)
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--json-out", default="")
    ap.add_argument("--mailto", default="",
                    help="礼貌池邮箱（也可设环境变量 OPENALEX_MAILTO / CROSSREF_MAILTO）；不传则匿名查")
    ap.add_argument("--api-key", default="",
                    help="OpenAlex API key（也可设环境变量 OPENALEX_API_KEY）；口径见本技能 references")
    ap.add_argument("--selftest", action="store_true", help="run offline synthetic self-test")
    args = ap.parse_args()

    global _MAILTO, _API_KEY
    if args.mailto:
        _MAILTO = args.mailto.strip()
    if args.api_key:
        _API_KEY = args.api_key.strip()

    if args.selftest:
        sys.exit(_selftest())

    out = run(args.csv, args.sleep, args.offline)
    md = to_markdown(out["results"])
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
    print(md)
    print(f"\n[SUMMARY] total={out['total']} ok={out['ok']} offline={out['offline']}")


if __name__ == "__main__":
    main()

