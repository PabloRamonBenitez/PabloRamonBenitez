"""F73: proporciones de la fachada exterior del ala larga SIN cámara: fila de ventanas = puntos colineales
igualmente espaciados -> ajuste proyectivo 1D u(s) = (a s + b)/(c s + 1), con el punto de fuga x_vf = a/c."""
import numpy as np
from scipy.optimize import least_squares
# bordes del hueco (oscuro) de la fila alta, desde el testero hacia la torre (px, leídos en rejilla)
L = np.array([891, 848, 808, 770, 740, 712, 685, 662, 642, 623, 605], float)
R = np.array([918, 868, 827, 787, 753, 723, 697, 672, 650, 630, 612], float)
ESQ = 1060.0        # esquina testero / fachada
VF = 356.0          # punto de fuga horizontal de la fachada (cruce de dinteles con el horizonte a 1,6 m)
def u(p, s): return VF + p[0] / (s + p[1])        # forma proyectiva con fuga en VF
def res(p):
    w = p[2]; i = np.arange(len(L))
    return np.r_[u(p, i) - R, u(p, i + w) - L]     # s crece hacia la torre; borde derecho del hueco en s=i
r = least_squares(res, [5000, 9.0, 0.4]); p = r.x
print("residuos px:", np.round(r.fun, 1))
print(f"ancho del hueco / intereje = {p[2]:.2f}")
# esquina del testero en unidades de intereje
s_esq = p[0] / (ESQ - VF) - p[1]
print(f"esquina del testero en s = {s_esq:.2f}  -> macizo entre esquina y el 1er hueco = {-s_esq:.2f} interejes")
# verticales: alturas trasladadas a la vertical de la esquina por rectas al punto de fuga (y_horizonte = 958)
YH = 958.0
def a_esquina(x, y): return YH + (y - YH) * (ESQ - VF) / (x - VF)
suelo, peto = 1062.0, 505.0
H = suelo - peto
for nm, (x, y) in {"dintel fila alta (hueco 1)": (918, 710), "alféizar fila alta (hueco 1)": (918, 800),
                   "dintel fila alta (hueco 2)": (868, 732), "alféizar fila alta (hueco 2)": (868, 820),
                   "dintel fila baja (hueco 1)": (924, 900)}.items():
    yc = a_esquina(x, y); print(f"{nm:30s} altura = {(suelo - yc) / H:.3f} H")
