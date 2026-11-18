# Worked checkpoints

Try the [exercises](exercises.md) before reading these notes. These are
reference calculations and reasoning prompts, not full substitutes for
the proofs in the thesis. Reproduce the numerical values with
`python examples/reader_checks.py`; select one with `--exercise E6`.

## E1

For x = (1,0), y = (1,1), the normalized dot product is 1/√2,
so the unsigned angle is 45°. The oriented opening from x to y is +45°.
A rotation by π/3 retains +45°. The reflection matrix with θ = π/3
has geometric axis θ/2 = π/6; its oriented opening becomes −45°.
Dilation by −2 retains +45° and doubles both lengths. Its determinant
is 4, while the rotation and reflection determinants are 1 and −1.
The zero dilation destroys bijectivity and gives undefined vector angles.

```python
from math import pi
import numpy as np
from pyconformal.linear import Reflection

transform = Reflection(pi / 3)
vector = np.array([1.0, 0.0])
print(transform.matrix @ vector)  # [0.5, sqrt(3)/2]
print(transform(1 + 0j))         # same vector, represented as a complex point
```

The array call interface represents an array of complex points; use the
matrix for a two-component real vector. Do not pass `[x,y]` to the point
interface expecting it to mean `x + iy`.

## E2

At z₀ = (1+i)/2, f′(z₀) = 1+i. Its modulus is √2 and its argument
is 45°. Both tangent vectors rotate by 45°; their opening stays 60°.
At zero, the parameter derivatives of the mapped curves vanish.
For outgoing rays t > 0, `f(t exp(iβ)) = t² exp(2iβ)`:
the limiting directions have opening 120°. For exp z, f′(0) = 1,
so zero is ordinary. Angles between unoriented tangent lines and between
oriented outgoing rays require different conventions; state which is used.

## E3

The four images are 0 → i, i → 1, −i → −1 and 1 → 0.
Multiplying numerator and denominator by `1 + conjugate(z)` gives
`Im w = (1-|z|²)/|1+z|²`. It is positive in the disk. The inverse is
`z = (i-w)/(i+w)`, defined in the upper half-plane, with the relevant
boundary limit at infinity. The denominator of the forward map vanishes
at z = −1; no finite image should be plotted there.

## E4

The principal logarithm chooses imaginary part in (−π,π]. The house's
imaginary range [−0.8,1] lies inside that strip, and its exponential
image lies in the right half-plane. Thus Log(exp w) recovers each house
point. The roof maps to `cos 1 + i sin 1`, approximately
`0.540302 + 0.841471i`, and its logarithm is i.
For w = 4i, the principal result is `(4−2π)i`, approximately −2.283185i.
At z = exp(0.65+0.35i), the length factor of Log is
`1/|z| = exp(−0.65) ≈ 0.522046`.

## E5

Use `f(z) = 1+i − (2i/κ)RF(z+1,z,z−1)`, with
`κ = RF(0,1,2) ≈ 1.311028777`. The analytic branch is in Im z > 0;
real-axis limits are evaluated separately. The prevertices map in order
to −1+i, −1−i, 1−i and 1+i; i maps to zero. The real intervals
`(−∞,−1)`, `(−1,0)`, `(0,1)`, `(1,∞)` map to top, left, bottom
and right, respectively. Nonzero affine output scaling changes rotation
and length units while preserving local angles.

## E6

Top: `60+40u`; bottom: `60−40u`; right: `60+40v`;
left: `60−40v`, all in °C. Both pure second derivatives are zero,
so ΔT = 0. Corners (−1,−1) and (1,1) are at 100 °C; the other
two are at 20 °C. The center is 60 °C. The Hessian has eigenvalues
±40, so the stationary center is a saddle.

The corresponding prevertex temperatures are −1 → 20, 0 → 100,
1 → 20, ∞ → 100 and i → 60. This differs from the earlier
electrostatic problem: all four thermal edges carry varying Dirichlet
data, whereas the voltage problem uses constant top/bottom potentials
and insulating sides.

For a physical coordinate X = L₀u, Y = L₀v, the gradient acquires
`1/L₀`. Heat flux needs conductivity k in addition to L₀.
Constant isotropic conductivity, steady state and no internal source
reduce the governing equation to Laplace's equation. A physical
half-plane interpretation requires its own physical coordinate scale.

## E7

The 50 Ω gap is about 0.258344 mm per side. At fixed geometry,
`Z₀ ∝ 1/√εᵣ`, so doubling εᵣ changes 50 Ω to about 35.3553 Ω.
The sensor capacitance is about 1.210915 pF; doubling the gap gives
about 1.010 pF. Doubling the uniform permittivity doubles capacitance.
Examples of missing effects are substrate interfaces, finite conductor
thickness, finite grounds, end effects, dispersion and conductor losses.
Choose the relevant ones for the proposed experiment.

## E8

At 1+i, `|f′| = |3z²| = 6`; the local area factor is 36.
At zero, f′ vanishes. The cyan boundary denotes the sampled rectangle;
the circles identify crater centers rather than fitted crater rims.
The colorbar measures output lengths per normalized Mercator source
unit. It excludes Mercator's own ground-to-plane scale.
The Peirce atlas instead normalizes spherical length scale by its value
at a pole. A 2× length factor there means a 4× local area factor relative
to a pole. Neither scale is an elevation map.

## E9

North lies at zero. Longitude conventions select one of the four corner
copies of the same south pole. The four exceptional equatorial points
are the midpoints of the tile edges; the equator is the central diamond.
The two points `1 ± 0.4i` invert to the same longitude, 45° E, and
the same southern latitude. Use the numerical inverse for that latitude.
Alternating half-turns match these paired edge coordinates across joins.
Nine tiles repeat the same coverage. Pole longitude is undefined.

## E10

The archived nearest-vertex comparison gives median distances of about
0.00597 for z² and 11.47464 for z³, in the published image's coordinate
units. Different path sampling and clipping limit this comparison, but
the large difference supports the squared-map reading of the plotted
panel. The written formula remains z³ and is documented separately.

Vector recovery extracts a printed planar construction. Registration
estimates a geographic frame for that construction. Ground control
would independently compare known physical coordinates and estimate
positional errors. Correlation is dimensionless and supplies no direct
kilometer uncertainty. Independent landmark residuals and a defensible
geographic model are needed before measurement.

For Log(1+z) on `0 ≤ Re z ≤ 12`, `0 ≤ Im z ≤ 6`, the argument
1+z stays in the right half-plane. The principal branch is analytic
there and f′ = 1/(1+z) never vanishes.
