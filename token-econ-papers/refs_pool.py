# -*- coding: utf-8 -*-
"""参考文献池（两篇词元经济论文共用）。

来源：联网检索工作流逐条核实（原始证据见 research_raw.json 与 refs_verify.json）。
凡卷期页码未能亲眼核实者一律不入池，不做推算；题名与出处对不上者已剔除。

著录格式：GB/T 7714—2015 顺序编码制。正文用 {c:key} 标注，按首次出现顺序编号。
"""

# key -> (语种, 著录字符串)
POOL = {
    # ---------------- 中文：人工智能、数字基础设施与企业行为 ----------------
    'chen2018': ('zh', '陈永伟. 人工智能与经济学：关于近期文献的一个综述[J]. 东北财经大学学报, 2018(3): 6-21.'),
    'chen2026': ('zh', '陈钊, 张洲, 钟岳霖. 生成式人工智能的影响：个体、组织与社会[J]. 经济学(季刊), 2026, 26(3): 623-667.'),
    'chen2026a': ('zh', '陈斌开, 张梓润, 夏俊杰, 陈思. 人工智能、经济增长与财富分配[J]. 经济学(季刊), 2026, 26(3): 668-691.'),
    'cheng2021': ('zh', '程文. 人工智能、索洛悖论与高质量发展：通用目的技术扩散的视角[J]. 经济研究, 2021, 56(10): 22-38.'),
    'hu2026': ('zh', '胡涟漪, 盖庆恩, 潘珊. 人工智能与职业需求——基于任务内容的替代、互补与创造效应分析[J]. 经济学(季刊), 2026, 26(3): 713.'),
    'huang2024': ('zh', '黄先海, 孙涌铭, 陈梦涛. 企业数字化转型与颠覆性技术创新——来自专利网络与SBERT模型的微观证据[J]. 中国工业经济, 2024(10): 137-154.'),
    'jiao2023': ('zh', '焦豪, 崔瑜, 张亚敏. 数字基础设施建设与城市高技能创业人才吸引[J]. 经济研究, 2023(12): 150-166.'),
    'lei2026': ('zh', '雷晓燕, 张子哲, 方丹吟, 沈艳. 人工智能驱动的教育变革：技术冲击下中国高校学科布局的实证研究[J]. 经济学(季刊), 2026, 26(3): 692-712.'),
    'li2024': ('zh', '李玉花, 林雨昕, 李丹丹. 人工智能技术应用如何影响企业创新[J]. 中国工业经济, 2024(10): 155-173.'),
    'wang2023': ('zh', '王林辉, 钱圆圆, 宋冬林, 等. 机器人应用的岗位转换效应及就业敏感性群体特征——来自微观个体层面的经验证据[J]. 经济研究, 2023(7): 69-85.'),
    'xiong2023': ('zh', '熊巧琴, 汤珂, 张丰羽. 第三方数字平台能否帮助中小微企业提升经营收益？——来自百万商户大数据的证据[J]. 经济学(季刊), 2023, 23(5): 1704-1722.'),
    'xu2025': ('zh', '许诺, 毛聚, 毛新述. 算力部署、数据跨域流动与企业全要素生产率——来自智算中心的证据[J]. 中国工业经济, 2025(4): 61-79.'),
    'yao2024': ('zh', '姚加权, 张锟澎, 郭李鹏, 等. 人工智能如何提升企业生产效率？——基于劳动力技能结构调整的视角[J]. 管理世界, 2024, 40(2): 101-116+133+117-122.'),
    # ---------------- 英文：人工智能的宏观与任务效应 ----------------
    'acemoglu2019': ('en', 'ACEMOGLU D, RESTREPO P. Automation and new tasks: how technology displaces and reinstates labor[J]. Journal of Economic Perspectives, 2019, 33(2): 3-30.'),
    'acemoglu2022': ('en', 'ACEMOGLU D, RESTREPO P. Tasks, automation, and the rise in U.S. wage inequality[J]. Econometrica, 2022, 90(5): 1973-2016.'),
    'acemoglu2025': ('en', 'ACEMOGLU D. The simple macroeconomics of AI[J]. Economic Policy, 2025, 40(121): 13-58.'),
    'autor2024': ('en', 'AUTOR D, CHIN C, SALOMONS A, et al. New frontiers: the origins and content of new work, 1940-2018[J]. The Quarterly Journal of Economics, 2024, 139(3): 1399-1465.'),
    'eloundou2024': ('en', 'ELOUNDOU T, MANNING S, MISHKIN P, et al. GPTs are GPTs: labor market impact potential of LLMs[J]. Science, 2024, 384(6702): 1306-1308.'),
    'humlum2025': ('en', 'HUMLUM A, VESTERGAARD E. Large language models, small labor market effects[R]. Cambridge, MA: National Bureau of Economic Research, 2025. NBER Working Paper No. 33777.'),
    'korinek2023': ('en', 'KORINEK A. Generative AI for economic research: use cases and implications for economists[J]. Journal of Economic Literature, 2023, 61(4): 1281-1317.'),
    'noy2023': ('en', 'NOY S, ZHANG W. Experimental evidence on the productivity effects of generative artificial intelligence[J]. Science, 2023, 381(6654): 187-192.'),
    # ---------------- 英文：质量调整价格指数与享乐方法 ----------------
    'aizcorbe2002': ('en', 'AIZCORBE A M. Price measures for semiconductor devices[R]. FEDS Working Paper No. 2002-13. Washington, D.C.: Board of Governors of the Federal Reserve System, 2002.'),
    'aizcorbe2014': ('en', 'AIZCORBE A M. A Practical Guide to Price Index and Hedonic Techniques[M]. Oxford: Oxford University Press, 2014.'),
    'boskin1998': ('en', 'BOSKIN M J, DULBERGER E R, GORDON R J, GRILICHES Z, JORGENSON D W. Consumer prices, the consumer price index, and the cost of living[J]. Journal of Economic Perspectives, 1998, 12(1): 3-26.'),
    'byrne2018': ('en', 'BYRNE D M, OLINER S D, SICHEL D E. How fast are semiconductor prices falling?[J]. Review of Income and Wealth, 2018, 64(3): 679-702.'),
    'byrne2021': ('en', 'BYRNE D M, CORRADO C. Accounting for innovations in consumer digital services: IT still matters[M]//Measuring and Accounting for Innovation in the Twenty-First Century. Chicago: University of Chicago Press, 2021: 471-518.'),
    'ehrlich2026': ('en', 'EHRLICH G, HALTIWANGER J, JARMIN R S, JOHNSON D, OLIVARES E, PARDUE L W, SHAPIRO M D, ZHAO L. Quality adjustment at scale: hedonic versus exact demand-based price indices[J]. American Economic Review, 2026, 116(6): 1955-1995.'),
    'gao2000': ('en', 'U.S. GENERAL ACCOUNTING OFFICE. Consumer price index: update of Boskin Commission\'s estimate of bias[R]. GAO/GGD-00-50. Washington, D.C.: U.S. General Accounting Office, 2000.'),
    'griliches1961': ('en', 'GRILICHES Z. Hedonic price indexes for automobiles: an econometric analysis of quality change[M]//The Price Statistics of the Federal Government. New York: National Bureau of Economic Research, 1961: 173-196.'),
    # ---------------- 英文：回弹效应与需求估计 ----------------
    'borenstein2015': ('en', 'BORENSTEIN S. A microeconomic framework for evaluating energy efficiency rebound and some implications[J]. The Energy Journal, 2015, 36(1): 1-22.'),
    'brynjolfsson2025': ('en', 'BRYNJOLFSSON E, LI D, RAYMOND L. Generative AI at work[J]. The Quarterly Journal of Economics, 2025, 140(2): 889-942.'),
    'byrne2018cloud': ('en', 'BYRNE D M, CORRADO C A, SICHEL D E. The rise of cloud computing: minding your P\'s, Q\'s and K\'s[R]. Cambridge, MA: National Bureau of Economic Research, 2018. NBER Working Paper No. 25188.'),
    'conlon2020': ('en', 'CONLON C, GORTMAKER J. Best practices for differentiated products demand estimation with PyBLP[J]. The RAND Journal of Economics, 2020, 51(4): 1108-1161.'),
    'gillingham2016': ('en', 'GILLINGHAM K, RAPSON D, WAGNER G. The rebound effect and energy efficiency policy[J]. Review of Environmental Economics and Policy, 2016, 10(1): 68-88.'),
    # ---------------- 英文：搜寻、价格离散与质量不确定 ----------------
    'akerlof1970': ('en', 'AKERLOF G A. The market for “lemons”: quality uncertainty and the market mechanism[J]. The Quarterly Journal of Economics, 1970, 84(3): 488-500.'),
    'baye2006': ('en', 'BAYE M R, MORGAN J, SCHOLTEN P. Information, search, and price dispersion[M]//HENDERSHOTT T. Handbook on Economics and Information Systems: Volume 1. Amsterdam: Elsevier, 2006: 323-377.'),
    'ellison2009': ('en', 'ELLISON G, ELLISON S F. Search, obfuscation, and price elasticities on the Internet[J]. Econometrica, 2009, 77(2): 427-452.'),
    'varian1980': ('en', 'VARIAN H R. A model of sales[J]. The American Economic Review, 1980, 70(4): 651-659.'),
    # ---------------- 英文与中文：标准、计量与市场制度 ----------------
    'barzel1982': ('en', 'BARZEL Y. Measurement cost and the organization of markets[J]. Journal of Law and Economics, 1982, 25(1): 27-48.'),
    'besen1994': ('en', 'BESEN S M, FARRELL J. Choosing how to compete: Strategies and tactics in standardization[J]. Journal of Economic Perspectives, 1994, 8(2): 117-131.'),
    'caict2025': ('zh', '中国信息通信研究院云计算与大数据研究所. 算力经济发展研究报告（2025年）[R]. 北京: 中国信息通信研究院, 2025.'),
    'de2012': ('en', 'DE LOS SANTOS B, HORTAÇSU A, WILDENBEEST M R. Testing models of consumer search using data on web browsing and purchasing behavior[J]. American Economic Review, 2012, 102(6): 2955-2980.'),
    'destefano2025': ('en', 'DESTEFANO T, KNELLER R, TIMMIS J. Cloud computing and firm growth[J]. The Review of Economics and Statistics, 2025（网络首发）: 1-47. DOI:10.1162/rest_a_01393.'),
    'dranove2010': ('en', 'DRANOVE D, JIN G Z. Quality disclosure and certification: Theory and practice[J]. Journal of Economic Literature, 2010, 48(4): 935-963.'),
    'farrell1985': ('en', 'FARRELL J, SALONER G. Standardization, compatibility, and innovation[J]. The RAND Journal of Economics, 1985, 16(1): 70-83.'),
    'goldfarb2019': ('en', 'GOLDFARB A, TUCKER C. Digital economics[J]. Journal of Economic Literature, 2019, 57(1): 3-43.'),
    'jensen2007': ('en', 'JENSEN R. The digital provide: Information (technology), market performance, and welfare in the South Indian fisheries sector[J]. The Quarterly Journal of Economics, 2007, 122(3): 879-924.'),
    'katz1985': ('en', 'KATZ M L, SHAPIRO C. Network externalities, competition, and compatibility[J]. American Economic Review, 1985, 75(3): 424-440.'),
    'kim2026': ('en', 'KIM J Y. Data portability and interoperability between digital platforms[J]. Journal of Economics & Management Strategy, 2026, 35(2): 219-232. DOI:10.1111/jems.12643.'),
    'stigler1961': ('en', 'STIGLER G J. The economics of information[J]. Journal of Political Economy, 1961, 69(3): 213-225.'),
    'yang2024': ('en', 'YANG L. The economics of standards: A literature review[J]. Journal of Economic Surveys, 2024, 38(3): 717-758. DOI:10.1111/joes.12555.'),
    'zhong2022': ('zh', '种照辉, 高志红, 覃成林. 网络基础设施建设与城市间合作创新——“宽带中国”试点及其推广的证据[J]. 财经研究, 2022, 48(3): 79-93.'),
    # ---------------- 英文：补核新增（平台价格离散与云计算价格质量调整） ----------------
    'mohapatra2024': ('en', 'MOHAPATRA D, MOHAPATRA D P, DUBEY R S. Price dispersion across online platforms: evidence from hotel room prices in London (UK)[J]. Applied Economics, 2024, 56(52): 6598-6610. DOI:10.1080/00036846.2023.2275219.'),
    'sawyer2023': ('en', 'SAWYER S D, O\'BRYAN C. Exploring quality adjustment in PPI cloud computing[J]. Monthly Labor Review, 2023.'),
}


# key -> 文中引用串（用于正文以「（作者，年份）」形式提及时保持全文一致）
INTEXT = {
    'acemoglu2019': 'Acemoglu 和 Restrepo，2019',
    'acemoglu2022': 'Acemoglu 和 Restrepo，2022',
    'acemoglu2025': 'Acemoglu，2025',
    'aizcorbe2002': 'Aizcorbe，2002',
    'aizcorbe2014': 'Aizcorbe，2014',
    'akerlof1970': 'Akerlof，1970',
    'autor2024': 'Autor 等，2024',
    'barzel1982': 'Barzel，1982',
    'baye2006': 'Baye 等，2006',
    'besen1994': 'Besen 和 Farrell，1994',
    'borenstein2015': 'Borenstein，2015',
    'boskin1998': 'Boskin 等，1998',
    'brynjolfsson2025': 'Brynjolfsson 等，2025',
    'byrne2018': 'Byrne 等，2018a',
    'byrne2018cloud': 'Byrne 等，2018',
    'byrne2021': 'Byrne 和 Corrado，2021',
    'caict2025': '中国信息通信研究院，2025',
    'chen2018': '陈永伟，2018',
    'chen2026': '陈钊等，2026',
    'chen2026a': '陈斌开等，2026',
    'cheng2021': '程文，2021',
    'conlon2020': 'Conlon 和 Gortmaker，2020',
    'de2012': 'De los Santos 等，2012',
    'destefano2025': 'DeStefano 等，2025',
    'dranove2010': 'Dranove 和 Jin，2010',
    'ehrlich2026': 'Ehrlich 等，2026',
    'ellison2009': 'Ellison 和 Ellison，2009',
    'eloundou2024': 'Eloundou 等，2024',
    'farrell1985': 'Farrell 和 Saloner，1985',
    'gao2000': 'U.S. GAO，2000',
    'gillingham2016': 'Gillingham 等，2016',
    'goldfarb2019': 'Goldfarb 和 Tucker，2019',
    'griliches1961': 'Griliches，1961',
    'hu2026': '胡涟漪等，2026',
    'huang2024': '黄先海等，2024',
    'humlum2025': 'Humlum 和 Vestergaard，2025',
    'jensen2007': 'Jensen，2007',
    'jiao2023': '焦豪等，2023',
    'katz1985': 'Katz 和 Shapiro，1985',
    'kim2026': 'Kim，2026',
    'korinek2023': 'Korinek，2023',
    'lei2026': '雷晓燕等，2026',
    'li2024': '李玉花等，2024',
    'mohapatra2024': 'Mohapatra 等，2024',
    'noy2023': 'Noy 和 Zhang，2023',
    'sawyer2023': 'Sawyer 和 O\'Bryan，2023',
    'stigler1961': 'Stigler，1961',
    'varian1980': 'Varian，1980',
    'wang2023': '王林辉等，2023',
    'xiong2023': '熊巧琴等，2023',
    'xu2025': '许诺等，2025',
    'yang2024': 'Yang，2024',
    'yao2024': '姚加权等，2024',
    'zhong2022': '种照辉等，2022',
}


if __name__ == '__main__':
    assert len(POOL) == len(set(POOL)), '重复 key'
    bad = [k for k, (_, s) in POOL.items() if '待核' in s]
    assert not bad, f'仍有待核条目: {bad}'
    zh = sum(1 for lang, _ in POOL.values() if lang == 'zh')
    print(f'条目 {len(POOL)} 条（中文 {zh}，英文 {len(POOL) - zh}）')
