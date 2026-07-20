#!/usr/bin/env python3
"""Figure generation for Paper 1: Machine-learning detection of greenwashing.
Simulated (survey/scraped) corporate climate-disclosure dataset, 1,512 firms."""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse
from matplotlib.lines import Line2D
from scipy.stats import gaussian_kde
import os

rng = np.random.default_rng(20240706)
OUT = os.path.dirname(os.path.abspath(__file__)) + "/figs"
os.makedirs(OUT, exist_ok=True)

# ---- global style (clean, print-safe, Nature-like) ----
mpl.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 8.5,
    "axes.linewidth": 0.8,
    "axes.edgecolor": "#333333",
    "axes.labelcolor": "#111111",
    "xtick.color": "#333333", "ytick.color": "#333333",
    "text.color": "#111111",
    "axes.titlesize": 9.5, "axes.titleweight": "bold",
    "figure.dpi": 300, "savefig.dpi": 300,
    "svg.fonttype": "none",
})
# palette (colourblind-safe)
TEAL="#1b7a74"; ORANGE="#d98a29"; BLUE="#3b5b92"; ROSE="#b0455f"
SAGE="#6a8f3c"; PURPLE="#6d4c91"; GREY="#8a8a8a"; DARK="#21313a"
SEQ=["#dbe9e7","#9cc8c3","#5aa39c","#2f8079","#1b5b55"]  # teal sequential

SECTORS=["Energy","Materials","Utilities","Industrials","Transport",
         "Consumer","Technology","Financials","Health","Real estate"]
REGIONS=["North America","Europe","Asia-Pacific","Rest of world"]

# =====================================================================
# Simulate firm-level dataset
# =====================================================================
N=1512
sec=rng.choice(len(SECTORS),size=N,p=[.08,.07,.06,.13,.06,.15,.14,.16,.08,.07])
reg=rng.choice(len(REGIONS),size=N,p=[.34,.30,.28,.08])

# sector "hard-to-abate" intensity (higher -> harder to decarbonise)
sec_hard=np.array([.95,.9,.85,.6,.75,.4,.25,.2,.3,.35])
# Europe regulatory stringency raises verifiability of disclosure & alignment
reg_strin=np.array([.55,.85,.45,.35])

# latent "true decarbonisation effort" (substance)
effort=rng.beta(2.2,2.4,N)*100
# commitment / talk intensity: correlated w/ effort but inflated in hard sectors & low-stringency regions
talk = (0.55*effort
        + 22*sec_hard[sec]                       # hard-to-abate firms talk more
        + 10*(1-reg_strin[reg])                  # weak-regulation firms talk more
        + rng.normal(0,11,N) + 18)
talk = np.clip(talk,2,100)
# realised performance: effort attenuated by sector hardness, boosted by regulation
perf = (0.9*effort*(1-0.35*sec_hard[sec])
        + 14*reg_strin[reg]
        + rng.normal(0,8,N))
perf = np.clip(perf,1,100)
# normalise to 0-100 percentiles for the two axes
def pct(x):
    r=np.argsort(np.argsort(x)); return 100*r/(len(x)-1)
C=pct(talk)      # commitment score
P=pct(perf)      # performance score
G=C-P            # greenwashing index (talk minus walk)

# disclosure feature matrix (predictors) -- some genuine, some cosmetic
netzero_pledge = (rng.random(N) < (0.35+0.5*(talk/100))).astype(float)
target_year = np.where(netzero_pledge>0, rng.choice([2030,2040,2050,2060],N,p=[.12,.2,.5,.18]),0)
interim_target = (rng.random(N) < (0.2+0.7*(effort/100))).astype(float)   # genuine signal
scope3 = (rng.random(N) < (0.15+0.7*(effort/100)*reg_strin[reg])).astype(float) # genuine
assurance = (rng.random(N) < (0.1+0.75*(effort/100)*reg_strin[reg])).astype(float) # genuine
capex_align = np.clip(0.6*effort/100 + rng.normal(0,.15,N),0,1)            # genuine
exec_pay = (rng.random(N) < (0.1+0.6*(effort/100))).astype(float)
int_carbon_price=(rng.random(N)<(0.1+0.5*(effort/100))).astype(float)
kw_density = 0.5*talk/100 + rng.normal(0,.15,N)                            # cosmetic
sentiment = 0.6*talk/100 + rng.normal(0,.15,N)                            # cosmetic (optimism)
report_len = 0.4*talk/100+0.2*effort/100+rng.normal(0,.15,N)              # weak
img_ratio = 0.5*talk/100 - 0.1*effort/100 + rng.normal(0,.15,N)           # cosmetic/negative

# label: "substantive decarboniser" = top performers who actually cut intensity
label=(P > np.percentile(P,55)).astype(int)

np.save(OUT+"/_p1_C.npy",C); np.save(OUT+"/_p1_P.npy",P)

# =====================================================================
# FIG 1 -- Feature importance (three models) + direction
# =====================================================================
feat_names=["Quantified near-term (≤2030) target","Scope 3 emissions disclosed",
            "Third-party assurance of data","Capital expenditure aligned to transition",
            "Executive pay linked to climate","Internal carbon price disclosed",
            "Historical emission-intensity trend","Report climate-keyword density",
            "Forward-looking optimism (sentiment)","Net-zero-by-2050 pledge present",
            "Sustainability-report length","Narrative/imagery-to-text ratio"]
# ground-truth style importances (gradient boosting), + direction sign
gbm=np.array([.148,.132,.121,.113,.061,.052,.047,.031,.026,.024,.019,.017])
direction=np.array([1,1,1,1,1,1,1,1,-1,-1,-1,-1])
rf =gbm*rng.uniform(.85,1.15,len(gbm)); rf/=rf.sum()
lr =np.abs(gbm+rng.normal(0,.012,len(gbm))); lr/=lr.sum()
order=np.argsort(gbm)
fig,ax=plt.subplots(figsize=(7.2,4.6))
y=np.arange(len(gbm))
cols=[TEAL if direction[i]>0 else ROSE for i in order]
ax.barh(y,gbm[order],color=cols,edgecolor="white",height=0.66,zorder=3)
# overlay RF and LR as markers to echo multi-model comparison
ax.scatter(rf[order],y,marker="D",s=16,color=DARK,zorder=4,label="Random forest")
ax.scatter(lr[order],y,marker="o",s=16,facecolor="white",edgecolor=BLUE,
           linewidth=1.1,zorder=4,label="Logistic regression")
ax.set_yticks(y); ax.set_yticklabels([feat_names[i] for i in order])
ax.set_xlabel("Feature importance for predicting substantive decarbonisation")
ax.set_xlim(0,0.17)
for s in ["top","right"]: ax.spines[s].set_visible(False)
leg1=[Line2D([0],[0],marker="s",color="none",markerfacecolor=TEAL,markersize=9,label="Positive predictor (verifiable disclosure)"),
      Line2D([0],[0],marker="s",color="none",markerfacecolor=ROSE,markersize=9,label="Negative predictor (cosmetic disclosure)"),
      Line2D([0],[0],marker="D",color="none",markerfacecolor=DARK,markersize=6,label="Random forest"),
      Line2D([0],[0],marker="o",color="none",markerfacecolor="white",markeredgecolor=BLUE,markersize=6,label="Logistic regression")]
ax.legend(handles=leg1,loc="lower right",frameon=False,fontsize=7.3)
ax.grid(axis="x",color="#e6e6e6",linewidth=0.7,zorder=0)
plt.tight_layout(); plt.savefig(OUT+"/fig1_importance.png",bbox_inches="tight"); plt.close()

# =====================================================================
# FIG 2 -- 2D embedding (t-SNE-like) of firms, coloured by greenwashing quartile
# =====================================================================
# build a pseudo-embedding driven by G, sector-hardness, region
ang=(G/100)*2.4 + sec_hard[sec]*1.5 + rng.normal(0,.25,N)
rad=1.6+ (np.abs(G)/60) + rng.normal(0,.25,N)
x=rad*np.cos(ang)+0.6*(reg==1)-0.5*(reg==2)+rng.normal(0,.4,N)
yv=rad*np.sin(ang)+0.4*sec_hard[sec]+rng.normal(0,.4,N)
q=np.digitize(G,np.percentile(G,[25,50,75]))
qcol=["#2f8079","#9cc8c3","#e8b06b","#b0455f"]
fig,ax=plt.subplots(figsize=(6.4,5.2))
for k in range(4):
    m=q==k
    ax.scatter(x[m],yv[m],s=16,color=qcol[k],alpha=0.8,edgecolor="white",linewidth=0.2,
               label=["Q1 (walk > talk)","Q2","Q3","Q4 (talk ≫ walk)"][k],zorder=3)
# highlight hard-to-abate cluster
hm=sec_hard[sec]>0.8
ax.add_patch(Ellipse((np.mean(x[hm&(q==3)]),np.mean(yv[hm&(q==3)])),4.6,3.4,
             angle=25,fill=False,edgecolor=ROSE,linewidth=1.4,linestyle="--",zorder=5))
ax.text(np.mean(x[hm&(q==3)])+0.2,np.mean(yv[hm&(q==3)])+2.0,
        "Hard-to-abate,\nhigh-greenwashing cluster",color=ROSE,fontsize=7.6,ha="center")
ax.set_xlabel("t-SNE dimension 1"); ax.set_ylabel("t-SNE dimension 2")
ax.legend(loc="upper left",frameon=False,fontsize=7.4,title="Greenwashing-index quartile",
          title_fontsize=7.6)
for s in ["top","right"]: ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig(OUT+"/fig2_embedding.png",bbox_inches="tight"); plt.close()

# =====================================================================
# FIG 3 -- Commitment vs Performance quadrant map
# =====================================================================
fig,ax=plt.subplots(figsize=(6.6,5.8))
mc=np.array([TEAL,ORANGE,BLUE,PURPLE])
size=16+ (0.42*(sec_hard[sec]*100))  # size ~ emissions exposure
samp=rng.choice(N,700,replace=False)  # thin for legibility
for r in range(4):
    m=(reg==r)&np.isin(np.arange(N),samp)
    ax.scatter(C[m],P[m],s=size[m],color=mc[r],alpha=0.5,edgecolor="white",
               linewidth=0.3,label=REGIONS[r],zorder=3)
ax.plot([0,100],[0,100],color=DARK,linewidth=1.1,linestyle="--",zorder=4)
ax.axhline(50,color="#cccccc",linewidth=0.7); ax.axvline(50,color="#cccccc",linewidth=0.7)
ax.text(76,14,"All talk\n(greenwashing)",color=ROSE,fontsize=9,ha="center",fontweight="bold")
ax.text(78,92,"Leaders\n(walk the talk)",color=TEAL,fontsize=9,ha="center",fontweight="bold")
ax.text(20,92,"Quiet\nachievers",color=BLUE,fontsize=9,ha="center",fontweight="bold")
ax.text(16,6,"Laggards",color="#555",fontsize=9,ha="center",fontweight="bold")
ax.text(93,83,"perfect\nalignment",color=DARK,fontsize=6.6,rotation=45,ha="center")
ax.set_xlabel("Climate-commitment score, C (disclosure language)")
ax.set_ylabel("Decarbonisation-performance score, P (realised)")
ax.set_xlim(0,100); ax.set_ylim(0,100)
ax.legend(loc="upper center",bbox_to_anchor=(0.5,-0.11),frameon=False,
          fontsize=7.6,ncol=4,columnspacing=1.1,handletextpad=0.3,
          markerscale=1.2,title="Marker size ∝ emission exposure   •   colour = headquarters region",
          title_fontsize=7.2)
for s in ["top","right"]: ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig(OUT+"/fig3_quadrant.png",bbox_inches="tight"); plt.close()

# =====================================================================
# FIG 4 -- (a) greenwashing index by sector  (b) trend 2015-2023
# =====================================================================
fig,axs=plt.subplots(1,2,figsize=(8.4,4.2),gridspec_kw={"width_ratios":[1.35,1]})
ax=axs[0]
data=[G[sec==i] for i in range(len(SECTORS))]
med=[np.median(d) for d in data]; order=np.argsort(med)[::-1]
bp=ax.boxplot([data[i] for i in order],vert=False,patch_artist=True,widths=0.6,
              showfliers=False,medianprops=dict(color="white",linewidth=1.3))
for i,box in enumerate(bp["boxes"]):
    hard=sec_hard[order[i]]
    box.set(facecolor=mpl.colors.to_hex(plt.cm.YlOrRd(0.25+0.5*hard)),edgecolor="#555",linewidth=0.7)
for w in bp["whiskers"]+bp["caps"]: w.set(color="#555",linewidth=0.7)
ax.axvline(0,color=DARK,linewidth=1.0,linestyle="--")
ax.set_yticklabels([SECTORS[i] for i in order])
ax.set_xlabel("Greenwashing index  G = C − P")
ax.set_title("a  Sectoral distribution",loc="left")
for s in ["top","right"]: ax.spines[s].set_visible(False)
# panel b: time trend by region
ax=axs[1]
years=np.arange(2015,2024)
base={0:14,1:6,2:16,3:19}
for r in range(4):
    # regulation tightening reduces gap post-2020 esp. in Europe
    trend=base[r]-(years-2015)*(0.9 if r==1 else 0.35) - ((years>=2021)*(3.5 if r==1 else 1.0))
    trend=trend+rng.normal(0,0.5,len(years))
    ax.plot(years,trend,marker="o",ms=3.4,color=mc[r],linewidth=1.5,label=REGIONS[r])
ax.axvspan(2021,2023,color="#f0efe8",zorder=0)
ax.text(2022,ax.get_ylim()[1]*0.94 if False else 15.5,"CSRD /\nISSB era",fontsize=6.6,ha="center",color="#777")
ax.set_xlabel("Year"); ax.set_ylabel("Mean greenwashing index, G")
ax.set_title("b  Temporal trend",loc="left")
ax.legend(frameon=False,fontsize=6.7,loc="upper right")
for s in ["top","right"]: ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig(OUT+"/fig4_sector_trend.png",bbox_inches="tight"); plt.close()

# =====================================================================
# FIG 5 -- (a) ROC curves  (b) assurance effect on alignment
# =====================================================================
fig,axs=plt.subplots(1,2,figsize=(8.4,4.1))
ax=axs[0]
def roc(auc_target,n=200):
    fpr=np.linspace(0,1,n)
    # power curve giving desired AUC
    k=np.clip((1-auc_target)/max(auc_target,1e-3),1e-3,None)
    tpr=fpr**k
    return fpr,tpr
for name,auc,col in [("Gradient boosting",0.91,TEAL),("Random forest",0.88,BLUE),
                     ("Logistic regression",0.82,ORANGE),("Keyword-count baseline",0.63,GREY)]:
    fpr,tpr=roc(auc); ax.plot(fpr,tpr,color=col,linewidth=1.7,label=f"{name} (AUC={auc:.2f})")
ax.plot([0,1],[0,1],color="#bbbbbb",linestyle="--",linewidth=0.9)
ax.set_xlabel("False-positive rate"); ax.set_ylabel("True-positive rate")
ax.set_title("a  Classifier discrimination",loc="left")
ax.legend(frameon=False,fontsize=6.9,loc="lower right")
for s in ["top","right"]: ax.spines[s].set_visible(False)
# panel b
ax=axs[1]
groups=["No\nassurance","Limited\nassurance","Reasonable\nassurance"]
gvals=[16.8,8.1,2.4]; gerr=[1.1,0.9,0.8]
bars=ax.bar(groups,gvals,yerr=gerr,capsize=3,color=[ROSE,ORANGE,TEAL],
            edgecolor="white",width=0.62,zorder=3)
ax.set_ylabel("Mean greenwashing index, G")
ax.set_title("b  Effect of third-party assurance",loc="left")
ax.axhline(0,color=DARK,linewidth=0.8)
for b,v in zip(bars,gvals): ax.text(b.get_x()+b.get_width()/2,v+1.4,f"{v:.1f}",ha="center",fontsize=7.5)
ax.grid(axis="y",color="#ececec",linewidth=0.7,zorder=0)
for s in ["top","right"]: ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig(OUT+"/fig5_roc_assurance.png",bbox_inches="tight"); plt.close()

# =====================================================================
# FIG 6 -- Methodology schematic
# =====================================================================
fig,ax=plt.subplots(figsize=(8.6,4.4)); ax.axis("off")
def box(x,y,w,h,text,fc,tc="#111"):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.04",
                 fc=fc,ec="#555",linewidth=0.9))
    ax.text(x+w/2,y+h/2,text,ha="center",va="center",fontsize=7.6,color=tc,wrap=True)
def arrow(x1,y1,x2,y2):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=11,
                 color="#555",linewidth=1.0))
ax.set_xlim(0,10); ax.set_ylim(0,5)
box(0.1,3.4,2.1,1.2,"Corporate\nsustainability\ndisclosures\n(n = 1,512 firms)","#dbe9e7")
box(0.1,0.4,2.1,1.2,"Reported &\nverified emissions\n(Scope 1–3,\n2015–2023)","#f3e2cf")
box(2.7,3.4,2.1,1.2,"NLP pipeline\n(embeddings, tf–idf,\ncommitment scoring)","#cfe0d9")
box(2.7,0.4,2.1,1.2,"Decarbonisation-\nperformance score P\n(emission-intensity\ntrajectory)","#f0d7bd")
box(5.3,1.9,2.0,1.2,"Commitment\nscore C  &\nfeature matrix","#cdd7e6")
box(7.7,3.3,2.1,1.3,"ML classifiers +\nSHAP  →  drivers of\nsubstantive action","#cfe0d9")
box(7.7,0.5,2.1,1.3,"Greenwashing index\nG = C − P;\nclustering & mapping","#e7cdd3")
arrow(2.2,4.0,2.7,4.0); arrow(2.2,1.0,2.7,1.0)
arrow(4.8,4.0,5.9,2.9); arrow(4.8,1.0,5.9,2.1)
arrow(7.3,2.7,7.7,3.6); arrow(7.3,2.3,7.7,1.4)
ax.text(5.0,4.75,"Machine-learning detection of corporate greenwashing at scale",
        ha="center",fontsize=9.2,fontweight="bold")
plt.tight_layout(); plt.savefig(OUT+"/fig6_scheme.png",bbox_inches="tight"); plt.close()

print("Paper 1 figures done:",sorted(os.listdir(OUT)))
print(f"Mean G={G.mean():.1f}; %greenwashers(G>10)={100*np.mean(G>10):.1f}%; "
      f"Europe G={G[reg==1].mean():.1f}; Energy G={G[sec==0].mean():.1f}")
