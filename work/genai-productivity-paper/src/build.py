# -*- coding: utf-8 -*-
"""将 paper.md 中的 [@key] 引文按首次出现顺序编号为上标 ^[n]^，
并在"参考文献"标题下生成著录列表，输出 paper_built.md。"""
import re
import sys

REFS = {
    # key: 著录条目（《统计与决策》风格，不含页码）
    "jiang2022": "江小涓,靳景.数字技术提升经济效率:服务分工、产业协同和数实孪生[J].管理世界,2022,38(12).",
    "chenyongwei2023": "陈永伟.超越ChatGPT:生成式AI的机遇、风险与挑战[J].山东大学学报(哲学社会科学版),2023(3).",
    "cai2019": "蔡跃洲,陈楠.新技术革命下人工智能与高质量增长、高质量就业[J].数量经济技术经济研究,2019,36(5).",
    "yao2024": "姚加权,张锟澎,郭李鹏,等.人工智能如何提升企业生产效率?——基于劳动力技能结构调整的视角[J].管理世界,2024,40(2).",
    "he2020": "何勤,李雅宁,程雅馨,等.人工智能技术应用对就业的影响及作用机制研究——来自制造业企业的微观证据[J].中国软科学,2020(S1).",
    "wanglinhui2020": "王林辉,胡晟明,董直庆.人工智能技术会诱致劳动收入不平等吗——模型推演与分类评估[J].中国工业经济,2020(4).",
    "guo2019": "郭凯明.人工智能发展、产业结构转型升级与劳动收入份额变动[J].管理世界,2019,35(7).",
    "zhang2025": "张丹丹,于航,李力行,等.中国人工智能技术暴露度的测算及其对劳动需求的影响——基于大语言模型的新证据[J].管理世界,2025,41(7).",
    "ma2024": "马晔风,陈楠,崔雪彬.生成式人工智能技术如何影响专业型工作?——来自软件工程行业的早期证据[J].劳动经济研究,2024,12(3).",
    "noy2023": "Noy S, Zhang W. Experimental Evidence on the Productivity Effects of Generative Artificial Intelligence [J]. Science, 2023, 381(6654).",
    "peng2023": "Peng S, Kalliamvakou E, Cihon P, et al. The Impact of AI on Developer Productivity: Evidence From GitHub Copilot [R]. arXiv Working Paper No.2302.06590, 2023.",
    "bryn2025": "Brynjolfsson E, Li D, Raymond L R. Generative AI at Work [J]. The Quarterly Journal of Economics, 2025, 140(2).",
    "dellacqua2023": "Dell'Acqua F, McFowland E, Mollick E R, et al. Navigating the Jagged Technological Frontier: Field Experimental Evidence of the Effects of Artificial Intelligence on Knowledge Worker Productivity and Quality [R]. Harvard Business School Working Paper No.24-013, 2023.",
    "eloundou2024": "Eloundou T, Manning S, Mishkin P, et al. GPTs are GPTs: Labor Market Impact Potential of LLMs [J]. Science, 2024, 384(6702).",
    "autor2003": "Autor D H, Levy F, Murnane R J. The Skill Content of Recent Technological Change: An Empirical Exploration [J]. Quarterly Journal of Economics, 2003, 118(4).",
    "acemoglu2018": "Acemoglu D, Restrepo P. The Race Between Man and Machine: Implications of Technology for Growth, Factor Shares, and Employment [J]. American Economic Review, 2018, 108(6).",
    "garicano2000": "Garicano L. Hierarchies and the Organization of Knowledge in Production [J]. Journal of Political Economy, 2000, 108(5).",
    "bresnahan1995": "Bresnahan T F, Trajtenberg M. General Purpose Technologies “Engines of Growth”? [J]. Journal of Econometrics, 1995, 65(1).",
    "brynjolfsson2021": "Brynjolfsson E, Rock D, Syverson C. The Productivity J-Curve: How Intangibles Complement General Purpose Technologies [J]. American Economic Journal: Macroeconomics, 2021, 13(1).",
    "dietvorst2015": "Dietvorst B J, Simmons J P, Massey C. Algorithm Aversion: People Erroneously Avoid Algorithms After Seeing Them Err [J]. Journal of Experimental Psychology: General, 2015, 144(1).",
    "logg2019": "Logg J M, Minson J A, Moore D A. Algorithm Appreciation: People Prefer Algorithmic to Human Judgment [J]. Organizational Behavior and Human Decision Processes, 2019, 151.",
    "fugener2022": "Fügener A, Grahl J, Gupta A, et al. Cognitive Challenges in Human-Artificial Intelligence Collaboration: Investigating the Path Toward Productive Delegation [J]. Information Systems Research, 2022, 33(2).",
    "wang2024": "Wang W, Gao G, Agarwal R. Friend or Foe? Teaming Between Artificial Intelligence and Workers With Variation in Experience [J]. Management Science, 2024, 70(9).",
    "doshi2024": "Doshi A R, Hauser O P. Generative AI Enhances Individual Creativity but Reduces the Collective Diversity of Novel Content [J]. Science Advances, 2024, 10(28).",
}

SRC = sys.argv[1] if len(sys.argv) > 1 else "paper.md"
DST = sys.argv[2] if len(sys.argv) > 2 else "paper_built.md"

text = open(SRC, encoding="utf-8").read()

order = []  # keys by first appearance

def repl(m):
    keys = [k.strip().lstrip("@") for k in m.group(1).split(";")]
    nums = []
    for k in keys:
        if k not in REFS:
            raise SystemExit(f"未登记的引文键：{k}")
        if k not in order:
            order.append(k)
        nums.append(order.index(k) + 1)
    joined = ",".join(str(n) for n in nums)
    return rf"^\[{joined}\]^"

text = re.sub(r"\[(@[^\]]+)\]", repl, text)

# 检查未使用的登记条目
unused = [k for k in REFS if k not in order]
if unused:
    print("警告：以下条目已登记但未被引用，将不会出现在参考文献中：", unused)

reflist = "\n\n".join(f"[{i+1}]{REFS[k]}" for i, k in enumerate(order))
refblock = f'::: {{custom-style="RefItem"}}\n{reflist}\n:::\n'
assert "# 参考文献" in text
text = text.replace("# 参考文献", "# 参考文献").rstrip() + "\n\n" + refblock

open(DST, "w", encoding="utf-8").write(text)
print(f"共引用 {len(order)} 条文献；输出 {DST}")
for i, k in enumerate(order):
    print(f"  [{i+1}] {k}")
