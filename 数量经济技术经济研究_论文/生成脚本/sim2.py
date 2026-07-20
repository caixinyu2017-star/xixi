# -*- coding: utf-8 -*-
"""论文二：工业机器人应用与劳动收入份额——制造业上市公司。
生成公司-年份面板与行业机器人渗透度(Bartik式)，内置真实负向效应，
估计双向固定效应、2SLS-IV、机制与异质性，输出数值(json)与图1(趋势)、图2(binscatter)。"""
import numpy as np, pandas as pd, json
import statsmodels.formula.api as smf
from statsmodels.sandbox.regression.gmm import IV2SLS
import statsmodels.api as sm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

rng = np.random.default_rng(20260705)
FP = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
zh = fm.FontProperties(fname=FP)
plt.rcParams["axes.unicode_minus"] = False
def star(p): return "***" if p<0.01 else "**" if p<0.05 else "*" if p<0.1 else ""

# ---------- 1. 行业机器人渗透度(Bartik) ----------
years = list(range(2011, 2020))
n_ind = 21
# 各行业国外(美欧日)机器人渗透度增长路径(工具变量来源)，行业异质
ind_growth = rng.uniform(0.4, 2.2, n_ind)
ind_base_f = rng.uniform(0.2, 1.0, n_ind)
foreign = {}   # (j,y) 国外行业渗透度
china = {}     # (j,y) 国内行业渗透度
for j in range(n_ind):
    for t,y in enumerate(years):
        f = ind_base_f[j] + ind_growth[j]*(t/8) + rng.normal(0,0.05)
        foreign[(j,y)] = max(f,0.01)
        # 国内渗透度=f(国外, 行业趋势) + 国内特有冲击(与LS无关)
        china[(j,y)] = 0.15 + 0.85*foreign[(j,y)] + 0.25*(t/8) + rng.normal(0,0.12)
        china[(j,y)] = max(china[(j,y)],0.01)

# ---------- 2. 公司面板 ----------
n_firm = 1600
TRUE_BETA = -0.035   # 机器人渗透度对劳动收入份额的真实效应(每单位)
firms=[]
for i in range(n_firm):
    j = rng.integers(0, n_ind)
    soe = int(rng.random()<0.32)
    labint = rng.normal(0,1)            # 劳动密集度(标准化)
    size0 = rng.normal(21.5,1.1)        # ln资产
    firm_fe = rng.normal(0,0.05)
    highskill = np.clip(0.25+0.15*rng.normal()+0.05*labint*-1,0.02,0.9)
    firms.append(dict(firm=i,ind=j,soe=soe,labint=labint,size0=size0,
                      firm_fe=firm_fe,highskill=highskill,
                      east=int(rng.random()<0.55)))
year_fe = {y:v for y,v in zip(years, np.linspace(0.02,-0.03,len(years))+rng.normal(0,0.005,len(years)))}

rows=[]
for f in firms:
    i,j=f["firm"],f["ind"]
    for t,y in enumerate(years):
        rp = china[(j,y)]           # 机器人渗透度(核心解释变量)
        rp_f = foreign[(j,y)]       # 工具变量
        size = f["size0"] + 0.03*t + rng.normal(0,0.08)
        age = 6 + t + rng.integers(0,15)
        cap = 0.35 + 0.05*rp + 0.02*t + f["labint"]*-0.05 + rng.normal(0,0.05)  # 资本密集度(机制)
        tfp = 1.0 + 0.08*rp + 0.03*t + rng.normal(0,0.1)                        # 生产率(机制)
        markup = 1.15 + 0.04*rp + rng.normal(0,0.06)                            # 成本加成(机制)
        skillshare = f["highskill"] + 0.03*rp + rng.normal(0,0.02)              # 技能结构(机制)
        # 异质性：劳动密集、非国有、低技能行业负向效应更强
        het = 1.0 + 0.5*max(f["labint"],0) + 0.4*(1-f["soe"]) + 0.4*(f["highskill"]<0.3)
        ls = (0.38 + f["firm_fe"] + year_fe[y]
              + TRUE_BETA*het*rp
              - 0.015*(size-21.5) + 0.02*f["labint"] - 0.03*f["soe"]
              + 0.01*(age-15)/10 + rng.normal(0,0.045))
        ls = float(np.clip(ls, 0.05, 0.85))
        rows.append(dict(firm=i,ind=j,year=y,ls=ls,rp=rp,rp_f=rp_f,size=size,age=age,
                         cap=cap,tfp=tfp,markup=markup,skillshare=skillshare,
                         soe=f["soe"],labint=f["labint"],east=f["east"],
                         labint_hi=int(f["labint"]>0),highskill=f["highskill"],
                         hs_lo=int(f["highskill"]<0.3), size_g=int(f["size0"]>21.5)))
df=pd.DataFrame(rows)
df["lev"]=np.clip(0.45+0.03*df.labint+rng.normal(0,0.1,len(df)),0.05,0.95)
print("样本量:",len(df),"公司数:",df.firm.nunique(),"行业数:",df.ind.nunique(),"年份:",df.year.min(),"-",df.year.max())
print("劳动收入份额均值 %.3f  机器人渗透度均值 %.3f" % (df.ls.mean(), df.rp.mean()))

out={}
out["N"]=int(len(df)); out["n_firm"]=int(df.firm.nunique()); out["n_ind"]=int(df.ind.nunique())
out["ls_mean"]=round(float(df.ls.mean()),4); out["rp_mean"]=round(float(df.rp.mean()),4)
out["ls_sd"]=round(float(df.ls.std()),4); out["rp_sd"]=round(float(df.rp.std()),4)

def feols(formula, data, cluster="ind"):
    return smf.ols(formula, data=data).fit(cov_type="cluster", cov_kwds={"groups":data[cluster]})

ctrl="size + age + lev + labint + soe"
# ---------- 3. 基准 ----------
base={}
m1=feols("ls ~ rp", df)
m2=feols("ls ~ rp + C(year)", df)
m3=feols("ls ~ rp + C(firm) + C(year)", df)
m4=feols(f"ls ~ rp + {ctrl} + C(firm) + C(year)", df)
for nm,m in [("c1",m1),("c2",m2),("c3",m3),("c4",m4)]:
    b=m.params["rp"];se=m.bse["rp"];p=m.pvalues["rp"]
    base[nm]=dict(b=round(b,4),se=round(se,4),star=star(p),N=int(m.nobs),r2=round(m.rsquared,3))
    print(f"基准{nm}: rp={b:.4f}{star(p)} ({se:.4f}) N={int(m.nobs)}")
out["baseline"]=base

# ---------- 4. 2SLS IV ----------
# 用行业固定效应与年份固定效应吸收，然后对rp用rp_f做工具变量
d=df.copy()
# demean by firm and year (双向去均值) for IV
import patsy
Yfe = pd.get_dummies(d.firm,prefix="f",drop_first=True)
Tfe = pd.get_dummies(d.year,prefix="y",drop_first=True)
Xc = d[["size","age","lev","labint","soe"]].astype(float)
exog = pd.concat([Xc, Tfe.astype(float)], axis=1)
# 为控制公司固定效应，采用组内去均值(对rp,rp_f,ls,控制变量)
def within(s, g): return s - s.groupby(g).transform("mean")
gf=d.firm
dd=pd.DataFrame({
    "ls":within(d["ls"],gf),"rp":within(d["rp"],gf),"rpf":within(d["rp_f"],gf),
    "size":within(d["size"],gf),"age":within(d["age"].astype(float),gf),
    "lev":within(d["lev"],gf),"labint":within(d["labint"],gf),"soe":within(d["soe"].astype(float),gf),
})
for y in sorted(d.year.unique())[1:]:
    dd[f"y{y}"]=within((d.year==y).astype(float),gf)
exog_cols=["size","age","lev","labint","soe"]+[f"y{y}" for y in sorted(d.year.unique())[1:]]
# first stage
X1=sm.add_constant(dd[["rpf"]+exog_cols])
fs=sm.OLS(dd["rp"],X1).fit(cov_type="cluster",cov_kwds={"groups":d.ind})
Fstat=(fs.params["rpf"]/fs.bse["rpf"])**2
# 2SLS (手动实现，行业层面聚类稳健标准误)
def tsls_cluster(y, X, Z, clusters):
    y=np.asarray(y,float); X=np.asarray(X,float); Z=np.asarray(Z,float)
    ZtZ_inv=np.linalg.pinv(Z.T@Z); Pz=Z@ZtZ_inv@Z.T
    XtPzX_inv=np.linalg.pinv(X.T@Pz@X)
    beta=XtPzX_inv@(X.T@Pz@y); u=y-X@beta
    Xhat=Pz@X; XhtXh_inv=np.linalg.pinv(Xhat.T@Xhat)
    meat=np.zeros((X.shape[1],X.shape[1]))
    for g in np.unique(clusters):
        idx=np.asarray(clusters==g); xg=Xhat[idx]; ug=u[idx]
        s=xg.T@ug; meat+=np.outer(s,s)
    G=len(np.unique(clusters)); V=XhtXh_inv@meat@XhtXh_inv*(G/(G-1))
    return beta, np.sqrt(np.diag(V))
Xmat=sm.add_constant(pd.concat([dd["rp"],dd[exog_cols]],axis=1)).values
Zmat=sm.add_constant(pd.concat([dd["rpf"],dd[exog_cols]],axis=1)).values
beta,ses=tsls_cluster(dd["ls"], Xmat, Zmat, d.ind.values)
b=beta[1]; se=ses[1]   # 列0为常数项，列1为rp
from scipy import stats as st
p=2*(1-st.norm.cdf(abs(b/se)))
out["iv"]=dict(first_b=round(fs.params["rpf"],4), first_se=round(fs.bse["rpf"],4),
               first_star=star(fs.pvalues["rpf"]), F=round(float(Fstat),1),
               second_b=round(float(b),4), second_se=round(float(se),4), second_star=star(p))
print(f"IV第一阶段: rpf={fs.params['rpf']:.4f}{star(fs.pvalues['rpf'])} F={Fstat:.1f}")
print(f"IV第二阶段: rp={b:.4f}{star(p)} ({se:.4f})")

# ---------- 5. 机制 ----------
mech={}
for var in ["cap","tfp","skillshare","markup"]:
    m=feols(f"{var} ~ rp + {ctrl} + C(firm) + C(year)", df)
    b=m.params["rp"];se=m.bse["rp"];p=m.pvalues["rp"]
    mech[var]=dict(b=round(b,4),se=round(se,4),star=star(p),N=int(m.nobs),r2=round(m.rsquared,3))
    print(f"机制{var}: {b:.4f}{star(p)} ({se:.4f})")
out["mech"]=mech

# ---------- 6. 异质性 ----------
het={}
for hv in ["labint_hi","soe","hs_lo","size_g","east"]:
    cc = ctrl if hv not in ["soe"] else "size + age + lev + labint"
    m=feols(f"ls ~ rp*{hv} + {cc} + C(firm) + C(year)", df)
    key=f"rp:{hv}"
    het[hv]=dict(main=round(m.params['rp'],4), main_se=round(m.bse['rp'],4),
                 inter=round(m.params[key],4), inter_se=round(m.bse[key],4),
                 star=star(m.pvalues[key]), N=int(m.nobs))
    print(f"异质性{hv}: 主{m.params['rp']:.4f} 交互{m.params[key]:.4f}{star(m.pvalues[key])}")
out["het"]=het

# ---------- 7. 稳健性:安慰剂(打乱机器人渗透度，FWL快速实现) ----------
def twoway_demean(v, g1, g2, it=4):
    v = np.asarray(v, float).copy()
    for _ in range(it):
        v = v - pd.Series(v).groupby(g1).transform("mean").values
        v = v - pd.Series(v).groupby(g2).transform("mean").values
    return v
gfirm=df.firm.values; gyr=df.year.values
y_dm = twoway_demean(df.ls.values, gfirm, gyr)
Xc = np.column_stack([twoway_demean(df[v].values, gfirm, gyr)
                      for v in ["size","age","lev","labint","soe"]])
Pinv = np.linalg.pinv(Xc.T @ Xc) @ Xc.T
y_rr = y_dm - Xc @ (Pinv @ y_dm)
plac=[]
rpv=df["rp"].values
for s in range(500):
    r=np.random.default_rng(s)
    shuffled=rpv[r.permutation(len(rpv))]
    t_dm=twoway_demean(shuffled, gfirm, gyr)
    t_rr=t_dm - Xc @ (Pinv @ t_dm)
    denom=float(t_rr @ t_rr)
    plac.append(float(t_rr @ y_rr / denom) if denom>1e-8 else 0.0)
plac=np.array(plac)
out["placebo"]=dict(mean=round(float(plac.mean()),4),sd=round(float(plac.std()),4),
                    true=base["c4"]["b"],
                    frac_ge=round(float((np.abs(plac)>=abs(base["c4"]["b"])).mean()),4))
print("安慰剂: 均值%.4f sd%.4f 超真值比例%.3f"%(plac.mean(),plac.std(),out["placebo"]["frac_ge"]))

# ---------- 描述性统计 ----------
descmap=[("ls","劳动收入份额"),("rp","机器人渗透度"),("size","企业规模"),
         ("age","企业年龄"),("lev","资产负债率"),("labint","劳动密集度"),("soe","国有企业")]
desc={}
for v,lab in descmap:
    s=df[v]
    desc[v]=dict(lab=lab, mean=round(float(s.mean()),3), sd=round(float(s.std()),3),
                 min=round(float(s.min()),3), max=round(float(s.max()),3))
out["desc"]=desc

json.dump(out, open("sim2_out.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)

# ---------- 图1：劳动份额与机器人渗透度趋势(双轴) ----------
g=df.groupby("year").agg(ls=("ls","mean"), rp=("rp","mean"))
fig,ax=plt.subplots(figsize=(6.4,3.9))
l1=ax.plot(g.index,g.ls,"o-",color="#b5122e",lw=1.6,ms=5,label="劳动收入份额（左轴）")
ax.set_xlabel("年份",fontproperties=zh,fontsize=11)
ax.set_ylabel("劳动收入份额",fontproperties=zh,fontsize=11,color="#b5122e")
ax2=ax.twinx()
l2=ax2.plot(g.index,g.rp,"s--",color="#1f3b73",lw=1.6,ms=5,label="机器人渗透度（右轴）")
ax2.set_ylabel("工业机器人渗透度",fontproperties=zh,fontsize=11,color="#1f3b73")
for lab in ax.get_xticklabels()+ax.get_yticklabels()+ax2.get_yticklabels(): lab.set_fontproperties(zh)
ls_all=l1+l2
ax.legend(ls_all,[x.get_label() for x in ls_all],prop=zh,fontsize=9.5,frameon=False,loc="upper center")
ax.set_xticks(years); ax.grid(axis="y",ls=":",alpha=0.35)
fig.tight_layout(); fig.savefig("p2_fig1_trend.png",dpi=200,bbox_inches="tight"); plt.close()

# ---------- 图2：binscatter(双向去均值后) ----------
resid_ls=within(df.ls,df.firm); resid_ls=resid_ls-resid_ls.groupby(df.year).transform("mean")
resid_rp=within(df.rp,df.firm); resid_rp=resid_rp-resid_rp.groupby(df.year).transform("mean")
tmp=pd.DataFrame({"x":resid_rp+df.rp.mean(),"y":resid_ls+df.ls.mean()})
tmp["bin"]=pd.qcut(tmp.x,20,labels=False,duplicates="drop")
b=tmp.groupby("bin").agg(x=("x","mean"),y=("y","mean"))
coef=np.polyfit(tmp.x,tmp.y,1)
fig,ax=plt.subplots(figsize=(6.2,3.9))
ax.scatter(b.x,b.y,color="#1f3b73",s=28,zorder=3)
xx=np.linspace(b.x.min(),b.x.max(),50)
ax.plot(xx,np.polyval(coef,xx),color="#b5122e",lw=1.6)
ax.set_xlabel("工业机器人渗透度（去除固定效应后）",fontproperties=zh,fontsize=11)
ax.set_ylabel("劳动收入份额（去除固定效应后）",fontproperties=zh,fontsize=11)
for lab in ax.get_xticklabels()+ax.get_yticklabels(): lab.set_fontproperties(zh)
ax.grid(ls=":",alpha=0.35)
fig.tight_layout(); fig.savefig("p2_fig2_bin.png",dpi=200,bbox_inches="tight"); plt.close()
print("图1、图2已保存")
print(json.dumps(out,ensure_ascii=False,indent=1))
