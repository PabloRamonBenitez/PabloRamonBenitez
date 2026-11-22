"""Reorganiza la matriz por dependencias: primero lo que, si esta mal, arrastra a todo lo demas."""
import collections
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import zonas_def as Z, columnas as CC

FASES = [
 ("F1", "ESQUELETO: escala y eje de la torre",
  "Si la escala o el eje están mal, todo lo demás se mide mal. Se usan como regla en todas las fotos.",
  ["Z06", "Z10"], ["C04", "C01", "C03"]),
 ("F2", "IMPLANTACIÓN: torre respecto a la L",
  "Ángulo del chaflán, dirección de las alas y dónde se engancha la torre. Es la aguja del pajar: de aquí salen casi todos los errores vistos.",
  ["Z11", "Z13", "Z23", "Z29", "Z30", "Z16"], ["C01", "C17", "C02", "C04", "C10"]),
 ("F3", "COTAS DE LA BASE: plantas baja y primera",
  "Fijan la altura del arranque de la torre y de todas las alas.",
  ["Z12", "Z14", "Z17", "Z15"], ["C04", "C03", "C08", "C05", "C06"]),
 ("F4", "APOYO DE LA TORRE: de la base al barril",
  "Une la base (F3) con el barril (F1): cuello, ménsulas y pavés.",
  ["Z09", "Z08", "Z07"], ["C05", "C06", "C04", "C03", "C07"]),
 ("F5", "CORONACIÓN DE LA TORRE",
  "Se apoya en el barril; el desplazamiento de la visera se mide respecto al eje (F1).",
  ["Z05", "Z04", "Z03", "Z02", "Z01"], ["C04", "C12", "C01", "C03"]),
 ("F6", "VOLÚMENES DE LAS ALAS",
  "Con la implantación (F2) y las cotas (F3) fijadas, se comprueban los cuerpos.",
  ["Z21", "Z22", "Z25", "Z26", "Z27", "Z18", "Z19", "Z20", "Z28", "Z31"], ["C01", "C02", "C17", "C18", "C05", "C10"]),
 ("F7", "DETALLES",
  "Huecos, poyetes, aletas, ventanas y lamas: no mueven nada más.",
  ["Z24"], ["C11", "C13", "C14", "C15", "C01", "C04"]),
]

if __name__ == "__main__":
    vis = {c[0]: set(c[6]) for c in CC.COLS}
    grado = collections.Counter([a for a, b, _ in Z.JUNTAS] + [b for a, b, _ in Z.JUNTAS])
    nombre = {k: n for k, n, *_ in Z.ZONAS}
    asignadas = [z for f in FASES for z in f[3]]
    falt = [k for k in nombre if k not in asignadas]
    assert not falt, falt
    # columnas ordenadas por cobertura (zonas visibles) y fiabilidad
    orden_cols = sorted(CC.COLS, key=lambda c: (-len(c[6]) if c[0] not in ("C16",) else 99))
    wb = load_workbook("MATRIZ_ZONAS_FOTOS.xlsx")
    ws = wb.create_sheet("ORDEN DE TRABAJO", 0)
    th = Side(style="thin", color="999999"); B = Border(th, th, th, th)
    hdr = ["Fase", "Zona", "Descripción", "Juntas", "Fotos de referencia (por orden)"] + [c[0] for c in orden_cols] + ["Visibles"]
    ws.append(hdr)
    colfase = ["F4CCCC", "FCE5CD", "FFF2CC", "D9EAD3", "D0E0E3", "CFE2F3", "EAD1DC"]
    r = 2
    for i, (f, tit, por, zonas, ref) in enumerate(FASES):
        ws.append([f, tit, por]); ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=5)
        for c in range(1, len(hdr) + 1):
            ws.cell(r, c).fill = PatternFill("solid", fgColor=colfase[i]); ws.cell(r, c).font = Font(bold=True, size=9)
            ws.cell(r, c).alignment = Alignment(wrap_text=True, vertical="center")
        ws.row_dimensions[r].height = 30; r += 1
        for z in sorted(zonas, key=lambda k: -grado[k]):
            vals = ["?" if z in vis[c[0]] else "–" for c in orden_cols]
            ws.append(["", z, nombre[z], grado[z], " > ".join(x for x in ref if z in vis[x])] + vals + [vals.count("?")])
            for j in range(len(orden_cols)):
                cell = ws.cell(r, 6 + j); cell.alignment = Alignment(horizontal="center")
                cell.fill = PatternFill("solid", fgColor="FFEB9C" if cell.value == "?" else "EDEDED")
            for c in range(1, len(hdr) + 1):
                ws.cell(r, c).border = B; ws.cell(r, c).font = Font(size=9)
            r += 1
    for c in range(1, len(hdr) + 1):
        ws.cell(1, c).font = Font(bold=True, size=9); ws.cell(1, c).fill = PatternFill("solid", fgColor="D9D9D9")
        ws.cell(1, c).alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
    for col, w in zip("ABCDE", (6, 7, 52, 7, 28)): ws.column_dimensions[col].width = w
    for j in range(len(orden_cols) + 1): ws.column_dimensions[get_column_letter(6 + j)].width = 5.5
    ws.freeze_panes = "F2"
    r += 1
    ws.cell(r, 3).value = "REGLAS: no se pasa a la fase siguiente con un NO abierto en la anterior. Si una corrección cambia una fase ya cerrada, se vuelve a comprobar esa fase y todas las posteriores."
    ws.cell(r + 1, 3).value = "Columnas ordenadas de más a menos zonas visibles; en cada zona se empieza por su foto de referencia."
    wb.save("MATRIZ_ZONAS_FOTOS.xlsx")
    for f in FASES: print(f[0], f[1], f[3])
