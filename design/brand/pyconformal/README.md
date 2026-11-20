# Fuentes de la marca PyConformal

**Firma activa:** [function-wordmark/](function-wordmark/README.md). Integra la f matemática y el sello Peirce. Las variantes descritas abajo son el primer bosquejo conservado como histórico.


Diseño preparado para el proyecto de César Augusto Vega Penagos, 20 de noviembre de 2026.

## Archivos editables

- `pyconformal-mark.svg`: original limpio del sello. Curvas y punto definidos como vectores; no requiere fuentes tipográficas.
- `pyconformal-construction.svg`: bosquejo con retícula, círculo y cuadrado de referencia. Las guías son auxiliares de diseño y no forman parte del logo final.
- `pyconformal-mark-monochrome.svg`: variante de una tinta para documentos sobre fondo blanco.
- `pyconformal-wordmark-light-background.svg`: sello y nombre para fondos claros.
- `pyconformal-wordmark-dark-background.svg`: sello y nombre para fondos oscuros.

Los SVG se pueden editar en Inkscape, Illustrator o Figma. El nombre en los logotipos horizontales sigue siendo texto editable (Segoe UI, con alternativas Arial y sans-serif); antes de entregar un archivo de imprenta, convertir ese texto a trazados en el editor elegido. El sello original ya está formado por trazados y formas vectoriales.

## Concepto y construcción

El contorno pasa de una curva redondeada a una frontera cuadrada. Los trazos interiores sugieren una retícula transformada y el punto dorado recuerda el punto que se sigue en los experimentos. Es un símbolo gráfico: sus curvas no representan una aplicación conforme calculada ni una proyección específica.

Lienzo del sello: 96 × 96 unidades. Fondo verde con radio de 24 unidades. Contorno principal entre las coordenadas 16 y 80. Punto destacado en (31, 44). El bosquejo añade guías de construcción en una mesa de 128 × 128 unidades.

Colores: verde `#153D31`, crema `#F2D9A2`, verde suave `#7AA997`, dorado `#EFBB68`. Mantener las proporciones y dejar alrededor al menos 12 unidades del lienzo original. Para usos pequeños, utilizar el sello sin el nombre ni el descriptor.

## Uso en web, documentos y artículos

La web utiliza una copia del original en `web/landing/pyconformal-mark.svg`, incluida en el manifiesto de publicación. Si se modifica el diseño, actualizar el original de esta carpeta y esa copia de la web a la vez.

Para documentos que admitan SVG, insertar el archivo vectorial directamente. Para un artículo, usar la versión monocromática y exportar desde el editor a PDF vectorial o al formato que solicite la revista. Para promoción, usar el logotipo horizontal correspondiente al color del fondo; si hace falta una imagen rasterizada, exportar a PNG con resolución suficiente desde el original. No usar capturas de pantalla como fuente.

El sello identifica el proyecto. La cita del software y los créditos científicos se mantienen por separado en los recursos del repositorio.
