# -*- coding: utf-8 -*-
"""Paper 9 reference pool.

Built on the pool carried forward from the earlier manuscripts, which is already
verified, plus the items this paper needs: the cobweb and heterogeneous-expectations
literature, field-of-study choice, the technology shock, and the systems apparatus.

Every entry was returned by a literature search rather than recalled.  Where the
verification was weaker than usual the entry carries a note in this file, and those
items are used only where an alternative would not do.
"""
from p8_refs import REFS8

# ------------------------------------------------------- cobweb and expectations
NEW9 = {
    'brock_hommes97': dict(
        authors='Brock, W.A.; Hommes, C.H.',
        title='A Rational Route to Randomness',
        journal='Econometrica', year='1997', volume='65', pages='1059–1095'),
    'brock_hommes98': dict(
        authors='Brock, W.A.; Hommes, C.H.',
        title='Heterogeneous Beliefs and Routes to Chaos in a Simple Asset Pricing Model',
        journal='J. Econ. Dyn. Control', year='1998', volume='22', pages='1235–1274'),
    'hommes_book': dict(
        raw=True, year='2013',
        full='Hommes, C.H. Behavioral Rationality and Heterogeneous Expectations in '
             'Complex Economic Systems; Cambridge University Press: Cambridge, UK, 2013.'),
    'hommes_jel': dict(
        authors='Hommes, C.H.',
        title='Behavioral and Experimental Macroeconomics and Policy Analysis: A Complex '
              'Systems Approach',
        journal='J. Econ. Lit.', year='2021', volume='59', pages='149–219'),
    'hommes_lab': dict(
        authors='Hommes, C.H.',
        title='The Heterogeneous Expectations Hypothesis: Some Evidence from the Lab',
        journal='J. Econ. Dyn. Control', year='2011', volume='35', pages='1–24'),
    'hommes_delays': dict(
        authors='Hommes, C.H.; Li, K.; Wagener, F.',
        title='Production Delays and Price Dynamics',
        journal='J. Econ. Behav. Organ.', year='2022', volume='194', pages='341–362'),
    'dieci_delays': dict(
        authors='Dieci, R.; Mignot, S.; Westerhoff, F.',
        title='Production Delays, Technology Choice and Cyclical Cobweb Dynamics',
        journal='Chaos Solitons Fractals', year='2022', volume='156', pages='111796'),
    'gardini_cobweb': dict(
        authors='Gardini, L.; Radi, D.; Schmitt, N.; Sushko, I.; Westerhoff, F.',
        title='Bifurcation Structures of a Two-Dimensional Piecewise Linear Discontinuous '
              'Map: Analysis of a Cobweb Model with Regime-Switching Expectations',
        journal='Nonlinear Dyn.', year='2024', volume='112', pages='15601–15624'),
    'berardi_cobweb': dict(
        authors='Berardi, M.',
        title='Beliefs Asymmetry and Price Stability in a Cobweb Model',
        journal='J. Econ. Behav. Organ.', year='2022', volume='203', pages='401–415'),
    'kukacka': dict(
        authors='Kukacka, J.; Sacht, S.',
        title='Estimation of Heuristic Switching in Behavioral Macroeconomic Models',
        journal='J. Econ. Dyn. Control', year='2023', volume='146', pages='104585'),
    'gusella': dict(
        authors='Gusella, F.; Ricchiuti, G.',
        title='Endogenous Cycles in Heterogeneous Agent Models: A State-Space Approach',
        journal='J. Evol. Econ.', year='2024', volume='34', pages='739–782'),
    'boehl_hommes': dict(
        authors='Boehl, G.; Hommes, C.H.',
        title='Rational vs. Irrational Beliefs in a Complex World',
        journal='J. Econ. Behav. Organ.', year='2025', volume='232', pages='106898'),
    'difrancesco': dict(
        authors='Di Francesco, T.; Hommes, C.H.',
        title='Sentiment-Driven Speculation in Financial Markets with Heterogeneous '
              'Beliefs: A Machine Learning Approach',
        journal='J. Econ. Dyn. Control', year='2025', volume='175', pages='105077'),
    'evans_ltf': dict(
        authors='Evans, G.W.; Gibbs, C.G.; McGough, B.',
        title='A Unified Model of Learning to Forecast',
        journal='Am. Econ. J. Macroecon.', year='2025', volume='17', pages='101–133'),
    'moll_re': dict(
        authors='Moll, B.',
        title='The Trouble with Rational Expectations in Heterogeneous Agent Models: A '
              'Challenge for Macroeconomics',
        journal='Econ. J.', year='2025', volume='135', pages='ueaf104'),
    'poitras': dict(
        authors='Poitras, G.',
        title='Cobweb Theory, Market Stability, and Price Expectations',
        journal='J. Hist. Econ. Thought', year='2023', volume='45', pages='137–161'),
    'ezekiel': dict(
        authors='Ezekiel, M.',
        title='The Cobweb Theorem',
        journal='Q. J. Econ.', year='1938', volume='52', pages='255–280'),
    'kaldor34': dict(
        authors='Kaldor, N.',
        title='A Classificatory Note on the Determinateness of Equilibrium',
        journal='Rev. Econ. Stud.', year='1934', volume='1', pages='122–136'),
    'nerlove': dict(
        authors='Nerlove, M.',
        title='Adaptive Expectations and Cobweb Phenomena',
        journal='Q. J. Econ.', year='1958', volume='72', pages='227–240'),

    # --------------------------------------------- field of study and its lag
    'freeman76': dict(
        authors='Freeman, R.B.',
        title='A Cobweb Model of the Supply and Starting Salary of New Engineers',
        journal='Ind. Labor Relat. Rev.', year='1976', volume='29', pages='236–248'),
    'freeman75': dict(
        authors='Freeman, R.B.',
        title='Overinvestment in College Training?',
        journal='J. Hum. Resour.', year='1975', volume='10', pages='287–311'),
    'ryoo_rosen': dict(
        authors='Ryoo, J.; Rosen, S.',
        title='The Engineering Labor Market',
        journal='J. Political Econ.', year='2004', volume='112', pages='S110–S140'),
    'long_majors': dict(
        authors='Long, M.C.; Goldhaber, D.; Huntington-Klein, N.',
        title='Do Completed College Majors Respond to Changes in Wages?',
        journal='Econ. Educ. Rev.', year='2015', volume='49', pages='1–14'),
    'beffy': dict(
        authors='Beffy, M.; Fougère, D.; Maurel, A.',
        title='Choosing the Field of Study in Postsecondary Education: Do Expected '
              'Earnings Matter?',
        journal='Rev. Econ. Stat.', year='2012', volume='94', pages='334–347'),
    'blom_cycle': dict(
        authors='Blom, E.; Cadena, B.C.; Keys, B.J.',
        title='Investment over the Business Cycle: Insights from College Major Choice',
        journal='J. Labor Econ.', year='2021', volume='39', pages='1043–1082'),
    'wiswall_zafar': dict(
        authors='Wiswall, M.; Zafar, B.',
        title='Determinants of College Major Choice: Identification Using an Information '
              'Experiment',
        journal='Rev. Econ. Stud.', year='2015', volume='82', pages='791–824'),
    'arcidiacono': dict(
        authors='Arcidiacono, P.',
        title='Ability Sorting and the Returns to College Major',
        journal='J. Econom.', year='2004', volume='121', pages='343–375'),
    'kirkeboen': dict(
        authors='Kirkebøen, L.J.; Leuven, E.; Mogstad, M.',
        title='Field of Study, Earnings, and Self-Selection',
        journal='Q. J. Econ.', year='2016', volume='131', pages='1057–1111'),
    'deming_noray': dict(
        authors='Deming, D.J.; Noray, K.',
        title='Earnings Dynamics, Changing Job Skills, and STEM Careers',
        journal='Q. J. Econ.', year='2020', volume='135', pages='1965–2005'),
    'altonji_cashier': dict(
        authors='Altonji, J.G.; Kahn, L.B.; Speer, J.D.',
        title='Cashier or Consultant? Entry Labor Market Conditions, Field of Study, and '
              'Career Success',
        journal='J. Labor Econ.', year='2016', volume='34', pages='S361–S401'),
    'bleemer': dict(
        authors='Bleemer, Z.; Mehta, A.',
        title='Will Studying Economics Make You Rich? A Regression Discontinuity Analysis '
              'of the Returns to College Major',
        journal='Am. Econ. J. Appl. Econ.', year='2022', volume='14', pages='1–22'),
    'speer_stem': dict(
        authors='Speer, J.D.',
        title='Bye Bye Ms. American Sci: Women and the Leaky STEM Pipeline',
        journal='Econ. Educ. Rev.', year='2023', volume='93', pages='102371'),
    'blume_kohout': dict(
        authors='Blume-Kohout, M.E.; Clack, J.W.',
        title='Are Graduate Students Rational? Evidence from the Market for Biomedical '
              'Scientists',
        journal='PLoS ONE', year='2013', volume='8', pages='e82759'),
    'conlon_major': dict(
        authors='Conlon, J.J.',
        title='Major Malfunction: A Field Experiment Correcting Undergraduates’ Beliefs '
              'about Salaries',
        journal='J. Hum. Resour.', year='2021', volume='56', pages='922–939'),
    'haaland': dict(
        authors='Haaland, I.; Roth, C.; Wohlfart, J.',
        title='Designing Information Provision Experiments',
        journal='J. Econ. Lit.', year='2023', volume='61', pages='3–40'),
    'ajayi_info': dict(
        authors='Ajayi, K.F.; Friedman, W.H.; Lucas, A.M.',
        title='When Information Is Not Enough: Evidence from a Centralised School Choice '
              'System',
        journal='Econ. J.', year='2026', volume='136', pages='26–60'),

    # ------------------------------------------------------- the demand shock
    'autor_newwork': dict(
        authors='Autor, D.; Chin, C.; Salomons, A.; Seegmiller, B.',
        title='New Frontiers: The Origins and Content of New Work, 1940–2018',
        journal='Q. J. Econ.', year='2024', volume='139', pages='1399–1465'),
    'hui_reshef': dict(
        authors='Hui, X.; Reshef, O.; Zhou, L.',
        title='The Short-Term Effects of Generative Artificial Intelligence on Employment: '
              'Evidence from an Online Labor Market',
        journal='Organ. Sci.', year='2024', volume='35', pages='1977–1989'),
    'acemoglu_ai': dict(
        authors='Acemoglu, D.',
        title='The Simple Macroeconomics of AI',
        journal='Econ. Policy', year='2025', volume='40', pages='13–58'),
    'peterson_obsol': dict(
        raw=True, year='2025',
        full='Peterson, A.J. Training for Obsolescence? The AI-Driven Education Trap; '
             'arXiv 2025, arXiv:2508.19625.'),

    # ------------------------------------------------ systems and the apparatus
    'sterman_misperc': dict(
        authors='Sterman, J.D.',
        title='Misperceptions of Feedback in Dynamic Decision Making',
        journal='Organ. Behav. Hum. Decis. Process.', year='1989', volume='43',
        pages='301–335'),
    'sterman_mgr': dict(
        authors='Sterman, J.D.',
        title='Modeling Managerial Behavior: Misperceptions of Feedback in a Dynamic '
              'Decision Making Experiment',
        journal='Manag. Sci.', year='1989', volume='35', pages='321–339'),
    'sterman_bd': dict(
        raw=True, year='2000',
        full='Sterman, J.D. Business Dynamics: Systems Thinking and Modeling for a Complex '
             'World; Irwin/McGraw-Hill: Boston, MA, USA, 2000.'),
    'forrester71': dict(
        authors='Forrester, J.W.',
        title='Counterintuitive Behavior of Social Systems',
        journal='Technol. Rev.', year='1971', volume='73', pages='52–68'),
    'meadows_ts': dict(
        raw=True, year='2008',
        full='Meadows, D.H. Thinking in Systems: A Primer; Wright, D., Ed.; Chelsea Green '
             'Publishing: White River Junction, VT, USA, 2008.'),
    'brunello_mismatch': dict(
        authors='Brunello, G.; Wruuck, P.',
        title='Skill Shortages and Skill Mismatch: A Review of the Literature',
        journal='J. Econ. Surv.', year='2021', volume='35', pages='1145–1167'),
    'bischof': dict(
        authors='Bischof, S.',
        title='Test-Based Measurement of Skill Mismatch: A Validation of Five Different '
              'Measurement Approaches Using the NEPS',
        journal='J. Labour Mark. Res.', year='2024', volume='58', pages='11'),
    'mckay_lhs': dict(
        authors='McKay, M.D.; Beckman, R.J.; Conover, W.J.',
        title='A Comparison of Three Methods for Selecting Values of Input Variables in the '
              'Analysis of Output from a Computer Code',
        journal='Technometrics', year='1979', volume='21', pages='239–245'),
    'razavi_sa': dict(
        authors='Razavi, S.; Jakeman, A.; Saltelli, A.; Prieur, C.; Iooss, B.; Borgonovo, E.; '
                'Plischke, E.; Lo Piano, S.; Iwanaga, T.; Becker, W.; et al.',
        title='The Future of Sensitivity Analysis: An Essential Discipline for Systems '
              'Modeling and Policy Support',
        journal='Environ. Model. Softw.', year='2021', volume='137', pages='104954'),
    'saltelli_false': dict(
        authors='Saltelli, A.; Aleksankina, K.; Becker, W.; Fennell, P.; Ferretti, F.; '
                'Holst, N.; Li, S.; Wu, Q.',
        title='Why So Many Published Sensitivity Analyses Are False: A Systematic Review of '
              'Sensitivity Analysis Practices',
        journal='Environ. Model. Softw.', year='2019', volume='114', pages='29–39'),
    'finkelstein_mvpf': dict(
        authors='Finkelstein, A.; Hendren, N.',
        title='Welfare Analysis Meets Causal Inference',
        journal='J. Econ. Perspect.', year='2020', volume='34', pages='146–167'),

    # -------------------------------------------------------- labour framework
    'katz_murphy': dict(
        authors='Katz, L.F.; Murphy, K.M.',
        title='Changes in Relative Wages, 1963–1987: Supply and Demand Factors',
        journal='Q. J. Econ.', year='1992', volume='107', pages='35–78'),
    'ciccone_peri': dict(
        authors='Ciccone, A.; Peri, G.',
        title='Long-Run Substitutability between More and Less Educated Workers: Evidence '
              'from U.S. States, 1950–1990',
        journal='Rev. Econ. Stat.', year='2005', volume='87', pages='652–663'),
}

REFS9 = dict(REFS8)
REFS9.update(NEW9)

# Items whose bibliographic detail the audit could not re-confirm and which are
# therefore not used anywhere in the manuscript:
#   Galanis et al. 2025 (volume/article number inconsistent with the PII)
#   Cavalli, Naimzada and Pecora 2025 (page range implausible for the journal)
#   Ost, Pan and Webber 2026; Conlon and Patel 2026; Delli Gatti et al. 2025
#   Weinstein 2022 (DOI encodes a different volume from the citation)
#   Dickson et al. 2022 (author order unresolved on a ten-author paper)
