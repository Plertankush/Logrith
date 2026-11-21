/* Meta Tag Generator — builds the <head> tags for SEO, Open Graph and Twitter, with live search and social previews. */
(function () {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const TITLE_LIMIT = 60;
  const DESCRIPTION_LIMIT = 160;
  const DESCRIPTION_MIN = 70;
  const INPUT_IDS = ['title', 'description', 'url', 'site-name', 'image', 'image-alt', 'og-type', 'twitter-card', 'twitter-handle', 'robots', 'theme-color'];
  const OPTION_IDS = ['opt-basic', 'opt-canonical', 'opt-og', 'opt-twitter', 'opt-theme'];

  const SAMPLE = {
    title: 'Free JSON Formatter and Validator | Example',
    description: 'Format, validate and minify JSON in your browser. Paste your data, spot syntax errors with line numbers and copy clean output. Free, fast and private.',
    url: 'https://example.com/tools/json-formatter',
    'site-name': 'Example',
    image: 'https://example.com/images/json-formatter-card.png',
    'image-alt': 'JSON formatter showing indented output',
    'twitter-handle': '@example',
  };

  const escapeAttribute = (value) => value.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const escapeText = (value) => value.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const isAbsoluteUrl = (value) => /^https?:\/\/[^\s/]+\.[^\s/]+/i.test(value);

  function readValues() {
    const values = {};
    INPUT_IDS.forEach((id) => { values[id] = $(id).value.trim(); });
    OPTION_IDS.forEach((id) => { values[id] = $(id).checked; });
    if (values['twitter-handle'] && !values['twitter-handle'].startsWith('@')) values['twitter-handle'] = `@${values['twitter-handle']}`;
    return values;
  }

  /** The tag lines for the options that are switched on; a tag is skipped when its field is empty. */
  function buildTags(v) {
    const tags = [];
    const meta = (attribute, name, content) => { if (content) tags.push(`<meta ${attribute}="${name}" content="${escapeAttribute(content)}">`); };

    if (v['opt-basic']) {
      tags.push('<meta charset="UTF-8">', '<meta name="viewport" content="width=device-width, initial-scale=1.0">');
      if (v.title) tags.push(`<title>${escapeText(v.title)}</title>`);
      meta('name', 'description', v.description);
      meta('name', 'robots', v.robots);
    }
    if (v['opt-theme']) meta('name', 'theme-color', v['theme-color']);
    if (v['opt-canonical'] && v.url) tags.push(`<link rel="canonical" href="${escapeAttribute(v.url)}">`);
    if (v['opt-og']) {
      meta('property', 'og:type', v['og-type']);
      meta('property', 'og:url', v.url);
      meta('property', 'og:site_name', v['site-name']);
      meta('property', 'og:title', v.title);
      meta('property', 'og:description', v.description);
      meta('property', 'og:image', v.image);
      if (v.image) meta('property', 'og:image:alt', v['image-alt']);
    }
    if (v['opt-twitter']) {
      meta('name', 'twitter:card', v['twitter-card']);
      meta('name', 'twitter:title', v.title);
      meta('name', 'twitter:description', v.description);
      meta('name', 'twitter:image', v.image);
      if (v.image) meta('name', 'twitter:image:alt', v['image-alt']);
      meta('name', 'twitter:site', v['twitter-handle']);
    }
    return tags;
  }

  /** Checks worth fixing before publishing: [level, message] pairs where level is "ok" or "warn". */
  function checkValues(v) {
    const notes = [];
    const titleLength = v.title.length;
    if (!titleLength) notes.push(['warn', uiText('Add a page title.')]);
    else if (titleLength > TITLE_LIMIT) notes.push(['warn', uiText('The title has {0} characters. Search results usually cut it off after about {1}.', titleLength, TITLE_LIMIT)]);
    else notes.push(['ok', uiText('The title length is good ({0} characters).', titleLength)]);

    const descriptionLength = v.description.length;
    if (!descriptionLength) notes.push(['warn', uiText('Add a meta description.')]);
    else if (descriptionLength > DESCRIPTION_LIMIT) notes.push(['warn', uiText('The description has {0} characters. Search results usually cut it off after about {1}.', descriptionLength, DESCRIPTION_LIMIT)]);
    else if (descriptionLength < DESCRIPTION_MIN) notes.push(['warn', uiText('The description is short ({0} characters). Aim for {1} to {2}.', descriptionLength, DESCRIPTION_MIN, DESCRIPTION_LIMIT)]);
    else notes.push(['ok', uiText('The description length is good ({0} characters).', descriptionLength)]);

    if (v.url && !isAbsoluteUrl(v.url)) notes.push(['warn', uiText('The page URL should be a full address starting with https://.')]);
    else if (v.url.startsWith('http://')) notes.push(['warn', uiText('The page URL uses http. Use https if your site supports it.')]);
    if (v.image && !isAbsoluteUrl(v.image)) notes.push(['warn', uiText('The image URL must be a full address. Social networks ignore relative paths.')]);
    if (!v.image && (v['opt-og'] || v['opt-twitter'])) notes.push(['warn', uiText('Add an image URL (1200 x 630 pixels works well) so shared links show a picture.')]);
    if (v.robots.includes('noindex')) notes.push(['warn', uiText('This page tells search engines not to index it.')]);
    return notes;
  }

  function hostOf(url) {
    try { return new URL(url).hostname.replace(/^www\./, ''); } catch (error) { return 'example.com'; }
  }

  function truncate(text, limit) {
    return text.length > limit ? `${text.slice(0, limit - 1).trimEnd()}…` : text;
  }

  function renderPreviews(v) {
    const host = hostOf(v.url);
    $('serp-site').textContent = v['site-name'] || host;
    $('serp-url').textContent = v.url || 'https://example.com/';
    $('serp-title').textContent = truncate(v.title || 'Page title', 62);
    $('serp-description').textContent = truncate(v.description || 'Your meta description appears here.', 160);

    $('social-host').textContent = host;
    $('social-title').textContent = truncate(v.title || 'Page title', 70);
    $('social-description').textContent = truncate(v.description || 'Your meta description appears here.', 110);
    const card = $('social-card');
    card.classList.toggle('is-summary', v['twitter-card'] === 'summary');
    const image = $('social-image');
    image.alt = v['image-alt'];
    if (!isAbsoluteUrl(v.image)) { image.removeAttribute('src'); image.hidden = true; }
    else if (image.getAttribute('src') !== v.image) image.src = v.image;      // shown by the load handler below
  }

  function renderCounters(v) {
    const set = (id, length, limit) => {
      const element = $(id);
      element.textContent = `${length} / ${limit}`;
      element.classList.toggle('is-over', length > limit);
    };
    set('title-count', v.title.length, TITLE_LIMIT);
    set('description-count', v.description.length, DESCRIPTION_LIMIT);
  }

  function update() {
    const values = readValues();
    $('output-text').value = buildTags(values).join('\n');
    $('check-list').innerHTML = checkValues(values).map(([level, message]) => `<li class="${level}">${escapeText(message)}</li>`).join('');
    renderCounters(values);
    renderPreviews(values);
  }

  function fillSample() {
    Object.entries(SAMPLE).forEach(([id, value]) => { $(id).value = value; });
    update();
  }

  function clearAll() {
    Object.keys(SAMPLE).forEach((id) => { $(id).value = ''; });
    update();
  }

  [...INPUT_IDS, ...OPTION_IDS].forEach((id) => $(id).addEventListener('input', update));
  $('social-image').addEventListener('load', () => { $('social-image').hidden = false; });
  $('social-image').addEventListener('error', () => { $('social-image').hidden = true; });
  $('copy-btn').addEventListener('click', () => copyText($('output-text').value, $('copy-btn')));
  $('sample-btn').addEventListener('click', fillSample);
  $('clear-btn').addEventListener('click', clearAll);

  fillSample();
}());
