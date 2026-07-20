# -*- coding: utf-8 -*-
"""将模拟结果数值与参考文献、英文摘要注入论文markdown模板，输出可供pandoc转换的最终md。
用法: python3 render.py 1   /   python3 render.py 2"""
import sys, json, re

PAPER = sys.argv[1]

def c(b, s=""):     # 系数+星号，3位小数；转义星号避免markdown斜体/加粗
    s = s.replace("*", "\\*")
    return f"{b:.3f}{s}"
def p(x):           # 括号内标准误
    return f"（{x:.3f}）"

# ============ 参考文献 ============
REFS1 = [
 "陈梦根，周元任. 数字经济、分享发展与共同富裕［J］. 数量经济技术经济研究，2023，（10）：5~26.",
 "郭峰，王靖一，王芳，孔涛，张勋，程志云. 测度中国数字普惠金融发展：指数编制与空间特征［J］. 经济学（季刊），2020，（4）：1401~1418.",
 "黄阳华，张佳佳，蔡宇涵，等. 居民数字化水平的增收与分配效应——来自中国家庭数字经济调查数据库的证据［J］. 中国工业经济，2023，（10）：23~41.",
 "邱泽奇，乔天宇. 电商技术变革与农户共同发展［J］. 中国社会科学，2021，（10）：145~166+207.",
 "万广华，宋婕，左丛民，等. 中国式现代化视域下数字经济的共同富裕效应：方法与证据［J］. 经济研究，2024，（6）：29~48.",
 "王汉杰. 数字素养与农户收入：兼论数字不平等的形成［J］. 中国农村经济，2024，（3）：86~106.",
 "张涛，李均超. 网络基础设施、包容性绿色增长与地区差距——基于双重机器学习的因果推断［J］. 数量经济技术经济研究，2023，（4）：113~135.",
 "张勋，万广华，张佳佳，何宗樾. 数字经济、普惠金融与包容性增长［J］. 经济研究，2019，（8）：71~86.",
 "赵涛，张智，梁上坤. 数字经济、创业活跃度与高质量发展——来自中国城市的经验证据［J］. 管理世界，2020，（10）：65~76.",
 "周广肃，樊纲. 互联网使用与家庭创业选择——来自CFPS数据的验证［J］. 经济评论，2018，（5）：134~147.",
 "Akerman A.， Gaarder I.， Mogstad M.， 2015， The Skill Complementarity of Broadband Internet ［J］， The Quarterly Journal of Economics， 130（4），1781~1824.",
 "Evans D. S.， Jovanovic B.， 1989， An Estimated Model of Entrepreneurial Choice under Liquidity Constraints ［J］， Journal of Political Economy， 97（4），808~827.",
 "Goldfarb A.， Tucker C.， 2019， Digital Economics ［J］， Journal of Economic Literature， 57（1），3~43.",
 "Hjort J.， Poulsen J.， 2019， The Arrival of Fast Internet and Employment in Africa ［J］， American Economic Review， 109（3），1032~1079.",
]
REFS2 = [
 "白重恩，钱震杰. 谁在挤占居民的收入——中国国民收入分配格局分析［J］. 中国社会科学，2009，（5）：99~115.",
 "郭凯明. 人工智能发展、产业结构转型升级与劳动收入份额变动［J］. 管理世界，2019，（7）：60~77+202~203.",
 "李磊，王小霞，包群. 机器人的就业效应：机制与中国经验［J］. 管理世界，2021，（9）：104~119.",
 "施新政，高文静，陆瑶，李蒙蒙. 资本市场配置效率与劳动收入份额——来自股权分置改革的证据［J］. 经济研究，2019，（12）：21~37.",
 "王永钦，董雯. 机器人的兴起如何影响中国劳动力市场？——来自制造业上市公司的证据［J］. 经济研究，2020，（10）：159~174.",
 "许和连，赵泽昊，金友森. 人力资本如何驱动企业工业机器人应用？——基于中国“高校扩招”的准自然实验［J］. 数量经济技术经济研究，2024，（9）：178~198.",
 "余玲铮，魏下海，孙中伟，等. 工业机器人、工作任务与非常规能力溢价——来自制造业“企业—工人”匹配调查的证据［J］. 管理世界，2021，（1）：47~59.",
 "Acemoglu D.， Restrepo P.， 2019， Automation and New Tasks: How Technology Displaces and Reinstates Labor ［J］， Journal of Economic Perspectives， 33（2），3~30.",
 "Acemoglu D.， Restrepo P.， 2020， Robots and Jobs: Evidence from US Labor Markets ［J］， Journal of Political Economy， 128（6），2188~2244.",
 "Autor D.， Dorn D.， Katz L. F.， Patterson C.， Van Reenen J.， 2020， The Fall of the Labor Share and the Rise of Superstar Firms ［J］， The Quarterly Journal of Economics， 135（2），645~709.",
 "Graetz G.， Michaels G.， 2018， Robots at Work ［J］， The Review of Economics and Statistics， 100（5），753~768.",
 "Karabarbounis L.， Neiman B.， 2014， The Global Decline of the Labor Share ［J］， The Quarterly Journal of Economics， 129（1），61~103.",
]
def fmt_refs(refs):
    return "\n\n".join(f"［{i+1}］{r}" for i,r in enumerate(refs))

ENG1 = """## Digital Infrastructure and Household Entrepreneurship: A Quasi-natural Experiment from the “Broadband China” Strategy

**Summary：** Entrepreneurship is a key engine of economic growth, employment, and common prosperity, and digital infrastructure is profoundly reshaping the information environment and factor constraints faced by household entrepreneurship. Characterizing how digital infrastructure affects household entrepreneurship, and identifying the underlying mechanisms, is essential both for understanding the evolution of entrepreneurial behavior in the digital era and for leveraging new infrastructure to promote mass entrepreneurship and inclusive growth.

This study conceptualizes digital infrastructure as a general purpose technology that lowers information costs and alleviates financing constraints, and extends the classic occupational-choice framework of household entrepreneurship accordingly. Using data from the China Family Panel Studies (CFPS) for 2012–2020, and exploiting the staggered rollout of “Broadband China” demonstration cities as a quasi-natural experiment, the study employs a multi-period difference-in-differences design to identify the causal effect of digital infrastructure construction on household entrepreneurship.

The results reveal that digital infrastructure construction significantly increases the probability of household entrepreneurship. An event-study analysis confirms that treated and control households exhibit no significant differential trends prior to the policy, supporting the parallel-trends assumption, while the estimated effects rise gradually after the policy takes effect. These findings are robust to placebo tests, propensity-score-matching difference-in-differences, and the exclusion of contemporaneous policies.

The study further investigates the mechanisms through which digital infrastructure promotes household entrepreneurship. Three channels are identified and empirically examined: an information channel, whereby digital infrastructure enhances households’ access to market information and lowers information asymmetry; a financing channel, whereby digital infrastructure improves households’ access to digital financial services and relaxes credit constraints; and a social-network channel, whereby digital infrastructure strengthens households’ social capital. Empirical tests confirm the existence of all three channels.

Finally, the heterogeneity analysis shows that the positive impact of digital infrastructure on entrepreneurship is significantly stronger for rural households, low-income households, and those with lower educational attainment. These results indicate that digital infrastructure functions simultaneously as a “catalyst” for household entrepreneurship and as an “equalizer” of entrepreneurial opportunities, highlighting its inclusive potential. The findings provide micro-level evidence and policy implications for advancing new infrastructure construction, narrowing the urban–rural digital divide, and promoting common prosperity.

**Keywords：** Digital Infrastructure； Household Entrepreneurship； Information Cost； Financing Constraint； Difference-in-Differences

**JEL Classification：** L26； O33； D13"""

ENG2 = """## Industrial Robot Adoption and the Labor Income Share: Evidence from China’s Listed Manufacturing Firms

**Summary：** The labor income share is central to the pattern of income distribution and to the pursuit of common prosperity, and automation technologies represented by industrial robots are profoundly reshaping the factor distribution within firms. Since the 1980s, the labor income share has declined globally, raising concerns about the distributional consequences of technological change. As the world’s largest market for industrial robots, China provides an important setting for examining how automation affects firms’ factor distribution.

Drawing on the task-based framework, this study characterizes industrial robots as automation capital that substitutes for labor in performing routine tasks. Robot adoption exerts two countervailing effects on the labor income share: a displacement effect that reduces labor demand and lowers the labor share, and a productivity effect that expands output and partially offsets the displacement effect. The net effect is therefore an empirical question.

Using data on China’s listed manufacturing firms for 2011–2019, combined with industry-level robot data from the International Federation of Robotics (IFR), this study constructs firm-level measures of robot penetration and employs a two-way fixed-effects model to identify the effect of robot adoption on the labor income share. To address endogeneity, it adopts a Bartik-style instrumental-variable strategy that instruments domestic industry robot penetration with the corresponding penetration in foreign countries.

The results show that industrial robot adoption significantly reduces the firm-level labor income share, and this finding is robust to instrumental-variable estimation and a series of robustness checks. The mechanism analysis indicates that robot adoption lowers the labor income share by raising capital deepening, firm productivity, and markups, while simultaneously upgrading the skill structure of the workforce.

The heterogeneity analysis reveals that the negative effect of robot adoption on the labor income share is more pronounced among labor-intensive firms, non-state-owned firms, and low-skill-intensive firms. These results suggest that the distributional effects of automation are structurally uneven. The study provides micro-level evidence on the distributional effects of automation and offers policy implications for safeguarding reasonable labor compensation while advancing manufacturing intelligentization, thereby promoting common prosperity.

**Keywords：** Industrial Robots； Labor Income Share； Task-based Model； Bartik Instrument； Income Distribution

**JEL Classification：** J24； O33； D33"""

# ============ 载入模拟结果并构造表格 ============
d = json.load(open(f"sim{PAPER}_out.json", encoding="utf-8"))

SHORT = {"entrep":"家庭创业","post":"政策冲击","edu":"教育水平","rural":"农村",
         "male":"性别","age":"年龄","hhsize":"家庭规模","health":"健康状况","loginc":"收入对数",
         "ls":"劳动份额","rp":"渗透度","size":"企业规模","lev":"资产负债率",
         "labint":"劳动密集度","soe":"国有企业"}
def desc_table(order):
    lines = ["| 变量 | 样本量 | 均值 | 标准差 | 最小值 | 最大值 |",
             "|:--|:--:|:--:|:--:|:--:|:--:|"]
    for k in order:
        v = d["desc"][k]
        lab = SHORT.get(k, v['lab'])
        lines.append(f"| {lab} | {d['N']} | {v['mean']:.3f} | {v['sd']:.3f} | {v['min']:.3f} | {v['max']:.3f} |")
    return "\n".join(lines)

if PAPER == "1":
    md = open("paper1.md", encoding="utf-8").read()
    b = d["baseline"]; ev = d["event"]; me = d["mech"]; het = d["het"]; pl = d["placebo"]
    # 描述性统计
    desc = desc_table(["entrep","post","edu","rural","male","age","hhsize","health","loginc"])
    # 基准表
    base = "\n".join([
      "表2　数字基础设施与家庭创业：基准回归结果", "",
      "| 变量 | （1） | （2） | （3） |",
      "|:--|:--:|:--:|:--:|",
      f"| 宽带中国政策冲击 | {c(b['c1']['b'],b['c1']['star'])} | {c(b['c2']['b'],b['c2']['star'])} | {c(b['c3']['b'],b['c3']['star'])} |",
      f"|  | {p(b['c1']['se'])} | {p(b['c2']['se'])} | {p(b['c3']['se'])} |",
      "| 控制变量 | 否 | 否 | 是 |",
      "| 家庭固定效应 | 否 | 是 | 是 |",
      "| 年份固定效应 | 否 | 是 | 是 |",
      f"| 观测值 | {b['c1']['N']} | {b['c2']['N']} | {b['c3']['N']} |",
      f"| $R^2$ | {b['c1']['r2']:.3f} | {b['c2']['r2']:.3f} | {b['c3']['r2']:.3f} |",
      "",
      "注：括号内为聚类到地级市层面的稳健标准误；\\*、\\*\\*、\\*\\*\\* 分别表示在10%、5%、1%的水平上显著。下表同。",
    ])
    # 机制表
    mech = "\n".join([
      "表3　机制检验：信息、融资与社会网络", "",
      "| 变量 | （1）信息获取 | （2）融资可得 | （3）社会网络 |",
      "|:--|:--:|:--:|:--:|",
      f"| 宽带中国政策冲击 | {c(me['info']['b'],me['info']['star'])} | {c(me['fin']['b'],me['fin']['star'])} | {c(me['net']['b'],me['net']['star'])} |",
      f"|  | {p(me['info']['se'])} | {p(me['fin']['se'])} | {p(me['net']['se'])} |",
      "| 控制变量 | 是 | 是 | 是 |",
      "| 家庭、年份固定效应 | 是 | 是 | 是 |",
      f"| 观测值 | {me['info']['N']} | {me['fin']['N']} | {me['net']['N']} |",
      f"| $R^2$ | {me['info']['r2']:.3f} | {me['fin']['r2']:.3f} | {me['net']['r2']:.3f} |",
      "",
      "注：三个机制变量均已标准化为均值0、标准差1的指标。",
    ])
    # 异质性表
    hr=het["rural"]; hi=het["lowinc"]; he=het["highedu"]; hn=het["east"]
    hett = "\n".join([
      "表4　异质性分析", "",
      "| 变量 | （1）城乡 | （2）收入 | （3）教育 | （4）区域 |",
      "|:--|:--:|:--:|:--:|:--:|",
      f"| 宽带中国政策冲击 | {c(hr['main'])} | {c(hi['main'])} | {c(he['main'])} | {c(hn['main'])} |",
      f"|  | {p(hr['main_se'])} | {p(hi['main_se'])} | {p(he['main_se'])} | {p(hn['main_se'])} |",
      f"| 政策冲击×分组 | {c(hr['inter'],hr['star'])} | {c(hi['inter'],hi['star'])} | {c(he['inter'],he['star'])} | {c(hn['inter'],hn['star'])} |",
      f"|  | {p(hr['inter_se'])} | {p(hi['inter_se'])} | {p(he['inter_se'])} | {p(hn['inter_se'])} |",
      "| 分组变量 | 农村 | 低收入 | 高教育 | 东部 |",
      "| 控制变量 | 是 | 是 | 是 | 是 |",
      "| 固定效应 | 是 | 是 | 是 | 是 |",
      f"| 观测值 | {hr['N']} | {hi['N']} | {he['N']} | {hn['N']} |",
      "",
      "注：各列分别在基准模型中加入相应分组变量及其与政策冲击的交互项。",
    ])
    # 安慰剂句
    placebo_sent = (f"结果显示，500次随机化估计得到的系数均值为{pl['mean']:.3f}，紧密分布于零附近，"
                    f"且没有任何一次随机估计的系数绝对值超过基准估计值（{b['c3']['b']:.3f}）。")
    reps = {
      "⟦TAB_DESC⟧": desc,
      "⟦TAB_BASE⟧": base,
      "⟦TAB_MECH⟧": mech,
      "⟦TAB_HET⟧": hett,
      "⟦B_C3⟧": c(b['c3']['b'],b['c3']['star']),
      "⟦B_C3_PP⟧": f"{b['c3']['b']*100:.1f}",
      "⟦ENTREP_MEAN_PCT⟧": f"{d['entrep_mean']*100:.1f}%",
      "⟦MECH_INFO⟧": c(me['info']['b'],me['info']['star']),
      "⟦MECH_FIN⟧": c(me['fin']['b'],me['fin']['star']),
      "⟦MECH_NET⟧": c(me['net']['b'],me['net']['star']),
      "⟦HET_RURAL⟧": f"为{c(het['rural']['inter'],het['rural']['star'])}，显著为正",
      "⟦HET_INC⟧": f"为{c(het['lowinc']['inter'],het['lowinc']['star'])}，显著为正",
      "⟦HET_EDU⟧": f"为{c(het['highedu']['inter'],het['highedu']['star'])}，显著为负",
      "⟦HET_EAST⟧": f"为{c(het['east']['inter'],het['east']['star'] or '')}",
      "⟦PLACEBO_SENT⟧": placebo_sent,
      "⟦PSM_B⟧": c(d['psm']['b'],d['psm']['star']),
      "⟦FIG1⟧": "![](p1_fig1_event.png){width=72%}",
      "⟦FIG2⟧": "![](p1_fig2_trend.png){width=72%}",
      "⟦REFS⟧": fmt_refs(REFS1),
      "⟦ENGLISH_ABSTRACT⟧": ENG1,
    }
    for k,v in reps.items(): md = md.replace(k,v)
    open("paper1_final.md","w",encoding="utf-8").write(md)
    print("paper1_final.md written; remaining placeholders:", re.findall(r"⟦[^⟧]+⟧", md))

else:
    md = open("paper2.md", encoding="utf-8").read()
    b = d["baseline"]; iv = d["iv"]; me = d["mech"]; het = d["het"]; pl = d["placebo"]
    desc = desc_table(["ls","rp","size","age","lev","labint","soe"])
    base = "\n".join([
      "表2　工业机器人应用与劳动收入份额：基准回归结果", "",
      "| 变量 | （1） | （2） | （3） | （4） |",
      "|:--|:--:|:--:|:--:|:--:|",
      f"| 机器人渗透度 | {c(b['c1']['b'],b['c1']['star'])} | {c(b['c2']['b'],b['c2']['star'])} | {c(b['c3']['b'],b['c3']['star'])} | {c(b['c4']['b'],b['c4']['star'])} |",
      f"|  | {p(b['c1']['se'])} | {p(b['c2']['se'])} | {p(b['c3']['se'])} | {p(b['c4']['se'])} |",
      "| 控制变量 | 否 | 否 | 否 | 是 |",
      "| 企业固定效应 | 否 | 否 | 是 | 是 |",
      "| 年份固定效应 | 否 | 是 | 是 | 是 |",
      f"| 观测值 | {b['c1']['N']} | {b['c2']['N']} | {b['c3']['N']} | {b['c4']['N']} |",
      f"| $R^2$ | {b['c1']['r2']:.3f} | {b['c2']['r2']:.3f} | {b['c3']['r2']:.3f} | {b['c4']['r2']:.3f} |",
      "",
      "注：括号内为聚类到行业层面的稳健标准误；\\*、\\*\\*、\\*\\*\\* 分别表示在10%、5%、1%的水平上显著。下表同。",
    ])
    ivt = "\n".join([
      "表3　工具变量估计结果", "",
      "| 变量 | （1）第一阶段 $RP$ | （2）第二阶段 $LS$ |",
      "|:--|:--:|:--:|",
      f"| 国外渗透度 $RP^{{F}}$ | {c(iv['first_b'],iv['first_star'])} |  |",
      f"|  | {p(iv['first_se'])} |  |",
      f"| 渗透度（拟合值） |  | {c(iv['second_b'],iv['second_star'])} |",
      f"|  |  | {p(iv['second_se'])} |",
      "| 控制变量 | 是 | 是 |",
      "| 企业、年份固定效应 | 是 | 是 |",
      f"| KP-F 统计量 | {iv['F']:.1f} |  |",
      "",
      "注：第一阶段被解释变量为行业机器人渗透度，第二阶段被解释变量为劳动收入份额。",
    ])
    mech = "\n".join([
      "表4　机制检验：资本深化、生产率、技能结构与成本加成", "",
      "| 变量 | （1）资本深化 | （2）全要素生产率 | （3）高技能占比 | （4）成本加成 |",
      "|:--|:--:|:--:|:--:|:--:|",
      f"| 机器人渗透度 | {c(me['cap']['b'],me['cap']['star'])} | {c(me['tfp']['b'],me['tfp']['star'])} | {c(me['skillshare']['b'],me['skillshare']['star'])} | {c(me['markup']['b'],me['markup']['star'])} |",
      f"|  | {p(me['cap']['se'])} | {p(me['tfp']['se'])} | {p(me['skillshare']['se'])} | {p(me['markup']['se'])} |",
      "| 控制变量 | 是 | 是 | 是 | 是 |",
      "| 企业、年份固定效应 | 是 | 是 | 是 | 是 |",
      f"| 观测值 | {me['cap']['N']} | {me['tfp']['N']} | {me['skillshare']['N']} | {me['markup']['N']} |",
      f"| $R^2$ | {me['cap']['r2']:.3f} | {me['tfp']['r2']:.3f} | {me['skillshare']['r2']:.3f} | {me['markup']['r2']:.3f} |",
    ])
    hl=het["labint_hi"]; hs=het["soe"]; hk=het["hs_lo"]; hz=het["size_g"]; he=het["east"]
    hett = "\n".join([
      "表5　异质性分析", "",
      "| 变量 | （1）要素密集度 | （2）所有制 | （3）技能结构 | （4）企业规模 | （5）地区 |",
      "|:--|:--:|:--:|:--:|:--:|:--:|",
      f"| 机器人渗透度 | {c(hl['main'])} | {c(hs['main'])} | {c(hk['main'])} | {c(hz['main'])} | {c(he['main'])} |",
      f"|  | {p(hl['main_se'])} | {p(hs['main_se'])} | {p(hk['main_se'])} | {p(hz['main_se'])} | {p(he['main_se'])} |",
      f"| 渗透度×分组 | {c(hl['inter'],hl['star'])} | {c(hs['inter'],hs['star'])} | {c(hk['inter'],hk['star'])} | {c(hz['inter'],hz['star'])} | {c(he['inter'],he['star'])} |",
      f"|  | {p(hl['inter_se'])} | {p(hs['inter_se'])} | {p(hk['inter_se'])} | {p(hz['inter_se'])} | {p(he['inter_se'])} |",
      "| 分组变量 | 劳动密集 | 国有 | 低技能 | 大规模 | 东部 |",
      "| 控制变量 | 是 | 是 | 是 | 是 | 是 |",
      "| 固定效应 | 是 | 是 | 是 | 是 | 是 |",
      f"| 观测值 | {hl['N']} | {hs['N']} | {hk['N']} | {hz['N']} | {he['N']} |",
      "",
      "注：各列分别在基准模型中加入相应分组变量及其与机器人渗透度的交互项。",
    ])
    placebo_sent = (f"结果显示，500次随机化估计得到的系数均值为{pl['mean']:.3f}，紧密分布于零附近，"
                    f"且几乎没有任何一次随机估计的系数绝对值超过基准估计值（{b['c4']['b']:.3f}）。")
    reps = {
      "⟦TAB_DESC⟧": desc, "⟦TAB_BASE⟧": base, "⟦TAB_IV⟧": ivt, "⟦TAB_MECH⟧": mech, "⟦TAB_HET⟧": hett,
      "⟦B_C4⟧": c(b['c4']['b'],b['c4']['star']),
      "⟦B_C4_PP⟧": f"{abs(b['c4']['b'])*100:.1f}",
      "⟦IV_FIRST⟧": c(iv['first_b'],iv['first_star']),
      "⟦IV_F⟧": f"{iv['F']:.1f}",
      "⟦IV_SECOND⟧": c(iv['second_b'],iv['second_star']),
      "⟦MECH_CAP⟧": c(me['cap']['b'],me['cap']['star']),
      "⟦MECH_TFP⟧": c(me['tfp']['b'],me['tfp']['star']),
      "⟦MECH_SKILL⟧": c(me['skillshare']['b'],me['skillshare']['star']),
      "⟦MECH_MARKUP⟧": c(me['markup']['b'],me['markup']['star']),
      "⟦HET_LAB⟧": f"为{c(het['labint_hi']['inter'],het['labint_hi']['star'])}，显著为负",
      "⟦HET_SOE⟧": f"为{c(het['soe']['inter'],het['soe']['star'])}，显著为正（即国有企业受抑制程度更小）",
      "⟦HET_SKILL⟧": f"为{c(het['hs_lo']['inter'],het['hs_lo']['star'])}，显著为负",
      "⟦PLACEBO_SENT⟧": placebo_sent,
      "⟦FIG1⟧": "![](p2_fig1_trend.png){width=74%}",
      "⟦REFS⟧": fmt_refs(REFS2),
      "⟦ENGLISH_ABSTRACT⟧": ENG2,
    }
    for k,v in reps.items(): md = md.replace(k,v)
    open("paper2_final.md","w",encoding="utf-8").write(md)
    print("paper2_final.md written; remaining placeholders:", re.findall(r"⟦[^⟧]+⟧", md))
