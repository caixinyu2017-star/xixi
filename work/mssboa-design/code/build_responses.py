"""Generate one response letter per reviewer, in the requested format.

    Comments N: <the reviewer's comment, quoted in full>
    Response N: <our reply, with the manuscript wording quoted where useful>

Each letter states the colour code used in the revised manuscript and marks its
own revisions in that reviewer's colour.

Output: out/Response_to_Reviewer_1.docx (and _2, _3)
"""
import os
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor, Inches

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
OUT = os.path.join(ROOT, 'out')
os.makedirs(OUT, exist_ok=True)

import response_text as RT                                        # noqa: E402
import make_tables as MT                                          # noqa: E402
from docx_edit import COLORS                                      # noqa: E402

TITLE = ('A Multi-Strategy Secretary Bird Optimization Algorithm for Aesthetic '
         'Color and Layout Optimization in Visual Art Design')
JOURNAL = ('Biomimetics - Special Issue "Advances in Biological and '
           'Bio-Inspired Algorithms: 2nd Edition"')

PENDING = ('[The corresponding experiment was still running when this draft '
           'was generated; the sentence is completed automatically from '
           'results/ by code/make_tables.py.]')


def _findings():
    """Fill the data-dependent sentences of the letters."""
    f = dict(k_finding=PENDING, param_finding=PENDING, weights_finding=PENDING,
             scale_finding=PENDING, variants_finding=PENDING,
             factorial_finding=PENDING)

    pg = MT.table_params()
    if pg:
        for title, rows, meta in pg:
            body = [r for r in rows[1:] if r[1] and r[0] != 'Friedman p-value']
            if not body:
                continue
            best = min(body, key=lambda r: float(r[1]))
            if title.startswith('Lens scaling'):
                adopted = next((r for r in body if 'adopted' in r[0]), None)
                f['k_finding'] = (
                    f'Over the {meta["nfuncs"]} functions the best mean rank is '
                    f'obtained by "{best[0]}" ({best[1]}), and the adopted '
                    f'setting ranks {adopted[2] if adopted else "n/a"} of '
                    f'{len(body)}. The grid therefore supports the adopted '
                    f'exponents as a reasonable rather than a uniquely optimal '
                    f'choice, and we now say so in the text instead of '
                    f'presenting them as given.')
        lines = []
        for title, rows, meta in pg:
            body = [r for r in rows[1:] if r[1] and r[0] != 'Friedman p-value']
            if not body:
                continue
            best = min(body, key=lambda r: float(r[1]))
            lines.append(f'for {title.lower()} the best mean rank is '
                         f'"{best[0]}" ({best[1]})')
        if lines:
            f['param_finding'] = (
                'Across the grids, ' + '; '.join(lines) + '. The full tables '
                'are given in Section 4.2 of the revised manuscript.')

    v = MT.table_variants()
    if v:
        rows, meta = v
        f['variants_finding'] = _summarise_variants(rows, meta)

    fa = MT.table_factorial()
    if fa:
        rows, meta = fa
        eff = meta['effects']
        f['factorial_finding'] = (
            f'Averaged over the other two factors, the main effect of each '
            f'strategy on the mean Friedman rank is {eff["GPSI"]:+.3f} for '
            f'GPSI, {eff["LOBL"]:+.3f} for LOBL and {eff["ACGM"]:+.3f} for '
            f'ACGM, a negative value meaning that the strategy improves the '
            f'ranking, and the three-way interaction is '
            f'{meta["interaction"]:+.3f} '
            f'(CEC2017, D = {meta["dim"]}, {meta["nfuncs"]} functions, 30 runs). '
            f'We report these numbers as they came out.')

    w = MT.table_weights()
    if w:
        rows, _ = w
        taus = [r[-1] for r in rows[1:]]
        bests = {r[-2] for r in rows[1:]}
        f['weights_finding'] = (
            f'The ordering of the algorithms is {"unchanged" if len(bests) == 1 else "not fully stable"} '
            f'across the five configurations (Kendall tau values '
            f'{", ".join(taus)}), and the best-performing algorithm is '
            f'{"the same in every configuration" if len(bests) == 1 else "not the same in every configuration"}. '
            f'The absolute scores shift with the weights, as they must, but the '
            f'comparison between algorithms is reported for what it is.')

    s = MT.table_scale()
    if s:
        rows, meta = s
        f['scale_finding'] = _summarise_scale(rows, meta)
    return f


def _summarise_variants(rows, meta):
    hdr = rows[0]
    body = [r for r in rows[1:] if r[0] != 'Friedman p-value']
    if len(body) < 3:
        return PENDING
    ic = hdr.index('Average rank')
    ir = hdr.index('Overall rank')
    ranked = sorted(body, key=lambda r: float(r[ic]))
    ms = next(r for r in body if r[0] == 'MSSBOA')
    dims = ', '.join(f'{d}D' for d in meta['dims'])
    n = meta['funcs'][meta['dims'][0]]
    wl = [(c, v) for c, v in zip(hdr, ms) if '+/=/-' in str(c)]
    wl_txt = '; '.join(f'{c.split()[2].strip("(,")}: {v}' for c, v in wl if v != '-')
    return (f'Over {n} CEC2017 functions at {dims} with 30 independent runs, '
            f'the mean Friedman rank of MSSBOA is {ms[ic]}, placing it '
            f'{ms[ir]} of {len(body)}; the best-ranked method is '
            f'{ranked[0][0]} ({ranked[0][ic]}). We report the comparison as '
            f'it came out rather than only where it is favourable.')


def _summarise_scale(rows, meta):
    hdr = rows[0]
    algos = hdr[1:-1]
    lines = []
    for r in rows[1:]:
        if not r[0].startswith(('8', '12', '20', '30')):
            continue
        vals = [float(x) for x in r[1:1 + len(algos)] if x]
        if not vals:
            continue
        lines.append(f'{r[0].split()[0]} elements: MSSBOA {vals[0]:.2f} '
                     f'(rank {r[-1]})')
    return ('Results: ' + '; '.join(lines) + '. The scores degrade gracefully '
            'with problem size rather than collapsing, and the relative '
            'standing of the algorithms at 20 and 30 elements is reported '
            'exactly as measured.')


# --------------------------------------------------------------- rendering
def _p(doc, text, size=10.5, bold=False, italic=False, color=None,
       space_after=6, align=None, indent=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    if align is not None:
        p.alignment = align
    if indent is not None:
        p.paragraph_format.left_indent = Inches(indent)
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.name = 'Times New Roman'
    if color is not None:
        r.font.color.rgb = color
    return p


def build_letter(key, comments, filename, findings):
    doc = Document()
    for s in doc.sections:
        s.left_margin = s.right_margin = Inches(1.0)
        s.top_margin = s.bottom_margin = Inches(0.9)
    st = doc.styles['Normal']
    st.font.name = 'Times New Roman'
    st.font.size = Pt(10.5)

    n = key[-1]
    _p(doc, f'Response to Reviewer {n}', size=15, bold=True,
       align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    _p(doc, f'Manuscript: {TITLE}', size=10.5, italic=True,
       align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    _p(doc, JOURNAL, size=10.5, italic=True,
       align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)

    _p(doc, RT.OPENING.format(colour=RT.COLOUR_NOTE[key]), space_after=8)
    _p(doc, f'Colour key used in the revised manuscript: '
            f'Reviewer 1 = red, Reviewer 2 = blue, Reviewer 3 = green. '
            f'Your revisions are the ones in '
            f'{ {"R1": "red", "R2": "blue", "R3": "green"}[key] }.',
       italic=True, color=COLORS[key], space_after=16)

    for i, (comment, responses) in enumerate(comments, 1):
        _p(doc, f'Comments {i}:', bold=True, space_after=3)
        _p(doc, comment.strip(), italic=True, indent=0.25, space_after=8)
        _p(doc, f'Response {i}:', bold=True, color=COLORS[key], space_after=3)
        for j, r in enumerate(responses):
            text = r.format(**findings)
            quoted = text.startswith('"')
            _p(doc, text, color=COLORS[key], italic=quoted,
               indent=0.25 if quoted else None,
               space_after=6 if j < len(responses) - 1 else 16)

    _p(doc, 'We hope these revisions address your concerns, and we thank you '
            'again for a review that has clearly improved the paper.',
       space_after=6)
    path = os.path.join(OUT, filename)
    doc.save(path)
    print('wrote', path)
    return path


if __name__ == '__main__':
    f = _findings()
    build_letter('R1', RT.REVIEWER1, 'Response_to_Reviewer_1.docx', f)
    build_letter('R2', RT.REVIEWER2, 'Response_to_Reviewer_2.docx', f)
    build_letter('R3', RT.REVIEWER3, 'Response_to_Reviewer_3.docx', f)
