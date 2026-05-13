"""Abstract base class for elements of group P (Chapter 1 of the thesis).

An element of group P is an angle-preserving linear map R² → R². By Theorem 5
of Vega Penagos & Olivero Zapata (2015), every such map can be written as a
composition of rotations, reflections, and dilations; equivalently, its matrix
is a (possibly negative) scalar multiple of an orthogonal matrix.

The :class:`LinearMap` base class provides the common interface and the
universal fallback type used when a composition does not simplify to a pure
:class:`Rotation`, :class:`Reflection`, or :class:`Dilation`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, overload

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    from collections.abc import Iterable

ArrayF = NDArray[np.float64]
ArrayC = NDArray[np.complex128]


class LinearMap:
    """Element of group P: an angle-preserving linear map R² → R².

    Parameters
    ----------
    matrix : array_like, shape (2, 2)
        The 2x2 real matrix representing this linear map in the canonical
        basis of R². It must be a scalar multiple of an orthogonal matrix
        (this is exactly the characterization of group P, see Theorem 5).

    Attributes
    ----------
    matrix : ndarray, shape (2, 2), dtype float64
        Read-only copy of the underlying matrix.

    Notes
    -----
    This base class can be instantiated directly with an arbitrary 2x2 matrix,
    but the preferred entry points are the subclasses :class:`Rotation`,
    :class:`Reflection`, and :class:`Dilation`, which mirror the three
    generators of group P enumerated in §1.1 of the thesis.

    Compositions of those generators that do not simplify to a single pure
    generator are returned as a generic :class:`LinearMap`.

    References
    ----------
    Vega Penagos, C. A. & Olivero Zapata, H. A. (2015).
    *Implementación en software de aplicaciones conformes*.
    Universidad del Tolima. See Chapter 1, Definition 1 and Theorem 5.
    """

    __slots__ = ("_matrix",)

    def __init__(self, matrix: NDArray[Any] | Iterable[Iterable[float]]) -> None:
        arr = np.asarray(matrix, dtype=np.float64)
        if arr.shape != (2, 2):
            raise ValueError(f"LinearMap requires a 2x2 matrix; got shape {arr.shape}.")
        self._matrix = arr

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------
    @property
    def matrix(self) -> ArrayF:
        """Return a copy of the underlying 2x2 matrix."""
        copy: ArrayF = self._matrix.copy()
        return copy

    @property
    def det(self) -> float:
        """Determinant of the matrix.

        For elements of group P the determinant equals ``±scale²``; positive
        for rotation-like elements (preserve orientation) and negative for
        reflection-like elements (invert orientation).
        """
        m = self._matrix
        return float(m[0, 0] * m[1, 1] - m[0, 1] * m[1, 0])

    @property
    def scale(self) -> float:
        """Positive scale factor: ``||M e₁||`` with ``e₁ = (1, 0)``.

        Every element of group P factors as ``scale · O`` with ``O``
        orthogonal; this property recovers ``scale``.
        """
        col = self._matrix[:, 0]
        return float(np.linalg.norm(col))

    @property
    def preserves_orientation(self) -> bool:
        """Whether this map preserves orientation (``det > 0``).

        Rotation-like elements preserve orientation; reflection-like elements
        invert it. See Theorem 8 of the thesis for the complex-analytic
        counterpart of this distinction.
        """
        return self.det > 0.0

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------
    @overload
    def __call__(self, z: complex) -> complex: ...

    @overload
    def __call__(self, z: NDArray[Any]) -> ArrayC: ...

    def __call__(self, z: complex | float | NDArray[Any]) -> complex | ArrayC:
        """Apply this linear map to a complex number or array of them.

        Parameters
        ----------
        z : complex or ndarray of complex
            Point(s) in C ≅ R² to transform.

        Returns
        -------
        complex or ndarray of complex
            The image(s), same shape as ``z``.
        """
        z_arr = np.asarray(z, dtype=np.complex128)
        x = z_arr.real
        y = z_arr.imag
        m = self._matrix
        out_x = m[0, 0] * x + m[0, 1] * y
        out_y = m[1, 0] * x + m[1, 1] * y
        out = out_x + 1j * out_y
        if z_arr.ndim == 0:
            return complex(out)
        result: ArrayC = np.asarray(out, dtype=np.complex128)
        return result

    # ------------------------------------------------------------------
    # Group operations
    # ------------------------------------------------------------------
    def __matmul__(self, other: LinearMap) -> LinearMap:
        """Compose ``self ∘ other`` via the dispatch of Theorem 6.

        The result is returned as the most specific subclass possible
        (``Rotation``, ``Reflection``, ``Dilation``, or a generic
        :class:`LinearMap`).
        """
        from .composition import compose  # local import to avoid cycle

        return compose(self, other)

    def inverse(self) -> LinearMap:
        """Return the inverse linear map.

        For a generic :class:`LinearMap` this inverts the matrix directly.
        Subclasses override with closed-form inverses (e.g. ``Rotation(-θ)``).
        """
        inv = np.linalg.inv(self._matrix)
        return LinearMap(inv)

    # ------------------------------------------------------------------
    # Numerical predicates
    # ------------------------------------------------------------------
    def is_orthogonal(self, *, tol: float = 1e-12) -> bool:
        """Whether the matrix is orthogonal (``M Mᵀ = I``).

        Theorem 1 of the thesis characterizes angle-preserving maps under
        the unit-vector hypothesis by orthogonality; this is the numerical
        counterpart.
        """
        m = self._matrix
        product = m @ m.T
        return bool(np.allclose(product, np.eye(2), atol=tol))

    def preserves_angles(
        self,
        *,
        n_samples: int = 64,
        seed: int = 20151217,
        tol: float = 1e-10,
    ) -> bool:
        """Numerically verify angle preservation on random vector pairs.

        Samples ``n_samples`` pairs of nonzero vectors uniformly from a
        standard normal distribution and checks that

            cos(angle(x, y)) ≈ cos(angle(M x, M y))

        within tolerance ``tol``. This is the direct numerical check of
        Definition 1 of the thesis.

        Parameters
        ----------
        n_samples : int, default 64
            Number of random vector pairs to test.
        seed : int, default 20151217
            RNG seed for reproducibility (set to the date of the thesis
            defense by tradition).
        tol : float, default 1e-10
            Absolute tolerance for the cosine comparison.

        Returns
        -------
        bool
            ``True`` iff all sampled pairs satisfy the angle-preservation
            condition.
        """
        rng = np.random.default_rng(seed)
        for _ in range(n_samples):
            x = rng.normal(size=2)
            y = rng.normal(size=2)
            nx = float(np.linalg.norm(x))
            ny = float(np.linalg.norm(y))
            if nx < 1e-12 or ny < 1e-12:
                continue
            tx = self._matrix @ x
            ty = self._matrix @ y
            ntx = float(np.linalg.norm(tx))
            nty = float(np.linalg.norm(ty))
            if ntx < 1e-12 or nty < 1e-12:
                return False
            cos_xy = float(x @ y) / (nx * ny)
            cos_txty = float(tx @ ty) / (ntx * nty)
            if not np.isclose(cos_xy, cos_txty, atol=tol):
                return False
        return True

    def equals(self, other: LinearMap, *, tol: float = 1e-12) -> bool:
        """Test equality of two linear maps element-wise within tolerance."""
        return bool(np.allclose(self._matrix, other._matrix, atol=tol))

    def is_identity(self, *, tol: float = 1e-12) -> bool:
        """Whether this map is (numerically) the identity."""
        return bool(np.allclose(self._matrix, np.eye(2), atol=tol))

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        """Return a developer-facing debug string."""
        m = self._matrix
        rows = ", ".join(f"[{m[i, 0]:.4g}, {m[i, 1]:.4g}]" for i in range(2))
        return f"LinearMap([{rows}])"
