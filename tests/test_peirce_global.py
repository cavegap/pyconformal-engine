import math

import pytest

from pyconformal.cartography import north_hemisphere_to_square, peirce_quincuncial


def test_global_poles_and_equator() -> None:
    assert peirce_quincuncial(15, 90) == 0j
    poles = [peirce_quincuncial(lon, -90) for lon in (0, 90, 180, -90)]
    assert poles == [1 - 1j, 1 + 1j, -1 + 1j, -1 - 1j]
    points = [peirce_quincuncial(lon, 0) for lon in (45, 135, -135, -45)]
    assert points == [1 + 0j, 1j, -1 + 0j, -1j]


@pytest.mark.parametrize("longitude", [-160, -90, -24, 0, 63, 111, 178])
def test_hemispheres_join_along_the_equator(longitude: float) -> None:
    equator = peirce_quincuncial(longitude, 0)
    north = peirce_quincuncial(longitude, 1e-7)
    south = peirce_quincuncial(longitude, -1e-7)
    assert abs(north - equator) < 1e-8
    assert abs(south - equator) < 1e-8
    assert abs(equator.real) + abs(equator.imag) == pytest.approx(1)
    assert abs(north.real) + abs(north.imag) < 1
    assert abs(south.real) + abs(south.imag) > 1
    assert (north - equator) == pytest.approx(equator - south, abs=1e-14)


@pytest.mark.parametrize("side", [0, 1, 2, 3])
def test_two_copies_of_each_southern_cut_share_one_tile_edge(side: int) -> None:
    east_longitude = 45 + side * 90
    rotate = (-1j) ** side
    east = peirce_quincuncial(east_longitude, -30) * rotate
    west = peirce_quincuncial(east_longitude - 1e-8, -30) * rotate
    assert east.real == pytest.approx(1.0, abs=1e-14)
    assert 0 < east.imag < 1
    assert west == pytest.approx(east.conjugate(), abs=1e-9)


@pytest.mark.parametrize(
    ("lon", "lat", "reference"),
    [
        (0, -45, 0.7772425651218512 - 0.7772425651218512j),
        (46, -45, 0.9944031020899546 + 0.6831646828137641j),
        (90, -45, 0.7772425651218513 + 0.7772425651218513j),
        (-90, -45, -0.7772425651218512 - 0.7772425651218512j),
    ],
)
def test_proj_global_reference(lon: float, lat: float, reference: complex) -> None:
    assert peirce_quincuncial(lon, lat) == pytest.approx(reference, abs=4e-8)
    assert peirce_quincuncial(lon + 390, lat, central_meridian=30) == pytest.approx(reference)


def test_northern_square_normalization() -> None:
    assert peirce_quincuncial(-25, 40) == north_hemisphere_to_square(-25, 40) * (0.5 + 0.5j)


@pytest.mark.parametrize("latitude", [-91, 91, math.nan])
def test_reject_invalid_global_latitude(latitude: float) -> None:
    with pytest.raises(ValueError, match="Spherical latitude"):
        peirce_quincuncial(0, latitude)
