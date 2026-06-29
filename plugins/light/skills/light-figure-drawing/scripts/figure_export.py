#!/usr/bin/env python3
"""figure_export.py — 投稿级图像导出工具 (Light / light-figure-drawing)

提供:
  - save_publication_figure(fig, basename, formats, dpi, ...)  多格式 + DPI 导出
  - save_for_journal(fig, basename, journal, column, ...)      按刊规格设尺寸并导出
  - check_figure_size(fig, max_width_mm, ...)                  校验栏宽(mm)是否合规
  - check_scaled_fonts(fig, journal, column, ...)             校验缩放到栏宽后的有效字号
  - JOURNAL_SPECS                                              逐刊硬规格表(mm/DPI/字号)

设计:无外部数据;matplotlib Agg 后端;__main__ 产 demo 图并自检。
依据规格见 SKILL.md 逐刊表;付费墙未实测项以 verified=False 标注。
"""
from __future__ import annotations
import os
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

MM_PER_INCH = 25.4

# 逐刊规格: width_mm 为 (单栏, 双栏/整版) 可选键; min_dpi 按线条图; min_font_pt 最终字号下限
JOURNAL_SPECS = {
    "nature": {
        "single_mm": 89.0, "double_mm": 183.0,
        "min_dpi_line": 600, "min_dpi_halftone": 300, "min_dpi_combo": 600,
        "min_font_pt": 5.0, "preferred_formats": ("pdf", "tiff", "eps"),
        "font_family": "sans-serif", "verified": True,
        "note": "实测 nature.com/nature/for-authors/final-submission (HTTP200): "
                "89mm单栏/183mm双栏; 面板标 8pt粗体 a,b,c; 正文最大7pt 最小5pt; "
                "Helvetica/Arial; 照片300-600dpi; 文字勿转曲",
    },
    "science": {
        "single_mm": 55.0, "double_mm": 120.0, "full_mm": 183.0,
        "min_dpi_line": 600, "min_dpi_halftone": 300, "min_dpi_combo": 500,
        "min_font_pt": 5.0, "preferred_formats": ("eps", "pdf", "ai", "tiff"),
        "font_family": "sans-serif", "verified": True,
        "note": "Science/AAAS 三档栏宽(联网核实 2026-06-11, science.org 作者指南三档制): "
                "1栏 5.5cm=55mm / 2栏 12cm=120mm / 整页 18.3cm=183mm。"
                "science.org 页对 curl/WebFetch 返回 403, 数值经 WebSearch 多源一致核实"
                "(5.5/12/18.3 cm); 细则 DPI 未逐项实测。原 121mm 系换算误差, 已订正为 120mm。",
    },
    "cell": {
        "single_mm": 85.0, "double_mm": 174.0,
        "min_dpi_line": 1000, "min_dpi_halftone": 300, "min_dpi_combo": 500,
        "min_font_pt": 5.0, "preferred_formats": ("pdf", "ai", "eps", "tiff"),
        "font_family": "sans-serif", "verified": False,
        "note": "Cell Press 数字艺术规格;线条图常要求 1000dpi;未逐项实测",
    },
    "plos": {
        "single_mm": 83.0, "onehalf_mm": 140.0, "double_mm": 190.0,
        "min_dpi_line": 600, "min_dpi_halftone": 300, "min_dpi_combo": 600,
        "min_font_pt": 8.0, "preferred_formats": ("tiff", "eps"),
        "max_height_px": 2625, "max_file_mb": 10.0,
        "font_family": "sans-serif", "verified": True,
        "note": "实测 journals.plos.org/plosone/s/figures (HTTP200): "
                "仅收 TIFF/EPS; 宽 789-2250px@300dpi (6.68-19.05cm); "
                "高<=2625px; 分辨率300-600dpi; 文字 Arial/Times/Symbol 8-12pt; <10MB",
    },
    "ieee": {
        "single_mm": 88.9, "double_mm": 181.0,
        "min_dpi_line": 600, "min_dpi_halftone": 300, "min_dpi_combo": 600,
        "min_font_pt": 8.0, "preferred_formats": ("pdf", "eps", "tiff"),
        "font_family": "sans-serif", "verified": False,
        "note": "IEEE 双栏模板栏宽约 3.5in/7.16in;Graphics Checker 建议 >=300dpi",
    },
    "elsevier": {
        "single_mm": 90.0, "double_mm": 190.0, "onehalf_mm": 140.0,
        "min_dpi_line": 1000, "min_dpi_halftone": 300, "min_dpi_combo": 500,
        "min_font_pt": 7.0, "preferred_formats": ("pdf", "eps", "tiff"),
        "font_family": "sans-serif", "verified": False,
        "note": "Elsevier 艺术指南:线条 1000dpi, 灰/彩 300dpi, 组合 500dpi;未逐项实测",
    },
    "mdpi": {
        "single_mm": 170.0, "full_mm": 170.0,
        "min_dpi_line": 1000, "min_dpi_halftone": 300, "min_dpi_combo": 1000,
        "min_font_pt": 8.0, "preferred_formats": ("tiff", "png", "eps"),
        "font_family": "sans-serif", "verified": False,
        "column_caveat": "⚠ MDPI 是单列版式：single/full 都=170mm 正文整宽，column 参数在 MDPI 下"
                         "不区分宽窄（不同于 Nature 等 single≈89mm 双栏刊）。要更窄的图按 170mm 的"
                         "整数分数(如 ½≈83mm)自行设 custom_width_mm，别指望 column='single' 给窄栏。",
        "note": "MDPI 单列版式正文宽 ≈170mm(图按此宽或其整数分数排); 线稿/组合图建议"
                "1000dpi, 照片>=300dpi; TIFF/PNG/EPS。数据来源: m11 light-figure-planning "
                "references.md「出版商图宽硬规格核查表」MDPI 行(含 db01 Animals/Agronomy/"
                "Sensors/Remote Sensing); ⚠️付费墙未逐项实测, 投稿前以目标刊当期官网为准。",
    },
}

def mm_to_inch(mm: float) -> float:
    return mm / MM_PER_INCH


def inch_to_mm(inch: float) -> float:
    return inch * MM_PER_INCH


def save_publication_figure(fig, basename, formats=("pdf", "png", "svg"),
                            dpi=600, transparent=False, pad_inches=0.02,
                            close=False, bbox_inches="tight"):
    """多格式 + DPI 导出。返回写出的文件路径列表。

    - basename 可含目录, 不含扩展名。
    - 矢量格式(pdf/svg/eps)忽略 dpi(对线条无意义), 但保留以便位图。
    - 自动确保 pdf/ps fonttype=42、svg 文字不转曲, 文字可二次编辑。
    - bbox_inches: 默认 "tight" 裁掉白边(通用导出器的常见诉求)。
      传 None 则严格按 fig 的 set_size_inches 落盘, 物理宽度不被裁剪改变
      (精确栏宽投稿场景必须用 None; 此时 pad_inches 不生效)。
    """
    os.makedirs(os.path.dirname(os.path.abspath(basename)), exist_ok=True)
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42
    plt.rcParams["svg.fonttype"] = "none"
    # 注意: matplotlib 里 savefig(bbox_inches=None) 不是"不裁剪", 而是回退到
    # rcParams["savefig.bbox"]。若活动样式(如 publication.mplstyle)设了
    # savefig.bbox=tight, 显式传 None 会被静默改回 tight。故此处把 rcParam
    # 同步成调用者意图, 让显式参数始终生效。
    written = []
    prev_bbox = plt.rcParams.get("savefig.bbox")
    plt.rcParams["savefig.bbox"] = bbox_inches
    try:
        for fmt in formats:
            path = f"{basename}.{fmt}"
            save_kwargs = {"format": fmt, "dpi": dpi, "transparent": transparent,
                           "bbox_inches": bbox_inches}
            # bbox_inches=None 时 pad_inches 不生效, 不传以免干扰
            if bbox_inches is not None:
                save_kwargs["pad_inches"] = pad_inches
            fig.savefig(path, **save_kwargs)
            written.append(path)
    finally:
        plt.rcParams["savefig.bbox"] = prev_bbox
    if close:
        plt.close(fig)
    return written


def _check_font_availability():
    """检查 mpl 当前首选无衬线字体是否真实可用，回退到 DejaVu 等兜底字体则告警。
    Linux/CI 常无 Arial/Helvetica，matplotlib 会静默回退 DejaVu Sans——'字体与正文一致'
    的诉求会悄悄落空。返回 {requested, resolved, fell_back, warning}。"""
    import matplotlib.font_manager as fm
    import matplotlib as mpl
    prefs = list(mpl.rcParams.get("font.sans-serif", []))
    fam = mpl.rcParams.get("font.family", ["sans-serif"])
    # 只在 sans-serif 家族时检查首选项
    if not prefs:
        return {"requested": [], "resolved": None, "fell_back": False, "warning": None}
    top = prefs[0]
    try:
        resolved_path = fm.findfont(fm.FontProperties(family=prefs), fallback_to_default=True)
        resolved_name = fm.FontProperties(fname=resolved_path).get_name()
    except Exception:
        resolved_name = None
    # 解析到的字体名是否匹配首选项里任一（大小写/空格宽松）
    norm = lambda s: (s or "").lower().replace(" ", "")
    ok = any(norm(p) == norm(resolved_name) for p in prefs)
    warning = None
    if not ok:
        warning = (f"字体落空：rcParams 首选 {prefs[:3]} 不可用，实际渲染回退为 '{resolved_name}'"
                   f"（常见于 Linux/CI 无 Arial/Helvetica）——'字体与正文一致'可能落空，"
                   f"装字体或在投稿环境复核；矢量 PDF/SVG 可后期在 Illustrator 替换字体")
    return {"requested": prefs[:3], "resolved": resolved_name, "fell_back": not ok,
            "warning": warning}


def save_for_journal(fig, basename, journal="nature", column="single",
                     height_mm=None, formats=None, dpi=None,
                     custom_width_mm=None, **kwargs):
    """按目标刊规格设置物理尺寸并导出。

    - journal: JOURNAL_SPECS 的键, 或 "custom"(配合 custom_width_mm 用)。
    - column: 'single' / 'double' / 'full' / 'onehalf' (依该刊有的键)。
    - height_mm: 不给则保持当前宽高比缩放到目标宽度。
    - custom_width_mm: 逃生通道。journal="custom" 时直接用此物理栏宽(mm),
      绕开 JOURNAL_SPECS 键名限制。用于尚未进 JOURNAL_SPECS 的刊(如中文刊),
      数据须有来源(db01 卡或实测记录), 禁止臆测。此时 dpi/formats 不给则取通用默认
      (600dpi, pdf+png), min_font 不强制。
    返回 (written_paths, info_dict)。
    """
    j = journal.lower()
    if j == "custom" or custom_width_mm is not None:
        if custom_width_mm is None:
            raise ValueError("journal='custom' 需传 custom_width_mm(mm)")
        width_mm = float(custom_width_mm)
        spec = {"min_font_pt": None, "verified": False,
                "note": f"custom 栏宽 {width_mm}mm(调用方提供,数据须有来源,禁止臆测)",
                "preferred_formats": ("pdf", "png"), "min_dpi_line": 600}
    else:
        if j not in JOURNAL_SPECS:
            raise ValueError(f"未知期刊 '{journal}', 可选: {list(JOURNAL_SPECS)} 或 'custom'+custom_width_mm")
        spec = JOURNAL_SPECS[j]
        key = f"{column}_mm"
        if key not in spec:
            avail = [k.replace("_mm", "") for k in spec if k.endswith("_mm")]
            raise ValueError(f"{journal} 无 '{column}' 栏宽, 可选: {avail}")
        width_mm = spec[key]
    width_in = mm_to_inch(width_mm)
    cur_w, cur_h = fig.get_size_inches()
    if height_mm is None:
        height_in = width_in * (cur_h / cur_w)
    else:
        height_in = mm_to_inch(height_mm)
    fig.set_size_inches(width_in, height_in)
    # 把内容压进固定画布(而非靠 bbox_inches="tight" 裁剪改变物理尺寸)。
    # constrained 引擎在固定 figsize 下重排 axes; 老版本回退 tight_layout。
    try:
        fig.set_layout_engine("constrained")
    except Exception:
        try:
            fig.tight_layout()
        except Exception:
            pass
    if formats is None:
        formats = spec["preferred_formats"][:2]
    if dpi is None:
        dpi = spec["min_dpi_line"]
    # 关键: bbox_inches=None 使落盘宽度严格等于 set_size_inches 设定值,
    # 不被 "tight" 按内容裁剪改变, 兑现"精确栏宽投稿"承诺。
    kwargs.setdefault("bbox_inches", None)
    font_check = _check_font_availability()
    if font_check["warning"]:
        print("[WARNING] " + font_check["warning"], file=sys.stderr)
    written = save_publication_figure(fig, basename, formats=formats, dpi=dpi, **kwargs)
    info = {"journal": j, "column": column, "width_mm": width_mm,
            "height_mm": round(inch_to_mm(height_in), 1), "dpi": dpi,
            "formats": list(formats), "min_font_pt": spec["min_font_pt"],
            "verified": spec["verified"], "note": spec["note"],
            "font": font_check}
    if spec.get("column_caveat"):
        info["column_caveat"] = spec["column_caveat"]
        print("[NOTE] " + spec["column_caveat"], file=sys.stderr)
    return written, info


def check_figure_size(fig, max_width_mm=None, journal=None, column="single",
                      tol_mm=0.5, verbose=True, measured=False, path=None,
                      custom_width_mm=None):
    """校验图形物理宽度(mm)是否符合栏宽。返回 dict 报告。

    给 journal 则用该刊该栏宽作为上限; 否则用 max_width_mm。
    journal="custom"(配合 custom_width_mm) 走逃生通道: 用 custom_width_mm 作目标栏宽,
      不强制最小字号(中文刊等尚未进 JOURNAL_SPECS 时用; 数据须有来源, 禁止臆测)。
    同时检查可见文字字号是否 >= 该刊下限(若给 journal 且该刊有下限)。

    measured=True: 不信任 fig.get_size_inches()(那是裁剪前画布尺寸),
      改为读回已落盘文件的真实物理宽度复核——这才能抓出 bbox_inches="tight"
      静默改变栏宽的问题。需传 path(已写出的文件)。
      PNG: 用 PIL 读像素宽/dpi 反推 mm(零额外重依赖)。
      PDF/SVG: 有 pypdf/PdfReader 走真实读取, 缺则降级跳过(report 标注)。
    """
    if journal is not None and journal.lower() == "custom":
        if custom_width_mm is None:
            raise ValueError("journal='custom' 需传 custom_width_mm(mm)")
        max_width_mm = float(custom_width_mm)
        journal = None  # 后续按 max_width_mm 路径走, 不查 JOURNAL_SPECS
    if measured:
        if path is None:
            raise ValueError("measured=True 需传 path(已写出的文件)")
        return _check_measured(path, max_width_mm=max_width_mm,
                               journal=journal, column=column,
                               tol_mm=tol_mm, verbose=verbose)
    w_in, h_in = fig.get_size_inches()
    w_mm, h_mm = inch_to_mm(w_in), inch_to_mm(h_in)
    report = {"width_mm": round(w_mm, 2), "height_mm": round(h_mm, 2),
              "ok": True, "problems": []}
    limit = max_width_mm
    min_font = None
    if journal is not None:
        spec = JOURNAL_SPECS[journal.lower()]
        limit = spec.get(f"{column}_mm", limit)
        min_font = spec["min_font_pt"]
        report["journal"] = journal.lower()
        report["column"] = column
    if limit is not None:
        report["max_width_mm"] = limit
        if w_mm > limit + tol_mm:
            report["ok"] = False
            report["problems"].append(
                f"宽度 {w_mm:.1f}mm 超过上限 {limit}mm")
    if min_font is not None:
        tiny = _collect_small_fonts(fig, min_font)
        report["min_font_pt"] = min_font
        if tiny:
            report["ok"] = False
            report["problems"].append(
                f"{len(tiny)} 处文字字号 < {min_font}pt: 最小 {min(tiny):.1f}pt")
    if verbose:
        status = "OK" if report["ok"] else "FAIL"
        print(f"[check_figure_size] {status}  {report}")
    return report


def _collect_small_fonts(fig, min_font_pt):
    """收集小于下限的可见文字字号(pt)。"""
    small = []
    for txt in fig.findobj(plt.Text):
        try:
            s = txt.get_text()
        except Exception:
            continue
        if not s or not s.strip():
            continue
        if not txt.get_visible():
            continue
        fs = txt.get_fontsize()
        if fs < min_font_pt - 1e-6:
            small.append(fs)
    return small


def check_scaled_fonts(fig, journal=None, column="single",
                       target_width_mm=None, min_font_pt=None, verbose=True):
    """校验"大尺寸画再缩小到栏宽"后的有效字号是否仍达下限。

    顶刊常见工作流：先按大画布作图（如 180mm 宽），投稿时整体缩放到栏宽
    （如单栏 89mm）。缩放系数 = 目标栏宽 / 当前画布宽，所有文字字号等比缩小。
    一个画布上 10pt 的字，缩到一半栏宽后实际只有 ~5pt——check_figure_size
    看的是原始字号，会漏掉这种缩放后失真。本函数补这个盲点。

    给 journal 自动取该刊栏宽与 min_font_pt；或显式传 target_width_mm/min_font_pt。
    返回报告：scale(缩放系数)、每处文字缩放后有效字号、低于下限的项。

    ⚠ 适用场景：本函数只对"**先大画布作图、再整体缩到栏宽**"的工作流有意义。若你已用
    `save_for_journal()` 把画布设成精确栏宽（scale≈1），本函数必然报"无缩放风险"——这是预期的
    空操作，不是 bug。standard 流程（save_for_journal）下字号下限由该函数导出时直接保证，无需再跑
    本函数；只有手动大画布出图再缩放时才需要它。
    """
    if journal is not None:
        spec = JOURNAL_SPECS[journal.lower()]
        if target_width_mm is None:
            target_width_mm = spec.get(f"{column}_mm")
        if min_font_pt is None:
            min_font_pt = spec["min_font_pt"]
    if target_width_mm is None or min_font_pt is None:
        raise ValueError("需要 journal，或同时给 target_width_mm 与 min_font_pt")

    cur_w_mm = inch_to_mm(fig.get_size_inches()[0])
    scale = target_width_mm / cur_w_mm if cur_w_mm else 1.0
    report = {"current_width_mm": round(cur_w_mm, 2),
              "target_width_mm": round(target_width_mm, 2),
              "scale": round(scale, 4), "min_font_pt": min_font_pt,
              "ok": True, "violations": []}

    if scale >= 0.999:
        # 不缩小（或放大）则无失真风险，仅提示
        report["note"] = "画布未缩小到栏宽以下，无缩放失真风险"
    for txt in fig.findobj(plt.Text):
        try:
            s = txt.get_text()
        except Exception:
            continue
        if not s or not s.strip() or not txt.get_visible():
            continue
        eff = txt.get_fontsize() * scale
        if eff < min_font_pt - 1e-6:
            report["ok"] = False
            report["violations"].append(
                {"text": s[:30], "raw_pt": round(txt.get_fontsize(), 1),
                 "effective_pt": round(eff, 2)})
    if verbose:
        status = "OK" if report["ok"] else "FAIL"
        msg = (f"[check_scaled_fonts] {status}  scale={report['scale']} "
               f"({report['current_width_mm']}→{report['target_width_mm']}mm)")
        if report["violations"]:
            worst = min(v["effective_pt"] for v in report["violations"])
            msg += f"  {len(report['violations'])} 处缩放后 <{min_font_pt}pt(最小 {worst}pt)"
        print(msg)
    return report



def _measure_file_width_mm(path):
    """读回已落盘文件的真实物理宽度(mm)。

    返回 (width_mm, backend) 或 (None, reason)。无重依赖:
      .png  -> PIL 读 (像素宽 / dpi) * 25.4
      .pdf  -> pypdf.PdfReader 读 MediaBox(单位 pt=1/72in)
      .svg  -> 解析根 <svg width="..."> (mm/in/px/pt)
    """
    ext = os.path.splitext(path)[1].lower()
    if ext == ".png":
        try:
            from PIL import Image
        except Exception:
            return None, "PIL-missing"
        with Image.open(path) as im:
            px_w = im.size[0]
            dpi = im.info.get("dpi", (None, None))[0]
        if not dpi:
            return None, "png-no-dpi"
        return px_w / float(dpi) * MM_PER_INCH, "PIL"
    if ext == ".pdf":
        try:
            from pypdf import PdfReader
        except Exception:
            try:
                from PyPDF2 import PdfReader
            except Exception:
                return None, "pypdf-missing"
        box = PdfReader(path).pages[0].mediabox
        return float(box.width) / 72.0 * MM_PER_INCH, "pypdf"
    if ext == ".svg":
        return _measure_svg_width_mm(path)
    return None, f"unsupported-ext-{ext}"


def _measure_svg_width_mm(path):
    """解析 SVG 根元素 width 属性 -> mm。无依赖。"""
    import re
    import xml.etree.ElementTree as ET
    try:
        root = ET.parse(path).getroot()
    except Exception as e:
        return None, f"svg-parse-{e.__class__.__name__}"
    raw = root.get("width")
    if not raw:
        return None, "svg-no-width"
    m = re.match(r"\s*([0-9.]+)\s*([a-z%]*)", raw)
    if not m:
        return None, "svg-bad-width"
    val, unit = float(m.group(1)), m.group(2)
    factor = {"mm": 1.0, "cm": 10.0, "in": MM_PER_INCH,
              "pt": MM_PER_INCH / 72.0, "px": MM_PER_INCH / 96.0,
              "": MM_PER_INCH / 96.0}.get(unit)
    if factor is None:
        return None, f"svg-unit-{unit}"
    return val * factor, "svg"


def _check_measured(path, max_width_mm=None, journal=None, column="single",
                    tol_mm=0.5, verbose=True):
    """读回落盘文件真实宽度并对照目标栏宽。"""
    w_mm, backend = _measure_file_width_mm(path)
    report = {"path": path, "measured": True, "backend": backend,
              "ok": True, "problems": []}
    limit = max_width_mm
    if journal is not None:
        spec = JOURNAL_SPECS[journal.lower()]
        limit = spec.get(f"{column}_mm", limit)
        report["journal"] = journal.lower()
        report["column"] = column
    if w_mm is None:
        report["skipped"] = True
        report["reason"] = backend
        if verbose:
            print(f"[check_figure_size:measured] SKIP ({backend})  {report}")
        return report
    report["width_mm"] = round(w_mm, 2)
    if limit is not None:
        report["target_mm"] = limit
        # 精确栏宽: 实测宽度应严格等于目标(双向容差), 而非仅"不超上限"
        if abs(w_mm - limit) > tol_mm:
            report["ok"] = False
            report["problems"].append(
                f"实测宽度 {w_mm:.2f}mm 偏离目标栏宽 {limit}mm "
                f"(差 {w_mm - limit:+.2f}mm, 容差 {tol_mm}mm)")
    if verbose:
        status = "OK" if report["ok"] else "FAIL"
        print(f"[check_figure_size:measured] {status}  {report}")
    return report


def check_export_compliance(path, journal, column="single", verbose=False):
    """落盘文件的合规校验：消费 JOURNAL_SPECS 里此前录了却没人用的字段——
    实测 dpi≥min_dpi、文件体积≤max_file_mb、高度≤max_height_px、格式∈preferred_formats。
    只对能从文件读出的维度判定，读不出的标 skip 不臆断。返回 {ok, problems, checks}。"""
    import os as _os
    j = journal.lower()
    if j not in JOURNAL_SPECS:
        return {"ok": True, "skipped": f"custom/未知刊 {journal}，无合规规格可校验", "problems": []}
    spec = JOURNAL_SPECS[j]
    problems, checks = [], {}
    ext = _os.path.splitext(path)[1].lstrip(".").lower()

    # 1) 格式是否在 preferred_formats
    pref = spec.get("preferred_formats", ())
    checks["format"] = {"ext": ext, "preferred": list(pref)}
    if pref and ext not in pref:
        problems.append(f"格式 .{ext} 不在 {j} 首选 {pref}（投稿可能被要求转格式）")

    # 2) 文件体积
    mb = _os.path.getsize(path) / 1e6 if _os.path.exists(path) else None
    if mb is not None:
        checks["file_mb"] = round(mb, 2)
        cap = spec.get("max_file_mb")
        if cap and mb > cap:
            problems.append(f"文件 {mb:.1f}MB 超 {j} 上限 {cap}MB")

    # 3) 位图的 dpi 与高度（PNG/TIFF 可读，矢量跳过）
    if ext in ("png", "tiff", "tif"):
        try:
            from PIL import Image
            with Image.open(path) as im:
                w_px, h_px = im.size
                dpi = im.info.get("dpi", (None, None))[0]
            checks["pixels"] = {"w": w_px, "h": h_px, "dpi": dpi}
            min_dpi = spec.get("min_dpi_halftone") or spec.get("min_dpi_line")
            if dpi and min_dpi and dpi < min_dpi - 1:
                problems.append(f"实测 dpi={dpi} < {j} 下限 {min_dpi}")
            max_h = spec.get("max_height_px")
            if max_h and h_px > max_h:
                problems.append(f"高度 {h_px}px 超 {j} 上限 {max_h}px")
        except ImportError:
            checks["pixels"] = "skip(无 Pillow)"
        except Exception as e:
            checks["pixels"] = f"skip({e.__class__.__name__})"
    else:
        checks["pixels"] = f"skip(矢量/不可读 dpi: .{ext})"

    report = {"path": path, "journal": j, "ok": len(problems) == 0,
              "problems": problems, "checks": checks}
    if verbose:
        print(f"[check_export_compliance] {'OK' if report['ok'] else 'FAIL'}  {report}")
    return report


def _demo_and_selfcheck():
    """产 demo 图, 跑函数, 断言关键不变量。"""
    import numpy as np
    here = os.path.dirname(os.path.abspath(__file__))
    style = os.path.join(here, "..", "assets", "publication.mplstyle")
    if os.path.exists(style):
        plt.style.use(style)
    rng = np.random.default_rng(0)
    x = np.linspace(0, 2 * np.pi, 100)
    fig, ax = plt.subplots(figsize=(3.5, 2.6))
    ax.plot(x, np.sin(x), label="sin")
    ax.plot(x, np.cos(x), label="cos", linestyle="--")
    ax.fill_between(x, np.sin(x) - 0.1, np.sin(x) + 0.1, alpha=0.2)
    ax.set_xlabel("phase (rad)")
    ax.set_ylabel("amplitude (a.u.)")
    ax.set_title("a", loc="left")
    ax.legend()

    outdir = os.path.join(here, "..", "examples", "_export_demo")
    base = os.path.join(outdir, "demo_export")
    written = save_publication_figure(fig, base, formats=("pdf", "png", "svg"))
    assert all(os.path.exists(p) and os.path.getsize(p) > 0 for p in written), written
    print("[demo] save_publication_figure ->", [os.path.basename(p) for p in written])

    # 按 Nature 单栏导出并校验
    fig2, ax2 = plt.subplots(figsize=(5.0, 4.0))
    ax2.bar(["A", "B", "C"], [3, 5, 2])
    ax2.set_ylabel("count")
    nat_base = os.path.join(outdir, "demo_nature")
    w2, info = save_for_journal(fig2, nat_base,
                                journal="nature", column="single",
                                formats=("pdf", "png"))
    assert abs(info["width_mm"] - 89.0) < 0.6, info
    print("[demo] save_for_journal nature/single ->", info["width_mm"], "mm",
          [os.path.basename(p) for p in w2])

    # 关键回归断言: 读回落盘文件的真实物理宽度, 而非由设定值反算的 width_mm。
    # bbox_inches="tight" 曾在此静默裁剪改变栏宽; 现 save_for_journal 传 None。
    for fmt in ("png", "pdf"):
        fpath = f"{nat_base}.{fmt}"
        rep_m = check_figure_size(fig2, journal="nature", column="single",
                                  measured=True, path=fpath, tol_mm=0.5)
        if rep_m.get("skipped"):
            print(f"[demo] measured {fmt}: SKIP ({rep_m['reason']}) — 环境缺读取后端")
            continue
        assert rep_m["ok"], rep_m
        assert abs(rep_m["width_mm"] - 89.0) < 0.5, rep_m
        print(f"[demo] 导出后读回实测宽度({fmt})={rep_m['width_mm']}mm "
              f"== 目标栏宽 89.0mm  [backend={rep_m['backend']}] PASS")

    rep_ok = check_figure_size(fig2, journal="nature", column="single", verbose=False)
    assert rep_ok["ok"], rep_ok

    # FD-2 字体落空检查：info 带 font 字段，结构完整（CI 无 Arial 时 fell_back=True 且有 warning）
    assert "font" in info and "fell_back" in info["font"], info.get("font")
    if info["font"]["fell_back"]:
        assert info["font"]["warning"], "回退时应有 warning"
        print(f"[demo] 字体落空检查: 回退到 '{info['font']['resolved']}' 并告警 PASS")
    else:
        print(f"[demo] 字体落空检查: 首选字体 '{info['font']['resolved']}' 可用 PASS")

    # FD-3 导出合规校验：消费 dpi/体积/格式/高度字段
    png_path = f"{nat_base}.png"
    if os.path.exists(png_path):
        comp = check_export_compliance(png_path, "nature", "single")
        assert "checks" in comp and "format" in comp["checks"], comp
        print(f"[demo] check_export_compliance(nature png): ok={comp['ok']} "
              f"problems={comp['problems'][:1]}")
    # plos 只收 tiff/eps，png 应被判格式不合规（消费 preferred_formats）
    if os.path.exists(png_path):
        comp_plos = check_export_compliance(png_path, "plos", "single")
        assert any("格式" in p for p in comp_plos["problems"]), comp_plos
        print("[demo] check_export_compliance(plos, png): 正确判格式不合规 PASS")
    # custom/未知刊跳过合规校验不崩
    assert check_export_compliance(png_path, "custom").get("skipped") if os.path.exists(png_path) else True

    # 故意造一个超宽图, 应 FAIL
    fig3, ax3 = plt.subplots(figsize=(10, 4))
    ax3.plot([0, 1], [0, 1])
    rep_bad = check_figure_size(fig3, journal="nature", column="single", verbose=False)
    assert not rep_bad["ok"], rep_bad
    print("[demo] check_figure_size: 合规图 OK, 超宽图正确判 FAIL")

    # R1.2: MDPI 单栏(170mm)导出并读回实测复核
    fig4, ax4 = plt.subplots(figsize=(6.0, 4.0))
    ax4.plot([0, 1, 2], [1, 3, 2])
    ax4.set_xlabel("x"); ax4.set_ylabel("y")
    mdpi_base = os.path.join(outdir, "demo_mdpi")
    w4, info4 = save_for_journal(fig4, mdpi_base, journal="mdpi", column="single",
                                 formats=("pdf", "png"))
    assert abs(info4["width_mm"] - 170.0) < 0.6, info4
    print("[demo] save_for_journal mdpi/single ->", info4["width_mm"], "mm")

    # R1.2: custom_mm 逃生通道(中文刊场景, 如农业工程学报正文栏宽 84mm)
    fig5, ax5 = plt.subplots(figsize=(5.0, 3.5))
    ax5.bar(["甲", "乙"], [2, 4])
    cust_base = os.path.join(outdir, "demo_custom")
    w5, info5 = save_for_journal(fig5, cust_base, journal="custom",
                                 custom_width_mm=84.0, formats=("pdf", "png"))
    assert abs(info5["width_mm"] - 84.0) < 0.6, info5
    rep5 = check_figure_size(fig5, journal="custom", custom_width_mm=84.0,
                             verbose=False)
    assert rep5["ok"] and rep5["max_width_mm"] == 84.0, rep5
    print("[demo] custom_width_mm=84 (中文刊逃生通道) ->", info5["width_mm"], "mm, check OK")

    plt.close("all")
    print("[selfcheck] ALL PASS, 输出目录:", os.path.abspath(outdir))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != "--selftest":
        raise SystemExit("usage: python figure_export.py [--selftest]")
    _demo_and_selfcheck()
