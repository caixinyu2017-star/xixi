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
OUT = os.path.join(SCRATCH, 'Cover_Letter_DTL_Youth_Employment_Systems.docx')

TITLE = ("Digital Transformation Leadership in Enterprise Systems: Multivariate Modeling and "
         "Cluster Typologies of Youth Employment and Retention Dynamics")
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
 ("This study investigates how digital transformation leadership and decision-making practices "
  "relate to the youth-employment profile of enterprises. Drawing on a survey of 308 firms in "
  "Zhejiang Province, China, we measure four practice dimensions—digital transformation "
  "leadership, data-driven decision-making, the breadth of artificial intelligence application, "
  "and digital skills training—and link them to the share of employees aged 16–29 and "
  "the voluntary turnover rate among young employees. Combining MANOVA-type multivariate "
  "modeling, exploratory factor analysis, and hierarchical plus k-means clustering, the study "
  "provides a systemic, organization-level account of how leadership and decision making shape "
  "the position of young people in digitally transforming enterprises.", ''),
]

FIT_PARA = [
 ("We believe that this manuscript fits well within the scope of ", ''),
 ("Systems", 'i'),
 (f" and the Special Issue “{SI}”, as it examines precisely the intersection the Special "
  "Issue highlights: how leadership and decision making drive digital initiatives, and how "
  "digital transformation reshapes organizational structures and practices—here, the structure "
  "of the workforce itself. The findings contribute to a systems-level understanding of digital "
  "transformation and offer practical implications for executives and policymakers seeking "
  "technology-enabled, youth-inclusive organizational development.", ''),
]

INNOV = [
 [("(1) This study shifts the analysis of the digital transformation–youth employment nexus "
   "from countries and industries to the organization, where hiring and retention decisions "
   "are actually made.", 'b'),
  (" It connects the digital leadership and data-driven decision-making literatures with "
   "demand-side youth-employment research, treating the age structure and stability of the "
   "workforce as strategic outcomes of leadership and decision-making practice.", '')],

 [("(2) This study distinguishes technology deployment from the leadership, decision, and "
   "training practices in which it is embedded, and shows that their youth-employment "
   "associations differ.", 'b'),
  (" Digital transformation leadership and data-driven decision-making are associated with "
   "both a younger workforce and lower youth turnover, whereas the breadth of AI application "
   "is associated with retention but not with a higher youth share. A single latent factor of "
   "digital leadership–decision capability underlies the four practices and is significantly "
   "associated with both outcomes.", '')],

 [("(3) This study identifies two socio-technical configurations of enterprises within a "
   "single regional economy.", 'b'),
  (" Digitally led, youth-integrating firms and conventionally managed firms with weaker "
   "youth outcomes cut across sector boundaries, demonstrating that the youth-employment "
   "relevance of digital transformation attaches to organizational capability configurations "
   "rather than to technology diffusion alone.", '')],
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
