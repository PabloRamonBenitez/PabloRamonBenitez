"""Zona VENTANAS del alzado 2 dibujada SOLO con proporciones medidas en las fotos (sin cámara).
Unidades: H = suelo→coronación del peto (vertical exacta en F73); S = intereje (fuga ajustada en F73, F01, F47).
Queda UNA escala libre (S en metros) que no fija ninguna foto por sí sola: se dibujan sus dos extremos."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
P = dict(hueco=0.47, macizo=1.13, n_alta=11, n_baja=7, dA=0.743, aA=0.545, dB=0.338)
fig, axs = plt.subplots(2, 1, figsize=(14, 6.5))
for ax, (S, H, tit) in zip(axs, ((3.55, 8.5, "S = 3,55 m (huecos cuadrados, como dices)"), (2.94, 8.5, "S = 2,94 m (si la concha acaba a 35,13 m del testero)"))):
    w = P["hueco"] * S; hA = (P["dA"] - P["aA"]) * H
    x_esq = 0.0
    for i in range(P["n_alta"]):
        x = x_esq + P["macizo"] * S - w / 2 + i * S       # centro del hueco 1 a 'macizo' interejes de la esquina
        ax.add_patch(Rectangle((x, P["aA"] * H), w, hA, fc="0.85", ec="k", lw=0.8))
        if i < P["n_baja"]:
            ax.add_patch(Rectangle((x, P["dB"] * H - hA), w, hA, fc="0.85", ec="k", lw=0.8))
            if i == 4: ax.add_patch(Rectangle((x, 0), w, P["dB"] * H - hA - 0.15, fc="none", ec="k", lw=0.8, ls="--"))
    L = P["macizo"] * S + (P["n_alta"] - 1) * S + 2
    ax.plot([0, L], [H, H], "k", lw=1.2); ax.plot([0, L], [0, 0], "k", lw=1.5); ax.plot([0, 0], [0, H], "k", lw=1.5)
    ax.text(0.2, H + 0.25, "testero", fontsize=7)
    ax.set_xlim(L + 0.5, -1); ax.set_ylim(-0.5, H + 1); ax.set_aspect("equal"); ax.set_title(tit, fontsize=9, loc="left")
    ax.text(L, -0.45, f"hueco {w:.2f} × {hA:.2f} m · intereje {S} · macizo final {P['macizo'] * S - w / 2:.2f} m · 11 arriba / 7 abajo · elemento claro bajo el 5º (¿puerta? F47, F01)", fontsize=7, ha="left")
fig.suptitle("ALZADO 2 · zona de ventanas desde PROPORCIONES (F73 verticales; F73, F01, F47 fila de ventanas)", fontsize=10, x=0.01, ha="left")
fig.savefig("PROP_ALZADO2_VENTANAS.png", dpi=90, bbox_inches="tight")
