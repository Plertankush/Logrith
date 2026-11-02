/* Image Rotate & Flip — 90° steps, flips and a free angle, with a live preview. */
(function () {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const preview = $('preview-canvas');
  const slider = $('angle');
  const number = $('angle-num');

  let base = null;       // image with the 90° steps and flips applied
  let original = null;   // untouched upload, used by "Reset"
  let file = null;
  let angle = 0;         // extra free rotation in degrees

  /** Render `source` rotated by `deg` onto a canvas that is just large enough to hold it. */
  function rotated(source, deg, fill) {
    const rad = (deg * Math.PI) / 180;
    const sin = Math.abs(Math.sin(rad));
    const cos = Math.abs(Math.cos(rad));
    const w = Math.round(source.width * cos + source.height * sin);
    const h = Math.round(source.width * sin + source.height * cos);
    const out = document.createElement('canvas');
    out.width = w;
    out.height = h;
    const ctx = out.getContext('2d');
    if (fill) { ctx.fillStyle = fill; ctx.fillRect(0, 0, w, h); }
    ctx.translate(w / 2, h / 2);
    ctx.rotate(rad);
    ctx.drawImage(source, -source.width / 2, -source.height / 2);
    return out;
  }

  function result(fill) {
    return angle ? rotated(base, angle, fill) : base;
  }

  function render() {
    const out = result(null);
    preview.width = out.width;
    preview.height = out.height;
    preview.getContext('2d').drawImage(out, 0, 0);
    $('angle-val').textContent = `${angle}°`;
    $('transform-info').innerHTML = `<span class="stat-chip">Size: <strong>${out.width} × ${out.height}px</strong></span>` +
      `<span class="stat-chip">Extra rotation: <strong>${angle}°</strong></span>`;
  }

  function setAngle(value) {
    angle = Math.max(-180, Math.min(180, Math.round(Number(value) || 0)));
    slider.value = number.value = angle;
    render();
  }

  function transform(type) {
    const w = base.width;
    const h = base.height;
    const swap = type === 'rot90' || type === 'rot270';
    const out = document.createElement('canvas');
    out.width = swap ? h : w;
    out.height = swap ? w : h;
    const ctx = out.getContext('2d');
    if (type === 'rot90') { ctx.translate(h, 0); ctx.rotate(Math.PI / 2); }
    else if (type === 'rot180') { ctx.translate(w, h); ctx.rotate(Math.PI); }
    else if (type === 'rot270') { ctx.translate(0, w); ctx.rotate(-Math.PI / 2); }
    else if (type === 'flipH') { ctx.translate(w, 0); ctx.scale(-1, 1); }
    else if (type === 'flipV') { ctx.translate(0, h); ctx.scale(1, -1); }
    ctx.drawImage(base, 0, 0);
    base = out;
    render();
  }

  function load(next) {
    if (!next || !next.type.startsWith('image/')) return;
    if (!checkFileSize(next, 20)) return;
    file = next;
    const img = new Image();
    const url = URL.createObjectURL(next);
    img.onload = () => {
      original = document.createElement('canvas');
      original.width = img.naturalWidth;
      original.height = img.naturalHeight;
      original.getContext('2d').drawImage(img, 0, 0);
      URL.revokeObjectURL(url);
      base = original;
      $('controls-card').classList.remove('is-hidden');
      setAngle(0);
    };
    img.src = url;
  }

  $('file-input').addEventListener('change', (event) => load(event.target.files[0]));
  initDragDrop($('upload-zone'), (files) => load(files[0]));

  $('rot-cw').addEventListener('click', () => transform('rot90'));
  $('rot-ccw').addEventListener('click', () => transform('rot270'));
  $('rot-180').addEventListener('click', () => transform('rot180'));
  $('flip-h').addEventListener('click', () => transform('flipH'));
  $('flip-v').addEventListener('click', () => transform('flipV'));
  slider.addEventListener('input', () => setAngle(slider.value));
  number.addEventListener('input', () => setAngle(number.value));

  $('reset-transforms').addEventListener('click', () => { base = original; setAngle(0); });
  $('upload-another').addEventListener('click', () => {
    $('controls-card').classList.add('is-hidden');
    $('file-input').value = '';
    $('upload-zone').querySelector('.upload-preview')?.remove();
    $('upload-zone').classList.remove('has-files');
    $('file-input').click();
  });

  $('download-btn').addEventListener('click', () => {
    if (!base) return;
    const type = $('rotate-format').value;
    const out = result(type === 'image/jpeg' ? '#ffffff' : null);
    const ext = { 'image/png': 'png', 'image/jpeg': 'jpg', 'image/webp': 'webp' }[type];
    out.toBlob((blob) => downloadBlob(blob, `${file.name.replace(/\.[^.]+$/, '')}_rotated.${ext}`), type, 0.92);
  });
}());
