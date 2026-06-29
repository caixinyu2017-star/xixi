#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""market_charts.py — 市场分析 JSON -> 四类市场数据图（matplotlib）

服务 light-competition（m17）：把创业类材料的真·市场数据渲染成评委一眼
看懂的四类图，对标 Market Research Reports skill 的可视化产出：
  ① TAM/SAM/SOM 三值     -> 分层同心圆（标各层金额与份额%）
  ② 竞品两轴打分          -> 2×2 定位矩阵（四象限标签 + 各家散点）
  ③ 波特五力 H/M/L        -> 分级条（逐力标等级 + rationale 缩写）
  ④ 风险概率×影响          -> 3×3 热图（按 概率×影响 严重度着色）

用法：
  python market_charts.py                        # 无参 -> 跑合成自测，出四张图
  python market_charts.py data.json              # 用自己的市场分析 JSON
  python market_charts.py data.json --kind tam --out t.png
  python market_charts.py --emit-sample sample.json   # 导出样例 JSON 模板

JSON 结构见 --emit-sample。其中 tam_sam_som 三值须与 db08/budget_template.md
第4节财务预测、case_skeletons.md §1 市场段共用同一套数（SOM 推导用户数、
ARPU、转化率跨材料一致，由 a07 一致性把关）。

诚实说明：matplotlib 渲染，纯本地、无网络、无外部数据；自测数据为合成占位，
非真实市场调研。图为可再生产物，按规范跑完即删，仓库只留本脚本。
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import os
import json
import argparse
import tempfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


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


# --- 色盲安全语义色 ---
# 取自 light-figure-drawing/scripts/color_palettes.py 的 Okabe-Ito (2008)
# 色盲安全 8 色板。此处不强依赖该脚本（跨技能 import 不便），就地定义等价常量，
# 来源同一调色板，保证印刷与色盲下可辨。
OKABE_ITO = {
    "black":        "#000000",
    "orange":       "#E69F00",
    "sky_blue":     "#56B4E9",
    "bluish_green": "#009E73",
    "yellow":       "#F0E442",
    "blue":         "#0072B2",
    "vermillion":   "#D55E00",
    "reddish_purple": "#CC79A7",
}
# 语义映射：低/中/高 三级用 蓝(安全)→橙(警示)→朱红(危险)，色盲下亦可分。
LEVEL_COLOR = {
    "L": OKABE_ITO["blue"],
    "M": OKABE_ITO["orange"],
    "H": OKABE_ITO["vermillion"],
}
LEVEL_LABEL = {"L": "低 (L)", "M": "中 (M)", "H": "高 (H)"}
# 同心圆三层：由外到内 浅→深，用蓝色系区分 TAM/SAM/SOM。
TSS_COLOR = {"TAM": OKABE_ITO["sky_blue"],
             "SAM": OKABE_ITO["blue"],
             "SOM": OKABE_ITO["bluish_green"]}


def _wrap_cjk(text, width):
    """按显示宽度软换行（CJK 记 2、其余记 1），返回多行字符串。不截断、不丢字。"""
    text = str(text)
    lines, cur, w = [], "", 0
    for ch in text:
        cw = 2 if ord(ch) > 0x2E7F else 1   # CJK/全角近似按双宽
        if ch == "\n" or (w + cw > width and cur):
            lines.append(cur)
            cur, w = ("" if ch == "\n" else ch), (0 if ch == "\n" else cw)
        else:
            cur += ch
            w += cw
    if cur:
        lines.append(cur)
    return "\n".join(lines)


def _wrap_truncate(text, width, max_lines):
    """软换行后限制最多 max_lines 行，超出截断并在末行加省略号，防止长文案溢出画布。"""
    wrapped = _wrap_cjk(text, width).split("\n")
    if len(wrapped) <= max_lines:
        return "\n".join(wrapped)
    kept = wrapped[:max_lines]
    kept[-1] = kept[-1].rstrip() + "…"
    return "\n".join(kept)


SAMPLE = {
    "title": "基层眼底病智能筛查",
    "currency": "亿元",
    "tam_sam_som": {
        "TAM": {"value": 320, "note": "全国糖网/眼底慢病筛查总市场"},
        "SAM": {"value": 64, "note": "县域基层医疗机构可服务市场"},
        "SOM": {"value": 6.4, "note": "3年内可获取（SOM→财务预测用户数同源）"}
    },
    "competitors": {
        "x_axis": "AI 分级准确率",
        "y_axis": "基层渠道覆盖",
        "items": [
            {"name": "本项目", "x": 0.82, "y": 0.35, "self": True},
            {"name": "三甲影像厂商A", "x": 0.88, "y": 0.20},
            {"name": "互联网医疗B", "x": 0.55, "y": 0.78},
            {"name": "传统器械C", "x": 0.40, "y": 0.65},
            {"name": "创业公司D", "x": 0.70, "y": 0.30}
        ]
    },
    "five_forces": [
        {"force": "现有竞争者", "level": "M", "rationale": "厂商分散未形成垄断"},
        {"force": "潜在进入者", "level": "H", "rationale": "AI门槛降、巨头可入"},
        {"force": "替代品", "level": "L", "rationale": "人工阅片成本高难替代"},
        {"force": "供应商议价", "level": "L", "rationale": "数据与算力来源多元"},
        {"force": "购买者议价", "level": "M", "rationale": "县医院预算敏感"}
    ],
    "risks": [
        {"name": "数据合规", "prob": "M", "impact": "H", "mitigation": "脱敏+伦理审批"},
        {"name": "现场灵敏度不达标", "prob": "M", "impact": "H", "mitigation": "前瞻验证go/no-go"},
        {"name": "渠道拓展慢", "prob": "H", "impact": "M", "mitigation": "县域试点先行"},
        {"name": "政策变动", "prob": "L", "impact": "M", "mitigation": "跟踪医保目录"}
    ]
}


def _validate(data):
    if not isinstance(data, dict):
        raise ValueError("顶层必须是 JSON 对象")
    if not any(k in data for k in
               ("tam_sam_som", "competitors", "five_forces", "risks")):
        raise ValueError("至少需含 tam_sam_som / competitors / "
                         "five_forces / risks 之一")
    tss = data.get("tam_sam_som")
    if tss:
        for k in ("TAM", "SAM", "SOM"):
            if k not in tss:
                raise ValueError(f"tam_sam_som 缺少 '{k}'")
            v = tss[k].get("value") if isinstance(tss[k], dict) else tss[k]
            if not isinstance(v, (int, float)) or v <= 0:
                raise ValueError(f"tam_sam_som.{k}.value 必须为正数")
        vals = [tss[k]["value"] if isinstance(tss[k], dict) else tss[k]
                for k in ("TAM", "SAM", "SOM")]
        if not (vals[0] >= vals[1] >= vals[2]):
            raise ValueError("应满足 TAM ≥ SAM ≥ SOM（自下而上收窄）")
    for f in data.get("five_forces", []):
        if f.get("level") not in ("L", "M", "H"):
            raise ValueError("five_forces.level 必须为 L/M/H")
    for r in data.get("risks", []):
        if r.get("prob") not in ("L", "M", "H") or \
                r.get("impact") not in ("L", "M", "H"):
            raise ValueError("risks.prob / impact 必须为 L/M/H")
    return data


def draw_tam_sam_som(data, out_path):
    """TAM/SAM/SOM 分层同心圆：面积∝金额，标各层金额与占上层份额%。"""
    tss = data["tam_sam_som"]
    unit = data.get("currency", "亿元")
    layers = []
    for k in ("TAM", "SAM", "SOM"):
        cell = tss[k]
        val = cell["value"] if isinstance(cell, dict) else cell
        note = cell.get("note", "") if isinstance(cell, dict) else ""
        layers.append((k, float(val), note))
    tam_val = layers[0][1]

    fig, ax = plt.subplots(figsize=(8.2, 6.2))
    ax.set_aspect("equal")
    ax.axis("off")
    rmax = 1.0
    for k, val, note in layers:                 # 半径∝sqrt(金额) -> 面积∝金额
        r = rmax * (val / tam_val) ** 0.5
        ax.add_patch(Circle((0, -1 + r), r, facecolor=TSS_COLOR[k],
                            edgecolor="black", linewidth=1.0, alpha=0.85,
                            zorder=layers.index((k, val, note)) + 1))
    # 各层标注：金额 + 占上层份额
    radii = [rmax * (val / tam_val) ** 0.5 for _, val, _ in layers]
    for idx, (k, val, note) in enumerate(layers):
        r = radii[idx]
        share = "" if idx == 0 else \
            f"  ({val / layers[idx - 1][1] * 100:.1f}% of {layers[idx-1][0]})"
        y = -1 + 2 * r - r * 0.32
        ax.text(0, y, f"{k}: {val:g} {unit}{share}", ha="center",
                va="center", fontsize=10, fontweight="bold",
                color="white" if idx >= 1 else "#222", zorder=10)
        if note:
            # 动态布局：note 的 y 锚到该层圆心高度（-1+r），按层半径分散；
            # 文本软换行 + 最多 3 行截断，固定落在圆右侧标注栏（x=1.15），不再用硬编码 idx*0.5。
            note_y = -1 + radii[idx]
            ax.annotate(_wrap_truncate(note, width=16, max_lines=3),
                        xy=(radii[idx] * 0.85, note_y), xytext=(1.15, note_y),
                        fontsize=7.5, color="#333", va="center",
                        arrowprops=dict(arrowstyle="-", color="#999", lw=0.6))
    ax.set_xlim(-1.2, 2.6)
    ax.set_ylim(-1.25, 1.25)
    ax.set_title(data.get("title", "市场规模") + " — TAM/SAM/SOM 分层市场",
                 fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def draw_positioning(data, out_path):
    """竞品 2×2 定位矩阵：双轴打分散点 + 四象限标签，本项目高亮。"""
    comp = data["competitors"]
    xlab = comp.get("x_axis", "维度X")
    ylab = comp.get("y_axis", "维度Y")
    items = comp["items"]

    fig, ax = plt.subplots(figsize=(7.6, 7.0))
    ax.axhline(0.5, color="#888", linewidth=1.0, zorder=1)
    ax.axvline(0.5, color="#888", linewidth=1.0, zorder=1)
    # 四象限底色（右上=领先，色盲安全语义色，低透明度）
    ax.fill_between([0.5, 1], 0.5, 1, color=OKABE_ITO["bluish_green"],
                    alpha=0.10, zorder=0)
    quad = [(0.75, 0.97, "领先者\n(双高)"), (0.25, 0.97, "渠道型\n(广而浅)"),
            (0.25, 0.03, "落后/利基"), (0.75, 0.03, "技术型\n(精而窄)")]
    for qx, qy, qt in quad:
        ax.text(qx, qy, qt, ha="center", va="center", fontsize=8.5,
                color="#555", style="italic", zorder=1)

    for it in items:
        is_self = bool(it.get("self"))
        c = OKABE_ITO["vermillion"] if is_self else OKABE_ITO["blue"]
        ax.scatter(it["x"], it["y"], s=260 if is_self else 150,
                   color=c, edgecolor="black",
                   linewidth=1.4 if is_self else 0.7,
                   marker="*" if is_self else "o", zorder=3)
        ax.annotate(it["name"], (it["x"], it["y"]),
                    xytext=(6, 6), textcoords="offset points",
                    fontsize=9, fontweight="bold" if is_self else "normal",
                    color=c, zorder=4)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel(f"{xlab} →", fontsize=10)
    ax.set_ylabel(f"{ylab} →", fontsize=10)
    ax.set_title(data.get("title", "竞品") + " — 2×2 竞品定位矩阵",
                 fontsize=12, fontweight="bold")
    ax.scatter([], [], marker="*", s=200, color=OKABE_ITO["vermillion"],
               edgecolor="black", label="本项目")
    ax.legend(loc="upper left", fontsize=8, frameon=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def draw_five_forces(data, out_path):
    """波特五力分级条：每力按 H/M/L 上色定长，逐条标 rationale 缩写。"""
    forces = data["five_forces"]
    n = len(forces)
    level_len = {"L": 1, "M": 2, "H": 3}
    fig, ax = plt.subplots(figsize=(10, 0.8 * n + 1.4))
    for i, f in enumerate(reversed(forces)):
        lv = f["level"]
        ax.barh(i, level_len[lv], height=0.55, color=LEVEL_COLOR[lv],
                edgecolor="black", linewidth=0.7, alpha=0.9, zorder=2)
        ax.text(0.05, i, f["force"], ha="left", va="center", fontsize=9.5,
                fontweight="bold", color="white", zorder=3)
        ax.text(level_len[lv] + 0.08, i, LEVEL_LABEL[lv], ha="left",
                va="center", fontsize=8.5, color=LEVEL_COLOR[lv],
                fontweight="bold")
        rat = f.get("rationale", "")
        if rat:
            # 长 rationale 软换行 + 最多 2 行截断，避免越界溢出右边界
            ax.text(level_len[lv] + 0.55, i, _wrap_truncate(rat, width=14, max_lines=2),
                    ha="left", va="center", fontsize=7.5, color="#333")
    ax.set_yticks([])
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(["低 L", "中 M", "高 H"], fontsize=8)
    ax.set_xlim(0, 5.2)
    ax.set_xlabel("威胁/议价强度分级", fontsize=9)
    ax.set_title(data.get("title", "竞争环境") + " — 波特五力分级",
                 fontsize=12, fontweight="bold")
    ax.grid(axis="x", linestyle=":", alpha=0.4, zorder=0)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def draw_risk_heatmap(data, out_path):
    """风险 概率×影响 3×3 热图：格底色按严重度，风险点落格并标缓解缩写。"""
    risks = data["risks"]
    lv_idx = {"L": 0, "M": 1, "H": 2}
    # 严重度 = 概率档×影响档（1..3），蓝(低)→橙(中)→朱红(高)
    sev_color = [[None] * 3 for _ in range(3)]
    for pi in range(3):
        for ii in range(3):
            s = (pi + 1) * (ii + 1)
            sev_color[pi][ii] = (LEVEL_COLOR["L"] if s <= 2 else
                                 LEVEL_COLOR["M"] if s <= 4 else
                                 LEVEL_COLOR["H"])
    fig, ax = plt.subplots(figsize=(7.4, 6.6))
    for pi in range(3):
        for ii in range(3):
            ax.add_patch(plt.Rectangle((ii, pi), 1, 1, facecolor=sev_color[pi][ii],
                                       edgecolor="white", linewidth=2, alpha=0.55))
    # 同格风险堆叠避免重叠
    bucket = {}
    for r in risks:
        ii, pi = lv_idx[r["impact"]], lv_idx[r["prob"]]
        bucket.setdefault((pi, ii), []).append(r)
    for (pi, ii), rs in bucket.items():
        m = len(rs)
        # 同格多风险：行距随密度自适配压缩，字号随之缩小，名称+缓解各自截断，避免堆出格子/溢出
        fs = 7.8 if m <= 2 else (6.6 if m <= 4 else 5.6)
        span = 0.8                       # 单格内可用纵向跨度
        for j, r in enumerate(rs):
            yo = (span / 2) - (j + 0.5) * (span / m)
            name = _wrap_truncate(r["name"], width=8, max_lines=2)
            label = name
            if r.get("mitigation"):
                label += "\n缓解:" + _wrap_truncate(r["mitigation"], width=8, max_lines=1)
            ax.text(ii + 0.5, pi + 0.5 + yo, label, ha="center", va="center",
                    fontsize=fs, fontweight="bold", color="#111",
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.8,
                              ec="none"))
    ax.set_xticks([0.5, 1.5, 2.5])
    ax.set_xticklabels(["低", "中", "高"], fontsize=9)
    ax.set_yticks([0.5, 1.5, 2.5])
    ax.set_yticklabels(["低", "中", "高"], fontsize=9)
    ax.set_xlabel("影响 (Impact) →", fontsize=10)
    ax.set_ylabel("概率 (Probability) →", fontsize=10)
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.set_title(data.get("title", "风险") + " — 风险 概率×影响 热图",
                 fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


KINDS = {
    "tam": ("tam_sam_som", draw_tam_sam_som, "tam_sam_som"),
    "positioning": ("competitors", draw_positioning, "positioning"),
    "fiveforces": ("five_forces", draw_five_forces, "five_forces"),
    "risk": ("risks", draw_risk_heatmap, "risk_heatmap"),
}



def _selftest() -> int:
    """离线自测：在临时目录生成四类图并验证输入校验。"""
    _setup_cjk_font()
    _validate(SAMPLE)
    with tempfile.TemporaryDirectory(prefix="light_market_charts_") as tmp:
        outputs = []
        for kind, (field, fn, suffix) in KINDS.items():
            out = os.path.join(tmp, f"{kind}_{suffix}.png")
            outputs.append(fn(SAMPLE, out))
        for out in outputs:
            assert os.path.exists(out) and os.path.getsize(out) > 0, out
    bad = json.loads(json.dumps(SAMPLE, ensure_ascii=False))
    bad["tam_sam_som"]["SAM"]["value"] = 999
    try:
        _validate(bad)
    except ValueError as exc:
        assert "TAM" in str(exc), exc
    else:
        raise AssertionError("invalid TAM/SAM/SOM hierarchy should fail")

    # --- C-5 文本布局工具单测 ---
    assert _wrap_cjk("县域基层医疗机构可服务市场", 8).count("\n") >= 2  # 13 CJK→宽16应多行
    assert _wrap_cjk("abcdefghij", 4) == "abcd\nefgh\nij"
    long_note = "这是一个非常长的市场说明文字用于测试软换行与截断是否会溢出画布边界"
    tr = _wrap_truncate(long_note, width=16, max_lines=3)
    assert tr.count("\n") == 2 and tr.endswith("…"), tr        # 超 3 行被截断加省略号

    # --- C-5 极端数据回归：6 力（>4 层）+ 超长 rationale/note + 同格 4 风险，应正常出图不抛错 ---
    stress = json.loads(json.dumps(SAMPLE, ensure_ascii=False))
    stress["tam_sam_som"]["SOM"]["note"] = long_note            # 长 note
    stress["five_forces"].append(
        {"force": "互补品", "level": "M",
         "rationale": "互补生态尚未成熟需要长期培育且依赖第三方平台开放程度"})  # 第 6 力 + 长 rationale
    stress["risks"] = [{"name": f"风险{i}号有较长名称", "prob": "H", "impact": "H",
                        "mitigation": "采取若干较长的缓解措施"} for i in range(4)]  # 同格 4 风险堆叠
    _validate(stress)
    with tempfile.TemporaryDirectory(prefix="light_market_stress_") as tmp:
        for kind, (field, fn, suffix) in KINDS.items():
            out = fn(stress, os.path.join(tmp, f"{kind}.png"))
            assert os.path.exists(out) and os.path.getsize(out) > 0, out
    print("[selftest] PASS market_charts")
    return 0


def main():
    p = argparse.ArgumentParser(description="市场分析 JSON -> 四类市场数据图")
    p.add_argument("data", nargs="?", help="市场分析 JSON 路径；省略则跑合成自测")
    p.add_argument("--kind", choices=list(KINDS) + ["all"], default="all",
                   help="画哪类图（默认 all）")
    p.add_argument("--out", help="输出文件名（单图时用）")
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

    if args.data:
        with open(args.data, "r", encoding="utf-8") as f:
            data = json.load(f)
        tag = os.path.splitext(os.path.basename(args.data))[0]
        demo_mode = False
    else:
        data = SAMPLE
        tag = "demo"
        demo_mode = True
        print("[自测] 未提供 JSON，使用内置合成市场数据（占位，非真实调研）")

    _validate(data)

    # 无 JSON 的 demo 路径：默认落临时目录，不污染技能根/当前目录（除非用户显式 --out）。
    demo_dir = tempfile.mkdtemp(prefix="light_market_charts_demo_") if (demo_mode and not args.out) else None

    todo = list(KINDS) if args.kind == "all" else [args.kind]
    outputs = []
    for kind in todo:
        field, fn, suffix = KINDS[kind]
        if field not in data:
            print(f"[跳过] 缺字段 '{field}'，不画 {kind}")
            continue
        default_name = f"{tag}_{suffix}.png"
        if demo_dir:
            default_name = os.path.join(demo_dir, default_name)
        out = (args.out if (args.out and args.kind == kind) else default_name)
        outputs.append(fn(data, out))

    if not outputs:
        print("[警告] 无可画图（数据缺对应字段）")
        sys.exit(0)
    for o in outputs:
        print(f"[已生成] {o}  ({os.path.getsize(o)} bytes)")
    if demo_dir:
        print(f"[demo] 合成图写入临时目录 {demo_dir}（不污染仓库；真实用法传 data.json/--out）。")
    print("[完成] 图为可再生产物，评审材料用完后可删除，仓库只留脚本。")


if __name__ == "__main__":
    sys.exit(main())
