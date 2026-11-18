import cmath
import math

import pytest

from pyconformal.mobius import disk_to_upper_half_plane


@pytest.mark.parametrize(("z", "expected"), [(0j, 1j), (1 + 0j, 0j), (1j, 1 + 0j), (-1j, -1 + 0j)])
def test_reference_points(z: complex, expected: complex) -> None:
    assert disk_to_upper_half_plane(z) == pytest.approx(expected)


@pytest.mark.parametrize("radius", [0.0, 0.5, 0.9, 0.999, 1.0])
def test_disk_and_boundary(radius: float) -> None:
    for angle in (0.2, 0.9, 1.5, 2.7, 3.6, 5.8):
        z = cmath.rect(radius, angle)
        w = disk_to_upper_half_plane(z)
        assert (1j - w) / (1j + w) == pytest.approx(z)
        if radius == 1:
            assert w.imag == pytest.approx(0, abs=1e-12)
        else:
            assert w.imag > 0


def test_pole_and_approach_from_inside() -> None:
    pole = disk_to_upper_half_plane(-1 + 0j)
    assert math.isinf(pole.real)
    assert pole.imag == 0
    assert disk_to_upper_half_plane(-1 + 1e-12j).real == pytest.approx(2e12)
    assert disk_to_upper_half_plane(-1 + 1e-8).imag == pytest.approx(2e8, rel=1e-7)


def test_nonfinite_input() -> None:
    with pytest.raises(ValueError, match="finite"):
        disk_to_upper_half_plane(complex(float("nan"), 0))


def test_large_finite_point() -> None:
    assert disk_to_upper_half_plane(1.7e308 + 1.7e308j) == pytest.approx(-1j)
