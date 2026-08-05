#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第二阶段：插入新增图/表/正文（红字），并重排全文图表编号缓存值。"""
import json, os, sys, re
from lxml import etree
import docxlib as D

W = D.W
def q(t): return '{%s}%s' % (W, t)

UNP = 'unpacked'
DOC = os.path.join(UNP, 'word', 'document.xml')

tree = etree.parse(DOC)
body = tree.getroot().find(q('body'))
BLOCKS = list(body)


def ptext(el):
    return ''.join(x.text or '' for x in el.iter(q('t')))


def find_idx(prefix, start=0, style=None):
    """按段首文字定位块索引。"""
    prefix = prefix.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
    for i in range(start, len(BLOCKS)):
        el = BLOCKS[i]
        if el.tag != q('p'):
            continue
        if style is not None:
            st = el.find(q('pPr') + '/' + q('pStyle'))
            if (st.get(q('val')) if st is not None else '') != style:
                continue
        t = ptext(el).replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
        if t.startswith(prefix) or (style == 'a7' and prefix in t):
            return i
    raise SystemExit('锚点未找到: %r' % prefix)


PENDING = []   # (after_index, [elements])


def insert_after(idx, els):
    PENDING.append((idx, els))


def apply_inserts():
    # 从后往前插，避免索引失效
    for idx, els in sorted(PENDING, key=lambda x: -x[0]):
        ref = BLOCKS[idx]
        pos = list(body).index(ref)
        for k, e in enumerate(els):
            body.insert(pos + 1 + k, e)


# ---------------------------------------------------------------- 编号重排
CHAP_TITLES = ['绪论', '案例研究对象', '案例主体', '案例分析',
               '基于DART模型', '总结与启示']


def renumber():
    """按文档顺序重算所有题注的章号与序号缓存值。"""
    chap = 0
    cnt = {'图': 0, '表': 0}
    changed = []
    for el in body:
        if el.tag != q('p'):
            continue
        st = el.find(q('pPr') + '/' + q('pStyle'))
        stv = st.get(q('val')) if st is not None else ''
        if stv == '1':
            t0 = ptext(el).strip()
            for k, title in enumerate(CHAP_TITLES):
                if t0.startswith(title):
                    chap = k + 1
                    cnt = {'图': 0, '表': 0}
                    break
            continue
        if stv != 'a7':
            continue
        txt = ptext(el).strip()
        if not txt or txt[0] not in '图表':
            continue
        kind = txt[0]
        cnt[kind] += 1
        # 收集 run 序列：定位 noBreakHyphen 与 SEQ 域
        seq_nodes = []
        chap_nodes = []
        seen_hyphen = False
        in_field = 0
        after_sep = False
        for r in el.iter(q('r')):
            for ch in r:
                tag = ch.tag
                if tag == q('noBreakHyphen'):
                    seen_hyphen = True
                elif tag == q('fldChar'):
                    ft = ch.get(q('fldCharType'))
                    if ft == 'begin':
                        in_field += 1
                        after_sep = False
                    elif ft == 'separate':
                        after_sep = True
                    elif ft == 'end':
                        in_field -= 1
                        after_sep = False
                elif tag == q('t'):
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
                                                   cnt[kind], txt[:34]))
    return changed


def fix_xrefs(mapping):
    """替换正文中的交叉引用，如 图5-1 -> 图5-2。mapping: {(kind,old):new}"""
    n = 0
    for el in body:
        if el.tag != q('p'):
            continue
        st = el.find(q('pPr') + '/' + q('pStyle'))
        stv = st.get(q('val')) if st is not None else ''
        if stv in ('a7', 'ad', 'TOC1', 'TOC2', 'TOC3'):
            continue
        for t in el.iter(q('t')):
            s = t.text or ''
            if not s:
                continue
            def rep(m):
                nonlocal n
                key = (m.group(1), m.group(2) + '-' + m.group(3))
                if key in mapping:
                    n += 1
                    return m.group(1) + mapping[key]
                return m.group(0)
            ns = re.sub(r'([图表])\s?(\d+)\s?[-‑–—]\s?(\d+)', rep, s)
            if ns != s:
                t.text = ns
    return n
