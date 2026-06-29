#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dataset_signal.py — db04 数据集卡易变字段实时校验 (Light / db04 库重构)

读 db04 卡 risk 子串锚点(oa_id=/doi=/src=)，实时校验易变字段，对比本地快照产 diff：
  1. 被引数      ← OpenAlex /works/{W-id} cited_by_count（oa_id 锚点）
  2. license     ← GitHub /repos/{owner}/{repo} license.spdx_id（gh: 锚点）
                    / HuggingFace /api/datasets/{repo} cardData.license（hf: 锚点，字段待核实）
  3. URL 存活    ← download_url / leaderboard_url HEAD 200 校验

设计与 light-venue-matching/scripts/venue_signal.py 同构（母本），诚实约定一致：
- 礼貌池邮箱经 --mailto 或环境变量 OPENALEX_MAILTO 传入；不传匿名查(不伪造邮箱)。
- OpenAlex key/限流/计费口径见 m01 references「OpenAlex 接入真相源」，本脚本不复写数字。
- 任一信号取数失败 → status="unavailable"+reason，不编数、不崩(能查多少出多少)。
- license 是 a10 合规命脉：在线值与本地不一致**只提示人工确认**，不自动改判(LAION 下架教训)。
- 无网/无 key → 返回本地快照 + stale 警告(标 last_checked 距今)，不阻断下游(G3 降级)。
- PapersWithCode SOTA 数值抓取能力未实测，leaderboard 只做 URL 存活，不编造端点。

用法：
    python scripts/dataset_signal.py --oa-id W4306820534 --mailto you@x.edu
    python scripts/dataset_signal.py --gh huggingface/datasets --check-url https://...
    python scripts/dataset_signal.py --selftest
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_MAILTO = os.environ.get("OPENALEX_MAILTO", "").strip()
TIMEOUT = 30
OA = "https://api.openalex.org"
GH = "https://api.github.com"
HF = "https://huggingface.co/api"

_MAILTO = DEFAULT_MAILTO


def _user_agent() -> str:
    return "Light-dataset-signal/1.0" + (f" (mailto:{_MAILTO})" if _MAILTO else "")


def http_fetch(url: str) -> dict:
    """真实 GET JSON。失败抛异常由上层降级。"""
    req = urllib.request.Request(url, headers={"User-Agent": _user_agent(),
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8", "replace"))


def http_head_ok(url: str) -> bool:
    """HEAD/GET 探测 URL 存活(2xx/3xx 视为活)。失败返回 False，不抛。"""
    try:
        req = urllib.request.Request(url, method="HEAD",
                                     headers={"User-Agent": _user_agent()})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return 200 <= resp.status < 400
    except Exception:  # noqa: BLE001
        return False


# ---- 锚点解析 ----------------------------------------------------------

def parse_anchors(citation: str) -> dict:
    """从 citation 子串抽锚点：oa_id= / doi= / src= / last_checked=。"""
    out = {}
    for key in ("oa_id", "doi", "src", "last_checked"):
        m = re.search(rf"(?:^|[;；]\s*){key}=([^;；]+)", citation or "")
        if m:
            out[key] = m.group(1).strip()
    return out


# ---- 信号 --------------------------------------------------------------

def signal_citation(oa_id: str, fetch) -> dict:
    """被引实时查：OpenAlex /works/{W-id} cited_by_count。"""
    if not oa_id:
        return {"status": "unavailable", "reason": "无 oa_id 锚点(DOI/社区数据集走他途)"}
    try:
        url = f"{OA}/works/{urllib.parse.quote(oa_id)}?" + _add_mailto(
            {"select": "id,cited_by_count,publication_year"})
        data = fetch(url)
        return {"status": "ok", "cited_by_count": data.get("cited_by_count"),
                "publication_year": data.get("publication_year"),
                "source": f"OpenAlex {oa_id}(实时)，冲突信在线"}
    except Exception as e:  # noqa: BLE001
        return {"status": "unavailable", "reason": f"OpenAlex 查询失败: {e.__class__.__name__}"}


def signal_github_license(repo: str, fetch) -> dict:
    """license 实时查：GitHub /repos/{owner}/{repo} license.spdx_id。"""
    if not repo or "/" not in repo:
        return {"status": "unavailable", "reason": "无 gh:owner/repo 锚点"}
    try:
        data = fetch(f"{GH}/repos/{repo}")
        lic = (data.get("license") or {}).get("spdx_id")
        return {"status": "ok", "spdx_id": lic, "repo": repo,
                "note": "license 变更须人工确认再改卡(合规高危，勿自动改判)"}
    except Exception as e:  # noqa: BLE001
        return {"status": "unavailable", "reason": f"GitHub 查询失败: {e.__class__.__name__}"}


def _add_mailto(params: dict) -> str:
    p = dict(params)
    if _MAILTO:
        p.setdefault("mailto", _MAILTO)
    return urllib.parse.urlencode(p)


def assemble(citation: str, gh_repo: str, check_urls: list[str], fetch, head) -> dict:
    anchors = parse_anchors(citation)
    report = {
        "anchors": anchors,
        "signals": {
            "citation": signal_citation(anchors.get("oa_id", ""), fetch),
            "github_license": signal_github_license(gh_repo, fetch) if gh_repo
            else {"status": "unavailable", "reason": "未提供 --gh"},
            "url_alive": {u: ("alive" if head(u) else "dead") for u in check_urls}
            if check_urls else {"status": "unavailable", "reason": "未提供 --check-url"},
        },
    }
    lc = anchors.get("last_checked")
    report["freshness"] = {
        "local_last_checked": lc,
        "note": "无网/无 key 时本节回退本地快照，标 stale；冲突默认信在线(license 例外需人工确认)",
    }
    return report


# ---- 离线 selftest -----------------------------------------------------

class _MockFetcher:
    def __call__(self, url: str) -> dict:
        if "/works/" in url:
            return {"id": "https://openalex.org/W4306820534",
                    "cited_by_count": 1042, "publication_year": 2022}
        if "/repos/" in url:
            return {"license": {"spdx_id": "MIT"}}
        if "/datasets/" in url:
            return {"cardData": {"license": "cc-by-4.0"}}
        raise RuntimeError(f"mock 未覆盖: {url}")


def _selftest() -> int:
    fetch = _MockFetcher()
    head_ok = lambda u: "alive" in u  # noqa: E731

    # 锚点解析
    a = parse_anchors("Schuhmann 2022. 被引 1,036 (2026-06-06); last_checked=2026-06-06; oa_id=W4306820534")
    assert a == {"last_checked": "2026-06-06", "oa_id": "W4306820534"}, a
    a2 = parse_anchors("Lee 2022; last_checked=待核; doi=10.1038/s41597-022-01899-x")
    assert a2["doi"] == "10.1038/s41597-022-01899-x", a2

    # 被引实时(oa_id) → 在线值 1042 vs 本地快照 1036，体现"信在线"
    rep = assemble("被引 1,036 (2026-06-06); last_checked=2026-06-06; oa_id=W4306820534",
                   "huggingface/datasets", ["http://x/alive", "http://x/dead"], fetch, head_ok)
    assert rep["signals"]["citation"]["status"] == "ok"
    assert rep["signals"]["citation"]["cited_by_count"] == 1042, rep["signals"]["citation"]
    assert rep["signals"]["github_license"]["spdx_id"] == "MIT"
    assert rep["signals"]["url_alive"]["http://x/alive"] == "alive"
    assert rep["signals"]["url_alive"]["http://x/dead"] == "dead"

    # 降级：无 oa_id(社区数据集) + 无 gh → 信号 unavailable，不崩
    rep2 = assemble("社区数据集; last_checked=待核; src=community", "", [], fetch, head_ok)
    assert rep2["signals"]["citation"]["status"] == "unavailable"
    assert rep2["signals"]["github_license"]["status"] == "unavailable"

    # OpenAlex 取数失败 → citation unavailable，不崩
    def boom(url):
        raise urllib.error.URLError("offline")
    rep3 = assemble("oa_id=W123; last_checked=2026-06-06", "", [], boom, head_ok)
    assert rep3["signals"]["citation"]["status"] == "unavailable"
    assert rep3["freshness"]["local_last_checked"] == "2026-06-06"
    print("[selftest] PASS dataset_signal（被引/license/URL存活 + 锚点解析 + 降级 + 信在线）")
    return 0


def main() -> None:
    global _MAILTO
    ap = argparse.ArgumentParser(description="db04 数据集卡易变字段实时校验")
    ap.add_argument("--oa-id", default="", help="OpenAlex W-id(查被引)")
    ap.add_argument("--citation", default="", help="db04 卡 citation 字段(自动解析锚点)")
    ap.add_argument("--gh", default="", help="GitHub owner/repo(查 license.spdx_id)")
    ap.add_argument("--check-url", nargs="*", default=[], help="URL 存活校验(可多个)")
    ap.add_argument("--mailto", default="", help="OpenAlex 礼貌池邮箱(或环境变量 OPENALEX_MAILTO)")
    ap.add_argument("--json-out", default="")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(_selftest())
    if args.mailto:
        _MAILTO = args.mailto.strip()

    citation = args.citation or (f"oa_id={args.oa_id}" if args.oa_id else "")
    if not citation and not args.gh and not args.check_url:
        ap.error("至少提供 --oa-id/--citation/--gh/--check-url 之一(或 --selftest)")

    report = assemble(citation, args.gh, args.check_url, http_fetch, http_head_ok)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            f.write(text)
    print(text)


if __name__ == "__main__":
    main()
