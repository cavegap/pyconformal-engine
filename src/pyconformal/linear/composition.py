r"""Composition of elements of group P: dispatch for the seven cases of Theorem 6.

The thesis proves closure of group P under composition by enumerating seven
cases (pp. 16–17). For each ordered pair of generators :math:`(a, b)` with
:math:`a, b \in \{R, \mathrm{Ref}, D\}`, the composition ``a ∘ b`` is shown
to be again of a recognizable form. This module implements that dispatch in
code: each pure case returns the most specific subclass possible
(:class:`Rotation`, :class:`Reflection`, :class:`Dilation`), and mixed
compositions involving a non-trivial scale fall through to a generic
:class:`LinearMap`.

General composition formulas (for arbitrary parameters, derived from the
matrix products):

* :math:`R(\alpha) \circ R(\beta) = R(\alpha + \beta)`
* :math:`D(\lambda) \circ D(\mu) = D(\lambda \mu)`
* :math:`\mathrm{Ref}(\alpha) \circ \mathrm{Ref}(\beta) = R(\alpha - \beta)`
* :math:`R(\alpha) \circ \mathrm{Ref}(\beta) = \mathrm{Ref}(\alpha + \beta)`
* :math:`\mathrm{Ref}(\alpha) \circ R(\beta) = \mathrm{Ref}(\alpha - \beta)`
* :math:`D(\lambda) \circ R(\beta)` is a generic scaled rotation
* :math:`D(\lambda) \circ \mathrm{Ref}(\beta)` is a generic scaled reflection
* Dilations commute with rotations and reflections.

The seven enumerated cases in the thesis use the *same* angle ``θ`` for both
factors, which is a notational simplification of the closure proof; here we
implement the general formulas, which obviously specialize to the thesis's
cases when ``α = β``.

References
----------
Vega Penagos & Olivero Zapata (2015), Theorem 6, pp. 16–17.
"""

from __future__ import annotations

from .base import LinearMap
from .generators import Dilation, Reflection, Rotation


def compose(a: LinearMap, b: LinearMap) -> LinearMap:
    """Return ``a ∘ b`` as the most specific subclass possible.

    Parameters
    ----------
    a, b : LinearMap
        Two elements of group P.

    Returns
    -------
    LinearMap
        The composition. When ``a`` and ``b`` are both pure generators
        (rotation, reflection, or dilation), the result is returned as the
        most specific subclass; otherwise, a generic :class:`LinearMap` is
        returned. The matrix of the result is always ``a.matrix @ b.matrix``.

    Notes
    -----
    This function implements the seven-case dispatch of Theorem 6 of the
    thesis. It is invoked via the ``@`` operator (``a @ b``) on instances.
    """
    # --- Case 1: Rotation ∘ Rotation = Rotation(sum of angles) -------------
    if isinstance(a, Rotation) and isinstance(b, Rotation):
        return Rotation(a.theta + b.theta)

    # --- Case 3: Dilation ∘ Dilation = Dilation(product of factors) --------
    if isinstance(a, Dilation) and isinstance(b, Dilation):
        return Dilation(a.lambda_ * b.lambda_)

    # --- Case 2: Reflection ∘ Reflection = Rotation(α - β) -----------------
    if isinstance(a, Reflection) and isinstance(b, Reflection):
        return Rotation(a.theta - b.theta)

    # --- Case 4: Rotation ∘ Reflection = Reflection(α + β) -----------------
    if isinstance(a, Rotation) and isinstance(b, Reflection):
        return Reflection(a.theta + b.theta)

    # --- Case 5: Reflection ∘ Rotation = Reflection(α - β) -----------------
    if isinstance(a, Reflection) and isinstance(b, Rotation):
        return Reflection(a.theta - b.theta)

    # --- Cases 6, 7: Dilation commutes with Rotation; trivial dilations
    # collapse to the rotation/reflection alone.
    if isinstance(a, Dilation) and isinstance(b, Rotation):
        if a.lambda_ == 1.0:
            return Rotation(b.theta)
        if a.lambda_ == -1.0:
            return Rotation(b.theta + _PI)
        # otherwise: scaled rotation, no pure type captures it
        return LinearMap(a.matrix @ b.matrix)

    if isinstance(a, Rotation) and isinstance(b, Dilation):
        if b.lambda_ == 1.0:
            return Rotation(a.theta)
        if b.lambda_ == -1.0:
            return Rotation(a.theta + _PI)
        return LinearMap(a.matrix @ b.matrix)

    # --- Final pair from Theorem 6 prose: Dilation × Reflection ------------
    if isinstance(a, Dilation) and isinstance(b, Reflection):
        if a.lambda_ == 1.0:
            return Reflection(b.theta)
        if a.lambda_ == -1.0:
            # -I commutes; (-I) Ref(β) is also a reflection (different axis)
            return LinearMap(a.matrix @ b.matrix)
        return LinearMap(a.matrix @ b.matrix)

    if isinstance(a, Reflection) and isinstance(b, Dilation):
        if b.lambda_ == 1.0:
            return Reflection(a.theta)
        return LinearMap(a.matrix @ b.matrix)

    # --- Fallback: any other LinearMap × LinearMap ------------------------
    return LinearMap(a.matrix @ b.matrix)


# Module-level constant for the case `λ = -1` shortcut above.
import math as _math  # noqa: E402

_PI = _math.pi
