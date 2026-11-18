"""Visualize the generators of group P from Chapter 1 of the thesis."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from pyconformal.linear import Dilation, LinearMap, Reflection, Rotation


def main() -> None:
    """Render the same grid and marked triangle under four linear maps."""
    maps = (
        ("Original", LinearMap(np.eye(2))),
        ("Rotation · 45°", Rotation(np.pi / 4)),
        ("Reflection · real axis", Reflection(0)),
        ("Dilation · scale 1.5", Dilation(1.5)),
    )
    triangle = np.array([0j, 0.85 + 0j, 0.55j, 0j])
    grid_axis = np.linspace(-1, 1, 9)
    extent = np.array([-1.0, 1.0])
    right_angle = np.array([0.15 + 0j, 0.15 + 0.15j, 0.15j])
    fig, axes = plt.subplots(1, 4, figsize=(11, 3.6), layout="constrained")
    for ax, (title, transform) in zip(axes, maps, strict=True):
        for offset in grid_axis:
            for line in (extent + 1j * offset, offset + 1j * extent):
                mapped = transform(line)
                ax.plot(mapped.real, mapped.imag, color="#cfdae5", linewidth=0.7)

        ax.axhline(0, color="#73889d", linewidth=0.8)
        ax.axvline(0, color="#73889d", linewidth=0.8)
        if isinstance(transform, Reflection):
            ax.axhline(0, color="#735789", linewidth=1.4, linestyle="--")

        mapped = transform(triangle)
        ax.fill(mapped.real, mapped.imag, color="#a4cae4", alpha=0.55)
        ax.plot(mapped.real, mapped.imag, color="#173851", linewidth=1.8)
        marker = transform(right_angle)
        ax.plot(marker.real, marker.imag, color="#173851", linewidth=1.15)
        labels = (
            ("O", "#173851", (-10, -11)),
            ("A", "#a23b24", (8, 7)),
            ("B", "#00665c", (-11, 7 if mapped[2].imag > 0 else -10)),
        )
        for point, (label, color, offset) in zip(mapped[:3], labels, strict=True):
            ax.scatter(point.real, point.imag, color=color, s=38, zorder=3)
            ax.annotate(
                label,
                (point.real, point.imag),
                xytext=offset,
                textcoords="offset points",
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
                color=color,
            )

        ax.set_title(title, fontsize=10, fontweight="bold")
        ax.set(xlim=(-1.6, 1.6), ylim=(-1.6, 1.6), aspect="equal")
        ax.set_xticks([-1, 0, 1])
        ax.set_yticks([-1, 0, 1])
        ax.set_xlabel("Real", fontsize=8)
        ax.tick_params(labelsize=8, length=2, colors="#44576a")
        for spine in ax.spines.values():
            spine.set_color("#d0d8e2")

    axes[0].set_ylabel("Imaginary", fontsize=8)
    output = Path(__file__).with_suffix(".png")
    fig.savefig(output, dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    main()
