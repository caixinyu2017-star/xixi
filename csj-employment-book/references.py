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
 ('zeng2004', '曾湘泉，2004',
  '曾湘泉. 变革中的就业环境与中国大学生就业[J]. 经济研究, 2004(6): 87-95.'),
 ('xing2011', '邢春冰和李实，2011',
  '邢春冰, 李实. 扩招“大跃进”、教育机会与大学毕业生就业[J]. 经济学(季刊), 2011, 10(4).'),
 ('yue2023', '岳昌君等，2023',
  '岳昌君, 冯沁雪, 等. 中国高校毕业生就业趋势研究报告：来自2003—2021年调查数据[J]. 华东师范大学学报(教育科学版), 2023(9): 138-154.'),
 ('xia2024', '夏安平等，2024',
  '夏安平, 苏亚琴, 赵丽秋. 学历错配对职业流动的影响：来自雇主—雇员匹配数据的证据[J]. 劳动经济研究, 2024.'),
 ('yang2024', '杨艳和易伟，2024',
  '杨艳, 易伟. 劳动保护会增加技能错配吗？——基于劳动力社保参保的视角[J]. 劳动经济研究, 2024.'),
 ('ma2022', '马晔风和蔡跃洲，2022',
  '马晔风, 蔡跃洲. 数字经济新就业形态的规模估算与疫情影响研究[J]. 劳动经济研究, 2022.'),
 ('qiu2024', '邱康权和梁占永，2024',
  '邱康权, 梁占永. 营商环境优化、经营主体与稳就业[J]. 经济学动态, 2024(8).'),
 ('wang2024a', '王美艳，2024',
  '王美艳. “00后”群体就业面临的挑战及应对建议[J]. 中国发展观察, 2024.'),
 ('qiu2024a', '邱文琪等，2024',
  '邱文琪, 岳昌君, 等. 2023年全国高校毕业生就业状况实证研究——基于单位就业与灵活就业的对比分析[J]. 北京大学教育评论, 2024.'),
 ('lai2022', '赖德胜，2022',
  '赖德胜. 以高质量充分就业推进中国式现代化[J]. 中国人口科学, 2022(6).'),
 ('shi2025', '史婵等，2025',
  '史婵, 杨志红, 王小林. 数字创新合作与高质量充分就业——基于上市公司联合申请专利数据的研究[J]. 劳动经济研究, 2025.'),
 ('yue2020', '岳昌君等，2020',
  '岳昌君, 夏洁, 邱文琪. 2019年全国高校毕业生就业状况实证研究[J]. 华东师范大学学报(教育科学版), 2020(4): 1-17.'),
 ('hu2021', '胡艳婷和蒋承，2021',
  '胡艳婷, 蒋承. 专业匹配对高校毕业生工资起薪的影响——基于倾向得分匹配法的实证研究[J]. 华东师范大学学报(教育科学版), 2021, 39(4): 53-63.'),
 ('feng2025', '冯沁雪和岳昌君，2025',
  '冯沁雪, 岳昌君. 本专科毕业生的专业兴趣匹配能促进就业匹配吗？——基于专业、学历、能力三维就业匹配的实证分析[J]. 华东师范大学学报(教育科学版), 2025, 43(5).'),
 ('yang2023', '杨素红等，2023',
  '杨素红, 叶晓阳, 等. 本科毕业生专业—工作匹配与工资溢价——基于Shift-share工具变量的估计[J]. 北京大学教育评论, 2023, 21(1).'),
 ('zh2023', '尤亮和李根丽，2023',
  '尤亮, 李根丽. 过度教育与劳动者离职倾向[J]. 外国经济与管理, 2023(12).'),
 ('yanqiao2021', 'Zheng等，2021',
  'ZHENG Y, ZHANG X, ZHU Y. Overeducation, major mismatch, and return to higher education tiers: Evidence from novel data source of a major online recruitment platform in China[J]. China Economic Review, 2021, 66: 101584.'),
 ('zh2025', 'Jones等，2025',
  'JONES M K, KAYA E, NAN J. Overeducation, earnings and job satisfaction among graduates in China[J]. China Economic Review, 2025, 93.'),
 ('li2016', '李骏，2016',
  '李骏. 中国高学历劳动者的教育匹配与收入回报[J]. 社会, 2016, 36(3): 64-85.'),
 ('zh2018', '颜敏和王维国，2018',
  '颜敏, 王维国. 教育错配对工资的惩罚效应——来自中国微观面板数据的证据[J]. 财经研究, 2018(3).'),
 ('he2022', '何海清和张广利，2022',
  '何海清, 张广利. 青年考编现象中的职业想象与内卷实践研究[J]. 中国青年研究, 2022(12): 84-91.'),
 ('li2023', '李春玲，2023',
  '李春玲. 风险与竞争加剧环境下大学生就业选择变化研究[J]. 中国青年社会科学, 2023(5).'),
 ('yue2023a', '岳昌君，2023',
  '岳昌君. 高校毕业生就业观念：特点、变化与差异研究[J]. 中国青年研究, 2023(5): 5-13.'),
 ('zh2023a', '黎娟娟和黎文华，2023',
  '黎娟娟, 黎文华. 后物质主义价值观视角下的大学生慢就业——基于北京某高校的质性研究[J]. 中国青年研究, 2023(5).'),
 ('liu2023', '刘保中和臧小森，2023',
  '刘保中, 臧小森. 转型理论视域下未就业大学毕业生的就业心态与生活状态分析[J]. 中国青年研究, 2023(9).'),
 ('li2023a', '李春瑶，2023',
  '李春瑶. 脱嵌与迷惘：“间隔年”青年的另类内卷实践[J]. 中国青年研究, 2023(11): 74-80.'),
 ('chen2020', '陈龙，2020',
  '陈龙. “数字控制”下的劳动秩序——外卖骑手的劳动控制研究[J]. 社会学研究, 2020(6).'),
 ('zhang2023', '张成刚和王静怡，2023',
  '张成刚, 王静怡. 新就业形态与大学生就业的双向赋能[J]. 中国大学生就业, 2023(4).'),
 ('wang2020', '王永钦和董雯，2020',
  '王永钦, 董雯. 机器人的兴起如何影响中国劳动力市场？——来自制造业上市公司的证据[J]. 经济研究, 2020, 55(10): 159-175.'),
 ('kong2020', '孔高文等，2020',
  '孔高文, 刘莎莎, 孔东民. 机器人与就业——基于行业与地区异质性的探索性分析[J]. 中国工业经济, 2020(8): 80-98.'),
 ('yu2021', '余玲铮等，2021',
  '余玲铮, 魏下海, 孙中伟, 等. 工业机器人、工作任务与非常规能力溢价——来自制造业“企业—工人”匹配调查的证据[J]. 管理世界, 2021, 37(1): 47-59.'),
 ('li2021', '李磊等，2021',
  '李磊, 王小霞, 包群. 机器人的就业效应：机制与中国经验[J]. 管理世界, 2021, 37(9): 104-118.'),
 ('zh2021', '柏培文和张云，2021',
  '柏培文, 张云. 数字经济、人口红利下降与中低技能劳动者权益[J]. 经济研究, 2021, 56(5): 91-108.'),
 ('tian2022', '田鸽和张勋，2022',
  '田鸽, 张勋. 数字经济、非农就业与社会分工[J]. 管理世界, 2022, 38(5): 72-84.'),
 ('wang2022', '王林辉等，2022',
  '王林辉, 胡晟明, 董直庆. 人工智能技术、任务属性与职业可替代风险——来自微观层面的经验证据[J]. 管理世界, 2022, 38(7): 60-79.'),
 ('zh2022', '肖土盛等，2022',
  '肖土盛, 孙瑞琦, 袁淳, 等. 企业数字化转型、人力资本结构调整与劳动收入份额[J]. 管理世界, 2022, 38(12): 220-237.'),
 ('yao2024', '姚加权等，2024',
  '姚加权, 张锟澎, 郭李鹏, 等. 人工智能如何提升企业生产效率？——基于劳动力技能结构调整的视角[J]. 管理世界, 2024, 40(2): 101-116.'),
 ('xu2024a', '许和连等，2024',
  '许和连, 赵泽昊, 金友森. 人力资本如何驱动企业工业机器人应用？——基于中国“高校扩招”的准自然实验[J]. 数量经济技术经济研究, 2024(9).'),
 ('song2010', '宋冬林等，2010',
  '宋冬林, 王林辉, 董直庆. 技能偏向型技术进步存在吗？——来自中国的经验证据[J]. 经济研究, 2010, 45(5): 68-81.'),
 ('c2023', 'Braxton和Taska，2023',
  'BRAXTON J C, TASKA B. Technological change and the consequences of job loss[J]. American Economic Review, 2023, 113(2): 279-316.'),
 ('d2024', 'Autor等，2024',
  'AUTOR D, CHIN C, SALOMONS A, et al. New frontiers: the origins and content of new work, 1940-2018[J]. The Quarterly Journal of Economics, 2024, 139(3): 1399-1465.'),
 ('e2025', 'Brynjolfsson等，2025',
  'BRYNJOLFSSON E, LI D, RAYMOND L R. Generative AI at work[J]. The Quarterly Journal of Economics, 2025, 140(2): 889-942.'),
 ('chen2023', '陈迪明，2023',
  '陈迪明. 构建新时代高校高质量就业工作体系路径研究——以华中师范大学“三位一体”就业工作体系为例[J]. 中国大学生就业, 2023(6).'),
 ('xu2022', '许泽宁等，2022',
  '许泽宁, 陈子韬, 甄茂成. 区域一体化政策对城市高学历人才分布的影响与作用机制——以长三角地区为例[J]. 地理研究, 2022, 41(6): 1540-1553.'),
 ('cui2022', '崔璨等，2022',
  '崔璨, 于程媛, 王强. 人才流动的空间特征、驱动因素及其对长三角一体化高质量发展的启示——基于高校毕业生的分析[J]. 自然资源学报, 2022, 37(6): 1440-1454.'),
 ('wang2021', '王一凡等，2021',
  '王一凡, 崔璨, 王强, 等. “人才争夺战”背景下人才流动的空间特征及影响因素——以中国“一流大学”毕业生为例[J]. 地理研究, 2021, 40(3): 743-761.'),
 ('kong2022', '孔令丞等，2022',
  '孔令丞, 王悦, 谢家平. 长三角区域一体化扩容、协调集聚与区域创新[J]. 财经研究, 2022(12).'),
 ('card2018', 'Card等，2018',
  'CARD D, KLUVE J, WEBER A. What works? A meta-analysis of recent active labor market program evaluations[J]. Journal of the European Economic Association, 2018, 16(3): 894-931.'),
 ('alfonsi2020', 'Alfonsi等，2020',
  'ALFONSI L, BANDIERA O, BASSI V, et al. Tackling youth unemployment: evidence from a labor market experiment in Uganda[J]. Econometrica, 2020, 88(6): 2369-2414.'),
 ('cahuc2021', 'Cahuc等，2021',
  'CAHUC P, CARCILLO S, MINEA A. The difficult school-to-work transition of high school dropouts: evidence from a field experiment[J]. Journal of Human Resources, 2021, 56(1): 159-183.'),
 ('bertrand2021', 'Bertrand等，2021',
  "BERTRAND M, MOGSTAD M, MOUNTJOY J. Improving educational pathways to social mobility: evidence from Norway's Reform 94[J]. Journal of Labor Economics, 2021, 39(4): 965-1010."),
 ('katz2022', 'Katz等，2022',
  'KATZ L F, ROTH J, HENDRA R, et al. Why do sectoral employment programs work? Lessons from WorkAdvance[J]. Journal of Labor Economics, 2022, 40(S1): S249-S291.'),
 ('barbanchon2023', 'Barbanchon等，2023',
  'LE BARBANCHON T, UBFAL D, ARAYA F. The effects of working while in school: evidence from employment lotteries[J]. American Economic Journal: Applied Economics, 2023, 15(1): 383-410.'),
 ('carranza2024', 'Carranza和McKenzie，2024',
  'CARRANZA E, MCKENZIE D. Job training and job search assistance policies in developing countries[J]. Journal of Economic Perspectives, 2024, 38(1): 221-244.'),
 ('(ilo)2024', 'ILO，2024',
  'INTERNATIONAL LABOUR ORGANIZATION. Global employment trends for youth 2024: decent work, brighter futures[R]. Geneva: International Labour Office, 2024.'),
 ('oecd2024', 'OECD，2024',
  'OECD. OECD employment outlook 2024: the net-zero transition and the labour market[R]. Paris: OECD Publishing, 2024.'),
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
