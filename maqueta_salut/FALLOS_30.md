# Pasada 16 – revisión de investigador: 31 fallos (28 corregidos, 3 anotados)

Método: cada pieza contra las fotos donde se ve (F09 telefoto casi ortogonal: 12,9 px/m por los forjados; F08 desde
arriba; F73, F36, F72), contra las otras vistas (planta/sección/alzado salen del mismo 3D) y contra la lógica
constructiva. Cada corrección tiene su comprobación automática en `coherencia_vistas.py` (44/44 OK).

## Parte alta (tambor, banda, visera, remate)
| # | fallo | prueba | corrección |
|---|---|---|---|
| 1 | Remate bajo (+49,1) | F09: 82 px = 6,4 m sobre el borde de la visera | **+50,1** |
| 2 | Remate ancho (R 5,15) | F09 9,8 · F08 9,7 · F14 10,3 · F01 10,0 · F70 9,6 | **R 4,95** |
| 3 | Visera desplazada en la dirección equivocada (−0,4; −4,2) | F09 (frontal) centro 2,3–2,5 m a la izquierda del tambor; F08 1,7 m a la izquierda en otra dirección → sistema de 2 ecuaciones | **(−2,4; −2,15)** |
| 4 | El tambor era macizo hasta la banda | F08: pasillo de servicio y peto entre tambor y banda | pasillo + peto de 1 m |
| 5 | La banda arrancaba sobre la coronación del tambor | F08: arranca en el pasillo | banda desde +37,2 |
| 6 | Cubierta de la visera sin barandilla | F08: barandilla perimetral | barandilla 1 m |
| 7 | Cubierta del barril con peto de 0,4 | F08: barandilla tubular | peto + barandilla 1,1 m |
| 8 | Escalera coronaba a +39,0 | F08: la caja sube hasta debajo de la visera | **+40,5** |
| 9 | Radio de la banda: F09 10,4 / F08 11,9 | contradicción entre fotos | ANOTADO (se mantiene 10,85) |

## Ala larga
| # | fallo | prueba | corrección |
|---|---|---|---|
| 10 | La concha tapaba el hueco 11 (y el 3D tenía una pieza invertida por el marco metido en la concha) | F73 ve el hueco 11 sobre la concha | curva desde **55,9**, pie a 58,9 (Bing 59,67: 0,8) |
| 11 | La planta baja hundida y el arco usaban 59,67 aparte de la concha | coherencia planta/alzado | ligados al pie de la concha |
| 12 | Cota en planta "35,13" fija | no coincidía con la geometría | cota calculada "pie concha" |
| 13 | Sin peto sobre la banda del hotel (caída de 7,2 m) | lógica constructiva | peto +8,5 |
| 14 | Sin entrada de la rampa 1 a la terraza | lógica de recorrido | abertura de 3 m en el peto |
| 15 | Azotea del bar sin barandilla en sus lados largos | F73 barandilla roja a lo largo | barandillas |
| 16 | La meseta de la rampa 2 se metía 0,3 m en las lamas | choque de volúmenes | arranca en el frente de lamas |
| 17 | Rótulo del peto en planta "+8,20" (fijo) | cuadro: 8,50 | sale del cuadro |
| 28 | Rótulo de nivel "+11,50 bloque alto" en secciones y alzados | es también la cubierta del bar | "cub. bar / bloque alto" |

## Planos, tablas y cuadro
| # | fallo | corrección |
|---|---|---|
| 18 | Título PLANTA 4 "corte a +25,9" (corta a +25,20) | calculado |
| 19 | Título PLANTA ÚLTIMA "+35,1" (corta a +35,00) | calculado |
| 20 | Subtítulo de todas las hojas citaba solo 4 fotos | lista real |
| 21 | Tabla de coherencia: "chaflán 28,9 (12,8+6,5+9,6)" de la planta antigua | 20,0 Google/usuario |
| 22 | Tabla de coherencia: remate 49,1 | 50,1 |
| 23 | Nota "pendiente: ángulo del chaflán 31° de tu esquema" | L 95° ± 2,3; fondo del ala corta |
| 24 | Regla de planos2d "caja en coordenadas radiales" (siempre OK, no comprobaba nada) | regla real: cuña en el hueco y corona = visera |
| 25 | 8 cotas muertas en el cuadro (ESC_L, ESC_REC, ESC_RL, ESC_RW, ESC_WY, VEN_PTA, R_MES, D_CUNA) | retiradas |
| 26 | `cotas.elementos()` seguía con la escalera rectangular | cuña |
| 27 | Catálogo de puntos con la escalera antigua (entrante) | bordes del hueco y de la cuña |
| 29 | Flecha "N aprox." = eje del ala | F36 (Google, norte arriba): el ala va a ~66° del N → flecha girada |

## Anotados (sin corregir: falta una segunda foto)
| # | fallo | prueba |
|---|---|---|
| 30 | Coronación del ala corta: en F72 baja en diagonal ~4 m hacia la torre; el plano la tiene horizontal a +11,5 | F72 (personas como escala: 46 px/m) — F01 la ve plana con lucernarios |
| 31 | Banda del hotel en F01 a 42 px con cualquier cámara | F01 |
