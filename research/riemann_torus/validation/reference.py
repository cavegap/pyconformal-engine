"""Independent 70-digit Jacobi reference for the browser theta implementation."""

import json
from pathlib import Path

import mpmath as mp

mp.mp.dps = 70
K = mp.ellipk(mp.mpf("0.5"))
points = [(a, b) for a in [0.07, 0.21, 0.37, 0.49, 0.71, 0.93] for b in [0.09, 0.28, 0.47, 0.76]]
points += [(0.5, 0), (0, 0.5), (0.5, 0.5), (0, 0), (1e-7, 2e-7), (0.9999999, 0.9999998)]
rows = []
for a, b in points:
    z = mp.mpc(mp.mpf(a), mp.mpf(b))  # Preserve the exact binary inputs used by JavaScript.
    if a == b == 0:
        value = None
        sphere = [0, 0, 1]
    else:
        sn = mp.ellipfun("sn", 2 * K * z, mp.mpf(".5"))
        w = 2 / sn**2 - 1
        value = [float(mp.re(w)), float(mp.im(w))]
        d = 1 + abs(w) ** 2
        sphere = [float(2 * mp.re(w) / d), float(2 * mp.im(w) / d), float((abs(w) ** 2 - 1) / d)]
    rows.append({"z": [a, b], "value": value, "sphere": sphere})
root = Path(__file__).parent
(root / "references.json").write_text(
    json.dumps({"precision_digits": 70, "K": str(K), "rows": rows}, indent=2) + "\n",
    encoding="utf-8",
)
