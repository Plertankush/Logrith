"""Find the user-visible English strings inside JavaScript, so translate_es.py can translate them.

The Spanish tool pages carry the same inline <script> as the English ones. Without this module their
status messages, errors and result labels stay English. Only strings that look like text shown to a
person are returned; selectors, class names, MIME types, object keys and values that are compared in
code are left alone, because translating them would break the tool.

Pieces of text are written with numbered placeholders where a template literal inserts code, e.g.
"Converted ${0} records." The translator must keep every placeholder; rewrite() puts the real code back.

Public API
    visible_strings(js)         the distinct pieces of text to translate
    rewrite(js, translations)   the script with each piece replaced by its translation
"""
import re
from collections import namedtuple

# A string literal found at the top level of a script. start/end span the characters between the quotes.
# parts: text pieces (raw source) and Expr entries for each ${...} of a template literal.
Literal = namedtuple('Literal', 'start end quote parts before after callee')
Expr = namedtuple('Expr', 'code')       # the JavaScript between ${ and }

REGEX_PRECEDERS = set('(,=:[!&|?{};+-*%<>~^')
REGEX_KEYWORDS = {'return', 'typeof', 'case', 'delete', 'void', 'throw', 'in', 'of', 'new', 'else', 'do'}
IDENT = re.compile(r'[A-Za-z_$][\w$]*')
PLACEHOLDER = re.compile(r'\$\{(\d+)\}')
TAG = re.compile(r'(<[^>]*>)')

# Calls whose string arguments are code, not text for the reader.
CODE_CALLEES = {
    '$', 'getElementById', 'querySelector', 'querySelectorAll', 'addEventListener', 'removeEventListener', 'add', 'remove',
    'toggle', 'contains', 'setAttribute', 'getAttribute', 'hasAttribute', 'removeAttribute', 'createElement', 'createElementNS',
    'fetch', 'closest', 'matches', 'getContext', 'toLocaleString', 'toLocaleDateString', 'toLocaleTimeString', 'NumberFormat',
    'DateTimeFormat', 'RegExp', 'require', 'import', 'getItem', 'setItem', 'removeItem', 'postMessage', 'toBlob', 'toDataURL',
    'padStart', 'padEnd', 'split', 'join', 'startsWith', 'endsWith', 'indexOf', 'includes', 'match', 'test', 'normalize',
    'defineProperty', 'getComputedStyle', 'getPropertyValue', 'setProperty', 'dispatchEvent', 'Event', 'CustomEvent', 'Worker',
    'TextDecoder', 'TextEncoder', 'digest', 'importKey', 'encode', 'decode', 'atob', 'btoa', 'parse', 'stringify', 'localeCompare',
}
NEVER = {   # capitalised values that are code, not text
    'Arial', 'Helvetica', 'Georgia', 'Courier', 'Times', 'Verdana', 'Segoe UI', 'Inter', 'Content-Type', 'Cache-Control',
    'GET', 'POST', 'PUT', 'Bearer', 'Escape', 'Enter', 'Tab', 'Backspace', 'Delete', 'Shift', 'Control', 'Alt', 'Meta',
    'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Space',
    'Root', 'Array', 'Pane', 'Make', 'Software', 'Orientation', 'DateTime', 'DateTimeOriginal',   # identifiers and EXIF tag names
}
COMPARISON = ('===', '!==', '==', '!=', 'case')


# --------------------------------------------------------------------------
# Lexing
# --------------------------------------------------------------------------
def _skip_quoted(js, i):
    """Index after the single- or double-quoted string starting at js[i]."""
    quote, n = js[i], len(js)
    i += 1
    while i < n and js[i] != quote:
        i += 2 if js[i] == '\\' else 1
    return i + 1


def _skip_regex(js, i):
    n, in_class = len(js), False
    i += 1
    while i < n:
        c = js[i]
        if c == '\\':
            i += 2
            continue
        if c == '[':
            in_class = True
        elif c == ']':
            in_class = False
        elif c == '/' and not in_class:
            i += 1
            while i < n and js[i].isalpha():
                i += 1
            return i
        elif c == '\n':
            return i
        i += 1
    return n


def _scan_template(js, i):
    """The template literal whose opening backtick is js[i]: (index after the closing backtick, parts)."""
    n, parts, text = len(js), [], []
    j = i + 1
    while j < n:
        c = js[j]
        if c == '\\':
            text.append(js[j:j + 2])
            j += 2
        elif c == '`':
            parts.append(''.join(text))
            return j + 1, parts
        elif c == '$' and js.startswith('${', j):
            parts.append(''.join(text))
            text = []
            end = _skip_expression(js, j + 2)
            parts.append(Expr(js[j + 2:end - 1]))
            j = end
        else:
            text.append(c)
            j += 1
    return n, parts


def _skip_expression(js, i):
    """Index after the '}' that closes a ${ substitution whose code starts at js[i]."""
    n, depth, last, last_word = len(js), 1, '(', ''
    while i < n:
        c = js[i]
        if c in '\'"':
            i, last, last_word = _skip_quoted(js, i), c, ''
        elif c == '`':
            i, last, last_word = _scan_template(js, i)[0], '`', ''
        elif c == '{':
            depth, i, last = depth + 1, i + 1, c
        elif c == '}':
            depth, i, last = depth - 1, i + 1, c
            if depth == 0:
                return i
        elif c == '/' and (last in REGEX_PRECEDERS or last_word in REGEX_KEYWORDS):
            i, last, last_word = _skip_regex(js, i), '/', ''
        elif c in ' \t\r\n':
            i += 1
        else:
            word = IDENT.match(js, i)
            if word:
                last, last_word, i = word.group(0)[-1], word.group(0), word.end()
            else:
                last, last_word, i = c, '', i + 1
    return n


def literals(js):
    """The string literals of js that are not inside a template's ${...} (those are reached through their Expr)."""
    found, n, i, last, last_word = [], len(js), 0, '', ''
    while i < n:
        ch = js[i]
        if ch in ' \t\r\n':
            i += 1
        elif js.startswith('//', i):
            i = js.find('\n', i)
            i = n if i < 0 else i
        elif js.startswith('/*', i):
            i = js.find('*/', i)
            i = n if i < 0 else i + 2
        elif ch in '\'"':
            end = _skip_quoted(js, i)
            found.append(_literal(js, i + 1, end - 1, ch, [js[i + 1:end - 1]]))
            i, last, last_word = end, ch, ''
        elif ch == '`':
            end, parts = _scan_template(js, i)
            found.append(_literal(js, i + 1, end - 1, '`', parts))
            i, last, last_word = end, '`', ''
        elif ch == '/' and (last in REGEX_PRECEDERS or last == '' or last_word in REGEX_KEYWORDS):
            i, last, last_word = _skip_regex(js, i), '/', ''
        else:
            word = IDENT.match(js, i)
            if word:
                last, last_word, i = word.group(0)[-1], word.group(0), word.end()
            else:
                last, last_word, i = ch, '', i + 1
    return found


def _literal(js, start, end, quote, parts):
    before = js[:start - 1].rstrip()
    after = js[end + 1:].lstrip()
    call = re.search(r'([A-Za-z_$][\w$]*)\s*\(\s*(?:[^()]*,\s*)?$', before[-80:])
    return Literal(start, end, quote, parts, before[-3:], after[:3], call.group(1) if call else '')


# --------------------------------------------------------------------------
# Choosing what to translate
# --------------------------------------------------------------------------
SIMPLE_ESCAPE = re.compile(r"\\(['\"`\\nt$])")
OTHER_ESCAPE = re.compile(r"\\(?!['\"`\\nt$])")


def decode(raw):
    """The text raw source stands for, for the escapes a message uses: quotes, backslash, \\n and \\t."""
    return SIMPLE_ESCAPE.sub(lambda m: {'n': '\n', 't': '\t'}.get(m.group(1), m.group(1)), raw)


def encode(text, quote):
    text = text.replace('\\', '\\\\').replace('\n', '\\n') if quote != '`' else text.replace('\\', '\\\\')
    if quote == '`':
        return text.replace('`', '\\`').replace('${', '\\${')
    return text.replace(quote, '\\' + quote)


def is_text(piece, in_markup):
    """True for a piece of text a person reads: words, not identifiers, class names or single acronyms."""
    bare = re.sub(r'&#?\w+;', ' ', PLACEHOLDER.sub(' ', piece)).strip()
    if not re.search(r'[A-Za-z]{2,}', bare) or bare in NEVER:
        return False
    if ' ' not in bare and re.search(r'\d', bare):
        return False                                    # a code such as "Il1O0"
    if re.search(r';|=>|\s=\s', bare):
        return False                                    # source code, e.g. a generated TypeScript snippet
    if re.fullmatch(r'[\w./:#@%?&=+*-]+', bare) and (not bare[0].isupper() or re.search(r'[/_]', bare)):
        return False                                    # a class name, path, selector, URL or time-zone id
    if re.search(r'"\w+"\s*:|^[\s"\]\[,:{}]+', bare):
        return False                                    # a piece of JSON, e.g. inside an AI prompt
    if re.match(r'^[^A-Za-z]*[A-Z][a-z]', bare):
        return True                                     # starts like a sentence or a label: "Copied!", "File size"
    return in_markup and not re.fullmatch(r'[a-z-]+', bare)


def _text_of(lit):
    """The literal's text with ${n} where code is inserted, and the code of each insertion."""
    text, exprs = [], []
    for part in lit.parts:
        if isinstance(part, Expr):
            text.append('${%d}' % len(exprs))
            exprs.append(part.code)
        else:
            text.append(decode(part))
    return ''.join(text), exprs


def _pieces(text, quoted):
    """The translatable cores of text, split around any HTML tags in it."""
    in_markup = bool(re.search(r'<[a-z/][^>]*>', text))
    return [part.strip() for part in TAG.split(text)
            if part.strip() and not part.startswith('<') and is_text(part.strip(), in_markup)]


def _is_list_item(lit):
    return lit.before[-1:] in '[,' and lit.after[:1] in ',]'


def _is_code(lit):
    if any(isinstance(part, str) and OTHER_ESCAPE.search(part) for part in lit.parts):
        return True                                     # \u00a0, \d ...: leave literals with unusual escapes alone
    if _is_list_item(lit) and len(re.findall(r'[A-Za-z]+', ''.join(p for p in lit.parts if isinstance(p, str)))) <= 2:
        return True                                     # short list entries are data: names, months, time zones
    return (lit.before.endswith(COMPARISON) or lit.after.startswith(COMPARISON) or lit.callee in CODE_CALLEES
            or (lit.after.startswith(':') and lit.before[-1:] in '{,'))          # an object key


def visible_strings(js):
    """Every distinct piece of text in js that should be translated, in source order."""
    seen = {}
    for lit in literals(js):
        text, exprs = _text_of(lit)
        if not _is_code(lit):
            for piece in _pieces(text, lit.quote):
                seen[piece] = None
        for code in exprs:
            for piece in visible_strings(code):
                seen[piece] = None
    return list(seen)


def rewrite(js, translations):
    """js with each translatable piece replaced by translations[piece]; pieces without a translation stay as they are."""
    edits = []
    for lit in literals(js):
        text, exprs = _text_of(lit)
        if not _is_code(lit):
            out = []
            for part in TAG.split(text):
                core = part.strip()
                if core in translations and core in _pieces(text, lit.quote) and not part.startswith('<'):
                    part = part[:len(part) - len(part.lstrip())] + translations[core] + part[len(part.rstrip()):]
                out.append(part)
            text = ''.join(out)
        if text == _text_of(lit)[0] and not any(visible_strings(code) for code in exprs):
            continue
        pieces, position = [], 0
        for match in PLACEHOLDER.finditer(text):
            pieces.append(encode(text[position:match.start()], lit.quote))
            pieces.append('${' + rewrite(exprs[int(match.group(1))], translations) + '}')
            position = match.end()
        pieces.append(encode(text[position:], lit.quote))
        edits.append((lit.start, lit.end, ''.join(pieces)))
    for start, end, replacement in sorted(edits, reverse=True):
        js = js[:start] + replacement + js[end:]
    return js
