# -*- coding: utf-8 -*-
"""References for the entry-level-jobs paper.

The pool verified for the companion paper is reused, and the entries added here
were each confirmed against the publisher record or an independent index
(DOI/Science/Oxford Academic/NBER/BFI listing) on 2026-07-28.  Classical results
in search theory and the economics of training are cited from their original
journal publication.
"""
import os
import sys

_YSTS = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", "..",
                                     "zhejiang-youth-systems-paper", "build"))
if _YSTS not in sys.path:
    sys.path.insert(0, _YSTS)

from ysts_refs import REFS as POOL          # noqa: E402

REFS = dict(POOL)

NEW = {
    # ---------------------------------------------- search and matching theory
    'diamond1982': dict(
        authors='Diamond, P.A.',
        title='Aggregate Demand Management in Search Equilibrium',
        journal='Journal of Political Economy', year='1982', volume='90',
        pages='881–894'),
    'mortensen1994': dict(
        authors='Mortensen, D.T.; Pissarides, C.A.',
        title='Job Creation and Job Destruction in the Theory of Unemployment',
        journal='The Review of Economic Studies', year='1994', volume='61',
        pages='397–415'),
    'hosios1990': dict(
        authors='Hosios, A.J.',
        title='On the Efficiency of Matching and Related Models of Search and '
              'Unemployment',
        journal='The Review of Economic Studies', year='1990', volume='57',
        pages='279–298'),
    'pissarides2000': dict(
        authors='Pissarides, C.A.',
        title='Equilibrium Unemployment Theory, 2nd ed.',
        journal='MIT Press: Cambridge, MA, USA', year='2000'),
    'shimer2005': dict(
        authors='Shimer, R.',
        title='The Cyclical Behavior of Equilibrium Unemployment and Vacancies',
        journal='American Economic Review', year='2005', volume='95',
        pages='25–49'),
    'hall2008': dict(
        authors='Hall, R.E.; Milgrom, P.R.',
        title='The Limited Influence of Unemployment on the Wage Bargain',
        journal='American Economic Review', year='2008', volume='98',
        pages='1653–1674'),
    'burdett1998': dict(
        authors='Burdett, K.; Mortensen, D.T.',
        title='Wage Differentials, Employer Size, and Unemployment',
        journal='International Economic Review', year='1998', volume='39',
        pages='257–273'),
    'postelvinay2002': dict(
        authors='Postel-Vinay, F.; Robin, J.-M.',
        title='Equilibrium Wage Dispersion with Worker and Employer '
              'Heterogeneity',
        journal='Econometrica', year='2002', volume='70', pages='2295–2350'),
    'cahuc2006': dict(
        authors='Cahuc, P.; Postel-Vinay, F.; Robin, J.-M.',
        title='Wage Bargaining with On-the-Job Search: Theory and Evidence',
        journal='Econometrica', year='2006', volume='74', pages='323–364'),
    'jovanovic1979': dict(
        authors='Jovanovic, B.',
        title='Job Matching and the Theory of Turnover',
        journal='Journal of Political Economy', year='1979', volume='87',
        pages='972–990'),

    # ---------------------------------------------- training and the job ladder
    'becker1964': dict(
        authors='Becker, G.S.',
        title='Human Capital: A Theoretical and Empirical Analysis, with '
              'Special Reference to Education',
        journal='Columbia University Press: New York, NY, USA', year='1964'),
    'acemoglupischke1998': dict(
        authors='Acemoglu, D.; Pischke, J.-S.',
        title='Why Do Firms Train? Theory and Evidence',
        journal='The Quarterly Journal of Economics', year='1998',
        volume='113', pages='79–119'),
    'acemoglupischke1999': dict(
        authors='Acemoglu, D.; Pischke, J.-S.',
        title='Beyond Becker: Training in Imperfect Labour Markets',
        journal='The Economic Journal', year='1999', volume='109',
        pages='F112–F142'),
    'stevens1994': dict(
        authors='Stevens, M.',
        title='A Theoretical Model of On-the-Job Training with Imperfect '
              'Competition',
        journal='Oxford Economic Papers', year='1994', volume='46',
        pages='537–562'),
    'gibbons1999': dict(
        authors='Gibbons, R.; Waldman, M.',
        title='A Theory of Wage and Promotion Dynamics inside Firms',
        journal='The Quarterly Journal of Economics', year='1999',
        volume='114', pages='1321–1358'),
    'topel1992': dict(
        authors='Topel, R.H.; Ward, M.P.',
        title='Job Mobility and the Careers of Young Men',
        journal='The Quarterly Journal of Economics', year='1992',
        volume='107', pages='439–479'),
    'kambourov2009': dict(
        authors='Kambourov, G.; Manovskii, I.',
        title='Occupational Specificity of Human Capital',
        journal='International Economic Review', year='2009', volume='50',
        pages='63–115'),

    # ---------------------------------------------- automation, tasks and AI
    'acemoglurestrepo2018': dict(
        authors='Acemoglu, D.; Restrepo, P.',
        title='The Race between Man and Machine: Implications of Technology '
              'for Growth, Factor Shares, and Employment',
        journal='American Economic Review', year='2018', volume='108',
        pages='1488–1542'),
    'autor2015': dict(
        authors='Autor, D.H.',
        title='Why Are There Still So Many Jobs? The History and Future of '
              'Workplace Automation',
        journal='Journal of Economic Perspectives', year='2015', volume='29',
        pages='3–30'),
    'acemoglu2025macro': dict(
        authors='Acemoglu, D.',
        title='The Simple Macroeconomics of AI',
        journal='Economic Policy', year='2025', volume='40', pages='13–58'),
    'eloundou2024': dict(
        authors='Eloundou, T.; Manning, S.; Mishkin, P.; Rock, D.',
        title='GPTs are GPTs: Labor Market Impact Potential of LLMs',
        journal='Science', year='2024', volume='384', pages='1306–1308'),
    'brynjolfsson2025canaries': dict(
        authors='Brynjolfsson, E.; Chandar, B.; Chen, R.',
        title='Canaries in the Coal Mine? Six Facts about the Recent '
              'Employment Effects of Artificial Intelligence',
        journal='Stanford Digital Economy Lab Working Paper: Stanford, CA, USA',
        year='2025'),
    'humlum2025': dict(
        authors='Humlum, A.; Vestergaard, E.',
        title='Large Language Models, Small Labor Market Effects',
        journal='Becker Friedman Institute Working Paper 2025-56: Chicago, IL, '
                'USA', year='2025'),
    # ---------------------------------------------- wage setting and rigidity
    'blanchard2007': dict(
        authors='Blanchard, O.; Gali, J.',
        title='Real Wage Rigidities and the New Keynesian Model',
        journal='Journal of Money, Credit and Banking', year='2007',
        volume='39', pages='35-65'),
    'hagedorn2008': dict(
        authors='Hagedorn, M.; Manovskii, I.',
        title='The Cyclical Behavior of Equilibrium Unemployment and Vacancies '
              'Revisited',
        journal='American Economic Review', year='2008', volume='98',
        pages='1692-1706'),
    'pissarides2009': dict(
        authors='Pissarides, C.A.',
        title='The Unemployment Volatility Puzzle: Is Wage Stickiness the '
              'Answer?',
        journal='Econometrica', year='2009', volume='77', pages='1339-1369'),
    'mayneris2018': dict(
        authors='Mayneris, F.; Poncet, S.; Zhang, T.',
        title='Improving or Disappearing: Firm-Level Adjustments to Minimum '
              'Wages in China',
        journal='Journal of Development Economics', year='2018', volume='135',
        pages='20-42'),
}

REFS.update(NEW)
