/* Unix Timestamp Converter — epoch to date and date to epoch, with a live clock and time zones. */
(function () {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const ZONES = ['UTC', 'America/New_York', 'America/Los_Angeles', 'Europe/London', 'Europe/Berlin', 'Asia/Kolkata', 'Asia/Singapore', 'Asia/Tokyo', 'Australia/Sydney'];
  const LOCAL = Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC';

  /** Guess the unit from the number of digits: s (10), ms (13), µs (16), ns (19). */
  function toMilliseconds(raw) {
    const value = Number(raw);
    const digits = String(Math.trunc(Math.abs(value))).length;
    if (digits >= 18) return { ms: value / 1e6, unit: 'nanoseconds' };
    if (digits >= 15) return { ms: value / 1e3, unit: 'microseconds' };
    if (digits >= 12) return { ms: value, unit: 'milliseconds' };
    return { ms: value * 1000, unit: 'seconds' };
  }

  function format(date, zone) {
    return new Intl.DateTimeFormat('en-GB', {
      timeZone: zone, year: 'numeric', month: 'short', day: '2-digit', weekday: 'short',
      hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false, timeZoneName: 'short',
    }).format(date);
  }

  function relative(ms) {
    const diff = ms - Date.now();
    const units = [['year', 31557600000], ['month', 2629800000], ['day', 86400000], ['hour', 3600000], ['minute', 60000], ['second', 1000]];
    const formatter = new Intl.RelativeTimeFormat('en', { numeric: 'auto' });
    for (const [unit, size] of units) {
      if (Math.abs(diff) >= size || unit === 'second') return formatter.format(Math.round(diff / size), unit);
    }
    return '';
  }

  function row(label, value) {
    return `<div class="result-row"><span class="result-label">${label}</span><code>${value}</code></div>`;
  }

  function showTimestamp() {
    const raw = $('ts-input').value.trim();
    const out = $('ts-output');
    if (!/^-?\d+(\.\d+)?$/.test(raw)) {
      out.innerHTML = raw ? '<p class="mini-note">Enter digits only, for example 1735689600.</p>' : '';
      return;
    }
    const { ms, unit } = toMilliseconds(raw);
    const date = new Date(ms);
    if (Number.isNaN(date.getTime())) { out.innerHTML = '<p class="mini-note">That number is out of range.</p>'; return; }
    const zone = $('ts-zone').value;
    out.innerHTML = row('Detected unit', unit) +
      row('UTC (ISO 8601)', date.toISOString()) +
      row(zone === 'local' ? `Local (${LOCAL})` : zone, format(date, zone === 'local' ? LOCAL : zone)) +
      row('Relative', relative(ms)) +
      row('Seconds', Math.floor(ms / 1000)) +
      row('Milliseconds', Math.floor(ms));
  }

  /** Convert a date-time typed as wall-clock time in `zone` into epoch milliseconds. */
  function zonedToEpoch(local, zone) {
    const [datePart, timePart = '00:00:00'] = local.split('T');
    const [y, m, d] = datePart.split('-').map(Number);
    const [hh, mm, ss = 0] = timePart.split(':').map(Number);
    const asUtc = Date.UTC(y, m - 1, d, hh, mm, Number(ss));
    if (zone === 'UTC') return asUtc;
    const tz = zone === 'local' ? LOCAL : zone;
    // Find the zone offset at that instant, then correct once (handles daylight saving shifts).
    const offsetAt = (ms) => {
      const parts = new Intl.DateTimeFormat('en-US', { timeZone: tz, hourCycle: 'h23', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit' }).formatToParts(new Date(ms));
      const get = (type) => Number(parts.find((p) => p.type === type).value);
      return Date.UTC(get('year'), get('month') - 1, get('day'), get('hour'), get('minute'), get('second')) - ms;
    };
    let guess = asUtc - offsetAt(asUtc);
    guess = asUtc - offsetAt(guess);
    return guess;
  }

  function showDate() {
    const value = $('date-input').value;
    const out = $('date-output');
    if (!value) { out.innerHTML = ''; return; }
    const ms = zonedToEpoch(value, $('date-zone').value);
    if (Number.isNaN(ms)) { out.innerHTML = ''; return; }
    out.innerHTML = row('Seconds', Math.floor(ms / 1000)) + row('Milliseconds', ms) + row('UTC (ISO 8601)', new Date(ms).toISOString());
  }

  function tick() {
    const now = Date.now();
    $('now-sec').textContent = Math.floor(now / 1000);
    $('now-ms').textContent = now;
  }

  function fillZones() {
    const options = [`<option value="local">Local (${LOCAL})</option>`, ...ZONES.map((z) => `<option value="${z}">${z}</option>`)].join('');
    $('ts-zone').innerHTML = options;
    $('date-zone').innerHTML = options;
    $('ts-zone').value = 'local';
    $('date-zone').value = 'local';
  }

  function setDefaultDate() {
    const now = new Date();
    const pad = (n) => String(n).padStart(2, '0');
    $('date-input').value = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}T${pad(now.getHours())}:${pad(now.getMinutes())}`;
  }

  fillZones();
  setDefaultDate();
  tick();
  setInterval(tick, 1000);
  $('ts-input').value = Math.floor(Date.now() / 1000);
  showTimestamp();
  showDate();

  ['ts-input', 'ts-zone'].forEach((id) => $(id).addEventListener('input', showTimestamp));
  ['date-input', 'date-zone'].forEach((id) => $(id).addEventListener('input', showDate));
  $('use-now').addEventListener('click', () => { $('ts-input').value = Math.floor(Date.now() / 1000); showTimestamp(); });
  $('copy-now').addEventListener('click', () => copyText($('now-sec').textContent, $('copy-now')));
}());
