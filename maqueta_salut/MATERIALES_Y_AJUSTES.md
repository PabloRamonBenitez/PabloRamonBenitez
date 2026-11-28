# Materiales para imprimir el máster del molde y holgura del encaje (investigación del 28/11)

Búsquedas en internet sobre (1) qué conviene imprimir para hacer tú el molde de silicona y (2) qué holgura usar en un encaje cilindro–hueco. Lo que sigue distingue **lo que dicen las fuentes** de **lo que deduzco yo**. Las fuentes son guías de fabricantes y de la comunidad: no he podido abrir las páginas completas, solo sus resúmenes de búsqueda.

## 1. Qué imprimir
| Qué | Material | Veredicto | Por qué |
|---|---|---|---|
| **Máster de la maqueta** (el positivo sobre el que viertes la silicona) | **Resina SLA** | **La mejor opción** | Es la que da el acabado más liso; los detalles de ≈ 1 mm de esta maqueta solo los reproduce bien la resina. |
| | PLA o PETG (FDM) | Posible, con trabajo | Las líneas de capa se copian a la silicona: hay que lijar y sellar (p. ej. con XTC-3D). La resolución de FDM es la más baja. |
| | ABS | No lo recomiendo | Necesita ventilación y cama caliente; no aporta nada frente a PLA o PETG. |
| **Carcasa rígida** (el molde madre que sujeta la silicona) | PLA o PETG | Buena opción | No necesita acabado fino; sí **llaves de registro**, desmoldeante y conicidad de 5–10° en las paredes verticales. |

### Buenas prácticas para el máster de resina
- **Curado total antes de verter:** lavar y poscurar por completo. La resina sin curar impide que fragüe la silicona de platino (Smooth-On, LIQCreate).
- **Platino o estaño:** el platino es más propenso a la inhibición con masters de resina; la silicona de **estaño tolera mejor** la resina y es más barata, pero dura menos y se mezcla por peso. Si no necesitas la durabilidad del platino, el estaño evita muchos fallos.
- **Sellar y desmoldear:** Smooth-On sugiere sellar con XTC-3D o con un acrílico en spray brillante (Krylon Crystal Clear) y aplicar después un desmoldeante (Ease Release 200 o 205). Hay usuarios que dicen que el spray acrílico solo ayuda a medias: **probar antes con una pieza de descarte**.
- **Rincones profundos:** a veces no reciben suficiente luz UV para curar del todo; las resinas transparentes curan más parejo que las opacas.

### Tamaño
La pieza A del molde partido mide 142 × 190 × 150 mm: es grande para una impresora de resina de sobremesa. Comprueba que el volumen de impresión sea al menos ese, o encárgala a un servicio (el CSIC describe una SLA de 335 × 200 × 300 mm).

## 2. Holgura del encaje
**Aclaración sobre las unidades:** 0,15 m es en el edificio real. En la maqueta (1:339) son **0,44 mm por lado**, es decir 0,9 mm de diferencia entre el diámetro del hueco y el del cilindro.

### Lo que dicen las fuentes (piezas **impresas**)
| Proceso | Holgura de diseño que da un ajuste deslizante | Fuente |
|---|---|---|
| Resina SLA | 0,025–0,06 mm (Formlabs: 0,05 con resina Tough, 0,0625 con Durable; BU: 0,025) | Formlabs, BU |
| FDM | 0,15–0,4 mm; Snapmaker propone 0,3–0,5 mm para huelgos; el aula de fabricación del CCI parte de 0,1 mm por lado, avisa de que **0 mm suele ser demasiado justo** y de que depende del material y de la orientación de impresión | Snapmaker, CCI, UMD |
| Siempre | Imprimir una **pieza de prueba** con tu impresora y tu material antes de la pieza final | todas |

### Lo que NO he encontrado
Ninguna fuente da holguras ni tolerancias para **piezas coladas en hormigón** que encajan entre sí. Solo dicen que la precisión baja al aumentar el número de coladas del mismo molde, y que la silicona de adición se anuncia sin contracción propia (afirmación de fabricantes). La contracción del propio hormigón no sale en los resultados.

### Mi conclusión (deducción mía, no de las fuentes)
- Tus piezas **se cuelan en hormigón**, no se imprimen. La superficie del hormigón es rugosa y tiene burbujas, y el molde de silicona flexa. Por eso las holguras de la resina (0,05) quedan muy cortas.
- **0,44 mm por lado queda en el extremo generoso de lo que se usa en FDM**: el encaje no se atascará, pero tendrá juego. El cilindro lo centra, y el asiento plano del cuello (Ø 53 mm) evita que se incline. El juego lateral de 0,4 mm sí podría dejar un escalón de ese tamaño donde se cortan las dos mitades de la escalera.
- Antes de fijar el valor haría una **pieza de prueba**: el cilindro y el hueco a escala con cuatro holguras (0,2 · 0,3 · 0,4 · 0,5 mm por lado) y con la llave y el canal. Se imprime en resina, se cuela una pareja en hormigón y se elige la que cierre bien. Si no tienes tiempo, partiría de **0,3 mm por lado** (0,1 m reales).
- La llave y el canal tienen la misma lógica: nervio de 3,5 mm y canal de 4,4 mm. El juego lateral de la llave es el que más importa para que la escalera coincida.

## Fuentes
- Formlabs, [cómo hacer moldes de silicona](https://formlabs.com/eu/blog/how-to-make-silicone-molds/) · Xometry, [moldes impresos para colada](https://xometry.pro/en/articles/3d-printed-molds-for-casting/)
- Smooth-On: [FAQ de inhibición](https://smooth-on.com/support/faq/210), [guía de moldeo de resina UV](https://smooth-on.com/assets/pdf/Molding%20UV%20Cured%20Resin%20Best%20Practices%20Guide.pdf), [guía de selladores y desmoldeantes](https://www.smooth-on.com/assets/pdf/Sealer_and_Release_Agent_Reference_Guide.pdf), [XTC-3D](https://www.smooth-on.com/products/xtc-3d/)
- [Hackaday: inhibición del curado](https://hackaday.com/tag/cure-inhibition/) · [foro de Formlabs](https://forum.formlabs.com/t/posting-again-mold-making-help/15726) · [LIQCreate](https://www.liqcreate.com/?p=21956)
- Tolerancias: [Formlabs](https://formlabs.com/global/blog/3D-printing-tolerances-for-engineering-fit/) · [Snapmaker](https://www.snapmaker.com/blog/3d-printing-tolerances) · [BU EPIC (SLA)](https://www.bu.edu/epic/files/2025/05/SLA_Tolerances.pdf) · [CCI](https://wiki.cci.arts.ac.uk/books/digital-fabrication-lab/page/design-the-clearance-and-tolerance) · [UMD](https://dozuki.umd.edu/Guide/Tolerancing/306)
- Moldes de dos partes y llaves: [MatterHackers](https://matterhackers.com/articles/how-to-use-3d-printing-to-make-two-part-silicone-molds) · [Prusa](https://blog.prusa3d.com/the-beginners-guide-to-mold-making-and-casting/) · [Make](https://makezine.com/projects/making-a-hard-shell-mold)
- Silicona y hormigón: [Elkem](https://magazine.elkem.com/faq/how-can-silicone-molds-be-used-for-casting-concrete-objects-or-parts/) · [Wacker](https://wacker.com/cms/en-de/products/applications/moldmaking/construction-molding/construction-molding.html)
- Impresión SLA grande en España: [CSIC](https://csic.es/en/node/136823)
