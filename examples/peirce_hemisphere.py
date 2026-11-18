"""Render a lunar graticule on the disk and the Peirce hemisphere square."""

from argparse import ArgumentParser
from collections.abc import Callable
from math import sqrt
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patheffects
from scipy.special import elliprf

from pyconformal.cartography import north_hemisphere_to_square, stereographic_north_disk

LANDMARKS = (
    ("Aristarchus", -47.49, 23.73, "#9a4b35"),
    ("Plato", -9.38, 51.62, "#23695d"),
    ("Jackson", -163.32, 22.05, "#725487"),
)


def render() -> None:
    """Draw a common lunar graticule and three named craters in both planes."""
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 6.8), layout="constrained")
    grid: list[tuple[Callable[[float, float], complex], str]] = [
        (stereographic_north_disk, "Stereographic disk"),
        (north_hemisphere_to_square, "Peirce hemisphere square"),
    ]
    longitude_samples = np.linspace(-180, 180, 361)
    latitude_samples = np.linspace(0, 90, 181)
    for ax, (project, title) in zip(axes, grid, strict=True):
        for latitude in (15, 30, 45, 60, 75):
            curve = np.array([project(float(lon), latitude) for lon in longitude_samples])
            ax.plot(curve.real, curve.imag, color="#287c70", alpha=0.8, linewidth=1.1)
        for longitude in range(-180, 180, 15):
            curve = np.array([project(longitude, float(lat)) for lat in latitude_samples])
            color = "#9b6245" if longitude % 90 == 0 else "#c09b86"
            ax.plot(
                curve.real, curve.imag, color=color, linewidth=0.9 if longitude % 90 == 0 else 0.55
            )
        equator = np.array([project(float(lon), 0) for lon in longitude_samples])
        ax.plot(equator.real, equator.imag, color="#264b58", linewidth=1.55)
        for longitude, label in ((45, "45°E"), (135, "135°E"), (-135, "135°W"), (-45, "45°W")):
            point = project(longitude, 0)
            ax.scatter(point.real, point.imag, s=24, color="#264b58", zorder=3)
            ax.annotate(
                label,
                (point.real, point.imag),
                xytext=(
                    7 if point.real > 0.05 else -7 if point.real < -0.05 else 0,
                    7 if point.imag >= 0 else -8,
                ),
                textcoords="offset points",
                ha="left" if point.real > 0.05 else "right" if point.real < -0.05 else "center",
                va="bottom" if point.imag >= 0 else "top",
                color="#264b58",
                fontsize=8,
            )
        for name, longitude, latitude, color in LANDMARKS:
            point = project(longitude, latitude)
            ax.scatter(
                point.real,
                point.imag,
                s=72,
                color=color,
                edgecolor="white",
                linewidth=1.7,
                zorder=4,
            )
            label = ax.annotate(
                name,
                (point.real, point.imag),
                xytext=(9, -15),
                textcoords="offset points",
                color=color,
                fontsize=10,
                fontweight="bold",
                bbox={"facecolor": "white", "edgecolor": color, "alpha": 0.92, "pad": 2.5},
                arrowprops={"arrowstyle": "-", "color": color},
            )
            label.set_path_effects([patheffects.withStroke(linewidth=2.5, foreground="white")])
        ax.scatter(0, 0, s=29, color="#264b58", zorder=4)
        pole = ax.annotate(
            "North pole",
            (0, 0),
            xytext=(6, 5),
            textcoords="offset points",
            color="#264b58",
            fontsize=8.5,
        )
        pole.set_path_effects([patheffects.withStroke(linewidth=2.5, foreground="white")])
        ax.set_title(title, color="#193746", fontweight="bold", fontsize=12)
        ax.set(xlim=(-1.26, 1.26), ylim=(-1.23, 1.23), aspect="equal")
        ax.set_axis_off()
    fig.suptitle("Lunar northern hemisphere", fontsize=17, color="#193746", fontweight="bold")
    fig.supxlabel(
        "Sphere → disk → upper half-plane → square\n"
        "ζ = tan(π/4 - φ/2) exp[i(λ + π/4)];  p = i(1 - ζ)/(1 + ζ)\n"
        "w = 1 + i - (2i/κ) RF(p + 1, p, p - 1),  κ = RF(0, 1, 2)\n"
        "φ: latitude; λ: east longitude (radians). Same crater centers in both views. "
        "See peirce-hemisphere.md for corner limits.\n"
        "Green: parallels. Brown: meridians. Dark rim: equator.",
        color="#254653",
        fontsize=8.5,
        linespacing=1.6,
    )
    fig.savefig(Path(__file__).with_suffix(".png"), dpi=180)
    plt.close(fig)


def compare_proj() -> None:
    """Print coordinate differences against the optional PROJ reference."""
    try:
        import pyproj
    except ImportError as error:
        raise SystemExit("Install pyproj to run the optional reference comparison.") from error
    projection = pyproj.Proj("+proj=peirce_q +shape=nhemisphere +lon_0=0 +R=1")
    scale = sqrt(2) * float(elliprf(0, 1, 2))
    samples = [(lon, lat) for lon in range(-180, 180, 15) for lat in (0, 8, 20, 35, 50, 65, 80, 90)]
    errors = [
        abs(north_hemisphere_to_square(lon, lat) - complex(*projection(lon, lat)) / scale)
        for lon, lat in samples
    ]
    print(f"PROJ {pyproj.proj_version_str}: {len(samples)} points, max error {max(errors):.3e}")


def main() -> None:
    """Generate the graticule and optionally run the PROJ comparison."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--compare-proj", action="store_true")
    options = parser.parse_args()
    render()
    if options.compare_proj:
        compare_proj()


if __name__ == "__main__":
    main()
