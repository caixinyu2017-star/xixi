#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cross_domain_search.py — 跨领域正交双轴检索（应用轴 × 方法轴）。

解决科研真实痛点：窄应用领域近三年好文稀少，但**真正的创新常来自跨领域嫁接**
——把别的领域的最前沿方法（目标检测/扩散模型/Transformer SOTA）迁移到你的应用
（病理识别/奶山羊行为/卫星图分析）。例：用 CV 最新目标检测做病理识别。

为什么不能简单拼词检索（实测依据）：
  把"应用词+方法词"拼成一个 query + 纯被引排序，会顶出蹭词的通用高被引文
  （实测搜 "deep learning livestock behaviour" 顶出 IPCC 气候报告/Lancet）。
  正确做法是**两轴正交分别检索、分别排序**，再把方法轴的前沿摆到应用研究者面前
  做迁移决策——“哪个方法能迁到我的应用”是研究者的判断，脚本只负责把候选找全找新，
  不替用户臆断可迁移性（诚实边界）。

本脚本复用 search_normalize 的检索/排序/去重函数，不重复实现：
  - 应用轴：相关度排序，允许经典（建立领域 baseline 与评测惯例）。
  - 方法轴：相关度排序 + 强时效（--recency-boost 默认开），抓最新 SOTA。
  - 输出双栏文献表 + 一段“迁移提示”：方法轴每条标“来自 <方法领域>，考虑迁移到 <你的应用>”。

诚实约定（见 d:/skill/Light/CONVENTIONS.md）：
- 不臆造可迁移性结论；只把候选找全找新，迁移判断交研究者（喂 m03 idea-generation）。
- 复用 search_normalize 的 [OFFLINE] 回退；无网络两轴都走合成样本，管线仍可验证。
- 被引数标来源库不跨库比；当前年份经 --current-year 显式传入（不依赖系统时钟，保可复现）。

用法：
  python cross_domain_search.py --application "dairy goat behaviour" \
      --method "YOLO real-time object detection" --current-year 2026
  python cross_domain_search.py --selftest
"""
from __future__ import annotations
import argparse
import json
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import search_normalize as sn


def cross_domain(application: str, method: str, *, per_page: int = 8,
                 current_year: int = 0, half_life: int = 3,
                 offline: bool = False) -> dict:
    """两轴正交检索：应用轴(允许经典) + 方法轴(强时效抓 SOTA)。返回双轴结果 + 迁移提示。"""
    # 应用轴：相关度排序，不强制时效（领域 baseline/评测惯例值得看经典）
    app = sn.run(application, per_page=per_page, offline_sample=offline,
                 sort_by="relevance")
    # 方法轴：相关度排序 + 强时效（要最新 SOTA），半衰期更短（默认 3 年，比主脚本 4 更激进）
    meth = sn.run(method, per_page=per_page, offline_sample=offline,
                  sort_by="relevance", recency_boost=bool(current_year),
                  current_year=current_year, half_life=half_life)
    transfer_hints = [
        {"method_title": r.get("title"), "method_year": r.get("year"),
         "doi": r.get("doi"),
         "hint": f"方法来自检索式「{method}」，考虑迁移到应用「{application}」——"
                 "可迁移性需研究者据方法假设/数据形态判断（喂 m03）。"}
        for r in (meth.get("records") or [])[:per_page]
    ]
    return {"application_query": application, "method_query": method,
            "current_year": current_year,
            "application": app, "method": meth,
            "transfer_hints": transfer_hints,
            "offline": app.get("offline") or meth.get("offline")}


def to_markdown(result: dict) -> str:
    app_recs = result["application"].get("records", [])
    meth_recs = result["method"].get("records", [])
    lines = [f"# 跨领域正交检索：应用「{result['application_query']}」 × 方法「{result['method_query']}」",
             "",
             "> 两轴**分别检索分别排序**（不拼词，避免跨领域拼词顶出通用高被引跑题文）。"
             "方法轴强时效抓 SOTA，应用轴允许经典建 baseline。"
             "**可迁移性由研究者判断，本表只把候选找全找新**。被引标来源库不跨库比。",
             "",
             "## 应用轴（你的领域：建 baseline / 评测惯例 / 数据形态）", ""]
    lines += _table(app_recs)
    lines += ["", "## 方法轴（别的领域的前沿技术：可迁移的方法库，强时效）", ""]
    lines += _table(meth_recs)
    lines += ["", "## 迁移提示（喂 m03 idea-generation 做嫁接）", "",
              "> 每条方法轴前沿 → 你的应用的潜在嫁接点；可迁移性需据“方法核心假设是否在你的数据/任务成立”判断。", ""]
    for i, h in enumerate(result.get("transfer_hints", []), 1):
        lines.append(f"{i}. **{(h.get('method_title') or '')[:70]}**（{h.get('method_year') or '?'}）"
                     f" → 迁移到「{result['application_query']}」？ DOI={h.get('doi') or 'NA'}")
    return "\n".join(lines)


def _table(records: list) -> list:
    out = ["| # | 标题 | 年 | venue | 被引(来源) | DOI |",
           "|---|------|----|-------|-----------|-----|"]
    for i, r in enumerate(records, 1):
        cb = "; ".join(f"{v}({k})" for k, v in r.get("cited_by_by_src", {}).items()) or "NA"
        title = (r.get("title") or "").replace("|", "/")[:70]
        out.append(f"| {i} | {title} | {r.get('year') or ''} | "
                   f"{(r.get('venue') or '')[:25]} | {cb} | {r.get('doi') or ''} |")
    return out


def _selftest() -> int:
    print("### cross_domain_search 离线自测", file=sys.stderr)
    res = cross_domain("dairy goat behaviour", "YOLO object detection",
                       per_page=3, current_year=2026, offline=True)
    assert res["offline"] is True, res
    # 两轴都跑了、各有记录
    assert res["application"].get("records"), res["application"]
    assert res["method"].get("records"), res["method"]
    # 迁移提示生成且绑定方法轴
    assert res["transfer_hints"], res
    assert "迁移" in res["transfer_hints"][0]["hint"], res["transfer_hints"][0]
    md = to_markdown(res)
    assert "应用轴" in md and "方法轴" in md and "迁移提示" in md, md
    print("[selftest] PASS cross_domain_search offline")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="跨领域正交双轴检索（应用轴 × 方法轴）")
    ap.add_argument("--application", default="dairy goat behaviour",
                    help="应用轴检索式（你的领域/任务）")
    ap.add_argument("--method", default="YOLO real-time object detection",
                    help="方法轴检索式（别的领域的前沿技术，要迁移过来的）")
    ap.add_argument("--per-page", type=int, default=8)
    ap.add_argument("--current-year", type=int, default=0,
                    help="当前年份（方法轴时效重排基准；不传则方法轴不做时效加权）")
    ap.add_argument("--half-life", type=int, default=3,
                    help="方法轴时效半衰期（年，默认3，比主脚本4更激进偏向最新 SOTA）")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--json-out", default="")
    ap.add_argument("--md-out", default="")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return _selftest()

    res = cross_domain(args.application, args.method, per_page=args.per_page,
                       current_year=args.current_year, half_life=args.half_life,
                       offline=args.offline)
    md = to_markdown(res)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2, default=str)
    if args.md_out:
        with open(args.md_out, "w", encoding="utf-8") as f:
            f.write(md)
    print(md)
    print(f"\n[SUMMARY] application={args.application!r} method={args.method!r} "
          f"offline={res['offline']} app={len(res['application'].get('records',[]))} "
          f"method={len(res['method'].get('records',[]))}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
