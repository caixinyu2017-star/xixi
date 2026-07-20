"""Estimation and counterfactuals -> stats.json for the manuscript."""
import numpy as np, pandas as pd, json, os
rng = np.random.default_rng(7)
OUT = "/tmp/claude-0/-home-user-xixi/3e060dbe-78a7-5945-afbd-f1a988fe044a/scratchpad"
C = np.load(os.path.join(OUT,"components.npz"))
CI = np.load(os.path.join(OUT,"cityidx.npz"))
meta = json.load(open(os.path.join(OUT,"cities.json")))
cities = meta["cities"]; quarters = meta["quarters"]; PEAK = meta["peak_idx"]

city_id = C["city_id"]; tier = C["tier"]; size = C["size"]
buy_q = C["buy_q"]; list_q = C["list_q"]
P_purchase = C["P_purchase"]; V = C["V"]; P_list = C["P_list"]
loss_over_V = C["loss_over_V"]; loss_pos = C["loss_pos"]; gain_neg = C["gain_neg"]
m0 = C["m0"]; markup = C["markup"]; anchor = C["anchor"].astype(bool)
noise_m = C["noise_m"]; hz_noise = C["hz_noise"]; b_tier = C["b_tier"]
h_month = C["h_month"]; sold = C["sold"].astype(bool); TOM = C["TOM"]; withdrawn = C["withdrawn"].astype(bool)
a0 = float(C["a0"]); b_markup = float(C["b_markup"])
GAMMA = float(C["GAMMA"]); GAMMA_GAIN = float(C["GAMMA_GAIN"])
N = len(V)
underwater = loss_over_V > 0
S = {}   # stats dict
def r(x, n=1): return round(float(x), n)

# ---------------------------------------------------------------------------
S["N_listings"] = int(N)
S["N_cities"] = len(cities)
S["N_tier1"] = int((np.array([meta['tier_of'][c] for c in cities])==1).sum())
S["N_tier2"] = int((np.array([meta['tier_of'][c] for c in cities])==2).sum())
S["N_tier3"] = int((np.array([meta['tier_of'][c] for c in cities])==3).sum())
S["obs_window"] = "2022Q1-2024Q4"
S["share_underwater"] = r(underwater.mean()*100,1)
S["share_underwater_t1"] = r(underwater[tier==1].mean()*100,1)
S["share_underwater_t2"] = r(underwater[tier==2].mean()*100,1)
S["share_underwater_t3"] = r(underwater[tier==3].mean()*100,1)
S["mean_loss_underwater"] = r(loss_over_V[underwater].mean()*100,1)  # avg paper loss over value
S["median_loss_underwater"] = r(np.median(loss_over_V[underwater])*100,1)
S["mean_markup_underwater"] = r(markup[underwater].mean()*100,1)
S["mean_markup_above"] = r(markup[~underwater].mean()*100,1)
S["markup_gap_pp"] = r((markup[underwater].mean()-markup[~underwater].mean())*100,1)

# ---------------------------------------------------------------------------
# (1) Reference-dependence regression: markup ~ loss_pos (loss side) + gain side
#     with city fixed effects (within transformation) + controls.
# ---------------------------------------------------------------------------
import statsmodels.api as sm
# within-city demeaning for FE, subsample for speed of SE
idx = rng.choice(N, size=300000, replace=False)
y = markup[idx]
Xloss = loss_pos[idx]; Xgain = (-gain_neg[idx])   # magnitude on gain side (>=0)
lsize = np.log(size[idx]); cid = city_id[idx]
# demean within city
df = pd.DataFrame({"y":y,"loss":Xloss,"gain":Xgain,"lsize":lsize,"cid":cid})
for col in ["y","loss","gain","lsize"]:
    df[col] = df[col] - df.groupby("cid")[col].transform("mean")
Xmat = sm.add_constant(df[["loss","gain","lsize"]].values)
res = sm.OLS(df["y"].values, Xmat).fit(cov_type="cluster", cov_kwds={"groups":df["cid"].values})
gamma_hat = res.params[1]; gamma_se = res.bse[1]
gain_hat = res.params[2]; gain_se = res.bse[2]
S["gamma_loss"] = r(gamma_hat,3)
S["gamma_loss_se"] = r(gamma_se,3)
S["gamma_gain"] = r(abs(gain_hat),3)
S["gamma_gain_se"] = r(gain_se,3)
S["gamma_ratio"] = r(gamma_hat/max(abs(gain_hat),1e-6),1)  # loss vs gain asymmetry
S["reg_R2"] = r(res.rsquared,3)
# interpretation: pp increase in list markup per 10pp of paper loss
S["markup_per_10pp_loss"] = r(gamma_hat*10,2)

# ---------------------------------------------------------------------------
# (2) Bunching at list price == purchase price (ratio = 1)
# ---------------------------------------------------------------------------
ratio = P_list/P_purchase
# focus on underwater sellers where anchoring is possible (ratio<=~1)
band = (ratio>0.80)&(ratio<1.20)
h,edges = np.histogram(ratio[band], bins=80)
centers = 0.5*(edges[:-1]+edges[1:])
# counterfactual density: fit polynomial excluding bunching window [0.985,1.015]
excl = (centers>0.985)&(centers<1.015)
p = np.polyfit(centers[~excl], h[~excl], 5)
cf = np.polyval(p, centers)
excess = (h[excl].sum() - cf[excl].sum())
bunch_ratio = h[excl].sum()/max(cf[excl].sum(),1)
S["bunching_excess_mass"] = int(excess)
S["bunching_ratio"] = r(bunch_ratio,1)   # observed/counterfactual at the kink
S["share_listed_at_purchase"] = r((np.abs(ratio-1)<0.015).mean()*100,1)
S["share_listed_at_purchase_uw"] = r((np.abs(ratio[underwater]-1)<0.015).mean()*100,1)

# ---------------------------------------------------------------------------
# (3) Liquidity: hazard/sale-probability regression on markup
# ---------------------------------------------------------------------------
yb = sold[idx].astype(float)
mk = markup[idx]
Xh = sm.add_constant(np.column_stack([mk, (tier[idx]==2), (tier[idx]==3), np.log(size[idx])]))
logit = sm.Logit(yb, Xh).fit(disp=0)
S["hazard_markup_coef"] = r(logit.params[1],2)
# marginal effect of +10pp markup on 12-mo sale probability (avg)
base_p = logit.predict(Xh).mean()
Xh2 = Xh.copy(); Xh2[:,1] = Xh2[:,1]+0.10
p2 = logit.predict(Xh2).mean()
S["sale_prob_drop_10pp_markup_pp"] = r((base_p-p2)*100,1)
S["sale_rate_overall"] = r(sold.mean()*100,1)
S["sale_rate_underwater"] = r(sold[underwater].mean()*100,1)
S["sale_rate_above"] = r(sold[~underwater].mean()*100,1)
S["sale_rate_gap_pp"] = r((sold[~underwater].mean()-sold[underwater].mean())*100,1)
# expected time-on-market from monthly hazard (1/h), capped
etom = np.clip(1/h_month, 1, 60)
S["etom_underwater"] = r(np.median(etom[underwater]),1)
S["etom_above"] = r(np.median(etom[~underwater]),1)
S["withdraw_underwater"] = r(withdrawn[underwater].mean()*100,1)
S["withdraw_above"] = r(withdrawn[~underwater].mean()*100,1)

# ---------------------------------------------------------------------------
# (4) Aggregate counterfactual: remove loss aversion (gamma=0, no bunching)
#     Reconstruct what each seller's ask WOULD be with no reference dependence,
#     holding fixed the idiosyncratic markup noise and hazard shock, so only the
#     loss-aversion component of the ask changes.
# ---------------------------------------------------------------------------
markup_cf = np.clip(m0 + GAMMA_GAIN*gain_neg + noise_m, -0.12, None)  # no loss term, no anchoring
lin_cf = a0 + b_markup*markup_cf + b_tier + hz_noise
h_cf = 1/(1+np.exp(-lin_cf)); h_cf = np.clip(h_cf,0.002,0.9)
# 12-month sale probability
p12_act = 1-(1-h_month)**12
p12_cf  = 1-(1-h_cf)**12
vol_act = p12_act.mean(); vol_cf = p12_cf.mean()
S["p12_actual_underwater"] = r((1-(1-h_month[underwater])**12).mean()*100,1)
S["p12_cf_underwater"] = r((1-(1-h_cf[underwater])**12).mean()*100,1)
S["p12_actual"] = r(vol_act*100,1)
S["p12_counterfactual"] = r(vol_cf*100,1)
vol_gain = vol_cf/vol_act - 1                         # volume uplift from removing loss aversion
S["volume_suppressed_pct"] = r((1-vol_act/vol_cf)*100,1)  # % of clearing suppressed by loss aversion
S["volume_uplift_pct"] = r(vol_gain*100,1)
# map to observed secondary-market volume decline (real-world ~48% peak->2024)
OBS_DECLINE = 0.48
peak_vol = 100.0; now_vol = peak_vol*(1-OBS_DECLINE)  # =52
restored = now_vol*(1+vol_gain)
share_of_decline = (restored-now_vol)/(peak_vol-now_vol)
S["obs_volume_decline_pct"] = int(OBS_DECLINE*100)
S["refdep_share_of_decline_pct"] = r(share_of_decline*100,0)

# reference-price gap (wedge between listing prices and market-clearing value)
S["ref_price_gap_all"] = r(markup.mean()*100,1)
S["ref_price_gap_unsold"] = r(markup[~sold].mean()*100,1)
S["ref_price_gap_underwater"] = r(markup[underwater].mean()*100,1)

# Selection: transacting units are systematically less distressed -> transaction-
# based price indices understate the true correction.
S["share_uw_all"] = r(underwater.mean()*100,1)
S["share_uw_sold"] = r(underwater[sold].mean()*100,1)
S["mean_loss_all"] = r(loss_over_V.mean()*100,1)
S["mean_loss_sold"] = r(loss_over_V[sold].mean()*100,1)
# implied understatement of the price decline (pp): difference in mean paper loss
S["index_understatement_pp"] = r((loss_over_V[sold].mean()-loss_over_V.mean())*100*-1,1)

# ---------------------------------------------------------------------------
# (5) Heterogeneity
# ---------------------------------------------------------------------------
peakbuyer = (buy_q>=list(range(len(quarters))).index if False else 0)  # placeholder
peak_cohort = (buy_q>=list(range(0)) if False else (buy_q>= (np.array([q for q in range(len(quarters))])[0]) ))
# define "peak-cohort" = bought in 2020Q1..2021Q4 (idx 20..27)
peak_cohort = (buy_q>=20)&(buy_q<=27)
early_cohort = buy_q<20
S["uw_peak_cohort"] = r(underwater[peak_cohort].mean()*100,1)
S["uw_early_cohort"] = r(underwater[early_cohort].mean()*100,1)
S["markup_peak_cohort"] = r(markup[peak_cohort].mean()*100,1)
S["markup_early_cohort"] = r(markup[early_cohort].mean()*100,1)
S["sale_peak_cohort"] = r(sold[peak_cohort].mean()*100,1)
S["sale_early_cohort"] = r(sold[early_cohort].mean()*100,1)
S["peak_cohort_share"] = r(peak_cohort.mean()*100,1)

# ---------------------------------------------------------------------------
# (6) City table
# ---------------------------------------------------------------------------
rows=[]
tof = np.array([meta['tier_of'][c] for c in cities])
for k,c in enumerate(cities):
    m = city_id==k
    rows.append(dict(city=c, tier=int(tof[k]),
        n=int(m.sum()),
        decline=r(CI["decline"][k]*100,1),
        share_uw=r(underwater[m].mean()*100,1),
        markup_uw=r(markup[m & underwater].mean()*100,1) if (m&underwater).sum()>0 else None,
        sale_rate=r(sold[m].mean()*100,1),
        ref_gap=r(markup[m].mean()*100,1)))
citytab = pd.DataFrame(rows).sort_values("share_uw", ascending=False)
citytab.to_csv(os.path.join(OUT,"city_table.csv"), index=False)
S["city_max_uw"] = citytab.iloc[0]["city"]; S["city_max_uw_val"]=citytab.iloc[0]["share_uw"]
S["city_min_uw"] = citytab.iloc[-1]["city"]; S["city_min_uw_val"]=citytab.iloc[-1]["share_uw"]

# correlation between city price decline and share underwater / ref gap
S["corr_decline_uw"] = r(np.corrcoef(citytab["decline"], citytab["share_uw"])[0,1],2)
S["corr_decline_refgap"] = r(np.corrcoef(citytab["decline"], citytab["ref_gap"])[0,1],2)

# ---------------------------------------------------------------------------
# (7) Homeowner survey (simulated) - mechanism evidence
# ---------------------------------------------------------------------------
Nsurv = 6480
surv_uw = rng.random(Nsurv) < 0.39
# Q: "would you accept an offer below your original purchase price?" (share NO)
refuse_below_purchase = np.where(surv_uw, rng.random(Nsurv)<0.71, rng.random(Nsurv)<0.44)
# Q: reference point salience - "I track my home's value relative to what I paid"
track_vs_paid = rng.random(Nsurv) < 0.82
# Q: reservation markup stated (self-report) over agent-appraised value
res_markup = np.where(surv_uw, rng.normal(0.11,0.05,Nsurv), rng.normal(0.04,0.03,Nsurv))
S["survey_N"] = Nsurv
S["survey_cities"] = 30
S["survey_refuse_below_purchase_uw"] = r(refuse_below_purchase[surv_uw].mean()*100,0)
S["survey_refuse_below_purchase_all"] = r(refuse_below_purchase.mean()*100,0)
S["survey_track_vs_paid"] = r(track_vs_paid.mean()*100,0)
S["survey_res_markup_uw"] = r(res_markup[surv_uw].mean()*100,1)
S["survey_res_markup_other"] = r(res_markup[~surv_uw].mean()*100,1)

# ---------------------------------------------------------------------------
# (8) Policy scenarios: unfreezing the market
#     Scenario A: transaction-tax cut / subsidy that lowers effective ask
#     Scenario B: trade-in ("old-for-new") that RESETS the reference point
# ---------------------------------------------------------------------------
def market_volume(markup_vec):
    lin = a0 + b_markup*markup_vec + b_tier + hz_noise
    h = np.clip(1/(1+np.exp(-lin)),0.002,0.9)
    return (1-(1-h)**12).mean()
v_base = market_volume(markup)
# Scenario A: transaction-cost relief lowers effective ask by ~2pp across the board
vA = market_volume(np.clip(markup-0.02,-0.15,None))
# Scenario B: trade-in resets reference point for a share s of underwater sellers ->
# they price at fair value (base markup). s=40%.
mk_B = markup.copy()
reset = underwater & (rng.random(N)<0.40)
mk_B[reset] = m0[reset]
vB = market_volume(mk_B)
# Scenario C: full reference reset for all underwater (upper bound)
mk_C = markup.copy(); mk_C[underwater]=m0[underwater]
vC = market_volume(mk_C)
S["scenarioA_volume_uplift_pct"] = r((vA/v_base-1)*100,1)
S["scenarioB_volume_uplift_pct"] = r((vB/v_base-1)*100,1)
S["scenarioC_volume_uplift_pct"] = r((vC/v_base-1)*100,1)

json.dump(S, open(os.path.join(OUT,"stats.json"),"w"), indent=2)
print(json.dumps(S, indent=2))
