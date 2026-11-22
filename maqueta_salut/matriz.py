"""Matriz de verificacion: filas = 20 puntos de plantas/secciones/alzados; columnas = 20 fotos.
Celda: OK / NO / – (no se ve en esa foto) / ? (pendiente). Listo cuando ninguna celda visible esta en NO o ?."""
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

FILAS = [
 ("R01", "Remate: Ø 11,2 · alto 5,4 · casi en el eje", "Alzado 1 / Sección L3"),
 ("R02", "Visera: Ø 25,6 · canto 3,2 · desplazada 2,4 hacia el restaurante · nervios en el intradós", "Alzado 1 / Planta aérea"),
 ("R03", "Banda acristalada: Ø 21,7 · alto 2,3 · montantes · casi centrada", "Alzado 1 / Planta última"),
 ("R04", "Tambor de ojos: Ø 27,1 · alto 5,4 · 19 ojos Ø 1,6 con aros", "Alzado 1 / Planta última"),
 ("R05", "Terraza de servicio sobre el barril: peto, puertas junto a la escalera", "Planta última / Sección S1"),
 ("R06", "Módulo del barril: forjado 0,45 · ranura · poyete 0,7 · ventana · balcón 1,8", "Detalle 1"),
 ("R07", "Barril: 6 plantas, alto 17,4, cota +15,2 a +32,6, 19 aletas que vuelan 0,9", "Alzado 1 / Planta 4"),
 ("R08", "Primera planta del barril: pavés, distinta de las demás", "Alzado 1 / Detalle 1"),
 ("R09", "Ménsulas triangulares bajo el barril (19), fondo inclinado hacia el cuello", "Alzado 1 / Sección L1"),
 ("R10", "Cuello: Ø 15 · alto · losa inferior volada como un plato", "Alzado 1 / Sección L3"),
 ("R11", "Columna Ø 6,5: entera del suelo al cuello, entre las dos bandas", "Alzado 1 / Planta 0"),
 ("R12", "Banda del restaurante en el chaflán: 12,8 · +3,9 a +7,3 · franja de ventanas", "Alzado 1 / Planta 1"),
 ("R13", "Banda del hotel: 9,6 · esquina a 90° volada · franja de ventanas", "Alzado 1 / Planta 1 / Detalle 2"),
 ("R14", "Planta baja hundida 2,5 bajo las bandas (entradas en hueco)", "Planta 0 / Detalle 2"),
 ("R15", "Concha / muro del relieve: arranca en la esquina del hotel, baja en curva, PB en sombra debajo", "Alzado 2 / Planta 0 / Sección S2"),
 ("R16", "Ala larga: 12,74 de ancho, recta; terraza +7,3 con peto; bar 6,21 con cubierta volada", "Secciones S2-S4 / Planta 2"),
 ("R17", "Ventanas del ala larga: 2 filas, mitad del fondo, hasta el final", "Alzado 2"),
 ("R18", "Ala corta: banda del restaurante + bloque alto +11,5 con lucernarios en diente de sierra", "Alzado 3 / Sección S5"),
 ("R19", "Extremo de la calle: bloque de ladrillo sobre pilares", "Alzado 3 / Planta 0"),
 ("R20", "Escalera trasera en línea con el ala larga; encuentro barril-escalera-ala", "Planta 4 / Sección L1 / Alzado 5"),
]
FOTOS = ["F01","F02","F03","F04","F08","F09","F10","F11","F12","F13","F14","F15","F18","F19","F22","F23","F24","F47","F50","F51"]
DESC = {"F01":"aérea época","F02":"época plaza","F03":"contrapicado","F04":"barril cerca","F08":"aérea ciudad","F09":"frontal tele",
        "F10":"remate","F11":"escalera","F12":"escalera/barril","F13":"escalera lateral","F14":"época plaza","F15":"base época",
        "F18":"color plaza","F19":"calle","F22":"maqueta orig.","F23":"aérea época 2","F24":"terraza","F47":"terraza/concha",
        "F50":"contrapicado color","F51":"color plaza 2"}
# visibilidad (lo que se ve en cada foto). '?' = se ve, pendiente de comparar; '–' = no se ve
VIS = {
 "R01":"F01 F02 F08 F09 F10 F14 F19 F22 F23",
 "R02":"F01 F02 F03 F08 F09 F10 F14 F18 F19 F22 F23 F50 F51",
 "R03":"F01 F02 F08 F09 F10 F14 F19 F22 F23",
 "R04":"F01 F02 F03 F04 F08 F09 F10 F14 F18 F19 F23 F50 F51",
 "R05":"F01 F10 F12 F23",
 "R06":"F01 F02 F03 F04 F08 F09 F12 F13 F14 F18 F23 F50 F51",
 "R07":"F01 F02 F03 F04 F08 F09 F14 F18 F19 F22 F23 F50 F51",
 "R08":"F02 F09 F14 F18 F50 F51",
 "R09":"F02 F09 F14 F15 F18 F50 F51",
 "R10":"F01 F02 F09 F14 F15 F18 F50 F51",
 "R11":"F01 F02 F09 F14 F15 F18 F50 F51",
 "R12":"F01 F02 F09 F14 F15 F18 F50 F51",
 "R13":"F01 F09 F18 F47 F50 F51",
 "R14":"F01 F02 F09 F14 F15 F18 F50 F51",
 "R15":"F01 F09 F18 F23 F24 F47 F51",
 "R16":"F01 F22 F23 F24 F47",
 "R17":"F01 F23 F24 F47",
 "R18":"F01 F02 F14 F15 F23",
 "R19":"F01 F23",
 "R20":"F01 F11 F12 F13 F22",
}
COL = {"OK":"C6EFCE","NO":"FFC7CE","?":"FFEB9C","–":"EDEDED"}

def crear(estado=None, ruta="MATRIZ_VERIFICACION.xlsx", pasada="1"):
    wb = Workbook(); ws = wb.active; ws.title = f"Pasada {pasada}"
    th = Side(style="thin", color="999999")
    hdr = ["Punto", "Qué se comprueba (medidas de los planos)", "Dónde está en los planos"] + [f"{f}\n{DESC[f]}" for f in FOTOS] + ["Visibles", "OK", "NO", "Pend."]
    ws.append(hdr)
    for c in range(1, len(hdr) + 1):
        cell = ws.cell(1, c); cell.font = Font(bold=True, size=9); cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        cell.fill = PatternFill("solid", fgColor="D9D9D9"); cell.border = Border(th, th, th, th)
    for r, (k, txt, donde) in enumerate(FILAS, start=2):
        vis = VIS[k].split()
        vals = []
        for f in FOTOS:
            v = (estado or {}).get((k, f)) or ("?" if f in vis else "–")
            vals.append(v)
        ws.append([k, txt, donde] + vals)
        n0 = 4; nl = get_column_letter(n0); nr = get_column_letter(n0 + len(FOTOS) - 1)
        ws.cell(r, n0 + len(FOTOS)).value = f'=COUNTIF({nl}{r}:{nr}{r},"<>–")'
        ws.cell(r, n0 + len(FOTOS) + 1).value = f'=COUNTIF({nl}{r}:{nr}{r},"OK")'
        ws.cell(r, n0 + len(FOTOS) + 2).value = f'=COUNTIF({nl}{r}:{nr}{r},"NO")'
        ws.cell(r, n0 + len(FOTOS) + 3).value = f'=COUNTIF({nl}{r}:{nr}{r},"?")'
        for c in range(1, len(hdr) + 1):
            cell = ws.cell(r, c); cell.border = Border(th, th, th, th)
            cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center" if c > 3 else "left")
            cell.font = Font(size=9)
            if 4 <= c < 4 + len(FOTOS):
                cell.fill = PatternFill("solid", fgColor=COL.get(cell.value, "FFFFFF"))
    ws.column_dimensions["A"].width = 6; ws.column_dimensions["B"].width = 52; ws.column_dimensions["C"].width = 24
    for c in range(4, 4 + len(FOTOS) + 4): ws.column_dimensions[get_column_letter(c)].width = 8.5
    ws.row_dimensions[1].height = 42; ws.freeze_panes = "D2"
    nfin = len(FILAS) + 3
    ws.cell(nfin, 2).value = "Leyenda: OK coincide · NO no coincide · ? se ve, pendiente de comparar · – no se ve en esa foto"
    ws.cell(nfin + 1, 2).value = "Criterio de terminado: ninguna celda en NO ni en ?"
    wb.save(ruta)

if __name__ == "__main__":
    crear()
    tot = sum(len(v.split()) for v in VIS.values())
    print("celdas a comparar:", tot)
