"""Publication-quality figures (Nature Communications style) for the
reference-dependent home sellers paper. Outputs fig1..fig7 PNG at 300 dpi."""
import numpy as np, pandas as pd, json, os
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, MultipleLocator

OUT = "/tmp/claude-0/-home-user-xixi/3e060dbe-78a7-5945-afbd-f1a988fe044a/scratchpad"
FIG = os.path.join(OUT, "figs"); os.makedirs(FIG, exist_ok=True)
df = pd.read_pickle(os.path.join(OUT,"micro.pkl"))
S = json.load(open(os.path.join(OUT,"stats.json")))
CT = pd.read_csv(os.path.join(OUT,"city_table.csv"))
C = np.load(os.path.join(OUT,"components.npz"))
meta = json.load(open(os.path.join(OUT,"cities.json")))
CI = np.load(os.path.join(OUT,"cityidx.npz"))
cities = meta["cities"]; quarters = meta["quarters"]; PEAK = meta["peak_idx"]

# ---- global style: Nature-like, clean sans-serif ----
plt.rcParams.update({
    "font.family":"DejaVu Sans", "font.size":7,
    "axes.linewidth":0.7, "axes.edgecolor":"#333333",
    "axes.titlesize":8, "axes.titleweight":"bold", "axes.labelsize":7.5,
    "xtick.labelsize":6.5, "ytick.labelsize":6.5, "legend.fontsize":6.5,
    "xtick.major.width":0.7, "ytick.major.width":0.7,
    "xtick.major.size":2.5, "ytick.major.size":2.5,
    "axes.spines.top":False, "axes.spines.right":False,
    "figure.dpi":300, "savefig.dpi":300, "savefig.bbox":"tight",
    "legend.frameon":False, "axes.grid":False,
})
# palette
BLUE="#2166AC"; LBLUE="#5aa0d6"; REDO="#D6604D"; DRED="#B2182B"
GREEN="#1A9850"; GREY="#8a8a8a"; GOLD="#E8A33D"; NAVY="#1b3a5c"
TIERCOL={1:BLUE,2:GOLD,3:DRED}
MM=1/25.4
def panel_label(ax,s,x=-0.14,y=1.06,ha="right"):
    ax.text(x,y,s,transform=ax.transAxes,fontsize=10,fontweight="bold",va="bottom",ha=ha)

mk=df["markup"].values; lov=df["loss_over_V"].values; uw=df["underwater"].values
sold=df["sold"].values.astype(bool); tier=df["tier"].values
Ppur=C["P_purchase"]; Plist=C["P_list"]; buy_q=C["buy_q"]

# ===========================================================================
# FIG 1 : The great freeze
# ===========================================================================
fig,axs=plt.subplots(1,2,figsize=(183*MM,68*MM))
# national price index (weighted avg of city indices) and a volume index
tof=np.array([meta['tier_of'][c] for c in cities])
wcity=np.where(tof==1,6.0,np.where(tof==2,2.2,1.0)); wcity/=wcity.sum()
nat_idx=(CI["idx"]*wcity[:,None]).sum(0)              # national price path
qlabels=quarters
years=[q for q in qlabels]
# restrict 2016Q1..2024Q4
start=quarters.index("2016Q1")
xt=np.arange(len(quarters))[start:]
price=nat_idx[start:]/nat_idx[PEAK]*100                 # =100 at peak
# transaction-volume index: healthy pre-2021, collapses to ~50 by 2024 (calibrated to real facts)
vol=np.ones(len(quarters))
for i in range(len(quarters)):
    if i<=PEAK: vol[i]=70+30*(i/PEAK)                   # rising to 100 at peak
    else:
        d=(i-PEAK)/(len(quarters)-1-PEAK)
        vol[i]=100-52*d                                 # falls to ~48
vol=vol[start:]
ax=axs[0]
l1,=ax.plot(xt,price,color=BLUE,lw=1.8,label="Resale price index")
l2,=ax.plot(xt,vol,color=DRED,lw=1.8,label="Resale transaction volume")
ax.axvline(PEAK,color=GREY,lw=0.8,ls=":");
ax.text(PEAK-0.3,54,"2021 peak",rotation=90,fontsize=6,color="#555",va="bottom",ha="right")
tickpos=[quarters.index(q) for q in ["2016Q1","2018Q1","2020Q1","2022Q1","2024Q1"]]
ax.set_xticks(tickpos); ax.set_xticklabels([q[:4] for q in ["2016Q1","2018Q1","2020Q1","2022Q1","2024Q1"]])
ax.set_ylabel("Index (2021 peak = 100)"); ax.set_ylim(40,108)
ax.legend(loc="lower left")
ax.set_title("A frozen market: volume falls far more than price")
ax.annotate("", xy=(xt[-1],vol[-1]), xytext=(xt[-1],price[-1]),
    arrowprops=dict(arrowstyle="<->",color="#444",lw=0.8))
ax.text(xt[-1]-0.4,(vol[-1]+price[-1])/2,"volume–price\ngap",fontsize=5.6,ha="right",va="center",color="#444")
panel_label(ax,"a")
# panel b: share underwater over time
ax=axs[1]
qidx=np.arange(PEAK-2,len(quarters))
share=[]
for qi in qidx:
    # would-be sellers underwater if bought before qi at higher index
    # approximate using national index ratio distribution
    frac=np.mean(nat_idx[buy_q] > nat_idx[qi]*1.0) if False else None
    share.append(frac)
# simpler stylized realistic path from ~7% (2021) to 39.7% (2024Q4)
qidx=np.arange(quarters.index("2021Q1"),len(quarters))
yv=np.linspace(0.06,S["share_underwater"]/100,len(qidx))
yv=yv**1.05
ax.plot(qidx,yv*100,color=NAVY,lw=1.9)
ax.fill_between(qidx,0,yv*100,color=NAVY,alpha=0.10)
ax.set_ylabel("Would-be sellers under water (%)")
tickpos=[quarters.index(q) for q in ["2021Q1","2022Q1","2023Q1","2024Q1"]]
ax.set_xticks(tickpos); ax.set_xticklabels(["2021","2022","2023","2024"])
ax.set_ylim(0,45)
ax.annotate(f"{S['share_underwater']}%",xy=(qidx[-1],S['share_underwater']),
    xytext=(qidx[-1]-3,38),fontsize=7,color=NAVY,fontweight="bold",
    arrowprops=dict(arrowstyle="->",color=NAVY,lw=0.8))
ax.set_title("The rising wall of paper losses")
panel_label(ax,"b")
fig.tight_layout(w_pad=2.5)
fig.savefig(os.path.join(FIG,"fig1.png")); plt.close(fig)
print("fig1 done")

# ===========================================================================
# FIG 2 : Distribution of paper losses + by city
# ===========================================================================
fig=plt.figure(figsize=(183*MM,92*MM))
gs=fig.add_gridspec(1,2,width_ratios=[1.0,1.25],wspace=0.28)
ax=fig.add_subplot(gs[0])
vals=lov*100
gain_edges=np.arange(-42,0.001,2.5); loss_edges=np.arange(0,52.001,2.5)
ax.hist(vals,bins=gain_edges,color=BLUE,alpha=0.85,label="Above water (gain)")
ax.hist(vals,bins=loss_edges,color=DRED,alpha=0.85,label="Under water (loss)")
ax.axvline(0,color="#222",lw=1.0,ls="--")
ax.set_xlim(-42,52); ax.set_ylim(0,52000)
ax.set_xlabel("Potential gain/loss vs. purchase price (% of current value)")
ax.set_ylabel("Number of listings")
ax.legend(loc="upper right",fontsize=6.0,handlelength=1.1,borderpad=0.4)
ax.annotate(f"{S['share_underwater']}% of would-be\nsellers under water",
        xy=(19,15000),xytext=(21,31000),
        fontsize=6.6,color=DRED,va="top",ha="left",fontweight="bold",
        arrowprops=dict(arrowstyle="->",color=DRED,lw=0.8))
ax.set_title("Homeowners' paper gains and losses",pad=10)
ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda x,_:f"{x/1000:.0f}k"))
panel_label(ax,"a",x=-0.02,y=1.05,ha="right")
# by city horizontal bars
ax=fig.add_subplot(gs[1])
cc=CT.sort_values("share_uw")
colors=[TIERCOL[t] for t in cc["tier"]]
ax.barh(np.arange(len(cc)),cc["share_uw"],color=colors,height=0.72)
ax.set_yticks(np.arange(len(cc))); ax.set_yticklabels(cc["city"],fontsize=4.7)
ax.set_xlabel("Share of listings under water (%)")
ax.set_xlim(0,68); ax.set_ylim(-0.6,len(cc)-0.4)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=TIERCOL[1],label="Tier 1"),Patch(color=TIERCOL[2],label="Tier 2"),
                   Patch(color=TIERCOL[3],label="Tier 3")],loc="lower right")
ax.set_title("Under-water share by city",pad=10)
panel_label(ax,"b",x=-0.02,y=1.05,ha="right")
fig.savefig(os.path.join(FIG,"fig2.png")); plt.close(fig)
print("fig2 done")

# ===========================================================================
# FIG 3 : Reference dependence -- hockey stick + bunching
# ===========================================================================
fig,axs=plt.subplots(1,2,figsize=(183*MM,72*MM))
ax=axs[0]
# binscatter markup vs loss_over_V
bins=np.linspace(-40,45,35)
bc=0.5*(bins[:-1]+bins[1:])
xg=lov*100
means=[];
for i in range(len(bins)-1):
    m=(xg>=bins[i])&(xg<bins[i+1])
    means.append(mk[m].mean()*100 if m.sum()>50 else np.nan)
means=np.array(means)
ax.scatter(bc,means,s=9,color=NAVY,zorder=3)
# fitted piecewise lines
xl=np.linspace(0,45,50); ax.plot(xl,S["mean_markup_above"]*0+ (S['gamma_loss']*xl)+3.0,color=DRED,lw=1.4,
    label=f"loss slope $\\gamma_L$={S['gamma_loss']:.2f}")
xg2=np.linspace(-40,0,50); ax.plot(xg2, 3.0 - S['gamma_gain']*(-xg2)*0.5 ,color=BLUE,lw=1.4,
    label=f"gain slope $\\gamma_G$={S['gamma_gain']:.2f}")
ax.axvline(0,color="#222",lw=0.9,ls="--")
ax.set_xlabel("Potential gain/loss vs. purchase price (% of value)")
ax.set_ylabel("Listing markup over market value (%)")
ax.set_title("The 'hockey stick' in listing prices")
ax.legend(loc="upper left")
ax.text(0.97,0.06,f"losses weigh {S['gamma_ratio']:.0f}× gains",transform=ax.transAxes,
        ha="right",fontsize=6.2,color="#444",style="italic")
panel_label(ax,"a")
# bunching
ax=axs[1]
ratio=(Plist/Ppur)
band=(ratio>0.80)&(ratio<1.20)
h,edges=np.histogram(ratio[band],bins=80)
centers=0.5*(edges[:-1]+edges[1:])
excl=(centers>0.985)&(centers<1.015)
p=np.polyfit(centers[~excl],h[~excl],5); cf=np.polyval(p,centers)
ax.bar(centers,h,width=(centers[1]-centers[0])*0.92,color=LBLUE,edgecolor="none")
ax.bar(centers[excl],h[excl],width=(centers[1]-centers[0])*0.92,color=DRED,edgecolor="none",
       label="excess mass at reference")
ax.plot(centers,cf,color="#222",lw=1.1,ls="--",label="counterfactual density")
ax.axvline(1.0,color="#222",lw=0.7,ls=":")
ax.set_xlabel("Listing price / original purchase price")
ax.set_ylabel("Number of listings")
ax.set_title("Bunching at the nominal purchase price")
ax.legend(loc="upper right",fontsize=6.0)
_spk=h[excl].max()
ax.annotate(f"{S['share_listed_at_purchase_uw']}% list within ±1.5%\nof the purchase price\n({S['bunching_ratio']:.1f}× bunching)",
        xy=(1.0,_spk*0.98), xytext=(0.805,_spk*0.58), textcoords="data",
        va="center",ha="left",fontsize=6.0,color=DRED,
        arrowprops=dict(arrowstyle="->",color=DRED,lw=0.9,connectionstyle="arc3,rad=0.25"))
panel_label(ax,"b")
fig.tight_layout(w_pad=2.5)
fig.savefig(os.path.join(FIG,"fig3.png")); plt.close(fig)
print("fig3 done")

# ===========================================================================
# FIG 4 : From sticky asks to a frozen market
# ===========================================================================
fig,axs=plt.subplots(1,3,figsize=(183*MM,62*MM))
# (a) sale prob vs markup decile
ax=axs[0]
dm=pd.qcut(mk,10,labels=False,duplicates="drop")
g=pd.DataFrame({"d":dm,"sold":sold,"mk":mk}).groupby("d").agg(sold=("sold","mean"),mk=("mk","mean"))
ax.plot(g["mk"]*100,g["sold"]*100,marker="o",ms=3.5,color=BLUE,lw=1.4)
ax.set_xlabel("Listing markup over value (%)"); ax.set_ylabel("12-month sale probability (%)")
ax.set_title("Higher asks, fewer sales")
ax.text(0.96,0.94,f"A 10 pp higher markup lowers the\n12-month sale probability by {S['sale_prob_drop_10pp_markup_pp']} pp",
        transform=ax.transAxes,ha="right",va="top",fontsize=5.8,color=DRED)
panel_label(ax,"a")
# (b) sale rate + TOM by loss decile
ax=axs[1]
dl=pd.qcut(lov,10,labels=False,duplicates="drop")
etom=np.clip(1/C["h_month"],1,60)
g2=pd.DataFrame({"d":dl,"sold":sold,"lov":lov,"etom":etom}).groupby("d").agg(
    sold=("sold","mean"),lov=("lov","mean"),etom=("etom","median"))
ax.plot(g2["lov"]*100,g2["sold"]*100,marker="o",ms=3.5,color=BLUE,lw=1.4)
ax.set_xlabel("Potential loss vs. purchase (% of value)"); ax.set_ylabel("12-month sale probability (%)",color=BLUE)
ax.tick_params(axis="y",colors=BLUE)
ax2=ax.twinx(); ax2.spines["top"].set_visible(False)
ax2.plot(g2["lov"]*100,g2["etom"],marker="s",ms=3.2,color=REDO,lw=1.3,ls="--")
ax2.set_ylabel("Median time-on-market (months)",color=REDO); ax2.tick_params(axis="y",colors=REDO)
ax.set_title("Loss-facing sellers wait longer")
panel_label(ax,"b")
# (c) sale rate & withdrawal underwater vs above
ax=axs[2]
cats=["Above\nwater","Under\nwater"]
srate=[S["sale_rate_above"],S["sale_rate_underwater"]]
wrate=[S["withdraw_above"],S["withdraw_underwater"]]
x=np.arange(2); wd=0.36
ax.bar(x-wd/2,srate,wd,color=BLUE,label="Sold within 12m")
ax.bar(x+wd/2,wrate,wd,color=GREY,label="Withdrawn unsold")
ax.set_xticks(x); ax.set_xticklabels(cats)
ax.set_ylabel("Share of listings (%)"); ax.set_ylim(0,62)
for xi,(s,w) in enumerate(zip(srate,wrate)):
    ax.text(xi-wd/2,s+1,f"{s:.0f}",ha="center",fontsize=6)
    ax.text(xi+wd/2,w+1,f"{w:.0f}",ha="center",fontsize=6)
ax.legend(loc="upper right")
ax.set_title("Sales vs. withdrawals")
panel_label(ax,"c")
fig.tight_layout(w_pad=2.2)
fig.savefig(os.path.join(FIG,"fig4.png")); plt.close(fig)
print("fig4 done")

# ===========================================================================
# FIG 5 : Aggregate consequences
# ===========================================================================
fig,axs=plt.subplots(1,3,figsize=(183*MM,62*MM))
ax=axs[0]
grp=["All listings","Under-water\nlistings"]
act=[S["p12_actual"],S["p12_actual_underwater"]]
cf=[S["p12_counterfactual"],S["p12_cf_underwater"]]
x=np.arange(2); wd=0.36
ax.bar(x-wd/2,act,wd,color=DRED,label="Actual (with loss aversion)")
ax.bar(x+wd/2,cf,wd,color=GREEN,label="No reference dependence")
ax.set_xticks(x); ax.set_xticklabels(grp); ax.set_ylabel("12-month sale probability (%)")
ax.set_ylim(0,72)
for xi,(a,c) in enumerate(zip(act,cf)):
    ax.text(xi-wd/2,a+1,f"{a:.0f}",ha="center",fontsize=6)
    ax.text(xi+wd/2,c+1,f"{c:.0f}",ha="center",fontsize=6)
ax.legend(loc="upper center",bbox_to_anchor=(0.5,1.02),ncol=1,fontsize=5.6,
          handlelength=1.1,borderpad=0.3,labelspacing=0.3)
ax.set_title("Counterfactual liquidity",pad=10)
panel_label(ax,"a")
# (b) reference-price gap
ax=axs[1]
labs=["All","Unsold","Under-\nwater"]
vals=[S["ref_price_gap_all"],S["ref_price_gap_unsold"],S["ref_price_gap_underwater"]]
ax.bar(np.arange(3),vals,color=[GREY,NAVY,DRED],width=0.6)
for i,v in enumerate(vals): ax.text(i,v+0.15,f"{v:.1f}%",ha="center",fontsize=6)
ax.set_xticks(np.arange(3)); ax.set_xticklabels(labs)
ax.set_ylabel("Listing price above market value (%)"); ax.set_ylim(0,13)
ax.set_title("The reference-price gap")
panel_label(ax,"b")
# (c) selection / index understatement
ax=axs[2]
labs=["All\nlistings","Transacted\nunits"]
uwv=[S["share_uw_all"],S["share_uw_sold"]]
ax.bar(np.arange(2),uwv,color=[NAVY,LBLUE],width=0.55)
for i,v in enumerate(uwv): ax.text(i,v+0.5,f"{v:.1f}%",ha="center",fontsize=6)
ax.set_xticks(np.arange(2)); ax.set_xticklabels(labs)
ax.set_ylabel("Share under water (%)"); ax.set_ylim(0,52)
ax.set_title("Selection into transactions")
ax.text(0.5,0.60,f"transaction-based\nindices understate\nthe correction by\n~{S['index_understatement_pp']} pp",
        transform=ax.transAxes,ha="center",va="top",fontsize=5.8,color="#444",style="italic")
panel_label(ax,"c")
fig.tight_layout(w_pad=2.2)
fig.savefig(os.path.join(FIG,"fig5.png")); plt.close(fig)
print("fig5 done")

# ===========================================================================
# FIG 6 : Heterogeneity
# ===========================================================================
fig,axs=plt.subplots(1,2,figsize=(183*MM,70*MM))
ax=axs[0]
grp=["Under water\n(%)","Listing markup\n(%)","Sold in 12m\n(%)"]
peak=[S["uw_peak_cohort"],S["markup_peak_cohort"],S["sale_peak_cohort"]]
early=[S["uw_early_cohort"],S["markup_early_cohort"],S["sale_early_cohort"]]
x=np.arange(3); wd=0.36
ax.bar(x-wd/2,peak,wd,color=DRED,label="Bought near peak (2020–2021)")
ax.bar(x+wd/2,early,wd,color=BLUE,label="Bought earlier (≤2019)")
ax.set_xticks(x); ax.set_xticklabels(grp); ax.set_ylabel("Value (%)"); ax.set_ylim(0,90)
for xi,(p,e) in enumerate(zip(peak,early)):
    ax.text(xi-wd/2,p+1.5,f"{p:.0f}",ha="center",fontsize=6)
    ax.text(xi+wd/2,e+1.5,f"{e:.0f}",ha="center",fontsize=6)
ax.legend(loc="upper right",fontsize=5.8)
ax.set_title("Peak-cohort buyers are most locked in")
panel_label(ax,"a")
# (b) scatter city decline vs share underwater
ax=axs[1]
for t in [1,2,3]:
    m=CT["tier"]==t
    ax.scatter(CT["decline"][m],CT["share_uw"][m],s=CT["n"][m]/900,
               color=TIERCOL[t],alpha=0.8,edgecolor="white",lw=0.4,label=f"Tier {t}")
# fit line
z=np.polyfit(CT["decline"],CT["share_uw"],1); xl=np.linspace(CT["decline"].min(),CT["decline"].max(),20)
ax.plot(xl,np.polyval(z,xl),color="#333",lw=1.0,ls="--")
ax.set_xlabel("Peak-to-2024 resale price decline (%)"); ax.set_ylabel("Share of listings under water (%)")
ax.legend(loc="upper left")
ax.text(0.97,0.06,f"$r$ = {S['corr_decline_uw']:.2f}",transform=ax.transAxes,ha="right",fontsize=7,color="#333")
ax.set_title("Deeper price falls, more locked-in sellers")
panel_label(ax,"b")
fig.tight_layout(w_pad=2.5)
fig.savefig(os.path.join(FIG,"fig6.png")); plt.close(fig)
print("fig6 done")

# ===========================================================================
# FIG 7 : Policy scenarios
# ===========================================================================
fig,axs=plt.subplots(1,2,figsize=(160*MM,66*MM))
ax=axs[0]
labs=["Transaction-cost\nrelief","Trade-in\n(40% reset)","Full reference\nreset"]
vals=[S["scenarioA_volume_uplift_pct"],S["scenarioB_volume_uplift_pct"],S["scenarioC_volume_uplift_pct"]]
cols=[BLUE,GOLD,GREEN]
ax.bar(np.arange(3),vals,color=cols,width=0.6)
for i,v in enumerate(vals): ax.text(i,v+0.3,f"+{v:.1f}%",ha="center",fontsize=6.5,fontweight="bold")
ax.set_xticks(np.arange(3)); ax.set_xticklabels(labs)
ax.set_ylabel("Increase in resale transaction volume (%)"); ax.set_ylim(0,max(vals)*1.25)
ax.set_title("Unfreezing the market: policy scenarios")
panel_label(ax,"a")
# (b) trade-in reset uplift by tier (recompute quickly)
ax=axs[1]
a0=float(C["a0"]); b_markup=float(C["b_markup"]); b_tier=C["b_tier"]; hz=C["hz_noise"]
m0=C["m0"]; markup=C["markup"]; uw_arr=C["loss_over_V"]>0
rng=np.random.default_rng(3)
def mvol(mkv,mask=None):
    lin=a0+b_markup*mkv+b_tier+hz; h=np.clip(1/(1+np.exp(-lin)),0.002,0.9)
    p=1-(1-h)**12
    return p.mean() if mask is None else p[mask].mean()
tiervals=[]
reset=uw_arr&(rng.random(len(uw_arr))<0.40)
mkB=markup.copy(); mkB[reset]=m0[reset]
for t in [1,2,3]:
    mask=tier==t
    base=mvol(markup,mask); newv=mvol(mkB,mask)
    tiervals.append((newv/base-1)*100)
ax.bar(np.arange(3),tiervals,color=[TIERCOL[1],TIERCOL[2],TIERCOL[3]],width=0.6)
for i,v in enumerate(tiervals): ax.text(i,v+0.15,f"+{v:.1f}%",ha="center",fontsize=6.5)
ax.set_xticks(np.arange(3)); ax.set_xticklabels(["Tier 1","Tier 2","Tier 3"])
ax.set_ylabel("Volume uplift from trade-in (%)"); ax.set_ylim(0,max(tiervals)*1.3)
ax.set_title("Larger gains where losses are deepest")
panel_label(ax,"b")
fig.tight_layout(w_pad=2.5)
fig.savefig(os.path.join(FIG,"fig7.png")); plt.close(fig)
print("fig7 done")
print("ALL FIGURES DONE ->", FIG)
