#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, os
from lxml import etree
import docxlib as D
import step2_insert as S

q = S.q
C = json.load(open('content.json', encoding='utf-8'))

# ---------------- 图片登记 ----------------
FIGS = {
    'F1': ('fig_new1.png', 1693, 929),
    'F2': ('fig_new2.png', 1693, 929),
    'F3': ('fig_new3.png', 1536, 1024),
    'F4': ('fig_new4.png', 1536, 1024),
    'F5': ('fig_new5.png', 1536, 1024),
    'F6': ('fig_new6.png', 1536, 1024),
    'F7': ('fig_new7.png', 1774, 887),
}
WIDTH_EMU = 5270000
RIDS = {}
DOCPR = 900
for k, (name, w, h) in FIGS.items():
    rid = D.add_image(S.UNP, 'figs_opt/%s.png' % k, name)
    RIDS[k] = (rid, WIDTH_EMU, int(WIDTH_EMU * h / w))


def img(key):
    global DOCPR
    DOCPR += 1
    rid, cx, cy = RIDS[key]
    return D.image_para(rid, cx, cy, DOCPR)


def cap(kind, text):
    # 章号/序号由 renumber() 统一重写，这里先占位
    return D.caption(kind, 0, 0, text)


def P(txt):
    return D.para(txt)


def H2(t): return D.heading(t, 2)
def H3(t): return D.heading(t, 3)


def T(block):
    return D.table(block['header'], block['rows'])


b3, b4, b5 = C['ch3'], C['ch4'], C['ch5']

# ================= 第三章 =================
i = S.find_idx('实践图景', style='1')
S.insert_after(i, [
    P(b3[0]['text']),
    P(b3[1]['text']),
    img('F1'),
    cap('图', b3[2]['text']),
    cap('表', b3[3]['title']),
    T(b3[3]),
])

i = S.find_idx('在人力资本要素方面')
S.insert_after(i, [
    P(b3[5]['text']),
    P(b3[6]['text']),
    img('F2'),
    cap('图', b3[4]['text']),
])

# 第三章末：表3-3 表格之后追加对标表 + 本章小结
i = S.find_idx('天和农业联农带农量化成效总数据表', style='a7')
tbl_idx = i + 1                       # 紧随其后的 w:tbl
assert S.BLOCKS[tbl_idx].tag == q('tbl'), S.BLOCKS[tbl_idx].tag
S.insert_after(tbl_idx, [
    cap('表', b3[7]['title']),
    T(b3[7]),
    H2(b3[8]['text']),
    P(b3[9]['text']),
    P(b3[10]['text']),
    img('F3'),
    cap('图', b3[11]['text']),
    P(b3[12]['text']),
])

# ================= 第四章 =================
i = S.find_idx('案例分析——三重利益联结的共富机理', style='1')
S.insert_after(i, [P(b4[0]['text']), P(b4[1]['text'])])

i = S.find_idx('三重利益联结体系最终实现内生共富')
S.insert_after(i, [
    H2(b4[2]['text']),
    H3(b4[3]['text']),
    P(b4[4]['text']), P(b4[5]['text']), P(b4[6]['text']), P(b4[7]['text']),
    cap('表', b4[8]['title']), T(b4[8]),
    H3(b4[9]['text']),
    P(b4[10]['text']), P(b4[11]['text']), P(b4[12]['text']),
    cap('表', b4[13]['title']), T(b4[13]),
    img('F5'), cap('图', b4[14]['text']),
    H3(b4[15]['text']),
    P(b4[16]['text']), P(b4[17]['text']), P(b4[18]['text']),
    img('F4'), cap('图', b4[19]['text']),
])

# ================= 第五章 =================
i = S.find_idx('基于DART模型的价值共创共富路径', style='1')
S.insert_after(i, [P(b5[0]['text']), P(b5[1]['text'])])

i = S.find_idx('DART四维度与天和农业价值共创实践的映射关系', style='a7')
tbl_idx = i + 1
assert S.BLOCKS[tbl_idx].tag == q('tbl')
S.insert_after(tbl_idx, [
    cap('表', b5[2]['title']), T(b5[2]),
    P(b5[3]['text']), P(b5[4]['text']), P(b5[5]['text']),
])

i = S.find_idx('天和农业的实践印证了这一递进逻辑')
S.insert_after(i, [
    H3(b5[6]['text']),
    P(b5[7]['text']), P(b5[8]['text']), P(b5[9]['text']),
    img('F6'), cap('图', 'DART四维协同的正反馈闭环机理图'),
])

i = S.find_idx('天和农业的DART实践并非不可复制的特例')
S.insert_after(i, [
    H2(b5[11]['text']),
    P(b5[12]['text']),
    img('F7'), cap('图', b5[13]['text']),
    P(b5[14]['text']), P(b5[15]['text']), P(b5[16]['text']),
    cap('表', b5[17]['title']), T(b5[17]),
])

S.apply_inserts()
print('插入完成，块数 %d -> %d' % (len(S.BLOCKS), len(list(S.body))))

# --------- 规范少数未套用题注样式的旧图题（含 SEQ 域但无 pStyle a7）---------
import re
FIXED = 0
for el in list(S.body):
    if el.tag != q('p'):
        continue
    instr = ''.join(x.text or '' for x in el.iter(q('instrText')))
    if 'SEQ' not in instr or not re.search(r'SEQ\s*[图表]', instr):
        continue
    pPr = el.find(q('pPr'))
    if pPr is None:
        continue
    st = pPr.find(q('pStyle'))
    if st is not None and st.get(q('val')) == 'a7':
        continue
    if st is None:
        st = etree.Element(q('pStyle'))
        pPr.insert(0, st)
    st.set(q('val'), 'a7')
    # 去掉行内小五号覆盖，交由 a7 样式（五号黑体）接管
    for rpr in el.iter(q('rPr')):
        for tag in ('sz', 'szCs'):
            e = rpr.find(q(tag))
            if e is not None and e.get(q('val')) == '20':
                rpr.remove(e)
    FIXED += 1
print('旧图题规范为题注样式:', FIXED)

# --------- 打开文档时自动更新域（目录/图索引/表索引/SEQ 编号） ---------
sp = os.path.join(S.UNP, 'word', 'settings.xml')
st_tree = etree.parse(sp)
st_root = st_tree.getroot()
if st_root.find(q('updateFields')) is None:
    uf = etree.Element(q('updateFields'))
    uf.set(q('val'), 'true')
    # updateFields 需排在 rsids 之前
    pos = len(st_root)
    for i, c in enumerate(st_root):
        if c.tag in (q('rsids'), q('compat'), q('hdrShapeDefaults'),
                     q('footnotePr'), q('endnotePr')):
            pos = i
            break
    st_root.insert(pos, uf)
    st_tree.write(sp, xml_declaration=True, encoding='UTF-8', standalone=True)
    print('已设置打开时自动更新域')

changed = S.renumber()
print('\n--- 图表编号重排（共 %d 条）---' % len(changed))
for c in changed:
    print('  ' + c)

# 交叉引用：本次插入未改变第五、六章既有图表序号，逐项确认
n = S.fix_xrefs({})
print('交叉引用替换:', n)

S.tree.write(S.DOC, xml_declaration=True, encoding='UTF-8', standalone=True)
print('written')
