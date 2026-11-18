"""Homogeneous electrostatic model for two equal coplanar electrodes."""

from math import isfinite, sqrt

from scipy.constants import epsilon_0
from scipy.special import ellipkm1

from ._coplanar import coplanar_geometry, root_product

__all__ = ["coplanar_sensor_capacitance", "coplanar_sensor_field"]


def coplanar_sensor_capacitance(width: float, gap: float, eps_r: float = 1.0) -> float:
    """Return mutual capacitance per unit length in F/m for two equal strips.

    Width and the full inner gap use the same length unit. The strips
    have zero thickness and are longitudinally invariant, with the same
    uniform dielectric above and below.

    References
    ----------
    Gevorgian & Berg (2001), *Line capacitance and impedance of
    coplanar-strip waveguides on substrates with multiple dielectric layers*,
    homogeneous limit.
    """
    if not isfinite(eps_r) or eps_r < 1:
        raise ValueError("Relative permittivity must be finite and at least one.")
    _, parameter, complement = coplanar_geometry(gap, width)
    aspect = float(ellipkm1(parameter) / ellipkm1(complement))
    return float(epsilon_0) * eps_r * aspect


def coplanar_sensor_field(point: complex, width: float, gap: float) -> complex:
    """Return Ex + i Ey in V/m with the left electrode at 0 V and right at 1 V.

    Supply point coordinates, width and full gap in meters. The point
    must lie above the conductor plane, with zero at the gap center.
    """
    if not (isfinite(point.real) and isfinite(point.imag) and point.imag > 0):
        raise ValueError("The field point must be finite and above the conductors.")
    half_span, parameter, complement = coplanar_geometry(gap, width)
    z = point / half_span
    roots = root_product(z, sqrt(parameter))
    derivative = -1 / (2 * float(ellipkm1(complement)) * roots) / half_span
    return -derivative.conjugate()
