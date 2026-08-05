#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第二篇稿件的格式规范化：
  A 直引号→中文弯引号，全部引号字符设宋体
  B 序号半角句点 "N." → 全角 "N．"
  C 题注样式 af7 → 五号黑体、不加粗、居中、无首行缩进
  D 正文样式 a0 的中文字体 仿宋 → 宋体
  E 新建三线表样式并应用；表内文字取消首行缩进
  F 拆开"1 列 × 2 行"的图片布局表格，还原为独立段落
  G 把混入表 2-3 末尾的图片与题注移出表格
  H 把嵌在正文段末的图片分离为独立居中、无缩进的图片段
"""
import re, copy
from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
def q(t): return '{%s}%s' % (W, t)

DOC = 'unpacked/word/document.xml'
STY = 'unpacked/word/styles.xml'
QUOTES = '“”‘’'



# ---------------------------------------------------------------- pPr 子元素顺序
PPR_ORDER = ['pStyle','keepNext','keepLines','pageBreakBefore','framePr','widowControl',
             'numPr','suppressLineNumbers','pBdr','shd','tabs','suppressAutoHyphens',
             'kinsoku','wordWrap','overflowPunct','topLinePunct','autoSpaceDE',
             'autoSpaceDN','bidi','adjustRightInd','snapToGrid','spacing','ind',
             'contextualSpacing','mirrorIndents','suppressOverlap','jc','textDirection',
             'textAlignment','textboxTightWrap','outlineLvl','divId','cnfStyle','rPr',
             'sectPr','pPrChange']
PPR_IDX = {q(t): i for i, t in enumerate(PPR_ORDER)}


def pPr_child(pPr, tag):
    """取得（必要时按 schema 顺序插入）pPr 的子元素。"""
    e = pPr.find(q(tag))
    if e is not None:
        return e
    e = etree.Element(q(tag))
    want = PPR_IDX[q(tag)]
    pos = len(pPr)
    for i, c in enumerate(pPr):
        if PPR_IDX.get(c.tag, 99) > want:
            pos = i
            break
    pPr.insert(pos, e)
    return e


# ---------------------------------------------------------------- A 引号
def set_songti(run):
    rPr = run.find(q('rPr'))
    if rPr is None:
        rPr = etree.Element(q('rPr'))
        run.insert(0, rPr)
    rf = rPr.find(q('rFonts'))
    if rf is None:
        rf = etree.Element(q('rFonts'))
        rPr.insert(0, rf)
    for a in ('asciiTheme', 'hAnsiTheme', 'eastAsiaTheme', 'cstheme'):
        if rf.get(q(a)) is not None:
            del rf.attrib[q(a)]
    rf.set(q('ascii'), '宋体'); rf.set(q('hAnsi'), '宋体')
    rf.set(q('eastAsia'), '宋体'); rf.set(q('cs'), '宋体')
    rf.set(q('hint'), 'eastAsia')


def normalize_quotes(root):
    nconv = nfont = 0
    for para in root.iter(q('p')):
        items = [(r, t) for r in para.iter(q('r')) for t in r.findall(q('t'))]
        if not items:
            continue
        dq = sq = True
        for r, t in items:
            s = t.text or ''
            if '"' in s or "'" in s:
                out = []
                for ch in s:
                    if ch == '"':
                        out.append('“' if dq else '”'); dq = not dq; nconv += 1
                    elif ch == "'":
                        out.append('‘' if sq else '’'); sq = not sq; nconv += 1
                    else:
                        out.append(ch)
                t.text = ''.join(out)
        for r, t in list(items):
            s = t.text or ''
            if not any(c in s for c in QUOTES):
                continue
            if all(c in QUOTES for c in s):
                set_songti(r); nfont += 1; continue
            keep = set()
            for mi, ch in enumerate(s):
                if ch == '’':
                    p0 = s[mi - 1] if mi else ''
                    n0 = s[mi + 1] if mi + 1 < len(s) else ''
                    if p0.isascii() and p0.isalpha() and (n0 == '' or n0.isascii()):
                        keep.add(mi)
            if keep and all(c not in '“”‘' for c in s) and \
               sum(1 for c in s if c == '’') == len(keep):
                continue
            parent = r.getparent(); idx = list(parent).index(r)
            if [c for c in r if c.tag not in (q('rPr'), q('t'))] or len(r.findall(q('t'))) != 1:
                set_songti(r); nfont += 1; continue
            segs = [x for x in re.split('([' + QUOTES + '])', s) if x != '']
            news = []
            for seg in segs:
                nr = copy.deepcopy(r); nt = nr.find(q('t')); nt.text = seg
                nt.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
                if seg in QUOTES:
                    set_songti(nr); nfont += 1
                news.append(nr)
            for k, nr in enumerate(news):
                parent.insert(idx + k, nr)
            parent.remove(r)
    return nconv, nfont




# ---------------------------------------------------------------- 引号配对修正
def fix_quote_pairs(root):
    """修正原稿中把左引号误打成右引号的情形（逐段做配对深度检查）。"""
    n = 0
    for para in root.iter(q('p')):
        runs = [(r, t) for r in para.iter(q('r')) for t in r.findall(q('t'))]
        depth = 0
        for r, t in runs:
            s = t.text or ''
            if '“' not in s and '”' not in s:
                continue
            out = []
            for ch in s:
                if ch == '“':
                    depth += 1
                elif ch == '”':
                    if depth == 0:          # 没有对应左引号，应为左引号
                        ch = '“'
                        depth += 1
                        n += 1
                    else:
                        depth -= 1
                out.append(ch)
            t.text = ''.join(out)
    return n


# ---------------------------------------------------------------- B 序号句点
def fullwidth_enum_period(root):
    n = 0
    for t in root.iter(q('t')):
        s = t.text or ''
        if '.' not in s:
            continue
        ns = re.sub(r'(?<![0-9A-Za-z])([1-9])\.(?=[一-鿿])', r'\1．', s)
        if ns != s:
            n += len(re.findall(r'[1-9]．', ns)) - len(re.findall(r'[1-9]．', s))
            t.text = ns
    return n


# ---------------------------------------------------------------- C/D 样式
def fix_styles(sroot):
    done = []
    for st in sroot.findall(q('style')):
        sid = st.get(q('styleId'))
        if sid == 'af7':                       # 题注
            pPr = st.find(q('pPr'))
            if pPr is None:
                pPr = etree.SubElement(st, q('pPr'))
            ind = pPr_child(pPr, 'ind')
            ind.set(q('firstLine'), '0'); ind.set(q('firstLineChars'), '0')
            pPr_child(pPr, 'jc').set(q('val'), 'center')
            rPr = st.find(q('rPr'))
            if rPr is None:
                rPr = etree.SubElement(st, q('rPr'))
            for bt in ('b', 'bCs'):
                e = rPr.find(q(bt))
                if e is not None:
                    rPr.remove(e)
            rf = rPr.find(q('rFonts'))
            if rf is None:
                rf = etree.Element(q('rFonts')); rPr.insert(0, rf)
            for a in ('asciiTheme', 'hAnsiTheme', 'eastAsiaTheme', 'cstheme'):
                if rf.get(q(a)) is not None:
                    del rf.attrib[q(a)]
            rf.set(q('ascii'), 'Times New Roman'); rf.set(q('hAnsi'), 'Times New Roman')
            rf.set(q('eastAsia'), '黑体'); rf.set(q('cs'), 'Times New Roman')
            for tag in ('sz', 'szCs'):
                e = rPr.find(q(tag))
                if e is None:
                    e = etree.SubElement(rPr, q(tag))
                e.set(q('val'), '21')
            done.append('af7 -> 五号黑体/居中/无缩进/不加粗')
        elif sid == 'a0':                      # 正文
            rPr = st.find(q('rPr'))
            rf = rPr.find(q('rFonts'))
            if rf is not None and rf.get(q('eastAsia')) == '仿宋':
                rf.set(q('eastAsia'), '宋体')
                done.append('a0 正文中文字体 仿宋 -> 宋体')
    return done


SANXIAN = '''<w:style xmlns:w="%s" w:type="table" w:customStyle="1" w:styleId="SanXian">
<w:name w:val="三线表"/><w:basedOn w:val="a2"/><w:uiPriority w:val="50"/><w:qFormat/>
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


def add_sanxian(sroot):
    if not any(s.get(q('styleId')) == 'SanXian' for s in sroot.findall(q('style'))):
        sroot.append(etree.fromstring(SANXIAN))


# ---------------------------------------------------------------- E 三线表
def tcborders(first, last):
    if first:
        inner = ('<w:top w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
                 '<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                 '<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
                 '<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>')
    elif last:
        inner = ('<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                 '<w:bottom w:val="single" w:sz="12" w:space="0" w:color="000000"/>'
                 '<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>')
    else:
        inner = ('<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                 '<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>')
    return etree.fromstring('<w:tcBorders xmlns:w="%s">%s</w:tcBorders>' % (W, inner))


def to_three_line(tbl):
    tblPr = tbl.find(q('tblPr'))
    if tblPr is None:
        tblPr = etree.Element(q('tblPr')); tbl.insert(0, tblPr)
    ts = tblPr.find(q('tblStyle'))
    if ts is None:
        ts = etree.Element(q('tblStyle')); tblPr.insert(0, ts)
    ts.set(q('val'), 'SanXian')
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
    after = [q(x) for x in ('tblStyle', 'tblpPr', 'tblOverlap', 'bidiVisual',
                            'tblStyleRowBandSize', 'tblStyleColBandSize',
                            'tblW', 'jc', 'tblCellSpacing', 'tblInd')]
    pos = 0
    for i, c in enumerate(tblPr):
        if c.tag in after:
            pos = i + 1
    tblPr.insert(pos, borders)
    for cnf in list(tbl.iter(q('cnfStyle'))):
        cnf.getparent().remove(cnf)
    for shd in list(tbl.iter(q('shd'))):
        shd.getparent().remove(shd)
    for col in list(tbl.iter(q('color'))):
        if (col.get(q('val')) or '').upper() in ('FFFFFF', 'FFF'):
            col.set(q('val'), '000000')
            if col.get(q('themeColor')) is not None:
                del col.attrib[q('themeColor')]
    rows = tbl.findall(q('tr'))
    for ri, tr in enumerate(rows):
        for tc in tr.findall(q('tc')):
            tcPr = tc.find(q('tcPr'))
            if tcPr is None:
                tcPr = etree.Element(q('tcPr')); tc.insert(0, tcPr)
            ob = tcPr.find(q('tcBorders'))
            if ob is not None:
                tcPr.remove(ob)
            nb = tcborders(ri == 0, ri == len(rows) - 1)
            afterc = [q(x) for x in ('cnfStyle', 'tcW', 'gridSpan', 'hMerge', 'vMerge')]
            p = 0
            for i, c in enumerate(tcPr):
                if c.tag in afterc:
                    p = i + 1
            tcPr.insert(p, nb)
            va = tcPr.find(q('vAlign'))
            if va is None:
                va = etree.SubElement(tcPr, q('vAlign'))
            va.set(q('val'), 'center')
            # 表内文字：取消首行缩进
            for para in tc.findall(q('p')):
                pPr = para.find(q('pPr'))
                if pPr is None:
                    pPr = etree.Element(q('pPr')); para.insert(0, pPr)
                ind = pPr_child(pPr, 'ind')
                ind.set(q('firstLine'), '0'); ind.set(q('firstLineChars'), '0')


# ---------------------------------------------------------------- F/G/H 图片
CENTER_NOIND = ('<w:pPr><w:keepNext/><w:widowControl w:val="0"/>'
                '<w:ind w:firstLineChars="0" w:firstLine="0"/>'
                '<w:jc w:val="center"/></w:pPr>')


def new_img_para(runs):
    p = etree.fromstring('<w:p xmlns:w="%s">%s</w:p>' % (W, CENTER_NOIND))
    for r in runs:
        p.append(r)
    return p


def unwrap_layout_tables(body):
    """1 列布局表格（仅承载图片与题注）还原为普通段落。"""
    n = 0
    for tbl in list(body.findall(q('tbl'))):
        rows = tbl.findall(q('tr'))
        if not rows or any(len(r.findall(q('tc'))) != 1 for r in rows):
            continue
        if 'blip' not in etree.tostring(tbl, encoding='unicode'):
            continue
        paras = []
        for tr in rows:
            for tc in tr.findall(q('tc')):
                for p in tc.findall(q('p')):
                    paras.append(copy.deepcopy(p))
        idx = list(body).index(tbl)
        for k, p in enumerate(paras):
            body.insert(idx + 1 + k, p)
        body.remove(tbl)
        n += 1
    return n


def strip_trailing_image_rows(body):
    """把混入表格末尾的图片行与题注行移出表格。"""
    n = 0
    for tbl in list(body.findall(q('tbl'))):
        rows = tbl.findall(q('tr'))
        if len(rows) < 3:
            continue
        tail = []
        while rows:
            last = rows[-1]
            txt = ''.join(x.text or '' for x in last.iter(q('t'))).strip()
            has_img = 'blip' in etree.tostring(last, encoding='unicode')
            is_cap = bool(re.match(r'^[图表]\s?\d', txt))
            if has_img or (is_cap and len(txt) < 40):
                tail.insert(0, last)
                tbl.remove(last)
                rows = tbl.findall(q('tr'))
                n += 1
            else:
                break
        if tail:
            idx = list(body).index(tbl)
            out = []
            for tr in tail:
                for tc in tr.findall(q('tc')):
                    for p in tc.findall(q('p')):
                        out.append(copy.deepcopy(p))
            for k, p in enumerate(out):
                body.insert(idx + 1 + k, p)
    return n


def split_inline_images(body):
    """正文段末嵌入的图片分离为独立居中段。"""
    n = 0
    for p in list(body.findall(q('p'))):
        runs = list(p.findall(q('r')))
        if not runs:
            continue
        img_runs = [r for r in runs if r.find('.//' + q('drawing')) is not None]
        if not img_runs:
            continue
        text = ''.join(x.text or '' for x in p.iter(q('t'))).strip()
        if not text:                       # 已是纯图片段，只需去掉首行缩进
            pPr = p.find(q('pPr'))
            if pPr is None:
                pPr = etree.Element(q('pPr')); p.insert(0, pPr)
            ind = pPr_child(pPr, 'ind')
            ind.set(q('firstLine'), '0'); ind.set(q('firstLineChars'), '0')
            pPr_child(pPr, 'jc').set(q('val'), 'center')
            continue
        for r in img_runs:
            p.remove(r)
        newp = new_img_para(img_runs)
        idx = list(body).index(p)
        body.insert(idx + 1, newp)
        n += 1
    return n


def caption_no_indent(body):
    n = 0
    for p in body.findall(q('p')):
        st = p.find(q('pPr') + '/' + q('pStyle'))
        if st is None or st.get(q('val')) != 'af7':
            continue
        pPr = p.find(q('pPr'))
        ind = pPr_child(pPr, 'ind')
        ind.set(q('firstLine'), '0'); ind.set(q('firstLineChars'), '0')
        pPr_child(pPr, 'jc').set(q('val'), 'center')
        for r in p.findall(q('r')):
            rPr = r.find(q('rPr'))
            if rPr is not None:
                for bt in ('b', 'bCs'):
                    e = rPr.find(q(bt))
                    if e is not None:
                        rPr.remove(e)
        n += 1
    return n


def main():
    dt = etree.parse(DOC); droot = dt.getroot(); body = droot.find(q('body'))
    st = etree.parse(STY); sroot = st.getroot()

    nc, nf = normalize_quotes(droot)
    print('直引号转换 %d 处；引号设宋体 %d 处' % (nc, nf))
    print('引号配对修正 %d 处' % fix_quote_pairs(droot))
    print('序号句点转全角 %d 处' % fullwidth_enum_period(droot))
    for d in fix_styles(sroot):
        print('样式:', d)
    add_sanxian(sroot)
    print('拆开图片布局表格 %d 个' % unwrap_layout_tables(body))
    print('移出表内图片/题注行 %d 行' % strip_trailing_image_rows(body))
    tbls = list(body.findall(q('tbl')))
    for t in tbls:
        to_three_line(t)
    print('三线表改造 %d 个' % len(tbls))
    print('分离正文内嵌图片 %d 处' % split_inline_images(body))
    print('题注取消缩进 %d 处' % caption_no_indent(body))

    dt.write(DOC, xml_declaration=True, encoding='UTF-8', standalone=True)
    st.write(STY, xml_declaration=True, encoding='UTF-8', standalone=True)
    print('done')


main()
