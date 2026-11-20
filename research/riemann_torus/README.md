# Aplicación: del toro cuadrado a la esfera de Riemann

Propuesta implementada el 20 de noviembre de 2026. Ejemplo clásico de superficies de Riemann que amplía la galería; no constituye todavía una contribución científica nueva ni decide la ruta del artículo.

## Matemática y alcance

La identificación de lados opuestos del cuadrado define el toro complejo T = C/(Z+iZ). Con k=1/√2 y K=K(k), la función F(z)=2/sn²(2Kz,k)−1 es elíptica, de períodos 1 e i. Es una normalización de la función de Weierstrass del retículo cuadrado. Es par: F(−z)=F(z).

F define un recubrimiento meromorfo de grado dos del toro sobre la esfera de Riemann. Los puntos 0, 1/2, i/2 y (1+i)/2 tienen imágenes ∞, +1, −1 y 0. Son puntos de ramificación. En 0 hay un polo doble: la coordenada esférica local 1/F tiene un cero doble. En los otros tres se anula F′. La conformalidad local se cumple fuera de estos cuatro puntos; no hay una equivalencia conforme biyectiva entre el toro y la esfera.

La figura tridimensional ilustra la identificación topológica. Su métrica inducida en R³ no representa la métrica plana de la carta compleja. Los cálculos se realizan en la carta; girar la figura no modifica F.

## Evaluación numérica

Se evalúa F=√2(θ₄(πz,q)/θ₁(πz,q))²−1, con q=exp(−π), usando nueve términos y reducción por períodos. Las coordenadas homogéneas [√2 θ₄²−θ₁² : θ₁²] permiten representar la esfera, incluido el polo, sin introducir un valor infinito numérico. Las derivadas se obtienen derivando la serie theta.

La validación independiente usa mpmath a 70 cifras y su función sn, no la misma implementación theta. Treinta puntos incluyen semiperíodos, puntos regulares y proximidad al polo. También se verifican períodos sin reducción previa, paridad, norma esférica y derivada mediante diferencias finitas. Los resultados completos están en validation/results.json.

## Fuentes

- Solanilla, Oostra y Yáñez (2016), *Peirce quincuncial projection*, https://doi.org/10.18273/revint.v34n1-2016002. Antecedente del proyecto.
- Solanilla, Leal y Tique (2021), *Inverses and n-uncial property of Jacobian elliptic functions*, https://doi.org/10.3233/JCM-215014. Se consultó el resumen editorial, que relaciona funciones inversas de Jacobi, toros y paralelogramos y señala la implementación numérica como perspectiva. No se obtuvo ni se revisó aquí el texto completo. Este ejemplo no se atribuye como reproducción de su familia de proyecciones.
- NIST DLMF, https://dlmf.nist.gov/20.2, https://dlmf.nist.gov/22.2, https://dlmf.nist.gov/22.4 y https://dlmf.nist.gov/23.6. Definiciones theta, cocientes de Jacobi, períodos y relaciones con Weierstrass.

## Qué falta revisar y qué sigue

1. Leer el artículo completo de 2021 y construir la correspondencia entre sus fórmulas, dominios, cortes y normalizaciones y nuestra implementación.
2. Estudiar las inversas por hojas, con cortes entre valores de ramificación y continuación analítica. La aplicación actual muestra F, no una inversa global.
3. Considerar retículos rectangulares y un parámetro τ con Im τ>0. Requiere cambiar el módulo, los períodos y los controles; no basta deformar el dibujo del toro.
4. Decidir juntos si interesa una extensión didáctica o un problema de investigación: estabilidad cerca de ramificaciones, selección de hojas o comparación reproducible de algoritmos. Su novedad requiere revisión bibliográfica adicional.

## Uso

Arrastrar P o usar u,v; Q≡−P comparte imagen. Sumar 1 o i cambia el representante. Los cuatro botones muestran la ramificación. El control de giro afecta solo la vista tridimensional. La página tiene versiones española e inglesa en el generador existente.

## Comprobación de la integración

El generador produjo 92 páginas y verificó 2162 enlaces y fragmentos locales. Pasaron 31 pruebas del generador, política e idiomas y 76 comprobaciones de páginas en Edge (19 casos × 2 idiomas × 2 tamaños). Se revisaron capturas de escritorio y móvil. Detalles en validation/qa.json. Integración local; esta aplicación no se ha publicado.
