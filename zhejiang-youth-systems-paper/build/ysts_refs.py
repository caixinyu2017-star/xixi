# -*- coding: utf-8 -*-
"""References for the YSTS paper.

Two sources are combined: (i) the previously verified structured pools in
paper_refs.py and p2_refs.py, and (ii) new entries added for this paper, each
confirmed by web search against at least two independent sources (publisher
page, Semantic Scholar/RePEc/DOI record) on 2026-07-28.
"""
from paper_refs import REFS as POOL1
from p2_refs import REFS2 as POOL2

REFS = {}
REFS.update(POOL1)
REFS.update(POOL2)

NEW = {
    # ------------------------------------------------ the two focal Systems papers
    'grigorescu2025': dict(
        authors='Grigorescu, A.; Alistar, T.V.; Lincaru, C.',
        title='Digital Skills, Ethics, and Integrity—The Impact of Risky Internet Use, '
              'a Multivariate and Spatial Approach to Understanding NEET Vulnerability',
        journal='Systems', year='2025', volume='13', pages='649'),
    'chacon2025': dict(
        authors='Chacón-Cuberos, R.; Rodríguez-Sabiote, C.; Expósito-López, J.; '
                'Olmedo-Moreno, E.; Serrano-García, J.; Hortas-Aliaga, O.',
        title='Development of an Employability Thinking Scale for Use with Young People '
              'in Training: Exploratory and Confirmatory Factor Analysis',
        journal='Systems', year='2025', volume='13', pages='479'),
    'chen2026': dict(
        authors='Chen, C.; Zhu, J.; Sun, H.',
        title='Mechanisms and Pathways of Promoting High-Quality Full Employment Under '
              'the Dual Circulation Paradigm: An Evolutionary Simulation Approach Based '
              'on System Dynamics',
        journal='Systems', year='2026', volume='14', pages='737'),
    'tleppayev2025': dict(
        authors='Tleppayev, A.; Zeinolla, S.',
        title='Forecasting Youth Unemployment Through Educational and Demographic '
              'Indicators: A Panel Time-Series Approach',
        journal='Forecasting', year='2025', volume='7', pages='37'),

    # ------------------------------------------------ system dynamics and systems science
    'forrester1961': dict(
        authors='Forrester, J.W.', raw=True,
        full='Forrester, J.W. Industrial Dynamics; MIT Press: Cambridge, MA, USA, 1961.',
        title='Industrial Dynamics', journal='MIT Press', year='1961'),
    'sterman2000': dict(
        authors='Sterman, J.D.', raw=True,
        full='Sterman, J.D. Business Dynamics: Systems Thinking and Modeling for a '
             'Complex World; Irwin/McGraw-Hill: Boston, MA, USA, 2000.',
        title='Business Dynamics', journal='McGraw-Hill', year='2000'),
    'meadows2008': dict(
        authors='Meadows, D.H.', raw=True,
        full='Meadows, D.H. Thinking in Systems: A Primer; Chelsea Green Publishing: '
             'White River Junction, VT, USA, 2008.',
        title='Thinking in Systems', journal='Chelsea Green', year='2008'),
    'barlas1996': dict(
        authors='Barlas, Y.',
        title='Formal aspects of model validity and validation in system dynamics',
        journal='Syst. Dyn. Rev.', year='1996', volume='12', pages='183–210'),
    'ford1999': dict(
        authors='Ford, D.N.',
        title='A behavioral approach to feedback loop dominance analysis',
        journal='Syst. Dyn. Rev.', year='1999', volume='15', pages='3–36'),
    'ghaffarzadegan2011': dict(
        authors='Ghaffarzadegan, N.; Lyneis, J.; Richardson, G.P.',
        title='How small system dynamics models can help the public policy process',
        journal='Syst. Dyn. Rev.', year='2011', volume='27', pages='22–44'),
    'rahmandad2012': dict(
        authors='Rahmandad, H.; Sterman, J.D.',
        title='Reporting guidelines for simulation-based research in social sciences',
        journal='Syst. Dyn. Rev.', year='2012', volume='28', pages='396–411'),
    'scheffer2009': dict(
        authors='Scheffer, M.; Bascompte, J.; Brock, W.A.; Brovkin, V.; Carpenter, S.R.; '
                'Dakos, V.; Held, H.; van Nes, E.H.; Rietkerk, M.; Sugihara, G.',
        title='Early-warning signals for critical transitions',
        journal='Nature', year='2009', volume='461', pages='53–59'),

    # ------------------------------------------------ methods
    'sobol2001': dict(
        authors='Sobol’, I.M.',
        title='Global sensitivity indices for nonlinear mathematical models and their '
              'Monte Carlo estimates',
        journal='Math. Comput. Simul.', year='2001', volume='55', pages='271–280'),
    'saltelli2010': dict(
        authors='Saltelli, A.; Annoni, P.; Azzini, I.; Campolongo, F.; Ratto, M.; '
                'Tarantola, S.',
        title='Variance based sensitivity analysis of model output. Design and estimator '
              'for the total sensitivity index',
        journal='Comput. Phys. Commun.', year='2010', volume='181', pages='259–270'),
    'petrongolo2001': dict(
        authors='Petrongolo, B.; Pissarides, C.A.',
        title='Looking into the black box: A survey of the matching function',
        journal='J. Econ. Lit.', year='2001', volume='39', pages='390–431'),
    'prelec1998': dict(
        authors='Prelec, D.',
        title='The probability weighting function',
        journal='Econometrica', year='1998', volume='66', pages='497–527'),
    'tversky1992': dict(
        authors='Tversky, A.; Kahneman, D.',
        title='Advances in prospect theory: Cumulative representation of uncertainty',
        journal='J. Risk Uncertain.', year='1992', volume='5', pages='297–323'),

    # ------------------------------------------------ youth transitions and mismatch
    'rahmani2023': dict(
        authors='Rahmani, H.; Groot, W.',
        title='Risk factors of being a youth not in education, employment or training '
              '(NEET): A scoping review',
        journal='Int. J. Educ. Res.', year='2023', volume='120', pages='102198'),
    'mcguinness2018': dict(
        authors='McGuinness, S.; Pouliakas, K.; Redmond, P.',
        title='Skills mismatch: Concepts, measurement and policy approaches',
        journal='J. Econ. Surv.', year='2018', volume='32', pages='985–1015'),
    'pan2025': dict(
        authors='Pan, Z.; Wang, Y.; Liu, Z.',
        title='Over-education, job satisfaction, and intention to quit: Evidence from China',
        journal='Soc. Indic. Res.', year='2025', volume='176', pages='287–307'),
    'zheng2021': dict(
        authors='Zheng, Y.; Zhang, X.; Zhu, Y.',
        title='Overeducation, major mismatch, and return to higher education tiers: '
              'Evidence from novel data source of a major online recruitment platform '
              'in China',
        journal='China Econ. Rev.', year='2021', volume='66', pages='101584'),
    'li2014': dict(
        authors='Li, S.; Whalley, J.; Xing, C.',
        title='China’s higher education expansion and unemployment of college graduates',
        journal='China Econ. Rev.', year='2014', volume='30', pages='567–582'),
    'rikala2024': dict(
        authors='Rikala, P.; Braun, G.; Järvinen, M.; Stahre, J.; Hämäläinen, R.',
        title='Understanding and measuring skill gaps in Industry 4.0—A review',
        journal='Technol. Forecast. Soc. Change', year='2024', volume='201',
        pages='123206'),
    'zhao2023': dict(
        authors='Zhao, K.; Wu, Y.; Kuang, Z.',
        title='Dynamic evolution and impact mechanism of human capital mismatch in '
              'strategic emerging industries: Evidence from the Yangtze River Delta '
              'region of China',
        journal='Heliyon', year='2023', volume='9', pages='e21684'),
    'devos2020': dict(
        authors='De Vos, A.; Van der Heijden, B.I.J.M.; Akkermans, J.',
        title='Sustainable careers: Towards a conceptual model',
        journal='J. Vocat. Behav.', year='2020', volume='117', pages='103196'),
    'liang2024': dict(
        authors='Liang, F.; Liu, Y.',
        title='Sustainable youth employment quality management: The impact of '
              'robotization in China',
        journal='PLoS ONE', year='2024', volume='19', pages='e0298081'),

    # ------------------------------------------------ policy and regional context
    'caliendo2016': dict(
        authors='Caliendo, M.; Schmidl, R.',
        title='Youth unemployment and active labor market policies in Europe',
        journal='IZA J. Labor Policy', year='2016', volume='5', pages='1'),
    'reskill2024': dict(
        authors='Li, L.',
        title='Reskilling and upskilling the future-ready workforce for Industry 4.0 '
              'and beyond',
        journal='Inf. Syst. Front.', year='2024', volume='26', pages='1697–1712'),
    'zhoupolicy2024': dict(
        authors='Zhou, L.; Fan, J.; Ding, L.; Xu, Z.; Zhang, J.',
        title='Can policy advantages be transformed into industrial advantages? Evidences '
              'from digital economy industry development in Zhejiang Province, China',
        journal='PLoS ONE', year='2024', volume='19', pages='e0298138'),
    'tong2026': dict(
        authors='Tong, W.; Guo, J.; Lo, K.; Xu, W.',
        title='Bridging the gap to common prosperity: Rural development and urban–rural '
              'income disparities in Zhejiang Province, China',
        journal='Chin. Geogr. Sci.', year='2026', volume='36', pages='207–221'),
    'wangguan2024': dict(
        authors='Wang, H.; Wang, H.; Guan, R.',
        title='Digitalization of industries and labor mobility in China',
        journal='China Econ. Rev.', year='2024', volume='87', pages='102248'),
    'liu2024sus': dict(
        authors='Liu, J.; Fang, Y.; Xia, Y.; Zou, W.; Chan, K.-L.; Lam, J.F.I.; Chen, H.',
        title='Can the digital economy promote sustainable improvement in the quality of '
              'employment for Chinese residents?—Moderated mediating effect model',
        journal='Sustainability', year='2024', volume='16', pages='6071'),
    'wangzhang2025': dict(
        authors='Wang, S.; Zhang, H.',
        title='Digital transformation and innovation performance in small- and '
              'medium-sized enterprises: A systems perspective on the interplay of '
              'digital adoption, digital drive, and digital culture',
        journal='Systems', year='2025', volume='13', pages='43'),

    # ------------------------------------------------ official statistics (raw entries)
    'nbs2026': dict(
        authors='National Bureau of Statistics of China (NBS).', raw=True,
        full='National Bureau of Statistics of China (NBS). Surveyed Urban Unemployment '
             'Rate of the Population Aged 16–24 Excluding Students; NBS: Beijing, China, '
             '2026.',
        title='Surveyed urban unemployment rate', journal='NBS', year='2026'),
    'zjstats2026': dict(
        authors='Statistics Bureau of Zhejiang Province.', raw=True,
        full='Statistics Bureau of Zhejiang Province. Statistical Communiqué of Zhejiang '
             'Province on the 2025 National Economic and Social Development; Statistics '
             'Bureau of Zhejiang Province: Hangzhou, China, 2026.',
        title='Statistical Communiqué 2025', journal='Zhejiang', year='2026'),
    'moe2026': dict(
        authors='Ministry of Education of China.', raw=True,
        full='Ministry of Education of China. Notice on the Employment and '
             'Entrepreneurship of 2026 National College Graduates; Ministry of Education: '
             'Beijing, China, 2025.',
        title='Graduate employment notice', journal='MOE', year='2025'),
    'oecd2025': dict(
        authors='Organisation for Economic Co-operation and Development (OECD).', raw=True,
        full='Organisation for Economic Co-operation and Development (OECD). Education at '
             'a Glance 2025: OECD Indicators; OECD Publishing: Paris, France, 2025.',
        title='Education at a Glance 2025', journal='OECD', year='2025'),
}

REFS.update(NEW)
