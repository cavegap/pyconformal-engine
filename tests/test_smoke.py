"""Smoke tests: verify that the package and its submodules import cleanly.

These tests do not exercise any mathematical functionality — they exist so
that the CI pipeline has something to run from day one, and so that any
catastrophic packaging mistake (broken ``__init__``, missing dependency,
incorrect ``src/`` layout) is caught immediately on push.
"""

from __future__ import annotations

import importlib

import pytest

SUBMODULES = [
    "pyconformal",
    "pyconformal.linear",
    "pyconformal.core",
    "pyconformal.mobius",
    "pyconformal.elementary",
    "pyconformal.sc",
    "pyconformal.viz",
    "pyconformal.examples",
]


@pytest.mark.parametrize("module_name", SUBMODULES)
def test_submodule_imports(module_name: str) -> None:
    """Every declared submodule must import without error."""
    module = importlib.import_module(module_name)
    assert module is not None


def test_package_version() -> None:
    """The package exposes a non-empty ``__version__`` string."""
    import pyconformal

    assert isinstance(pyconformal.__version__, str)
    assert len(pyconformal.__version__) > 0


def test_numpy_available() -> None:
    """NumPy is a hard dependency and must be importable."""
    import numpy as np

    arr = np.array([1.0 + 2.0j, 3.0 - 4.0j])
    assert arr.dtype == np.complex128


def test_scipy_available() -> None:
    """SciPy is a hard dependency and must be importable."""
    import scipy  # noqa: F401
    from scipy import integrate  # noqa: F401
