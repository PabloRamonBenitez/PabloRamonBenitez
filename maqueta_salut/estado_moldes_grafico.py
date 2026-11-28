"""Gráfico de estado de moldes y proveedores (28/11/2026): una vista para ver de un vistazo qué hay que contestar."""
import traduccion
traduccion.ACTIVO = False
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

filas = [
    ("MoldeSilicona (Etsy)", "revisaron el STL, dicen que comentan", "CONTESTAR", "texto 1"),
    ("HOUSEOFMOLDS (Etsy)", "pidió el archivo", "CONTESTAR", "texto 2"),
    ("3DDeluxeStore (Etsy)", "pidió imagen o modelo", "CONTESTAR", "texto 3"),
    ("PLAybelope (Etsy)", "pidió el STL en Drive", "CONTESTAR", "texto 2 adaptado"),
    ("StudioRollins (Etsy)", "pide imagen; no consta en la lista", "REVISAR HILO", "texto 4"),
    ("MinghuiLink (correo)", "propuesta enviada 27/11, sin precio", "CONTESTAR", "texto 5"),
    ("moldesilicona.com, Modelarte, Milab3D, Flossy", "sin respuesta", "ESPERAR 48 h", "reenviar"),
    ("BK Silicone (correo)", "rechazó por complejidad", "CERRADO", "—"),
    ("Hubs / JLC3DP (web)", "presupuesto de la pieza A", "PENDIENTE", "sesión local"),
    ("FormX (web, silicona)", "precio y formato de kit", "PENDIENTE", "sesión local"),
]
colores = {"CONTESTAR": "#f6d8a6", "REVISAR HILO": "#f6e7a6", "ESPERAR 48 h": "#e6e6e6", "CERRADO": "#f3c7c7", "PENDIENTE": "#cfe3f7"}

fig, ax = plt.subplots(figsize=(14, 7.2)); ax.axis("off")
fig.suptitle("Hotel Salut · moldes y proveedores · 28/11", fontsize=16, weight="bold", x=0.02, ha="left", y=0.97)
fig.text(0.02, 0.905, "Planteamiento: cuatro modelos (original y menos detalle, cada uno en versión de una pieza y desmontable en tambor + base).\n"
         "Orden: primero imprimir los másters en resina; después el molde de silicona.", fontsize=10, va="top")
cols = ["Proveedor", "Qué ha pasado", "Estado", "Texto a usar"]
xs = [0.02, 0.36, 0.70, 0.84]
y0, dy = 0.74, 0.066
for x, c in zip(xs, cols):
    fig.text(x, y0 + 0.035, c, fontsize=11, weight="bold", va="center")
fig.add_artist(plt.Line2D([0.01, 0.99], [y0 + 0.012, y0 + 0.012], color="0.3", lw=1, transform=fig.transFigure))
for i, (p, q, e, t) in enumerate(filas):
    y = y0 - i * dy
    fig.patches.append(plt.Rectangle((0.01, y - 0.028), 0.98, dy - 0.008, transform=fig.transFigure, fc=colores.get(e, "white"), ec="none", alpha=0.55, zorder=0))
    fig.text(xs[0], y, p, fontsize=10, va="center")
    fig.text(xs[1], y, q, fontsize=10, va="center")
    fig.text(xs[2], y, e, fontsize=10, va="center", weight="bold")
    fig.text(xs[3], y, t, fontsize=10, va="center")
fig.text(0.02, 0.03, "Documento completo y textos: ESTADO_MOLDES_Y_PROVEEDORES (Drive, carpeta «Stl salyt»). Pendiente de Pablo: confirmar la división de la maqueta.",
         fontsize=9, va="center", style="italic")
fig.savefig("ESTADO_MOLDES_GRAFICO.png", dpi=120); print("ok")
