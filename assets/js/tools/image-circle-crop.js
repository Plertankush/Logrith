/* Circle Image Cropper — drag and zoom a photo inside a round mask, then export at an exact size. */
(function () {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const canvas = $('circle-canvas');
  const MAX_SIZE = 4096;
  const MIN_SIZE = 32;

  const state = { image: null, file: null, size: 512, zoom: 1, offsetX: 0, offsetY: 0 };

  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

  /** Pixels per source pixel at zoom 1: the shorter image side exactly fills the circle. */
  function baseScale() {
    return state.size / Math.min(state.image.width, state.image.height);
  }

  /** Keep the image covering the whole circle so no empty edge shows. */
  function clampOffsets() {
    const scale = baseScale() * state.zoom;
    const maxX = Math.max(0, (state.image.width * scale - state.size) / 2);
    const maxY = Math.max(0, (state.image.height * scale - state.size) / 2);
    state.offsetX = clamp(state.offsetX, -maxX, maxX);
    state.offsetY = clamp(state.offsetY, -maxY, maxY);
  }

  function draw(target, size, background) {
    const ctx = target.getContext('2d');
    const scale = baseScale() * state.zoom * (size / state.size);
    const ratio = size / state.size;
    const width = state.image.width * scale;
    const height = state.image.height * scale;
    const border = Math.min(Number($('border-width').value) || 0, size / 2) * ratio;

    target.width = size;
    target.height = size;
    ctx.clearRect(0, 0, size, size);
    if (background) {
      ctx.fillStyle = background;
      ctx.fillRect(0, 0, size, size);
    }
    ctx.save();
    ctx.beginPath();
    ctx.arc(size / 2, size / 2, size / 2, 0, Math.PI * 2);
    ctx.clip();
    ctx.drawImage(state.image, size / 2 + state.offsetX * ratio - width / 2, size / 2 + state.offsetY * ratio - height / 2, width, height);
    ctx.restore();

    if (border > 0) {
      ctx.beginPath();
      ctx.arc(size / 2, size / 2, size / 2 - border / 2, 0, Math.PI * 2);
      ctx.lineWidth = border;
      ctx.strokeStyle = $('border-color').value;
      ctx.stroke();
    }
  }

  function backgroundFor(type) {
    return type === 'image/jpeg' ? $('bg-color').value : null;
  }

  function render() {
    clampOffsets();
    draw(canvas, state.size, backgroundFor($('circle-format').value));
    $('zoom-val').textContent = `${Math.round(state.zoom * 100)}%`;
    $('circle-info').innerHTML = `<span class="stat-chip">Output: <strong>${state.size} × ${state.size}px</strong></span>` +
      `<span class="stat-chip">Source: <strong>${state.image.width} × ${state.image.height}px</strong></span>`;
  }

  function setSize(value) {
    state.size = clamp(Math.round(Number(value) || 512), MIN_SIZE, MAX_SIZE);
    $('size-input').value = state.size;
    render();
  }

  function setZoom(value) {
    state.zoom = clamp(Number(value) || 1, 1, 4);
    $('zoom').value = state.zoom;
    render();
  }

  function resetPosition() {
    state.offsetX = 0;
    state.offsetY = 0;
    setZoom(1);
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
      $('circle-card').classList.remove('is-hidden');
      state.offsetX = 0;
      state.offsetY = 0;
      state.zoom = 1;
      $('zoom').value = 1;
      setSize(Math.min(1024, Math.min(img.naturalWidth, img.naturalHeight)));
    };
    img.onerror = () => showStatus($('status-msg'), 'error', 'This file could not be read as an image.');
    img.src = url;
  }

  /* Drag the photo inside the circle (mouse, touch and pen via pointer events). */
  let drag = null;
  canvas.addEventListener('pointerdown', (event) => {
    if (!state.image) return;
    canvas.setPointerCapture(event.pointerId);
    drag = { x: event.clientX, y: event.clientY, offsetX: state.offsetX, offsetY: state.offsetY };
    canvas.classList.add('is-dragging');
  });
  canvas.addEventListener('pointermove', (event) => {
    if (!drag) return;
    const factor = state.size / canvas.getBoundingClientRect().width;
    state.offsetX = drag.offsetX + (event.clientX - drag.x) * factor;
    state.offsetY = drag.offsetY + (event.clientY - drag.y) * factor;
    render();
  });
  const endDrag = () => { drag = null; canvas.classList.remove('is-dragging'); };
  canvas.addEventListener('pointerup', endDrag);
  canvas.addEventListener('pointercancel', endDrag);
  canvas.addEventListener('wheel', (event) => {
    if (!state.image) return;
    event.preventDefault();
    setZoom(state.zoom - Math.sign(event.deltaY) * 0.1);
  }, { passive: false });

  $('file-input').addEventListener('change', (event) => load(event.target.files[0]));
  initDragDrop($('upload-zone'), (files) => load(files[0]));

  $('zoom').addEventListener('input', () => setZoom($('zoom').value));
  $('size-input').addEventListener('change', () => setSize($('size-input').value));
  document.querySelectorAll('[data-size]').forEach((button) => {
    button.addEventListener('click', () => setSize(button.dataset.size));
  });
  ['border-width', 'border-color', 'bg-color'].forEach((id) => $(id).addEventListener('input', render));
  $('circle-format').addEventListener('change', () => {
    $('bg-field').classList.toggle('is-hidden', $('circle-format').value !== 'image/jpeg');
    render();
  });
  $('reset-btn').addEventListener('click', resetPosition);

  $('download-btn').addEventListener('click', () => {
    if (!state.image) return;
    const type = $('circle-format').value;
    const out = document.createElement('canvas');
    draw(out, state.size, backgroundFor(type));
    const ext = { 'image/png': 'png', 'image/jpeg': 'jpg', 'image/webp': 'webp' }[type];
    out.toBlob((blob) => {
      downloadBlob(blob, `${state.file.name.replace(/\.[^.]+$/, '')}_circle.${ext}`);
      showStatus($('status-msg'), 'success', `Saved ${formatSize(blob.size)} ${ext.toUpperCase()}.`);
    }, type, 0.92);
  });

  $('upload-another').addEventListener('click', () => {
    $('circle-card').classList.add('is-hidden');
    $('file-input').value = '';
    $('upload-zone').querySelector('.upload-preview')?.remove();
    $('upload-zone').classList.remove('has-files');
    $('file-input').click();
  });
}());
