"""Tests for the generic :class:`LinearMap` base class.

These exercise the parts of the base API not specific to any one generator:
shape validation, the generic ``inverse()`` fallback (via matrix inversion),
``__repr__``, and the edge cases of ``preserves_angles`` and the composition
fallback cases.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from pyconformal.linear import Dilation, LinearMap, Reflection, Rotation


class TestBaseLinearMap:
    """Tests for the generic :class:`LinearMap` class."""

    def test_shape_validation_rejects_non_2x2(self) -> None:
        """The constructor must reject matrices of the wrong shape."""
        with pytest.raises(ValueError, match="2x2 matrix"):
            LinearMap(np.array([1.0, 2.0]))
        with pytest.raises(ValueError, match="2x2 matrix"):
            LinearMap(np.eye(3))

    def test_matrix_returns_copy_not_view(self) -> None:
        """Mutating the returned matrix must not affect the underlying state."""
        R = Rotation(0.5)
        m = R.matrix
        m[0, 0] = 999.0
        # The original is unchanged
        assert R.matrix[0, 0] != 999.0

    def test_generic_inverse_via_matrix_inversion(self) -> None:
        """The base ``inverse()`` uses numpy's matrix inverse."""
        # Build a generic LinearMap that is not a pure generator
        m = LinearMap(np.array([[2.0, 1.0], [0.5, 1.5]]))
        # This matrix is not in group P; we are only testing the inverse
        # mechanics here, not the conformal property.
        inv = m.inverse()
        product = m.matrix @ inv.matrix
        np.testing.assert_allclose(product, np.eye(2), atol=1e-12)

    def test_repr_of_generic_linearmap(self) -> None:
        """``__repr__`` produces a reasonable string."""
        m = LinearMap(np.array([[1.5, -0.5], [0.5, 1.5]]))
        text = repr(m)
        assert "LinearMap" in text
        assert "1.5" in text

    def test_preserves_angles_false_for_degenerate_image(self) -> None:
        """A singular (rank-1) map sends some nonzero vectors to zero, so it
        does not preserve angles in the sense of Definition 1."""
        # Projection onto the x-axis: (x, y) -> (x, 0)
        proj = LinearMap(np.array([[1.0, 0.0], [0.0, 0.0]]))
        assert not proj.preserves_angles()

    def test_preserves_angles_handles_zero_input_pair(self) -> None:
        """If the RNG happens to produce an (almost) zero vector, the
        function should skip it rather than divide by zero. With our fixed
        seed this is statistically unlikely but the code path exists."""
        R = Rotation(0.5)
        # Just run the check; if any zero-vector samples are produced they
        # are skipped without error.
        assert R.preserves_angles(n_samples=4)


class TestComposeFallbackBranches:
    """Cover the trivial-lambda short-circuits in ``compose``."""

    def test_dilation_one_compose_rotation(self) -> None:
        """D(1) ∘ R(θ) = R(θ) (the dilation is the identity)."""
        result = Dilation(1.0) @ Rotation(0.5)
        assert isinstance(result, Rotation)
        assert math.isclose(result.theta, 0.5)

    def test_dilation_minus_one_compose_rotation(self) -> None:
        """D(-1) ∘ R(θ) = R(θ + π) since -I is a half-turn."""
        result = Dilation(-1.0) @ Rotation(0.5)
        assert isinstance(result, Rotation)
        # Compare matrices: should equal Rotation(0.5 + π)
        expected = Rotation(0.5 + math.pi)
        assert result.equals(expected)

    def test_rotation_compose_dilation_one(self) -> None:
        """R(θ) ∘ D(1) = R(θ)."""
        result = Rotation(0.7) @ Dilation(1.0)
        assert isinstance(result, Rotation)
        assert math.isclose(result.theta, 0.7)

    def test_rotation_compose_dilation_minus_one(self) -> None:
        """R(θ) ∘ D(-1) = R(θ + π)."""
        result = Rotation(0.7) @ Dilation(-1.0)
        assert isinstance(result, Rotation)
        assert result.equals(Rotation(0.7 + math.pi))

    def test_dilation_one_compose_reflection(self) -> None:
        """D(1) ∘ Ref(θ) = Ref(θ)."""
        result = Dilation(1.0) @ Reflection(0.3)
        assert isinstance(result, Reflection)
        assert math.isclose(result.theta, 0.3)

    def test_reflection_compose_dilation_one(self) -> None:
        """Ref(θ) ∘ D(1) = Ref(θ)."""
        result = Reflection(0.3) @ Dilation(1.0)
        assert isinstance(result, Reflection)
        assert math.isclose(result.theta, 0.3)

    def test_dilation_minus_one_compose_reflection_is_generic(self) -> None:
        """D(-1) ∘ Ref(θ) is still in P but our dispatch returns it as a
        generic LinearMap (it equals Ref(θ + π), but the simplification is
        not implemented for this case)."""
        result = Dilation(-1.0) @ Reflection(0.3)
        # Either way, it must preserve angles
        assert result.preserves_angles()

    def test_generic_linearmap_compose_falls_through(self) -> None:
        """Composition of two generic LinearMaps returns a generic LinearMap."""
        a = LinearMap(np.array([[2.0, 0.0], [0.0, 3.0]]))  # not in P
        b = LinearMap(np.array([[1.0, 1.0], [0.0, 1.0]]))  # not in P
        result = a @ b
        expected_matrix = a.matrix @ b.matrix
        np.testing.assert_allclose(result.matrix, expected_matrix)
