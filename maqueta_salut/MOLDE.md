# Versión molde – STL para molde de silicona y colada de hormigón

`Hotel_Salut_15cm_MOLDE.stl` · escala 1:339 · caja 142 × 299 × 150 mm · volumen 877 cm³ · una sola pieza: sí · estanco: sí · aristas abiertas: 0 · aristas no manifold: 0 · base plana a z = 0

`Hotel_Salut_15cm_MOLDE_baja.stl` (para compartir): la misma geometría con la malla simplificada a 0,012 mm de maqueta · 28706 triángulos (1.4 MB, frente a 71822 y 3.6 MB) · volumen 877 cm³ · estanco, sin aristas abiertas ni no manifold

## Criterios (1 mm de maqueta = 0,34 m reales)
| criterio | valor real | en la maqueta |
|---|---|---|
| grosor mínimo de cualquier elemento | 0.55 m | 1.6 mm |
| rendija o hueco mínimo | 0.33 m | 1.0 mm |
| relieve mínimo | 0,25 m | 0.7 mm |

## Qué cambia respecto a la versión de detalle
- Barandillas abiertas (cubierta del barril, visera, azoteas, terrazas): fuera. En hormigón no se pueden colar.
- Balcones: canto, ranura de 0,27 (0,8 mm) y poyete en **una sola banda** de 1,64. El hueco de 1,46 entre bandas se mantiene, a 1,2 de fondo (3,5 mm).
- Aletas y vigas radiales de 0,40 → 0,70 (2,1 mm).
- Tambor macizo hasta la banda: sin el pasillo de servicio ni el peto de 0,25. Banda acristalada sin montantes.
- Letrero САЛЮТ: letras en volumen de 0,6 de fondo (trazo engrosado 0,12), pegadas al remate. Separadas a 1,5 m, como en la versión de detalle, se romperían al desmoldar.
- Escalera: la pantalla de lamas (0,08 cada 0,35) se cuela como volumen macizo. El muro de coronación, el peto y los forjados vistos pasan a 0,60.
- Petos de la terraza, la rampa y la meseta: 0,25–0,30 → 0,60. Sin marcos de ventana (relieve de 0,08) ni montantes del chaflán.
- Muro final de la fachada retranqueada del ala larga y fondo del barril, a 0,6–0,7. (La fuente ya no está en ninguna de las dos versiones: la quitó el usuario el 27/11.)
- Se mantienen: forjados y huecos del barril, ojos (Ø 1,6, 4,7 mm), visera, remate, claraboya, rampa, concha, ventanas del ala larga, los 10 lucernarios piramidales del bloque alto (base 3,8 mm, alto 3,5 mm), los 6 lucernarios bajo el cuello, columna, cuello y vigas.

## Comprobación por cortes (95 detecciones en 36 piezas)
| tipo | dónde | cortes | área máx. (m²) |
|---|---|---|---|
| fino | planta (12.4, 16.3) | 4 | 1.10 |
| fino | radial 30° (-32.4, 6.9) | 1 | 0.28 |
| fino | radial 210° (32.4, 6.9) | 1 | 0.28 |
| fino | planta (12.9, 11.6) | 2 | 0.22 |
| fino | planta (5.6, 17.5) | 2 | 0.22 |
| fino | planta (-22.0, 9.5) | 7 | 0.18 |
| rendija | planta (11.1, 16.4) | 9 | 0.17 |
| rendija | planta (2.3, 13.5) | 9 | 0.17 |
| fino | radial 90° (15.5, 11.4) | 1 | 0.15 |
| fino | radial 270° (-15.5, 11.4) | 1 | 0.15 |
| fino | planta (8.9, 15.4) | 2 | 0.13 |
| fino | planta (10.2, 14.7) | 2 | 0.13 |
| fino | planta (7.3, 15.5) | 2 | 0.12 |
| fino | planta (17.6, 21.3) | 7 | 0.12 |
| rendija | planta (5.7, 27.6) | 9 | 0.11 |
| fino | planta (-5.5, 17.3) | 1 | 0.10 |
| fino | planta (-22.7, -0.3) | 1 | 0.10 |
| fino | planta (-21.4, 6.5) | 1 | 0.10 |
| fino | planta (-22.5, -2.2) | 1 | 0.10 |
| fino | planta (-22.9, 1.6) | 1 | 0.10 |
| fino | planta (-23.0, 3.5) | 1 | 0.10 |
| fino | planta (-23.2, 5.4) | 1 | 0.10 |
| fino | planta (-21.2, 4.6) | 1 | 0.10 |
| fino | planta (-20.7, -1.1) | 1 | 0.10 |
| fino | planta (-20.9, 0.8) | 1 | 0.10 |
| fino | planta (-21.1, 2.7) | 1 | 0.10 |
| rendija | radial 90° (15.5, 11.7) | 1 | 0.09 |
| rendija | radial 270° (-15.5, 11.7) | 1 | 0.09 |
| rendija | radial 45° (5.0, 47.4) | 1 | 0.08 |
| rendija | radial 225° (-5.0, 47.4) | 1 | 0.08 |
| rendija | planta (5.3, 17.6) | 2 | 0.08 |
| rendija | planta (13.1, 11.8) | 2 | 0.08 |
| rendija | planta (4.6, 22.7) | 14 | 0.06 |
| rendija | planta (10.5, 14.2) | 1 | 0.04 |
| rendija | planta (9.9, 17.6) | 1 | 0.04 |
| rendija | planta (2.0, 11.9) | 1 | 0.04 |
