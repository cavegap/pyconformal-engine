import numpy as np
import pytest
from examples.peirce_mosaic import LANDMARKS, local_scale, sample_global_mosaic

from pyconformal.cartography import peirce_quincuncial, peirce_quincuncial_inverse


def test_inverse_recovers_both_hemispheres_and_landmarks() -> None:
    points: list[tuple[float, float]] = [
        (lon, lat) for lon in range(-180, 180, 5) for lat in range(-85, 90, 5)
    ]
    points.extend((lon, lat) for _, lon, lat, _ in LANDMARKS)
    expected_lon, expected_lat = np.asarray(points).T
    tile = np.array([peirce_quincuncial(lon, lat) for lon, lat in points])
    longitude, latitude = peirce_quincuncial_inverse(tile)
    np.testing.assert_allclose((longitude - expected_lon + 180) % 360 - 180, 0, atol=1e-11)
    np.testing.assert_allclose(latitude, expected_lat, rtol=0, atol=1e-11)


def test_inverse_handles_duplicate_cuts_and_poles() -> None:
    longitude, latitude = peirce_quincuncial_inverse(np.array([[1 + 0.5j, 1 - 0.5j]]))
    assert longitude.shape == (1, 2)
    np.testing.assert_allclose(longitude, [[45, 45]], atol=1e-12)
    assert latitude[0, 0] == pytest.approx(latitude[0, 1], abs=1e-12)
    assert latitude[0, 0] < 0
    for point in (-1 - 1j, -1 + 1j, 1 - 1j, 1 + 1j):
        lon, lat = peirce_quincuncial_inverse(point, central_meridian=25)
        assert float(lon) == 25
        assert float(lat) == -90
    _, north = peirce_quincuncial_inverse(0)
    assert float(north) == 90
    point = peirce_quincuncial(-120, -30, central_meridian=25)
    lon, lat = peirce_quincuncial_inverse(point, central_meridian=25)
    assert float(lon) == pytest.approx(-120)
    assert float(lat) == pytest.approx(-30)


def test_invalid_tile_coordinate() -> None:
    with pytest.raises(ValueError, match="normalized Peirce square"):
        peirce_quincuncial_inverse(1.01 + 0j)


@pytest.mark.parametrize("rotation", [1, 1j, -1, -1j])
def test_half_turn_neighbor_tiles_join_geographically(rotation: complex) -> None:
    samples = np.linspace(-1, 1, 401)
    edge = rotation * (1 + 1j * samples)
    neighboring_edge = rotation * (1 - 1j * samples)
    lon_a, lat_a = peirce_quincuncial_inverse(edge, central_meridian=25)
    lon_b, lat_b = peirce_quincuncial_inverse(neighboring_edge, central_meridian=25)
    np.testing.assert_allclose((lon_a - lon_b + 180) % 360 - 180, 0, atol=1e-10)
    np.testing.assert_allclose(lat_a, lat_b, rtol=0, atol=1e-10)


def test_raster_wraps_longitude_without_wrapping_latitude() -> None:
    mosaic = np.array([[10, 20, 30, 70], [40, 50, 60, 90]], dtype=np.float64)
    north = sample_global_mosaic(mosaic, np.array([-180.0, 180.0]), np.array([90.0, 90.0]))
    south = sample_global_mosaic(mosaic, np.array([-180.0, 180.0]), np.array([-90.0, -90.0]))
    np.testing.assert_allclose(north, [40, 40])
    np.testing.assert_allclose(south, [65, 65])


@pytest.mark.parametrize(("lon", "lat"), [(12, 25), (78, -62), (-111, 64), (-135, -28.0)])
def test_linear_scale_agrees_with_meridian_derivative(lon: float, lat: float) -> None:
    h = 1e-4
    displacement = peirce_quincuncial(lon, lat + h) - peirce_quincuncial(lon, lat - h)
    numerical_scale = abs(displacement) / np.deg2rad(2 * h)
    expected = local_scale(np.array(lon), np.array(lat))
    assert numerical_scale == pytest.approx(float(expected), rel=1e-7)
