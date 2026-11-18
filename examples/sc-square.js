// Shared SC square kernel. Carlson RF duplication: NIST DLMF 19.36.
// Normalization: thesis section 3.4, Figure 3.17. null denotes infinity.
(() => {
"use strict";
  function add([a, b], [c, d]) { return [a + c, b + d]; }
  function multiply([a, b], [c, d]) { return [a * c - b * d, a * d + b * c]; }
  function scale([a, b], factor) { return [a * factor, b * factor]; }
  function magnitude([a, b]) { return Math.hypot(a, b); }

  function root([x, y]) {
    const modulus = Math.hypot(x, y);
    if (modulus === 0) return [0, 0];
    if (x >= 0) {
      const realPart = Math.sqrt((modulus + x) / 2);
      return [realPart, y / (2 * realPart)];
    }
    const imaginaryPart = Math.sqrt((modulus - x) / 2) * (y < 0 ? -1 : 1);
    return [y / (2 * imaginaryPart), imaginaryPart];
  }

  function carlsonRF(x, y, z) {
    // Duplication contracts differences by four. At this tolerance the
    // quadratic correction to 1/sqrt(mean) is below rounding error (§19.36).
    for (let step = 0; step < 32; step++) {
      const mean = scale(add(add(x, y), z), 1 / 3);
      const spread = Math.max(magnitude(add(x, scale(y, -1))), magnitude(add(x, scale(z, -1))));
      if (spread <= 1e-9 * magnitude(mean)) {
        const [a, b] = root(mean);
        return scale([a, -b], 1 / (a * a + b * b));
      }
      const sx = root(x), sy = root(y), sz = root(z);
      const lambda = add(add(multiply(sx, sy), multiply(sy, sz)), multiply(sz, sx));
      x = scale(add(x, lambda), .25);
      y = scale(add(y, lambda), .25);
      z = scale(add(z, lambda), .25);
    }
    throw new Error("Carlson duplication did not converge.");
  }

  const K = carlsonRF([0, 0], [1, 0], [2, 0])[0];

  function squareMap(point) {
    if (point === null) return [1, 1];
    const [x, y] = point;
    if (y > 0) {
      const [u, v] = carlsonRF([x + 1, y], [x, y], [x - 1, y]);
      return [1 + 2 * v / K, 1 - 2 * u / K];
    }
    const a = Math.abs(x);
    // Real-axis limits via the same square symmetries as the Python API.
    const value = a < 1
      ? [1 - 2 * Math.sqrt(1 - a) * carlsonRF([2, 0], [1 + a, 0], [2 * a, 0])[0] / K, -1]
      : [1, 1 - 2 * carlsonRF([a + 1, 0], [a, 0], [a - 1, 0])[0] / K];
    return x < 0 ? [value[1], value[0]] : value;
  }

window.SCSquare = Object.freeze({map: squareMap, add, scale, K});
})();
