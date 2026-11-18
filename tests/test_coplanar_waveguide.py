import math

import pytest
from scipy.integrate import quad

from pyconformal.sc import coplanar_electric_field, coplanar_waveguide, gap_for_impedance


@pytest.mark.parametrize(
    ("gap_ratio", "reference"),
    [
        (0.03, 60.112015323624),
        (0.1, 78.232188366566),
        (0.2, 93.308087504633),
        (0.5, 120.484159416401),
        (1.0, 147.245224257507),
        (2.0, 179.010023804977),
    ],
)
def test_matches_scikit_rf_quasi_static_reference(gap_ratio: float, reference: float) -> None:
    assert coplanar_waveguide(1, gap_ratio).impedance_ohm == pytest.approx(reference, rel=2.1e-6)


def test_find_50_ohm_design() -> None:
    gap = gap_for_impedance(1, 50, eps_r=4)
    result = coplanar_waveguide(1, gap, eps_r=4)
    assert gap == pytest.approx(0.2583435705)
    assert result.impedance_ohm == pytest.approx(50)
    assert result.capacitance_f_per_m == pytest.approx(133.42563808e-12, rel=1e-9)
    assert coplanar_waveguide(1, gap * 1.1, eps_r=4).impedance_ohm > 50


def test_scale_and_dielectric_relations() -> None:
    air = coplanar_waveguide(1, 0.25)
    dielectric = coplanar_waveguide(0.001, 0.00025, eps_r=4)
    assert dielectric.impedance_ohm == pytest.approx(air.impedance_ohm / 2)
    assert dielectric.capacitance_f_per_m == pytest.approx(4 * air.capacitance_f_per_m, abs=1e-19)
    assert dielectric.velocity_m_per_s == pytest.approx(air.velocity_m_per_s / 2)


def test_field_is_symmetric_and_has_one_volt_across_slot() -> None:
    field = coplanar_electric_field(0.4 + 0.3j, 2, 1)
    reflected = coplanar_electric_field(-0.4 + 0.3j, 2, 1)
    assert reflected == pytest.approx(-field.conjugate())
    assert coplanar_electric_field(0.3j, 2, 1).imag > 0

    def slot_drop(t: float) -> float:
        x = 1 + math.sin(t) ** 2  # regularize the endpoint integrals
        return coplanar_electric_field(complex(x, 1e-9), 2, 1).real * math.sin(2 * t)

    drop, _ = quad(slot_drop, 0, math.pi / 2)
    assert drop == pytest.approx(1, abs=1e-4)


@pytest.mark.parametrize(("width", "gap", "eps_r"), [(0, 1, 1), (1, -1, 1), (1, 1, 0.8)])
def test_reject_invalid_geometry_or_material(width: float, gap: float, eps_r: float) -> None:
    with pytest.raises(ValueError, match=r"Width and gap|Relative permittivity"):
        coplanar_waveguide(width, gap, eps_r)
