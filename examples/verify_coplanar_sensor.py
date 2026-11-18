"""Verify the coplanar sensor via a logarithmic boundary-element model."""

import numpy as np
from numpy.typing import NDArray
from scipy.constants import epsilon_0

from pyconformal.sc import coplanar_sensor_capacitance

FloatGrid = NDArray[np.float64]


def log_primitive(offset: FloatGrid) -> FloatGrid:
    """Integrate log|offset| with the continuous zero-offset limit."""
    magnitude = np.where(offset == 0, 1.0, np.abs(offset))
    return np.asarray(offset * (np.log(magnitude) - 1), dtype=np.float64)


def boundary_element_capacitance(gap_ratio: float, panels: int) -> float:
    """Compute the capacitance per length in air for a unit-width strip pair."""
    a = gap_ratio / 2
    edges = a + (1 - np.cos(np.linspace(0, np.pi, panels + 1))) / 2
    start, end = edges[:-1], edges[1:]
    collocation = ((start + end) / 2)[:, None]
    # Antisymmetric charge on the negative electrode gives the log ratio.
    mirror = log_primitive(collocation + end) - log_primitive(collocation + start)
    direct = log_primitive(end - collocation) - log_primitive(start - collocation)
    # Unknown charge densities are normalized by epsilon_0. Voltage is +0.5 V.
    density = np.linalg.solve((mirror - direct) / (2 * np.pi), np.full(panels, 0.5))
    return float(epsilon_0) * float(density @ (end - start))


def main() -> None:
    """Print the maximum relative difference at each panel count."""
    ratios = (0.1, 0.25, 0.5, 1.0, 2.0)
    for panels in (24, 48, 96, 192):
        errors = [
            abs(
                boundary_element_capacitance(ratio, panels) / coplanar_sensor_capacitance(1, ratio)
                - 1
            )
            for ratio in ratios
        ]
        print(f"{panels:3d} panels per strip   maximum relative difference {max(errors):.3e}")


if __name__ == "__main__":
    main()
