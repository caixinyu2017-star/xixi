#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rank_ideas.py — 候选 idea **分层组合裁定**（m03 内部 triage，突破口不被性价比压杀）。

【为什么不是单一性价比榜】impact/effort 性价比天然惩罚高 effort——而突破型 idea（moonshot）
几乎必然高 effort/低当前可行性，用性价比排会把它系统性压到稳妥项后面，与 SKILL "产出高风险高
回报/稳妥/保底分层、按潜力排序" 直接矛盾。本脚本改为**分层组合裁定**：先把候选分到三道，每道
用各自合理的排序键，再 round-robin 组合 shortlist——让突破口在自己的赛道里竞争，不和保底项在
同一根轴上 PK。这是 m03 内部 triage，不替代 m04 八维严审，只决定"送哪几个、按什么结构送"。

三道（确定性规则，先判 moonshot 再判 safe，避免"又稳又突破"被埋进保底道）：
  - moonshot 冲刺/高风险高回报：impact≥4 且 (novelty≥4 或 effort≥4)。道内按 影响→新颖→工作量→id。
  - safe 保底：feasibility≥4 且 effort≤2（几乎稳出结果）。道内按 可行→工作量→影响→id。
  - solid 稳妥：其余均衡项。道内按 性价比(impact/effort)→影响→工作量→id（此处性价比才合理）。

输入：JSON 数组，每条 {id, title, impact(1-5), effort(1-5), novelty?(默认3), feasibility?(默认3)}。
输出：三道分层榜 + round-robin 组合 shortlist（默认每轮 moonshot→solid→safe 各取一，凑 SKILL 的
分层产出）+ 每条 lane 与潜力分(impact+novelty)。

诚实：impact/effort/novelty/feasibility 都是**主观快评**，本脚本只按声明值做**确定性分层与排序**，
不判 idea 真实价值（那靠 m04），更不产生 idea（那靠人 + 底座模型）。分数从哪来要人填，垃圾进垃圾出。

用法：
  python rank_ideas.py --in candidates.json --top-k 6
  python rank_ideas.py --selftest
"""
from __future__ import annotations
import argparse
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

LANES = ["moonshot", "solid", "safe"]
_LANE_CN = {"moonshot": "冲刺(高风险高回报)", "solid": "稳妥", "safe": "保底"}


def _lane(imp: float, eff: float, nov: float, fea: float) -> str:
    """确定性分道。先判 moonshot：高影响 + (高新颖 或 高代价) 即突破口候选，
    不让"又新又稳"的 idea 被埋进保底道浪费。"""
    if imp >= 4 and (nov >= 4 or eff >= 4):
        return "moonshot"
    if fea >= 4 and eff <= 2:
        return "safe"
    return "solid"


def _lane_sort_key(lane: str):
    """每道各自合理的排序键（返回 lambda）。"""
    if lane == "moonshot":  # 回报与新颖优先，同等下工作量小的先
        return lambda r: (-r["impact"], -r["novelty"], r["effort"], str(r["id"]))
    if lane == "safe":      # 稳出优先：可行高、工作量小
        return lambda r: (-r["feasibility"], r["effort"], -r["impact"], str(r["id"]))
    return lambda r: (-r["value_ratio"], -r["impact"], r["effort"], str(r["id"]))  # solid 性价比合理


def rank(items: list, top_k: int = 0) -> dict:
    rows = []
    for it in items:
        imp = float(it.get("impact", 0) or 0)
        eff = float(it.get("effort", 0) or 0)
        nov = float(it.get("novelty", 3) or 3)
        fea = float(it.get("feasibility", 3) or 3)
        ratio = round(imp / eff, 3) if eff > 0 else (imp if imp else 0.0)
        rows.append({
            "id": it.get("id", "?"), "title": it.get("title", ""),
            "impact": imp, "effort": eff, "novelty": nov, "feasibility": fea,
            "value_ratio": ratio, "potential": round(imp + nov, 1),
            "lane": _lane(imp, eff, nov, fea),
        })
    # 分道 + 道内排序
    lanes = {ln: sorted([r for r in rows if r["lane"] == ln], key=_lane_sort_key(ln))
             for ln in LANES}
    # round-robin 组合：每轮 moonshot→solid→safe 各取一，保证三层都有代表（不压杀突破口）
    shortlist, depth = [], 0
    maxd = max((len(v) for v in lanes.values()), default=0)
    while depth < maxd and (not top_k or len(shortlist) < top_k):
        for ln in LANES:
            if depth < len(lanes[ln]) and (not top_k or len(shortlist) < top_k):
                shortlist.append(lanes[ln][depth])
        depth += 1
    # 完整展示榜：按道顺序平铺（道内已排序）
    ranked = [r for ln in LANES for r in lanes[ln]]
    return {"n": len(rows), "top_k": top_k,
            "lane_counts": {ln: len(lanes[ln]) for ln in LANES},
            "lanes": lanes, "ranked": ranked, "shortlist": shortlist,
            "note": ("分层组合裁定：moonshot/solid/safe 各赛道独立排序再 round-robin 组合，"
                     "突破口(高影响高代价)不被性价比压杀；这是 m03 内部 triage，不替代 m04 八维严审。"
                     "分数为主观快评，垃圾进垃圾出。")}


def render(res: dict) -> str:
    lc = res["lane_counts"]
    lines = [f"# 候选 idea 分层组合裁定（m03 triage，共 {res['n']} 条）", "",
             f"分道：冲刺 {lc['moonshot']} · 稳妥 {lc['solid']} · 保底 {lc['safe']}", ""]
    for ln in LANES:
        rows = res["lanes"][ln]
        if not rows:
            continue
        lines += [f"## {_LANE_CN[ln]}（{ln}，{len(rows)} 条）",
                  "| 道内序 | id | 标题 | 影响 | 工作量 | 新颖 | 可行 | 潜力(影响+新颖) |",
                  "|---|---|---|---|---|---|---|---|"]
        for i, r in enumerate(rows, 1):
            lines.append(f"| {i} | {r['id']} | {(r['title'] or '')[:36]} | {r['impact']:.0f} | "
                         f"{r['effort']:.0f} | {r['novelty']:.0f} | {r['feasibility']:.0f} | {r['potential']} |")
        lines.append("")
    sl = res["shortlist"]
    lines += [f"## round-robin 组合 shortlist（{len(sl)} 条，三层交替取，送 m04）",
              "| 送审序 | id | 道 | 标题 | 潜力 |", "|---|---|---|---|---|"]
    for i, r in enumerate(sl, 1):
        lines.append(f"| {i} | {r['id']} | {_LANE_CN[r['lane']]} | {(r['title'] or '')[:36]} | {r['potential']} |")
    lines += ["", f"> {res['note']}"]
    return "\n".join(lines)


def _selftest() -> int:
    print("### rank_ideas 离线自测", file=sys.stderr)
    items = [
        # 突破口：高影响高新颖但高工作量——旧性价比逻辑会把它压到稳妥项后
        {"id": "M-01", "title": "颠覆性新机制", "impact": 5, "effort": 5, "novelty": 5, "feasibility": 2},
        # 稳妥均衡
        {"id": "S-01", "title": "中规中矩增量", "impact": 3, "effort": 3, "novelty": 3, "feasibility": 3},
        # 保底：可行高、工作量小
        {"id": "B-01", "title": "稳出保底", "impact": 2, "effort": 1, "novelty": 2, "feasibility": 5},
        # 又一个 moonshot：高影响高工作量
        {"id": "M-02", "title": "高风险高回报", "impact": 5, "effort": 4, "novelty": 4, "feasibility": 2},
    ]
    res = rank(items, top_k=6)
    # 分道正确
    assert res["lanes"]["moonshot"] and {r["id"] for r in res["lanes"]["moonshot"]} == {"M-01", "M-02"}, res["lane_counts"]
    assert any(r["id"] == "B-01" for r in res["lanes"]["safe"]), res["lanes"]["safe"]
    assert any(r["id"] == "S-01" for r in res["lanes"]["solid"]), res["lanes"]["solid"]
    # 核心诉求：突破口 M-01 进 shortlist 且排在保底 B-01 之前（不被压杀）
    sl_ids = [r["id"] for r in res["shortlist"]]
    assert "M-01" in sl_ids, sl_ids
    assert sl_ids.index("M-01") < sl_ids.index("B-01"), f"突破口被保底压杀: {sl_ids}"
    # round-robin：第一个就是 moonshot（突破口领跑，而非按性价比让保底领跑）
    assert res["shortlist"][0]["lane"] == "moonshot", sl_ids
    # moonshot 道内 M-01(影响5) 在 M-02(影响5) 前——同影响按新颖 5>4
    m_order = [r["id"] for r in res["lanes"]["moonshot"]]
    assert m_order == ["M-01", "M-02"], m_order
    # 潜力分 = impact + novelty
    assert next(r for r in res["ranked"] if r["id"] == "M-01")["potential"] == 10.0
    # top_k 截断
    assert len(rank(items, top_k=2)["shortlist"]) == 2
    # effort=0 / 缺省 novelty,feasibility 不崩
    rank([{"id": "x", "impact": 3, "effort": 0}])
    # 渲染含三道与组合
    md = render(res)
    assert "冲刺" in md and "round-robin" in md and "潜力" in md, md
    print("[selftest] PASS rank_ideas offline")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="候选 idea 分层组合裁定（m03 内部 triage）")
    ap.add_argument("--in", dest="infile", help="候选 JSON 数组")
    ap.add_argument("--top-k", type=int, default=0)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest or not args.infile:
        return _selftest()
    with open(args.infile, encoding="utf-8") as f:
        items = json.load(f)
    res = rank(items, args.top_k)
    print(json.dumps(res, ensure_ascii=False, indent=2) if args.json else render(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
