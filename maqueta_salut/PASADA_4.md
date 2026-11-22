# Pasada 4 – celdas «?R» recomprobadas con la planta nueva (sin corregir nada)

Cámaras calibradas solo con la torre y con la dirección limitada al frente del chaflán (la torre es simétrica: sin esa condición la cámara salía invertida): C04 3,3 px · C02 6,7 px.

## Siguen bien con la planta nueva
- Alturas de la base (+3,2 / +7,3) en C04 y C08.
- Banda del restaurante: continúa por la calle; su extremo cae donde la foto (69 vs 80 px).
- Columna recta, marquesina, caja de ladrillo elevada, escalera (ancho, lamas y encuentro).

## NO agrupados por causa (para corregir juntos en el cuadro de cotas)
| # | Causa | Celdas | Cota del cuadro |
|---|---|---|---|
| 1 | Por el lado del hotel el chaflán queda ~5,8 m corto (o la torre demasiado a la derecha): en C04 el muro del relieve debería empezar en x=455 y empieza en 391 | Z13×C04, Z21×C04 | L_CHF / T_POS |
| 2 | La escalera asoma por la derecha del barril vista de frente | Z29×C04 | ESC_X (más hacia la izquierda/detrás) o T_POS |
| 3 | Ángulo de la L: con 90° el ala larga y el ala corta salen mal orientadas en C02 (final del ala a 130 px); con ~110° encajaban | Z23, Z25, Z26, Z18 ×C02 | THL |

Pendiente: Z21×C02 (concha) y Z29×C01, que dependen de 1 y 3.
