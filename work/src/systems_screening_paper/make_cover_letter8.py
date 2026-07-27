# -*- coding: utf-8 -*-
"""Build the paper-7 cover letter from the user's template docx by replacing
paragraph texts while preserving the template's formatting."""
import re, shutil, zipfile, os, copy
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
OUT = os.path.join(SCRATCH, 'Cover_Letter_Screening_Under_Signal_Collapse_Systems.docx')

TITLE = ('Screening Under Signal Collapse: Choice and Architecture Experiments on '
         'Employer Decision Rules and Youth Access to Entry-Level Work')
SI = 'Navigating Digital Transformation: Leadership and Decision Making in Today\u2019s Systems'

TITLE_PARA = [
 ('We would like to submit the enclosed manuscript entitled ', ''),
 (f'\u201c{TITLE}\u201d', 'b'),
 (', which we wish to be considered for publication in ', ''),
 ('Systems', 'i'),
 (' for the Special Issue ', ''),
 (f'\u201c{SI}.\u201d', 'b'),
]

STUDY_PARA = [
 ('This study asks how employers screen young applicants once generative artificial '
  'intelligence has made the written application cheap to produce, and whether the answer is '
  'a property of the people who screen or of the system they screen inside. Signalling theory '
  'predicts that a signal which everyone can produce at near-zero cost stops separating '
  'candidates, and platform evidence now shows exactly that collapse for written '
  'applications. What has been missing is the employer\u2019s side of the adjustment. We ran two '
  'linked experiments with 452 managers who make real shortlisting decisions in '
  'knowledge-intensive firms in China\u2019s Yangtze River Delta. Part A is a D-efficient '
  'discrete choice experiment: 6,328 choice tasks and 12,656 profile evaluations in which '
  'applicant profiles vary in AI-disclosure, process evidence, verified assessment results, '
  'institutional tier, referral, internship and salary, estimated by conditional logit, mixed '
  'logit with 500 scrambled Halton draws and a latent-class conditional logit. Part B holds '
  'the candidate pool fixed and randomises the screening interface itself\u2014AI-score first, '
  'credential first, or verified-evidence first\u2014so that the architecture is identified with '
  'preferences held constant by design, exactly as the preferences are identified with the '
  'architecture held constant in Part A.', ''),
]

FIT_PARA = [
 ('We believe that this manuscript fits well within the scope of ', ''),
 ('Systems', 'i'),
 (f' and the Special Issue \u201c{SI}\u201d. Its object of study is a decision that digital '
  'transformation has quietly moved from people to configuration: what the first screen puts '
  'in front of a manager, and in what order. We show that this configuration choice moves '
  'hiring outcomes far more than the preferences of the individual managers do, which '
  'relocates a problem usually framed as individual bias into the domain of system design and '
  'leadership. The paper is quantitative and multi-method in the way the journal\u2019s recent '
  'issues are\u2014random-utility modelling of individual decision data, discrete heterogeneity, '
  'out-of-sample validation and a randomised manipulation of the decision environment\u2014and it '
  'speaks directly to the Special Issue\u2019s concern with how leaders make and govern decisions '
  'inside digitally transformed systems. It also complements the survey-based and '
  'macro-econometric contributions the Special Issue has attracted by supplying experimental '
  'identification at the level of the individual screening decision.', ''),
]

INNOV = [
 [('(1) This study prices a signalling failure and shows that the repair is cheaper than the '
   'replacement.', 'b'),
  (' Expressing every attribute as a compensating salary differential puts the substitutes '
   'for the collapsed written signal in one metric. A verified assessment at the 90th '
   'percentile is worth 2.55 thousand CNY per month (95% CI 2.20 to 2.90), more than an elite '
   'degree at 1.83 and more than a referral at 1.73. Employers therefore prefer a costly, '
   'verifiable signal to an ascriptive one when it is available\u2014but it almost never is, '
   'because virtually no applicant arrives holding a verified result. The binding constraint '
   'is the infrastructure, not employer demand, and that is a policy-actionable finding rather '
   'than an exhortation.', '')],

 [('(2) This study shows that the penalty for disclosing AI assistance is large, conditional '
   'and largely repairable.', 'b'),
  (' Disclosure without corroboration costs an applicant 1.74 thousand CNY per month in '
   'compensating terms, about a sixth of monthly pay. Adding a portfolio of process '
   'evidence\u2014drafts, revisions, prompts, supervision records\u2014removes roughly three quarters '
   'of it, leaving \u22120.42, and removes all of it for the third of employers who already screen '
   'on evidence. This reframes the disclosure debate from whether declarations should be '
   'mandated, which invites an unenforceable answer, to what must accompany a declaration to '
   'make it informative. It also identifies a concealment trap: penalising honest disclosure '
   'without supplying a corroboration channel pushes applicants towards non-disclosure and '
   'destroys the information the rule was meant to create.', '')],

 [('(3) This study shows that the equity\u2013quality trade-off used to justify credential '
   'screening is an artefact of the interface, not a fact about candidates.', 'b'),
  (' Employer heterogeneity is discrete, not continuous: a three-class model recovers a '
   'credential-retreat regime (38.1%), a test-triage regime (28.4%) and an evidence-weighting '
   'regime (33.5%), and it beats the more flexible mixed logit out of sample (hit rate 0.642 '
   'versus 0.635; chance 0.333). The population-average disclosure coefficient of \u22120.741 '
   'describes no actual employer. Yet the architecture experiment dominates all of this: with '
   'the same managers and an identical candidate pool, evidence-first ordering raised the '
   'non-elite share of shortlists by 21.3 percentage points over credential-first and raised '
   'shortlist quality by 8.6 percentile points at the same time, at a cost of about 16 '
   'additional seconds per applicant. Screening on pedigree sacrifices quality as well as '
   'access, and the lever that fixes it sits with whoever configures the funnel.', '')],
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
            ET.SubElement(rpr, f'{{{W}}}b')
            ET.SubElement(rpr, f'{{{W}}}bCs')
        elif style == 'i':
            ET.SubElement(rpr, f'{{{W}}}i')
            ET.SubElement(rpr, f'{{{W}}}iCs')
        t = ET.SubElement(r, f'{{{W}}}t')
        t.set(XMLSP, 'preserve')
        t.text = text


paras = body.findall(f'{{{W}}}p')

# the template closes with two near-identical thank-you sentences; drop the
# first so the letter does not repeat itself to the editor
for p in paras:
    if para_text(p).strip().startswith('We sincerely appreciate your consideration'):
        body.remove(p)
        break
paras = body.findall(f'{{{W}}}p')

innov_idx = 0
hits = {'title': 0, 'study': 0, 'fit': 0}
for p in paras:
    txt = para_text(p).strip()
    if not txt:
        continue
    if txt.startswith('We would like to submit the enclosed manuscript entitled'):
        set_para_rich(p, TITLE_PARA); hits['title'] += 1
    elif txt.startswith('This study investigates how industrial'):
        set_para_rich(p, STUDY_PARA); hits['study'] += 1
    elif re.match(r'^\(\d\)\s', txt) or txt.startswith(('(1)', '(2)', '(3)')):
        if innov_idx < 3:
            set_para_rich(p, INNOV[innov_idx]); innov_idx += 1
    elif txt.startswith('We believe that this manuscript fits well'):
        set_para_rich(p, FIT_PARA); hits['fit'] += 1

assert innov_idx == 3, f'innovation paragraphs replaced: {innov_idx}'
assert all(v == 1 for v in hits.values()), hits

new_doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           + ET.tostring(root, encoding='unicode'))

with zipfile.ZipFile(SRC) as zin, zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        if item.filename == 'word/document.xml':
            zout.writestr(item, new_doc)
        else:
            zout.writestr(item, zin.read(item.filename))
print('written:', OUT)
