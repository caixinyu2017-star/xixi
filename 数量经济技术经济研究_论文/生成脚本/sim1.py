# -*- coding: utf-8 -*-
"""论文一：数字基础设施与家庭创业——"宽带中国"多期DID模拟。
生成CFPS风格个体面板，内置真实处理效应，估计TWFE-DID、事件研究、机制与异质性，
输出表格数值(json)与图1(事件研究)、图2(趋势图)。"""
import numpy as np, pandas as pd, json
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

rng = np.random.default_rng(20260705)
FP = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
zh = fm.FontProperties(fname=FP)
plt.rcParams["axes.unicode_minus"] = False

# ---------- 1. 生成城市与处理时点 ----------
n_city = 150
waves = [2012, 2014, 2016, 2018, 2020]
# 处理批次：2014/2015/2016三批"宽带中国"试点，映射到最近调查波次的处理后状态
# 约60%城市为试点城市，处理年份∈{2014,2016}（对应CFPS波次），其余为控制城市
treat_year = {}
for c in range(n_city):
    r = rng.random()
    if r < 0.30:
        treat_year[c] = 2014
    elif r < 0.58:
        treat_year[c] = 2016
    else:
        treat_year[c] = 9999  # 从未处理
city_fe = rng.normal(0, 0.05, n_city)
east = (rng.random(n_city) < 0.45).astype(int)  # 东部
year_fe = {y: v for y, v in zip(waves, rng.normal(0, 0.02, len(waves)) + np.linspace(0, 0.03, len(waves)))}

# ---------- 2. 生成家庭 ----------
n_hh = 6000
rows = []
BETA_P = 0.028             # 概率尺度核心效应(单位:pp)，经异质性放大后基准≈4-5pp
for i in range(n_hh):
    c = rng.integers(0, n_city)
    rural = int(rng.random() < 0.46)
    edu = rng.integers(1, 6)             # 1-5受教育层次
    highedu = int(edu >= 4)
    male = int(rng.random() < 0.5)
    age0 = rng.integers(22, 60)
    hhsize = rng.integers(1, 7)
    health = rng.integers(1, 6)
    inc_base = 10.2 + 0.18*edu - 0.25*rural + rng.normal(0, 0.5)
    lowb = int(inc_base < 10.2)
    hh_ability = rng.normal(0, 0.03)     # 家庭固定不可观测能力
    for y in waves:
        age = age0 + (y - 2012)
        post = int(treat_year[c] != 9999 and y >= treat_year[c])
        # 动态效应：政策实施当期0.6倍、其后逐步显现
        k = int(round((y - treat_year[c]) / 2)) if treat_year[c] != 9999 else -99
        dyn = {0: 0.6, 1: 1.0, 2: 1.25}.get(k, 0.0) if post else 0.0
        loginc = inc_base + 0.02*(y-2012) + rng.normal(0, 0.15)
        # 异质性：农村、低教育、低收入群体处理效应更强
        het = 1.0 + 0.6*rural + 0.5*(1-highedu) + 0.4*lowb
        p = (0.145 + hh_ability + city_fe[c]*0.4 + (year_fe[y]-0.015)*0.5
             + 0.010*(edu-3) - 0.020*rural - 0.0015*(age-42)
             + 0.020*(loginc-10.5) + 0.004*(hhsize-3) + 0.006*male
             + BETA_P*het*dyn + rng.normal(0, 0.02))
        p = float(np.clip(p, 0.01, 0.75))
        entrep = int(rng.random() < p)
        # 机制变量(受政策影响)：信息获取、数字金融可得、社会网络(后续标准化)
        info = (0.30 + 0.34*post*(1+0.3*rural) + 0.22*edu + city_fe[c]*3
                + rng.normal(0, 0.95))
        fin = (0.20 + 0.30*post*(1+0.4*lowb) + 0.18*edu
               + rng.normal(0, 0.95))
        net = (0.25 + 0.20*post + 0.12*edu + rng.normal(0, 0.95))
        rows.append(dict(hh=i, city=c, year=y, post=post, entrep=entrep,
                         rural=rural, edu=edu, highedu=highedu, male=male,
                         age=age, hhsize=hhsize, health=health, loginc=loginc,
                         east=east[c], treatever=int(treat_year[c]!=9999),
                         treatyr=treat_year[c], lowinc=int(inc_base<10.2),
                         info=info, fin=fin, net=net,
                         rel=(y-treat_year[c]) if treat_year[c]!=9999 else np.nan))
df = pd.DataFrame(rows)
df["age2"] = df["age"]**2/100
# 机制变量标准化为z分数(均值0,标准差1)，使系数可解释为"标准差变动"
for v in ["info","fin","net"]:
    df[v] = (df[v]-df[v].mean())/df[v].std()
print("样本量:", len(df), "| 家庭数:", df.hh.nunique(), "| 城市数:", df.city.nunique())
print("创业率均值: %.3f" % df.entrep.mean(), "| 处理组占比: %.2f" % df.treatever.mean())

out = {}
out["N"] = int(len(df)); out["n_hh"]=int(df.hh.nunique()); out["n_city"]=int(df.city.nunique())
out["entrep_mean"]=round(float(df.entrep.mean()),4)

def star(p):
    return "***" if p<0.01 else "**" if p<0.05 else "*" if p<0.1 else ""

# ---------- 3. 基准DID ----------
def did(formula, data, cluster="city"):
    m = smf.ols(formula, data=data).fit(cov_type="cluster", cov_kwds={"groups": data[cluster]})
    return m

ctrl = "edu + rural + male + age + age2 + hhsize + health + loginc"
m1 = did("entrep ~ post", df)
m2 = did("entrep ~ post + C(city) + C(year)", df)
m3 = did(f"entrep ~ post + {ctrl} + C(city) + C(year)", df)
base = {}
for name, m in [("c1",m1),("c2",m2),("c3",m3)]:
    b=m.params["post"]; se=m.bse["post"]; p=m.pvalues["post"]
    base[name]=dict(b=round(b,4), se=round(se,4), star=star(p), N=int(m.nobs), r2=round(m.rsquared,3))
    print(f"基准{name}: post={b:.4f}{star(p)} ({se:.4f}) N={int(m.nobs)} R2={m.rsquared:.3f}")
out["baseline"]=base

# ---------- 4. 事件研究 ----------
dd = df[df.treatever==1].copy()
# 相对时间：-2,-1(基准),0,1,2 (以调查波次为单位)；限制在[-2,2]
dd["k"] = ((dd.year - dd.treatyr)/2).round().astype(int)
dd["k"] = dd["k"].clip(-2, 2)
# 加入控制城市作为对照(k设为参照)；用交互哑变量，省略k=-1
evrows=[]
df2 = df.copy()
df2["k"] = np.where(df2.treatever==1, ((df2.year-df2.treatyr)/2).round().clip(-2,2), -99).astype(int)
terms=[]
for k in [-2,0,1,2]:
    df2[f"D{k}"]=((df2.k==k)).astype(int)
    terms.append(f"D{k}" if k>=0 else f"Dm{abs(k)}")
    if k<0: df2[f"Dm{abs(k)}"]=df2[f"D{k}"]
form = "entrep ~ " + " + ".join([c for c in ["Dm2","D0","D1","D2"]]) + f" + {ctrl} + C(city) + C(year)"
me = did(form, df2)
ev={}
labelmap={"Dm2":-2,"D0":0,"D1":1,"D2":2}
for t,k in labelmap.items():
    ev[str(k)]=dict(b=round(me.params[t],4), se=round(me.bse[t],4))
ev["-1"]=dict(b=0.0, se=0.0)  # 基准期
out["event"]=ev
print("事件研究:", ev)

# ---------- 5. 机制检验 ----------
mech={}
for var in ["info","fin","net"]:
    m = did(f"{var} ~ post + {ctrl} + C(city) + C(year)", df)
    b=m.params["post"]; se=m.bse["post"]; p=m.pvalues["post"]
    mech[var]=dict(b=round(b,4), se=round(se,4), star=star(p), N=int(m.nobs), r2=round(m.rsquared,3))
    print(f"机制{var}: {b:.4f}{star(p)} ({se:.4f})")
out["mech"]=mech

# ---------- 6. 异质性(交互项) ----------
het={}
for hv,lab in [("rural","城乡"),("lowinc","收入"),("highedu","教育"),("east","区域")]:
    m = did(f"entrep ~ post*{hv} + {ctrl} + C(city) + C(year)", df)
    key=f"post:{hv}"
    b=m.params["post"]; ib=m.params[key]; ise=m.bse[key]; ip=m.pvalues[key]
    het[hv]=dict(main=round(b,4), main_se=round(m.bse["post"],4), inter=round(ib,4),
                 inter_se=round(ise,4), star=star(ip), N=int(m.nobs))
    print(f"异质性{lab}: 主效应{b:.4f} 交互{ib:.4f}{star(ip)} ({ise:.4f})")
out["het"]=het

# ---------- 7. 稳健性：安慰剂(随机分配处理时点，FWL快速实现) ----------
def twoway_demean(v, g1, g2, it=4):
    v = np.asarray(v, float).copy()
    for _ in range(it):
        v = v - pd.Series(v).groupby(g1).transform("mean").values
        v = v - pd.Series(v).groupby(g2).transform("mean").values
    return v
gcity = df.city.values; gyear = df.year.values
# 预先双向去均值：结果与控制变量
y_dm = twoway_demean(df.entrep.values, gcity, gyear)
Xc = np.column_stack([twoway_demean(df[v].values, gcity, gyear)
                      for v in ["edu","rural","male","age","age2","hhsize","health","loginc"]])
Pinv = np.linalg.pinv(Xc.T @ Xc) @ Xc.T          # (k×n) 投影算子
y_rr = y_dm - Xc @ (Pinv @ y_dm)                  # 结果对控制变量残差(一次)
plac=[]
for s in range(500):
    r = np.random.default_rng(s)
    fake = {c: r.choice([2014,2016,9999]) for c in range(n_city)}
    tt = df.city.map(fake).values
    fp = ((tt!=9999)&(df.year.values>=tt)).astype(float)
    t_dm = twoway_demean(fp, gcity, gyear)
    t_rr = t_dm - Xc @ (Pinv @ t_dm)
    denom = float(t_rr @ t_rr)
    plac.append(float(t_rr @ y_rr / denom) if denom>1e-8 else 0.0)
plac=np.array(plac)
out["placebo"]=dict(mean=round(float(plac.mean()),4), sd=round(float(plac.std()),4),
                    true=base["c3"]["b"],
                    frac_ge_true=round(float((np.abs(plac)>=abs(base["c3"]["b"])).mean()),4))
print("安慰剂: 均值%.4f sd%.4f 超过真值比例%.3f" % (plac.mean(), plac.std(), out["placebo"]["frac_ge_true"]))

# ---------- 8. PSM-DID 粗略(倾向得分加权后再DID) ----------
from statsmodels.api import Logit, add_constant
Xp = df.groupby("hh").first()[["edu","rural","male","hhsize","health"]]
yp = df.groupby("hh").first()["treatever"]
ps = Logit(yp, add_constant(Xp)).fit(disp=0).predict(add_constant(Xp))
wmap = {}
for hh,p in ps.items():
    t=yp[hh]; wmap[hh]= (1/p) if t==1 else (1/(1-p))
df["w"]=df.hh.map(wmap).clip(upper=10)
mw = smf.wls(f"entrep ~ post + {ctrl} + C(city) + C(year)", df, weights=df.w).fit(
    cov_type="cluster", cov_kwds={"groups": df.city})
out["psm"]=dict(b=round(mw.params["post"],4), se=round(mw.bse["post"],4), star=star(mw.pvalues["post"]), N=int(mw.nobs))
print("PSM-IPW-DID:", out["psm"])

# ---------- 描述性统计 ----------
descmap=[("entrep","家庭创业"),("post","宽带中国政策冲击"),("edu","受教育水平"),
         ("rural","农村"),("male","性别"),("age","年龄"),("hhsize","家庭规模"),
         ("health","健康状况"),("loginc","家庭人均收入对数")]
desc={}
for v,lab in descmap:
    s=df[v]
    desc[v]=dict(lab=lab, mean=round(float(s.mean()),3), sd=round(float(s.std()),3),
                 min=round(float(s.min()),3), max=round(float(s.max()),3))
out["desc"]=desc

json.dump(out, open("sim1_out.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)

# ---------- 图1：事件研究 ----------
ks=[-2,-1,0,1,2]; bs=[ev[str(k)]["b"] for k in ks]; ses=[ev[str(k)]["se"] for k in ks]
fig,ax=plt.subplots(figsize=(6.2,3.8))
ax.axhline(0,color="0.6",lw=0.8); ax.axvline(-0.5 if False else 0,color="0.85",lw=0.6,ls=":")
ci=[1.96*s for s in ses]
ax.errorbar(ks,bs,yerr=ci,fmt="o-",color="#1f3b73",ecolor="#1f3b73",capsize=3,ms=5,lw=1.3)
ax.set_xticks(ks)
ax.set_xlabel("相对政策实施的时期（调查波次）",fontproperties=zh,fontsize=11)
ax.set_ylabel("对家庭创业的估计效应",fontproperties=zh,fontsize=11)
for lab in ax.get_xticklabels()+ax.get_yticklabels(): lab.set_fontproperties(zh)
ax.grid(axis="y",ls=":",alpha=0.4)
fig.tight_layout(); fig.savefig("p1_fig1_event.png",dpi=200,bbox_inches="tight"); plt.close()

# ---------- 图2：处理组vs控制组创业率趋势 ----------
g=df.groupby(["year","treatever"]).entrep.mean().unstack()
fig,ax=plt.subplots(figsize=(6.2,3.8))
ax.plot(g.index,g[1],"o-",color="#b5122e",label="试点城市（处理组）",lw=1.5,ms=5)
ax.plot(g.index,g[0],"s--",color="#1f3b73",label="非试点城市（控制组）",lw=1.5,ms=5)
ax.set_xlabel("年份",fontproperties=zh,fontsize=11)
ax.set_ylabel("家庭创业率",fontproperties=zh,fontsize=11)
ax.legend(prop=zh,fontsize=10,frameon=False)
for lab in ax.get_xticklabels()+ax.get_yticklabels(): lab.set_fontproperties(zh)
ax.grid(axis="y",ls=":",alpha=0.4); ax.set_xticks(waves)
fig.tight_layout(); fig.savefig("p1_fig2_trend.png",dpi=200,bbox_inches="tight"); plt.close()
print("图1、图2已保存")
print(json.dumps(out, ensure_ascii=False, indent=1))
