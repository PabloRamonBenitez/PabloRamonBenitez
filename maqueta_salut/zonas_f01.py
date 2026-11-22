"""Zonas de la base dibujadas sobre F01 (aerea de epoca) con camara calibrada con la geometria de edificio.py."""
import math, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from PIL import Image
import edificio as E
I='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
im=Image.open(I+'1.webp').convert('RGB'); W,H=im.size

def cam(x):
    az,el,dist,tx,ty,tz,fov,roll=x
    a,e=math.radians(az),math.radians(el); tgt=np.array([tx,ty,tz])
    c=tgt+dist*np.array([math.sin(a)*math.cos(e),-math.cos(a)*math.cos(e),math.sin(e)])
    d=tgt-c; d/=np.linalg.norm(d); r=np.cross(d,[0,0,1]); r/=np.linalg.norm(r); u=np.cross(r,d)
    rr=math.radians(roll); r,u=r*math.cos(rr)+u*math.sin(rr),-r*math.sin(rr)+u*math.cos(rr)
    return c,r,u,d,(W/2)/math.tan(math.radians(fov)/2)
def proj(K,P):
    c,r,u,d,f=K; v=np.atleast_2d(P)-c
    return np.c_[W/2+f*(v@r)/(v@d), H/2-f*(v@u)/(v@d)]
T=np.array(E.T)
OBS=[(T,15.3,32.6,170,550,262),(T,15.3,15.6,187,532,476),(T,13.55,35.4,190,525,232),
     (np.array(E.P(*E.OFF_R)),5.6,49.1,293,417,45),(T,3.25,0.5,322,388,652)]
def silueta(K,c,R,z):
    P=np.array([c[0],c[1],z]); v=P-K[0]; h=np.array([v[0],v[1],0]); h/=np.linalg.norm(h); l=np.array([-h[1],h[0],0])
    q=proj(K,np.array([P+R*l,P-R*l])); q=q[np.argsort(q[:,0])]; return q
def res(x):
    K=cam(x); out=[]
    for c,R,z,xl,xr,y in OBS:
        q=silueta(K,c,R,z); out+=[q[0,0]-xl,q[1,0]-xr,(q[0,1]+q[1,1])/2-y]
    # chaflan: frente de la planta 1 a +7,3 (Y torre = -(R_COL-RET))
    yf=-(E.R_COL-E.RET)
    for (X0,X1,p0,p1) in ((4,10,(431,538),(548,532)),(-13,-5,(156,566),(325,550))):
        a,b=np.array(p0,float),np.array(p1,float); t=(b-a)/np.linalg.norm(b-a); n=np.array([-t[1],t[0]])
        for s in np.linspace(0,1,4):
            X=X0+(X1-X0)*s; P=np.array([*E.P(X,yf),7.3]); out.append(float((proj(K,P)[0]-a)@n))
    return np.array(out)
best=None
for az in range(-30,61,15):
    for f in (25,35):
        try: r=least_squares(res,[az+31,22,200,T[0],T[1],20,f,0],bounds=([-60,8,80,-40,-40,0,12,-6],[120,45,900,50,50,50,50,6]))
        except Exception: continue
        e=np.sqrt(np.mean(r.fun**2))
        if best is None or e<best[0]: best=(e,r.x)
print("rms px",round(best[0],1),np.round(best[1],2)); K=cam(best[1])

fig=plt.figure(figsize=(13,12.5)); ax=fig.add_axes([0.01,0.01,0.98,0.94]); ax.imshow(im); ax.axis('off')
fig.suptitle("Zonas de la base y del arranque sobre F01 (cámara calibrada, error %.1f px)"%best[0],fontsize=13,weight='bold')
COL=plt.cm.tab20(np.linspace(0,1,20))
def caja3d(poly,z0,z1,k,i):
    poly=np.array(poly); n=len(poly)
    lo=proj(K,np.c_[poly,np.full(n,z0)]); hi=proj(K,np.c_[poly,np.full(n,z1)])
    c=COL[i]
    for j in range(n):
        for A,B in ((lo[j],lo[(j+1)%n]),(hi[j],hi[(j+1)%n]),(lo[j],hi[j])):
            ax.plot([A[0],B[0]],[A[1],B[1]],color=c,lw=2)
    m=hi.mean(axis=0); ax.text(*m,k,color='white',fontsize=11,weight='bold',ha='center',va='center',bbox=dict(fc=c,ec='none',pad=1.5))
def cil3d(c,R,z0,z1,k,i):
    t=np.linspace(0,2*np.pi,90); col=COL[i]
    for z in (z0,z1):
        q=proj(K,np.c_[c[0]+R*np.cos(t),c[1]+R*np.sin(t),np.full(90,z)]); ax.plot(q[:,0],q[:,1],color=col,lw=2)
    q=silueta(K,c,R,z1); ax.text(q[0,0]+4,q[0,1]+12,k,color='white',fontsize=11,weight='bold',bbox=dict(fc=col,ec='none',pad=1.5))
cil3d(T,E.R_AL,E.Z_B0,E.Z_B0+E.F,"Z6",5)
cil3d(T,E.R_AL,E.Z_P1,E.Z_B0,"Z7",6)
P=E.P; yf=-(E.R_COL-E.RET); pl=E.plantas_base()
caja3d([P(-15.85,yf),P(-E.R_COL,yf),P(-E.R_COL,yf+6),P(-15.85,yf+6)],0,7.3,"Z8",7)
caja3d([P(-E.R_COL,yf-1.5),P(E.R_COL,yf-1.5),P(E.R_COL,yf+4),P(-E.R_COL,yf+4)],0,7.3,"Z9",8)
caja3d([P(E.R_COL,yf),P(E.R_COL+E.HOT,yf),P(E.R_COL+E.HOT,yf+6),P(E.R_COL,yf+6)],0,7.3,"Z10",9)
caja3d([(E.W_P,pl["Q"][1]),(E.W_EXT,pl["Q"][1]),(E.W_EXT,E.Y_CUNA),(E.W_P,E.Y_CUNA)],0,7.3,"Z11",10)
caja3d([(-E.L_C+E.L_LADR,0),(-9,0),(-9,E.W_C),(-E.L_C+E.L_LADR,E.W_C)],0,11.5,"Z12",11)
caja3d([(-E.L_C,0),(-E.L_C+E.L_LADR,0),(-E.L_C+E.L_LADR,E.W_C),(-E.L_C,E.W_C)],0,9.0,"Z13",12)
caja3d([(0,22),(E.W_P,22),(E.W_P,45),(0,45)],0,11.1,"Z14",13)
caja3d([(0,45),(E.W_P,45),(E.W_P,80),(0,80)],0,11.1,"Z15",14)
fig.savefig("ZONAS_base_sobre_F01.png",dpi=80)
np.save("cam_F01_edificio.npy",best[1])
