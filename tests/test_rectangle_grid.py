import numpy as np
import pytest
from numpy.typing import NDArray

from pyconformal.viz import apply_conformal_to_rectangle


def cube(points: NDArray[np.complex128]) -> NDArray[np.complex128]:
    return points * points * points


def test_lunar_cubic_rectangle() -> None:
    grid = apply_conformal_to_rectangle(cube, 0j, 12 + 6j, 13, 7, samples=121)
    assert grid.horizontal.shape == (7, 121)
    assert grid.vertical.shape == (13, 121)
    np.testing.assert_allclose(grid.horizontal[:, 0], grid.vertical[0, ::20])
    np.testing.assert_allclose(grid.horizontal[:, -1], grid.vertical[-1, ::20])
    np.testing.assert_allclose(
        grid.mapped_horizontal[np.ix_([0, -1], [0, -1])],
        [[0j, 1728 + 0j], [-216j, 432 + 2376j]],
    )
    np.testing.assert_allclose(
        grid.mapped_vertical[np.ix_([0, -1], [0, -1])],
        [[0j, -216j], [1728 + 0j, 432 + 2376j]],
    )


def test_shifted_domain() -> None:
    grid = apply_conformal_to_rectangle(lambda z: z + 1j, -2 - 3j, 1 - 1j, 3, 2, samples=5)
    np.testing.assert_allclose(grid.horizontal[[0, 1], [0, -1]], [-2 - 3j, 1 - 1j])
    np.testing.assert_allclose(grid.mapped_vertical, grid.vertical + 1j)


@pytest.mark.parametrize("end", [-1 + 2j, 2 + 0j, complex(float("inf"), 2)])
def test_invalid_rectangle(end: complex) -> None:
    with pytest.raises(ValueError, match="corners"):
        apply_conformal_to_rectangle(cube, 0j, end, 2, 2)


def test_invalid_sampling_and_output_shape() -> None:
    with pytest.raises(ValueError, match="at least two"):
        apply_conformal_to_rectangle(cube, 0j, 1 + 1j, 2, 2, samples=1)
    with pytest.raises(ValueError, match="same shape"):
        apply_conformal_to_rectangle(lambda z: z[0], 0j, 1 + 1j, 3, 3)
