#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recommend_chart.py — 论文图型启发式推荐（数据字段 + 分析任务 → 候选图型排序）。

借 Draco/Voyager 的"形式化图型推荐"思路，但**轻量、可解释、纯规则**：给定要呈现的数据
字段类型与分析任务，输出候选图型 + 排序 + 每个的理由/适用/注意，把 figure-planning 里
"给 claim 匹配呈现形式"这一步从凭感觉变成可复现的规则建议。产物喂规划卡(figure_plan_card)
的"建议工具/图型"字段，再交 validate_plan_card.py 做契约校验、m11 出图。

⚠ 诚实声明（勿读成"最优解/真值"）：
- 这是**启发式规则**，不是约束求解最优化（Draco 那种），更不是替你做图设计判断。规则依据
  可视化领域共识（Cleveland & McGill 1984 感知精度排序、Mackinlay APT、Munzner task taxonomy、
  Bertin 视觉变量），但具体排序权重是**经验设定、可调**，非实验反推。
- 输出是"候选 + 理由"，**最终选型须人工结合 claim 重要性/领域惯例/期刊偏好定夺**。
- 不涉及 AI 生图：只推荐"该用什么图型"，真图由 m11 程序化绘制（matplotlib/ggplot/TikZ）。

数据字段类型（Stevens 测量尺度 + 时间）：
  nominal 定类(类别无序) / ordinal 定序(有序类别) / quantitative 定量(数值) / temporal 时间
分析任务（Munzner/Shneiderman 任务族 + 论文常见）：
  comparison 比较 / distribution 分布 / correlation 关系 / composition 构成 /
  trend 趋势 / ranking 排序 / part-of-whole 占比 / uncertainty 不确定性

用法：
  python recommend_chart.py --task comparison --fields nominal quantitative
  python recommend_chart.py --task trend --fields temporal quantitative --n-series 5
  python recommend_chart.py --selftest
"""
from __future__ import annotations
import argparse
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

FIELD_TYPES = ("nominal", "ordinal", "quantitative", "temporal")
TASKS = ("comparison", "distribution", "correlation", "composition",
         "trend", "ranking", "part-of-whole", "uncertainty")

# 图型知识库：每个候选给 适用字段组合 / 适用任务 / base_score(经验先验) / 理由 / 注意。
# base_score 是经验先验(0-10)，反映该图型在对应任务下的感知精度与论文常用度，可调。
# 感知精度序参考 Cleveland & McGill 1984：位置 > 长度 > 角度/面积 > 颜色/体积。
CHART_KB = [
    {"chart": "grouped_bar", "zh": "分组柱状图",
     "tasks": {"comparison": 9, "ranking": 7, "part-of-whole": 3},
     "needs": {"nominal", "quantitative"}, "max_series": 6,
     "why": "类别间数值比较首选——条形等基线、长度编码感知精度高(Cleveland-McGill 仅次于位置)",
     "caution": "系列>5~6 拥挤；不传达占比(占比用堆叠/饼);零基线不可截断"},
    {"chart": "line", "zh": "折线图",
     "tasks": {"trend": 10, "comparison": 6, "correlation": 4},
     "needs": {"temporal", "quantitative"}, "max_series": 8,
     "why": "连续/时间趋势首选——位置编码+连线传达变化方向与速率",
     "caution": "类别型(无序)不可用线连;系列过多用小多图(small multiples)"},
    {"chart": "scatter", "zh": "散点图",
     "tasks": {"correlation": 10, "distribution": 6},
     "needs": {"quantitative", "quantitative"}, "max_series": 4,
     "why": "两连续变量关系/相关首选——双位置编码精度最高，可加回归线/置信带",
     "caution": "过度绘制(overplotting)用透明度/hexbin/2D 密度;相关≠因果"},
    {"chart": "box_violin", "zh": "箱线图/小提琴图",
     "tasks": {"distribution": 9, "comparison": 7, "uncertainty": 6},
     "needs": {"nominal", "quantitative"}, "max_series": 10,
     "why": "跨组分布比较——显示中位/四分位/离群;小提琴叠加密度。小样本叠散点(遵 db07 R5)",
     "caution": "小样本(n<10)箱线图误导，必叠原始散点;标注 n"},
    {"chart": "histogram_kde", "zh": "直方图/核密度",
     "tasks": {"distribution": 10},
     "needs": {"quantitative"}, "max_series": 3,
     "why": "单变量分布形状首选——直方看分箱频数，KDE 看平滑密度",
     "caution": "分箱宽度敏感(标 bin 宽/带宽);多组叠加>3 难辨"},
    {"chart": "stacked_bar", "zh": "堆叠柱状图",
     "tasks": {"composition": 9, "part-of-whole": 8, "trend": 5},
     "needs": {"nominal", "quantitative"}, "max_series": 6,
     "why": "构成/占比随类别或时间变化——同一条内分段看组成",
     "caution": "非底层段难比较(基线不齐);占比固定看总量用百分比堆叠"},
    {"chart": "pie_donut", "zh": "饼图/环图",
     "tasks": {"part-of-whole": 6, "composition": 5},
     "needs": {"nominal", "quantitative"}, "max_series": 5,
     "why": "单一总体的占比构成——直观但精度低(角度/面积编码弱于长度)",
     "caution": "类别>5 或需精确比较时改用柱状图;审稿人常嫌饼图;切片标百分比"},
    {"chart": "heatmap", "zh": "热力图",
     "tasks": {"correlation": 8, "comparison": 6, "distribution": 5},
     "needs": {"nominal", "nominal", "quantitative"}, "max_series": 999,
     "why": "二维类别网格的数值模式——相关矩阵/混淆矩阵/消融网格",
     "caution": "颜色编码精度低(只看模式不读精确值);固定 vmin-vmax(遵 db07 R6);色盲安全色图"},
    {"chart": "grouped_line_smallmult", "zh": "小多图折线",
     "tasks": {"trend": 8, "comparison": 7},
     "needs": {"temporal", "quantitative"}, "max_series": 999,
     "why": "多系列趋势避免线缠绕——每系列一个小图，共享坐标轴",
     "caution": "占版面;统一 y 轴范围才能跨子图比较"},
    {"chart": "ranking_bar", "zh": "排序条形图(横向)",
     "tasks": {"ranking": 10, "comparison": 8},
     "needs": {"nominal", "quantitative"}, "max_series": 30,
     "why": "排名/Top-N 首选——横向条形按值排序，标签好读",
     "caution": "按值排序而非字母序;太多项截 Top-N 并说明"},
    {"chart": "error_bar_point", "zh": "点估计+误差棒",
     "tasks": {"uncertainty": 10, "comparison": 7},
     "needs": {"nominal", "quantitative"}, "max_series": 10,
     "why": "带不确定性的组间比较——点估计+CI/SD/SEM(遵 db07 R7 注明类型与 n)",
     "caution": "必须注明误差棒含义(SD/SEM/CI)与 n;勿用柱状图掩盖分布"},
]


def _field_match(needs: set, fields: list) -> float:
    """字段匹配度 0~1：needs 是图型要求的字段类型集合，fields 是用户给的字段类型。
    全覆盖=1.0；部分覆盖按比例；多出的定量字段不罚（可做 size/color 第三维）。"""
    if not needs:
        return 0.5
    fset = set(fields)
    hit = len(needs & fset)
    cover = hit / len(needs)
    # 用户字段里有 needs 要求的重复类型（如 scatter 要两个 quantitative）做个粗校验
    from collections import Counter
    need_c, have_c = Counter(needs), Counter(fields)
    for t, c in need_c.items():
        if have_c.get(t, 0) < c:
            cover *= 0.7  # 类型数量不足，降权但不归零
    return round(cover, 3)


def recommend(task: str, fields: list, n_series: int = 1, top_k: int = 5) -> dict:
    """按任务+字段+系列数推荐图型，返回排序候选 + 理由。纯启发式、可解释。"""
    if task not in TASKS:
        raise ValueError(f"task 须是 {TASKS} 之一: {task!r}")
    for f in fields:
        if f not in FIELD_TYPES:
            raise ValueError(f"field 须是 {FIELD_TYPES} 之一: {f!r}")
    scored = []
    for kb in CHART_KB:
        task_score = kb["tasks"].get(task, 0)
        if task_score == 0:
            continue  # 该图型不适用此任务
        fm = _field_match(kb["needs"], fields)
        if fm == 0:
            continue
        # 系列数惩罚：超过 max_series 线性降分
        series_pen = 1.0
        if n_series > kb["max_series"]:
            series_pen = max(0.3, kb["max_series"] / n_series)
        # 综合分 = 任务先验 × 字段匹配 × 系列惩罚（满分 10）
        score = round(task_score * fm * series_pen, 2)
        notes = []
        if n_series > kb["max_series"]:
            notes.append(f"系列数 {n_series}>{kb['max_series']}：考虑小多图/Top-N/聚合")
        scored.append({"chart": kb["chart"], "zh": kb["zh"], "score": score,
                       "field_match": fm, "why": kb["why"], "caution": kb["caution"],
                       "notes": notes})
    scored.sort(key=lambda r: (-r["score"], r["chart"]))
    return {
        "task": task, "fields": list(fields), "n_series": n_series,
        "candidates": scored[:top_k],
        "note": ("启发式推荐(非最优化/非真值)，依据 Cleveland-McGill 感知精度+任务族经验先验；"
                 "最终选型须结合 claim 重要性/领域惯例/期刊偏好人工定夺。图由 m11 程序化绘制，不 AI 生图。"),
        "next": "选定图型后填 figure_plan_card 的图型/工具字段，跑 validate_plan_card.py 校验契约。",
    }


def to_markdown(rec: dict) -> str:
    lines = [f"# 图型推荐 — task={rec['task']} fields={rec['fields']} series={rec['n_series']}\n",
             "| 排名 | 图型 | 综合分 | 字段匹配 | 理由 | 注意 |",
             "|---|---|---|---|---|---|"]
    for i, c in enumerate(rec["candidates"], 1):
        caution = c["caution"] + ("；" + "；".join(c["notes"]) if c["notes"] else "")
        lines.append("| %d | %s(%s) | %.2f | %.2f | %s | %s |" % (
            i, c["zh"], c["chart"], c["score"], c["field_match"],
            c["why"][:40], caution[:50]))
    lines.append(f"\n> {rec['note']}\n> 下一步：{rec['next']}")
    return "\n".join(lines)


def _selftest() -> int:
    print("### recommend_chart 离线自测", file=sys.stderr)

    # 1) 比较任务+定类定量 → 分组柱状图应排前
    r = recommend("comparison", ["nominal", "quantitative"])
    assert r["candidates"], r
    top = r["candidates"][0]["chart"]
    assert top in ("grouped_bar", "box_violin", "ranking_bar", "error_bar_point"), top
    assert any(c["chart"] == "grouped_bar" for c in r["candidates"]), r

    # 2) 趋势+时间定量 → 折线图应第一
    r2 = recommend("trend", ["temporal", "quantitative"])
    assert r2["candidates"][0]["chart"] == "line", r2["candidates"][0]

    # 3) 关系+双定量 → 散点图应第一
    r3 = recommend("correlation", ["quantitative", "quantitative"])
    assert r3["candidates"][0]["chart"] == "scatter", r3["candidates"][0]

    # 4) 分布+单定量 → 直方/核密度应第一
    r4 = recommend("distribution", ["quantitative"])
    assert r4["candidates"][0]["chart"] == "histogram_kde", r4["candidates"][0]

    # 5) 系列数惩罚：趋势 20 系列时 line 降分、小多图相对受益
    r5 = recommend("trend", ["temporal", "quantitative"], n_series=20)
    line_c = next(c for c in r5["candidates"] if c["chart"] == "line")
    assert line_c["notes"], line_c  # 应提示系列过多
    assert any(c["chart"] == "grouped_line_smallmult" for c in r5["candidates"]), r5

    # 6) 排序任务 → 横向排序条形图第一
    r6 = recommend("ranking", ["nominal", "quantitative"], n_series=15)
    assert r6["candidates"][0]["chart"] == "ranking_bar", r6["candidates"][0]

    # 7) 非法输入报错
    try:
        recommend("bad_task", ["nominal"])
        raise AssertionError("should raise on bad task")
    except ValueError:
        pass
    try:
        recommend("comparison", ["bad_field"])
        raise AssertionError("should raise on bad field")
    except ValueError:
        pass

    # 8) markdown 输出含诚实声明
    md = to_markdown(r)
    assert "启发式" in md and "人工定夺" in md, md
    print("[selftest] PASS recommend_chart offline")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="论文图型启发式推荐（数据字段+任务→候选图型排序）")
    ap.add_argument("--task", choices=TASKS, help="分析任务")
    ap.add_argument("--fields", nargs="+", choices=FIELD_TYPES, help="数据字段类型(可多个)")
    ap.add_argument("--n-series", type=int, default=1, help="系列/分组数(影响拥挤度惩罚)")
    ap.add_argument("--top-k", type=int, default=5, help="返回候选数")
    ap.add_argument("--json", action="store_true", help="输出 JSON 而非 markdown")
    ap.add_argument("--selftest", action="store_true", help="run offline synthetic self-test")
    args = ap.parse_args()

    if args.selftest:
        return _selftest()
    if not (args.task and args.fields):
        ap.error("需 --task 与 --fields（或 --selftest）")

    rec = recommend(args.task, args.fields, args.n_series, args.top_k)
    if args.json:
        import json
        print(json.dumps(rec, ensure_ascii=False, indent=2))
    else:
        print(to_markdown(rec))
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] == "--selftest"):
        sys.exit(_selftest())
    sys.exit(main())
