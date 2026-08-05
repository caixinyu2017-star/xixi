#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""构造与原文体例一致的 Word 块：正文段、标题、题注（含 SEQ 域）、图、三线表。
新增内容一律红色 FF0000；引号字符强制宋体。"""
import os, re, copy
from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
WP = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
PIC = 'http://schemas.openxmlformats.org/drawingml/2006/picture'
NSMAP = {'w': W, 'r': R, 'wp': WP, 'a': A, 'pic': PIC}
RED = 'FF0000'
QUOTES = '“”‘’'


def q(t):
    return '{%s}%s' % (W, t)


def X(s):
    """把带 w:/r:/wp:/a:/pic: 前缀的片段解析成元素。"""
    decl = ' '.join('xmlns:%s="%s"' % (k, v) for k, v in NSMAP.items())
    s = s.replace('<ROOT>', '<ROOT %s>' % decl)
    return etree.fromstring(s)


def _runs(text, red=True, bold=False, songti_quotes=True, sz=None):
    """把一段文字切成若干 run：引号字符单独成 run 且用宋体。"""
    out = []
    if songti_quotes:
        segs = [x for x in re.split('([' + QUOTES + '])', text) if x != '']
    else:
        segs = [text]
    for seg in segs:
        isq = seg in QUOTES
        rpr = ['<w:rPr>']
        if isq:
            rpr.append('<w:rFonts w:hint="eastAsia" w:ascii="宋体" w:hAnsi="宋体"'
                       ' w:eastAsia="宋体" w:cs="宋体"/>')
        else:
            rpr.append('<w:rFonts w:hint="eastAsia"/>')
        if bold:
            rpr.append('<w:b/><w:bCs/>')
        if sz:
            rpr.append('<w:sz w:val="%s"/><w:szCs w:val="%s"/>' % (sz, sz))
        if red:
            rpr.append('<w:color w:val="%s"/>' % RED)
        rpr.append('<w:lang w:eastAsia="zh-CN"/></w:rPr>')
        esc = (seg.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))
        out.append('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (''.join(rpr), esc))
    return ''.join(out)


def para(text, red=True, indent=480, jc=None, bold=False):
    ppr = ['<w:pPr>']
    if indent is not None:
        ppr.append('<w:ind w:firstLine="%d"/>' % indent)
    else:
        ppr.append('<w:ind w:firstLineChars="0" w:firstLine="0"/>')
    if jc:
        ppr.append('<w:jc w:val="%s"/>' % jc)
    ppr.append('<w:rPr>')
    if red:
        ppr.append('<w:color w:val="%s"/>' % RED)
    ppr.append('<w:lang w:eastAsia="zh-CN"/></w:rPr></w:pPr>')
    return X('<ROOT><w:p>%s%s</w:p></ROOT>' % (''.join(ppr), _runs(text, red=red, bold=bold)))[0]


def heading(text, level=2, red=True):
    if level == 2:
        ppr = ('<w:pPr><w:pStyle w:val="2"/><w:spacing w:before="312" w:after="312"/>'
               '<w:rPr>%s<w:lang w:eastAsia="zh-CN"/></w:rPr></w:pPr>')
    else:
        ppr = ('<w:pPr><w:pStyle w:val="3"/><w:spacing w:before="312" w:after="312"/>'
               '<w:ind w:firstLine="480"/>'
               '<w:rPr>%s<w:lang w:eastAsia="zh-CN"/></w:rPr></w:pPr>')
    ppr = ppr % ('<w:color w:val="%s"/>' % RED if red else '')
    return X('<ROOT><w:p>%s%s</w:p></ROOT>' % (ppr, _runs(text, red=red)))[0]


_SEQ_TMPL = (
    '<w:r><w:rPr>{C}<w:lang w:eastAsia="zh-CN"/></w:rPr>'
    '<w:fldChar w:fldCharType="begin"/></w:r>'
    '<w:r><w:rPr>{C}<w:lang w:eastAsia="zh-CN"/></w:rPr>'
    '<w:instrText xml:space="preserve"> SEQ {KIND} \\* ARABIC \\s 1 </w:instrText></w:r>'
    '<w:r><w:rPr>{C}<w:lang w:eastAsia="zh-CN"/></w:rPr>'
    '<w:fldChar w:fldCharType="separate"/></w:r>'
    '<w:r><w:rPr>{C}<w:noProof/><w:lang w:eastAsia="zh-CN"/></w:rPr>'
    '<w:t>{NUM}</w:t></w:r>'
    '<w:r><w:rPr>{C}<w:lang w:eastAsia="zh-CN"/></w:rPr>'
    '<w:fldChar w:fldCharType="end"/></w:r>')


def caption(kind, chap, num, text, red=True):
    """kind: '图' 或 '表'；chap 章号；num 该章内序号（作为域缓存值）。"""
    c = '<w:color w:val="%s"/>' % RED if red else ''
    head = ('<w:r><w:rPr><w:rFonts w:hint="eastAsia"/>%s<w:lang w:eastAsia="zh-CN"/></w:rPr>'
            '<w:t>%s</w:t></w:r>'
            '<w:r><w:rPr><w:rFonts w:hint="eastAsia"/>%s<w:lang w:eastAsia="zh-CN"/></w:rPr>'
            '<w:t xml:space="preserve"> </w:t></w:r>'
            '<w:r><w:rPr><w:rFonts w:hint="eastAsia"/>%s<w:lang w:eastAsia="zh-CN"/></w:rPr>'
            '<w:t>%d</w:t></w:r>'
            '<w:r><w:rPr>%s<w:lang w:eastAsia="zh-CN"/></w:rPr><w:noBreakHyphen/></w:r>'
            % (c, kind, c, c, chap, c))
    seq = _SEQ_TMPL.format(C=c, KIND=kind, NUM=num)
    tail = ('<w:r><w:rPr><w:rFonts w:hint="eastAsia"/>%s<w:lang w:eastAsia="zh-CN"/></w:rPr>'
            '<w:t xml:space="preserve"> </w:t></w:r>%s' % (c, _runs(text, red=red)))
    keep = '<w:keepNext/>' if kind == '表' else ''
    ppr = ('<w:pPr><w:pStyle w:val="a7"/>%s<w:ind w:firstLineChars="0" w:firstLine="0"/>'
           '<w:jc w:val="center"/><w:rPr>%s<w:lang w:eastAsia="zh-CN"/></w:rPr></w:pPr>'
           % (keep, c))
    return X('<ROOT><w:p>%s%s%s%s</w:p></ROOT>' % (ppr, head, seq, tail))[0]


_IMG = ('<w:p><w:pPr><w:keepNext/><w:widowControl w:val="0"/>'
        '<w:ind w:firstLineChars="0" w:firstLine="0"/><w:jc w:val="center"/></w:pPr>'
        '<w:r><w:rPr><w:noProof/><w:kern w:val="2"/><w:sz w:val="21"/>'
        '<w:szCs w:val="24"/><w:lang w:eastAsia="zh-CN"/></w:rPr>'
        '<w:drawing><wp:inline distT="0" distB="0" distL="114300" distR="114300">'
        '<wp:extent cx="{CX}" cy="{CY}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
        '<wp:docPr id="{ID}" name="图片 {ID}"/>'
        '<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>'
        '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic><pic:nvPicPr><pic:cNvPr id="{ID}" name="图片 {ID}"/>'
        '<pic:cNvPicPr><a:picLocks noChangeAspect="1"/></pic:cNvPicPr></pic:nvPicPr>'
        '<pic:blipFill><a:blip r:embed="{RID}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{CX}" cy="{CY}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:ln><a:noFill/></a:ln></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')


def image_para(rid, cx, cy, docpr_id):
    return X('<ROOT>%s</ROOT>' % _IMG.format(CX=cx, CY=cy, RID=rid, ID=docpr_id))[0]


def table(header, rows, red=True, total_w=8296):
    """三线表。header: list[str]；rows: list[list[str]]。"""
    ncol = len(header)
    # 按各列内容长度按比例分配列宽（压缩极差，并设下限）
    def wlen(s):
        return sum(2 if ord(c) > 127 else 1 for c in s)
    maxlen = []
    for ci in range(ncol):
        vals = [wlen(header[ci])]
        for r in rows:
            if ci < len(r):
                vals.append(wlen(r[ci]))
        maxlen.append(max(vals) or 1)
    weights = [m ** 0.62 for m in maxlen]
    tot = sum(weights)
    widths = [max(1150, int(total_w * w / tot)) for w in weights]
    # 归一化回 total_w
    scale = total_w / sum(widths)
    widths = [int(w * scale) for w in widths]
    widths[-1] = total_w - sum(widths[:-1])
    grid = ''.join('<w:gridCol w:w="%d"/>' % w for w in widths)

    def cell(txt, w, first_row, last_row, bold):
        if first_row:
            bd = ('<w:tcBorders><w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
                  '<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                  '<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
                  '<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/></w:tcBorders>')
        elif last_row:
            bd = ('<w:tcBorders><w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                  '<w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
                  '<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/></w:tcBorders>')
        else:
            bd = ('<w:tcBorders><w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                  '<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/></w:tcBorders>')
        jc = 'center' if (first_row or len(txt) <= 12) else 'left'
        return ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s<w:vAlign w:val="center"/></w:tcPr>'
                '<w:p><w:pPr><w:spacing w:line="240" w:lineRule="auto"/>'
                '<w:ind w:firstLineChars="0" w:firstLine="0"/><w:jc w:val="%s"/>'
                '<w:rPr><w:rFonts w:ascii="宋体" w:hAnsi="宋体"/><w:kern w:val="2"/>'
                '<w:sz w:val="21"/>%s<w:lang w:eastAsia="zh-CN"/></w:rPr></w:pPr>%s</w:p></w:tc>'
                % (w, bd, jc,
                   '<w:color w:val="%s"/>' % RED if red else '',
                   _runs(txt, red=red, bold=bold, sz='21')))

    trs = []
    nrow = 1 + len(rows)
    trs.append('<w:tr><w:trPr><w:tblHeader/><w:jc w:val="center"/></w:trPr>%s</w:tr>'
               % ''.join(cell(h, widths[i], True, nrow == 1, True) for i, h in enumerate(header)))
    for ri, row in enumerate(rows):
        cells = []
        for ci in range(ncol):
            txt = row[ci] if ci < len(row) else ''
            cells.append(cell(txt, widths[ci], False, ri == len(rows) - 1, False))
        trs.append('<w:tr><w:trPr><w:jc w:val="center"/></w:trPr>%s</w:tr>' % ''.join(cells))

    xml = ('<w:tbl><w:tblPr><w:tblStyle w:val="SanXian"/><w:tblW w:w="0" w:type="auto"/>'
           '<w:jc w:val="center"/>'
           '<w:tblBorders><w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
           '<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
           '<w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
           '<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
           '<w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
           '<w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/></w:tblBorders>'
           '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="0"'
           ' w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr>'
           '<w:tblGrid>%s</w:tblGrid>%s</w:tbl>' % (grid, ''.join(trs)))
    return X('<ROOT>%s</ROOT>' % xml)[0]


# ---------------------------------------------------------------- 关系与媒体
def add_image(unpacked, src_png, name):
    """复制图片到 media 并登记关系，返回 rId。"""
    dst = os.path.join(unpacked, 'word', 'media', name)
    if not os.path.exists(dst):
        import shutil
        shutil.copy(src_png, dst)
    relpath = os.path.join(unpacked, 'word', '_rels', 'document.xml.rels')
    t = etree.parse(relpath)
    root = t.getroot()
    RNS = 'http://schemas.openxmlformats.org/package/2006/relationships'
    for rel in root:
        if rel.get('Target') == 'media/' + name:
            return rel.get('Id')
    used = {r.get('Id') for r in root}
    n = 200
    while 'rId%d' % n in used:
        n += 1
    rid = 'rId%d' % n
    e = etree.SubElement(root, '{%s}Relationship' % RNS)
    e.set('Id', rid)
    e.set('Type', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image')
    e.set('Target', 'media/' + name)
    t.write(relpath, xml_declaration=True, encoding='UTF-8', standalone=True)
    return rid
