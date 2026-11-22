"""FASE 1 – esqueleto: escala y eje de la torre (Z06 barril, Z10 columna) contra las fotos de referencia.
Para cada foto: camara calibrada SOLO con barril y columna; residuos por elemento; ficha con la zona del plano
(aristas del modelo, rojo) superpuesta al recorte de la foto, y el recorte de la foto limpio al lado."""
import json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
from manifold3d import Manifold
import edificio as E, calib_e as C

IMG = '/tmp/claude-0/-home-user-PabloRamonBenitez/6aecfee3-0e37-5370-9a32-0a87a530abec/images/'
FOTOS = {
    "C04": dict(f="9.webp", az=(20, 90), el=(-3, 25), fov=(3, 25), hcam=(2.0, 5.0),
                obs=[("barril_sup", 105, 502, 366), ("barril_inf", 108, 500, 598), ("columna", 246, 330, 720)]),
    "C01": dict(f="1.webp", az=(20, 100), el=(10, 50), fov=(10, 50),
                obs=[("barril_sup", 170, 550, 262), ("barril_inf", 187, 532, 476), ("columna_pie", 322, 388, 652)]),
    "C03": dict(f="2.webp", az=(-10, 80), el=(-3, 30), fov=(5, 40), hcam=(1.6, 5.0),
                obs=[("barril_sup", 780, 1365, 410), ("barril_inf", 795, 1350, 760)]),
}
EXTRA = {  # comprobacion independiente (no usada en la calibracion): tambor, visera, remate
    "C04": [("tambor", 133, 485, 335), ("visera", 110, 442, 245), ("remate", 240, 385, 190)],
    "C01": [("tambor", 190, 525, 232), ("remate", 293, 417, 45)],
    "C03": [("tambor", 805, 1332, 385), ("visera", 785, 1252, 305), ("remate", 975, 1198, 180)],
}


def zona_modelo(m, zonas):
    """recorta el modelo al volumen de las zonas Z06 (barril) y Z10 (columna)"""
    T = E.T; v = []
    if "Z06" in zonas:
        v.append(Manifold.cylinder(E.Z_B1 + 1.2 - E.Z_ALETA0 + 0.1, E.R_AL + 0.5, E.R_AL + 0.5, 96).translate((T[0], T[1], E.Z_ALETA0 - 0.1)))
    if "Z10" in zonas:
        v.append(Manifold.cylinder(E.Z_CU0, E.R_COL + 0.3, E.R_COL + 0.3, 64).translate((T[0], T[1], 0)))
    return m ^ Manifold.batch_boolean(v, __import__("manifold3d").OpType.Add)


if __name__ == "__main__":
    M = E.edificio()
    Mz = zona_modelo(M, {"Z06", "Z10"})
    res = {}
    fig, axs = plt.subplots(len(FOTOS), 2, figsize=(16, 7.2 * len(FOTOS)))
    for i, (k, d) in enumerate(FOTOS.items()):
        best, (W, H) = C.calibrar(IMG + d["f"], d["obs"], d["az"], d["el"], d["fov"], d.get("hcam"))
        if d.get("hcam"): best = (best[0], best[1], best[2][1:])
        K = C.cam(best[1], W, H)
        r_cal = best[2].reshape(-1, 3)
        r_ext = C.residuos(best[1], EXTRA[k], W, H).reshape(-1, 3)
        res[k] = dict(rms=round(best[0], 1), cam=[round(float(v), 2) for v in best[1]],
                      calib={o[0]: [round(float(v), 1) for v in rr] for o, rr in zip(d["obs"], r_cal)},
                      control={o[0]: [round(float(v), 1) for v in rr] for o, rr in zip(EXTRA[k], r_ext)})
        e, occ = C.aristas(Mz, K)
        ys, xs = np.nonzero(occ)
        x0, x1 = max(xs.min() - 40, 0), min(xs.max() + 40, W); y0, y1 = max(ys.min() - 40, 0), min(ys.max() + 40, H)
        foto = np.asarray(Image.open(IMG + d["f"]).convert("RGB")).astype(float)
        sup = foto.copy(); sup = sup * 0.75 + 255 * 0.25; sup[e] = (255, 0, 0)
        axs[i, 0].imshow(sup[y0:y1, x0:x1].astype(np.uint8)); axs[i, 0].axis("off")
        axs[i, 0].set_title(f"{k} ({d['f']}): Z06 + Z10 del plano (rojo) sobre la foto – error de calibración {best[0]:.1f} px", fontsize=9, loc="left")
        axs[i, 1].imshow(foto[y0:y1, x0:x1].astype(np.uint8)); axs[i, 1].axis("off")
        txt = "control independiente (px, izq/der/altura): " + "; ".join(f"{kk} {vv}" for kk, vv in res[k]["control"].items())
        axs[i, 1].set_title("foto limpia\n" + txt, fontsize=7.5, loc="left")
    fig.tight_layout(); fig.savefig("FASE1_fichas.png", dpi=70)
    json.dump(res, open("FASE1_resultados.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps(res, indent=1, ensure_ascii=False))
