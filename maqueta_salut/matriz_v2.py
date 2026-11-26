"""MATRIZ ZONAS × FOTOS v2 (26/11): estado real de cada zona en cada foto tras todos los cambios.
OK = comprobado (medida o superposición) · ≈ = coincide en forma, medida aproximada · NO = conflicto abierto
? = la zona se ve en la foto pero no se ha vuelto a contrastar tras los últimos cambios · – = no se ve."""
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
import zonas_def as Z

COLS = [  # (col, foto, descripción)
 ("C01", "F01", "aérea 1984 (triangulación A–B–C–D)"), ("C02", "F23", "aérea lejana 1984"), ("C03", "F02/F14", "época, desde la plaza"),
 ("C04", "F09", "frontal teleobjetivo (7 forjados)"), ("C05", "F18", "color actual desde la plaza"), ("C08", "F15", "época, base con autobuses"),
 ("C09", "F19", "calle, lejos"), ("C10", "F08", "aérea desde detrás"), ("C11", "F04/F06", "barril de cerca"), ("C12", "F10", "remate de cerca"),
 ("C13", "F11", "escalera de cerca"), ("C14", "F12", "encuentro escalera–barril"), ("C15", "F13", "escalera lateral"), ("C16", "F22", "maqueta (solo organización)"),
 ("C17", "F35", "Bing cenital"), ("C18", "F38", "Bing con medidas"), ("C19", "F47", "terraza y ala larga 1984"), ("C20", "F71", "rampa al techo del restaurante"),
 ("C21", "F73", "desde el testero"), ("C22", "F76", "maqueta: rampas"), ("C23", "F58", "cenital: escalera en el ala"),
 ("C24", "ALAMY", "casi alzado: código de la verdad de la torre"), ("C25", "F78", "base: cuello, lucernarios, pie de escalera"),
 ("C26", "ESC-LAT", "escalera de frente/lateral (juntas = forjados)"), ("C27", "ESC-FRENTE", "escalera de frente (2 fotos del usuario)"),
 ("C28", "DRON", "dron: tambor, terraza, muro inclinado, letras"), ("C29", "BOOKING", "concha desde la plaza (líneas roja/amarilla/verde)"),
 ("C30", "FRONTAL", "ala corta frontal (logia, vuelo)"), ("C31", "F70", "postal 1984 frontal (paso de forjados)")]
OLD = ["C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08", "C09", "C10", "C11", "C12", "C13", "C14", "C15", "C16", "C17", "C18"]

E = {  # evidencias documentadas en la conversación (zona -> {col: (estado, nota)})
 "Z01": {"C24": ("OK", "MGF: 7,62 m sobre la visera, +50,81; letras 5 planas"), "C04": ("OK", "+50,95 con corrección de profundidad"), "C28": ("≈", "letras planas sobre estructura")},
 "Z02": {"C24": ("OK", "canto 1,89; R 11,7; eje 4,46"), "C04": ("≈", "cara sup. +43,6 frente a +43,18 (0,4)"), "C28": ("≈", "barandilla abierta")},
 "Z03": {"C24": ("OK", "2,56; R 9,45; eje 2,75"), "C04": ("OK", "+41,37")},
 "Z04": {"C24": ("OK", "5,68; Ø 27,0; 5 ojos ≤0,4 m; lado ciego"), "C27": ("OK", "puerta del tambor en lugar de ojo"), "C28": ("≈", "tubos de ojos")},
 "Z05": {"C24": ("OK", "barandilla 0,85"), "C28": ("OK", "peto cortado en la escalera")},
 "Z06": {"C24": ("OK", "forjados ≤0,05; canto 0,59, poyete 0,78, ranura 0,27; 19 aletas, giro 14,21°"), "C04": ("OK", "7 forjados, rms 0,02"), "C26": ("OK", "juntas de lamas cada 3,10")},
 "Z07": {"C04": ("OK", "+13,90")},
 "Z08": {"C25": ("≈", "aristas de las aletas bajo el barril")},
 "Z09": {"C04": ("OK", "+9,03 (7 forjados + profundidad)"), "C03": ("OK", "F14: +9,02 aparente / ≈ +9,4"), "C31": ("OK", "+9,05 aparente / +9,2"), "C25": ("≈", "pirámides casi tocan el cuello")},
 "Z32": {"C25": ("OK", "6 pequeñas, 33°–100°, en el camino de la rampa (usuario 26/11)")},
 "Z11": {"C04": ("OK", "X 12,8; 6 paños"), "C05": ("OK", "5 y pico")},
 "Z13": {"C04": ("OK", "Y 10,1; 4 paños"), "C05": ("OK", "4 y pico; esquina a 90°")},
 "Z16": {"C30": ("OK", "logia, pilar, ladrillo ciego"), "C01": ("OK", "triangulación A–B")},
 "Z17": {"C30": ("≈", "")},
 "Z18": {"C01": ("OK", "A–B 7,3 · A–C 16,66 · A–D 106,5/106,7 · D–C 1,5 %"), "C30": ("≈", "")},
 "Z19": {"C01": ("OK", "vuelo 1,2"), "C30": ("≈", "")},
 "Z20": {"C01": ("?", "teoría del usuario, sin foto que la confirme")},
 "Z34": {"C17": ("≈", "aéreas actuales")},
 "Z21": {"C29": ("OK", "rojo P2 convexo y verde G3 (usuario 26/11); sin retranqueo de PB tras el arco"), "C22": ("≈", "giro H1 confirmado"), "C20": ("≈", "")},
 "Z24": {"C21": ("OK", "11 + 7 huecos, alturas exactas"), "C01": ("OK", "11/7"), "C19": ("OK", "11/7")},
 "Z25": {"C18": ("OK", "bar 6,21; tramo sin bar 7,81"), "C21": ("≈", ""), "C19": ("≈", ""), "C20": ("≈", "")},
 "Z26": {"C19": ("≈", "")},
 "Z27": {"C21": ("OK", "testero, puerta, porche")},
 "Z35": {"C20": ("OK", "rampa al techo (usuario)"), "C22": ("≈", "")},
 "Z29": {"C26": ("OK", "remate 2,97; frente 6,0"), "C27": ("OK", "16 lamas; cuña 20,2°; 2 m hasta el corte"), "C28": ("OK", "muro de coronación inclinada"), "C24": ("OK", "borde de silueta −16,2; +40,8→+41,6"), "C23": ("≈", "dentro del ala")},
 "Z30": {"C27": ("OK", "cristalera con dintel, rellanos, borde dcho. con lamas")},
 "Z33": {"C25": ("≈", "losa blanca, núcleo, celosía"), "C27": ("≈", "losa a +12,2 por el paso de la rampa; F78 sugería +11–11,5")},
}
CONFLICTOS = [
 ("Z09", "Base del cuello", "F09 +9,03 · F70 +9,2 · F14 +9,0/9,4", "RESUELTO 26/11: Z_CU0 = 9,20 (DUDA1_BASE_CUELLO.png)"),
 ("Z21", "Perfil de la concha", "Booking + F24", "RESUELTO 26/11: P2 convexo (z = 7,2 (1 − u²)) y arco G3 (horizontal 27 %, al suelo 42 %)"),
 ("Z32", "Lucernarios bajo el cuello", "F78 + usuario", "RESUELTO 26/11: 6 de 1,0 m, r 4,7, 33°–100°"),
 ("Z33", "Losa de arranque de la escalera", "F78 +11–11,5 frente al paso de la rampa (exige ≥ +12,1)", "decidir"),
 ("Z20", "Línea posterior del ala corta", "teoría del usuario, sin foto", "fondo del ala corta estimado (W_C 12,74)"),
 ("Z02", "Cara superior de la visera", "Alamy +43,18 / F09 +43,6", "se sigue a Alamy"),
 ("—", "U de 180° y curva abierta de la rampa (planta de cubiertas)", "foto de la base con trazos del usuario", "sin incorporar"),
]

wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Matriz v2"
F = {"OK": "B7E1A1", "≈": "FFE699", "NO": "F4A6A6", "?": "E7E6E6", "–": "FFFFFF"}
hdr = ["Zona", "Descripción", "Grupo"] + [f"{c}\n{f}" for c, f, _ in COLS] + ["OK", "≈", "NO", "?", "visibles", "estado"]
ws.append(hdr)
old = openpyxl.load_workbook("MATRIZ_ZONAS_FOTOS.xlsx")["Matriz zonas x fotos"]
vis = {}
for r in old.iter_rows(min_row=2, values_only=True):
    if r[0] and str(r[0]).startswith("Z"):
        vis[r[0]] = {OLD[i]: r[3 + i] for i in range(len(OLD))}
notas = openpyxl.Workbook().active
for k, n, g, t, d in Z.ZONAS:
    row = [k, n, g]; cnt = {"OK": 0, "≈": 0, "NO": 0, "?": 0}
    for c, f, _ in COLS:
        if c in E.get(k, {}): s = E[k][c][0]
        elif c in vis.get(k, {}) and vis[k][c] not in ("–", None): s = "?"
        else: s = "–"
        row.append(s)
        if s in cnt: cnt[s] += 1
    v = sum(cnt.values())
    est = "NO" if cnt["NO"] else ("OK" if cnt["OK"] and not cnt["?"] else ("parcial" if cnt["OK"] or cnt["≈"] else "sin contrastar"))
    ws.append(row + [cnt["OK"], cnt["≈"], cnt["NO"], cnt["?"], v, est])
for row in ws.iter_rows(min_row=2):
    for cell in row[3:3 + len(COLS)]:
        cell.fill = PatternFill("solid", fgColor=F.get(cell.value, "FFFFFF")); cell.alignment = Alignment(horizontal="center")
for cell in ws[1]: cell.font = Font(bold=True); cell.alignment = Alignment(wrap_text=True, horizontal="center")
ws.column_dimensions["B"].width = 52
# notas por celda
w2 = wb.create_sheet("Evidencias")
w2.append(["Zona", "Foto", "Estado", "Medida / nota"])
for k in sorted(E):
    for c, (s, nt) in E[k].items():
        w2.append([k, dict((a, b) for a, b, _ in COLS)[c], s, nt])
w3 = wb.create_sheet("Conflictos abiertos"); w3.append(["Zona", "Qué", "Datos", "Estado"])
for r in CONFLICTOS: w3.append(list(r))
w4 = wb.create_sheet("Columnas (fotos)"); w4.append(["Col.", "Foto", "Para qué sirve"])
for r in COLS: w4.append(list(r))
w5 = wb.create_sheet("Juntas"); w5.append(["Zona A", "Zona B", "Límite"])
for r in Z.JUNTAS: w5.append(list(r))
wb.save("MATRIZ_ZONAS_FOTOS_v2.xlsx")
tot = {s: sum(1 for r in ws.iter_rows(min_row=2, values_only=True) for v in r[3:3 + len(COLS)] if v == s) for s in ("OK", "≈", "NO", "?")}
print(tot)
for r in ws.iter_rows(min_row=2, values_only=True): print(r[0], r[-1], r[-6:-1])
