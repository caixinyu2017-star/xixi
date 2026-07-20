# -*- coding: utf-8 -*-
"""Paper 4 references — reuse of the verified paper-3 pool plus RCT-specific
additions (all adversarially verified; evidence in references_verified_new.json
and the paper-3 references_verified.json)."""
import json, os
from p3_refs_pool import REFS3 as POOL

HERE = os.path.dirname(os.path.abspath(__file__))

REUSE = ['ilo2024', 'mcgorry2024', 'gariepy2022', 'paul2009', 'peng2024',
         'involution', 'lieflat', 'ou2022', 'jones2025', 'creed2016',
         'maggiori2017', 'savickas2012', 'savickas2013', 'hou2012',
         'kroenke2009', 'duffy2016', 'wanberg2020', 'vanhooft2021',
         'ai_career_rev', 'ai_career_bs', 'bankins2024', 'demszky2023',
         'kjell2019', 'kjell2024', 'rathje2024', 'insel2017', 'abdurahman2024',
         'openai_gpt4o', 'qwen25', 'bh1995', 'eloundou2024', 'noy2023',
         'rudolph2017', 'elyoseph2023']
REFS4 = {k: dict(POOL[k]) for k in REUSE}

# inject verified DOIs/issues for reused keys (from the paper-3 evidence file)
_p3v = json.load(open(os.path.join(HERE, 'p3_references_verified.json')))['records']
_map = {'involution': 'involution1', 'lieflat': 'involution3', 'peng2024': 'cn_stress2',
        'ai_career_rev': 'ai_career1', 'ai_career_bs': 'ai_career2'}
for k in REUSE:
    rec = _p3v.get(_map.get(k, k))
    if rec and rec['verdict'] == 'CONFIRMED' and not REFS4[k].get('raw'):
        fin = rec['final']
        if fin.get('doi') and not REFS4[k].get('doi'):
            REFS4[k]['doi'] = fin['doi']
        for fld in ('issue', 'volume', 'pages'):
            if fin.get(fld) and not REFS4[k].get(fld):
                REFS4[k][fld] = fin[fld]

# new verified entries (fields from references_verified_new.json)
_new = json.load(open(os.path.join(HERE, 'references_verified_new.json')))['records']
INTEXT = {'ryan2000': 'Ryan & Deci', 'chen2015': 'Chen et al.',
          'tennant2007': 'Tennant et al.', 'fitzpatrick2017': 'Fitzpatrick et al.',
          'li2023': 'Li et al.', 'heinz2025': 'Heinz et al.', 'liu2014': 'Liu et al.',
          'koen2012': 'Koen et al.', 'caplan1989': 'Caplan et al.',
          'whiston2017': 'Whiston et al.', 'betz1996': 'Betz et al.',
          'consort2010': 'Schulz et al.', 'preacher2008': 'Preacher & Hayes',
          'darcy2021': 'Darcy et al.', 'torous2021': 'Torous et al.',
          'savickas1997': 'Savickas'}
for k, intext in INTEXT.items():
    f = _new[k]['final']
    REFS4[k] = dict(intext=intext, year=f['year'], authors=f['authors'],
                    title=f['title'].rstrip('.'), journal=f['journal'],
                    volume=f['volume'], issue=f['issue'],
                    pages=f['pages'].replace('-', '\u2013'), doi=f['doi'])
# journal-style normalization for two records
REFS4['tennant2007']['issue'] = ''
REFS4['consort2010']['issue'] = ''

# books (raw)
REFS4['ryan2017'] = dict(intext='Ryan & Deci', year='2017', raw=True,
    authors='Ryan, R. M., & Deci, E. L.', title='Self-determination theory', journal='',
    full='Ryan, R. M., & Deci, E. L. (2017). ⟦Self-determination theory: Basic psychological '
         'needs in motivation, development, and wellness⟧. Guilford Press.')
REFS4['cohen1988'] = dict(intext='Cohen', year='1988', raw=True,
    authors='Cohen, J.', title='Statistical power analysis', journal='',
    full='Cohen, J. (1988). ⟦Statistical power analysis for the behavioral sciences⟧ (2nd ed.). '
         'Lawrence Erlbaum Associates.')

# titles in sentence case where verifier returned Title Case
REFS4['betz1996']['title'] = 'Evaluation of a short form of the Career Decision-Making Self-Efficacy Scale'
REFS4['darcy2021']['title'] = ('Evidence of human-level bonds established with a digital conversational '
                               'agent: Cross-sectional, retrospective observational study')
REFS4['heinz2025']['title'] = 'Randomized trial of a generative AI chatbot for mental health treatment'
REFS4['tennant2007']['title'] = ('The Warwick–Edinburgh Mental Well-being Scale (WEMWBS): '
                                 'Development and UK validation')

REFS4['torous2021']['title'] = ('The growing field of digital psychiatry: Current evidence and the future of apps, social media, chatbots, and virtual reality')
