#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pipeline.py — 文献调研端到端编排（串起本目录 5 个脚本，减少 agent 每次手拼）。

把 检索→相关度过滤→滚雪球→去重→(可选)PRISMA 勾稽→引用核验→落盘 literature_review 骨架
串成一条龙。**不重复实现各步**，只按顺序调用已有脚本的可复用函数：
  search_normalize.run() → snowball.snowball() → verify_citations.verify_batch()
  → prisma_flow.reconcile()（系统综述时）→ 汇总成 docs/literature_review.md 骨架。

每步沿用各脚本自身的诚实纪律（[OFFLINE] 回退、被引标来源、不臆造、留痕）。本编排器只做
"流程串联 + 产物汇总"，不改各步判定。无网络时各步自动走 [OFFLINE] 合成样本，整条管线仍可跑通。

用法：
  python pipeline.py "dairy goat behavior" --require-terms goat --per-page 20
  python pipeline.py "..." --seed 10.1016/j.compag.2021.100001 --snowball  # 带滚雪球
  python pipeline.py --selftest
"""
from __future__ import annotations
import argparse
import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# 复用同目录脚本（加入 sys.path 以便直接 import）
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import search_normalize as sn
import snowball as sb
import verify_citations as vc
import prisma_flow as pf


def run_pipeline(query: str, *, per_page: int = 10, max_results: int = 0,
                 require_terms=None, exclude_terms=None, min_score: float = 0.0,
                 seed: str = "", do_snowball: bool = False,
                 prisma_counts: dict | None = None,
                 offline: bool = False) -> dict:
    """串联执行，返回各步结果 + 汇总。每步独立可降级。"""
    steps = {}

    # 1) 检索 + 相关度过滤
    search = sn.run(query, per_page=per_page, offline_sample=offline,
                    require_terms=require_terms, exclude_terms=exclude_terms,
                    min_score=min_score, max_results=max_results)
    steps["search"] = {"merged_count": search.get("merged_count"),
                       "dropped_count": search.get("dropped_count", 0),
                       "offline": search.get("offline")}
    records = search.get("records", [])

    # 2) 滚雪球（可选，从种子或检索首条做）
    snow = None
    if do_snowball:
        s = seed or (records[0].get("doi") if records else "")
        if s:
            snow = sb.snowball(s, hops=1, offline_sample=offline)
            steps["snowball"] = {"seed": s, "merged": snow.get("merged_count"),
                                 "offline": snow.get("offline")}
        else:
            steps["snowball"] = {"skipped": "无可用种子（检索为空且未给 --seed）"}

    # 3) 引用核验（对检索到的有 DOI 条目）
    claims = [{"doi": r.get("doi"), "title": r.get("title"), "year": r.get("year")}
              for r in records if r.get("doi")]
    verify = vc.verify_batch(claims) if claims else {"total": 0, "summary": {}, "results": []}
    steps["verify"] = {"total": verify["total"], "summary": verify["summary"]}

    # 4) PRISMA 勾稽（仅系统综述：给了各阶段计数才做）
    prisma = None
    if prisma_counts:
        prisma = pf.reconcile(prisma_counts)
        steps["prisma"] = {"ok": prisma.get("ok"),
                           "errors": prisma.get("errors", [])}

    return {"query": query, "records": records, "search": search,
            "snowball": snow, "verify": verify, "prisma": prisma, "steps": steps}


def to_review_skeleton(result: dict) -> str:
    """汇总成 docs/literature_review.md 骨架（文献表 + 核验摘要 + 待人工补的脉络/gap 占位）。"""
    recs = result["records"]
    lines = [f"# 文献综述骨架：{result['query']}", "",
             "> 由 pipeline.py 串联检索→过滤→滚雪球→核验自动生成的**骨架**；"
             "研究脉络/方法族/优缺点/gap 需人工据文献填。被引数标来源库不可跨库比。", ""]
    s = result["steps"]
    lines.append(f"**管线摘要**：检索去重后 {s['search']['merged_count']} 条"
                 f"（相关度剔 {s['search'].get('dropped_count', 0)} 条）"
                 f"{'｜[OFFLINE 合成样本]' if s['search'].get('offline') else ''}；"
                 f"引用核验 {s['verify']['total']} 条 {s['verify']['summary']}。")
    if result.get("snowball"):
        lines.append(f"**滚雪球**：种子 {s['snowball'].get('seed','')} → 邻居 {s['snowball'].get('merged','?')} 条。")
    if result.get("prisma"):
        ok = s["prisma"]["ok"]
        lines.append(f"**PRISMA 勾稽**：{'✅ 计数自洽' if ok else '❌ 计数不自洽：'+str(s['prisma']['errors'])}")
    lines += ["", "## 文献表（按被引降序，标来源库）", "",
              "| # | 标题 | 年 | venue | 被引(来源) | 相关度 | DOI |",
              "|---|------|----|-------|-----------|--------|-----|"]
    for i, r in enumerate(recs, 1):
        cb = r.get("cited_by")
        lines.append(f"| {i} | {(r.get('title') or '')[:70].replace('|','/')} | "
                     f"{r.get('year') or ''} | {(r.get('venue') or '')[:25]} | "
                     f"{cb}({r.get('cited_by_src','?')}) | {r.get('relevance_score','-')} | "
                     f"{r.get('doi') or ''} |")
    lines += ["", "## 研究脉络（人工填）", "_问题怎么提出→怎么被解决→还剩什么_", "",
              "## 代表方法卡（人工填，字段对齐 db03）", "",
              "## 优缺点对比（人工填）", "",
              "## 空白与机会 gap（人工填，喂 m03）", ""]
    return "\n".join(lines)


def _selftest() -> int:
    print("### pipeline 离线自测", file=sys.stderr)
    # 全 offline 串一遍：检索(合成)+滚雪球(合成)+核验+PRISMA 勾稽
    counts = {
        "identification": {"databases": {"openalex": 100, "crossref": 80}, "other_sources": 20},
        "duplicates_removed": 50,
        "screening": {"records_screened": 150, "excluded": 100},
        "eligibility": {"fulltext_assessed": 50, "excluded_by_reason": {"无对照": 20, "非英文": 10}},
        "included": {"studies": 20},
    }
    res = run_pipeline("dairy goat behavior", per_page=5, require_terms=["goat"],
                       do_snowball=True, prisma_counts=counts, offline=True)
    # 各步都跑了
    assert res["steps"]["search"]["offline"] is True, res["steps"]
    assert "snowball" in res["steps"], res["steps"]
    assert res["steps"]["verify"]["total"] >= 1, res["steps"]
    assert res["steps"]["prisma"]["ok"] is True, res["steps"]["prisma"]
    # require-terms 生效：留下的都含 goat
    assert all("goat" in ((r.get("title") or "")+(r.get("abstract") or "")).lower()
               for r in res["records"]), res["records"]
    # 骨架产出含文献表 + 人工填占位
    md = to_review_skeleton(res)
    assert "文献表" in md and "空白与机会" in md and "PRISMA 勾稽" in md, md
    # PRISMA 不自洽时如实报错
    bad = dict(counts, included={"studies": 999})
    res2 = run_pipeline("x", offline=True, prisma_counts=bad)
    assert res2["steps"]["prisma"]["ok"] is False, res2["steps"]["prisma"]
    print("[selftest] PASS pipeline offline")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="文献调研端到端编排（串 5 脚本）")
    ap.add_argument("query", nargs="?", default="dairy goat behavior")
    ap.add_argument("--per-page", type=int, default=10)
    ap.add_argument("--max-results", type=int, default=0)
    ap.add_argument("--require-terms", default="")
    ap.add_argument("--exclude-terms", default="")
    ap.add_argument("--min-score", type=float, default=0.0)
    ap.add_argument("--seed", default="", help="滚雪球种子 DOI/workid（不给则用检索首条）")
    ap.add_argument("--snowball", action="store_true", help="启用滚雪球步骤")
    ap.add_argument("--offline", action="store_true", help="强制各步走合成样本")
    ap.add_argument("--out", default="", help="literature_review 骨架输出路径")
    ap.add_argument("--json-out", default="")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return _selftest()

    req = [t.strip() for t in args.require_terms.split(",") if t.strip()]
    exc = [t.strip() for t in args.exclude_terms.split(",") if t.strip()]
    res = run_pipeline(args.query, per_page=args.per_page, max_results=args.max_results,
                       require_terms=req, exclude_terms=exc, min_score=args.min_score,
                       seed=args.seed, do_snowball=args.snowball, offline=args.offline)
    md = to_review_skeleton(res)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"骨架已写入 {args.out}", file=sys.stderr)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2, default=str)
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
