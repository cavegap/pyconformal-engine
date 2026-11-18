# Reader exercises

These exercises accompany the [thesis reading guide](thesis-guide.md).
Use the HTML demonstrations for exploration and Python for numerical
checks. Each submission should state the map and domain, predict the
result, show a calculation, and explain what the figure demonstrates.
Screenshots alone are not evidence of conformality.

The numerical checkpoints run with `python examples/reader_checks.py`
after installing the local package. They check selected consequences;
they do not assess a reader's proof or explanation. Suggested answers
are in [a separate file](exercise-solutions.md).

## E1. Vector angles and orientation

**Thesis:** §1.1–1.2, Figs. 1.1–1.3 and Definition 1, pp. 10–12.
**Tool:** [Group P](../examples/group-p.html). **Level:** foundation.

Take x = (1,0), y = (1,1). Compute their unsigned and oriented angles.
Apply a rotation by π/3, a reflection with matrix parameter π/3, and a
dilation by −2. Predict the angle, orientation and length ratio in each
case. Explain why the reflection axis is at π/6, not π/3.

Use the figure presets, then move the vectors to an oblique configuration.
For the written calculation, use the stated vectors even if a browser
drag limit prevents those exact coordinates. Explain why λ = 0 must be
excluded, and why λ < 0 does not reverse plane orientation.

**Deliver:** dot-product calculation, signed determinant for each map,
and a short comparison with the visual construction.

## E2. Curves, tangents and a critical point

**Thesis:** §3.1, Theorems 9–10 and Figs. 3.1–3.3, pp. 29–32.
**Tool:** [Curves and tangents](../examples/conformal-angle.html).
**Level:** foundation / intermediate.

For f(z) = z² at z₀ = (1+i)/2, take T₁ = 1 and T₂ = exp(iπ/3).
Calculate f′(z₀), the local length factor, the common tangent rotation,
and the image tangent opening. Verify these with the controls.

Move z₀ to zero. Explain why f′(0)Tⱼ gives zero vectors and cannot define
a tangent angle from that parameterization. For the outgoing rays
`z = tTⱼ`, t > 0, compute their limiting image directions and opening.
Repeat at zero for exp z and explain why that case remains ordinary.

**Deliver:** one chain-rule calculation and one explanation of the
difference between parameter derivatives and limiting directions.

## E3. The Cayley map and its pole

**Thesis:** §3.2, Fig. 3.6, p. 37.
**Tool:** [Disk to half-plane](../examples/disk-to-halfplane.html).
**Level:** foundation.

For `w = i(1-z)/(1+z)`, evaluate the images of 0, i, −i and 1. Derive
`Im w = (1-|z|²)/|1+z|²`. What happens as z approaches −1 from the disk?
Find the inverse map and state its domain. Distinguish the finite real
boundary from the pole.

**Deliver:** four reference values, the identity, and an inverse check
at z = 0.2 + 0.3i.

## E4. Recovering an object with a logarithm

**Thesis connection:** §3.3 and §4.2; this inverse-designed house is new.
**Tool:** [Object reveal](../examples/object-reveal.html).
**Level:** intermediate.

Explain why `Log(exp w) = w` on the house's strip, whose imaginary part
lies between −0.8 and 1. Calculate the exponential image of the roof
vertex w = i and its principal logarithm. Repeat with w = 4i to show
why the identity fails without a branch restriction.

Evaluate the local scale of Log at z = exp(0.65 + 0.35i). Explain why
recovering the constructed house does not establish recovery of an
unknown physical object from an arbitrary image.

**Deliver:** the domain restriction, two inverse calculations and a
scale estimate.

## E5. Normalizing the SC square

**Thesis:** §3.4, Fig. 3.17, p. 53.
**Tool:** [SC square](../examples/schwarz-christoffel-square.html).
**Level:** intermediate.

Write the implemented Carlson RF formula, including κ and the branch
domain. Evaluate the images of −1, 0, 1, ∞ and i. Sketch the order of
the square corners and identify the real-axis intervals mapping to each
side. Explain why choosing other affine constants changes the picture
without changing local conformality.

**Deliver:** the corner correspondence and one interior check at i.
The point at infinity is a boundary limit, not a finite plotting coordinate.

## E6. A second SC boundary problem

**Thesis connection:** the map in §3.4; the thermal problem is new.
**Tool:** [SC heat problem](../examples/schwarz-christoffel-heat.html).
**Level:** intermediate / advanced.

For a normalized square plate with `T(u,v) = 60 + 40uv °C`, write the
temperature on every edge. Verify Laplace's equation and determine
the four corner values and center temperature. Explain why the center
is a saddle rather than a maximum or minimum.

Pull the solution back using the SC map. Determine T at the prevertices
and at z = i. Explain which assumptions allow this to represent steady
heat conduction and what information is missing for a heat flux in W/m².

**Deliver:** boundary data, a Laplacian calculation and a discussion of
units. Compare with the earlier 0 V / 1 V mixed-boundary example.

## E7. Electronics and model assumptions

**Thesis connection:** a new application of §3.4.
**Tools:** [CPW](../examples/coplanar-waveguide.html),
[sensor](../examples/coplanar-sensor.html). **Level:** applied.

Find the gap for a 1 mm CPW trace at 50 Ω in a uniform medium with
εᵣ = 4. Predict the impedance change if εᵣ doubles with geometry fixed.
For two sensor strips of width 1 mm, gap 0.25 mm, length 20 mm and
εᵣ = 3, calculate the capacitance. Compare with a doubled gap and with
a doubled permittivity.

**Deliver:** values with units and three missing physical effects that
would matter for a particular PCB or material-sensing experiment.
Do not treat a partially inserted dielectric sample as a uniform medium.

## E8. What does local scale measure?

**Thesis:** §4.2, Fig. 4.5, p. 57.
**Tools:** [Lunar crop](../examples/lunar_mercator.png),
[tracing](../examples/lunar-thesis-interactive.html). **Level:** intermediate.

For f(z) = z³, calculate the local length and area factors at z = 1+i.
Explain what happens at the origin. Identify the cyan rectangle boundary
and crater markers in the crop figure. Explain why the colorbar is not
a lunar elevation scale or a kilometers-per-pixel scale.

Compare that scale with the pole-relative scale in the Peirce atlas.
State the reference metric for each. Explain why the orthographic sphere
is useful context even though it is not itself conformal.

**Deliver:** length and area factors plus a caption that distinguishes
source-coordinate stretching from geographic stretching.

## E9. Poles, cuts and tile joins

**Thesis connection:** Recommendations, p. 59.
**Tool:** [Unified Peirce atlas](../examples/peirce-atlas.html).
**Level:** intermediate / advanced.

Choose Tycho, then switch among all four views without changing its
longitude or latitude. Identify the northern diamond, southern triangles,
four exceptional equatorial points and repeated south-pole corners.
At local length scale 2×, what is the relative area factor?

Explain why a neighboring tile needs a half-turn. Compare geographic
inverse coordinates at `1 + 0.4i` and `1 − 0.4i`. What additional surface
coverage do nine joined tiles provide? Is longitude a unique coordinate
at a pole?

**Deliver:** matching inverse coordinates, an area factor, and a diagram
or explanation of one tile join.

## E10. Audit the historical figure

**Thesis:** §4.2, Fig. 4.5, p. 57.
**Tools:** [Recovery notes](lunar-thesis-outlines.md),
[tracing explorer](../examples/lunar-thesis-interactive.html).
**Level:** research practice.

Compare the written formula z³ with the plotted contour's agreement
with z². Identify the coordinate-based evidence and its limitations.
Explain the difference between vector recovery, geographic registration,
and physical ground control. Why does an image correlation of 0.816
not provide a positional error in kilometers?

Switch to Log(1+z). State why its branch is valid on the source rectangle.
Propose an independent validation before using any traced boundary for
a geographic measurement.

**Deliver:** a short audit with links to the relevant data and calculation,
clearly separating historical evidence from the new demonstration.
