# -*- coding: utf-8 -*-
"""Markdown -> journal-style docx.
- pandoc converts $...$ / $$...$$ to native OMML (Word equation editor objects).
- EQNUM:n markers after a display equation become right-aligned equation numbers
  via a borderless 3-column table (equation centered, number right).
- Ordinary tables are converted to three-line (三线表) style.
Usage: python3 build.py input.md output.docx
"""
import sys, subprocess, zipfile, os, shutil, re
from lxml import etree

MD, OUT = sys.argv[1], sys.argv[2]
REF = "reference.docx"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
NS = {"w": W, "m": M}
def w(tag): return f"{{{W}}}{tag}"
def mtag(tag): return f"{{{M}}}{tag}"

# 0. 预处理：将公式中的多字母变量名包裹为 \mathit{}，避免字母间距问题
IDENTS = ["Entrep","Post","Broadband","Firstyear","Treat","LS","VA","RP"]
def fix_math(m):
    s = m.group(0)
    for ident in IDENTS:
        s = re.sub(r'(?<![A-Za-z\\{])'+ident+r'(?![A-Za-z}])', r'\\text{'+ident+'}', s)
    return s
_src = open(MD, encoding="utf-8").read()
_src = re.sub(r'\$\$.*?\$\$', fix_math, _src, flags=re.S)          # display math
_src = re.sub(r'(?<!\$)\$(?!\$)[^\$\n]*?\$(?!\$)', fix_math, _src)  # inline math
MD_PRE = "._pre.md"
open(MD_PRE, "w", encoding="utf-8").write(_src)

# 1. pandoc
tmpdocx = "._pandoc_tmp.docx"
subprocess.run(["pandoc", MD_PRE, "-o", tmpdocx, "--reference-doc", REF,
                "-f", "markdown+tex_math_dollars+raw_tex-subscript-superscript"], check=True)

# 2. unzip
wd = "._docx_work"
if os.path.exists(wd): shutil.rmtree(wd)
os.makedirs(wd)
with zipfile.ZipFile(tmpdocx) as z:
    z.extractall(wd)

docpath = os.path.join(wd, "word", "document.xml")
tree = etree.parse(docpath)
root = tree.getroot()
body = root.find(w("body"))

def para_text(p):
    return "".join(t.text or "" for t in p.iter(w("t")))

def make_eqnum_table(math_p, number):
    """Wrap a math paragraph into a borderless 3-col table with right-aligned number."""
    tbl_xml = f'''<w:tbl xmlns:w="{W}" xmlns:m="{M}">
      <w:tblPr>
        <w:tblW w:w="9440" w:type="dxa"/>
        <w:jc w:val="center"/>
        <w:tblBorders>
          <w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>
          <w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>
          <w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>
          <w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>
          <w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>
          <w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>
        </w:tblBorders>
        <w:tblLayout w:type="fixed"/>
        <w:tblCellMar>
          <w:top w:w="0" w:type="dxa"/><w:left w:w="0" w:type="dxa"/>
          <w:bottom w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/>
        </w:tblCellMar>
        <w:tblCaption w:val="__eqnum__"/>
      </w:tblPr>
      <w:tblGrid>
        <w:gridCol w:w="850"/><w:gridCol w:w="7740"/><w:gridCol w:w="850"/>
      </w:tblGrid>
      <w:tr>
        <w:tc><w:tcPr><w:tcW w:w="850" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>
          <w:p><w:pPr><w:ind w:firstLine="0" w:firstLineChars="0"/></w:pPr></w:p></w:tc>
        <w:tc><w:tcPr><w:tcW w:w="7740" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>
          <w:p><w:pPr><w:jc w:val="center"/><w:ind w:firstLine="0" w:firstLineChars="0"/></w:pPr></w:p></w:tc>
        <w:tc><w:tcPr><w:tcW w:w="850" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>
          <w:p><w:pPr><w:jc w:val="right"/><w:ind w:firstLine="0" w:firstLineChars="0"/></w:pPr>
            <w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="宋体"/></w:rPr><w:t xml:space="preserve">（{number}）</w:t></w:r></w:p></w:tc>
      </w:tr>
    </w:tbl>'''
    tbl = etree.fromstring(tbl_xml)
    # place the math paragraph's content into the middle cell paragraph
    tcs = tbl.findall(f".//{w('tc')}")
    mid_p = tcs[1].find(w("p"))
    # move all children of math_p (except pPr) into mid_p (keep mid_p's pPr)
    math_ppr = math_p.find(w("pPr"))
    for child in list(math_p):
        if child.tag == w("pPr"):
            continue
        mid_p.append(child)
    return tbl

# 3. Equation numbering pass
children = list(body)
i = 0
while i < len(children):
    el = children[i]
    if el.tag == w("p") and el.find(f".//{mtag('oMathPara')}") is not None:
        # look ahead for EQNUM marker
        j = i + 1
        if j < len(children):
            nxt = children[j]
            m = re.match(r"^\s*EQNUM:(\S+)\s*$", para_text(nxt)) if nxt.tag == w("p") else None
            if m:
                number = m.group(1)
                tbl = make_eqnum_table(el, number)
                el.addprevious(tbl)
                body.remove(el)
                body.remove(nxt)
                children = list(body)
                i = list(body).index(tbl) + 1
                continue
    i += 1

# 4. Three-line table pass (skip our equation-number tables)
def set_three_line(tbl):
    # 列数
    rows = tbl.findall(w("tr"))
    ncol = len(rows[0].findall(w("tc"))) if rows else 0
    total, first = 9200, 2600
    rest = (total - first)//(ncol-1) if ncol > 1 else total
    widths = [first] + [rest]*(ncol-1) if ncol > 1 else [total]
    # 重建 tblGrid（列宽）
    old_grid = tbl.find(w("tblGrid"))
    if old_grid is not None: tbl.remove(old_grid)
    grid = etree.Element(w("tblGrid"))
    for wd in widths:
        gc = etree.SubElement(grid, w("gridCol")); gc.set(w("w"), str(wd))
    # 重建 tblPr（按 schema 顺序：tblStyle→tblW→jc→tblBorders→tblLayout→tblCellMar→tblLook）
    old_pr = tbl.find(w("tblPr"))
    if old_pr is not None: tbl.remove(old_pr)
    pr = etree.fromstring(f'''<w:tblPr xmlns:w="{W}">
        <w:tblW w:w="{total}" w:type="dxa"/>
        <w:jc w:val="center"/>
        <w:tblBorders>
          <w:top w:val="single" w:sz="12" w:space="0" w:color="auto"/>
          <w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>
          <w:bottom w:val="single" w:sz="12" w:space="0" w:color="auto"/>
          <w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>
          <w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>
          <w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>
        </w:tblBorders>
        <w:tblLayout w:type="fixed"/>
        <w:tblCellMar>
          <w:top w:w="15" w:type="dxa"/><w:left w:w="80" w:type="dxa"/>
          <w:bottom w:w="15" w:type="dxa"/><w:right w:w="80" w:type="dxa"/>
        </w:tblCellMar>
        <w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>
      </w:tblPr>''')
    tbl.insert(0, pr)
    tbl.insert(1, grid)   # tblGrid 紧跟 tblPr
    # 单元格宽度 + 表头行底边框 + 行不跨页断开
    for ri, r in enumerate(rows):
        trPr = r.find(w("trPr"))
        if trPr is None:
            trPr = etree.Element(w("trPr")); r.insert(0, trPr)
        if trPr.find(w("cantSplit")) is None:
            etree.SubElement(trPr, w("cantSplit"))
        if ri == 0 and trPr.find(w("tblHeader")) is None:
            etree.SubElement(trPr, w("tblHeader"))  # 跨页时重复表头
        for idx, tc in enumerate(r.findall(w("tc"))):
            tcPr = tc.find(w("tcPr"))
            if tcPr is None:
                tcPr = etree.Element(w("tcPr")); tc.insert(0, tcPr)
            for e in tcPr.findall(w("tcW")): tcPr.remove(e)
            for e in tcPr.findall(w("tcBorders")): tcPr.remove(e)
            tcw = etree.Element(w("tcW"))
            tcw.set(w("w"), str(widths[idx] if idx < len(widths) else rest)); tcw.set(w("type"),"dxa")
            tcPr.insert(0, tcw)
            if ri == 0:
                tcb = etree.fromstring(f'<w:tcBorders xmlns:w="{W}"><w:bottom w:val="single" w:sz="6" w:space="0" w:color="auto"/></w:tcBorders>')
                tcPr.append(tcb)

def is_eqnum_table(tbl):
    cap = tbl.find(f"{w('tblPr')}/{w('tblCaption')}")
    return cap is not None and cap.get(w("val")) == "__eqnum__"

for tbl in body.iter(w("tbl")):
    if is_eqnum_table(tbl):
        continue  # our borderless equation-number table
    set_three_line(tbl)

# 4b. 表题/图题/注释 段落样式
def set_ppr(p, jc="center", eastAsia="黑体", sz="18", indent0=True, bold=False, keepnext=False):
    ppr = p.find(w("pPr"))
    if ppr is None:
        ppr = etree.Element(w("pPr")); p.insert(0, ppr)
    for tag in ["jc","ind","keepNext"]:
        for e in ppr.findall(w(tag)): ppr.remove(e)
    if keepnext:
        ppr.insert(0, etree.Element(w("keepNext")))
    j = etree.SubElement(ppr, w("jc")); j.set(w("val"), jc)
    if indent0:
        ind = etree.SubElement(ppr, w("ind"))
        ind.set(w("firstLine"),"0"); ind.set(w("firstLineChars"),"0")
    # run fonts
    for r in p.findall(w("r")):
        rpr = r.find(w("rPr"))
        if rpr is None:
            rpr = etree.Element(w("rPr")); r.insert(0, rpr)
        for e in rpr.findall(w("rFonts")): rpr.remove(e)
        rf = etree.SubElement(rpr, w("rFonts"))
        rf.set(w("eastAsia"), eastAsia); rf.set(w("ascii"),"Times New Roman"); rf.set(w("hAnsi"),"Times New Roman")
        for e in rpr.findall(w("sz")): rpr.remove(e)
        for e in rpr.findall(w("szCs")): rpr.remove(e)
        s1=etree.SubElement(rpr,w("sz")); s1.set(w("val"),sz)
        s2=etree.SubElement(rpr,w("szCs")); s2.set(w("val"),sz)
        if bold:
            if rpr.find(w("b")) is None: etree.SubElement(rpr,w("b"))

# 4c. 含图片的段落：居中、自动行距(避免被固定行距裁剪)、无缩进
for p in body.findall(w("p")):
    if p.find(f".//{w('drawing')}") is None:
        continue
    ppr = p.find(w("pPr"))
    if ppr is None:
        ppr = etree.Element(w("pPr")); p.insert(0, ppr)
    for e in ppr.findall(w("spacing")): ppr.remove(e)
    for e in ppr.findall(w("jc")): ppr.remove(e)
    for e in ppr.findall(w("ind")): ppr.remove(e)
    sp = etree.SubElement(ppr, w("spacing"))
    sp.set(w("before"),"60"); sp.set(w("after"),"60"); sp.set(w("line"),"240"); sp.set(w("lineRule"),"auto")
    jc = etree.SubElement(ppr, w("jc")); jc.set(w("val"),"center")
    ind = etree.SubElement(ppr, w("ind")); ind.set(w("firstLine"),"0"); ind.set(w("firstLineChars"),"0")

for p in body.findall(w("p")):
    txt = para_text(p).strip()
    if re.match(r"^表\s*\d", txt):        # 表题：居中黑体小五，与表格同页
        set_ppr(p, jc="center", eastAsia="黑体", sz="18", keepnext=True)
    elif re.match(r"^图\s*\d", txt):      # 图题：居中黑体小五
        set_ppr(p, jc="center", eastAsia="黑体", sz="18")
    elif re.match(r"^(注：|资料来源：|数据来源：)", txt):  # 注释：左对齐宋体小五
        set_ppr(p, jc="left", eastAsia="宋体", sz="18")

# 5. write back
tree.write(docpath, xml_declaration=True, encoding="UTF-8", standalone=True)

# repackage
if os.path.exists(OUT): os.remove(OUT)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for r, _, files in os.walk(wd):
        for fn in files:
            full = os.path.join(r, fn)
            arc = os.path.relpath(full, wd)
            z.write(full, arc)
print("wrote", OUT)
