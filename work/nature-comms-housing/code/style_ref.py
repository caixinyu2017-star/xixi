"""Customize the pandoc reference.docx to a clean, journal-like manuscript style."""
import docx
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT="/tmp/claude-0/-home-user-xixi/3e060dbe-78a7-5945-afbd-f1a988fe044a/scratchpad"
d=docx.Document(OUT+"/reference.docx")
BODYFONT="Calibri"; HEADFONT="Calibri"

def setfont(style, name, size, bold=None, italic=None, color=None, spacing_after=None,
            spacing_before=None, line=None, align=None, justify=False):
    f=style.font; f.name=name; f.size=Pt(size)
    if bold is not None: f.bold=bold
    if italic is not None: f.italic=italic
    if color is not None: f.color.rgb=RGBColor(*color)
    # ensure east-asian + ascii font set
    rpr=style.element.get_or_add_rPr(); rfonts=rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts=OxmlElement('w:rFonts'); rpr.append(rfonts)
    for a in ('w:ascii','w:hAnsi','w:cs'): rfonts.set(qn(a), name)
    pf=style.paragraph_format
    if spacing_after is not None: pf.space_after=Pt(spacing_after)
    if spacing_before is not None: pf.space_before=Pt(spacing_before)
    if line is not None:
        pf.line_spacing=line; pf.line_spacing_rule=WD_LINE_SPACING.MULTIPLE
    if align is not None: pf.alignment=align
    if justify: pf.alignment=WD_ALIGN_PARAGRAPH.JUSTIFY

byname={s.name:s for s in d.styles}
def S(name): return byname.get(name)
def apply(name, *a, **k):
    s=S(name)
    if s is None: print("  (skip missing style:",name,")"); return
    setfont(s, *a, **k)
apply('Normal', BODYFONT, 10.5, line=1.45, spacing_after=6, justify=True)
apply('Body Text', BODYFONT, 10.5, line=1.45, spacing_after=6, justify=True)
apply('First Paragraph', BODYFONT, 10.5, line=1.45, spacing_after=6, justify=True)
apply('Title', HEADFONT, 17, bold=True, color=(0x11,0x22,0x44),
        spacing_after=6, line=1.1, align=WD_ALIGN_PARAGRAPH.LEFT)
apply('Heading 1', HEADFONT, 16.5, bold=True, italic=False, color=(0x0f,0x1e,0x3d),
        spacing_before=4, spacing_after=8, line=1.12, align=WD_ALIGN_PARAGRAPH.LEFT)
apply('Heading 2', HEADFONT, 12.5, bold=True, italic=False, color=(0x1b,0x3a,0x5c),
        spacing_before=13, spacing_after=4, line=1.15)
apply('Heading 3', HEADFONT, 11, bold=True, italic=True, color=(0x33,0x33,0x33),
        spacing_before=9, spacing_after=2, line=1.15)
apply('Bibliography', BODYFONT, 9.5, line=1.15, spacing_after=3)

# page margins ~1 inch (letter)
for sec in d.sections:
    sec.top_margin=Inches(1.0); sec.bottom_margin=Inches(1.0)
    sec.left_margin=Inches(1.0); sec.right_margin=Inches(1.0)

d.save(OUT+"/reference.docx")
print("styled reference.docx saved")
