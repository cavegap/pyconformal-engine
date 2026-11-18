import cmath
import math

import pytest
from scipy.integrate import quad

from pyconformal.elementary import exponential
from pyconformal.sc import upper_half_plane_to_square


def test_exponential_grid() -> None:
    for x in (-1.0, 0.0, 1.0):
        for y in (-3 * math.pi / 4, 0.0, math.pi / 2):
            image = exponential(complex(x, y))
            assert abs(image) == pytest.approx(math.exp(x))
            assert cmath.phase(image) == pytest.approx(y)
            assert exponential(complex(x, y + math.tau)) == pytest.approx(image)


def test_square_vertices() -> None:
    vertices = [upper_half_plane_to_square(z) for z in (-1 + 0j, 0j, 1 + 0j, complex(math.inf, 0))]
    assert vertices == pytest.approx([-1 + 1j, -1 - 1j, 1 - 1j, 1 + 1j])
    assert upper_half_plane_to_square(1j) == pytest.approx(0j, abs=1e-14)


@pytest.mark.parametrize(
    ("points", "normal", "coordinate"),
    [
        ((-100, -3, -1.01), 1j, 1),
        ((-0.99, -0.5, -0.01), 1, -1),
        ((0.01, 0.5, 0.99), 1j, -1),
        ((1.01, 3, 100), 1, 1),
    ],
)
def test_square_sides(points: tuple[float, ...], normal: complex, coordinate: float) -> None:
    values = [upper_half_plane_to_square(complex(point)) / normal for point in points]
    assert [value.real for value in values] == pytest.approx([coordinate] * 3)
    assert all(-1 < value.imag < 1 for value in values)


@pytest.mark.parametrize("z", [-3 + 0.1j, -0.01 + 0.03j, 0.7 + 0.1j, 2 + 3j, 12 + 5j])
def test_square_against_disk_quadrature(z: complex) -> None:
    disk_point = (z - 1j) / (z + 1j)

    def integrand(t: float) -> complex:
        return disk_point / cmath.sqrt(1 - (t * disk_point) ** 4)

    # Independent representation via the disk's four roots of unity.
    real, _ = quad(lambda t: integrand(t).real, 0, 1, epsabs=1e-12, epsrel=1e-12)
    imag, _ = quad(lambda t: integrand(t).imag, 0, 1, epsabs=1e-12, epsrel=1e-12)
    scale, _ = quad(lambda t: 1 / math.sqrt(1 - t**4), 0, 1, epsabs=1e-12, epsrel=1e-12)
    expected = (1 + 1j) * complex(real, imag) / scale
    mapped = upper_half_plane_to_square(z)
    assert mapped == pytest.approx(expected, abs=2e-12)
    assert abs(mapped.real) < 1
    assert abs(mapped.imag) < 1


@pytest.mark.parametrize("x", [-2.0, -0.5, 0.5, 2.0])
def test_square_boundary_limit_from_above(x: float) -> None:
    boundary = upper_half_plane_to_square(complex(x))
    limit = upper_half_plane_to_square(complex(x, 1e-10))
    assert limit == pytest.approx(boundary, abs=2e-10)


@pytest.mark.parametrize("z", [1 - 1j, complex(math.nan, 0), complex(0, math.inf)])
def test_square_rejects_invalid_points(z: complex) -> None:
    with pytest.raises(ValueError, match="closed upper half-plane"):
        upper_half_plane_to_square(z)
