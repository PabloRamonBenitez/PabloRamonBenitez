"""Ajuste conjunto camara + angulo del chaflan con la foto F01 (cilindros + dos aristas de la base)."""
import math, numpy as np
from scipy.optimize import least_squares
from PIL import Image
import salut_v2 as s, calibrar as C, superponer as sp
foto='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/1.webp'
W,H=Image.open(foto).size
obs={"barril_sup":[170,550,262],"barril_inf":[187,532,476],"tambor_ojos":[190,525,232],"tambor_sup":[293,417,45],"columna_pie":[322,388,652]}

def geom(a_deg):
    A=math.radians(a_deg)
    A1=np.array([s.W_L-s.L_CH*math.cos(A),0.0]); A2=np.array([s.W_L,s.L_CH*math.sin(A)])
    u=(A2-A1)/np.linalg.norm(A2-A1); n=np.array([-u[1],u[0]])
    cen=A1+s.D_REST*u+s.RET*n
    return cen,u,n

def res(x):
    x=list(x); a_ch=x[8]; x[0]=a_ch+x[0]; cen,u,n=geom(a_ch)
    # todo en coords relativas al eje de la torre (cen en el origen) -> los cilindros no dependen del angulo
    s.CEN=(0.0,0.0)
    r=list(C.residuos(x[:8],obs,W,H))
    cam=sp.camara(*x[:3],tuple(x[3:6]),x[6],x[7],W,H)
    def lin(p3a,p3b,q0,q1,peso=1.0):
        q0,q1=np.array(q0,float),np.array(q1,float); t=(q1-q0)/np.linalg.norm(q1-q0); nn=np.array([-t[1],t[0]])
        out=[]
        for a in np.linspace(0,1,6):
            P=np.array(p3a)*(1-a)+np.array(p3b)*a
            X,Y,Z=C.proyectar(cam,P); uu=np.array([W/2+cam[4]*X/Z,H/2-cam[4]*Y/Z]); out.append(peso*float((uu-q0)@nn))
        return out
    # chaflan (frente de planta primera a +8,9): Y_torre = -RET  ->  en coords relativas: -RET*n + X*u
    pa=-s.RET*n+(-12)*u; pb=-s.RET*n+(12)*u
    r+=lin([pa[0],pa[1],8.9],[pb[0],pb[1],8.9],(156,566),(548,532))
    # fachada exterior del ala larga (peto +9,9): x_solar = W_P  ->  relativa: x - cen
    for yy in ():
        pass
    pa=np.array([s.W_P,25.0])-cen; pb=np.array([s.W_P,50.0])-cen
    r+=lin([pa[0],pa[1],9.9],[pb[0],pb[1],9.9],(548,410),(728,352))
    return np.array(r)

best=None
for a0 in (15,25,35,45,55):
    for az0 in (-30,0,30):
        try:
            rr=least_squares(res,[az0,25,200,0,0,24,22,0,a0],bounds=([-45,8,100,-60,-60,-5,12,-6,5],[45,45,700,60,60,60,45,6,80]))
        except Exception as e:
            continue
        e=np.sqrt(np.mean(rr.fun**2))
        if best is None or e<best[0]: best=(e,rr.x)
        print(a0,az0,round(e,1),np.round(rr.x,1))
print("MEJOR",round(best[0],1),np.round(best[1],2))
