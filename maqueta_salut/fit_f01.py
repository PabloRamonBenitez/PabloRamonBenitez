"""Ajuste en F01: camara (casi frontal al chaflan) + relacion torre-L (angulo del chaflan, distancia del eje de
la torre a la fachada exterior del ala larga)."""
import math, numpy as np, sys
from scipy.optimize import least_squares
from PIL import Image
import salut_v2 as s, calibrar as C, superponer as sp
I='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
foto=I+'1.webp'; W,H=Image.open(foto).size
obs={"barril_sup":[170,550,262],"barril_inf":[187,532,476],"tambor_ojos":[190,525,232],"tambor_sup":[293,417,45],"columna_pie":[322,388,652]}
LIN=[  # (descripcion, funcion 3D(a_ch, ex) -> (p3a,p3b), q0, q1)
 ("chaflan P1 +8,9 hotel", (431,538),(548,532)),
 ("chaflan P1 +8,9 rest.", (156,566),(325,550)),
 ("peto exterior ala larga", (555,405),(728,352)),
]
def lineas3d(a_ch, ex):
    A=math.radians(a_ch); u=np.array([math.cos(A),math.sin(A)]); n=np.array([-u[1],u[0]])
    # torre en el origen; chaflan (frente P1) en Y_t=-RET; ala larga: direccion perpendicular a la calle (y)...
    # en coords solares relativas a la torre, la calle es el eje x, el ala larga va en +y y su fachada exterior en x=ex
    o=-s.RET*n
    return [ (o+3*u, o+12*u, 8.9), (o-14*u, o-4*u, 8.9), (np.array([ex,10.0]), np.array([ex,40.0]), 9.9) ]
def res(x, ret_parts=False):
    cam_x=list(x[:8]); a_ch, ex = x[8], x[9]
    cam_x[0]=a_ch+cam_x[0]
    s.CEN=(0.0,0.0)
    r=list(C.residuos(cam_x,obs,W,H))
    cam=sp.camara(*cam_x[:3],tuple(cam_x[3:6]),cam_x[6],cam_x[7],W,H)
    for (desc,q0,q1),(pa,pb,z) in zip(LIN,lineas3d(a_ch,ex)):
        q0,q1=np.array(q0,float),np.array(q1,float); t=(q1-q0)/np.linalg.norm(q1-q0); nn=np.array([-t[1],t[0]])
        for a in np.linspace(0,1,5):
            P=np.append(pa*(1-a)+pb*a, z)
            X,Y,Z=C.proyectar(cam,P); uu=np.array([W/2+cam[4]*X/Z,H/2-cam[4]*Y/Z]); r.append(float((uu-q0)@nn))
    return np.array(r)
best=None
for a0 in (20,31,45,60):
    for d0 in (-20,0,20):
        for ex0 in (3,8,14):
            try: rr=least_squares(res,[d0,20,250,0,0,24,25,0,a0,ex0],bounds=([-40,8,100,-40,-40,0,10,-6,5,-5],[40,45,800,40,40,50,45,6,85,30]))
            except Exception: continue
            e=np.sqrt(np.mean(rr.fun**2))
            if best is None or e<best[0]: best=(e,rr.x,rr.fun)
print("rms",round(best[0],1)); print("x",np.round(best[1],2)); print("res",np.round(best[2],1))
np.save('fit_f01.npy',best[1])
