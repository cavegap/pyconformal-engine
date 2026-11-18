"""Render the lunar graticule in Peirce's global quincuncial square."""

from argparse import ArgumentParser
from itertools import pairwise
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patheffects
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon
from scipy.special import elliprf

from pyconformal.cartography import peirce_quincuncial

LANDMARKS = (
    ("Copernicus", -20.08, 9.62, (6, 7)),
    ("Jackson", -163.32, 22.05, (-7, 7)),
    ("Tycho", -11.22, -43.30, (-8, -10)),
    ("Tsiolkovskiy", 128.97, -20.38, (8, 7)),
)
MERIDIAN_CUTS = (-135, -45, 45, 135, 225)


def render() -> None:
    """Draw both hemispheres, both sides of the cuts and four pole copies."""
    fig, ax = plt.subplots(figsize=(8.3, 8.3), layout="constrained")
    ax.set_aspect("equal")
    ax.set(xlim=(-1.19, 1.19), ylim=(-1.16, 1.16))
    ax.set_axis_off()
    ax.add_patch(Polygon([(-1, -1), (1, -1), (1, 1), (-1, 1)], facecolor="#fcf1e9"))
    ax.add_patch(Polygon([(0, -1), (1, 0), (0, 1), (-1, 0)], facecolor="#edf6f1"))

    def draw_line(points: list[complex], color: str, thickness: float = 0.72) -> None:
        curve = np.asarray(points, dtype=np.complex128)
        ax.plot(curve.real, curve.imag, color=color, linewidth=thickness)

    lon_samples = [-180 + i for i in range(361)]
    for lat in (15, 30, 45, 60, 75):
        draw_line([peirce_quincuncial(lon, lat) for lon in lon_samples], "#558e80")

    # Separate paths at each duplicated cut so plotting cannot join opposite edges.
    cut_padding = 1e-8
    for left, right in pairwise(MERIDIAN_CUTS):
        for lat in (-15, -30, -45, -60, -75):
            samples = np.linspace(left + cut_padding, right - cut_padding, 121)
            draw_line([peirce_quincuncial(float(lon), lat) for lon in samples], "#558e80")

    for lon in range(-180, 180, 15):
        draw_line([peirce_quincuncial(lon, lat) for lat in range(91)], "#bb8269")
        if lon % 90 != 45:
            draw_line([peirce_quincuncial(lon, -lat) for lat in range(91)], "#bb8269")
    equator = [peirce_quincuncial(lon, 0) for lon in lon_samples]
    draw_line(equator, "#224653", 1.45)
    outer = [-1 - 1j, 1 - 1j, 1 + 1j, -1 + 1j, -1 - 1j]
    draw_line(outer, "#224653", 1.45)

    for meridian, label in ((45, "45°E"), (135, "135°E"), (-135, "135°W"), (-45, "45°W")):
        point = peirce_quincuncial(meridian, 0)
        ax.scatter(point.real, point.imag, marker="s", s=24, color="#224653", zorder=3)
        ax.annotate(
            label,
            (point.real, point.imag),
            xytext=(9 * round(point.real), 9 * round(point.imag)),
            textcoords="offset points",
            color="#224653",
            ha="left" if point.real > 0.5 else "right" if point.real < -0.5 else "center",
            va="bottom" if point.imag > 0.5 else "top" if point.imag < -0.5 else "center",
        )

    for lon in (0, 90, 180, -90):
        pole = peirce_quincuncial(lon, -90)
        ax.scatter(pole.real, pole.imag, s=27, color="#a35038", zorder=4)
        ax.annotate(
            "S",
            (pole.real, pole.imag),
            xytext=(8 * round(pole.real), 6 * round(pole.imag)),
            textcoords="offset points",
            color="#a35038",
            fontweight="bold",
            ha="left" if pole.real > 0 else "right",
            va="bottom" if pole.imag > 0 else "top",
        )
    ax.scatter(0, 0, s=28, color="#224653", zorder=4)
    ax.annotate("N", (0, 0), xytext=(6, 5), textcoords="offset points", color="#224653")

    for name, lon, lat, offset in LANDMARKS:
        point = peirce_quincuncial(lon, lat)
        ax.scatter(point.real, point.imag, s=26, color="#725487", edgecolor="white", zorder=4)
        marker = ax.annotate(
            name,
            (point.real, point.imag),
            xytext=offset,
            textcoords="offset points",
            ha="right" if offset[0] < 0 else "left",
            color="#523562",
            fontsize=9,
        )
        marker.set_path_effects([patheffects.withStroke(linewidth=2.5, foreground="#fff")])

    fig.suptitle(
        "The Moon in Peirce's quincuncial projection",
        fontsize=17,
        color="#193746",
        fontweight="bold",
    )
    fig.legend(
        [Line2D([0], [0], color=color) for color in ("#558e80", "#bb8269", "#224653")],
        ["Parallels", "Meridians", "Equator and cuts"],
        loc="outside lower center",
        ncols=3,
        frameon=False,
        fontsize=9,
    )
    fig.savefig(Path(__file__).with_suffix(".png"), dpi=180)
    plt.close(fig)


def compare_proj() -> None:
    """Compare both hemispheres with the optional PROJ square reference."""
    try:
        import pyproj
    except ImportError as error:
        raise SystemExit("Install pyproj to run the optional reference comparison.") from error
    projection = pyproj.Proj("+proj=peirce_q +shape=square +lon_0=0 +R=1")
    scale = 2 * float(elliprf(0, 1, 2))
    latitudes = (-85, -65, -45, -25, -5, 0, 5, 25, 45, 65, 85, 90)
    samples = [(lon, lat) for lon in range(-180, 180, 10) for lat in latitudes]
    errors = [
        abs(peirce_quincuncial(lon, lat) - complex(*projection(lon, lat)) / scale)
        for lon, lat in samples
    ]
    print(f"PROJ {pyproj.proj_version_str}: {len(samples)} points, max error {max(errors):.3e}")


def main() -> None:
    """Generate the lunar graticule and optionally compare it with PROJ."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--compare-proj", action="store_true")
    options = parser.parse_args()
    render()
    if options.compare_proj:
        compare_proj()


if __name__ == "__main__":
    main()
