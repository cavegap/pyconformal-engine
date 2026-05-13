"""Shared pytest fixtures and configuration.

Add reusable fixtures here as the library grows. Keeping fixtures centralized
prevents duplication across test files and makes it easier to update the
default numerical tolerances in one place.
"""

from __future__ import annotations

import numpy as np
import pytest


@pytest.fixture
def rng() -> np.random.Generator:
    """A deterministic random generator for reproducible tests."""
    return np.random.default_rng(seed=20151217)  # date of thesis defense


@pytest.fixture
def tol() -> float:
    """Default numerical tolerance for floating-point comparisons."""
    return 1e-12
