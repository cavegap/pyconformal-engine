import math

import pytest
from examples.verify_coplanar_sensor import boundary_element_capacitance
from scipy.integrate import quad

from pyconformal.sc import coplanar_sensor_capacitance, coplanar_sensor_field


@pytest.mark.parametrize("gap", [0.1, 0.25, 0.5, 1.0, 2.0])
def test_strip_capacitance_against_boundary_elements(gap: float) -> None:
    analytical = coplanar_sensor_capacitance(1, gap)
    coarse = abs(boundary_element_capacitance(gap, 24) / analytical - 1)
    fine = abs(boundary_element_capacitance(gap, 96) / analytical - 1)
    assert fine < coarse / 10
    assert fine < 2.6e-4


def test_sensor_scales_with_permittivity_and_larger_gap_reduces_coupling() -> None:
    air = coplanar_sensor_capacitance(1, 0.25)
    filled = coplanar_sensor_capacitance(0.001, 0.00025, eps_r=3)
    assert filled == pytest.approx(3 * air, rel=1e-12)
    assert filled > coplanar_sensor_capacitance(0.001, 0.0005, eps_r=3)
    assert filled * 0.02 == pytest.approx(1.2109151283e-12, rel=1e-9)


def test_field_integrates_to_one_volt() -> None:
    assert coplanar_sensor_field(0.3j, 1, 2).real < 0
    assert coplanar_sensor_field(1.5 + 0.01j, 1, 2).imag > 0

    def gap_voltage(t: float) -> float:
        x = math.sin(t)
        return -coplanar_sensor_field(complex(x, 1e-9), 1, 2).real * math.cos(t)

    drop, _ = quad(gap_voltage, -math.pi / 2, math.pi / 2)
    assert drop == pytest.approx(1, abs=1e-4)


def test_reject_invalid_inputs() -> None:
    with pytest.raises(ValueError, match="Width and gap"):
        coplanar_sensor_capacitance(1, 0)
    with pytest.raises(ValueError, match="Relative permittivity"):
        coplanar_sensor_capacitance(1, 1, 0.2)
    with pytest.raises(ValueError, match="above the conductors"):
        coplanar_sensor_field(0j, 1, 1)
