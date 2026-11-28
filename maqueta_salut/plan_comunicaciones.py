"""Gráfico de comunicaciones y objetivos del proyecto Hotel Salut (28/11/2026). Para el proyecto continuo: una vista de todo."""
import traduccion
traduccion.ACTIVO = False
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(16, 10.5)); ax.set_xlim(0, 100); ax.set_ylim(0, 77); ax.axis("off")
fig.suptitle("Hotel Salut · comunicaciones y objetivos · 28/11/2026", fontsize=17, weight="bold", x=0.02, ha="left", y=0.985)

COL = {"ESPERA": "#fde7b0", "PENDIENTE": "#cfe3f7", "CERRADO": "#f2c6c6", "HECHO": "#cfeccf"}


def caja(x, y, w, h, titulo, color="#f4f4f4"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.25,rounding_size=1.0", fc=color, ec="0.3", lw=1.2))
    ax.text(x + 1.2, y + h - 1.4, titulo, fontsize=11, weight="bold", va="top")


def fila(x, y, texto, estado, w=50):
    ax.add_patch(FancyBboxPatch((x, y - 0.9), w, 2.9, boxstyle="round,pad=0.15,rounding_size=0.5", fc=COL[estado], ec="none"))
    ax.text(x + 0.8, y + 0.6, texto, fontsize=8.8, va="center")


# ---- OBJETIVO
caja(1, 58, 98, 11, "OBJETIVO", "#e8f0fb")
ax.text(2.5, 63.5, "Tener la maqueta del Hotel Salut en cuatro modelos (original y menos detalle, cada uno en una pieza y en versión desmontable: tambor + base),\n"
        "impresos en resina, con moldes de silicona y piezas de hormigón que encajen. Hoy: confirmar la división y elegir proveedor de impresión y de molde.",
        fontsize=10, va="center")

# ---- CORREO
caja(1, 30, 47, 25, "CORREO (Gmail)")
fila(2, 50, "MinghuiLink (China): propuesta de dos piezas enviada 28/11. Espera precio y plazo.", "ESPERA", w=44)
fila(2, 46.5, "BK Silicone: rechazó (demasiado complejo). Cerrado.", "CERRADO", w=44)
fila(2, 43, "Flossy Candle: sin respuesta (25/11 y seguimiento 27/11).", "ESPERA", w=44)
fila(2, 39.5, "moldesilicona.com: sin respuesta (25/11 y seguimiento 27/11).", "ESPERA", w=44)
fila(2, 36, "Modelarte: sin respuesta (25/11 y seguimiento 27/11).", "ESPERA", w=44)
fila(2, 32.5, "Milab3D: sin respuesta (25/11 y seguimiento 27/11).", "ESPERA", w=44)

# ---- ETSY
caja(52, 30, 47, 25, "ETSY (lo envía la sesión local)")
fila(53, 50, "MoldeSilicona (Alfredo y Karina): revisaron el STL. Texto 1.", "PENDIENTE", w=42)
fila(53, 46.5, "HOUSEOFMOLDS (Tania): pidió el archivo. Texto 2.", "PENDIENTE", w=42)
fila(53, 43, "3DDeluxeStore (Scott): pidió imagen o modelo. Texto 3.", "PENDIENTE", w=42)
fila(53, 39.5, "PLAybelope (Razieh): pidió el STL en Drive. Texto 4 (inglés).", "PENDIENTE", w=42)
fila(53, 36, "StudioRollins: pide imagen. Texto 5. Hay que mandar renders.", "PENDIENTE", w=42)
fila(53, 32.5, "Sesión de Etsy iniciada por Pablo. Nada enviado todavía.", "HECHO", w=42)

# ---- WEB / PRESUPUESTOS
caja(1, 2, 98, 25, "PRESUPUESTOS EN WEB (sin contacto todavía)")
fila(2, 22.5, "Hubs / Protolabs: pieza A (142 × 190 × 150 mm) en resina SLA. Sube la sesión local con Chrome. Pieza B después.", "PENDIENTE", w=94)
fila(2, 19, "JLC3DP, Craftcloud, 3DEXPERIENCE Make, Xometry Europe: presupuesto al subir el STL (mismo archivo para todos).", "PENDIENTE", w=94)
fila(2, 15.5, "España (Innovatia3D, Additium3D, Dynamical 3D, Aitiip, Pantur): buscar correo en su web y escribir.", "PENDIENTE", w=94)
fila(2, 12, "FormX (silicona Smooth-On, España): precio y formato de kit. Para el molde si lo hace Pablo.", "PENDIENTE", w=94)
fila(2, 8.5, "Molde de silicona: lo hace Pablo (silicona de estaño o platino) o lo encarga un proveedor. Se decide con los presupuestos.", "PENDIENTE", w=94)

# ---- PRÓXIMOS PASOS (en la parte baja)
ax.text(2, 0.6, "Orden: 1) confirmar división (DESMONTABLE_DIVISION.png)  2) enviar textos Etsy  3) presupuesto pieza A y B  4) renders para StudioRollins  "
        "5) generar desmontables  6) buscar correos españoles  7) elegir proveedor.", fontsize=9, va="bottom", style="italic")

ax.add_patch(FancyBboxPatch((1, 60.2), 1, 1, boxstyle="square", fc="none", ec="none"))
leyenda = [("ESPERA", "esperando respuesta"), ("PENDIENTE", "falta hacerlo"), ("CERRADO", "cerrado"), ("HECHO", "hecho")]
for i, (k, t) in enumerate(leyenda):
    ax.add_patch(FancyBboxPatch((58 + i * 11, 73.8), 1.6, 1.3, boxstyle="square", fc=COL[k], ec="0.3"))
    ax.text(60 + i * 11 + 0.8, 74.4, t, fontsize=8.5, va="center")

fig.savefig("PLAN_COMUNICACIONES.png", dpi=120, bbox_inches="tight"); print("ok")
