# Sistema de comprobación del modelo contra las fotos

## Herramientas (en esta carpeta)
- `fotos_F01-F24.png`, `fotos_F25-F46.png`: catálogo numerado de las 46 imágenes de la conversación.
- `superponer.py`: renderiza el modelo con una cámara en perspectiva y dibuja sus aristas en rojo sobre la foto, con el volumen velado en azul. La diferencia se ve directamente, sin interpretarla.
- `calibrar.py`: calcula la cámara de una foto por mínimos cuadrados. Usa las siluetas de los cilindros (barril, tambor, remate, columna) y aristas rectas de la base leídas en la foto.

## Bucle de comprobación
1. Para cada foto F: calibrar la cámara con elementos seguros (la torre).
2. Superponer el modelo completo.
3. Anotar en la matriz rasgo × foto: OK / NO / no visible.
4. Corregir solo en las plantas o secciones (fuente única), regenerar el volumen y volver al paso 1 con TODAS las fotos.
5. Terminar cuando todas las superposiciones coinciden a la vez.

## Primer barrido: F01 (foto aérea de época)
- Torre (barril, tambor, visera, remate, columna): la calibración por cilindros cierra con un error de unos 3–5 px. OK.
- Base: NO coincide. Con la cámara que encaja la torre, el ala larga del modelo queda detrás de la torre, mientras que en la foto sale en diagonal hacia la derecha.
- Ajustar a la vez la cámara y el ángulo del chaflán no converge a una solución física: las aristas de la base que leí en la foto son incompatibles con la planta actual. La relación torre–L de la planta está mal, no solo los detalles.
- Siguiente paso: fijar la planta torre–L midiendo en la vista de Bing (F35/F36, casi ortofoto) y repetir el barrido sobre F01, F09, F14, F18, F23, F31 y F41.
