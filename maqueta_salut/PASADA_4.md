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
| 3 | Ángulo de la L: medido en los mapas 2D (no en vistas inclinadas) = 94,6° (Google) / 96,4° (Bing); los edificios vecinos son paralelos a la calle y perpendiculares al ala. Los 102–112° anteriores salían de vistas 3D inclinadas: descartados. El desvío del ala en C02 tiene otra causa (posición de la torre respecto al ala o deformación de la foto de época). | Z23, Z25, Z26, Z18 ×C02 | THL = 95 (aplicado); causa del desvío en C02 abierta |

Pendiente: Z21×C02 (concha) y Z29×C01, que dependen de 1 y 3.

## Búsqueda de la implantación (L_CHF, T_POS, ESC_X) – solo anotación
Cámaras calibradas solo con la torre (C04 3,3 px, C02 6,7 px), trasladadas con la torre al moverla en planta.

| Configuración | Fin del chaflán en C04 (foto x=455) | Escalera oculta en C04 | Ala en C02 | Error total |
|---|---|---|---|---|
| Actual: chaflán 20 m, torre al 58 % | −75 px (chaflán corto por el lado del hotel) | asoma 22 px | fin del ala a 90 px | 52 px |
| Mejor encontrada: chaflán 22 m, torre al 30 % | +5 px | asoma 35 px | fin del ala a 63 px | 37 px |

Lectura:
- C04 (la foto fiable) pide que el chaflán se prolongue por el lado del hotel: con la torre fija, el chaflán sigue ~6 m más hacia el ala larga. Eso equivale a torre **más a la izquierda** del centro del chaflán (≈30 %), no a la derecha.
- Ninguna combinación oculta la escalera en C04 y encaja a la vez el ala en C02: o la escalera no está donde la tenemos, o C02 (foto de época) no es fiable para el ala.
- No aplicado: contradice la hipótesis de torre algo a la derecha; pendiente de decisión.

## DECISIÓN de implantación (por medición en planta real, no por perspectiva)
Método: el mapa 2D de Google es una proyección ortogonal de la planta. Se miden ahí directamente, sin cámaras:
- escala = ancho del ala (12,74 m) → 12,26 px/m; comprobación: círculo gris = columna, radio 2,9 m (cuadro 3,25) ✔
- eje de la torre (centro del círculo gris) a **3,4 m de la cara exterior del ala** y 9,3 m de la interior.
- ángulo ala–calle 94,6° (Bing 96,4°).
Con chaflán de 20 m a 45° eso sitúa la torre al **84 %** del chaflán (a la derecha, junto a la fachada exterior del ala).
Comprobación independiente en C04 (foto frontal): el arranque del chaflán cae en x=92 (foto: banda del restaurante acaba en 80) y la banda del hotel sigue **10,6 m por la fachada exterior del ala** hasta x=455, donde empieza el muro del relieve (concha). Las dos fuentes son coherentes.
Aplicado en el cuadro: T_POS = 0,837 · D_HOTF = 10,6. Queda abierto: la escalera sigue asomando en C04.
