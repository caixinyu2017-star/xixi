# -*- coding: utf-8 -*-
"""质量检查：
1. 文中（作者，年份）引用是否都能在 refs_db.json 中找到（按 cite_variants 精确匹配）
2. refs_db 中未被引用的条目
3. [[FIG/TAB/EQ]] 占位与正文交叉引用（"图X.Y""表X.Y""式(X-Y)"）一致性
4. 各章字数（去空白含标点）
"""
import os, re, json, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, 'chapters')

def load_chapters():
    files = sorted(glob.glob(os.path.join(CH, '*.md')))
    return [(os.path.basename(f), open(f, encoding='utf-8').read()) for f in files]

CITE_RE = re.compile(r'（([^（）]{1,60}?)，((?:19|20)\d{2}[a-c]?)）')

def check(refs_json):
    with open(refs_json, encoding='utf-8') as f:
        refs = json.load(f)
    variants = {}
    for r in refs:
        for v in (r.get('cite_variants') or [r['cite']]):
            variants[v.replace(' ', '')] = r['key']
    chapters = load_chapters()
    total = 0
    problems = []
    used_keys = set()
    fig_defs, tab_defs, eq_defs = set(), set(), set()
    fig_refs, tab_refs, eq_refs = set(), set(), set()
    for name, txt in chapters:
        n = len(re.sub(r'\s', '', re.sub(r'\[\[.*?\]\]', '', txt)))
        total += n
        print(f'{name}: {n} 字')
        for m in CITE_RE.finditer(txt):
            inner = m.group(0).strip('（）')
            parts = re.split(r'；', inner)
            for part in parts:
                part = part.strip().replace(' ', '')
                if not re.search(r'(19|20)\d{2}', part):
                    continue
                if part in variants:
                    used_keys.add(variants[part])
                else:
                    problems.append(f'{name}: 未匹配引用 （{part}）')
        for m in re.finditer(r'\[\[FIG:([\d.]+)\]\]', txt): fig_defs.add(m.group(1))
        for m in re.finditer(r'\[\[TAB:([\d.]+)\]\]', txt): tab_defs.add(m.group(1))
        for m in re.finditer(r'\[\[EQ:([\d\-]+)\]\]', txt): eq_defs.add(m.group(1))
        for m in re.finditer(r'图(\d+\.\d+)', txt): fig_refs.add(m.group(1))
        for m in re.finditer(r'表(\d+\.\d+)', txt): tab_refs.add(m.group(1))
        for m in re.finditer(r'式（?\((\d+-\d+)\)', txt): eq_refs.add(m.group(1))
    print('=' * 50)
    print(f'总字数（正文，去空白）：{total}')
    print(f'引用匹配问题：{len(problems)}')
    for p in sorted(set(problems)): print('  !', p)
    unused = [r['key'] for r in refs if r['key'] not in used_keys]
    print(f'文献总数 {len(refs)}，被引用 {len(used_keys)}，未被引用 {len(unused)}')
    if unused: print('  未引用：', unused)
    print(f'图定义 {len(fig_defs)}：', sorted(fig_defs, key=lambda s: tuple(map(int, s.split(".")))))
    print(f'表定义 {len(tab_defs)}：', sorted(tab_defs, key=lambda s: tuple(map(int, s.split(".")))))
    print(f'公式定义 {len(eq_defs)}')
    miss_fig = fig_defs - fig_refs
    if miss_fig: print('  ! 正文未提及的图：', sorted(miss_fig))
    dangling_fig = {f for f in fig_refs if f not in fig_defs}
    if dangling_fig: print('  ! 正文引用但未定义的图：', sorted(dangling_fig))
    dangling_tab = {t for t in tab_refs if t not in tab_defs}
    if dangling_tab: print('  ! 正文引用但未定义的表：', sorted(dangling_tab))
    # 图文件存在性
    for f in sorted(fig_defs):
        p = os.path.join(ROOT, 'figs', 'fig_%s.png' % f.replace('.', '_'))
        if not os.path.exists(p): print('  ! 缺图文件：', p)
    return total, problems

if __name__ == '__main__':
    check(os.path.join(ROOT, 'plan', 'refs_db.json'))
