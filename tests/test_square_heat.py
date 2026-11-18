import math

import numpy as np
import pytest

from pyconformal.sc import square_heat_temperature as temperature


@pytest.mark.parametrize(
    ("point", "expected"),
    [(-1 + 0j, 20), (0j, 100), (1 + 0j, 20), (complex(math.inf), 100), (1j, 60)],
)
def test_thermal_corner_and_center_data(point: complex, expected: float) -> None:
    assert temperature(point) == pytest.approx(expected)


@pytest.mark.parametrize("center", [0.3 + 0.6j, -1.2 + 0.35j, 1.7 + 1.2j])
def test_harmonic_mean_value_on_independent_circles(center: complex) -> None:
    boundary = center + 0.15 * np.exp(2j * np.pi * np.arange(256) / 256)
    average = float(np.mean([temperature(complex(z)) for z in boundary]))
    assert average == pytest.approx(temperature(center), abs=2e-10)


def test_constant_boundary_midpoint_and_affine_temperature_units() -> None:
    assert temperature(1j, cold=0, hot=1) == pytest.approx(0.5)
    for point in (0.4 + 0.5j, -2 + 0.2j, 2j):
        assert temperature(point, cold=273.15, hot=373.15) == pytest.approx(
            273.15 + 100 * temperature(point, cold=0, hot=1)
        )


@pytest.mark.parametrize(("cold", "hot"), [(20, 20), (100, 20), (math.nan, 100), (0, math.inf)])
def test_reject_invalid_temperature_data(cold: float, hot: float) -> None:
    with pytest.raises(ValueError, match="cold < hot"):
        temperature(1j, cold=cold, hot=hot)


def test_reject_lower_half_plane() -> None:
    with pytest.raises(ValueError, match="upper half-plane"):
        temperature(-1j)
