#!/usr/bin/env python3
"""Figure generation for Paper 2: Generative AI, knowledge-worker productivity
and wage inequality. Simulated survey of 3,214 workers across 820 firms."""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D
import os

rng=np.random.default_rng(20240707)
OUT=os.path.dirname(os.path.abspath(__file__))+"/figs"
os.makedirs(OUT,exist_ok=True)

mpl.rcParams.update({
    "font.family":"DejaVu Sans","font.size":8.5,"axes.linewidth":0.8,
    "axes.edgecolor":"#333333","axes.labelcolor":"#111111",
    "xtick.color":"#333333","ytick.color":"#333333","text.color":"#111111",
    "axes.titlesize":9.5,"axes.titleweight":"bold","figure.dpi":300,"savefig.dpi":300})
TEAL="#1b7a74"; ORANGE="#d98a29"; BLUE="#3b5b92"; ROSE="#b0455f"
SAGE="#6a8f3c"; PURPLE="#6d4c91"; GREY="#8a8a8a"; DARK="#21313a"

OCC=["Customer support","Writing & content","Data analysis","Software development",
     "Paralegal & legal","Financial analysis","Accounting","Marketing",
     "Consulting","HR & administration","Design & creative","Management"]
# task exposure to generative AI (0-1)
EXP=np.array([.83,.79,.72,.71,.69,.66,.62,.63,.57,.55,.50,.44])
EXP_err=np.array([.03,.03,.035,.03,.04,.035,.04,.04,.045,.04,.05,.045])

# =====================================================================
# FIG 1 -- (a) exposure by occupation  (b) productivity gain by skill tercile
# =====================================================================
fig,axs=plt.subplots(1,2,figsize=(8.6,4.4),gridspec_kw={"width_ratios":[1.25,1]})
ax=axs[0]
order=np.argsort(EXP)
cols=[mpl.cm.viridis(0.15+0.7*(EXP[i]-EXP.min())/(EXP.max()-EXP.min())) for i in order]
ax.barh(np.arange(len(OCC)),EXP[order],xerr=EXP_err[order],color=cols,edgecolor="white",
        height=0.66,error_kw=dict(ecolor="#555",lw=0.7,capsize=2),zorder=3)
ax.set_yticks(np.arange(len(OCC))); ax.set_yticklabels([OCC[i] for i in order])
ax.set_xlabel("Task-exposure index to generative AI, $E_o$")
ax.set_xlim(0,1.0); ax.set_title("a  Occupational exposure",loc="left")
ax.grid(axis="x",color="#ececec",lw=0.7,zorder=0)
for s in ["top","right"]: ax.spines[s].set_visible(False)
# panel b -- productivity gain by baseline-skill tercile for three exposure levels
ax=axs[1]
terciles=["Bottom\ntercile","Middle\ntercile","Top\ntercile"]
gain_high=np.array([37,24,14]); gain_mid=np.array([26,17,10]); gain_low=np.array([13,8,5])
err=np.array([2.2,1.8,1.6])
x=np.arange(3); w=0.26
ax.bar(x-w,gain_high,w,yerr=err,color=TEAL,label="High-exposure tasks",capsize=2,edgecolor="white",zorder=3)
ax.bar(x,gain_mid,w,yerr=err*0.9,color=ORANGE,label="Medium-exposure",capsize=2,edgecolor="white",zorder=3)
ax.bar(x+w,gain_low,w,yerr=err*0.8,color=BLUE,label="Low-exposure",capsize=2,edgecolor="white",zorder=3)
ax.set_xticks(x); ax.set_xticklabels(terciles)
ax.set_ylabel("Task-completion productivity gain (%)")
ax.set_title("b  Gains by baseline-skill tercile",loc="left")
ax.legend(frameon=False,fontsize=7,loc="upper right")
ax.grid(axis="y",color="#ececec",lw=0.7,zorder=0)
ax.annotate("within-task\ncompression",xy=(0,37),xytext=(1.1,42),fontsize=7,color=ROSE,
            ha="center",arrowprops=dict(arrowstyle="->",color=ROSE,lw=0.9))
for s in ["top","right"]: ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig(OUT+"/fig1_exposure_gain.png",bbox_inches="tight"); plt.close()

# =====================================================================
# FIG 2 -- adoption diffusion: (a) by firm size  (b) by scenario
# =====================================================================
years=np.arange(2022,2041)
def logistic(t,L,k,t0): return L/(1+np.exp(-k*(t-t0)))
fig,axs=plt.subplots(1,2,figsize=(8.6,4.1))
ax=axs[0]
for name,col,(L,k,t0) in [("Large firms (>5,000)",BLUE,(0.95,0.55,2027.5)),
                          ("Mid-sized (250–5,000)",TEAL,(0.88,0.5,2029.5)),
                          ("Small firms (<250)",ORANGE,(0.72,0.45,2032.5))]:
    ax.plot(years,100*logistic(years,L,k,t0),color=col,lw=1.9,label=name)
ax.set_xlabel("Year"); ax.set_ylabel("Firms with deep GenAI integration (%)")
ax.set_title("a  Adoption by firm size (BAU)",loc="left")
ax.legend(frameon=False,fontsize=7,loc="upper left")
ax.set_ylim(0,100)
for s in ["top","right"]: ax.spines[s].set_visible(False)
ax=axs[1]
for name,col,(L,k,t0) in [("Policy-supported",TEAL,(0.93,0.5,2028.5)),
                          ("BAU + capability growth",BLUE,(0.85,0.45,2030.5)),
                          ("Business-as-usual",ORANGE,(0.7,0.4,2032.5)),
                          ("Frozen (2024 level)",GREY,(0.09,3,2024))]:
    y=100*logistic(years,L,k,t0)
    if "Frozen" in name: y=np.full_like(years,7.5,dtype=float)
    ax.plot(years,y,color=col,lw=1.9,label=name)
ax.set_xlabel("Year"); ax.set_ylabel("Economy-wide adoption (%)")
ax.set_title("b  Adoption by scenario",loc="left")
ax.legend(frameon=False,fontsize=7,loc="upper left")
ax.set_ylim(0,100)
for s in ["top","right"]: ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig(OUT+"/fig2_adoption.png",bbox_inches="tight"); plt.close()

# =====================================================================
# FIG 3 -- aggregate knowledge-work productivity projections by scenario
# =====================================================================
yrs=np.arange(2024,2041)
org=1.0+0.010*(yrs-2024)                       # organic ~1%/yr
def uplift(L,k,t0,pot):
    a=logistic(yrs,L,k,t0); return pot*a
scen={
 "Frozen":(GREY, org+uplift(0.09,3,2024,0.19)*0 + 0.0),   # only organic + frozen adoption
 "Business-as-usual":(ORANGE, org+uplift(0.70,0.40,2032.5,0.20)),
 "BAU + capability growth":(BLUE, org+uplift(0.85,0.45,2030.5,0.235)),
 "Policy-supported":(TEAL, org+uplift(0.93,0.50,2028.5,0.26)),
}
# frozen: organic + small frozen adoption uplift
scen["Frozen"]=(GREY, org+0.19*0.075)
fig,ax=plt.subplots(figsize=(6.9,4.7))
for name,(col,series) in scen.items():
    idx=100*series
    band=idx*(0.06 if name!="Frozen" else 0.03)
    ax.fill_between(yrs,idx-band,idx+band,color=col,alpha=0.15,zorder=2)
    ax.plot(yrs,idx,color=col,lw=2.0,label=name,zorder=3)
    ax.text(2040.2,idx[-1],f"+{idx[-1]-100:.0f}%",color=col,fontsize=7.6,va="center")
ax.set_xlabel("Year"); ax.set_ylabel("Knowledge-work labour-productivity index (2024 = 100)")
ax.set_xlim(2024,2041.8)
ax.legend(frameon=False,fontsize=7.6,loc="upper left")
for s in ["top","right"]: ax.spines[s].set_visible(False)
ax.grid(axis="y",color="#f0f0f0",lw=0.7,zorder=0)
plt.tight_layout(); plt.savefig(OUT+"/fig3_productivity.png",bbox_inches="tight"); plt.close()

# =====================================================================
# FIG 4 -- inequality: (a) within-occupation Gini  (b) between-firm dispersion
# =====================================================================
fig,axs=plt.subplots(1,2,figsize=(8.6,4.2))
ax=axs[0]
base_g=0.34
for name,col,(L,k,t0,strength) in [("Policy-supported",TEAL,(0.93,0.5,2028.5,0.085)),
                                   ("BAU + capability growth",BLUE,(0.85,0.45,2030.5,0.07)),
                                   ("Business-as-usual",ORANGE,(0.70,0.40,2032.5,0.055)),
                                   ("Frozen",GREY,(0.09,3,2024,0.0))]:
    a=logistic(yrs,L,k,t0) if name!="Frozen" else np.zeros_like(yrs,dtype=float)
    g=base_g-strength*a + rng.normal(0,0.0015,len(yrs))
    ax.plot(yrs,g,color=col,lw=1.9,label=name)
ax.set_xlabel("Year"); ax.set_ylabel("Within-occupation wage Gini")
ax.set_title("a  Within-occupation inequality",loc="left")
ax.legend(frameon=False,fontsize=6.8,loc="lower left")
for s in ["top","right"]: ax.spines[s].set_visible(False)
ax.annotate("compression",xy=(2038,0.27),xytext=(2032,0.24),fontsize=7,color=TEAL,
            arrowprops=dict(arrowstyle="->",color=TEAL,lw=0.9))
ax=axs[1]
base_d=0.22
for name,col,(L,k,t0,strength) in [("Business-as-usual",ORANGE,(0.70,0.40,2032.5,0.11)),
                                   ("BAU + capability growth",BLUE,(0.85,0.45,2030.5,0.10)),
                                   ("Policy-supported",TEAL,(0.93,0.5,2028.5,0.055)),
                                   ("Frozen",GREY,(0.09,3,2024,0.0))]:
    a=logistic(yrs,L,k,t0) if name!="Frozen" else np.zeros_like(yrs,dtype=float)
    d=base_d+strength*a + rng.normal(0,0.0015,len(yrs))
    ax.plot(yrs,d,color=col,lw=1.9,label=name)
ax.set_xlabel("Year"); ax.set_ylabel("Between-firm productivity dispersion (SD of log)")
ax.set_title("b  Between-firm inequality",loc="left")
ax.legend(frameon=False,fontsize=6.8,loc="upper left")
ax.annotate("divergence",xy=(2038,0.31),xytext=(2031,0.32),fontsize=7,color=ORANGE,
            arrowprops=dict(arrowstyle="->",color=ORANGE,lw=0.9))
for s in ["top","right"]: ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig(OUT+"/fig4_inequality.png",bbox_inches="tight"); plt.close()

# =====================================================================
# FIG 5 -- mechanism: (a) gain vs baseline decile  (b) task-time reallocation
# =====================================================================
fig,axs=plt.subplots(1,2,figsize=(8.6,4.1))
ax=axs[0]
dec=np.arange(1,11)
gain=38-2.9*(dec-1)+rng.normal(0,1.0,10)   # downward slope
ax.scatter(dec,gain,s=34,color=TEAL,zorder=3,edgecolor="white")
z=np.polyfit(dec,gain,1); ax.plot(dec,np.polyval(z,dec),color=DARK,lw=1.3,ls="--",zorder=2)
ax.set_xlabel("Baseline-performance decile (worker skill)")
ax.set_ylabel("Productivity gain from GenAI (%)")
ax.set_title("a  Skill-levelling mechanism",loc="left")
ax.text(6.5,32,f"slope = {z[0]:.1f}%/decile",fontsize=7.4,color=DARK)
ax.set_xticks(dec)
for s in ["top","right"]: ax.spines[s].set_visible(False)
ax=axs[1]
cats=["Routine\ngeneration","Information\nsearch","Analysis &\njudgement","Coordination\n& review","Client /\ncreative"]
before=np.array([34,22,20,12,12]); after=np.array([18,13,29,19,21])
x=np.arange(len(cats)); w=0.38
ax.bar(x-w/2,before,w,label="Before GenAI",color=GREY,edgecolor="white",zorder=3)
ax.bar(x+w/2,after,w,label="After GenAI",color=PURPLE,edgecolor="white",zorder=3)
ax.set_xticks(x); ax.set_xticklabels(cats,fontsize=7)
ax.set_ylabel("Share of working time (%)")
ax.set_title("b  Task reallocation",loc="left")
ax.legend(frameon=False,fontsize=7,loc="upper right")
ax.grid(axis="y",color="#ececec",lw=0.7,zorder=0)
for s in ["top","right"]: ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig(OUT+"/fig5_mechanism.png",bbox_inches="tight"); plt.close()

# =====================================================================
# FIG 6 -- methodology schematic
# =====================================================================
fig,ax=plt.subplots(figsize=(8.6,4.4)); ax.axis("off")
def box(x,y,w,h,text,fc,tc="#111"):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.04",
                 fc=fc,ec="#555",linewidth=0.9))
    ax.text(x+w/2,y+h/2,text,ha="center",va="center",fontsize=7.5,color=tc)
def arrow(x1,y1,x2,y2):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=11,
                 color="#555",linewidth=1.0))
ax.set_xlim(0,10); ax.set_ylim(0,5)
box(0.1,3.3,2.15,1.35,"Worker–task survey\n(n = 3,214 workers,\n820 firms)","#d7e3ef")
box(0.1,0.4,2.15,1.35,"Task taxonomy &\nexposure scoring\n$E_o$ (O*NET-based)","#e7dced")
box(2.75,3.3,2.05,1.35,"Productivity-gain\nestimation by skill\ntercile  $g_{o,q}$","#d5e6df")
box(2.75,0.4,2.05,1.35,"Technology-adoption\nmodel (nested logit)\n$A_{s}(t)$","#f3e2cf")
box(5.3,1.95,2.0,1.25,"Firm-level CES\nproduction &\nuplift  $U_s(t)$","#cdd7e6")
box(7.75,3.25,2.1,1.4,"Productivity\nprojections to 2040\n(6 scenarios)","#d5e6df")
box(7.75,0.45,2.1,1.4,"Inequality\ndecomposition\n(within/between)","#e7cdd3")
arrow(2.25,3.97,2.75,3.97); arrow(2.25,1.07,2.75,1.07)
arrow(4.8,3.97,5.9,2.9); arrow(4.8,1.07,5.9,2.2)
arrow(7.3,2.75,7.75,3.6); arrow(7.3,2.35,7.75,1.45)
ax.text(5.0,4.8,"Generative AI, knowledge-worker productivity and wage inequality",
        ha="center",fontsize=9.2,fontweight="bold")
plt.tight_layout(); plt.savefig(OUT+"/fig6_scheme2.png",bbox_inches="tight"); plt.close()

print("Paper 2 figures done:",sorted(f for f in os.listdir(OUT) if f.endswith('.png')))
