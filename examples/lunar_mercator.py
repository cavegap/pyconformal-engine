"""Warp a georeferenced LROC mosaic crop with the cubic map from thesis §4.2."""

from itertools import pairwise
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patheffects
from matplotlib.colors import PowerNorm
from numpy.typing import NDArray
from scipy.ndimage import map_coordinates

from pyconformal.viz import apply_conformal_to_rectangle

FloatGrid = NDArray[np.float64]
ComplexGrid = NDArray[np.complex128]
WEST, SOUTH, EAST, NORTH = -55.0, 2.0, -15.0, 28.0
MERCATOR_SOUTH = float(np.arcsinh(np.tan(np.deg2rad(6.0))))
UNIT_ANGLE = float(np.deg2rad(EAST - WEST) / 12)
LANDMARKS = (
    ("Aristarchus", -47.49, 23.73, "#ffd095"),
    ("Kepler", -38.01, 8.12, "#bde9e0"),
    ("Copernicus", -20.08, 9.62, "#f7c3dc"),
)


def source_coordinate(longitude: float, latitude: float) -> complex:
    """Convert east-positive degrees into normalized lunar Mercator coordinates."""
    x = np.deg2rad(longitude - WEST) / UNIT_ANGLE
    y = (np.arcsinh(np.tan(np.deg2rad(latitude))) - MERCATOR_SOUTH) / UNIT_ANGLE
    return complex(x, y)


def inverse_cube(points: ComplexGrid) -> ComplexGrid:
    """Recover points in the thesis rectangle and mark exterior samples as NaN."""
    argument = np.mod(np.angle(points), 2 * np.pi)
    argument = np.where(np.isclose(argument, 2 * np.pi, atol=1e-12, rtol=0), 0, argument)
    radius = np.cbrt(np.abs(points))
    x = radius * np.cos(argument / 3)
    y = radius * np.sin(argument / 3)
    inside = (argument <= 1.5 * np.pi + 1e-12) & (x <= 12 + 1e-10) & (y <= 6 + 1e-10)
    return np.where(inside, np.clip(x, 0, 12) + 1j * np.clip(y, 0, 6), complex(np.nan, np.nan))


def sample_mosaic(mosaic: FloatGrid, points: ComplexGrid) -> FloatGrid:
    """Interpolate the geographic image at normalized Mercator coordinates."""
    valid = np.isfinite(points)
    safe = np.where(valid, points, 0j)
    longitudes = WEST + np.rad2deg(UNIT_ANGLE * safe.real)
    latitudes = np.rad2deg(np.arctan(np.sinh(MERCATOR_SOUTH + UNIT_ANGLE * safe.imag)))
    height, width = mosaic.shape
    columns = (longitudes - WEST) * width / (EAST - WEST) - 0.5
    rows = (NORTH - latitudes) * height / (NORTH - SOUTH) - 0.5
    samples = map_coordinates(mosaic, [rows, columns], order=1, mode="nearest")
    return np.asarray(np.where(valid, samples, np.nan), dtype=np.float64)


def pixel_grid(extent: tuple[float, float, float, float], height: int, width: int) -> ComplexGrid:
    """Create complex coordinates at output pixel centers, starting at the bottom."""
    left, right, bottom, top = extent
    x = left + (np.arange(width) + 0.5) * (right - left) / width
    y = bottom + (np.arange(height) + 0.5) * (top - bottom) / height
    return x[None, :] + 1j * y[:, None]


def main() -> None:
    """Render the Mercator crop, cubic image, and local scale."""
    path = Path(__file__)
    mosaic = np.asarray(plt.imread(path.with_name("lunar-lroc-wac.jpg")), dtype=np.float64)
    if mosaic.shape != (520, 800):
        raise ValueError("Expected the 800 by 520 grayscale LROC crop described in the example.")
    source_extent = (0.0, 12.0, 0.0, 6.0)
    image_extent = (-432.0, 1728.0, -216.0, 2376.0)
    source_pixels = pixel_grid(source_extent, 380, 760)
    image_pixels = pixel_grid(image_extent, 960, 800)
    original = sample_mosaic(mosaic, source_pixels)
    warped = sample_mosaic(mosaic, inverse_cube(image_pixels))
    mapped_grid = apply_conformal_to_rectangle(lambda z: z**3, 0j, 12 + 6j, 7, 4)
    black, white = np.percentile(original, [2, 99])
    fig = plt.figure(figsize=(12.4, 8.0), layout="constrained")
    layout = fig.add_gridspec(2, 2, width_ratios=(1, 1.27))
    source = fig.add_subplot(layout[0, 0])
    scale_ax = fig.add_subplot(layout[1, 0])
    image = fig.add_subplot(layout[:, 1])
    for ax, raster, extent, horizontal, vertical in (
        (source, original, source_extent, mapped_grid.horizontal, mapped_grid.vertical),
        (image, warped, image_extent, mapped_grid.mapped_horizontal, mapped_grid.mapped_vertical),
    ):
        ax.imshow(raster, origin="lower", extent=extent, cmap="gray", vmin=black, vmax=white)
        for family in (horizontal, vertical):
            for line in family:
                ax.plot(line.real, line.imag, color="#c4e2df", linewidth=0.55, alpha=0.45)

    corners = np.array([0j, 12 + 0j, 12 + 6j, 6j, 0j])
    boundary = np.concatenate(
        [np.linspace(a, b, 150, endpoint=False) for a, b in pairwise(corners)]
    )
    boundary = np.append(boundary, boundary[0])
    for ax, outline in ((source, boundary), (image, boundary**3)):
        line = ax.plot(outline.real, outline.imag, color="#65fff0", lw=2, zorder=4)[0]
        line.set_path_effects(
            [patheffects.Stroke(linewidth=4, foreground="#173442"), patheffects.Normal()]
        )
    for panel, ax in enumerate((source, image)):
        for label, corner in zip("OABC", corners[:4], strict=True):
            z = corner if panel == 0 else corner**3
            ax.scatter(z.real, z.imag, s=55, c="#65fff0", edgecolors="#173442", zorder=5)
            annotation = ax.annotate(
                label,
                (z.real, z.imag),
                xytext=(6, 6),
                textcoords="offset points",
                fontsize=9,
                fontweight="bold",
                color="#173442",
            )
            annotation.set_path_effects([patheffects.withStroke(linewidth=3, foreground="white")])

    source_offsets = ((5, -14), (-4, 12), (-8, 12))
    image_offsets = ((12, 15), (7, 20), (8, 10))
    for (name, longitude, latitude, color), offset_in, offset_out in zip(
        LANDMARKS, source_offsets, image_offsets, strict=True
    ):
        point = source_coordinate(longitude, latitude)
        for ax, z, offset in ((source, point, offset_in), (image, point**3, offset_out)):
            ax.scatter(
                z.real, z.imag, s=68, color=color, edgecolor="#172f3c", linewidth=1.4, zorder=6
            )
            ax.annotate(
                name,
                (z.real, z.imag),
                xytext=offset,
                textcoords="offset points",
                fontsize=8.5,
                color="#173342",
                fontweight="medium",
                bbox={"facecolor": "#ffffff", "edgecolor": "none", "alpha": 0.84, "pad": 1.4},
            )

    heat = scale_ax.imshow(
        3 * np.abs(source_pixels) ** 2,
        origin="lower",
        extent=source_extent,
        cmap="viridis",
        norm=PowerNorm(gamma=0.55, vmin=0, vmax=540),
    )
    bar = fig.colorbar(
        heat,
        ax=scale_ax,
        orientation="horizontal",
        fraction=0.13,
        pad=0.06,
        ticks=(0, 90, 180, 360, 540),
    )
    bar.set_label("Output length per source-coordinate unit", fontsize=9)
    source.set(title="Source · lunar crop in Mercator coordinates", ylabel="Im z")
    scale_ax.set(title=r"Local scale of the cubic map, $3|z|^2$", xlabel="Re z", ylabel="Im z")
    image.set(title=r"Inverse-resampled image under $w=z^3$", xlabel="Re w", ylabel="Im w")
    source.set(xlim=(-0.45, 12.55), ylim=(-0.45, 6.55))
    fig.supxlabel(
        "Cyan O-A-B-C: the sampled rectangle boundary, not a geological rim. "
        "Colored circles: the same three crater centers.\n"
        "Local scale = |f'(z)| = 3|z|²: short lengths multiply by this factor; "
        "areas multiply by its square. O is a critical point.\n"
        "Scale refers to the normalized Mercator plane, not kilometers on the Moon. "
        "Imagery: NASA / GSFC / Arizona State University.",
        fontsize=8.5,
        color="#254653",
        linespacing=1.6,
    )
    for ax in (source, scale_ax, image):
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=8, colors="#375460")
    image.set(xlim=(-520, 1820), ylim=(-280, 2460))
    fig.savefig(path.with_suffix(".png"), dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()
