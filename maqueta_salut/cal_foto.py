"""Calibra una foto con la planta actual: cilindros + lineas (en coords de torre X,Y,z) y superpone."""
import sys, json, numpy as np, salut_v2 as s, fit_fijo as F, superponer as sp
from PIL import Image
I='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
S='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/scratchpad/'
CASOS={
 "F01": dict(f="1.webp", obs={"barril_sup":[170,550,262],"barril_inf":[187,532,476],"tambor_ojos":[190,525,232],"tambor_sup":[293,417,45],"columna_pie":[322,388,652]},
             lin=[((4,-1.5,7.4),(11,-1.5,7.4),(431,538),(548,532)),((-13,-1.5,7.4),(-5,-1.5,7.4),(156,566),(325,550))],
             az=(-30,90), el=(10,40), fov=(12,45)),
 "F09": dict(f="9.webp", obs={"barril_sup":[105,502,375],"barril_inf":[108,500,590],"tambor_ojos":[133,485,335],"tambor_sup":[240,385,190],"visera":[110,442,245]},
             lin=[((4,-1.5,7.4),(10,-1.5,7.4),(330,700),(455,700)),((-13,-1.5,7.4),(-5,-1.5,7.4),(80,700),(245,700))],
             az=(-30,90), el=(-3,8), fov=(3,20)),
}
def correr(k):
    c=CASOS[k]; P=lambda X,Y,z: [*s.solar(X,Y),z]
    lin=[(P(*a),P(*b),q0,q1) for a,b,q0,q1 in c["lin"]]
    x0s=[[az,(c["el"][0]+c["el"][1])/2,300,s.CEN[0],s.CEN[1],20,f,0] for az in range(c["az"][0],c["az"][1]+1,15) for f in (c["fov"][0]+2,(c["fov"][0]+c["fov"][1])/2)]
    lo=[c["az"][0],c["el"][0],80,-60,-60,0,c["fov"][0],-6]; hi=[c["az"][1],c["el"][1],2500,60,60,50,c["fov"][1],6]
    b=F.ajustar(I+c["f"],c["obs"],lin,x0s,(lo,hi))
    x=b[1]
    print(k,"rms",round(b[0],1),"cam",",".join(f"{v:.2f}" for v in x))
    sp.superponer(I+c["f"],*x[:3],tuple(x[3:6]),x[6],x[7],S+f"ov_{k}.png")
    return x
if __name__=="__main__":
    for k in sys.argv[1:]: correr(k)
