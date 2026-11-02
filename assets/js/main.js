/* ==========================================================================
   Logrith — shared site script
   --------------------------------------------------------------------------
   1. Shared header & footer  (loaded from /components)
   2. Tool search             (header + home page)
   3. Helpers used by tool pages (copy, status messages, downloads, drag & drop)
   4. AdSense loader
   ========================================================================== */

(function () {
  'use strict';

  const ADSENSE_CLIENT = 'ca-pub-2892592901355098';
  const SEARCH_INDEX_URL = '/assets/data/tools.json';
  const MAX_RESULTS = 8;


  /* 1. Shared header & footer
     ====================================================================== */
  async function loadPartial(slotId, url) {
    const slot = document.getElementById(slotId);
    if (!slot) return null;
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`${url}: ${response.status}`);
      slot.innerHTML = await response.text();
      return slot;
    } catch (error) {
      console.error('Could not load shared component', error);
      return null;
    }
  }

  function markCurrentLinks(root) {
    const path = location.pathname.replace(/\/index\.html$/, '/').replace(/\.html$/, '');
    root.querySelectorAll('.site-nav a').forEach((link) => {
      if (new URL(link.href).pathname === path) link.setAttribute('aria-current', 'page');
    });
  }

  async function initChrome() {
    const [header] = await Promise.all([
      loadPartial('navbar', '/components/navbar.html'),
      loadPartial('footer', '/components/footer.html'),
    ]);
    if (!header) return;
    markCurrentLinks(header);
    const input = header.querySelector('[data-tool-search]');
    if (input) initToolSearch(input);
  }


  /* 2. Tool search
     ====================================================================== */
  let searchIndex = null;

  function loadSearchIndex() {
    if (!searchIndex) {
      searchIndex = fetch(SEARCH_INDEX_URL)
        .then((response) => response.json())
        .catch(() => []);
    }
    return searchIndex;
  }

  function scoreTool(tool, terms) {
    const name = tool.name.toLowerCase();
    const words = name.split(/[\s/&-]+/);
    const extra = `${tool.category} ${tool.summary}`.toLowerCase();
    let score = 0;
    for (const term of terms) {
      if (name.startsWith(term)) score += 4;
      else if (words.some((word) => word.startsWith(term))) score += 3;
      else if (name.includes(term)) score += 2;
      else if (extra.includes(term)) score += 1;
      else return 0;
    }
    return score;
  }

  function searchTools(tools, query) {
    const terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) return [];
    return tools
      .map((tool) => ({ tool, score: scoreTool(tool, terms) }))
      .filter((entry) => entry.score > 0)
      .sort((a, b) => b.score - a.score || a.tool.name.localeCompare(b.tool.name))
      .slice(0, MAX_RESULTS)
      .map((entry) => entry.tool);
  }

  function escapeHtml(value) {
    return value.replace(/[&<>"']/g, (ch) => (
      { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]
    ));
  }

  /**
   * Attach live search to an input. The results container is found through the
   * input's `data-results` selector, or created next to the input.
   */
  function initToolSearch(input) {
    let results = input.dataset.results ? document.querySelector(input.dataset.results) : null;
    if (!results) {
      results = document.createElement('div');
      results.className = 'search-results';
      input.insertAdjacentElement('afterend', results);
    }
    results.setAttribute('role', 'listbox');
    results.hidden = true;
    input.setAttribute('aria-expanded', 'false');

    const close = () => {
      results.hidden = true;
      input.setAttribute('aria-expanded', 'false');
    };

    const links = () => [...results.querySelectorAll('a')];

    function move(step) {
      const items = links();
      if (!items.length) return;
      const current = items.findIndex((item) => item.classList.contains('is-active'));
      items.forEach((item) => item.classList.remove('is-active'));
      const next = (current + step + items.length) % items.length;
      items[next].classList.add('is-active');
      items[next].scrollIntoView({ block: 'nearest' });
    }

    async function update() {
      const query = input.value.trim();
      if (!query) return close();
      const matches = searchTools(await loadSearchIndex(), query);
      results.innerHTML = matches.length
        ? matches.map((tool) => (
            `<a role="option" href="${tool.url}">` +
            `<span class="sr-name">${escapeHtml(tool.name)}</span>` +
            `<span class="sr-cat">${escapeHtml(tool.category)}</span></a>`
          )).join('')
        : '<div class="sr-empty">No tools found</div>';
      results.hidden = false;
      input.setAttribute('aria-expanded', 'true');
    }

    input.addEventListener('focus', loadSearchIndex, { once: true });
    input.addEventListener('input', update);
    input.addEventListener('keydown', (event) => {
      if (event.key === 'ArrowDown') { event.preventDefault(); move(1); }
      else if (event.key === 'ArrowUp') { event.preventDefault(); move(-1); }
      else if (event.key === 'Escape') { close(); input.blur(); }
      else if (event.key === 'Enter') {
        const target = results.querySelector('a.is-active') || results.querySelector('a');
        if (target) { event.preventDefault(); location.href = target.href; }
      }
    });
    const submit = input.dataset.submit ? document.querySelector(input.dataset.submit) : null;
    if (submit) {
      submit.addEventListener('click', async () => {
        const matches = searchTools(await loadSearchIndex(), input.value.trim());
        if (matches.length) location.href = matches[0].url;
        else input.focus();
      });
    }
    document.addEventListener('click', (event) => {
      if (!input.contains(event.target) && !results.contains(event.target)) close();
    });
  }



  /* 3b. Upload preview
     Every image/PDF upload zone shows what was picked (thumbnail + name + size)
     instead of only a file name. Works for click-to-browse and drag & drop.
     ====================================================================== */
  const previewUrls = new WeakMap();

  function fileSize(bytes) {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / 1048576).toFixed(2)} MB`;
  }

  function renderUploadPreview(zone, files) {
    (previewUrls.get(zone) || []).forEach((url) => URL.revokeObjectURL(url));
    previewUrls.set(zone, []);
    zone.querySelector('.upload-preview')?.remove();
    zone.classList.remove('has-files');
    const list = [...files].slice(0, 12);
    if (!list.length) return;

    const urls = [];
    const wrap = document.createElement('div');
    wrap.className = 'upload-preview' + (list.length === 1 ? ' is-single' : '');
    list.forEach((file) => {
      const item = document.createElement('figure');
      item.className = 'upload-item';
      if (file.type.startsWith('image/')) {
        const img = document.createElement('img');
        img.alt = file.name;
        img.src = URL.createObjectURL(file);
        urls.push(img.src);
        item.appendChild(img);
      } else {
        item.insertAdjacentHTML('beforeend', `<span class="upload-file-icon">${icon(file.type === 'application/pdf' ? 'pdf' : 'file')}</span>`);
      }
      const caption = document.createElement('figcaption');
      caption.textContent = `${file.name} · ${fileSize(file.size)}`;
      item.appendChild(caption);
      wrap.appendChild(item);
    });
    const hint = document.createElement('p');
    hint.className = 'upload-replace';
    hint.textContent = 'Click or drop to replace';
    wrap.appendChild(hint);
    previewUrls.set(zone, urls);
    zone.appendChild(wrap);
    zone.classList.add('has-files');
  }

  window.renderUploadPreview = renderUploadPreview;

  document.addEventListener('change', (event) => {
    const input = event.target;
    if (!(input instanceof HTMLInputElement) || input.type !== 'file') return;
    const zone = input.closest('.upload-zone');
    if (!zone || !/image|pdf/i.test(input.accept)) return;
    renderUploadPreview(zone, input.files);
  });

  /* 4. AdSense loader
     ====================================================================== */
  function loadAds() {
    const script = document.createElement('script');
    script.async = true;
    script.crossOrigin = 'anonymous';
    script.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${ADSENSE_CLIENT}`;
    document.head.appendChild(script);
  }


  /* Boot
     ====================================================================== */
  loadAds();
  initChrome();
  document.querySelectorAll('[data-tool-search]').forEach((input) => {
    if (!input.closest('#navbar')) initToolSearch(input);
  });
}());


/* 3. Helpers used by tool pages
   --------------------------------------------------------------------------
   These stay global on purpose: tool pages call them from inline handlers.
   ========================================================================== */

function icon(name) {
  return `<svg class="icon icon-inline" aria-hidden="true"><use href="/assets/svg/icons.svg#${name}"></use></svg>`;
}

function copyText(text, button) {
  navigator.clipboard.writeText(text).then(() => {
    const original = button.innerHTML;
    button.innerHTML = `${icon('check')} Copied`;
    button.classList.add('is-copied');
    setTimeout(() => {
      button.innerHTML = original;
      button.classList.remove('is-copied');
    }, 2000);
  });
}

function showStatus(element, type, message) {
  const icons = { success: 'check-circle', error: 'x-circle', info: 'info' };
  element.className = `status-msg ${type}`;
  element.innerHTML = `${icons[type] ? icon(icons[type]) : ''} ${message}`;
  element.style.display = 'flex';
  if (type === 'success') setTimeout(() => { element.style.display = 'none'; }, 4000);
}

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1048576).toFixed(2)} MB`;
}

function checkFileSize(file, maxMB = 20) {
  if (file.size > maxMB * 1048576) {
    alert(`File too large. Max ${maxMB}MB allowed.`);
    return false;
  }
  return true;
}

function initDragDrop(zone, onFiles) {
  zone.addEventListener('dragover', (event) => { event.preventDefault(); zone.classList.add('dragover'); });
  zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
  zone.addEventListener('drop', (event) => {
    event.preventDefault();
    zone.classList.remove('dragover');
    if (event.dataTransfer.files.length) {
      if (window.renderUploadPreview && /image|pdf/i.test(zone.querySelector('input[type=file]')?.accept || '')) {
        window.renderUploadPreview(zone, event.dataTransfer.files);
      }
      onFiles(event.dataTransfer.files);
    }
  });
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 5000);
}

function downloadCanvas(canvas, filename) {
  const link = document.createElement('a');
  link.download = filename;
  link.href = canvas.toDataURL('image/png');
  link.click();
}
