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
        _h(H, f"VA{i + 1:02d}", "ala larga fila alta", "ventana", (W_P - V["FAC_R"], yc), (0, 1), (1, 0), w, V["VA_0"], V["VA_1"])
        if i < nb:
            _h(H, f"VB{i + 1:02d}", "ala larga fila baja", "ventana", (W_P - V["FAC_R"], yc), (0, 1), (1, 0), w, V["VB_0"], V["VB_1"])
    # 2. testero: puerta de servicio y ventana encima [F73]
    xa, xb = W_P - 0.63 * W_P, W_P - 0.49 * W_P
    _h(H, "TP1", "testero", "puerta", ((xa + xb) / 2, L_L), (-1, 0), (0, 1), xb - xa, 0.0, 2.6)
    xa, xb = W_P - 0.55 * W_P, W_P - 0.43 * W_P
    _h(H, "TV1", "testero", "ventana", ((xa + xb) / 2, L_L), (-1, 0), (0, 1), xb - xa, 4.6, 5.3)
    # 3-4. chaflán, planta primera: paños de vidrio de módulo M_CH desde la columna hacia fuera; restaurante 5 y pico,
    #      hotel 4 y pico (hasta la esquina a 90° con la rampa) [F09 frontal, F18, usuario]
    yf = -(E.R_COL - E.RET)
    U, N = E.U, E.N
    out = (-N[0], -N[1])                                        # N apunta al interior
    M = V["M_CH"]
    for nm, sg, L_, z0, z1, grupo in (("CR", -1, V["REST_L"], 4.6, 6.4, "chaflán restaurante"), ("CH", 1, V["HOT_L"], 4.35, 6.0, "chaflán hotel")):
        x = E.R_COL; i = 0
        while x < E.R_COL + L_ - 0.3:
            w = min(M, E.R_COL + L_ - 0.2 - x)
            _h(H, f"{nm}{i + 1}", grupo, "ventana", E.P(sg * (x + w / 2), yf), U, out, w - 0.15, z0, z1)
            x += M; i += 1
    # 5. ala corta: la fachada a la calle tras la logia es ladrillo ciego (foto frontal) → sin banda de ventanas
    PHI, KC = E.PHI, E.KC
    def R(x, y):
        dx, dy = x - KC[0], y - KC[1]; c, s = math.cos(PHI), math.sin(PHI)
        return (KC[0] + c * dx - s * dy, KC[1] + s * dx + c * dy)
    # 6. torre: un hueco por módulo entre aletas y por planta, en la línea de vidrio rf [F04, F06, F09]
    T = E.T; rf = E.R_B - 1.8
    def en_escalera(a_, r_):          # módulo ocupado por la caja de la escalera insertada en el cilindro
        return abs((a_ - E.ESC_ANG + math.pi) % (2 * math.pi) - math.pi) < E.ESC_HA
    for i in range(V["N_PL"]):
        z = E.Z_B0 + i * E.F
        for k in range(V["N_AL"]):
            a_ = 2 * math.pi * (k + 0.5) / V["N_AL"] + E.FASE_AL
            if en_escalera(a_, rf): continue
            c, s = math.cos(a_), math.sin(a_)
            _h(H, f"T{i}{k:02d}", f"torre planta {i + 1}", "ventana", (T[0] + rf * c, T[1] + rf * s), (-s, c), (c, s),
               2.6 if i == 0 else 2.4, z + 1.7, z + 3.1)
    # 6b. fachada retranqueada a cada lado del cuerpo de escalera: una ventana por planta y lado [F08, F11]
    RR = V["ESC_RR"]
    for i in range(V["N_PL"]):
        z = E.Z_B0 + i * E.F
        for sg, nm in ((-1, "a"), (1, "b")):
            a_ = E.ESC_ANG + sg * (E.ESC_HA + E.ESC_HB) / 2
            c, s = math.cos(a_), math.sin(a_)
            _h(H, f"ER{i}{nm}", "escalera retranqueo", "ventana", (T[0] + RR * c, T[1] + RR * s), (-s, c), (c, s),
               0.7 * RR * (E.ESC_HA - E.ESC_HB), z + 1.0, z + 2.6)
    # 6c. puerta de la escalera a la terraza (+Z_P1), junto al arranque de la rampa del techo del restaurante
    c, s = math.cos(E.ESC_ANG), math.sin(E.ESC_ANG)
    for nm, z0 in ():
        _h(H, nm, "escalera puertas", "puerta", (T[0] + V["ESC_RC"] * c, T[1] + V["ESC_RC"] * s), (-s, c), (c, s), 1.2, z0, z0 + 2.2)
    # 6d. puertas del hotel en planta baja, junto a la columna, en la fachada retranqueada RETR [usuario, F18]
    yfp = -(E.R_COL - E.RET) + V["RETR"]
    for i in range(int(V["PUERTAS_H"])):
        X = E.R_COL + 1.2 + i * 2.6
        _h(H, f"HP{i + 1}", "hotel puertas PB", "puerta", E.P(X, yfp), U, out, 1.8, 0.0, 2.5)
    # 6e. ventanas de la fachada posterior del bloque alto (línea A) [croquis del usuario]
    for i, xx in enumerate((1.5, 3.0, 7.5, 10.5)):
        a, b = R(-E.L_C + xx, E.W_C), R(-E.L_C + xx + 1.2, E.W_C)
        tt = ((b[0] - a[0]) / math.dist(a, b), (b[1] - a[1]) / math.dist(a, b))
        _h(H, f"BA{i + 1}", "bloque alto posterior", "ventana", ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), tt, (-tt[1], tt[0]), 1.2, 8.3, 10.1)
    # 6f. puerta del tambor a la cubierta del barril, junto a la escalera (lado izquierdo mirando la escalera) [foto de frente, usuario]
    at = math.radians(V["TP_ANG"]); c, s = math.cos(at), math.sin(at); zb = E.Z_B1 + V["FOR_C"]
    _h(H, "TP1", "tambor puerta", "puerta", (T[0] + E.R_T * c, T[1] + E.R_T * s), (-s, c), (c, s), V["TP_W"], zb, zb + V["TP_H"])
    # 6g. cristalera suelo-techo con dintel en el hueco de 2 m entre tambor y escalera, a la altura del tambor [foto de frente]
    am = E.ESC_ANG - (E.ESC_HA + E.ESC_HB) / 2; c, s = math.cos(am), math.sin(am); rr = V["ESC_RR"]
    _h(H, "CR1", "escalera cristalera", "ventana", (T[0] + rr * c, T[1] + rr * s), (-s, c), (c, s), 0.95 * rr * (E.ESC_HA - E.ESC_HB), zb, V["CR_Z1"])
    # 6h. logia de planta 1 bajo el cuerpo volado: vidrio retranqueado LOG_D en dos paños a los lados del pilar [foto frontal]
    x0l = -E.L_C; ld, lx = V["LOG_D"], V["LOG_PX"]
    for nm, xa, xb in (("LG1", x0l + V["LOG_X0"] + 0.1, x0l + lx - 0.35), ("LG2", x0l + lx + 0.35, x0l + V["LOG_X1"] - 0.1)):
        a, b = R(xa, ld), R(xb, ld)
        tt = ((b[0] - a[0]) / math.dist(a, b), (b[1] - a[1]) / math.dist(a, b))
        _h(H, nm, "logia", "ventana", ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), tt, (-tt[1], tt[0]), math.dist(a, b), E.Z_PB + 0.3, E.Z_P1 - 0.3)
    # 6i. cristalera de la PB bajo el arco de la concha (fachada retranqueada RETR) [usuario 26/11, F76, F24]
    pl = E.plantas_base(); ya = pl["Q"][1] + V["D_HOTF"] + 0.6; yb = pl["PB"][3][1] - 0.6
    xr = E.W_P - V["RETR"]; nm = max(int((yb - ya) / 2.4), 1); wm = (yb - ya) / nm
    for i in range(nm):
        _h(H, f"CP{i + 1}", "cristalera PB concha", "ventana", (xr, ya + (i + 0.5) * wm), (0, 1), (1, 0), wm - 0.15, 0.15, V["Z_ARC"] - 0.25)
    # 7. tambor: 19 ojos circulares [F01, F09]
    zt = (E.Z_B1 + E.Z_T1) / 2
    for k in range(V["N_AL"]):
        a_ = 2 * math.pi * (k + 0.5) / V["N_AL"] + E.FASE_AL
        if en_escalera(a_, E.R_T): continue
        if V["OJO_C0"] < math.degrees(a_) % 360 < V["OJO_C1"]: continue      # lado ciego (Alamy, MGF)
        if 0 < math.degrees(E.ESC_ANG - E.ESC_HA - a_) % 360 < 360 / V["N_AL"]: continue   # junto a la escalera (lado izq.): puerta, no ojo [foto de frente]
        if V["OJO_C1"] < math.degrees(a_) % 360 < V["OJO_C1"] + 18:          # primer ojo tras el lado ciego: fuera de módulo [Alamy]
            a_ += math.radians(V["OJO_DP"])
        c, s = math.cos(a_), math.sin(a_); zo, ro = V["OJO_Z"], V["OJO_D"] / 2
        _h(H, f"OJ{k:02d}", "tambor ojos", "ojo", (T[0] + E.R_T * c, T[1] + E.R_T * s), (-s, c), (c, s), V["OJO_D"], zo - ro, zo + ro)
    return H


def cortados(z):
    """huecos que corta un plano horizontal a la cota z"""
    return [h for h in catalogo() if h["z0"] < z < h["z1"]]


if __name__ == "__main__":
    from collections import Counter
    c = Counter(h["grupo"] for h in catalogo())
    for k, v in c.items(): print(f"{v:4d}  {k}")
    print(len(catalogo()), "huecos")
