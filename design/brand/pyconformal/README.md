# Identidad final de PyConformal

Selección de Cesar A. Vega Penagos, 20 de noviembre de 2026. Conserva la silueta del monograma y la superficie de la referencia elegida, con retícula azul mineral, letras verdes y punto cobre. En el nombre, la f se sustituye por la f matemática cursiva. La marca se sigue escribiendo y leyendo PyConformal. La biblioteca y sus citas conservan PyConformal Engine.

## Archivos necesarios

- `logo.svg`: símbolo y nombre debajo.
- `horizontal.svg`: firma para cabeceras.
- `symbol.svg`: símbolo detallado, sin nombre.
- `wordmark.svg`: nombre con f matemática.
- `icon.svg`: monograma con trazos finos retirados para tamaños pequeños.
- Los sufijos `-dark` indican versiones claras para fondos oscuros.
- `monochrome.svg`: logotipo negro para documentos.
- `reference-original.png`: única referencia raster conservada, separada de los SVG.
- `preview.html`: prueba sobre fondos claros y oscuros y de iconos a tamaño real.
- `logo-kit.zip`: paquete portátil de estas fuentes.

Los SVG tienen transparencia real, trazados editables y grupos separados. No contienen PNG incrustados, scripts, texto dependiente de fuentes ni recursos externos. Se conserva el trazado de la imagen original; sus bordes no son las curvas Bézier generativas originales. La separación de monograma y retícula se infiere de sus grosores y puede retocarse en un editor vectorial. El glifo matemático de la f se entregó como contorno de Cambria Math, sin distribuir el archivo tipográfico.

## Colores

Verde #0A4F3C; marfil #F8F1E3; azul mineral #4D879B; cobre #C47754. Sobre oscuro: azul #8CC2D0 y cobre #D9A086. Mantener las proporciones de cada viewBox. Para tamaños pequeños, usar icon.svg y reservar symbol.svg para formatos mayores.

## Copias de publicación

La web usa web/landing/pyconformal-mark.svg (icono y favicon), pyconformal-symbol.svg (símbolo detallado), pyconformal-wordmark-dark.svg (sobre fondos oscuros) y pyconformal-wordmark-light.svg (sobre fondos claros). Son copias necesarias para el sitio estático; la carpeta de diseño es el original de entrega. El historial de Git conserva las exploraciones retiradas.
