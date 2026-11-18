/* JSON ⇄ CSV Converter — flattens nested JSON for CSV and rebuilds JSON from CSV. */
(function () {
  'use strict';

  const $ = (id) => document.getElementById(id);
  let mode = 'json-to-csv';

  const SAMPLES = {
    'json-to-csv': '[\n  {"id": 1, "name": "Asha", "address": {"city": "Pune", "zip": "411001"}, "tags": ["admin", "beta"]},\n  {"id": 2, "name": "Liam", "address": {"city": "Leeds", "zip": "LS1"}, "tags": []}\n]',
    'csv-to-json': 'id,name,city\n1,Asha,Pune\n2,"Smith, Liam",Leeds',
  };

  const delimiter = () => ({ comma: ',', semicolon: ';', tab: '\t' }[$('delimiter').value]);

  /** Flatten nested objects to dot-notation keys. Arrays are stored as JSON text in one cell. */
  function flatten(value, prefix = '', out = {}) {
    if (value !== null && typeof value === 'object' && !Array.isArray(value)) {
      const keys = Object.keys(value);
      if (!keys.length && prefix) out[prefix] = '';
      keys.forEach((key) => flatten(value[key], prefix ? `${prefix}.${key}` : key, out));
    } else {
      out[prefix] = Array.isArray(value) ? JSON.stringify(value) : value;
    }
    return out;
  }

  function csvCell(value, sep) {
    if (value === null || value === undefined) return '';
    const text = String(value);
    return text.includes('"') || text.includes('\n') || text.includes('\r') || text.includes(sep) ? `"${text.replace(/"/g, '""')}"` : text;
  }

  function jsonToCsv(text) {
    const data = JSON.parse(text);
    const rows = (Array.isArray(data) ? data : [data]).map((item) => (item !== null && typeof item === 'object' ? (Array.isArray(item) ? { value: JSON.stringify(item) } : $('flatten').checked ? flatten(item) : item) : { value: item }));
    const columns = [];
    rows.forEach((row) => Object.keys(row).forEach((key) => { if (!columns.includes(key)) columns.push(key); }));
    const sep = delimiter();
    const cell = (v) => csvCell(typeof v === 'object' && v !== null ? JSON.stringify(v) : v, sep);
    const lines = rows.map((row) => columns.map((col) => cell(row[col])).join(sep));
    if ($('header').checked) lines.unshift(columns.map((c) => csvCell(c, sep)).join(sep));
    return { text: lines.join('\n'), count: rows.length };
  }

  /** RFC 4180 style parser: quoted fields, doubled quotes and line breaks inside quotes. */
  function parseCsv(text, sep) {
    const rows = [];
    let row = [];
    let field = '';
    let quoted = false;
    for (let i = 0; i < text.length; i += 1) {
      const ch = text[i];
      if (quoted) {
        if (ch === '"' && text[i + 1] === '"') { field += '"'; i += 1; }
        else if (ch === '"') quoted = false;
        else field += ch;
      } else if (ch === '"') quoted = true;
      else if (ch === sep) { row.push(field); field = ''; }
      else if (ch === '\n' || ch === '\r') {
        if (ch === '\r' && text[i + 1] === '\n') i += 1;
        row.push(field); rows.push(row); row = []; field = '';
      } else field += ch;
    }
    if (field !== '' || row.length) { row.push(field); rows.push(row); }
    return rows.filter((r) => r.some((c) => c !== ''));
  }

  function typed(value) {
    if (!$('types').checked) return value;
    if (value === '') return value;
    if (value === 'true') return true;
    if (value === 'false') return false;
    if (value === 'null') return null;
    if (/^-?(0|[1-9]\d*)(\.\d+)?$/.test(value)) return Number(value);
    return value;
  }

  function csvToJson(text) {
    const rows = parseCsv(text, delimiter());
    if (!rows.length) throw new Error(uiText('No CSV rows found.'));
    const header = $('header').checked ? rows.shift() : rows[0].map((_, i) => `column${i + 1}`);
    const objects = rows.map((row) => Object.fromEntries(header.map((key, i) => [key, typed(row[i] ?? '')])));
    return { text: JSON.stringify(objects, null, 2), count: objects.length };
  }

  function convert() {
    const status = $('status-msg');
    try {
      const result = mode === 'json-to-csv' ? jsonToCsv($('input-text').value) : csvToJson($('input-text').value);
      $('output-text').value = result.text;
      showStatus(status, 'success', uiText(result.count === 1 ? 'Converted {0} record.' : 'Converted {0} records.', result.count));
    } catch (error) {
      $('output-text').value = '';
      showStatus(status, 'error', mode === 'json-to-csv' ? uiText('Invalid JSON: {0}', error.message) : error.message);
    }
  }

  function setMode(next) {
    mode = next;
    document.querySelectorAll('.mode-card').forEach((card) => card.classList.toggle('active', card.dataset.mode === next));
    const toCsv = next === 'json-to-csv';
    $('input-label').textContent = toCsv ? 'JSON Input' : 'CSV Input';
    $('output-label').textContent = toCsv ? 'CSV Output' : 'JSON Output';
    $('flatten-field').classList.toggle('is-hidden', !toCsv);
    $('types-field').classList.toggle('is-hidden', toCsv);
    $('input-text').value = SAMPLES[next];
    $('output-text').value = '';
    $('status-msg').style.display = 'none';
  }

  document.querySelectorAll('.mode-card').forEach((card) => card.addEventListener('click', () => setMode(card.dataset.mode)));
  $('convert-btn').addEventListener('click', convert);
  $('copy-btn').addEventListener('click', () => copyText($('output-text').value, $('copy-btn')));
  $('download-btn').addEventListener('click', () => {
    const out = $('output-text').value;
    if (!out) return;
    const toCsv = mode === 'json-to-csv';
    downloadBlob(new Blob([out], { type: toCsv ? 'text/csv' : 'application/json' }), toCsv ? 'data.csv' : 'data.json');
  });
  $('swap-btn').addEventListener('click', () => {
    const output = $('output-text').value;
    setMode(mode === 'json-to-csv' ? 'csv-to-json' : 'json-to-csv');
    if (output) $('input-text').value = output;
  });

  setMode('json-to-csv');
  convert();
}());
