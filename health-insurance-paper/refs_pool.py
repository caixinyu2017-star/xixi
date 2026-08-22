# -*- coding: utf-8 -*-
"""参考文献池。

两个来源：
（A）四篇《经济研究》范文的文末参考文献表（已由该刊编辑部审校，可信度高，
     本文件中的条目均经与两篇以上范文交叉比对或联网复核）；
（B）联网检索并逐条打开权威来源核实的条目（见 refs_verified.json，由工作流产出）。

著录格式：GB/T 7714—2015 顺序编码制。正文用 {c:key} 标注，按首次出现顺序编号。
"""

# key -> (语种, 著录字符串)
POOL = {
    # ---------------- 中文：中国医保制度与医疗费用 ----------------
    'fengjin2022': ('zh', '封进, 陈昕欣, 胡博. 效率与公平统一的医疗保险水平——来自城乡居民医疗保险制度整合的证据[J]. 经济研究, 2022(6): 155-172.'),
    'zhuhengpeng2021': ('zh', '朱恒鹏, 岳阳, 续继. 政府财政投入模式对医疗费用的影响[J]. 经济研究, 2021(12): 155-172.'),
    'yueyang2023': ('zh', '岳阳, 朱恒鹏, 王誉霖. 财政补贴对医院经营行为的影响研究[J]. 经济研究, 2023(3): 172-190.'),
    'zangwenbin2020': ('zh', '臧文斌, 陈晨, 赵绍阳. 社会医疗保险、疾病异质性和医疗费用[J]. 经济研究, 2020(12): 156-172.'),
    'zhaoshaoyang2015': ('zh', '赵绍阳, 臧文斌, 尹庆双. 医疗保障水平的福利效果[J]. 经济研究, 2015(8): 130-145.'),
    'tayuqi2023': ('zh', '沓钰淇, 黄炜, 雷晓燕. 实物类转移支付的道德风险：以中国城职保个人账户为例[J]. 世界经济, 2023(5): 121-148.'),
    'heqinghong2021': ('zh', '何庆红, 赵绍阳, 刘国恩. 医药分开改革对医疗费用和医疗质量的影响[J]. 世界经济, 2021(12): 154-179.'),
    'fumingwei2020': ('zh', '付明卫, 王普鹤, 赵嘉珩, 等. 市级统筹、制度设计与医保控费[J]. 产业经济评论, 2020(6): 5-20.'),
    'duchuang2023': ('zh', '杜创. 财政投入、激励相容与中国疾病防控体制改革[J]. 世界经济, 2023(1): 3-27.'),
    'duchuang2016': ('zh', '杜创, 朱恒鹏. 中国城市医疗卫生体制的演变逻辑[J]. 中国社会科学, 2016(8): 66-89.'),
    'machao2016': ('zh', '马超, 赵广川, 顾海. 城乡医保一体化制度对农村居民就医行为的影响[J]. 统计研究, 2016(4): 78-85.'),
    'pengxiaobo2019': ('zh', '彭晓博, 杜创. 医疗支出集中性与持续性研究：来自中国的微观经验证据[J]. 世界经济, 2019(12): 121-144.'),
    'fengjin2015': ('zh', '封进, 余央央, 楼平易. 医疗需求与中国医疗费用增长——基于城乡老年医疗支出差异的视角[J]. 中国社会科学, 2015(3): 85-103.'),
    'fengjin2010': ('zh', '封进, 刘芳, 陈沁. 新型农村合作医疗对县村两级医疗价格的影响[J]. 经济研究, 2010(11): 127-140.'),
    'chengeng2012': ('zh', '程令国, 张晔. “新农合”：经济绩效还是健康绩效？[J]. 经济研究, 2012(1): 120-133.'),
    'baizhongen2012': ('zh', '白重恩, 李宏彬, 吴斌珍. 医疗保险与消费：来自新型农村合作医疗的证据[J]. 经济研究, 2012(2): 41-53.'),
    'ganli2010': ('zh', '甘犁, 刘国恩, 马双. 基本医疗保险对促进家庭消费的影响[J]. 经济研究, 2010(S1): 30-38.'),
    'huangjialin2022': ('zh', '黄家林, 傅虹桥, 宋泽. 补充医疗保险对居民消费的影响——来自城乡居民大病保险的证据[J]. 金融研究, 2022(10): 133-151.'),
    'chenzui2018': ('zh', '陈醉, 宋泽, 张川川. 医药分开改革的政策效果——基于医疗保险报销数据的经验分析[J]. 金融研究, 2018(10): 90-107.'),
    'fengjin2018': ('zh', '封进, 王贞, 宋弘. 中国医疗保险体系中的自选择与医疗费用——基于灵活就业人员参保行为的研究[J]. 金融研究, 2018(8): 106-122.'),
    'wangzhen2019': ('zh', '王贞, 封进, 宋弘. 提升医保待遇对我国老年医疗服务利用的影响[J]. 财贸经济, 2019(6): 132-146.'),
    'gushin2019': ('zh', '顾昕. “健康中国”战略中基本卫生保健的治理创新[J]. 中国社会科学, 2019(12): 121-138.'),
    'lihua2013': ('zh', '李华, 俞卫. 政府卫生支出对中国农村居民健康的影响[J]. 中国社会科学, 2013(10): 41-60.'),
    'zhengxiyang2019': ('zh', '郑喜洋, 申曙光. 财政卫生支出：提升健康与降低费用——兼论企业医保降费[J]. 经济管理, 2019(1): 173-190.'),

    # ---------------- 中文：方法 ----------------
    'huangwei2022': ('zh', '黄炜, 张子尧, 刘安然. 从双重差分法到事件研究法[J]. 产业经济评论, 2022(2): 17-36.'),

    # ---------------- 英文：医保、道德风险与医疗费用 ----------------
    'chandra2010': ('en', 'CHANDRA A, GRUBER J, MCKNIGHT R. Patient cost-sharing and hospitalization offsets in the elderly[J]. American Economic Review, 2010, 100(1): 193-213.'),
    'dobkin2018': ('en', 'DOBKIN C, FINKELSTEIN A, KLUENDER R, et al. The economic consequences of hospital admissions[J]. American Economic Review, 2018, 108(2): 308-352.'),
    'einav2017': ('en', 'EINAV L, FINKELSTEIN A, SCHRIMPF P. Bunching at the kink: implications for spending responses to health insurance contracts[J]. Journal of Public Economics, 2017, 146: 27-40.'),
    'lu2019': ('en', 'LU Y, SHI J, YANG W. Expenditure response to health insurance policies: evidence from kinks in rural China[J]. Journal of Public Economics, 2019, 178: 104049.'),
    'layton2022': ('en', 'LAYTON T, MAESTAS N, PRINZ D, et al. Healthcare rationing in public insurance programs: evidence from Medicaid[J]. American Economic Journal: Economic Policy, 2022, 14(4): 397-431.'),
    'garthwaite2012': ('en', 'GARTHWAITE C L. The doctor might see you now: the supply side effects of public health insurance expansions[J]. American Economic Journal: Economic Policy, 2012, 4(3): 190-215.'),
    'freedman2015': ('en', 'FREEDMAN S, LIN H, SIMON K. Public health insurance expansions and hospital technology adoption[J]. Journal of Public Economics, 2015, 121: 117-131.'),
    'chetty2013': ('en', 'CHETTY R, FINKELSTEIN A. Social insurance: connecting theory to data[M]//AUERBACH A J, CHETTY R, FELDSTEIN M, et al. Handbook of public economics: Vol. 5. Amsterdam: Elsevier, 2013: 111-193.'),

    # ---------------- 英文：医院竞争与产业组织 ----------------
    'gaynor2015': ('en', 'GAYNOR M, HO K, TOWN R J. The industrial organization of health-care markets[J]. Journal of Economic Literature, 2015, 53(2): 235-284.'),
    'dengpan2019': ('en', 'DENG C, PAN J. Hospital competition and the expenses for treatments of acute and non-acute common diseases: evidence from China[J]. BMC Health Services Research, 2019, 19: 739.'),

    # ---------------- 联网逐条核实（已打开权威页面确认题名与出处） ----------------
    'ginsburg2026': ('en', 'GINSBURG P B. The emerging role of competition in health care[J]. Journal of Economic Perspectives, 2026, 40(2): 3-16.'),
    'gaynor2016': ('en', 'GAYNOR M, PROPPER C, SEILER S. Free to choose? Reform, choice, and consideration sets in the English National Health Service[J]. American Economic Review, 2016, 106(11): 3521-3557.'),
    'moscelli2021': ('en', 'MOSCELLI G, GRAVELLE H, SICILIANI L. Hospital competition and quality for non-emergency patients in the English NHS[J]. RAND Journal of Economics, 2021, 52(2): 382-414.'),
    'raval2022': ('en', 'RAVAL D, ROSENBAUM T, WILSON N E. Using disaster-induced closures to evaluate discrete choice models of hospital demand[J]. RAND Journal of Economics, 2022, 53(3): 561-589.'),
    'avdic2024': ('en', 'AVDIC D, LUNDBORG P, VIKSTROM J. Does health care consolidation harm patients? Evidence from maternity ward closures[J]. American Economic Journal: Economic Policy, 2024, 16(1): 160-189.'),
    'fischer2024': ('en', 'FISCHER S, ROYER H, WHITE C. Health care centralization: the health impacts of obstetric unit closures in the United States[J]. American Economic Journal: Applied Economics, 2024, 16(3): 113-141.'),
    'chan2023': ('en', 'CHAN D C, CARD D, TAYLOR L. Is there a VA advantage? Evidence from dually eligible veterans[J]. American Economic Review, 2023, 113(11): 3003-3043.'),
    'chandra2024': ('en', 'CHANDRA A, KAKANI P, SACARNY A. Hospital allocation and racial disparities in health care[J]. Review of Economics and Statistics, 2024, 106(4): 924-937.'),
    'wangshusen2023': ('zh', '王树森, 杨澄宇. 卫生支出结构、个人健康投资与居民福利[J]. 经济研究, 2023(6): 190-208.'),
}
