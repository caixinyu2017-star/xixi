# -*- coding: utf-8 -*-
"""Assemble the paper-3 manuscript docx (LLM assessment of youth career distress)
on the official MDPI Behavioral Sciences template."""
import os, re, struct, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bs_builder import (CITE_RE, build_docx, p_style, p_h1, p_h2, p_h3, p_body,
                        p_body_ni, p_hyp, p_equation, p_table_caption,
                        p_fig_caption, p_notes, p_backmatter, p_reference,
                        p_figure, smart_table, wr, rich_runs,
                        check_intext_collisions, _sortkey)
from p3_equations import EQUATIONS_P3
from p3_content_a import PART_A, TITLE, ABSTRACT, KEYWORDS
from p3_content_b import PART_B
from p3_refs import REFS3

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- inject verified bibliographic fields (DOI, issue, corrected title/pages)
import json as _json, difflib as _difflib
_rv = os.path.join(HERE, 'references_verified.json')
if os.path.exists(_rv):
    _recs = _json.load(open(_rv))['records']
    for _k, _rec in _recs.items():
        if _k not in REFS3 or _rec['verdict'] != 'CONFIRMED' or REFS3[_k].get('raw'):
            continue
        _fin = _rec['final']
        _e = REFS3[_k]
        if _fin.get('doi') and not _e.get('doi'):
            _e['doi'] = _fin['doi']
        for _fld in ('issue', 'volume', 'pages'):
            if _fin.get(_fld) and not _e.get(_fld):
                _e[_fld] = _fin[_fld]
        _vt = (_fin.get('title') or '').strip().rstrip('.')
        _norm = lambda t: ' '.join(t.lower().replace('—', '–').replace('’', "'").split())
        if _vt and _norm(_vt) != _norm(_e['title']):
            if _difflib.SequenceMatcher(None, _norm(_vt), _norm(_e['title'])).ratio() > 0.72:
                print(f'title update {_k}: {_e["title"][:50]!r} -> {_vt[:60]!r}')
                _e['title'] = _vt

BLOCKS = PART_A + PART_B

# ------------------------------------------------------------- citation audit
def texts_of(b):
    if b[0] in ('p', 'pni', 'notes', 'quote'):
        return [b[1]]
    if b[0] == 'hyp':
        return [b[2]]
    if b[0] in ('tabcap', 'figcap'):
        return [b[2]]
    if b[0] == 'table':
        out = []
        for row in b[1]:
            for cell in row:
                out.extend(cell if isinstance(cell, list) else [str(cell)])
        return out
    return []

used = []
for b in BLOCKS:
    for t in texts_of(b):
        for m in CITE_RE.finditer(t):
            for k in m.group(1).lstrip('@').split('|'):
                if k not in used:
                    used.append(k)
missing = [k for k in used if k not in REFS3]
if missing:
    raise SystemExit('MISSING REFS: %s' % missing)
unused = [k for k in REFS3 if k not in used]
if unused:
    print('note: unused refs (dropped from list):', unused)
check_intext_collisions(REFS3, used)
print('references cited:', len(used))

# ------------------------------------------------------------- figure sizing
def png_size(path):
    with open(path, 'rb') as f:
        head = f.read(24)
    w, h = struct.unpack('>II', head[16:24])
    return w, h

FIG_WIDTH_IN = {'p3_fig1.png': 6.55, 'p3_fig2.png': 6.90, 'p3_fig3.png': 6.10,
                'p3_fig4.png': 4.30, 'p3_fig5.png': 6.80}
FIG_RIDS = {f'p3_fig{i}.png': f'rId{19 + i}' for i in range(1, 6)}

def fig_block(fname, doc_id):
    w, h = png_size(os.path.join(HERE, fname))
    cx = int(FIG_WIDTH_IN[fname] * 914400)
    cy = int(cx * h / w)
    return p_figure(FIG_RIDS[fname], cx, cy, doc_id)

# ------------------------------------------------------------- front matter
def front_matter():
    parts = []
    parts.append(p_style('MDPI11articletype', wr('Article')))
    parts.append(p_style('MDPI12title', wr(TITLE)))
    authors = (wr('Xinyu Cai ') + wr('1', sup=True) + wr(', Dingpei Hu ')
               + wr('1', sup=True) + wr(' and Tiantian Mo ') + wr('1,', sup=True) + wr('*'))
    parts.append(p_style('MDPI13authornames', authors))
    FR = ('<w:framePr w:w="2155" w:hSpace="181" w:vSpace="120" w:wrap="around" '
          'w:vAnchor="text" w:hAnchor="margin" w:x="1" w:y="1"/>')
    parts.append(p_style('MDPI15academiceditor',
                         wr('Academic Editor: Danilo Garcia'),
                         FR + '<w:spacing w:before="0" w:after="120"/>'))
    for lab in ('Received: date', 'Revised: date', 'Accepted: date', 'Published: date'):
        parts.append(p_style('MDPI14history', wr(lab),
                             FR + ('<w:spacing w:before="120"/>' if lab.startswith('Received') else '')))
    parts.append(p_style('MDPI61citation',
                         wr('Citation: ', b=True) + wr('To be added by editorial staff during production.'),
                         FR))
    parts.append(p_style('MDPI72copyright',
                         wr('Copyright:', b=True) + wr(' © 2026 by the authors. Submitted for possible open '
                            'access publication under the terms and conditions of the Creative Commons '
                            'Attribution (CC BY) license (https://creativecommons.org/licenses/by/4.0/).'),
                         FR))
    parts.append(p_style('MDPI16affiliation',
                         wr('1', sup=True) + '<w:r><w:tab/></w:r>'
                         + wr('College of Business, Jiaxing University, Jiaxing 314001, China; '
                              'caixinyu@zjxu.edu.cn (X.C.); hudingpei@zjxu.edu.cn (D.H.)')))
    parts.append(p_style('MDPI16affiliation',
                         wr('*', b=True) + '<w:r><w:tab/></w:r>'
                         + wr('Correspondence: 00008227@zjxu.edu.cn')))
    parts.append(p_style('MDPI17abstract', wr('Abstract', b=True), '<w:jc w:val="left"/>'))
    parts.append(p_style('MDPI17abstract', wr(ABSTRACT), '<w:spacing w:before="0" w:after="0"/>'))
    parts.append(p_style('MDPI18keywords', wr('Keywords: ', b=True) + wr(KEYWORDS)))
    parts.append(p_style('MDPI19line', ''))
    return ''.join(parts)

# --------------------------------------------------------------------- body
parts = [front_matter()]
doc_id = 100
for b in BLOCKS:
    kind = b[0]
    if kind == 'h1':
        parts.append(p_h1(b[1]))
    elif kind == 'h2':
        parts.append(p_h2(b[1]))
    elif kind == 'h3':
        parts.append(p_h3(b[1]))
    elif kind == 'p':
        parts.append(p_body(b[1], REFS3))
    elif kind == 'pni':
        parts.append(p_body_ni(b[1], REFS3))
    elif kind == 'hyp':
        parts.append(p_hyp(b[1], b[2], REFS3))
    elif kind == 'eq':
        parts.append(p_equation(EQUATIONS_P3[b[1]], b[2]))
    elif kind == 'tabcap':
        parts.append(p_table_caption(b[1], b[2], REFS3))
    elif kind == 'table':
        parts.append(smart_table(b[1], b[2], refs=REFS3))
    elif kind == 'notes':
        parts.append(p_notes(b[1], REFS3))
    elif kind == 'figure':
        doc_id += 1
        parts.append(fig_block(b[1], doc_id))
    elif kind == 'figcap':
        parts.append(p_fig_caption(b[1], b[2], REFS3))
    elif kind == 'back':
        parts.append(p_backmatter(b[1], b[2], REFS3))
    else:
        raise SystemExit('unknown block: %r' % (b[:1],))

# --------------------------------------------------------------- references
parts.append(p_h1('References'))
for k in sorted(used, key=lambda k: (_sortkey(REFS3[k]['authors']), REFS3[k]['year'])):
    parts.append(p_reference(REFS3[k]))

parts.append(p_style('MDPI63notes',
    wr('Disclaimer/Publisher’s Note: ', b=True)
    + wr('The statements, opinions and data contained in all publications are solely those of the '
         'individual author(s) and contributor(s) and not of MDPI and/or the editor(s). MDPI and/or '
         'the editor(s) disclaim responsibility for any injury to people or property resulting from '
         'any ideas, methods, instructions or products referred to in the content.')))

out = build_docx(os.path.join(HERE, 'behavsci_template.dot'),
                 os.path.join(HERE, 'LLM_Career_Distress_BehavSci.docx'),
                 ''.join(parts),
                 extra_media={f: os.path.join(HERE, f) for f in FIG_RIDS})
print('built:', out)
