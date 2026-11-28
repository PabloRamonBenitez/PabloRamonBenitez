"""Esquema para el usuario (28/11): dónde está cada cosa (Mac, móvil, nube, GitHub, Gmail/Drive, internet) y qué es el «entorno».
Hoja de explicación, no del juego de planos: se hace en español y sin el traductor de planos."""
import traduccion
traduccion.ACTIVO = False
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(16, 10.5))
ax.set_xlim(0, 100); ax.set_ylim(-1, 72); ax.axis("off")
fig.suptitle("¿Dónde está cada cosa? Tu Mac, tu móvil, la nube, GitHub e internet", fontsize=16, weight="bold", x=0.02, ha="left", y=0.975)


def caja(x, y, w, h, titulo, lineas, fc):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.25,rounding_size=1.2", fc=fc, ec="0.25", lw=1.4))
    ax.text(x + 1.4, y + h - 1.6, titulo, fontsize=10.5, weight="bold", va="top")
    for i, t in enumerate(lineas):
        ax.text(x + 1.4, y + h - 5.0 - i * 3.6, t, fontsize=8.6, va="top")


def flecha(p, q, texto="", tx=None, ty=None, ls="-", color="0.1", ha="center"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="<|-|>" if ls == "<->" else "-|>", mutation_scale=14, lw=1.4, color=color,
                                 linestyle="-" if ls in ("-", "<->") else (0, (4, 3))))
    if texto:
        mx, my = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2) if tx is None else (tx, ty)
        ax.text(mx, my, texto, fontsize=8.2, ha=ha, va="center", color="0.15",
                bbox=dict(fc="white", ec="none", pad=0.6))


# ---- TU ORDENADOR (Mac)
caja(2, 42, 30, 26, "TU ORDENADOR (Mac)", [
    "• App Claude de escritorio: la ventana de tu captura.",
    "• Carpeta Workspace: TU copia de los archivos.",
    "• Chrome con la extensión de Claude (solo si lo conectas).",
    "• No se actualiza sola: se sincroniza con GitHub a mano.",
], "#e8f0fb")

# ---- TU MÓVIL
caja(2, 20, 30, 16, "TU MÓVIL", [
    "• App Claude: ves y sigues las sesiones de la nube.",
    "• No tiene los archivos del proyecto.",
], "#eef7ea")

# ---- NUBE
caja(46, 40, 52, 28, "NUBE DE ANTHROPIC (sesiones en la nube)", [
    "• Cada sesión es un ordenador virtual con una copia del repositorio.",
    "• Esta conversación («Salyt hotel Kyiv scale model») vive aquí.",
    "• No ve tu Mac hasta que conectas tu carpeta y lo apruebas.",
    "• Sus conectores: Gmail y Drive (esta sesión los usa).",
    "• Internet: bloqueado en esta sesión (por eso no abro las webs).",
], "#fff4e0")

# ---- GITHUB
caja(46, 22, 26, 13, "GITHUB (copia del proyecto)", [
    "• Rama ccr-3578fcb9-cjje54.",
    "• Commit + push: subir. Pull: bajar.",
], "#f1ecfa")

# ---- GMAIL / DRIVE
caja(74, 22, 24, 13, "GMAIL Y DRIVE", [
    "• Tu correo y tus archivos.",
    "• Aquí están el STL y el borrador.",
], "#fbeaea")

# ---- ENTORNO (explicación)
caja(2, 2, 30, 14, "ENTORNO = configuración de la nube", [
    "Qué webs puede abrir, qué repos ve y sus claves.",
    "«Default»: sin webs de proveedores (el de ahora).",
    "«pabloramonbenitez-proveedores»: con webs permitidas.",
], "#f7f7f7")

# ---- INTERNET
caja(46, 2, 52, 13, "INTERNET (webs de los proveedores)", [
    "• Aquí, en esta sesión: bloqueado. Por eso no veo sus precios ni correos.",
    "• En el entorno «pabloramonbenitez-proveedores»: abierto (hay que abrir allí una sesión nueva).",
], "#eef3f8")

# ---- FLECHAS
flecha((32, 58), (46, 58), "abres la sesión desde la app", tx=39, ty=61)
flecha((46, 52), (32, 52), "solo si conectas tu carpeta (pide tu aprobación)", tx=39, ty=49.5, ls="--", color="0.4")
flecha((34, 29), (46, 45), "ves la misma sesión", tx=36.8, ty=36.5, ha="left")
flecha((32, 44), (46, 31), "git: a mano (tu copia)", tx=38.5, ty=40.7, ls="--", color="0.4", ha="right")
flecha((57, 40), (57, 35), "push / pull", tx=60.5, ty=37.5, ha="left")
flecha((84, 40), (84, 35), "conectores", tx=86.5, ty=37.5, ha="left")

# ---- REGLA
ax.text(2, 70, "Regla: la nube no ve tu Mac, y tu Mac no ve la nube, salvo que los conectes. GitHub es el puente entre los dos.",
        fontsize=9.5, weight="bold", va="top", color="0.15")

fig.savefig("ESQUEMA_DONDE_ESTA_CADA_COSA.png", dpi=110, bbox_inches="tight"); print("ok")
