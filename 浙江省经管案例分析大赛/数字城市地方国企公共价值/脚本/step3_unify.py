#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第三阶段：全文格式统一 + 章过渡段一段化 + 第三章条目式短段合并。

顺序：先做内容层的替换（过渡段、第三章合并），再做全文格式统一刷一遍，
      避免新插入的内容绕过统一规则。
"""
import re, copy
from lxml import etree
import docxlib2 as D
import content3 as C3

W = D.W
def q(t): return '{%s}%s' % (W, t)

DOC = 'unpacked/word/document.xml'
STY = 'unpacked/word/styles.xml'
QUOTES = '“”‘’'

tree = etree.parse(DOC)
root = tree.getroot()
body = root.find(q('body'))


def ptext(el):
    return ''.join(x.text or '' for x in el.iter(q('t')))


def norm(s):
    return (s.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
             .replace(' ', '').replace('　', '').replace('　', ''))


def find_p(prefix, start=0):
    pn = norm(prefix)
    for i in range(start, len(body)):
        el = body[i]
        if el.tag != q('p'):
            continue
        if norm(ptext(el)).startswith(pn):
            return i
    return -1


def is_red(el):
    for c in el.iter(q('color')):
        if c.get(q('val')) == 'FF0000':
            return True
    return False


# ================================================================ 1 章过渡段
def do_transitions():
    n = 0
    for key, spec in C3.TRANSITIONS.items():
        if spec['anchor'] == 'ADD_AFTER_HEADING':
            continue
        i = find_p(spec['anchor'])
        if i < 0:
            print('  [跳过] 未找到过渡段锚点:', spec['anchor'][:20]); continue
        body.remove(body[i])
        body.insert(i, D.para(spec['text']))
        n += 1
        print('  %s 过渡段已替换为单段（%d 字）' % (key, len(spec['text'])))
    # 第二、五章：章标题后新增
    for key, title in (('ch2', '案例研究对象'), ('ch5', '案例总结')):
        spec = C3.TRANSITIONS[key]
        idx = -1
        for i, el in enumerate(body):
            if el.tag != q('p'):
                continue
            st = el.find(q('pPr') + '/' + q('pStyle'))
            if st is not None and st.get(q('val')) == '1' and ptext(el).strip().startswith(title):
                idx = i
                break
        if idx < 0:
            print('  [跳过] 未找到章标题:', title); continue
        body.insert(idx + 1, D.para(spec['text']))
        n += 1
        print('  %s 过渡段已新增（%d 字）' % (key, len(spec['text'])))
    return n


# ================================================================ 2 第三章合并
def do_merge():
    total_del = total_new = 0
    for grp in C3.CH3_MERGE:
        base = find_p(grp['anchor'])
        if base < 0:
            print('  [跳过] 未找到锚点:', grp['name']); continue
        targets = []
        for d in grp['dels']:
            j = find_p(d, max(0, base - 3))
            if j < 0:
                print('    [警告] 未找到待删段:', d[:22])
            else:
                targets.append(j)
        if not targets:
            continue
        targets = sorted(set(targets))
        insert_at = targets[0]
        for j in sorted(targets, reverse=True):
            body.remove(body[j])
        for k, txt in enumerate(grp['new']):
            body.insert(insert_at + k, D.para(txt))
        total_del += len(targets)
        total_new += len(grp['new'])
        print('  %-24s 删 %d 段 -> 增 %d 段' % (grp['name'], len(targets), len(grp['new'])))
    return total_del, total_new


# ================================================================ 3 标题样式统一
HEADING_SPEC = {
    # styleId: (eastAsia, sz, bold, jc)
    '1': ('黑体', '32', True, 'center'),   # 章标题 三号黑体加粗居中
    '2': ('黑体', '28', False, 'left'),    # 节标题 四号黑体
    'a': ('黑体', '24', False, 'left'),    # 三级标题 小四黑体
}


def unify_heading_styles(sroot):
    for st in sroot.findall(q('style')):
        sid = st.get(q('styleId'))
        if sid not in HEADING_SPEC:
            continue
        ea, sz, bold, jc = HEADING_SPEC[sid]
        pPr = st.find(q('pPr'))
        if pPr is None:
            pPr = etree.SubElement(st, q('pPr'))
        # jc
        e = pPr.find(q('jc'))
        if e is None:
            e = etree.Element(q('jc'))
            pos = len(pPr)
            for i, c in enumerate(pPr):
                if c.tag in (q('outlineLvl'), q('rPr')):
                    pos = i; break
            pPr.insert(pos, e)
        e.set(q('val'), jc)
        rPr = st.find(q('rPr'))
        if rPr is None:
            rPr = etree.SubElement(st, q('rPr'))
        rf = rPr.find(q('rFonts'))
        if rf is None:
            rf = etree.Element(q('rFonts')); rPr.insert(0, rf)
        for a in ('asciiTheme', 'hAnsiTheme', 'eastAsiaTheme', 'cstheme'):
            if rf.get(q(a)) is not None:
                del rf.attrib[q(a)]
        rf.set(q('ascii'), 'Times New Roman'); rf.set(q('hAnsi'), 'Times New Roman')
        rf.set(q('eastAsia'), ea); rf.set(q('cs'), 'Times New Roman')
        for tag, val in (('sz', sz), ('szCs', sz)):
            x = rPr.find(q(tag))
            if x is None:
                x = etree.SubElement(rPr, q(tag))
            x.set(q('val'), val)
        for tag in ('b', 'bCs'):
            x = rPr.find(q(tag))
            if bold:
                if x is None:
                    etree.SubElement(rPr, q(tag))
            elif x is not None:
                rPr.remove(x)
        print('  样式 %s -> %s %spt%s' % (sid, ea, int(sz) / 2, '加粗' if bold else ''))


# ================================================================ 4 全文字体清洗
def in_table(el):
    p = el.getparent()
    while p is not None:
        if p.tag == q('tbl'):
            return True
        p = p.getparent()
    return False


def strip_run_fonts(run, keep_sz=False):
    """删除 run 上的字体与字号内联覆盖，交回样式接管；保留加粗与颜色。"""
    rPr = run.find(q('rPr'))
    if rPr is None:
        return 0
    n = 0
    rf = rPr.find(q('rFonts'))
    if rf is not None:
        rPr.remove(rf); n += 1
    if not keep_sz:
        for tag in ('sz', 'szCs'):
            x = rPr.find(q(tag))
            if x is not None:
                rPr.remove(x); n += 1
    return n


def sweep_fonts():
    n_head = n_body = n_cell = n_quote = 0
    for p in body.iter(q('p')):
        st = p.find(q('pPr') + '/' + q('pStyle'))
        stv = st.get(q('val')) if st is not None else ''
        cell = in_table(p)
        txt = ptext(p).strip()
        is_note = txt.startswith('注：')
        for r in p.findall(q('r')):
            t = r.find(q('t'))
            s = (t.text or '') if t is not None else ''
            if s and all(c in QUOTES for c in s):
                # 引号 run：强制宋体，字号交回样式
                D_set_songti(r)
                rPr = r.find(q('rPr'))
                if not cell and not is_note:
                    for tag in ('sz', 'szCs'):
                        x = rPr.find(q(tag))
                        if x is not None:
                            rPr.remove(x)
                n_quote += 1
                continue
            if stv in ('1', '2', 'a'):
                n_head += strip_run_fonts(r)
            elif cell:
                # 表内：统一宋体五号
                rPr = r.find(q('rPr'))
                if rPr is None:
                    rPr = etree.Element(q('rPr')); r.insert(0, rPr)
                rf = rPr.find(q('rFonts'))
                if rf is None:
                    rf = etree.Element(q('rFonts')); rPr.insert(0, rf)
                for a in ('asciiTheme', 'hAnsiTheme', 'eastAsiaTheme', 'cstheme'):
                    if rf.get(q(a)) is not None:
                        del rf.attrib[q(a)]
                rf.set(q('ascii'), '宋体'); rf.set(q('hAnsi'), '宋体')
                rf.set(q('eastAsia'), '宋体'); rf.set(q('cs'), '宋体')
                for tag in ('sz', 'szCs'):
                    x = rPr.find(q(tag))
                    if x is None:
                        x = etree.SubElement(rPr, q(tag))
                    x.set(q('val'), '21')
                n_cell += 1
            elif stv == 'af7':
                n_head += strip_run_fonts(r)
            else:
                n_body += strip_run_fonts(r, keep_sz=is_note)
    return n_head, n_body, n_cell, n_quote


def D_set_songti(run):
    rPr = run.find(q('rPr'))
    if rPr is None:
        rPr = etree.Element(q('rPr')); run.insert(0, rPr)
    rf = rPr.find(q('rFonts'))
    if rf is None:
        rf = etree.Element(q('rFonts')); rPr.insert(0, rf)
    for a in ('asciiTheme', 'hAnsiTheme', 'eastAsiaTheme', 'cstheme'):
        if rf.get(q(a)) is not None:
            del rf.attrib[q(a)]
    rf.set(q('ascii'), '宋体'); rf.set(q('hAnsi'), '宋体')
    rf.set(q('eastAsia'), '宋体'); rf.set(q('cs'), '宋体')
    rf.set(q('hint'), 'eastAsia')


# ================================================================ 5 段落格式统一
PPR_ORDER = ['pStyle', 'keepNext', 'keepLines', 'pageBreakBefore', 'framePr', 'widowControl',
             'numPr', 'suppressLineNumbers', 'pBdr', 'shd', 'tabs', 'suppressAutoHyphens',
             'kinsoku', 'wordWrap', 'overflowPunct', 'topLinePunct', 'autoSpaceDE',
             'autoSpaceDN', 'bidi', 'adjustRightInd', 'snapToGrid', 'spacing', 'ind',
             'contextualSpacing', 'mirrorIndents', 'suppressOverlap', 'jc', 'textDirection',
             'textAlignment', 'textboxTightWrap', 'outlineLvl', 'divId', 'cnfStyle', 'rPr',
             'sectPr', 'pPrChange']
PPR_IDX = {q(t): i for i, t in enumerate(PPR_ORDER)}


def pPr_child(pPr, tag):
    e = pPr.find(q(tag))
    if e is not None:
        return e
    e = etree.Element(q(tag))
    want = PPR_IDX[q(tag)]
    pos = len(pPr)
    for i, c in enumerate(pPr):
        if PPR_IDX.get(c.tag, 99) > want:
            pos = i; break
    pPr.insert(pos, e)
    return e


def sweep_paragraphs():
    n_ind = n_img = 0
    for p in body.iter(q('p')):
        st = p.find(q('pPr') + '/' + q('pStyle'))
        stv = st.get(q('val')) if st is not None else ''
        pPr = p.find(q('pPr'))
        if pPr is None:
            pPr = etree.Element(q('pPr')); p.insert(0, pPr)
        has_img = p.find('.//' + q('drawing')) is not None
        txt = ptext(p).strip()
        if has_img or stv == 'af7' or txt.startswith('注：'):
            ind = pPr_child(pPr, 'ind')
            ind.set(q('firstLine'), '0'); ind.set(q('firstLineChars'), '0')
            pPr_child(pPr, 'jc').set(q('val'), 'center')
            n_img += 1
        elif in_table(p):
            ind = pPr_child(pPr, 'ind')
            ind.set(q('firstLine'), '0'); ind.set(q('firstLineChars'), '0')
        elif stv in ('1', '2', 'a'):
            ind = pPr.find(q('ind'))
            if ind is not None:
                pPr.remove(ind)
            n_ind += 1
        elif not stv and txt:
            ind = pPr_child(pPr, 'ind')
            ind.set(q('firstLineChars'), '200'); ind.set(q('firstLine'), '480')
            pPr_child(pPr, 'jc').set(q('val'), 'both')
            sp = pPr_child(pPr, 'spacing')
            sp.set(q('line'), '360'); sp.set(q('lineRule'), 'auto')
            n_ind += 1
    return n_ind, n_img


# ================================================================ 主流程
print('[1] 章过渡段一段化')
do_transitions()
print('[2] 第三章条目式短段合并')
d, a = do_merge()
print('    合计：删除 %d 段，替换为 %d 段' % (d, a))

print('[3] 标题样式统一')
sroot = etree.parse(STY)
unify_heading_styles(sroot.getroot())
sroot.write(STY, xml_declaration=True, encoding='UTF-8', standalone=True)

print('[4] 全文字体内联覆盖清洗')
h, b_, c_, qq = sweep_fonts()
print('    标题/题注清除 %d 处，正文清除 %d 处，表内统一 %d 处，引号宋体 %d 处' % (h, b_, c_, qq))

print('[5] 段落缩进/对齐/行距统一')
i1, i2 = sweep_paragraphs()
print('    正文段 %d 处，图/题注/表内段 %d 处' % (i1, i2))

tree.write(DOC, xml_declaration=True, encoding='UTF-8', standalone=True)
print('written')
