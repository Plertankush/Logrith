/* Round Image Corners — set one radius for every corner or a different radius per corner. */
(function () {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const canvas = $('corner-canvas');
  const CORNERS = ['tl', 'tr', 'br', 'bl'];

  const state = { image: null, file: null, unit: 'px', linked: true };

  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
  const shortSide = () => Math.min(state.image.width, state.image.height);

  /** Radius range for the current unit: up to half the shorter side. */
  const maxRadius = () => (state.unit === '%' ? 50 : Math.floor(shortSide() / 2));

  /** Convert a field value to pixels for drawing. */
  const toPixels = (value) => (state.unit === '%' ? (value / 100) * shortSide() : value);

  function radii() {
    const read = (id) => clamp(Number($(id).value) || 0, 0, maxRadius());
    const all = read('radius');
    return CORNERS.map((corner) => toPixels(state.linked ? all : read(`r-${corner}`)));
  }

  /** Trace a rounded rectangle. If neighbouring radii overlap they are scaled down, as CSS does. */
  function roundedPath(ctx, w, h, [tl, tr, br, bl]) {
    const factor = Math.min(1, w / (tl + tr || 1), w / (bl + br || 1), h / (tl + bl || 1), h / (tr + br || 1));
    [tl, tr, br, bl] = [tl, tr, br, bl].map((r) => r * factor);
    ctx.beginPath();
    ctx.moveTo(tl, 0);
    ctx.lineTo(w - tr, 0);
    ctx.arcTo(w, 0, w, tr, tr);
    ctx.lineTo(w, h - br);
    ctx.arcTo(w, h, w - br, h, br);
    ctx.lineTo(bl, h);
    ctx.arcTo(0, h, 0, h - bl, bl);
    ctx.lineTo(0, tl);
    ctx.arcTo(0, 0, tl, 0, tl);
    ctx.closePath();
  }

  function draw(target, background) {
    const { width, height } = state.image;
    const ctx = target.getContext('2d');
    target.width = width;
    target.height = height;
    ctx.clearRect(0, 0, width, height);
    if (background) {
      ctx.fillStyle = background;
      ctx.fillRect(0, 0, width, height);
    }
    ctx.save();
    roundedPath(ctx, width, height, radii());
    ctx.clip();
    ctx.drawImage(state.image, 0, 0);
    ctx.restore();
  }

  const backgroundFor = (type) => (type === 'image/jpeg' ? $('bg-color').value : null);

  function syncFields(source) {
    if (state.linked) CORNERS.forEach((corner) => { $(`r-${corner}`).value = $('radius').value; });
    if (source === 'slider') $('radius').value = $('radius-range').value;
    if (source === 'number') $('radius-range').value = $('radius').value;
  }

  function render() {
    const max = maxRadius();
    $('radius-range').max = max;
    ['radius', ...CORNERS.map((c) => `r-${c}`)].forEach((id) => { $(id).max = max; });
    draw(canvas, backgroundFor($('corner-format').value));
    $('corner-info').innerHTML = `<span class="stat-chip">${uiText('Size:')} <strong>${state.image.width} × ${state.image.height}px</strong></span>` +
      `<span class="stat-chip">${uiText('Radius:')} <strong>${$('radius').value}${state.unit}</strong></span>`;
  }

  function setUnit(unit) {
    if (unit === state.unit) return;
    const factor = unit === '%' ? 100 / shortSide() : shortSide() / 100;
    const ids = ['radius', ...CORNERS.map((c) => `r-${c}`)];
    ids.forEach((id) => { $(id).value = Math.round((Number($(id).value) || 0) * factor); });
    state.unit = unit;
    $('radius-range').value = $('radius').value;
    $('unit-label').textContent = unit;
    render();
  }

  function setRadius(value) {
    $('radius').value = value;
    $('radius-range').value = value;
    syncFields();
    render();
  }

  function load(file) {
    if (!file || !file.type.startsWith('image/')) return;
    if (!checkFileSize(file, 20)) return;
    const img = new Image();
    const url = URL.createObjectURL(file);
    img.onload = () => {
      state.image = img;
      state.file = file;
      URL.revokeObjectURL(url);
      $('corner-card').classList.remove('is-hidden');
      const start = Math.round(shortSide() * 0.12);
      $('radius').value = $('radius-range').value = state.unit === '%' ? 12 : start;
      syncFields();
      render();
    };
    img.onerror = () => showStatus($('status-msg'), 'error', uiText('This file could not be read as an image.'));
    img.src = url;
  }

  $('file-input').addEventListener('change', (event) => load(event.target.files[0]));
  initDragDrop($('upload-zone'), (files) => load(files[0]));

  $('radius-range').addEventListener('input', () => { syncFields('slider'); render(); });
  $('radius').addEventListener('input', () => { syncFields('number'); render(); });
  CORNERS.forEach((corner) => $(`r-${corner}`).addEventListener('input', render));

  $('unit').addEventListener('change', () => setUnit($('unit').value));
  $('link-corners').addEventListener('change', () => {
    state.linked = $('link-corners').checked;
    $('corner-fields').classList.toggle('is-hidden', state.linked);
    syncFields();
    render();
  });

  document.querySelectorAll('[data-preset]').forEach((button) => {
    button.addEventListener('click', () => {
      const share = Number(button.dataset.preset);   // fraction of the maximum radius
      setRadius(Math.round(maxRadius() * share));
    });
  });

  $('corner-format').addEventListener('change', () => {
    $('bg-field').classList.toggle('is-hidden', $('corner-format').value !== 'image/jpeg');
    render();
  });
  $('bg-color').addEventListener('input', render);

  $('download-btn').addEventListener('click', () => {
    if (!state.image) return;
    const type = $('corner-format').value;
    const out = document.createElement('canvas');
    draw(out, backgroundFor(type));
    const ext = { 'image/png': 'png', 'image/jpeg': 'jpg', 'image/webp': 'webp' }[type];
    out.toBlob((blob) => {
      downloadBlob(blob, `${state.file.name.replace(/\.[^.]+$/, '')}_rounded.${ext}`);
      showStatus($('status-msg'), 'success', uiText('Saved {0} {1}.', formatSize(blob.size), ext.toUpperCase()));
    }, type, 0.92);
  });

  $('upload-another').addEventListener('click', () => {
    $('corner-card').classList.add('is-hidden');
    $('file-input').value = '';
    $('upload-zone').querySelector('.upload-preview')?.remove();
    $('upload-zone').classList.remove('has-files');
    $('file-input').click();
  });
}());
