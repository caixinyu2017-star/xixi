# -*- coding: utf-8 -*-
"""References for the rationing paper.

The pool verified for the two companion papers is reused, and the entries added
here were each confirmed against the publisher record or an independent index on
2026-07-28.  Classical results in development and search economics are cited
from their original journal publication.
"""
import os
import sys

_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", ".."))
for _p in (os.path.join(_ROOT, "zhejiang-youth-systems-paper", "build"),
           os.path.join(_ROOT, "ai-entry-level-jobs-paper", "build")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from ai_refs import REFS as POOL          # noqa: E402

REFS = dict(POOL)

NEW = {
    # ------------------------------------------------ rationing and queueing
    'harris1970': dict(
        authors='Harris, J.R.; Todaro, M.P.',
        title='Migration, Unemployment and Development: A Two-Sector Analysis',
        journal='American Economic Review', year='1970', volume='60',
        pages='126-142'),
    'krueger1974': dict(
        authors='Krueger, A.O.',
        title='The Political Economy of the Rent-Seeking Society',
        journal='American Economic Review', year='1974', volume='64',
        pages='291-303'),
    'murphy1991': dict(
        authors='Murphy, K.M.; Shleifer, A.; Vishny, R.W.',
        title='The Allocation of Talent: Implications for Growth',
        journal='The Quarterly Journal of Economics', year='1991',
        volume='106', pages='503-530'),
    'gelb1991': dict(
        authors='Gelb, A.; Knight, J.B.; Sabot, R.H.',
        title='Public Sector Employment, Rent Seeking and Economic Growth',
        journal='The Economic Journal', year='1991', volume='101',
        pages='1186-1199'),
    'zenou2011': dict(
        authors='Zenou, Y.',
        title='Rural-Urban Migration and Unemployment: Theory and Policy '
              'Implications',
        journal='Journal of Regional Science', year='2011', volume='51',
        pages='65-82'),

    # ------------------------------------------------ retirement and the young
    'gruber2010': dict(
        authors='Gruber, J.; Wise, D.A. (Eds.)',
        title='Social Security Programs and Retirement around the World: The '
              'Relationship to Youth Employment',
        journal='University of Chicago Press: Chicago, IL, USA', year='2010'),
    'boeri2022': dict(
        authors='Boeri, T.; Garibaldi, P.; Moen, E.R.',
        title='In Medio Stat Victus: Labor Demand Effects of an Increase in '
              'the Retirement Age',
        journal='Journal of Population Economics', year='2022', volume='35',
        pages='519-556'),
    'bianchi2023': dict(
        authors='Bianchi, N.; Bovini, G.; Li, J.; Paradisi, M.; Powell, M.',
        title='Career Spillovers in Internal Labour Markets',
        journal='The Review of Economic Studies', year='2023', volume='90',
        pages='1800-1831'),
    'jiang2025': dict(
        authors='Jiang, M.; Kim, E.',
        title='Measuring Impacts of Retirement Age Extension on Economic '
              'Growth and Labor Market in China Using a Recursively Dynamic '
              'CGE Model',
        journal='Economic Systems Research', year='2025', volume='37',
        pages='306-334'),
    'gao2025': dict(
        authors='Gao, H.; Lu, B.',
        title='Reforming China’s Public Pension System: Fiscal Sustainability '
              'and the Challenge of Formality-Based Inequality',
        journal='Economic Modelling', year='2025', volume='153',
        pages='107336'),
    'mohnen2025': dict(
        authors='Mohnen, P.',
        title='The Impact of the Retirement Slowdown on the US Youth Labor '
              'Market',
        journal='Journal of Labor Economics', year='2025', volume='43',
        pages='203-246'),
    'vestad2013': dict(
        authors='Vestad, O.L.',
        title='Labour Supply Effects of Early Retirement Provision',
        journal='Labour Economics', year='2013', volume='25', pages='98-109'),
    'martins2009': dict(
        authors='Martins, J.O.; Gonand, F.; Antolin, P.; de la Maisonneuve, C.; '
                'Yoo, K.-Y.',
        title='The Impact of Ageing on Demand, Factor Markets and Growth',
        journal='OECD Economics Department Working Paper 420: Paris, France',
        year='2005'),

    # ------------------------------------------------ examination queues
    'mangal2024': dict(
        authors='Mangal, K.',
        title='The Long-Run Costs of Highly Competitive Exams for Government '
              'Jobs',
        journal='Journal of Development Economics', year='2024', volume='171'),
    'armijos2025': dict(
        authors='Armijos Bravo, G.; Vall Castelló, J.',
        title='Job Competition in Civil Service Public Exams and Sick Leave '
              'Behaviour',
        journal='Fiscal Studies', year='2025', volume='46', pages='91-123'),
    'gindling2020': dict(
        authors='Gindling, T.H.; Hasnain, Z.; Newhouse, D.; Shi, R.',
        title='Are Public Sector Workers in Developing Countries Overpaid? '
              'Evidence from a New Global Dataset',
        journal='World Development', year='2020', volume='126',
        pages='104737'),

    # ------------------------------------------------ public sector in DMP
    'albrecht2019': dict(
        authors='Albrecht, J.; Robayo-Abril, M.; Vroman, S.',
        title='Public-Sector Employment in an Equilibrium Search and Matching '
              'Model',
        journal='The Economic Journal', year='2019', volume='129',
        pages='35-61'),
    'chassamboulli2023': dict(
        authors='Chassamboulli, A.; Gomes, P.',
        title='Public-Sector Employment, Wages and Education Decisions',
        journal='Labour Economics', year='2023', volume='82'),
    'zhangx2024': dict(
        authors='Zhang, X.',
        title='Public Sector Employment Rigidity and Macroeconomic '
              'Fluctuation: A DSGE Simulation for China',
        journal='PLoS ONE', year='2024', volume='19', pages='e0308663'),

    # ------------------------------------------------ measuring slack
    'houston2025': dict(
        authors='Houston, D.; Lindsay, C.',
        title='Reconceptualising Labour Utilisation and Underutilisation with '
              'New “Full-Time Equivalent” Employment and Unemployment Rates',
        journal='Journal for Labour Market Research', year='2025',
        volume='59', pages='5'),

    # ------------------------------------------------ search theory additions
    'moen1997': dict(
        authors='Moen, E.R.',
        title='Competitive Search Equilibrium',
        journal='Journal of Political Economy', year='1997', volume='105',
        pages='385-411'),
    'rogerson2005': dict(
        authors='Rogerson, R.; Shimer, R.; Wright, R.',
        title='Search-Theoretic Models of the Labor Market: A Survey',
        journal='Journal of Economic Literature', year='2005', volume='43',
        pages='959-988'),

    # ------------------------------------------------ welfare accounting
    'hendren2020': dict(
        authors='Hendren, N.; Sprung-Keyser, B.',
        title='A Unified Welfare Analysis of Government Policies',
        journal='The Quarterly Journal of Economics', year='2020',
        volume='135', pages='1209-1318'),

    # ------------------------------------------------ systems and indicators
    'forrester1971': dict(
        authors='Forrester, J.W.',
        title='Counterintuitive Behavior of Social Systems',
        journal='Technology Review', year='1971', volume='73', pages='52-68'),
    'meadows1998': dict(
        authors='Meadows, D.H.',
        title='Indicators and Information Systems for Sustainable Development',
        journal='The Sustainability Institute: Hartland, VT, USA', year='1998'),
    'goodhart1984': dict(
        authors='Goodhart, C.A.E.',
        title='Problems of Monetary Management: The U.K. Experience. In '
              'Monetary Theory and Practice',
        journal='Macmillan Education: London, UK', year='1984',
        pages='91-121'),
}

REFS.update(NEW)
