"""Geometria estimada del Hotel Salut (Kyiv) TAL COMO SE CONSTRUYO (1984).
Todas las cotas en METROS reales. Escala de maqueta 1:300.
Hechos documentados: nucleo central de hormigon, 6 plantas de habitaciones en
voladizo de planta eliptica ('barril'), 19 muros radiales, planta tecnica,
pequena sobreconstruccion en cubierta (sala), estilobato alargado hacia el este
(Dnipro). Las DIMENSIONES son estimaciones (no hay planos publicados)."""
import math
ESCALA = 300
def mm(m):  # metros reales -> mm de maqueta
    return m * 1000.0 / ESCALA

H_PLANTA = 3.0
N_MUROS = 19
# Base (vestibulo + nucleo) cilindrica
BASE_R, BASE_Z0, BASE_Z1 = 6.0, 0.0, 6.0
NUCLEO_R = 3.5
# Estilobato (2 plantas) hacia el este
ESTI_X0, ESTI_X1, ESTI_ANCHO, ESTI_H = 6.0, 46.0, 16.0, 6.0
# Planta tecnica
TEC_A, TEC_B, TEC_Z0, TEC_Z1 = 10.0, 8.5, 6.0, 9.0
# Plantas de habitaciones (forma de barril: las centrales algo mas anchas)
HAB_A0, HAB_B0, HAB_Z0, N_HAB = 12.0, 10.5, 9.0, 6
BALCON = 1.2          # vuelo del balcon corrido
LOSA = 0.45           # espesor de losa (exagerado para que aguante en yeso)
CUBIERTA = 0.4        # losa de cubierta
def planta(i):
    s = 1 + 0.06 * math.sin(math.pi * (i + 0.5) / N_HAB)
    a, b = HAB_A0 * s, HAB_B0 * s
    z0 = HAB_Z0 + i * H_PLANTA
    return dict(i=i, a=a, b=b, fa=a - BALCON, fb=b - BALCON, z0=z0, z1=z0 + H_PLANTA)
PLANTAS = [planta(i) for i in range(N_HAB)]
TECHO_Z = HAB_Z0 + N_HAB * H_PLANTA            # 27.0
# Sobreconstruccion (sala de conferencias)
SUP_A, SUP_B = 6.0, 5.2
SUP_Z0, SUP_Z1 = TECHO_Z + CUBIERTA, TECHO_Z + CUBIERTA + 3.6
ALTURA_TOTAL = SUP_Z1

def perimetro_elipse(a, b):  # Ramanujan
    h = ((a - b) / (a + b)) ** 2
    return math.pi * (a + b) * (1 + 3 * h / (10 + math.sqrt(4 - 3 * h)))
