import numpy as np
from examples.lunar_mercator import LANDMARKS, inverse_cube, source_coordinate


def test_cubic_inverse_across_the_thesis_rectangle() -> None:
    grid = np.linspace(0, 12, 49)[None, :] + 1j * np.linspace(0, 6, 25)[:, None]
    mapped = np.asarray(grid**3, dtype=np.complex128)
    np.testing.assert_allclose(inverse_cube(mapped), grid, rtol=0, atol=5e-14)


def test_cubic_inverse_masks_points_outside_the_raster() -> None:
    outside = np.array([1 - 1j, 13**3 + 0j, (7j) ** 3])
    assert np.all(np.isnan(inverse_cube(outside)))


def test_lunar_landmarks_are_inside_the_mercator_crop() -> None:
    projected = np.array([source_coordinate(lon, lat) for _, lon, lat, _ in LANDMARKS])
    assert np.all((projected.real > 0) & (projected.real < 12))
    assert np.all((projected.imag > 0) & (projected.imag < 6))
    np.testing.assert_allclose(
        inverse_cube(projected * projected * projected), projected, rtol=0, atol=5e-14
    )
