"""Escribe resultados en la hoja ORDEN DE TRABAJO de MATRIZ_ZONAS_FOTOS.xlsx: marcar(zona, columna, estado, nota)."""
import sys, json
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.comments import Comment
COL = {"OK": "C6EFCE", "NO": "FFC7CE", "?": "FFEB9C", "–": "EDEDED", "OK*": "E2EFDA"}

def marcar(cambios, ruta="MATRIZ_ZONAS_FOTOS.xlsx"):
    wb = load_workbook(ruta); ws = wb["ORDEN DE TRABAJO"]
    hdr = {ws.cell(1, c).value: c for c in range(1, ws.max_column + 1)}
    filas = {ws.cell(r, 2).value: r for r in range(2, ws.max_row + 1)}
    for z, c, est, nota in cambios:
        cell = ws.cell(filas[z], hdr[c]); cell.value = est
        cell.fill = PatternFill("solid", fgColor=COL[est])
        if nota: cell.comment = Comment(nota, "Claude")
    wb.save(ruta)

if __name__ == "__main__":
    marcar(json.loads(sys.argv[1]))
