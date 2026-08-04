# -*- coding: utf-8 -*-
"""核查：每个图/表编号是否在正文中先被引用，再出现图名/表名。"""
import re, sys, zipfile
from docx import Document
from docx.oxml.ns import qn

def check(path):
    d = Document(path)
    body = d.element.body
    seq = []          # (kind, text)
    for child in body.iterchildren():
        if child.tag == qn('w:p'):
            txt = "".join(t.text or "" for t in child.iter(qn('w:t')))
            has_img = child.find('.//'+qn('a:blip')) is not None or child.find('.//'+qn('w:drawing')) is not None
            seq.append(("img" if has_img else "p", txt))
        elif child.tag == qn('w:tbl'):
            seq.append(("tbl", ""))
    cap_fig = {}; cap_tbl = {}; mention_fig = {}; mention_tbl = {}
    for i, (k, txt) in enumerate(seq):
        m = re.match(r"^图\s*(\d+)\s", txt)
        if m and k == "p":
            cap_fig.setdefault(int(m.group(1)), i)
            continue
        m = re.match(r"^表\s*(\d+)\s", txt)
        if m and k == "p":
            cap_tbl.setdefault(int(m.group(1)), i)
            continue
        for n in re.findall(r"图\s*(\d+)", txt):
            mention_fig.setdefault(int(n), i)
        for n in re.findall(r"表\s*(\d+)", txt):
            mention_tbl.setdefault(int(n), i)
    nimg = sum(1 for k, _ in seq if k == "img")
    print(f"\n{'='*72}\n{path.split('/')[-1]}\n{'='*72}")
    print(f"嵌入图片 {nimg} 张；图名 {len(cap_fig)} 条；表名 {len(cap_tbl)} 条；表格 {sum(1 for k,_ in seq if k=='tbl')} 个")
    bad = []
    for n in sorted(cap_fig):
        mi = mention_fig.get(n)
        if mi is None: bad.append(f"图{n}: 正文未引用")
        elif mi >= cap_fig[n]: bad.append(f"图{n}: 先出现图名(pos {cap_fig[n]})后被引用(pos {mi})")
    for n in sorted(cap_tbl):
        mi = mention_tbl.get(n)
        if mi is None: bad.append(f"表{n}: 正文未引用")
        elif mi >= cap_tbl[n]: bad.append(f"表{n}: 先出现表名(pos {cap_tbl[n]})后被引用(pos {mi})")
    # 编号连续性
    for nm, d_ in [("图", cap_fig), ("表", cap_tbl)]:
        ks = sorted(d_)
        if ks != list(range(1, len(ks)+1)):
            bad.append(f"{nm}编号不连续: {ks}")
    if bad:
        print("[!] 问题：")
        for b in bad: print("   -", b)
    else:
        print("[✓] 所有图表均在正文中先引用后出现，编号连续")
    return len(bad)

tot = 0
for p in sys.argv[1:]:
    tot += check(p)
print(f"\n合计问题数：{tot}")
