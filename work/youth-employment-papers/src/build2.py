# -*- coding: utf-8 -*-
"""将 [@key] 引文按首次出现顺序编号为上标 ^[n]^，并按 GB/T 7714 顺序编码制生成
参考文献著录列表。

著录格式：
    期刊  [序号] 作者. 文章名[J]. 期刊名, 出版年, 卷(期): 起止页码.
    专著  [序号] 作者. 书名[M]. 出版地: 出版者, 出版年: 起止页码.

全部条目的作者、年份、卷期与起止页码均经联网核验，核验来源见 refs_verification.md；
其中 2022 年及以后发表的文献占多数，2021 年及以前的仅限本主题不可替代的奠基性文献。
"""
import re
import sys

REFS = {
    # ==== 2022 年及以后（占多数）====
    "chen2022": "陈晓红,李杨扬,宋丽洁,等.数字经济理论体系与研究展望[J].管理世界,2022,38(2):208-224.",
    "jiang2022": "江小涓,靳景.数字技术提升经济效率:服务分工、产业协同和数实孪生[J].管理世界,2022,38(12):9-26.",
    "tian2022": "田鸽,张勋.数字经济、非农就业与社会分工[J].管理世界,2022,38(5):72-84.",
    "chengui2022": "陈贵富,韩静,韩恺明.城市数字经济发展、技能偏向型技术进步与劳动力不充分就业[J].中国工业经济,2022(8):118-136.",
    "liu2022": "刘翠花.数字经济对产业结构升级和创业增长的影响[J].中国人口科学,2022(2):112-125.",
    "yang2022": "杨伟国,吴邦正.平台经济对就业结构的影响[J].中国人口科学,2022(4):2-16.",
    "wanglinhui2023": "王林辉,钱圆圆,宋冬林,等.机器人应用的岗位转换效应及就业敏感性群体特征——来自微观个体层面的经验证据[J].经济研究,2023,58(7):69-85.",
    "yao2024": "姚加权,张锟澎,郭李鹏,等.人工智能如何提升企业生产效率?——基于劳动力技能结构调整的视角[J].管理世界,2024,40(2):101-116.",
    "li2024": "李建奇,黄维晨.“数实融合”下的平台经济与包容性就业——基于网络招聘大数据的经验研究[J].财经研究,2024,50(10):34-48.",
    "xu2024": "徐明,陈斯洁,聂云蕊.我国青年就业研究的核心议题、演变与展望[J].人口与经济,2024(5):92-107.",
    "ding2024": "丁述磊,王佳萍,刘翠花.教育错配对青年就业质量的影响:理论与实证[J].中国青年研究,2024(9):101-110.",
    "zhang2025": "张丹丹,于航,李力行,等.中国人工智能技术暴露度的测算及其对劳动需求的影响——基于大语言模型的新证据[J].管理世界,2025,41(7):59-72.",
    "acemoglu2022": "Acemoglu D, Restrepo P. Tasks, Automation, and the Rise in U.S. Wage Inequality[J]. Econometrica, 2022, 90(5): 1973-2016.",
    "noy2023": "Noy S, Zhang W. Experimental Evidence on the Productivity Effects of Generative Artificial Intelligence[J]. Science, 2023, 381(6654): 187-192.",
    "eloundou2024": "Eloundou T, Manning S, Mishkin P, et al. GPTs Are GPTs: Labor Market Impact Potential of LLMs[J]. Science, 2024, 384(6702): 1306-1308.",
    "acemoglu2025": "Acemoglu D. The Simple Macroeconomics of AI[J]. Economic Policy, 2025, 40(121): 13-58.",
    "bryn2025": "Brynjolfsson E, Li D, Raymond L R. Generative AI at Work[J]. The Quarterly Journal of Economics, 2025, 140(2): 889-942.",
    # ==== 2021 年及以前：本主题不可替代的奠基性文献 ====
    "qi2020": "戚聿东,刘翠花,丁述磊.数字经济发展、就业结构优化与就业质量提升[J].经济学动态,2020(11):17-35.",
    "zhao2020": "赵涛,张智,梁上坤.数字经济、创业活跃度与高质量发展——来自中国城市的经验证据[J].管理世界,2020,36(10):65-76.",
    "guo2020": "郭峰,王靖一,王芳,等.测度中国数字普惠金融发展:指数编制与空间特征[J].经济学(季刊),2020,19(4):1401-1418.",
    "wang2020": "王永钦,董雯.机器人的兴起如何影响中国劳动力市场?——来自制造业上市公司的证据[J].经济研究,2020,55(10):159-175.",
    "autor2003": "Autor D H, Levy F, Murnane R J. The Skill Content of Recent Technological Change: An Empirical Exploration[J]. The Quarterly Journal of Economics, 2003, 118(4): 1279-1333.",
    "kahn2010": "Kahn L B. The Long-Term Labor Market Consequences of Graduating from College in a Bad Economy[J]. Labour Economics, 2010, 17(2): 303-316.",
    "autor2013": "Autor D H, Dorn D. The Growth of Low-Skill Service Jobs and the Polarization of the US Labor Market[J]. American Economic Review, 2013, 103(5): 1553-1597.",
    "acemoglu2018": "Acemoglu D, Restrepo P. The Race between Man and Machine: Implications of Technology for Growth, Factor Shares, and Employment[J]. American Economic Review, 2018, 108(6): 1488-1542.",
    "dauth2021": "Dauth W, Findeisen S, Suedekum J, et al. The Adjustment of Labor Markets to Robots[J]. Journal of the European Economic Association, 2021, 19(6): 3104-3153.",
}

SRC = sys.argv[1]
DST = sys.argv[2]
text = open(SRC, encoding="utf-8").read()
order = []


def repl(m):
    keys = [k.strip().lstrip("@") for k in m.group(1).split(";")]
    nums = []
    for k in keys:
        if k not in REFS:
            raise SystemExit(f"未登记的引文键：{k}")
        if k not in order:
            order.append(k)
        nums.append(order.index(k) + 1)
    return rf"^\[{','.join(str(n) for n in nums)}\]^"


text = re.sub(r"\[(@[^\]]+)\]", repl, text)
reflist = "\n\n".join(f"[{i+1}]{REFS[k]}" for i, k in enumerate(order))
text = text.rstrip() + "\n\n" + f'::: {{custom-style="RefItem"}}\n{reflist}\n:::\n'
open(DST, "w", encoding="utf-8").write(text)
print(f"{SRC} → {DST}：共引用 {len(order)} 条文献")
for i, k in enumerate(order, 1):
    print(f"  [{i}] {k}")
