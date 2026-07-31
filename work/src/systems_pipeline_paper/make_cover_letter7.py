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
OUT = os.path.join(SCRATCH, 'Cover_Letter_Vanishing_First_Rung_Systems.docx')

TITLE = ('The Vanishing First Rung: A System Dynamics Study of Entry-Level Automation, '
         'Senior Time Allocation and the Erosion of the Professional Expertise Pipeline')
SI = 'Navigating Digital Transformation: Leadership and Decision Making in Today’s Systems'

TITLE_PARA = [
 ('We would like to submit the enclosed manuscript entitled ', ''),
 (f'“{TITLE}”', 'b'),
 (', which we wish to be considered for publication in ', ''),
 ('Systems', 'i'),
 (' for the Special Issue ', ''),
 (f'“{SI}.”', 'b'),
]

STUDY_PARA = [
 ('This study asks what happens to a profession when the tasks it has always used to train '
  'newcomers can be performed by a machine. Generative artificial intelligence automates '
  'precisely the routine, supervised work through which graduates become proficient '
  'professionals, so every automation decision a manager takes today silently withdraws a '
  'unit of practice whose value would have appeared six to eight years later. We combine two '
  'studies. Study 1 surveys 356 knowledge-intensive firms in China’s Yangtze River Delta and '
  'estimates, from administrative staffing and personnel records rather than from attitude '
  'scales, the behavioural parameters that link automation depth to entry hiring, senior '
  'verification time, mentoring intensity and time to independent proficiency. Study 2 embeds '
  'those estimates in a five-stock system dynamics model of the entrant pool, the junior and '
  'senior workforce and the skill capital of excluded entrants, and subjects it to the full '
  'confidence-building protocol for dynamic models—dimensional, equilibrium, '
  'extreme-condition, integration-error, structural and behaviour-reproduction tests—before '
  'using it to run counterfactual, threshold, decomposition and policy experiments over a '
  'thirty-year horizon.', ''),
]

FIT_PARA = [
 ('We believe that this manuscript fits well within the scope of ', ''),
 ('Systems', 'i'),
 (f' and the Special Issue “{SI}”. The paper is squarely about leadership and decision '
  'making: its object of study is the managerial decision of how deeply to automate '
  'entry-level work and how to allocate the finite time of senior professionals between '
  'delivery, verification of machine output and mentoring. It shows that a sequence of '
  'locally rational decisions of this kind produces a systemically costly outcome because the '
  'accumulation being depleted lies outside the horizon of the measures that govern the '
  'decision, and it identifies which leadership levers actually move the system. The '
  'methodology is explicitly systemic—stocks, flows, feedback loops, delays, thresholds and '
  'leverage points—which we hope makes the paper a natural fit for the journal’s readership, '
  'and it complements the survey-based and econometric contributions that the Special Issue '
  'has attracted by supplying the longitudinal, feedback-based perspective that those designs '
  'cannot provide.', ''),
]

INNOV = [
 [('(1) This study supplies the longitudinal, feedback-based account of entry-level AI '
   'exposure that the current empirical literature calls for but cannot itself provide.', 'b'),
  (' Recent payroll and vacancy studies observe at most two years of what is a thirty-year '
   'adjustment. By making time to independent proficiency an endogenous variable that responds '
   'to mentoring, to the learning content of practice and to cohort quality, and by letting '
   'the senior workforce feed back into all three, we show that a transitory hiring shock is '
   'converted into a persistent capability deficit. The stock of proficient professionals ends '
   '46.3% below the no-automation counterfactual, yet productive capacity first rises 8.7% '
   'above it and does not cross back below until year 16.6—so for sixteen years every '
   'indicator a firm actually tracks confirms that the decision was correct.', '')],

 [('(2) This study relocates the mechanism, contradicting the account that dominates current '
   'commentary.', 'b'),
  (' It is widely asserted that AI erodes professional training because it leaves senior staff '
   'with no time to teach. Our survey finds no direct effect of automation depth on mentoring '
   'intensity once delivery pressure is controlled, and the simulation shows that automation '
   'initially lowers senior utilisation rather than raising it. Structural decomposition '
   'attributes 41.2 of the 46.3 percentage-point deficit to task substitution and to the loss '
   'of learning content in the entry work that survives, and only 5.7 points to the mentoring '
   'squeeze, which engages after year 23 and then produces an abrupt regime shift. We also '
   'find that the system’s only self-correcting loop is self-defeating: hiring more graduates '
   'in response to a visible shortage dilutes the mentoring that converts them, worsening the '
   'year-30 outcome by 2.7 percentage points.', '')],

 [('(3) This study identifies a leverage point that differs from the instrument policy '
   'debate has settled on, and shows that it is already achievable.', 'b'),
  (' Subsidising entry hiring works but requires 0.306 additional entry hires per additional '
   'senior-year created; restoring the learning content of entry work through structured '
   'AI-assisted apprenticeship requires only 0.122, is 2.5 times more efficient, and is the '
   'only single lever that raises the pipeline’s conversion rate above its pre-automation '
   'value. Crucially, our survey shows this is not aspirational: the learning penalty of '
   'automation is large at the 25th percentile of structured practice and statistically '
   'indistinguishable from zero at the 95th percentile, so firms already at the top of the '
   'observed distribution avoid the damage entirely, using protocols that require no '
   'additional headcount or budget.', '')],
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
