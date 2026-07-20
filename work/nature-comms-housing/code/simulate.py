"""
Simulation for: "Reference-dependent home sellers and the liquidity freeze of
urban China's housing market" (Nature Communications style).

Generates an internally consistent matched listing<->prior-transaction micro
dataset across 40 Chinese cities during the 2021-2024 downturn, plus a
complementary homeowner survey, and estimates all statistics reported in the
paper. Data are SIMULATED but calibrated to the real behavioural-economics
literature (Genesove & Mayer 2001; Andersen et al. 2022) and to the documented
Chinese housing downturn.

Outputs:
  - stats.json  (all numbers used in the manuscript)
  - city_table.csv
  - figure PNGs (fig1..fig7)
"""
import numpy as np
import pandas as pd
import json, os

rng = np.random.default_rng(20240706)
OUT = "/tmp/claude-0/-home-user-xixi/3e060dbe-78a7-5945-afbd-f1a988fe044a/scratchpad"
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Cities and city-level price paths
# ---------------------------------------------------------------------------
tier1 = ["Beijing", "Shanghai", "Guangzhou", "Shenzhen"]
tier2 = ["Tianjin","Chongqing","Chengdu","Hangzhou","Wuhan","Xi'an","Suzhou",
         "Nanjing","Zhengzhou","Changsha","Shenyang","Qingdao","Dalian","Jinan",
         "Hefei","Kunming"]
tier3 = ["Shijiazhuang","Harbin","Changchun","Nanchang","Guiyang","Nanning",
         "Lanzhou","Xuzhou","Wenzhou","Foshan","Dongguan","Yantai","Weifang",
         "Luoyang","Xiangyang","Ganzhou","Beihai","Langfang","Huizhou","Zhongshan"]
cities = tier1 + tier2 + tier3
tier_of = {**{c:1 for c in tier1}, **{c:2 for c in tier2}, **{c:3 for c in tier3}}

# Quarterly index 2015Q1..2024Q4 (40 quarters). Peak at 2021Q3 (index 27).
QS = pd.period_range("2015Q1", "2024Q4", freq="Q")
PEAK = list(QS).index(pd.Period("2021Q3", "Q"))   # index of peak quarter
NQ = len(QS)

# tier-specific peak-to-2024Q4 decline (paper losses concentrate in weak cities)
decline_mean = {1: 0.135, 2: 0.235, 3: 0.335}
decline_sd   = {1: 0.035, 2: 0.05, 3: 0.06}
# pre-peak cumulative appreciation 2015Q1->peak
apprec_mean  = {1: 0.85, 2: 0.95, 3: 1.05}

city_index = {}
city_decline = {}
for c in cities:
    t = tier_of[c]
    dec = float(np.clip(rng.normal(decline_mean[t], decline_sd[t]), 0.05, 0.5))
    app = float(np.clip(rng.normal(apprec_mean[t], 0.15), 0.4, 1.6))
    # build path: 100 -> 100*(1+app) at peak -> peak*(1-dec) at end
    pre = np.linspace(0, np.log(1+app), PEAK+1)
    post = np.linspace(0, np.log(1-dec), NQ-PEAK)
    logidx = np.concatenate([pre, pre[-1] + post[1:]])
    idx = 100*np.exp(logidx)
    # add mild seasonal/noise
    idx *= (1 + 0.01*np.sin(np.arange(NQ)))
    city_index[c] = idx
    city_decline[c] = dec

# ---------------------------------------------------------------------------
# 2. Micro listing dataset (matched listing <-> prior purchase)
#    Listings observed during the downturn window 2022Q1..2024Q4.
# ---------------------------------------------------------------------------
N = 1_200_000
# assign listings to cities proportional to size by tier
w = np.array([ {1:6.0,2:2.2,3:1.0}[tier_of[c]] for c in cities ])
w = w/w.sum()
city_id = rng.choice(len(cities), size=N, p=w)
tier_arr = np.array([tier_of[cities[i]] for i in city_id])

# listing quarter within 2022Q1..2024Q4 (obs window), weighted toward later
obs_start = list(QS).index(pd.Period("2022Q1","Q"))
obs_qs = np.arange(obs_start, NQ)
obs_w = np.linspace(0.6, 1.4, len(obs_qs)); obs_w/=obs_w.sum()
list_q = rng.choice(obs_qs, size=N, p=obs_w)

# purchase quarter: earlier than listing; sellers who bought near peak (2020-2021)
# are over-represented (they list to exit). Mixture.
def draw_purchase_q(lq):
    # candidate purchase quarters 2015Q1.. up to lq-8 (>=2yr hold typical)
    out = np.empty(len(lq), dtype=int)
    for i,l in enumerate(lq):
        hi = max(4, l-8)
        # weight: bump around peak (2020Q1..2021Q4)
        cand = np.arange(0, hi)
        base = np.ones(len(cand))
        # over-weight 2019Q4..2021Q4 (indices ~19..27)
        for j,q in enumerate(cand):
            if 19 <= q <= 27: base[j]*=3.2
            elif 12 <= q <= 18: base[j]*=1.6
        base/=base.sum()
        out[i]=rng.choice(cand, p=base)
    return out
# vectorized-ish: precompute weights per listing-quarter bucket for speed
buy_q = np.empty(N, dtype=int)
for lq in np.unique(list_q):
    mask = list_q==lq
    hi = max(4, lq-8)
    cand = np.arange(0, hi)
    base = np.ones(len(cand))
    base[(cand>=19)&(cand<=27)] *= 3.2
    base[(cand>=12)&(cand<=18)] *= 1.6
    base/=base.sum()
    buy_q[mask] = rng.choice(cand, size=mask.sum(), p=base)

# unit size (sqm) and persistent quality effect
size = np.clip(rng.lognormal(mean=np.log(89), sigma=0.33, size=N), 30, 400)
quality = np.exp(rng.normal(0, 0.18, size=N))          # persistent unit quality
u_buy = np.exp(rng.normal(0, 0.07, size=N))            # transitory noise at purchase
u_now = np.exp(rng.normal(0, 0.07, size=N))            # transitory noise now

idx_buy = np.array([city_index[cities[city_id[i]]][buy_q[i]] for i in range(N)])
idx_now = np.array([city_index[cities[city_id[i]]][list_q[i]] for i in range(N)])

price_psm_buy = idx_buy * quality * u_buy * 90       # scale to yuan/sqm-ish (x100)
V_psm         = idx_now * quality * u_now * 90        # current market value psm
P_purchase = price_psm_buy * size
V          = V_psm * size

# potential loss relative to current value
loss_over_V = (P_purchase - V)/V                 # >0 = underwater (paper loss)
underwater  = loss_over_V > 0
loss_pos    = np.clip(loss_over_V, 0, None)      # loss magnitude over V (>=0)
gain_neg    = np.clip(loss_over_V, None, 0)      # gain side (<=0)

# ---------------------------------------------------------------------------
# 3. Behavioural listing price (reference dependence + bunching)
# ---------------------------------------------------------------------------
GAMMA = 0.22          # loss-aversion pass-through (continuous part)
GAMMA_GAIN = 0.05     # gains passed through much less
m0 = rng.normal(0.045, 0.02, size=N)     # base bargaining markup over value
noise_m = rng.normal(0, 0.035, size=N)

markup = m0 + GAMMA*loss_pos + GAMMA_GAIN*(-gain_neg)*(-1) + noise_m
# note gain_neg<=0; sellers with gains shave a little: add GAMMA_GAIN*gain_neg (negative)
markup = m0 + GAMMA*loss_pos + GAMMA_GAIN*gain_neg + noise_m

# Bunching: a share of underwater sellers anchor list price EXACTLY at purchase
# price -> markup = loss_over_V. Share rises with being underwater.
phi = 0.14
anchor = underwater & (rng.random(N) < phi)
markup = np.where(anchor, loss_over_V + rng.normal(0,0.006,N), markup)
markup = np.clip(markup, -0.15, 1.2)

P_list = V*(1+markup)
list_over_purchase = P_list / P_purchase     # ratio; bunching spike at 1.0

# ---------------------------------------------------------------------------
# 4. Sale outcome: monthly hazard decreasing in markup (liquidity)
# ---------------------------------------------------------------------------
# baseline monthly log-odds; higher markup and weaker city lower hazard
a0 = -2.30
b_markup = -9.5
b_tier = np.array([0.0,0.0,-0.12,-0.24])[tier_arr]  # weaker cities slower
hz_noise = rng.normal(0, 0.22, size=N)
lin = a0 + b_markup*markup + b_tier + hz_noise
h_month = 1/(1+np.exp(-lin))
h_month = np.clip(h_month, 0.002, 0.9)
# time on market via geometric; observation censoring at 12 months
TOM = rng.geometric(h_month)          # months to sale (uncensored)
sold = TOM <= 12
TOM_obs = np.minimum(TOM, 12)
withdrawn = (~sold) & (rng.random(N) < 0.45)

df = pd.DataFrame({
    "city": [cities[i] for i in city_id],
    "tier": tier_arr,
    "size": size,
    "buy_q": buy_q, "list_q": list_q,
    "P_purchase": P_purchase, "V": V, "P_list": P_list,
    "loss_over_V": loss_over_V, "underwater": underwater,
    "markup": markup, "list_over_purchase": list_over_purchase,
    "h_month": h_month, "TOM": TOM_obs, "sold": sold, "withdrawn": withdrawn,
})
df.to_pickle(os.path.join(OUT,"micro.pkl"))
np.savez_compressed(os.path.join(OUT,"components.npz"),
    city_id=city_id, tier=tier_arr, size=size, buy_q=buy_q, list_q=list_q,
    P_purchase=P_purchase, V=V, P_list=P_list, loss_over_V=loss_over_V,
    loss_pos=loss_pos, gain_neg=gain_neg, m0=m0, markup=markup, anchor=anchor,
    noise_m=noise_m, hz_noise=hz_noise, b_tier=b_tier,
    h_month=h_month, sold=sold.astype(int), TOM=TOM_obs, withdrawn=withdrawn.astype(int),
    a0=a0, b_markup=b_markup, GAMMA=GAMMA, GAMMA_GAIN=GAMMA_GAIN)
# persist city index paths + declines
np.savez_compressed(os.path.join(OUT,"cityidx.npz"),
    idx=np.array([city_index[c] for c in cities]),
    decline=np.array([city_decline[c] for c in cities]),
    tier=np.array([tier_of[c] for c in cities]))
with open(os.path.join(OUT,"cities.json"),"w") as f:
    json.dump({"cities":cities,"tier_of":tier_of,
               "quarters":[str(q) for q in QS],"peak_idx":int(PEAK)}, f)
print("simulated micro rows:", len(df))
print("share underwater:", underwater.mean().round(4))
print("mean markup underwater vs not:", markup[underwater].mean().round(4), markup[~underwater].mean().round(4))
print("mean TOM sold:", TOM_obs[sold].mean().round(2), "overall sale rate:", sold.mean().round(4))
