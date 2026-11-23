"""CATÁLOGO ÚNICO DE HUECOS (ventanas, puertas, bandas, ojos), calculado solo desde el cuadro de cotas.
Lo usan: edificio.py (huecos del 3D), laminas.py (símbolo en planta, cortes en sección, cotas) → todas las vistas
coinciden porque salen de la misma lista.

Cada hueco: dict(id, grupo, tipo, p=(x,y) centro en la cara exterior del muro, t=(tx,ty) dirección de la fachada,
n=(nx,ny) normal hacia fuera, w ancho, z0, z1, e espesor de muro dibujado)."""
import math
import edificio as E

V = E._v
MURO = 0.30          # muros de carga / fachada
PART = 0.20          # particiones radiales de la torre


def _h(lst, id_, grupo, tipo, p, t, n, w, z0, z1, e=MURO):
    lst.append(dict(id=id_, grupo=grupo, tipo=tipo, p=(float(p[0]), float(p[1])), t=(float(t[0]), float(t[1])),
                    n=(float(n[0]), float(n[1])), w=float(w), z0=float(z0), z1=float(z1), e=e))


def catalogo():
    H = []
    W_P, L_L = V["W_P"], V["L_L"]
    # 1. ala larga, fachada exterior: 11 arriba, 7 abajo desde el testero [F73, F01, F47]
    n, nb, w, S = int(V["N_VEN"]), int(V["N_VEN_B"]), V["VEN_W"], V["S_VEN"]
    for i in range(n):
        yc = L_L - V["VEN_FIN"] - i * S - w / 2
        _h(H, f"VA{i + 1:02d}", "ala larga fila alta", "ventana", (W_P, yc), (0, 1), (1, 0), w, V["VA_0"], V["VA_1"])
        if i < nb:
            _h(H, f"VB{i + 1:02d}", "ala larga fila baja", "ventana", (W_P, yc), (0, 1), (1, 0), w, V["VB_0"], V["VB_1"])
    # 2. testero: puerta de servicio y ventana encima [F73]
    xa, xb = W_P - 0.63 * W_P, W_P - 0.49 * W_P
    _h(H, "TP1", "testero", "puerta", ((xa + xb) / 2, L_L), (-1, 0), (0, 1), xb - xa, 0.0, 2.6)
    xa, xb = W_P - 0.55 * W_P, W_P - 0.43 * W_P
    _h(H, "TV1", "testero", "ventana", ((xa + xb) / 2, L_L), (-1, 0), (0, 1), xb - xa, 4.6, 5.3)
    # 3. banda del hotel sobre la fachada exterior del ala (vidrio) [C04]
    C = E.C
    y0, y1 = C[1] + 0.3, C[1] + V["D_HOTF"] - 0.3
    _h(H, "HB1", "banda hotel (ala)", "banda", (W_P, (y0 + y1) / 2), (0, 1), (1, 0), y1 - y0, 4.35, 6.0)
    # 4. chaflán: vidrio restaurante y hotel (coordenadas de torre) [F09, F50]
    yf = -(E.R_COL - E.RET)
    U, N = E.U, E.N
    def Pt(X, Y): return E.P(X, Y)
    out = (-N[0], -N[1])                                        # N apunta al interior
    xr0, xr1 = -E._k + 0.4, -E.R_COL - 0.3
    _h(H, "CR1", "chaflán restaurante", "banda", Pt((xr0 + xr1) / 2, yf), U, out, xr1 - xr0, 4.6, 6.4)
    if E.L_CH - E._k - E.R_COL > 1.0:
        xh0, xh1 = E.R_COL + 0.3, E.L_CH - E._k - 0.4
        _h(H, "CH1", "chaflán hotel", "banda", Pt((xh0 + xh1) / 2, yf), U, out, xh1 - xh0, 4.35, 6.0)
    # 5. ala corta: banda continua a la calle (+4,6/+6,6) [F09, F14]
    PHI, KC = E.PHI, E.KC
    def R(x, y):
        dx, dy = x - KC[0], y - KC[1]; c, s = math.cos(PHI), math.sin(PHI)
        return (KC[0] + c * dx - s * dy, KC[1] + s * dx + c * dy)
    xA = W_P - E._a
    x0, x1 = -E.L_C + E.L_LADR + 0.4, xA
    a, b = R(x0, 0.0), R(x1, 0.0)
    tt = ((b[0] - a[0]) / math.dist(a, b), (b[1] - a[1]) / math.dist(a, b))
    _h(H, "AC1", "ala corta banda calle", "banda", ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), tt, (tt[1], -tt[0]), x1 - x0, 4.6, 6.6)
    # 6. torre: un hueco por módulo entre aletas y por planta, en la línea de vidrio rf [F04, F06, F09]
    T = E.T; rf = E.R_B - 1.8
    def en_escalera(a_, r_):          # módulo ocupado por la caja de la escalera insertada en el cilindro
        return abs((a_ - E.ESC_ANG + math.pi) % (2 * math.pi) - math.pi) < math.atan2(E.ESC_WY / 2 + 1.2, r_)
    for i in range(V["N_PL"]):
        z = E.Z_B0 + i * E.F
        for k in range(V["N_AL"]):
            a_ = 2 * math.pi * (k + 0.5) / V["N_AL"]
            if en_escalera(a_, rf): continue
            c, s = math.cos(a_), math.sin(a_)
            _h(H, f"T{i}{k:02d}", f"torre planta {i + 1}", "ventana", (T[0] + rf * c, T[1] + rf * s), (-s, c), (c, s),
               2.6 if i == 0 else 2.4, z + 1.7, z + 3.1)
    # 7. tambor: 19 ojos circulares [F01, F09]
    zt = (E.Z_B1 + E.Z_T1) / 2
    for k in range(V["N_AL"]):
        a_ = 2 * math.pi * (k + 0.5) / V["N_AL"]
        if en_escalera(a_, E.R_T): continue
        c, s = math.cos(a_), math.sin(a_)
        _h(H, f"OJ{k:02d}", "tambor ojos", "ojo", (T[0] + E.R_T * c, T[1] + E.R_T * s), (-s, c), (c, s), 1.6, zt - 0.8, zt + 0.8)
    return H


def cortados(z):
    """huecos que corta un plano horizontal a la cota z"""
    return [h for h in catalogo() if h["z0"] < z < h["z1"]]


if __name__ == "__main__":
    from collections import Counter
    c = Counter(h["grupo"] for h in catalogo())
    for k, v in c.items(): print(f"{v:4d}  {k}")
    print(len(catalogo()), "huecos")
