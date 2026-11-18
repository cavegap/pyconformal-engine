"""Inverse-resample the global LROC mosaic into Peirce's square."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patheffects
from matplotlib.colors import LogNorm
from matplotlib.lines import Line2D
from numpy.typing import NDArray
from scipy.ndimage import map_coordinates
from scipy.special import elliprf

from pyconformal.cartography import peirce_quincuncial, peirce_quincuncial_inverse

FloatGrid = NDArray[np.float64]
LANDMARKS = (
    ("Copernicus", -20.08, 9.62, (15, 13)),
    ("Jackson", -163.32, 22.05, (-14, 13)),
    ("Tycho", -11.22, -43.30, (-15, -14)),
    ("Tsiolkovskiy", 128.97, -20.38, (16, -15)),
)
INK = "#122b38"
EQUATOR = "#91f5f0"
CRATERS = "#ffd479"
POLES = "#ffffff"


def sample_global_mosaic(mosaic: FloatGrid, longitude: FloatGrid, latitude: FloatGrid) -> FloatGrid:
    """Interpolate an equirectangular global mosaic with longitude wrapping."""
    height, width = mosaic.shape
    # The source raster spans longitude −180 to 180 and latitude −90 to 90.
    columns = ((longitude + 180) % 360) * width / 360 + 0.5
    rows = (90 - latitude) * height / 180 - 0.5
    padded = np.pad(mosaic, ((0, 0), (1, 1)), mode="wrap")
    values = map_coordinates(padded, [rows, columns], order=1, mode="nearest")
    return np.asarray(values, dtype=np.float64)


def local_scale(longitude: FloatGrid, latitude: FloatGrid) -> FloatGrid:
    """Return linear scale relative to great-circle arc length on the unit sphere."""
    radius = np.tan(np.deg2rad(90 - np.abs(latitude)) / 2)
    disk = radius * np.exp(1j * np.deg2rad(longitude + 45))
    k = float(elliprf(0, 1, 2))
    # The inverse lemniscate map contributes the denominator and
    # stereographic projection contributes (1 + r²)/2.
    with np.errstate(divide="ignore"):
        factor = (1 + radius**2) / (2 * k * np.sqrt(np.abs(1 - disk**4)))
    return np.asarray(factor, dtype=np.float64)


def main() -> None:
    """Generate the labeled lunar map and its linear-scale panel."""
    path = Path(__file__)
    mosaic = np.asarray(plt.imread(path.with_name("lunar-global-wac.jpg")), dtype=np.float64)
    if mosaic.shape != (900, 1800):
        raise ValueError("Expected the 1800 by 900 global LROC WMS raster.")
    count = 1100
    pixel_centers = -1 + 2 * (np.arange(count) + 0.5) / count
    points = pixel_centers[None, :] + 1j * pixel_centers[:, None]
    longitude, latitude = peirce_quincuncial_inverse(points)
    image = sample_global_mosaic(mosaic, longitude, latitude)
    scale = local_scale(longitude, latitude)
    pole_scale = 1 / (2 * float(elliprf(0, 1, 2)))
    low, high = np.percentile(image, [2, 98])

    fig, (map_ax, scale_ax) = plt.subplots(
        1, 2, figsize=(11.2, 6.2), layout="constrained", width_ratios=(1.48, 1)
    )
    extent = (-1, 1, -1, 1)
    map_ax.imshow(image, origin="lower", extent=extent, cmap="gray", vmin=low, vmax=high)
    zoom = scale_ax.imshow(
        scale / pole_scale,
        origin="lower",
        extent=extent,
        cmap="viridis",
        norm=LogNorm(1, 5),
    )
    colorbar = fig.colorbar(
        zoom,
        ax=scale_ax,
        orientation="horizontal",
        fraction=0.075,
        pad=0.07,
        extend="max",
        ticks=(1, 2, 3, 5),
    )
    colorbar.minorticks_off()
    colorbar.ax.set_xticklabels(["1\u00d7", "2\u00d7", "3\u00d7", "5\u00d7+"])
    colorbar.set_label("Local length scale relative to a pole", fontsize=9, labelpad=6)
    scale_ax.text(
        0.5,
        -0.04,
        "Purple · 1\u00d7 at the poles\n"
        "Green to yellow · increasing enlargement\n"
        "At 2\u00d7, equal short ground distances appear twice as long.\n"
        "Yellow includes values above 5\u00d7 near the four cut points.",
        transform=scale_ax.transAxes,
        ha="center",
        va="top",
        fontsize=8.2,
        linespacing=1.55,
        color="#254653",
    )
    equator_x, equator_y = [0, 1, 0, -1, 0], [-1, 0, 1, 0, -1]
    for ax in (map_ax, scale_ax):
        ax.set(xlim=(-1.12, 1.12), ylim=(-1.12, 1.12), aspect="equal")
        ax.set_axis_off()
        ax.plot([-1, 1, 1, -1, -1], [-1, -1, 1, 1, -1], color=INK, linewidth=1.3)
        rim = ax.plot(equator_x, equator_y, color=EQUATOR, linewidth=1.65, zorder=3)[0]
        rim.set_path_effects(
            [patheffects.Stroke(linewidth=3.65, foreground=INK), patheffects.Normal()]
        )
        ax.scatter(
            equator_x[:-1],
            equator_y[:-1],
            marker="D",
            s=37,
            facecolor=EQUATOR,
            edgecolor=INK,
            linewidth=1.45,
            zorder=4,
        )
    for name, lon, lat, offset in LANDMARKS:
        point = peirce_quincuncial(lon, lat)
        map_ax.scatter(
            point.real,
            point.imag,
            s=55,
            color=CRATERS,
            edgecolor=INK,
            linewidth=1.65,
            zorder=5,
        )
        label = map_ax.annotate(
            name,
            (point.real, point.imag),
            xytext=offset,
            textcoords="offset points",
            color="#ffffff",
            fontsize=10,
            fontweight="semibold",
            ha="right" if offset[0] < 0 else "left",
            va="center",
            bbox={"boxstyle": "round,pad=0.25", "facecolor": INK, "edgecolor": "none"},
            arrowprops={"arrowstyle": "-", "color": CRATERS, "lw": 1.2, "shrinkA": 2, "shrinkB": 5},
            zorder=6,
        )
        if label.arrow_patch is not None:
            label.arrow_patch.set_path_effects(
                [
                    patheffects.Stroke(linewidth=2.8, foreground=INK),
                    patheffects.Normal(),
                ]
            )
    for lon in (0, 90, 180, -90):
        pole = peirce_quincuncial(lon, -90)
        map_ax.scatter(
            pole.real,
            pole.imag,
            s=44,
            marker="P",
            facecolor=POLES,
            edgecolor=INK,
            linewidth=1.3,
            zorder=5,
        )
        map_ax.annotate(
            "S",
            (pole.real, pole.imag),
            xytext=(7 * round(pole.real), 7 * round(pole.imag)),
            textcoords="offset points",
            fontsize=10,
            color="#193746",
            fontweight="bold",
            ha="left" if pole.real > 0 else "right",
            va="bottom" if pole.imag > 0 else "top",
        )
    map_ax.scatter(0, 0, s=44, marker="P", facecolor=POLES, edgecolor=INK, linewidth=1.3, zorder=5)
    map_ax.annotate(
        "N",
        (0, 0),
        xytext=(7, 7),
        textcoords="offset points",
        fontsize=10,
        color="white",
        fontweight="bold",
        bbox={"boxstyle": "round,pad=0.22", "facecolor": INK, "edgecolor": "none"},
        zorder=6,
    )
    map_ax.set_title(
        "Whole Moon · north at center, south at four corners", color="#193746", fontsize=11
    )
    scale_ax.set_title("Local enlargement relative to the poles", color="#193746", fontsize=11)
    fig.suptitle(
        "The Moon in Peirce's quincuncial projection",
        fontsize=17,
        color="#193746",
        fontweight="bold",
    )
    fig.legend(
        handles=[
            Line2D(
                [0],
                [0],
                color=INK,
                marker="D",
                markerfacecolor=EQUATOR,
                markeredgecolor=INK,
                label="Equator and cut points",
            ),
            Line2D(
                [0],
                [0],
                linestyle="none",
                marker="o",
                markerfacecolor=CRATERS,
                markeredgecolor=INK,
                label="Named crater",
            ),
            Line2D(
                [0],
                [0],
                linestyle="none",
                marker="P",
                markerfacecolor=POLES,
                markeredgecolor=INK,
                label="Pole",
            ),
        ],
        loc="outside lower center",
        ncols=3,
        frameon=False,
        fontsize=9,
    )
    fig.savefig(path.with_suffix(".png"), dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()
