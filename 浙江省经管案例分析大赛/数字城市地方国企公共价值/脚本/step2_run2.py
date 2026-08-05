#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第二篇稿件：插入摘要与正文增补、图表；重排编号；设置打开时更新域。"""
import os, re
from lxml import etree
from PIL import Image
import docxlib2 as D
import content2 as C

W = D.W
def q(t): return '{%s}%s' % (W, t)

UNP = 'unpacked'
DOC = os.path.join(UNP, 'word', 'document.xml')
tree = etree.parse(DOC)
body = tree.getroot().find(q('body'))

# ---------------------------------------------------------------- 图片登记
SRC = {
    'G1': 'figs/G1.png', 'G2': 'figs/G2.png', 'G3': 'figs/G3.png',
    'G4': 'figs/G4.png', 'G5': 'figs/G5.png', 'G6': 'figs/G6.png',
    'A': 'analysis/figs/A_efficiency.png', 'B': 'analysis/figs/B_headcount.png',
    'C': 'analysis/figs/C_qualification.png', 'D': 'analysis/figs/D_structure.png',
}
WIDTH = {'A': 5270000, 'B': 4300000, 'C': 4900000, 'D': 5270000}
RIDS, DOCPR = {}, [900]
for k, p in SRC.items():
    im = Image.open(p)
    w = WIDTH.get(k, 5270000)
    RIDS[k] = (D.add_image(UNP, p, 'newfig_%s.png' % k.lower()), w,
               int(w * im.size[1] / im.size[0]))


def IMG(k):
    DOCPR[0] += 1
    rid, cx, cy = RIDS[k]
    return D.image_para(rid, cx, cy, DOCPR[0])


def FIGCAP(text):
    return D.caption('图', 0, 0, text)


def TABCAP(text):
    return D.caption('表', 0, 0, text)


def NOTE(text):
    # 图注：小五号，居中，不缩进
    return D.para(text, indent=None, jc='center', sz='18')


P, H2, H3 = D.para, (lambda t: D.heading(t, 2)), (lambda t: D.heading(t, 3))
TBL = lambda h, r: D.table(h, r)


def ptext(el):
    return ''.join(x.text or '' for x in el.iter(q('t')))


def norm(s):
    return (s.replace('“', '"').replace('”', '"')
             .replace('‘', "'").replace('’', "'").replace(' ', '').replace('　', ''))


def find(prefix, style=None):
    pn = norm(prefix)
    for i, el in enumerate(body):
        if el.tag != q('p'):
            continue
        if style is not None:
            st = el.find(q('pPr') + '/' + q('pStyle'))
            if (st.get(q('val')) if st is not None else '') != style:
                continue
        if norm(ptext(el)).startswith(pn):
            return i
    raise SystemExit('锚点未找到: %r' % prefix)


PENDING = []
def after(prefix, els, style=None):
    PENDING.append((find(prefix, style), els))


# ================================================================ 摘要
def abstract():
    els = [D.heading(C.ABSTRACT_CN_TITLE, 2, numbered=False)]
    els += [P(x) for x in C.ABSTRACT_CN]
    els.append(P(C.KEYWORDS_CN))
    els.append(D.heading(C.ABSTRACT_EN_TITLE, 2, numbered=False))
    els += [P(x) for x in C.ABSTRACT_EN]
    els.append(P(C.KEYWORDS_EN))
    els.append(etree.fromstring(
        '<w:p xmlns:w="%s"><w:pPr><w:ind w:firstLineChars="0" w:firstLine="0"/></w:pPr>'
        '<w:r><w:br w:type="page"/></w:r></w:p>' % W))
    return els


# ================================================================ 第一章
after('本文以单案例研究法为核心', [
    P(C.CH1[0]['text']),
    TABCAP(C.CH1[1]['title']), TBL(C.CH1[1]['header'], C.CH1[1]['rows']),
    IMG('G3'), FIGCAP(C.CH1[2]['caption']),
])
after('全文严格遵循战略三角闭环逻辑推进', [
    P(C.CH1[3]['text']),
    TABCAP(C.CH1[4]['title']), TBL(C.CH1[4]['header'], C.CH1[4]['rows']),
])

# ================================================================ 第二章（章末）
c2 = C.CH2
after('2021至2022年，公司先后通过CS1级', [], style=None)   # 占位，实际插在章末
PENDING.pop()
IDX_CH3 = find('案例主体', style='1')
CH2_END = IDX_CH3 - 1
while body[CH2_END].tag == q('p') and not ptext(body[CH2_END]).strip():
    CH2_END -= 1
PENDING.append((CH2_END, [
    H2(c2[0]['text']),
    P(c2[1]['text']), P(c2[2]['text']),
    IMG('B'), FIGCAP(c2[3]['caption']), NOTE(c2[3]['note']),
    P(c2[4]['text']),
    IMG('C'), FIGCAP(c2[5]['caption']),
    P(c2[6]['text']),
    TABCAP(c2[7]['title']), TBL(c2[7]['header'], c2[7]['rows']),
    IMG('D'), FIGCAP(c2[8]['caption']),
    P(c2[9]['text']),
]))

# ================================================================ 第三章
c3 = C.CH3
after('案例主体', [
    P(c3[0]['text']), P(c3[1]['text']),
    TABCAP(c3[2]['title']), TBL(c3[2]['header'], c3[2]['rows']),
], style='1')
after('打通交通、气象、安防、消防实时数据', [
    P(c3[3]['text']),
    IMG('A'), FIGCAP(c3[4]['caption']), NOTE(c3[4]['note']),
    P(c3[5]['text']),
])
after('各类民生数字化项目不以商业盈利为目标', [
    IMG('G5'), FIGCAP(c3[6]['caption']),
    TABCAP(c3[7]['title']), TBL(c3[7]['header'], c3[7]['rows']),
])
IDX_CH4 = find('案例分析', style='1')
CH3_END = IDX_CH4 - 1
while body[CH3_END].tag == q('p') and not ptext(body[CH3_END]).strip():
    CH3_END -= 1
PENDING.append((CH3_END, [
    H2(c3[8]['text']), P(c3[9]['text']), P(c3[10]['text']),
]))

# ================================================================ 第四章
c4 = C.CH4
after('案例分析', [
    P(c4[0]['text']), P(c4[1]['text']),
    TABCAP(c4[2]['title']), TBL(c4[2]['header'], c4[2]['rows']),
    IMG('G2'), FIGCAP(c4[3]['caption']),
], style='1')
after('在外部协同层面多元化、跨界化的产学研协同体系', [
    P(c4[4]['text']),
    IMG('G4'), FIGCAP(c4[5]['caption']),
])
after('综上，战略三角模型所蕴含的层级递进逻辑', [
    IMG('G1'), FIGCAP(c4[6]['caption']),
    P(c4[7]['text']),
    H2(c4[8]['text']), P(c4[9]['text']),
])

# ================================================================ 第五章
c5 = C.CH5
after('中小型城市数字化建设应优先选择兼具公共使命与专业能力', [
    IMG('G6'), FIGCAP(c5[0]['caption']),
    P(c5[1]['text']),
])

# ---------------------------------------------------------------- 应用
for idx, els in sorted(PENDING, key=lambda x: -x[0]):
    ref = body[idx]
    pos = list(body).index(ref)
    for k, e in enumerate(els):
        body.insert(pos + 1 + k, e)
print('正文增补插入完成')

for k, e in enumerate(abstract()):
    body.insert(k, e)
print('摘要/Abstract/关键词已插入文首')


# ---------------------------------------------------------------- 题名修正
for el in body:
    if el.tag != q('p'):
        continue
    st = el.find(q('pPr') + '/' + q('pStyle'))
    if st is None or st.get(q('val')) != 'af7':
        continue
    for t in el.iter(q('t')):
        if t.text and '主要资质与荣誉汇总表' in t.text:
            t.text = t.text.replace('主要资质与荣誉汇总表', '主要资质与荣誉一览')
            print('题名修正: 图 2-4 …汇总表 -> …一览（该项为图片，避免图表标签混淆）')


# ---------------------------------------------------------------- 编号重排
CHAP_TITLES = ['绪论', '案例研究对象', '案例主体', '案例分析', '案例总结']


def renumber():
    chap, cnt, changed = 0, {'图': 0, '表': 0}, []
    for el in body:
        if el.tag != q('p'):
            continue
        st = el.find(q('pPr') + '/' + q('pStyle'))
        stv = st.get(q('val')) if st is not None else ''
        if stv == '1':
            t0 = ptext(el).strip()
            for k, title in enumerate(CHAP_TITLES):
                if t0.startswith(title):
                    chap, cnt = k + 1, {'图': 0, '表': 0}
                    break
            continue
        if stv != 'af7':
            continue
        txt = ptext(el).strip()
        if not txt or txt[0] not in '图表':
            continue
        kind = txt[0]
        cnt[kind] += 1
        chap_nodes, seq_nodes = [], []
        seen_hyphen, in_field, after_sep = False, 0, False
        for r in el.iter(q('r')):
            for ch in r:
                if ch.tag == q('noBreakHyphen'):
                    seen_hyphen = True
                elif ch.tag == q('fldChar'):
                    ft = ch.get(q('fldCharType'))
                    if ft == 'begin':
                        in_field += 1; after_sep = False
                    elif ft == 'separate':
                        after_sep = True
                    elif ft == 'end':
                        in_field -= 1; after_sep = False
                elif ch.tag == q('t'):
                    s = (ch.text or '').strip()
                    if not s.isdigit():
                        continue
                    if not seen_hyphen:
                        chap_nodes.append(ch)
                    elif in_field > 0 and after_sep:
                        seq_nodes.append(ch)
        old = (chap_nodes[-1].text if chap_nodes else '?',
               seq_nodes[-1].text if seq_nodes else '?')
        if chap_nodes:
            chap_nodes[-1].text = str(chap)
            for n in chap_nodes[:-1]:
                n.text = ''
        if seq_nodes:
            seq_nodes[-1].text = str(cnt[kind])
            for n in seq_nodes[:-1]:
                n.text = ''
        changed.append('%s%s-%s -> %s%d-%d  %s' % (kind, old[0], old[1], kind, chap,
                                                   cnt[kind], txt[:36]))
    return changed


ch = renumber()
print('\n--- 图表编号重排（%d 条）---' % len(ch))
for c in ch:
    print('  ' + c)

# ---------------------------------------------------------------- 打开更新域
sp = os.path.join(UNP, 'word', 'settings.xml')
stt = etree.parse(sp); sr = stt.getroot()
if sr.find(q('updateFields')) is None:
    uf = etree.Element(q('updateFields')); uf.set(q('val'), 'true')
    pos = len(sr)
    for i, c in enumerate(sr):
        if c.tag in (q('rsids'), q('compat'), q('hdrShapeDefaults'),
                     q('footnotePr'), q('endnotePr')):
            pos = i; break
    sr.insert(pos, uf)
    stt.write(sp, xml_declaration=True, encoding='UTF-8', standalone=True)
    print('已设置打开时自动更新域')

tree.write(DOC, xml_declaration=True, encoding='UTF-8', standalone=True)
print('written')
