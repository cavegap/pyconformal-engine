"""Reproductions of the thesis figures as runnable examples.

Each example here corresponds to a specific figure of Vega Penagos & Olivero
Zapata (2015). When fully implemented they will be invokable from the command
line as::

    python -m pyconformal.examples <name>

Planned examples (by thesis figure):

* ``disk_to_halfplane`` — Figure 3.6, w = i(1−z)/(1+z).
* ``crescent_to_strip`` — Figures 3.8 and 3.9.
* ``square_mapping`` — Figures 3.4 and 3.5 (z² and angle magnification).
* ``strip_to_disk_via_exp`` — Figure 3.10.
* ``tan_strip_to_disk`` — Figure 3.12.
* ``sc_arcsine`` — Figure 3.16.
* ``sc_square`` — Figure 3.17 (resolves the open problem of page 53).
* ``cube_and_inverse`` — Figure 4.2.
* ``exp_polygon`` — Figure 4.3.
* ``lunar_mercator`` — Figures 4.4–4.5 (flagship example).

References
----------
Vega Penagos & Olivero Zapata (2015), passim.
"""

from __future__ import annotations

__all__: list[str] = []
