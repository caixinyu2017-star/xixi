# -*- coding: utf-8 -*-
"""Build the cover letter from the author's own template, preserving formatting."""
import copy
import os
import re
import shutil
import xml.etree.ElementTree as ET
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
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

SRC = os.path.join(HERE, 'cover_letter_template.docx')
OUT = os.path.join(HERE, '..',
                   'Cover_Letter_Youth_School_to_Work_Transition_System_Zhejiang.docx')

TITLE = ("A Moving Target, Not a Tipping Point: Attractor Drift, Queue Congestion and "
         "Policy Sequencing in the Youth School-to-Work Transition System of Zhejiang, "
         "China")
SI = "Systems Thinking for Real-World Problem Solving"

TITLE_PARA = [
    ("We would like to submit the enclosed manuscript entitled ", ''),
    (f"“{TITLE}”", 'b'),
    (", which we wish to be considered for publication in ", ''),
    ("Systems", 'i'),
    (" for the Special Issue ", ''),
    (f"“{SI}.”", 'b'),
]

STUDY_PARA = [
    ("This study asks why youth employment outcomes deteriorate in a region where jobs "
     "are plentiful and the digital economy is expanding. We treat the graduate "
     "school-to-work transition in Zhejiang Province as a socio-technical system and "
     "build a six-state continuous-time feedback model in which open search, "
     "exam-oriented queueing, matched and mismatched employment, employability capital "
     "and aspirations co-evolve with an employer skill threshold that rises as "
     "digitalisation proceeds. Five structural parameters are estimated by simulated "
     "method of moments against seven published moments for China and Zhejiang, all of "
     "which the calibrated model reproduces within 3.5 per cent. The model is then "
     "subjected to fixed-point continuation and a multi-start uniqueness search, "
     "eigenvalue analysis, loop-deactivation experiments, Latin-hypercube Monte Carlo, "
     "Sobol variance decomposition, logistic and tree-based meta-modelling of the "
     "simulation output, and equal-effort policy experiments including deployment "
     "sequencing.", ''),
]

FIT_PARA = [
    ("We believe that this manuscript fits well within the scope of ", ''),
    ("Systems", 'i'),
    (f" and the Special Issue “{SI}”. The Special Issue calls for work that uses systems "
     "thinking as a holistic lens on the dynamic interactions, feedback mechanisms and "
     "emergent behaviours of socio-technical systems, and that integrates research with "
     "practice on a real-world problem. Youth employment in a digital-frontrunner "
     "province is precisely such a problem: the symptoms are widely measured, the "
     "single-cause explanations conflict with one another, and the instruments in use "
     "are chosen by convention rather than by evidence about leverage. Our contribution "
     "is to identify the feedback structure that generates the observed behaviour, to "
     "quantify which loops and which parameters dominate it, and to convert that "
     "structural knowledge into an effort-normalised ranking of policy instruments and a "
     "sequencing rule. The manuscript also connects directly to two recent articles in "
     "the journal—Grigorescu, Alistar and Lincaru (Systems 2025, 13, 649) on NEET "
     "vulnerability as an emergent systemic outcome, and Chacón-Cuberos et al. (Systems "
     "2025, 13, 479) on employability thinking as a latent competence system—by "
     "supplying the temporal dynamics that cross-sectional designs cannot provide.", ''),
]

INNOV = [
    [("(1) The paper reports a substantive negative result and shows why it matters.",
      'b'),
     (" Two-directional continuation in two control parameters and a multi-start search "
      "across twenty-four parameter cells find a unique stable fixed point throughout, "
      "so the youth transition system has no fold bifurcation, no second attractor and "
      "no hysteresis. What looks like a trap is in fact a drifting attractor combined "
      "with a slow state: the equilibrium non-employment rate moves from 0.119 in 2015 "
      "to 0.478 in 2040 while the realised state, whose slowest relaxation time is "
      "exactly eight years, lags it by about two years. Measured youth non-employment is "
      "therefore a lagging indicator of structural deterioration by a knowable margin. "
      "This distinction changes both the diagnosis and the vocabulary that should be "
      "used in the policy debate.", '')],

    [("(2) The paper triangulates structural dominance, variance attribution and "
      "statistical meta-modelling on the same calibrated object.", 'b'),
     (" Loop-deactivation experiments identify exam-queue congestion and aspiration "
      "adjustment as the dominant balancing loops and threshold escalation as the "
      "dominant reinforcing loop; a Sobol decomposition based on 14,336 model runs "
      "attributes 35.8 per cent of the output variance to the sensitivity of the "
      "employer threshold to digitalisation; and a logistic meta-model of the Monte "
      "Carlo sample, with an area under the curve of 0.994 and a non-significant "
      "Hosmer–Lemeshow statistic, together with a cross-validated classification tree, "
      "identify the same parameter as the root split. That three methods answering "
      "different questions converge on one mechanism is itself evidence about the "
      "model’s behaviour, and we suggest the triangulation as a routine step in "
      "simulation-based social science.", '')],

    [("(3) The paper delivers an actionable and counter-intuitive policy result.", 'b'),
     (" At equal standardised effort, moderating the escalation of the employer hiring "
      "bar—through competence-based rather than credential-based recruitment standards, "
      "certified micro-credentials and structured internships—lowers the 2040 "
      "non-employment rate by 0.107, roughly eighteen times the effect of vacancy "
      "creation and twenty-four times that of training intensity, the two instruments "
      "that dominate public spending. Sequencing matters at unchanged cumulative effort: "
      "front-loading expectation guidance before matching-efficiency investment lowers "
      "cumulative youth non-employment by about ten per cent relative to the reverse "
      "order. An archetype analysis further shows that the most digitally advanced "
      "prefectures face the steepest deterioration and also the largest policy "
      "dividend.", '')],
]

with zipfile.ZipFile(SRC) as z:
    doc = z.read('word/document.xml').decode('utf-8')

root = ET.fromstring(doc)
body = root.find(f'{{{W}}}body')
XMLSP = '{http://www.w3.org/XML/1998/namespace}space'


def para_text(p):
    return ''.join(t.text or '' for t in p.iter(f'{{{W}}}t'))


def base_rpr(p):
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
        rpr = copy.deepcopy(base) if base is not None else ET.Element(f'{{{W}}}rPr')
        r.append(rpr)
        if style == 'b':
            ET.SubElement(rpr, f'{{{W}}}b'); ET.SubElement(rpr, f'{{{W}}}bCs')
        elif style == 'i':
            ET.SubElement(rpr, f'{{{W}}}i'); ET.SubElement(rpr, f'{{{W}}}iCs')
        t = ET.SubElement(r, f'{{{W}}}t')
        t.set(XMLSP, 'preserve')
        t.text = text


innov_idx = 0
hits = set()
for p in body.findall(f'{{{W}}}p'):
    txt = para_text(p).strip()
    if not txt:
        continue
    if txt.startswith('We would like to submit the enclosed manuscript entitled'):
        set_para_rich(p, TITLE_PARA); hits.add('title')
    elif txt.startswith('This study investigates how industrial'):
        set_para_rich(p, STUDY_PARA); hits.add('study')
    elif re.match(r'^\(\d\)\s', txt):
        if innov_idx < 3:
            set_para_rich(p, INNOV[innov_idx]); innov_idx += 1
    elif txt.startswith('We believe that this manuscript fits well'):
        set_para_rich(p, FIT_PARA); hits.add('fit')

assert innov_idx == 3, f'innovation paragraphs replaced: {innov_idx}'
assert {'title', 'study', 'fit'} <= hits, hits

new_doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           + ET.tostring(root, encoding='unicode'))

shutil.copy(SRC, OUT)
with zipfile.ZipFile(SRC) as zin, zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        if item.filename == 'word/document.xml':
            zout.writestr(item, new_doc)
        else:
            zout.writestr(item, zin.read(item.filename))
print('written:', os.path.abspath(OUT))
