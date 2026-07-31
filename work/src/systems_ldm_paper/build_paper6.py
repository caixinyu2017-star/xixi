# -*- coding: utf-8 -*-
"""Assemble the paper-6 manuscript docx (digital transformation leadership ×
youth employment, enterprise survey)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xml.sax.saxutils import escape
from PIL import Image

from mdpi_builder import (CITE_RE, build_docx, p_body, p_h1, p_h2, p_h3, p_hyp,
                          p_equation, p_table_caption, p_fig_caption, p_notes,
                          p_backmatter, p_reference, p_figure, _tc, _borders, wrun)
from p6_equations import EQUATIONS_P6
from p6_content_a import PART_A, TITLE, ABSTRACT, KEYWORDS
from p6_content_b import PART_B
from p6_refs import REFS6 as REFS

SCRATCH = os.path.dirname(os.path.abspath(__file__))
BLOCKS = PART_A + PART_B

# ---------------------------------------------------------- citation numbering
def texts_of(b):
    if b[0] in ('p', 'notes'):
        return [b[1]]
    if b[0] == 'hyp':
        return [b[2]]
    if b[0] == 'table':
        out = []
        for row in b[1]:
            for cell in row:
                out.extend(cell if isinstance(cell, list) else [cell])
        return [str(t) for t in out]
    return []

key_order = []
for b in BLOCKS:
    for t in texts_of(b):
        for m in CITE_RE.finditer(t):
            for k in m.group(1).split('|'):
                if k not in key_order:
                    key_order.append(k)
missing = [k for k in key_order if k not in REFS]
if missing:
    raise SystemExit('MISSING REFS: %s' % missing)
REFMAP = {k: i + 1 for i, k in enumerate(key_order)}
print('total references cited:', len(key_order))
recent = sum(1 for k in key_order if REFS[k]['year'] >= '2023')
print('2023+ share: %d/%d = %.0f%%' % (recent, len(key_order), 100 * recent / len(key_order)))

# ---------------------------------------------------------- tables (with citations)
def _fmt_cell_cites(text):
    return CITE_RE.sub(
        lambda m: '[' + ','.join(str(REFMAP[k]) for k in m.group(1).split('|')) + ']', text)

def smart_table(rows, widths, repeat_header=True):
    ncols = len(rows[0])
    if widths is None:
        widths = [9640 // ncols] * ncols

    def cell_len(c):
        return len(' '.join(c)) if isinstance(c, list) else len(str(c))
    left_col = [ci == 0 or max(cell_len(r[ci]) for r in rows) > 45
                for ci in range(ncols)]
    trs = []
    for ri, row in enumerate(rows):
        header = ri == 0
        last = ri == len(rows) - 1
        borders = _borders(top=8 if header else None,
                           bottom=6 if header else (8 if last else None))
        tcs = []
        for ci, cell in enumerate(row):
            if isinstance(cell, list):
                cell = [_fmt_cell_cites(str(x)) for x in cell]
            else:
                cell = _fmt_cell_cites(str(cell))
            align = 'left' if left_col[ci] else 'center'
            tcs.append(_tc(cell, widths[ci], borders, bold=header, align=align))
        trpr = ('<w:trPr>' + ('<w:tblHeader/>' if header and repeat_header else '')
                + '<w:jc w:val="center"/></w:trPr>')
        trs.append(f'<w:tr>{trpr}{"".join(tcs)}</w:tr>')
    tblpr = ('<w:tblPr><w:tblW w:w="0" w:type="auto"/><w:jc w:val="center"/>'
             '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:top w:w="0" w:type="dxa"/>'
             '<w:left w:w="40" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/>'
             '<w:right w:w="40" w:type="dxa"/></w:tblCellMar></w:tblPr>')
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    return f'<w:tbl>{tblpr}<w:tblGrid>{grid}</w:tblGrid>{"".join(trs)}</w:tbl>'

# ------------------------------------------------------------------ front matter
front = open(os.path.join(SCRATCH, 'front_matter.xml'), encoding='utf8').read()

OLD_TITLE = ('Artificial Intelligence Adoption and Youth Employment: A Socio-Technical '
             'Systems Perspective on Business Model Innovation and Entrepreneurial Governance')
assert OLD_TITLE in front
front = front.replace(OLD_TITLE, escape(TITLE))

front = ('<w:p><w:pPr><w:pStyle w:val="169"/></w:pPr>'
         '<w:r><w:t>Article</w:t></w:r></w:p>') + front

TITLE_PPR = ('<w:pPr><w:spacing w:after="120"/><w:ind w:left="0" w:leftChars="0" '
             'w:firstLine="0" w:firstLineChars="0"/></w:pPr>')
assert TITLE_PPR in front
front = front.replace(
    TITLE_PPR,
    '<w:pPr><w:spacing w:after="120"/><w:ind w:left="0" w:leftChars="0" '
    'w:firstLine="0" w:firstLineChars="0"/><w:jc w:val="left"/></w:pPr>', 1)

m = re.search(r'(<w:t>)(The diffusion of artificial intelligence.*?entrepreneurship\.)(</w:t>)', front, re.S)
assert m, 'abstract body not found'
front = front[:m.start(2)] + escape(ABSTRACT) + front[m.end(2):]

m = re.search(r'(<w:t>)(artificial intelligence adoption; youth employment;.*?technological change)(</w:t>)', front, re.S)
assert m, 'keywords not found'
front = front[:m.start(2)] + escape(KEYWORDS) + front[m.end(2):]

# ------------------------------------------------------------------ body
FIG_RIDS = {f'p6_fig{i}.png': f'rId{19 + i}' for i in range(1, 6)}
EMU_PER_IN = 914400

def fig_emu(name, width_in):
    with Image.open(os.path.join(SCRATCH, name)) as im:
        w, h = im.size
    cx = int(width_in * EMU_PER_IN)
    cy = int(cx * h / w)
    return cx, cy

parts = [front]
for b in BLOCKS:
    kind = b[0]
    if kind == 'h1':
        parts.append(p_h1(b[1]))
    elif kind == 'h2':
        parts.append(p_h2(b[1]))
    elif kind == 'h3':
        parts.append(p_h3(b[1]))
    elif kind == 'p':
        parts.append(p_body(b[1], REFMAP))
    elif kind == 'hyp':
        parts.append(p_hyp(b[1], b[2], REFMAP))
    elif kind == 'eq':
        parts.append(p_equation(EQUATIONS_P6[b[1]], b[2]))
    elif kind == 'tabcap':
        parts.append(p_table_caption(b[1], b[2]))
    elif kind == 'table':
        parts.append(smart_table(b[1], b[2],
                                 repeat_header=(len(b) < 4 or b[3] != 'norepeat')))
    elif kind == 'notes':
        parts.append(p_notes(b[1], REFMAP))
    elif kind == 'figure':
        cx, cy = fig_emu(b[1], b[2])
        parts.append(p_figure(FIG_RIDS[b[1]], cx, cy, b[4]))
    elif kind == 'figcap':
        parts.append(p_fig_caption(b[1], b[2]))
    elif kind == 'back':
        parts.append(p_backmatter(b[1], b[2]))
    else:
        raise SystemExit('unknown block: %r' % (b[:1],))

# ------------------------------------------------------------------ references
parts.append(p_h1('References'))
REF_PPR = '<w:spacing w:after="20"/><w:ind w:left="2920" w:hanging="312"/><w:jc w:val="both"/>'
for k in key_order:
    r = REFS[k]
    if r.get('raw'):
        inner = wrun(f"{REFMAP[k]}. {r['full']}", sz=16)
        parts.append(f'<w:p><w:pPr>{REF_PPR}</w:pPr>{inner}</w:p>')
        continue
    tail = ''
    if r.get('volume'):
        tail = r['volume'] + '|' + r.get('pages', '')
    elif r.get('pages'):
        tail = '|' + r['pages']
    parts.append(p_reference(REFMAP[k], r['authors'], r['title'],
                             r['journal'], r['year'], tail))

parts.append(p_backmatter(
    'Disclaimer/Publisher’s Note:',
    'The statements, opinions and data contained in all publications are solely those of the '
    'individual author(s) and contributor(s) and not of MDPI and/or the editor(s). MDPI and/or '
    'the editor(s) disclaim responsibility for any injury to people or property resulting from '
    'any ideas, methods, instructions or products referred to in the content.'))

body_xml = ''.join(parts)
out = build_docx(os.path.join(SCRATCH, 'template_scaffold.docx'),
                 os.path.join(SCRATCH, 'Digital_Leadership_Decision_Agility_Systems.docx'),
                 body_xml,
                 extra_media={f'p6_fig{i}.png': os.path.join(SCRATCH, f'p6_fig{i}.png')
                              for i in range(1, 6)})

# ------------------------------------------- patch header/footer volume/year
import zipfile, shutil, tempfile
tmp = out + '.tmp'
with zipfile.ZipFile(out) as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename in ('word/header1.xml', 'word/footer2.xml'):
            x = data.decode('utf8')
            x = x.replace('<w:t>2025</w:t>', '<w:t>2026</w:t>')
            x = x.replace('<w:t xml:space="preserve"> 13</w:t>',
                          '<w:t xml:space="preserve"> 14</w:t>')
            data = x.encode('utf8')
        elif item.filename == 'word/document.xml':
            x = data.decode('utf8')
            x = x.replace('© 2025 by the authors', '© 2026 by the authors')
            data = x.encode('utf8')
        zout.writestr(item, data)
shutil.move(tmp, out)
print('built:', out)
