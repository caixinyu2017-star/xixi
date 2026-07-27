# -*- coding: utf-8 -*-
"""对 pandoc 生成的 docx 做期刊化排版后处理：中文字体、字号、
版面、表格与题注样式等。"""
import re
import sys
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

SRC = sys.argv[1] if len(sys.argv) > 1 else "paper.docx"

doc = Document(SRC)

# ---------- 页面：A4，常规页边距 ----------
for sec in doc.sections:
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.top_margin = sec.bottom_margin = Cm(2.54)
    sec.left_margin = sec.right_margin = Cm(2.6)


def set_fonts(style, east="宋体", ascii_font="Times New Roman", size=None,
              bold=None, color_black=True):
    f = style.font
    if size is not None:
        f.size = Pt(size)
    if bold is not None:
        f.bold = bold
    f.italic = False
    f.name = ascii_font
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = rpr.makeelement(qn("w:rFonts"), {})
        rpr.append(rfonts)
    rfonts.set(qn("w:ascii"), ascii_font)
    rfonts.set(qn("w:hAnsi"), ascii_font)
    rfonts.set(qn("w:eastAsia"), east)
    if color_black:
        f.color.rgb = RGBColor(0, 0, 0)


def para_fmt(style, align=None, first_indent=None, before=None, after=None,
             line=None):
    pf = style.paragraph_format
    if align is not None:
        pf.alignment = align
    if first_indent is not None:
        pf.first_line_indent = first_indent
    if before is not None:
        pf.space_before = Pt(before)
    if after is not None:
        pf.space_after = Pt(after)
    if line is not None:
        pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        pf.line_spacing = line


S = {s.name: s for s in doc.styles}

# ---------- 基础正文：段前段后间距一律为 0 ----------
for name in ("Normal", "Body Text", "First Paragraph",
             "Body Text First Indent", "Plain Text"):
    if name in S:
        set_fonts(S[name], east="宋体", size=10.5)
        para_fmt(S[name], align=WD_ALIGN_PARAGRAPH.JUSTIFY, before=0, after=0,
                 line=1.5)
for name in ("Body Text", "First Paragraph"):
    if name in S:
        para_fmt(S[name], first_indent=Cm(0.74))

# ---------- 标题层级 ----------
if "Heading 1" in S:
    set_fonts(S["Heading 1"], east="黑体", ascii_font="Times New Roman",
              size=12, bold=True)
    para_fmt(S["Heading 1"], align=WD_ALIGN_PARAGRAPH.LEFT, before=10,
             after=6, line=1.5, first_indent=Cm(0))
for name in ("Heading 2", "Heading 3"):
    if name in S:
        set_fonts(S[name], east="黑体", ascii_font="Times New Roman",
                  size=10.5, bold=True)
        para_fmt(S[name], align=WD_ALIGN_PARAGRAPH.LEFT, before=6, after=3,
                 line=1.5, first_indent=Cm(0))

# ---------- 自定义样式 ----------
custom = {
    "TitleCN": dict(east="黑体", size=15, bold=True,
                    align=WD_ALIGN_PARAGRAPH.CENTER, before=6, after=12),
    "AuthorCN": dict(east="仿宋", size=10.5, bold=False,
                     align=WD_ALIGN_PARAGRAPH.CENTER, before=0, after=3),
    "AffilCN": dict(east="宋体", size=9, bold=False,
                    align=WD_ALIGN_PARAGRAPH.CENTER, before=0, after=10),
    "AbstractCN": dict(east="楷体", size=9, bold=False,
                       align=WD_ALIGN_PARAGRAPH.JUSTIFY, before=0, after=4),
    "TableNote": dict(east="宋体", size=8, bold=False,
                      align=WD_ALIGN_PARAGRAPH.LEFT, before=2, after=8),
    "RefItem": dict(east="宋体", size=9, bold=False,
                    align=WD_ALIGN_PARAGRAPH.JUSTIFY, before=0, after=2),
    "Table Caption": dict(east="黑体", size=9, bold=True,
                          align=WD_ALIGN_PARAGRAPH.CENTER, before=8, after=3),
    "Image Caption": dict(east="黑体", size=9, bold=True,
                          align=WD_ALIGN_PARAGRAPH.CENTER, before=3, after=8),
    "Captioned Figure": dict(east="宋体", size=10.5, bold=False,
                             align=WD_ALIGN_PARAGRAPH.CENTER, before=8,
                             after=0),
    "Compact": dict(east="宋体", size=9, bold=False,
                    align=WD_ALIGN_PARAGRAPH.CENTER, before=0, after=0),
}
for name, cfg in custom.items():
    if name not in S:
        continue
    set_fonts(S[name], east=cfg["east"], size=cfg["size"], bold=cfg["bold"])
    para_fmt(S[name], align=cfg["align"], before=cfg["before"],
             after=cfg["after"], line=1.2, first_indent=Cm(0))

# ---------- 表格：三线表、满栏宽、居中、单元格对齐 ----------
TOP_BOTTOM_SZ = "12"          # 顶线与底线：1.5 磅（单位为 1/8 磅）
HEADER_SZ = "6"               # 栏目线：0.75 磅


def _border(parent, tag, val, sz=None):
    attrs = {qn("w:val"): val, qn("w:color"): "000000"}
    if sz is not None:
        attrs[qn("w:sz")] = sz
        attrs[qn("w:space")] = "0"
    parent.append(parent.makeelement(qn("w:" + tag), attrs))


TEXT_TWIPS = 8957                       # 版心宽度 15.8 cm 折合缇
CELL_MARGIN = 216                       # 单元格左右内边距合计
PAD = 110                               # 留白余量，避免恰好触界而折行
UNIT = 105                              # 9 磅字下一个半角字符的宽度（含余量）
UNBREAK = re.compile(
    r"[0-9A-Za-z.,%*+\-−–—()（）:：/×±≤≥\u0370-\u03ff\u2070-\u209f]+")


def _dw(s):
    """字符串的显示宽度，以半角字符为 1 个单位。"""
    return sum(2 if ord(ch) > 0x2E80 else 1 for ch in s)


def col_widths(tbl):
    """按各列内容计算列宽：先保证最长不可断串不被拆行，余量再按需求比例分配。"""
    ncol = len(tbl.columns)
    need, mini = [], []
    for j in range(ncol):
        full = brk = 0
        for row in tbl.rows:
            if j >= len(row.cells):
                continue
            t = row.cells[j].text.strip()
            full = max(full, _dw(t))
            for m in UNBREAK.findall(t):
                brk = max(brk, _dw(m))
        need.append(max(full, 3))
        mini.append(max(brk, 3))
    base = [m * UNIT + CELL_MARGIN + PAD for m in mini]
    if sum(base) > TEXT_TWIPS:                     # 极端情形：按比例压缩
        k = TEXT_TWIPS / sum(base)
        return [int(b * k) for b in base]
    extra = TEXT_TWIPS - sum(base)
    gap = [max(need[j] - mini[j], 0) * UNIT for j in range(ncol)]
    tot = sum(gap)
    out = ([base[j] + int(extra * gap[j] / tot) for j in range(ncol)]
           if tot else [b + extra // ncol for b in base])
    # 单列宽度封顶，溢出的宽度均摊给其余各列，避免首列独占版面
    cap = int(TEXT_TWIPS * (0.45 if ncol >= 3 else 0.62))
    surplus = sum(max(0, w - cap) for w in out)
    if surplus:
        free = [j for j, w in enumerate(out) if w <= cap]
        out = [min(w, cap) for w in out]
        if free:
            for j in free:
                out[j] += surplus // len(free)
    out[-1] += TEXT_TWIPS - sum(out)
    return out


for tbl in doc.tables:
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tblPr = tbl._tbl.tblPr
    for tag in ("w:tblW", "w:tblLayout", "w:tblBorders", "w:tblStyle"):
        for old in tblPr.findall(qn(tag)):
            tblPr.remove(old)
    tblPr.append(tblPr.makeelement(qn("w:tblW"),
                                   {qn("w:w"): str(TEXT_TWIPS),
                                    qn("w:type"): "dxa"}))
    tblPr.append(tblPr.makeelement(qn("w:tblLayout"), {qn("w:type"): "fixed"}))
    ws = col_widths(tbl)
    grid = tbl._tbl.find(qn("w:tblGrid"))
    if grid is not None:
        for gc, wd in zip(grid.findall(qn("w:gridCol")), ws):
            gc.set(qn("w:w"), str(wd))
    for row in tbl.rows:
        for j, cell in enumerate(row.cells):
            if j >= len(ws):
                continue
            tcPr = cell._tc.get_or_add_tcPr()
            for old in tcPr.findall(qn("w:tcW")):
                tcPr.remove(old)
            tcPr.append(tcPr.makeelement(qn("w:tcW"),
                                         {qn("w:w"): str(ws[j]),
                                          qn("w:type"): "dxa"}))
    # 三线表：仅保留顶线、栏目线与底线，取消所有竖线与其余横线
    bd = tblPr.makeelement(qn("w:tblBorders"), {})
    _border(bd, "top", "single", TOP_BOTTOM_SZ)
    _border(bd, "left", "none")
    _border(bd, "bottom", "single", TOP_BOTTOM_SZ)
    _border(bd, "right", "none")
    _border(bd, "insideH", "none")
    _border(bd, "insideV", "none")
    tblPr.append(bd)
    nrow = len(tbl.rows)
    for ri, row in enumerate(tbl.rows):
        for cell in row.cells:
            tcPr = cell._tc.get_or_add_tcPr()
            for old in tcPr.findall(qn("w:tcBorders")):
                tcPr.remove(old)
            tb = tcPr.makeelement(qn("w:tcBorders"), {})
            if ri == 0:
                _border(tb, "top", "single", TOP_BOTTOM_SZ)
                _border(tb, "bottom", "single", HEADER_SZ)
            elif ri == nrow - 1:
                _border(tb, "top", "none")
                _border(tb, "bottom", "single", TOP_BOTTOM_SZ)
            else:
                _border(tb, "top", "none")
                _border(tb, "bottom", "none")
            _border(tb, "left", "none")
            _border(tb, "right", "none")
            tcPr.append(tb)
    for ri, row in enumerate(tbl.rows):
        trPr = row._tr.get_or_add_trPr()
        # 禁止表格行跨页断开；首行在跨页时重复
        trPr.append(trPr.makeelement(qn("w:cantSplit"), {}))
        if ri == 0:
            trPr.append(trPr.makeelement(qn("w:tblHeader"), {}))
        for cell in row.cells:
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(1)
                p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE

# ---------- 插图：按版心宽度等比缩放 ----------
TEXT_WIDTH = Cm(15.8)
for shape in doc.inline_shapes:
    if shape.width and shape.width != TEXT_WIDTH:
        ratio = TEXT_WIDTH / shape.width
        shape.width = TEXT_WIDTH
        shape.height = int(shape.height * ratio)

# ---------- 清除正文段落上的直接间距设置，确保段前段后均为 0 ----------
BODY_STYLES = {"Normal", "Body Text", "First Paragraph",
               "Body Text First Indent", "Plain Text"}
for p in doc.paragraphs:
    if p.style.name in BODY_STYLES:
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)

doc.save(SRC)
print("finalize done:", SRC)
