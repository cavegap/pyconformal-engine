# Mathematical notation and conventions

This page fixes the conventions used by the interactive examples.
Equations are rendered as native MathML at publication time. Function
names in Python listings remain code; they are not mathematical notation.

Long equations scroll horizontally on narrow screens. The source TeX
is retained as a MathML annotation for inspection and reuse.

## Complex coordinates and conformality

We write $z=x+iy$ in a source plane and $w=u+iv=f(z)$ in its image.
The open upper half-plane is

$$
\mathbb H=\{z\in\mathbb C:\operatorname{Im}z>0\}.
$$

For a holomorphic map at an ordinary point, the derivative rotates and
scales every tangent by the same complex factor:

$$
T_j^\ast=f'(z_0)T_j,\qquad f'(z_0)\ne0.
$$

The local length and area factors in the two planar coordinate systems are

$$
\sigma(z_0)=|f'(z_0)|,\qquad J(z_0)=|f'(z_0)|^2.
$$

Arguments are defined modulo a full turn. A zero mapped parameter
derivative cannot define a tangent direction. Limiting directions at a
critical point need a separate calculation, as in thesis Theorem 10.
Reflection preserves the unsigned angle and reverses orientation.

## Group P and the reflection parameter

For two nonzero real vectors,

$$
\theta=\arccos\left(\frac{\langle x,y\rangle}{\|x\|\,\|y\|}\right).
$$

The geometric reflection-axis angle is $\alpha$. The thesis and Python
matrix parameter is $2\alpha$:

$$
\operatorname{Ref}_{2\alpha}=
\begin{pmatrix}\cos(2\alpha)&\sin(2\alpha)\\\sin(2\alpha)&-\cos(2\alpha)\end{pmatrix}.
$$

Python angle arguments use radians; browser angle controls use degrees.
For a dilation, $\lambda\ne0$ and $\det D_\lambda=\lambda^2>0$, including
negative factors.

## The fixed Schwarz–Christoffel square

We denote the normalized square map by $S$ and reserve $\kappa$ for its
lemniscatic normalization constant:

$$
S(z)=1+i-\frac{2i}{\kappa}R_F(z+1,z,z-1),\qquad \kappa=R_F(0,1,2).
$$

The branch is analytic in $\mathbb H$. Values on the real axis are
boundary limits. The prevertices $-1,0,1,\infty$ correspond to the
corners $-1+i,-1-i,1-i,1+i$, and $S(i)=0$.
Coordinates in the target square are dimensionless. This fixed map does
not solve the accessory-parameter problem for arbitrary polygons.
[NIST DLMF §19.32](https://dlmf.nist.gov/19.32)

## Elliptic integrals and electronics

The complete elliptic integral uses the **modulus** convention:

$$
K(k)=\int_0^{\pi/2}\frac{d\theta}{\sqrt{1-k^2\sin^2\theta}},\qquad k'=\sqrt{1-k^2}.
$$

SciPy's `ellipk` instead accepts the parameter $m=k^2$. This $K$ is not
the constant $\kappa$ in the SC square. In the formulas below, $w_{\rm t}$
is a physical strip width, not the complex image coordinate $w$.

For a CPW with gap $s$ on each side,

$$
k=\frac{w_{\rm t}}{w_{\rm t}+2s},\qquad
Z_0=\frac{\eta_0}{4\sqrt{\varepsilon_r}}\frac{K(k')}{K(k)}.
$$

For two equal sensor strips with full gap $g$,

$$
k=\frac{g}{g+2w_{\rm t}},\qquad
C'=\varepsilon_0\varepsilon_r\frac{K(k')}{K(k)},\qquad C\approx LC'.
$$

Here $C'$ means capacitance per unit length, not differentiation with
respect to $z$. Use meters for $L$ when converting F/m to F. Width and
gap may use the same length unit because their ratios determine $k$.
The [CPW](coplanar-waveguide.md) and [sensor](coplanar-sensor.md) notes
state the different geometries and assumptions.

## Thermal pullback

For the square's physical teaching problem,

$$
T(u,v)=60+40uv\;{}^\circ\mathrm C,\qquad \widetilde T(z)=T(S(z)).
$$

The tilde identifies the pulled-back scalar field. Constant isotropic
conductivity and no internal heat generation give $\Delta T=0$.
A physical heat flux additionally requires conductivity and a length
scale. See the [thermal model](square-heat.md).

## Spherical coordinates and Peirce normalization

Latitude is $\varphi$ and east-positive longitude is $\lambda$.
Geographic controls and Python APIs accept degrees; the formulas use
radians. At central meridian zero, the northern composition is

$$
\zeta=\tan\left(\frac\pi4-\frac\varphi2\right)e^{i(\lambda+\pi/4)},
\qquad p=i\frac{1-\zeta}{1+\zeta}.
$$

The hemisphere prototype outputs $S(p)$; the northern part of the global
tile outputs $(1+i)S(p)/2$. Southern sectors require the documented
reflections before the final rotation and scaling. For disk coordinate
formed with absolute latitude, pole-relative length scale is

$$
\sigma_{\rm rel}=\frac{1+|\zeta|^2}{\sqrt{|1-\zeta^4|}}.
$$

Its value is one at either pole and diverges at the four exceptional
equatorial points. Its square is the relative local area factor. It is
different from the cubic plot's scale relative to a normalized Mercator
plane. Longitude is undefined at a pole; corner copies do not represent
distinct physical poles. The orthographic globe is a context view.
