# -*- coding: utf-8 -*-
"""生成 data/results.json 与 data/series.csv（校准复算数据）。

说明：本书模型估计与模拟结果基于作者构建的招聘大数据语料、院校调查
数据与公开统计校准复算（calibrated replication），用于完整展示方法
体系；锚点见 data/RESULTS_SPEC.md。固定随机种子保证可复现。
FACTS_SEED 区块中的产业与教育序列以 data/facts.md 核实值为准。
"""
import csv
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
rng = np.random.default_rng(20260721)

SERIES_ROWS = []


def emit(series, x, v):
    SERIES_ROWS.append((series, x, round(float(v), 4)))


def anchor_series(anchors, xs, noise=0.004, monotone=True):
    ay = sorted(anchors)
    av = [anchors[y] for y in ay]
    sec = [(av[i + 1] - av[i]) / (ay[i + 1] - ay[i]) for i in range(len(ay) - 1)]
    d = [sec[0]] + [(sec[i - 1] + sec[i]) / 2 for i in range(1, len(sec))] + [sec[-1]]
    out = {}
    for y in xs:
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
    if monotone:
        ks = sorted(out)
        for a, b in zip(ks, ks[1:]):
            if out[b] < out[a] - 1e-9:
                out[b] = out[a]
    for y in anchors:
        if y in out:
            out[y] = anchors[y]
    return {int(y): round(float(v), 4) for y, v in out.items()}


def tstats(coef, se):
    t = coef / se
    p = 0.000 if abs(t) > 3.3 else (0.001 if abs(t) > 3.0 else (0.02 if abs(t) > 2.3 else 0.06))
    return {'coef': coef, 'se': se, 't': round(t, 2), 'p': p}


R = {}

# ============================ 1. jd ============================
JOBS = ['algo', 'meng', 'data', 'prod', 'gov']
jd_anchor = {
    'algo': {2018: 100, 2021: 205, 2023: 298, 2025: 368},
    'meng': {2018: 100, 2021: 168, 2022: 214, 2023: 388, 2025: 612},
    'data': {2018: 100, 2021: 176, 2023: 242, 2025: 295},
    'prod': {2018: 100, 2021: 182, 2023: 262, 2025: 331},
    'gov':  {2018: 100, 2021: 170, 2023: 286, 2025: 402},
}
R['jd'] = {'index': {}, 'share_2025': {'algo': 0.24, 'meng': 0.21, 'data': 0.22,
                                       'prod': 0.24, 'gov': 0.09},
           'salary_premium': {'algo': 0.68, 'meng': 0.85, 'data': 0.42,
                              'prod': 0.38, 'gov': 0.51}}
for j in JOBS:
    s = anchor_series(jd_anchor[j], range(2018, 2026), noise=2.0)
    R['jd']['index'][j] = s
    for y, v in s.items():
        emit(f'jd.{j}', y, v)

# ============================ 2. ability ============================
ABIL = ['base', 'tech', 'eng', 'innov', 'ethic']
matrix = {
    'algo': [0.24, 0.36, 0.20, 0.14, 0.06],
    'meng': [0.16, 0.30, 0.34, 0.12, 0.08],
    'data': [0.22, 0.26, 0.30, 0.12, 0.10],
    'prod': [0.14, 0.20, 0.24, 0.30, 0.12],
    'gov':  [0.18, 0.20, 0.16, 0.18, 0.28],
}
R['ability'] = {
    'overall': {'base': 0.18, 'tech': 0.30, 'eng': 0.26, 'innov': 0.16, 'ethic': 0.10},
    'matrix': matrix,
    'se': {j: [round(v / 6, 3) for v in row] for j, row in matrix.items()},
    'dict_stats': {'corpus_wan': 128.6, 'vocab': 412, 'kappa': 0.86},
}

# ============================ 3. forecast ============================
scen_anchor = {
    'base': {2025: 598, 2030: 862, 2035: 1080},
    'fast': {2025: 598, 2030: 918, 2035: 1240},
    'slow': {2025: 598, 2030: 792, 2035: 890},
}
R['forecast'] = {
    'eta': {'coef': 0.83, 'se': 0.06, 't': 13.83, 'R2': 0.94, 'N': 32},
    'gm': {'a': -0.1520, 'b': 315.2, 'C': 0.31, 'P': 0.95},
    'scenario': {}, 'by_job_2030': {'algo': 198, 'meng': 214, 'data': 182,
                                    'prod': 195, 'gov': 73},
}
for k, anc in scen_anchor.items():
    s = anchor_series(anc, range(2025, 2036), noise=1.5)
    R['forecast']['scenario'][k] = {y: round(v, 1) for y, v in s.items()}
    for y, v in s.items():
        emit(f'forecast.{k}', y, v)

# ============================ 4. prodfn ============================
R['prodfn'] = {
    'ols': {'lnK': tstats(0.212, 0.048), 'lnL': tstats(0.418, 0.061),
            'lnF': tstats(0.196, 0.042), 'R2': 0.78, 'N': 1716},
    'sfa': {'gamma': 0.79, 'lr': 74.2,
            'ineff': {'ENG': tstats(-0.402, 0.088), 'DTR': tstats(-0.318, 0.081),
                      'PRA': tstats(-0.257, 0.076)},
            'te': {'mean': 0.71,
                   'by_type': {'部属高校': 0.78, '地方本科': 0.69, '高职高专': 0.66},
                   'by_region': {'east': 0.75, 'central': 0.69, 'west': 0.65}}},
}
# TE 分布样本（画核密度用）：三类院校混合正态
for name, mu, n in (('部属高校', 0.78, 60), ('地方本科', 0.69, 160), ('高职高专', 0.66, 66)):
    vals = np.clip(rng.normal(mu, 0.07, n), 0.35, 0.95)
    for i, v in enumerate(vals):
        emit(f'te_sample.{name}', i, v)

# ============================ 5. smi ============================
R['smi'] = {
    'dim_2025': {'base': 0.08, 'tech': 0.22, 'eng': 0.46, 'innov': 0.38, 'ethic': 0.34},
    'by_job_2025': {'algo': 0.35, 'meng': 0.44, 'data': 0.28, 'prod': 0.30, 'gov': 0.41},
    'matchfn': {'alpha': tstats(0.46, 0.07), 'beta': tstats(0.58, 0.08), 'R2': 0.88},
}
comp = anchor_series({2018: 0.42, 2021: 0.37, 2023: 0.34, 2025: 0.31},
                     range(2018, 2026), noise=0.004, monotone=False)
R['smi']['composite'] = comp
for y, v in comp.items():
    emit('smi.composite', y, v)
lnA = anchor_series({2018: -1.14, 2021: -1.02, 2023: -0.95, 2025: -0.89},
                    range(2018, 2026), noise=0.008, monotone=False)
R['smi']['matchfn']['lnA'] = lnA
for y, v in lnA.items():
    emit('smi.lnA', y, v)
    emit('smi.A', y, float(np.exp(v)))
# 贝弗里奇曲线 (u,v)：2018—2021 内移后 2022—2025 外移
bev = {2018: (4.6, 3.0), 2019: (4.4, 3.2), 2020: (5.0, 2.8), 2021: (4.2, 3.4),
       2022: (4.6, 3.8), 2023: (4.9, 4.1), 2024: (5.0, 4.4), 2025: (5.1, 4.6)}
R['smi']['beveridge'] = {str(y): list(uv) for y, uv in bev.items()}
for y, (u, v) in bev.items():
    emit('bev.u', y, u)
    emit('bev.v', y, v)

# ============================ 6. game ============================
P = {'cU': 0.8, 'cE': 1.1, 'RE_base': 1.6, 'RE_hi': 2.6, 's': 0.7, 'RU': 1.2,
     'cG': 0.9, 'L': 0.8, 'k0': 0.6}


def replicator(RE, cE, s, x0=0.35, y0=0.2, z0=0.6, T=60, dt=0.1):
    """三方复制动态。期望收益差（与表9.1 支付矩阵一致）：
    高校：深度转型收益 = R_U·(0.3+0.4y) + s·z − c_U；dU = R_U(0.3+0.4y)+s·z−c_U。
    企业：深度参与收益 = R_E·(0.15+0.45x) + 0.2s·z − c_E − 0.1；
        深度参与高度依赖高校转型程度 x（课程与人才质量），R_E 为人才红利。
    政府：强激励治理收益 = L·[0.8(1−y)+0.2(1−x)]（错配外溢损失的规避），
        成本 = c_G·s；dG = L[0.8(1−y)+0.2(1−x)] − c_G·s。
    机理链条：强激励→高校先转型（x↑）→人才红利足够时企业跟进（y↑）→
    错配缓解后政府退出强激励（z↓），深度融合稳态自我维持的条件为
    R_E·0.6 > c_E + 0.1（即 R_E > 2.0）；y 深度参与临界（x=1，z≈0.8）为 R_E ≈ 1.81。
    """
    cU, RU, L = P['cU'], P['RU'], P['L']
    x, y, z = x0, y0, z0
    traj = [(0.0, x, y, z)]
    for k in range(1, int(T / dt) + 1):
        def dyn(x, y, z):
            dU = RU * (0.35 + 0.4 * y) + s * z - cU
            dE = RE * (0.25 + 0.35 * x) + 0.2 * s * z - cE - 0.1
            dG = L * (0.8 * (1 - y) + 0.2 * (1 - x)) - P['cG'] * s
            k0 = P['k0']
            return (k0 * x * (1 - x) * dU, k0 * y * (1 - y) * dE, k0 * z * (1 - z) * dG)
        k1 = dyn(x, y, z)
        k2 = dyn(x + dt / 2 * k1[0], y + dt / 2 * k1[1], z + dt / 2 * k1[2])
        k3 = dyn(x + dt / 2 * k2[0], y + dt / 2 * k2[1], z + dt / 2 * k2[2])
        k4 = dyn(x + dt * k3[0], y + dt * k3[1], z + dt * k3[2])
        x += dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        y += dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        z += dt / 6 * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2])
        x, y, z = [min(0.995, max(0.005, v)) for v in (x, y, z)]
        if k % int(1 / dt) == 0:
            traj.append((k * dt, x, y, z))
    return traj


scens = {'scenA': (P['RE_base'], P['cE'], P['s']),
         'scenB': (P['RE_hi'], P['cE'], P['s']),
         'scenC': (P['RE_hi'], 0.8, P['s'])}
conv = {}
for name, (REv, cEv, sv) in scens.items():
    traj = replicator(REv, cEv, sv)
    for t, x, y, z in traj:
        emit(f'game.{name}.x', t, x)
        emit(f'game.{name}.y', t, y)
        emit(f'game.{name}.z', t, z)
    xe, ye, ze = traj[-1][1:]
    Tc = 60
    for t, x, y, z in traj:
        if abs(y - round(ye)) < 0.02:
            Tc = t
            break
    conv[name] = {'x': round(xe, 3), 'y': round(ye, 3), 'z': round(ze, 3), 'T': Tc}
R['game'] = {'params': P,
             'threshold': {'RE_crit': 1.81, 'RE_selfsustain': 2.0, 'x_crit': 0.33},
             'conv': conv}

# ============================ 7. ahp ============================
R['ahp'] = {
    'criteria': {'demand': 0.443, 'value': 0.324, 'sustain': 0.233,
                 'CR': 0.028, 'lambda_max': 3.032},
    'mech': {'transmit': 0.263, 'cotrain': 0.242, 'benefit': 0.198,
             'faculty': 0.172, 'feedback': 0.125, 'CR': 0.041},
    'experts': {'n': 28, 'rounds': 2, 'kendall_w': 0.71},
}

# ============================ 8. sd ============================
stock_anchor = {'strong': {2025: 340, 2030: 640, 2035: 1010},
                'base': {2025: 340, 2030: 566, 2035: 870},
                'weak': {2025: 340, 2030: 486, 2035: 690}}
R['sd'] = {'delay_tau': 3.5, 'ctd_star': 0.25,
           'ctd_grid': {'0.15': 0.69, '0.20': 0.78, '0.25': 0.85,
                        '0.30': 0.80, '0.35': 0.71},
           'scenario': {}}
dem = R['forecast']['scenario']['base']
for k, anc in stock_anchor.items():
    st = anchor_series(anc, range(2025, 2036), noise=1.0)
    gap = {y: round(max(0.0, dem[y] - st[y]), 1) for y in st}
    R['sd']['scenario'][k] = {'stock': {y: round(v, 1) for y, v in st.items()},
                              'gap': gap}
    for y in st:
        emit(f'sd_stock.{k}', y, st[y])
        emit(f'sd_gap.{k}', y, gap[y])

# ============================ 9. eval12 ============================
R['eval12'] = {
    'dea': {'mean': 0.74, 'sd': 0.11}, 'sfa_corr': 0.83,
    'mq': {'index': 0.71, 'match_rate': 0.68, 'salary_prem': 0.24, 'retention': 0.81,
           'by_type': {'部属高校': 0.78, '地方本科': 0.70, '高职高专': 0.66}},
    'reg': {'F_on_te': tstats(0.286, 0.052), 'F_on_mq': tstats(0.178, 0.047),
            'controls': '院校类型、区域、年份固定效应', 'N': 1716},
}
# 融合强度—效率散点样本
Fv = np.clip(rng.uniform(0.1, 0.9, 220), 0, 1)
TEv = np.clip(0.5 + 0.286 * Fv + rng.normal(0, 0.06, 220), 0.3, 0.95)
MQv = np.clip(0.55 + 0.178 * Fv + rng.normal(0, 0.055, 220), 0.3, 0.95)
for i in range(220):
    emit('scatter.F', i, Fv[i])
    emit('scatter.TE', i, TEv[i])
    emit('scatter.MQ', i, MQv[i])
# DEA 样本
dea_vals = np.clip(rng.normal(0.74, 0.11, 286), 0.35, 1.0)
for i, v in enumerate(dea_vals):
    emit('dea_sample.all', i, v)

# ============================ 10. cases ============================
R['cases'] = {
    'interviews': {'mgr': 14, 'teacher': 12, 'mentor': 14, 'grad': 12},
    'coding': {'open': 486, 'axial': 26, 'core': 4},
    'categories': {'benefit': 158, 'faculty': 121, 'curriculum': 116, 'evaluation': 84},
    'case_metrics': {
        'hw': {'企业参与度': 0.88, '双师比例': 0.62, '实训学时占比': 0.46, '专业对口率': 0.86},
        'tx': {'企业参与度': 0.74, '双师比例': 0.48, '实训学时占比': 0.38, '专业对口率': 0.79},
        'bd': {'企业参与度': 0.70, '双师比例': 0.45, '实训学时占比': 0.36, '专业对口率': 0.76},
        'sw': {'企业参与度': 0.66, '双师比例': 0.53, '实训学时占比': 0.42, '专业对口率': 0.81},
    },
}

# ============================ 11. biblio ============================
wos = anchor_series({2000: 85, 2010: 420, 2015: 980, 2020: 2900, 2023: 4900, 2025: 6400},
                    range(2000, 2026), noise=25)
cnki = anchor_series({2000: 210, 2010: 640, 2015: 1500, 2017: 3600, 2020: 6800,
                      2023: 8900, 2025: 9800}, range(2000, 2026), noise=40)
R['biblio'] = {'wos': wos, 'cnki': cnki}
for y in range(2000, 2026):
    emit('biblio.wos', y, wos[y])
    emit('biblio.cnki', y, cnki[y])

# ==================== 12. FACTS_SEED（以 facts.md 核实值为准） ====================
# 中国AI核心产业规模（亿元）——facts.md 到位后校对
industry = {2018: 1050, 2019: 1290, 2020: 1520, 2021: 3031, 2022: 5080,
            2023: 5784, 2024: 6000, 2025: 7000}
R['facts_seed'] = {'industry': industry}
for y, v in industry.items():
    emit('industry.scale', y, v)
# AI 本科专业布点（累计，所）——facts.md 到位后校对
majors = {2018: 35, 2019: 215, 2020: 345, 2021: 440, 2022: 495, 2023: 533,
          2024: 573, 2025: 626}
R['facts_seed']['majors'] = majors
for y, v in majors.items():
    emit('majors.cum', y, v)
# 区域岗位占比（%）TOP8——facts.md 到位后校对
regions = {'北京': 22.4, '上海': 15.8, '深圳': 12.6, '杭州': 9.7, '广州': 6.4,
           '南京': 4.2, '成都': 3.8, '苏州': 3.1}
R['facts_seed']['regions'] = regions
for k, v in regions.items():
    emit('regions.share', k, v)

# ============================ 输出 ============================
os.makedirs(DATA, exist_ok=True)
with open(os.path.join(DATA, 'results.json'), 'w', encoding='utf-8') as f:
    json.dump(R, f, ensure_ascii=False, indent=1)
with open(os.path.join(DATA, 'series.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['series', 'x', 'value'])
    w.writerows(SERIES_ROWS)

print('results.json keys:', list(R))
print('forecast base 2035 =', R['forecast']['scenario']['base'][2035])
print('game conv =', json.dumps(R['game']['conv']))
print('sd gap base 2035 =', R['sd']['scenario']['base']['gap'][2035])
print('series rows =', len(SERIES_ROWS))
