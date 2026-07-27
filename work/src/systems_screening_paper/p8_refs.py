# -*- coding: utf-8 -*-
"""Paper 8 references.

New items were found and double-verified by web search (two independent
passes each, confirming author list, year and venue). Entries with raw=True
are books, reports, conference papers and working papers, which MDPI formats
as free-form strings rather than as journal articles.
"""
from p7_refs import REFS7

REFS8 = dict(REFS7)

NEW8 = {
    # ------------------------- generative AI in recruitment and selection
    'writing_assist': dict(
        authors='van Inwegen, E.; Munyikwa, Z.; Horton, J.J.',
        title='Algorithmic Writing Assistance on Jobseekers’ Resumes Increases Hires',
        journal='Manag. Sci.', year='2025', volume='71', pages='10144–10164'),
    'voice_ai_interviews': dict(
        raw=True, year='2025',
        full='Jabarian, B.; Henkel, L. Voice AI in Firms: A Natural Field Experiment on '
             'Automated Job Interviews; SSRN Working Paper No. 5395709; Social Science '
             'Research Network: Rochester, NY, USA, 2025.'),
    'async_ai_assessment': dict(
        raw=True, year='2026',
        full='Avery, M.; Ip, E.; Leibbrandt, A.; Vecci, J. A Brave New World of Hiring: '
             'A Natural Field Experiment on How Asynchronous Interviews and AI Assessment '
             'Reshape Recruitment; CESifo Working Paper No. 12573; CESifo: Munich, '
             'Germany, 2026.'),
    'ai_assisted_recruit': dict(
        raw=True, year='2025',
        full='Aka, A.; Palikot, E.; Ansari, A.; Yazdani, N. Better Together: Quantifying '
             'the Benefits of AI-Assisted Recruitment. arXiv 2025, arXiv:2507.08029.'),
    'hrm_structuration': dict(
        authors='Dutta, D.; Naveen, P.M.',
        title='Transforming Recruitment and Selection Practices in Organizations Through '
              'Discriminative and Generative AI Adoption: A Structuration Lens',
        journal='Hum. Resour. Manag.', year='2026', volume='65', pages='77–115'),
    'applicant_ai_use': dict(
        authors='Robie, C.; Wingate, T.G.; Baytalskaya, N.; Butera, H.',
        title='Candidate Generative AI Use in Pre-Hire Employment Assessments: '
              'Self-Reported Incidence and the Impact of Warnings',
        journal='Int. J. Sel. Assess.', year='2026', volume='34', pages='e70056'),

    # ------------------------------- generative AI and entry-level workers
    'canaries': dict(
        raw=True, year='2025',
        full='Brynjolfsson, E.; Chandar, B.; Chen, R. Canaries in the Coal Mine? Six '
             'Facts about the Recent Employment Effects of Artificial Intelligence; '
             'Working Paper; Stanford Digital Economy Lab: Stanford, CA, USA, 2025.'),
    'seniority_biased': dict(
        raw=True, year='2025',
        full='Hosseini Maasoum, S.M.; Lichtinger, G. Generative AI as Seniority-Biased '
             'Technological Change: Evidence from U.S. Résumé and Job Posting Data; SSRN '
             'Working Paper No. 5425555; Social Science Research Network: Rochester, NY, '
             'USA, 2025.'),
    'still_waters': dict(
        raw=True, year='2025',
        full='Humlum, A.; Vestergaard, E. Still Waters, Rapid Currents: Early Labor Market '
             'Transformation under Generative AI; NBER Working Paper No. 33777; National '
             'Bureau of Economic Research: Cambridge, MA, USA, 2025.'),
    'who_is_ai_replacing': dict(
        authors='Demirci, O.; Hannane, J.; Zhu, X.',
        title='Who Is AI Replacing? The Impact of Generative AI on Online Freelancing '
              'Platforms',
        journal='Manag. Sci.', year='2025', volume='71', pages='8097–8108'),

    # --------------------------------------- signalling and employer learning
    'spence73': dict(
        authors='Spence, M.',
        title='Job Market Signaling',
        journal='Q. J. Econ.', year='1973', volume='87', pages='355–374'),
    'altonji_pierret': dict(
        authors='Altonji, J.G.; Pierret, C.R.',
        title='Employer Learning and Statistical Discrimination',
        journal='Q. J. Econ.', year='2001', volume='116', pages='313–350'),
    'cover_letters_ai': dict(
        raw=True, year='2025',
        full='Cui, J.; Dias, G.; Ye, J. Signaling in the Age of AI: Evidence from Cover '
             'Letters. arXiv 2025, arXiv:2509.25054.'),
    'making_talk_cheap': dict(
        raw=True, year='2025',
        full='Galdin, A.; Silbert, J. Making Talk Cheap: Generative AI and Labor Market '
             'Signaling. arXiv 2025, arXiv:2511.08785.'),

    # --------------------------- algorithmic hiring, fairness, adverse impact
    'hiring_exploration': dict(
        authors='Li, D.; Raymond, L.R.; Bergman, P.',
        title='Hiring as Exploration',
        journal='Rev. Econ. Stud.', year='2026', volume='93', pages='1200–1240'),
    'discretion_hiring': dict(
        authors='Hoffman, M.; Kahn, L.B.; Li, D.',
        title='Discretion in Hiring',
        journal='Q. J. Econ.', year='2018', volume='133', pages='765–800'),
    'resume_lm_bias': dict(
        raw=True, year='2024',
        full='Wilson, K.; Caliskan, A. Gender, Race, and Intersectional Bias in Resume '
             'Screening via Language Model Retrieval. In Proceedings of the AAAI/ACM '
             'Conference on AI, Ethics, and Society (AIES), San Jose, CA, USA, 21–23 '
             'October 2024; Volume 7, pp. 1578–1590.'),
    'ai_self_preferencing': dict(
        raw=True, year='2025',
        full='Xu, J.; Li, G.; Jiang, J.Y. AI Self-preferencing in Algorithmic Hiring: '
             'Empirical Evidence and Insights. In Proceedings of the 5th ACM Conference '
             'on Equity and Access in Algorithms, Mechanisms, and Optimization (EAAMO ’25), '
             'Pittsburgh, PA, USA, 3–5 November 2025.'),
    'systemic_discrimination': dict(
        authors='Kline, P.; Rose, E.K.; Walters, C.R.',
        title='Systemic Discrimination Among Large U.S. Employers',
        journal='Q. J. Econ.', year='2022', volume='137', pages='1963–2036'),
    'attention_discrimination': dict(
        authors='Bartoš, V.; Bauer, M.; Chytilová, J.; Matějka, F.',
        title='Attention Discrimination: Theory and Field Experiments with Monitoring '
              'Information Acquisition',
        journal='Am. Econ. Rev.', year='2016', volume='106', pages='1437–1475'),

    # ------------------------------- credentials, referrals, elite signals
    'cultural_matching': dict(
        authors='Rivera, L.A.',
        title='Hiring as Cultural Matching: The Case of Elite Professional Service Firms',
        journal='Am. Sociol. Rev.', year='2012', volume='77', pages='999–1022'),
    'class_advantage': dict(
        authors='Rivera, L.A.; Tilcsik, A.',
        title='Class Advantage, Commitment Penalty: The Gendered Effect of Social Class '
              'Signals in an Elite Labor Market',
        journal='Am. Sociol. Rev.', year='2016', volume='81', pages='1097–1131'),
    'referral_value': dict(
        authors='Burks, S.V.; Cowgill, B.; Hoffman, M.; Housman, M.',
        title='The Value of Hiring through Employee Referrals',
        journal='Q. J. Econ.', year='2015', volume='130', pages='805–839'),
    'ivy_plus': dict(
        raw=True, year='2023',
        full='Chetty, R.; Deming, D.J.; Friedman, J.N. Diversifying Society’s Leaders? '
             'The Determinants and Causal Effects of Admission to Highly Selective Private '
             'Colleges; NBER Working Paper No. 31492; National Bureau of Economic '
             'Research: Cambridge, MA, USA, 2023.'),

    # -------------------------------- verified assessment and skills signals
    'inefficient_entry': dict(
        authors='Pallais, A.',
        title='Inefficient Hiring in Entry-Level Labor Markets',
        journal='Am. Econ. Rev.', year='2014', volume='104', pages='3565–3599'),
    'limited_information': dict(
        authors='Carranza, E.; Garlick, R.; Orkin, K.; Rankin, N.',
        title='Job Search and Hiring with Limited Information about Workseekers’ Skills',
        journal='Am. Econ. Rev.', year='2022', volume='112', pages='3547–3583'),
    'reference_letters': dict(
        authors='Abel, M.; Burger, R.; Piraino, P.',
        title='The Value of Reference Letters: Experimental Evidence from South Africa',
        journal='Am. Econ. J. Appl. Econ.', year='2020', volume='12', pages='40–71'),
    'skill_requirements': dict(
        authors='Deming, D.J.; Kahn, L.B.',
        title='Skill Requirements across Firms and Labor Markets: Evidence from Job '
              'Postings for Professionals',
        journal='J. Labor Econ.', year='2018', volume='36', pages='S337–S369'),
}

REFS8.update(NEW8)

# ---------------------------------------------------------------------------
# Methods, precedents and context (second verification round)
# ---------------------------------------------------------------------------
METHODS8 = {
    # ------------------------------------------- choice modelling methodology
    'train09': dict(
        raw=True, year='2009',
        full='Train, K.E. Discrete Choice Methods with Simulation, 2nd ed.; Cambridge '
             'University Press: Cambridge, UK, 2009.'),
    'hensher15': dict(
        raw=True, year='2015',
        full='Hensher, D.A.; Rose, J.M.; Greene, W.H. Applied Choice Analysis, 2nd ed.; '
             'Cambridge University Press: Cambridge, UK, 2015.'),
    'mcfadden_train': dict(
        authors='McFadden, D.; Train, K.',
        title='Mixed MNL models for discrete response',
        journal='J. Appl. Econom.', year='2000', volume='15', pages='447–470'),
    'rose_bliemer': dict(
        authors='Rose, J.M.; Bliemer, M.C.J.',
        title='Constructing Efficient Stated Choice Experimental Designs',
        journal='Transp. Rev.', year='2009', volume='29', pages='587–617'),
    'train_weeks': dict(
        raw=True, year='2005',
        full='Train, K.; Weeks, M. Discrete Choice Models in Preference Space and '
             'Willingness-to-Pay Space. In Applications of Simulation Methods in '
             'Environmental and Resource Economics; Alberini, A., Scarpa, R., Eds.; '
             'Springer: Dordrecht, The Netherlands, 2005; pp. 1–17.'),
    'ispor_design': dict(
        authors='Johnson, F.R.; Lancsar, E.; Marshall, D.; Kilambi, V.; Mühlbacher, A.; '
                'Regier, D.A.; Bresnahan, B.W.; Kanninen, B.; Bridges, J.F.P.',
        title='Constructing experimental designs for discrete-choice experiments: report '
              'of the ISPOR Conjoint Analysis Experimental Design Good Research Practices '
              'Task Force',
        journal='Value Health', year='2013', volume='16', pages='3–13'),
    'ispor_analysis': dict(
        authors='Hauber, A.B.; González, J.M.; Groothuis-Oudshoorn, C.G.M.; Prior, T.; '
                'Marshall, D.A.; Cunningham, C.; IJzerman, M.J.; Bridges, J.F.P.',
        title='Statistical Methods for the Analysis of Discrete Choice Experiments: A '
              'Report of the ISPOR Conjoint Analysis Good Research Practices Task Force',
        journal='Value Health', year='2016', volume='19', pages='300–315'),
    'greene_hensher': dict(
        authors='Greene, W.H.; Hensher, D.A.',
        title='A latent class model for discrete choice analysis: contrasts with mixed '
              'logit',
        journal='Transp. Res. Part B Methodol.', year='2003', volume='37', pages='681–698'),
    'nylund07': dict(
        authors='Nylund, K.L.; Asparouhov, T.; Muthén, B.O.',
        title='Deciding on the Number of Classes in Latent Class Analysis and Growth '
              'Mixture Modeling: A Monte Carlo Simulation Study',
        journal='Struct. Equ. Model.', year='2007', volume='14', pages='535–569'),

    # ----------------------------- conjoint and vignette designs in social science
    'hainmueller14': dict(
        authors='Hainmueller, J.; Hopkins, D.J.; Yamamoto, T.',
        title='Causal Inference in Conjoint Analysis: Understanding Multidimensional '
              'Choices via Stated Preference Experiments',
        journal='Political Anal.', year='2014', volume='22', pages='1–30'),
    'bansak18': dict(
        authors='Bansak, K.; Hainmueller, J.; Hopkins, D.J.; Yamamoto, T.',
        title='The Number of Choice Tasks and Survey Satisficing in Conjoint Experiments',
        journal='Political Anal.', year='2018', volume='26', pages='112–119'),
    'auspurg_hinz': dict(
        raw=True, year='2015',
        full='Auspurg, K.; Hinz, T. Factorial Survey Experiments; Quantitative '
             'Applications in the Social Sciences, Vol. 175; SAGE: Thousand Oaks, CA, '
             'USA, 2015.'),
    'irr': dict(
        authors='Kessler, J.B.; Low, C.; Sullivan, C.D.',
        title='Incentivized Resume Rating: Eliciting Employer Preferences without '
              'Deception',
        journal='Am. Econ. Rev.', year='2019', volume='109', pages='3713–3744'),
    'quillian17': dict(
        authors='Quillian, L.; Pager, D.; Hexel, O.; Midtbøen, A.H.',
        title='Meta-analysis of field experiments shows no change in racial '
              'discrimination in hiring over time',
        journal='Proc. Natl. Acad. Sci. USA', year='2017', volume='114', pages='10870–10875'),
    'lippens23': dict(
        authors='Lippens, L.; Vermeiren, S.; Baert, S.',
        title='The state of hiring discrimination: A meta-analysis of (almost) all recent '
              'correspondence experiments',
        journal='Eur. Econ. Rev.', year='2023', volume='151', pages='104315'),
    'forster24': dict(
        authors='Forster, A.G.; Neugebauer, M.',
        title='Factorial Survey Experiments to Predict Real-World Behavior: A Cautionary '
              'Tale from Hiring Studies',
        journal='Sociol. Sci.', year='2024', volume='11', pages='886–906'),
    'gutfleisch21': dict(
        authors='Gutfleisch, T.; Samuel, R.; Sacchi, S.',
        title='The application of factorial surveys to study recruiters’ hiring '
              'intentions: comparing designs based on hypothetical and real vacancies',
        journal='Qual. Quant.', year='2021', volume='55', pages='775–804'),
    'cbc_graduates': dict(
        authors='Maer Matei, M.M.; Zamfir, A.-M.; Mocanu, C.',
        title='Criteria Weights in Hiring Decisions—A Conjoint Approach',
        journal='Mathematics', year='2023', volume='11', pages='728'),
    'cbc_recruiters': dict(
        authors='Oberst, U.; De Quintana, M.; Del Cerro, S.; Chamarro, A.',
        title='Recruiters prefer expert recommendations over digital hiring algorithm: a '
              'choice-based conjoint study in a pre-employment screening scenario',
        journal='Manag. Res. Rev.', year='2021', volume='44', pages='625–641'),

    # ---------------------------------------------- youth entry and scarring
    'first_job_firm': dict(
        authors='Arellano-Bover, J.',
        title='Career Consequences of Firm Heterogeneity for Young Workers: First Job and '
              'Firm Size',
        journal='J. Labor Econ.', year='2024', volume='42', pages='549–589'),
    'scarring_synthesis': dict(
        authors='Tomlinson, M.; Tholen, G.',
        title='Scarring effects for young people in challenging economic times: a '
              'conceptual synthesis and future policy and research agenda',
        journal='Labour Ind.', year='2023', volume='33', pages='308–325'),

    # ------------------------------ digital transformation and digital leadership
    'hanelt21': dict(
        authors='Hanelt, A.; Bohnsack, R.; Marz, D.; Antunes Marante, C.',
        title='A Systematic Review of the Literature on Digital Transformation: Insights '
              'and Implications for Strategy and Organizational Change',
        journal='J. Manag. Stud.', year='2021', volume='58', pages='1159–1197'),
    'braojos24': dict(
        authors='Braojos, J.; Weritz, P.; Matute, J.',
        title='Empowering organisational commitment through digital transformation '
              'capabilities: The role of digital leadership and a continuous learning '
              'environment',
        journal='Inf. Syst. J.', year='2024', volume='34', pages='1466–1492'),

    # ------------------------------------- survey methodology and data quality
    'key_informants': dict(
        authors='Kumar, N.; Stern, L.W.; Anderson, J.C.',
        title='Conducting Interorganizational Research Using Key Informants',
        journal='Acad. Manag. J.', year='1993', volume='36', pages='1633–1651'),
    'panel_quality': dict(
        authors='Peer, E.; Rothschild, D.; Gordon, A.; Evernden, Z.; Damer, E.',
        title='Data quality of platforms and panels for online behavioral research',
        journal='Behav. Res. Methods', year='2022', volume='54', pages='1643–1662'),
    'attention_checks': dict(
        authors='Berinsky, A.J.; Margolis, M.F.; Sances, M.W.',
        title='Separating the Shirkers from the Workers? Making Sure Respondents Pay '
              'Attention on Self-Administered Surveys',
        journal='Am. J. Political Sci.', year='2014', volume='58', pages='739–753'),
}

REFS8.update(METHODS8)
