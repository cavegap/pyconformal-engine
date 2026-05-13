"""Tests for the individual generators of group P.

Covers Theorems 2 (rotation), 3 (reflection), and 4 (dilation) of the thesis,
plus basic API tests for ``__call__``, ``inverse``, ``matrix``, ``det``, etc.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from pyconformal.linear import Dilation, Reflection, Rotation


# =========================================================================
# Rotation (Theorem 2)
# =========================================================================
class TestRotation:
    """Tests for :class:`Rotation` — Theorem 2 of the thesis."""

    def test_zero_angle_is_identity(self) -> None:
        R = Rotation(0.0)
        assert R.is_identity()

    def test_quarter_turn_sends_1_to_i(self) -> None:
        R = Rotation(math.pi / 2)
        w = R(1.0 + 0.0j)
        assert isinstance(w, complex)
        assert abs(w - 1j) < 1e-12

    def test_half_turn_sends_1_to_minus_1(self) -> None:
        R = Rotation(math.pi)
        w = R(1.0 + 0.0j)
        assert abs(w - (-1.0)) < 1e-12

    def test_full_turn_is_identity(self) -> None:
        R = Rotation(2 * math.pi)
        assert R.is_identity(tol=1e-12)

    @pytest.mark.parametrize("theta", [0.1, 0.7, 1.5, -0.3, 3.0])
    def test_is_orthogonal(self, theta: float) -> None:
        assert Rotation(theta).is_orthogonal()

    @pytest.mark.parametrize("theta", [0.1, 0.7, -1.4])
    def test_determinant_is_one(self, theta: float) -> None:
        assert abs(Rotation(theta).det - 1.0) < 1e-12

    @pytest.mark.parametrize("theta", [0.1, 0.7, -1.4])
    def test_preserves_orientation(self, theta: float) -> None:
        assert Rotation(theta).preserves_orientation

    @pytest.mark.parametrize("theta", [0.1, 0.7, 1.4, -2.0])
    def test_inverse_is_negative_angle(self, theta: float) -> None:
        R = Rotation(theta)
        Rinv = R.inverse()
        assert isinstance(Rinv, Rotation)
        assert abs(Rinv.theta - (-theta)) < 1e-12

    @pytest.mark.parametrize("theta", [0.1, 0.7, 1.4, -2.0])
    def test_inverse_round_trip(self, theta: float) -> None:
        R = Rotation(theta)
        z = 2.0 + 3.0j
        w = R(z)
        z_back = R.inverse()(w)
        assert abs(z_back - z) < 1e-12

    def test_preserves_angles_numerically(self) -> None:
        """Theorem 2: rotations preserve angles between vectors."""
        for theta in (0.1, 0.7, 1.5, -0.4, 2.8):
            assert Rotation(theta).preserves_angles()

    def test_array_input(self) -> None:
        R = Rotation(math.pi / 2)
        z = np.array([1.0 + 0.0j, 0.0 + 1.0j, 1.0 + 1.0j])
        w = R(z)
        assert isinstance(w, np.ndarray)
        expected = np.array([1j, -1.0 + 0j, -1.0 + 1j])
        np.testing.assert_allclose(w, expected, atol=1e-12)

    def test_repr(self) -> None:
        assert "Rotation(theta=0.5)" in repr(Rotation(0.5))


# =========================================================================
# Reflection (Theorem 3)
# =========================================================================
class TestReflection:
    """Tests for :class:`Reflection` — Theorem 3 of the thesis."""

    def test_reflection_zero_is_x_axis(self) -> None:
        """Ref(0) reflects across the x-axis: (x, y) -> (x, -y)."""
        Ref = Reflection(0.0)
        assert abs(Ref(1.0 + 2.0j) - (1.0 - 2.0j)) < 1e-12

    @pytest.mark.parametrize("theta", [0.0, 0.5, 1.0, -0.7, 2.3])
    def test_is_orthogonal(self, theta: float) -> None:
        assert Reflection(theta).is_orthogonal()

    @pytest.mark.parametrize("theta", [0.0, 0.5, 1.0, -0.7])
    def test_determinant_is_minus_one(self, theta: float) -> None:
        assert abs(Reflection(theta).det - (-1.0)) < 1e-12

    @pytest.mark.parametrize("theta", [0.0, 0.5, 1.0, -0.7])
    def test_inverts_orientation(self, theta: float) -> None:
        assert not Reflection(theta).preserves_orientation

    @pytest.mark.parametrize("theta", [0.0, 0.5, 1.0, -0.7, 3.0])
    def test_is_involution(self, theta: float) -> None:
        """Ref(θ) ∘ Ref(θ) = identity."""
        Ref = Reflection(theta)
        assert (Ref @ Ref).is_identity()

    @pytest.mark.parametrize("theta", [0.0, 0.5, -0.7])
    def test_inverse_equals_self(self, theta: float) -> None:
        Ref = Reflection(theta)
        inv = Ref.inverse()
        assert isinstance(inv, Reflection)
        assert Ref.equals(inv)

    def test_preserves_angles_numerically(self) -> None:
        """Theorem 3: reflections preserve angles."""
        for theta in (0.0, 0.4, 1.1, -0.3, 2.5):
            assert Reflection(theta).preserves_angles()


# =========================================================================
# Dilation (Theorem 4)
# =========================================================================
class TestDilation:
    """Tests for :class:`Dilation` — Theorem 4 of the thesis."""

    def test_lambda_zero_raises(self) -> None:
        with pytest.raises(ValueError, match="nonzero"):
            Dilation(0.0)

    def test_identity_when_lambda_one(self) -> None:
        assert Dilation(1.0).is_identity()

    @pytest.mark.parametrize("lam", [0.5, 2.0, -1.5, 10.0])
    def test_applies_as_scalar_multiplication(self, lam: float) -> None:
        D = Dilation(lam)
        z = 3.0 + 4.0j
        assert abs(D(z) - lam * z) < 1e-12

    @pytest.mark.parametrize("lam", [0.5, 2.0, -1.5])
    def test_determinant_is_lambda_squared(self, lam: float) -> None:
        assert abs(Dilation(lam).det - lam**2) < 1e-12

    @pytest.mark.parametrize("lam", [0.5, 2.0, -1.5, -3.0])
    def test_preserves_orientation_always(self, lam: float) -> None:
        """Det = λ² > 0 for any nonzero λ, so orientation is always preserved."""
        assert Dilation(lam).preserves_orientation

    @pytest.mark.parametrize("lam", [0.5, 2.0, -1.5])
    def test_inverse_is_reciprocal(self, lam: float) -> None:
        D = Dilation(lam)
        Dinv = D.inverse()
        assert isinstance(Dinv, Dilation)
        assert abs(Dinv.lambda_ - 1.0 / lam) < 1e-12

    @pytest.mark.parametrize("lam", [0.7, 1.5, -2.0])
    def test_inverse_round_trip(self, lam: float) -> None:
        D = Dilation(lam)
        z = 1.0 + 2.0j
        assert abs(D.inverse()(D(z)) - z) < 1e-12

    def test_preserves_angles_numerically(self) -> None:
        """Theorem 4: dilations preserve angles (though not distances)."""
        for lam in (0.5, 1.0, 2.0, -1.5):
            assert Dilation(lam).preserves_angles()

    def test_not_orthogonal_when_lambda_not_unit(self) -> None:
        """Dilations are orthogonal iff |λ| = 1 (rotations / -I)."""
        assert not Dilation(2.0).is_orthogonal()
        assert not Dilation(0.5).is_orthogonal()
        assert Dilation(1.0).is_orthogonal()
        assert Dilation(-1.0).is_orthogonal()
