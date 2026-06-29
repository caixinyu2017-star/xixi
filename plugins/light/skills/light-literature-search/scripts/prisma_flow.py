#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prisma_flow.py — 系统综述 PRISMA 2020 流程留痕与计数核对。

系统综述/Meta 分析的纳排过程必须可复现：每个库检索命中多少、去重去掉
多少、标题摘要筛掉多少、全文筛掉多少、最终纳入多少——这些数字要能勾稽
（前一阶段 - 排除 = 后一阶段），并产出 PRISMA 2020 流程图所需的结构化数据。

本脚本不替你做筛选判断（那是研究者的工作），它做两件机械但易错的事：
  ① 勾稽核对：各阶段计数是否自洽，排除数加总对不对，有没有"凭空消失/
     多出来"的记录——这种算术错误在综述里很常见且审稿人必查。
  ② 产出 PRISMA 流程图的结构化 JSON + 文字版流程，供 m09 绘图、m07 写作。

输入一个 counts JSON（见 --selftest 输出的样例），字段对齐 PRISMA 2020：
  identification（各库命中、其他来源）→ 去重 → screening（标题摘要筛）
  → eligibility（全文评估，按理由分类排除）→ included（最终纳入）。

诚实原则：脚本只核对你填的数字是否自洽，不核对筛选决定本身对不对；
检索式与纳排标准的合理性仍需研究者与领域判断。

用法：
  python prisma_flow.py --counts counts.json --out prisma.json
  python prisma_flow.py --selftest
"""
from __future__ import annotations

import argparse
import json
import sys


def reconcile(c: dict) -> dict:
    """核对各阶段计数勾稽关系，返回 {ok, errors, flow}。"""
    errors = []

    ident = c.get("identification", {})
    db_hits = ident.get("databases", {})  # {库名: 命中数}
    other = ident.get("other_sources", 0)  # 引文滚雪球/手检等
    total_identified = sum(db_hits.values()) + other

    dedup_removed = c.get("duplicates_removed", 0)
    after_dedup = total_identified - dedup_removed

    screen = c.get("screening", {})
    screened = screen.get("records_screened", after_dedup)
    screen_excluded = screen.get("excluded", 0)
    after_screen = screened - screen_excluded

    elig = c.get("eligibility", {})
    fulltext_assessed = elig.get("fulltext_assessed", after_screen)
    # 全文排除按理由分类：{理由: 数量}
    ft_excl_by_reason = elig.get("excluded_by_reason", {})
    ft_excluded = sum(ft_excl_by_reason.values())
    after_elig = fulltext_assessed - ft_excluded

    included = c.get("included", {}).get("studies", after_elig)

    # 勾稽断言
    def chk(cond, msg):
        if not cond:
            errors.append(msg)

    chk(screened == after_dedup,
        f"去重后应为 {after_dedup}，但 records_screened={screened} 对不上")
    chk(fulltext_assessed == after_screen,
        f"标题摘要筛后应为 {after_screen}，但 fulltext_assessed={fulltext_assessed} 对不上")
    chk(included == after_elig,
        f"全文排除后应为 {after_elig}，但 included.studies={included} 对不上")
    chk(after_dedup >= 0 and after_screen >= 0 and after_elig >= 0,
        "出现负数：某阶段排除数超过了进入该阶段的记录数")
    chk(included >= 0, "最终纳入数为负")

    flow = {
        "total_identified": total_identified,
        "from_databases": sum(db_hits.values()),
        "from_other_sources": other,
        "duplicates_removed": dedup_removed,
        "records_screened": after_dedup,
        "records_excluded_screening": screen_excluded,
        "fulltext_assessed": after_screen,
        "fulltext_excluded": ft_excluded,
        "fulltext_excluded_by_reason": ft_excl_by_reason,
        "studies_included": included,
    }
    return {"ok": len(errors) == 0, "errors": errors, "flow": flow}


def render_text(flow: dict) -> str:
    lines = [
        "PRISMA 2020 流程（识别 → 筛选 → 纳入）",
        f"  识别：数据库 {flow['from_databases']} + 其他来源 {flow['from_other_sources']} = {flow['total_identified']}",
        f"  去重：移除 {flow['duplicates_removed']} → 待筛 {flow['records_screened']}",
        f"  标题摘要筛选：排除 {flow['records_excluded_screening']} → 全文评估 {flow['fulltext_assessed']}",
        f"  全文评估：排除 {flow['fulltext_excluded']}",
    ]
    for reason, n in flow.get("fulltext_excluded_by_reason", {}).items():
        lines.append(f"      - {reason}: {n}")
    lines.append(f"  最终纳入研究：{flow['studies_included']}")
    return "\n".join(lines)


def selftest() -> int:
    sample = {
        "identification": {
            "databases": {"PubMed": 420, "Web of Science": 310, "中国知网": 150},
            "other_sources": 12,
        },
        "duplicates_removed": 180,
        "screening": {"records_screened": 712, "excluded": 600},
        "eligibility": {
            "fulltext_assessed": 112,
            "excluded_by_reason": {"非随机对照": 40, "结局指标不符": 25, "全文不可得": 7},
        },
        "included": {"studies": 40},
    }
    r = reconcile(sample)
    print(render_text(r["flow"]))
    print("[reconcile]", "OK 计数自洽" if r["ok"] else f"FAIL: {r['errors']}")

    # 反例：故意填错一个数，应被抓出
    bad = json.loads(json.dumps(sample))
    bad["included"]["studies"] = 45  # 应为 40
    r2 = reconcile(bad)
    caught = not r2["ok"]
    print("[反例检测]", "OK 抓出了不勾稽的计数" if caught else "FAIL 没抓出错误")
    return 0 if (r["ok"] and caught) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="PRISMA 2020 流程留痕与计数核对")
    ap.add_argument("--counts", help="计数 JSON 路径")
    ap.add_argument("--out", help="输出结构化流程 JSON 路径")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not args.counts:
        ap.error("需要 --counts 或 --selftest")
        return 2

    with open(args.counts, encoding="utf-8") as f:
        counts = json.load(f)
    r = reconcile(counts)
    print(render_text(r["flow"]))
    if not r["ok"]:
        print("\n[计数不勾稽，必须修正]", file=sys.stderr)
        for e in r["errors"]:
            print("  -", e, file=sys.stderr)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(r, f, ensure_ascii=False, indent=2)
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
