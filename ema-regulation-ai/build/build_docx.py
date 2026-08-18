# -*- coding: utf-8 -*-
"""Assemble the manuscript as a Word document in the journal's format.

The published article supplied by the journal is used as the template:
its style table, numbering definitions, page geometry, header and
two-column section properties are reused verbatim, and only the body
content is replaced. Consequently the output reproduces the journal's
layout exactly — a one-column title block followed by a two-column
body, Roman-numbered small-capital section headings, italic lettered
subsection headings, nine-point abstract and index terms, centred
display equations with right-aligned numbers rendered as native Word
(OMML) objects, three-line tables, and a bracket-numbered reference
list.
"""
from __future__ import annotations

import os
import re
import zipfile

import content as C
import refs as R
import tables_spec as TS
import l2omml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
TEMPLATE = os.path.join(HERE, "template.docx")
FIGDIR = os.path.abspath(os.path.join(ROOT, "figures"))
OUT = os.path.join(
    ROOT, "Dual_Pathway_Affective_Process_Tracing_manuscript.docx")

# ---------------------------------------------------------------------------
# Style identifiers taken from the template. The template is the
# author's own copy of the manuscript, which WPS re-saved with renumbered
# style identifiers; the mapping below is to that file, so that the
# author's formatting and title block survive a rebuild.
S_TITLE = "25"       # Title, carries the frame
S_BODY = "45"        # the custom body style ("Text")
S_AFFIL = "74"       # List Paragraph, used for the affiliation line
S_ABSTRACT = "45"    # abstract shares the body style; size set per run
S_REF = "24"         # Normal (Web), used for the reference list
S_TABLE = "27"       # Normal Table
NUM_HEAD = 3         # upper-Roman / upper-letter heading list
NUM_REF = 4          # [1], [2], ... reference list
HEADER_RID = "rId4"  # the running header in the template

XMLNS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/'
         '2006/main" xmlns:r="http://schemas.openxmlformats.org/'
         'officeDocument/2006/relationships" '
         'xmlns:m="http://schemas.openxmlformats.org/officeDocument/'
         '2006/math" xmlns:wp="http://schemas.openxmlformats.org/'
         'drawingml/2006/wordprocessingDrawing" '
         'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/'
         'main" xmlns:pic="http://schemas.openxmlformats.org/drawingml/'
         '2006/picture"')

CIT_ORDER, CIT_NUM = [], {}


def cite(key):
    if key not in CIT_NUM:
        CIT_ORDER.append(key)
        CIT_NUM[key] = len(CIT_ORDER)
    return CIT_NUM[key]


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;"))


_APOS = re.compile(r"(?<=[A-Za-z])'(?=[A-Za-z])")
_MINUS = re.compile(r"(?<![\w–—-])-(?=\d)")


def typo(s):
    s = _APOS.sub("’", s)
    return _MINUS.sub("−", s)


# ---------------------------------------------------------------------------
def run(text, bold=False, italic=False, size=None, sc=False,
        sup=False):
    rpr = []
    if bold:
        rpr.append("<w:b/><w:bCs/>")
    if italic:
        rpr.append("<w:i/><w:iCs/>")
    if sc:
        rpr.append("<w:smallCaps/>")
    if sup:
        rpr.append('<w:vertAlign w:val="superscript"/>')
    if size is not None:
        rpr.append('<w:sz w:val="%d"/><w:szCs w:val="%d"/>'
                   % (int(size * 2), int(size * 2)))
    rpr.append('<w:color w:val="000000"/>')
    return ('<w:r><w:rPr>%s</w:rPr><w:t xml:space="preserve">%s</w:t>'
            '</w:r>' % ("".join(rpr), esc(text)))


TOKEN = re.compile(r"(\[\[[a-zA-Z0-9_,\-]+\]\]|\*\*[^*]+\*\*|"
                   r"__[^_]+__|\$[^$]+\$)")


def rich(text, size=None):
    """Body text with [[cite]] groups, **bold**, __italic__ and $math$."""
    out = []
    for seg in TOKEN.split(typo(text)):
        if not seg:
            continue
        if seg.startswith("[[") and seg.endswith("]]"):
            keys = seg[2:-2].split(",")
            nums = [cite(k.strip()) for k in keys]
            out.append(run("[%s]" % "], [".join(str(n) for n in nums),
                           size=size))
        elif seg.startswith("**"):
            out.append(run(seg[2:-2], bold=True, size=size))
        elif seg.startswith("__"):
            out.append(run(seg[2:-2], italic=True, size=size))
        elif seg.startswith("$"):
            out.append(l2omml.inline(seg[1:-1]))
        else:
            out.append(run(seg, size=size))
    return "".join(out)


# ---------------------------------------------------------------------------
def p_body(text, first_indent=None, jc="both", space=None, size=None):
    pr = ['<w:pStyle w:val="%s"/>' % S_BODY]
    if space:
        pr.append('<w:spacing w:before="%d" w:after="%d"/>' % space)
    if first_indent is not None:
        pr.append('<w:ind w:firstLine="%d"/>' % first_indent)
    pr.append('<w:jc w:val="%s"/>' % jc)
    return "<w:p><w:pPr>%s</w:pPr>%s</w:p>" % ("".join(pr),
                                               rich(text, size=size))


def p_h1(text):
    pr = ('<w:pStyle w:val="%s"/><w:keepNext/><w:numPr><w:ilvl w:val="0"/>'
          '<w:numId w:val="%d"/></w:numPr>'
          '<w:spacing w:before="240" w:after="80"/>'
          '<w:jc w:val="center"/><w:outlineLvl w:val="0"/>'
          % (S_BODY, NUM_HEAD))
    return ("<w:p><w:pPr>%s</w:pPr>%s</w:p>"
            % (pr, run(text, sc=True)))


def p_h2(text):
    pr = ('<w:pStyle w:val="%s"/><w:keepNext/><w:numPr><w:ilvl w:val="1"/>'
          '<w:numId w:val="%d"/></w:numPr>'
          '<w:spacing w:before="120" w:after="60"/>'
          '<w:jc w:val="both"/><w:outlineLvl w:val="1"/>'
          % (S_BODY, NUM_HEAD))
    return ("<w:p><w:pPr>%s</w:pPr>%s</w:p>"
            % (pr, run(text, italic=True)))


def p_refs_head():
    pr = ('<w:pStyle w:val="%s"/><w:keepNext/>'
          '<w:spacing w:before="240" w:after="80"/>'
          '<w:jc w:val="center"/>' % S_BODY)
    return "<w:p><w:pPr>%s</w:pPr>%s</w:p>" % (pr, run("References",
                                                       sc=True))


def p_equation(latex, number):
    """A centred display equation with the number right-aligned."""
    body = l2omml.math_body(latex)
    tail = ('<m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t xml:space='
            '"preserve">  </m:t></m:r>'
            '<m:r><m:rPr><m:sty m:val="p"/><m:nor m:val="on"/></m:rPr>'
            '<m:t>(%d)</m:t></m:r>' % number)
    return ('<w:p><w:pPr><w:pStyle w:val="%s"/><w:jc w:val="center"/>'
            '</w:pPr><m:oMathPara><m:oMathParaPr><m:jc m:val="right"/>'
            '</m:oMathParaPr><m:oMath>%s%s</m:oMath></m:oMathPara></w:p>'
            % (S_BODY, body, tail))


def p_caption(text, bold=False, space=(120, 40)):
    pr = ('<w:pStyle w:val="%s"/><w:spacing w:before="%d" w:after="%d"/>'
          '<w:jc w:val="center"/>' % (S_BODY, space[0], space[1]))
    inner = (run(text, bold=True) if bold else rich(text))
    return "<w:p><w:pPr>%s</w:pPr>%s</w:p>" % (pr, inner)


# ---------------------------------------------------------------------------
def table(spec):
    """A three-line table in the template's table style."""
    ncol = len(spec["header"])
    # the label column takes the larger share and the value columns the
    # rest, in the proportion the journal's own tables use; a table may
    # override the split when one of its columns carries running text
    frac = spec.get("widths")
    if frac is None:
        lead = 0.5 if ncol <= 3 else 0.40
        frac = [lead] + [(1.0 - lead) / (ncol - 1)] * (ncol - 1)
    widths = [int(round(5000 * x)) for x in frac]
    widths[0] += 5000 - sum(widths)
    grid = "".join('<w:gridCol w:w="%d"/>' % int(9720 * x / 5000)
                   for x in widths)
    tblPr = (
        '<w:tblPr><w:tblStyle w:val="%s"/>'
        '<w:tblW w:w="5000" w:type="pct"/><w:jc w:val="center"/>'
        '<w:tblBorders>'
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:left w:val="nil"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        '<w:right w:val="nil"/><w:insideH w:val="nil"/>'
        '<w:insideV w:val="nil"/></w:tblBorders>'
        '<w:tblCellMar><w:top w:w="20" w:type="dxa"/>'
        '<w:left w:w="60" w:type="dxa"/>'
        '<w:bottom w:w="20" w:type="dxa"/>'
        '<w:right w:w="60" w:type="dxa"/></w:tblCellMar>'
        '</w:tblPr>' % S_TABLE)

    def cell(text, bold, align, colw, last_header=False,
             first_row=False, bottom=False):
        borders = ["<w:left w:val=\"nil\"/><w:right w:val=\"nil\"/>"]
        if first_row:
            borders.append('<w:top w:val="single" w:sz="12" w:space="0" '
                           'w:color="000000"/>')
        if last_header:
            borders.append('<w:bottom w:val="single" w:sz="6" '
                           'w:space="0" w:color="000000"/>')
        if bottom:
            borders.append('<w:bottom w:val="single" w:sz="12" '
                           'w:space="0" w:color="000000"/>')
        tcpr = ('<w:tcPr><w:tcW w:w="%d" w:type="pct"/><w:tcBorders>%s'
                '</w:tcBorders><w:shd w:val="clear" w:color="auto" '
                'w:fill="ffffff"/><w:vAlign w:val="center"/></w:tcPr>'
                % (colw, "".join(borders)))
        ppr = ('<w:pPr><w:pStyle w:val="%s"/>'
               '<w:spacing w:before="20" w:after="20"/>'
               '<w:jc w:val="%s"/></w:pPr>' % (S_BODY, align))
        # an explicit newline in a header lets the break fall at a
        # readable point instead of wherever the column happens to end
        parts = text.split("\n")
        body = "<w:r><w:br/></w:r>".join(
            (run(t, bold=True, size=9) if bold else rich(t, size=9))
            for t in parts)
        return "<w:tc>%s<w:p>%s%s</w:p></w:tc>" % (tcpr, ppr, body)

    rows = []
    align = spec.get("align", ["left"] + ["center"] * (ncol - 1))
    hdr = "".join(cell(h, True, align[j], widths[j], last_header=True,
                       first_row=True)
                  for j, h in enumerate(spec["header"]))
    rows.append('<w:tr><w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>%s'
                '</w:tr>' % hdr)
    for i, r in enumerate(spec["rows"]):
        last = (i == len(spec["rows"]) - 1)
        cells = "".join(cell(v, False, align[j], widths[j], bottom=last)
                        for j, v in enumerate(r))
        rows.append("<w:tr><w:trPr><w:cantSplit/></w:trPr>%s</w:tr>"
                    % cells)
    return "<w:tbl>%s<w:tblGrid>%s</w:tblGrid>%s</w:tbl>" % (
        tblPr, grid, "".join(rows))


# ---------------------------------------------------------------------------
IMAGES = []


def figure(fname, width_cm):
    """An inline picture, centred, sized to the column width."""
    path = os.path.join(FIGDIR, fname)
    from PIL import Image
    with Image.open(path) as im:
        wpx, hpx = im.size
    cx = int(width_cm * 360000)
    cy = int(cx * hpx / wpx)
    rid = "rIdImg%d" % (len(IMAGES) + 1)
    IMAGES.append((rid, path))
    return (
        '<w:p><w:pPr><w:pStyle w:val="%s"/>'
        '<w:spacing w:before="120" w:after="40"/>'
        '<w:jc w:val="center"/><w:keepNext/></w:pPr>'
        '<w:r><w:rPr/><w:drawing><wp:inline distT="0" distB="0" '
        'distL="0" distR="0"><wp:extent cx="%d" cy="%d"/>'
        '<wp:docPr id="%d" name="Picture %d"/>'
        '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.'
        'org/drawingml/2006/picture"><pic:pic>'
        '<pic:nvPicPr><pic:cNvPr id="%d" name="%s"/><pic:cNvPicPr/>'
        '</pic:nvPicPr>'
        '<pic:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/>'
        '</a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/>'
        '<a:ext cx="%d" cy="%d"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing>'
        '</w:r></w:p>'
        % (S_BODY, cx, cy, len(IMAGES), len(IMAGES), len(IMAGES),
           fname, rid, cx, cy))


# ---------------------------------------------------------------------------
def front_matter():
    out = []
    out.append('<w:p><w:pPr><w:pStyle w:val="%s"/><w:framePr w:w="0" '
               'w:hSpace="0" w:vSpace="0" w:wrap="auto" '
               'w:hAnchor="text" w:vAnchor="margin" w:xAlign="left" '
               'w:yAlign="inline"/></w:pPr>%s</w:p>'
               % (S_TITLE, run(C.TITLE)))
    # authors, with superscript affiliation markers
    aruns = []
    for text, sup in C.AUTHORS:
        aruns.append(run(text, sup=sup))
    out.append('<w:p><w:pPr><w:pStyle w:val="%s"/><w:jc w:val="center"/>'
               '</w:pPr>%s</w:p>' % (S_BODY, "".join(aruns)))
    # A single-affiliation title block needs no numbered list, and the
    # template no longer defines one; the parentheses are literal, as in
    # the author's own copy.
    for aff in C.AFFILIATIONS:
        out.append('<w:p><w:pPr><w:pStyle w:val="%s"/>'
                   '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="0"/>'
                   '</w:numPr><w:ind w:left="420" w:leftChars="0" '
                   'w:hanging="420" w:firstLineChars="0"/>'
                   '<w:jc w:val="center"/></w:pPr>%s</w:p>'
                   % (S_AFFIL, run("( " + aff + ")")))
    # the empty paragraph that carries the one-column section break
    out.append('<w:p><w:pPr><w:pStyle w:val="%s"/>'
               '<w:spacing w:before="20" w:after="320"/>'
               '<w:ind w:firstLine="202"/><w:jc w:val="both"/>'
               '<w:sectPr><w:headerReference w:type="default" '
               'r:id="%s"/><w:type w:val="continuous"/>'
               '<w:pgSz w:w="12240" w:h="15840" w:orient="portrait"/>'
               '<w:pgMar w:top="1008" w:right="936" w:bottom="1008" '
               'w:left="936" w:header="432" w:footer="432" '
               'w:gutter="0"/><w:pgNumType w:start="1"/>'
               '<w:cols w:space="288" w:num="1"></w:cols></w:sectPr>'
               '</w:pPr></w:p>' % (S_BODY, HEADER_RID))
    # abstract and index terms, nine point
    out.append('<w:p><w:pPr><w:pStyle w:val="%s"/>'
               '<w:ind w:firstLine="0"/></w:pPr>%s%s</w:p>'
               % (S_ABSTRACT, run("Abstract", bold=True, size=9),
                  rich("—" + C.ABSTRACT, size=9)))
    out.append('<w:p><w:pPr><w:pStyle w:val="%s"/><w:jc w:val="both"/>'
               '</w:pPr>%s%s</w:p>'
               % (S_BODY, run("Index Terms", bold=True, size=9),
                  run("—" + C.INDEX_TERMS, size=9)))
    return "".join(out)


def body():
    out = []
    for block in C.BLOCKS:
        kind = block[0]
        if kind == "h1":
            out.append(p_h1(block[1]))
        elif kind == "h2":
            out.append(p_h2(block[1]))
        elif kind == "p":
            out.append(p_body(block[1]))
        elif kind == "item":
            out.append(p_body("**%s**%s" % (block[1], block[2]),
                              first_indent=402))
        elif kind == "eq":
            out.append(p_equation(block[1], block[2]))
        elif kind == "where":
            out.append(p_body(block[1], first_indent=0))
        elif kind == "table":
            spec = TS.TABLES[block[1]]()
            out.append(p_caption("Table %s. %s"
                                 % (spec["number"], spec["caption"]),
                                 bold=True))
            out.append(table(spec))
        elif kind == "fig":
            spec = TS.FIGURES[block[1]]
            out.append(figure(spec["file"], spec["width_cm"]))
            out.append(p_caption("Figure %d. %s"
                                 % (spec["number"], spec["caption"]),
                                 space=(40, 160)))
    return "".join(out)


def references():
    out = [p_refs_head()]
    for key in CIT_ORDER:
        before, ital, after = R.REFS[key]
        pr = ('<w:pStyle w:val="%s"/><w:numPr><w:ilvl w:val="0"/>'
              '<w:numId w:val="%d"/></w:numPr>'
              '<w:spacing w:before="0" w:after="0"/>'
              '<w:jc w:val="both"/>' % (S_REF, NUM_REF))
        runs = (run(before, size=10) + run(ital, italic=True, size=10)
                + run(after, size=10))
        out.append("<w:p><w:pPr>%s</w:pPr>%s</w:p>" % (pr, runs))
    return "".join(out)


FINAL_SECT = ('<w:sectPr><w:footnotePr><w:numRestart w:val="eachSect"/>'
              '</w:footnotePr><w:type w:val="continuous"/>'
              '<w:pgSz w:w="12240" w:h="15840" w:orient="portrait"/>'
              '<w:pgMar w:top="1008" w:right="936" w:bottom="1008" '
              'w:left="936" w:header="432" w:footer="432" '
              'w:gutter="0"/><w:pgNumType w:start="1"/>'
              '<w:cols w:equalWidth="0" w:num="2">'
              '<w:col w:w="5040" w:space="288"/><w:col w:w="5040"/>'
              '</w:cols></w:sectPr>')


# ---------------------------------------------------------------------------
def build():
    fm = front_matter()
    bd = body()                      # fills CIT_ORDER
    rf = references()
    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           '<w:document %s><w:body>%s%s%s%s</w:body></w:document>'
           % (XMLNS, fm, bd, rf, FINAL_SECT))

    with zipfile.ZipFile(TEMPLATE) as zin:
        items = {i.filename: zin.read(i.filename)
                 for i in zin.infolist()}

    # register the figure images
    rels = items["word/_rels/document.xml.rels"].decode("utf-8")
    add = []
    for rid, path in IMAGES:
        name = "media/" + os.path.basename(path)
        items["word/" + name] = open(path, "rb").read()
        add.append('<Relationship Id="%s" Type="http://schemas.'
                   'openxmlformats.org/officeDocument/2006/relationships/'
                   'image" Target="%s"/>' % (rid, name))
    rels = rels.replace("</Relationships>", "".join(add)
                        + "</Relationships>")
    items["word/_rels/document.xml.rels"] = rels.encode("utf-8")

    ct = items["[Content_Types].xml"].decode("utf-8")
    if 'Extension="png"' not in ct:
        ct = ct.replace("<Types ", "<Types ", 1)
        ct = ct.replace("</Types>",
                        '<Default Extension="png" '
                        'ContentType="image/png"/></Types>')
    items["[Content_Types].xml"] = ct.encode("utf-8")

    items["word/document.xml"] = doc.encode("utf-8")
    # drop the old media, which the new body no longer references
    for k in [k for k in items if k.startswith("word/media/image")]:
        del items[k]

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in items.items():
            zout.writestr(name, data)

    missing = [k for k in CIT_ORDER if k not in R.REFS]
    unused = sorted(set(R.REFS) - set(CIT_ORDER))
    print("saved:", OUT)
    print("references cited: %d / %d" % (len(CIT_ORDER), len(R.REFS)))
    if unused:
        print("UNCITED:", ", ".join(unused))
    if missing:
        print("MISSING:", missing)


if __name__ == "__main__":
    build()
