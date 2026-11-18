# Design a 50 Ω coplanar waveguide

Open [the interactive example](../examples/coplanar-waveguide.html) in a
browser. Enter the trace width and relative permittivity, then select
**Find 50 Ω gap** to calculate the gap on each side. A 1 mm trace in a
uniform dielectric with relative permittivity 4 needs a gap of
0.258344 mm per side in this model. The capacitance per unit length
is 133.43 pF/m.

## Model

The geometry has a thin center strip between two semi-infinite grounds,
equal gaps, and the same lossless dielectric on both sides. It uses the
quasi-static limit with zero conductor thickness and no backside metal.
The relative permittivity is that of the uniform medium. A PCB with
air above and substrate below has different boundary conditions.
[scikit-rf CPW model and references](https://scikit-rf.readthedocs.io/en/latest/_modules/skrf/media/cpw.html)

For width `w` and gap `s`, the four real prevertices are `±w/2` and
`±(w/2+s)`. The Schwarz–Christoffel map sends a quadrant of the upper
half-plane cross-section to a rectangle. Its aspect is set by two
complete elliptic integrals. With `k = w/(w+2s)` and
`k′ = √(1−k²)`, the model uses
`Z₀ = η₀ K(k′)/(4 √εᵣ K(k))`,
`v = c/√εᵣ`, and `C′ = 1/(Z₀v)`.
Here `K` is written with a modulus. SciPy's parameter convention uses
its square. [Ghione & Naldi, 1984](https://doi.org/10.1049/el:19840120)

The browser traces the direction of the electric field using the four
square-root factors of the Schwarz–Christoffel derivative. Lines are
seeded on the signal strip and reflected across the conductor plane
by symmetry. The curve density has no quantitative meaning.

## Verification

Six air-filled cross-sections with gap-to-width ratios from 0.03 to 2
were compared with `CPW.analyse_quasi_static` in scikit-rf 2.2.0 using
`ep_r=1`, no backside metal and no thickness correction. The maximum
relative impedance difference was `1.96e-6`. The regression tests store
those reference values, so scikit-rf is only needed to regenerate the
comparison. Tests also check dielectric scaling and the unit voltage
drop obtained by integrating the field along a gap.

```python
from pyconformal.sc import coplanar_waveguide, gap_for_impedance

gap_mm = gap_for_impedance(width=1, impedance_ohm=50, eps_r=4)
print(gap_mm)
print(coplanar_waveguide(width=1, gap=gap_mm, eps_r=4))
```
