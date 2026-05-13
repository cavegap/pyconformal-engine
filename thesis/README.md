# Thesis (reference)

This directory holds the underlying thesis PDF as a primary reference:

> Vega Penagos, C. A. & Olivero Zapata, H. A. (2015).
> **Implementación en software de aplicaciones conformes**.
> Universidad del Tolima, Ibagué, Tolima, Colombia.
> Director: Mg. Juan Pablo Yáñez Puentes.

Filename in the project (drop the PDF in here when you clone the repo):

    IMPLEMENTACION_EN_SOFTWARE_DE_APLICACIONES_CONFORMES.pdf

The PDF is tracked in git so that the library is fully self-contained: any
contributor can clone the repo and immediately read the mathematical source
referenced by the docstrings. If you redistribute this repository, ensure you
respect the authors' and Universidad del Tolima's rights regarding the thesis.

## Maple legacy

The original Maple 17 worksheets (`*.mw`) used to produce the figures of the
thesis are kept in the parent project as historical reference. The Python
implementation in `../src/pyconformal/` is designed so that each Maple file
has a Python counterpart with the same mathematical behavior; see the
correspondence table in `../ROADMAP.md`.
