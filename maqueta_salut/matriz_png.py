"""MATRIZ_v2.png: la tabla zonas × fotos de MATRIZ_ZONAS_FOTOS_v2.xlsx en una imagen (OK verde, ≈ amarillo, NO rojo)."""
import openpyxl
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
ws = openpyxl.load_workbook("MATRIZ_ZONAS_FOTOS_v2.xlsx")["Matriz v2"]
rows = list(ws.iter_rows(values_only=True)); hdr = rows[0]; body = rows[1:]
nc = len(hdr) - 9
C = {"OK": "#9fd88a", "≈": "#ffe28a", "NO": "#f08080", "?": "#dddddd", "–": "white"}
fig = plt.figure(figsize=(26, 0.42 * len(body) + 3)); ax = fig.add_axes([0.01, 0.01, 0.98, 0.9]); ax.axis("off")
W0 = 16
for j, h in enumerate(hdr[3:3 + nc]):
    ax.text(W0 + j + 0.5, len(body) + 0.2, str(h).replace("\n", " "), rotation=60, fontsize=7.5, ha="left", va="bottom")
for i, r in enumerate(body):
    y = len(body) - 1 - i
    ax.text(0, y + 0.5, f"{r[0]}  {r[1]}"[:78], fontsize=8, va="center")
    for j, v in enumerate(r[3:3 + nc]):
        ax.add_patch(Rectangle((W0 + j, y), 1, 1, fc=C.get(v, "white"), ec="0.6", lw=0.4))
        if v and v != "–": ax.text(W0 + j + 0.5, y + 0.5, v, fontsize=7, ha="center", va="center")
    ax.text(W0 + nc + 0.3, y + 0.5, f"OK {r[-6]} · ≈ {r[-5]}" + (f" · NO {r[-4]}" if r[-4] else ""), fontsize=7.5, va="center")
tot = {s: sum(1 for r in body for v in r[3:3 + nc] if v == s) for s in ("OK", "≈", "NO", "?")}
ax.set_xlim(0, W0 + nc + 5); ax.set_ylim(0, len(body) + 4)
fig.suptitle(f"MATRIZ ZONAS × FOTOS v2 – ronda absoluta 26/11 · OK {tot['OK']} · ≈ {tot['≈']} · NO {tot['NO']} · ? {tot['?']}",
             fontsize=15, x=0.01, ha="left", weight="bold")
fig.savefig("MATRIZ_v2.png", dpi=70); print(tot)
