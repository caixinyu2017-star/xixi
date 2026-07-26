# -*- coding: utf-8 -*-
"""将 [@key] 引文按首次出现顺序编号为上标 ^[n]^，并生成《统计与决策》格式的
参考文献著录列表。全部条目均经联网核验为真实文献。"""
import re
import sys

REFS = {
    # —— 首轮联网核验通过（含核验来源，见 refs_verification.md）——
    "tian2022": "田鸽,张勋.数字经济、非农就业与社会分工[J].管理世界,2022,38(5).",
    "qi2020": "戚聿东,刘翠花,丁述磊.数字经济发展、就业结构优化与就业质量提升[J].经济学动态,2020(11).",
    "zhao2020": "赵涛,张智,梁上坤.数字经济、创业活跃度与高质量发展——来自中国城市的经验证据[J].管理世界,2020,36(10).",
    "bai2021": "柏培文,张云.数字经济、人口红利下降与中低技能劳动者权益[J].经济研究,2021(5).",
    "liu2022": "刘翠花.数字经济对产业结构升级和创业增长的影响[J].中国人口科学,2022(2).",
    "yang2022": "杨伟国,吴邦正.平台经济对就业结构的影响[J].中国人口科学,2022(4).",
    "li2024": "李建奇,黄维晨.“数实融合”下的平台经济与包容性就业——基于网络招聘大数据的经验研究[J].财经研究,2024,50(10).",
    "xu2024": "徐明,陈斯洁,聂云蕊.我国青年就业研究的核心议题、演变与展望[J].人口与经济,2024(5).",
    "guo2022": "郭冉,田丰,王露瑶.量减质升:青年就业状况变化及分析(2006—2021)——基于CSS的调查数据[J].中国青年研究,2022(11).",
    "ding2024": "丁述磊,王佳萍,刘翠花.教育错配对青年就业质量的影响:理论与实证[J].中国青年研究,2024(9).",
    "wang2020": "王永钦,董雯.机器人的兴起如何影响中国劳动力市场?——来自制造业上市公司的证据[J].经济研究,2020,55(10).",
    "yu2021": "余玲铮,魏下海,孙中伟,等.工业机器人、工作任务与非常规能力溢价——来自制造业企业—工人匹配调查的证据[J].管理世界,2021,37(1).",
    "autor2003": "Autor D H, Levy F, Murnane R J. The Skill Content of Recent Technological Change: An Empirical Exploration [J]. The Quarterly Journal of Economics, 2003, 118(4).",
    "acemoglu2018": "Acemoglu D, Restrepo P. The Race Between Man and Machine: Implications of Technology for Growth, Factor Shares, and Employment [J]. American Economic Review, 2018, 108(6).",
    "autor2013": "Autor D H, Dorn D. The Growth of Low-Skill Service Jobs and the Polarization of the US Labor Market [J]. American Economic Review, 2013, 103(5).",
    "goos2014": "Goos M, Manning A, Salomons A. Explaining Job Polarization: Routine-Biased Technological Change and Offshoring [J]. American Economic Review, 2014, 104(8).",
    "kahn2010": "Kahn L B. The Long-Term Labor Market Consequences of Graduating From College in a Bad Economy [J]. Labour Economics, 2010, 17(2).",
    "dauth2021": "Dauth W, Findeisen S, Suedekum J, et al. The Adjustment of Labor Markets to Robots [J]. Journal of the European Economic Association, 2021, 19(6).",
    # —— 前期同一会话中已联网核验通过 ——
    "jiang2022": "江小涓,靳景.数字技术提升经济效率:服务分工、产业协同和数实孪生[J].管理世界,2022,38(12).",
    "cai2019": "蔡跃洲,陈楠.新技术革命下人工智能与高质量增长、高质量就业[J].数量经济技术经济研究,2019,36(5).",
    "he2020": "何勤,李雅宁,程雅馨,等.人工智能技术应用对就业的影响及作用机制研究——来自制造业企业的微观证据[J].中国软科学,2020(S1).",
    "wanglinhui2020": "王林辉,胡晟明,董直庆.人工智能技术会诱致劳动收入不平等吗——模型推演与分类评估[J].中国工业经济,2020(4).",
    "guo2019": "郭凯明.人工智能发展、产业结构转型升级与劳动收入份额变动[J].管理世界,2019,35(7).",
    "yao2024": "姚加权,张锟澎,郭李鹏,等.人工智能如何提升企业生产效率?——基于劳动力技能结构调整的视角[J].管理世界,2024,40(2).",
    "zhang2025": "张丹丹,于航,李力行,等.中国人工智能技术暴露度的测算及其对劳动需求的影响——基于大语言模型的新证据[J].管理世界,2025,41(7).",
    "bryn2025": "Brynjolfsson E, Li D, Raymond L R. Generative AI at Work [J]. The Quarterly Journal of Economics, 2025, 140(2).",
    "eloundou2024": "Eloundou T, Manning S, Mishkin P, et al. GPTs are GPTs: Labor Market Impact Potential of LLMs [J]. Science, 2024, 384(6702).",
    "bresnahan1995": "Bresnahan T F, Trajtenberg M. General Purpose Technologies “Engines of Growth”? [J]. Journal of Econometrics, 1995, 65(1).",
    # —— 来自约稿方提供的《统计与决策》已刊论文参考文献列表 ——
    "guo2020": "郭峰,王靖一,王芳,等.测度中国数字普惠金融发展:指数编制与空间特征[J].经济学(季刊),2020,19(4).",
    "han2019": "韩先锋,宋文飞,李勃昕.互联网能成为中国区域创新效率提升的新动能吗[J].中国工业经济,2019(7).",
    "chen2022": "陈晓红,李杨扬,宋丽洁,等.数字经济理论体系与研究展望[J].管理世界,2022,38(2).",
    "qin2022": "秦建群,赵晶晶,王薇.数字经济对产业结构升级影响的中介效应与经验证据[J].统计与决策,2022,38(11).",
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
