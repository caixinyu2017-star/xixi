#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""data_feasibility.py — 把"数据先行四问"汇成喂给 m03/m04 的标准结论卡。

m02 对 m05/a03/m06 的交接有 data_card.md / quality_report.md（重工件，给做实验用）。
但 m02 对 m03(提 idea)/m04(审 idea) 的交接只有"四问结论"——idea 该不该立项，看的是
"数据够不够支撑"，不是完整数据卡。本脚本把四问收敛成一份轻量、可机检的落盘工件
`data_feasibility.md`，补上 CONVENTIONS §6.1 里 m02→m03/m04 这条原本靠聊天传的单向挂载。

四问（与 SKILL 核心原则一致）：
  Q1 数据是否足以支撑研究？      sufficiency
  Q2 质量是否可靠？             quality
  Q3 规模是否足够？             scale       （可吃 sample_size_check.py --json）
  Q4 特征是否有挖掘价值？        feature_value（可吃 data_doctor 的泄漏/ID-like 信号）

每问三态 ok/warn/insufficient + 依据 + 证据来源（脚本输出/人工判断）。
整体 verdict 取四问最差档：全 ok→usable / 含 warn→usable_with_caveats /
含 insufficient→insufficient（建议补采，回 m02 不进 m03）。

纯标准库零依赖、零网络。可手填，也可 --from-json 吃前序脚本的结构化输出拼装。

用法：
  # 交互式手填四问（给 level/note）：
  python data_feasibility.py --project goat-behavior \
      --q1 ok:"3类行为有判别性传感器特征" \
      --q2 warn:"accel_x 偶发越界(warn级门禁)" \
      --q3 warn:"发情类须>=100，正式量待power analysis" \
      --q4 ok:"剔除泄漏列后25维有效特征" --out data_feasibility.md
  # 吃 sample_size_check 的 JSON 自动填 Q3：
  python data_feasibility.py --project x --scale-json size.json --q1 ok:... --q2 ok:... --q4 ok:...
  # 自测
  python data_feasibility.py --selftest
"""
from __future__ import annotations
import argparse
import io
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

LEVELS = ("ok", "warn", "insufficient")
_ORDER = {"ok": 0, "warn": 1, "insufficient": 2}

QUESTIONS = [
    ("sufficiency", "Q1 数据是否足以支撑研究？"),
    ("quality", "Q2 质量是否可靠？"),
    ("scale", "Q3 规模是否足够？"),
    ("feature_value", "Q4 特征是否有挖掘价值？"),
]

# 整体判定：四问最差档 → verdict
VERDICT = {
    "ok": ("USABLE", "✅", "数据基础充分，可进 m03 提 idea"),
    "warn": ("USABLE_WITH_CAVEATS", "⚠️", "可进 m03，但须在 idea 里正视下列保留项"),
    "insufficient": ("INSUFFICIENT", "🛑", "数据不足以支撑，先回 m02 补采/补质，不进 m03"),
}


def parse_answer(raw: str) -> tuple[str, str]:
    """'ok:理由' / 'warn:理由' → (level, note)。无冒号视为 note，level 默认 warn（须人工定档）。"""
    if raw is None:
        return ("warn", "(未填，须人工判定)")
    if ":" in raw:
        lvl, _, note = raw.partition(":")
        lvl = lvl.strip().lower()
        if lvl not in LEVELS:
            return ("warn", raw.strip())
        return (lvl, note.strip() or "(无理由)")
    return ("warn", raw.strip())


def scale_from_json(d: dict) -> tuple[str, str]:
    """吃 sample_size_check.py --json 的输出，转成 Q3 的 (level, note)。"""
    lvl = d.get("level", "warn")
    if lvl not in LEVELS:
        lvl = "warn"
    findings = d.get("findings") or []
    note = findings[0] if findings else f"sample_size_check level={lvl}"
    return (lvl, f"{note}（sample_size_check.py，非 power analysis）")


def assess(project: str, answers: dict, sources: dict | None = None) -> dict:
    """answers: {key: (level, note)}。返回结论 dict（含整体 verdict）。"""
    sources = sources or {}
    rows = []
    worst = "ok"
    for key, label in QUESTIONS:
        lvl, note = answers.get(key, ("warn", "(未填，须人工判定)"))
        if lvl not in LEVELS:
            lvl = "warn"
        if _ORDER[lvl] > _ORDER[worst]:
            worst = lvl
        rows.append({"key": key, "label": label, "level": lvl,
                     "note": note, "source": sources.get(key, "人工判断")})
    code, icon, action = VERDICT[worst]
    return {"project": project, "verdict": code, "icon": icon,
            "verdict_level": worst, "action": action, "questions": rows}


def render(rep: dict) -> str:
    L = [f"# 数据先行四问结论 — {rep['project']}", ""]
    L.append(f"**Verdict: {rep['icon']} {rep['verdict']}** — {rep['action']}")
    L.append("")
    L.append("> 交给 m03(idea-generation) / m04(idea-critique) 判 idea 是否有数据基础。"
             "本卡是结论摘要；完整数据卡见 `data_card.md`、体检见 `quality_report.md`。")
    L.append("")
    L.append("| 四问 | 档位 | 依据 | 证据来源 |")
    L.append("| --- | --- | --- | --- |")
    mark = {"ok": "ok", "warn": "**warn**", "insufficient": "**insufficient**"}
    for q in rep["questions"]:
        note = q["note"].replace("|", "\\|")
        L.append(f"| {q['label']} | {mark[q['level']]} | {note} | {q['source']} |")
    L.append("")
    if rep["verdict_level"] == "insufficient":
        L.append("> 🛑 至少一问 insufficient：按 SKILL 核心原则，**不进 m03**，先回数据处理/补采。")
    elif rep["verdict_level"] == "warn":
        L.append("> ⚠ 含保留项：可进 m03，但 m04 复核会针对 warn 项核 idea 是否正视该限制。")
    else:
        L.append("> ✅ 四问皆 ok：数据基础充分。仍提醒规模结论须正式 power analysis 背书。")
    L.append("")
    L.append("<!-- 由 data_feasibility.py 生成；档位为人工/脚本判定，非自动结论。 -->")
    return "\n".join(L)


def _selftest() -> int:
    print("### data_feasibility 离线自测", file=sys.stderr)
    # 全 ok → USABLE
    r = assess("p", {"sufficiency": ("ok", "a"), "quality": ("ok", "b"),
                     "scale": ("ok", "c"), "feature_value": ("ok", "d")})
    assert r["verdict"] == "USABLE" and r["verdict_level"] == "ok", r
    # 含 warn → USABLE_WITH_CAVEATS（取最差档）
    r = assess("p", {"sufficiency": ("ok", "a"), "quality": ("warn", "b"),
                     "scale": ("ok", "c"), "feature_value": ("ok", "d")})
    assert r["verdict"] == "USABLE_WITH_CAVEATS", r
    # 含 insufficient → INSUFFICIENT（最差档压倒 warn）
    r = assess("p", {"sufficiency": ("ok", "a"), "quality": ("warn", "b"),
                     "scale": ("insufficient", "c"), "feature_value": ("ok", "d")})
    assert r["verdict"] == "INSUFFICIENT" and r["verdict_level"] == "insufficient", r
    # 缺答 → 默认 warn（不静默当 ok）
    r = assess("p", {"sufficiency": ("ok", "a")})
    assert r["verdict_level"] == "warn", r
    # parse_answer：合法档位 / 非法档位回退 warn / 无冒号
    assert parse_answer("ok:理由") == ("ok", "理由")
    assert parse_answer("bogus:x")[0] == "warn"
    assert parse_answer("只有理由")[0] == "warn"
    # scale_from_json：吃 sample_size_check 输出
    lvl, note = scale_from_json({"level": "insufficient",
                                 "findings": ["[insufficient] 最小类=40 < 50/类"]})
    assert lvl == "insufficient" and "最小类" in note, (lvl, note)
    # 渲染可读、含 verdict 与四问
    md = render(assess("demo", {"scale": ("warn", "x")}))
    assert "Verdict" in md and "Q3" in md and "data_card.md" in md, md
    # 渲染不抛异常、含转义
    render(assess("p", {"quality": ("ok", "含|竖线")}))
    print("[selftest] PASS data_feasibility offline")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="数据先行四问 → data_feasibility.md（喂 m03/m04）")
    ap.add_argument("--project", default="unnamed")
    ap.add_argument("--q1", help="Q1 数据是否足以支撑：'ok|warn|insufficient:理由'")
    ap.add_argument("--q2", help="Q2 质量是否可靠")
    ap.add_argument("--q3", help="Q3 规模是否足够（也可用 --scale-json 自动填）")
    ap.add_argument("--q4", help="Q4 特征是否有挖掘价值")
    ap.add_argument("--scale-json", help="sample_size_check.py --json 的输出文件，自动填 Q3")
    ap.add_argument("--out", help="输出路径（默认 stdout）；契约标准名 data_feasibility.md")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return _selftest()

    answers, sources = {}, {}
    if args.q1:
        answers["sufficiency"] = parse_answer(args.q1)
    if args.q2:
        answers["quality"] = parse_answer(args.q2)
    if args.q4:
        answers["feature_value"] = parse_answer(args.q4)
    if args.scale_json:
        with io.open(args.scale_json, encoding="utf-8") as fh:
            answers["scale"] = scale_from_json(json.load(fh))
        sources["scale"] = "sample_size_check.py --json"
    elif args.q3:
        answers["scale"] = parse_answer(args.q3)

    rep = assess(args.project, answers, sources)
    md = render(rep)
    if args.out:
        with io.open(args.out, "w", encoding="utf-8") as fh:
            fh.write(md)
        print(f"Wrote {args.out}", file=sys.stderr)
    else:
        print(md)
    # insufficient → 退出码 1，可在 pipeline 当"不进 m03"的闸门
    return 1 if rep["verdict_level"] == "insufficient" else 0


if __name__ == "__main__":
    sys.exit(main())
