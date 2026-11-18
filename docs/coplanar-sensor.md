# Coplanar capacitive sensor

Open the [interactive sensor](../examples/coplanar-sensor.html) in a
browser. Change the width, gap, length or relative permittivity. The
example displays the coupling capacitance per length, estimates the
capacitance for the selected strip length and shows the effect of
doubling the gap.

Two strips 1 mm wide and 20 mm long in a uniform dielectric with
relative permittivity 3 give approximately **1.211 pF** at a gap of
0.25 mm. A gap of 0.50 mm gives **1.010 pF**, a decrease of about 17%.

## Cross-section model

The two equal strips have zero thickness. The dielectric is uniform
throughout the cross-section and the strips extend along an invariant
longitudinal axis. The length estimate multiplies the 2D capacitance
per meter by physical length and omits end effects, leads and substrate
interfaces.

For a full gap `g` and strip width `w`, the prevertices are `±g/2`
and `±(g/2+w)`. Define `k = g/(g+2w)` and
`k′ = √(1−k²)`. The upper half-plane maps to a rectangle with
the physical electrodes on opposite sides. The two faces of the
strips give a combined capacitance per length of
`C′ = ε₀ εᵣ K(k′)/K(k)`. The field curves use the phase of the
four square-root factors in the Schwarz–Christoffel derivative.
[Gevorgian & Berg, 2001](https://amsacta.unibo.it/id/eprint/393/)

## Independent verification

A boundary-element calculation solves for the charge densities directly
on the strips using the 2D logarithmic Green's function. The strips carry
opposite charges. The solve uses piecewise constant density, exact
logarithmic panel integrals and edge-clustered panels. It obtains
capacitance by summing the charge on one strip at a 1 V difference.

| Panels per strip | Maximum relative difference from the conformal map |
| ---: | ---: |
| 24 | 0.393% |
| 48 | 0.0995% |
| 96 | 0.0250% |
| 192 | 0.00627% |

The comparison covers gap-to-width ratios from 0.1 to 2 in air. To
regenerate it from the repository root after installing the package,
run `python examples/verify_coplanar_sensor.py`.

```python
from pyconformal.sc import coplanar_sensor_capacitance

per_meter = coplanar_sensor_capacitance(width=1, gap=0.25, eps_r=3)
print(per_meter * 0.02)  # capacitance in farads for a 20 mm strip
```
