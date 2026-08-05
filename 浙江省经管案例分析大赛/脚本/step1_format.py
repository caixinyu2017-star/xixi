#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第一阶段格式化：
  A. 全文直引号 -> 中文弯引号，并把所有引号字符单独成 run 且强制宋体
  B. 题注样式 a7 -> 五号(sz=21) 黑体
  C. 全部表格改为三线表（新建 SanXian 表格样式 + 清除条件格式/底纹/白字）
"""
import re, sys, copy
from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}
def q(t): return '{%s}%s' % (W, t)

DOC = 'unpacked/word/document.xml'
STY = 'unpacked/word/styles.xml'

# ---------------------------------------------------------------- A. 引号
def normalize_quotes(root):
    """按段落逐个处理：直引号配对成中文弯引号；所有引号字符独立成 run 并设宋体。"""
    n_conv = 0
    n_font = 0
    for para in root.iter(q('p')):
        # 收集该段落内、直接位于 w:r 下的 w:t（跳过 instrText / delText）
        items = []  # (run, t_element)
        for r in para.iter(q('r')):
            for t in r.findall(q('t')):
                items.append((r, t))
        if not items:
            continue
        # --- 直引号配对 ---
        dq_open = True
        sq_open = True
        for r, t in items:
            s = t.text or ''
            if '"' in s or "'" in s:
                out = []
                for ch in s:
                    if ch == '"':
                        out.append('“' if dq_open else '”')
                        dq_open = not dq_open
                        n_conv += 1
                    elif ch == "'":
                        out.append('‘' if sq_open else '’')
                        sq_open = not sq_open
                        n_conv += 1
                    else:
                        out.append(ch)
                t.text = ''.join(out)

        # --- 引号字符拆出独立 run 并设宋体 ---
        QUOTES = '“”‘’'
        for r, t in list(items):
            s = t.text or ''
            if not any(c in s for c in QUOTES):
                continue
            # 已经是纯引号 run：直接改字体
            if all(c in QUOTES for c in s):
                set_songti(r)
                n_font += 1
                continue
            # 需要拆分：把 t 所在 run 按引号切成多段
            parent = r.getparent()
            idx = list(parent).index(r)
            # 只处理 run 中仅含这一个 w:t 且无 drawing 等复杂子元素的情况
            others = [c for c in r if c.tag not in (q('rPr'), q('t'))]
            if others or len(r.findall(q('t'))) != 1:
                set_songti(r)
                n_font += 1
                continue
            # 英文撇号（如 China’s / farmers’）不是中文引号，保持原西文字体
            keep = set()
            for mi, ch in enumerate(s):
                if ch == '’':
                    prev = s[mi - 1] if mi > 0 else ''
                    nxt = s[mi + 1] if mi + 1 < len(s) else ''
                    if (prev.isascii() and prev.isalpha()) and (nxt == '' or nxt.isascii()):
                        keep.add(mi)
            if keep and all(c not in '“”‘' for c in s) and \
               len([1 for c in s if c == '’']) == len(keep):
                continue  # 整段只含英文撇号，跳过

            segs = re.split('([' + QUOTES + '])', s)
            segs = [x for x in segs if x != '']
            new_runs = []
            for seg in segs:
                nr = copy.deepcopy(r)
                nt = nr.find(q('t'))
                nt.text = seg
                if seg.strip() != seg or seg == ' ':
                    nt.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                if seg in QUOTES:
                    set_songti(nr)
                    n_font += 1
                new_runs.append(nr)
            for k, nr in enumerate(new_runs):
                parent.insert(idx + k, nr)
            parent.remove(r)
    return n_conv, n_font


def set_songti(run):
    rPr = run.find(q('rPr'))
    if rPr is None:
        rPr = etree.SubElement(run, q('rPr'))
        run.remove(rPr)
        run.insert(0, rPr)
    rf = rPr.find(q('rFonts'))
    if rf is None:
        rf = etree.Element(q('rFonts'))
        rPr.insert(0, rf)
    for a in ('asciiTheme', 'hAnsiTheme', 'eastAsiaTheme', 'cstheme'):
        if rf.get(q(a)) is not None:
            del rf.attrib[q(a)]
    rf.set(q('ascii'), '宋体')
    rf.set(q('hAnsi'), '宋体')
    rf.set(q('eastAsia'), '宋体')
    rf.set(q('cs'), '宋体')
    rf.set(q('hint'), 'eastAsia')


# ---------------------------------------------------------------- B. 题注样式
def fix_caption_style(sroot):
    for st in sroot.findall(q('style')):
        if st.get(q('styleId')) == 'a7':
            rPr = st.find(q('rPr'))
            if rPr is None:
                rPr = etree.SubElement(st, q('rPr'))
            rf = rPr.find(q('rFonts'))
            if rf is None:
                rf = etree.Element(q('rFonts'))
                rPr.insert(0, rf)
            for a in ('asciiTheme', 'hAnsiTheme', 'eastAsiaTheme', 'cstheme'):
                if rf.get(q(a)) is not None:
                    del rf.attrib[q(a)]
            rf.set(q('ascii'), 'Times New Roman')
            rf.set(q('hAnsi'), 'Times New Roman')
            rf.set(q('eastAsia'), '黑体')
            rf.set(q('cs'), 'Times New Roman')
            for tag, val in (('sz', '21'), ('szCs', '21')):
                e = rPr.find(q(tag))
                if e is None:
                    e = etree.SubElement(rPr, q(tag))
                e.set(q('val'), val)
            # 保证 b 不被继承成粗体
            return True
    return False


SANXIAN = '''<w:style xmlns:w="%s" w:type="table" w:customStyle="1" w:styleId="SanXian">
<w:name w:val="三线表"/><w:basedOn w:val="a5"/><w:uiPriority w:val="50"/><w:qFormat/>
<w:tblPr><w:tblBorders>
<w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/>
<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>
<w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000"/>
<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>
<w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>
<w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>
</w:tblBorders></w:tblPr>
<w:tblStylePr w:type="firstRow"><w:rPr><w:b/><w:bCs/></w:rPr><w:tblPr/>
<w:tcPr><w:tcBorders>
<w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/>
<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>
</w:tcBorders><w:shd w:val="clear" w:color="auto" w:fill="auto"/></w:tcPr></w:tblStylePr>
</w:style>''' % W


def add_sanxian_style(sroot):
    if any(s.get(q('styleId')) == 'SanXian' for s in sroot.findall(q('style'))):
        return
    sroot.append(etree.fromstring(SANXIAN))


def to_three_line_tables(root):
    n = 0
    for tbl in root.iter(q('tbl')):
        n += 1
        tblPr = tbl.find(q('tblPr'))
        if tblPr is None:
            tblPr = etree.Element(q('tblPr'))
            tbl.insert(0, tblPr)
        ts = tblPr.find(q('tblStyle'))
        if ts is None:
            ts = etree.Element(q('tblStyle'))
            tblPr.insert(0, ts)
        ts.set(q('val'), 'SanXian')
        # 显式边框，避免依赖样式解析差异
        old = tblPr.find(q('tblBorders'))
        if old is not None:
            tblPr.remove(old)
        borders = etree.fromstring(
            '<w:tblBorders xmlns:w="%s">'
            '<w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
            '<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            '<w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
            '<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            '<w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            '<w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
            '</w:tblBorders>' % W)
        # tblBorders 须位于 tblStyle/tblpPr/tblOverlap/bidiVisual/tblStyleRowBandSize/
        # tblStyleColBandSize/tblW/jc/tblCellSpacing/tblInd 之后
        after = [q(t) for t in ('tblStyle','tblpPr','tblOverlap','bidiVisual',
                                'tblStyleRowBandSize','tblStyleColBandSize',
                                'tblW','jc','tblCellSpacing','tblInd')]
        pos = 0
        for i, c in enumerate(tblPr):
            if c.tag in after:
                pos = i + 1
        tblPr.insert(pos, borders)

        # 清条件格式
        for cnf in list(tbl.iter(q('cnfStyle'))):
            cnf.getparent().remove(cnf)
        # 清底纹
        for shd in list(tbl.iter(q('shd'))):
            shd.getparent().remove(shd)
        # 白字改黑
        for col in list(tbl.iter(q('color'))):
            if (col.get(q('val')) or '').upper() in ('FFFFFF', 'FFF'):
                col.set(q('val'), '000000')
                if col.get(q('themeColor')) is not None:
                    del col.attrib[q('themeColor')]
        # 首行加下框线、其余行去内框线
        rows = tbl.findall(q('tr'))
        for ri, tr in enumerate(rows):
            for tc in tr.findall(q('tc')):
                tcPr = tc.find(q('tcPr'))
                if tcPr is None:
                    tcPr = etree.Element(q('tcPr'))
                    tc.insert(0, tcPr)
                ob = tcPr.find(q('tcBorders'))
                if ob is not None:
                    tcPr.remove(ob)
                if ri == 0:
                    nb = etree.fromstring(
                        '<w:tcBorders xmlns:w="%s">'
                        '<w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
                        '<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                        '<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
                        '<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                        '</w:tcBorders>' % W)
                elif ri == len(rows) - 1:
                    nb = etree.fromstring(
                        '<w:tcBorders xmlns:w="%s">'
                        '<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                        '<w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
                        '<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                        '</w:tcBorders>' % W)
                else:
                    nb = etree.fromstring(
                        '<w:tcBorders xmlns:w="%s">'
                        '<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                        '<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                        '</w:tcBorders>' % W)
                # tcBorders 位于 cnfStyle/tcW/gridSpan/hMerge/vMerge 之后
                afterc = [q(t) for t in ('cnfStyle', 'tcW', 'gridSpan', 'hMerge', 'vMerge')]
                p = 0
                for i, c in enumerate(tcPr):
                    if c.tag in afterc:
                        p = i + 1
                tcPr.insert(p, nb)
                # 单元格内首行缩进清零，居中
                for para in tc.findall(q('p')):
                    pPr = para.find(q('pPr'))
                    if pPr is not None:
                        ind = pPr.find(q('ind'))
                        if ind is not None:
                            for a in ('firstLine', 'firstLineChars'):
                                if ind.get(q(a)) is not None:
                                    ind.set(q(a), '0')
    return n


def main():
    parser = etree.XMLParser(remove_blank_text=False)
    dt = etree.parse(DOC, parser)
    droot = dt.getroot()
    st = etree.parse(STY, parser)
    sroot = st.getroot()

    nc, nf = normalize_quotes(droot)
    print('直引号转换 %d 处；引号设为宋体 %d 处' % (nc, nf))
    print('题注样式 a7 -> 五号黑体:', fix_caption_style(sroot))
    add_sanxian_style(sroot)
    print('三线表改造表格数:', to_three_line_tables(droot))

    dt.write(DOC, xml_declaration=True, encoding='UTF-8', standalone=True)
    st.write(STY, xml_declaration=True, encoding='UTF-8', standalone=True)
    print('done')

main()
