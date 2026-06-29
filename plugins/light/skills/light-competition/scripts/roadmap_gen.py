#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""roadmap_gen.py — 里程碑 JSON -> 技术路线图 / 甘特图（matplotlib）

服务 light-competition（m17）：把项目进度安排画成评委一眼看懂的
(1) 甘特图（gantt）：阶段/任务 + 起止 + 交付物 + go/no-go 节点
(2) 技术路线图（roadmap）：阶段块 + 箭头流向 + 每阶段产出

用法：
  python roadmap_gen.py                       # 无参 -> 跑内置合成自测，出两张图
  python roadmap_gen.py plan.json             # 用自己的里程碑 JSON
  python roadmap_gen.py plan.json --kind gantt --out g.png
  python roadmap_gen.py plan.json --out figures/        # --out 为目录则两图都落该目录
  python roadmap_gen.py plan.json --granularity week     # 周粒度（数模等短周期），start 用 YYYY-MM-DD、时长用 weeks
  python roadmap_gen.py --emit-sample sample.json   # 导出一份样例 JSON 模板

JSON 结构（见 --emit-sample）：
{
  "title": "项目名",
  "start": "2026-09",            # 全局起始；month 粒度用 YYYY-MM，week 粒度用 YYYY-MM-DD
  "milestones": [
    {"phase":"调研与立项","start":"2026-09","months":2,
     "deliverable":"需求报告+数据集清单","gate":"go/no-go:数据可得性",
     "owner":"全员"},
    # week 粒度：{"phase":"建模","start":"2026-09-01","weeks":1.5,...}（缺 weeks 则按 months×4.345 兜底）
    ...
  ]
}
诚实说明：matplotlib 渲染，纯本地、无网络、无外部数据；自测数据为合成。
图为可再生产物，按规范跑完即删，仓库只留本脚本。
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import os
import json
import argparse
import tempfile
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


def _setup_cjk_font():
    """尽量挂上一个中文字体，挂不上则降级（不报错），保证脚本可跑。"""
    candidates = ["Microsoft YaHei", "SimHei", "SimSun",
                  "Noto Sans CJK SC", "WenQuanYi Zen Hei", "Arial Unicode MS"]
    from matplotlib import font_manager
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            matplotlib.rcParams["font.sans-serif"] = [name]
            matplotlib.rcParams["axes.unicode_minus"] = False
            return name
    matplotlib.rcParams["axes.unicode_minus"] = False
    return None


def _month_index(ym, origin):
    """把 'YYYY-MM' 转成相对 origin 的月份偏移（整数）。"""
    a = datetime.strptime(ym, "%Y-%m")
    o = datetime.strptime(origin, "%Y-%m")
    return (a.year - o.year) * 12 + (a.month - o.month)


def _parse_date(s):
    """宽松解析 'YYYY-MM-DD' 或 'YYYY-MM'（按当月 1 号）。"""
    for fmt in ("%Y-%m-%d", "%Y-%m"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise ValueError(f"无法解析日期 '{s}'（应为 YYYY-MM 或 YYYY-MM-DD）")


def _unit_index(value, origin, gran):
    """阶段起点相对 origin 的偏移，单位由 gran 决定（month / week）。"""
    if gran == "week":
        delta = _parse_date(value) - _parse_date(origin)
        return delta.days / 7.0
    return _month_index(value, origin)


def _duration_units(m, gran):
    """阶段时长，按粒度取字段：week 优先 'weeks'（无则 months×4.345 兜底）；month 取 'months'。"""
    if gran == "week":
        if "weeks" in m:
            return float(m["weeks"])
        return float(m["months"]) * 4.345   # 月→周近似，便于沿用旧 JSON
    return float(m["months"])


def _validate(plan, gran="month"):
    if not isinstance(plan, dict):
        raise ValueError("顶层必须是 JSON 对象")
    ms = plan.get("milestones")
    if not ms or not isinstance(ms, list):
        raise ValueError("缺少非空的 'milestones' 列表")
    for i, m in enumerate(ms):
        for k in ("phase", "start"):
            if k not in m:
                raise ValueError(f"milestones[{i}] 缺少字段 '{k}'")
        # 时长字段：month 粒度需 'months'；week 粒度需 'weeks' 或 'months'（后者按 4.345 周/月换算）
        if "months" not in m and "weeks" not in m:
            raise ValueError(f"milestones[{i}] 缺少时长字段 'months'（week 粒度可用 'weeks'）")
        dur = _duration_units(m, gran)
        if not isinstance(dur, (int, float)) or dur <= 0:
            raise ValueError(f"milestones[{i}] 时长必须为正数")
    return plan


SAMPLE = {
    "title": "基层眼底病智能筛查系统",
    "start": "2026-09",
    "milestones": [
        {"phase": "调研与立项", "start": "2026-09", "months": 2,
         "deliverable": "需求报告 + 数据集清单 + 立项核心页",
         "gate": "go/no-go: 数据可得性确认", "owner": "全员"},
        {"phase": "数据采集与标注", "start": "2026-11", "months": 3,
         "deliverable": "≥3000 张标注眼底图 + 质量分级标签",
         "gate": "", "owner": "数据组"},
        {"phase": "模型研发", "start": "2027-01", "months": 4,
         "deliverable": "轻量化分级模型 v1 (<5M 参数)",
         "gate": "go/no-go: 验证集灵敏度≥90%", "owner": "算法组"},
        {"phase": "端侧部署与原型", "start": "2027-04", "months": 3,
         "deliverable": "手机端小程序原型 (50ms 内推理)",
         "gate": "", "owner": "工程组"},
        {"phase": "县医院前瞻验证", "start": "2027-07", "months": 3,
         "deliverable": "前瞻性验证报告 + 试点协议",
         "gate": "go/no-go: 现场灵敏度达标", "owner": "全员"},
        {"phase": "结题与成果产出", "start": "2027-10", "months": 2,
         "deliverable": "论文 + 软著 + 结题报告 + 开源代码",
         "gate": "", "owner": "全员"},
    ],
}


def draw_gantt(plan, out_path, gran="month"):
    """阶段甘特图：横向条 + 交付物 + go/no-go 菱形节点。gran 控制时间粒度（month/week）。"""
    ms = plan["milestones"]
    origin = plan.get("start", ms[0]["start"])
    n = len(ms)
    fig, ax = plt.subplots(figsize=(11, 0.85 * n + 1.6))

    total = max(_unit_index(m["start"], origin, gran) + _duration_units(m, gran) for m in ms)
    cmap = plt.colormaps.get_cmap("viridis")

    for i, m in enumerate(reversed(ms)):
        row = i
        x0 = _unit_index(m["start"], origin, gran)
        w = _duration_units(m, gran)
        color = cmap((n - 1 - i) / max(n - 1, 1))
        ax.barh(row, w, left=x0, height=0.5, color=color, alpha=0.85,
                edgecolor="black", linewidth=0.6, zorder=2)
        ax.text(x0 + w / 2, row, m["phase"], ha="center", va="center",
                color="white", fontsize=9, fontweight="bold", zorder=3)
        deliver = m.get("deliverable", "")
        if deliver:
            ax.text(x0 + w + 0.15, row + 0.18, "交付: " + deliver,
                    ha="left", va="center", fontsize=7.5, color="#333")
        gate = m.get("gate", "")
        if gate:
            ax.scatter([x0 + w], [row], marker="D", s=90, color="#d62728",
                       edgecolor="black", linewidth=0.6, zorder=4)
            ax.text(x0 + w + 0.15, row - 0.22, gate, ha="left", va="center",
                    fontsize=7.5, color="#d62728")

    ax.set_yticks(range(n))
    ax.set_yticklabels([""] * n)
    unit_label = {"month": "M", "week": "W"}[gran]
    n_ticks = int(total) + 1
    # 周粒度阶段多时，刻度过密则按步长稀释，避免标签重叠
    step = 1 if n_ticks <= 16 else (n_ticks // 16 + 1)
    ticks = list(range(0, n_ticks + 1, step))
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{unit_label}{k}" for k in ticks], fontsize=8)
    unit_cn = {"month": "月份", "week": "周次"}[gran]
    ax.set_xlabel(f"项目{unit_cn}（起点 {origin}）", fontsize=9)
    ax.set_xlim(-0.3, total + 4.5)
    ax.set_title(plan.get("title", "项目进度甘特图") + " — 进度甘特图",
                 fontsize=12, fontweight="bold")
    ax.grid(axis="x", linestyle=":", alpha=0.4, zorder=0)
    # 图例：红菱形 = go/no-go 决策节点
    ax.scatter([], [], marker="D", s=90, color="#d62728", edgecolor="black",
               label="go/no-go 决策节点")
    ax.legend(loc="lower right", fontsize=8, frameon=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def draw_roadmap(plan, out_path):
    """技术路线图：阶段块自左向右排，箭头连接，块下标注交付物。"""
    ms = plan["milestones"]
    n = len(ms)
    per_row = 3
    rows = (n + per_row - 1) // per_row
    fig, ax = plt.subplots(figsize=(4.2 * min(n, per_row) + 1, 2.7 * rows + 1))
    ax.set_xlim(0, per_row)
    ax.set_ylim(0, rows)
    ax.axis("off")
    cmap = plt.colormaps.get_cmap("plasma")

    box_w, box_h = 0.78, 0.42
    centers = []
    for i, m in enumerate(ms):
        r = i // per_row
        c = i % per_row
        if r % 2 == 1:           # 蛇形排布：奇数行从右往左，箭头连续
            c = per_row - 1 - c
        cx = c + 0.5
        cy = rows - 1 - r + 0.5
        centers.append((cx, cy, i))
        color = cmap(i / max(n - 1, 1))
        box = FancyBboxPatch((cx - box_w / 2, cy - box_h / 2), box_w, box_h,
                             boxstyle="round,pad=0.02,rounding_size=0.05",
                             linewidth=1.2, edgecolor="black",
                             facecolor=color, alpha=0.85, zorder=2)
        ax.add_patch(box)
        ax.text(cx, cy + 0.07, f"阶段{i+1}", ha="center", va="center",
                fontsize=8, color="white", zorder=3)
        ax.text(cx, cy - 0.05, m["phase"], ha="center", va="center",
                fontsize=9, fontweight="bold", color="white", zorder=3)
        deliver = m.get("deliverable", "")
        if deliver:
            ax.text(cx, cy - box_h / 2 - 0.08, "→ " + deliver, ha="center",
                    va="top", fontsize=7, color="#333", zorder=3)

    for k in range(n - 1):       # 按 milestone 顺序连接（含蛇形换行）
        x0, y0, _ = centers[k]
        x1, y1, _ = centers[k + 1]
        arr = FancyArrowPatch((x0, y0), (x1, y1),
                              arrowstyle="-|>", mutation_scale=14,
                              color="#444", linewidth=1.3, zorder=1,
                              shrinkA=box_w * 36, shrinkB=box_w * 36)
        ax.add_patch(arr)

    ax.set_title(plan.get("title", "技术路线") + " — 技术路线图",
                 fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path



def _selftest() -> int:
    """离线自测：在临时目录生成甘特图与路线图并验证输入校验。"""
    _setup_cjk_font()
    _validate(SAMPLE)
    assert _month_index("2026-11", "2026-09") == 2
    # 周粒度索引与时长换算
    assert _unit_index("2026-09-15", "2026-09-01", "week") == 2.0   # 14 天 = 2 周
    assert abs(_duration_units({"months": 2}, "week") - 2 * 4.345) < 1e-6  # 月→周兜底
    assert _duration_units({"weeks": 6, "months": 2}, "week") == 6.0       # weeks 优先
    assert _duration_units({"months": 2}, "month") == 2.0
    with tempfile.TemporaryDirectory(prefix="light_roadmap_gen_") as tmp:
        gantt = draw_gantt(SAMPLE, os.path.join(tmp, "gantt.png"))
        roadmap = draw_roadmap(SAMPLE, os.path.join(tmp, "roadmap.png"))
        # 周粒度甘特图（用 YYYY-MM-DD start + weeks），短周期竞赛场景
        wk_plan = {"title": "数模 99 小时", "start": "2026-09-01", "milestones": [
            {"phase": "建模", "start": "2026-09-01", "weeks": 1.5, "gate": "go/no-go: 模型选定"},
            {"phase": "求解", "start": "2026-09-12", "weeks": 2},
            {"phase": "写作", "start": "2026-09-26", "weeks": 1.5, "deliverable": "论文+摘要"}]}
        _validate(wk_plan, "week")
        gantt_w = draw_gantt(wk_plan, os.path.join(tmp, "gantt_w.png"), "week")
        for out in (gantt, roadmap, gantt_w):
            assert os.path.exists(out) and os.path.getsize(out) > 0, out
    bad = {"milestones": [{"phase": "bad", "start": "2026-09", "months": 0}]}
    try:
        _validate(bad)
    except ValueError as exc:
        assert "时长" in str(exc) or "months" in str(exc), exc
    else:
        raise AssertionError("non-positive months should fail")
    # 缺时长字段应报错
    try:
        _validate({"milestones": [{"phase": "x", "start": "2026-09"}]})
    except ValueError as exc:
        assert "时长" in str(exc), exc
    else:
        raise AssertionError("missing duration should fail")
    print("[selftest] PASS roadmap_gen")
    return 0


def main():
    p = argparse.ArgumentParser(description="里程碑 JSON -> 甘特图/技术路线图")
    p.add_argument("plan", nargs="?", help="里程碑 JSON 路径；省略则跑合成自测")
    p.add_argument("--kind", choices=["gantt", "roadmap", "both"],
                   default="both", help="画哪种图（默认 both）")
    p.add_argument("--out", help="输出路径：以 / 结尾或为已存在目录时落该目录用默认名；否则当单图文件名用")
    p.add_argument("--granularity", choices=["month", "week"], default="month",
                   help="甘特图时间粒度：month（默认，start=YYYY-MM/duration=months）或 week（start=YYYY-MM-DD/duration=weeks，适合数模等短周期）")
    p.add_argument("--emit-sample", metavar="PATH",
                   help="导出样例 JSON 模板到指定路径后退出")
    p.add_argument("--selftest", action="store_true", help="run offline synthetic self-test")
    args = p.parse_args()

    if args.selftest:
        return _selftest()

    if args.emit_sample:
        with open(args.emit_sample, "w", encoding="utf-8") as f:
            json.dump(SAMPLE, f, ensure_ascii=False, indent=2)
        print(f"[已导出样例] {args.emit_sample}")
        return

    font = _setup_cjk_font()
    print(f"[字体] 中文字体: {font or '未找到，中文可能显示为方块（不影响逻辑）'}")

    if args.plan:
        with open(args.plan, "r", encoding="utf-8") as f:
            plan = json.load(f)
        tag = os.path.splitext(os.path.basename(args.plan))[0]
        demo_mode = False
    else:
        plan = SAMPLE
        tag = "demo"
        demo_mode = True
        print("[自测] 未提供 JSON，使用内置合成里程碑")

    _validate(plan, args.granularity)

    # --out 目录语义：以 / 结尾或为已存在目录 → 落该目录用默认名（both 也支持）；否则当单图文件名。
    out_dir = None
    if args.out and (args.out.endswith(("/", os.sep)) or os.path.isdir(args.out)):
        out_dir = args.out
        os.makedirs(out_dir, exist_ok=True)
    # 无 JSON 的 demo 路径：默认落临时目录，不污染技能根/当前目录（除非用户显式 --out）。
    demo_dir = tempfile.mkdtemp(prefix="light_roadmap_gen_demo_") if (demo_mode and not args.out) else None

    def _resolve(default_name):
        if out_dir:
            return os.path.join(out_dir, default_name)
        if demo_dir:
            return os.path.join(demo_dir, default_name)
        return default_name

    single_file = args.out if (args.out and not out_dir) else None
    outputs = []
    if args.kind in ("gantt", "both"):
        out = single_file if (single_file and args.kind == "gantt") else _resolve(f"{tag}_gantt.png")
        outputs.append(draw_gantt(plan, out, args.granularity))
    if args.kind in ("roadmap", "both"):
        out = single_file if (single_file and args.kind == "roadmap") else _resolve(f"{tag}_roadmap.png")
        outputs.append(draw_roadmap(plan, out))

    for o in outputs:
        print(f"[已生成] {o}  ({os.path.getsize(o)} bytes)")
    if demo_dir:
        print(f"[demo] 合成图写入临时目录 {demo_dir}（不污染仓库；真实用法传 --plan/--out）。")
    print("[完成] 图为可再生产物，评审材料用完后可删除，仓库只留脚本。")


if __name__ == "__main__":
    sys.exit(main())
