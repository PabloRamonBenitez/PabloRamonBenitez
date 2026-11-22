import os, sys, subprocess, json
import numpy as np
for a in [34,37,40,43,46,49]:
    out=subprocess.run(['python3','-c',f'''
import numpy as np, salut_v2 as s, fit_fijo as F, calibrar as C, superponer as sp
from PIL import Image
I="/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/"
obs={{"barril_sup":[170,550,262],"barril_inf":[187,532,476],"tambor_ojos":[190,525,232],"tambor_sup":[293,417,45],"columna_pie":[322,388,652]}}
def P(X,Y,z): p=s.solar(X,Y); return [p[0],p[1],z]
lin=[(P(4,-s.RET,8.9),P(11,-s.RET,8.9),(431,538),(548,532)),(P(-13,-s.RET,8.9),P(-5,-s.RET,8.9),(156,566),(325,550))]
x0s=[[az,el,250,s.CEN[0],s.CEN[1],24,f,0] for az in range(-20,91,15) for el in (15,25) for f in (20,30)]
b=F.ajustar(I+"1.webp",obs,lin,x0s,([-30,10,120,-60,-60,0,12,-6],[90,40,800,60,60,50,45,6]))
x=b[1]; W,H=Image.open(I+"1.webp").size; K=sp.camara(*x[:3],tuple(x[3:6]),x[6],x[7],W,H)
def pr(p):
    X,Y,Z=C.proyectar(K,p); return (W/2+K[4]*X/Z, H/2-K[4]*Y/Z)
# arista superior exterior del ala (peto a +9,9 y fachada a x=W_P) en y = A2+5 ... A2+40
pts=[pr([s.W_P, s._A2[1]+d, 9.9]) for d in (5,20,40,60,80)]
print(round(b[0],1), [tuple(round(v) for v in q) for q in pts])
'''],env=dict(os.environ,SALUT_ACH=str(a)),capture_output=True,text=True,cwd='.')
    print(a, out.stdout.strip(), out.stderr.strip()[-200:])
