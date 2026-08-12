# -*- coding: utf-8 -*-
"""用 OMML（Office Math Markup Language）构造 Word 原生公式。

只实现本方案用到的少量结构：变量、上下标、分式、根式、求和、括号。
生成的公式在 Word 中可编辑、可复制，优于以纯文本模拟数学式。
"""
from xml.sax.saxutils import escape

from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.oxml import OxmlElement

SZ = 24  # 半磅值，24 = 小四（12 pt）


def r(text, upright=False, sz=SZ):
    """数学运行块。upright=True 用于函数名与文字（如 exp、softmax）。"""
    sty = '<m:rPr><m:sty m:val="p"/></m:rPr>' if upright else ""
    return (f'<m:r>{sty}<w:rPr><w:rFonts w:ascii="Cambria Math" '
            f'w:hAnsi="Cambria Math"/><w:sz w:val="{sz}"/>'
            f'<w:szCs w:val="{sz}"/></w:rPr>'
            f'<m:t xml:space="preserve">{escape(text)}</m:t></m:r>')


def sub(base, s):
    return f"<m:sSub><m:e>{base}</m:e><m:sub>{s}</m:sub></m:sSub>"


def sup(base, s):
    return f"<m:sSup><m:e>{base}</m:e><m:sup>{s}</m:sup></m:sSup>"


def subsup(base, sb, sp):
    return (f"<m:sSubSup><m:e>{base}</m:e><m:sub>{sb}</m:sub>"
            f"<m:sup>{sp}</m:sup></m:sSubSup>")


def frac(num, den):
    return f"<m:f><m:num>{num}</m:num><m:den>{den}</m:den></m:f>"


def sqrt(e):
    return ('<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/>'
            f"<m:e>{e}</m:e></m:rad>")


def nary(e, lower="", chr_="∑"):
    """求和号：仅带下标。"""
    return (f'<m:nary><m:naryPr><m:chr m:val="{chr_}"/>'
            '<m:limLoc m:val="undOvr"/><m:supHide m:val="1"/></m:naryPr>'
            f"<m:sub>{lower}</m:sub><m:sup/><m:e>{e}</m:e></m:nary>")


def d(e, beg="(", end=")"):
    return (f'<m:d><m:dPr><m:begChr m:val="{beg}"/>'
            f'<m:endChr m:val="{end}"/></m:dPr><m:e>{e}</m:e></m:d>')


def math_paragraph(doc, omml_body, number, cn_font="宋体"):
    """插入一行居中显示的公式，右侧以制表位对齐公式编号。"""
    p = doc.add_paragraph()
    pf = p.paragraph_format
    from docx.shared import Pt
    pf.space_before = Pt(6)
    pf.space_after = Pt(6)
    pf.line_spacing = 1.5

    tabs = OxmlElement("w:tabs")
    for pos, val in ((4100, "center"), (8300, "right")):
        t = OxmlElement("w:tab")
        t.set(qn("w:val"), val)
        t.set(qn("w:pos"), str(pos))
        tabs.append(t)
    pPr = p._p.get_or_add_pPr()
    pPr.insert_element_before(
        tabs, "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap",
        "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN",
        "w:bidi", "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind",
        "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap", "w:jc",
        "w:textDirection", "w:textAlignment", "w:textboxTightWrap",
        "w:outlineLvl", "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr",
        "w:pPrChange")

    lead = parse_xml(f"<w:r {nsdecls('w')}><w:tab/></w:r>")
    p._p.append(lead)
    p._p.append(parse_xml(
        f"<m:oMath {nsdecls('m', 'w')}>{omml_body}</m:oMath>"))
    tail = parse_xml(
        f'<w:r {nsdecls("w")}><w:rPr><w:rFonts w:ascii="Times New Roman" '
        f'w:hAnsi="Times New Roman" w:eastAsia="{cn_font}"/>'
        f'<w:sz w:val="{SZ}"/><w:szCs w:val="{SZ}"/></w:rPr>'
        f"<w:tab/><w:t>（{number}）</w:t></w:r>")
    p._p.append(tail)
    return p
