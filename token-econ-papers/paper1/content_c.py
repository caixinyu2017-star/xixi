# -*- coding: utf-8 -*-
"""论文一：第五部分（需求弹性估计与回弹效应分解）、第六部分（异质性、稳健性与
统计口径含义）与第七部分（结论与政策建议）。

一切实证数字由 data/results.json 以 f-string 取出或由其数值直接演算，不手写常数；
宏观公开事实取自 data/facts.md（已进入 results.json 的 anchor 一律走 anchor）。
分析样本为按公开锚校准生成的模拟面板，正文与脚注均已声明。

口径纪律（见 DESIGN.md 第八节）：
  · DWH 检验不能拒绝价格外生，正文只写点估计方向，不写「内生性检验支持使用工具变量」；
  · |ε|>1 的 5% 显著性只依据双向固定效应陈述，2SLS 口径只支持方向；
  · 名义指数低估真实降价，故以名义指数平减会低估真实投入增长。
"""
import json
import os
from math import exp, log

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, 'data', 'results.json'), encoding='utf-8'))

AN = R['anchor']
SB = R['sampleB']
DB = R['descB']
IDX = R['index']
RATE = IDX['rates']
DEC = R['decomp_price']['full']
DEM = R['demand']
IV = R['iv']
REB = R['rebound']
HET = R['hetero']
RB = R['robustB']
RA = R['robustA']
CAL = R['calibration']
REC = R['dgp_recovery']
DT = AN['daily_tokens_wanyi']

# 成本份额写在 results.json 的 iv.design 里（硬件 0.72、电力 0.28），此处解析取用，不手抄
import re as _re
_CS = _re.search(r'成本份额取硬件\s*([0-9.]+)、电力\s*([0-9.]+)', IV['design'])
COST_HW, COST_EL = float(_CS.group(1)), float(_CS.group(2))

FE = DEM['fe_quality_adjusted']
FEN = DEM['fe_nominal']
POA = DEM['pooled_quality_adjusted']
PON = DEM['pooled_nominal']
BIAS = DEM['bias']
CRIT = DEM['critical']
WILD = DEM['wild_bootstrap']
IVM = IV['main']
IVN = IV['nominal']
IVJ = IV['just_identified_hw']
DWH = IV['dwh']
CIV = IV['critical_iv']
RBASE = REB['full']
RIV = REB['full_iv']
RW1 = REB['window_2024Q4_2025Q2']
RW2 = REB['window_2024Q1_2026Q2']

MINUS = '−'          # U+2212，负号一律用它


def n(x, d=4):
    """数值转字符串，负号用 U+2212。"""
    s = f'{abs(float(x)):.{d}f}'
    return (MINUS + s) if float(x) < 0 else s


def pc(x, d=1, signed=False):
    """百分数（输入已是百分点）。"""
    s = f'{abs(float(x)):.{d}f}%'
    if float(x) < 0:
        return MINUS + s
    return ('+' + s) if signed else s


def star(p):
    return '***' if p < 0.01 else ('**' if p < 0.05 else ('*' if p < 0.1 else ''))


def cell(c, se, p, d=4):
    return f'{n(c, d)}{star(p)}\n({se:.{d}f})'


def pv(p, d=3):
    p = float(p)
    return '＜0.001' if p < 0.001 else f'{p:.{d}f}'


def sh(x, d=1):
    """占比（输入为小数）。"""
    return pc(100.0 * float(x), d)


def fold(lnx, d=2):
    return f'{exp(abs(float(lnx))):.{d}f}'


def price_resp(eps, drop=0.10):
    """真实价格下降 drop 后的用量与支出反应（百分点）。"""
    k = 1.0 - drop
    return 100.0 * (k ** eps - 1.0), 100.0 * (k ** (1.0 + eps) - 1.0)


EPS = FE['elasticity']
EPS_IV = IVM['second_stage']['ln_p_adj']['coef']
GAM = FE['z_agent']['coef']
T_UP, E_UP = price_resp(EPS)
T_UP_IV, E_UP_IV = price_resp(EPS_IV)
DEFLATE_GAP = RBASE['dln_T_std'] - RBASE['dln_T_phy']
NET_SHARE = RBASE['net_price_channel'] / RBASE['total_lnE']
NET_SHARE_IV = RIV['net_price_channel'] / RIV['total_lnE']


# ============================================================ 第五部分
def sec5():
    b = []
    a = b.append
    a({'h1': '五、需求弹性估计与回弹效应分解'})

    a({'h2': '（一）需求方程的设定与基准结果'})

    a({'p': f'需求方程即式(6)。被解释变量为行业标准词元用量的对数，'
            f'核心解释变量为该行业面对的质量调整价格的对数，'
            f'控制变量为智能体化程度$z_{{it}}$；'
            f'行业固定效应吸收各行业在规模、任务构成与数字化起点上的固定差异，'
            f'时期固定效应吸收模型能力跃迁、算力扩张与政策推动等共同冲击。'
            f'样本为{SB["n_industry"]}个行业在{SB["quarters"][0]}至{SB["quarters"][1]}共'
            f'{SB["T"]}个季度上的平衡面板，{SB["nobs"]}个观测，'
            f'标准误按行业聚类（{FE["ncluster"]}簇）。'
            f'各行业面对的质量调整价格由其档位使用结构与第四部分估计的效值系数合成，'
            f'故同一季度不同行业的真实价格并不相同；'
            f'剔除两组固定效应之后剩下的正是这一部分变异，弹性由它识别。'})

    a({'p': f'两套口径必须成对使用：质量调整价格对应标准词元用量，'
            f'名义价格对应物理词元用量；混搭估出的既不是真实弹性也不是名义弹性。'
            f'表1乙栏显示，质量调整价格的对数标准差为{DB["ln_p_adj"]["sd"]:.4f}，'
            f'名义价格为{DB["ln_p_nom"]["sd"]:.4f}：'
            f'质量调整之后价格的离散度扩大而非缩小，'
            f'因为效值系数本身在行业间高度分化'
            f'（对数标准差{DB["ln_eta"]["sd"]:.4f}），'
            f'把原先被档位结构掩盖的真实价差释放了出来。'})

    a({'p': f'表4并列报告五个设定，用意在于把口径差别与识别差别分开看。'
            f'第(1)、(2)、(4)列为质量调整价格口径，第(3)、(5)列为名义价格口径，'
            f'口径之别检验推论2；第(1)列为混合最小二乘，第(2)、(3)列为双向固定效应，'
            f'第(4)、(5)列为工具变量两阶段最小二乘'
            f'（two-stage least squares, 2SLS），识别之别检验价格的外生性。'
            f'混合最小二乘只作对照而非识别结果：不含双向固定效应时，'
            f'识别变异几乎全部来自价格与用量的共同时间路径，'
            f'而其标准误反映不出这一脆弱——'
            f'改按季度聚类得到{POA["se_cluster_quarter"]:.4f}，'
            f'与按行业聚类的{POA["ln_p_adj"]["se"]:.4f}几乎相同，'
            f'恰说明问题不在聚类方式而在识别本身。'
            f'本文的基准估计是第(2)列与第(4)列。'})

    rows = [
        ['价格口径', '质量调整', '质量调整', '名义', '质量调整', '名义'],
        ['价格弹性 $\\varepsilon$',
         cell(POA['ln_p_adj']['coef'], POA['ln_p_adj']['se'], POA['ln_p_adj']['p']),
         cell(FE['ln_p_adj']['coef'], FE['ln_p_adj']['se'], FE['ln_p_adj']['p']),
         cell(FEN['ln_p_nom']['coef'], FEN['ln_p_nom']['se'], FEN['ln_p_nom']['p']),
         cell(IVM['second_stage']['ln_p_adj']['coef'],
              IVM['second_stage']['ln_p_adj']['se'],
              IVM['second_stage']['ln_p_adj']['p']),
         cell(IVN['second_stage']['ln_p_nom']['coef'],
              IVN['second_stage']['ln_p_nom']['se'],
              IVN['second_stage']['ln_p_nom']['p'])],
        ['智能体化程度 $\\gamma$',
         cell(POA['z_agent']['coef'], POA['z_agent']['se'], POA['z_agent']['p']),
         cell(FE['z_agent']['coef'], FE['z_agent']['se'], FE['z_agent']['p']),
         cell(FEN['z_agent']['coef'], FEN['z_agent']['se'], FEN['z_agent']['p']),
         cell(IVM['second_stage']['z_agent']['coef'],
              IVM['second_stage']['z_agent']['se'],
              IVM['second_stage']['z_agent']['p']),
         cell(IVN['second_stage']['z_agent']['coef'],
              IVN['second_stage']['z_agent']['se'],
              IVN['second_stage']['z_agent']['p'])],
        ['行业固定效应', '否', '是', '是', '是', '是'],
        ['时期固定效应', '否', '是', '是', '是', '是'],
        ['第一阶段 $F$', '—', '—', '—',
         f'{IVM["first_stage_F"]:.3f}', f'{IVN["first_stage_F"]:.3f}'],
        ['Hansen $J$（$p$ 值）', '—', '—', '—',
         f'{IVM["hansen_J"]["J"]:.4f}\n({IVM["hansen_J"]["p"]:.4f})',
         f'{IVN["hansen_J"]["J"]:.4f}\n({IVN["hansen_J"]["p"]:.4f})'],
        ['$H_{0}$: $\\varepsilon=-1$ 的 $t$', '—', n(CRIT['t_H0_eps_eq_minus1'], 4),
         '—', n(CIV['t_H0_eps_eq_minus1'], 4), '—'],
        ['单侧 $p$ 值', '—', f'{CRIT["p_one_sided"]:.4f}', '—',
         f'{CIV["p_one_sided"]:.4f}', '—'],
        ['观测值', str(POA['n']), str(FE['n']), str(FEN['n']),
         str(IVM['n']), str(IVN['n'])],
        ['聚类数', str(POA['ncluster']), str(FE['ncluster']), str(FEN['ncluster']),
         str(IVM['ncluster']), str(IVN['ncluster'])],
        ['组内 $R^{2}$', f'{POA["r2"]:.4f}', f'{FE["r2_within"]:.4f}',
         f'{FEN["r2_within"]:.4f}', '—', '—'],
    ]
    a({'table': {'caption': '表4　需求价格弹性：基准估计与工具变量估计',
                 'header': ['项', '混合OLS\n(1)', '双向固定\n效应 (2)',
                            '双向固定\n效应 (3)', '2SLS\n(4)', '2SLS\n(5)'],
                 'rows': rows,
                 'note': f'注：被解释变量为标准词元用量的对数（第(3)、(5)列为物理词元'
                         f'用量的对数）。括号内为按行业聚类的稳健标准误。'
                         f'第(1)列的$R^{{2}}$为总$R^{{2}}$，第(2)、(3)列为组内$R^{{2}}$。'
                         f'第(4)、(5)列的工具为算力硬件租金与电价的行业暴露，'
                         f'第一阶段$F$为聚类稳健的联合Wald统计量除以工具个数。'
                         f'$H_{{0}}$: $\\varepsilon=-1$的检验只对两个质量调整口径的基准'
                         f'设定报告，单侧备择为$\\varepsilon<-1$。'}})

    a({'p': f'双向固定效应给出的质量调整口径弹性为{n(EPS)}'
            f'（标准误{FE["ln_p_adj"]["se"]:.4f}），名义口径为{n(FEN["elasticity"])}'
            f'（标准误{FEN["ln_p_nom"]["se"]:.4f}），'
            f'名义口径把弹性的绝对值放大了{pc(BIAS["overstate_pct"], 2)}，'
            f'正是推论2所预言的方向：名义口径把效值改进同时从价格降幅与用量增幅中扣掉，'
            f'式(8)的分子与分母被同一个量压缩，而分母（价格降幅）本身较小，'
            f'相对压缩的幅度更大，商的绝对值因而被抬高。'
            f'混合最小二乘的两个数字同样保持这一次序'
            f'（{n(POA["ln_p_adj"]["coef"])}对{n(PON["ln_p_nom"]["coef"])}），'
            f'但绝对值整体偏大，说明不作任何控制时价格与用量的共同时间趋势'
            f'会被整个记到弹性头上。'})

    a({'p': f'弹性的量级需要落到可感知的尺度上。以第(2)列为准，'
            f'质量调整价格每下降10%，行业的标准词元用量上升{pc(T_UP, 1)}，'
            f'智能服务支出上升{pc(E_UP, 1)}；'
            f'临界量$\\mathrm{{d}}\\ln E/\\mathrm{{d}}\\ln\\tilde{{p}}=1+\\varepsilon='
            f'{n(CRIT["dlnE_dlnp"])}$小于零，命题2的条件成立。'
            f'检验$H_{{0}}$: $\\varepsilon=-1$得$t={n(CRIT["t_H0_eps_eq_minus1"], 4)}$，'
            f'单侧$p$值{CRIT["p_one_sided"]:.4f}；考虑到聚类数只有{WILD["ncluster"]}个，'
            f'另做野聚类自助法（$B={WILD["B"]}$）重做推断，'
            f'$p$值为{WILD["p_wild"]:.3f}，两种推断都在5%的水平上拒绝弹性等于$-1$。'
            f'这是本文关于$|\\varepsilon|>1$的显著性证据的全部来源。'
            f'换一个更直观的说法：真实价格若降到原来的一半，'
            f'标准词元用量将增至约{(0.5 ** EPS):.2f}倍，'
            f'而支出不降反升约{pc(price_resp(EPS, 0.5)[1], 1)}。'
            f'降价没有省钱，只是把预算配置到了更多的任务上。'})

    a({'p': f'弹性绝对值大于1的经济来源值得点明。'
            f'智能服务的需求不是对某一件既定商品的需求，'
            f'而是对认知任务承接能力的派生需求。真实价格下行不只是让企业'
            f'在原有任务上多买几枚词元，更是把一批原先由人工完成、'
            f'或因不划算而干脆不做的任务推过替代的临界点，'
            f'需求因而在广延边际上扩张。'
            f'任务层面的实验与实地证据显示，生成式模型能在写作、编码与客服等'
            f'一大批任务上直接替代或加速人工{{c:noy2023}}{{c:brynjolfsson2025}}，'
            f'可被推过临界点的任务存量相当庞大，'
            f'这正是弹性绝对值可以稳定大于1的微观基础。'
            f'智能体化程度的系数为{n(GAM)}（标准误{FE["z_agent"]["se"]:.4f}，'
            f'$p$值{FE["z_agent"]["p"]:.3f}），在5%的水平上显著；'
            f'样本期内该指数对应的加权词元消耗倍数由'
            f'{CAL["agent_multiple_check"]["implied_multiple_first"]:.2f}倍升至'
            f'{CAL["agent_multiple_check"]["implied_multiple_last"]:.2f}倍，'
            f'落在公开记录的单轮问答1倍与多智能体系统约'
            f'{AN["agent_multiple"]["multi_agent"]:.0f}倍之间。'
            f'这一通道与价格无关，若并入弹性，回弹的强度会被系统性高估{c_rebound()}。'})

    a({'h2': '（二）成本推移工具变量'})

    a({'p': f'价格在这里未必外生。第二部分记述的峰谷分时定价'
            f'把一个原本就存在的机制显性化了：'
            f'高峰时段的限流、降级与重试同样会抬高完成同一件任务的实际支出，'
            f'只是不写在价目表上。'
            f'行业自身的需求冲击因而会经由排队拥塞与时段结构进入其有效购进价格，'
            f'使价格与扰动项正相关，双向固定效应估计的弹性绝对值因此向零偏。'
            f'{{fn:本文的分析样本按公开锚校准生成，'
            f'其数据生成过程中把行业需求冲击进入有效购进价格的传导系数设为'
            f'{REC["demand"]["endogeneity"]["phi_congestion"]:.2f}。'
            f'该系数是模拟设定的参数，不是对真实市场的估计。}}'
            f'处理办法是找到只从供给侧推动价格、且不直接进入行业用量方程的变动。'})

    a({'p': f'本文采用份额—移动式（Bartik）成本推移工具：份额为各行业基期推理算力在东、中、西、'
            f'东北四个地区的分布，移动为各地区的算力硬件租金指数与电价指数，'
            f'成本份额取硬件{COST_HW:.2f}、电力{COST_EL:.2f}。'
            f'行业$i$在期$t$的成本暴露为'})
    a({'eq': r'B_{it}^{k}=\sum_{r}s_{ir,0}\,\Delta\ln c_{rt}^{k},'
             r'\qquad k\in\{\mathrm{hw},\ \mathrm{el}\}', 'num': '14'})
    a({'p': f'其中$s_{{ir,0}}$为行业$i$基期算力落在地区$r$的份额，'
            f'$c_{{rt}}^{{k}}$为地区$r$的第$k$类成本指数。'
            f'两个暴露变量均已在行业与时期两个维度上去均值，'
            f'故其变异来自份额结构与地区成本移动的交互，而非全国性的成本共同趋势。'
            f'这一构造的现实基础是算力供给的地区不均衡：'
            f'第二部分引述的官方数据显示，东、中、西、东北地区的智算规模占比分别为'
            f'{pc(100 * AN["region_share"]["east"], 1)}、'
            f'{pc(100 * AN["region_share"]["central"], 1)}、'
            f'{pc(100 * AN["region_share"]["west"], 1)}与'
            f'{pc(100 * AN["region_share"]["northeast"], 1)}，'
            f'地区间的电价与机架租金差异由此转化为供给方成本的横截面差异'
            f'{{c:xu2025}}{{c:caict2025}}。第一阶段方程为'})
    a({'eq': r'\ln\tilde{p}_{it}=\theta_{\mathrm{hw}}B_{it}^{\mathrm{hw}}'
             r'+\theta_{\mathrm{el}}B_{it}^{\mathrm{el}}+\gamma_{1}z_{it}'
             r'+\mu_{i}+\lambda_{t}+v_{it}', 'num': '15'})

    a({'p': f'排他性不能由数据检验，只能由构造与制度事实来论证。'
            f'行业并不直接购买机架与电力，其算力使用经由供给方的服务合约中介，'
            f'因此地区成本移动影响行业词元用量的唯一自然通道就是购进价格。'
            f'两处可能的漏洞需要言明：若某行业本身即算力硬件或电力的生产者，'
            f'成本移动会经营收渠道直接影响其自身用量；'
            f'若基期算力份额与行业的长期增长路径相关，份额本身可能携带趋势。'
            f'本文以时期固定效应与暴露变量的双向去均值缓解前者，'
            f'后者则要求份额的外生性只在增量意义上成立，是份额—移动式工具的一般代价。'
            f'过度识别检验只能检验两个工具是否一致，'
            f'在至少一个工具有效的前提下才有解释力，不能证明工具集整体外生。'})

    a({'p': f'第一阶段的结果支持工具的相关性。硬件租金暴露的系数为'
            f'{n(IVM["first_stage"]["B_hw"]["coef"])}'
            f'（标准误{IVM["first_stage"]["B_hw"]["se"]:.4f}），电价暴露为'
            f'{n(IVM["first_stage"]["B_el"]["coef"])}'
            f'（标准误{IVM["first_stage"]["B_el"]["se"]:.4f}），'
            f'两者均为正号——成本上行推高购进价格。'
            f'聚类稳健的联合$F$统计量为{IVM["first_stage_F"]:.3f}，'
            f'既高于常用的10这一经验界，也高于两工具情形下'
            f'Stock–Yogo 10%偏误临界值{IVM["weak_iv"]["stock_yogo_10pct"]:.2f}。'
            f'过度识别的Hansen $J$统计量为{IVM["hansen_J"]["J"]:.4f}'
            f'（$p$值{IVM["hansen_J"]["p"]:.4f}），不能拒绝两个工具同时外生；'
            f'仅用硬件租金一个工具的恰好识别估计为{n(IVJ["second_stage"]["ln_p_adj"]["coef"])}，'
            f'与两工具结果几乎重合。'})

    a({'p': f'2SLS的质量调整口径弹性为{n(EPS_IV)}'
            f'（标准误{IVM["second_stage"]["ln_p_adj"]["se"]:.4f}），'
            f'绝对值大于双向固定效应的{n(EPS)}；'
            f'名义口径为{n(IVN["second_stage"]["ln_p_nom"]["coef"])}'
            f'（标准误{IVN["second_stage"]["ln_p_nom"]["se"]:.4f}），'
            f'与质量调整口径已相当接近。两口径在工具变量下的收敛本身就是一条旁证：'
            f'成本推移只挑出与效值改进无关的供给侧价格变动，'
            f'当被利用的价格变异不再携带质量信息时，'
            f'用名义价格还是用质量调整价格自然差别不大；'
            f'反过来说，双向固定效应下两口径相差{pc(BIAS["overstate_pct"], 2)}，'
            f'这一差距只能归于质量改进与档位替代被计入了名义价格。'})

    a({'p': f'但内生性的证据到此为止，不宜再往前推一步。'
            f'以控制函数形式做的Durbin–Wu–Hausman检验给出的系数为'
            f'{n(DWH["cf_coef"])}（标准误{DWH["cf_se"]:.4f}，'
            f'$t={n(DWH["cf_t"], 4)}$，$p$值{DWH["cf_p"]:.3f}），'
            f'在常规水平上{b_no_reject()}；'
            f'{SB["n_industry"]}个行业的聚类稳健推断本就检验力有限，'
            f'这一结果既不能证明价格外生，也不能证明价格内生。'
            f'因此本文的表述限于：2SLS的点估计绝对值大于双向固定效应，'
            f'方向与拥塞加价所隐含的向零偏一致，'
            f'工具变量的作用是方向性佐证，而非经检验确立的必要修正。'
            f'这一克制在显著性陈述上同样必须坚持：工具变量口径的临界量为'
            f'$1+\\varepsilon={n(CIV["dlnE_dlnp"])}$，'
            f'检验$H_{{0}}$: $\\varepsilon=-1$得$t={n(CIV["t_H0_eps_eq_minus1"], 4)}$，'
            f'单侧$p$值{CIV["p_one_sided"]:.4f}——点估计支持$|\\varepsilon|>1$，'
            f'但标准误更大，未达5%的水平。'
            f'本文关于$|\\varepsilon|>1$在5%水平上显著的结论，只依据双向固定效应估计；'
            f'工具变量口径只支持点估计的方向。'
            f'两个口径的点估计分别为{n(EPS_IV)}与{n(EPS)}，均在$-1$以下。'})

    a({'p': f'模拟面板还允许做一件真实数据做不到的事——直接检验估计量能否找回真值。'
            f'在弹性异质的设定下，双向固定效应最小二乘的估计目标不是各行业弹性的算术平均'
            f'（{n(REC["demand"]["eps_true_mean"])}），'
            f'而是以各行业价格组内方差为权的加权平均'
            f'（{n(REC["demand"]["eps_true_varweighted"])}）。以后者为基准，'
            f'双向固定效应估计距真值{REC["demand"]["z_fe_vs_weighted"]:.3f}个标准误，'
            f'2SLS距真值{REC["demand"]["z_2sls_vs_weighted"]:.2f}个标准误：'
            f'成本推移工具把偏误基本消掉。'
            f'这只说明估计量在本文设定的环境中表现如何，'
            f'不能代替真实数据上的识别检验。图3汇总各设定的估计。'})

    a({'fig': 'figs/fig3.png',
       'caption': '图3　需求弹性估计的系数图（含工具变量与分组）',
       'source': '资料来源：作者依据式(6)、式(14)与式(15)对校准生成的模拟面板估计。',
       'note': f'注：横轴为需求价格弹性，误差棒为按行业聚类稳健标准误算得的95%置信区间，'
               f'虚线为$\\varepsilon={MINUS}1$参考线。'
               f'上三行为全样本设定，下两行为分组估计，组间差异的检验见第六部分。'})

    a({'h2': '（三）支出变化的回弹分解'})

    a({'p': f'弹性与临界条件确立之后，回弹分解要回答的是量级问题：'
            f'支出的实际增长中，有多少经由价格通道，有多少与价格无关。'
            f'窗口取{RBASE["window"][0]}至{RBASE["window"][1]}，'
            f'区间内智能服务支出的对数变化为{n(RBASE["total_lnE"])}；'
            f'同期质量调整价格的对数变化为{n(RBASE["dln_p_adj"])}，'
            f'标准词元用量为{n(RBASE["dln_T_std"])}；'
            f'若改用名义口径，价格为{n(RBASE["dln_p_nom"])}、'
            f'物理词元用量为{n(RBASE["dln_T_phy"])}。'
            f'两套口径给出同一个支出变化，却给出很不相同的价格与数量分工，'
            f'这是命题1在支出侧的直接体现。'})

    a({'p': f'按式(7)分解，价格效应为{n(RBASE["decomp4"]["price_effect"])}个对数点'
            f'（占支出总变化的{sh(RBASE["share4"]["price_effect"])}）：'
            f'若用量不变，仅真实价格的下行就会把支出压低到原来的'
            f'{100 * exp(RBASE["decomp4"]["price_effect"]):.2f}%。'
            f'纯回弹效应为{n(RBASE["decomp4"]["pure_rebound"])}，占'
            f'{sh(RBASE["share4"]["pure_rebound"])}；'
            f'任务复杂化效应为{n(RBASE["decomp4"]["task_complexity"])}，占'
            f'{sh(RBASE["share4"]["task_complexity"])}，'
            f'相当于把用量放大{fold(RBASE["decomp4"]["task_complexity"])}倍；'
            f'共同扩散与其他数量效应为{n(RBASE["decomp4"]["diffusion_other"])}，占'
            f'{sh(RBASE["share4"]["diffusion_other"])}；四项加总与总变化之差在机器精度内为零。'
            f'前两项同源于同一个价格变化，后两项则与该行业面对的价格无关；'
            f'混在一起就分不清哪一部分是价格政策可以撬动的。'})

    a({'p': f'关键的一项是前两项之和。价格效应与纯回弹效应相加得'
            f'{n(RBASE["net_price_channel"])}个对数点，'
            f'占支出总变化的{sh(NET_SHARE)}，'
            f'折合支出增长{pc(RBASE["net_price_channel_pct"], 2)}。'
            f'这就是背离的定量条件：即使把任务复杂化与市场扩散全部剥离，'
            f'单靠价格通道本身也足以让支出上升约四倍。'
            f'能源经济学称之为超回弹，其成立只取决于$|\\varepsilon|$是否大于1'
            f'{c_rebound()}，与扩散速度无关。'
            f'弹性口径的选择不改变这一结论，只改变量级：'
            f'改用第(4)列2SLS的弹性与智能体化系数重算，纯回弹效应升至'
            f'{n(RIV["decomp4"]["pure_rebound"])}（占'
            f'{sh(RIV["share4"]["pure_rebound"])}），'
            f'价格通道净效应升至{n(RIV["net_price_channel"])}'
            f'（占{sh(NET_SHARE_IV)}，折合支出增长'
            f'{pc(RIV["net_price_channel_pct"], 2)}），'
            f'共同扩散与其他数量效应相应降至{n(RIV["decomp4"]["diffusion_other"])}。'
            f'由于双向固定效应的弹性绝对值向零偏，'
            f'基准分解中的纯回弹是下界、扩散项是上界；'
            f'两套口径的价格通道净效应同号且都远离零。图4与表5并列报告二者。'})

    a({'fig': 'figs/fig4.png',
       'caption': '图4　支出变化的回弹分解瀑布图',
       'source': '资料来源：作者依据式(7)与表4的弹性估计对校准生成的模拟面板计算。',
       'note': f'注：纵轴为对数变化，右轴为占支出总变化的比重，'
               f'窗口为{RBASE["window"][0]}至{RBASE["window"][1]}。'
               f'实心柱为基准口径（双向固定效应弹性$\\varepsilon={n(EPS)}$），'
               f'斜纹柱为工具变量口径（$\\varepsilon={n(EPS_IV)}$）；'
               f'价格通道净效应为价格效应与纯回弹效应之和。'})

    def r4(label, key):
        return [label,
                n(RBASE['decomp4'][key]), sh(RBASE['share4'][key]),
                n(RIV['decomp4'][key]), sh(RIV['share4'][key])]

    rows = [
        ['支出总变化', n(RBASE['total_lnE']), '100.0%',
         n(RIV['total_lnE']), '100.0%'],
        r4('价格效应', 'price_effect'),
        r4('纯回弹效应', 'pure_rebound'),
        r4('任务复杂化效应', 'task_complexity'),
        ['共同扩散与其他', n(RBASE['decomp4']['diffusion_other']),
         sh(RBASE['share4']['diffusion_other']),
         n(RIV['decomp4']['diffusion_other']),
         sh(RIV['share4']['diffusion_other'])],
        ['价格通道净效应', n(RBASE['net_price_channel']), sh(NET_SHARE),
         n(RIV['net_price_channel']), sh(NET_SHARE_IV)],
        ['恒等式误差', f'{abs(RBASE["identity_gap4"]):.4f}', '—',
         f'{abs(RIV["identity_gap4"]):.4f}', '—'],
    ]
    a({'table': {'caption': '表5　支出变化的回弹分解',
                 'header': ['项', f'基准口径\n$\\varepsilon={n(EPS)}$', '占总变化',
                            f'工具变量口径\n$\\varepsilon={n(EPS_IV)}$', '占总变化'],
                 'rows': rows,
                 'note': f'注：窗口为{RBASE["window"][0]}至{RBASE["window"][1]}，'
                         f'各项为对数变化，占比以支出总变化为分母。'
                         f'价格效应为质量调整价格的对数变化，'
                         f'纯回弹效应为弹性与价格效应之积，'
                         f'任务复杂化效应为智能体化系数与其均值变化之积；'
                         f'价格通道净效应为前两项之和，两口径分别折合支出增长'
                         f'{pc(RBASE["net_price_channel_pct"], 2)}与'
                         f'{pc(RIV["net_price_channel_pct"], 2)}。'
                         f'两列的支出总变化与价格效应相同，'
                         f'差别来自所用的弹性与智能体化系数：'
                         f'基准列取表4第(2)列，工具变量列取第(4)列。'}})

    a({'p': f'共同扩散与其他数量效应这一项容易被误读。'
            f'它来自时期固定效应的变化，把模型能力的公共跃迁、新场景的涌现、'
            f'政策推动与企业内部采纳节奏一并吸收，'
            f'其中绝大部分与任何单一行业面对的价格无关：'
            f'全国日均词元调用量两年放大约{DT["2026Q1"] / DT["2024Q1"]:.0f}倍，'
            f'这样的量级跃迁不是价格弹性所能承载的。'
            f'若把这一项算进回弹，本文样本上的回弹率会由{abs(EPS):.4f}升到'
            f'{abs(RBASE["decomp3"]["pure_rebound"] + RBASE["decomp3"]["nonprice_quantity"]) / abs(RBASE["decomp3"]["price_effect"]):.4f}，'
            f'数字更醒目，却不再是任何一个可用于政策推演的参数。'})

    a({'p': f'把窗口缩短可以看到通道权重的变化。'
            f'{RW1["window"][0]}至{RW1["window"][1]}的半年内，支出增长'
            f'{pc(RW1["total_pct"], 1)}，价格通道净效应仅'
            f'{n(RW1["net_price_channel"])}'
            f'（折合支出增长{pc(RW1["net_price_channel_pct"], 2)}），'
            f'扩散项占到{sh(RW1["share4"]["diffusion_other"])}；'
            f'把起点后移到{RW2["window"][0]}，价格通道净效应为'
            f'{n(RW2["net_price_channel"])}，扩散项占'
            f'{sh(RW2["share4"]["diffusion_other"])}。'
            f'越是靠近扩散最猛烈的时段，价格通道的相对权重越低；'
            f'而在全样本这一较长的窗口上，价格通道重新占到支出总变化的{sh(NET_SHARE)}。'
            f'回弹的度量因此对窗口高度敏感，报告回弹率时必须写明区间。'
            f'需要说明的是，公开调研记录的企业接口支出同期半年增长约'
            f'{pc(100 * AN["api_spend_halfyear_growth"], 0)}，'
            f'为美国市场、美元口径且只含接口支出，'
            f'与本文人民币口径的全口径支出不可相除、不可互相校验，只作方向性对照。'})

    return b


# ============================================================ 第六部分
def sec6():
    b = []
    a = b.append
    a({'h1': '六、异质性、稳健性与统计口径含义'})

    a({'h2': '（一）弹性的异质性'})

    ab, fs = HET['ai_base'], HET['firm_size']
    a({'p': f'总量弹性是各行业弹性的加权平均，其背后的分布同样有政策含义。'
            f'本文按两个维度分组重估式(6)：一是行业智能化基础，'
            f'以其标准化取值的中位数（{n(ab["median"], 4)}）为界；'
            f'二是企业规模结构，以大型企业用量占比的中位数（{fs["median"]:.3f}）为界；'
            f'每组各{ab["high"]["n"]}个观测、{ab["high"]["ncluster"]}个行业，'
            f'组间差异以两组系数之差的$z$统计量检验。'
            f'这两个维度分别对应把降价转化为用量的两类前提：'
            f'任务是否已被拆解为模型可以承接的形态，'
            f'以及企业是否具备把新价格迅速落到生产流程上的组织能力。'
            f'结果见表6甲栏。'})

    a({'p': f'智能化基础高的行业弹性为{n(ab["high"]["coef"])}'
            f'（标准误{ab["high"]["se"]:.4f}），低的行业为{n(ab["low"]["coef"])}'
            f'（标准误{ab["low"]["se"]:.4f}），相差{n(ab["diff"]["coef"])}，'
            f'$z={n(ab["diff"]["z"], 4)}$，$p$值{ab["diff"]["p"]:.3f}，'
            f'在5%的水平上显著。这一差别符合任务改造的成本逻辑：'
            f'已经把业务流程拆解为可由模型承接的任务模块的行业，'
            f'把降价转化为新用量所需的额外投入很小；'
            f'尚未完成这一步的行业则仍受制于数据接口、流程改造与人员适配等互补投入'
            f'{{c:yao2024}}{{c:huang2024}}。'
            f'值得注意的是低组弹性的绝对值仅{abs(ab["low"]["coef"]):.4f}，'
            f'与临界值$-1$的距离不足一个标准误，即在统计上无法与$-1$区分：'
            f'在这些行业，降价是否推高支出并无把握，价格通道净效应至多很薄。'})

    a({'p': f'企业规模结构给出同向但更弱的结果。大型企业用量占比高的行业弹性为'
            f'{n(fs["high"]["coef"])}（标准误{fs["high"]["se"]:.4f}），'
            f'占比低的行业为{n(fs["low"]["coef"])}'
            f'（标准误{fs["low"]["se"]:.4f}），相差{n(fs["diff"]["coef"])}，'
            f'$z={n(fs["diff"]["z"], 4)}$，$p$值{fs["diff"]["p"]:.3f}，'
            f'仅在10%的水平上边际显著，不宜过度解读。'
            f'可作的谨慎判断是：规模企业有工程团队把价格下行转化为新场景，'
            f'中小企业则更多依赖第三方平台的现成能力'
            f'{{c:destefano2025}}{{c:xiong2023}}。'})

    a({'p': f'异质性的政策含义与直觉相反。若把降价视为普惠的成本红利，'
            f'那么弹性越大的行业越能把红利转化为用量，'
            f'降价本身就会拉开行业之间智能化程度的差距。'
            f'这意味着单靠价格下行不足以缩小行业间的采纳鸿沟：'
            f'对低弹性行业而言，制约用量的不是价格而是流程改造、'
            f'数据接口与人员适配等互补投入。'
            f'还须说明的是，在斜率异质的面板中，双向固定效应估计量收敛到'
            f'以各行业价格组内方差为权的加权平均而非简单平均'
            f'（本文数据生成过程中前者为{n(REC["demand"]["eps_true_varweighted"])}，'
            f'后者为{n(REC["demand"]["eps_true_mean"])}），'
            f'故报告总量弹性时须同时说明其权重含义，'
            f'否则容易被读成代表性行业的弹性。'})

    a({'h2': '（二）稳健性'})

    a({'p': f'表6乙栏列出弹性的八个稳健性设定。'
            f'需求面板止于2026年第二季度，结构性提价落在窗口之外，'
            f'相应的检验是剔除样本末两个季度，弹性为{n(RB["drop_turn"]["elasticity"])}；'
            f'剔除用量最大的三个行业为{n(RB["drop_top3"]["elasticity"])}，'
            f'加入档位结构控制为{n(RB["add_structure"]["elasticity"])}，'
            f'加入行业特定线性时间趋势为{n(RB["ind_trend"]["elasticity"])}，'
            f'仅用{SB["quarters"][0]}至2025Q2的早期样本为'
            f'{n(RB["early_sample"]["elasticity"])}。'
            f'改按季度聚类不改变点估计，只把标准误由'
            f'{FE["ln_p_adj"]["se"]:.4f}降到'
            f'{RB["cluster_quarter"]["ln_p_adj"]["se"]:.4f}，'
            f'可见按行业聚类更保守。'
            f'八个设定的点估计落在[{n(RB["ind_trend"]["elasticity"])}, '
            f'{n(RB["dynamic"]["long_run"]["coef"])}]之间，全部小于$-1$。'
            f'其中两个设定尤其值得注意：加入档位结构控制之后弹性并未向零收缩，'
            f'说明识别出的用量反应不只是行业在档位之间的重新配置；'
            f'加入行业特定线性时间趋势之后绝对值反而略有上升，'
            f'说明基准结果并非由行业增长趋势与价格下行的偶然同向所致。'})

    a({'p': f'动态设定值得单独一提。加入价格的一期滞后后，'
            f'当期系数为{n(RB["dynamic"]["ln_p_adj"]["coef"])}'
            f'（标准误{RB["dynamic"]["ln_p_adj"]["se"]:.4f}），'
            f'滞后项系数为{n(RB["dynamic"]["ln_p_adj_l1"]["coef"])}'
            f'（标准误{RB["dynamic"]["ln_p_adj_l1"]["se"]:.4f}）而不显著，'
            f'长期弹性为{n(RB["dynamic"]["long_run"]["coef"])}'
            f'（标准误{RB["dynamic"]["long_run"]["se"]:.4f}）。'
            f'长期与当期弹性接近，意味着用量对价格的调整在当季基本完成。'
            f'这与智能服务的技术特征相符：切换档位或扩大调用规模不需要重资产投入。'
            f'回弹的时间形态因而与能源不同——'
            f'能源效率改进的回弹要经由设备更替缓慢释放，'
            f'词元价格下行的回弹则几乎在同一期内完成，'
            f'这意味着价格政策的效果会来得很快、退得也很快。'})

    a({'p': f'价格指数一侧同样做了两项检验。剔除2026年7月与8月的结构转向期后重估享乐方程，'
            f'质量调整指数在2026年6月的年均降幅为'
            f'{RA["drop_break"]["rate"]["annual_fold"]:.3f}倍'
            f'（累计{pc(RA["drop_break"]["rate"]["total_pct"], 3)}），'
            f'与全样本的{RATE["STPI"]["annual_fold"]:.3f}倍几无差别；'
            f'改用中位数回归估计享乐方程，'
            f'指数期末水平为{RA["median_reg"]["stpi_2026_06"]:.4f}，'
            f'年均降幅{RA["median_reg"]["rate"]["annual_fold"]:.3f}倍。'
            f'两项检验说明第四部分的指数结论既不由结构转向期驱动，也不由少数极端报价驱动。'
            f'至于结构断点本身，分时定价意味着同一档位在同一月内存在多个价格，'
            f'若采集时只取其一，指数就会出现与买方真实购进成本无关的跳变；'
            f'相应的处理是按时段用量加权采集并显式标注断点，'
            f'而不是把它当作异常值平滑掉。'
            f'以上各项只能表明结论对设定不敏感，无法弥补识别本身的局限。'})

    rows = []
    rows.append([f'甲栏：异质性分组（分组变量的中位数为界）', '', '', '', ''])
    for lab, d in (('行业智能化基础', ab), ('企业规模结构', fs)):
        rows.append([f'　{lab}：高组', n(d['high']['coef']),
                     f'{d["high"]["se"]:.4f}', pv(d['high']['p']), str(d['high']['n'])])
        rows.append([f'　{lab}：低组', n(d['low']['coef']),
                     f'{d["low"]["se"]:.4f}', pv(d['low']['p']), str(d['low']['n'])])
        rows.append([f'　{lab}：组间差异', n(d['diff']['coef']),
                     f'{d["diff"]["se"]:.4f}', pv(d['diff']['p']),
                     str(d['high']['n'] + d['low']['n'])])
    rows.append(['乙栏：稳健性设定（双向固定效应，质量调整价）', '', '', '', ''])
    RB_LABEL = {'drop_turn': '剔除样本末两个季度（2026Q1—Q2）'}
    for key in ('drop_turn', 'drop_top3', 'add_structure', 'ind_trend',
                'cluster_quarter', 'early_sample'):
        d = RB[key]
        rows.append(['　' + RB_LABEL.get(key, d['label']), n(d['elasticity']),
                     f'{d["ln_p_adj"]["se"]:.4f}', pv(d['ln_p_adj']['p']),
                     str(d['n'])])
    dy = RB['dynamic']
    rows.append(['　动态设定：当期弹性', n(dy['ln_p_adj']['coef']),
                 f'{dy["ln_p_adj"]["se"]:.4f}', pv(dy['ln_p_adj']['p']), str(dy['n'])])
    rows.append(['　动态设定：长期弹性', n(dy['long_run']['coef']),
                 f'{dy["long_run"]["se"]:.4f}', pv(dy['long_run']['p']), str(dy['n'])])
    a({'table': {'caption': '表6　异质性与稳健性检验',
                 'header': ['设定或分组', '价格弹性 $\\varepsilon$', '标准误',
                            '$p$ 值', '观测值'],
                 'rows': rows,
                 'note': f'注：各行均为式(6)的双向固定效应估计，'
                         f'被解释变量为标准词元用量的对数，'
                         f'除注明外标准误按行业聚类。'
                         f'甲栏的组间差异为高组系数减低组系数，'
                         f'其$p$值由两组独立估计的$z$检验给出。'
                         f'乙栏动态设定的长期弹性为当期系数与滞后系数之和。'
                         f'基准设定的弹性为{n(EPS)}（标准误'
                         f'{FE["ln_p_adj"]["se"]:.4f}），见表4第(2)列。'}})

    a({'h2': '（三）统计口径的含义'})

    a({'p': f'本文的测度结论最终要落回统计口径。'
            f'由式(1)，效值系数的对数变化同时等于两个差：'})
    a({'eq': r'\Delta\ln\tilde{T}-\Delta\ln T=\Delta\ln\eta'
             r'=\Delta\ln P^{N}-\Delta\ln\tilde{P}', 'num': '16'})
    a({'p': f'左端是真实投入增长与名义投入增长之差，右端是两套价格指数的降幅之差。'
            f'二者恒等，意味着价格指数上少记的降幅就是数量上少记的增长。'
            f'在需求面板上，这一缺口为{n(DEFLATE_GAP)}个对数点：'
            f'标准词元用量的对数增长{n(RBASE["dln_T_std"])}，'
            f'物理词元用量的对数增长{n(RBASE["dln_T_phy"])}。'
            f'换算成倍数，正确口径下的真实投入增长是以名义词元价格平减所得结果的'
            f'{fold(DEFLATE_GAP)}倍。这不是小数点后的修正，而是量级上的遗漏。'})

    a({'p': f'第一个后果落在生产率核算上。在增长核算中，'
            f'产出增长减去各要素与中间投入的加权增长即为全要素生产率残差。'
            f'若智能服务作为中间投入的真实数量增长被系统性记少，'
            f'被记少的那一块就转而进入残差，表现为全要素生产率的虚增；'
            f'与此同时，同一笔支出变化中被划归价格的比重被记多。'
            f'这恰恰颠倒了通用目的技术扩散期的真实情形'
            f'{{c:cheng2021}}{{c:acemoglu2025}}。'
            f'消费价格指数的质量偏误曾引出一整轮统计口径改革'
            f'{{c:boskin1998}}{{c:gao2000}}，'
            f'信息技术与云计算服务的价格测度至今仍是官方统计的难题'
            f'{{c:byrne2021}}{{c:sawyer2023}}；'
            f'词元只是把同一问题以更快的节奏重演了一遍。'})

    a({'p': f'第二个后果落在补贴核定上。当前面向算力与模型调用的支持政策，'
            f'多以物理词元量或名义单价为发放依据。'
            f'按式(16)，样本期内以物理词元计量的用量增长倍数只及'
            f'以标准词元计量的1/{fold(DEFLATE_GAP)}，'
            f'按枚数发放的补贴因而会把实际支撑的服务能力增长记少；'
            f'更麻烦的是激励方向：按枚数补贴等于奖励多买便宜档位的词元，'
            f'而不是奖励买到能把任务真正做完的词元；'
            f'档位替代本身能把观测均价压低'
            f'{pc(100 * (1 - exp(DEC["structure_ln"])))}'
            f'（第四部分结构效应），这部分并非真实成本节约，却会被计入补贴绩效。'
            f'以标准词元作为核定单位，才能使补贴与效值对齐。'})

    a({'p': f'第三个后果落在投资回报评估上。企业内部评估智能化项目时，'
            f'习惯把账单总额的上升读作成本失控，把单价下行读作已经省下的钱。'
            f'本文的分解给出了另一种读法：在$|\\varepsilon|>1$的条件下，'
            f'价格通道净效应为正是弹性的必然结果而非项目的失败，'
            f'样本期内仅价格通道就把支出推高'
            f'{pc(RBASE["net_price_channel_pct"], 2)}。'
            f'正确的评估对象不是账单总额，而是完成单位任务所耗的标准词元成本'
            f'与被新纳入任务本身的价值。'
            f'三项后果合起来看，编制质量调整的词元价格指数不只是统计技术问题，'
            f'而是让核算、补贴与投资决策建立在同一套可比价格上的前提。'})

    return b


# ============================================================ 第七部分
def sec7():
    b = []
    a = b.append
    a({'h1': '七、结论与政策建议'})

    a({'h2': '（一）主要结论'})

    a({'p': f'{{b:第一，名义词元价格指数低估了真实降价幅度，而非高估。}}'
            f'2023年1月至2026年6月，单位价值口径的名义指数累计'
            f'{pc(RATE["NPI"]["total_pct"], 3)}'
            f'（年均{RATE["NPI"]["annual_fold"]:.3f}倍），'
            f'质量调整指数累计{pc(RATE["STPI"]["total_pct"], 3)}'
            f'（年均{RATE["STPI"]["annual_fold"]:.3f}倍）。'
            f'对支出份额加权的对数均价指数（同期累计'
            f'{pc(DEC["total_pct"], 3)}）作三重分解，'
            f'真实价格效应占名义降幅的{sh(DEC["share"]["real_price"])}，'
            f'质量效应占{sh(DEC["share"]["quality"])}，'
            f'结构效应占{sh(DEC["share"]["structure"])}，'
            f'残差占{sh(DEC["share"]["residual"])}。'
            f'质量效应为正号，说明能力改进把观测均价托高：'
            f'同样一笔钱买到的词元变强了，这份收益被记进了价格，'
            f'于是名义降价看上去比真实降价温和。'})

    a({'p': f'{{b:第二，在质量调整价格上，需求价格弹性的绝对值大于1，'
            f'支出上升主要经由回弹通道实现。}}'
            f'双向固定效应估计的弹性为{n(EPS)}，名义口径为{n(FEN["elasticity"])}，'
            f'后者把绝对值放大了{pc(BIAS["overstate_pct"], 2)}；'
            f'$H_{{0}}$: $\\varepsilon=-1$的单侧$p$值为{CRIT["p_one_sided"]:.4f}，'
            f'野聚类自助法为{WILD["p_wild"]:.3f}，在5%的水平上拒绝。'
            f'工具变量估计为{n(EPS_IV)}，方向一致而标准误更大。'
            f'回弹分解显示，价格效应与纯回弹效应之和为'
            f'{n(RBASE["net_price_channel"])}个对数点'
            f'（工具变量口径为{n(RIV["net_price_channel"])}），'
            f'即不计任务复杂化与市场扩散，仅价格通道本身就足以让支出上升。'
            f'任务复杂化另贡献{n(RBASE["decomp4"]["task_complexity"])}个对数点，'
            f'与价格无关，不应计入回弹。'})

    a({'p': f'{{b:第三，以名义词元价格平减将低估真实投入增长，'
            f'并使核算、补贴与投资评估建立在错误的价格上。}}'
            f'名义与质量调整两套口径给出同一笔支出变化，'
            f'却相差{n(DEFLATE_GAP)}个对数点的数量增长，'
            f'正确口径下的真实投入增长是名义平减所得结果的{fold(DEFLATE_GAP)}倍。'
            f'其后果是全要素生产率残差虚增、按枚数发放的补贴激励用量而非效值、'
            f'企业把弹性大于1所必然带来的账单上升误读为项目失控——'
            f'三者同源于一件事：把不同效值的词元按枚数相加。'})

    a({'h2': '（二）政策建议'})

    a({'p': f'第一，建立质量调整的词元价格指数的常规编制制度。'
            f'可行的做法是先立样本框后编指数：以代表性供给方的档位—任务单元为抽样单位，'
            f'按月采集挂牌价与可观测特征，保持特征清单的跨期可比与版本留痕；'
            f'再以享乐回归的时期效应编制质量调整指数，'
            f'同时公布固定篮子指数与单位价值指数，使档位替代与真实降价可分开阅读。'
            f'鉴于公开报告记录的词元推理价格年降幅因任务而异，'
            f'区间可达每年{AN["task_annual_fold_range"][0]:.0f}倍至'
            f'{AN["task_annual_fold_range"][1]:.0f}倍，'
            f'总指数之外还应编制按任务类型分层的分指数。'
            f'这项工作可与工业和信息化部拟印发的《算力标准体系建设指南》相衔接，'
            f'该指南推动建立算力服务能力评估与算力市场化定价等标准{{c:yang2024}}。'})

    a({'p': f'第二，明确计价规则并推动账单的可核验披露。'
            f'指数的质量取决于原始记录的质量，而当前的计价口径在输入与输出、'
            f'是否命中缓存、是否处于高峰时段之间差别很大，'
            f'账单却往往只给出一个合计金额。'
            f'建议在服务合约与结算凭证中分项标注词元用量与对应单价，'
            f'并留存可核验的调用记录。'
            f'计价维度与使用维度错位所产生的计量成本{{c:barzel1982}}、'
            f'质量不可观测所引致的逆向选择{{c:akerlof1970}}，'
            f'都要靠可核验的披露来压缩，'
            f'第三方评测与认证在此可以承担质量披露的职能{{c:dranove2010}}。'})

    a({'p': f'第三，在统计核算与政策工具中替换平减因子与核定单位。'
            f'生产率核算中，智能服务作为中间投入应以质量调整价格平减；'
            f'补贴与算力券的核定应以标准词元而非物理词元为单位，'
            f'使支持力度与实际获得的服务能力对齐；'
            f'投资回报评估应以完成单位任务的标准词元成本为口径，'
            f'而不以账单总额的增减为准。'
            f'词元的计量、结算与统计三重职能既已确立，'
            f'把质量调整的价格指数补上，才算把这三重职能真正落到统计口径上。'})

    a({'h2': '（三）研究局限'})

    a({'p': f'本文的局限首先在数据。分析样本是按公开锚校准生成的模拟面板，'
            f'其价格路径、调用量总量与档位价比均已对齐公开发布的锚点，'
            f'但行业与档位的横截面结构出自设定而非观测。'
            f'{{fn:全部实证数字由随附的data_gen.py产生并可复现，'
            f'校准锚与其来源逐条列于data/facts.md。'
            f'本文的实证部分意在完整展示从质量调整测度到弹性识别再到回弹分解的方法链条，'
            f'各项参数的量级不应外推为对真实市场的估计。}}'
            f'因此本文的贡献应被理解为测度框架与识别策略的示范，'
            f'而非对中国智能服务市场弹性的最终估计；'
            f'享乐方程的偏$R^{{2}}$达到'
            f'{R["hedonic"]["output_price"]["r2_partial"]:.4f}，'
            f'高于真实挂牌价数据可期的水平，即为模拟设定所致的上界。'})

    a({'p': f'其次是样本长度与识别的边界。价格面板只有{R["sampleA"]["T"]}个月，'
            f'需求面板只有{SB["T"]}个季度、{SB["n_industry"]}个行业，'
            f'结构性提价期只覆盖两个月，转向之后的价格路径无法可靠估计。'
            f'聚类数偏少同样限制了推断：'
            f'Durbin–Wu–Hausman检验的$p$值为{DWH["cf_p"]:.3f}，'
            f'在{SB["n_industry"]}个行业上{b_no_reject()}，'
            f'故本文只报告工具变量点估计的方向，'
            f'不据此宣称价格内生已获检验支持。'
            f'再次是分解本身的近似性质：式(7)建立在总量层面的对数线性近似上，'
            f'而弹性在行业间是异质的，'
            f'用一个总量弹性去乘总量价格变化，'
            f'会把组间弹性差异连同权重变化一并折进扩散项；'
            f'第四部分的三重分解也有类似问题——享乐方程若遗漏定价上重要的特征，'
            f'遗漏部分会同时污染质量效应与真实价格效应，'
            f'而占比仅{sh(DEC["share"]["residual"])}的残差察觉不到这种污染。'})

    a({'p': f'循此而下有三个方向。其一，以真实的调用明细与结算账单重做本文的测度链条，'
            f'并检验享乐特征集合在真实报价上的解释力；'
            f'其二，把指数按任务类型分层编制，'
            f'使不同任务结构的使用者能读到与自己相关的价格路径；'
            f'其三，从简约式弹性转向供给侧定价行为的结构估计{{c:conlon2020}}，'
            f'把档位纵向差异化下的加成、峰谷分时定价与拥塞外部性一并纳入模型。'
            f'词元的价格测度刚刚开始，而它已经是许多重要核算数字的分母。'})

    return b




def c_rebound():
    """回弹文献的引注串（单列以避免 f-string 中的花括号）。"""
    return '{c:gillingham2016}{c:borenstein2015}'


def b_no_reject():
    """不能拒绝价格外生（单列以保持措辞在全文一致）。"""
    return '不能拒绝价格外生'
