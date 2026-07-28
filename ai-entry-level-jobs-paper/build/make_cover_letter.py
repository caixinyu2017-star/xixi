# -*- coding: utf-8 -*-
"""Build the cover letter from the author's own template, preserving formatting."""
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
B, P, W_ = S['baseline'], S['planner'], S['wedge']
SH, EX, WS = S['shock'], S['exposure'], S['wedge_sources']
POL = {r['key']: r for r in S['policy_baseline']}
RIG0 = S['rigidity'][0]
RIG1 = [r for r in S['rigidity'] if r['gamma_w'] == 1.0][0]
FOLD = 1.0 + W_['mentoring']


def pc(x, d=1):
    return ('%%.%df' % d) % (100 * x)


def n(x, d=2):
    return ('%%.%df' % d) % x


import math                                                   # noqa: E402


def lp(x, d=0):
    return ('%%.%df' % d) % abs(100 * (math.exp(x) - 1.0))


SRC = os.path.join(HERE, 'cover_letter_template.docx')
OUT = os.path.join(HERE, '..',
                   'Cover_Letter_Narrowing_the_Gate_AI_and_Entry_Level_Access.docx')

TITLE = ('Narrowing the Gate, Not Breaking the Ladder: Artificial Intelligence, '
         'Entry-Level Access and the Under-Provision of On-the-Job Training')
SI = 'Artificial Intelligence in Socio-Technical Systems'

TITLE_PARA = [
    ('We would like to submit the enclosed manuscript entitled ', ''),
    (f'“{TITLE}”', 'b'),
    (', which we wish to be considered for publication in ', ''),
    ('Systems', 'i'),
    (' for the Special Issue ', ''),
    (f'“{SI}.”', 'b'),
]

STUDY_PARA = [
    ('An entry-level job is a joint product: it delivers output today and it is the '
     'only technology that turns a novice into an experienced worker. Artificial '
     'intelligence substitutes for the first component and not for the second, which '
     'has made the fate of the career ladder an urgent question for every economy '
     'with a large graduating cohort. This study builds a two-tier '
     'search-and-matching model of that ladder in which mentoring intensity, '
     'promotion, vacancy creation on both tiers, wages and the demand for artificial '
     'intelligence are all determined jointly, and in which two ordinary contracting '
     'frictions—non-contractible training and poaching of trained workers—separate '
     'the private from the social return to producing an experienced worker. Eight '
     'structural parameters are estimated so that the model reproduces eight '
     'published Chinese labour-market moments exactly rather than approximately, and '
     'the estimated economy is then confronted with a relationship that was held out '
     'of the estimation entirely.', ''),
]

FIT_PARA = [
    ('We believe that this manuscript fits well within the scope of ', ''),
    ('Systems', 'i'),
    (f' and the Special Issue “{SI}”. The Special Issue calls for work on '
     'the interaction between artificial intelligence and the human, organisational '
     'and institutional structures it is embedded in. The career ladder is exactly '
     'such a structure: it is a feedback loop in which entry-level hiring produces '
     'experienced workers and experienced workers supply the mentoring without which '
     'no further entrants can be promoted. Our contribution is to show that whether '
     'artificial intelligence damages that loop, and who bears the cost when it does '
     'not, depends on institutional features—the contractibility of training and the '
     'rigidity of entry wages—rather than on the technology alone. The manuscript '
     'also connects to recent work in the journal on artificial intelligence in '
     'organisational decision systems and on youth transition outcomes as emergent '
     'systemic properties, to which it supplies the price-theoretic mechanism and an '
     'estimated magnitude.', ''),
]

INNOV = [
    [('(1) The paper identifies and quantifies a large market failure in an economy '
      'that is efficient by construction on every other margin.', 'b'),
     (' Worker bargaining power is set equal to the matching elasticity, so the '
      'Hosios condition holds exactly and the classical search externality is '
      'switched off. Even so, the estimated economy provides about one seventh of '
      f'the socially efficient amount of on-the-job training, so first promotion '
      f'takes {n(B["promo_years"], 1)} years instead of {n(P["promo_years"], 1)}, '
      f'the stock of experienced workers is {pc(W_["e_s"], 1)} per cent below the '
      f'optimum and welfare is {n(W_["welfare_pct"], 2)} per cent below it. We prove '
      'and then verify numerically to machine precision that the Hosios condition '
      'decentralises vacancy creation but can never decentralise training, and we '
      'decompose the residual wedge into a hold-up component '
      f'({pc(WS["holdup_share"], 0)} per cent) and a poaching component.', '')],

    [('(2) The paper reports a substantive negative result: artificial intelligence '
      'narrows the gate but does not break the ladder.', 'b'),
     (' Our prior, and the prevailing reading of the evidence, was that automating '
      'entry-level work must eventually starve an economy of experienced workers. '
      'The estimated model says otherwise. When the artificial-intelligence share of '
      'entry-level tasks doubles, the entry-level employment rate falls by '
      f'{lp(SH["d_ln_emp_rate_j"], 1)} per cent, but firms respond by mentoring the '
      f'smaller intake {lp(SH["d_ln_m"])} per cent more intensively, so the flow of '
      'promotions and the stock of experienced workers move by less than '
      f'{lp(SH["d_ln_e_s"], 1)} per cent and time to first promotion falls rather '
      'than rises. The training wedge narrows rather than widens, because scarcer '
      'entrants are individually more worth training. The externality is large, but '
      'it is pre-existing and is not created by the technology—which changes the '
      'policy question from how to slow artificial intelligence to how to price '
      'training.', '')],

    [('(3) The paper shows that the incidence of the shock is institutional rather '
      'than technological, and validates the model out of sample.', 'b'),
     (' Whether the shock is borne by entry-level pay or by entry-level access '
      'depends almost entirely on the wage rule. With flexible bargaining the entry '
      f'wage falls {lp(RIG0["d_ln_w_j"], 1)} per cent and the employment rate barely '
      f'moves; with a rigid entry wage the employment rate falls '
      f'{lp(RIG1["d_ln_emp_rate_j"], 1)} per cent and pay does not move at all. The '
      'widely cited stylised fact that artificial intelligence reduces young '
      'workers’ employment without reducing their pay is therefore evidence '
      'about wage-setting institutions, and it reconciles studies that find large '
      'employment effects with studies that find precise nulls. Using no '
      'employment-by-exposure information anywhere in the estimation, the model '
      f'predicts a cross-occupation entry-level employment gradient of '
      f'{n(EX["did_pct"], 1)} per cent against the {n(EX["target_pct"], 1)} per cent '
      'estimated from United States payroll microdata, and reproduces the '
      'employment-not-pay pattern at approximately the observed relative magnitude. '
      'At a common budget a mentoring credit dominates entry-level wage and vacancy '
      f'subsidies and a tax on artificial intelligence, with a marginal value of '
      f'public funds of {n(POL["s_m"]["mvpf"], 1)} against '
      f'{n(POL["s_w"]["mvpf"], 2)} for the wage subsidy, which is worse than doing '
      'nothing.', '')],
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
