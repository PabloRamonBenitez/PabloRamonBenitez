"""F01: camara + angulo del chaflan con la calle (a_ch) + angulo del ala larga con la calle (beta) + posicion
de su fachada exterior. La torre, el chaflan y el ala corta se definen como en salut_v2."""
import math, numpy as np
from scipy.optimize import least_squares
from PIL import Image
import salut_v2 as s, calibrar as C, superponer as sp
I='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
S='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/scratchpad/'
W,H=Image.open(I+'1.webp').size
obs={"barril_sup":[170,550,262],"barril_inf":[187,532,476],"tambor_ojos":[190,525,232],"tambor_sup":[293,417,45],"columna_pie":[322,388,652]}
def geo(a_ch):
    A=math.radians(a_ch)
    A1=np.array([s.W_L-s.L_CH*math.cos(A),0.0]); A2=np.array([s.W_L,s.L_CH*math.sin(A)])
    u=(A2-A1)/np.linalg.norm(A2-A1); n=np.array([-u[1],u[0]]); cen=A1+s.D_REST*u+s.RET*n
    return A1,A2,u,n,cen
def lines(p):
    a_ch,beta,off=p
    A1,A2,u,n,cen=geo(a_ch)
    c=lambda q: np.array(q)-cen          # todo relativo al eje de la torre
    out=[]
    out.append((c(cen+4*u-s.RET*n),c(cen+11*u-s.RET*n),8.9,(431,538),(548,532)))
    out.append((c(cen-13*u-s.RET*n),c(cen-5*u-s.RET*n),8.9,(156,566),(325,550)))
    # ala larga: arranca en A2 (fin del chaflan) con direccion beta respecto a la calle; fachada exterior desplazada 'off'
    d=np.array([math.cos(math.radians(beta)),math.sin(math.radians(beta))]); m=np.array([d[1],-d[0]])  # m hacia fuera
    b0=A2+off*m
    out.append((c(b0+10*d),c(b0+35*d),9.9,(555,405),(728,352)))
    return out
def res(x):
    cam=list(x[:8]); p=x[8:]
    s.CEN=(0.0,0.0)
    r=list(C.residuos(cam,obs,W,H)); K=sp.camara(*cam[:3],tuple(cam[3:6]),cam[6],cam[7],W,H)
    for pa,pb,z,q0,q1 in lines(p):
        q0,q1=np.array(q0,float),np.array(q1,float); t=(q1-q0)/np.linalg.norm(q1-q0); nn=np.array([-t[1],t[0]])
        for a in np.linspace(0,1,5):
            P=np.append(pa*(1-a)+pb*a,z); X,Y,Z=C.proyectar(K,P)
            r.append(float((np.array([W/2+K[4]*X/Z,H/2-K[4]*Y/Z])-q0)@nn))
    return np.array(r)
best=None
for b0 in (60,75,90,105):
  for a0 in (25,35,45):
    for az in (0,30,60):
        try: rr=least_squares(res,[az,20,250,0,0,20,30,0,a0,b0,0],bounds=([-60,10,120,-40,-40,0,12,-6,10,40,-6],[120,40,800,40,40,50,45,6,70,130,6]))
        except Exception: continue
        e=np.sqrt(np.mean(rr.fun**2))
        if best is None or e<best[0]: best=(e,rr.x,rr.fun)
print("rms",round(best[0],1)); print(np.round(best[1],2)); print(np.round(best[2][15:],1))
