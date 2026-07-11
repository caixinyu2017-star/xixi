# -*- coding: utf-8 -*-
"""MDPI Systems docx builder.

Rebuilds word/document.xml of the sample MDPI-template docx with new content,
preserving styles, headers/footers, line numbering (sectPr) from the sample.

Formatting patterns are cloned from the user's own sample paper
(sample_ai_youth.docx), which was built on the official MDPI Systems template:
  - body font Palatino Linotype, sz 20 (10pt), justified, Normal style ind left=2608
  - display equations: tabs center@4600 / right@9200, OMML centered, "(n)" right
  - three-line tables, references with hanging indent, etc.
"""
import re, shutil, zipfile, os
from xml.sax.saxutils import escape

SCRATCH = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- OMML helpers
# words that LibreOffice's OMML->StarMath importer treats as operators/keywords
# and garbles into symbols (e.g. "Size" -> font-size command, "INT" -> integral);
# Word renders them fine, but splitting into two runs is safe everywhere.
_LO_MATH_KEYWORDS = {'size', 'int', 'sum', 'mod', 'ln', 'log', 'exp', 'abs',
                     'min', 'max', 'lim', 'sin', 'cos', 'tan', 'func', 'fact'}

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
    """OMML run. By default math-italic (Word style); upright for =, numbers."""
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

def msum(sub, sup, body):
    """n-ary sum with sub/sup limits; empty limits are hidden (an empty
    m:sub/m:sup slot renders as a dashed placeholder box in Word)."""
    pr = ['<m:chr m:val="∑"/>', '<m:limLoc m:val="subSup"/>']
    if not sub:
        pr.append('<m:subHide m:val="1"/>')
    if not sup:
        pr.append('<m:supHide m:val="1"/>')
    return ('<m:nary><m:naryPr>' + ''.join(pr) + '</m:naryPr>'
            f'<m:sub>{sub}</m:sub><m:sup>{sup}</m:sup><m:e>{body}</m:e></m:nary>')

def mdelim(body, left='(', right=')'):
    return (f'<m:d><m:dPr><m:begChr m:val="{left}"/><m:endChr m:val="{right}"/></m:dPr>'
            f'<m:e>{body}</m:e></m:d>')

def omath(inner):
    return f'<m:oMath>{inner}</m:oMath>'

_GREEK = {'alpha':'α','beta':'β','gamma':'γ','delta':'δ','epsilon':'ε',
          'lambda':'λ','mu':'μ','theta':'θ','phi':'φ','eta':'η',
          'kappa':'κ','omega':'ω','vartheta':'ϑ','times':'×','prime':'′'}

def inline_math(spec):
    """Parse a simple inline-math spec into OMML: NAME, NAME_{sub}, NAME^{sup},
    greek names get mapped; '×' upright. Variable codes containing a bare
    underscore (e.g. EDL_SPEC) are emitted as italic text runs — they are
    labels, not formulas, and a literal '_' inside m:t breaks LibreOffice's
    OMML import."""
    spec = spec.strip()
    for k, v in _GREEK.items():
        spec = spec.replace('\\' + k, v)
    if '_' in spec and '_{' not in spec:
        return wrun(spec, sz=20, i=True)
    m = re.fullmatch(r'([^_^]+?)_\{([^}]*)\}', spec)
    if m:
        return omath(msub(mr(m.group(1)), mr(m.group(2))))
    m = re.fullmatch(r'([^_^]+?)\^\{([^}]*)\}', spec)
    if m:
        return omath(msup(mr(m.group(1)), mr(m.group(2))))
    m = re.fullmatch(r'([^_^]+?)_\{([^}]*)\}\^\{([^}]*)\}', spec)
    if m:
        return omath(f'<m:sSubSup><m:sSubSupPr/><m:e>{mr(m.group(1))}</m:e>'
                     f'<m:sub>{mr(m.group(2))}</m:sub><m:sup>{mr(m.group(3))}</m:sup></m:sSubSup>')
    return omath(mr(spec))

# ---------------------------------------------------------- paragraph helpers
PALATINO = ('<w:rFonts w:ascii="Palatino Linotype" w:hAnsi="Palatino Linotype" '
            'w:eastAsia="Palatino Linotype"/>')

def wrun(text, sz=20, b=False, i=False, sup=False):
    rpr = [PALATINO]
    rpr.append('<w:b/>' if b else '<w:b w:val="0"/>')
    rpr.append('<w:i/>' if i else '<w:i w:val="0"/>')
    rpr.append(f'<w:sz w:val="{sz}"/>')
    if sup:
        rpr.append('<w:vertAlign w:val="superscript"/>')
    sp = ' xml:space="preserve"' if text != text.strip() else ''
    return f'<w:r><w:rPr>{"".join(rpr)}</w:rPr><w:t{sp}>{escape(text)}</w:t></w:r>'

CITE_RE = re.compile(r'\{\{([a-z0-9_|]+)\}\}')
IMATH_RE = re.compile(r'⟪(.+?)⟫')  # ⟪...⟫

def _fmt_citation(keys, refmap):
    nums = sorted({refmap[k] for k in keys})
    parts, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        parts.append(str(nums[i]) if j == i else (f'{nums[i]},{nums[j]}' if j == i + 1
                     else f'{nums[i]}–{nums[j]}'))
        i = j + 1
    return '[' + ','.join(parts) + ']'

def rich_runs(text, refmap, sz=20, b=False, i=False):
    """Convert text with {{cite|keys}} and ⟪math⟫ into a run sequence."""
    text = CITE_RE.sub(lambda m: _fmt_citation(m.group(1).split('|'), refmap), text)
    out, pos = [], 0
    for m in IMATH_RE.finditer(text):
        if m.start() > pos:
            out.append(wrun(text[pos:m.start()], sz=sz, b=b, i=i))
        out.append(inline_math(m.group(1)))
        pos = m.end()
    if pos < len(text):
        out.append(wrun(text[pos:], sz=sz, b=b, i=i))
    return ''.join(out)

def para(inner, ppr=''):
    return f'<w:p><w:pPr>{ppr}</w:pPr>{inner}</w:p>'

# block builders -----------------------------------------------------------
def p_title(text):
    return para(wrun(text, sz=36, b=True),
                '<w:spacing w:after="120"/><w:ind w:left="0" w:leftChars="0" '
                'w:firstLine="0" w:firstLineChars="0"/>')

def p_style(style_id, runs_xml, extra_ppr=''):
    return f'<w:p><w:pPr><w:pStyle w:val="{style_id}"/>{extra_ppr}</w:pPr>{runs_xml}</w:p>'

def p_h1(text):
    return para(wrun(text, sz=24, b=True), '<w:keepNext/><w:spacing w:before="200" w:after="80"/>')

def p_h2(text):
    return para(wrun(text, sz=20, b=True), '<w:keepNext/><w:spacing w:before="140" w:after="80"/>')

def p_h3(text):
    return para(wrun(text, sz=20, b=True, i=True), '<w:keepNext/><w:spacing w:before="140" w:after="80"/>')

def p_body(text, refmap):
    return para(rich_runs(text, refmap), '<w:spacing w:after="120"/><w:jc w:val="both"/>')

def p_hyp(label, text, refmap):
    inner = (wrun(label + ' ', sz=20, b=True) + rich_runs(text, refmap, i=True))
    return para(inner, '<w:spacing w:before="60" w:after="60"/><w:ind w:left="2948"/><w:jc w:val="both"/>')

def p_equation(omml_xml, number):
    ppr = ('<w:tabs><w:tab w:val="center" w:pos="4600"/><w:tab w:val="right" w:pos="9200"/></w:tabs>'
           '<w:spacing w:before="80" w:after="80"/><w:ind w:left="0"/><w:jc w:val="right"/>')
    inner = (f'<w:r><w:rPr>{PALATINO}<w:b w:val="0"/><w:i w:val="0"/><w:sz w:val="20"/></w:rPr><w:tab/></w:r>'
             + omml_xml +
             f'<w:r><w:rPr>{PALATINO}<w:b w:val="0"/><w:i w:val="0"/><w:sz w:val="20"/></w:rPr><w:tab/></w:r>'
             + wrun(f'({number})', sz=20))
    return para(inner, ppr)

def p_table_caption(num, text):
    inner = wrun(f'Table {num}. ', sz=17, b=True) + wrun(text, sz=17)
    return para(inner, '<w:keepNext/><w:spacing w:before="160" w:after="40"/>')

def p_fig_caption(num, text):
    inner = wrun(f'Figure {num}. ', sz=17, b=True) + wrun(text, sz=17)
    return para(inner, '<w:spacing w:after="160"/><w:jc w:val="center"/>')

def p_notes(text, refmap):
    inner = wrun('Notes: ', sz=14, i=True) + rich_runs(text, refmap, sz=14)
    return para(inner, '<w:spacing w:before="40" w:after="160"/><w:jc w:val="both"/>')

def p_backmatter(label, text):
    inner = (f'<w:r><w:rPr>{PALATINO}<w:b/><w:i/><w:sz w:val="17"/></w:rPr>'
             f'<w:t>{escape(label)}</w:t></w:r>'
             + wrun(' ' + text, sz=17))
    return para(inner, '<w:spacing w:before="40" w:after="60"/><w:jc w:val="both"/>')

def p_reference(num, authors, title, journal, year, tail):
    """MDPI reference: authors+title regular, journal italic, year bold, vol italic, pages regular."""
    runs = [wrun(f'{num}. {authors} {title}. ', sz=16),
            wrun(journal + ' ', sz=16, i=True),
            wrun(f'{year}', sz=16, b=True)]
    if tail:
        vol, _, pages = tail.partition('|')
        if vol:
            runs.append(wrun(', ', sz=16))
            runs.append(wrun(vol, sz=16, i=True))
        if pages:
            runs.append(wrun(', ' + pages, sz=16))
    runs.append(wrun('.', sz=16))
    return para(''.join(runs),
                '<w:spacing w:after="20"/><w:ind w:left="2920" w:hanging="312"/><w:jc w:val="both"/>')

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
    return para(f'<w:r>{drawing}</w:r>', '<w:spacing w:after="40"/><w:jc w:val="center"/>')

# ------------------------------------------------------------------- tables
def _tc(text_lines, width, borders, bold=False, align='center', sz=16):
    tcpr = f'<w:tcW w:w="{width}" w:type="dxa"/>{borders}'
    paras = []
    for ln in (text_lines if isinstance(text_lines, list) else [text_lines]):
        runs = wrun(str(ln), sz=sz, b=bold) if str(ln) else ''
        paras.append(f'<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="240" '
                     f'w:lineRule="auto"/><w:ind w:left="0"/><w:jc w:val="{align}"/>'
                     f'<w:rPr><w:sz w:val="19"/></w:rPr></w:pPr>{runs}</w:p>')
    return f'<w:tc><w:tcPr>{tcpr}</w:tcPr>{"".join(paras)}</w:tc>'

def _borders(top=None, bottom=None):
    b = []
    if top:
        b.append(f'<w:top w:val="single" w:color="000000" w:sz="{top}" w:space="0"/>')
    else:
        b.append('<w:top w:val="nil"/>')
    b.append('<w:left w:val="nil"/>')
    if bottom:
        b.append(f'<w:bottom w:val="single" w:color="000000" w:sz="{bottom}" w:space="0"/>')
    else:
        b.append('<w:bottom w:val="nil"/>')
    b.append('<w:right w:val="nil"/>')
    return '<w:tcBorders>' + ''.join(b) + '</w:tcBorders>'

def three_line_table(rows, col_widths=None, total_width=9640):
    """rows: list of row-lists; row cell = str or list-of-str (multi-line).
    First row = header (bold, top sz8 + bottom sz6); last row bottom sz8."""
    ncols = len(rows[0])
    if col_widths is None:
        col_widths = [total_width // ncols] * ncols
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in col_widths)
    trs = []
    for ri, row in enumerate(rows):
        header = ri == 0
        last = ri == len(rows) - 1
        borders = _borders(top=8 if header else None,
                           bottom=6 if header else (8 if last else None))
        tcs = []
        for ci, cell in enumerate(row):
            align = 'left' if ci == 0 else 'center'
            tcs.append(_tc(cell, col_widths[ci], borders, bold=header, align=align))
        trpr = '<w:trPr>' + ('<w:tblHeader/>' if header else '') + '<w:jc w:val="center"/></w:trPr>'
        trs.append(f'<w:tr>{trpr}{"".join(tcs)}</w:tr>')
    tblpr = ('<w:tblPr><w:tblW w:w="0" w:type="auto"/><w:jc w:val="center"/>'
             '<w:tblLayout w:type="fixed"/><w:tblCellMar><w:top w:w="0" w:type="dxa"/>'
             '<w:left w:w="40" w:type="dxa"/><w:bottom w:w="0" w:type="dxa"/>'
             '<w:right w:w="40" w:type="dxa"/></w:tblCellMar></w:tblPr>')
    return f'<w:tbl>{tblpr}<w:tblGrid>{grid}</w:tblGrid>{"".join(trs)}</w:tbl>'

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

SECT_PR = ('<w:sectPr><w:headerReference r:id="rId7" w:type="first"/>'
           '<w:footerReference r:id="rId9" w:type="first"/>'
           '<w:headerReference r:id="rId5" w:type="default"/>'
           '<w:footerReference r:id="rId8" w:type="default"/>'
           '<w:headerReference r:id="rId6" w:type="even"/>'
           '<w:pgSz w:w="11906" w:h="16838"/>'
           '<w:pgMar w:top="1417" w:right="720" w:bottom="907" w:left="720" '
           'w:header="720" w:footer="612" w:gutter="0"/>'
           '<w:lnNumType w:countBy="1" w:distance="255" w:restart="continuous"/>'
           '<w:pgNumType w:start="1"/><w:cols w:space="425" w:num="1"/>'
           '<w:titlePg/><w:docGrid w:linePitch="360" w:charSpace="0"/></w:sectPr>')

def build_docx(sample_path, out_path, body_xml, extra_media=None):
    """Repackage sample docx with new document.xml; extra_media: {zipname: filepath};
    also appends image relationships rId20/rId21 if extra_media given."""
    shutil.copy(sample_path, out_path)
    doc_xml = DOC_HEAD + body_xml + SECT_PR + '</w:body></w:document>'

    import tempfile
    tmpd = tempfile.mkdtemp(dir=SCRATCH)
    with zipfile.ZipFile(sample_path) as zin:
        names = zin.namelist()
        rels = zin.read('word/_rels/document.xml.rels').decode('utf8')

    new_rels = rels
    if extra_media:
        add = ''
        rid_map = {}
        rid_n = 20
        for zname in extra_media:
            rid = f'rId{rid_n}'
            rid_map[zname] = rid
            add += (f'<Relationship Id="{rid}" '
                    'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
                    f'Target="media/{zname}"/>')
            rid_n += 1
        new_rels = rels.replace('</Relationships>', add + '</Relationships>')

    with zipfile.ZipFile(sample_path) as zin, zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename == 'word/document.xml':
                zout.writestr(item, doc_xml)
            elif item.filename == 'word/_rels/document.xml.rels':
                zout.writestr(item, new_rels)
            else:
                zout.writestr(item, zin.read(item.filename))
        if extra_media:
            for zname, fpath in extra_media.items():
                zout.write(fpath, f'word/media/{zname}')
    return out_path
