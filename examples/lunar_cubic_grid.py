"""Render the cubic coordinate grid for the lunar example in thesis §4.2."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from pyconformal.viz import apply_conformal_to_rectangle


def cube(z: NDArray[np.complex128]) -> NDArray[np.complex128]:
    """Evaluate the cubic map from Figure 4.5."""
    return z * z * z


def main() -> None:
    """Plot the thesis rectangle and the image of its coordinate grid."""
    grid = apply_conformal_to_rectangle(cube, 0j, 12 + 6j, n_real=13, n_imag=7)
    fig, (source, image) = plt.subplots(
        1, 2, figsize=(10.5, 5.0), layout="constrained", width_ratios=[1, 1.16]
    )
    for ax, horizontal, vertical in (
        (source, grid.horizontal, grid.vertical),
        (image, grid.mapped_horizontal, grid.mapped_vertical),
    ):
        for lines, color in ((horizontal, "#24756c"), (vertical, "#a45136")):
            for line in lines[1:-1]:
                ax.plot(line.real, line.imag, color=color, linewidth=0.85, alpha=0.76)
            for side in lines[[0, -1]]:
                ax.plot(side.real, side.imag, color="#254857", linewidth=1.4)
        ax.set_aspect("equal")
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=8, colors="#375460")
        ax.margins(x=0.14, y=0.13)

    corners = np.array([0j, 12 + 0j, 12 + 6j, 6j])
    labels = ("O", "A", "B", "C")
    colors = ("#213f50", "#984a34", "#126a5e", "#725487")
    offsets = ((6, -13), (7, 0), (7, 5), (-13, 7))
    image_offsets = ((-12, -13), (-4, -17), (8, 3), (-13, -15))
    for ax, points, marker_offsets in (
        (source, corners, offsets),
        (image, cube(corners), image_offsets),
    ):
        for point, label, color, offset in zip(points, labels, colors, marker_offsets, strict=True):
            ax.scatter(point.real, point.imag, color=color, zorder=3, s=31)
            ax.annotate(
                label,
                (point.real, point.imag),
                xytext=offset,
                textcoords="offset points",
                color=color,
                fontweight="bold",
                fontsize=10,
            )

    source.set(title="Source coordinates", xlabel="Re z", ylabel="Im z")
    image.set(title="Cubic image", xlabel="Re w", ylabel="Im w")
    fig.suptitle(r"Lunar example coordinates under $w=z^3$", fontweight="bold")
    fig.savefig(Path(__file__).with_suffix(".png"), dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()
