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
OUT = os.path.join(SCRATCH, 'Cover_Letter_Pipeline_Overshoots_Shock_Systems.docx')

TITLE = ('The Pipeline Overshoots the Shock: An Adaptive-Belief Systems Model of '
         'Delayed Educational Supply and Graduate Labour-Market Adjustment')
SI = ('Economic System Management, Sustainability, and Innovation in Digital '
      'Environments')

TITLE_PARA = [
 ('We would like to submit the enclosed manuscript entitled ', ''),
 (f'\u201c{TITLE}\u201d', 'b'),
 (', which we wish to be considered for publication in ', ''),
 ('Systems', 'i'),
 (' for the Special Issue ', ''),
 (f'\u201c{SI}.\u201d', 'b'),
]

STUDY_PARA = [
 ('A degree takes four years to produce, so the students who react to a labour market '
  'reach it four years late. This study asks what that delay does to an education '
  'system when demand for one field falls abruptly, as demand for entry-level '
  'computing work has since 2023. We build a two-field model in which firms hire '
  'entry-tier graduates through a matching market with free entry, the two kinds of '
  'graduate are imperfect substitutes in production so that a crowded field is one in '
  'which graduates are both poorly paid and hard to place, and entrants choose a field '
  'by a discrete-choice rule after forecasting what it will be worth on graduation. '
  'Forecasts come from two competing rules\u2014one anchored on the field\u2019s long-run '
  'value, one that projects the recent trend\u2014and the weight on each evolves with its '
  'recent accuracy, which makes the education system an adaptive belief system in the '
  'sense of Brock and Hommes. The labour block is calibrated to four moments of the '
  'pre-shock graduate market and matches them to thirteen decimal places; the size of '
  'the technology shock is then set so that the model reproduces the new-graduate '
  'unemployment rate now observed in the exposed field, which leaves the entire '
  'transition free to be right or wrong. The model is solved, calibrated and simulated '
  'from a single seeded pipeline, and it uses no individual-level data: every '
  'calibration target is a published aggregate.', ''),
]

FIT_PARA = [
 ('We believe that this manuscript fits well within the scope of ', ''),
 ('Systems', 'i'),
 (f' and the Special Issue \u201c{SI}\u201d. Its subject is the management of an economic '
  'system under a digital-technology shock: how a coupled education\u2013labour system '
  'allocates people between fields when the information it runs on arrives later than '
  'the decisions it governs. The paper is explicitly systemic in its machinery\u2014state '
  'variables, a production delay, a balancing loop crossed with a reinforcing one, '
  'stability analysis of the stationary state and a global sensitivity sweep\u2014and it '
  'is quantitative economics throughout, which we hope complements the more empirical '
  'and management-oriented contributions the Special Issue has attracted. Its policy '
  'content concerns resource allocation and the design of information flows under '
  'digital transformation, which sit squarely in the call\u2019s keyword list.', ''),
]

INNOV = [
 [('(1) This study brings adaptive belief systems to the education market, where the '
   'production lag is a degree.', 'b'),
  (' The Brock\u2013Hommes mechanism\u2014agents switching between forecasting rules according '
   'to recent accuracy, with the intensity of switching as the bifurcation '
   'parameter\u2014has been applied to asset markets, to macroeconomic expectations and to '
   'commodity markets with production lags. We could not find it applied to the choice '
   'of what to study, which is the market with the longest production lag of all and '
   'the one in which a bad forecast is least reversible. Embedding it in an equilibrium '
   'search-and-matching labour block, rather than in a reduced-form demand curve, is '
   'what allows the model to speak about unemployment as well as wages, and it is what '
   'lets the current configuration of the exposed field\u2014a high early-career wage '
   'alongside an unusually high new-graduate unemployment rate\u2014be reproduced as a '
   'property of the transition rather than assumed.', '')],

 [('(2) The enrolment response overreacts by a factor of two, and the delay alone does '
   'not explain it.', 'b'),
  (' The entering share falls 28.5 per cent on impact when the warranted long-run fall '
   'is 13.9 per cent. Most of the enrolment collapse that follows such a shock is '
   'therefore transitional rather than warranted. The decomposition across belief '
   'regimes is the part we regard as most informative: with beliefs anchored on the '
   'field\u2019s long-run value the amplification is only 1.10, so a four-year delay by '
   'itself produces very nearly the right answer. It is the competition between '
   'forecasting rules that does the work, and the amplification rises monotonically to '
   '1.89 when a trend-projecting rule is present and to 2.48 when entrants imitate the '
   'recently successful rule sharply. The result survives a global sensitivity sweep: '
   'the amplification exceeds one in every draw that admits an exact recalibration.', '')],

 [('(3) The size of a system\u2019s correction is not a measure of how well it is behaving, '
   'and we show that an indicator built on it ranks interventions backwards.', 'b'),
  (' This is the finding we did not expect and the one with the clearest practical '
   'content. Making the signal about current returns noisier shrinks the enrolment '
   'swing markedly, from an amplification of 2.05 to 1.65, and it raises the adjustment '
   'cost by 14 per cent. Publishing the enrolment pipeline\u2014the cohorts already '
   'enrolled and not yet graduated\u2014does the opposite: it makes the immediate response '
   'deeper and lowers the adjustment cost by about six per cent. The two rankings are '
   'opposite because the deeper response is the better-informed one: at the moment the '
   'shock lands, four large pre-shock cohorts are still coming, and an entrant who can '
   'see them correctly infers that the field will stay crowded. A ministry that judged '
   'an information policy by whether it calmed enrolment swings would therefore reject '
   'the policy that improves allocation and adopt the one that degrades it. The '
   'stabilising series is an administrative by-product that education systems already '
   'hold and almost none publish in usable form.', '')],
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
