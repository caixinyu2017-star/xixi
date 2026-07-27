# -*- coding: utf-8 -*-
"""Paper 6 references: verified pools from papers 1/2/5 plus new
decision-making/agility/TMT additions (verified 2026-07-20; evidence in
p6_references_verified.json)."""
from p5_refs import REFS5

REFS6 = dict(REFS5)

NEW6 = {
 'eisenhardt1989': dict(authors='Eisenhardt, K.M.',
     title='Making Fast Strategic Decisions in High-Velocity Environments',
     journal='Acad. Manag. J.', year='1989', volume='32', pages='543–576'),
 'baum2003': dict(authors='Baum, J.R.; Wally, S.',
     title='Strategic Decision Speed and Firm Performance',
     journal='Strateg. Manag. J.', year='2003', volume='24', pages='1107–1129'),
 'shrestha2019': dict(authors='Shrestha, Y.R.; Ben-Menahem, S.M.; von Krogh, G.',
     title='Organizational Decision-Making Structures in the Age of Artificial Intelligence',
     journal='Calif. Manag. Rev.', year='2019', volume='61', pages='66–83'),
 'teece_agility': dict(authors='Teece, D.; Peteraf, M.; Leih, S.',
     title='Dynamic Capabilities and Organizational Agility: Risk, Uncertainty, and Strategy in the Innovation Economy',
     journal='Calif. Manag. Rev.', year='2016', volume='58', pages='13–35'),
 'csaszar_ai': dict(authors='Csaszar, F.A.; Ketkar, H.; Kim, H.',
     title='Artificial Intelligence and Strategic Decision-Making: Evidence from Entrepreneurs and Investors',
     journal='Strategy Sci.', year='2024', volume='9', pages='322–345'),
 'tmt_age_digital': dict(authors='Zou, Z.; Fu, J.; Zeng, Y.; Huang, Y.',
     title='Do young CEOs matter for corporate digital transformation?',
     journal='Econ. Lett.', year='2024', volume='237', pages='111636'),
 'reverse_mentor': dict(authors='Chaudhuri, S.; Park, S.; Johnson, K.R.',
     title='Engagement, inclusion, knowledge sharing, and talent development: Is reverse mentoring a panacea to all? Findings from literature review',
     journal='Eur. J. Train. Dev.', year='2022', volume='46', pages='468–483'),
 'voice_part': dict(authors='Chamberlin, M.; Newton, D.W.; LePine, J.A.',
     title='A meta-analysis of voice and its promotive and prohibitive forms: Identification of key associations, distinctions, and future research directions',
     journal='Pers. Psychol.', year='2017', volume='70', pages='11–71'),
 'agility_dt': dict(authors='Troise, C.; Corvello, V.; Ghobadian, A.; O’Regan, N.',
     title='How can SMEs successfully navigate VUCA environment: The role of agility in the digital transformation era',
     journal='Technol. Forecast. Soc. Change', year='2022', volume='174', pages='121227'),
 'young_promotion': dict(authors='Steindórsdóttir, B.D.; Sanders, K.; Arnulf, J.K.; Dysvik, A.',
     title='Career transitions and career success from a lifespan developmental perspective: A 15-year longitudinal study',
     journal='J. Vocat. Behav.', year='2023', volume='140', pages='103809'),
}
REFS6.update(NEW6)
