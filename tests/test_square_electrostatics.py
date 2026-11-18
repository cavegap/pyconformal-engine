import numpy as np
import pytest
from scipy.sparse import diags, eye, kron
from scipy.sparse.linalg import spsolve

from pyconformal.sc import square_electrostatic_potential as potential


@pytest.mark.parametrize(("x", "voltage"), [(-4.0, 1), (-1.0, 1), (0.0, 0), (0.3, 0), (1.0, 0)])
def test_electrode_voltage(x: float, voltage: float) -> None:
    assert potential(complex(x)) == voltage


@pytest.mark.parametrize("x", [-0.75, -0.25, 1.25, 2.5])
def test_insulating_segments_have_zero_normal_derivative(x: float) -> None:
    h = 1e-5
    derivative = (
        4 * potential(complex(x, h)) - potential(complex(x, 2 * h)) - 3 * potential(x)
    ) / (2 * h)
    assert derivative == pytest.approx(0, abs=2e-8)


def finite_difference_error(intervals: int) -> float:
    """Solve a separate five-point Laplace system on an interior box."""
    x = np.linspace(-1.6, 1.6, intervals + 1)
    y = np.linspace(0.25, 1.85, intervals + 1)
    reference = np.array([[potential(complex(a, b)) for a in x] for b in y])
    n = intervals - 1
    wx = 1 / (x[1] - x[0]) ** 2
    wy = 1 / (y[1] - y[0]) ** 2
    axis_operator = diags([-1, 2, -1], [-1, 0, 1], shape=(n, n))
    identity = eye(n)
    operator = wx * kron(identity, axis_operator) + wy * kron(axis_operator, identity)
    rhs = np.zeros((n, n))
    rhs[:, 0] += wx * reference[1:-1, 0]
    rhs[:, -1] += wx * reference[1:-1, -1]
    rhs[0, :] += wy * reference[0, 1:-1]
    rhs[-1, :] += wy * reference[-1, 1:-1]
    interior = spsolve(operator.tocsr(), rhs.ravel()).reshape(n, n)
    return float(np.max(np.abs(interior - reference[1:-1, 1:-1])))


def test_independent_laplace_solution_converges() -> None:
    coarse = finite_difference_error(20)
    fine = finite_difference_error(40)
    assert potential(1j) == pytest.approx(0.5)
    assert fine < coarse / 3.5
    assert fine < 3e-4
