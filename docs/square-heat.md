# A second Schwarz–Christoffel problem: steady heat

Open the [thermal example](../examples/schwarz-christoffel-heat.html).
It uses the normalized [SC square](schwarz-christoffel-square.md) from
thesis §3.4, Figure 3.17, p. 53, to solve a new boundary problem.
The thermal data are an educational extension of the thesis.

## Boundary data and solution

Let `w = u+iv` lie in `[-1,1]²`. Prescribe the following temperatures:

| Edge | Temperature in °C |
| --- | --- |
| v = 1 | 60 + 40u |
| v = −1 | 60 − 40u |
| u = 1 | 60 + 40v |
| u = −1 | 60 − 40v |

The corner values agree between adjacent edges. The exact solution is
`T(u,v) = 60 + 40uv`. Since both pure second derivatives vanish, T is
harmonic. The maximum principle and uniqueness of the Dirichlet problem
identify it as the solution. Its stationary center is a saddle at 60 °C.
Constant-temperature contours are hyperbolas `uv = constant`; the 60 °C
level consists of the two coordinate axes.

For the same normalized Carlson map f used by the square demo,
`T(z) = 60 + 40 Re(f(z)) Im(f(z))`. In the open half-plane,
`Δz(T ∘ f) = |f′(z)|² (Δw T) ∘ f = 0`.
This is why conformal mapping transports the boundary problem.
The earlier electrostatic example has different boundary data: constant
top/bottom values and insulating vertical sides.

## Assumptions and units

Steady, two-dimensional conduction with constant isotropic conductivity
and no internal generation satisfies Laplace's equation. The coordinates
are dimensionless. If `X = L₀u`, `Y = L₀v`, then
`q = −(k/L₀)(40v,40u)` for physical conductivity k. Neither k nor L₀
is inferred by the demo. It displays temperatures and heat-flow directions,
not a calibrated heat flux or a fabricated device simulation.

## Verification and reproduction

```python
from pyconformal.sc import square_heat_temperature

print(square_heat_temperature(1j))  # 60 °C
print(square_heat_temperature(0j))  # 100 °C
print(square_heat_temperature(1j, cold=0, hot=1))  # 0.5
```

Run `python -m pytest tests/test_square_heat.py` and
`python examples/reader_checks.py --exercise E6`. Tests cover corner
and center values, temperature-unit changes, invalid inputs and the
harmonic mean-value property on independently sampled circles inside
the half-plane. The browser shares `sc-square.js` with the geometric
SC demo; the [browser-math verifier](../scripts/verify_browser_math.py)
compares its map with the Python implementation.

The browser raster is inverse-free sampling of T at half-plane pixels
and direct sampling in the square. Source isotherms are approximated by
linear interpolation on a triangulated sampling grid. Contour and arrow
density are visual choices, not error estimates or flux magnitudes.
See [Exercise E6](exercises.md#e6-a-second-sc-boundary-problem).
