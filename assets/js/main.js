/* ===== LOGRITH MAIN JS — FIXED ===== */

const ALL_TOOLS = [
  { name: 'Image Converter',           cat: 'Image',   url: 'tools/image-converter',       icon: '🔄' },
  { name: 'Image Compressor',          cat: 'Image',   url: 'tools/image-compressor',      icon: '📦' },
  { name: 'Image Resize',              cat: 'Image',   url: 'tools/image-resize',          icon: '↔️' },
  { name: 'Image Crop',                cat: 'Image',   url: 'tools/image-crop',            icon: '✂️' },
  { name: 'Image Rotate & Flip',       cat: 'Image',   url: 'tools/image-rotate',          icon: '🔃' },
  { name: 'PDF Merge',                 cat: 'PDF',     url: 'tools/pdf-merge',             icon: '📎' },
  { name: 'PDF Split',                 cat: 'PDF',     url: 'tools/pdf-split',             icon: '✂️' },
  { name: 'JPG to PDF',                cat: 'PDF',     url: 'tools/jpg-to-pdf',            icon: '🖼️' },
  { name: 'PDF to JPG',                cat: 'PDF',     url: 'tools/pdf-to-jpg',            icon: '📄' },
  { name: 'PDF Rotate',                cat: 'PDF',     url: 'tools/pdf-rotate',            icon: '🔃' },
  { name: 'JSON Formatter',            cat: 'Dev',     url: 'tools/json-formatter',        icon: '{ }' },
  { name: 'Base64 Encode/Decode',      cat: 'Dev',     url: 'tools/base64',                icon: '🔐' },
  { name: 'URL Encoder/Decoder',       cat: 'Dev',     url: 'tools/url-encoder',           icon: '🔗' },
  { name: 'Password Generator',        cat: 'Dev',     url: 'tools/password-generator',    icon: '🔑' },
  { name: 'Hash Generator',            cat: 'Dev',     url: 'tools/hash-generator',        icon: '#'  },
  { name: 'UUID Generator',            cat: 'Dev',     url: 'tools/uuid-generator',        icon: '🆔' },
  { name: 'Regex Tester',              cat: 'Dev',     url: 'tools/regex-tester',          icon: '🔍' },
  { name: 'Word Counter',              cat: 'Text',    url: 'tools/word-counter',          icon: '📝' },
  { name: 'Case Converter',            cat: 'Text',    url: 'tools/case-converter',        icon: 'Aa' },
  { name: 'Character Counter',         cat: 'Text',    url: 'tools/character-counter',     icon: '🔢' },
  { name: 'Lorem Ipsum Generator',     cat: 'Text',    url: 'tools/lorem-ipsum',           icon: '📃' },
  { name: 'Text Diff Checker',         cat: 'Text',    url: 'tools/text-diff',             icon: '🔍' },
  { name: 'Duplicate Line Remover',    cat: 'Text',    url: 'tools/duplicate-remover',     icon: '🧹' },
  { name: 'Slug Generator',            cat: 'Text',    url: 'tools/slug-generator',        icon: '🔗' },
  { name: 'QR Code Generator',         cat: 'Utility', url: 'tools/qr-generator',         icon: '▣'  },
  { name: 'Color Converter',           cat: 'Utility', url: 'tools/color-converter',       icon: '🎨' },
  { name: 'Age Calculator',            cat: 'Utility', url: 'tools/age-calculator',        icon: '📅' },
  { name: 'Unit Converter',            cat: 'Utility', url: 'tools/unit-converter',        icon: '📐' },
  { name: 'Percentage Calculator',     cat: 'Utility', url: 'tools/percentage-calculator', icon: '%'  },
  { name: 'GST Calculator',            cat: 'Utility', url: 'tools/gst-calculator',        icon: '💹' },
  { name: 'EMI Calculator',            cat: 'Utility', url: 'tools/emi-calculator',        icon: '💰' },
  { name: 'Password Strength Checker', cat: 'Utility', url: 'tools/password-strength',     icon: '🔒' },
  { name: 'PDF Inspector',             cat: 'Global',  url: 'tools/pdf-inspector',           icon: '📄' },
  { name: 'Image Privacy Cleaner',     cat: 'Global',  url: 'tools/image-privacy-cleaner',   icon: '🖼️' },
  { name: 'JSON Repair Tool',          cat: 'Global',  url: 'tools/json-repair',             icon: '{ }' },
  { name: 'CSV Cleaner',               cat: 'Global',  url: 'tools/csv-cleaner',             icon: '📊' },
  { name: 'AI Token & Context Calculator', cat: 'Global', url: 'tools/ai-context-calculator', icon: '🧮' },
  { name: 'Markdown to HTML',          cat: 'Global',  url: 'tools/markdown-to-html',        icon: '📝' },
  { name: 'URL Deduplicator',          cat: 'Global',  url: 'tools/url-deduplicator',        icon: '🔗' },
];

/* ─────────────────────────────────────────────────────────
   PATH PREFIX
   /index.html               → ''
   /tools/x.html             → '../'
   /categories/x.html        → '../'
   /pages/x.html             → '../'
   /blog/x.html               → '../'
───────────────────────────────────────────────────────── */
function getRootPrefix() {
  const path = window.location.pathname;
  if (/\/(tools|categories|pages|blog)\//.test(path)) return '../';
  return '';
}

/* ─────────────────────────────────────────────────────────
   SEARCH ENGINE — 1st letter se kaam kare
   Priority: word-start match > anywhere match > cat match
───────────────────────────────────────────────────────── */
function searchTools(q, limit) {
  limit = limit || 8;
  if (!q || !q.trim()) return [];
  const lq = q.toLowerCase().trim();
  const t1 = [], t2 = [], t3 = [];
  const seen = new Set();

  ALL_TOOLS.forEach(t => {
    const nl = t.name.toLowerCase();
    const cl = t.cat.toLowerCase();
    const wordMatch = nl.split(/[\s/\-&]+/).some(w => w.startsWith(lq));
    const nameMatch = nl.includes(lq);
    const catMatch  = cl.startsWith(lq);

    if (!seen.has(t.url)) {
      if (wordMatch)      { t1.push(t); seen.add(t.url); }
      else if (nameMatch) { t2.push(t); seen.add(t.url); }
      else if (catMatch)  { t3.push(t); seen.add(t.url); }
    }
  });

  return [...t1, ...t2, ...t3].slice(0, limit);
}

/* ─────────────────────────────────────────────────────────
   RENDER dropdown results into a container element
───────────────────────────────────────────────────────── */
function renderDropdown(container, results, prefix) {
  if (!container) return;
  if (!results.length) { container.style.display = 'none'; return; }
  container.innerHTML = results.map(t =>
    `<a href="${prefix}${t.url}">
       <span class="sr-icon">${t.icon}</span>
       <span class="sr-name">${t.name}</span>
       <span class="sr-cat">${t.cat}</span>
     </a>`
  ).join('');
  container.style.display = 'block';
}

/* ─────────────────────────────────────────────────────────
   ARROW KEY nav inside any dropdown container
───────────────────────────────────────────────────────── */
function handleArrows(e, container) {
  if (!container || (e.key !== 'ArrowDown' && e.key !== 'ArrowUp')) return;
  const links = [...container.querySelectorAll('a')];
  if (!links.length) return;
  const cur = container.querySelector('a.sr-active');
  let idx = links.indexOf(cur);
  idx = e.key === 'ArrowDown' ? (idx + 1) % links.length : (idx - 1 + links.length) % links.length;
  links.forEach(l => l.classList.remove('sr-active'));
  links[idx].classList.add('sr-active');
  e.preventDefault();
}

/* ─────────────────────────────────────────────────────────
   NAV SEARCH
   FIX: initSearch ko call karo with retry — component
   dynamically load hota hai, isliye direct DOMContentLoaded
   pe element nahi milta. MutationObserver use karte hain.
───────────────────────────────────────────────────────── */
function setupNavSearch() {
  const input   = document.getElementById('nav-search-input');
  const results = document.getElementById('search-results');
  if (!input || !results) return false; // not ready yet

  const prefix = getRootPrefix();

  function doNavSearch() {
    const q = input.value.trim();
    if (!q) { results.style.display = 'none'; return; }
    renderDropdown(results, searchTools(q, 8), prefix);
  }
  input.addEventListener('input', doNavSearch);
  input.addEventListener('keyup', doNavSearch);  // extra fallback for some mobile keyboards
  input.addEventListener('focus', doNavSearch);  // show results if text already typed

  document.addEventListener('click', e => {
    if (!input.contains(e.target) && !results.contains(e.target))
      results.style.display = 'none';
  });

  input.addEventListener('keydown', e => {
    if (e.key === 'Escape') { results.style.display = 'none'; input.blur(); return; }
    if (e.key === 'Enter') {
      const a = results.querySelector('a.sr-active') || results.querySelector('a');
      if (a) { window.location = a.href; return; }
    }
    handleArrows(e, results);
  });

  return true;
}

/* ─────────────────────────────────────────────────────────
   HAMBURGER MENU
   FIX: Same MutationObserver approach — navbar dynamically
   inject hota hai, button baad mein aata hai DOM mein
───────────────────────────────────────────────────────── */
function setupHamburger() {
  const btn   = document.getElementById('hamburger');
  const mNav  = document.getElementById('mobile-nav');
  const close = document.getElementById('mobile-close');
  if (!btn || !mNav) return false;

  // Remove any old listeners by cloning
  const newBtn = btn.cloneNode(true);
  btn.parentNode.replaceChild(newBtn, btn);

  newBtn.addEventListener('click', () => mNav.classList.add('open'));
  if (close) {
    const newClose = close.cloneNode(true);
    close.parentNode.replaceChild(newClose, close);
    newClose.addEventListener('click', () => mNav.classList.remove('open'));
  }

  // Close on overlay click
  mNav.addEventListener('click', e => {
    if (e.target === mNav) mNav.classList.remove('open');
  });

  return true;
}

/* ─────────────────────────────────────────────────────────
   WATCH DOM for dynamically injected navbar/mobile-nav
   Yahi main fix hai — navbar component inject hone ke
   baad hi listeners lagao
───────────────────────────────────────────────────────── */
function watchForComponents() {
  let navDone  = false;
  let hambDone = false;

  // Try immediately first
  navDone  = setupNavSearch();
  hambDone = setupHamburger();

  if (navDone && hambDone) return; // already in DOM, done

  // Otherwise watch for changes
  const observer = new MutationObserver(() => {
    if (!navDone)  navDone  = setupNavSearch();
    if (!hambDone) hambDone = setupHamburger();
    if (navDone && hambDone) observer.disconnect();
  });

  observer.observe(document.body, { childList: true, subtree: true });

  // Safety fallback after 3s
  setTimeout(() => {
    observer.disconnect();
    if (!navDone)  setupNavSearch();
    if (!hambDone) setupHamburger();
  }, 3000);
}

/* ─────────────────────────────────────────────────────────
   HERO SEARCH
   FIX: Dropdown #hero-search-results positioned absolute
   over page (z-index:9999). Hero overflow:visible in CSS.
   Mobile pe nav search hide, hero search hi kaam kare.
───────────────────────────────────────────────────────── */
function initHeroSearch() {
  const input   = document.getElementById('hero-search');
  const btn     = document.getElementById('hero-search-btn');
  const results = document.getElementById('hero-search-results');
  if (!input) return;

  const prefix = getRootPrefix();

  // Live results on input
  input.addEventListener('input', () => {
    if (!results) return;
    const q = input.value.trim();
    if (!q) { results.style.display = 'none'; return; }
    renderDropdown(results, searchTools(q, 6), prefix);
  });

  // Close on outside click
  document.addEventListener('click', e => {
    if (!results) return;
    if (!input.contains(e.target) && !results.contains(e.target) && !(btn && btn.contains(e.target)))
      results.style.display = 'none';
  });

  // Navigate
  function go() {
    const q = input.value.trim();
    if (!q) return;
    if (results) {
      const a = results.querySelector('a.sr-active') || results.querySelector('a');
      if (a) { window.location = a.href; return; }
    }
    const found = searchTools(q, 1);
    window.location = found.length ? prefix + found[0].url : '#all-tools';
  }

  if (btn) btn.addEventListener('click', go);
  input.addEventListener('keydown', e => {
    if (e.key === 'Enter') { go(); return; }
    if (e.key === 'Escape') { if (results) results.style.display = 'none'; return; }
    if (results) handleArrows(e, results);
  });
}

/* ─────────────────────────────────────────────────────────
   FAQ
───────────────────────────────────────────────────────── */
function initFAQ() {
  document.querySelectorAll('.faq-q').forEach(q => {
    q.addEventListener('click', () => q.closest('.faq-item').classList.toggle('open'));
  });
}

/* ─────────────────────────────────────────────────────────
   UTILITIES — unchanged
───────────────────────────────────────────────────────── */
function copyText(text, btn) {
  navigator.clipboard.writeText(text).then(() => {
    const orig = btn.textContent;
    btn.textContent = '✓ Copied!';
    btn.style.background = 'var(--success)';
    btn.style.color = 'white';
    setTimeout(() => { btn.textContent = orig; btn.style.background = ''; btn.style.color = ''; }, 2000);
  });
}
function showStatus(el, type, msg) {
  el.className = `status-msg ${type}`;
  const icons = { success: '✅', error: '❌', info: 'ℹ️' };
  el.innerHTML = `${icons[type] || ''} ${msg}`;
  el.style.display = 'flex';
  if (type === 'success') setTimeout(() => { el.style.display = 'none'; }, 4000);
}
function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / 1048576).toFixed(2) + ' MB';
}
function checkFileSize(file, maxMB = 20) {
  if (file.size > maxMB * 1048576) { alert(`File too large. Max ${maxMB}MB allowed.`); return false; }
  return true;
}
function initDragDrop(zone, onFiles) {
  zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('dragover'); });
  zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
  zone.addEventListener('drop', e => {
    e.preventDefault(); zone.classList.remove('dragover');
    if (e.dataTransfer.files.length) onFiles(e.dataTransfer.files);
  });
}
function downloadCanvas(canvas, filename) {
  const a = document.createElement('a'); a.download = filename;
  a.href = canvas.toDataURL('image/png'); a.click();
}
function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a'); a.href = url; a.download = filename; a.click();
  setTimeout(() => URL.revokeObjectURL(url), 5000);
}

/* ─────────────────────────────────────────────────────────
   INIT
───────────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  initHeroSearch();
  initFAQ();
  watchForComponents(); // handles nav search + hamburger with retry
});

/* ─────────────────────────────────────────────────────────
   DRAWER GLOBALS — window pe taaki navbar inline onclick kaam kare
───────────────────────────────────────────────────────── */
window.openDrawer = function() {
  var nav = document.getElementById('mobile-nav');
  var ov  = document.getElementById('mob-overlay');
  if (nav) nav.classList.add('open');
  if (ov)  ov.classList.add('open');
  document.body.classList.add('drawer-open');
};

window.closeDrawer = function() {
  var nav = document.getElementById('mobile-nav');
  var ov  = document.getElementById('mob-overlay');
  if (nav) nav.classList.remove('open');
  if (ov)  ov.classList.remove('open');
  document.body.classList.remove('drawer-open');
};

window.toggleMobCat = function(header) {
  var group = header.parentElement;
  document.querySelectorAll('.mob-cat-group.open').forEach(function(g) {
    if (g !== group) g.classList.remove('open');
  });
  group.classList.toggle('open');
};

document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') window.closeDrawer();
});

/* Fade-in effect */
window.onload = () => {
  document.body.classList.add('loaded');
};