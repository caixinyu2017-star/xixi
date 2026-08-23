# -*- coding: utf-8 -*-
"""参考文献数据库与引用引擎（GB/T 7714 顺序编码制＋文中（作者，年份））。
来源：refs_own.json（用户前期成果，取自原文 PDF）；经典理论（权威著录）；
youth-employment-paper 已核实英文池；检索工作流逐条核实条目（含来源链接见 data/refs_raw*.json）。"""

_DATA = [
 # ———— 一、用户前期成果（7 条，著录取自原文/官网检索） ————
 ('own_biomimetics', 'Cai和Zhang，2025',
  'CAI X, ZHANG C. An innovative differentiated creative search based on collaborative development and population evaluation[J]. Biomimetics, 2025, 10(5): 260.'),
 ('own_cluster', 'Qian和Cai，2025',
  'QIAN C, CAI X. An efficient social-driven educational competition optimizer for numerical optimization[J]. Cluster Computing, 2025, 28: 1024.'),
 ('own_scirep', 'Zhao等，2025',
  'ZHAO D, FENG L, WANG Y, et al. An improved enterprise development optimizer based on labor migration for numerical optimization[J]. Scientific Reports, 2025, 15: 26227.'),
 ('own_pension', '蔡鑫宇和张琳，2026',
  '蔡鑫宇, 张琳. 社会养老政策、劳动供给与生育率[J]. 数学的实践与认识, 2026, 56(4).'),
 ('own_youngwomen', 'Cai等，2025',
  "CAI X, ZHANG L, CHEN X, et al. Young women's employment in China: trends, challenges, and policy responses[C]//Proceedings of the 2025 11th International Conference on Humanities and Social Science Research (ICHSSR 2025). Dordrecht: Atlantis Press, 2025."),
 ('own_cefv', 'Jiang等，2025',
  'JIANG K, CAI X, LV Y, et al. Causal-enhanced feature validation for robust big data-driven employment market analysis[J/OL]. Journal of Emerging Applied AI, 2025[2026-08-23]. https://www.inno-press.com/index.php/JAAI/article/view/14.'),
 ('own_cnnatt', 'Wang等，2025',
  'WANG M, CHEN X, CAI X. Interpretable CNN-attention hybrid framework for spatiotemporal feature engineering in youth employment market trend prediction[J/OL]. Journal of Emerging Applied AI, 2025[2026-08-23]. https://www.inno-press.com/index.php/JAAI/article/view/11.'),

 # ———— 二、经典理论文献 ————
 ('schultz1961', 'Schultz，1961',
  'SCHULTZ T W. Investment in human capital[J]. The American Economic Review, 1961, 51(1): 1-17.'),
 ('becker1993', 'Becker，1993',
  'BECKER G S. Human capital: a theoretical and empirical analysis, with special reference to education[M]. 3rd ed. Chicago: University of Chicago Press, 1993.'),
 ('spence1973', 'Spence，1973',
  'SPENCE M. Job market signaling[J]. The Quarterly Journal of Economics, 1973, 87(3): 355-374.'),
 ('stigler1962', 'Stigler，1962',
  'STIGLER G J. Information in the labor market[J]. Journal of Political Economy, 1962, 70(5): 94-105.'),
 ('mccall1970', 'McCall，1970',
  'MCCALL J J. Economics of information and job search[J]. The Quarterly Journal of Economics, 1970, 84(1): 113-126.'),
 ('mortensen1994', 'Mortensen和Pissarides，1994',
  'MORTENSEN D T, PISSARIDES C A. Job creation and job destruction in the theory of unemployment[J]. The Review of Economic Studies, 1994, 61(3): 397-415.'),
 ('granovetter1973', 'Granovetter，1973',
  'GRANOVETTER M S. The strength of weak ties[J]. American Journal of Sociology, 1973, 78(6): 1360-1380.'),
 ('granovetter1995', 'Granovetter，1995',
  'GRANOVETTER M. Getting a job: a study of contacts and careers[M]. 2nd ed. Chicago: University of Chicago Press, 1995.'),
 ('super1980', 'Super，1980',
  'SUPER D E. A life-span, life-space approach to career development[J]. Journal of Vocational Behavior, 1980, 16(3): 282-298.'),
 ('savickas2005', 'Savickas，2005',
  'SAVICKAS M L. The theory and practice of career construction[M]//BROWN S D, LENT R W. Career development and counseling: putting theory and research to work. Hoboken: John Wiley & Sons, 2005: 42-70.'),
 ('bronfenbrenner1979', 'Bronfenbrenner，1979',
  'BRONFENBRENNER U. The ecology of human development: experiments by nature and design[M]. Cambridge, MA: Harvard University Press, 1979.'),
 ('sattinger1993', 'Sattinger，1993',
  'SATTINGER M. Assignment models of the distribution of earnings[J]. Journal of Economic Literature, 1993, 31(2): 831-880.'),

 # ———— 三、数字经济、AI 与就业英文文献（youth-employment-paper 已核实池） ————
 ('ogbonna2023', 'Ogbonna等，2023',
  'OGBONNA A E, ADEDIRAN I A, OLOKO T F, et al. Information and Communication Technology (ICT) and youth unemployment in Africa[J]. Quality & Quantity, 2023, 57(6): 5055-5077.'),
 ('azu2021', 'Azu等，2021',
  'AZU N P, JELIVOV G, ARAS O N, et al. Influence of digital economy on youth unemployment in West Africa[J]. Transnational Corporations Review, 2021, 13(1): 32-42.'),
 ('başol2023', 'Başol等，2023',
  'BAŞOL O, SEVGI H, YALÇIN E C. The Effect of Digitalization on Youth Unemployment for EU Countries: Treat or Threat?[J]. Sustainability, 2023, 15(14): 11080.'),
 ('acemoglu2019', 'Acemoglu和Restrepo，2019',
  'ACEMOGLU D, RESTREPO P. Automation and New Tasks: How Technology Displaces and Reinstates Labor[J]. Journal of Economic Perspectives, 2019, 33(2): 3-30.'),
 ('frey2017', 'Frey和Osborne，2017',
  'FREY C B, OSBORNE M A. The future of employment: How susceptible are jobs to computerisation?[J]. Technological Forecasting and Social Change, 2017, 114: 254-280.'),
 ('liang2024', 'Liang和Liu，2024',
  'LIANG F, LIU Y. Sustainable youth employment quality management: The impact of robotization in China[J]. PLoS ONE, 2024, 19(4): e0298081.'),
 ('xiong2024', 'Xiong和Yu，2024',
  "XIONG B, YU B. The Impact of Internet Development on Youth's Job Quality in the Digital Economy Era: Transmission Mechanism and Empirical Test[J]. Social Indicators Research, 2024, 175(1): 269-294."),
 ('xu2024', 'Xu等，2024',
  'XU G, QIU Y, QI J. Artificial intelligence and labor demand: An empirical analysis of Chinese small and micro enterprises[J]. Heliyon, 2024, 10(13): e33893.'),
 ('acemoglu2020', 'Acemoglu和Restrepo，2020',
  'ACEMOGLU D, RESTREPO P. Robots and Jobs: Evidence from US Labor Markets[J]. Journal of Political Economy, 2020, 128(6): 2188-2244.'),
 ('adachi2024', 'Adachi等，2024',
  'ADACHI D, KAWAGUCHI D, SAITO Y U. Robots and Employment: Evidence from Japan, 1978-2017[J]. Journal of Labor Economics, 2024, 42(2): 591-634.'),
 ('wang2024', 'Wang等，2024',
  'WANG T, ZHANG Y, LIU C. Robot adoption and employment adjustment: Firm-level evidence from China[J]. China Economic Review, 2024, 84: 102137.'),
 ('zhu2026', 'Zhu和Nie，2026',
  'ZHU G, NIE A. How industrial robots affect employment: firm-level evidence from China[J]. Journal of the Asia Pacific Economy, 2026, 31(1): 31-61.'),

 # ———— 四、检索工作流核实条目（自动追加区，勿手改标记行） ————
 # <<<WF_ENTRIES>>>
]

REFS = {k: {'intext': it, 'gb': gb} for k, it, gb in _DATA}
_ORDER = []


def c(key, paren=True, prefix='', suffix=''):
    """登记并返回文中引用串。paren=False 用于句法嵌入。"""
    if key not in REFS:
        raise KeyError(f'未知文献 key: {key}')
    if key not in _ORDER:
        _ORDER.append(key)
    it = REFS[key]['intext']
    body = f'{prefix}{it}{suffix}'
    return f'（{body}）' if paren else body


def _year_of(key):
    import re as _re
    m = _re.search(r'(\d{4})', REFS[key]['intext'])
    return int(m.group(1)) if m else 9999


def cc(*keys):
    """合引：自动按年份升序排列（同年保持传入顺序）。"""
    for k in keys:
        if k not in REFS:
            raise KeyError(f'未知文献 key: {k}')
    parts = []
    for k in sorted(keys, key=_year_of):
        if k not in _ORDER:
            _ORDER.append(k)
        parts.append(REFS[k]['intext'])
    return '（' + '；'.join(parts) + '）'


def gb_ordered():
    used = list(_ORDER)
    rest = [k for k in REFS if k not in _ORDER]
    return [REFS[k]['gb'] for k in used + rest]


def n_used():
    return len(_ORDER)


def reset():
    _ORDER.clear()


if __name__ == '__main__':
    keys = [k for k, _, _ in _DATA]
    assert len(keys) == len(set(keys)), '存在重复 key'
    print('条目数:', len(_DATA))
