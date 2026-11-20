/* Animated landing page: the same geographic point uses the atlas's Peirce projection. */
(() => {
  'use strict';
  const globe = document.getElementById('globe'), square = document.getElementById('square');
  const ctx = globe.getContext('2d'), sq = square.getContext('2d');
  const motion = document.getElementById('motion'), slider = document.getElementById('longitude');
  const readout = document.getElementById('coordinates'), preference = matchMedia('(prefers-reduced-motion: reduce)');
  const size = globe.width, radius = size / 2 - 5, frame = ctx.createImageData(size, size);
  const radians = Math.PI / 180, pixels = [];
  // Orthographic inverse coordinates are fixed; only the central longitude rotates.
  for (let y = 0; y < size; y++) for (let x = 0; x < size; x++) {
    const nx = (x - size / 2) / radius, ny = (size / 2 - y) / radius;
    const r2 = nx * nx + ny * ny;
    if (r2 > 1) continue;
    const z = Math.sqrt(1 - r2), latitude = Math.asin(ny);
    pixels.push({index: (y * size + x) * 4, latitude,
      longitude: Math.atan2(nx, z) / radians,
      light: .72 + .28 * Math.max(0, -.32 * nx + .38 * ny + .86 * z)});
  }
  let texture, imageWidth, imageHeight, phase = 0, longitude = -25, latitude = 24;
  let paused = preference.matches, ready = false, visible = true, previous = 0, request = 0;
  const trail = [];
  const wrap = value => ((value + 180) % 360 + 360) % 360 - 180;
  const graticule = document.createElement('canvas');
  graticule.width = graticule.height = size;
  const grid = graticule.getContext('2d');
  const gridColors = {meridian: '#91e5df', parallel: '#fff0c6', equator: '#ffd27a'};
  function strokeGrid(context, color) {
    context.lineWidth = 2.8; context.strokeStyle = '#081810a6'; context.stroke();
    context.lineWidth = 1.05; context.strokeStyle = color; context.stroke();
  }
  function strokeEquator(context) {
    context.save(); context.lineJoin = 'round'; context.lineCap = 'round';
    context.lineWidth = 4.6; context.strokeStyle = '#102018'; context.stroke();
    context.lineWidth = 2.2; context.strokeStyle = gridColors.equator; context.stroke();
    context.restore();
  }
  for (const path of window.heroGraticule) {
    grid.beginPath();
    path.points.forEach(([u, v], index) => {
      const x = (u + 1) / 2 * size, y = (1 - v) / 2 * size;
      if (index) grid.lineTo(x, y); else grid.moveTo(x, y);
    });
    strokeGrid(grid, gridColors[path.kind]);
  }

  function mark(context, x, y, label = 'P') {
    context.beginPath(); context.arc(x, y, 7, 0, 2 * Math.PI);
    context.fillStyle = '#eebc70'; context.fill();
    context.lineWidth = 2; context.strokeStyle = '#172019'; context.stroke();
    context.beginPath(); context.arc(x, y, 11, 0, 2 * Math.PI);
    context.strokeStyle = '#eebc7099'; context.lineWidth = 1; context.stroke();
    if (label) {
      context.font = 'bold 18px system-ui'; context.fillStyle = '#fff1d9';
      context.strokeStyle = '#15201a'; context.lineWidth = 4;
      context.strokeText(label, x + 13, y - 12); context.fillText(label, x + 13, y - 12);
    }
  }
  function draw() {
    if (!ready) return;
    const cameraLongitude = longitude - 25;
    globe.dataset.cameraLongitude = String(cameraLongitude);
    for (const pixel of pixels) {
      const lon = wrap(cameraLongitude + pixel.longitude);
      const u = Math.min(imageWidth - 1, Math.floor((lon + 180) / 360 * imageWidth));
      const v = Math.min(imageHeight - 1, Math.floor((.5 - pixel.latitude / Math.PI) * imageHeight));
      const source = (v * imageWidth + u) * 4, target = pixel.index;
      for (let c = 0; c < 3; c++) frame.data[target + c] =
        Math.min(255, 255 * Math.pow(texture[source + c] / 255, .78) * pixel.light * 1.06);
      frame.data[target + 3] = 255;
    }
    ctx.putImageData(frame, 0, 0);
    const projectGlobe = (lon, lat) => {
      const a = (lon - cameraLongitude) * radians, b = lat * radians;
      return [size / 2 + radius * Math.cos(b) * Math.sin(a),
        size / 2 - radius * Math.sin(b), Math.cos(b) * Math.cos(a)];
    };
    for (let parallel = -75; parallel <= 75; parallel += 15) {
      if (parallel === 0) continue;
      ctx.beginPath(); let connected = false;
      for (let lon = -180; lon <= 180; lon += 3) {
        const [x, y, z] = projectGlobe(lon, parallel);
        if (z < 0) { connected = false; continue; }
        if (connected) ctx.lineTo(x, y); else ctx.moveTo(x, y);
        connected = true;
      }
      strokeGrid(ctx, gridColors.parallel);
    }
    for (let lon = -180; lon < 180; lon += 15) {
      ctx.beginPath(); let connected = false;
      for (let lat = -90; lat <= 90; lat += 3) {
        const [x, y, z] = projectGlobe(lon, lat);
        if (z < 0) { connected = false; continue; }
        if (connected) ctx.lineTo(x, y); else ctx.moveTo(x, y);
        connected = true;
      }
      strokeGrid(ctx, gridColors.meridian);
    }
    // One geographic location drives both markers; the globe camera changes only the view.
    const selected = {longitude, latitude};
    ctx.beginPath(); let connectedEquator = false;
    for (let lon = -180; lon <= 180; lon += 1) {
      const [x, y, z] = projectGlobe(lon, 0);
      if (z < 0) { connectedEquator = false; continue; }
      if (connectedEquator) ctx.lineTo(x, y); else ctx.moveTo(x, y);
      connectedEquator = true;
    }
    strokeEquator(ctx);
    const point = PeirceMap.project(selected.longitude, selected.latitude);
    const sx = (point[0] + 1) / 2 * size, sy = (1 - point[1]) / 2 * size;
    sq.clearRect(0, 0, size, size);
    sq.drawImage(graticule, 0, 0);
    square.dataset.gridPaths = String(window.heroGraticule.length);
    // The diamond separates hemispheres; its four vertices are the equatorial cuts.
    sq.beginPath(); sq.moveTo(size / 2, 0); sq.lineTo(size, size / 2);
    sq.lineTo(size / 2, size); sq.lineTo(0, size / 2); sq.closePath();
    strokeEquator(sq);
    sq.beginPath(); let last;
    for (const p of trail) {
      const x = (p[0] + 1) / 2 * size, y = (1 - p[1]) / 2 * size;
      if (!last || Math.hypot(x - last[0], y - last[1]) > size / 3) sq.moveTo(x, y);
      else sq.lineTo(x, y);
      last = [x, y];
    }
    sq.strokeStyle = '#eebc7090'; sq.lineWidth = 1.5; sq.stroke();
    mark(sq, sx, sy, 'P′');
    const [gx, gy] = projectGlobe(selected.longitude, selected.latitude); mark(ctx, gx, gy);
    readout.textContent = `P · ${Math.abs(latitude).toFixed(1)}°${latitude < 0 ? 'S' : 'N'}  ${Math.abs(longitude).toFixed(1)}°${longitude < 0 ? 'W' : 'E'}`;
    globe.dataset.longitude = String(longitude); globe.dataset.latitude = String(latitude);
    square.dataset.x = String(point[0]); square.dataset.y = String(point[1]);
  }
  function controls() {
    motion.textContent = paused ? 'Play animation  ▷' : 'Pause animation  Ⅱ';
    motion.setAttribute('aria-pressed', String(paused));
    motion.setAttribute('aria-label', paused ? 'Play animation' : 'Pause animation');
  }
  function tick(now) {
    request = 0;
    if (!ready || paused || document.hidden || !visible) { previous = 0; return; }
    if (!previous) previous = now;
    const delta = now - previous;
    if (delta >= 80) {
      phase += Math.min(delta, 160) / 1000;
      longitude = wrap(-25 + phase * 7);
      latitude = 24 + 32 * Math.sin(phase / 6);
      slider.value = String(longitude);
      trail.push(PeirceMap.project(longitude, latitude)); if (trail.length > 48) trail.shift();
      previous = now; draw();
    }
    request = requestAnimationFrame(tick);
  }
  function schedule() {
    if (request) cancelAnimationFrame(request);
    request = 0; previous = 0;
    if (ready && !paused && !document.hidden && visible) request = requestAnimationFrame(tick);
  }
  motion.addEventListener('click', () => { paused = !paused; controls(); schedule(); });
  slider.addEventListener('input', () => {
    paused = true; longitude = Number(slider.value); phase = (longitude + 25) / 7;
    latitude = 24 + 32 * Math.sin(phase / 6); trail.length = 0;
    controls(); schedule(); draw();
  });
  preference.addEventListener('change', event => { paused = event.matches; controls(); schedule(); });
  document.addEventListener('visibilitychange', schedule);
  new IntersectionObserver(entries => { visible = entries[0].isIntersecting; schedule(); }).observe(globe);
  const image = new Image();
  image.onload = () => {
    const buffer = document.createElement('canvas');
    imageWidth = buffer.width = image.naturalWidth; imageHeight = buffer.height = image.naturalHeight;
    const bufferContext = buffer.getContext('2d'); bufferContext.drawImage(image, 0, 0);
    texture = bufferContext.getImageData(0, 0, imageWidth, imageHeight).data;
    ready = true; draw(); schedule();
  };
  image.onerror = () => { document.getElementById('load-error').hidden = false; motion.disabled = true; readout.textContent = 'Static preview'; };
  controls(); image.src = 'examples/lunar-global-wac.jpg';
})();
