"""Estimación por rangos: cada fuente da un valor con su margen (σ); se combinan por media ponderada (1/σ²) y se
comprueba que cada fuente cae dentro del rango combinado (2σ). Fuentes fuera de rango quedan señaladas."""
import math
EST = {
 "Distancia del eje de la torre a la fachada exterior del ala (m)": [
   ("Foto frontal C04 (búsqueda de implantación)", 11.4, 5.0),
   ("Mapa Google (orientativo)", 3.5, 4.0),
   ("Restitución F01 con puntos de satélite", 12.2, 6.0),
   ("Tu esquema (torre algo a la derecha)", 6.8, 3.0)],
 "Ángulo de la L, ala larga – calle (°)": [
   ("Mapa Google 2D", 94.6, 4.0), ("Mapa Bing 2D", 96.4, 4.0),
   ("Triangulación satélite A-B-C-D-E", 94.0, 12.0), ("Foto aérea C02 (ajuste del ala)", 110.0, 10.0),
   ("Tu indicación (esquina original recta)", 90.0, 5.0)],
}
def combina(fuentes):
    w = [1 / s ** 2 for _, _, s in fuentes]; m = sum(v * wi for (_, v, _), wi in zip(fuentes, w)) / sum(w)
    sg = 1 / math.sqrt(sum(w)); return m, sg
if __name__ == "__main__":
    out = ["# Estimaciones por rangos (combinación de fuentes)", ""]
    for q, f in EST.items():
        m, sg = combina(f)
        out += [f"## {q}", f"**Resultado: {m:.1f} ± {sg:.1f}**", "", "| Fuente | Valor | Margen | ¿Dentro de 2σ? |", "|---|---|---|---|"]
        for n, v, s in f:
            ok = abs(v - m) <= 2 * math.hypot(s, sg)
            out.append(f"| {n} | {v} | ±{s} | {'sí' if ok else 'NO'} |")
        out.append(""); print(q, round(m, 2), round(sg, 2))
    open("ESTIMACIONES.md", "w").write("\n".join(out).replace(".", ",").replace("ESTIMACIONES,md", "ESTIMACIONES.md"))
