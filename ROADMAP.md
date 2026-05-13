# 📄 PROYECTO: PyConformal Engine
**De la Matemática Simbólica (Maple 17) a una Librería Científica de Alto Rendimiento (Python)**

> **Tesis base:** Vega Penagos, C. A. & Olivero Zapata, H. A. (2015). *Implementación en software de aplicaciones conformes*. Universidad del Tolima, Facultad de Ciencias, Programa de Matemáticas con énfasis en Estadística. Director: Mg. Juan Pablo Yáñez Puentes. Jurados: Dr. Arnold Oostra Van Noppen, Dr. Leonardo Solanilla Chavarro. Calificación: 4.8 (Meritorio), 17 de diciembre de 2015.

---

## 🎯 Objetivo del Proyecto

Construir una librería de Python de alto rendimiento que sea, en sentido literal, **la tesis ejecutable**: cada capítulo se traduce en un módulo, cada teorema en una propiedad verificable mediante tests, cada figura en un notebook reproducible. El proyecto extiende explícitamente el trabajo dejado abierto en la sección de Recomendaciones de la tesis (página 59), donde se invita a determinar las soluciones numéricas de las integrales subyacentes a la transformación de Schwarz-Christoffel.

El producto final debe permitir a ingenieros, matemáticos y estudiantes de Análisis Complejo resolver problemas de mapeo conforme y visualización sin depender de software privativo (Maple, MATLAB), preservando la rigurosidad teórica de la tesis original.

---

## 🧭 Filosofía de Diseño

**Trazabilidad bibliográfica.** Cada función pública de la librería lleva en su docstring la referencia exacta al teorema, lema, corolario, ejemplo o figura de la tesis que implementa. Un lector debe poder leer la tesis con la librería al lado y ver la correspondencia uno a uno.

**Estructura pedagógica preservada.** La jerarquía de módulos refleja la jerarquía de capítulos: las transformaciones lineales del grupo P (Capítulo 1) son los bloques constructivos primarios; las funciones holomorfas/antiholomorfas (Capítulo 2) los amplían a C; las Möbius, elementales y SC (Capítulo 3) son aplicaciones concretas; el Capítulo 4 corresponde a la capa de visualización y aplicaciones cartográficas.

**Orientación tan importante como ángulos.** A diferencia de muchas implementaciones SC genéricas, esta librería distingue de primera clase entre aplicaciones holomorfas (preservan orientación, condiciones de Cauchy-Riemann Tipo A) y antiholomorfas (invierten orientación, Tipo B). Todas las APIs exponen un atributo `preserves_orientation`.

---

## 🗺️ Ruta de Trabajo (Roadmap)

### Fase 0: Cimientos del Proyecto (Setup)
* **Estructura del repositorio:** Layout `src/pyconformal/`, `tests/`, `docs/`, `notebooks/`, `examples/`, `thesis/` (PDF de referencia).
* **Empaquetado mínimo:** `pyproject.toml` con metadata, dependencias, y configuración de `ruff`, `mypy --strict` y `pytest` desde el día uno.
* **Entorno reproducible:** Gestión con `uv`. `.python-version` fijado a 3.10+.
* **Control de calidad:** GitHub Actions con lint, type-check y tests en cada push. Pre-commit hooks locales.
* **Licencia y metadata:** MIT o BSD-3. `CITATION.cff` con la cita exacta de la tesis. `README.md` con atribución a Vega Penagos, Olivero Zapata, Yáñez Puentes y la Universidad del Tolima.
* **Criterio de cierre:** `pip install -e .` funcional, `pytest` corre con un test trivial, CI verde.

### Fase 1: El Grupo P de Aplicaciones Lineales (Capítulo 1 de la tesis)
> Esta fase es nueva respecto a versiones anteriores del roadmap. Implementa el fundamento del Capítulo 1, que se omitió por error en las primeras lecturas.

* **Módulo `pyconformal.linear`:** Clases `Rotation(θ)`, `Reflection(θ)`, `Dilation(λ)` con métodos `__call__`, `inverse`, `compose`, `matrix`, `det`.
* **Estructura de grupo:** Implementar y testear las propiedades del grupo P enunciadas en el Teorema 6 (clausurativa por los 7 casos demostrados en la tesis, asociativa, neutro, inversa).
* **Tests basados en teoremas:** Cada uno de los Teoremas 1–6 se traduce en un test (`hypothesis` para variar parámetros).
* **Caracterización por matrices ortogonales** (Teorema 1) como test invariante automático.
* **Criterio de cierre:** Cobertura ≥ 95 %, los siete casos del Teorema 6 implementados como tests independientes, y un notebook `01_grupo_P.ipynb` que reproduce las Figuras 1.1, 1.2, 1.3.

### Fase 2: Aplicaciones Holomorfas y Antiholomorfas (Capítulo 2 de la tesis)
* **Clase abstracta `ConformalMap`:** Con atributos `preserves_angles: bool`, `preserves_orientation: bool` y métodos `__call__`, `inverse`, `derivative`, `compose`.
* **Subclases `HolomorphicMap` y `AntiholomorphicMap`:** Reflejan la distinción del Teorema 7 (∂f/∂z̄ = 0 vs ∂f/∂z = 0).
* **Verificación numérica de Cauchy-Riemann** (Tipo A y Tipo B de la sección 1.3.1) como test de propiedad para cualquier mapa definido por el usuario.
* **Detección automática de puntos críticos** (Teorema 10): dado un mapa f y un punto z₀, calcular el factor k de magnificación de ángulos.
* **Criterio de cierre:** Cualquier `ConformalMap` instanciable pasa automáticamente los tests de C-R en una malla de puntos de prueba; la detección de puntos críticos funciona sobre los ejemplos f(z)=z² y f(z)=z³ con los k correctos.

### Fase 3: Transformaciones de Möbius (Sección 3.2 de la tesis)
> Reordenado para empezar por la familia más simple antes de mapeos elementales transcendentes.

* **Clase `Mobius`:** Coeficientes (a, b, c, d) con restricción ad ≠ bc. Inversa analítica derivada en (3.2.2).
* **Construcción por fórmula implícita** (Teorema 11) como método de clase: `Mobius.from_three_points(z1, z2, z3, w1, w2, w3)`.
* **Variantes con punto al infinito** (Corolario 2) como métodos separados: `from_three_points_z_inf` y `from_three_points_w_inf`, correspondientes a los Casos 1 y 2 del corolario, archivo `corolario.mw`.
* **Extensión al plano complejo extendido:** Comportamiento explícito en ∞ siguiendo las ecuaciones de la sección 3.2.
* **Validación canónica:** Reproducir exactamente el Ejemplo 1 (disco unitario → semiplano superior, w = i(1−z)/(1+z), Figura 3.6) y el Ejemplo de la región en forma de media luna → cinta horizontal (Figuras 3.8 y 3.9).
* **Criterio de cierre:** Los ejemplos de la sección 3.2 se reproducen con error puntual < 10⁻¹².

### Fase 4: Mapeos Elementales y Trigonométricos (Sección 3.3 de la tesis)
* **Funciones primitivas:** `Exponential`, `Logarithm` (rama principal), `Power`, `Sine`, `Cosine`, `Tangent`, `Arcsine`.
* **Composición funcional:** El operador `@` o método `.compose()` para construir mapas como w = (e^z − i)/(e^z + i) directamente como `Mobius(...) @ Exponential()`.
* **Validación visual:** Reproducir las Figuras 3.10 (w = (e^z−i)/(e^z+i)), 3.11 (w = log((1+z)/(1−z))), 3.12 (w = tan z), 3.13 (w = sen z), 3.14 (w = Arcsen z).
* **Magnificación de ángulos** documentada con el ejemplo z² (Figuras 3.4–3.5) como tutorial visual del Teorema 10.
* **Criterio de cierre:** Las seis figuras 3.10–3.14 reproducidas a calidad de publicación.

### Fase 5: Motor de Schwarz-Christoffel (Sección 3.4 de la tesis, Teorema 12)
> Es la fase matemáticamente más densa; se aborda con toda la infraestructura ya madura.

#### Fase 5a: SC con pre-vértices conocidos
* **Implementación directa del Teorema 12:** `SchwarzChristoffel(prevertices, exterior_angles, A, B)` con la integral indefinida de la ecuación (3.4.3).
* **Integración numérica:** Cuadratura compleja vía `scipy.integrate.quad_vec` con manejo explícito de singularidades de tipo (z − xₖ)^(−αₖ/π) mediante Gauss-Jacobi.
* **Validación de los ejemplos resueltos:** Reproducir analíticamente w = sen⁻¹(z) (Figura 3.16, semiplano superior → cinta semi-infinita) verificando A = −i y B = 0 como en la tesis.
* **Caso del cuadrado** (Figura 3.17): completar numéricamente lo que la tesis explícitamente deja abierto en la página 53. Determinar A y B numéricamente para el mapeo del semiplano superior al cuadrado vía f(z) = A∫dz/((z+1)^(1/2) z^(1/2) (z−1)^(1/2)) + B.
* **Criterio de cierre:** El triángulo equilátero, el cuadrado y el rectángulo se mapean con error puntual < 10⁻⁸. El cuadrado resuelve el ejemplo abierto de la página 53.

#### Fase 5b: The Parameter Problem
* **Solver no lineal:** Implementación del método de Newton con escalado de Driscoll–Trefethen (referencia [8] de la tesis) para resolver automáticamente los pre-vértices.
* **Robustez numérica:** Estrategias de *crowding* y reformulación logarítmica para polígonos con vértices cercanos.
* **Criterio de cierre:** Mapeo automático del cuadrado, hexágono regular y un polígono no convexo con error verificable.

### Fase 6: Visualización y Aplicación Cartográfica Lunar (Capítulo 4 de la tesis)
> El Capítulo 4 de la tesis define qué significa que el proyecto esté "terminado" en sentido pleno.

* **Mallas ortogonales:** Funciones `orthogonal_grid(map, domain)` que reproducen las cuadrículas curvilíneas características de la sección 3.3 (e.g. cuadrícula ortogonal del mapeo exponencial).
* **Diagrama de flujo del algoritmo:** Implementación literal del diagrama de la Figura 4.1, expuesto como función pública `apply_conformal_to_rectangle(f, z1, z2, n_real, n_imag)`.
* **Notebook bandera `lunar_mercator.ipynb`:** Reproduce las Figuras 4.4 y 4.5 — aplicación de f(z) = z³ al rectángulo [0, 12+6i] sobre la proyección de Mercator de la Luna. Este es el ejemplo que da identidad al proyecto y debe destacarse en el README y la portada de la documentación.
* **Galería:** Cada figura de la tesis tiene su contrapartida en `examples/` como SVG/PNG generado por el código.
* **Criterio de cierre:** Las Figuras 4.2, 4.3, 4.4 y 4.5 reproducidas con un solo comando (`python -m pyconformal.examples lunar`).

### Fase 7: Documentación y Empaquetado
* **Docstrings bilingües:** Inglés en la API pública (estilo NumPy), notas técnicas extendidas en español dentro de los módulos. Cada función/clase cita el teorema, ejemplo o figura específico de la tesis.
* **Tutoriales progresivos** en notebooks:
  - `01_grupo_P.ipynb` — Capítulo 1
  - `02_holomorfas_antiholomorfas.ipynb` — Capítulo 2
  - `03_propiedades_y_puntos_criticos.ipynb` — Sección 3.1 (Teorema 10 visualizado)
  - `04_mobius.ipynb` — Sección 3.2
  - `05_elementales_y_trigonometricas.ipynb` — Sección 3.3
  - `06_schwarz_christoffel.ipynb` — Sección 3.4 y resolución del ejemplo abierto
  - `07_lunar_mercator.ipynb` — Capítulo 4 (notebook bandera)
* **Sitio de documentación:** Sphinx + MyST + `pydata-sphinx-theme`, desplegado en GitHub Pages.
* **Publicación:** Release en PyPI, registro de DOI en Zenodo, entrada en `awesome-scientific-python`.

### Fase 8 (Investigación): Proyección Quincuncial de Peirce
> Mencionada explícitamente en las Recomendaciones de la tesis (p. 59) como la extensión natural de SC.

* **Implementación de la proyección quincuncial** como composición SC + funciones elípticas de Jacobi.
* **Publicación académica complementaria:** Posible artículo corto en *SoftwareX* o *Journal of Open Source Software* presentando la librería y este caso de uso.

### Fase 9 (Opcional): Rendimiento
* **Profiling con `py-spy` o `scalene`** antes de optimizar.
* **Aceleración** con `numba` o `cython` solo en kernels críticos de integración SC.
* **Speedup objetivo:** ≥ 5× sobre la implementación pura NumPy en los kernels SC.

---

## 📋 Correspondencia Tesis ↔ Código

Tabla de trazabilidad explícita. Cada elemento matemático de la tesis tiene su contrapartida en código, test y notebook.

| Tesis (sección / teorema / figura)            | Archivo `.mw` original              | Módulo Python                                 | Test                                            | Notebook                            |
|-----------------------------------------------|-------------------------------------|-----------------------------------------------|-------------------------------------------------|-------------------------------------|
| §1.1 Rotación, reflexión, dilatación          | `algebra.mw`, `locc.mw`             | `linear.Rotation`, `Reflection`, `Dilation`   | `test_linear_basic.py`                          | `01_grupo_P.ipynb`                  |
| Teoremas 1–5 (preservación de ángulos)        | —                                   | `linear._preserves_angle()`                   | `test_theorems_1_to_5.py`                       | `01_grupo_P.ipynb`                  |
| Teorema 6 (grupo P), Corolario 1              | —                                   | `linear.GroupP`                               | `test_group_closure.py` (7 casos)               | `01_grupo_P.ipynb`                  |
| §1.3 Tipo A / Tipo B (Cauchy-Riemann)         | —                                   | `core.CauchyRiemann.verify()`                 | `test_cauchy_riemann.py`                        | `02_holomorfas.ipynb`               |
| Teorema 7 (holomorfa ⇔ preserva ángulos)      | —                                   | `core.HolomorphicMap` / `AntiholomorphicMap`  | `test_theorem_7.py`                             | `02_holomorfas.ipynb`               |
| Teorema 8 (holomorfa ⇔ preserva orientación)  | —                                   | `core.ConformalMap.preserves_orientation`     | `test_theorem_8.py`                             | `02_holomorfas.ipynb`               |
| §3.1 Teorema 9 (f' ≠ 0 ⇒ conforme)            | —                                   | `core.is_conformal_at(f, z0)`                 | `test_theorem_9.py`                             | `03_propiedades.ipynb`              |
| §3.1 Teorema 10 (magnificación factor k)      | `funcion_z_2.mw`                    | `core.angle_magnification(f, z0)`             | `test_critical_points.py`                       | `03_propiedades.ipynb`              |
| §3.1 Ejemplo f(z) = z², Figuras 3.4–3.5        | `funcion_z_2.mw`                    | `examples.square_mapping`                     | `test_z_squared.py`                             | `03_propiedades.ipynb`              |
| §3.2 Möbius (forma general)                   | `bili.mw`, `bili2.mw`, `bilineal.mw`| `mobius.Mobius`                               | `test_mobius_basic.py`                          | `04_mobius.ipynb`                   |
| §3.2 Disco → semiplano, Figura 3.6            | `disco.mw`                          | `examples.disk_to_halfplane`                  | `test_disk_to_halfplane.py`                     | `04_mobius.ipynb`                   |
| §3.2 Teorema 11 (fórmula implícita)           | `funcion_implicita.mw`              | `Mobius.from_three_points()`                  | `test_implicit_formula.py`                      | `04_mobius.ipynb`                   |
| §3.2 Corolario 2 (punto al infinito)          | `corolario.mw`                      | `Mobius.from_three_points_z_inf()`, `w_inf()` | `test_implicit_with_infinity.py`                | `04_mobius.ipynb`                   |
| §3.2 Media luna → cinta, Figuras 3.8–3.9       | `bili.mw`, `bili2.mw`               | `examples.crescent_to_strip`                  | `test_crescent.py`                              | `04_mobius.ipynb`                   |
| §3.3 Exponencial                              | `exponencial.mw`                    | `elementary.Exponential`                      | `test_exponential.py`                           | `05_elementales.ipynb`              |
| §3.3 Logaritmo y composición, Figura 3.11      | `logaritmo.mw`, `composicion.mw`    | `elementary.Logarithm`                        | `test_logarithm.py`                             | `05_elementales.ipynb`              |
| §3.3 w = (e^z−i)/(e^z+i), Figura 3.10         | `composicion.mw`                    | `examples.strip_to_disk_via_exp`              | `test_strip_to_disk.py`                         | `05_elementales.ipynb`              |
| §3.3 Trigonométricas                          | `trigonometricas.mw`                | `elementary.Sine`, `Cosine`, `Tangent`        | `test_trig.py`                                  | `05_elementales.ipynb`              |
| §3.3 w = tan(z), Figura 3.12                  | `w_tan_z_.mw`                       | `examples.tan_strip_to_disk`                  | `test_tan_mapping.py`                           | `05_elementales.ipynb`              |
| §3.3 Arcsen, Figura 3.14                      | —                                   | `elementary.Arcsine`                          | `test_arcsine.py`                               | `05_elementales.ipynb`              |
| §3.4 Teorema 12 (Schwarz-Christoffel)         | `algo.mw`, `proceso.mw`             | `sc.SchwarzChristoffel`                       | `test_sc_known_polygons.py`                     | `06_schwarz_christoffel.ipynb`      |
| §3.4 Ejemplo sen⁻¹(z), Figura 3.16            | —                                   | `examples.sc_arcsine`                         | `test_sc_arcsine_constants.py` (A=−i, B=0)      | `06_schwarz_christoffel.ipynb`      |
| §3.4 Cuadrado abierto, Figura 3.17 (p. 53) ★  | —                                   | `examples.sc_square`                          | `test_sc_square_open_problem.py`                | `06_schwarz_christoffel.ipynb`      |
| §4.1 Diagrama de flujo, Figura 4.1            | `algo.mw`, `proceso.mw`             | `viz.apply_conformal_to_rectangle()`          | `test_flow_diagram.py`                          | `07_lunar_mercator.ipynb`           |
| §4.1 f(z) = z³ y f(z) = 1/z, Figura 4.2        | `Example_11_26.mw`, `ejemplo10.mw`  | `examples.cube_and_inverse`                   | `test_cube_inverse.py`                          | `03_propiedades.ipynb`              |
| §4.2 f(z) = exp(z), Figura 4.3                | `exponencial.mw`                    | `examples.exp_polygon`                        | `test_exp_polygon.py`                           | `05_elementales.ipynb`              |
| §4.2 Mercator lunar, Figuras 4.4–4.5 ★        | `mapeo_luna.mw`                     | `examples.lunar_mercator`                     | `test_lunar_mercator.py`                        | `07_lunar_mercator.ipynb` (bandera) |

**★ = items destacados:** El mapeo del cuadrado de la página 53 resuelve un problema explícitamente abierto en la tesis. El Mercator lunar es la demostración bandera del proyecto.

---

## ✅ Estrategia Transversal

* **Testing:** `pytest` desde Fase 0. Tests de propiedades matemáticas (Cauchy-Riemann Tipo A/B, preservación de ángulos en puntos no críticos, magnificación correcta en puntos críticos) además de tests numéricos. `hypothesis` para tests basados en propiedades sobre el grupo P.
* **Type hints + `mypy --strict`** en todo el código.
* **Benchmarking continuo:** `pytest-benchmark` contra Maple 17 (snapshots de imágenes generadas en la tesis original) y, donde aplique, contra `SC Toolbox` de MATLAB (Driscoll, referencia [8] de la tesis).
* **Versionado semántico** desde la primera release pública.
* **Atribución bibliográfica** en cada commit relevante: los PRs que implementan un teorema citan número de teorema y página de la tesis.

---

## 🛠️ Stack Técnico

* **Lenguaje:** Python 3.10+ (API pública en inglés).
* **Cálculo numérico:** `numpy`, `scipy` (integración compleja con `quad_vec`, optimización con `optimize.fsolve` para el parameter problem).
* **Visualización:** `matplotlib` (calidad de publicación científica, paridad con figuras de la tesis).
* **Calidad de código:** `ruff`, `mypy --strict`, `pytest`, `pytest-cov`, `pytest-benchmark`, `hypothesis`.
* **Entorno:** GitHub + `uv` para gestión de dependencias.
* **Documentación:** Sphinx + MyST. Docstrings estilo NumPy con citas a la tesis. Notebooks ejecutables con Jupyter.

---

## 🔍 Objetivos de Investigación

1. **Parameter Problem:** Métodos modernos para encontrar pre-vértices (Driscoll–Trefethen 1996, métodos homotópicos, posibles inicializaciones con redes neuronales). Bibliografía base: referencia [8] de la tesis.
2. **Proyección quincuncial de Peirce:** Extensión natural mencionada explícitamente en las Recomendaciones de la tesis (p. 59).
3. **Aplicaciones cartográficas modernas:** Mercator generalizado para cuerpos celestes (continuación directa de §4.2), aplicaciones en visualización de datos planetarios.
4. **Aplicaciones en ingeniería:** Microelectrónica (MEMS), aerodinámica (perfiles Joukowski), procesamiento de imágenes.

---

## 📏 Definition of Done (Por Fase)

| Fase | Métrica de cierre                                                                              |
|------|------------------------------------------------------------------------------------------------|
| 0    | `pytest` y CI en verde; `pip install -e .` funcional                                            |
| 1    | Los 7 casos del Teorema 6 implementados como tests; Figuras 1.1–1.3 reproducidas                |
| 2    | Cauchy-Riemann (Tipo A y B) verificable automáticamente; Teoremas 7 y 8 como tests              |
| 3    | Figura 3.6 reproducida con error < 10⁻¹²; corolario con infinito en ambos casos                 |
| 4    | Figuras 3.10–3.14 reproducidas a calidad de publicación                                         |
| 5a   | Triángulo equilátero, rectángulo y cuadrado (ejemplo abierto de p. 53) con error < 10⁻⁸          |
| 5b   | Cuadrado, hexágono y polígono no convexo mapeados automáticamente                               |
| 6    | Figuras 4.2, 4.3, 4.4 y 4.5 reproducidas; notebook `07_lunar_mercator.ipynb` como flagship      |
| 7    | Release `v1.0.0` en PyPI con DOI en Zenodo; documentación bilingüe en GitHub Pages              |
| 8    | Proyección quincuncial de Peirce implementada; artículo corto enviado a JOSS o SoftwareX        |
| 9    | Speedup ≥ 5× en kernels SC vs implementación pura NumPy                                         |

---

## 📂 Archivos de Referencia (Legacy)

Organizados por capítulo de la tesis al que corresponden:

**Capítulo 1 — Aplicaciones lineales:**
* `algebra.mw` — Estructura algebraica del grupo P
* `locc.mw` — Notas algebraicas auxiliares

**Capítulo 2 — Aplicaciones complejas:**
* (Sin archivos `.mw` directamente asociados; teoría base)

**Capítulo 3 — Aplicaciones conformes:**
* `funcion_z_2.mw` — §3.1, Teorema 10, Figuras 3.4–3.5 (mapeo z² y magnificación)
* `bili.mw`, `bili2.mw`, `bilineal.mw` — §3.2, transformaciones de Möbius
* `disco.mw` — §3.2, Figura 3.6 (disco → semiplano)
* `funcion_implicita.mw` — §3.2, Teorema 11 (fórmula implícita)
* `corolario.mw` — §3.2, Corolario 2 (punto al infinito)
* `exponencial.mw` — §3.3, función exponencial
* `logaritmo.mw` — §3.3, logaritmo y composiciones
* `composicion.mw` — §3.3, Figuras 3.10–3.11 (composiciones)
* `trigonometricas.mw` — §3.3, funciones trigonométricas
* `w_tan_z_.mw` — §3.3, Figura 3.12 (w = tan z)
* `algo.mw`, `proceso.mw` — §3.4 y Capítulo 4, Schwarz-Christoffel y diagrama de flujo

**Capítulo 4 — Implementación:**
* `mapeo_luna.mw` — §4.2, Figuras 4.4–4.5 (Mercator lunar) **[flagship]**

**Ejemplos varios y soporte:**
* `Example_11_26.mw`, `ejemplo10.mw` — Ejemplos auxiliares numerados
* `AplicacioÌ-n_conforme_.mw` — Aplicación conforme genérica

**PDF base:**
* `IMPLEMENTACION_EN_SOFTWARE_DE_APLICACIONES_CONFORMES.pdf` — Tesis original (Vega Penagos & Olivero Zapata, 2015)

---

## 📚 Bibliografía Clave (de la tesis)

Las referencias [7] y [8] de la tesis son centrales para el proyecto:

* **[7]** Mathews, J. H. & Howell, R. W. (2006). *Complex Analysis for Mathematics and Engineering* (5th ed.). Jones and Bartlett. — Base teórica principal del Capítulo 3.
* **[8]** Driscoll, T. A. & Trefethen, L. N. (2002). *Schwarz-Christoffel Mapping*. Cambridge University Press. — Referencia obligatoria para Fase 5b (parameter problem).
* **[9]** Solanilla, L. (2008). *Geometría diferencial de superficies*. Sello Editorial Universidad de Medellín. — Base del enfoque de superficies de Riemann (§1.4 y §2.2–2.5).

---

*Última revisión del roadmap: v3, basada en lectura íntegra de la tesis. Las versiones anteriores no incorporaban el Capítulo 1 (grupo P) ni la distinción holomorfo/antiholomorfo del Capítulo 2, y subestimaban la centralidad de la aplicación cartográfica lunar del Capítulo 4.*
