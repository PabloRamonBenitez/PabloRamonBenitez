"""ALZADO 3 – CALLE dibujado como alzado de arquitectura (no es un render del 3D): cada pieza se proyecta en la
dirección perpendicular a la calle a partir del cuadro de cotas y se dibuja con su material (ladrillo con trama,
hormigón blanco, vidrio oscuro), de atrás hacia delante. Fuentes de cada pieza en cotas.py."""
import math
import numpy as np
from matplotlib.patches import Polygon, Rectangle, Ellipse
import edificio as E
import cotas as K

V = E._v
G = K.planta()
EU = -np.array(E.US)                    # dirección de la calle (u crece hacia el chaflán)
ED = np.array(E.NS)                     # profundidad (hacia dentro del edificio)
KC = np.array(E.KC)

LADR = dict(fc="white", ec="k", lw=0.7, hatch="---")
HORM = dict(fc="white", ec="k", lw=0.7)
VIDR = dict(fc="0.45", ec="k", lw=0.5)
OSCU = dict(fc="0.25", ec="k", lw=0.5)


def u_of(P):
    return float(V["W_P"] - (np.array(P, float) - KC) @ np.array(E.US))


def rect(ax, u0, u1, z0, z1, st, zo):
    ax.add_patch(Rectangle((min(u0, u1), z0), abs(u1 - u0), z1 - z0, zorder=zo, **st))


def baranda_alz(ax, uc, R, z0, h, zo, paso=2.0):
    """barandilla abierta en alzado: pasamanos, travesaño y postes"""
    for zz in (z0 + 0.5, z0 + h):
        ax.plot([uc - R, uc + R], [zz, zz], color="k", lw=0.4, zorder=zo)
    n = max(int(2 * math.pi * R / paso), 8)
    for k in range(n):
        a = 2 * math.pi * k / n
        if math.sin(a) > 0: continue
        uu = uc + R * math.cos(a); ax.plot([uu, uu], [z0, z0 + h], color="k", lw=0.3, zorder=zo)


def torre(ax, zo=10):
    T = np.array(E.T); uT = u_of(T)
    # escalera en cuña (detrás): asoma por encima del barril
    pe = np.array(E.esc_ang_pt(V["ESC_RC"], 0.0)); ue = u_of(pe)
    ch = 2 * V["ESC_RC"] * math.sin(E.ESC_HB)
    rect(ax, ue - ch / 2, ue + ch / 2, V["ESC_Z0"], V["ESC_ZL"], dict(fc="white", ec="k", lw=0.6, hatch="||||"), zo)   # lamas
    rect(ax, ue - ch / 2, ue + ch / 2, V["ESC_ZL"], E.Z_T1, dict(fc="white", ec="k", lw=0.6), zo)                   # remate sin lamas
    uw = u_of(np.array(E.esc_ang_pt(V["ESC_R1"], -E.ESC_HB)))
    rect(ax, uw - 0.3, uw + 0.3, E.Z_T1, V["ESC_Z1"], dict(fc="white", ec="k", lw=0.6), zo)                         # muro de coronación inclinada
    # pie de la escalera: losa blanca, núcleo y celosía baja [F78, foto de frente]
    rect(ax, ue - ch / 2, ue + ch / 2, V["ESC_Z0"] - 0.3, V["ESC_Z0"], HORM, zo + 0.5)
    cn = ch * V["ESC_NU"]
    rect(ax, ue - cn / 2, ue + cn / 2, E.Z_P1, V["ESC_Z0"] - 0.3, HORM, zo + 0.4)
    rect(ax, ue - ch / 2, ue + ch / 2, E.Z_P1, E.Z_P1 + V["ESC_CB"], dict(fc="white", ec="k", lw=0.5, hatch="||||"), zo + 0.6)
    # lucernarios piramidales bajo el cuello
    for L_ in E.lucernarios_cuello():
        o = np.array([math.cos(L_["a"]), math.sin(L_["a"])])
        if o @ ED > 0.3: continue
        uu = u_of(L_["c"]); w = L_["l"] / 2 * (abs(o @ EU) + abs(o @ ED))
        ax.add_patch(Polygon([(uu - w, L_["z"]), (uu + w, L_["z"]), (uu, L_["z"] + L_["h"])], closed=True, fc="#dfe8ee", ec="k", lw=0.5, zorder=zo + 2))
    # columna, cuello y losa
    rect(ax, uT - E.R_COL, uT + E.R_COL, 0, E.Z_CU0, HORM, zo + 3)
    rect(ax, uT - E.R_CU, uT + E.R_CU, E.Z_CU0, E.Z_CU1, HORM, zo + 1)
    rect(ax, uT - E.R_CU - 0.6, uT + E.R_CU + 0.6, E.Z_CU0, E.Z_CU0 + 0.6, HORM, zo + 1)
    # sofito del barril y ménsulas
    rect(ax, uT - E.R_B, uT + E.R_B, E.Z_CU1, E.Z_ALETA0, HORM, zo + 1)
    rf = E.R_B - 1.8
    rect(ax, uT - rf, uT + rf, E.Z_B0, E.Z_B1, VIDR, zo + 1)                         # fondo acristalado
    for i in range(V["N_PL"] + 1):
        z = E.Z_B0 + i * E.F
        rect(ax, uT - E.R_B, uT + E.R_B, z, z + E._v["FOR_C"], HORM, zo + 2)                   # canto del forjado
        if i < V["N_PL"]:
            zp = z + E._v["FOR_C"] + E._v["FOR_R"]
            rect(ax, uT - E.R_B + 0.25, uT + E.R_B - 0.25, zp, zp + E._v["FOR_P"], HORM, zo + 2)   # poyete [MGF]
    for k in range(V["N_AL"]):                                                           # aletas visibles
        a = 2 * math.pi * k / V["N_AL"] + E.FASE_AL; o = np.array([math.cos(a), math.sin(a)])
        if o @ ED > 0.05: continue
        s = o @ EU
        u0, u1 = uT + s * rf, uT + s * E.R_AL
        if abs(u1 - u0) < 0.4: u0, u1 = uT + s * E.R_AL - 0.2, uT + s * E.R_AL + 0.2
        rect(ax, u0, u1, E.Z_ALETA0, E.Z_B1 + E._v["FOR_C"], HORM, zo + 3)
        ax.plot([uT + s * E.R_CU, uT + s * E.R_AL], [E.Z_CU1, E.Z_ALETA0], color="k", lw=0.5, zorder=zo + 3)   # ménsula
    baranda_alz(ax, uT, E.R_B, E.Z_B1 + E._v["FOR_C"], E._v["BAR_B"], zo + 3)                                # barandilla abierta
    # tambor con ojos
    rect(ax, uT - E.R_T, uT + E.R_T, E.Z_B1 + E._v["FOR_C"], E.Z_T1, HORM, zo + 2)
    import ventanas as VT
    for h in VT.catalogo():                                                              # ojos y puerta del catálogo único
        o = np.array(h["n"])
        if o @ ED > -0.05: continue
        if h["grupo"] == "tambor ojos":
            ax.add_patch(Ellipse((u_of(h["p"]), (h["z0"] + h["z1"]) / 2), h["w"] * abs(o @ ED), h["w"], fc="0.2", ec="k", lw=0.4, zorder=zo + 3))
        elif h["grupo"] == "tambor puerta":
            uu = u_of(h["p"]); ww = h["w"] * abs(o @ ED)
            rect(ax, uu - ww / 2, uu + ww / 2, h["z0"], h["z1"], OSCU, zo + 3)
    # banda acristalada con montantes
    zb0 = E.Z_T1 - V["H_PT"]
    uB = u_of(E.P(V["OB_X"], V["OB_Y"]))
    rect(ax, uB - E.R_G, uB + E.R_G, zb0, E.Z_G1, VIDR, zo + 1)
    nm = int(2 * math.pi * E.R_G / 2.4)
    for k in range(nm):
        a = 2 * math.pi * k / nm; o = np.array([math.cos(a), math.sin(a)])
        if o @ ED < 0:
            uu = uB + E.R_G * (o @ EU); ax.plot([uu, uu], [zb0, E.Z_G1], color="0.9", lw=0.5, zorder=zo + 2)
    # visera, remate y lucernario
    pv = np.array(E.P(V["OV_X"], V["OV_Y"])); uv = u_of(pv)
    rect(ax, uv - E.R_V, uv + E.R_V, E.Z_G1, E.Z_V1, HORM, zo + 4)
    baranda_alz(ax, uv, E.R_V, E.Z_V1, 1.0, zo + 4)                                                      # barandilla abierta
    pr = np.array(E.P(V["OR_X"], V["OR_Y"])); ur = u_of(pr)
    rect(ax, ur - E.R_R, ur + E.R_R, E.Z_V1, E.Z_R1, HORM, zo + 4)
    rect(ax, ur - V["REM_ZR"], ur + V["REM_ZR"], E.Z_V1, E.Z_V1 + V["REM_ZH"], HORM, zo + 4)                      # zócalo (poyete) del remate
    for L_ in E.letrero():                                                                # letrero САЛЮТ
        nrm = np.array([math.cos(math.radians(L_["rot"])), math.sin(math.radians(L_["rot"]))])
        if nrm @ ED > 0.2: continue
        uu = u_of(L_["c"]); ww = L_["w"] * abs(nrm @ ED) + 0.3 * abs(nrm @ EU)
        rect(ax, uu - ww / 2, uu + ww / 2, L_["z0"], L_["z1"], dict(fc="#d9c36a", ec="k", lw=0.5), zo + 5)
    pl = np.array(E.P(V["LUC_X"], V["LUC_Y"])); ul = u_of(pl)
    ax.add_patch(Polygon([(ul - V["LUC_R"], E.Z_V1), (ul + V["LUC_R"], E.Z_V1), (ul, E.Z_V1 + V["LUC_H"] + 0.25)],
                         closed=True, fc="0.8", ec="k", lw=0.5, zorder=zo + 5))
    return uT


def base(ax, zo=30):
    L_C = V["L_C"]; uM = u_of(E.SWP(-L_C, 0)); uA1 = u_of(G["A1"]); uE90 = u_of(G["E90"])
    # ala larga y bar (al fondo)
    us = [u_of(p) for p in E.plantas_base()["P1"][3:7]]
    rect(ax, min(us), max(us), 0, E.Z_P1, HORM, 5)
    rect(ax, u_of((0, 20)), u_of((E.W_BAR + V["V_BAR"], 20)), E.Z_P1, E.Z_BAR_C, HORM, 5)
    # chaflán: planta baja retranqueada y banda de planta 1 con sus paños (restaurante / hotel)
    rect(ax, uA1, uE90, 0, E.Z_PB, OSCU, zo)
    rect(ax, uA1, uE90, E.Z_PB, E.Z_P1, HORM, zo + 1)
    import ventanas as VT
    for h in VT.catalogo():
        if h["grupo"] in ("chaflán restaurante", "chaflán hotel"):
            p, t = np.array(h["p"]), np.array(h["t"])
            a, b = u_of(p - t * h["w"] / 2), u_of(p + t * h["w"] / 2)
            rect(ax, a, b, h["z0"], h["z1"], VIDR, zo + 2)
    # ala corta: muro de ladrillo de planta baja y 1 tras la logia
    uL0, uL1 = uM + V["LOG_X0"], uM + V["LOG_X1"]
    rect(ax, uL1, uA1, 0, E.Z_P1, LADR, zo + 3)
    # logia: muro de medianera, planta baja oscura, antepecho, vidrio, pilar
    rect(ax, uM, uL0, 0, V["Z_VOL0"], HORM, zo + 3)
    rect(ax, uL0, uL1, 0, E.Z_PB + 0.2, OSCU, zo + 3)
    rect(ax, uL0, uL1, E.Z_PB + 0.2, E.Z_PB + 1.0, HORM, zo + 3)
    rect(ax, uL0, uL1, E.Z_PB + 1.0, V["Z_VOL0"], OSCU, zo + 3)
    for uu in np.linspace(uL0, uL1, 6)[1:-1]:
        ax.plot([uu, uu], [E.Z_PB + 1.0, V["Z_VOL0"]], color="0.8", lw=0.5, zorder=zo + 4)
    up = uM + V["LOG_PX"]
    rect(ax, up - 0.35, up + 0.35, E.Z_PB, V["Z_VOL0"], HORM, zo + 5)
    rect(ax, uL1 - 0.25, uL1, 0, V["Z_VOL0"], HORM, zo + 5)
    # bloque alto: cara inclinada / curva (hormigón) y cuerpo volado (ladrillo, peto y esquina de hormigón)
    ba = E.bloque_alto_poligono(); umax = max(u_of(p) for p in ba)
    uv1 = uM + V["VOL_L"]
    rect(ax, uv1, umax, E.Z_P1, E.Z_ALTO, HORM, zo + 6)
    rect(ax, uM, uv1, V["Z_VOL0"], E.Z_ALTO, LADR, zo + 7)
    rect(ax, uM, uv1, E.Z_ALTO - 0.6, E.Z_ALTO + 0.6, HORM, zo + 8)
    rect(ax, uv1 - 1.2, uv1, V["Z_VOL0"], E.Z_ALTO + 0.6, HORM, zo + 8)
    # edificio colindante (medianera)
    ax.add_patch(Rectangle((uM - 4, 0), 4, 20, fc="none", ec="0.5", lw=0.5, hatch="////", zorder=zo + 9))
    ax.text(uM - 2, 10, "edificio\ncolindante", fontsize=5, ha="center", rotation=90, color="0.4", zorder=zo + 10)
    return uM, uL0, up, uL1, uv1, uA1, uE90


def dibujar(ax, coord="l", cotas=True):
    """coord='l': u = x de la L recta; coord='e': u = P·(dirección de la calle) (para alinear con plantas giradas)"""
    import matplotlib.transforms as mt
    c = 0.0 if coord == "l" else float(KC @ EU - V["W_P"])
    antes = set(ax.get_children())
    uT = torre(ax)
    marks = base(ax)
    ax.plot([marks[0] - 6, uT + 30], [0, 0], color="k", lw=1.6, zorder=60)
    if cotas:
        import lineas as L
        uM, uL0, up, uL1, uv1, uA1, uE90 = marks
        pts = [uM, uL0, uL1, uv1, uA1, uT, uE90]
        for a, b in zip(pts, pts[1:]):
            if b - a > 0.2: L.cota(ax, (a, 0), (b, 0), -2.2, "", fs=5)
        L.cota(ax, (uM, 0), (uA1, 0), -4.4, "X", fs=5.5)
        for z, t in ((0, "±0,00"), (E.Z_PB, "techo PB"), (E.Z_P1, "planta 1 / terraza"),
                     (E.Z_ALTO, "bloque alto / bar"), (E.Z_CU1, "base del barril"), (E.Z_B1, "cub. habitaciones"),
                     (E.Z_T1, "tambor"), (E.Z_G1, "banda"), (E.Z_V1, "visera"), (E.Z_R1, "remate")):
            L.nivel(ax, uT + 18, z, t)
    if c:
        tr = mt.Affine2D().translate(c, 0) + ax.transData
        for a in set(ax.get_children()) - antes:
            try: a.set_transform(tr)
            except Exception: pass
    return uT + c, marks[0] + c


if __name__ == "__main__":
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(14, 12))
    uT, uM = dibujar(ax)
    ax.set_xlim(uM - 6, uT + 32); ax.set_ylim(-6, 52); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("ALZADO 3 – CALLE (dibujado desde el cuadro de cotas)", loc="left")
    fig.savefig("ALZADO_CALLE.png", dpi=90, bbox_inches="tight")
