#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""novelty_audit.py — idea 新颖性检索证否的四阶段结构化留痕 + 一致性勾稽。

借 OpenNovelty 的"检索证否 pipeline"思路，把 idea-critique Step 2 散在文字里的检索证否
固化为**可复现、可核对**的四阶段结构化产物（类比 prisma_flow 对 PRISMA 计数的勾稽）：

  阶段1 抽论断（claims）：把 idea 的核心新颖性主张拆成可检验的原子论断
  阶段2 检索证据（evidence）：每个论断在哪些库检索、HTTP 码、最像的命中（DOI/标题/年）
  阶段3 逐条对比（collision）：每个命中判撞车等级 same/extension/unrelated + 量化 delta
  阶段4 novelty 判定（verdict）：综合给每个论断的 novelty 档 + 整体结论

**本脚本不做检索本身**（检索由 m01 literature-search 的 search_normalize/snowball 等脚本或
agent 完成）；它做的是把检索证否过程**结构化记录**并**勾稽自相矛盾**——这正是审稿人最爱抓、
也最容易被跳过的环节。核心勾稽（抓"嘴上说新、证据打脸"）：
  - 论断声称 novel 但其 collision 里有 same（核心实质等价）→ 矛盾，应触发 NOVELTY-OVERCLAIM
  - 论断有 same 撞车却没标 block → 漏判（idea-critique 撞车 same→创新性<45 block）
  - 论断无任何检索证据（evidence 空）却给了 novelty 档 → evidence-missing，档位不可成立

⚠ 诚实：只勾稽"记录是否自洽/证据是否支撑结论"，不替你判断 idea 到底新不新（那要真检索+人判）。
输入是你/agent 检索后填的结构化 JSON，垃圾进垃圾出——脚本只保证"结论不与自己的证据打架"。

用法：
  python novelty_audit.py --in audit.json
  python novelty_audit.py --selftest        # 离线合成数据自测（含矛盾检测）
"""
from __future__ import annotations
import argparse
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

COLLISION_LEVELS = ("same", "extension", "unrelated")
# same=核心实质等价(同现象/方法/结论) extension=前作做过但有实质扩展 unrelated=无关/阴性
NOVELTY_TIERS = ("novel", "incremental", "overlap", "evidence-missing")


def _audit_claim(claim: dict) -> dict:
    """对单条论断做一致性勾稽，返回 {flags:[...], derived_*}。"""
    flags = []
    cid = claim.get("id", "?")
    evidence = claim.get("evidence", []) or []
    collisions = claim.get("collisions", []) or []
    declared = (claim.get("declared_novelty") or "").strip().lower()

    # 检索覆盖：用了几个库、有没有 HTTP 200
    libs = {e.get("source") for e in evidence if e.get("source")}
    ok_hits = [e for e in evidence if e.get("http") == 200]
    has_evidence = len(ok_hits) > 0

    levels = [c.get("level") for c in collisions]
    has_same = "same" in levels
    has_ext = "extension" in levels

    # 勾稽1：声称 novel 但有 same 命中 → 过度宣称
    if declared == "novel" and has_same:
        flags.append({"code": "NOVELTY-OVERCLAIM", "severity": "high",
                      "msg": f"论断{cid}声称 novel，但 collision 有 same（核心实质等价）——过度宣称，"
                             f"创新性应 <45 触发 block"})
    # 勾稽2：有 same 撞车 → 必须 block（idea-critique 规则）
    if has_same:
        flags.append({"code": "COLLISION-SAME-BLOCK", "severity": "high",
                      "msg": f"论断{cid}存在 same 撞车 → 触发创新性<45 block、判不通过（rubric 否决项）"})
    # 勾稽3：无检索证据却给了非 evidence-missing 档 → 档位不成立
    if not has_evidence and declared in ("novel", "incremental"):
        flags.append({"code": "EVIDENCE-MISSING", "severity": "high",
                      "msg": f"论断{cid}无 HTTP 200 检索证据却标 {declared}——创新性维度应封顶并标 evidence-missing"})
    # 勾稽4：单库检索（<2 库）→ 覆盖不足警告（idea-critique 要求至少 2 库交叉）
    if has_evidence and len(libs) < 2:
        flags.append({"code": "SINGLE-SOURCE", "severity": "warn",
                      "msg": f"论断{cid}仅 {libs or '0'} 单库检索 < 2 库——可能高估新颖性，补检索交叉验证"})
    # 勾稽5：extension 但未记 delta → 增量没说清
    for c in collisions:
        if c.get("level") == "extension" and not (c.get("delta") or "").strip():
            flags.append({"code": "DELTA-MISSING", "severity": "warn",
                          "msg": f"论断{cid}对 {c.get('ref','?')} 判 extension 却未写量化 delta——增量贡献须说清"})

    # 推导 novelty 档（按证据，覆盖 declared 若矛盾）
    if not has_evidence:
        derived = "evidence-missing"
    elif has_same:
        derived = "overlap"
    elif has_ext:
        derived = "incremental"
    else:
        derived = "novel"

    return {"id": cid, "declared": declared or None, "derived_novelty": derived,
            "libs": sorted(libs), "n_ok_hits": len(ok_hits),
            "has_same": has_same, "flags": flags}


def audit(data: dict) -> dict:
    """对整份四阶段 novelty 留痕做勾稽，汇总 flags 与整体结论。"""
    claims = data.get("claims", []) or []
    if not claims:
        return {"error": "无 claims（阶段1 抽论断为空）——先把 idea 核心新颖主张拆成原子论断",
                "n_claims": 0}
    rows = [_audit_claim(c) for c in claims]
    all_flags = [f for r in rows for f in r["flags"]]
    high = [f for f in all_flags if f["severity"] == "high"]
    has_overclaim = any(f["code"] == "NOVELTY-OVERCLAIM" for f in all_flags)
    has_block = any(f["code"] == "COLLISION-SAME-BLOCK" for f in all_flags)
    has_evmiss = any(f["code"] == "EVIDENCE-MISSING" for f in all_flags)

    # 整体 novelty：任一 same→overlap；否则任一 evidence-missing→evidence-missing；
    # 否则任一 incremental→incremental；全 novel→novel
    derived = [r["derived_novelty"] for r in rows]
    if "overlap" in derived:
        overall = "overlap"
    elif "evidence-missing" in derived:
        overall = "evidence-missing"
    elif "incremental" in derived:
        overall = "incremental"
    else:
        overall = "novel"

    return {
        "n_claims": len(claims),
        "claims": rows,
        "overall_novelty": overall,
        "high_flag_count": len(high),
        "verdict_hooks": {  # 喂回 idea-critique Step 6 否决项
            "trigger_novelty_overclaim": has_overclaim,
            "trigger_originality_block": has_block,   # same 撞车→创新性<45 block
            "trigger_evidence_missing_cap": has_evmiss,
        },
        "flags": all_flags,
        "note": ("只勾稽'结论是否与自己的检索证据自洽'，不替你判 idea 真新不新（须真检索+人判）。"
                 "same 撞车→创新性<45 block；overclaim/evidence-missing 喂回 Step6 否决项。"),
    }


def to_markdown(rep: dict) -> str:
    if rep.get("error"):
        return f"# Novelty 证否审计\n\n{rep['error']}"
    lines = [f"# Novelty 证否审计 — {rep['n_claims']} 条论断｜整体={rep['overall_novelty']}"
             f"｜high flags={rep['high_flag_count']}\n",
             "| 论断 | 声称 | 据证推导 | 库数 | same撞车 | flags |",
             "|---|---|---|---|---|---|"]
    for r in rep["claims"]:
        lines.append("| %s | %s | %s | %d | %s | %s |" % (
            r["id"], r["declared"] or "—", r["derived_novelty"], len(r["libs"]),
            "是" if r["has_same"] else "否",
            ";".join(f["code"] for f in r["flags"]) or "—"))
    hooks = rep["verdict_hooks"]
    lines.append(f"\n**喂回 Step6 否决项**：overclaim={hooks['trigger_novelty_overclaim']} "
                 f"originality-block={hooks['trigger_originality_block']} "
                 f"evidence-missing={hooks['trigger_evidence_missing_cap']}")
    if rep["flags"]:
        lines.append("\n**全部 flags：**")
        lines += [f"- [{f['severity']}] {f['code']}: {f['msg']}" for f in rep["flags"]]
    lines.append(f"\n> {rep['note']}")
    return "\n".join(lines)


def _selftest() -> int:
    print("### novelty_audit 离线自测", file=sys.stderr)

    # 论断A：声称 novel 但有 same 撞车 → 应触发 OVERCLAIM + BLOCK，推导 overlap
    # 论断B：extension 但缺 delta + 单库 → warn
    # 论断C：无检索证据却标 novel → EVIDENCE-MISSING
    data = {"claims": [
        {"id": "A", "declared_novelty": "novel",
         "evidence": [{"source": "openalex", "http": 200, "hit": "10.x/a"},
                      {"source": "s2", "http": 200, "hit": "10.x/a"}],
         "collisions": [{"ref": "Smith2023", "level": "same"}]},
        {"id": "B", "declared_novelty": "incremental",
         "evidence": [{"source": "openalex", "http": 200, "hit": "10.x/b"}],
         "collisions": [{"ref": "Lee2022", "level": "extension", "delta": ""}]},
        {"id": "C", "declared_novelty": "novel",
         "evidence": [], "collisions": []},
    ]}
    rep = audit(data)
    print(to_markdown(rep), file=sys.stderr)

    codes = {f["code"] for f in rep["flags"]}
    assert "NOVELTY-OVERCLAIM" in codes, codes      # A
    assert "COLLISION-SAME-BLOCK" in codes, codes   # A
    assert "DELTA-MISSING" in codes, codes          # B
    assert "SINGLE-SOURCE" in codes, codes          # B 单库
    assert "EVIDENCE-MISSING" in codes, codes       # C
    # 整体：有 same → overlap
    assert rep["overall_novelty"] == "overlap", rep["overall_novelty"]
    # verdict hooks
    h = rep["verdict_hooks"]
    assert h["trigger_novelty_overclaim"] and h["trigger_originality_block"], h
    assert h["trigger_evidence_missing_cap"], h
    # A 论断据证推导应覆盖声称：declared novel 但 derived overlap
    a = next(r for r in rep["claims"] if r["id"] == "A")
    assert a["declared"] == "novel" and a["derived_novelty"] == "overlap", a

    # 干净论断：2 库 + unrelated → novel，无 high flag
    clean = {"claims": [{"id": "X", "declared_novelty": "novel",
             "evidence": [{"source": "openalex", "http": 200}, {"source": "arxiv", "http": 200}],
             "collisions": [{"ref": "r", "level": "unrelated"}]}]}
    rc = audit(clean)
    assert rc["overall_novelty"] == "novel" and rc["high_flag_count"] == 0, rc

    # 空 claims 不崩
    assert audit({"claims": []}).get("n_claims") == 0
    print("[selftest] PASS novelty_audit offline")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="idea 新颖性检索证否四阶段留痕 + 一致性勾稽")
    ap.add_argument("--in", dest="infile", help="四阶段结构化 JSON 路径")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--selftest", action="store_true", help="run offline synthetic self-test")
    args = ap.parse_args()

    if args.selftest or not args.infile:
        return _selftest()
    with open(args.infile, encoding="utf-8") as f:
        data = json.load(f)
    rep = audit(data)
    print(json.dumps(rep, ensure_ascii=False, indent=2) if args.json else to_markdown(rep))
    return 0


if __name__ == "__main__":
    sys.exit(main())
