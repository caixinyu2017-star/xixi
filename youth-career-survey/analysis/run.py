# -*- coding: utf-8 -*-
"""Run the planned analysis over the simulated dataset.

This is the pipeline that will be run, unchanged, on the collected data. It
is exercised here against simulated responses so that the tables, the sample
size and the reporting decisions are settled before fieldwork.
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
for p in ("design", "sim", "analysis"):
    sys.path.insert(0, os.path.join(ROOT, p))
import items as I                                             # noqa: E402
import simulate as SIM                                        # noqa: E402
import stats as ST                                            # noqa: E402

OUT = os.path.join(ROOT, "out")
os.makedirs(OUT, exist_ok=True)
T0 = time.time()


def log(m):
    print("[%6.1fs] %s" % (time.time() - T0, m))


def tsv(name, header, rows):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write("\t".join(header) + "\n")
        for r in rows:
            fh.write("\t".join(str(c) for c in r) + "\n")
    log("   写出 %s（%d 行）" % (name, len(rows)))


def f2(x):
    return "%.2f" % x


def f3(x):
    return "%.3f" % x


def star(p):
    return "***" if p < .001 else "**" if p < .01 else "*" if p < .05 else ""


# ==========================================================================
S = {}
log("生成模拟作答 ...")
data, truth, meta = SIM.simulate()
S["sample"] = meta
n = meta["n_valid"]
log("   有效样本 %d（发放 %d）" % (n, meta["n_collected"]))

# ---------------------------------------------------------------- scoring
scored = {}
for con in I.CONSTRUCTS:
    _, k = I.SCALES[con.scale]
    cols = []
    for code, _, rev in con.items:
        v = data[code].astype(float)
        cols.append((k + 1 - v) if rev else v)      # reverse-key back
    M = np.column_stack(cols)
    scored[con.key] = M
    data[con.key + "_mean"] = M.mean(axis=1)

V = {c.key: data[c.key + "_mean"] for c in I.CONSTRUCTS}
CTRL = np.column_stack([data[c].astype(float) for c in I.CONTROLS])

# ============================================================== Table 1
log("表 1 样本特征 ...")
LAB = {c: (name, opts) for c, name, opts in I.DEMO}
rows = []
for code in I.CONTROLS:
    name, opts = LAB[code]
    for o in opts:
        val = int(o.split()[0])
        cnt = int((data[code] == val).sum())
        rows.append([name, o, cnt, "%.1f" % (100.0 * cnt / n)])
tsv("t1_sample.tsv", ["变量", "类别", "人数", "占比(%)"], rows)
S["demographics"] = {c: {int(v): int((data[c] == v).sum())
                         for v in sorted(set(data[c].tolist()))}
                     for c in I.CONTROLS}

# ============================================================== Table 2
log("表 2 验证性因子分析与信度 ...")
sub = [c for c in I.CONSTRUCTS if c.key in I.SUBSTANTIVE]
allitems, blocks, pos = [], [], 0
for con in sub:
    idx = list(range(pos, pos + len(con.items)))
    blocks.append((con.key, idx))
    allitems.append(scored[con.key])
    pos += len(con.items)
X = np.column_stack(allitems)
fit = ST.cfa(X, blocks)
log("   chi2/df %.2f  CFI %.3f  TLI %.3f  RMSEA %.3f  SRMR %.3f"
    % (fit["ratio"], fit["cfi"], fit["tli"], fit["rmsea"], fit["srmr"]))

rows, rel = [], {}
for f, (key, idx) in enumerate(blocks):
    con = I.BY_KEY[key]
    lam = fit["loadings"][idx]
    th = fit["residuals"][idx]
    a = ST.cronbach_alpha(scored[key])
    om, ave = ST.omega_cr_ave(lam, th)
    rel[key] = dict(alpha=float(a), omega=om, ave=ave,
                    lam_min=float(lam.min()), lam_max=float(lam.max()))
    rows.append([con.cn, len(idx), "%.2f–%.2f" % (lam.min(), lam.max()),
                 f2(a), f2(om), f2(ave)])
tsv("t2_measurement.tsv",
    ["构念", "条目数", "标准化载荷", "Cronbach α", "CR (ω)", "AVE"], rows)
S["cfa"] = {k: fit[k] for k in
            ("chi2", "df", "ratio", "cfi", "tli", "rmsea", "srmr",
             "converged")}
S["reliability"] = rel

# competing measurement models: does splitting parental involvement help?
log("   竞争模型比较 ...")
comp = []
merged = [("CA", blocks[0][1]), ("CE", blocks[1][1]), ("SE", blocks[2][1]),
          ("P", blocks[3][1] + blocks[4][1] + blocks[5][1]),
          ("CD", blocks[6][1])]
f5 = ST.cfa(X, merged)
one = [("G", list(range(X.shape[1])))]
f1 = ST.cfa(X, one)
for nm, f in (("七因子（假设模型）", fit), ("五因子（父母三量表合并）", f5),
              ("单因子", f1)):
    comp.append([nm, "%.1f" % f["chi2"], f["df"], f2(f["ratio"]),
                 f3(f["cfi"]), f3(f["tli"]), f3(f["rmsea"]), f3(f["srmr"])])
tsv("t3_model_comparison.tsv",
    ["测量模型", "χ²", "df", "χ²/df", "CFI", "TLI", "RMSEA", "SRMR"], comp)
S["model_comparison"] = {
    "seven": {k: f5 and fit[k] for k in ("chi2", "df", "cfi", "rmsea")},
    "five": {k: f5[k] for k in ("chi2", "df", "cfi", "rmsea")},
    "one": {k: f1[k] for k in ("chi2", "df", "cfi", "rmsea")}}

H = ST.htmt(X, blocks)
rows = []
for i, (a, _) in enumerate(blocks):
    rows.append([I.BY_KEY[a].cn] + [f2(H[i, j]) if j < i else ""
                                    for j in range(len(blocks))])
tsv("t4_htmt.tsv", [""] + [I.BY_KEY[a].cn for a, _ in blocks], rows)
S["htmt_max"] = float(H[np.triu_indices(len(blocks), 1)].max())

# ============================================================== CMB
log("共同方法偏差检验 ...")
XA = np.column_stack([scored[c.key] for c in I.CONSTRUCTS])
share, eig = ST.harman(XA)
mk = V["MK"]
raw, adj = {}, {}
for i, a in enumerate(I.SUBSTANTIVE):
    for b in I.SUBSTANTIVE[i + 1:]:
        raw["%s-%s" % (a, b)] = float(np.corrcoef(V[a], V[b])[0, 1])
        adj["%s-%s" % (a, b)] = ST.partial_corr(V[a], V[b], mk)
shift = max(abs(raw[k] - adj[k]) for k in raw)
sign_flips = sum(1 for k in raw
                 if (abs(raw[k]) > .098) != (abs(adj[k]) > .098))
S["cmb"] = dict(harman_first=share, eigen=eig,
                marker_alpha=float(ST.cronbach_alpha(scored["MK"])),
                marker_max_r=float(max(abs(np.corrcoef(V[k], mk)[0, 1])
                                       for k in I.SUBSTANTIVE)),
                max_shift=float(shift), sign_flips=int(sign_flips))
log("   Harman 首因子 %.1f%%；标记变量校正后相关最大变动 %.3f"
    % (100 * share, shift))

# ============================================================== Table 5
log("表 5 描述统计与相关 ...")
keys = I.SUBSTANTIVE
rows = []
for i, a in enumerate(keys):
    con = I.BY_KEY[a]
    _, k = I.SCALES[con.scale]
    r = ["%d. %s" % (i + 1, con.cn), "1–%d" % k,
         f2(V[a].mean()), f2(V[a].std(ddof=1))]
    for j, b in enumerate(keys):
        if j < i:
            rr = float(np.corrcoef(V[a], V[b])[0, 1])
            t = rr * np.sqrt((n - 2) / max(1e-12, 1 - rr ** 2))
            from scipy import stats as _s
            p = 2 * _s.t.sf(abs(t), n - 2)
            r.append(("%.2f" % rr).replace("0.", ".").replace("-.", "−.")
                     + star(p))
        elif j == i:
            r.append("(%s)" % f2(rel[a]["alpha"]))
        else:
            r.append("")
    rows.append(r)
tsv("t5_correlations.tsv",
    ["构念", "量程", "M", "SD"] + [str(i + 1) for i in range(len(keys))],
    rows)
S["correlations"] = raw

# ============================================================== Table 6
log("表 6 层级回归与调节效应 ...")
zs = {k: ST.z(V[k]) for k in keys}
zc = np.column_stack([ST.z(CTRL[:, j]) for j in range(CTRL.shape[1])])

m1 = ST.ols(zc, zs["CD"], I.CONTROLS)
main = np.column_stack([zc, zs["CA"], zs["PA"], zs["PD"], zs["PF"]])
m2 = ST.ols(main, zs["CD"], I.CONTROLS + ["CA", "PA", "PD", "PF"])
ints = np.column_stack([zs["CA"] * zs["PA"], zs["CA"] * zs["PD"],
                        zs["CA"] * zs["PF"]])
m3 = ST.ols(np.column_stack([main, ints]), zs["CD"],
            I.CONTROLS + ["CA", "PA", "PD", "PF",
                          "CA×PA", "CA×PD", "CA×PF"])

NAME = {"CA": "职业决策焦虑", "PA": "自主支持型支持", "PD": "指导代办型介入",
        "PF": "参与频率", "CA×PA": "焦虑 × 自主支持",
        "CA×PD": "焦虑 × 指导代办", "CA×PF": "焦虑 × 参与频率",
        "SE": "职业决策自我效能", "CE": "职业探索行为"}
rows = []
for lab in ["CA", "PA", "PD", "PF", "CA×PA", "CA×PD", "CA×PF"]:
    r = [NAME[lab]]
    for mdl in (m1, m2, m3):
        if lab in mdl["names"]:
            i = mdl["names"].index(lab)
            r.append(f2(mdl["b"][i]) + star(mdl["p"][i]))
        else:
            r.append("")
    rows.append(r)
rows.append(["控制变量", "已控制", "已控制", "已控制"])
rows.append(["R²", f3(m1["r2"]), f3(m2["r2"]), f3(m3["r2"])])
rows.append(["调整 R²", f3(m1["adj_r2"]), f3(m2["adj_r2"]), f3(m3["adj_r2"])])
f21, p21 = ST.delta_f(m2["r2"], m1["r2"], 4, n, main.shape[1])
f32, p32 = ST.delta_f(m3["r2"], m2["r2"], 3, n, main.shape[1] + 3)
rows.append(["ΔR²", "", f3(m2["r2"] - m1["r2"]), f3(m3["r2"] - m2["r2"])])
rows.append(["ΔF", "", "%.2f%s" % (f21, star(p21)),
             "%.2f%s" % (f32, star(p32))])
tsv("t6_hierarchical.tsv", ["预测变量", "模型 1", "模型 2", "模型 3"], rows)

vifs = ST.vif(np.column_stack([main, ints]))
S["regression"] = dict(
    r2=[m1["r2"], m2["r2"], m3["r2"]],
    delta=[[m2["r2"] - m1["r2"], f21, p21], [m3["r2"] - m2["r2"], f32, p32]],
    max_vif=float(vifs.max()),
    coef={lab: dict(b=float(m3["b"][m3["names"].index(lab)]),
                    se=float(m3["se"][m3["names"].index(lab)]),
                    t=float(m3["t"][m3["names"].index(lab)]),
                    p=float(m3["p"][m3["names"].index(lab)]))
          for lab in ["CA", "PA", "PD", "PF", "CA×PA", "CA×PD", "CA×PF"]})
log("   焦虑×自主支持 β=%.3f p=%.4f | 焦虑×指导代办 β=%.3f p=%.4f | "
    "焦虑×频率 β=%.3f p=%.4f"
    % (S["regression"]["coef"]["CA×PA"]["b"],
       S["regression"]["coef"]["CA×PA"]["p"],
       S["regression"]["coef"]["CA×PD"]["b"],
       S["regression"]["coef"]["CA×PD"]["p"],
       S["regression"]["coef"]["CA×PF"]["b"],
       S["regression"]["coef"]["CA×PF"]["p"]))

# ============================================================== Table 7
log("表 7 简单斜率 ...")
rows, slopes = [], {}
for w in ("PA", "PD", "PF"):
    s = ST.simple_slopes(zs["CA"], zs[w], zs["CD"], zc)
    slopes[w] = dict(low=s["low"], high=s["high"], inter=s["inter"])
    rows.append([NAME[w], f2(s["low"]), f2(s["high"]),
                 f2(s["high"] - s["low"]),
                 "放大" if s["inter"] > 0 else "缓冲"])
tsv("t7_simple_slopes.tsv",
    ["调节变量", "低水平（−1 SD）斜率", "高水平（+1 SD）斜率", "差值",
     "方向"], rows)
S["simple_slopes"] = slopes

# ============================================================== Table 8
log("表 8 链式中介（Bootstrap 5000 次）...")
med = ST.serial_mediation(zs["CA"], zs["CE"], zs["SE"], zs["CD"],
                          cov=zc, boots=5000, seed=SIM.SEED % 10000)
PATHS = [("总效应（焦虑 → 困难）", "total", None),
         ("直接效应", "cdash", None),
         ("间接效应：焦虑 → 探索 → 困难", "ind_m1", "ind_m1"),
         ("间接效应：焦虑 → 自我效能 → 困难", "ind_m2", "ind_m2"),
         ("链式：焦虑 → 探索 → 自我效能 → 困难", "ind_serial", "ind_serial"),
         ("间接效应合计", "total_ind", "total_ind")]
rows = []
for lab, key, ci in PATHS:
    c = ("[%s, %s]" % (f3(med["ci"][ci][0]), f3(med["ci"][ci][1]))
         if ci else "—")
    rows.append([lab, f3(med[key]), c])
tsv("t8_mediation.tsv", ["路径", "效应值", "95% Bootstrap 区间"], rows)
S["mediation"] = {k: (float(v) if isinstance(v, (int, float, np.floating))
                      else v) for k, v in med.items() if k != "ci"}
S["mediation"]["ci"] = med["ci"]

# ============================================================== power
log("检验力：在若干样本量下各重复抽取 400 次研究 ...")
REPS = 400
GRID = [400, 500, 600, 700, 800, 900, 1000]
LABS = ("CA×PA", "CA×PD", "CA×PF")
rng = np.random.default_rng(4242)
curve = {}
for nn in GRID:
    hits = {k: 0 for k in LABS}
    bs = {k: [] for k in LABS}
    for r in range(REPS):
        d2, _, _ = SIM.simulate(n_valid=nn, seed=int(rng.integers(1, 10 ** 8)))
        vv = {}
        for con in I.CONSTRUCTS:
            _, kk = I.SCALES[con.scale]
            cs = [(kk + 1 - d2[c].astype(float)) if rv
                  else d2[c].astype(float) for c, _, rv in con.items]
            vv[con.key] = ST.z(np.column_stack(cs).mean(axis=1))
        cc = np.column_stack([ST.z(d2[c].astype(float)) for c in I.CONTROLS])
        dm = np.column_stack([cc, vv["CA"], vv["PA"], vv["PD"], vv["PF"],
                              vv["CA"] * vv["PA"], vv["CA"] * vv["PD"],
                              vv["CA"] * vv["PF"]])
        f = ST.ols(dm, vv["CD"])
        j0 = dm.shape[1] - 3
        for j, k in enumerate(LABS):
            bs[k].append(f["b"][j0 + j + 1])
            hits[k] += int(f["p"][j0 + j + 1] < .05)
    curve[nn] = {k: dict(power=hits[k] / REPS, mean_b=float(np.mean(bs[k])),
                         sd_b=float(np.std(bs[k], ddof=1))) for k in LABS}
    log("   n=%4d  放大 %.1f%%  缓冲 %.1f%%  频率 %.1f%%"
        % (nn, 100 * curve[nn]["CA×PA"]["power"],
           100 * curve[nn]["CA×PD"]["power"],
           100 * curve[nn]["CA×PF"]["power"]))
S["power_curve"] = {str(k): v for k, v in curve.items()}
S["power"] = curve[400]

rows = [[str(nn),
         "%.3f" % curve[nn]["CA×PA"]["mean_b"],
         "%.1f" % (100 * curve[nn]["CA×PA"]["power"]),
         "%.3f" % curve[nn]["CA×PD"]["mean_b"],
         "%.1f" % (100 * curve[nn]["CA×PD"]["power"]),
         "%.3f" % curve[nn]["CA×PF"]["mean_b"],
         "%.1f" % (100 * curve[nn]["CA×PF"]["power"])] for nn in GRID]
tsv("t9_power.tsv",
    ["有效样本量", "焦虑×自主支持 β", "检出率(%)", "焦虑×指导代办 β",
     "检出率(%)", "焦虑×参与频率 β", "检出率(%)"], rows)

need = next((nn for nn in GRID
             if min(curve[nn]["CA×PA"]["power"],
                    curve[nn]["CA×PD"]["power"]) >= 0.80), None)
S["required_n"] = need
log("   两个关键交互同时达到 80%% 检出率所需有效样本：%s"
    % (need if need else ">1000"))

# ==========================================================================
S["meta"] = dict(seed=meta["seed"], n=n, boots=5000, power_reps=REPS, power_grid=GRID,
                 runtime_s=round(time.time() - T0, 1),
                 simulated=True,
                 note=("本文件中的全部数值均由 sim/simulate.py 生成的模拟"
                       "作答计算得到，不含任何真实被试数据。"))
with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as fh:
    json.dump(S, fh, ensure_ascii=False, indent=1)
np.save(os.path.join(OUT, "scored.npy"),
        np.column_stack([V[k] for k in keys]))
with open(os.path.join(OUT, "dataset.json"), "w", encoding="utf-8") as fh:
    json.dump({k: np.asarray(v).tolist() for k, v in data.items()
               if k in SIM.ORDER}, fh)
log("完成，用时 %.1f 秒" % (time.time() - T0))
