"""Schematic diagrams: Fig 1 taxonomy, Fig 2 lens-OBL, Fig 3 MSSBOA flowchart."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Polygon, Ellipse
import numpy as np

FIG="/tmp/claude-0/-home-user-xixi/013086be-932a-56cd-b187-9ec3125f6bc6/scratchpad/figs"
os.makedirs(FIG,exist_ok=True)
plt.rcParams.update({"font.family":"serif","font.serif":["DejaVu Serif","Liberation Serif"],
                     "savefig.dpi":320,"font.size":10})

def box(ax,x,y,w,h,text,fc="#e8f0fe",ec="#2b5797",fs=9,bold=False,rounded=0.02):
    p=FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle=f"round,pad=0.01,rounding_size={rounded}",
                     fc=fc,ec=ec,lw=1.3)
    ax.add_patch(p)
    ax.text(x,y,text,ha="center",va="center",fontsize=fs,wrap=True,
            fontweight="bold" if bold else "normal")

def arrow(ax,x1,y1,x2,y2,style="-|>",color="#444",lw=1.3,rad=0.0):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle=style,mutation_scale=12,
                 color=color,lw=lw,connectionstyle=f"arc3,rad={rad}"))

# ---------------- Figure 1: taxonomy ----------------
fig,ax=plt.subplots(figsize=(11,6.2)); ax.set_xlim(0,11); ax.set_ylim(0,6.2); ax.axis("off")
box(ax,5.5,5.7,4.0,0.7,"Metaheuristic Algorithms",fc="#2b5797",ec="#1b3a6b",fs=12,bold=True)
ax.text(5.5,5.7,"",color="white")
# recolor title text white
ax.texts[-1]
cats=[("Evolution-based\nalgorithms","#fde7e9","#c0392b",["Genetic Algorithm (GA)","Differential Evolution (DE)","CMA-ES","Human Evolutionary (HEOA)"]),
      ("Physics-based\nalgorithms","#e8f8ef","#1e8449",["Multi-Verse Optimizer (MVO)","Snow Ablation (SAO)","RIME","Kepler Opt. (KOA)"]),
      ("Mathematics-based\nalgorithms","#fef5e7","#b9770e",["Sine Cosine (SCA)","Arithmetic Opt. (AOA)","Weighted Average (WAA)","TTAO"]),
      ("Swarm-based\nalgorithms","#eaf2fb","#2471a3",["Particle Swarm (PSO)","Grey Wolf (GWO)","Crayfish (COA)","Secretary Bird (SBOA)"])]
xs=[1.6,4.2,6.8,9.4]
for (title,fc,ec,items),x in zip(cats,xs):
    box(ax,x,4.4,2.1,0.85,title,fc=fc,ec=ec,fs=9.5,bold=True)
    arrow(ax,5.5,5.35,x,4.85)
    for i,it in enumerate(items):
        box(ax,x,3.5-i*0.62,2.1,0.5,it,fc="white",ec=ec,fs=7.6)
        if i==0: arrow(ax,x,3.98,x,3.76)
        else: arrow(ax,x,3.5-(i-1)*0.62-0.25,x,3.5-i*0.62+0.25)
# make title text white
for t in ax.texts:
    if t.get_text()=="Metaheuristic Algorithms": t.set_color("white")
fig.tight_layout(); fig.savefig(os.path.join(FIG,"fig01_taxonomy.png"),bbox_inches="tight"); plt.close(fig); print("fig01 done")

# ---------------- Figure 2: lens opposition-based learning ----------------
fig,ax=plt.subplots(figsize=(8.5,4.6)); ax.set_xlim(0,10); ax.set_ylim(0,5.4); ax.axis("off")
# optical axis (search interval [lb,ub])
lb,ub=1.0,9.0; axis_y=1.2
ax.annotate("",xy=(ub+0.4,axis_y),xytext=(lb-0.4,axis_y),arrowprops=dict(arrowstyle="-|>",lw=1.4))
ax.text(lb,axis_y-0.35,"$lb$",ha="center",fontsize=11); ax.text(ub,axis_y-0.35,"$ub$",ha="center",fontsize=11)
ax.plot([lb,lb],[axis_y-0.12,axis_y+0.12],"k-"); ax.plot([ub,ub],[axis_y-0.12,axis_y+0.12],"k-")
base=(lb+ub)/2
ax.plot([base,base],[axis_y-0.12,axis_y+0.12],"k-"); ax.text(base,axis_y-0.35,r"$O=\frac{lb+ub}{2}$",ha="center",fontsize=10)
# convex lens at base
lens=Ellipse((base,3.0),0.5,2.2,fc="#cfe2ff",ec="#2b5797",lw=1.5,alpha=0.8); ax.add_patch(lens)
ax.plot([base,base],[1.7,4.3],color="#2b5797",lw=0.8,ls=":")
# object (candidate x) -> image (lens-reverse x*)
x=3.0; xstar=base+(base-x)  # symmetric for k=1 illustration
hx=1.7
ax.annotate("",xy=(x,axis_y+0.05),xytext=(x,axis_y+hx),arrowprops=dict(arrowstyle="-|>",color="#c0392b",lw=2))
ax.text(x,axis_y+hx+0.2,"object  $x$  (current)",ha="center",color="#c0392b",fontsize=9)
ax.annotate("",xy=(xstar,axis_y-0.05),xytext=(xstar,axis_y-hx*0.55),arrowprops=dict(arrowstyle="-|>",color="#1e8449",lw=2))
ax.text(xstar,axis_y-hx*0.55-0.25,"image  $x^{*}$  (lens-opposite)",ha="center",color="#1e8449",fontsize=9)
# rays through lens
ax.plot([x,base],[axis_y+hx,3.0],color="#888",lw=0.9)
ax.plot([base,xstar],[3.0,axis_y-hx*0.55],color="#888",lw=0.9)
ax.plot([x,xstar],[axis_y+hx,axis_y+hx],color="none")
ax.text(5.0,4.7,"Lens (refraction) opposition-based learning",ha="center",fontsize=12,fontweight="bold")
ax.text(5.0,0.35,r"$x^{*}=\frac{lb+ub}{2}+\frac{lb+ub}{2k}-\frac{x}{k}$",ha="center",fontsize=12)
fig.tight_layout(); fig.savefig(os.path.join(FIG,"fig02_lensobl.png"),bbox_inches="tight"); plt.close(fig); print("fig02 done")

# ---------------- Figure 3: MSSBOA flowchart ----------------
fig,ax=plt.subplots(figsize=(7.6,10.6)); ax.set_xlim(0,8); ax.set_ylim(0,15.5); ax.axis("off")
def fbox(y,text,fc="#e8f0fe",ec="#2b5797",w=4.6,h=0.78,x=4,fs=9.2,bold=False):
    box(ax,x,y,w,h,text,fc=fc,ec=ec,fs=fs,bold=bold); return y
def diamond(x,y,w,h,text,fc="#fff3cd",ec="#b9770e",fs=8.8):
    ax.add_patch(Polygon([(x,y+h/2),(x+w/2,y),(x,y-h/2),(x-w/2,y)],closed=True,fc=fc,ec=ec,lw=1.3))
    ax.text(x,y,text,ha="center",va="center",fontsize=fs)
ys=15.0
fbox(15.0,"Start",fc="#d5f5e3",ec="#1e8449",w=2.0,h=0.6,bold=True)
fbox(13.95,"Good Point Set initialization of population $X$ (S1)\nset $FEs=0$, $FEs_{max}$",h=0.95)
fbox(12.75,"Evaluate fitness of $X$; record best $X_{best}$")
diamond(4,11.55,3.2,1.0,"$FEs < FEs_{max}$ ?")
fbox(10.2,"Compute time ratio $t/T$ (current/maximum FEs)",h=0.7)
diamond(4,8.95,3.6,1.3,"exploration\nor exploitation\nphase?")
# two branches
box(ax,1.9,7.2,2.7,1.05,"Hunting strategy\n(3-stage: search /\nconsume / attack snake)",fc="#fde7e9",ec="#c0392b",fs=8.4)
box(ax,6.1,7.2,2.7,1.05,"Escape strategy\n(C1 camouflage /\nC2 flee, with\nLevy flight)",fc="#fde7e9",ec="#c0392b",fs=8.4)
fbox(5.7,"Lens opposition-based learning on inferior birds (S2)",fc="#e8f8ef",ec="#1e8449",h=0.7,fs=8.8)
fbox(4.7,"Adaptive Cauchy-Gauss mutation on $X_{best}$ (S3)",fc="#e8f8ef",ec="#1e8449",h=0.7,fs=8.8)
fbox(3.65,"Greedy selection; update $X$, $X_{best}$; $FEs$ increase",h=0.7)
fbox(2.6,"Update best-so-far solution")
# loop back & end
diamondless=2.6
fbox(1.0,"Output the best solution $X_{best}$",fc="#d5f5e3",ec="#1e8449",w=3.4,bold=True)
# arrows
arrow(ax,4,14.7,4,14.42)
arrow(ax,4,13.47,4,13.14)
arrow(ax,4,12.36,4,12.05)
arrow(ax,4,11.05,4,10.55); ax.text(4.2,10.78,"Yes",fontsize=8,color="#1e8449")
arrow(ax,4,9.85,4,9.6)
# branch arrows from phase diamond
arrow(ax,2.6,8.95,1.9,7.72); ax.text(2.0,8.5,"explore",fontsize=7.5)
arrow(ax,5.4,8.95,6.1,7.72); ax.text(6.0,8.5,"exploit",fontsize=7.5)
arrow(ax,1.9,6.68,3.0,6.05); arrow(ax,6.1,6.68,5.0,6.05)
arrow(ax,4,5.35,4,5.05)
arrow(ax,4,4.35,4,4.0)
arrow(ax,4,3.3,4,2.98)
# loop back to while
arrow(ax,6.3,2.6,7.4,2.6,style="-|>"); ax.add_patch(FancyArrowPatch((7.4,2.6),(7.4,11.55),arrowstyle="-",color="#444",lw=1.3))
arrow(ax,7.4,11.55,5.6,11.55)
ax.text(7.5,7.0,"loop",rotation=90,fontsize=8,color="#444")
# No -> end
arrow(ax,2.4,11.55,1.0,11.55); ax.text(1.5,11.8,"No",fontsize=8,color="#c0392b")
ax.add_patch(FancyArrowPatch((1.0,11.55),(1.0,1.4),arrowstyle="-",color="#444",lw=1.3))
arrow(ax,1.0,1.4,2.3,1.0)
fig.tight_layout(); fig.savefig(os.path.join(FIG,"fig03_flowchart.png"),bbox_inches="tight"); plt.close(fig); print("fig03 done")
print("DIAGRAMS DONE")
