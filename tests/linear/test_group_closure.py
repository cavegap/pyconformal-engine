"""Tests for Theorem 6 of the thesis: closure of group P under composition.

The thesis (pp. 16–17) proves closure by enumerating seven cases of the form
"composition of generator-type A with generator-type B = element of the
group". This test module reproduces each of those seven cases as an
independent test, plus the explicit commutativity claims of cases 6 and 7
and the dilation–reflection composition stated after case 7.

It also tests the group axioms (associativity, identity, inverse), giving
the full structural verification of Theorem 6.

Reference
---------
Vega Penagos & Olivero Zapata (2015), Theorem 6 and Corollary 1, pp. 16–17.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from pyconformal.linear import Dilation, LinearMap, Reflection, Rotation


# =========================================================================
# The seven cases of Theorem 6
# =========================================================================
class TestTheorem6Closure:
    """Each test corresponds to one of the seven cases in the closure proof
    of Theorem 6. The thesis uses the same angle θ for both factors as a
    notational simplification; here we test the general formulas with
    distinct parameters."""

    # ------------------------------------------------------------------
    # Case 1: Rotation ∘ Rotation = Rotation
    # ------------------------------------------------------------------
    @pytest.mark.parametrize(
        ("alpha", "beta"),
        [(0.3, 0.7), (1.2, -0.5), (math.pi, math.pi), (0.0, 1.4)],
    )
    def test_case_1_rotation_compose_rotation(self, alpha: float, beta: float) -> None:
        """R(α) ∘ R(β) = R(α + β)."""
        result = Rotation(alpha) @ Rotation(beta)
        expected = Rotation(alpha + beta)
        assert isinstance(result, Rotation)
        assert result.equals(expected)

    # ------------------------------------------------------------------
    # Case 2: Reflection ∘ Reflection = Rotation
    # ------------------------------------------------------------------
    @pytest.mark.parametrize(
        ("alpha", "beta"),
        [(0.3, 0.3), (0.5, 0.0), (1.1, 0.4), (-0.7, 0.2)],
    )
    def test_case_2_reflection_compose_reflection(self, alpha: float, beta: float) -> None:
        """Ref(α) ∘ Ref(β) = R(α − β).

        Specializing to α = β = θ recovers the thesis statement
        Ref(θ) ∘ Ref(θ) = I.
        """
        result = Reflection(alpha) @ Reflection(beta)
        expected = Rotation(alpha - beta)
        assert isinstance(result, Rotation)
        assert result.equals(expected)

    def test_case_2_special_same_angle_is_identity(self) -> None:
        """The thesis's specialization: Ref(θ) ∘ Ref(θ) = I."""
        for theta in (0.0, 0.5, 1.7, -0.3):
            assert (Reflection(theta) @ Reflection(theta)).is_identity()

    # ------------------------------------------------------------------
    # Case 3: Dilation ∘ Dilation = Dilation
    # ------------------------------------------------------------------
    @pytest.mark.parametrize(
        ("lam", "mu"),
        [(2.0, 3.0), (0.5, 4.0), (-1.5, 2.0), (1.0, -1.0)],
    )
    def test_case_3_dilation_compose_dilation(self, lam: float, mu: float) -> None:
        """D(λ) ∘ D(μ) = D(λ μ)."""
        result = Dilation(lam) @ Dilation(mu)
        expected = Dilation(lam * mu)
        assert isinstance(result, Dilation)
        assert result.equals(expected)

    # ------------------------------------------------------------------
    # Case 4: Rotation ∘ Reflection = Reflection
    # ------------------------------------------------------------------
    @pytest.mark.parametrize(
        ("alpha", "beta"),
        [(0.3, 0.7), (math.pi / 4, math.pi / 3), (0.0, 1.2), (-0.5, 0.5)],
    )
    def test_case_4_rotation_compose_reflection(self, alpha: float, beta: float) -> None:
        """R(α) ∘ Ref(β) = Ref(α + β)."""
        result = Rotation(alpha) @ Reflection(beta)
        expected = Reflection(alpha + beta)
        assert isinstance(result, Reflection)
        assert result.equals(expected)

    # ------------------------------------------------------------------
    # Case 5: Reflection ∘ Rotation = Reflection
    # ------------------------------------------------------------------
    @pytest.mark.parametrize(
        ("alpha", "beta"),
        [(0.3, 0.3), (1.0, 0.4), (0.0, 0.0), (0.7, -0.3)],
    )
    def test_case_5_reflection_compose_rotation(self, alpha: float, beta: float) -> None:
        """Ref(α) ∘ R(β) = Ref(α − β).

        Specializing to α = β = θ gives the thesis's matrix
        [[1, 0], [0, -1]] = Ref(0).
        """
        result = Reflection(alpha) @ Rotation(beta)
        expected = Reflection(alpha - beta)
        assert isinstance(result, Reflection)
        assert result.equals(expected)

    def test_case_5_special_same_angle(self) -> None:
        """Thesis specialization: Ref(θ) ∘ R(θ) is the reflection across the
        x-axis, i.e. matrix [[1, 0], [0, -1]] = Ref(0)."""
        for theta in (0.3, 1.1, -0.7):
            result = Reflection(theta) @ Rotation(theta)
            expected_matrix = np.array([[1.0, 0.0], [0.0, -1.0]])
            np.testing.assert_allclose(result.matrix, expected_matrix, atol=1e-12)

    # ------------------------------------------------------------------
    # Case 6: Dilation ∘ Rotation = scaled rotation
    # ------------------------------------------------------------------
    @pytest.mark.parametrize(
        ("lam", "theta"),
        [(2.0, 0.5), (0.3, 1.7), (-1.5, math.pi / 4)],
    )
    def test_case_6_dilation_compose_rotation(self, lam: float, theta: float) -> None:
        """D(λ) ∘ R(θ) has the scaled-rotation matrix of the thesis.

        Matrix form (thesis page 17):

            [[λ cos θ, -λ sin θ], [λ sin θ,  λ cos θ]]
        """
        result = Dilation(lam) @ Rotation(theta)
        c, s = math.cos(theta), math.sin(theta)
        expected = np.array([[lam * c, -lam * s], [lam * s, lam * c]])
        np.testing.assert_allclose(result.matrix, expected, atol=1e-12)
        # Closure: it preserves angles ⇒ it is still in P
        assert result.preserves_angles()

    # ------------------------------------------------------------------
    # Case 7: commutativity D ∘ R = R ∘ D
    # ------------------------------------------------------------------
    @pytest.mark.parametrize(
        ("lam", "theta"),
        [(2.0, 0.5), (0.3, 1.7), (-1.5, math.pi / 4), (3.0, -0.6)],
    )
    def test_case_7_dilation_rotation_commute(self, lam: float, theta: float) -> None:
        """Rotations and dilations commute: D(λ) ∘ R(θ) = R(θ) ∘ D(λ)."""
        a = Dilation(lam) @ Rotation(theta)
        b = Rotation(theta) @ Dilation(lam)
        assert a.equals(b)

    # ------------------------------------------------------------------
    # Final pair: Dilation ∘ Reflection (and its commutative twin)
    # ------------------------------------------------------------------
    @pytest.mark.parametrize(
        ("lam", "theta"),
        [(2.0, 0.5), (0.3, 1.7), (-1.5, 0.4)],
    )
    def test_dilation_reflection_is_scaled_reflection(self, lam: float, theta: float) -> None:
        """D(λ) ∘ Ref(θ) is a scaled reflection.

        Matrix form (thesis page 17, last paragraph of the proof):

            [[λ cos θ, λ sin θ], [λ sin θ, -λ cos θ]]
        """
        result = Dilation(lam) @ Reflection(theta)
        c, s = math.cos(theta), math.sin(theta)
        expected = np.array([[lam * c, lam * s], [lam * s, -lam * c]])
        np.testing.assert_allclose(result.matrix, expected, atol=1e-12)
        assert result.preserves_angles()

    @pytest.mark.parametrize(
        ("lam", "theta"),
        [(2.0, 0.5), (0.3, 1.7), (-1.5, 0.4)],
    )
    def test_dilation_reflection_commute(self, lam: float, theta: float) -> None:
        """The thesis states: Ref ∘ D = D ∘ Ref (same matrix)."""
        a = Dilation(lam) @ Reflection(theta)
        b = Reflection(theta) @ Dilation(lam)
        assert a.equals(b)


# =========================================================================
# Group axioms (Theorem 6)
# =========================================================================
class TestGroupAxioms:
    """The four group axioms required by Theorem 6: closure, associativity,
    identity, inverse."""

    def test_closure_preserves_angle_predicate(self) -> None:
        """Closure: composition of two angle-preserving maps preserves angles."""
        elements = [
            Rotation(0.5),
            Reflection(0.7),
            Dilation(2.0),
            Rotation(-1.2) @ Reflection(0.3),
            Dilation(0.5) @ Rotation(0.8),
        ]
        for a in elements:
            for b in elements:
                composed = a @ b
                assert composed.preserves_angles(), (
                    f"Composition {a!r} @ {b!r} should preserve angles"
                )

    @pytest.mark.parametrize(
        ("a", "b", "c"),
        [
            (Rotation(0.3), Rotation(0.7), Rotation(1.1)),
            (Rotation(0.3), Reflection(0.7), Dilation(2.0)),
            (Dilation(1.5), Reflection(0.5), Rotation(0.2)),
            (Reflection(0.1), Dilation(2.0), Reflection(0.9)),
        ],
    )
    def test_associativity(self, a: LinearMap, b: LinearMap, c: LinearMap) -> None:
        """(a ∘ b) ∘ c = a ∘ (b ∘ c)."""
        left = (a @ b) @ c
        right = a @ (b @ c)
        assert left.equals(right)

    def test_identity_element(self) -> None:
        """The identity element of P is Rotation(0) = Dilation(1)."""
        e1 = Rotation(0.0)
        e2 = Dilation(1.0)
        assert e1.is_identity()
        assert e2.is_identity()
        # Both are neutral when composed with anything
        for elt in (Rotation(0.5), Reflection(0.7), Dilation(2.0)):
            assert (e1 @ elt).equals(elt)
            assert (elt @ e1).equals(elt)
            assert (e2 @ elt).equals(elt)
            assert (elt @ e2).equals(elt)

    @pytest.mark.parametrize(
        "elt",
        [
            Rotation(0.5),
            Rotation(-1.2),
            Reflection(0.7),
            Reflection(0.0),
            Dilation(2.0),
            Dilation(-0.5),
        ],
    )
    def test_inverse_exists(self, elt: LinearMap) -> None:
        """Every element has an inverse with elt ∘ elt⁻¹ = I."""
        inv = elt.inverse()
        product = elt @ inv
        assert product.is_identity()
        product_other = inv @ elt
        assert product_other.is_identity()


# =========================================================================
# Corollary 1: rotations and dilations are subgroups
# =========================================================================
class TestCorollary1:
    """Corollary 1 of the thesis: rotations and dilations each form a
    subgroup of P (reflections do not, since the composition of two
    reflections is a rotation — Case 2 above)."""

    def test_rotations_form_subgroup(self) -> None:
        """The composition of two rotations is a rotation; the inverse of a
        rotation is a rotation. Hence rotations form a subgroup of P."""
        for theta in (0.3, 0.7, -0.5):
            for phi in (0.4, 1.2, -0.8):
                product = Rotation(theta) @ Rotation(phi)
                assert isinstance(product, Rotation)
            assert isinstance(Rotation(theta).inverse(), Rotation)

    def test_dilations_form_subgroup(self) -> None:
        """Same check for dilations."""
        for lam in (2.0, 0.5, -1.5):
            for mu in (3.0, 0.7, -0.3):
                product = Dilation(lam) @ Dilation(mu)
                assert isinstance(product, Dilation)
            assert isinstance(Dilation(lam).inverse(), Dilation)

    def test_reflections_do_not_form_subgroup(self) -> None:
        """Counter-example: Ref(0.5) ∘ Ref(0.0) = R(0.5), which is *not* a
        reflection. Hence reflections do *not* form a subgroup of P."""
        product = Reflection(0.5) @ Reflection(0.0)
        assert isinstance(product, Rotation)
        assert not isinstance(product, Reflection)
