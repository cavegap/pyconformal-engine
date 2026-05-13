# Notebooks

Jupyter notebooks that mirror the chapter structure of the thesis. Each
notebook is both a tutorial and a reproducibility artifact: running it from
top to bottom should regenerate the corresponding figures of the thesis.

| Notebook                                  | Thesis chapter / section | Status |
|-------------------------------------------|--------------------------|--------|
| `01_grupo_P.ipynb`                        | Capítulo 1               | TODO   |
| `02_holomorfas_antiholomorfas.ipynb`      | Capítulo 2               | TODO   |
| `03_propiedades_y_puntos_criticos.ipynb`  | §3.1                     | TODO   |
| `04_mobius.ipynb`                         | §3.2                     | TODO   |
| `05_elementales_y_trigonometricas.ipynb`  | §3.3                     | TODO   |
| `06_schwarz_christoffel.ipynb`            | §3.4                     | TODO   |
| `07_lunar_mercator.ipynb` (flagship)      | Capítulo 4               | TODO   |

## Running

```bash
uv pip install -e ".[notebooks]"
jupyter lab notebooks/
```
