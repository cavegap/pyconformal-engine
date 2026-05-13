# PyConformal Engine

[![CI](https://github.com/cavegap/pyconformal-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/cavegap/pyconformal-engine/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**Conformal mapping for Python.** A numerical, open-source implementation of the
mathematical content of Vega Penagos & Olivero Zapata's undergraduate thesis
*Implementación en software de aplicaciones conformes* (Universidad del Tolima,
2015), replacing the original Maple 17 implementation with a Python library
designed for research, education, and engineering use.

> Esta es la **tesis ejecutable**: cada capítulo se traduce en un módulo, cada
> teorema en una propiedad verificable mediante tests, cada figura en un
> notebook reproducible.

---

## Estado del proyecto

🚧 **Pre-alpha (Fase 0 — Cimientos).** Ver [`ROADMAP.md`](./ROADMAP.md) para el
plan completo. Hoy esta release contiene únicamente la infraestructura del
proyecto (empaquetado, CI, linting, tests, layout modular). La implementación
matemática se irá agregando por fases.

## Atribución académica

Este proyecto extiende y traduce a Python la tesis de pregrado:

> **Vega Penagos, C. A. & Olivero Zapata, H. A.** (2015).
> *Implementación en software de aplicaciones conformes*.
> Trabajo de grado, Universidad del Tolima, Facultad de Ciencias,
> Programa de Matemáticas con énfasis en Estadística. Ibagué, Tolima, Colombia.
> Director: Mg. Juan Pablo Yáñez Puentes.

El PDF de la tesis se incluye en [`thesis/`](./thesis/) como referencia
primaria. Cualquier uso académico del software debe citar también la tesis
original. Ver [`CITATION.cff`](./CITATION.cff).

## Instalación (desarrollo)

```bash
# Con uv (recomendado)
uv venv
uv pip install -e ".[dev,notebooks]"

# Con pip
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -e ".[dev,notebooks]"
```

## Uso rápido

```python
import pyconformal

print(pyconformal.__version__)
```

A medida que las fases del roadmap se completen, los módulos
`pyconformal.linear`, `pyconformal.mobius`, `pyconformal.elementary`,
`pyconformal.sc` y `pyconformal.viz` irán expandiéndose. Los notebooks de
[`notebooks/`](./notebooks/) servirán como tutoriales progresivos siguiendo la
estructura de capítulos de la tesis.

## Comandos comunes

```bash
# Tests
pytest                          # corre toda la suite con cobertura
pytest -m "not slow"            # excluye tests lentos
pytest tests/test_smoke.py -v   # un archivo específico

# Lint y formato
ruff check .                    # lint
ruff format .                   # auto-format
ruff check --fix .              # lint con auto-fix

# Type checking
mypy

# Pre-commit (corre lint + format + mypy + tests rápidos)
pre-commit run --all-files
```

## Estructura del repositorio

```
pyconformal-engine/
├── src/pyconformal/        Código fuente del paquete
│   ├── linear/             Grupo P: rotación, reflexión, dilatación (Cap. 1)
│   ├── core/               Clases base: ConformalMap, Holomorphic, Antiholomorphic (Cap. 2)
│   ├── mobius/             Transformaciones de Möbius (§3.2)
│   ├── elementary/         Funciones exp, log, trigonométricas (§3.3)
│   ├── sc/                 Schwarz-Christoffel (§3.4)
│   ├── viz/                Visualización y mallas (Cap. 4)
│   └── examples/           Reproducción de figuras de la tesis
├── tests/                  Suite de pruebas
├── notebooks/              Tutoriales Jupyter por capítulo
├── examples/               Scripts de ejemplo
├── docs/                   Documentación (Sphinx)
├── thesis/                 PDF de la tesis original
├── pyproject.toml          Configuración del paquete y herramientas
├── CITATION.cff            Metadata de citación
└── ROADMAP.md              Plan de trabajo por fases
```

## Filosofía

- **Trazabilidad bibliográfica.** Cada función pública cita en su docstring el
  teorema, lema, ejemplo o figura específico de la tesis que implementa.
- **API en inglés, documentación interna en español.** Lo público sigue las
  convenciones de la comunidad científica internacional; las notas técnicas
  internas preservan el lenguaje original del trabajo.
- **Orientación es tan importante como ángulos.** Las aplicaciones holomorfas
  (preservan orientación) y antiholomorfas (la invierten) son ciudadanas de
  primera clase, siguiendo el Teorema 7 y la distinción Tipo A / Tipo B del
  Capítulo 1.

## Licencia

MIT — ver [`LICENSE`](./LICENSE).

## Cómo contribuir

Antes de abrir un PR, asegúrate de que:

1. Los tests pasan: `pytest`
2. El código está formateado: `ruff format .`
3. El lint pasa: `ruff check .`
4. Los tipos son correctos: `mypy`
5. Si implementas un teorema o ejemplo de la tesis, el docstring lo cita
   explícitamente (capítulo, sección, número de teorema/figura, página).
