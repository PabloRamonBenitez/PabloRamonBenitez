import json, numpy as np, calibrar as C
from scipy.optimize import least_squares
from PIL import Image
foto='/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/1.webp'
W,H=Image.open(foto).size
obs={"barril_sup":[170,550,262],"barril_inf":[187,532,476],"tambor_ojos":[190,525,232],"tambor_sup":[293,417,45],"columna_pie":[322,388,652]}
linea=[[[12.7,22,9.9],[12.7,50,9.9],[548,410],[728,352],1]]
for az in range(-180,180,15):
    def f(x):
        return C.residuos([az]+list(x),obs,W,H)
    r=least_squares(f,[25,200,4,8,24,22,0],bounds=([-10,30,-60,-60,-5,3,-10],[89,3000,80,120,60,80,10]))
    C.LINEAS[:]=linea
    full=C.residuos([az]+list(r.x),obs,W,H); C.LINEAS[:]=[]
    cyl=np.sqrt(np.mean(f(r.x)**2)); lin=np.sqrt(np.mean(full[len(obs)*3:]**2))
    print(az, round(cyl,1), round(lin,1), np.round(r.x,1))
