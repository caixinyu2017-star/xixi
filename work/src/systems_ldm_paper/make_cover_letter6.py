# -*- coding: utf-8 -*-
"""Build the paper-5 cover letter from the user's template docx by replacing
paragraph texts while preserving the template's formatting."""
import re, shutil, zipfile, os
import xml.etree.ElementTree as ET

SCRATCH = os.path.dirname(os.path.abspath(__file__))
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
ET.register_namespace('w', W)
for pref, uri in [
    ('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'),
    ('wp', 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'),
    ('m', 'http://schemas.openxmlformats.org/officeDocument/2006/math'),
    ('mc', 'http://schemas.openxmlformats.org/markup-compatibility/2006'),
    ('w14', 'http://schemas.microsoft.com/office/word/2010/wordml'),
    ('wps', 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape'),
    ('wpg', 'http://schemas.microsoft.com/office/word/2010/wordprocessingGroup'),
    ('v', 'urn:schemas-microsoft-com:vml'),
    ('o', 'urn:schemas-microsoft-com:office:office'),
    ('w10', 'urn:schemas-microsoft-com:office:word'),
]:
    ET.register_namespace(pref, uri)

SRC = os.path.join(SCRATCH, 'cover_letter_template.docx')
OUT = os.path.join(SCRATCH, 'Cover_Letter_Digital_Leadership_Decision_Agility_Systems.docx')

TITLE = ("Leadership and Decision Making in Digitally Transforming Enterprises: "
         "Multivariate Modeling and Cluster Typologies of Decision Agility and "
         "Young Managerial Advancement")
SI = "Navigating Digital Transformation: Leadership and Decision Making in Today’s Systems"

# rich paragraph specs: list of (text, style) with style in '', 'b', 'i'
TITLE_PARA = [
 ("We would like to submit the enclosed manuscript entitled ", ''),
 (f"“{TITLE}”", 'b'),
 (", which we wish to be considered for publication in ", ''),
 ("Systems", 'i'),
 (" for the Special Issue ", ''),
 (f"“{SI}.”", 'b'),
]

STUDY_PARA = [
 ("This study investigates how the leadership and decision-making practices of digitally "
  "transforming enterprises relate to organizational decision agility and to the advancement "
  "of young people into management. Drawing on an executive survey of 285 firms in China's "
  "Yangtze River Delta, we measure four practices—digital transformation leadership, the "
  "breadth of AI-assisted managerial decision-making, decision-process digitalization, and "
  "the involvement of young employees in transformation decisions—and relate them to decision "
  "agility and to the share of managerial positions held by employees aged 35 or younger. "
  "Combining MANOVA-type multivariate modeling, exploratory factor analysis, and hierarchical "
  "plus k-means clustering, the study offers a system-level account of how digital "
  "transformation is steered inside enterprises, and by whom.", ''),
]

FIT_PARA = [
 ("We believe that this manuscript fits well within the scope of ", ''),
 ("Systems", 'i'),
 (f" and the Special Issue \u201c{SI}\u201d. The paper addresses the Special Issue's three focal "
  "themes in a single design—the role of leadership in driving digital initiatives, the "
  "strategies and processes of decision making in the digital age, and the impact of digital "
  "transformation on organizational structures and practices—and does so with a systems "
  "methodology that examines direct associations, a latent configuration, and emergent "
  "typologies. The findings offer actionable implications for executives and policymakers "
  "concerned with agile, generationally renewed organizations.", ''),
]

INNOV = [
 [("(1) This study places leadership and decision making—the core of the Special Issue—at "
   "the center of the empirical design.", 'b'),
  (" Rather than treating digital transformation as technology adoption, we model the "
   "decision system of the enterprise: who leads it, how broadly AI assists it, how deeply "
   "the decision process is digitalized, and who participates in it.", '')],

 [("(2) This study documents a complementary asymmetry between technology and participation "
   "in decision systems.", 'b'),
  (" The breadth of AI-assisted decision-making is significantly associated with decision "
   "agility but only marginally with young managerial presence, whereas institutionalized "
   "involvement of young employees shows the reverse pattern; transformation leadership and "
   "digitalized decision processes accompany both outcomes. A single latent "
   "leadership–decision configuration underlies the four practices and is significantly "
   "associated with agility and with managerial rejuvenation.", '')],

 [("(3) This study identifies two socio-technical decision regimes that cut across "
   "sectors.", 'b'),
  (" An agile, digitally led regime with a distinctly younger management corps contrasts "
   "with a conventional hierarchical regime; the regimes barely differ in sectoral "
   "composition, indicating that decision regimes reflect organizational choice rather than "
   "industry environment—an insight directly relevant to leadership audiences navigating "
   "digital transformation.", '')],
]

with zipfile.ZipFile(SRC) as z:
    doc = z.read('word/document.xml').decode('utf-8')

root = ET.fromstring(doc)
body = root.find(f'{{{W}}}body')

import copy

XMLSP = '{http://www.w3.org/XML/1998/namespace}space'

def para_text(p):
    return ''.join(t.text or '' for t in p.iter(f'{{{W}}}t'))

def base_rpr(p):
    """First run's rPr with any bold/italic toggles stripped."""
    for r in p.findall(f'{{{W}}}r'):
        rpr = r.find(f'{{{W}}}rPr')
        if rpr is not None:
            rpr = copy.deepcopy(rpr)
            for tag in ('b', 'bCs', 'i', 'iCs', 'rStyle'):
                for el in rpr.findall(f'{{{W}}}{tag}'):
                    rpr.remove(el)
            return rpr
    return None

def set_para_rich(p, parts):
    base = base_rpr(p)
    for r in p.findall(f'{{{W}}}r'):
        p.remove(r)
    for text, style in parts:
        r = ET.SubElement(p, f'{{{W}}}r')
        if base is not None:
            rpr = copy.deepcopy(base)
        else:
            rpr = ET.Element(f'{{{W}}}rPr')
        r.append(rpr)
        if style == 'b':
            ET.SubElement(rpr, f'{{{W}}}b')
            ET.SubElement(rpr, f'{{{W}}}bCs')
        elif style == 'i':
            ET.SubElement(rpr, f'{{{W}}}i')
            ET.SubElement(rpr, f'{{{W}}}iCs')
        t = ET.SubElement(r, f'{{{W}}}t')
        t.set(XMLSP, 'preserve')
        t.text = text

paras = body.findall(f'{{{W}}}p')
innov_idx = 0
for p in paras:
    txt = para_text(p).strip()
    if not txt:
        continue
    if txt.startswith('We would like to submit the enclosed manuscript entitled'):
        set_para_rich(p, TITLE_PARA)
    elif txt.startswith('This study investigates how industrial'):
        set_para_rich(p, STUDY_PARA)
    elif re.match(r'^\(\d\)\s', txt) or txt.startswith(('(1)', '(2)', '(3)')):
        if innov_idx < 3:
            set_para_rich(p, INNOV[innov_idx])
            innov_idx += 1
    elif txt.startswith('We believe that this manuscript fits well'):
        set_para_rich(p, FIT_PARA)

assert innov_idx == 3, f'innovation paragraphs replaced: {innov_idx}'

new_doc = ET.tostring(root, encoding='unicode')
new_doc = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + new_doc

shutil.copy(SRC, OUT)
import tempfile
with zipfile.ZipFile(SRC) as zin, zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        if item.filename == 'word/document.xml':
            zout.writestr(item, new_doc)
        else:
            zout.writestr(item, zin.read(item.filename))
print('written:', OUT)
