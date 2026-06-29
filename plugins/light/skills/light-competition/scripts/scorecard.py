#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scorecard.py — 竞赛材料「评委视角自审」可机检评分卡（零依赖）。

把 SKILL.md「评审模拟」段的文字化自审，落成一份可回归的量化工具：
读一份逐维度自评 JSON（每维 1–10 分），按所选赛事的评审维度加权求和，
输出总分 + 薄弱维度预警 + 对照 anti_patterns 的红旗提示，并给放行判定。

借鉴 GitHub tjboudreaux/cc-skills-vc-fundraising 把评审框架固化为可机检评分卡的思路，
但**严守诚实边界**（见下「权重依据声明」）：中国赛事确切权重多不公开，本卡权重是
**经验相对参考、非官方分值**，仅用于自审时发现"哪一维明显拖后腿"，不冒充官方评分。

用法：
  python scorecard.py                         # 无参 -> 跑合成自测
  python scorecard.py rating.json             # 用自己的自评 JSON（含 contest 字段）
  python scorecard.py rating.json --contest innovation   # 显式指定赛事
  python scorecard.py --emit-sample r.json    # 导出样例自评 JSON
  python scorecard.py --list                  # 列出内置赛事 rubric 维度
  python scorecard.py --selftest

⚠ 权重依据声明（诚实底线，勿读成"官方金标准"）：
  下方各赛事 WEIGHTS 锚定的是 db08 case_skeletons.md 与公开赛制口径的**维度构成**
  （创新性/可行性/团队/…），但**官方评分表多不公开数值权重或逐年逐校变动**——这里的
  0.25/0.20/… 是"按公开口径里维度重要性排序"的经验设定，非某届官方权重，也未做大样本回归。
  评委/用户若质疑"为何创新 0.25 而非 0.30"，诚实回答是"经验相对参考，可在 JSON 里传
  weights_override 覆盖，并以当届《评审规则》压缩包为准"。总分只用于自审排序薄弱项，
  不等于真实得分。
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import os
import json
import argparse
import tempfile

# === 各赛事评审维度与经验权重（合计 1.00）——非官方分值，自审相对参考，可被 JSON 覆盖 ===
# 维度名锚定 db08 case_skeletons.md 的公开评审维度；权重为经验设定（见上「权重依据声明」）。
RUBRICS = {
    "innovation": {   # 中国国际大学生创新大赛（原互联网+）创业/创意组
        "label": "中国国际大学生创新大赛（创业组）",
        "weights": {"创新性": 0.22, "商业价值/成长性": 0.20, "团队": 0.16,
                    "社会价值/带动就业": 0.16, "可行性": 0.16, "引领性": 0.10},
        "redflags": {"商业价值/成长性": "C3 市场自上而下虚高？C5 财务只有收入无现金流？",
                     "创新性": "A2 创新只是'首次把A用到B'未说为何难？A3 把先发/团队当壁垒？",
                     "社会价值/带动就业": "B3 价值喊口号无数据？"},
    },
    "dachuang": {     # 大创 / 科研训练
        "label": "大创 / 科研训练",
        "weights": {"选题/创新性": 0.22, "方案可行性": 0.20, "学生主体与培养价值": 0.22,
                    "研究基础": 0.14, "预期成果": 0.12, "经费合理性": 0.10},
        "redflags": {"学生主体与培养价值": "E3 写得像导师横向课题、看不出学生主体？",
                     "方案可行性": "B2 进度笼统'第一阶段调研'无交付物？C4 子目标互相依赖？",
                     "经费合理性": "D4 预算堆某一类、与研究活动脱节？"},
    },
    "dating": {       # 挑战杯"大挑" 课外学术科技作品
        "label": "挑战杯大挑（课外学术）",
        "weights": {"科学性": 0.24, "先进性/创新性": 0.24, "现实意义/应用价值": 0.20,
                    "研究深度/完成度": 0.20, "论证严谨性": 0.12},
        "redflags": {"研究深度/完成度": "当成课程论文交（无创新）？发明制作只有PPT没实物？",
                     "论证严谨性": "社会调查无一手数据、臆造样本？"},
    },
    "mcm": {          # 数学建模（CUMCM / MCM-ICM）
        "label": "数学建模 CUMCM/MCM-ICM",
        "weights": {"摘要质量": 0.26, "模型与求解": 0.24, "结果与检验": 0.18,
                    "灵敏度分析": 0.16, "创新性": 0.10, "写作与规范": 0.06},
        "redflags": {"摘要质量": "B1 摘要写成问题重述/复制引言？（数模初筛重灾区）",
                     "灵敏度分析": "C1 缺灵敏度分析与误差检验？（公认拉分项）",
                     "写作与规范": "D1 MCM 超25页（含附录代码）？漏 AI 使用说明？"},
    },
}


def list_rubrics():
    for key, r in RUBRICS.items():
        dims = "、".join(f"{d}({w:.0%})" for d, w in r["weights"].items())
        print(f"[{key}] {r['label']}\n    维度：{dims}\n")

# 自审放行判据——经验相对线（非官方），可被 JSON thresholds 覆盖。
DEFAULT_THRESHOLDS = {
    "weak_dim": 6,     # 单维 < 此分 → 列为薄弱项并触发该维红旗（10 分制下 6 为及格偏下）
    "pass_line": 75,   # 加权总分(0-100) ≥ 此 → 自审"较稳"；介于 reject~pass 为"待打磨"
    "reject_line": 55, # < 此 → 自审"风险高，重改"
}

SAMPLE = {
    "title": "基层眼底病智能筛查系统",
    "contest": "innovation",
    "ratings": {       # 每维 1–10 自评；缺的维度按 0 计并提示未评
        "创新性": 8, "商业价值/成长性": 5, "团队": 7,
        "社会价值/带动就业": 8, "可行性": 7, "引领性": 6,
    },
    # "weights_override": {...},  # 可选：覆盖经验权重（以当届官方规则为准时填）
    # "thresholds": {...},        # 可选：覆盖放行经验线
}


def evaluate(data, contest=None):
    """返回评分结果 dict：加权总分、逐维贡献、薄弱项、红旗、放行判定。"""
    contest = contest or data.get("contest")
    if contest not in RUBRICS:
        raise ValueError(f"未知赛事 '{contest}'，可选：{', '.join(RUBRICS)}（或用 --list 查看）")
    rubric = RUBRICS[contest]
    weights = dict(rubric["weights"])
    weights.update(data.get("weights_override", {}) or {})
    th = dict(DEFAULT_THRESHOLDS)
    th.update(data.get("thresholds", {}) or {})
    ratings = data.get("ratings", {})

    # 权重归一化（覆盖后可能不为 1）
    wsum = sum(weights.values())
    if wsum <= 0:
        raise ValueError("权重之和必须为正")

    rows, total, missing = [], 0.0, []
    for dim, w in weights.items():
        score = ratings.get(dim)
        if score is None:
            missing.append(dim)
            score = 0
        if not isinstance(score, (int, float)) or not (0 <= score <= 10):
            raise ValueError(f"维度 '{dim}' 自评分须在 0–10，得到 {score!r}")
        wn = w / wsum
        contrib = score * 10 * wn          # 10 分制 → 百分制贡献
        total += contrib
        rows.append({"dim": dim, "score": score, "weight": wn, "contrib": contrib})

    weak = [r["dim"] for r in rows if r["score"] < th["weak_dim"]]
    redflags = [f"{d}：{rubric['redflags'][d]}" for d in weak if d in rubric["redflags"]]
    verdict = ("较稳（仍须按 anti_patterns 终审）" if total >= th["pass_line"]
               else "风险高，重改" if total < th["reject_line"]
               else "待打磨")
    # 按自评分升序排（最该改进的维度在最上）；同分时贡献大的优先（改它对总分提升更多）
    return {"contest": contest, "label": rubric["label"], "total": round(total, 1),
            "rows": sorted(rows, key=lambda r: (r["score"], -r["contrib"])), "weak_dims": weak,
            "missing_dims": missing, "redflags": redflags, "verdict": verdict,
            "thresholds": th}


def render(res):
    out = [f"== {res['label']} 评委视角自审评分卡 =="]
    out.append(f"加权总分：{res['total']}/100  →  {res['verdict']}")
    out.append("（权重为经验相对参考、非官方分值；以当届《评审规则》为准）")
    out.append("\n逐维（按自评分升序，最该改进的在最上）：")
    for r in res["rows"]:
        mark = " ⚠薄弱" if r["dim"] in res["weak_dims"] else ""
        out.append(f"  {r['dim']:<16} 自评 {r['score']:>4}/10 × 权重 {r['weight']:.0%} = {r['contrib']:5.1f}{mark}")
    if res["missing_dims"]:
        out.append(f"\n未评维度（按 0 计，请补）：{', '.join(res['missing_dims'])}")
    if res["redflags"]:
        out.append("\n🚩 薄弱维度对照 anti_patterns 红旗自查：")
        for rf in res["redflags"]:
            out.append(f"  - {rf}")
    out.append("\n下一步：对薄弱维逐条过 references/anti_patterns.md，再做 defense_qa 答辩预演。")
    return "\n".join(out)


def _selftest() -> int:
    res = evaluate(SAMPLE)
    # 商业价值自评 5 < 6 应进薄弱项并触发 C3/C5 红旗
    assert "商业价值/成长性" in res["weak_dims"], res["weak_dims"]
    assert any("C3" in rf or "C5" in rf for rf in res["redflags"]), res["redflags"]
    # 逐维按自评分升序：最低自评分（商业价值 5）排第一
    assert res["rows"][0]["dim"] == "商业价值/成长性", res["rows"][0]
    # 权重归一化：总分应在 0–100
    assert 0 <= res["total"] <= 100, res["total"]
    # 满分应接近 100
    full = evaluate({"contest": "mcm", "ratings": {d: 10 for d in RUBRICS["mcm"]["weights"]}})
    assert abs(full["total"] - 100) < 0.1, full["total"]
    assert full["verdict"].startswith("较稳"), full["verdict"]
    # 缺维度按 0 计并列入 missing
    miss = evaluate({"contest": "dachuang", "ratings": {"选题/创新性": 8}})
    assert "方案可行性" in miss["missing_dims"], miss["missing_dims"]
    # weights_override 生效（归一化）
    ov = evaluate({"contest": "mcm", "ratings": {d: 6 for d in RUBRICS["mcm"]["weights"]},
                   "weights_override": {"摘要质量": 0.5}})
    assert abs(ov["total"] - 60) < 0.5, ov["total"]  # 全 6 分，任何归一化权重总分仍 60
    # 越界自评分应报错
    try:
        evaluate({"contest": "mcm", "ratings": {"摘要质量": 11}})
    except ValueError as e:
        assert "0–10" in str(e), e
    else:
        raise AssertionError("out-of-range rating should fail")
    # 未知赛事报错
    try:
        evaluate({"contest": "nope", "ratings": {}})
    except ValueError as e:
        assert "未知赛事" in str(e), e
    else:
        raise AssertionError("unknown contest should fail")
    render(res)  # 不抛错即可
    print("[selftest] PASS scorecard")
    return 0


def main():
    p = argparse.ArgumentParser(description="竞赛材料评委视角自审评分卡（可机检）")
    p.add_argument("rating", nargs="?", help="自评 JSON 路径；省略则跑合成自测")
    p.add_argument("--contest", choices=list(RUBRICS), help="赛事 rubric（覆盖 JSON 内 contest 字段）")
    p.add_argument("--emit-sample", metavar="PATH", help="导出样例自评 JSON 后退出")
    p.add_argument("--list", action="store_true", help="列出内置赛事 rubric 维度后退出")
    p.add_argument("--json", action="store_true", help="输出机读 JSON 而非文本报告")
    p.add_argument("--selftest", action="store_true", help="run offline synthetic self-test")
    args = p.parse_args()

    if args.selftest:
        return _selftest()
    if args.list:
        list_rubrics()
        return 0
    if args.emit_sample:
        with open(args.emit_sample, "w", encoding="utf-8") as f:
            json.dump(SAMPLE, f, ensure_ascii=False, indent=2)
        print(f"[已导出样例] {args.emit_sample}")
        return 0

    if args.rating:
        with open(args.rating, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = SAMPLE
        print("[自测] 未提供 JSON，使用内置合成自评\n")
    res = evaluate(data, args.contest)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(render(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
