"""Clean, academic, template-consistent schematic diagrams:
Fig 1 taxonomy, Fig 2 lens-OBL, Fig 3 MSSBOA flowchart.
Design goals: restrained muted palette, thin borders, orthogonal connectors with
neat arrowheads, generous margins (nothing clipped / overflowing the frame)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon, Ellipse, PathPatch
from matplotlib.path import Path
import numpy as np

FIG="/tmp/claude-0/-home-user-xixi/013086be-932a-56cd-b187-9ec3125f6bc6/scratchpad/figs"
os.makedirs(FIG,exist_ok=True)
plt.rcParams.update({"font.family":"serif","font.serif":["DejaVu Serif","Liberation Serif"],
                     "savefig.dpi":340,"font.size":10})

INK="#2b2b2b"; LINE="#555555"
# restrained muted palette (consistent with the data figures)
NAVY="#33527a"; RED="#b4524e"; GREEN="#4f8a5b"; GOLD="#bf9233"; BLUE="#3e74a8"
def tint(hexc, a):  # light fill tint of a hex color
    import matplotlib.colors as mc
    r,g,b=mc.to_rgb(hexc); return (r+(1-r)*(1-a), g+(1-g)*(1-a), b+(1-b)*(1-a))

def rbox(ax,x,y,w,h,text,fc="white",ec=NAVY,fs=9,bold=False,tc=INK,lw=1.2,pad=0.014,round=0.018):
    p=FancyBboxPatch((x-w/2,y-h/2),w,h,
        boxstyle=f"round,pad={pad},rounding_size={round}",
        fc=fc,ec=ec,lw=lw,clip_on=False,zorder=3)
    ax.add_patch(p)
    ax.text(x,y,text,ha="center",va="center",fontsize=fs,color=tc,
            fontweight="bold" if bold else "normal",zorder=4,clip_on=False,
            linespacing=1.25)

def diamond(ax,x,y,w,h,text,fc="white",ec=GOLD,fs=8.6,tc=INK):
    ax.add_patch(Polygon([(x,y+h/2),(x+w/2,y),(x,y-h/2),(x-w/2,y)],closed=True,
        fc=fc,ec=ec,lw=1.2,clip_on=False,zorder=3))
    ax.text(x,y,text,ha="center",va="center",fontsize=fs,color=tc,zorder=4,clip_on=False,linespacing=1.2)

def arrow(ax,p0,p1,color=LINE,lw=1.3,style="-|>"):
    ax.add_patch(FancyArrowPatch(p0,p1,arrowstyle=style,mutation_scale=12,
        color=color,lw=lw,shrinkA=0,shrinkB=0,clip_on=False,zorder=2,
        joinstyle="miter",capstyle="butt"))

def elbow(ax,pts,color=LINE,lw=1.3,head=True):
    """orthogonal polyline through pts; neat arrowhead on final segment."""
    for i in range(len(pts)-2):
        ax.plot([pts[i][0],pts[i+1][0]],[pts[i][1],pts[i+1][1]],color=color,lw=lw,
                solid_capstyle="round",clip_on=False,zorder=2)
    if head:
        arrow(ax,pts[-2],pts[-1],color=color,lw=lw)
    else:
        ax.plot([pts[-2][0],pts[-1][0]],[pts[-2][1],pts[-1][1]],color=color,lw=lw,clip_on=False,zorder=2)

# ============================ Figure 1: taxonomy ============================
def fig1():
    W,H=12.0,7.4
    fig,ax=plt.subplots(figsize=(11.6,5.7)); ax.set_xlim(0,W); ax.set_ylim(1.95,7.4); ax.axis("off")
    # title
    tx,ty=W/2,6.9; tw,th=4.6,0.72
    rbox(ax,tx,ty,tw,th,"Metaheuristic Algorithms",fc=NAVY,ec=NAVY,fs=13,bold=True,tc="white",round=0.03)
    cats=[("Evolution-based",RED,["Genetic Algorithm (GA)","Differential Evolution (DE)",
                                  "CMA-ES","Human Evolutionary (HEOA)"]),
          ("Physics-based",GREEN,["Multi-Verse Optimizer (MVO)","Snow Ablation (SAO)",
                                  "RIME","Kepler Optimization (KOA)"]),
          ("Mathematics-based",GOLD,["Sine Cosine (SCA)","Arithmetic Opt. (AOA)",
                                     "Weighted Average (WAA)","TTAO"]),
          ("Swarm-based",BLUE,["Particle Swarm (PSO)","Grey Wolf (GWO)",
                               "Crayfish (COA)","Secretary Bird (SBOA)"])]
    xs=[1.65,4.55,7.45,10.35]
    cat_y=5.55; cat_w,cat_h=2.45,0.72
    bus_y=6.18
    for (title,col,_),x in zip(cats,xs):
        rbox(ax,x,cat_y,cat_w,cat_h,title,fc=tint(col,0.22),ec=col,fs=10.5,bold=True,tc=INK,round=0.03)
        elbow(ax,[(tx,ty-th/2),(tx,bus_y),(x,bus_y),(x,cat_y+cat_h/2)],color=LINE,lw=1.2)
    # example boxes stacked under each category
    ex_w,ex_h,gap=2.45,0.62,0.16
    top0=cat_y-cat_h/2-0.42
    for (title,col,items),x in zip(cats,xs):
        # connector from category to the stack
        arrow(ax,(x,cat_y-cat_h/2),(x,top0+ex_h/2+0.0),color=col,lw=1.2)
        for i,it in enumerate(items):
            y=top0-i*(ex_h+gap)
            rbox(ax,x,y,ex_w,ex_h,it,fc="white",ec=col,fs=8.4,tc=INK,lw=1.0,round=0.02)
            if i>0:
                ax.plot([x,x],[y+ex_h/2+gap,y+ex_h/2],color=col,lw=0.9,clip_on=False,zorder=1)
    fig.subplots_adjust(left=0.01,right=0.99,top=0.99,bottom=0.01)
    fig.savefig(os.path.join(FIG,"fig01_taxonomy.png"),bbox_inches="tight",pad_inches=0.08)
    plt.close(fig); print("fig01 done")

# ============================ Figure 2: lens OBL ============================
def fig2():
    fig,ax=plt.subplots(figsize=(8.8,4.7)); ax.set_xlim(0,10); ax.set_ylim(0,5.4); ax.axis("off")
    ax.text(5.0,5.12,"Lens (refraction) opposition-based learning",ha="center",fontsize=12.5,fontweight="bold")
    axis_y=2.05; lb,ub=1.3,8.7; O=(lb+ub)/2
    lens_cy=3.55
    # optical axis with arrowhead
    arrow(ax,(lb-0.5,axis_y),(ub+0.6,axis_y),color=INK,lw=1.4)
    for xx,lab in [(lb,"$lb$"),(O,"$O$"),(ub,"$ub$")]:
        ax.plot([xx,xx],[axis_y-0.14,axis_y+0.14],color=INK,lw=1.2,clip_on=False)
        ax.text(xx,axis_y-0.34,lab,ha="center",va="top",fontsize=11.5)
    # convex lens centred on O (above the axis)
    ax.add_patch(Ellipse((O,lens_cy),0.46,2.3,fc=tint(BLUE,0.30),ec=BLUE,lw=1.5,zorder=2,clip_on=False))
    ax.plot([O,O],[axis_y+0.18,lens_cy+1.35],color=BLUE,lw=0.9,ls=(0,(4,3)),clip_on=False,zorder=1)
    # object (current x) pointing up; image (x*) pointing down
    xo, xi = O-1.95, O+1.55
    arrow(ax,(xo,axis_y),(xo,axis_y+1.55),color=RED,lw=2.1)
    ax.text(xo,axis_y+1.78,"object $x$\n(current)",ha="center",va="bottom",color=RED,fontsize=9.4,linespacing=1.2)
    arrow(ax,(xi,axis_y),(xi,axis_y-1.0),color=GREEN,lw=2.1)
    ax.text(xi+0.28,axis_y-0.62,"image $x^{*}$\n(lens-opposite)",ha="left",va="center",color=GREEN,fontsize=9.4,linespacing=1.2)
    # principal rays through the lens centre
    ax.plot([xo,O],[axis_y+1.55,lens_cy],color=LINE,lw=0.9,clip_on=False,zorder=1)
    ax.plot([O,xi],[lens_cy,axis_y-1.0],color=LINE,lw=0.9,clip_on=False,zorder=1)
    # formula at the bottom, clear of everything
    ax.text(5.0,0.34,r"$x^{*}=\dfrac{lb+ub}{2}+\dfrac{lb+ub}{2k}-\dfrac{x}{k}$",ha="center",va="center",fontsize=13)
    fig.savefig(os.path.join(FIG,"fig02_lensobl.png"),bbox_inches="tight",pad_inches=0.12)
    plt.close(fig); print("fig02 done")

# ============================ Figure 3: flowchart ============================
def fig3():
    fig,ax=plt.subplots(figsize=(7.2,10.6)); ax.set_xlim(0,8.6); ax.set_ylim(0,15.8); ax.axis("off")
    cx=3.8; loop_x=7.7; no_x=0.7
    Gproc=tint(NAVY,0.10); Ginit=tint(GREEN,0.18); Gstrat=tint(GREEN,0.16); Gphase=tint(GOLD,0.22); Gbr=tint(RED,0.14)
    def proc(y,text,fc=Gproc,ec=NAVY,w=5.2,h=0.82,x=cx,fs=9.2,bold=False,tc=INK):
        rbox(ax,x,y,w,h,text,fc=fc,ec=ec,fs=fs,bold=bold,tc=tc); return y
    # --- nodes (top -> bottom) ---
    proc(15.15,"Start",fc=tint(GREEN,0.25),ec=GREEN,w=2.0,h=0.60,bold=True)
    proc(13.95,"Good point set initialization of $X$ (S1);\nset $t=0$, $T$, $N$",fc=Ginit,ec=GREEN,h=1.0)
    proc(12.60,"Evaluate fitness of $X$; record the best $X_{best}$")
    diamond(ax,cx,11.05,3.4,1.05,"$t<T$ ?",fc=Gphase,ec=GOLD,fs=9.4)
    proc(9.55,"Compute the time ratio $t/T$",h=0.74)
    diamond(ax,cx,8.20,3.7,1.25,"exploration or\nexploitation ?",fc=Gphase,ec=GOLD)
    by=6.35                                                  # branch centre y
    rbox(ax,1.95,by,2.85,1.20,"Hunting strategy\n(searching / consuming /\nattacking the snake)",fc=Gbr,ec=RED,fs=8.3)
    rbox(ax,5.65,by,2.85,1.20,"Escape strategy\n($C_1$ camouflage /\n$C_2$ flee with Lévy flight)",fc=Gbr,ec=RED,fs=8.3)
    proc(4.70,"Lens opposition-based learning on the inferior birds (S2)",fc=Gstrat,ec=GREEN,h=0.74,fs=8.8)
    proc(3.70,"Adaptive Cauchy–Gauss mutation on $X_{best}$ (S3)",fc=Gstrat,ec=GREEN,h=0.74,fs=8.8)
    proc(2.70,"Greedy selection; update $X$ and $X_{best}$; $t=t+1$",h=0.74)
    proc(1.05,"Output the best solution $X_{best}$",fc=tint(GREEN,0.25),ec=GREEN,w=3.8,bold=True)
    # --- arrows ---
    arrow(ax,(cx,14.85),(cx,14.47))                          # start -> init
    arrow(ax,(cx,13.45),(cx,13.04))                          # init -> eval
    arrow(ax,(cx,12.19),(cx,11.59))                          # eval -> while
    arrow(ax,(cx,10.525),(cx,9.93)); ax.text(cx+0.2,10.25,"Yes",fontsize=8.2,color=GREEN,va="center")
    arrow(ax,(cx,9.18),(cx,8.83))                            # ratio -> phase
    # phase diamond side vertices: left (cx-1.85,8.20)=(1.95,8.20), right (5.65,8.20)
    arrow(ax,(1.95,8.20),(1.95,by+0.60)); ax.text(2.12,7.55,"explore",fontsize=7.6,va="center")
    arrow(ax,(5.65,8.20),(5.65,by+0.60)); ax.text(5.82,7.55,"exploit",fontsize=7.6,va="center")
    # branches merge down to S2 (top of S2 = 4.70+0.37 = 5.07)
    busy=5.45
    elbow(ax,[(1.95,by-0.60),(1.95,busy),(cx,busy)],color=LINE,head=False)
    elbow(ax,[(5.65,by-0.60),(5.65,busy),(cx,busy)],color=LINE,head=False)
    arrow(ax,(cx,busy),(cx,5.07))                            # bus -> S2
    arrow(ax,(cx,4.33),(cx,4.07))                            # S2 -> S3
    arrow(ax,(cx,3.33),(cx,3.07))                            # S3 -> greedy
    # feedback loop on the right: greedy -> while
    elbow(ax,[(cx+2.6,2.70),(loop_x,2.70),(loop_x,11.05),(cx+1.7,11.05)],color=NAVY,lw=1.25)
    ax.text(loop_x+0.14,6.9,"next iteration",rotation=90,fontsize=8,color=NAVY,va="center")
    # while "No" -> output (left side)
    elbow(ax,[(cx-1.7,11.05),(no_x,11.05),(no_x,1.05),(cx-1.9,1.05)],color=LINE,lw=1.25)
    ax.text(no_x+0.14,11.32,"No",fontsize=8.2,color=RED,va="center")
    fig.savefig(os.path.join(FIG,"fig03_flowchart.png"),bbox_inches="tight",pad_inches=0.12)
    plt.close(fig); print("fig03 done")

fig1(); fig2(); fig3(); print("DIAGRAMS DONE")
