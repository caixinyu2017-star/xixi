#!/usr/bin/env python3
"""Build a Nature-Communications-style reference.docx for pandoc, incl. custom
paragraph styles addressable from markdown via ::: {custom-style="..."} divs."""
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn

doc = Document("/tmp/ref_default.docx")
styles = doc.styles
BODY="Times New Roman"; HEAD="Arial"

def _rfonts(style,name):
    rpr=style.element.get_or_add_rPr()
    rf=rpr.find(qn('w:rFonts'))
    if rf is None:
        rf=rpr.makeelement(qn('w:rFonts'),{}); rpr.append(rf)
    for a in ('w:ascii','w:hAnsi','w:cs'): rf.set(qn(a),name)

def style_set(style,name=None,size=None,bold=None,italic=None,color=None,
              align=None,spacing=None,before=None,after=None,keep=None,indent=None):
    f=style.font
    if name: f.name=name; _rfonts(style,name)
    if size is not None: f.size=Pt(size)
    if bold is not None: f.bold=bold
    if italic is not None: f.italic=italic
    if color is not None: f.color.rgb=RGBColor(*color)
    pf=style.paragraph_format
    if align is not None: pf.alignment=align
    if spacing is not None: pf.line_spacing=spacing; pf.line_spacing_rule=WD_LINE_SPACING.MULTIPLE
    if before is not None: pf.space_before=Pt(before)
    if after is not None: pf.space_after=Pt(after)
    if keep is not None: pf.keep_with_next=keep
    if indent is not None: pf.first_line_indent=Pt(indent)

def ensure(name):
    try: return styles[name]
    except KeyError: return styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)

# ---- built-in styles ----
style_set(styles['Normal'], name=BODY, size=11.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
          spacing=1.5, after=6, before=0)
for h,sz,it in [('Heading 1',13.5,False),('Heading 2',11.8,False),('Heading 3',11.5,True)]:
    try: style_set(styles[h],name=HEAD,size=sz,bold=True,italic=it,color=(0x1a,0x1a,0x1a),
                   align=WD_ALIGN_PARAGRAPH.LEFT,spacing=1.2,
                   before=(15 if h=='Heading 1' else 10),after=4,keep=True)
    except KeyError: pass
# figure image paragraph + caption (pandoc uses these names)
for cs in ['Figure','Captioned Figure','Image Caption','Caption']:
    try:
        if cs in ('Image Caption','Caption'):
            style_set(styles[cs],name=BODY,size=9.5,italic=False,color=(0x33,0x33,0x33),
                      align=WD_ALIGN_PARAGRAPH.JUSTIFY,spacing=1.15,before=3,after=12)
        else:
            style_set(styles[cs],align=WD_ALIGN_PARAGRAPH.CENTER,before=8,after=2)
    except KeyError: pass

# ---- custom styles addressable from markdown ----
style_set(ensure('PaperTitle'),name=HEAD,size=19,bold=True,color=(0x0f,0x0f,0x0f),
          align=WD_ALIGN_PARAGRAPH.LEFT,spacing=1.08,before=4,after=10)
style_set(ensure('Authors'),name=HEAD,size=12,bold=False,color=(0x1a,0x1a,0x1a),
          align=WD_ALIGN_PARAGRAPH.LEFT,spacing=1.15,after=3)
style_set(ensure('Affiliation'),name=BODY,size=9.5,italic=True,color=(0x44,0x44,0x44),
          align=WD_ALIGN_PARAGRAPH.LEFT,spacing=1.1,after=1)
style_set(ensure('Corresp'),name=BODY,size=9.5,italic=False,color=(0x44,0x44,0x44),
          align=WD_ALIGN_PARAGRAPH.LEFT,spacing=1.1,after=10)
style_set(ensure('AbstractBody'),name=BODY,size=11.5,bold=False,color=(0x11,0x11,0x11),
          align=WD_ALIGN_PARAGRAPH.JUSTIFY,spacing=1.4,before=2,after=12)
style_set(ensure('MetaBlock'),name=BODY,size=9.5,color=(0x33,0x33,0x33),
          align=WD_ALIGN_PARAGRAPH.JUSTIFY,spacing=1.2,after=5)
style_set(ensure('RefList'),name=BODY,size=9.5,color=(0x11,0x11,0x11),
          align=WD_ALIGN_PARAGRAPH.LEFT,spacing=1.15,after=2)

doc.save("/tmp/claude-0/-home-user-xixi/6d43c964-2cf2-5046-b36a-f5cde2a6d8f9/scratchpad/papers/reference.docx")
print("reference.docx built with custom styles")
