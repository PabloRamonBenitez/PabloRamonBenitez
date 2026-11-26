"""CATÁLOGO DE PUNTOS DE REFERENCIA (método de verificación, pasada 10).

Cada punto: id, zona, descripción, coordenadas 3D (m) calculadas SOLO desde el cuadro de cotas (via edificio.py).
Las fotos se comparan contra estos puntos: para cada foto se calibra la cámara con elementos ya fiables
(torre) y se proyectan TODOS los puntos; el residuo de cada punto (distancia a la arista real en la foto)
dice si el plano coincide con la foto. Nada se corrige hasta tener la matriz completa (puntos × fotos).
"""
import math, csv
import numpy as np
import edificio as E

V = E._v
T = np.array(E.T)
PTS = []          # (id, zona, desc, x, y, z)


def add(pid, zona, desc, p):
    PTS.append((pid, zona, desc, float(p[0]), float(p[1]), float(p[2])))


def circ(c, r, z, n, k, fase=0.0):
    a = 2 * math.pi * (k + fase) / n + E.FASE_AL
    return (c[0] + r * math.cos(a), c[1] + r * math.sin(a), z)


def generar():
    PTS.clear()
    pl = E.plantas_base()
    Q = pl["Q"]
    # ---------------- TORRE
    for k in range(V["N_AL"]):
        add(f"TOR-ALS-{k:02d}", "TORRE aletas", f"aleta {k}: punta arriba", circ(T, E.R_AL, E.Z_B1 + V["FOR_C"], V["N_AL"], k))
        add(f"TOR-ALI-{k:02d}", "TORRE aletas", f"aleta {k}: punta abajo", circ(T, E.R_AL, E.Z_ALETA0, V["N_AL"], k))
        add(f"TOR-OJO-{k:02d}", "TORRE tambor", f"ojo {k}: centro", circ(T, E.R_T, (E.Z_B1 + E.Z_T1) / 2, V["N_AL"], k, 0.5))
        for i in range(V["N_PL"] + 1):
            z = E.Z_B0 + i * E.F
            add(f"TOR-FOR-{i}-{k:02d}", "TORRE forjados", f"canto forjado {i}, módulo {k}", circ(T, E.R_B, z, V["N_AL"], k, 0.5))
    pv, pr = np.array(E.P(*E.OFF_V)), np.array(E.P(*E.OFF_R))
    for k in range(24):
        add(f"TOR-VIS-S{k:02d}", "TORRE visera", f"visera borde sup {k}", circ(pv, E.R_V, E.Z_V1, 24, k))
        add(f"TOR-VIS-I{k:02d}", "TORRE visera", f"visera borde inf {k}", circ(pv, E.R_V, E.Z_G1, 24, k))
        add(f"TOR-BAN-{k:02d}", "TORRE banda", f"banda acristalada arriba {k}", circ(T, E.R_G, E.Z_G1, 24, k))
        add(f"TOR-TAM-{k:02d}", "TORRE tambor", f"tambor coronación {k}", circ(T, E.R_T, E.Z_T1, 24, k))
    for k in range(12):
        add(f"TOR-REM-{k:02d}", "TORRE remate", f"remate borde sup {k}", circ(pr, E.R_R, E.Z_R1, 12, k))
        add(f"TOR-COL-{k:02d}", "TORRE columna", f"columna pie {k}", circ(T, E.R_COL, 0.0, 12, k))
        add(f"TOR-CUE-{k:02d}", "TORRE cuello", f"cuello losa {k}", circ(T, E.R_CU + 0.6, E.Z_CU0 + 0.6, 12, k))
    # ---------------- ESCALERA (caja radial insertada en el cilindro)
    for nr, r in (("IN", E.ESC_R0), ("EX", E.ESC_RC)):
        for nv, v in (("A", -E.ESC_HB * r), ("B", E.ESC_HB * r)):
            for z, nz in ((0.0, "0"), (E.Z_P1, "P1"), (V["ESC_Z1"], "SUP")):
                add(f"ESC-{nr}{nv}-{nz}", "ESCALERA caja", f"esquina r={r:.1f} v={v:.1f} z={z:.1f}", (*E.esc_pt(r, v), z))
    for nv, d in (("A", -E.ESC_HA), ("B", E.ESC_HA)):
        for z, nz in ((E.Z_B0, "INF"), (E.Z_B1, "SUP")):
            add(f"ESC-HUE-{nv}-{nz}", "ESCALERA hueco", f"borde del hueco en el cilindro {nv} {nz}", (*E.esc_ang_pt(E.R_B, d), z))
    # ---------------- ALA LARGA: fachada exterior, testero
    W_P, L_L = V["W_P"], V["L_L"]
    for yy in np.arange(Q[1], L_L + 0.01, 2.5):
        add(f"ALA-PET-{yy:05.1f}", "ALA LARGA peto", f"coronación peto exterior y={yy:.1f}", (W_P, yy, E.Z_P1 + V["H_PET"]))
        add(f"ALA-PIE-{yy:05.1f}", "ALA LARGA pie", f"pie de fachada exterior y={yy:.1f}", (W_P, yy, 0.0))
        add(f"ALA-INT-{yy:05.1f}", "ALA LARGA patio", f"coronación fachada patio y={yy:.1f}", (0.0, yy, E.Z_P1))
    for nm, p in (("EXT-SUP", (W_P, L_L, E.Z_P1 + V["H_PET"])), ("EXT-0", (W_P, L_L, 0)), ("INT-SUP", (0, L_L, V["Z_FIN"])),
                  ("INT-0", (0, L_L, 0)), ("BAR-SUP", (0, L_L - 0.2, V["Z_FIN"] + 1.1))):
        add(f"TES-{nm}", "TESTERO", f"testero {nm}", p)
    # ---------------- VENTANAS (4 esquinas de cada hueco): 11 arriba, 7 abajo desde el testero
    n, nb, wv, S_ = int(V["N_VEN"]), int(V["N_VEN_B"]), V["VEN_W"], V["S_VEN"]
    for i in range(n):
        y1_ = L_L - V["VEN_FIN"] - i * S_; y = y1_ - wv
        for fila, z0, z1 in (("A", V["VA_0"], V["VA_1"]), ("B", V["VB_0"], V["VB_1"])):
            if fila == "B" and i >= nb: continue
            for c_, (yy, zz) in zip("abcd", ((y, z0), (y + wv, z0), (y + wv, z1), (y, z1))):
                add(f"VEN-{fila}{i + 1:02d}-{c_}", f"VENTANAS fila {fila}", f"hueco {i + 1} (desde testero) fila {fila} esquina {c_}", (W_P + V["MAR_P"], yy, zz))
    # ---------------- BAR
    yb0, yb1 = max(Q[1], E.T[1] + V["ESC_R1"] + 0.3), L_L - V["L_FIN"]
    for nm, (x, y, z) in {"CUB-EI": (0, yb0, E.Z_BAR_C), "CUB-EF": (V["W_BAR"] + V["V_BAR"], yb0, E.Z_BAR_C),
                          "CUB-FF": (V["W_BAR"] + V["V_BAR"], yb1 + V["V_BAR"], E.Z_BAR_C), "CUB-FI": (0, yb1 + V["V_BAR"], E.Z_BAR_C),
                          "CUB-FF-INF": (V["W_BAR"] + V["V_BAR"], yb1 + V["V_BAR"], E.Z_BAR),
                          "VID-FF-SUP": (V["W_BAR"], yb1, E.Z_BAR), "VID-FF-INF": (V["W_BAR"], yb1, E.Z_P1)}.items():
        add(f"BAR-{nm}", "BAR", f"bar {nm}", (x, y, z))
    for yy in np.arange(yb0, yb1, 5.0):
        add(f"BAR-BOR-{yy:05.1f}", "BAR", f"borde cubierta volada y={yy:.1f}", (V["W_BAR"] + V["V_BAR"], yy, E.Z_BAR_C))
    # ---------------- cubierta inclinada del restaurante (+7,2 → +11,5), arranca tras los lucernarios [26/11]
    xr2 = V["W_BAR"] + V["V_BAR"]; ya2 = Q[1] + V["R2_Y0"]
    for j in range(11):
        u = j / 10
        add(f"RA2-PET-{j:02d}", "RAMPA 2", f"borde cubierta inclinada u={u:.1f}", (xr2, ya2 + u * V["R2_L"], E.Z_P1 + u * (E.Z_BAR_C - E.Z_P1)))
    # ---------------- concha: coronación del peto (perfil P2) y borde inferior (arco G3) [26/11]
    y0r = Q[1] + V["D_HOTF"]; LR = E.Y_CUNA - y0r
    Y_ARC = y0r + V["U_ARC"] * LR
    for j in range(21):
        u = j / 20; yy = y0r + u * LR
        zr = max(0.05, V["Z_CON"] * (1 - u ** V["RAMPA_P"]))
        if yy >= Y_ARC: zs = 0.0
        else:
            ua = (yy - y0r) / (Y_ARC - y0r); w = 0.0 if ua <= V["ARC_D"] else (ua - V["ARC_D"]) / (1 - V["ARC_D"])
            zs = max(0.0, min(V["Z_ARC"] * math.sqrt(max(0.0, 1 - w ** 2)), zr - 0.6))
        add(f"RAM-PET-{j:02d}", "RAMPA peto", f"coronación concha y={yy:.1f}", (V["W_EXT"], yy, zr + V["H_PET"]))
        add(f"RAM-ARC-{j:02d}", "RAMPA arco", f"borde inferior y={yy:.1f}", (V["W_EXT"], yy, zs))
    # ---------------- BASE: chaflán y ala corta (vértices de P1 y PB a sus cotas)
    for i, p in enumerate(pl["P1"]):
        add(f"BAS-P1-{i}", "BASE planta 1", f"vértice P1 {i} coronación", (p[0], p[1], E.Z_P1))
    for i, p in enumerate(pl["PB"]):
        add(f"BAS-PB-{i}", "BASE planta baja", f"vértice PB {i} techo", (p[0], p[1], E.Z_PB))
        add(f"BAS-P0-{i}", "BASE planta baja", f"vértice PB {i} suelo", (p[0], p[1], 0.0))
    return PTS


if __name__ == "__main__":
    generar()
    with open("PUNTOS_REFERENCIA.csv", "w", newline="") as f:
        wr = csv.writer(f); wr.writerow(["id", "zona", "descripcion", "x", "y", "z"]); wr.writerows(PTS)
    from collections import Counter
    c = Counter(p[1] for p in PTS)
    for k, v in c.items():
        print(f"{v:5d}  {k}")
    print(f"{len(PTS):5d}  TOTAL")
