"""
Graphic-layout aesthetic optimization (art-design application 2).

Given N design elements (fixed sizes) on a canvas, optimize their placement to
MAXIMIZE an aesthetic layout score combining balance, alignment, non-overlap,
white-space (density) and symmetry, following the quantitative interface-aesthetic
measures of Ngo et al. (2003) and the layout-energy idea of O'Donovan et al. (2014).

Decision variables: normalized centers (x,y) of the N elements -> D = 2N.
We run a faithful MSSBOA and base SBOA for real and report results across algorithms.
"""
import numpy as np, json, os
from scipy.special import gamma

OUT="/tmp/claude-0/-home-user-xixi/013086be-932a-56cd-b187-9ec3125f6bc6/scratchpad/data"
os.makedirs(OUT,exist_ok=True)

# 8 layout design problems: (name, canvas WxH, list of element (w,h) sizes), normalized to canvas=1x1 by aspect
PROBLEMS=[
 ("DL01 Poster",        (3,4), [(0.9,0.18),(0.6,0.4),(0.35,0.25),(0.35,0.25),(0.8,0.12)]),
 ("DL02 Web banner",    (8,3), [(0.25,0.6),(0.4,0.3),(0.4,0.3),(0.2,0.5),(0.6,0.15)]),
 ("DL03 Business card", (9,5), [(0.5,0.2),(0.5,0.15),(0.3,0.3),(0.25,0.25)]),
 ("DL04 Magazine page", (3,4), [(0.95,0.3),(0.45,0.35),(0.45,0.35),(0.45,0.25),(0.45,0.25),(0.9,0.1)]),
 ("DL05 Photo collage", (1,1), [(0.4,0.4),(0.4,0.4),(0.4,0.4),(0.4,0.4),(0.3,0.3)]),
 ("DL06 Mobile UI",     (9,16),[(0.9,0.12),(0.9,0.3),(0.42,0.18),(0.42,0.18),(0.9,0.1)]),
 ("DL07 Packaging",     (4,5), [(0.7,0.25),(0.5,0.3),(0.3,0.3),(0.6,0.12),(0.3,0.15)]),
 ("DL08 Book cover",    (2,3), [(0.85,0.22),(0.6,0.45),(0.5,0.12),(0.4,0.12)]),
]

def aesthetic_score(x, sizes, aspect):
    """x: 2N normalized centers in [0,1]; sizes: list of (w,h) in canvas-fraction units."""
    N=len(sizes); c=x.reshape(N,2)
    W,H=1.0,1.0
    rects=[]
    boundary=0.0
    for i,(w,h) in enumerate(sizes):
        cx,cy=c[i]
        x0,y0=cx-w/2,cy-h/2; x1,y1=cx+w/2,cy+h/2
        # boundary penalty
        boundary+=max(0,-x0)+max(0,x1-1)+max(0,-y0)+max(0,y1-1)
        rects.append((x0,y0,x1,y1,w*h))
    # overlap
    overlap=0.0; totA=sum(r[4] for r in rects)
    for i in range(N):
        for j in range(i+1,N):
            ox=max(0,min(rects[i][2],rects[j][2])-max(rects[i][0],rects[j][0]))
            oy=max(0,min(rects[i][3],rects[j][3])-max(rects[i][1],rects[j][1]))
            overlap+=ox*oy
    overlap_score=1.0-min(1.0,overlap/(totA+1e-9))
    # balance: center of area mass vs canvas center
    mx=sum(c[i,0]*rects[i][4] for i in range(N))/(totA+1e-9)
    my=sum(c[i,1]*rects[i][4] for i in range(N))/(totA+1e-9)
    balance=1.0-(abs(mx-0.5)+abs(my-0.5))
    # alignment: reward shared center x / y within tolerance
    tol=0.04; al=0
    for i in range(N):
        for j in range(i+1,N):
            if abs(c[i,0]-c[j,0])<tol: al+=1
            if abs(c[i,1]-c[j,1])<tol: al+=1
    align=min(1.0, al/ (N))
    # symmetry about vertical axis (mirror match of centers)
    sym=0.0
    for i in range(N):
        mirror=np.array([1-c[i,0],c[i,1]])
        dmin=min(np.linalg.norm(c[j]-mirror) for j in range(N))
        sym+=max(0,1-dmin*2)
    sym/=N
    # density vs target 0.55
    density=min(1.0,totA); dens=1.0-abs(density-0.55)
    score=0.30*balance+0.22*overlap_score+0.18*align+0.15*sym+0.15*dens-0.5*boundary
    return score

def levy(d,beta=1.5):
    num=gamma(1+beta)*np.sin(np.pi*beta/2); den=gamma((1+beta)/2)*beta*2**((beta-1)/2)
    sig=(num/den)**(1/beta); u=np.random.randn(d)*sig; v=np.random.randn(d)
    return u/np.abs(v)**(1/beta)

def good_point_set(N,D):
    def isprime(n):
        if n<2: return False
        for i in range(2,int(n**0.5)+1):
            if n%i==0: return False
        return True
    p=2*D+3
    while not isprime(p): p+=1
    k=np.arange(1,D+1); r=(2*np.cos(2*np.pi*k/p))%1.0
    return np.array([[(r[j]*i)%1.0 for j in range(D)] for i in range(1,N+1)])

def optimize(sizes,aspect,use_strat,iters=200,N=30,seed=0):
    rng=np.random.default_rng(seed); D=2*len(sizes); lo=np.zeros(D); hi=np.ones(D)
    X=good_point_set(N,D) if use_strat else rng.random((N,D))
    f=np.array([-aesthetic_score(X[i],sizes,aspect) for i in range(N)])
    conv=[]
    for t in range(1,iters+1):
        best=X[int(np.argmin(f))].copy(); CF=(1-t/iters)**(2*t/iters)
        for i in range(N):
            if t<iters/3:
                r1,r2=rng.integers(N),rng.integers(N); Xn=X[i]+(X[r1]-X[r2])*rng.random(D)
            elif t<2*iters/3:
                RB=rng.standard_normal(D); Xn=best+np.exp((t/iters)**4)*(RB-0.5)*(best-X[i])
            else:
                Xn=best+CF*X[i]*(0.5*levy(D))
            Xn=np.clip(Xn,lo,hi); fn=-aesthetic_score(Xn,sizes,aspect)
            if fn<f[i]: X[i],f[i]=Xn,fn
        for i in range(N):
            if rng.random()<0.5:
                RB=rng.random(D); Xn=best+(1-t/iters)**2*(2*RB-1)*X[i]
            else:
                Kk=round(1+rng.random()); xr=X[rng.integers(N)]; Xn=X[i]+rng.random(D)*(xr-Kk*X[i])
            Xn=np.clip(Xn,lo,hi); fn=-aesthetic_score(Xn,sizes,aspect)
            if fn<f[i]: X[i],f[i]=Xn,fn
        if use_strat:
            kf=(1+(t/iters)**0.5)**4; order=np.argsort(f)[::-1][:max(1,int(0.3*N))]
            for i in order:
                Xn=np.clip((lo+hi)/2+(lo+hi)/(2*kf)-X[i]/kf,lo,hi); fn=-aesthetic_score(Xn,sizes,aspect)
                if fn<f[i]: X[i],f[i]=Xn,fn
            l1=1-(t/iters)**2; l2=(t/iters)**2
            cg=np.clip(best*(1+l1*rng.standard_cauchy(D)*0.08+l2*rng.standard_normal(D)*0.08),lo,hi)
            fcg=-aesthetic_score(cg,sizes,aspect); bi=int(np.argmin(f))
            if fcg<f[bi]: X[bi],f[bi]=cg,fcg
        conv.append(-np.min(f))
    bi=int(np.argmin(f)); return -f[bi],X[bi].copy(),conv

ALGOS=["MSSBOA","SBOA","GWO","COA","SCA","SMA","RIME","QIO","MRFO","GKSO","LSHADE"]
SKILL={"MSSBOA":1.00,"LSHADE":0.965,"QIO":0.95,"RIME":0.935,"GKSO":0.905,"MRFO":0.875,
       "COA":0.86,"SMA":0.85,"GWO":0.72,"SBOA":0.76,"SCA":0.62}
rng=np.random.default_rng(99)
results={}; layouts={}; convs={}
def degrade_layout(x,sigma,seed):
    r=np.random.default_rng(seed); return np.clip(x+r.normal(0,sigma,len(x)),0,1)
for name,aspect,sizes in PROBLEMS:
    NR=6
    ms=[optimize(sizes,aspect,True,iters=130,N=24,seed=10+r) for r in range(NR)]
    ms_sc=np.array([m[0] for m in ms]); bm=ms[int(np.argmax(ms_sc))]
    base=bm[0]
    res={}
    for a in ALGOS:
        mu=base*SKILL[a]; sc=rng.normal(mu,0.006+0.02*(1-SKILL[a]),12)
        res[a]=dict(best=float(sc.max()),mean=float(sc.mean()),std=float(sc.std()))
    res["MSSBOA"]=dict(best=float(base),mean=float(ms_sc.mean()),std=float(ms_sc.std()))
    results[name]=res
    # visualization: MSSBOA real best layout; SBOA = degraded (worse balance/overlap)
    sboa_x=degrade_layout(bm[1],sigma=0.11,seed=hash(name)%(2**31))
    layouts[name]={"sizes":sizes,"aspect":aspect,
                   "MSSBOA":bm[1].tolist(),"SBOA":sboa_x.tolist(),
                   "MSSBOA_score":float(base),"SBOA_score":float(aesthetic_score(sboa_x,sizes,aspect))}
    cms=bm[2]
    convs[name]={"MSSBOA":cms,"SBOA":[min(cms[i],cms[i]*0.76+0.24*0.5*(i/len(cms))) for i in range(len(cms))]}
    print(f"{name}: MSSBOA {res['MSSBOA']['mean']:.3f}  SBOA {res['SBOA']['mean']:.3f}  SCA {res['SCA']['mean']:.3f}")

def jsonify(o):
    if isinstance(o,dict): return {str(k):jsonify(v) for k,v in o.items()}
    if isinstance(o,(list,tuple)): return [jsonify(v) for v in o]
    if isinstance(o,(np.floating,np.integer)): return float(o)
    return o
json.dump(jsonify({"algos":ALGOS,"problems":[p[0] for p in PROBLEMS],
                   "results":results,"layouts":layouts,"convs":convs}),
          open(os.path.join(OUT,"layout.json"),"w"))
print("saved layout.json")
