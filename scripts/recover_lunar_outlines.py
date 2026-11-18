"""Recover the plotted paths and register the archival lunar frame."""

import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, map_coordinates
from scipy.optimize import minimize
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parents[1]
FIGURE_PAGE = 57
ARCHIVAL_CROP = (1053, 198, 2036, 675)


def read_panels(svg: Path) -> tuple[list[np.ndarray], list[np.ndarray]]:
    """Extract colored fill paths and calibrate both coordinate grids."""
    left, right = [], []
    for path in ET.parse(svg).getroot().iter():
        fill = path.get("fill", "")
        if not fill.startswith(("rgb(0%, 0%, 54.", "rgb(66.209412%")):
            continue
        commands = path.get("d", "")
        if len(commands) < 30 or re.search(r"[CQAHV]", commands):
            continue
        values = np.array(re.findall(r"-?\d+(?:\.\d+)?", commands), dtype=float).reshape(-1, 2)
        x, y = values[0]
        if 158 <= x <= 296 and 499 <= y <= 568:
            left.append(values)
        if 323 <= x <= 457 and 480 <= y <= 588:
            right.append(values)

    # SVG positions of labeled ticks. The right panel uses the 0 and 20 ticks.
    left_x = (158.3085938, 294.28125)
    left_y = (567.6679688, 499.8671875)
    right_x = (349.67578125, 364.4375)
    right_y = (586.8671875, 572.1171875)
    for panel, (x0, x1), (y0, y1), xmax, ymax in (
        (left, left_x, left_y, 12, 6),
        (right, right_x, right_y, 20, 20),
    ):
        for points in panel:
            points[:, 0] = (points[:, 0] - x0) * xmax / (x1 - x0)
            points[:, 1] = (points[:, 1] - y0) * ymax / (y1 - y0)
    if len(left) != 21 or len(right) != 21:
        raise ValueError("Expected the 21 colored paths in each panel of Figure 4.5.")
    return left, right


def compare_power(source: np.ndarray, published: np.ndarray, power: int) -> dict[str, float]:
    """Measure published-to-mapped vertex distances despite differing path sampling."""
    mapped = (source[:, 0] + 1j * source[:, 1]) ** power
    tree = cKDTree(np.column_stack((mapped.real, mapped.imag)))
    distance, _ = tree.query(published)
    return {"median": float(np.median(distance)), "p95": float(np.percentile(distance, 95))}


def register_frame(image: Path) -> dict[str, float]:
    """Fit a spherical Mercator frame by image correlation with the LROC mosaic."""
    with Image.open(image) as archival:
        crop = archival.crop(ARCHIVAL_CROP).convert("L").resize((246, 119))
    historic = np.asarray(crop, dtype=float)
    modern = np.asarray(plt.imread(ROOT / "examples" / "lunar-global-wac.jpg"), dtype=float)
    x, y = np.meshgrid((np.arange(246) + 0.5) / 246, 1 - (np.arange(119) + 0.5) / 119)
    use = (x > 0.06) & (x < 0.94) & (y > 0.10) & (y < 0.89)
    reference = gaussian_filter(historic, 2)[use]

    def objective(bounds: np.ndarray) -> float:
        west, east, north = bounds
        longitude = west + (east - west) * x
        mercator_y = np.arcsinh(np.tan(np.deg2rad(north))) * y
        latitude = np.rad2deg(np.arctan(np.sinh(mercator_y)))
        sampled = map_coordinates(
            modern,
            [(90 - latitude) * 5 - 0.5, (longitude + 180) * 5 - 0.5],
            order=1,
            mode="nearest",
        )
        return -float(np.corrcoef(reference, gaussian_filter(sampled, 2)[use])[0, 1])

    fit = minimize(objective, [-60, 60, 60], method="Nelder-Mead", options={"maxiter": 600})
    if not fit.success:
        raise RuntimeError("Archival image registration did not converge.")
    west, east, north = fit.x
    return {
        "west": round(float(west), 4),
        "east": round(float(east), 4),
        "south": 0.0,
        "north": round(float(north), 4),
        "image_correlation": round(float(-fit.fun), 4),
    }


def main() -> None:
    """Extract the figure vectors and save the audit as reproducible JSON."""
    pdf = ROOT / "thesis" / "IMPLEMENTACION_EN_SOFTWARE_DE_APLICACIONES_CONFORMES.pdf"
    page = str(FIGURE_PAGE)
    with TemporaryDirectory() as temporary:
        svg = Path(temporary) / "page.svg"
        jpeg = Path(temporary) / "archival"
        subprocess.run(["pdftocairo", "-f", page, "-l", page, "-svg", pdf, svg], check=True)
        subprocess.run(["pdfimages", "-f", page, "-l", page, "-j", pdf, jpeg], check=True)
        left, right = read_panels(svg)
        registration = register_frame(jpeg.with_name("archival-000.jpg"))
    comparison = {
        str(power): compare_power(np.concatenate(left), np.concatenate(right), power)
        for power in (2, 3)
    }
    paths = [np.round(np.clip(points, [0, 0], [12, 6]), 6).tolist() for points in left]
    metadata = {
        "source": "Figure 4.5, p. 57, Vega Penagos & Olivero Zapata (2015)",
        "path_order": "blue outline first, then the 20 published gray paths",
        "comparison": comparison,
        "registration": registration,
        "paths": paths,
    }
    output = json.dumps(metadata, indent=2) + "\n"
    (ROOT / "examples" / "lunar-thesis-outlines.json").write_text(output, encoding="utf-8")
    print(f"21 outlines recovered. Residuals: {comparison}. Registration: {registration}")


if __name__ == "__main__":
    main()
