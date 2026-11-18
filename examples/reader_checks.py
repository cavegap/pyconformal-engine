"""Run numerical checkpoints for docs/exercises.md alongside the 2015 thesis."""

from __future__ import annotations

import cmath
import json
import math
from argparse import ArgumentParser
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from numpy.typing import ArrayLike

from pyconformal.cartography import peirce_quincuncial, peirce_quincuncial_inverse
from pyconformal.linear import Dilation, Reflection, Rotation
from pyconformal.mobius import disk_to_upper_half_plane
from pyconformal.sc import (
    coplanar_sensor_capacitance,
    coplanar_waveguide,
    gap_for_impedance,
    square_heat_temperature,
    upper_half_plane_to_square,
)


@dataclass(frozen=True)
class Checkpoint:
    """One named numerical consequence of a reader exercise."""

    exercise: str
    label: str
    error: float
    tolerance: float
    passed: bool


def run_checks() -> list[Checkpoint]:
    """Evaluate the documented reference cases without browser dependencies."""
    results: list[Checkpoint] = []

    def record(
        exercise: str, label: str, actual: ArrayLike, expected: ArrayLike, tolerance: float = 1e-11
    ) -> None:
        a = np.asarray(actual, dtype=np.complex128)
        b = np.asarray(expected, dtype=np.complex128)
        error = float(np.max(np.abs(a - b))) if a.shape == b.shape else math.inf
        results.append(
            Checkpoint(
                exercise, label, error, tolerance, math.isfinite(error) and error <= tolerance
            )
        )

    x, y = np.array([1.0, 0.0]), np.array([1.0, 1.0])
    for transform in (Rotation(math.pi / 3), Reflection(math.pi / 3), Dilation(-2)):
        a, b = transform.matrix @ x, transform.matrix @ y
        cosine = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
        record("E1", f"{transform}: unsigned angle", math.acos(cosine), math.pi / 4)
    record("E1", "negative dilation preserves orientation", Dilation(-2).det, 4)
    z0 = 0.5 + 0.5j
    record("E2", "tangent scale at (1+i)/2", abs(2 * z0), math.sqrt(2))
    record("E2", "tangent rotation at (1+i)/2", cmath.phase(2 * z0), math.pi / 4)
    t2 = cmath.exp(1j * math.pi / 3)
    record(
        "E2",
        "common derivative preserves opening",
        cmath.phase((2 * z0 * t2) / (2 * z0)),
        math.pi / 3,
    )
    record("E2", "outgoing square rays at zero", cmath.phase(t2**2), 2 * math.pi / 3)
    for z, expected in ((0j, 1j), (1j, 1), (-1j, -1), (1 + 0j, 0)):
        record("E3", f"Cayley({z})", disk_to_upper_half_plane(z), expected)
    z = 0.2 + 0.3j
    w = disk_to_upper_half_plane(z)
    record("E3", "inverse Cayley", (1j - w) / (1j + w), z)
    record("E4", "roof vertex survives principal Log", cmath.log(cmath.exp(1j)), 1j)
    record("E4", "branch outside strip", cmath.log(cmath.exp(4j)), (4 - 2 * math.pi) * 1j)
    record("E4", "log local scale", abs(1 / cmath.exp(0.65 + 0.35j)), math.exp(-0.65))
    prevertices = (-1 + 0j, 0j, 1 + 0j, complex(math.inf), 1j)
    for z, expected in zip(prevertices, (-1 + 1j, -1 - 1j, 1 - 1j, 1 + 1j, 0j), strict=True):
        record("E5", f"SC({z})", upper_half_plane_to_square(z), expected)
    for z, expected in zip(prevertices, (20, 100, 20, 100, 60), strict=True):
        record("E6", f"temperature at {z}", square_heat_temperature(z), expected)
    gap = gap_for_impedance(width=1, impedance_ohm=50, eps_r=4)
    record("E7", "50 ohm gap in mm", gap, 0.258344, 1e-6)
    record(
        "E7", "50 ohm design", coplanar_waveguide(width=1, gap=gap, eps_r=4).impedance_ohm, 50, 1e-8
    )
    sensor = coplanar_sensor_capacitance(width=1, gap=0.25, eps_r=3) * 0.02
    record("E7", "sensor capacitance in pF", sensor * 1e12, 1.211, 0.001)
    record(
        "E7",
        "doubling permittivity",
        coplanar_sensor_capacitance(width=1, gap=0.25, eps_r=6) * 0.02 / sensor,
        2,
    )
    record("E8", "cubic length scale", abs(3 * (1 + 1j) ** 2), 6)
    record("E8", "cubic area scale", abs(3 * (1 + 1j) ** 2) ** 2, 36)
    record("E9", "north pole", peirce_quincuncial(0, 90), 0j)
    record(
        "E9",
        "four south-pole copies",
        [peirce_quincuncial(lon, -90) for lon in (0, 90, 180, -90)],
        [1 - 1j, 1 + 1j, -1 + 1j, -1 - 1j],
    )
    lon, lat = peirce_quincuncial_inverse(np.array([1 + 0.4j, 1 - 0.4j]))
    record("E9", "paired cut copies", [lon[0] - lon[1], lat[0] - lat[1]], [0, 0])
    archive = json.loads(
        Path(__file__).with_name("lunar-thesis-outlines.json").read_text(encoding="utf-8")
    )
    record("E10", "archived contour count", len(archive["paths"]), 21, 0)
    record(
        "E10",
        "archived squared-fit median",
        archive["comparison"]["2"]["median"],
        0.005970467892381027,
    )
    record(
        "E10", "archived cubic-fit median", archive["comparison"]["3"]["median"], 11.474637497876712
    )
    return results


def main() -> None:
    """Print checkpoints, optionally selecting one exercise or JSON output."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--exercise", choices=[f"E{i}" for i in range(1, 11)])
    parser.add_argument("--json", action="store_true", help="print a machine-readable report")
    options = parser.parse_args()
    results = [
        r for r in run_checks() if options.exercise is None or r.exercise == options.exercise
    ]
    if options.json:
        print(json.dumps([asdict(r) for r in results], indent=2, allow_nan=False))
    else:
        for r in results:
            print(
                f"{'PASS' if r.passed else 'FAIL'} {r.exercise} {r.label}: "
                f"error={r.error:.3g}, tolerance={r.tolerance:.3g}"
            )
        print(f"{sum(r.passed for r in results)}/{len(results)} numerical checkpoints passed.")
    if not all(r.passed for r in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
