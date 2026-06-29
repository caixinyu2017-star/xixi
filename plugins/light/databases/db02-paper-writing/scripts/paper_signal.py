#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""paper_signal.py — db02 写作样本卡「被引数」实时校验 (Light / db02 库重构)

db02 是写作训练库，被引仅作 social proof（非下游载荷）。本脚本把卡内被引快照
实时对照 OpenAlex，按「冲突信在线」回报，无网降级留快照并标 stale。

与 db03/method_signal.py、db01/venue_signal.py 同构（母本），诚实约定一致：
- 礼貌池邮箱经 --mailto 或环境变量 OPENALEX_MAILTO；不传则匿名查(不伪造邮箱)。
- OpenAlex key/限流口径见 m01 references「OpenAlex 接入真相源」，本脚本不复写数字。
- 查询失败 → status="unavailable"+reason，不编数、不崩。
- 无网 → 返回本地被引快照 + stale 警告(标 checked 距今)，不阻断写作(被引非载荷, G3)。
- 冲突默认信在线；在线 vs 快照差异>50% 提示可能 OpenAlex 记录合并/拆分(arXiv vs 正式版)，供人工核。

db02 卡锚点格式(samples_real / samples_recent 两种行都覆盖)：
  - **被引数**：221,133（2026-06-06 OpenAlex 快照…）
  - **DOI**：10.1109/cvpr.2016.90 · **OpenAlex**：W2194775991 · domain_scope=cv-视觉
  - **venue**：… · **被引**：34（2026-06-12 快照） · **DOI**：10.52202/079017-2694 …

用法：
    python scripts/paper_signal.py --doi 10.1109/cvpr.2016.90 --mailto you@x.edu
    python scripts/paper_signal.py --card-block "$(sed -n '39,46p' samples_real.md)"
    python scripts/paper_signal.py --selftest
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
_MAILTO = DEFAULT_MAILTO


def _user_agent() -> str:
    return "Light-paper-signal/1.0" + (f" (mailto:{_MAILTO})" if _MAILTO else "")


def http_fetch(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": _user_agent(),
                                               "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8", "replace"))


def _add_mailto(params: dict) -> str:
    p = dict(params)
    if _MAILTO:
        p.setdefault("mailto", _MAILTO)
    return urllib.parse.urlencode(p)


def parse_card_block(block: str) -> dict:
    """从一张卡的若干行抽锚点：DOI / 被引快照数 / OpenAlex id / 采集日期。

    兼容 samples_real(被引数：N（YYYY-MM-DD …）) 与 samples_recent(被引：N（YYYY-MM-DD 快照）)。
    被引数允许带千分位逗号；日期取行内首个 YYYY-MM-DD。
    """
    out = {}
    m = re.search(r"\*\*DOI\*\*[：:]\s*([^\s·|]+)", block)
    if m:
        out["doi"] = m.group(1).rstrip("。.")
    m = re.search(r"被引[数]?\*{0,2}[：:]\s*([\d,]+)", block)
    if m:
        out["cited_snapshot"] = int(m.group(1).replace(",", ""))
    m = re.search(r"\*\*OpenAlex\*\*[：:]\s*(W\d+)", block)
    if m:
        out["openalex_id"] = m.group(1)
    m = re.search(r"(\d{4}-\d{2}-\d{2})", block)
    if m:
        out["checked"] = m.group(1)
    return out


def signal_citation(doi: str, openalex_id: str, snapshot, fetch) -> dict:
    """被引实时查 OpenAlex(优先 DOI,无 DOI 用 OpenAlex id)，与快照对比，冲突信在线。"""
    if not doi and not openalex_id:
        return {"status": "unavailable", "reason": "无 doi / openalex_id 锚点",
                "cited_snapshot": snapshot}
    try:
        if doi:
            url = f"{OA}/works/doi:{urllib.parse.quote(doi)}?"
        else:
            url = f"{OA}/works/{openalex_id}?"
        url += _add_mailto({"select": "id,cited_by_count,publication_year"})
        data = fetch(url)
        live = data.get("cited_by_count")
        out = {"status": "ok", "cited_by_count_live": live,
               "cited_snapshot": snapshot,
               "publication_year": data.get("publication_year"),
               "source": f"OpenAlex {'doi:'+doi if doi else openalex_id}(实时)，冲突信在线"}
        if snapshot and live and snapshot > 0:
            ratio = abs(live - snapshot) / snapshot
            if ratio > 0.5:
                out["anomaly"] = (f"在线值({live})与快照({snapshot})差异>{int(ratio*100)}%，"
                                  "可能 OpenAlex 记录合并/拆分(arXiv vs 正式版)，人工核")
        return out
    except Exception as e:  # noqa: BLE001
        return {"status": "unavailable", "reason": f"OpenAlex 失败:{e.__class__.__name__}",
                "cited_snapshot": snapshot, "note": "降级用本地快照，标 stale"}


def assemble(card_block: str, doi: str, openalex_id: str, fetch) -> dict:
    anchors = parse_card_block(card_block) if card_block else {}
    use_doi = doi or anchors.get("doi", "")
    use_oa = openalex_id or anchors.get("openalex_id", "")
    snap = anchors.get("cited_snapshot")
    return {
        "anchors": anchors,
        "signals": {"citation": signal_citation(use_doi, use_oa, snap, fetch)},
        "freshness": {"local_checked": anchors.get("checked"),
                      "note": "无网回退被引快照并标 stale；冲突默认信在线；被引非载荷不阻断写作"},
    }


class _MockFetcher:
    def __call__(self, url: str) -> dict:
        if "/works/" in url:
            return {"id": "https://openalex.org/W2194775991",
                    "cited_by_count": 221500, "publication_year": 2016}
        raise RuntimeError(f"mock 未覆盖:{url}")


def _selftest() -> int:
    fetch = _MockFetcher()
    # samples_real 双行卡块
    block_real = ("- **被引数**：221,133（2026-06-06 OpenAlex 快照）\n"
                  "- **DOI**：10.1109/cvpr.2016.90 · **OpenAlex**：W2194775991 · domain_scope=cv-视觉")
    a = parse_card_block(block_real)
    assert a["doi"] == "10.1109/cvpr.2016.90", a
    assert a["cited_snapshot"] == 221133, a  # 千分位逗号已去
    assert a["openalex_id"] == "W2194775991", a
    assert a["checked"] == "2026-06-06", a
    rep = assemble(block_real, "", "", fetch)
    assert rep["signals"]["citation"]["status"] == "ok"
    assert rep["signals"]["citation"]["cited_by_count_live"] == 221500
    assert rep["signals"]["citation"]["cited_snapshot"] == 221133  # 信在线但留快照对比

    # samples_recent 单行卡块(被引：N)
    block_recent = ("- **venue**：NeurIPS 2024 · **被引**：34（2026-06-12 快照） · "
                    "**DOI**：10.52202/079017-2694 · domain_scope=cv-视觉")
    b = parse_card_block(block_recent)
    assert b["doi"] == "10.52202/079017-2694", b
    assert b["cited_snapshot"] == 34, b
    assert b["checked"] == "2026-06-12", b

    # 差异>50% 异常提示(快照 100 → 在线 221500)
    rep2 = assemble("- **被引数**：100 · **DOI**：10.1/x", "", "", fetch)
    assert "anomaly" in rep2["signals"]["citation"], rep2["signals"]["citation"]

    # 无锚点 → unavailable，不崩
    rep3 = assemble("- 无 DOI 无被引", "", "", fetch)
    assert rep3["signals"]["citation"]["status"] == "unavailable"

    # OpenAlex 失败 → 降级留快照
    def boom(url):
        raise urllib.error.URLError("offline")
    rep4 = assemble("- **被引数**：50 · **DOI**：10.2/y", "", "", boom)
    assert rep4["signals"]["citation"]["status"] == "unavailable"
    assert rep4["signals"]["citation"]["cited_snapshot"] == 50
    print("[selftest] PASS paper_signal（被引解析(千分位/两种行) + 冲突信在线 + 差异提示 + 降级）")
    return 0


def main() -> None:
    global _MAILTO
    ap = argparse.ArgumentParser(description="db02 写作样本卡被引实时校验")
    ap.add_argument("--doi", default="")
    ap.add_argument("--openalex-id", default="", help="W 开头的 OpenAlex Works id")
    ap.add_argument("--card-block", default="", help="一张卡的若干行(自动解析锚点)")
    ap.add_argument("--mailto", default="")
    ap.add_argument("--json-out", default="")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        sys.exit(_selftest())
    if args.mailto:
        _MAILTO = args.mailto.strip()
    if not args.doi and not args.openalex_id and not args.card_block:
        ap.error("至少提供 --doi/--openalex-id/--card-block 之一(或 --selftest)")
    report = assemble(args.card_block, args.doi, args.openalex_id, http_fetch)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json_out:
        open(args.json_out, "w", encoding="utf-8").write(text)
    print(text)


if __name__ == "__main__":
    main()
