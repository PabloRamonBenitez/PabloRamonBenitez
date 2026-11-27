# Método de comprobación (desde el 26/11, tarde)

Nada se entrega sin pasar, **en este orden**, las cinco puertas. Si una falla, se corrige y se vuelve a empezar por la 1.

| # | Puerta | Herramienta | Qué detecta | Criterio para pasar |
|---|---|---|---|---|
| 1 | **Reglas del usuario** | `auditoria_planos.py` (D) | Decisiones ya tomadas y que no se pueden perder: sin 90° en el rincón de la L, línea posterior paralela al chaflán, triangulación A–B / A–C / A–D exactas y D–C ≤ 1,5 %, testero sin tacón, base de la torre en ángulo recto | 0 incumplimientos |
| 2 | **Coherencia 3D ↔ cuadro ↔ catálogo** | `coherencia_vistas.py`, `planos2d.py` | Que el 3D tenga lo que dice el cuadro de cotas: sondas de macizo y vacío, huecos y piezas | 100 % OK |
| 3 | **Dibujo** (Ching y normas) | `auditoria_planos.py` (A, B, C) y `AUDITORIA_NUDOS.png` | Astillas, rendijas de < 0,20 m y nudos entre contornos en **todas** las plantas y secciones. Además, una hoja con los encuentros más complejos ampliados, que se revisa uno a uno | 0 defectos; hoja de nudos revisada |
| 4 | **Fotos** | collages: `collage_alamy.py`, `collage_f09.py`, `collage_base.py`; matriz | Cada zona cambiada se superpone (foto al 50 %, misma escala por paso de forjados) en **todas** las fotos de la matriz que la muestran; las fotos oblicuas, por proporciones | ninguna celda NO |
| 5 | **Entregables** | `auditoria_planos.py` (D) y `organizar_dibujos.py` | Ningún PDF o STL entregado es anterior al cuadro de cotas; las láminas superadas van a `HISTORICO/` | 0 entregables antiguos |

## Reglas de representación que se comprueban a mano en la hoja de nudos
- Rampas: contorno y triángulo muy fino. La base en el arranque y el vértice en el extremo superior, sin punto. Nunca curvas de nivel.
- Una cota, una fuente: los suelos del barril salen solo de `E.niveles_suelo()`. Forjados, rellanos de la escalera, 3D y rótulos de nivel la leen de ahí, y la auditoría dibuja cada sección que corta la escalera y comprueba que cada rellano de planta coincide con su forjado.
- Dos cuerpos que se encuentran comparten **una** línea; ninguno atraviesa al otro (p. ej. el restaurante contra el pie de la escalera).
- Burbujas de ejes que no se pisan: si dos están a menos de 2 m, una baja de fila. Los puntos de corte de la torre solo llevan un tic.
- Solo líneas, sin colores; cortado grueso con trama, visto fino, por encima discontinuo.

## Por qué
El 26/11 salieron fallos ya corregidos antes: el ángulo de 90°, la X antigua, la base del tambor en diagonal y la T del cuello.
La causa fue doble:
- se comprobaba cada cambio solo contra una o dos fotos y los planos entre sí;
- se entregaban láminas fijas antiguas.

Las puertas 1 y 5 impiden lo segundo; las puertas 3 y 4 obligan a comparar con todo.
