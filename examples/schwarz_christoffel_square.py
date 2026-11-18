"""Render the Schwarz-Christoffel square in Figure 3.17 of the thesis."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from pyconformal.sc import upper_half_plane_to_square


def main() -> None:
    """Plot a sampled upper half-plane grid and its image in the square."""
    fig, (source, image) = plt.subplots(1, 2, figsize=(8.5, 4.1), layout="constrained")
    grid = (
        ([np.linspace(-3, 3, 220) + 1j * y for y in (0.08, 0.25, 0.5, 1, 2, 3)], "#307e73"),
        ([x + 1j * np.linspace(0, 3, 150) for x in np.linspace(-3, 3, 13)], "#b76644"),
    )
    for lines, color in grid:
        for line in lines:
            mapped = np.array([upper_half_plane_to_square(complex(z)) for z in line])
            source.plot(line.real, line.imag, color=color, alpha=0.7, linewidth=0.85)
            image.plot(mapped.real, mapped.imag, color=color, alpha=0.7, linewidth=0.85)

    prevertices = (-1 + 0j, 0j, 1 + 0j, complex(float("inf"), 0))
    vertices = np.array([upper_half_plane_to_square(z) for z in prevertices])
    boundary = vertices[[0, 1, 2, 3, 0]]
    source.axhline(0, color="#183746", linewidth=1.25)
    image.plot(boundary.real, boundary.imag, color="#183746", linewidth=1.45)
    colors = ("#1b567c", "#97502d", "#1f7160", "#76528b")
    for index, (z, w, color) in enumerate(zip(prevertices, vertices, colors, strict=True)):
        label = ("-1", "0", "1", "∞")[index]
        if index < 3:
            source.scatter(z.real, z.imag, s=40, color=color, zorder=3)
            source.annotate(
                label,
                (z.real, z.imag),
                xytext=(0, -17),
                textcoords="offset points",
                ha="center",
                color=color,
            )
        image.scatter(w.real, w.imag, s=40, color=color, zorder=3)
        image.annotate(
            label,
            (w.real, w.imag),
            xytext=(-9 if w.real < 0 else 9, 8 if w.imag > 0 else -14),
            textcoords="offset points",
            ha="center",
            color=color,
        )

    source.set(
        title="Upper half-plane",
        xlabel="Re z",
        ylabel="Im z",
        xlim=(-3.25, 3.25),
        ylim=(-0.48, 3.25),
    )
    source.set_xticks([-3, -2, 2, 3])
    image.set(
        title="Schwarz-Christoffel square",
        xlabel="Re w",
        ylabel="Im w",
        xlim=(-1.27, 1.27),
        ylim=(-1.27, 1.27),
    )
    image.set_xticks([-1, 0, 1])
    image.set_yticks([-1, 0, 1])
    for ax in (source, image):
        ax.set_aspect("equal")
        for spine in ax.spines.values():
            spine.set_color("#c1d2d5")
    fig.savefig(Path(__file__).with_suffix(".png"), dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    main()
