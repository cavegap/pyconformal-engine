"""Compare the lunar outlines in Figure 4.5 and register them on Peirce's map."""

import json
from argparse import ArgumentParser
from collections.abc import Callable
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patheffects
from numpy.typing import NDArray
from peirce_mosaic import sample_global_mosaic
from PIL import Image

from pyconformal.cartography import peirce_quincuncial, peirce_quincuncial_inverse
from pyconformal.viz import apply_conformal_to_rectangle

HERE = Path(__file__).resolve().parent
ComplexLine = NDArray[np.complex128]
Extent = tuple[float, float, float, float]
LABELS = ("A", "B", "C", "D")
LABEL_OFFSETS = ((-9, 9), (-7, 8), (5, -10), (5, 9))


def densify(points: ComplexLine) -> ComplexLine:
    """Sample each closed source edge before applying a nonlinear map."""
    segments = [
        np.linspace(a, b, max(2, int(np.ceil(abs(b - a) / 0.035))), endpoint=False)
        for a, b in zip(points, np.roll(points, -1), strict=True)
    ]
    return np.concatenate([*segments, points[:1]])


def draw_markers(ax: plt.Axes, points: ComplexLine, color: str) -> None:
    """Mark the same four source boundary points in each panel."""
    for point, label, offset in zip(points, LABELS, LABEL_OFFSETS, strict=True):
        ax.scatter(point.real, point.imag, color=color, edgecolor="#203344", s=24, zorder=4)
        mark = ax.annotate(
            label,
            (point.real, point.imag),
            xytext=offset,
            textcoords="offset points",
            color=color,
            fontsize=9,
            fontweight="bold",
            ha="center",
            zorder=4,
        )
        mark.set_path_effects([patheffects.withStroke(linewidth=2, foreground="#203344")])


def compare_contours(paths: list[ComplexLine], markers: ComplexLine) -> None:
    """Render the archived points and both candidate power maps."""
    fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.7), layout="constrained")

    def power(n: int) -> Callable[[ComplexLine], ComplexLine]:
        return lambda z: np.asarray(z**n, dtype=np.complex128)

    for index, ax in enumerate(axes):
        transform = power(index + 1)
        grid = apply_conformal_to_rectangle(transform, 0j, 12 + 6j, 13, 7)
        for family, color in (
            (grid.mapped_horizontal, "#9e8270"),
            (grid.mapped_vertical, "#86a4ae"),
        ):
            for curve in family:
                ax.plot(curve.real, curve.imag, color=color, alpha=0.5, linewidth=0.55)
        for position, path in enumerate(paths):
            image = transform(path)
            fill, edge = ("#164f79", "#143c65") if position == 0 else ("#b7c1c3", "#74878e")
            ax.fill(
                image.real, image.imag, facecolor=fill, edgecolor=edge, linewidth=0.45, alpha=0.86
            )
        draw_markers(ax, transform(markers), "#ffda8f")
        ax.set_aspect("equal")
        ax.set_xlabel("Re z" if index == 0 else "Re w")
        ax.set_ylabel("Im z" if index == 0 else "Im w")
        ax.set_title(
            (
                "Source traced in the thesis",
                r"$w=z^2$ · published drawing",
                r"$w=z^3$ · written formula",
            )[index],
            color="#203a4b",
            fontweight="bold",
            fontsize=11,
        )
        ax.tick_params(colors="#385360", labelsize=8)
        ax.spines[["top", "right"]].set_visible(False)
        ax.margins(0.08)
    fig.suptitle(
        "Lunar outlines recovered from Figure 4.5", color="#203a4b", fontweight="bold", fontsize=15
    )
    fig.savefig(HERE / "lunar_thesis_outlines.png", dpi=180)
    plt.close(fig)


def geographic_coordinates(
    points: ComplexLine, frame: dict[str, float]
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Convert points in the archival Mercator frame to longitude and latitude."""
    longitude = frame["west"] + (frame["east"] - frame["west"]) * points.real / 12
    top = np.arcsinh(np.tan(np.deg2rad(frame["north"])))
    latitude = np.rad2deg(np.arctan(np.sinh(top * points.imag / 6)))
    return longitude, latitude


def project_outline(points: ComplexLine, frame: dict[str, float]) -> ComplexLine:
    """Register planar points in the archival frame and project them to Peirce."""
    longitude, latitude = geographic_coordinates(points, frame)
    return np.array(
        [
            peirce_quincuncial(float(lon), float(lat))
            for lon, lat in zip(longitude, latitude, strict=True)
        ],
        dtype=np.complex128,
    )


def raster_at_extent(
    mosaic: NDArray[np.float64], extent: Extent, width: int
) -> NDArray[np.float64]:
    """Inverse-sample the source mosaic at regularly spaced tile pixel centers."""
    left, right, bottom, top = extent
    height = max(2, round(width * (top - bottom) / (right - left)))
    x = left + (right - left) * (np.arange(width) + 0.5) / width
    y = bottom + (top - bottom) * (np.arange(height) + 0.5) / height
    longitude, latitude = peirce_quincuncial_inverse(x[None, :] + 1j * y[:, None])
    return sample_global_mosaic(mosaic, longitude, latitude)


def render_registered_overlay(
    paths: list[ComplexLine], markers: ComplexLine, frame: dict[str, float]
) -> None:
    """Render global context and a detailed view of the same registered contours."""
    projected = [project_outline(path, frame) for path in paths]
    points = np.concatenate(projected)
    projected_markers = project_outline(markers, frame)
    global_view = (-1.0, 1.0, -1.0, 1.0)
    zoom = (
        max(-1, float(points.real.min()) - 0.085),
        min(1, float(points.real.max()) + 0.085),
        max(-1, float(points.imag.min()) - 0.085),
        min(1, float(points.imag.max()) + 0.085),
    )
    mosaic = np.asarray(plt.imread(HERE / "lunar-global-wac.jpg"), dtype=np.float64)
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 5.8), layout="constrained")
    contrast = np.percentile(mosaic, [2, 98])
    for ax, extent, title in zip(
        axes, (global_view, zoom), ("Global context", "Detail of the archived tracing"), strict=True
    ):
        image = raster_at_extent(mosaic, extent, 980)
        ax.imshow(
            image, origin="lower", extent=extent, cmap="gray", vmin=contrast[0], vmax=contrast[1]
        )
        ax.plot([0, 1, 0, -1, 0], [-1, 0, 1, 0, -1], color="#e8f5f0", alpha=0.45, lw=0.7)
        for index, path in enumerate(projected):
            if index == 0:
                ax.fill(path.real, path.imag, color="#42ced0", alpha=0.20, linewidth=0)
            color = "#74f7f1" if index == 0 else "#ffe1a8"
            line = ax.plot(path.real, path.imag, color=color, lw=1 if index == 0 else 0.7)[0]
            line.set_path_effects(
                [
                    patheffects.Stroke(linewidth=2.05 if index == 0 else 1.5, foreground="#264149"),
                    patheffects.Normal(),
                ]
            )
        draw_markers(ax, projected_markers, "#ffda8f")
        ax.set(xlim=extent[:2], ylim=extent[2:], title=title)
        ax.set_axis_off()
    fig.suptitle(
        "The thesis outlines on the Peirce lunar mosaic",
        color="#203a4b",
        fontweight="bold",
        fontsize=15,
    )
    fig.supxlabel(
        "Approximate archival registration · LROC WAC: NASA / GSFC / Arizona State University",
        color="#385360",
        fontsize=8,
    )
    fig.savefig(HERE / "lunar_thesis_peirce.png", dpi=180)
    plt.close(fig)


def write_interactive_data(
    paths: list[ComplexLine], markers: ComplexLine, frame: dict[str, float]
) -> None:
    """Generate the browser's synchronized curves and undecorated mosaic tile."""
    projected = [project_outline(path, frame) for path in paths]
    lon, lat = geographic_coordinates(paths[0], frame)
    sphere = []
    tilt = np.deg2rad(30)
    for path in paths:
        longitude, latitude = geographic_coordinates(path, frame)
        lam, phi = np.deg2rad(longitude), np.deg2rad(latitude)
        sphere.append(
            np.round(
                np.column_stack(
                    (
                        np.cos(phi) * np.sin(lam),
                        np.cos(tilt) * np.sin(phi) - np.sin(tilt) * np.cos(phi) * np.cos(lam),
                    )
                ),
                8,
            ).tolist()
        )
    points = {
        "sphere": sphere,
        "source": [np.round(np.column_stack((path.real, path.imag)), 6).tolist() for path in paths],
        "peirce": [
            np.round(np.column_stack((path.real, path.imag)), 8).tolist() for path in projected
        ],
        "geographic": np.round(np.column_stack((lon, lat)), 5).tolist(),
        "markers": [int(np.argmin(np.abs(paths[0] - marker))) for marker in markers],
    }
    payload = json.dumps(points, separators=(",", ":"), allow_nan=False)
    (HERE / "lunar-thesis-data.js").write_text(
        "// Generated by lunar_thesis_outlines.py --interactive.\n"
        f"window.lunarOutlineData = {payload};\n",
        encoding="utf-8",
    )
    mosaic = np.asarray(plt.imread(HERE / "lunar-global-wac.jpg"), dtype=np.float64)
    tile = raster_at_extent(mosaic, (-1.0, 1.0, -1.0, 1.0), 880)
    low, high = np.percentile(mosaic, [2, 98])
    pixels = np.clip(255 * (tile - low) / (high - low), 0, 255).astype(np.uint8)
    Image.fromarray(pixels[::-1]).save(HERE / "lunar-thesis-tile.jpg", quality=90)
    mercator_x = 12 * (np.arange(880) + 0.5) / 880
    mercator_y = 6 * (np.arange(440) + 0.5) / 440
    longitude, latitude = geographic_coordinates(
        mercator_x[None, :] + 1j * mercator_y[:, None], frame
    )
    mercator = sample_global_mosaic(mosaic, longitude, latitude)
    pixels = np.clip(255 * (mercator - low) / (high - low), 0, 255).astype(np.uint8)
    Image.fromarray(pixels[::-1]).save(HERE / "lunar-thesis-mercator.jpg", quality=92)
    axis = -1 + 2 * (np.arange(700) + 0.5) / 700
    x, y = np.meshgrid(axis, axis)
    rho = np.hypot(x, y)
    inside = rho <= 1
    c = np.arcsin(np.minimum(rho, 1))
    ratio = np.sin(c) / np.maximum(rho, 1e-15)
    phi = np.arcsin(np.clip(np.cos(c) * np.sin(tilt) + y * ratio * np.cos(tilt), -1, 1))
    lam = np.arctan2(x * ratio, np.cos(c) * np.cos(tilt) - y * ratio * np.sin(tilt))
    globe = sample_global_mosaic(mosaic, np.rad2deg(lam), np.rad2deg(phi))
    pixels = np.clip(255 * (globe - low) / (high - low), 0, 255).astype(np.uint8)
    pixels[~inside] = 255
    Image.fromarray(pixels[::-1]).save(HERE / "lunar-thesis-globe.jpg", quality=92)


def main() -> None:
    """Generate the planar comparison and the Peirce overlay."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--interactive", action="store_true", help="regenerate browser data")
    options = parser.parse_args()
    stored = json.loads((HERE / "lunar-thesis-outlines.json").read_text(encoding="utf-8"))
    outlines = [np.asarray(path, dtype=float) for path in stored["paths"]]
    points = [path[:, 0] + 1j * path[:, 1] for path in outlines]
    targets = (1.0 + 4.5j, 5.0 + 5.5j, 7.0 + 1.1j, 10.0 + 4.0j)
    markers = np.array([points[0][np.argmin(abs(points[0] - target))] for target in targets])
    paths = [densify(path) for path in points]
    if options.interactive:
        write_interactive_data(paths, markers, stored["registration"])
    else:
        compare_contours(paths, markers)
        render_registered_overlay(paths, markers, stored["registration"])


if __name__ == "__main__":
    main()
