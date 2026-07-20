# -*- coding: utf-8 -*-
"""Assemble the full manuscript docx."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xml.sax.saxutils import escape

from mdpi_builder import (CITE_RE, build_docx, p_body, p_h1, p_h2, p_h3, p_hyp,
                          p_equation, p_table_caption, p_fig_caption, p_notes,
                          p_backmatter, p_reference, p_figure, three_line_table,
                          _tc, _borders, wrun)
import mdpi_builder
from paper_equations import EQUATIONS
from paper_content_part1 import PART1, TITLE, ABSTRACT, KEYWORDS
from paper_content_part2 import PART2
from paper_content_part3 import PART3
from paper_refs import REFS

SCRATCH = os.path.dirname(os.path.abspath(__file__))
BLOCKS = PART1 + PART2 + PART3

# ---------------------------------------------------------- citation numbering
def collect_keys(blocks):
    order = []
    for b in blocks:
        texts = []
        if b[0] in ('p', 'notes'):
            texts.append(b[1])
        elif b[0] == 'hyp':
            texts.append(b[2])
        for t in texts:
            for m in CITE_RE.finditer(t):
                for k in m.group(1).split('|'):
                    if k not in order:
                        order.append(k)
    return order

key_order = collect_keys(BLOCKS)
missing = [k for k in key_order if k not in REFS]
if missing:
    raise SystemExit('MISSING REFS: %s' % missing)
unused = [k for k in REFS if k not in key_order]
if unused:
    print('note: unused refs (will be omitted):', unused)
REFMAP = {k: i + 1 for i, k in enumerate(key_order)}
print('total references cited:', len(key_order))

# ------------------------------------------------------------- special tables
def render_table(rows, widths):
    # left-align long text cells (e.g., variable-definition tables)
    return three_line_table(rows, col_widths=widths)

# patch: allow left alignment for definition table by overriding cell align
_orig_tc = mdpi_builder._tc
def smart_table(rows, widths):
    ncols = len(rows[0])
    if widths is None:
        widths = [9640 // ncols] * ncols
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)

    def cell_len(c):
        return len(' '.join(c)) if isinstance(c, list) else len(str(c))
    # a column is left-aligned if it is the stub column or contains long prose
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
            align = 'left' if left_col[ci] else 'center'
            tcs.append(_orig_tc(cell, widths[ci], borders, bold=header, align=align))
        trpr = '<w:trPr>' + ('<w:tblHeader/>' if header else '') + '<w:jc w:val="center"/></w:trPr>'
        trs.append(f'<w:tr>{trpr}{"".join(tcs)}</w:tr>')
    tblpr = ('<w:tblPr><w:tblW w:w="0" w:type="auto"/><w:jc w:val="center"/>'
             '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:top w:w="0" w:type="dxa"/>'
             '<w:left w:w="40" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/>'
             '<w:right w:w="40" w:type="dxa"/></w:tblCellMar></w:tblPr>')
    return f'<w:tbl>{tblpr}<w:tblGrid>{grid}</w:tblGrid>{"".join(trs)}</w:tbl>'

# ------------------------------------------------------------------ front matter
front = open(os.path.join(SCRATCH, 'front_matter.xml'), encoding='utf8').read()

OLD_TITLE = ('Artificial Intelligence Adoption and Youth Employment: A Socio-Technical '
             'Systems Perspective on Business Model Innovation and Entrepreneurial Governance')
assert OLD_TITLE in front
front = front.replace(OLD_TITLE, escape(TITLE))

# MDPI article-type label above the title
front = ('<w:p><w:pPr><w:pStyle w:val="169"/></w:pPr>'
         '<w:r><w:t>Article</w:t></w:r></w:p>') + front

# title is left-aligned in the MDPI template, not justified
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
FIG_RIDS = {'fig_framework.png': 'rId20', 'fig_psm.png': 'rId21'}
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
        parts.append(p_equation(EQUATIONS[b[1]], b[2]))
    elif kind == 'tabcap':
        parts.append(p_table_caption(b[1], b[2]))
    elif kind == 'table':
        parts.append(smart_table(b[1], b[2]))
    elif kind == 'notes':
        parts.append(p_notes(b[1], REFMAP))
    elif kind == 'figure':
        parts.append(p_figure(FIG_RIDS[b[1]], b[2], b[3], b[4]))
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

# MDPI disclaimer boilerplate after the reference list
parts.append(p_backmatter(
    'Disclaimer/Publisher’s Note:',
    'The statements, opinions and data contained in all publications are solely those of the '
    'individual author(s) and contributor(s) and not of MDPI and/or the editor(s). MDPI and/or '
    'the editor(s) disclaim responsibility for any injury to people or property resulting from '
    'any ideas, methods, instructions or products referred to in the content.'))

body_xml = ''.join(parts)
out = build_docx(os.path.join(SCRATCH, 'template_scaffold.docx'),
                 os.path.join(SCRATCH, 'Zhejiang_Youth_Employment_Systems.docx'),
                 body_xml,
                 extra_media={'fig_framework.png': os.path.join(SCRATCH, 'fig_framework.png'),
                              'fig_psm.png': os.path.join(SCRATCH, 'fig_psm.png')})
print('built:', out)
