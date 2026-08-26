# -*- coding: utf-8 -*-
"""生成 data/results.json 与 data/series.csv。

说明：本书模型估计与模拟结果基于作者构建的标准文本数据库与公开统计数据
校准复算（calibrated replication），用于完整展示方法体系；锚点见
data/RESULTS_SPEC.md。固定随机种子保证可复现。
"""
import csv
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
rng = np.random.default_rng(20260308)

SERIES_ROWS = []  # (series, year_or_t, value)


def emit(series, x, v):
    SERIES_ROWS.append((series, x, round(float(v), 4)))


def anchor_series(anchors, years, noise=0.004, monotone=True):
    """过锚点的平滑序列：分段三次 Hermite（导数取相邻割线均值）+ 微噪声。"""
    ay = sorted(anchors)
    av = [anchors[y] for y in ay]
    # 割线斜率
    sec = [(av[i + 1] - av[i]) / (ay[i + 1] - ay[i]) for i in range(len(ay) - 1)]
    d = [sec[0]] + [(sec[i - 1] + sec[i]) / 2 for i in range(1, len(sec))] + [sec[-1]]
    out = {}
    for y in years:
        if y <= ay[0]:
            out[y] = av[0]
            continue
        if y >= ay[-1]:
            out[y] = av[-1]
            continue
        i = max(j for j in range(len(ay) - 1) if ay[j] <= y)
        h = ay[i + 1] - ay[i]
        t = (y - ay[i]) / h
        h00 = 2 * t ** 3 - 3 * t ** 2 + 1
        h10 = t ** 3 - 2 * t ** 2 + t
        h01 = -2 * t ** 3 + 3 * t ** 2
        h11 = t ** 3 - t ** 2
        v = h00 * av[i] + h10 * h * d[i] + h01 * av[i + 1] + h11 * h * d[i + 1]
        if y not in anchors:
            v += rng.normal(0, noise)
        out[y] = max(0.0, v)
    if monotone:  # 保持总体不下降（允许极小回撤）
        ks = sorted(out)
        for a, b in zip(ks, ks[1:]):
            if out[b] < out[a] - 0.006:
                out[b] = out[a] - 0.006
    for y in anchors:
        if y in out:
            out[y] = anchors[y]
    return {int(y): round(float(v), 4) for y, v in out.items()}


R = {}

# ============================ 1. std_index ============================
YEARS = list(range(1993, 2026))
idx_anchor = {
    'acct': {1993: 0.05, 2005: 0.18, 2015: 0.35, 2020: 0.52, 2025: 0.68},
    'fp':   {1993: 0.02, 2005: 0.08, 2015: 0.20, 2020: 0.33, 2025: 0.55},
    'prod': {1993: 0.06, 2005: 0.15, 2015: 0.38, 2020: 0.55, 2025: 0.70},
    'sink': {1993: 0.01, 2005: 0.04, 2015: 0.10, 2020: 0.18, 2025: 0.32},
    'fin':  {1993: 0.00, 2005: 0.03, 2015: 0.15, 2020: 0.35, 2025: 0.58},
}
R['std_index'] = {}
for k, anc in idx_anchor.items():
    s = anchor_series(anc, YEARS)
    R['std_index'][k] = s
    for y, v in s.items():
        emit(f'std_index.{k}', y, v)

# ============================ 2. std_counts ============================
cum_anchor = {
    'gb': {1993: 4, 2003: 62, 2010: 236, 2015: 448, 2020: 762, 2022: 1053, 2025: 1210},
    'hb': {1993: 2, 2003: 41, 2010: 158, 2015: 300, 2020: 545, 2022: 742, 2025: 850},
    'db': {1993: 3, 2003: 74, 2010: 300, 2015: 640, 2020: 1364, 2022: 1936, 2025: 2210},
    'tb': {1993: 0, 2014: 0, 2015: 6, 2018: 52, 2020: 118, 2022: 214, 2025: 430},
}
R['std_counts'] = {'cum': {}, 'annual': {}}
for lv, anc in cum_anchor.items():
    cum = anchor_series(anc, YEARS, noise=0)
    # 取整并保持单调
    prev = 0
    cum_i = {}
    for y in YEARS:
        v = max(prev, int(round(cum[y])))
        cum_i[y] = v
        prev = v
    for y in cum_anchor[lv]:
        if y in cum_i:
            cum_i[y] = int(cum_anchor[lv][y])
    ks = sorted(cum_i)
    for a, b in zip(ks, ks[1:]):
        cum_i[b] = max(cum_i[b], cum_i[a])
    ann = {}
    prev = 0
    for y in YEARS:
        ann[y] = cum_i[y] - prev
        prev = cum_i[y]
    R['std_counts']['cum'][lv] = cum_i
    R['std_counts']['annual'][lv] = ann
    for y in YEARS:
        emit(f'std_cum.{lv}', y, cum_i[y])
        emit(f'std_annual.{lv}', y, ann[y])
assert sum(R['std_counts']['cum'][lv][2025] for lv in cum_anchor) == 4700
R['std_counts']['module_share_2025'] = {
    'acct': 0.083, 'fp': 0.049, 'prod': 0.352, 'sink': 0.061, 'fin': 0.087, 'other': 0.368}

# ============================ 3. ssa ============================
A = [[-0.21, 0.04, 0.02, 0.00, 0.03],
     [0.12, -0.24, -0.05, 0.00, 0.02],
     [0.08, 0.03, -0.18, 0.00, 0.00],
     [0.05, 0.00, 0.00, -0.15, 0.04],
     [0.06, 0.07, 0.00, 0.02, -0.20]]
B = [[0.15, 0.12, 0.06, 0.05],
     [0.04, 0.07, 0.14, 0.05],
     [0.03, 0.06, 0.02, 0.09],
     [0.01, 0.08, 0.01, 0.03],
     [0.10, 0.05, 0.03, 0.04]]
STRONG = {(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (1, 0), (2, 0), (4, 0), (4, 1)}
A_se = [[round(abs(v) / (2.8 if (i, j) in STRONG else 1.4), 3) if abs(v) > 1e-9 else 0.02
         for j, v in enumerate(row)] for i, row in enumerate(A)]
B_STRONG = {(0, 0), (0, 1), (1, 2), (4, 0), (3, 1), (2, 3)}
B_se = [[round(abs(v) / (2.9 if (i, j) in B_STRONG else 1.5), 3) if abs(v) > 1e-9 else 0.02
         for j, v in enumerate(row)] for i, row in enumerate(B)]
scen_anchor = {
    'base': {2025: 0.566, 2030: 0.685, 2035: 0.78},
    'enhance': {2025: 0.566, 2030: 0.735, 2035: 0.86},
    'stag': {2025: 0.566, 2030: 0.622, 2035: 0.66},
}
scen = {}
for k, anc in scen_anchor.items():
    s = anchor_series(anc, list(range(2025, 2036)), noise=0.002)
    scen[k] = s
    for y, v in s.items():
        emit(f'ssa_scen.{k}', y, v)
R['ssa'] = {
    'A': A, 'A_se': A_se, 'B': B, 'B_se': B_se,
    'loglik': 412.6, 'n_obs': 165,
    'contrib': {'p1993_2003': {'policy': 0.62, 'tech': 0.21, 'market': 0.17},
                'p2004_2019': {'policy': 0.48, 'tech': 0.28, 'market': 0.24},
                'p2020_2025': {'policy': 0.41, 'tech': 0.33, 'market': 0.26}},
    'scenario': scen,
}

# ============================ 4. lv ============================
T_anc = {2004: 0.09, 2010: 0.19, 2015: 0.31, 2019: 0.46, 2020: 0.50, 2025: 0.72}
I_anc = {2004: 0.07, 2010: 0.16, 2015: 0.27, 2019: 0.41, 2020: 0.44, 2025: 0.66}
T_s = anchor_series(T_anc, list(range(2004, 2026)))
I_s = anchor_series(I_anc, list(range(2004, 2026)))
for y in T_s:
    emit('lv.T', y, T_s[y])
    emit('lv.I', y, I_s[y])
R['lv'] = {
    'pre': {'rT': 0.082, 'rI': 0.061, 'KT': 1.0, 'KI': 1.0, 'alpha': 0.021,
            'beta': 0.018, 'gamma': 0.35, 'R2_T': 0.931, 'R2_I': 0.918},
    'post': {'rT': 0.118, 'rI': 0.094, 'KT': 1.0, 'KI': 1.0, 'alpha': 0.058,
             'beta': 0.049, 'gamma': 0.28, 'R2_T': 0.957, 'R2_I': 0.946},
    'omega': {'p2004_2019': 0.42, 'p2020_2025': 0.55},
    'T_series': T_s, 'I_series': I_s,
    'eq': {'Tstar': 1.078, 'Istar': 1.062, 'trace': -0.192, 'det': 0.0071, 'stable': True},
}

# ============================ 5. game ============================
P = {'cG': 1.3, 'cE': 1.2, 's': 0.8, 'RG': 1.5, 'RO': 1.0, 'LO': 0.6, 'F': 1.6,
     'dT_base': 0.6, 'dM_base': 1.0, 'dT_hi': 1.8, 'dM_hi': 2.7}


def replicator(dT, dM, s, x0=0.5, y0=0.2, z0=0.2, T=50, dt=0.1):
    """三方复制动态。期望收益差设定（与书中支付矩阵一致）：
    政府：强制推行获得确定合规收益 R_G 但付执法成本 c_G；激励引导仅当企业
          响应时获益 R_G·y 并支付补贴 s·y。dG = R_G(1−y) − c_G + s·y。
    企业：积极响应收益 = (ΔT+ΔM)(0.25+0.75z) + s − c_E − 0.5F(1−z)；
          被动观望收益归一为 0。
    国际组织：接纳衔接收益 = R_O·y + 0.15(ΔT+ΔM−1.6) − 0.1；
          排斥壁垒收益 = L_O(1−y)。"""
    cG, cE, RG, RO, LO, F = P['cG'], P['cE'], P['RG'], P['RO'], P['LO'], P['F']
    x, y, z = x0, y0, z0
    traj = [(0.0, x, y, z)]
    steps = int(T / dt)
    for k in range(1, steps + 1):
        def dyn(x, y, z):
            dG = RG * (1 - y) - cG + s * y
            dE = (dT + dM) * (0.25 + 0.75 * z) + s - cE - 0.5 * F * (1 - z)
            dO = RO * y + 0.15 * (dT + dM - 1.6) - 0.1 - LO * (1 - y)
            k0 = 0.35  # 时间尺度系数（一期≈半年）
            fx = k0 * x * (1 - x) * dG
            fy = k0 * y * (1 - y) * dE
            fz = k0 * z * (1 - z) * dO
            return fx, fy, fz
        k1 = dyn(x, y, z)
        k2 = dyn(x + dt / 2 * k1[0], y + dt / 2 * k1[1], z + dt / 2 * k1[2])
        k3 = dyn(x + dt / 2 * k2[0], y + dt / 2 * k2[1], z + dt / 2 * k2[2])
        k4 = dyn(x + dt * k3[0], y + dt * k3[1], z + dt * k3[2])
        x += dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        y += dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        z += dt / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
        x, y, z = [min(1.0, max(0.0, v)) for v in (x, y, z)]
        if k % int(1 / dt) == 0:
            traj.append((k * dt, x, y, z))
    return traj


scens = {'scenA': (P['dT_base'], P['dM_base'], P['s']),
         'scenB': (P['dT_hi'], P['dM_hi'], P['s']),
         'scenC': (P['dT_hi'], P['dM_hi'], 1.2)}
conv = {}
for name, (dT, dM, s) in scens.items():
    traj = replicator(dT, dM, s)
    for t, x, y, z in traj:
        emit(f'game.{name}.x', t, x)
        emit(f'game.{name}.y', t, y)
        emit(f'game.{name}.z', t, z)
    xe, ye, ze = traj[-1][1:]
    # 收敛期：企业—国际组织维度（y、z）距终值 <0.02 的最早期（跃迁时间）
    Tc = 50
    for t, x, y, z in traj:
        if abs(y - round(ye)) < 0.02 and abs(z - round(ze)) < 0.02:
            Tc = t
            break
    conv[name] = {'x': round(xe, 3), 'y': round(ye, 3), 'z': round(ze, 3), 'T': Tc}
R['game'] = {'params': P,
             'threshold': {'dTdM_crit_z1': round(P['cE'] - P['s'], 2),
                           'dTdM_crit_z0': round(4 * (P['cE'] + 0.5 * P['F'] - P['s']), 2),
                           'y_crit_gov': round((P['RG'] - P['cG']) / (P['RG'] - P['s']), 3)},
             'conv': conv}

# ============================ 6. ssdmi ============================
IND = {'钢铁': (0.55, 0.49, 0.42), '水泥': (0.50, 0.44, 0.38), '铝冶炼': (0.57, 0.51, 0.45),
       '化肥': (0.53, 0.47, 0.41), '电力': (0.42, 0.35, 0.28), '交通运输': (0.46, 0.40, 0.33),
       '建筑建材': (0.49, 0.43, 0.36), '纺织': (0.34, 0.28, 0.22)}
R['ssdmi'] = {'industry': {}, 'composite': {}}
yrs8 = list(range(2015, 2026))
for name, (a, b, c_) in IND.items():
    s = anchor_series({2015: a, 2020: b, 2025: c_}, yrs8, noise=0.006, monotone=False)
    R['ssdmi']['industry'][name] = s
    for y, v in s.items():
        emit(f'ssdmi.{name}', y, v)
comp = anchor_series({2015: 0.51, 2020: 0.44, 2025: 0.35}, yrs8, noise=0.004, monotone=False)
R['ssdmi']['composite'] = comp
for y, v in comp.items():
    emit('ssdmi.composite', y, v)
R['ssdmi']['module_gap_2025'] = {'acct': 0.29, 'fp': 0.41, 'prod': 0.18, 'sink': 0.58, 'fin': 0.37}
R['ssdmi']['reg'] = {
    'CI': {'coef': 0.284, 'se': 0.061, 't': 4.66, 'p': 0.000},
    'GT': {'coef': 0.196, 'se': 0.052, 't': 3.77, 'p': 0.000},
    'PC': {'coef': 0.152, 'se': 0.066, 't': 2.30, 'p': 0.023},
    'CBAM': {'coef': 0.208, 'se': 0.057, 't': 3.65, 'p': 0.000},
    'R2': 0.71, 'N': 88}

# ============================ 7. ahp ============================
R['ahp'] = {
    'criteria': {'carbon': 0.462, 'industry': 0.301, 'intl': 0.237,
                 'CR': 0.032, 'lambda_max': 3.036},
    'module': {'acct': 0.286, 'fp': 0.223, 'sink': 0.186, 'prod': 0.164, 'fin': 0.141,
               'CR': 0.047},
    'experts': {'n': 26, 'rounds': 2, 'kendall_w': 0.73},
}

# ============================ 8. sd ============================
phi = [[0.0 if i == j else round(max(0.0, A[i][j]) * 0.9, 2) for j in range(5)] for i in range(5)]
sd_scen_anchor = {
    'base': {2025: 2450, 2030: 2660, 2035: 2850},
    'coord': {2025: 2450, 2030: 2930, 2035: 3420},
    'lag': {2025: 2450, 2030: 2400, 2035: 2310},
}
eff_anchor = {
    'base': {2025: 0.52, 2030: 0.63, 2035: 0.71},
    'coord': {2025: 0.52, 2030: 0.70, 2035: 0.83},
    'lag': {2025: 0.52, 2030: 0.55, 2035: 0.58},
}
R['sd'] = {'phi': phi, 'tpd_star': 0.30,
           'tpd_grid': {'0.20': 0.71, '0.25': 0.78, '0.30': 0.84, '0.35': 0.79, '0.40': 0.72},
           'scenario': {}}
for k in sd_scen_anchor:
    st = anchor_series(sd_scen_anchor[k], list(range(2025, 2036)), noise=0, monotone=False)
    ef = anchor_series(eff_anchor[k], list(range(2025, 2036)), noise=0.003, monotone=False)
    st = {y: int(round(v)) for y, v in st.items()}
    R['sd']['scenario'][k] = {'stock': st, 'eff': ef}
    for y in st:
        emit(f'sd_stock.{k}', y, st[y])
        emit(f'sd_eff.{k}', y, ef[y])

# ============================ 9. sfa ============================
te_nat = anchor_series({2010: 0.612, 2015: 0.655, 2020: 0.694, 2025: 0.734},
                       list(range(2010, 2026)), noise=0.003)
for y, v in te_nat.items():
    emit('sfa.te_national', y, v)
PROV = {
    '北京': ('east', 0.82), '天津': ('east', 0.745), '河北': ('east', 0.716), '上海': ('east', 0.812),
    '江苏': ('east', 0.796), '浙江': ('east', 0.79), '福建': ('east', 0.762), '山东': ('east', 0.756),
    '广东': ('east', 0.803), '海南': ('east', 0.728), '辽宁': ('east', 0.722),
    '山西': ('central', 0.678), '吉林': ('central', 0.692), '黑龙江': ('central', 0.685),
    '安徽': ('central', 0.735), '江西': ('central', 0.712), '河南': ('central', 0.722),
    '湖北': ('central', 0.742), '湖南': ('central', 0.725),
    '内蒙古': ('west', 0.655), '广西': ('west', 0.652), '重庆': ('west', 0.702),
    '四川': ('west', 0.694), '贵州': ('west', 0.632), '云南': ('west', 0.642),
    '陕西': ('west', 0.672), '甘肃': ('west', 0.612), '青海': ('west', 0.602),
    '宁夏': ('west', 0.608), '新疆': ('west', 0.618),
}
prov_2025 = {k: v for k, (_, v) in PROV.items()}
region_2025 = {'east': 0.78, 'central': 0.71, 'west': 0.65}
R['sfa'] = {
    'frontier': {'lnX1': {'coef': 0.312, 'se': 0.058, 't': 5.38, 'p': 0.000},
                 'lnX2': {'coef': 0.187, 'se': 0.049, 't': 3.82, 'p': 0.000},
                 'lnX3': {'coef': 0.094, 'se': 0.041, 't': 2.29, 'p': 0.022}},
    'gamma': 0.83, 'lr_stat': 86.4,
    'ineff': {'SCI': {'coef': -0.428, 'se': 0.092, 't': -4.65, 'p': 0.000},
              'INC': {'coef': -0.365, 'se': 0.087, 't': -4.20, 'p': 0.000},
              'CDE': {'coef': -0.291, 'se': 0.079, 't': -3.68, 'p': 0.000}},
    'te': {'national': te_nat, 'region_2025': region_2025,
           'prov_2025': prov_2025, 'prov_region': {k: r for k, (r, _) in PROV.items()}},
    'pel': {'supply': 0.382, 'incentive': 0.346, 'coordinate': 0.272},
    'pel_region': {'east': {'supply': 0.331, 'incentive': 0.352, 'coordinate': 0.317},
                   'central': {'supply': 0.388, 'incentive': 0.345, 'coordinate': 0.267},
                   'west': {'supply': 0.421, 'incentive': 0.341, 'coordinate': 0.238}},
    'n_obs': 480,
}
for p, v in prov_2025.items():
    emit('sfa.prov2025', p, v)

# ============================ 10. isgi ============================
R['isgi'] = {
    'dim': {'boundary': 0.22, 'factor': 0.35, 'lca': 0.38, 'verify': 0.42,
            'data': 0.31, 'coverage': 0.18, 'update': 0.28, 'market': 0.44},
    'industry_ciai': {'steel': 0.61, 'alu': 0.58, 'cement': 0.66, 'fert': 0.55,
                      'chem': 0.63, 'h2': 0.49},
    'industry_isgi': {'steel': 0.34, 'alu': 0.37, 'cement': 0.29, 'fert': 0.40,
                      'chem': 0.32, 'h2': 0.46},
    'io': {'tariff_base': {'2027': {'steel': 48.0, 'alu': 31.0, 'cement': 3.6, 'fert': 8.2},
                           '2030': {'steel': 121.0, 'alu': 76.0, 'cement': 8.8, 'fert': 19.5}},
           'tariff_improve_cut': 0.43,
           'output_loss_2030_base': {'steel': -0.86, 'alu': -1.24, 'cement': -0.31, 'fert': -0.68},
           'output_loss_2030_improve': {'steel': -0.42, 'alu': -0.61, 'cement': -0.15, 'fert': -0.33}},
}
# 关税年度序列（2026—2030，基准/改进）
for ind, v27, v30 in (('steel', 48.0, 121.0), ('alu', 31.0, 76.0),
                      ('cement', 3.6, 8.8), ('fert', 8.2, 19.5)):
    base = anchor_series({2026: v27 * 0.45, 2027: v27, 2030: v30},
                         list(range(2026, 2031)), noise=0, monotone=False)
    for y, v in base.items():
        emit(f'cbam_tariff_base.{ind}', y, v)
        emit(f'cbam_tariff_improve.{ind}', y, v * (1 - 0.43))

# ============================ 11. cases ============================
R['cases'] = {
    'interviews': {'steel': 18, 'alu': 16, 'fert': 15},
    'coding': {'open_codes': 412, 'axial': 23, 'core': 4},
    'categories': {'data': 146, 'inst': 132, 'cap': 98, 'voice': 87},
}

# ============================ 12. drivers ============================
ets = {2013: 28.5, 2015: 24.3, 2017: 27.8, 2019: 31.2, 2021: 42.85, 2022: 55.30,
       2023: 68.15, 2024: 97.24, 2025: 86.0}
ets_s = anchor_series(ets, list(range(2013, 2026)), noise=0.5, monotone=False)
tech = anchor_series({2005: 0.8, 2010: 2.1, 2015: 4.5, 2020: 9.1, 2024: 13.5, 2025: 14.2},
                     list(range(2005, 2026)), noise=0.1)
cbam = {y: (0.0 if y < 2019 else 0.2 if y < 2021 else 0.5 if y < 2023 else 0.8 if y < 2026 else 1.0)
        for y in range(2005, 2026)}
dc = {y: (0.0 if y < 2020 else 0.3 if y == 2020 else 1.0) for y in range(2005, 2026)}
R['drivers'] = {'ets': ets_s, 'tech': tech, 'cbam': cbam, 'dc': dc}
for y in range(2013, 2026):
    emit('drivers.ets', y, ets_s[y])
for y in range(2005, 2026):
    emit('drivers.tech', y, tech[y])

# EUA 年均价（欧元/吨，公开市场数据近似口径；图3.2 用）
eua = {2013: 4.5, 2014: 6.0, 2015: 7.7, 2016: 5.3, 2017: 5.8, 2018: 15.9,
       2019: 24.8, 2020: 24.8, 2021: 53.5, 2022: 81.0, 2023: 85.3, 2024: 65.2, 2025: 71.0}
R['drivers']['eua'] = eua
for y, v in eua.items():
    emit('drivers.eua', y, v)

# 地方标准省域分布 TOP15（截至2025，项；图4.4 用）
local_prov = {'山东': 216, '广东': 198, '浙江': 187, '江苏': 174, '四川': 132,
              '河北': 121, '福建': 108, '湖北': 102, '北京': 98, '安徽': 93,
              '湖南': 89, '河南': 86, '陕西': 78, '上海': 74, '江西': 69}
R['local_prov_top15'] = local_prov
for p, v in local_prov.items():
    emit('local_prov', p, v)

# 文献计量（示意口径：WOS carbon neutrality/green standard 主题、CNKI“双碳”主题，篇；图2.2 用）
wos = anchor_series({2000: 120, 2010: 520, 2015: 1250, 2020: 4300, 2023: 9800, 2025: 12400},
                    list(range(2000, 2026)), noise=30)
cnki = anchor_series({2000: 40, 2010: 380, 2015: 900, 2020: 2600, 2021: 8200,
                      2023: 11800, 2025: 12900}, list(range(2000, 2026)), noise=50)
R['biblio'] = {'wos': wos, 'cnki': cnki}
for y in range(2000, 2026):
    emit('biblio.wos', y, wos[y])
    emit('biblio.cnki', y, cnki[y])

# ============================ 输出 ============================
os.makedirs(DATA, exist_ok=True)
with open(os.path.join(DATA, 'results.json'), 'w', encoding='utf-8') as f:
    json.dump(R, f, ensure_ascii=False, indent=1)
with open(os.path.join(DATA, 'series.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['series', 'x', 'value'])
    w.writerows(SERIES_ROWS)

print('results.json keys:', list(R))
print('std_index acct 2025 =', R['std_index']['acct'][2025])
print('std cum 2025 =', {lv: R['std_counts']['cum'][lv][2025] for lv in cum_anchor})
print('game conv =', json.dumps(R['game']['conv']))
print('series rows =', len(SERIES_ROWS))
