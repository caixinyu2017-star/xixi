# -*- coding: utf-8 -*-
"""将 [@key] 引文按首次出现顺序编号为上标 ^[n]^，并按 GB/T 7714 顺序编码制生成
参考文献著录列表。

著录格式：
    期刊  [序号] 作者. 文章名[J]. 期刊名, 出版年, 卷(期): 起止页码.
    专著  [序号] 作者. 书名[M]. 出版地: 出版者, 出版年: 起止页码.

全部条目的作者、年份、卷期与起止页码均经联网核验，核验来源见 refs_verification.md。
"""
import re
import sys

REFS = {
    # ==== 2022 年及以后 ====
    "fang2023": "方锦程,刘颖,高昊宇,等.公共数据开放能否促进区域协调发展?——来自政府数据平台上线的准自然实验[J].管理世界,2023,39(9):124-141.",
    "lirh2025": "李荣华,王娇娇,张磊.公共数据开放的新质生产力效应——基于企业数字创新的视角[J].财经研究,2025,51(2):19-33.",
    "chen2022": "陈晓红,李杨扬,宋丽洁,等.数字经济理论体系与研究展望[J].管理世界,2022,38(2):208-224.",
    "jiang2022a": "江小涓,靳景.数字技术提升经济效率:服务分工、产业协同和数实孪生[J].管理世界,2022,38(12):9-26.",
    "tian2022": "田鸽,张勋.数字经济、非农就业与社会分工[J].管理世界,2022,38(5):72-84.",
    "shao2022": "邵帅,范美婷,杨莉莉.经济结构调整、绿色技术进步与中国低碳转型发展——基于总体技术前沿和空间溢出效应视角的经验考察[J].管理世界,2022,38(2):46-69.",
    "pan2022": "潘旭文,付文林.环境信息公开与地区空气质量——基于PM2.5监测的准自然实验分析[J].财经研究,2022,48(5):110-124.",
    "jiangting2022": "江艇.因果推断经验研究中的中介效应与调节效应[J].中国工业经济,2022(5):100-120.",
    "shen2024": "沈可,孙慧琳.人口老龄化对科技创新的空间效应与异质性影响——基于中国地级市面板数据的分析[J].人口研究,2024,48(2):90-103.",
    "wang2025": "汪伟,王春超.人口转变、人口红利与人口老龄化[J].浙江社会科学,2025(4):4-18.",
    "acemoglu2022": "Acemoglu D, Restrepo P. Tasks, Automation, and the Rise in U.S. Wage Inequality[J]. Econometrica, 2022, 90(5): 1973-2016.",
    "maestas2023": "Maestas N, Mullen K J, Powell D. The Effect of Population Aging on Economic Growth, the Labor Force, and Productivity[J]. American Economic Journal: Macroeconomics, 2023, 15(2): 306-332.",
    # ==== 2021 年及以前：本主题不可替代的奠基性文献 ====
    "zhao2020": "赵涛,张智,梁上坤.数字经济、创业活跃度与高质量发展——来自中国城市的经验证据[J].管理世界,2020,36(10):65-76.",
    "guo2020": "郭峰,王靖一,王芳,等.测度中国数字普惠金融发展:指数编制与空间特征[J].经济学(季刊),2020,19(4):1401-1418.",
    "wang2020": "王永钦,董雯.机器人的兴起如何影响中国劳动力市场?——来自制造业上市公司的证据[J].经济研究,2020,55(10):159-175.",
    "callaway2021": "Callaway B, Sant'Anna P H C. Difference-in-Differences with Multiple Time Periods[J]. Journal of Econometrics, 2021, 225(2): 200-230.",
    "bacon2021": "Goodman-Bacon A. Difference-in-Differences with Variation in Treatment Timing[J]. Journal of Econometrics, 2021, 225(2): 254-277.",
    "sun2021": "Sun L, Abraham S. Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects[J]. Journal of Econometrics, 2021, 225(2): 175-199.",
    "chaise2020": "de Chaisemartin C, D'Haultfoeuille X. Two-Way Fixed Effects Estimators with Heterogeneous Treatment Effects[J]. American Economic Review, 2020, 110(9): 2964-2996.",
    "montiel2019": "Montiel Olea J L, Plagborg-Moller M. Simultaneous Confidence Bands: Theory, Implementation, and an Application to SVARs[J]. Journal of Applied Econometrics, 2019, 34(1): 1-17.",
    "hansen1999": "Hansen B E. Threshold Effects in Non-dynamic Panels: Estimation, Testing, and Inference[J]. Journal of Econometrics, 1999, 93(2): 345-368.",
    "anselin1996": "Anselin L, Bera A K, Florax R, et al. Simple Diagnostic Tests for Spatial Dependence[J]. Regional Science and Urban Economics, 1996, 26(1): 77-104.",
    "leeyu2010": "Lee L F, Yu J. Estimation of Spatial Autoregressive Panel Data Models with Fixed Effects[J]. Journal of Econometrics, 2010, 154(2): 165-185.",
    "acemoglu2018": "Acemoglu D, Restrepo P. The Race between Man and Machine: Implications of Technology for Growth, Factor Shares, and Employment[J]. American Economic Review, 2018, 108(6): 1488-1542.",
    "dauth2021": "Dauth W, Findeisen S, Suedekum J, et al. The Adjustment of Labor Markets to Robots[J]. Journal of the European Economic Association, 2021, 19(6): 3104-3153.",
    "chung1997": "Chung Y H, Fare R, Grosskopf S. Productivity and Undesirable Outputs: A Directional Distance Function Approach[J]. Journal of Environmental Management, 1997, 51(3): 229-240.",
    "oh2010": "Oh D H. A Global Malmquist-Luenberger Productivity Index[J]. Journal of Productivity Analysis, 2010, 34(3): 183-197.",
    "lesage2009": "LeSage J P, Pace R K. Introduction to Spatial Econometrics[M]. Boca Raton: Chapman & Hall/CRC, 2009: 1-374.",
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
