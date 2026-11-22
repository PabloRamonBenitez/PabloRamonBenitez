"""Busca longitud del chaflan (L_CHF), posicion de la torre sobre el (T_POS) y eje de la escalera (ESC_X)
con camaras calibradas solo con la torre (C04, C02). La camara va solidaria a la torre: al mover la torre en la
planta, se traslada la camara con ella. Solo ANOTA el resultado."""
import json, math, numpy as np, cotas as K, calib_e as C, cal_gen as G
B = json.load(open("cams_base.json")); T0 = np.array(B["T"])
def camara(key, W, H, T):
    k = C.cam(B[key]["cam"], W, H); d = np.array([T[0] - T0[0], T[1] - T0[1], 0.0])
    return (k[0] + d,) + tuple(k[1:])
def evalua(lch, tpos, escx, detalle=False):
    K.V["L_CHF"], K.V["T_POS"], K.V["ESC_X"] = lch, tpos, escx
    g = K.planta(); T = g["T"]
    k4 = camara("R04", 874, 890, T); k2 = camara("R02", 732, 650, T)
    p = lambda kk, q: C.proj(kk, np.array(q, float))[0]
    r = {}
    r["C04 fin chaflán (hotel) x=455"] = p(k4, [*g["C"], 7.3])[0] - 455
    ys = T[1] + 10, T[1] + K.V["R_AL"] + 1
    xs = [p(k4, [x, y, 25])[0] for x in (escx - K.V["ESC_W"] / 2, escx + K.V["ESC_W"] / 2) for y in ys]
    r["C04 escalera oculta (borde dcho <= 495)"] = max(0.0, max(xs) - 495)
    A = np.array([K.V["W_P"], g["Q"][1] + 3, 8.3]); Bf = np.array([K.V["W_P"], K.V["L_L"], 8.3])
    r["C02 arista ala por (500,415)"] = G.dl(k2, A, Bf, (500, 415))
    q = p(k2, Bf); r["C02 fin ala (628,357) dx"] = q[0] - 628; r["C02 fin ala dy"] = q[1] - 357
    r["escalera dentro de la L"] = 20 * max(0.0, K.V["ESC_W"] / 2 - escx) + 20 * max(0.0, escx + K.V["ESC_W"] / 2 - K.V["W_P"])
    v = np.array(list(r.values()))
    return (float(np.sqrt(np.mean(v ** 2))), r) if detalle else float(np.sqrt(np.mean(v ** 2)))
best = None
for lch in np.arange(12, 36.1, 1.0):
    for tp in np.arange(0.30, 0.901, 0.025):
        for ex in np.arange(5.0, 7.75, 0.5):
            e = evalua(lch, tp, ex)
            if best is None or e < best[0]: best = (e, lch, tp, ex)
e, r = evalua(*best[1:], detalle=True)
print("MEJOR: L_CHF %.1f  T_POS %.3f  ESC_X %.2f  error %.1f px" % (best[1], best[2], best[3], e))
for k, v in r.items(): print("  %-40s %7.1f" % (k, v))
e0, r0 = evalua(20.0, 0.58, 5.0, detalle=True)
print("ACTUAL (20 / 0,58 / 5,0): error %.1f" % e0)
for k, v in r0.items(): print("  %-40s %7.1f" % (k, v))
json.dump(dict(mejor=dict(L_CHF=best[1], T_POS=best[2], ESC_X=best[3], error=e, res=r), actual=dict(error=e0, res=r0)), open("IMPLANTACION.json", "w"), indent=1)
