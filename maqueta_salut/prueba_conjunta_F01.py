"""¿Existe UNA cámara que encaje a la vez torre + chaflán + ala larga con el cuadro actual?"""
import numpy as np, verif_foto as VF, edificio as E
tor=[("barril_sup",170,550,262),("barril_inf",187,532,476),("columna_pie",322,388,652),("forj",[281.7,320,358.3,396.7,435,473]),
     ("tambor",190,525,232),("remate",293,417,45)]
lin=[("banda_hotel",(431,538),(548,532)),("banda_rest",(156,566),(325,550))]
V=E._v
pts=[((V["W_P"],V["L_L"],E.Z_P1+V["H_PET"]),(728,352)),((V["W_P"],V["L_L"],0.0),(727,458))]
for nombre,p in (("sin ala",()),("con ala",pts)):
    best,_=VF.calibrar("1.webp",tor,lin,az=(-60,120),el=(5,75),fov=(8,60),pts=p)
    print(nombre,"rms",round(best[0],1)); print("  residuos",np.round(best[2],1).tolist())
