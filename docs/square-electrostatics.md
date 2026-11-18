# Electrostatics with the Schwarz–Christoffel square

Open the [square demonstration](../examples/schwarz-christoffel-square.html)
in a browser and select **Electrostatics**. Move a point to read its voltage
in either plane. Green curves mark equipotentials and rust curves follow
the electric field from higher to lower voltage.

## Boundary conditions

The example models a source-free two-dimensional region with uniform
permittivity. In the square, the bottom side is held at 0 V, the top at
1 V, and the vertical sides have zero normal electric flux. If
`w = u + iv` is the [normalized square map](schwarz-christoffel-square.md),
the potential is `V = (v + 1)/2` volts. Its level sets have constant
`v`, and the field lines have constant `u`. Pulling back through the
conformal map preserves the harmonic potential and the right angle
between the two line families in the interior.
[Driscoll & Trefethen, Applications](https://doi.org/10.1017/CBO9780511546808.006)

| Half-plane boundary | Condition |
| --- | --- |
| `x < −1` | 1 V |
| `−1 < x < 0` | Insulating |
| `0 < x < 1` | 0 V |
| `x > 1` | Insulating |

The browser approximates the drawn curves by interpolating level sets
on a sampled triangular grid in the source window. The voltage readout
evaluates the map directly. At the finite prevertices, the model has
an ideal edge singularity in field magnitude. The potential remains
finite there.

## Validation

The automated checks verify electrode voltages and the zero normal
derivative at representative points on both insulating segments. A
separate five-point finite-difference solver uses analytical values only
on the boundary of an interior box. It checks convergence of the interior
potential under grid refinement, away from the ideal electrode edges.

| Intervals per axis | Maximum potential difference |
| ---: | ---: |
| 20 | 4.72e−4 V |
| 40 | 1.26e−4 V |
| 80 | 3.15e−5 V |

```bash
python -m pytest tests/test_square_electrostatics.py
```

```python
from pyconformal.sc import square_electrostatic_potential

print(square_electrostatic_potential(1j))  # 0.5 V, to floating-point precision
```
