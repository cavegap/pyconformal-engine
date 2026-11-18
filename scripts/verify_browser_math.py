"""Compare the shared offline JavaScript maps against Python reference values."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
from scipy.special import elliprf

from pyconformal.cartography import peirce_quincuncial
from pyconformal.sc import upper_half_plane_to_square


def main() -> None:
    """Run JavaScript with Node; compare coordinates and an independent scale."""
    node = shutil.which("node")
    if node is None:
        raise SystemExit(
            "Node.js is needed for this maintainer check; reader_checks.py needs only Python."
        )
    here = Path(__file__).resolve().parents[1] / "examples"
    square_samples = [[x, y] for x in (-3, -1, -0.7, 0, 0.4, 1, 3) for y in (0, 1e-6, 0.1, 0.7, 2)]
    geographic = [
        [lon, lat]
        for lon in range(-180, 180, 15)
        for lat in (-90, -75, -30, -1e-6, 0, 1e-6, 30, 75, 90)
    ]
    scale_samples = [[12, 25], [78, -62], [-111, 64], [-135, -28]]
    payload = {
        "sources": [
            (here / name).read_text(encoding="utf-8") for name in ("sc-square.js", "peirce-map.js")
        ],
        "square": [*square_samples, None],
        "geographic": geographic,
        "scales": scale_samples,
    }
    program = """
const fs = require('node:fs'), vm = require('node:vm');
const data = JSON.parse(fs.readFileSync(0,'utf8')); global.window = global;
for(const source of data.sources) vm.runInThisContext(source);
process.stdout.write(JSON.stringify({
  square: data.square.map(SCSquare.map),
  peirce: data.geographic.map(([lon,lat])=>PeirceMap.project(lon,lat)),
  scales: data.scales.map(([lon,lat])=>PeirceMap.relativeScale(lon,lat))
}));
"""
    run = subprocess.run(
        [node, "--eval", program],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=True,
        timeout=30,
    )
    actual = json.loads(run.stdout)
    expected_square = [upper_half_plane_to_square(complex(x, y)) for x, y in square_samples]
    expected_square.append(1 + 1j)
    expected_peirce = [peirce_quincuncial(lon, lat) for lon, lat in geographic]
    for label, key, expected in (
        ("SC square", "square", expected_square),
        ("Peirce", "peirce", expected_peirce),
    ):
        a = np.asarray(actual[key])
        target = np.array([[p.real, p.imag] for p in expected])
        error = float(np.max(np.abs(a - target)))
        print(f"{label}: {len(expected)} samples, max coordinate error {error:.3e}")
        if error > 1e-9:
            raise SystemExit(f"{label} differs from Python by more than 1e-9.")
    expected_scales = []
    step = 1e-4
    pole_scale = 1 / (2 * float(elliprf(0, 1, 2)))
    for lon, lat in scale_samples:
        displacement = peirce_quincuncial(lon, lat + step) - peirce_quincuncial(lon, lat - step)
        expected_scales.append(abs(displacement) / np.deg2rad(2 * step) / pole_scale)
    relative_error = float(np.max(np.abs(np.asarray(actual["scales"]) / expected_scales - 1)))
    print(
        f"Relative scale: 4 meridian-derivative references, max relative error {relative_error:.3e}"
    )
    if relative_error > 1e-7:
        raise SystemExit("Browser scale differs from the meridian derivative by more than 1e-7.")


if __name__ == "__main__":
    main()
