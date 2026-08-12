# -*- coding: utf-8 -*-
"""全书结构审计：图表编号顺序、先文后图、公式编号、引用完整性、标点。只读，不改文件。"""
import importlib
import os
import re
import sys

import references as refs
from docxbuilder import count_chars

HERE = os.path.dirname(os.path.abspath(__file__))
CHAPTERS = [f'content_ch{i:02d}' for i in range(1, 15)]

problems = []


def P(msg):
    problems.append(msg)


refs.reset()
used_order = []
for idx, mod in enumerate(CHAPTERS, 1):
    m = importlib.import_module(mod)
    before = refs.n_used()
    blocks = m.blocks()
    # ---- 图表编号顺序 + 先文后图 ----
    seen_text = []
    fig_seq, tab_seq, eq_seq = [], [], []
    for b in blocks:
        for key in ('p', 'lead', 'h1', 'h2', 'h3', 'h4'):
            if key in b and isinstance(b[key], str):
                seen_text.append(b[key])
        if 'items' in b:
            seen_text += [str(x) for x in b['items']]
        if 'fig' in b:
            cap = b.get('caption', '')
            mo = re.match(r'图(\d+)\.(\d+)', cap)
            if not mo:
                P(f'{mod}: 图题格式异常 {cap!r}')
                continue
            c, k = int(mo.group(1)), int(mo.group(2))
            if c != idx:
                P(f'{mod}: 图题章号错 {cap!r}')
            fig_seq.append(k)
            tag = f'图{c}.{k}'
            if not any(tag in t for t in seen_text):
                P(f'{mod}: {tag} 未在图前正文提及（先文后图）')
            nt = b.get('note')
            if nt and not nt.startswith('注：'):
                P(f'{mod}: {tag} 图注未以“注：”开头')
            p = os.path.join(HERE, b['fig'])
            if not os.path.exists(p):
                P(f'{mod}: {tag} 图片文件缺失 {b["fig"]}')
        if 'table' in b:
            tb = b['table']
            cap = tb.get('caption', '')
            mo = re.match(r'表(\d+)\.(\d+)', cap)
            if not mo:
                P(f'{mod}: 表题格式异常 {cap!r}')
                continue
            c, k = int(mo.group(1)), int(mo.group(2))
            if c != idx:
                P(f'{mod}: 表题章号错 {cap!r}')
            tab_seq.append(k)
            tag = f'表{c}.{k}'
            if not any(tag in t for t in seen_text):
                P(f'{mod}: {tag} 未在表前正文提及（先文后表）')
            nt = tb.get('note')
            if nt and not nt.startswith('注：'):
                P(f'{mod}: {tag} 表注未以“注：”开头')
        if 'eq' in b and b.get('num'):
            mo = re.match(r'(\d+)-(\d+)$', str(b['num']))
            if not mo:
                P(f'{mod}: 公式编号格式异常 {b["num"]!r}')
            else:
                if int(mo.group(1)) != idx:
                    P(f'{mod}: 公式编号章号错 {b["num"]}')
                eq_seq.append(int(mo.group(2)))
    if fig_seq != sorted(fig_seq) or fig_seq != list(range(1, len(fig_seq) + 1)):
        P(f'{mod}: 图编号非顺序 {fig_seq}')
    if tab_seq != sorted(tab_seq) or tab_seq != list(range(1, len(tab_seq) + 1)):
        P(f'{mod}: 表编号非顺序 {tab_seq}')
    if eq_seq != list(range(1, len(eq_seq) + 1)):
        P(f'{mod}: 公式编号非连续 {eq_seq}')
    # ---- 标点 ----
    halfwidth = re.compile(r'[a-zA-Z一-鿿]\s*[,;:]\s*[一-鿿]')
    for t in seen_text:
        mo = halfwidth.search(t)
        if mo:
            P(f'{mod}: 疑似半角标点 …{t[max(0, mo.start() - 12):mo.end() + 12]}…')
            break
    n_new = refs.n_used() - before
    print(f'{mod}: {count_chars(blocks):>6} 字, 图{len(fig_seq)} 表{len(tab_seq)} 式{len(eq_seq)}, 新增引用{n_new}')

used = set(refs._ORDER)
unused = [k for k in refs.REFS if k not in used]
print(f'\n已引用 {len(used)} / 库 {len(refs.REFS)}；未引用 {len(unused)} 条：')
for k in unused:
    print('   ', k, '|', refs.REFS[k]['gb'][:70])

print(f'\n=== 问题 {len(problems)} 条 ===')
for p in problems:
    print(' *', p)
sys.exit(1 if problems else 0)
