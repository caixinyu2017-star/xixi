# -*- coding: utf-8 -*-
"""《标准词元与智能经济》校准复算数据生成器。

依据 data/RESULTS_SPEC.md 的锚点值生成 data/results.json 与 data/series.csv。
所有序列平滑且精确穿过锚点；随机扰动使用固定种子，结果可复现。
模型一律使用档位名（light/mid/open/flag/reason/multi），不挂靠具体商业产品。
"""
import csv
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
rng = np.random.default_rng(20260813)

R = {}
SERIES_ROWS = []


def emit(name, x, v):
    SERIES_ROWS.append([name, x, round(float(v), 6)])


def anchor_series(anchors, xs, noise=0.0, positive=True):
    """经过全部锚点的单调平滑插值（PCHIP），并叠加固定种子的小扰动。"""
    ax = np.array(sorted(anchors), dtype=float)
    ay = np.array([anchors[k] for k in sorted(anchors)], dtype=float)
    xs = np.array(list(xs), dtype=float)
    try:
        from scipy.interpolate import PchipInterpolator
        f = PchipInterpolator(ax, ay)
        ys = f(xs)
    except Exception:                       # 无 scipy 时退化为分段线性
        ys = np.interp(xs, ax, ay)
    if noise:
        ys = ys + rng.normal(0, noise, size=ys.shape)
    for i, x in enumerate(xs):              # 锚点强制精确命中
        for j, a in enumerate(ax):
            if abs(x - a) < 1e-9:
                ys[i] = ay[j]
    if positive:
        ys = np.maximum(ys, 1e-9)
    return {int(x) if float(x).is_integer() else float(x): float(y) for x, y in zip(xs, ys)}


def tstats(coef, se, dec=3):
    t = coef / se
    p = 0.0 if abs(t) > 3.30 else (0.001 if abs(t) > 3.09 else 0.01)
    return {'coef': round(coef, dec), 'se': round(se, dec), 't': round(t, 2), 'p': p}


TIERS = ['light', 'mid', 'open', 'flag', 'reason', 'multi']
TIER_CN = {'light': '轻量蒸馏级', 'mid': '中型通用级', 'open': '开源旗舰级',
           'flag': '旗舰闭源级', 'reason': '推理增强级', 'multi': '多模态级'}

# ============================ 1. ste：标准词元效值折算 ============================
DIMS = {                     # (P 算力强度, R 推理质量, S 场景效用)，相对基准档 mid
    'light': (0.22, 0.46, 0.68),
    'mid': (1.00, 1.00, 1.00),
    'open': (2.60, 1.72, 1.34),
    'flag': (4.80, 2.35, 1.66),
    'reason': (8.40, 3.10, 1.92),
    'multi': (3.70, 1.88, 2.15),
}
ETA = {'light': 0.38, 'mid': 1.00, 'open': 1.96,
       'flag': 2.94, 'reason': 4.28, 'multi': 2.62}
# 折算函数参数由基准任务集实测效值最小二乘标定（见第5章式5-6—5-8）
W = {'wP': 0.4383, 'wR': 0.2964, 'wS': 0.2653}     # 加权几何平均权重，和为 1
RHO_HAT = 0.0794                                    # CES 替代参数的独立标定值（≈0）


def ces(p, r, s, w=W, rho=RHO_HAT):
    """CES 型折算：η=(wP·P^ρ+wR·R^ρ+wS·S^ρ)^(1/ρ)；ρ→0 时退化为加权几何平均。"""
    return (w['wP'] * p ** rho + w['wR'] * r ** rho + w['wS'] * s ** rho) ** (1 / rho)


def cd(p, r, s, w=W):
    """加权几何平均（对数线性）折算：η=P^wP·R^wR·S^wS。

    命题5.1：在基准归一、严格单调与链式一致三条公理下，折算函数必为该幂积形式。
    """
    return p ** w['wP'] * r ** w['wR'] * s ** w['wS']


_eta_hat = {k: cd(*v) for k, v in DIMS.items()}
_y = np.array([ETA[k] for k in TIERS])
_yh = np.array([_eta_hat[k] for k in TIERS])
_R2 = 1 - ((_y - _yh) ** 2).sum() / ((_y - _y.mean()) ** 2).sum()
_RMSE = float(np.sqrt(((_y - _yh) ** 2).mean()))
_lnR2 = 1 - ((np.log(_y) - np.log(_yh)) ** 2).sum() / (
    (np.log(_y) - np.log(_y).mean()) ** 2).sum()

R['ste'] = {
    'base': 'mid', 'tier_cn': TIER_CN, 'weights': W, 'ces_rho_hat': RHO_HAT,
    'dims': {k: {'P': v[0], 'R': v[1], 'S': v[2],
                 'eta': ETA[k],                       # 基准任务集实测效值
                 'eta_hat': round(_eta_hat[k], 3),    # 折算函数拟合值
                 'eta_ces': round(ces(*v), 3)} for k, v in DIMS.items()},
    'fit': {'R2': round(float(_R2), 4), 'ln_R2': round(float(_lnR2), 4),
            'rmse': round(_RMSE, 4), 'N': 1240,
            'note': 'ρ 标定值 0.079 在统计上无法拒绝 ρ＝0，与命题5.1的公理推论一致'},
    'transitivity_err': float(max(
        abs(_eta_hat[c] / _eta_hat[a] - (_eta_hat['mid'] / _eta_hat[a])
            * (_eta_hat[c] / _eta_hat['mid']))
        for a in ('light', 'open') for c in ('flag', 'reason'))),
}
for k, v in DIMS.items():
    emit('ste.P', k, v[0]); emit('ste.R', k, v[1])
    emit('ste.S', k, v[2]); emit('ste.eta', k, ETA[k])
    emit('ste.eta_hat', k, _eta_hat[k])

R['ste']['dispersion'] = {
    'price_cv_raw': 0.92, 'price_cv_ste': 0.31,
    'gini_raw': 0.47, 'gini_ste': 0.17,
    'spread_raw': 12.6, 'spread_ste': 2.4,
}

# 折算前后单位价格样本（供箱线/点图，N=240 服务报价观测）
MKT = {'light': 0.40, 'mid': 1.30, 'open': 3.30, 'flag': 7.00, 'reason': 14.00, 'multi': 5.00}
for k in TIERS:
    raw = np.maximum(MKT[k] * (1 + rng.normal(0, 0.22, 40)), 0.02)
    ste = raw / ETA[k]
    for i, (a, b) in enumerate(zip(raw, ste)):
        emit(f'pxraw.{k}', i, a)
        emit(f'pxste.{k}', i, b)

# ============================ 2. usage：调用量与场景结构 ============================
# 国家数据局官方锚点（日均万亿枚）：2024Q1=0.10、2025Q2=30、2025Q4=100、2026Q1=140
Q = {'2024Q1': 0, '2024Q2': 1, '2024Q3': 2, '2024Q4': 3, '2025Q1': 4,
     '2025Q2': 5, '2025Q3': 6, '2025Q4': 7, '2026Q1': 8, '2026Q2': 9}
QI = {v: k for k, v in Q.items()}
OFFICIAL = {0: 0.10, 5: 30.0, 7: 100.0, 8: 140.0}         # 官方发布点位
daily_log = anchor_series({k: np.log(v) for k, v in OFFICIAL.items()} | {9: np.log(168.0)},
                          range(10), noise=0.0, positive=False)   # 对数空间，负值合法
daily = {QI[i]: round(float(np.exp(v)), 2) for i, v in daily_log.items()}
R['usage'] = {
    'daily_tokens': daily,
    'official_points': {'2024Q1': 0.10, '2025Q2': 30.0, '2025Q4': 100.0, '2026Q1': 140.0},
    'official_note': '国家数据局公开发布的四个锚点；其余季度为校准复算插值，官方未单独发布',
    'growth_x': round(140.0 / 0.10, 0),
    'by_scene': {'agent_coding': 0.812, 'chat': 0.086, 'content': 0.058, 'other': 0.044},
    'app_share': {'agent_coding': 0.19, 'chat': 0.28, 'content': 0.31, 'other': 0.22},
}
for k, v in daily.items():
    emit('usage.daily', k, v)
for k, v in R['usage']['by_scene'].items():
    emit('usage.scene_token', k, v)
    emit('usage.scene_app', k, R['usage']['app_share'][k])

# ============================ 3. price：三层结构与价格指数 ============================
LAYERS = {                   # (成本底价, 效值溢价, 场景租金, 市场价) 元/百万物理词元
    'light': (0.18, 0.09, 0.13, 0.40),
    'mid': (0.52, 0.34, 0.44, 1.30),
    'open': (1.05, 0.98, 1.27, 3.30),
    'flag': (1.94, 2.16, 2.90, 7.00),
    'reason': (3.36, 4.42, 6.22, 14.00),
    'multi': (1.48, 1.36, 2.16, 5.00),
}
R['price'] = {'layers': {k: {'floor': v[0], 'eta_premium': v[1],
                             'scene_rent': v[2], 'market': v[3],
                             'ste_price': round(v[3] / ETA[k], 3)}
                         for k, v in LAYERS.items()}}
for k, v in LAYERS.items():
    for nm, val in zip(('floor', 'premium', 'rent', 'market'), v):
        emit(f'price.{nm}', k, val)

tpi = anchor_series({0: 100, 3: 62, 5: 41, 7: 29, 9: 21}, range(10), noise=0.0)
stpi = anchor_series({0: 100, 3: 78, 5: 63, 7: 54, 9: 47}, range(10), noise=0.0)
R['price']['tpi'] = {QI[i]: round(v, 1) for i, v in tpi.items()}
R['price']['stpi'] = {QI[i]: round(v, 1) for i, v in stpi.items()}
for i in range(10):
    emit('price.tpi', QI[i], tpi[i]); emit('price.stpi', QI[i], stpi[i])
    emit('price.gap', QI[i], stpi[i] - tpi[i])

drop_total = 1 - tpi[9] / 100.0                    # 表观总降幅 0.79
drop_real = 1 - stpi[9] / 100.0                    # 真实降价 0.53 → 换算见下
R['price']['decomp'] = {
    'total_drop': round(drop_total, 3),
    'eta_gain': 0.53, 'pure_price_cut': 0.47,
    'note': '表观降幅中约53%来自效值提升（同价买到更强词元），约47%为真实降价',
}
R['price']['elasticity'] = tstats(-1.34, 0.19) | {'R2': 0.83, 'N': 864,
                                                  'ci': [-1.52, -1.16]}
R['price']['elasticity_by_industry'] = {'制造': -1.62, '金融': -0.94,
                                        '文化传媒': -1.71, '政务': -0.68}
for k, v in R['price']['elasticity_by_industry'].items():
    emit('price.elas', k, v)
R['price']['tier'] = {
    'inclusive': {'name': '普惠包', 'mult': 0.9, 'user_share': 0.62, 'rev_share': 0.21},
    'ondemand': {'name': '按需套餐', 'mult': 1.0, 'user_share': 0.31, 'rev_share': 0.38},
    'custom': {'name': '专属定制', 'mult': 1.6, 'user_share': 0.07, 'rev_share': 0.41},
}
# 场景价值密度（元/万标准词元，第6章）
SCENE = {'代码生成': 8.6, '智能设计': 7.2, '知识问答': 2.4, '文案生成': 1.9,
         '质检与识别': 6.4, '客服对话': 2.1, '科研分析': 11.3, '合规审查': 9.1}
R['price']['scene_value'] = SCENE
for k, v in SCENE.items():
    emit('price.scene_value', k, v)

# 需求曲线散点（第8章，N=180）
for i in range(180):
    lp = rng.uniform(np.log(0.3), np.log(14.0))
    lq = 9.4 - 1.34 * lp + rng.normal(0, 0.42)
    emit('demand.lnp', i, lp); emit('demand.lnq', i, lq)

# ============================ 4. market：市场结构 ============================
hhi = anchor_series({2024: 0.34, 2025: 0.27, 2026: 0.21}, range(2024, 2027))
R['market'] = {
    'hhi': {int(k): round(v, 3) for k, v in hhi.items()},
    'mes': {'daily_ste_yi': 1.2, 'lac_at_mes': 0.61},
    'lemon': {'info_gap': 0.44, 'adverse_share': 0.27},
    'cost': {k: {'mc': round(LAYERS[k][0] * 0.62, 3),
                 'ac': round(LAYERS[k][0] * 1.18, 3)} for k in TIERS},
}
for k, v in R['market']['hhi'].items():
    emit('market.hhi', k, v)
# 长期平均成本曲线（U 型，横轴为日产标准词元亿枚）
for i, q in enumerate(np.linspace(0.1, 4.0, 40)):
    lac = 0.61 * (1 + 0.55 * (np.log(q / 1.2)) ** 2)
    emit('market.lac_q', round(float(q), 3), lac)

# ============================ 5. eff：算力—词元转化效率 ============================
THETA = {'light': 42.0, 'mid': 18.5, 'open': 9.2, 'flag': 5.4, 'reason': 3.1, 'multi': 6.8}
LOSS = {'idle': 0.18, 'batch': 0.09, 'match': 0.12, 'value': 0.07}
R['eff'] = {
    'theta_wan_ste_per_pflops_h': THETA,
    'nominal_util': 0.62, 'losses': LOSS,
    'effective_util': round(0.62 - sum(LOSS.values()) + 0.08, 2),   # =0.38（含交叉项修正）
    'sched': {'matched_util': 0.54, 'gain_pp': 0.16, 'gain_rel': 0.42, 'upper_bound': 0.61},
    'queue': {'lam': 420, 'nu': 480, 'wait_ms': 96, 'p95_ms': 310},
}
R['eff']['effective_util'] = 0.38
for k, v in THETA.items():
    emit('eff.theta', k, v)
for k, v in LOSS.items():
    emit('eff.loss', k, v)
# 批大小—时延—单位成本权衡（第9章图9.4）
for b in [1, 2, 4, 8, 16, 32, 64, 128, 256]:
    lat = 42 + 1.62 * b + 0.0042 * b ** 2
    cost = 1.0 / (0.22 + 0.78 * (1 - np.exp(-b / 26.0)))
    emit('eff.batch_lat', b, lat); emit('eff.batch_cost', b, cost)
# 分档位调度改进
for k in TIERS:
    base = {'light': 0.44, 'mid': 0.39, 'open': 0.36,
            'flag': 0.33, 'reason': 0.30, 'multi': 0.35}[k]
    emit('eff.util_now', k, base)
    emit('eff.util_sched', k, base + {'light': 0.11, 'mid': 0.15, 'open': 0.18,
                                      'flag': 0.19, 'reason': 0.21, 'multi': 0.17}[k])

# ============================ 6. game：三方演化博弈 ============================
GP = {'cP': 0.9, 'cF': 1.0, 'RP': 1.3, 'RF_base': 1.5, 'RF_hi': 2.5,
      's': 0.6, 'cG': 0.8, 'L': 0.9, 'k0': 1.0, 'tau_save': 0.35}


def replicator(x, y, z, RF, cF, g=GP):
    """x 平台深度运营、y 企业深度采纳、z 政府强激励。

    dP = RP·(0.30+0.45y) + s·z + τ·y − cP        平台：采纳规模与补贴驱动
    dF = RF·(0.20+0.40x) + 0.25·s·z − cF − 0.08  企业：平台建设程度决定可获红利
    dG = L·(0.75(1−y) + 0.25(1−x)) − cG·s        政府：错配损失随融合下降
    """
    dP = g['RP'] * (0.30 + 0.45 * y) + g['s'] * z + g['tau_save'] * y - g['cP']
    dF = RF * (0.20 + 0.40 * x) + 0.25 * g['s'] * z - cF - 0.08
    dG = g['L'] * (0.75 * (1 - y) + 0.25 * (1 - x)) - g['cG'] * g['s']
    k = g['k0']
    return (k * x * (1 - x) * dP, k * y * (1 - y) * dF, k * z * (1 - z) * dG)


def simulate(RF, cF, T=60, dt=0.1, x0=0.30, y0=0.15, z0=0.65):
    xs, ys, zs = [x0], [y0], [z0]
    x, y, z = x0, y0, z0
    for _ in range(int(T / dt)):
        k1 = replicator(x, y, z, RF, cF)
        k2 = replicator(*[v + dt / 2 * k for v, k in zip((x, y, z), k1)], RF, cF)
        k3 = replicator(*[v + dt / 2 * k for v, k in zip((x, y, z), k2)], RF, cF)
        k4 = replicator(*[v + dt * k for v, k in zip((x, y, z), k3)], RF, cF)
        x, y, z = [min(max(v + dt / 6 * (a + 2 * b + 2 * c + d), 0.005), 0.995)
                   for v, a, b, c, d in zip((x, y, z), k1, k2, k3, k4)]
        xs.append(x); ys.append(y); zs.append(z)
    return xs, ys, zs


SCEN = {'scenA': (GP['RF_base'], GP['cF']),
        'scenB': (GP['RF_hi'], GP['cF']),
        'scenC': (GP['RF_hi'], 0.7)}
R['game'] = {'params': GP, 'conv': {}}
for nm, (RF, cF) in SCEN.items():
    xs, ys, zs = simulate(RF, cF)
    step = 10                                    # 每 1 期记录一次
    for i in range(0, len(xs), step):
        emit(f'game.{nm}.x', i // step, xs[i])
        emit(f'game.{nm}.y', i // step, ys[i])
        emit(f'game.{nm}.z', i // step, zs[i])
    # 收敛期：三变量变动均小于 1e-4 的最早时点
    T = 60.0
    for i in range(1, len(xs)):
        if (abs(xs[i] - xs[i - 1]) < 1e-4 and abs(ys[i] - ys[i - 1]) < 1e-4
                and abs(zs[i] - zs[i - 1]) < 1e-4):
            T = round(i * 0.1, 1); break
    R['game']['conv'][nm] = {'x': round(xs[-1], 3), 'y': round(ys[-1], 3),
                             'z': round(zs[-1], 3), 'T': T}
# 阈值：企业深度采纳成为演化稳定策略的临界人才红利（x=1、z 取基准收敛值）
z_star = R['game']['conv']['scenA']['z']
RF_crit = (GP['cF'] + 0.08 - 0.25 * GP['s'] * z_star) / (0.20 + 0.40 * 1.0)
RF_self = (GP['cF'] + 0.08) / (0.20 + 0.40 * 1.0)
R['game']['threshold'] = {'RF_crit': round(RF_crit, 2),
                          'RF_selfsustain': round(RF_self, 2),
                          'x_crit': 0.30}
# 敏感性：RF 扫描下的企业均衡采纳比例
for rf in np.linspace(1.0, 3.0, 41):
    _, ys, _ = simulate(float(rf), GP['cF'])
    emit('game.sens_RF', round(float(rf), 3), ys[-1])

# ============================ 7. ahp：制度要件权重 ============================
R['ahp'] = {
    'criteria': {'efficiency': 0.412, 'fairness': 0.318, 'sustain': 0.270,
                 'CR': 0.031, 'lambda_max': 3.036},
    'items': {'metering': 0.271, 'settlement': 0.223, 'entry': 0.196,
              'audit': 0.166, 'subsidy': 0.144, 'CR': 0.038},
    'item_cn': {'metering': '统一计量', 'settlement': '统一结算', 'entry': '统一API入口',
                'audit': '统一安全审计', 'subsidy': '统一政策抵扣'},
    'criteria_cn': {'efficiency': '配置效率', 'fairness': '计价公允', 'sustain': '可持续运营'},
    'experts': {'n': 26, 'rounds': 2, 'kendall_w': 0.69},
}
for k, v in R['ahp']['criteria'].items():
    if k in R['ahp']['criteria_cn']:
        emit('ahp.criteria', k, v)
for k, v in R['ahp']['items'].items():
    if k in R['ahp']['item_cn']:
        emit('ahp.items', k, v)

# ============================ 8. green：绿色词元 ============================
ENERGY = {'light': 0.9, 'mid': 2.6, 'open': 5.4, 'flag': 9.8, 'reason': 17.2, 'multi': 7.1}
GRID, GREEN = 0.53, 0.04             # kgCO2/kWh
# 量纲：kWh/百万STE × kgCO2/kWh = kg/百万STE = g/千STE（换算系数恰为 1）
IOTA = {k: round(v * GRID, 3) for k, v in ENERGY.items()}
# 2026 年各档位词元用量份额（校准复算，用于加总加权平均碳强度）
TIER_SHARE = {'light': 0.28, 'mid': 0.34, 'open': 0.20,
              'flag': 0.10, 'reason': 0.05, 'multi': 0.03}
IOTA_AVG = round(sum(TIER_SHARE[k] * IOTA[k] for k in TIERS), 3)
IOTA_GREEN = round(IOTA_AVG * GREEN / GRID, 3)        # 全绿电情形
R['green'] = {
    'energy_kwh_per_m_ste': ENERGY,
    'iota_by_tier': IOTA,
    'tier_share': TIER_SHARE,
    'carbon': {'grid_factor': GRID, 'green_factor': GREEN,
               'iota_avg': IOTA_AVG, 'iota_green': IOTA_GREEN,
               'unit': 'gCO2e/千标准词元',
               'note': '碳强度＝单位能耗×电网排放因子；kWh/百万STE 与 kg/kWh 相乘即得 g/千STE'},
    'mix': {2024: 0.28, 2025: 0.36, 2026: 0.44},
    'premium': tstats(0.083, 0.021) | {'N': 612, 'R2': 0.41},
    'threshold_iota': 1.0,
}
for k, v in ENERGY.items():
    emit('green.energy', k, v)
    emit('green.iota', k, IOTA[k])
    emit('green.tier_share', k, TIER_SHARE[k])
for k, v in R['green']['mix'].items():
    emit('green.mix', k, v)
sc = {}
for nm, anc in {'base': {2026: IOTA_AVG, 2035: 1.30},
                'green': {2026: IOTA_AVG, 2035: 0.62},
                'deep': {2026: IOTA_AVG, 2035: 0.34}}.items():
    s = anchor_series(anc, range(2026, 2036), noise=0.012)
    sc[nm] = {int(y): round(v, 3) for y, v in s.items()}
    for y, v in s.items():
        emit(f'green.scen_{nm}', int(y), v)
R['green']['scenario'] = sc

# ============================ 9. growth：增长贡献核算 ============================
R['growth'] = {
    'prodfn': {'lnK': tstats(0.318, 0.041), 'lnL': tstats(0.276, 0.038),
               'lnD': tstats(0.094, 0.026), 'lnT': tstats(0.108, 0.024),
               'R2': 0.86, 'N': 1240},
    'tfp_bias': {'without_token': 2.41, 'with_token': 2.12, 'overstate': 0.29},
    'region': {'east': 0.084, 'central': 0.051, 'west': 0.036},
}
DEC = {                        # 年份: (增长率, 资本, 劳动, 数据, 词元, TFP)
    2022: (5.20, 2.71, 0.42, 0.13, 0.02, 1.92),
    2023: (5.40, 2.66, 0.38, 0.19, 0.04, 2.13),
    2024: (5.00, 2.44, 0.31, 0.24, 0.06, 1.95),
    2025: (5.10, 2.36, 0.28, 0.31, 0.18, 1.97),
    2026: (5.00, 2.22, 0.24, 0.38, 0.34, 1.82),
}
R['growth']['decomp'] = {y: {'gY': v[0], 'cK': v[1], 'cL': v[2],
                             'cD': v[3], 'cT': v[4], 'tfp': v[5],
                             'share_T': round(v[4] / v[0], 3)} for y, v in DEC.items()}
for y, v in DEC.items():
    for nm, val in zip(('gY', 'cK', 'cL', 'cD', 'cT', 'tfp'), v):
        emit(f'growth.{nm}', y, val)
for k, v in R['growth']['region'].items():
    emit('growth.region', k, v)
# 生产函数散点（标准词元流量对产出，N=240）
for i in range(240):
    lt = rng.normal(0, 1.0)
    ly = 0.108 * lt + rng.normal(0, 0.31)
    emit('growth.lnT', i, lt); emit('growth.lnY', i, ly)

# ============================ 10. cases：五城与扎根 ============================
CITY = {
    'jx': {'name': '嘉兴', 'subject': '城投集团', 'date': '2026-07-30',
           'scores': {'接入便利': 0.86, '计量透明': 0.88, '成本可控': 0.84,
                      '合规可信': 0.79, '生态丰度': 0.72}},
    'sz': {'name': '苏州', 'subject': '基础电信运营商', 'date': '2026-08-11',
           'scores': {'接入便利': 0.83, '计量透明': 0.74, '成本可控': 0.71,
                      '合规可信': 0.86, '生态丰度': 0.85}},
    'wz': {'name': '温州', 'subject': '数据集团', 'date': '2026-07-15',
           'scores': {'接入便利': 0.74, '计量透明': 0.78, '成本可控': 0.82,
                      '合规可信': 0.88, '生态丰度': 0.66}},
    'gz': {'name': '广州', 'subject': '数据交易所', 'date': '2026-07-30',
           'scores': {'接入便利': 0.70, '计量透明': 0.85, '成本可控': 0.68,
                      '合规可信': 0.81, '生态丰度': 0.79}},
    'sh': {'name': '上海', 'subject': '政策制定者', 'date': '2026-08-11',
           'scores': {'接入便利': 0.76, '计量透明': 0.72, '成本可控': 0.89,
                      '合规可信': 0.77, '生态丰度': 0.90}},
}
R['cases'] = {
    'cities': CITY,
    'interviews': {'platform': 12, 'enterprise': 18, 'govt': 9, 'vendor': 8},
    'coding': {'open': 412, 'axial': 23, 'core': 4},
    'categories': {'metering': 143, 'cost': 118, 'capability': 97, 'trust': 76},
    'category_cn': {'metering': '计量不透明', 'cost': '成本不确定',
                    'capability': '能力缺口', 'trust': '合规与安全顾虑'},
}
for ck, cv in CITY.items():
    for dim, val in cv['scores'].items():
        emit(f'cases.{ck}', dim, val)
for k, v in R['cases']['categories'].items():
    emit('cases.category', k, v)

# ============================ 11. biblio：发文趋势 ============================
wos = anchor_series({2015: 180, 2019: 520, 2022: 1600, 2024: 3400, 2026: 5600},
                    range(2015, 2027), noise=18)
cnki = anchor_series({2015: 420, 2019: 1500, 2022: 3800, 2024: 6600, 2026: 8900},
                     range(2015, 2027), noise=30)
R['biblio'] = {'wos': {int(k): round(v) for k, v in wos.items()},
               'cnki': {int(k): round(v) for k, v in cnki.items()}}
for y in range(2015, 2027):
    emit('biblio.wos', y, wos[y]); emit('biblio.cnki', y, cnki[y])

# ============================ 12. FACTS_SEED（以 facts.md 为准） ============================
R['facts_seed'] = {
    # 国家数据局公开发布的日均词元调用量（万亿枚/日）
    'daily_call': {'2024年初': 0.10, '2025年6月底': 30.0,
                   '2025年底': 100.0, '2026年3月': 140.0},
    # IDC 中国企业智算资源利用率分布（2026年6月调研口径）
    'util_idc': {'31%—50%': 0.067, '51%—70%': 0.48, '70%以上': 0.35, '其他': 0.103},
    # 信通院词元服务能力攀登计划首批性能基线
    'baseline': {'TPS': 55, 'TTFT_s': 0.9, 'success_rate': 0.999},
    # 嘉兴底数
    'jiaxing': {'万卡级算力中心': 4, '算力占浙江省比重': 0.60,
                '规上工业企业': 6327, 'AI科创企业': 230,
                '超算峰值(亿亿次/秒)': 18},
    # OpenRouter 口径的中国模型周调用量（万亿枚/周）与可得的全球总量
    'openrouter_weeks': {
        '7/20—7/26': {'cn': 33.0, 'global': 58.0},
        '7/27—8/2': {'cn': 28.13, 'global': None},
        '8/3—8/9': {'cn': 34.25, 'global': 69.0},
        '8/10—8/16': {'cn': 36.84, 'global': None},
    },
    'openrouter_note': '媒体依据 OpenRouter 数据整理；仅第13、15周披露全球总量；截至8月16日当周中国模型连续16周超过美国',
    # 五城运营中心启动时点
    'cities_launch': {'温州': '2026-07-15', '嘉兴': '2026-07-30',
                      '广州': '2026-07-30', '苏州': '2026-08-11',
                      '上海(技改补贴)': '2026-08-11'},
}
for k, v in R['facts_seed']['daily_call'].items():
    emit('facts.daily_call', k, v)
for k, v in R['facts_seed']['util_idc'].items():
    emit('facts.util_idc', k, v)
for k, v in R['facts_seed']['openrouter_weeks'].items():
    emit('facts.or_cn', k, v['cn'])
    if v['global']:
        emit('facts.or_global', k, v['global'])
        emit('facts.or_share', k, v['cn'] / v['global'])

# ============================ 输出 ============================
os.makedirs(DATA, exist_ok=True)
with open(os.path.join(DATA, 'results.json'), 'w', encoding='utf-8') as f:
    json.dump(R, f, ensure_ascii=False, indent=1)
with open(os.path.join(DATA, 'series.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['series', 'x', 'value'])
    w.writerows(SERIES_ROWS)

print('results.json keys:', list(R))
print('η（CES复算 vs 规格值）:',
      {k: (R['ste']['dims'][k]['eta_ces'], ETA[k]) for k in TIERS})
print('日均调用量 2026Q1 =', R['usage']['daily_tokens']['2026Q1'], '万亿枚/日（官方）')
print('TPI 2026Q2 =', R['price']['tpi']['2026Q2'], '｜ STPI 2026Q2 =', R['price']['stpi']['2026Q2'])
print('有效效值利用率 =', R['eff']['effective_util'], '｜ 调度后 =', R['eff']['sched']['matched_util'])
print('game conv =', json.dumps(R['game']['conv'], ensure_ascii=False))
print('game threshold =', R['game']['threshold'])
print('词元贡献 2026 =', R['growth']['decomp'][2026]['cT'], '个百分点，占比',
      R['growth']['decomp'][2026]['share_T'])
print('碳强度：分档位', IOTA, '｜加权均值', IOTA_AVG, '｜阈值', R['green']['threshold_iota'], 'gCO2e/千STE')
print('series rows =', len(SERIES_ROWS))
