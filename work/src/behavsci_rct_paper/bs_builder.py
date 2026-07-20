# -*- coding: utf-8 -*-
"""MDPI Behavioral Sciences docx builder.

Targets the official behavsci template (.dot, docx-format zip): writes a fresh
word/document.xml that uses the template's own named styles (MDPI11articletype,
MDPI31text, ...), keeps its headers/footers/line numbering, and repackages the
zip. Citation style: APA author-year in text ({{key}}, {{k1|k2}}, {{@key}} for
narrative cites), alphabetical unnumbered APA reference list (full journal
names, DOIs). Display equations: OMML inside the template's two-column
equation table (MDPI39equation / MDPI3aequationnumber).

Inline markup in content strings:
  {{key}} / {{k1|k2}}  -> (Author, 2024; Author & Author, 2023)
  {{@key}}             -> Author et al. (2024)
  ⟦text⟧               -> italic span (APA stats symbols: p, F, t, r, ...)
  ⟪spec⟫               -> inline OMML math (NAME, NAME_{sub}, NAME^{sup})
  ^{text}              -> not supported in body; use wr(..., sup=True) directly
"""
import re, shutil, zipfile, os, tempfile, unicodedata
from xml.sax.saxutils import escape

SCRATCH = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- OMML helpers
_LO_MATH_KEYWORDS = {'size', 'int', 'sum', 'mod', 'ln', 'log', 'exp', 'abs',
                     'lim', 'sin', 'cos', 'tan', 'func', 'fact', 'it'}

def _mr_raw(t, upright=False, bold=False):
    sty = []
    if upright:
        sty.append('<m:sty m:val="p"/>')
    if bold:
        sty.append('<m:sty m:val="b"/>')
    pr = '<m:rPr>' + ''.join(sty) + '</m:rPr>' if sty else '<m:rPr/>'
    sp = ' xml:space="preserve"' if t != t.strip() or ' ' in t else ''
    return f'<m:r>{pr}<m:t{sp}>{escape(t)}</m:t></m:r>'

def mr(t, upright=False, bold=False):
    if t and t.strip().lower() in _LO_MATH_KEYWORDS and len(t.strip()) > 1:
        s = t.strip()
        return _mr_raw(s[0], upright, bold) + _mr_raw(s[1:], upright, bold)
    return _mr_raw(t, upright, bold)

def msub(base, sub):
    return f'<m:sSub><m:sSubPr/><m:e>{base}</m:e><m:sub>{sub}</m:sub></m:sSub>'

def msup(base, sup):
    return f'<m:sSup><m:sSupPr/><m:e>{base}</m:e><m:sup>{sup}</m:sup></m:sSup>'

def mfrac(num, den):
    return f'<m:f><m:fPr/><m:num>{num}</m:num><m:den>{den}</m:den></m:f>'

def msum(sub, sup, body, chr_='∑'):
    pr = [f'<m:chr m:val="{chr_}"/>', '<m:limLoc m:val="subSup"/>']
    if not sub:
        pr.append('<m:subHide m:val="1"/>')
    if not sup:
        pr.append('<m:supHide m:val="1"/>')
    return ('<m:nary><m:naryPr>' + ''.join(pr) + '</m:naryPr>'
            f'<m:sub>{sub}</m:sub><m:sup>{sup}</m:sup><m:e>{body}</m:e></m:nary>')

def mdelim(body, left='(', right=')'):
    return (f'<m:d><m:dPr><m:begChr m:val="{left}"/><m:endChr m:val="{right}"/></m:dPr>'
            f'<m:e>{body}</m:e></m:d>')

def macc(base, chr_='̄'):
    return (f'<m:acc><m:accPr><m:chr m:val="{chr_}"/></m:accPr>'
            f'<m:e>{base}</m:e></m:acc>')

def msqrt(body):
    return f'<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/><m:e>{body}</m:e></m:rad>'

def omath(inner):
    return f'<m:oMath>{inner}</m:oMath>'

_GREEK = {'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ', 'epsilon': 'ε',
          'lambda': 'λ', 'mu': 'μ', 'theta': 'θ', 'phi': 'φ', 'eta': 'η',
          'kappa': 'κ', 'omega': 'ω', 'sigma': 'σ', 'times': '×', 'prime': '′'}

def inline_math(spec):
    spec = spec.strip()
    for k, v in _GREEK.items():
        spec = spec.replace('\\' + k, v)
    if '_' in spec and '_{' not in spec:
        return wr(spec, i=True)
    m = re.fullmatch(r'([^_^]+?)_\{([^}]*)\}\^\{([^}]*)\}', spec)
    if m:
        return omath(f'<m:sSubSup><m:sSubSupPr/><m:e>{mr(m.group(1))}</m:e>'
                     f'<m:sub>{mr(m.group(2))}</m:sub><m:sup>{mr(m.group(3))}</m:sup></m:sSubSup>')
    m = re.fullmatch(r'([^_^]+?)_\{([^}]*)\}', spec)
    if m:
        return omath(msub(mr(m.group(1)), mr(m.group(2))))
    m = re.fullmatch(r'([^_^]+?)\^\{([^}]*)\}', spec)
    if m:
        return omath(msup(mr(m.group(1)), mr(m.group(2))))
    return omath(mr(spec))

# ---------------------------------------------------------- run / rich text
def wr(text, b=False, i=False, sup=False, sz=None, font=None):
    """Run inheriting the paragraph style; only toggles are set."""
    rpr = []
    if font:
        rpr.append(f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:eastAsia="{font}"/>')
    if b:
        rpr.append('<w:b/>')
    if i:
        rpr.append('<w:i/>')
    if sz:
        rpr.append(f'<w:sz w:val="{sz}"/>')
    if sup:
        rpr.append('<w:vertAlign w:val="superscript"/>')
    pr = f'<w:rPr>{"".join(rpr)}</w:rPr>' if rpr else ''
    sp = ' xml:space="preserve"' if text != text.strip() else ''
    return f'<w:r>{pr}<w:t{sp}>{escape(text)}</w:t></w:r>'

CITE_RE = re.compile(r'\{\{([@~]?[a-zA-Z0-9_|]+)\}\}')
IMATH_RE = re.compile(r'⟪(.+?)⟫')
ITAL_RE = re.compile(r'⟦(.+?)⟧')

def _sortkey(s):
    t = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return ' '.join(re.sub(r'[^a-z0-9 ]', '', t).split())

def fmt_citation(spec, refs):
    """{{k1|k2}} -> (A et al., 2023; B, 2024); {{@key}} -> A et al. (2024);
    {{~key}} -> A et al., 2024 (bare, for use inside an existing parenthesis).
    Same-author works are merged per APA: (Ryan & Deci, 2000, 2017)."""
    if spec.startswith('@'):
        r = refs[spec[1:]]
        return f"{r['intext']} ({r['year']}{r.get('suffix','')})"
    if spec.startswith('~'):
        r = refs[spec[1:]]
        return f"{r['intext']}, {r['year']}{r.get('suffix','')}"
    keys = spec.split('|')
    parts = sorted((refs[k] for k in keys),
                   key=lambda r: (_sortkey(r.get('sort') or r['intext']), r['year']))
    groups = []
    for r in parts:
        yr = f"{r['year']}{r.get('suffix','')}"
        if groups and groups[-1][0] == r['intext']:
            groups[-1][1].append(yr)
        else:
            groups.append([r['intext'], [yr]])
    return '(' + '; '.join(f"{g[0]}, {', '.join(g[1])}" for g in groups) + ')'

def rich_runs(text, refs, b=False, i=False, sz=None):
    text = CITE_RE.sub(lambda m: fmt_citation(m.group(1), refs), text)
    out = []
    # split by math first, then italics inside the plain segments
    pos = 0
    for m in IMATH_RE.finditer(text):
        if m.start() > pos:
            out.append(_ital_runs(text[pos:m.start()], b, i, sz))
        out.append(inline_math(m.group(1)))
        pos = m.end()
    if pos < len(text):
        out.append(_ital_runs(text[pos:], b, i, sz))
    return ''.join(out)

def _ital_runs(text, b, i, sz):
    out, pos = [], 0
    for m in ITAL_RE.finditer(text):
        if m.start() > pos:
            out.append(wr(text[pos:m.start()], b=b, i=i, sz=sz))
        seg = m.group(1)
        pos = m.end()
        if pos < len(text) and text[pos] == ' ':
            seg += ' '
            pos += 1
        out.append(wr(seg, b=b, i=True, sz=sz))
    if pos < len(text):
        out.append(wr(text[pos:], b=b, i=i, sz=sz))
    return ''.join(out)

# ---------------------------------------------------------- paragraph blocks
def p_style(style, runs_xml, extra_ppr=''):
    return f'<w:p><w:pPr><w:pStyle w:val="{style}"/>{extra_ppr}</w:pPr>{runs_xml}</w:p>'

def p_h1(text):
    return p_style('MDPI21heading1', wr(text, b=True), '<w:keepNext/>')

def p_h2(text):
    return p_style('MDPI22heading2', wr(text, i=True), '<w:keepNext/>')

def p_h3(text):
    return p_style('MDPI23heading3', wr(text), '<w:keepNext/>')

def p_body(text, refs):
    return p_style('MDPI31text', rich_runs(text, refs))

def p_body_ni(text, refs):
    return p_style('MDPI31text', rich_runs(text, refs),
                   '<w:ind w:left="2608" w:firstLine="0"/>')

def p_quote(text, refs):
    """Indented translated participant quote (italic)."""
    return p_style('MDPI31text', rich_runs(text, refs, i=True),
                   '<w:ind w:left="2948" w:right="340" w:firstLine="0"/>'
                   '<w:spacing w:before="60" w:after="60"/>')

def p_hyp(label, text, refs):
    inner = wr(label + ' ', b=True) + rich_runs(text, refs, i=True)
    return p_style('MDPI31text', inner,
                   '<w:ind w:left="2948" w:firstLine="0"/>'
                   '<w:spacing w:before="60" w:after="60"/>')

def p_equation(omml_xml, number):
    """Template pattern: 2-column borderless table, eq cell + number cell."""
    return (
        '<w:tbl><w:tblPr><w:tblW w:w="7859" w:type="dxa"/><w:tblInd w:w="2608" w:type="dxa"/>'
        '<w:tblCellMar><w:left w:w="0" w:type="dxa"/><w:right w:w="0" w:type="dxa"/></w:tblCellMar>'
        '<w:tblLook w:val="04A0"/></w:tblPr>'
        '<w:tblGrid><w:gridCol w:w="7428"/><w:gridCol w:w="431"/></w:tblGrid>'
        '<w:tr><w:tc><w:tcPr><w:tcW w:w="7428" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>'
        f'<w:p><w:pPr><w:pStyle w:val="MDPI39equation"/></w:pPr>{omml_xml}</w:p></w:tc>'
        '<w:tc><w:tcPr><w:tcW w:w="431" w:type="dxa"/><w:vAlign w:val="center"/></w:tcPr>'
        f'<w:p><w:pPr><w:pStyle w:val="MDPI3aequationnumber"/></w:pPr>{wr(f"({number})")}</w:p></w:tc>'
        '</w:tr></w:tbl>')

def p_table_caption(num, text, refs):
    inner = wr(f'Table {num}. ', b=True) + rich_runs(text, refs)
    return p_style('MDPI41tablecaption', inner, '<w:keepNext/>')

def p_fig_caption(num, text, refs):
    inner = wr(f'Figure {num}. ', b=True) + rich_runs(text, refs)
    return p_style('MDPI51figurecaption', inner)

def p_notes(text, refs):
    return p_style('MDPI43tablefooter', rich_runs(text, refs, sz=16),
                   '<w:spacing w:before="40" w:after="200"/>')

def p_backmatter(label, text, refs=None):
    inner = wr(label + ' ', b=True) + (rich_runs(text, refs or {}, sz=18))
    return p_style('MDPI62backmatter', inner, '<w:spacing w:before="120" w:after="120"/>')

def p_figure(rid, cx, cy, doc_id):
    drawing = (f'<w:drawing><wp:inline distT="0" distB="0" distL="114300" distR="114300">'
               f'<wp:extent cx="{cx}" cy="{cy}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
               f'<wp:docPr id="{doc_id}" name="Picture {doc_id}"/>'
               '<wp:cNvGraphicFramePr><a:graphicFrameLocks '
               'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
               '</wp:cNvGraphicFramePr>'
               '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
               '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
               '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
               f'<pic:nvPicPr><pic:cNvPr id="{doc_id}" name="Picture {doc_id}"/>'
               '<pic:cNvPicPr><a:picLocks noChangeAspect="1"/></pic:cNvPicPr></pic:nvPicPr>'
               f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
               f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
               '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
               '</a:graphicData></a:graphic></wp:inline></w:drawing>')
    return p_style('MDPI52figure', f'<w:r>{drawing}</w:r>')

# ------------------------------------------------------------------- tables
def _tc(cell, width, borders, bold=False, align='center', refs=None):
    tcpr = f'<w:tcW w:w="{width}" w:type="dxa"/>{borders}<w:vAlign w:val="center"/>'
    paras = []
    for ln in (cell if isinstance(cell, list) else [cell]):
        runs = rich_runs(str(ln), refs or {}, b=bold, sz=16) if str(ln) else ''
        paras.append(f'<w:p><w:pPr><w:spacing w:before="14" w:after="14" w:line="240" '
                     f'w:lineRule="auto"/><w:ind w:left="0" w:firstLine="0"/><w:jc w:val="{align}"/>'
                     f'<w:rPr><w:sz w:val="16"/></w:rPr></w:pPr>{runs}</w:p>')
    return f'<w:tc><w:tcPr>{tcpr}</w:tcPr>{"".join(paras)}</w:tc>'

def _borders(top=None, bottom=None):
    b = []
    b.append(f'<w:top w:val="single" w:color="000000" w:sz="{top}" w:space="0"/>' if top
             else '<w:top w:val="nil"/>')
    b.append('<w:left w:val="nil"/>')
    b.append(f'<w:bottom w:val="single" w:color="000000" w:sz="{bottom}" w:space="0"/>' if bottom
             else '<w:bottom w:val="nil"/>')
    b.append('<w:right w:val="nil"/>')
    return '<w:tcBorders>' + ''.join(b) + '</w:tcBorders>'

def smart_table(rows, widths=None, refs=None, total=10460, left_cols=None):
    ncols = len(rows[0])
    if widths is None:
        widths = [total // ncols] * ncols
    def cell_len(c):
        return len(' '.join(map(str, c))) if isinstance(c, list) else len(str(c))
    if left_cols is None:
        left_cols = [ci == 0 or max(cell_len(r[ci]) for r in rows) > 42 for ci in range(ncols)]
    trs = []
    for ri, row in enumerate(rows):
        header = ri == 0
        last = ri == len(rows) - 1
        borders = _borders(top=8 if header else None,
                           bottom=6 if header else (8 if last else None))
        tcs = []
        for ci, cell in enumerate(row):
            align = 'left' if left_cols[ci] else 'center'
            tcs.append(_tc(cell, widths[ci], borders, bold=header, align=align, refs=refs))
        trpr = '<w:trPr>' + ('<w:tblHeader/>' if header else '') + '<w:jc w:val="center"/></w:trPr>'
        trs.append(f'<w:tr>{trpr}{"".join(tcs)}</w:tr>')
    tblpr = ('<w:tblPr><w:tblW w:w="0" w:type="auto"/><w:jc w:val="center"/>'
             '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:top w:w="0" w:type="dxa"/>'
             '<w:left w:w="40" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/>'
             '<w:right w:w="40" w:type="dxa"/></w:tblCellMar></w:tblPr>')
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    return f'<w:tbl>{tblpr}<w:tblGrid>{grid}</w:tblGrid>{"".join(trs)}</w:tbl>'

# ----------------------------------------------------------- APA references
def apa_reference_runs(r):
    """Build APA entry runs: Authors (Year). Title. Journal(i), Vol(issue), pages. DOI"""
    if r.get('raw'):
        return rich_runs(r['full'], {}, sz=18)
    t_end = '' if r['title'].endswith(('?', '!', '…')) else '.'
    runs = [wr(f"{r['authors']} ({r['year']}{r.get('suffix','')}). {r['title']}{t_end} ", sz=18)]
    runs.append(wr(r['journal'], i=True, sz=18))
    tail = ''
    if r.get('volume'):
        runs.append(wr(', ', sz=18))
        runs.append(wr(str(r['volume']), i=True, sz=18))
        if r.get('issue'):
            runs.append(wr(f"({r['issue']})", sz=18))
    if r.get('pages'):
        runs.append(wr(f", {r['pages']}", sz=18))
    runs.append(wr('.', sz=18))
    if r.get('doi'):
        runs.append(wr(f" https://doi.org/{r['doi']}", sz=18))
    return ''.join(runs)

REF_PPR = ('<w:numPr><w:numId w:val="0"/></w:numPr>'
           '<w:ind w:left="2892" w:hanging="284"/><w:spacing w:after="30"/>')

def p_reference(r):
    return p_style('MDPI81references', apa_reference_runs(r), REF_PPR)

def check_intext_collisions(refs, used_keys):
    seen = {}
    for k in used_keys:
        r = refs[k]
        sig = (r['intext'], r['year'])
        if sig in seen and seen[sig] != k:
            raise SystemExit(f'in-text citation collision: {seen[sig]} vs {k} -> {sig}; add suffix a/b')
        seen[sig] = k

# ------------------------------------------------------------------ assembly
DOC_HEAD = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
            'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
            'xmlns:o="urn:schemas-microsoft-com:office:office" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
            'xmlns:v="urn:schemas-microsoft-com:vml" '
            'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
            'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
            'xmlns:w10="urn:schemas-microsoft-com:office:word" '
            'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
            'xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml" '
            'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
            'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
            'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
            'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
            'mc:Ignorable="w14 w15 wp14"><w:body>')

# Template's own sectPr (headers rId11/12/13, footer rId14), bidi removed for
# clean LibreOffice rendering; line numbering preserved.
SECT_PR = ('<w:sectPr><w:headerReference w:type="even" r:id="rId11"/>'
           '<w:headerReference w:type="default" r:id="rId12"/>'
           '<w:headerReference w:type="first" r:id="rId13"/>'
           '<w:footerReference w:type="first" r:id="rId14"/>'
           '<w:type w:val="continuous"/>'
           '<w:pgSz w:w="11906" w:h="16838" w:code="9"/>'
           '<w:pgMar w:top="1417" w:right="720" w:bottom="907" w:left="720" '
           'w:header="720" w:footer="612" w:gutter="0"/>'
           '<w:lnNumType w:countBy="1" w:distance="255" w:restart="continuous"/>'
           '<w:pgNumType w:start="1"/><w:cols w:space="425"/><w:titlePg/>'
           '<w:docGrid w:type="lines" w:linePitch="326"/></w:sectPr>')

def build_docx(template_path, out_path, body_xml, extra_media=None, year='2026', volume='16'):
    doc_xml = DOC_HEAD + body_xml + SECT_PR + '</w:body></w:document>'
    with zipfile.ZipFile(template_path) as zin:
        rels = zin.read('word/_rels/document.xml.rels').decode('utf8')
    new_rels = rels
    if extra_media:
        add = ''
        rid_n = 20
        for zname in extra_media:
            add += (f'<Relationship Id="rId{rid_n}" '
                    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                    f'Target="media/{zname}"/>')
            rid_n += 1
        new_rels = rels.replace('</Relationships>', add + '</Relationships>')
    with zipfile.ZipFile(template_path) as zin, \
         zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == 'word/document.xml':
                data = doc_xml.encode('utf8')
            elif item.filename == 'word/_rels/document.xml.rels':
                data = new_rels.encode('utf8')
            elif item.filename in ('word/header2.xml', 'word/footer1.xml'):
                t = data.decode('utf8')
                t = t.replace('>2025<', f'>{year}<').replace('> 15<', f'> {volume}<')
                data = t.encode('utf8')
            zout.writestr(item, data)
        if extra_media:
            for zname, fpath in extra_media.items():
                zout.write(fpath, f'word/media/{zname}')
    return out_path
