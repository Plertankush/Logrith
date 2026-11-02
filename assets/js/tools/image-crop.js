/* Image Crop — draggable, resizable selection with ratio lock and exact numeric control.
   All coordinates are kept in natural image pixels; the overlay is positioned from them. */
(function () {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const stage = $('crop-stage');
  const img = $('crop-img');
  const box = $('crop-box');
  const inputs = { x: $('cx'), y: $('cy'), w: $('cw'), h: $('ch') };
  const info = $('crop-info');
  const status = $('status-msg');

  const MIN = 8;                       // smallest selection edge, in image pixels
  let file = null;
  let natural = { w: 0, h: 0 };
  let sel = { x: 0, y: 0, w: 0, h: 0 };
  let ratio = null;                    // width / height, or null for free-form
  let drag = null;

  const clamp = (v, lo, hi) => Math.min(Math.max(v, lo), hi);
  const scale = () => img.clientWidth / natural.w;

  /* ---- rendering ----------------------------------------------------- */
  function render() {
    if (!natural.w) return;
    const k = scale();
    box.hidden = false;
    box.style.cssText = `left:${sel.x * k}px;top:${sel.y * k}px;width:${sel.w * k}px;height:${sel.h * k}px`;
    inputs.x.value = Math.round(sel.x);
    inputs.y.value = Math.round(sel.y);
    inputs.w.value = Math.round(sel.w);
    inputs.h.value = Math.round(sel.h);
    info.innerHTML =
      `<span class="stat-chip">Image: <strong>${natural.w} × ${natural.h}px</strong></span>` +
      `<span class="stat-chip">Selection: <strong>${Math.round(sel.w)} × ${Math.round(sel.h)}px</strong></span>`;
  }

  /** Keep the selection inside the image and honour the ratio lock. */
  function normalise(next, anchor) {
    let { x, y, w, h } = next;
    w = clamp(w, MIN, natural.w);
    h = clamp(h, MIN, natural.h);
    if (ratio) {
      // Fit the ratio inside the requested size, then inside the image.
      if (w / h > ratio) w = h * ratio; else h = w / ratio;
      if (w > natural.w) { w = natural.w; h = w / ratio; }
      if (h > natural.h) { h = natural.h; w = h * ratio; }
      if (anchor) {                       // keep the fixed corner/edge where it was
        if (anchor.x === 'right') x = anchor.px - w;
        if (anchor.y === 'bottom') y = anchor.py - h;
      }
    }
    x = clamp(x, 0, natural.w - w);
    y = clamp(y, 0, natural.h - h);
    return { x, y, w, h };
  }

  function setSelection(next, anchor) {
    sel = normalise(next, anchor);
    render();
  }

  function centeredSelection(r) {
    let w = natural.w;
    let h = r ? w / r : natural.h;
    if (h > natural.h) { h = natural.h; w = h * r; }
    setSelection({ x: (natural.w - w) / 2, y: (natural.h - h) / 2, w, h });
  }

  /* ---- pointer interaction ------------------------------------------- */
  function toImage(event) {
    const rect = img.getBoundingClientRect();
    const k = scale();
    return { x: clamp((event.clientX - rect.left) / k, 0, natural.w), y: clamp((event.clientY - rect.top) / k, 0, natural.h) };
  }

  stage.addEventListener('pointerdown', (event) => {
    if (!natural.w || event.button > 0) return;
    const handle = event.target.dataset?.handle;
    const p = toImage(event);
    if (handle) drag = { mode: 'resize', handle, start: p, origin: { ...sel } };
    else if (event.target === box || box.contains(event.target)) drag = { mode: 'move', start: p, origin: { ...sel } };
    else drag = { mode: 'draw', start: p, origin: { ...sel } };
    stage.setPointerCapture(event.pointerId);
    event.preventDefault();
  });

  stage.addEventListener('pointermove', (event) => {
    if (!drag) return;
    const p = toImage(event);
    const o = drag.origin;
    const dx = p.x - drag.start.x;
    const dy = p.y - drag.start.y;

    if (drag.mode === 'move') {
      setSelection({ ...o, x: o.x + dx, y: o.y + dy });
    } else if (drag.mode === 'draw') {
      setSelection({ x: Math.min(p.x, drag.start.x), y: Math.min(p.y, drag.start.y),
                     w: Math.abs(dx), h: Math.abs(dy) },
                   { x: p.x < drag.start.x ? 'right' : 'left', px: drag.start.x,
                     y: p.y < drag.start.y ? 'bottom' : 'top', py: drag.start.y });
    } else {
      const hd = drag.handle;
      let { x, y, w, h } = o;
      if (hd.includes('e')) w = o.w + dx;
      if (hd.includes('s')) h = o.h + dy;
      if (hd.includes('w')) { w = o.w - dx; x = o.x + dx; }
      if (hd.includes('n')) { h = o.h - dy; y = o.y + dy; }
      if (w < 0 || h < 0) return;
      if (ratio && !hd.includes('n') && !hd.includes('s')) h = w / ratio;   // edge handles e/w
      if (ratio && !hd.includes('e') && !hd.includes('w')) w = h * ratio;   // edge handles n/s
      setSelection({ x, y, w, h }, {
        x: hd.includes('w') ? 'right' : 'left', px: o.x + o.w,
        y: hd.includes('n') ? 'bottom' : 'top', py: o.y + o.h,
      });
    }
  });

  const endDrag = () => { drag = null; };
  stage.addEventListener('pointerup', endDrag);
  stage.addEventListener('pointercancel', endDrag);
  window.addEventListener('resize', render);

  /* ---- numeric inputs and presets ------------------------------------ */
  Object.entries(inputs).forEach(([key, input]) => {
    input.addEventListener('input', () => {
      if (!natural.w) return;
      const v = parseFloat(input.value);
      if (Number.isNaN(v)) return;
      const next = { ...sel, [key]: v };
      if (ratio && key === 'w') next.h = v / ratio;
      if (ratio && key === 'h') next.w = v * ratio;
      setSelection(next);
    });
    input.addEventListener('change', render);
  });

  function setRatio(value, button) {
    document.querySelectorAll('[data-ratio]').forEach((b) => b.classList.toggle('is-active', b === button));
    if (value === 'free') { ratio = null; return; }
    ratio = value === 'original' ? natural.w / natural.h : value.split(':').reduce((a, b) => a / b);
    centeredSelection(ratio);
  }

  document.querySelectorAll('[data-ratio]').forEach((button) => {
    button.addEventListener('click', () => natural.w && setRatio(button.dataset.ratio, button));
  });

  $('crop-full').addEventListener('click', () => {
    if (!natural.w) return;
    setRatio('free', document.querySelector('[data-ratio="free"]'));
    setSelection({ x: 0, y: 0, w: natural.w, h: natural.h });
  });

  /* ---- loading ------------------------------------------------------- */
  function handleFile(next) {
    if (!next || !next.type.startsWith('image/')) return;
    if (!checkFileSize(next, 20)) return;
    file = next;
    const url = URL.createObjectURL(next);
    img.onload = () => {
      natural = { w: img.naturalWidth, h: img.naturalHeight };
      $('crop-card').classList.remove('is-hidden');
      $('output-card').classList.add('is-hidden');
      ratio = null;
      document.querySelectorAll('[data-ratio]').forEach((b) => b.classList.toggle('is-active', b.dataset.ratio === 'free'));
      // start with a centred selection covering 80% of the image so the handles are visible
      setSelection({ x: natural.w * 0.1, y: natural.h * 0.1, w: natural.w * 0.8, h: natural.h * 0.8 });
    };
    img.src = url;
  }

  $('file-input').addEventListener('change', (event) => handleFile(event.target.files[0]));
  initDragDrop($('upload-zone'), (files) => handleFile(files[0]));

  /* ---- output -------------------------------------------------------- */
  $('crop-btn').addEventListener('click', () => {
    if (!natural.w) { showStatus(status, 'error', 'Upload an image first.'); return; }
    const x = Math.round(sel.x), y = Math.round(sel.y), w = Math.round(sel.w), h = Math.round(sel.h);
    const type = $('crop-format').value;
    const canvas = document.createElement('canvas');
    canvas.width = w;
    canvas.height = h;
    const ctx = canvas.getContext('2d');
    if (type === 'image/jpeg') { ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, w, h); }
    ctx.drawImage(img, x, y, w, h, 0, 0, w, h);
    canvas.toBlob((blob) => {
      const ext = { 'image/png': 'png', 'image/jpeg': 'jpg', 'image/webp': 'webp' }[type];
      $('output-img').src = URL.createObjectURL(blob);
      $('output-stats').innerHTML =
        `<span class="stat-chip">Cropped: <strong>${w} × ${h}px</strong></span>` +
        `<span class="stat-chip">Size: <strong>${formatSize(blob.size)}</strong></span>`;
      $('output-card').classList.remove('is-hidden');
      showStatus(status, 'success', 'Image cropped!');
      $('download-btn').onclick = () => downloadBlob(blob, `${file.name.replace(/\.[^.]+$/, '')}_cropped.${ext}`);
      $('output-card').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, type, 0.92);
  });

  $('reset-btn').addEventListener('click', () => {
    $('crop-card').classList.add('is-hidden');
    $('output-card').classList.add('is-hidden');
    $('file-input').value = '';
    $('upload-zone').querySelector('.upload-preview')?.remove();
    $('upload-zone').classList.remove('has-files');
    natural = { w: 0, h: 0 };
    box.hidden = true;
  });
  $('crop-another').addEventListener('click', () => $('output-card').classList.add('is-hidden'));
}());
