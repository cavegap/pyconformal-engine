"""Shared four-prevertex geometry for coplanar cross-sections."""

import cmath
from math import isfinite


def coplanar_geometry(inner_span: float, outer_band: float) -> tuple[float, float, float]:
    """Return the outer half-span and the elliptic parameter and complement."""
    if not (isfinite(inner_span) and isfinite(outer_band) and inner_span > 0 and outer_band > 0):
        raise ValueError("Width and gap must be positive and finite.")
    half_span = inner_span / 2 + outer_band
    modulus = (inner_span / 2) / half_span
    parameter = modulus**2
    complement = (outer_band / half_span) * (1 + modulus)
    if not (parameter > 0 and complement > 0):
        raise ValueError("Width-to-gap ratio is outside floating-point range.")
    return half_span, parameter, complement


def root_product(z: complex, k: float) -> complex:
    """Return the product of the four principal roots in the upper half-plane."""
    return cmath.sqrt(z + 1) * cmath.sqrt(z + k) * cmath.sqrt(z - k) * cmath.sqrt(z - 1)
