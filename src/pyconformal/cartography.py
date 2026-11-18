"""Spherical conformal map projections."""

from cmath import rect
from math import floor, isfinite, radians, remainder, sqrt, tan

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.special import ellipj, elliprf

from pyconformal.mobius import disk_to_upper_half_plane
from pyconformal.sc import upper_half_plane_to_square

__all__ = [
    "north_hemisphere_to_square",
    "peirce_quincuncial",
    "peirce_quincuncial_inverse",
    "stereographic_north_disk",
]

_LEMNISCATE_CONSTANT = float(elliprf(0, 1, 2))


def _longitude_angle(longitude: float, central_meridian: float) -> float:
    if not (isfinite(longitude) and isfinite(central_meridian)):
        raise ValueError("Longitude and central meridian must be finite.")
    return remainder(remainder(longitude, 360) - remainder(central_meridian, 360) + 45, 360)


def _stereographic(angle: float, latitude: float) -> complex:
    radius = 1.0 if latitude == 0 else tan(radians((90 - latitude) / 2))
    if abs(angle) == 180:
        return complex(-radius)
    return rect(radius, radians(angle))


def stereographic_north_disk(
    longitude: float, latitude: float, *, central_meridian: float = 0
) -> complex:
    """Project the closed northern hemisphere to a unit disk, using degrees.

    Longitudes increase eastward. The disk is oriented so its four
    cardinal points become the corners of the Peirce hemisphere square.
    """
    if not 0 <= latitude <= 90:
        raise ValueError("Northern latitude must be between 0 and 90 degrees.")
    angle = _longitude_angle(longitude, central_meridian)
    return _stereographic(angle, latitude)


def north_hemisphere_to_square(
    longitude: float, latitude: float, *, central_meridian: float = 0
) -> complex:
    """Project a northern hemisphere to the normalized Peirce square.

    Coordinates are east-positive longitude and spherical latitude, in
    degrees. The north pole maps to zero and the equator to the boundary
    of ``[-1, 1] x [-1, 1]``. The corners are at longitudes 45, 135,
    225 and 315 degrees east of the chosen central meridian.

    References
    ----------
    Peirce (1879), *A quincuncial projection of the sphere*.
    Vega Penagos & Olivero Zapata (2015), pp. 8 and 59.
    """
    if not 0 <= latitude <= 90:
        raise ValueError("Northern latitude must be between 0 and 90 degrees.")
    return _north_square(_longitude_angle(longitude, central_meridian), latitude)


def _north_square(angle: float, latitude: float) -> complex:
    if latitude == 90:
        return 0j
    if latitude == 0:
        # The Cayley value on the unit circle is real, with a pole at −1.
        if abs(angle) == 180:
            half_plane = complex(float("inf"), 0)
        elif abs(angle) == 90:
            half_plane = complex(angle / 90)
        else:
            half_plane = complex(tan(radians(angle / 2)))
    else:
        half_plane = disk_to_upper_half_plane(_stereographic(angle, latitude))
        # Values within rounding distance of the equator can acquire a
        # small negative imaginary part when the disk point is rounded.
        if half_plane.imag < 0:
            half_plane = complex(half_plane.real)
    return upper_half_plane_to_square(half_plane)


def peirce_quincuncial(
    longitude: float, latitude: float, *, central_meridian: float = 0
) -> complex:
    """Project the sphere to Peirce's normalized global square.

    Longitudes are east-positive and latitudes are spherical, in degrees.
    The outer square is ``[-1, 1] x [-1, 1]`` and its central diamond
    contains the northern hemisphere. Four southern triangles fill the
    corners. Each southern cut meridian has two edge copies. An input on
    a cut uses the sector immediately to its east. Longitude selects
    which of the four equivalent corners represents the south pole.

    References
    ----------
    Peirce (1879), *A quincuncial projection of the sphere*.
    PROJ, https://proj.org/en/stable/operations/projections/peirce_q.html.
    """
    if not -90 <= latitude <= 90:
        raise ValueError("Spherical latitude must be between -90 and 90 degrees.")
    angle = _longitude_angle(longitude, central_meridian)
    square = _north_square(angle, abs(latitude))
    if latitude < 0:
        # Reflect the corresponding northern sector across its equatorial side.
        sector = floor(angle / 90) % 4
        match sector:
            case 0:
                square = complex(square.real, -2 - square.imag)
            case 1:
                square = complex(2 - square.real, square.imag)
            case 2:
                square = complex(square.real, 2 - square.imag)
            case 3:
                square = complex(-2 - square.real, square.imag)
    point = square * (0.5 + 0.5j)
    # At cuts a round-off error can put a coordinate just outside the tile.
    return complex(max(-1, min(1, point.real)), max(-1, min(1, point.imag)))


def peirce_quincuncial_inverse(
    points: ArrayLike, *, central_meridian: float = 0
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Return east-positive longitude and spherical latitude in degrees.

    Supply complex coordinates in the normalized global square. Arrays
    produce equally shaped arrays, and a scalar produces zero-dimensional
    arrays. The longitude interval is [-180, 180). The central meridian
    is returned at either pole, where longitude is undefined. Both
    copies of a cut invert to the same geographic coordinates.

    References
    ----------
    NIST DLMF §§22.6, 22.8 and 22.17 for Jacobi transformation formulas.
    """
    if not isfinite(central_meridian):
        raise ValueError("Central meridian must be finite.")
    tile = np.asarray(points, dtype=np.complex128)
    if np.any(~np.isfinite(tile) | (np.abs(tile.real) > 1) | (np.abs(tile.imag) > 1)):
        raise ValueError("Expected finite points in the normalized Peirce square.")
    north_square = tile * (1 - 1j)
    x, y = north_square.real, north_square.imag
    south = (np.abs(x) > 1) | (np.abs(y) > 1)
    x = np.where(np.abs(x) > 1, 2 * np.sign(x) - x, x)
    y = np.where(np.abs(y) > 1, 2 * np.sign(y) - y, y)
    disk = _lemniscate_sine((x + 1j * y) * (0.5 + 0.5j) * (1j * _LEMNISCATE_CONSTANT))

    radius = np.minimum(np.abs(disk), 1)
    latitude = 90 - np.rad2deg(2 * np.arctan(radius))
    latitude = np.where(south, -latitude, latitude)
    meridian = remainder(central_meridian, 360)
    longitude = np.where(radius == 0, meridian, np.rad2deg(np.angle(disk)) - 45 + meridian)
    return np.asarray((longitude + 180) % 360 - 180), np.asarray(latitude)


def _lemniscate_sine(argument: NDArray[np.complex128]) -> NDArray[np.complex128]:
    # Rotate by a quarter turn when needed to keep cn(Im u) away from zero.
    # sl(i u) = i sl(u), and sl(u) = sd(sqrt(2) u | 1/2) / sqrt(2).
    rotate = np.abs(argument.real) < np.abs(argument.imag)
    u = np.where(rotate, -1j * argument, argument) * sqrt(2)
    sr, cr, dr, _ = ellipj(u.real, 0.5)
    si, ci, di, _ = ellipj(u.imag, 0.5)
    # Apply the addition and imaginary-argument formulas to sn(u)/dn(u).
    numerator = sr * di + 1j * si * ci * cr * dr
    denominator = ci * dr * di - 0.5j * sr * cr * si
    disk = numerator / denominator / sqrt(2)
    return np.asarray(np.where(rotate, 1j * disk, disk), dtype=np.complex128)
