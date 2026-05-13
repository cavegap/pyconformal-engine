"""Property-based tests for group P using Hypothesis.

These tests verify the algebraic identities of Theorem 6 against random
parameter values, complementing the parametrized examples in
``test_group_closure.py``.
"""

from __future__ import annotations

import math

import numpy as np
from hypothesis import given, settings
from hypothesis import strategies as st

from pyconformal.linear import Dilation, Reflection, Rotation

# A safe range for angle parameters: avoid near-singular cases.
ANGLE = st.floats(
    min_value=-2 * math.pi,
    max_value=2 * math.pi,
    allow_nan=False,
    allow_infinity=False,
)
# Nonzero, bounded dilation factors (positive or negative).
LAMBDA = st.one_of(
    st.floats(min_value=1e-3, max_value=1e3, allow_nan=False, allow_infinity=False),
    st.floats(min_value=-1e3, max_value=-1e-3, allow_nan=False, allow_infinity=False),
)
# Bounded complex points for application tests.
COMPLEX_POINT = st.complex_numbers(
    min_magnitude=0.0,
    max_magnitude=100.0,
    allow_nan=False,
    allow_infinity=False,
)


@given(alpha=ANGLE, beta=ANGLE)
def test_property_rotation_composition_adds_angles(alpha: float, beta: float) -> None:
    """R(α) ∘ R(β) ≡ R(α + β) for all real α, β."""
    composed = Rotation(alpha) @ Rotation(beta)
    expected = Rotation(alpha + beta)
    assert composed.equals(expected, tol=1e-10)


@given(lam=LAMBDA, mu=LAMBDA)
def test_property_dilation_composition_multiplies(lam: float, mu: float) -> None:
    """D(λ) ∘ D(μ) ≡ D(λμ) for nonzero λ, μ."""
    composed = Dilation(lam) @ Dilation(mu)
    expected = Dilation(lam * mu)
    assert composed.equals(expected, tol=1e-8)


@given(alpha=ANGLE, beta=ANGLE)
def test_property_reflection_composition_subtracts_angles(alpha: float, beta: float) -> None:
    """Ref(α) ∘ Ref(β) ≡ R(α − β)."""
    composed = Reflection(alpha) @ Reflection(beta)
    expected = Rotation(alpha - beta)
    assert composed.equals(expected, tol=1e-10)


@given(alpha=ANGLE, beta=ANGLE)
def test_property_rotation_reflection_adds_angles(alpha: float, beta: float) -> None:
    """R(α) ∘ Ref(β) ≡ Ref(α + β)."""
    composed = Rotation(alpha) @ Reflection(beta)
    expected = Reflection(alpha + beta)
    assert composed.equals(expected, tol=1e-10)


@given(alpha=ANGLE, beta=ANGLE)
def test_property_reflection_rotation_subtracts_angles(alpha: float, beta: float) -> None:
    """Ref(α) ∘ R(β) ≡ Ref(α − β)."""
    composed = Reflection(alpha) @ Rotation(beta)
    expected = Reflection(alpha - beta)
    assert composed.equals(expected, tol=1e-10)


@given(theta=ANGLE)
def test_property_rotation_preserves_norms(theta: float) -> None:
    """Any rotation preserves the modulus of any complex point."""
    R = Rotation(theta)
    z = 3.0 + 4.0j  # |z| = 5
    w = R(z)
    assert isinstance(w, complex)
    assert math.isclose(abs(w), abs(z), abs_tol=1e-12)


@given(lam=LAMBDA, z=COMPLEX_POINT)
def test_property_dilation_scales_modulus(lam: float, z: complex) -> None:
    """|D(λ)(z)| = |λ| · |z|."""
    D = Dilation(lam)
    w = D(z)
    assert isinstance(w, complex)
    assert math.isclose(abs(w), abs(lam) * abs(z), rel_tol=1e-10, abs_tol=1e-12)


@given(theta=ANGLE)
def test_property_reflection_involution(theta: float) -> None:
    """Any reflection is its own inverse."""
    Ref = Reflection(theta)
    assert (Ref @ Ref).is_identity(tol=1e-10)


@given(lam=LAMBDA, theta=ANGLE)
def test_property_dilation_rotation_commute(lam: float, theta: float) -> None:
    """D(λ) ∘ R(θ) ≡ R(θ) ∘ D(λ)."""
    a = Dilation(lam) @ Rotation(theta)
    b = Rotation(theta) @ Dilation(lam)
    assert a.equals(b, tol=1e-10)


@settings(max_examples=50)
@given(theta=ANGLE)
def test_property_rotation_preserves_angles(theta: float) -> None:
    """Any rotation passes the numerical angle-preservation check."""
    assert Rotation(theta).preserves_angles(n_samples=16)


@settings(max_examples=50)
@given(lam=LAMBDA)
def test_property_dilation_preserves_angles(lam: float) -> None:
    """Any nonzero dilation passes the numerical angle-preservation check."""
    assert Dilation(lam).preserves_angles(n_samples=16)


@settings(max_examples=50)
@given(theta=ANGLE)
def test_property_reflection_preserves_angles(theta: float) -> None:
    """Any reflection passes the numerical angle-preservation check."""
    assert Reflection(theta).preserves_angles(n_samples=16)


@given(theta=ANGLE, z=COMPLEX_POINT)
def test_property_rotation_inverse_roundtrip(theta: float, z: complex) -> None:
    """R(θ).inverse()(R(θ)(z)) ≈ z."""
    R = Rotation(theta)
    z_back = R.inverse()(R(z))
    assert isinstance(z_back, complex)
    assert abs(z_back - z) < 1e-10 + 1e-10 * abs(z)


@given(lam=LAMBDA, z=COMPLEX_POINT)
def test_property_dilation_inverse_roundtrip(lam: float, z: complex) -> None:
    """D(λ).inverse()(D(λ)(z)) ≈ z."""
    D = Dilation(lam)
    z_back = D.inverse()(D(z))
    assert isinstance(z_back, complex)
    assert abs(z_back - z) < 1e-8 + 1e-8 * abs(z)


@given(theta=ANGLE)
def test_property_rotation_is_orthogonal_and_det_one(theta: float) -> None:
    """Theorem 2 corollary: rotations are orthogonal with det = 1."""
    R = Rotation(theta)
    assert R.is_orthogonal()
    assert math.isclose(R.det, 1.0, abs_tol=1e-12)


@given(theta=ANGLE)
def test_property_reflection_is_orthogonal_and_det_minus_one(theta: float) -> None:
    """Theorem 3 corollary: reflections are orthogonal with det = -1."""
    Ref = Reflection(theta)
    assert Ref.is_orthogonal()
    assert math.isclose(Ref.det, -1.0, abs_tol=1e-12)


@given(alpha=ANGLE, beta=ANGLE, gamma=ANGLE)
def test_property_associativity_of_rotations(alpha: float, beta: float, gamma: float) -> None:
    """(R(α) ∘ R(β)) ∘ R(γ) ≡ R(α) ∘ (R(β) ∘ R(γ))."""
    left = (Rotation(alpha) @ Rotation(beta)) @ Rotation(gamma)
    right = Rotation(alpha) @ (Rotation(beta) @ Rotation(gamma))
    assert left.equals(right, tol=1e-10)


@given(theta=ANGLE)
def test_property_rotation_call_matches_complex_multiplication(theta: float) -> None:
    """R(θ)(z) = e^(iθ) · z."""
    R = Rotation(theta)
    z = 2.0 - 0.5j
    w = R(z)
    expected = np.exp(1j * theta) * z
    assert isinstance(w, complex)
    assert abs(w - expected) < 1e-12
