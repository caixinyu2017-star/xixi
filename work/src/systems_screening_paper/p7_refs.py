# -*- coding: utf-8 -*-
"""Paper 7 references.

Carries forward the verified pools of papers 1/2/5/6 and adds the new
system-dynamics, generative-AI-and-work, apprenticeship, scarring and
sensitivity-analysis items collected for this manuscript (evidence in
refs_pool.json; `tier` field there records how many independent verification
rounds each item passed).

Entries with `raw=True` are books, reports and working papers, which MDPI
formats as free-form strings rather than as journal articles.
"""
from p6_refs import REFS6

REFS7 = dict(REFS6)

NEW7 = {
    # ------------------------------------------- generative AI and productivity
    'noy_zhang': dict(
        authors='Noy, S.; Zhang, W.',
        title='Experimental evidence on the productivity effects of generative artificial intelligence',
        journal='Science', year='2023', volume='381', pages='187–192'),
    'bly_genai_work': dict(
        authors='Brynjolfsson, E.; Li, D.; Raymond, L.',
        title='Generative AI at Work',
        journal='Q. J. Econ.', year='2025', volume='140', pages='889–942'),
    'jagged_frontier': dict(
        authors='Dell’Acqua, F.; McFowland, E., III; Mollick, E.R.; Lifshitz-Assaf, H.; '
                'Kellogg, K.C.; Rajendran, S.; Krayer, L.; Candelon, F.; Lakhani, K.R.',
        title='Navigating the Jagged Technological Frontier: Field Experimental Evidence of '
              'the Effects of Artificial Intelligence on Knowledge Worker Productivity and Quality',
        journal='Organ. Sci.', year='2026', volume='37', pages='403–423'),
    'copilot_rct': dict(
        raw=True, year='2023',
        full='Peng, S.; Kalliamvakou, E.; Cihon, P.; Demirer, M. The Impact of AI on Developer '
             'Productivity: Evidence from GitHub Copilot. arXiv 2023, arXiv:2302.06590.'),
    'eloundou_gpts': dict(
        authors='Eloundou, T.; Manning, S.; Mishkin, P.; Rock, D.',
        title='GPTs are GPTs: Labor market impact potential of LLMs',
        journal='Science', year='2024', volume='384', pages='1306–1308'),
    # ------------------------------------------- entry-level exposure evidence
    'canaries': dict(
        raw=True, year='2025',
        full='Brynjolfsson, E.; Chandar, B.; Chen, R. Canaries in the Coal Mine? Six Facts about '
             'the Recent Employment Effects of Artificial Intelligence; Working Paper; Stanford '
             'Digital Economy Lab: Stanford, CA, USA, 2025.'),
    'seniority_biased': dict(
        raw=True, year='2025',
        full='Hosseini Maasoum, S.M.; Lichtinger, G. Generative AI as Seniority-Biased '
             'Technological Change: Evidence from U.S. Résumé and Job Posting Data; SSRN Working '
             'Paper No. 5425555; Social Science Research Network: Rochester, NY, USA, 2025.'),
    'ide_intergen': dict(
        raw=True, year='2026',
        full='Ide, E. Automation, AI, and the Intergenerational Transmission of Knowledge; CEPR '
             'Discussion Paper; Centre for Economic Policy Research: London, UK, 2026.'),
    'ladder_eig': dict(
        raw=True, year='2026',
        full='Iscenko, Z.; Curto Millet, F. Looking for the Ladder: Is AI Impacting Entry-Level '
             'Jobs?; The American Worker Project; Economic Innovation Group: Washington, DC, USA, 2026.'),
    'acemoglu_race': dict(
        authors='Acemoglu, D.; Restrepo, P.',
        title='The Race between Man and Machine: Implications of Technology for Growth, Factor '
              'Shares, and Employment',
        journal='Am. Econ. Rev.', year='2018', volume='108', pages='1488–1542'),
    'albanesi_newtech': dict(
        authors='Albanesi, S.; Dias da Silva, A.; Jimeno, J.F.; Lamo, A.; Wabitsch, A.',
        title='New technologies and jobs in Europe',
        journal='Econ. Policy', year='2025', volume='40', pages='71–139'),
    # ------------------------------------------------------- system dynamics
    'forrester61': dict(
        raw=True, year='1961',
        full='Forrester, J.W. Industrial Dynamics; MIT Press: Cambridge, MA, USA, 1961.'),
    'sterman00': dict(
        raw=True, year='2000',
        full='Sterman, J.D. Business Dynamics: Systems Thinking and Modeling for a Complex '
             'World; Irwin/McGraw-Hill: Boston, MA, USA, 2000.'),
    'barlas96': dict(
        authors='Barlas, Y.',
        title='Formal aspects of model validity and validation in system dynamics',
        journal='Syst. Dyn. Rev.', year='1996', volume='12', pages='183–210'),
    'sterman02_models': dict(
        authors='Sterman, J.D.',
        title='All models are wrong: reflections on becoming a systems scientist',
        journal='Syst. Dyn. Rev.', year='2002', volume='18', pages='501–531'),
    'capability_traps': dict(
        authors='Repenning, N.P.; Sterman, J.D.',
        title='Capability Traps and Self-Confirming Attribution Errors in the Dynamics of '
              'Process Improvement',
        journal='Adm. Sci. Q.', year='2002', volume='47', pages='265–295'),
    'nobody_credit': dict(
        authors='Repenning, N.P.; Sterman, J.D.',
        title='Nobody Ever Gets Credit for Fixing Problems That Never Happened: Creating and '
              'Sustaining Process Improvement',
        journal='Calif. Manag. Rev.', year='2001', volume='43', pages='64–88'),
    'capability_erosion': dict(
        authors='Rahmandad, H.; Repenning, N.',
        title='Capability Erosion Dynamics',
        journal='Strateg. Manag. J.', year='2016', volume='37', pages='649–672'),
    'leverage_points': dict(
        raw=True, year='1999',
        full='Meadows, D.H. Leverage Points: Places to Intervene in a System; The Sustainability '
             'Institute: Hartland, VT, USA, 1999.'),
    'thinking_systems': dict(
        raw=True, year='2008',
        full='Meadows, D.H. Thinking in Systems: A Primer; Chelsea Green Publishing: White River '
             'Junction, VT, USA, 2008.'),
    'small_models': dict(
        authors='Ghaffarzadegan, N.; Lyneis, J.; Richardson, G.P.',
        title='How small system dynamics models can help the public policy process',
        journal='Syst. Dyn. Rev.', year='2011', volume='27', pages='22–44'),
    'workforce_multimethod': dict(
        authors='Willis, G.; Cave, S.; Kunc, M.',
        title='Strategic workforce planning in healthcare: A multi-methodology approach',
        journal='Eur. J. Oper. Res.', year='2018', volume='267', pages='250–263'),
    'thailand_sd': dict(
        authors='Leerapan, B.; Teekasap, P.; Urwannachotima, N.; Jaichuen, W.; '
                'Chiangchaisakulthai, K.; Udomaksorn, K.; Meeyai, A.; Noree, T.; Sawaengdee, K.',
        title='System dynamics modelling of health workforce planning to address future '
              'challenges of Thailand’s Universal Health Coverage',
        journal='Hum. Resour. Health', year='2021', volume='19', pages='31'),
    'ireland_nursing_sd': dict(
        authors='Hynes, T.; Caulfield, P.; O’Connor, P.; Cullinan, J.',
        title='Self-sufficiency in the healthcare workforce: a system dynamics model of the '
              'domestic and foreign educated nursing and midwifery workforce in Ireland',
        journal='Hum. Resour. Health', year='2025', volume='23', pages='44'),
    'construction_retention_sd': dict(
        authors='Elbashbishy, T.; El-adaway, I.H.',
        title='System Dynamic Modeling to Study the Impact of Construction Industry '
              'Characteristics and Associated Macroeconomic Indicators on Workforce Size and '
              'Labor Retention Rate',
        journal='J. Constr. Eng. Manag.', year='2023', volume='149', pages='04023100'),
    # ------------------------------------------------ learning and expertise
    'arrow62': dict(
        authors='Arrow, K.J.',
        title='The Economic Implications of Learning by Doing',
        journal='Rev. Econ. Stud.', year='1962', volume='29', pages='155–173'),
    'ericsson93': dict(
        authors='Ericsson, K.A.; Krampe, R.T.; Tesch-Römer, C.',
        title='The Role of Deliberate Practice in the Acquisition of Expert Performance',
        journal='Psychol. Rev.', year='1993', volume='100', pages='363–406'),
    'learning_coworkers': dict(
        authors='Jarosch, G.; Oberfield, E.; Rossi-Hansberg, E.',
        title='Learning From Coworkers',
        journal='Econometrica', year='2021', volume='89', pages='647–676'),
    'proximity': dict(
        authors='Emanuel, N.; Harrington, E.; Pallais, A.',
        title='The Power of Proximity to Coworkers',
        journal='Q. J. Econ.', year='2026', volume='141', pages='1825–1870'),
    'people_mgmt': dict(
        authors='Hoffman, M.; Tadelis, S.',
        title='People Management Skills, Employee Attrition, and Manager Rewards: An Empirical '
              'Analysis',
        journal='J. Polit. Econ.', year='2021', volume='129', pages='243–285'),
    'managers_productivity': dict(
        authors='Fenizia, A.',
        title='Managers and Productivity in the Public Sector',
        journal='Econometrica', year='2022', volume='90', pages='1063–1084'),
    # ----------------------------------------------- apprenticeship economics
    'appr_roi': dict(
        authors='Muehlemann, S.; Wolter, S.C.',
        title='Return on investment of apprenticeship systems for enterprises: Evidence from '
              'cost-benefit analyses',
        journal='IZA J. Labor Policy', year='2014', volume='3', pages='25'),
    'appr_cycle': dict(
        authors='Muehlemann, S.; Pfeifer, H.; Wittek, B.H.',
        title='The effect of business cycle expectations on the German apprenticeship market: '
              'Estimating the impact of Covid-19',
        journal='Empir. Res. Vocat. Educ. Train.', year='2020', volume='12', pages='8'),
    'appr_costs': dict(
        authors='Schuss, E.',
        title='Beyond windfall gains: The redistribution of apprenticeship costs and vocational '
              'education of care workers',
        journal='Economica', year='2023', volume='90', pages='978–1002'),
    # ----------------------------------------------------- scarring and youth
    'vonwachter20': dict(
        authors='von Wachter, T.',
        title='The Persistent Effects of Initial Labor Market Conditions for Young Adults and '
              'Their Sources',
        journal='J. Econ. Perspect.', year='2020', volume='34', pages='168–194'),
    'scars_youth': dict(
        authors='Schmillen, A.; Umkehrer, M.',
        title='The Scars of Youth: Effects of Early-Career Unemployment on Future Unemployment '
              'Experience',
        journal='Int. Labour Rev.', year='2017', volume='156', pages='465–494'),
    'lost_generation': dict(
        authors='Rothstein, J.',
        title='The Lost Generation? Labor Market Outcomes for Post-Great Recession Entrants',
        journal='J. Hum. Resour.', year='2023', volume='58', pages='1452–1479'),
    'scarring_meta': dict(
        authors='Filomena, M.',
        title='Unemployment Scarring Effects: An Overview and Meta-Analysis of Empirical Studies',
        journal='Ital. Econ. J.', year='2024', volume='10', pages='459–518'),
    'ilo_get2024': dict(
        raw=True, year='2024',
        full='International Labour Organization. Global Employment Trends for Youth 2024: Decent '
             'Work, Brighter Futures; International Labour Office: Geneva, Switzerland, 2024.'),
    'oecd_eo2025': dict(
        raw=True, year='2025',
        full='OECD. OECD Employment Outlook 2025: Can We Get Through the Demographic Crunch?; '
             'OECD Publishing: Paris, France, 2025.'),
    'neet_cee': dict(
        authors='Karma, E.',
        title='NEET youth in central and eastern European countries: a panel model approach',
        journal='J. Youth Stud.', year='2025', volume='28', pages='1458–1475'),
    # ------------------------------------------------ deskilling and reliance
    'deskilling_endoscopy': dict(
        authors='Budzyń, K.; Romańczyk, M.; Kitala, D.; Kołodziej, P.; Bugajski, M.; '
                'Adami, H.-O.; Blom, J.; Buszkiewicz, M.; Halvorsen, N.G.; Hassan, C.; et al.',
        title='Endoscopist deskilling risk after exposure to artificial intelligence in '
              'colonoscopy: a multicentre, observational study',
        journal='Lancet Gastroenterol. Hepatol.', year='2025', volume='10', pages='896–903'),
    'overreliance': dict(
        authors='Klingbeil, A.; Grützner, C.; Schreck, P.',
        title='Trust and reliance on AI—An experimental study on the extent and costs of '
              'overreliance on AI',
        journal='Comput. Hum. Behav.', year='2024', volume='160', pages='108352'),
    'human_ai_meta': dict(
        authors='Vaccaro, M.; Almaatouq, A.; Malone, T.',
        title='When combinations of humans and AI are useful: A systematic review and '
              'meta-analysis',
        journal='Nat. Hum. Behav.', year='2024', volume='8', pages='2293–2303'),
    'ai_aversion_meta': dict(
        authors='Qin, X.; Zhou, X.; Chen, C.; Wu, D.; Zhou, H.; Dong, X.; Cao, L.; Lu, J.G.',
        title='AI Aversion or Appreciation? A Capability–Personalization Framework and a '
              'Meta-Analytic Review',
        journal='Psychol. Bull.', year='2025', volume='151', pages='580–599'),
    'delegation': dict(
        authors='Fügener, A.; Grahl, J.; Gupta, A.; Ketter, W.',
        title='Cognitive Challenges in Human–Artificial Intelligence Collaboration: '
              'Investigating the Path Toward Productive Delegation',
        journal='Inf. Syst. Res.', year='2022', volume='33', pages='678–696'),
    # ------------------------------------------------------ method references
    'lhs': dict(
        authors='McKay, M.D.; Beckman, R.J.; Conover, W.J.',
        title='A Comparison of Three Methods for Selecting Values of Input Variables in the '
              'Analysis of Output from a Computer Code',
        journal='Technometrics', year='1979', volume='21', pages='239–245'),
    'saltelli10': dict(
        authors='Saltelli, A.; Annoni, P.; Azzini, I.; Campolongo, F.; Ratto, M.; Tarantola, S.',
        title='Variance based sensitivity analysis of model output. Design and estimator for the '
              'total sensitivity index',
        journal='Comput. Phys. Commun.', year='2010', volume='181', pages='259–270'),
    'razavi21': dict(
        authors='Razavi, S.; Jakeman, A.; Saltelli, A.; Prieur, C.; Iooss, B.; Borgonovo, E.; '
                'Plischke, E.; Lo Piano, S.; Iwanaga, T.; Becker, W.; et al.',
        title='The Future of Sensitivity Analysis: An Essential Discipline for Systems Modeling '
              'and Policy Support',
        journal='Environ. Model. Softw.', year='2021', volume='137', pages='104954'),
}

REFS7.update(NEW7)
