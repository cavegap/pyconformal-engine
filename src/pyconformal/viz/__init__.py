"""Visualization helpers and orthogonal grids (Chapter 4 of the thesis).

Use :func:`apply_conformal_to_rectangle` to sample a rectangular grid
and evaluate a complex map on the sampled lines.

References
----------
Vega Penagos & Olivero Zapata (2015), Chapter 4, Figures 4.1–4.5.
Maple source files: ``algo.mw``, ``proceso.mw``, ``mapeo luna.mw``.
"""

from __future__ import annotations

from collections.abc import Callable
from math import isfinite
from typing import NamedTuple

import numpy as np
from numpy.typing import NDArray

__all__ = ["MappedRectangleGrid", "apply_conformal_to_rectangle"]

ComplexGrid = NDArray[np.complex128]


class MappedRectangleGrid(NamedTuple):
    """Source and image curves, with one sampled line per row."""

    horizontal: ComplexGrid
    vertical: ComplexGrid
    mapped_horizontal: ComplexGrid
    mapped_vertical: ComplexGrid


def apply_conformal_to_rectangle(
    mapping: Callable[[ComplexGrid], ComplexGrid],
    lower_left: complex,
    upper_right: complex,
    n_real: int,
    n_imag: int,
    *,
    samples: int = 241,
) -> MappedRectangleGrid:
    """Evaluate a vectorized complex map on an axis-aligned rectangular grid.

    The grid includes all four sides. ``n_real`` counts vertical lines,
    ``n_imag`` counts horizontal lines, and ``samples`` counts points per line.
    The callable receives a two-dimensional complex array for each family
    of lines and must return the same shape. Nonfinite image values are
    retained so plotting callers can represent poles as breaks.

    References
    ----------
    Vega Penagos & Olivero Zapata (2015), §4.1, Figure 4.1.
    """
    bounds = (lower_left.real, lower_left.imag, upper_right.real, upper_right.imag)
    if not all(map(isfinite, bounds)) or not (
        lower_left.real < upper_right.real and lower_left.imag < upper_right.imag
    ):
        raise ValueError("Expected finite lower-left and upper-right corners of a rectangle.")
    if min(n_real, n_imag, samples) < 2:
        raise ValueError("Each grid direction and each line need at least two samples.")

    x = np.linspace(lower_left.real, upper_right.real, samples)
    y = np.linspace(lower_left.imag, upper_right.imag, samples)
    real_lines = np.linspace(lower_left.real, upper_right.real, n_real)
    imag_lines = np.linspace(lower_left.imag, upper_right.imag, n_imag)
    horizontal = x[None, :] + 1j * imag_lines[:, None]
    vertical = real_lines[:, None] + 1j * y[None, :]
    mapped_horizontal = np.asarray(mapping(horizontal), dtype=np.complex128)
    mapped_vertical = np.asarray(mapping(vertical), dtype=np.complex128)
    if mapped_horizontal.shape != horizontal.shape or mapped_vertical.shape != vertical.shape:
        raise ValueError("The map must return an array with the same shape as its input.")
    return MappedRectangleGrid(horizontal, vertical, mapped_horizontal, mapped_vertical)
