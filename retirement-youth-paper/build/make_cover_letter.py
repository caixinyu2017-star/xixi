# -*- coding: utf-8 -*-
"""Build the cover letter from the author's own template, preserving formatting.

Every figure quoted in the letter is read from stats.json, so the letter cannot
disagree with the manuscript.
"""
import copy
import json
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

S = json.load(open(os.path.join(HERE, 'stats.json')))
B, QC, RF = S['baseline'], S['queue_cost'], S['reform']
CH, IND, IX, UNC = S['channels'], S['indicator'], S['indexation'], S['uncertainty']
MET = S['meta']
POL = {r['key']: r for r in S['policy_baseline']}


def _m(t):
    """Typographic minus sign, as the journal's style requires."""
    return t.replace('-', '\u2212')


def pc(x, d=1):
    return _m(('%%.%df' % d) % (100 * x))


def n(x, d=2):
    return _m(('%%.%df' % d) % x)


def lpt(x, d=2):
    return _m(('%%+.%df' % d) % (100 * x))


SRC = os.path.join(HERE, 'cover_letter_template.docx')
OUT = os.path.join(HERE, '..',
                   'Cover_Letter_The_Queue_Absorbs_the_Shock.docx')

TITLE = ('The Queue Absorbs the Shock: Administrative Job Rationing, Delayed '
         'Retirement and the Blind Spot in Youth Unemployment Statistics')
SI = 'Systems Thinking and Modelling in Socio-Economic Systems'

TITLE_PARA = [
    ('We would like to submit the enclosed manuscript entitled ', ''),
    (f'“{TITLE}”', 'b'),
    (', which we wish to be considered for publication in ', ''),
    ('Systems', 'i'),
    (' for the Special Issue ', ''),
    (f'“{SI}.”', 'b'),
    (' Should that Special Issue have closed by the time of submission, we '
     'would be glad for the manuscript to be considered for the ', ''),
    ('Systems Practice in Social Science', 'i'),
    (' Section instead.', ''),
]

STUDY_PARA = [
    ('China began raising its statutory retirement age on 1 January 2025, and '
     'the public debate has been dominated by a single question: whether older '
     'workers staying longer will cost younger workers their jobs. This study '
     'shows that the question is the wrong one, and that the statistic used to '
     'answer it cannot detect what the reform actually does. We build a '
     'two-sector, two-age search-and-matching model in which an establishment '
     'sector whose headcount is fixed by administrative rule coexists with a '
     'free-entry market sector. Because establishment posts pay a large '
     'compensation premium and are allocated by examination, young workers '
     'queue for them exactly as rural migrants queue for urban jobs in Harris '
     'and Todaro. Six structural parameters are estimated so that the model '
     'reproduces six published Chinese labour-market moments exactly rather '
     'than approximately, and the estimated economy then reproduces a queueing '
     'duration that was never targeted and that matches independent evidence '
     'on repeat examination candidates.', ''),
]

FIT_PARA = [
    ('We believe that this manuscript fits well within the scope of ', ''),
    ('Systems', 'i'),
    (f' and the Special Issue “{SI}”. The Special Issue calls for systems '
     'thinking and modelling applied to current socio-economic problems, and '
     'this paper is a worked instance of the classical systems proposition '
     'that a social system responds counterintuitively to intervention. A '
     'labour market with an administratively rationed segment is a coupled '
     'system, not a single market: a demographic shock propagates through '
     'three distinct routes that do not share a sign, and the aggregate '
     'indicator used to monitor the system adds them together and reports '
     'nothing. We can say exactly why the indicator is silent, decompose the '
     'offsetting forces by the Shapley value, measure how much larger the real '
     'change is than the measured one, and show that the intuitive remedy '
     'makes the system worse. The manuscript also connects directly to recent '
     'work in the journal on youth transition outcomes as emergent systemic '
     'properties and on employment systems modelled by simulation, to which it '
     'supplies an estimated general-equilibrium mechanism and a concrete '
     'proposal for what to measure instead.', ''),
]

INNOV = [
    [('(1) The paper separates two questions that the retirement debate has '
      'merged, and shows that the reassuring answer to the first does not '
      'carry over to the second.', 'b'),
     (' “Will I be displaced from a job I hold?” is governed by free entry, '
      'which restores what a shock takes away; our crowding-out coefficient is '
      f'{n(RF["crowding_out"], 4)}, so the lump-of-labour hypothesis is '
      'rejected and the international consensus is reproduced in a model never '
      'calibrated to it. “Will the job I am preparing for still be there?” is '
      'governed by an administrative ceiling, which restores nothing, because '
      'there is no employer-side decision to restore. The chance that a member '
      'of an entering cohort ever holds a rationed job falls '
      f'{pc(abs(RF["d_entry_prob"]), 1)} per cent—about '
      f'{"{:,.0f}".format(round(1000 * RF["entry_lost_thousands"], -3))} young '
      'people a year at a cohort of '
      f'{n(MET["cohort"], 1)} million—and a Shapley decomposition attributes '
      'the whole of that fall to the establishment’s shrinking replacement '
      'flow, with the horizon and demographic routes contributing exactly '
      'zero.', '')],

    [('(2) The paper demonstrates, rather than asserts, that a headline '
      'indicator can be structurally blind to a large change.', 'b'),
     (' Over the full fifteen-year reform the youth unemployment rate moves by '
      f'{n(RF["u_rate_y_pp"], 3)} percentage points. It does so not because '
      'nothing happens but because three channels of opposite sign almost '
      'exactly cancel inside it: in log points the quota route contributes '
      f'{lpt(CH["u_rate_y"]["quota"])}, the horizon route '
      f'{lpt(CH["u_rate_y"]["value"])} and the demographic route '
      f'{lpt(CH["u_rate_y"]["demo"])}. Access falls '
      f'{n(IND["ratio"], 0)} times more than the headline rate moves, in the '
      'estimated economy and in every one of '
      f'{UNC["n_solved"]} Latin hypercube draws over the parameters we did not '
      'estimate. The blindness is structural, not statistical: an '
      'unemployment rate is a stock ratio at a moment, while access to a '
      'rationed sector is a probability over a lifetime, and broadening the '
      'unemployment concept would not help because the people affected are '
      'employed. We therefore propose three administrative series—'
      'establishment hires per cohort, registered candidates per cohort, and '
      'the implied wait—that would have caught this, cost nothing, and are '
      'not currently published.', '')],

    [('(3) The paper prices the queue and shows that the intuitive remedy '
      'lowers welfare.', 'b'),
     (' The young people preparing full time for examinations forgo output '
      f'worth {n(QC["pct_of_output"], 1)} per cent of gross domestic product a '
      'year, and selection by examination would have to raise the '
      'productivity of every establishment worker by '
      f'{pc(QC["break_even_screening"], 0)} per cent, permanently, for that to '
      'be efficient. At a common budget of '
      f'{n(100 * MET["budget"], 1)} per cent of output, expanding the '
      'establishment—the response most often proposed—raises access but lowers '
      'welfare per head and returns '
      f'{n(POL["s_N"]["mvpf"], 2)} units of welfare per unit of public money, '
      'because the Harris–Todaro indifference condition restores the queue in '
      'proportion to whatever is added to the prize. Cutting the administered '
      f'premium returns {n(POL["tau_q"]["mvpf"], 2)}, and is the best of the '
      'three instruments in every uncertainty draw. Fully indexing the '
      'establishment to the labour force restores '
      f'{n(IX["restored_pct"], 0)} per cent of the lost access but costs '
      f'{n(IX["fiscal_pct_Y"], 2)} per cent of output and lowers welfare per '
      'head. The paper therefore ends on a policy recommendation that runs '
      'against the direction of current practice, and on a measurement '
      'recommendation that costs nothing to adopt.', '')],
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
