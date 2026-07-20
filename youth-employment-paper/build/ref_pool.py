# -*- coding: utf-8 -*-
"""Curated mapping: citation key -> ordered list of real reference dicts.
Draws on the workflow pool (pool_wf.json), the verified core (core_refs.CORE),
and three web-verified gap references. All references are real with valid DOIs."""
import json, os, re
import core_refs

HERE = os.path.dirname(os.path.abspath(__file__))
POOL = json.load(open(os.path.join(HERE, "pool_wf.json")))


def _norm_pages(p):
    if not p:
        return p
    # convert hyphen page ranges between digits to en-dash
    return re.sub(r'(\d)\s*-\s*(\d)', r'\1–\2', str(p))


# index by DOI (lowercased)
IDX = {}
for r in POOL:
    d = (r.get('doi') or '').lower().strip()
    if d:
        r = dict(r); r['pages'] = _norm_pages(r.get('pages', ''))
        IDX[d] = r
for r in core_refs.CORE:
    d = (r.get('doi') or '').lower().strip()
    if d and d not in IDX:
        r2 = {k: r.get(k, '') for k in ('authors', 'title', 'journal_abbrev', 'year',
                                        'volume', 'issue', 'pages', 'doi')}
        r2['pages'] = _norm_pages(r2.get('pages', ''))
        IDX[d] = r2

# three web-verified gap references
GAP = [
    {'authors': 'Yang, X.; Wang, C.; Liu, B.',
     'title': 'ESG performance and corporate labor investment efficiency: Evidence from China',
     'journal_abbrev': 'Int. Rev. Econ. Finance', 'year': 2025, 'volume': '98', 'pages': '103910',
     'doi': '10.1016/j.iref.2025.103910'},
    {'authors': 'Huang, Y.; Liu, S.; Gan, J.; Liu, B.; Wu, Y.',
     'title': 'How does the construction of new generation of national AI innovative development pilot zones drive enterprise ESG development? Empirical evidence from China',
     'journal_abbrev': 'Energy Econ.', 'year': 2024, 'volume': '140', 'pages': '108011',
     'doi': '10.1016/j.eneco.2024.108011'},
    {'authors': 'Shen, L.; Li, Z.; Liang, Y.; Feng, Y.; Zhang, Z.',
     'title': 'Artificial intelligence adoption and corporate ESG performance: Evidence from a refined large language model',
     'journal_abbrev': 'Front. Artif. Intell.', 'year': 2025, 'volume': '8', 'pages': '1691468',
     'doi': '10.3389/frai.2025.1691468'},
]
for r in GAP:
    IDX[r['doi'].lower()] = r


def R(doi):
    d = doi.lower().strip()
    if d not in IDX:
        raise KeyError("Missing ref DOI: " + doi)
    return IDX[d]


# citation key -> ordered list of DOIs
KEY_MAP = {
    'ilo-neet': ['10.1007/s11135-022-01600-9', '10.1080/19186444.2020.1849936', '10.3390/su151411080'],
    'acemoglu-tasks': ['10.1257/jep.33.2.3', '10.3982/ECTA19815'],
    'ai-future-work': ['10.3389/frai.2024.1337264', '10.1007/s40821-025-00314-w'],
    'frey-automation': ['10.1016/j.techfore.2016.08.019'],
    'rammer-ai-innovation': ['10.1016/j.respol.2022.104555'],
    'ai-skills-demand': ['10.1016/j.econmod.2021.01.009', '10.1016/j.iref.2024.103739'],
    'sociotech-theory': ['10.1016/j.jenvman.2022.115596', '10.3390/su15032590',
                         '10.1016/j.jbusres.2020.07.045', '10.1016/j.apergo.2025.104604'],
    'digital-transformation-st': ['10.1007/s11023-024-09680-2', '10.1080/0960085X.2024.2347950',
                                  '10.1016/j.tourman.2025.105442'],
    'china-youth-unemp': ['10.1371/journal.pone.0298081', '10.1007/s11205-024-03439-z'],
    'china-digital-economy': ['10.1016/j.techsoc.2025.103129', '10.1016/j.heliyon.2024.e33893'],
    'acemoglu-robots': ['10.1086/705716', '10.1016/j.euroecorev.2024.104881', '10.1086/723205'],
    'youth-emp-determinants': ['10.1371/journal.pone.0298081', '10.1186/s13731-025-00531-7'],
    'bmi-value': ['10.1016/j.techfore.2022.122307', '10.1002/joe.22200', '10.1080/08276331.2023.2239039'],
    'ai-employment-firm': ['10.1016/j.chieco.2024.102137', '10.3390/su17093842',
                           '10.1080/13547860.2024.2403399', '10.1016/j.techfore.2020.120142'],
    'human-capital-skills': ['10.1007/s40821-025-00314-w', '10.1016/j.econmod.2021.01.009'],
    'dynamic-capabilities-ai': ['10.1002/smj.640', '10.1002/smj.2593', '10.1002/bse.3762'],
    'ai-bmi': ['10.1016/j.jbusres.2024.114764', '10.1007/s11846-022-00521-z',
               '10.1016/j.technovation.2025.103191'],
    'digital-entrepreneurship': ['10.1016/j.techfore.2023.122372', '10.1016/j.jbusres.2022.113507',
                                 '10.1016/j.techfore.2024.123330', '10.1002/sej.1542'],
    'skill-biased-tech': ['10.3982/ECTA19815', '10.1086/723205'],
    'oipt': ['10.5465/amr.1978.4305791'],
    'esg-employment': ['10.1016/j.iref.2025.103910', '10.3389/frai.2025.1691468'],
    'sustainable-entrepreneurship': ['10.1002/bse.3551', '10.1002/bse.3466',
                                     '10.1016/j.jbusres.2022.113379', '10.1002/bse.3418'],
    'ai-governance-policy': ['10.1016/j.eneco.2024.108011', '10.1108/DTS-08-2023-0061'],
    'digital-transformation-measure': ['10.1017/jmo.2023.34', '10.1002/bse.3691', '10.1093/qje/qjw024'],
    'psm-wellman': ['10.1007/s11142-016-9385-8'],
    'bartik-iv': ['10.1257/aer.20181047'],
}

KEY_REFS = {k: [R(doi) for doi in dois] for k, dois in KEY_MAP.items()}
