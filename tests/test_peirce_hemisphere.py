import math

import pytest

from pyconformal.cartography import north_hemisphere_to_square, stereographic_north_disk


@pytest.mark.parametrize(
    ("lon", "expected"), [(45, 1 - 1j), (135, 1 + 1j), (225, -1 + 1j), (315, -1 - 1j)]
)
def test_equatorial_corners(lon: float, expected: complex) -> None:
    assert north_hemisphere_to_square(lon, 0) == pytest.approx(expected, abs=1e-14)
    assert north_hemisphere_to_square(lon + 30, 0, central_meridian=30) == pytest.approx(expected)


def test_boundary_pole_and_angular_wrap() -> None:
    for lon in range(-180, 180, 5):
        point = north_hemisphere_to_square(lon, 0)
        assert max(abs(point.real), abs(point.imag)) == pytest.approx(1, abs=1e-14)
        assert abs(stereographic_north_disk(lon, 0)) == pytest.approx(1, abs=1e-14)
        assert north_hemisphere_to_square(lon, 90) == 0j
        assert north_hemisphere_to_square(lon, 30) == north_hemisphere_to_square(lon + 360, 30)


@pytest.mark.parametrize(("lon", "lat"), [(-132, 18), (-8, 31), (45, 65), (91, 82)])
def test_local_angles_and_spherical_scale(lon: float, lat: float) -> None:
    h = 1e-4
    east = north_hemisphere_to_square(lon + h, lat) - north_hemisphere_to_square(lon - h, lat)
    north = north_hemisphere_to_square(lon, lat + h) - north_hemisphere_to_square(lon, lat - h)
    assert (east * north.conjugate()).real / (abs(east) * abs(north)) == pytest.approx(0, abs=1e-7)
    assert abs(east) / abs(north) == pytest.approx(math.cos(math.radians(lat)), rel=1e-7)


@pytest.mark.parametrize(
    ("lon", "lat", "reference"),
    [
        (0, 45, -0.4455148697562977j),
        (45, 45, 0.3168871220651066 - 0.31688712206510666j),
        (90, 45, 0.4455148697562977 + 0j),
        (225, 0, -1.000000009955541 + 1.0000000052475717j),
    ],
)
def test_proj_reference(lon: float, lat: float, reference: complex) -> None:
    assert north_hemisphere_to_square(lon, lat) == pytest.approx(reference, abs=4e-8)


def test_reject_outside_hemisphere() -> None:
    with pytest.raises(ValueError, match="Northern latitude"):
        north_hemisphere_to_square(0, -1)
    with pytest.raises(ValueError, match="Longitude"):
        north_hemisphere_to_square(math.inf, 0)
