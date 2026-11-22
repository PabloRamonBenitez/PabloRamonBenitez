"""Zonas de verificacion v2: volumenes de izquierda y derecha, proyectados sobre F01 (camara calibrada),
y las mismas zonas en planta y en dos secciones, con el mismo color e identificador."""
import math, os, sys, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Circle
from scipy.optimize import least_squares
from PIL import Image
from manifold3d import Manifold
import edificio as E
I='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
im=Image.open(I+'1.webp').convert('RGB'); W,H=im.size
T=np.array(E.T); P=E.P; yf=-(E.R_COL-E.RET); pl=E.plantas_base(); Qy=pl["Q"][1]
# ------------------------------------------------------------------ camara
def cam(x):
    az,el,dist,tx,ty,tz,fov,roll=x
    a,e=math.radians(az),math.radians(el); tgt=np.array([tx,ty,tz])
    c=tgt+dist*np.array([math.sin(a)*math.cos(e),-math.cos(a)*math.cos(e),math.sin(e)])
    d=tgt-c; d/=np.linalg.norm(d); r=np.cross(d,[0,0,1]); r/=np.linalg.norm(r); u=np.cross(r,d)
    rr=math.radians(roll); r,u=r*math.cos(rr)+u*math.sin(rr),-r*math.sin(rr)+u*math.cos(rr)
    return c,r,u,d,(W/2)/math.tan(math.radians(fov)/2)
def proj(K,P3):
    c,r,u,d,f=K; v=np.atleast_2d(P3)-c
    return np.c_[W/2+f*(v@r)/(v@d), H/2-f*(v@u)/(v@d)]
OBS=[(T,15.3,32.6,170,550,262),(T,15.3,15.6,187,532,476),(T,13.55,35.4,190,525,232),
     (np.array(P(*E.OFF_R)),5.6,49.1,293,417,45),(T,3.25,0.5,322,388,652)]
def sil(K,c,R,z):
    Pp=np.array([c[0],c[1],z]); v=Pp-K[0]; h=np.array([v[0],v[1],0]); h/=np.linalg.norm(h); l=np.array([-h[1],h[0],0])
    q=proj(K,np.array([Pp+R*l,Pp-R*l])); return q[np.argsort(q[:,0])]
def res(x):
    K=cam(x); o=[]
    for c,R,z,xl,xr,y in OBS:
        q=sil(K,c,R,z); o+=[q[0,0]-xl,q[1,0]-xr,(q[0,1]+q[1,1])/2-y]
    for (X0,X1,p0,p1) in ((4,10,(431,538),(548,532)),(-13,-5,(156,566),(325,550))):
        a,b=np.array(p0,float),np.array(p1,float); t=(b-a)/np.linalg.norm(b-a); n=np.array([-t[1],t[0]])
        for s in np.linspace(0,1,4):
            X=X0+(X1-X0)*s; o.append(float((proj(K,np.array([*P(X,yf),7.3]))[0]-a)@n))
    return np.array(o)
best=None
for az in range(-30,61,15):
    for f in (25,35):
        try: r=least_squares(res,[az+math.degrees(E.A_CH),22,200,T[0],T[1],20,f,0],bounds=([-90,8,80,-60,-60,0,12,-6],[150,45,900,60,60,50,50,6]))
        except Exception: continue
        e=np.sqrt(np.mean(r.fun**2))
        if best is None or e<best[0]: best=(e,r.x)
K=cam(best[1])
# ------------------------------------------------------------------ zonas: (id, nombre, [ (poligono planta, z0, z1) ...] )
xe=E.W_BAR/2+0.5
ZON=[
 ("Z6","Barril: 1ª planta (pavés)", "cil", (T,E.R_AL,E.Z_B0,E.Z_B0+E.F)),
 ("Z7","Arranque: ménsulas, cuello, columna", "cil", (T,E.R_AL,E.Z_P1,E.Z_B0)),
 ("Z8","Chaflán: banda del restaurante", "pri", [([P(-15.85,yf),P(-E.R_COL,yf),P(-E.R_COL,yf+6),P(-15.85,yf+6)],E.Z_PB,E.Z_P1)]),
 ("Z9","Pie de columna y entrada", "pri", [([P(-E.R_COL,yf-1.5),P(E.R_COL,yf-1.5),P(E.R_COL,yf+4),P(-E.R_COL,yf+4)],0,E.Z_P1)]),
 ("Z10","Chaflán: banda del hotel y esquina 90°", "pri", [([P(E.R_COL,yf),pl["P1"][2],pl["Q"],P(E.R_COL,yf+6)],E.Z_PB,E.Z_P1)]),
 ("Z19","PB hundida del chaflán", "pri", [([P(-15.85,yf+E.RETR),P(E.R_COL+E.HOT,yf+E.RETR),P(E.R_COL+E.HOT,yf+6),P(-15.85,yf+6)],0,E.Z_PB)]),
 ("Z12","Ala corta: bloque alto y lucernarios", "pri", [([(-E.L_C+E.L_LADR,5.5),(pl["P1"][1][0]-1,5.5),(pl["P1"][1][0]-1,E.W_C),(-E.L_C+E.L_LADR,E.W_C)],E.Z_P1,E.Z_ALTO+1)]),
 ("Z20","Ala corta: banda a la calle", "pri", [([(-E.L_C+E.L_LADR,0),(pl["P1"][1][0],0),(pl["P1"][1][0],5.5),(-E.L_C+E.L_LADR,5.5)],0,E.Z_P1)]),
 ("Z13","Extremo: ladrillo sobre pilares", "pri", [([(-E.L_C,0),(-E.L_C+E.L_LADR,0),(-E.L_C+E.L_LADR,E.W_C),(-E.L_C,E.W_C)],0,E.Z_LADR)]),
 ("Z11","Concha / muro del relieve", "concha", None),
 ("Z14","Bar (mitad interior del ala)", "pri", [([(0,Qy),(E.W_BAR+1.2,Qy),(E.W_BAR+1.2,E.L_L-E.L_FIN),(0,E.L_L-E.L_FIN)],E.Z_P1,E.Z_BAR_C)]),
 ("Z15","Terraza de las sombrillas + peto", "pri", [([(E.W_BAR,Qy),(E.W_P,Qy),(E.W_P,E.L_L),(E.W_BAR,E.L_L)],E.Z_P1,E.Z_P1+1.0)]),
 ("Z16","Fachada exterior del ala: ventanas", "pri", [([(E.W_P-1,52),(E.W_P,52),(E.W_P,E.L_L),(E.W_P-1,E.L_L)],0,E.Z_P1)]),
 ("Z21","Cuerpo del ala larga (PB y P1)", "pri", [([(0,Qy),(E.W_P,Qy),(E.W_P,52),(0,52)],0,E.Z_P1)]),
 ("Z22","Testero final del ala", "pri", [([(0,E.L_L-E.L_FIN),(E.W_P,E.L_L-E.L_FIN),(E.W_P,E.L_L),(0,E.L_L)],0,E.Z_P1+1)]),
 ("Z17","Escalera trasera y encuentro", "pri", [([(xe-E.ESC_W/2,E.ESC_Y0),(xe+E.ESC_W/2,E.ESC_Y0),(xe+E.ESC_W/2,E.ESC_Y1+0.5),(xe-E.ESC_W/2,E.ESC_Y1+0.5)],E.Z_P1,E.Z_T1+1)]),
]
COL=plt.cm.tab20(np.linspace(0,1,20)); COL=np.vstack([COL,plt.cm.Set2(np.linspace(0,1,8))])
def concha_lineas():
    y0,y1=Qy,E.Y_CUNA; out=[]
    ys=np.linspace(0,1,30)
    top=[(E.W_P+(E.W_EXT-E.W_P)*(1-s)*0.999, y0+s*(y1-y0), E.Z_PB*(1-s)+max(0.05,(E.Z_P1-E.Z_PB*(1-s))*(1-s)**1.3)) for s in ys]
    inn=[(E.W_P, y0+s*(y1-y0), E.Z_PB*(1-s)+max(0.05,(E.Z_P1-E.Z_PB*(1-s))*(1-s)**1.3)) for s in ys]
    base=[(E.W_P+(E.W_EXT-E.W_P)*(1-s), y0+s*(y1-y0), E.Z_PB*(1-s)) for s in ys]
    return [np.array(top),np.array(inn),np.array(base),np.array([top[0],base[0]]),np.array([top[0],inn[0]])], [(E.W_P,y0),(E.W_EXT,y0),(E.W_P,y1)]
# ------------------------------------------------------------------ dibujo sobre F01
fig=plt.figure(figsize=(13,12.5)); ax=fig.add_axes([0.01,0.01,0.98,0.94]); ax.imshow(im); ax.axis('off')
fig.suptitle(f"Zonas sobre F01 (cámara calibrada con la torre, error {best[0]:.1f} px) – chaflán {math.degrees(E.A_CH):.0f}°",fontsize=13,weight='bold')
def etiqueta(ax,p,k,c): ax.text(*p,k,color='white',fontsize=10,weight='bold',ha='center',va='center',bbox=dict(fc=c,ec='none',pad=1.2))
for i,(k,n,tipo,g) in enumerate(ZON):
    c=COL[i]
    if tipo=="cil":
        cc,R,z0,z1=g; t=np.linspace(0,2*np.pi,90)
        for z in (z0,z1):
            q=proj(K,np.c_[cc[0]+R*np.cos(t),cc[1]+R*np.sin(t),np.full(90,z)]); ax.plot(q[:,0],q[:,1],color=c,lw=2)
        q=sil(K,cc,R,z1); etiqueta(ax,(q[0,0]+14,q[0,1]),k,c)
    elif tipo=="pri":
        for poly,z0,z1 in g:
            poly=np.array(poly); m=len(poly)
            lo=proj(K,np.c_[poly,np.full(m,z0)]); hi=proj(K,np.c_[poly,np.full(m,z1)])
            for j in range(m):
                for A,B in ((lo[j],lo[(j+1)%m]),(hi[j],hi[(j+1)%m]),(lo[j],hi[j])):
                    ax.plot([A[0],B[0]],[A[1],B[1]],color=c,lw=1.8)
            etiqueta(ax,hi.mean(axis=0),k,c)
    else:
        ls,_=concha_lineas()
        for L3 in ls:
            q=proj(K,L3); ax.plot(q[:,0],q[:,1],color=c,lw=2)
        etiqueta(ax,proj(K,ls[0][5])[0],k,c)
fig.savefig("ZONAS_v2_F01.png",dpi=80); plt.close(fig)
# ------------------------------------------------------------------ planta con las mismas zonas
fig=plt.figure(figsize=(13,15)); ax=fig.add_axes([0.05,0.03,0.6,0.92])
ax.add_patch(MPoly(pl["P1"],closed=True,fc="0.93",ec="k",lw=1.2)); ax.add_patch(MPoly(pl["PB"],closed=True,fc="none",ec="k",lw=0.7,ls="--"))
for r,ls in ((E.R_AL,"--"),(E.R_CU,":"),(E.R_COL,"-")): ax.add_patch(Circle(T,r,fc="none",ec="0.4",ls=ls))
for i,(k,n,tipo,g) in enumerate(ZON):
    c=COL[i]
    if tipo=="cil": continue
    polys=[np.array(p) for p,_,_ in g] if tipo=="pri" else [np.array(concha_lineas()[1])]
    for pp in polys:
        ax.add_patch(MPoly(pp,closed=True,fc=(*c[:3],0.28),ec=c,lw=2)); etiqueta(ax,pp.mean(axis=0),k,c)
ax.text(*T,"Z1-Z7",ha="center",fontsize=9)
ax.set_xlim(-27,20); ax.set_ylim(-6,98); ax.set_aspect("equal"); ax.grid(True,lw=0.2); ax.set_title("Zonas en planta (P1 continua, PB discontinua)",fontsize=10,loc="left")
ax2=fig.add_axes([0.67,0.03,0.32,0.92]); ax2.axis("off")
ax2.text(0,1,"\n".join(["Z1  Remate y letrero (F09)","Z2  Visera (F09)","Z3  Banda acristalada (F09)","Z4  Tambor de ojos y terraza (F09)","Z5  Barril: plantas tipo (F09)"]+
         [f"{k:<4} {n}" for k,n,*_ in ZON]+["","Z18 Patio interior de la L (sin foto)"]),fontsize=9,va="top",family="DejaVu Sans")
fig.savefig("ZONAS_v2_planta.png",dpi=80); plt.close(fig)
# ------------------------------------------------------------------ dos secciones con las mismas zonas
M=E.edificio()
def corte(ax,p0,p1,titulo,zon_ids):
    a=math.degrees(math.atan2(p1[1]-p0[1],p1[0]-p0[0])); Lg=math.hypot(p1[0]-p0[0],p1[1]-p0[1])
    m=M.translate((-p0[0],-p0[1],0)).rotate((0,0,-a)).rotate((-90,0,0))
    for Pp in m.slice(0.0).to_polygons(): ax.add_patch(MPoly(np.array(Pp),closed=True,fc="#cfcfcf",ec="k",lw=1.4,hatch="///"))
    for Pp in (m^Manifold.cube((800,100,800)).translate((-400,-50,-800))).project().to_polygons():
        ax.add_patch(MPoly(np.array(Pp),closed=True,fc="none",ec="0.6",lw=0.4,zorder=0))
    # zonas: interseccion de cada prisma con el plano de corte -> rectangulo (s0,s1,z0,z1)
    d=np.array([math.cos(math.radians(a)),math.sin(math.radians(a))]); nn=np.array([-d[1],d[0]])
    from shapely.geometry import Polygon as SP, LineString
    for i,(k,n,tipo,g) in enumerate(ZON):
        if k not in zon_ids: continue
        c=COL[i]
        if tipo=="cil":
            cc,R,z0,z1=g; s_c=(np.array(cc)-p0)@d; dd=abs((np.array(cc)-p0)@nn)
            if dd<R: w=math.sqrt(R*R-dd*dd); ax.add_patch(plt.Rectangle((s_c-w,z0),2*w,z1-z0,fill=False,ec=c,lw=2.2)); etiqueta(ax,(s_c-w+1.5,z1-0.8),k,c)
            continue
        polys=[(np.array(pp),z0,z1) for pp,z0,z1 in g] if tipo=="pri" else [(np.array(concha_lineas()[1]),0,E.Z_P1)]
        for pp,z0,z1 in polys:
            inter=SP(pp).intersection(LineString([tuple(p0),tuple(p1)]))
            if inter.is_empty: continue
            ss=[(np.array(q)-p0)@d for q in np.array(inter.coords)]
            ax.add_patch(plt.Rectangle((min(ss),z0),max(ss)-min(ss),z1-z0,fill=False,ec=c,lw=2.2)); etiqueta(ax,((min(ss)+max(ss))/2,z1+0.6),k,c)
    ax.axhline(0,color="k",lw=1.5); ax.set_xlim(-1,Lg+1); ax.set_ylim(-1,20); ax.set_aspect("equal"); ax.grid(True,lw=0.2)
    ax.set_title(titulo,fontsize=9,loc="left")
fig,axs=plt.subplots(2,1,figsize=(16,11))
corte(axs[0],(-4,40.0),(20,40.0),"Sección transversal del ala larga a y=40 (izquierda = patio)",{"Z11","Z14","Z15","Z21"})
pa=np.array(P(7,-14)); pb=np.array(P(7,14))
corte(axs[1],pa,pb,"Sección por la banda del hotel, perpendicular al chaflán (izquierda = plaza)",{"Z7","Z10","Z19","Z6","Z9"})
fig.savefig("ZONAS_v2_secciones.png",dpi=80)
print("ok rms",round(best[0],1))
