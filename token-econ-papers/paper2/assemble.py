# -*- coding: utf-8 -*-
"""装配论文 Word 文件。

用法：python3 assemble.py
"""
import os
import re
import sys

import docxbuild as D
from docxbuild import HEI, KAI, SIZE, SONG

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'build')
os.makedirs(OUT, exist_ok=True)


def collect_blocks():
    import content_a as A
    import content_b as B
    import content_c as C
    import content_lit as L
    return (A.front() + A.sec1() + L.sec_lit() + A.sec2()
            + B.sec3() + B.sec4() + C.sec5() + C.sec6() + C.sec7())


def build():
    blocks = collect_blocks()
    p = D.Paper(OUT)
    p.prepare_math(blocks)

    title_para = None
    for blk in blocks:
        k = next(iter(blk))
        if k == 'title_zh':
            title_para = p.para(blk[k], indent=False, align='center', cn=HEI,
                                size=SIZE['小三'], bold=True, space_after=4)
        elif k == 'subtitle_zh':
            p.para(blk[k], indent=False, align='center', cn=HEI, size=SIZE['四号'],
                   space_after=8)
        elif k == 'authors_zh':
            p.para(blk[k], indent=False, align='center', cn=KAI, size=SIZE['四号'],
                   space_after=2)
        elif k == 'affil_zh':
            p.para(blk[k], indent=False, align='center', cn=SONG, size=SIZE['五号'],
                   space_after=10)
        elif k == 'abstract_zh':
            p.para('内容提要：' + blk[k], indent=True, size=SIZE['五号'], spacing=1.0,
                   space_after=4)
        elif k == 'kw_zh':
            p.para('关键词：' + blk[k], indent=True, size=SIZE['五号'], spacing=1.0,
                   space_after=10)
        elif k == 'title_en':
            p.para(blk[k], indent=False, align='center', cn=HEI, size=SIZE['四号'],
                   bold=True, space_after=6)
        elif k == 'abstract_en':
            p.para('Abstract: ' + blk[k], indent=True, size=SIZE['五号'], spacing=1.0,
                   space_after=4)
        elif k == 'kw_en':
            p.para('Key Words: ' + blk[k], indent=True, size=SIZE['五号'], spacing=1.0,
                   space_after=10)
        elif k == 'author_note':
            p.footnote_star(title_para, blk[k])
        elif k in ('h1', 'h2', 'h3', 'h4'):
            p.heading(blk[k], int(k[1]))
        elif k == 'p':
            p.para(blk[k])
        elif k == 'lead':
            p.para(blk[k], indent=True)
        elif k == 'eq':
            p.equation(blk['eq'], blk['num'])
        elif k == 'fig':
            p.figure(os.path.join(HERE, blk['fig']), blk['caption'],
                     legend=blk.get('legend'), source=blk.get('source'),
                     note=blk.get('note'))
        elif k == 'table':
            t = blk['table']
            p.table(t['caption'], t['header'], t['rows'], note=t.get('note'),
                    width_cm=t.get('width_cm'))
        else:
            raise ValueError('未知块类型: %s' % k)

    # ---- 参考文献 ----
    import refs_pool
    missing = [k for k in p.refs_order if k not in refs_pool.POOL]
    if missing:
        print('!! 缺少著录的引用 key:', missing)
    p.heading('参考文献', 1)
    for i, key in enumerate(p.refs_order, 1):
        lang, s = refs_pool.POOL.get(key, ('zh', f'【缺失著录：{key}】'))
        p.para(f'[{i}] {s}', indent=False, size=SIZE['五号'], spacing=1.0, space_after=2)

    name = '医保异地结算改革、患者跨区流动与医院竞争.docx'
    path = os.path.join(OUT, name)
    p.save(path)

    cjk = sum(len(re.findall(r'[一-鿿]', v))
              for b in blocks for v in b.values() if isinstance(v, str))
    print(f'saved: {path}')
    print(f'正文汉字 {cjk}；表 {len([b for b in blocks if "table" in b])}；'
          f'图 {len([b for b in blocks if "fig" in b])}；'
          f'公式 {len([b for b in blocks if "eq" in b])}；'
          f'参考文献 {len(p.refs_order)}；脚注 {len(p.footnotes)}')
    return path


if __name__ == '__main__':
    build()
