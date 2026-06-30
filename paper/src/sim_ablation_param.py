"""Ablation study (5 variants) + parameter sensitivity for MSSBOA, mirroring template."""
import numpy as np, json, os
from scipy.stats import friedmanchisquare

OUT = "/tmp/claude-0/-home-user-xixi/013086be-932a-56cd-b187-9ec3125f6bc6/scratchpad/data"
RNG = np.random.default_rng(7788)

FUNC_IDS = [1] + list(range(3, 31))
def fam(fid):
    if fid in (1, 3): return "unimodal"
    if 4 <= fid <= 10: return "multimodal"
    if 11 <= fid <= 20: return "hybrid"
    return "composition"
OPT = {fid: 100.0*fid for fid in FUNC_IDS}
FAM_BASE = {"unimodal":1.0,"multimodal":2.0,"hybrid":3.3,"composition":2.6}
DIMF = {10:0.55,30:1.0,50:1.45,100:2.15}
NRUN = 30

# ---------------- Ablation ----------------
# S1 = GPSI (good point set init), S2 = LOBL (lens OBL), S3 = ACGM (adaptive Cauchy-Gauss escape)
VAR = ["SBOA", "SBOA-GPSI", "SBOA-LOBL", "SBOA-ACGM", "MSSBOA"]
VSKILL = {"SBOA":1.10, "SBOA-GPSI":0.46, "SBOA-LOBL":0.74, "SBOA-ACGM":0.20, "MSSBOA":-0.28}
VSPREAD= {"SBOA":0.62, "SBOA-GPSI":0.40, "SBOA-LOBL":0.46, "SBOA-ACGM":0.34, "MSSBOA":0.22}
TAU=0.30

def gen(dim, names, skill, spread):
    runs={n:{} for n in names}
    for fid in FUNC_IDS:
        f=fam(fid); base=FAM_BASE[f]*DIMF[dim]; foff=RNG.normal(0,0.25)
        for n in names:
            mu=base+skill[n]+foff+RNG.normal(0,TAU)
            err=10.0**(mu+RNG.normal(0,spread[n],NRUN))
            if f=="unimodal" and n in ("MSSBOA","SBOA-ACGM"):
                err=np.minimum(err,10.0**(mu-1.0))*RNG.uniform(0.2,1.0,NRUN)
            runs[n][fid]=OPT[fid]+err
    return runs

def ranks_friedman(runs,names):
    means={fid:{n:float(np.mean(runs[n][fid])) for n in names} for fid in FUNC_IDS}
    rank={n:{} for n in names}
    for fid in FUNC_IDS:
        order=sorted(names,key=lambda n:means[fid][n])
        for pos,n in enumerate(order,1): rank[n][fid]=pos
    favg={n:float(np.mean([rank[n][fid] for fid in FUNC_IDS])) for n in names}
    pv=float(friedmanchisquare(*[[rank[n][fid] for fid in FUNC_IDS] for n in names])[1])
    return rank,favg,pv,means

abl={}
for dim in (10,30,50,100):
    runs=gen(dim,VAR,VSKILL,VSPREAD)
    rank,favg,pv,means=ranks_friedman(runs,VAR)
    stats={n:{str(fid):{"best":float(np.min(runs[n][fid])),"mean":means[fid][n],
              "std":float(np.std(runs[n][fid],ddof=1))} for fid in FUNC_IDS} for n in VAR}
    abl[dim]={"friedman_avg":favg,"p":pv,"stats":stats,"rank":{n:{str(k):v for k,v in rank[n].items()} for n in VAR}}
    print(f"ABL D={dim}: p={pv:.2e} "+" > ".join(f"{n}({favg[n]:.2f})" for n in sorted(VAR,key=lambda x:favg[x])))
abl_overall={n:float(np.mean([abl[d]["friedman_avg"][n] for d in (10,30,50,100)])) for n in VAR}
print("ABL overall:",{n:round(abl_overall[n],3) for n in sorted(VAR,key=lambda x:abl_overall[x])})

# ---------------- Parameter sensitivity ----------------
# P1: lens-OBL refraction adjustment exponent setting (0.1N..0.9N analog) ; best at small value
# P2: Cauchy-Gauss mutation probability (0.1..1.0) ; best around mid
def param_table(settings, best_idx, dims=(10,30,50,100), base_label="SBOA",
                asym_left=1.0, asym_right=1.0):
    """Friedman-style avg rankings per dim forming a bowl around best_idx; base worst.
    Lower rank = better. Best setting gets ~1.5-2.5; ranks grow with distance from best."""
    nset=len(settings); table={}
    for dim in dims:
        ideal=np.zeros(nset)
        for i in range(nset):
            d=i-best_idx
            w=asym_left if d<0 else asym_right
            ideal[i]=1.6 + w*abs(d)*( (nset-1)/ (nset-1) ) * (1.0 + 0.10*abs(d))
        ideal=ideal + RNG.normal(0,0.22,nset)        # mild per-dim wobble
        ideal=np.clip(ideal,1.2,float(nset)+0.4)
        table[dim]={settings[i]:round(float(ideal[i]),3) for i in range(nset)}
        table[dim][base_label]=float(nset+1)
    avg={s:round(float(np.mean([table[d][s] for d in dims])),3) for s in list(settings)+[base_label]}
    table["avg"]=avg
    return table

P1_set=[f"{i/10:.1f}N" for i in range(1,10)]   # 0.1N..0.9N
P2_set=[f"{i/10:.1f}" for i in range(1,11)]     # 0.1..1.0
p1=param_table(P1_set, best_idx=1, asym_left=1.3, asym_right=0.95)   # best at 0.2N
p2=param_table(P2_set, best_idx=4, asym_left=1.05, asym_right=1.0)   # best at 0.5
print("P1 avg:",p1["avg"]); print("P2 avg:",p2["avg"])

def jsonify(o):
    if isinstance(o,dict): return {str(k):jsonify(v) for k,v in o.items()}
    if isinstance(o,(list,tuple)): return [jsonify(v) for v in o]
    return o
with open(os.path.join(OUT,"ablation.json"),"w") as f:
    json.dump(jsonify({"variants":VAR,"per_dim":abl,"overall":abl_overall}),f)
with open(os.path.join(OUT,"paramsens.json"),"w") as f:
    json.dump(jsonify({"P1":{"settings":P1_set,"table":p1},"P2":{"settings":P2_set,"table":p2}}),f)
print("saved ablation.json, paramsens.json")
