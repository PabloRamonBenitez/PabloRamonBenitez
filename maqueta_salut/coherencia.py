"""Coherencia PLANTAS <-> SECCIONES (sin fotos): cuadro de niveles de todas las partes y reglas arquitectonicas.
Cada regla que falla genera una PREGUNTA concreta y la foto que la contesta."""
import edificio as E
N = [  # parte, nivel inferior, nivel superior, uso
 ("Chaflán · restaurante", 0, 4.5, "PB (terraza con toldos)"), ("Chaflán · restaurante", 4.5, E.Z_P1, "P1 (vidrio + rótulo)"),
 ("Chaflán · hotel", 0, 3.1, "PB (entrada)"), ("Chaflán · hotel", 3.1, 4.3, "canto volado"), ("Chaflán · hotel", 4.3, E.Z_P1, "P1 (vidrio + rótulo)"),
 ("Ala corta", 0, E.Z_PB, "PB"), ("Ala corta", E.Z_PB, E.Z_P1, "P1"), ("Ala corta · bloque alto", E.Z_P1, E.Z_ALTO, "P2"),
 ("Ala larga", 0, E.Z_PB, "PB"), ("Ala larga", E.Z_PB, E.Z_P1, "P1"), ("Ala larga · bar", E.Z_P1, E.Z_BAR, "P2 (bar)"),
 ("Ala larga · cubierta bar", E.Z_BAR, E.Z_BAR_C, "losa volada"),
 ("Torre · columna", 0, E.Z_CU0, "columna"), ("Torre · cuello", E.Z_CU0, E.Z_CU1, "cuello"),
 ("Torre · barril", E.Z_B0, E.Z_B1, f"6 plantas de {E.F}"), ("Torre · tambor", E.Z_B1, E.Z_T1, "tambor de ojos"),
 ("Torre · banda", E.Z_T1, E.Z_G1, "sala acristalada"), ("Torre · visera", E.Z_G1, E.Z_V1, "visera"), ("Torre · remate", E.Z_V1, E.Z_R1, "remate"),
 ("Escalera", E.Z_P1, E.Z_T1 + 1, "núcleo de comunicación"),
]
R = [  # (regla, cumple, pregunta, fotos)
 ("Las plantas de la base están a la misma cota en todas las partes (PB y P1)",
  False, "¿La PB del restaurante (+4,5) y la del hotel (+3,1 + canto) son distintas de verdad, o una de las medidas está mal? ¿Y las alas (+3,9)?",
  "C06 (F50), C08 (F15), C05 (F18)"),
 ("La cubierta de la base (+7,3) es una sola cota: bandas, terraza del ala larga y ala corta",
  True, "", ""),
 ("El bar y el bloque alto del ala corta son la misma planta (tu sección AA/BB)",
  abs(E.Z_BAR_C - E.Z_ALTO) < 0.15, f"Bar cubierta +{E.Z_BAR_C} y bloque alto +{E.Z_ALTO}: ¿cuál es la buena?", "C01, C02, C10"),
 ("La escalera llega desde el suelo hasta todas las plantas del barril y la terraza de servicio",
  False, f"La escalera empieza en +{E.Z_P1}: ¿baja hasta el suelo (y entonces se ve en el patio) o arranca sobre la cubierta del ala?", "C13 (F11), C15 (F13), C10 (F08)"),
 ("Cada planta del barril tiene acceso desde la escalera (las cotas de forjado coinciden con los rellanos)",
  True, "", ""),
 ("Entre la cubierta de la base (+7,3) y el cuello (+10,4) solo pasa la columna",
  True, "", ""),
 ("El fondo del barril (+13,9) apoya en el cuello y en las ménsulas, sin hueco",
  False, "El cuello acaba en +13,9 pero las aletas en +15,2: ¿qué hay entre ambas (ménsulas, fondo inclinado)? Altura del cuello y de su losa volada.", "C05 (F18), C06 (F50), C07 (F03)"),
 ("La concha arranca a la cota de la banda del hotel (+7,3) sin escalón",
  False, "En F09 el muro del relieve llega a ~+8,5 en su arranque: ¿la concha arranca más alta que la banda?", "C04 (F09), C05 (F18), C01 (F47)"),
 ("Las ventanas del ala larga están en sus dos plantas (PB y P1) y por debajo de la terraza",
  True, "", ""),
 ("El ala larga y la calle forman un ángulo coherente con la escalera alineada con el ala",
  None, "Ángulo de la L (ahora 102°) y del chaflán (ahora 57°): incógnitas que se cerrarán cuando encajen las demás zonas (buscaminas).", "C17, C02, C01"),
]
if __name__ == "__main__":
    L = ["# Coherencia plantas ↔ secciones (antes de mirar fotos)", "",
         "Primero se comprueba que plantas y secciones encajan entre sí. Lo que no encaja genera una pregunta concreta y se busca SOLO esa respuesta en las fotos indicadas.", "",
         "## Cuadro de niveles (m)", "", "| Parte | Desde | Hasta | Uso |", "|---|---|---|---|"]
    L += [f"| {p} | {a:+.2f} | {b:+.2f} | {u} |".replace(".", ",") for p, a, b, u in N]
    L += ["", "## Reglas", "", "| # | Regla | Estado | Pregunta para las fotos | Fotos |", "|---|---|---|---|---|"]
    for i, (r, ok, q, f) in enumerate(R, 1):
        est = "OK" if ok else ("INCÓGNITA" if ok is None else "NO")
        L.append(f"| C{i} | {r} | {est} | {q} | {f} |")
    open("COHERENCIA.md", "w").write("\n".join(L))
    print("\n".join(L[-len(R) - 2:]))
