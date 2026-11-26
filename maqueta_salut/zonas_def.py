"""Catalogo de ZONAS de verificacion (volumenes 3D en coordenadas de planta, m), definidas sobre edificio.py.
Cada zona: id, nombre, grupo, tipo y geometria.
  tipo 'cil'    -> (centro, r_int, r_ext, z0, z1)    anillo o cilindro
  tipo 'pri'    -> [(poligono_planta, z0, z1), ...]  prismas
  tipo 'concha' -> franja en cuña que baja en curva
JUNTAS: pares de zonas que comparten un limite; se comprueban desde las dos."""
import math
import numpy as np
import edificio as E

T = tuple(E.T); P = E.P
yf = -(E.R_COL - E.RET)                 # frente de la planta primera en el chaflan (coordenada de torre)
pl = E.plantas_base(); Qy = pl["Q"][1]; A1 = E.A1; C = E.C
xe = E._v["ESC_X"]
xA = E.W_P - E._a                     # arranque del chaflan en coordenadas "de L recta"
Y_V = 52.0                              # inicio de las ventanas del ala larga [F47]

ZONAS = [
 # ---------------------------------------------------------------- TORRE
 ("Z01", "Remate, zócalo y letrero САЛЮТ (5 letras planas)", "Torre", "cil", (P(*E.OFF_R), 0, E.R_R + 0.6, E.Z_V1, E.Z_R1 + 0.5)),
 ("Z02", "Visera desplazada, barandilla abierta y lucernario", "Torre", "cil", (P(*E.OFF_V), 0, E.R_V, E.Z_G1, E.Z_V1)),
 ("Z03", "Banda acristalada con montantes", "Torre", "cil", (T, 0, E.R_G, E.Z_T1, E.Z_G1)),
 ("Z04", "Tambor: 13 ojos con tubos, lado ciego y puerta", "Torre", "cil", (T, 0, E.R_T + 0.6, E.Z_B1 + 1.1, E.Z_T1)),
 ("Z05", "Cubierta del barril: barandilla abierta, peto cortado en la escalera", "Torre", "cil", (T, E.R_T - 0.5, E.R_B, E.Z_B1, E.Z_B1 + 1.1)),
 ("Z06", "Barril: forjados, canto, poyete, ranura y 19 aletas", "Torre", "cil", (T, 0, E.R_AL, E.Z_B0 + E.F, E.Z_B1)),
 ("Z07", "Barril: 1ª planta", "Torre", "cil", (T, 0, E.R_AL, E.Z_B0, E.Z_B0 + E.F)),
 ("Z08", "Ménsulas y fondo inclinado bajo el barril", "Torre", "cil", (T, E.R_CU, E.R_AL, 12.6, E.Z_B0)),
 ("Z09", "Cuello y losa inferior volada", "Torre", "cil", (T, 0, E.R_CU + 0.6, E.Z_CU0, E.Z_B0)),
 ("Z10", "Columna", "Torre", "cil", (T, 0, E.R_COL, 0, E.Z_CU0)),
 # ---------------------------------------------------------------- CHAFLAN
 ("Z11", "Chaflán: banda del restaurante (P1, franja de ventanas)", "Chaflán", "pri",
  [([pl["P1"][1], P(-E.R_COL, yf), P(-E.R_COL, yf + 6), P(-E.REST - E.COL / 2, yf + 6)], E.Z_PB, E.Z_P1)]),
 ("Z12", "Chaflán: PB del restaurante hundida", "Chaflán", "pri",
  [([P(-E.REST - E.COL / 2 + 1.5, yf), P(-E.R_COL, yf), P(-E.R_COL, yf + 6), P(-E.REST - E.COL / 2 + 1.5, yf + 6)], 0, E.Z_PB)]),
 ("Z13", "Chaflán: banda del hotel y esquina a 90° volada", "Chaflán", "pri",
  [([P(E.R_COL, yf), C, pl["Q"], P(E.R_COL, yf + 6)], E.Z_PB, E.Z_P1)]),
 ("Z14", "Chaflán: entrada del hotel en hueco (PB)", "Chaflán", "pri",
  [([P(E.R_COL, yf), C, pl["Q"], P(E.R_COL, yf + 6)], 0, E.Z_PB)]),
 ("Z15", "Pie de columna y fuente", "Chaflán", "pri",
  [([P(-E.R_COL - 1, yf - 7), P(E.R_COL + 1, yf - 7), P(E.R_COL + 1, yf), P(-E.R_COL - 1, yf)], 0, 1.0)]),
 # ---------------------------------------------------------------- ALA CORTA
 ("Z16", "Ala corta P1: logia (medianera, pilar, vidrio) y ladrillo ciego", "Ala corta", "pri",
  [([(-E.L_C + E.L_LADR, 0), (xA, 0), (xA, 5.5), (-E.L_C + E.L_LADR, 5.5)], E.Z_PB, E.Z_P1)]),
 ("Z17", "Ala corta: PB a la calle", "Ala corta", "pri",
  [([(-E.L_C + E.L_LADR, 0), (xA, 0), (xA, 5.5), (-E.L_C + E.L_LADR, 5.5)], 0, E.Z_PB)]),
 ("Z18", "Ala corta: bloque alto (A–B 7,3, diagonal, arco por C)", "Ala corta", "pri",
  [([(-E.L_C + E.L_LADR, 5.5), (xA - 1, 5.5), (xA - 1, E.W_C), (-E.L_C + E.L_LADR, E.W_C)], E.Z_P1, E.Z_ALTO + 1.0)]),
 ("Z19", "Ala corta: cuerpo volado y medianera", "Ala corta", "pri",
  [([(-E.L_C, 0), (-E.L_C + E.L_LADR, 0), (-E.L_C + E.L_LADR, E.W_C), (-E.L_C, E.W_C)], 0, E.Z_LADR)]),
 ("Z20", "Rincón: línea posterior paralela al chaflán (teoría)", "Ala corta", "pri",
  [([(xA - 1, 5.5), (0, 5.5), (0, E.W_C), (xA - 1, E.W_C)], 0, E.Z_ALTO)]),
 # ---------------------------------------------------------------- ALA LARGA
 ("Z21", "Concha: rampa de acceso con muro del relieve", "Ala larga", "concha", None),
 ("Z22", "PB en sombra bajo la concha", "Ala larga", "pri",
  [([(E.W_P - 2.0, Qy), (E.W_P, Qy), (E.W_P, E.Y_CUNA), (E.W_P - 2.0, E.Y_CUNA)], 0, E.Z_PB)]),
 ("Z23", "Ala larga: tramo ciego junto a la torre", "Ala larga", "pri",
  [([(0, Qy), (E.W_P, Qy), (E.W_P, Y_V), (0, Y_V)], 0, E.Z_P1)]),
 ("Z24", "Ala larga: fachada exterior con ventanas", "Ala larga", "pri",
  [([(E.W_P - 1.0, Y_V), (E.W_P, Y_V), (E.W_P, E.L_L - E.L_FIN), (E.W_P - 1.0, E.L_L - E.L_FIN)], 0, E.Z_P1)]),
 ("Z25", "Bar: planta sobre la terraza con cubierta volada", "Ala larga", "pri",
  [([(0, Qy), (E.W_BAR + 1.2, Qy), (E.W_BAR + 1.2, E.L_L - E.L_FIN), (0, E.L_L - E.L_FIN)], E.Z_P1, E.Z_BAR_C)]),
 ("Z26", "Terraza de las sombrillas y peto", "Ala larga", "pri",
  [([(E.W_BAR, Qy), (E.W_P, Qy), (E.W_P, E.L_L), (E.W_BAR, E.L_L)], E.Z_P1, E.Z_P1 + 1.0)]),
 ("Z27", "Tramo final sin bar, testero y porche", "Ala larga", "pri",
  [([(0, E.L_L - E.L_FIN), (E.W_P, E.L_L - E.L_FIN), (E.W_P, E.L_L), (0, E.L_L)], 0, E.Z_P1 + 1.0)]),
 ("Z28", "Fachada interior del ala larga (patio)", "Ala larga", "pri",
  [([(0, E.W_C), (1.0, E.W_C), (1.0, E.L_L), (0, E.L_L)], 0, E.Z_BAR_C)]),
 # ---------------------------------------------------------------- ESCALERA Y PATIO
 ("Z29", "Escalera: cuña 20,2°, 16 lamas, remate y muro inclinado", "Escalera", "pri",
  [([tuple(p) for p in E.ESC_POLY], E.Z_P1, E._v["ESC_Z1"])]),
 ("Z30", "Escalera, lado izq.: puerta del tambor, cristalera, rellanos; lado dcho. lamas", "Escalera", "pri",
  [([(xe - E.ESC_W / 2 - 1, E.ESC_Y0 - 3), (xe + E.ESC_W / 2 + 1, E.ESC_Y0 - 3), (xe + E.ESC_W / 2 + 1, E.ESC_Y0 + 1), (xe - E.ESC_W / 2 - 1, E.ESC_Y0 + 1)], E.Z_P1, E.Z_B1)]),
 ("Z32", "Lucernarios piramidales bajo el cuello", "Torre", "cil", (T, E.R_COL, E._v["LUC_CR"] + 1.5, E.Z_P1, E.Z_P1 + E._v["LUC_CH"])),
 ("Z33", "Pie de la escalera: losa blanca, núcleo y celosía baja", "Escalera", "pri",
  [([tuple(E.esc_ang_pt(r, d)) for r, d in ((E.ESC_R0, -E.ESC_HB), (E.ESC_RC, -E.ESC_HB), (E.ESC_RC, E.ESC_HB), (E.ESC_R0, E.ESC_HB))], E.Z_P1, E._v["ESC_Z0"])]),
 ("Z34", "Claraboyas piramidales sobre la cubierta del ala corta", "Ala corta", "pri",
  [([(-E.L_C + 5.5, E.W_C + 1), (-E.L_C + 12.5, E.W_C + 1), (-E.L_C + 12.5, E.W_C + 3), (-E.L_C + 5.5, E.W_C + 3)], E.Z_P1, E.Z_P1 + 1.5)]),
 ("Z35", "Techo del restaurante en rampa (+7,20 → +11,50)", "Ala larga", "pri",
  [([(0, Qy + 0.5), (E.W_BAR + E._v["V_BAR"], Qy + 0.5), (E.W_BAR + E._v["V_BAR"], Qy + 0.5 + E._v["R2_L"]), (0, Qy + 0.5 + E._v["R2_L"])], E.Z_P1, E.Z_BAR_C)]),
 ("Z31", "Patio interior de la L", "Escalera", "pri",
  [([(-E.L_C + E.L_LADR, E.W_C), (0, E.W_C), (0, 45), (-E.L_C + E.L_LADR, 45)], 0, 0.5)]),
]

# las zonas del ala corta se han escrito en coordenadas "de L recta": se pasan a la planta real
def _a_real(z):
    k, n, g_, t, d = z
    if k in ("Z16", "Z17", "Z18", "Z19", "Z20", "Z31", "Z34"):
        d = [([E.SWP(*p) for p in poly], z0, z1) for poly, z0, z1 in d]
    return (k, n, g_, t, d)


ZONAS = [_a_real(z) for z in ZONAS]

JUNTAS = [
 ("Z01", "Z02", "+43,7 apoyo del remate sobre la visera"), ("Z02", "Z03", "+40,5 visera sobre la banda"),
 ("Z03", "Z04", "+38,2 banda sobre el tambor"), ("Z04", "Z05", "pie del tambor y terraza de servicio"),
 ("Z05", "Z06", "+32,6 cubierta del barril"), ("Z06", "Z07", "+18,1 pavés / plantas tipo"),
 ("Z07", "Z08", "+15,2 canto inferior del barril y ménsulas"), ("Z08", "Z09", "ménsulas que mueren en el cuello"),
 ("Z09", "Z10", "+10,4 losa del cuello sobre la columna"), ("Z10", "Z11", "columna entre la banda del restaurante"),
 ("Z10", "Z13", "columna y banda del hotel"), ("Z10", "Z15", "pie de la columna y fuente"),
 ("Z11", "Z12", "vuelo de la banda del restaurante sobre la PB"), ("Z13", "Z14", "vuelo de la banda del hotel sobre la entrada"),
 ("Z11", "Z16", "arranque del chaflán en la calle"), ("Z16", "Z17", "vuelo de la banda a la calle"),
 ("Z16", "Z18", "banda a la calle y bloque alto"), ("Z18", "Z19", "bloque alto y ladrillo"),
 ("Z18", "Z20", "bloque alto y rincón"), ("Z20", "Z28", "rincón y fachada interior del ala larga"),
 ("Z13", "Z21", "esquina a 90° y arranque de la concha"), ("Z21", "Z22", "concha y PB en sombra"),
 ("Z21", "Z23", "concha contra el tramo ciego"), ("Z23", "Z24", "fin de la fachada ciega, inicio de ventanas"),
 ("Z24", "Z27", "ventanas y testero"), ("Z25", "Z26", "voladizo del bar sobre la terraza"),
 ("Z25", "Z27", "fin del bar"), ("Z26", "Z27", "peto del testero"),
 ("Z06", "Z29", "escalera pegada al barril"), ("Z29", "Z30", "escalera y su encuentro"),
 ("Z30", "Z25", "escalera entrando en el bar"), ("Z05", "Z29", "puertas de servicio junto a la escalera"),
 ("Z28", "Z31", "fachada interior y patio"),
 ("Z09", "Z32", "lucernarios bajo el vuelo del cuello"), ("Z29", "Z33", "losa blanca: fin de las lamas, núcleo debajo"),
 ("Z33", "Z35", "la rampa del techo pasa junto al núcleo"), ("Z18", "Z34", "claraboyas detrás del bloque alto"),
]


def concha_lineas(n=30):
    """polilineas 3D de la concha y su huella en planta"""
    y0, y1 = Qy, E.Y_CUNA
    s = np.linspace(0, 1, n)
    zt = E.Z_PB * (1 - s) + np.maximum(0.05, (E.Z_P1 - E.Z_PB * (1 - s)) * (1 - s) ** 1.3)
    xo = E.W_P + (E.W_EXT - E.W_P) * (1 - s); y = y0 + s * (y1 - y0)
    top = np.c_[xo, y, zt]; inn = np.c_[np.full(n, E.W_P), y, zt]; base = np.c_[xo, y, E.Z_PB * (1 - s)]
    return [top, inn, base, np.array([top[0], base[0]]), np.array([top[0], inn[0]])], [(E.W_P, y0), (E.W_EXT, y0), (E.W_P, y1)]


def huella(z):
    """poligonos en planta y rango z de la zona z (para plantas y secciones)"""
    k, n, g, t, d = z
    if t == "cil":
        c, r0, r1, z0, z1 = d
        a = np.linspace(0, 2 * np.pi, 72, endpoint=False)
        return [(np.c_[c[0] + r1 * np.cos(a), c[1] + r1 * np.sin(a)], z0, z1)]
    if t == "pri":
        return [(np.array(p), z0, z1) for p, z0, z1 in d]
    return [(np.array(concha_lineas()[1]), 0, E.Z_P1)]
