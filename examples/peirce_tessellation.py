"""Compare lunar Mercator imagery, one Peirce tile and a continuous tiling."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from peirce_mosaic import sample_global_mosaic

from pyconformal.cartography import peirce_quincuncial_inverse


def main() -> None:
    """Render geographic context and alternating half-turn copies of a tile."""
    here = Path(__file__).resolve().parent
    mosaic = np.asarray(plt.imread(here / "lunar-global-wac.jpg"), dtype=np.float64)
    count = 600
    axis = -1 + 2 * (np.arange(count) + 0.5) / count
    lon, lat = peirce_quincuncial_inverse(axis[None, :] + 1j * axis[:, None])
    tile = sample_global_mosaic(mosaic, lon, lat)
    tiling = np.block(
        [
            [tile if (row + col) % 2 == 0 else tile[::-1, ::-1] for col in range(3)]
            for row in range(3)
        ]
    )
    longitude = -180 + 360 * (np.arange(1200) + 0.5) / 1200
    bound = np.arcsinh(np.tan(np.deg2rad(80)))
    mercator_y = -bound + 2 * bound * (np.arange(600) + 0.5) / 600
    latitude = np.rad2deg(np.arctan(np.sinh(mercator_y)))
    longitude, latitude = np.meshgrid(longitude, latitude)
    mercator = sample_global_mosaic(mosaic, longitude, latitude)
    low, high = np.percentile(mosaic, [2, 98])
    fig, axes = plt.subplots(1, 3, figsize=(15, 6.3), layout="constrained")
    for ax, image, extent, title in zip(
        axes,
        (mercator, tile, tiling),
        ((-np.pi, np.pi, -bound, bound), (-1, 1, -1, 1), (-3, 3, -3, 3)),
        (
            "Mercator · 80°S to 80°N",
            "One Peirce tile · whole Moon",
            "Nine tiles · alternating 180° turns",
        ),
        strict=True,
    ):
        ax.imshow(image, origin="lower", extent=extent, cmap="gray", vmin=low, vmax=high)
        ax.set_title(title, fontsize=11, color="#193746", fontweight="bold")
        ax.set_axis_off()
    axes[1].plot([0, 1, 0, -1, 0], [-1, 0, 1, 0, -1], c="#91f5f0", lw=1.7)
    for coordinate in (-1, 1):
        axes[2].axhline(coordinate, c="#91f5f0", lw=0.8)
        axes[2].axvline(coordinate, c="#91f5f0", lw=0.8)
    # North is at the central diamond's center; the four outer corners are
    # copies of the same south pole. Alternating half-turns join tile edges.
    for x, y, label in ((0, 0, "N"), (-1, -1, "S"), (1, -1, "S"), (-1, 1, "S"), (1, 1, "S")):
        axes[1].annotate(
            label,
            (x, y),
            xytext=(4 if x < 1 else -12, 5 if y < 1 else -14),
            textcoords="offset points",
            color="white",
            fontsize=11,
            fontweight="bold",
            bbox={"facecolor": "#122b38", "edgecolor": "none", "alpha": 0.85, "pad": 1},
        )
    fig.suptitle(
        "From lunar Mercator to Peirce's repeating square",
        fontsize=18,
        color="#193746",
        fontweight="bold",
    )
    fig.supxlabel(
        "Mercator excludes the poles. Peirce includes both: north in the center, "
        "south repeated at the four corners.\n"
        "The cyan diamond is the equator. The right panel repeats the same Moon; "
        "it adds no geographic coverage. Cyan seams mark tile joins.\n"
        "Source: LROC WAC, NASA / GSFC / Arizona State University. "
        "The projection is conformal away from its four equatorial branch points.",
        fontsize=9,
        color="#254653",
        linespacing=1.7,
    )
    fig.savefig(here / "peirce_tessellation.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()
