"""CUADRO DE COTAS UNICO del Hotel Salut. Fuente de TODO (planos 2D y, al final, el volumen).
Cada cota: valor (m o grados) y origen. Los elementos 2D/3D se derivan de aqui, sin pasar por ningun modelo."""
import math
import numpy as np

COTAS = {
 # --- alturas de la base
 "Z_PB":   (3.2,  "techo de planta baja, única en toda la base", "F15 (época, autobús como escala)"),
 "Z_P1":   (7.2,  "coronación de planta primera = terraza (7,1 ± 0,3)", "rangos: F09 7,3 · F14 7,2 · F15 7,2 · F70 6,5"),
 "Z_BAR":  (10.5, "techo del acristalamiento del bar (vidrio +9,6…+10,5 visto tras el testero)", "F73 (escala puerta testero) 10,5 ± 0,8 · F76 maqueta ~10"),
 "Z_BARC": (11.5, "cubierta volada del bar (= bloque alto ala corta)", "F73 11,3 ± 1,1 · sección AA usuario · F76 ~10,4 (orientativa)"),
 "Z_ALTO": (11.5, "bloque alto del ala corta", "F01, sección AA del usuario"),
 "Z_LAD0": (0.0,  "el ladrillo arranca del suelo", "F72"),
 "Z_FIN":  (7.2,  "testero del ala larga: corona a la cota de la terraza (NO hay bloque alto); barandilla encima", "F73: testero +7,1 ± 0,9; lo alto que se ve detrás es el extremo del bar · F76"),
 "N_VEN": (11, "huecos fila alta", "F73 11 · F01 11 · F47 11"),
 "VEN_W": (1.6, "ancho del hueco (0,47 S)", "F73 ajuste proyectivo: hueco/intereje 0,47"),
 "VEN_FIN": (2.94, "macizo esquina testero → borde del 1er hueco (1,1 S al centro)", "F01 1,22 S · F47 1,05 S (F73 actual 2,5 S: anotado)"),
 "Z_ARC":  (3.2,  "arranque del arco bajo la rampa (hueco de la planta baja hundida)", "F47 vacío oscuro bajo la concha · F71 curva · F76 arco"),
 "U_ARC":  (0.72, "fracción de la rampa donde el arco llega al suelo", "F71 / F47 (estimado ± 0,1)"),
 "S_VEN": (3.4, "intereje de huecos del ala larga", "fila equiespaciada (F73 1,0 px, F01 1,3, F47 1,6); escala: huecos ~cuadrados (usuario) y arco a 35 m (Bing) → 2,94–3,55 → 3,4"),
 "N_VEN_B": (7, "huecos fila baja, bajo los 7 más cercanos al testero", "F01 7 · F47 7 · usuario 7"),
 "MAR_P": (0.08, "relieve del marco del hueco sobre el muro", "F73 perfiles: 0,08 / 0,07 / 0,07"),
 "MAR_B": (0.27, "banda del marco", "F73: 0,08–0,09 S"),
 "MAR_R": (0.16, "del frente del marco al vidrio (2 × relieve)", "F73 escalón interior ≈ 2× exterior · usuario"),
 "R2_L": (19.0, "rampa del techo del restaurante: arranca junto a la torre a +7,2, pasa bajo la caja de escaleras y llega a la cubierta plana del bar (+11,5)", "usuario · F76 (la cubierta baja hasta la terraza junto a la torre) · F71 (tramo inclinado junto a la torre)"),
 "Y_CA":   (55.9, "pie de la rampa de acceso − R_FIN (el pie sobre la fachada es Y_CA + R_FIN = 58,9)", "Bing 59,67 · F73: el hueco 11 se ve por encima de la rampa"),
 "R_FIN":  (3.0,  "desarrollo de la curva final de la concha (cae casi vertical arriba y se abre abajo)", "F73 (tramo alto casi vertical), F71, F47 (estimado ± 2)"),
 "ESC_Y": (22.71, "centro de la caja a lo largo del eje radial", "F58 · ESC_R0/ESC_R1"),
 "ESC_Z1": (41.6, 'coronación de la caja de escalera en su cara exterior: cubierta INCLINADA (muro o lucernario en pendiente para el agua)', 'Alamy (de perfil): +41,6 fuera → +40,8 dentro; dron: el borde del muro blanco sube hacia fuera; la foto lateral la ve de frente (no se aprecia la pendiente) · usuario'),
 "ESC_R0": (5.65, "escalera: muro interior en arco (borde del pasillo anular)", "radio del núcleo 3,25 + pasillo 2,2 + muro"),
 "ESC_R1": (15.9, "cara exterior de la pantalla de lamas (separada 0,3 del cuerpo)", "F08, F11: lamas separadas del muro"),
 "ESC_SEC": (37.9, 'hueco de la escalera en el cilindro = 2 módulos entre muros radiales', 'coherencia aletas–escalera (Alamy) · antes 41 estimado'),
 "ESC_RC": (15.3, "cara exterior del cuerpo cerrado de la escalera", "F08: lamas al nivel de las puntas de las aletas"),
 "ESC_SECB": (25.0, "cuerpo de escalera en cuña (grados), centrado en el hueco, forrado de lamas", "F08: lamas de 18,5° hasta ~43° (su cara lateral se ve en escorzo) · usuario"),
 "ESC_RR": (11.0, "fachada retranqueada con ventanas a cada lado de la cuña (radio)", "F08 franja oscura 9,5°–18,5° con barandillas y huecos, ~1,6 m detrás de la línea de vidrio · F11 · usuario"),
 "H_PT": (1.0, "peto del tambor sobre el pasillo de servicio entre tambor y banda", "F08: pasillo y peto entre el tambor y la banda acristalada"),
 "R_ENT": (3.0, "abertura del peto de la terraza donde llega la rampa 1", "lógica de recorrido"),
 "RAMPA_C": (0.2, "convexidad del perfil de la rampa de acceso: z = Z_CON·(1−u)·(1+c·u); pendiente 14 % arriba, 22 % abajo", "F76 (maqueta: rampa curva desde la plaza), F47, F71"),
 "ESC_Z0": (12.5, "arranque inferior del cuerpo de escalera: la rampa del techo del restaurante pasa por debajo", "usuario: la rampa sube por debajo de la caja de escaleras"),
 "REST_L": (12.8, "planta 1 del chaflán: restaurante, de la esquina de la calle a la columna (5 y pico ventanas)", "F09 frontal 165 px / 12,9 px/m · F18 5+ huecos · usuario"),
 "HOT_L":  (10.1, "planta 1 del chaflán: hotel, de la columna a la esquina a 90° con la rampa (4 y pico ventanas)", "F09 130 px / 12,9 px/m (lectura antigua 9,6) · F18 4+ huecos · usuario"),
 "M_CH":   (2.45, "módulo de los paños de vidrio de la planta primera del chaflán", "F09: 33 px / 12,9 px/m"),
 "R_RAMPA": (6.0, "radio de la curva hacia fuera con la que el borde exterior de la rampa llega a 90° al chaflán", "usuario (croquis) · F76 · ESTIMADO ± 2"),
 "POR_X0": (3.67, "porche del testero: cara exterior del muro izquierdo (x desde la fachada del patio)", "croquis del usuario sobre la planta baja · F73 (muros verdes junto a la puerta)"),
 "POR_X1": (8.27, "porche del testero: cara exterior del muro derecho", "croquis del usuario · F73"),
 "POR_D":  (1.3,  "vuelo del porche (muros y marquesina) delante del testero", "croquis del usuario (65 px / 49 px/m)"),
 "POR_E":  (0.35, "espesor de los muros del porche", "croquis del usuario"),
 "ESQ_D":  (1.2,  "muro de esquina: la fachada exterior del ala sobresale del testero en toda su altura", "F73 (franja verde en la esquina) · croquis del usuario"),
 "VOL_L": (7.3, "cuerpo volado: frente A–B desde la medianera (perpendicular al colindante)", "triangulación satélite A–B = 7,3 (usuario marca A y B en la planta)"),
 "VOL_V": (1.2, "vuelo del cuerpo volado sobre la alineación de fachada (colindante)", "usuario · foto frontal del ala corta"),
 "Z_VOL0": (6.6, "cara inferior del cuerpo volado", "foto frontal (proporción vertical)"),
 "R_AC": (18.6, "radio del arco del bloque alto (DERIVADO: pasa por C)", "A–C 16,66 con el lado B–C paralelo al chaflán"),
 "LOG_D": (1.8, "profundidad de la logia de planta 1 bajo el vuelo (vidrio retranqueado)", "foto frontal · croquis del usuario"),
 "LOG_PX": (3.2, "pilar intermedio de la logia", "foto frontal: a 0,4 del ancho de la logia"),
 "PUERTAS_H": (3, "puertas del hotel en planta baja alrededor de la columna (por lado)", "usuario (imagina más entradas) · F18 (puertas bajo la banda del hotel)"),
 "LUC_X": (0.0, "lucernario: X (según U)", "F01 / postal: de frente al mirar desde la plaza"),
 "LUC_Y": (-13.06, 'lucernario: Y (según N)', 'Alamy con vista corregida a 179,7° (cuña de escalera en el borde izquierdo; 19 aletas) + componente U de F09: lateral 8,34 m'),
 "LUC_R": (1.6, "radio de la base del lucernario", "Alamy: base 92 px / 28,4 px/m = 3,2 m"),
 "LUC_H": (1.8, "altura del lucernario", "Alamy: 45 px / 25 px/m"),
 "LOG_X0": (0.6, "logia: inicio", "croquis del usuario"),
 "LOG_X1": (7.05, "logia: fin (bajo el final del vuelo, muro de 0,25)", "el vuelo A–B mide 7,3 (triangulación)"),
 "AC_TRI": (16.66, "distancia A–C: de la esquina del vuelo en la medianera al final del lado inclinado (arranque del arco)", "triangulación satélite A–C = 16,66 (usuario marca C)"),
 "OB_X": (-0.5, 'banda: desplazamiento según U', "F09 'centrada' ± 0,5: −0,5 para que la banda apoye dentro del tambor con la vista corregida"),
 "OB_Y": (-3.7, 'banda: desplazamiento según N', 'Alamy con vista corregida a 179,7° (cuña de escalera en el borde izquierdo; 19 aletas) + componente U de F09: lateral 2,75 m'),
 "OR_Y": (-0.38, 'remate: desplazamiento según N', 'Alamy con vista corregida a 179,7° (cuña de escalera en el borde izquierdo; 19 aletas) + componente U de F09: lateral −0,22 m'),
 "H_PET":  (1.3,  "peto exterior de la terraza del ala larga (corona ≈ +8,5)", "F73 esquina del testero +8,5 ± 0,6"),
 "VA_0": (4.63, "alféizar fila alta (0,545 H)", "F73 vertical exacta, 3 huecos ±0,006 H"),
 "VA_1": (6.32, "dintel fila alta (0,743 H)", "F73 vertical exacta, 3 huecos ±0,002 H"),
 "VB_0": (1.19, "alféizar fila baja (mismo alto de hueco que la alta)", "F01/F47 huecos iguales arriba y abajo"),
 "VB_1": (2.87, "dintel fila baja (0,338 H)", "F73 vertical exacta, 3 huecos ±0,002 H"),
 "L_HOR":  (6.0,  "cuerpo de hormigón sobre pilares en el extremo del ala corta", "F72 (estimado ± 2)"),
 "Z_LAD1": (10.0, "coronación de la caja de ladrillo", "F01, F19"),
 "Z_CON":  (7.2,  "llegada de la rampa de acceso a la terraza-restaurante = cota de la terraza", "lógica de recorrido · peto F09 +8,3 ± 0,8"),
 # --- torre
 "Z_CU0":  (10.4, "base del cuello", "F09"),
 "Z_CU1":  (13.9, "cara superior del cuello = cara inferior del barril (primer forjado)", "F09 14,4 ± 0,6 ajustado por coherencia con Z_B0 (pasada 7)"),
 "Z_ALE":  (15.2, "borde inferior de las aletas (fin de las ménsulas)", "F09"),
 "Z_B0":   (13.9, "primer forjado del barril", "F09 (paso 3,10)"),
 "F":      (3.10, "altura de planta del barril", "F09: dinteles cada 40 px"),
 "N_PL":   (6,    "plantas del barril (5 de ventanas + pavés)", "F09"),
 "Z_T1": (38.73, 'coronación del tambor de ojos', 'MGF Alamy (vertical de medida del usuario; ref. cara inferior de la losa de cubierta del barril y=1337 = +32,50; 56,53 px/m por 5 forjados, paso 175,25 px)'),
 "Z_G1": (41.29, 'coronación de la banda = cara inferior de la visera', 'MGF Alamy (vertical de medida del usuario; ref. cara inferior de la losa de cubierta del barril y=1337 = +32,50; 56,53 px/m por 5 forjados, paso 175,25 px)'),
 "Z_V1": (43.18, 'coronación de la visera (canto 1,89)', 'MGF Alamy (vertical de medida del usuario; ref. cara inferior de la losa de cubierta del barril y=1337 = +32,50; 56,53 px/m por 5 forjados, paso 175,25 px)'),
 "Z_R1": (50.81, 'coronación del remate (sin antenas)', 'MGF Alamy (vertical de medida del usuario; ref. cara inferior de la losa de cubierta del barril y=1337 = +32,50; 56,53 px/m por 5 forjados, paso 175,25 px)'),
 "R_COL":  (3.25, "radio de la columna (Ø 6,5)", "F09, F14"),
 "R_CONO": (3.25, "pie de la columna: recto (lo que parecía un cono era un toldo)", "usuario; F15/F18"),
 "R_CU":   (9.0,  "radio del cuello (Ø 18)", "F01, F02"),
 "R_B":    (14.4, "radio del borde de balcones", "escala"),
 "R_AL":   (15.3, "radio a la punta de las aletas (Ø 30,6)", "escala"),
 "R_T":    (13.55,"radio del tambor de ojos (Ø 27,1)", "F01, F09, F14"),
 "R_G": (9.45, 'radio de la banda acristalada', 'MGF (generatriz frontal de su cilindro en Alamy, 56,5 px/m vertical, 64,4 px/m horizontal, ref. losa del barril +32,50): Ø 1217 px = 18,9 m'),
 "R_V": (11.7, "radio de la visera", "Alamy (referencia): vista desde −U (rótulo САЛЮТ de frente); 25 px/m vertical por el paso de forjados (175 px/3,1 m) y 28,4 px/m horizontal por el barril (foto de pantalla deformada): 665 px"),
 "R_R": (4.77, 'radio del remate', 'MGF (generatriz frontal de su cilindro en Alamy, 56,5 px/m vertical, 64,4 px/m horizontal, ref. losa del barril +32,50): Ø 614 px = 9,5 m (F09 4,9)'),
 "OV_X": (-2.4, "visera: desplazamiento según U (a lo largo del chaflán)", "F09 (vista según N): 2,4 a la izquierda"),
 "OV_Y": (-4.09, 'visera: desplazamiento según N', 'Alamy con vista corregida a 179,7° (cuña de escalera en el borde izquierdo; 19 aletas) + componente U de F09: lateral 4,46 m'),
 "OR_X": (0.6, "remate: desplazamiento según U", "F09"),
 "N_AL":   (19,   "aletas / muros radiales", "fuentes + F09 · MGF Alamy: paso 18,9° entre 6 aletas"),
 "OJO_D": (1.7, "diámetro de los ojos del tambor (aro exterior)", "MGF Alamy: 1,67 (5 ojos) · antes 1,60"),
 "OJO_V": (0.8, "vuelo del tubo de los ojos fuera del tambor", "MGF Alamy: desplazamiento de los aros hacia el borde de la silueta 0,6–0,9 m"),
 "OJO_Z": (35.84, 'cota del centro de los ojos', 'MGF Alamy (vertical de medida del usuario; ref. cara inferior de la losa de cubierta del barril y=1337 = +32,50; 56,53 px/m por 5 forjados, paso 175,25 px)'),
 "OJO_C0": (110.0, 'lado ciego: ángulo inicial (grados absolutos) = muro del hueco de escalera', 'Alamy con vista a 179,7°: sin ojos entre la escalera y 166°'),
 "OJO_C1": (166.0, 'lado ciego: ángulo final', 'Alamy: primer ojo a 170,9°'),
 "OJO_DP": (-4.3, "giro del primer ojo tras el lado ciego respecto al centro de su módulo (grados)", "MGF Alamy: 1,1 m (70 px) fuera de módulo"),
 "FOR_C": (0.59, "canto de los forjados del barril", "MGF Alamy (vertical de medida del usuario; ref. cara inferior de la losa de cubierta del barril y=1337 = +32,50; 56,53 px/m por 5 forjados, paso 175,25 px): 31–37 px en 5 forjados"),
 "FOR_R": (0.27, "ranura entre canto y poyete", "MGF Alamy (vertical de medida del usuario; ref. cara inferior de la losa de cubierta del barril y=1337 = +32,50; 56,53 px/m por 5 forjados, paso 175,25 px): 12–17 px"),
 "FOR_P": (0.78, "poyete (antepecho) de las habitaciones", "MGF Alamy (vertical de medida del usuario; ref. cara inferior de la losa de cubierta del barril y=1337 = +32,50; 56,53 px/m por 5 forjados, paso 175,25 px): 43–45 px; hueco libre 1,45"),
 "BAR_B": (0.85, "barandilla de la cubierta del barril sobre el canto", "MGF Alamy (vertical de medida del usuario; ref. cara inferior de la losa de cubierta del barril y=1337 = +32,50; 56,53 px/m por 5 forjados, paso 175,25 px): 50 px"),
 "ESC_ZI": (40.8, 'coronación de la caja de escalera en su extremo interior', 'Alamy (de perfil)'),
 "ESC_ZL": (38.2, "coronación de las lamas: por encima, remate de hormigón visto de ~3 m", "foto lateral: remate de 2,97 m (132 px a 44,5 px/m, escala de las juntas de las lamas a 3,10 m)"),
 "LAMA_E": (0.08, "espesor de las lamas de la escalera", "dron y foto lateral: lamas finas y muy juntas · usuario"),
 "LAMA_P": (0.35, "separación entre lamas (a ejes)", "dron: ~0,3–0,4 m con los ojos (Ø 1,70) como escala"),
 "ESC_RS": (10.2, "radio donde termina la caja de escalera por encima del tambor (hueco de cielo hasta la banda)", "Alamy (collage): s = −10,2 con la caja a 90° de la vista"),
 "SIG_S0": (-7.2, "letrero САЛЮТ: borde izquierdo (lateral en la vista de Alamy, m)", "Alamy: x 615 px"),
 "SIG_S1": (4.0, "letrero: borde derecho", "Alamy: x 1335 px"),
 "SIG_Z0": (46.3, "letrero: base de las letras", "Alamy: y 557"),
 "SIG_Z1": (48.5, "letrero: coronación de las letras", "Alamy: y 435"),
 "REM_ZR": (5.7, "zócalo (poyete) del remate: radio", "Alamy: resalte oscuro hasta s −5,9"),
 "REM_ZH": (0.4, "zócalo (poyete) del remate: alto sobre la visera", "Alamy: +43,2 → +43,6"),
 "VISTA_ALAMY": (179.7, "dirección en planta torre → cámara de la foto de Alamy (grados)", "cuña de la escalera en el borde izquierdo de la silueta (s −15,8) + 19 aletas; alternativas 160,8° (taparía balcones) y 198,7° (escalera oculta) descartadas"),
 "FASE_AL": (14.21, 'giro del módulo radial (grados): muros en los bordes del hueco de escalera de 2 módulos', 'Alamy: α mod 18,95° = 9,21 (5 aletas, dispersión 0,8°) con la vista a 179,7° · antes 7,6 con la vista mal supuesta a 230°'),
 "ESC_W": (8.8, "largo radial de la caja (ESC_R1 − ESC_R0)", "F36 cubierta 8,3–8,8 m"),
 "ESC_X": (5.43, "eje de la escalera: radial desde el centro de la torre a lo largo del ala larga (dentro del ala)", "F58 (cenital casi vertical): la caja está en el encuentro barril–ala, dentro de la franja del ala · usuario"),
 # --- planta
 "W_P":    (12.74,"ancho del ala larga", "Bing"),
 "W_BAR":  (6.21, "ancho del bar (mitad interior)", "Bing"),
 "V_BAR":  (1.2,  "vuelo de la cubierta del bar sobre la terraza", "F47"),
 "L_L":    (94.8, "largo total del ala larga desde la calle", "Google 94,82"),
 "L_FIN":  (7.81, "tramo final sin bar: el bar llega casi al testero", "Bing (usuario) 7,81 · F73 extremo del bar tras el testero · F47 fachada acristalada del bar con barandilla a lo largo de la terraza"),
 "W_EXT":  (15.7, "ancho máximo con la concha", "Google"),
 "THL":  (95.0, "ángulo interior de la L (ala larga – calle)", "estimación por rangos: 95,0 ± 2,3° (ESTIMACIONES.md)"),
 "ACH":    (45.0, "chaflán simétrico que corta la esquina de 90°", "usuario + mapa Bing (chaflán ~ bisectriz)"),
 "COL":    (6.5,  "columna en el chaflán", "F09"),
 "L_CHF": (0.0, "longitud del chaflán A1→C (DERIVADA de REST_L, COL, HOT_L y la curva de la rampa)", "F09 + croquis del usuario"),
 "T_POS": (0.0, "posición del eje de la torre sobre A1→C (DERIVADA)", "F09: restaurante 12,8 + columna"),
 "D_HOTF": (0.0, "de C al arranque recto de la rampa (DERIVADA: la esquina curva ocupa este tramo)", "geometría de la curva"),
 "RET":    (1.5,  "lo que asoma la columna delante de la planta primera", "F09/F18"),
 "RETR":   (2.5,  "retranqueo de la planta baja bajo la planta primera", "F09, F14, F47"),
 "L_C": (23.4, "ala corta: KC → medianera (X ≈ 22,4) – RESTAURADO; pendiente de casar con la triangulación A-B-C", "versión anterior a la medición errónea de la foto frontal (12,7 descartado)"),
 "W_C":    (12.74,"fondo del ala corta (igual que el ala larga)", "mapa Bing: las dos alas del mismo ancho"),
 "L_LAD":  (5.0,  "largo de la caja de ladrillo", "F01"),
}
V = {k: v[0] for k, v in COTAS.items()}
import os as _os
for _k in ("ACH", "THL"):
    if _os.environ.get(_k):
        V[_k] = float(_os.environ[_k])


def _derivar():
    """el chaflán sigue más allá de la fachada del ala hasta la esquina a 90° (E90) con el borde curvo de la rampa:
    A1 →(REST_L)→ columna (COL) →(HOT_L)→ E90. De ahí salen L_CHF (A1→C), T_POS y D_HOTF (C → arranque de la rampa)."""
    th, a = math.radians(V["THL"]), math.radians(V["ACH"])
    angC = math.pi - th - a
    US = np.array([math.cos(math.pi / 2 + th), math.sin(math.pi / 2 + th)])
    u = (np.array([0, math.sin(a)]) - math.sin(angC) * US) / math.sin(th)       # U sin normalizar (por unidad de L_CHF)
    U = u / np.linalg.norm(u)
    giro = math.atan2(U[1], U[0])                                                # giro hacia fuera del borde de la rampa
    R = V["R_RAMPA"]
    xE = V["W_EXT"] + R * (1 - math.cos(giro))
    sE = V["REST_L"] + 2 * V["R_COL"] + V["HOT_L"]                               # A1 → E90 a lo largo del chaflán
    V["L_CHF"] = round(sE - (xE - V["W_P"]) / U[0], 3)
    V["T_POS"] = round((V["REST_L"] + V["R_COL"]) / V["L_CHF"], 4)
    V["X_E90"] = xE
    V["D_HOTF"] = round(U[1] / U[0] * (xE - V["W_P"]) + R * math.sin(giro), 3)   # de C al arranque recto de la rampa
    V["GIRO_R"] = giro


_derivar()


# ======================================================================== geometria de planta (2D)
def planta():
    g = dict(V)
    th, a = math.radians(V["THL"]), math.radians(V["ACH"])
    LCH = V["L_CHF"]
    angC = math.pi - th - a
    _a = LCH * math.sin(angC) / math.sin(th); _c = LCH * math.sin(a) / math.sin(th)
    US = np.array([math.cos(math.pi / 2 + th), math.sin(math.pi / 2 + th)]); NS = np.array([US[1], -US[0]])
    KC = np.array([V["W_P"], 0.0]); A1 = KC + _a * US; C = KC + np.array([0, _c])
    U = (C - A1) / LCH; N = np.array([-U[1], U[0]])
    T = A1 + V["T_POS"] * LCH * U + (V["R_COL"] - V["RET"]) * N
    def SWP(x, y):             # ala corta en coordenadas "de L recta"
        return KC + (V["W_P"] - x) * US + y * NS
    def inter(p, d, q, e):
        den = d[0] * e[1] - d[1] * e[0]; s = ((q[0] - p[0]) * e[1] - (q[1] - p[1]) * e[0]) / den
        return p + s * d
    Q = C.copy()
    # esquina: el chaflán sigue hasta E90 y el borde de la rampa vuelve en curva hasta (W_EXT, C.y + D_HOTF)
    R = V["R_RAMPA"]; gr = V["GIRO_R"]; yS = C[1] + V["D_HOTF"]; cen = np.array([V["W_EXT"] + R, yS])
    ARC = [cen + R * np.array([math.cos(math.pi + gr * (1 - t)), math.sin(math.pi + gr * (1 - t))]) for t in np.linspace(0, 1, 13)]
    IC = inter(SWP(-V["L_C"], V["W_C"]), U, np.array([0.0, 0.0]), np.array([0.0, 1.0]))   # línea posterior paralela al chaflán [usuario]
    P1 = [SWP(-V["L_C"], 0), A1, C] + ARC + [np.array([V["W_P"], yS]), np.array([V["W_P"], V["L_L"]]),
          np.array([0, V["L_L"]]), IC, SWP(-V["L_C"], V["W_C"])]
    o_s = KC + V["RETR"] * NS; o_c = A1 + V["RETR"] * N
    a1 = inter(o_s, US, o_c, U); b1 = inter(o_c, U, np.array([V["W_P"] - V["RETR"], 0]), np.array([0.0, 1.0]))
    YC = V["Y_CA"] + V["R_FIN"]
    PB = [SWP(-V["L_C"], V["RETR"]), a1, b1, np.array([V["W_P"] - V["RETR"], YC]),
          np.array([V["W_P"], YC]), np.array([V["W_P"], V["L_L"]]), np.array([0, V["L_L"]]), IC,
          SWP(-V["L_C"], V["W_C"])]
    P = lambda X, Y: T + X * U + Y * N
    return dict(T=T, U=U, N=N, A1=A1, C=C, Q=Q, ARC=ARC, E90=ARC[0], YS=yS, KC=KC, US=US, NS=NS, SWP=SWP, P=P, P1=P1, PB=PB, IC=IC, YC=YC, xA=V["W_P"] - _a)


# ======================================================================== elementos (tipo, nombre, huella, z0, z1)
def elementos():
    g = planta(); V_ = V; T = g["T"]; P = g["P"]; SWP = g["SWP"]
    E = []
    def pri(nombre, poly, z0, z1, zona=""): E.append(dict(t="pri", n=nombre, p=[np.array(q, float) for q in poly], z0=z0, z1=z1, zona=zona))
    def cil(nombre, c, r, z0, z1, zona="", r0=None): E.append(dict(t="cil", n=nombre, c=np.array(c, float), r=r, r0=r0 if r0 else r, z0=z0, z1=z1, zona=zona))
    pri("planta baja", g["PB"], 0, V_["Z_PB"], "base")
    pri("planta primera", g["P1"], V_["Z_PB"], V_["Z_P1"], "base")
    xA = g["xA"]
    pri("bloque alto ala corta", [SWP(-V_["L_C"], -V_["VOL_V"]), SWP(-V_["L_C"] + V_["VOL_L"], -V_["VOL_V"]), SWP(-8.0, 7.0), SWP(-8.2, V_["W_C"]), SWP(-V_["L_C"], V_["W_C"])], V_["Z_P1"], V_["Z_ALTO"], "Z18")
    yb0 = g["Q"][1] + 0.5                                     # la rampa del techo arranca junto a la torre, bajo la escalera
    import math as _mm
    pri("techo del restaurante en rampa", [(0, yb0), (V_["W_BAR"] + V_["V_BAR"], yb0), (V_["W_BAR"] + V_["V_BAR"], yb0 + V_["R2_L"]), (0, yb0 + V_["R2_L"])], V_["Z_P1"], V_["Z_BARC"], "Z25")
    pri("bar", [(0, yb0), (V_["W_BAR"], yb0), (V_["W_BAR"], V_["L_L"] - V_["L_FIN"]), (0, V_["L_L"] - V_["L_FIN"])], V_["Z_P1"], V_["Z_BAR"], "Z25")
    pri("cubierta del bar", [(0, yb0), (V_["W_BAR"] + V_["V_BAR"], yb0), (V_["W_BAR"] + V_["V_BAR"], V_["L_L"] - V_["L_FIN"]), (0, V_["L_L"] - V_["L_FIN"])], V_["Z_BAR"], V_["Z_BARC"], "Z25")
    pri("peto terraza", [(V_["W_P"] - 0.3, yb0), (V_["W_P"], yb0), (V_["W_P"], V_["L_L"]), (V_["W_P"] - 0.3, V_["L_L"])], V_["Z_P1"], V_["Z_P1"] + V_["H_PET"], "Z26")
    pri("concha", [(V_["W_P"], g["Q"][1]), (V_["W_EXT"], g["Q"][1]), (V_["W_P"], g["YC"])], 0, V_["Z_CON"], "Z21")
    # torre
    cil("pie cónico", T, V_["R_COL"], 0, 4.0, "Z10", r0=V_["R_CONO"])
    cil("columna", T, V_["R_COL"], 0, V_["Z_CU0"], "Z10")
    cil("cuello", T, V_["R_CU"], V_["Z_CU0"], V_["Z_CU1"], "Z09")
    cil("ménsulas / fondo", T, V_["R_AL"], V_["Z_CU1"], V_["Z_ALE"], "Z08", r0=V_["R_CU"])
    zb1 = V_["Z_B0"] + V_["N_PL"] * V_["F"]
    cil("barril", T, V_["R_AL"], V_["Z_ALE"], zb1 + V_["FOR_C"], "Z06")
    cil("tambor de ojos", T, V_["R_T"], zb1 + V_["FOR_C"], V_["Z_T1"], "Z04")
    cil("banda acristalada", P(V_["OB_X"], V_["OB_Y"]), V_["R_G"], V_["Z_T1"] - V_["H_PT"], V_["Z_G1"], "Z03")
    cil("visera", P(V_["OV_X"], V_["OV_Y"]), V_["R_V"], V_["Z_G1"], V_["Z_V1"], "Z02")
    cil("remate", P(V_["OR_X"], V_["OR_Y"]), V_["R_R"], V_["Z_V1"], V_["Z_R1"], "Z01")
    import math as _m
    _ang = _m.atan2(V_["ESC_Y"] - T[1], V_["ESC_X"] - T[0]); _hb = _m.radians(V_["ESC_SECB"]) / 2
    _pt = lambda r, d: (T[0] + r * _m.cos(_ang + d), T[1] + r * _m.sin(_ang + d))
    pri("escalera (cuña)", [_pt(V_["ESC_RC"], -_hb + 2 * _hb * k / 8) for k in range(9)] + [_pt(V_["ESC_R0"], _hb - 2 * _hb * k / 8) for k in range(9)], 0, V_["ESC_Z1"], "Z29")
    return E, g


def niveles():
    zb1 = V["Z_B0"] + V["N_PL"] * V["F"]
    return [(0, "±0"), (V["Z_PB"], "techo PB"), (V["Z_P1"], "planta 1 / terraza"), (V["Z_BARC"], "bar / bloque alto"),
            (V["Z_CU0"], "cuello"), (V["Z_ALE"], "aletas"), (zb1, "cubierta barril"), (V["Z_T1"], "tambor"),
            (V["Z_G1"], "banda"), (V["Z_V1"], "visera"), (V["Z_R1"], "remate")]

# Margen (±) de cada cota: medido en varias fotos ≈ 0,3-0,6 · una foto ≈ 1 · estimado ≈ 1,5-2 · satélite ≈ 1
RANGOS = {
 "Z_PB": 0.3, "Z_P1": 0.3, "Z_BAR": 0.8, "Z_BARC": 0.8, "Z_ALTO": 1.0, "Z_LAD0": 0.5, "Z_FIN": 0.9, "H_PET": 0.6, "VA_0": 0.5, "VA_1": 0.6, "VB_0": 0.3, "VB_1": 0.4, "L_HOR": 2.0, "VOL_L": 0.3, "AC_TRI": 0.3, "VOL_V": 0.3, "Z_VOL0": 0.4, "R_AC": 1.5, "LOG_D": 0.5, "LOG_PX": 0.8, "LOG_X0": 0.5, "LOG_X1": 0.8, "LUC_X": 1.5, "LUC_Y": 1.5, "LUC_R": 0.5, "LUC_H": 0.5,
 "FASE_AL": 1.0, "ESC_ZI": 0.4, "ESC_ZL": 0.5, "LAMA_E": 0.04, "LAMA_P": 0.1, "ESC_RS": 0.8, "SIG_S0": 0.5, "SIG_S1": 0.5, "SIG_Z0": 0.2, "SIG_Z1": 0.2, "REM_ZR": 0.3, "REM_ZH": 0.15, "VISTA_ALAMY": 2.0, "FOR_C": 0.05, "FOR_R": 0.05, "FOR_P": 0.05, "BAR_B": 0.15, "OJO_D": 0.1, "OJO_V": 0.3, "OJO_Z": 0.2, "OJO_C0": 10.0, "OJO_C1": 6.0, "OJO_DP": 2.0, "Z_LAD1": 1.0, "Z_CON": 0.8, "Z_CU0": 0.6, "Z_CU1": 0.6, "Z_ALE": 0.6, "Z_B0": 0.4, "F": 0.05, "N_PL": 0,
 "Z_T1": 0.5, "Z_G1": 0.5, "Z_V1": 0.5, "Z_R1": 0.6, "R_COL": 0.3, "R_CONO": 0.3, "R_CU": 0.5, "R_B": 0.3,
 "R_AL": 0.3, "R_T": 0.5, "R_G": 0.5, "R_V": 0.6, "R_R": 0.25, "OV_X": 1.0, "OV_Y": 1.5, "OR_X": 0.5, "OR_Y": 0.5, "OB_X": 0.5, "OB_Y": 0.8, "N_AL": 0,
 "ESC_W": 1.5, "ESC_X": 1.0, "H_PT": 0.3, "R_ENT": 1.0, "POR_X0": 0.3, "POR_X1": 0.3, "POR_D": 0.3, "ESQ_D": 0.3, "REST_L": 0.8, "HOT_L": 0.6, "R_RAMPA": 2.0, "M_CH": 0.2, "ESC_Z0": 1.0, "RAMPA_C": 0.1, "ESC_SEC": 4.0, "ESC_SECB": 4.0, "ESC_RR": 0.8, "ESC_RC": 1.0, "ESC_Y": 2.0, "ESC_Z1": 0.8, "W_P": 0.5, "W_BAR": 0.5, "V_BAR": 0.5, "L_L": 1.0, "L_FIN": 0.5, "Y_CA": 0.6, "R_FIN": 2.0, "S_VEN": 0.3, "N_VEN_B": 0, "MAR_P": 0.02, "MAR_B": 0.05, "MAR_R": 0.04, "R2_L": 3.0, "N_VEN": 0, "VEN_W": 0.2, "VEN_FIN": 1.5, "Z_ARC": 0.5, "U_ARC": 0.1, "D_CUNA": 1.0,
 "W_EXT": 1.0, "THL": 2.3, "ACH": 8.0, "COL": 0.3, "L_CHF": 3.0, "T_POS": 0.1,
 "D_HOTF": 2.0, "RET": 0.5, "RETR": 0.5, "L_C": 3.0, "W_C": 1.0, "L_LAD": 1.5,
}
