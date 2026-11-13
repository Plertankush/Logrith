"""Articles for the AI & Technology topic. Rendered by scripts/build_articles.py.

Fields: slug, topic, subtopic, title, description, intro (HTML), takeaways (list),
sections [(anchor, heading, HTML)], faq [(question, answer)], tools [tool slugs].
"""

ARTICLES = [
    {
        'slug': 'how-large-language-models-work',
        'topic': 'ai-technology',
        'subtopic': 'artificial-intelligence-ml',
        'title': 'How Large Language Models Work: A Plain-English Guide',
        'description': 'A clear explanation of how large language models are trained, what tokens and context windows are, why they make mistakes, and how to use them sensibly.',
        'intro': '''<p>Large language models, or LLMs, power chatbots, writing assistants and coding tools. They can draft an email, explain a concept or write a function, and they can also state something false in a perfectly confident tone. Both behaviours come from the same mechanism, and understanding it makes you a far better user.</p>
<p>This guide explains how an LLM is built and how it produces an answer, with no maths required. By the end you will know what a token is, why context limits matter, why "hallucinations" happen and how to get more reliable results.</p>''',
        'takeaways': [
            'An LLM is trained to predict the next piece of text. Everything else it does is built on that skill.',
            'Models read and write in tokens, and limits and prices are counted in tokens rather than words.',
            'Fluent text is not the same as true text. Check facts, numbers and citations.',
            'Better results come from clear context, examples and constraints, plus a review step.',
        ],
        'sections': [
            ('what-it-is', 'What a large language model actually is', '''<p>A large language model is a program that has learned statistical patterns in a huge amount of text. Given some text, it estimates which piece of text is most likely to come next, adds it and repeats. Do that a few hundred times and you have a paragraph.</p>
<p>That description sounds too simple to explain what these systems can do, but the scale changes things. To predict the next word well across millions of documents, the model has to pick up grammar, facts, writing styles, reasoning patterns and the structure of code. Those abilities are not programmed in one by one. They emerge from the prediction task.</p>'''),
            ('tokens', 'Tokens: the unit models read and write', '''<p>Models do not read letters or whole words. They read <strong>tokens</strong>, which are chunks of text. A common word may be one token, a rare word may be split into several, and punctuation and spaces count too. As a rough rule of thumb for English, one token is about four characters, or three quarters of a word, though the exact split depends on the model.</p>
<p>Tokens matter because almost everything practical is measured in them. Providers usually price usage per token, and every model has a maximum number of tokens it can handle at once. If you want to estimate how much text fits or what a job might cost, the <a href="/tool/tools/ai-context-calculator">AI Context Calculator</a> gives a quick approximation in your browser.</p>'''),
            ('training', 'How a model is trained', '''<p>Training happens in stages.</p>
<ol>
<li><strong>Pre-training.</strong> The model reads an enormous collection of text and repeatedly tries to predict the next token. When it is wrong, its internal numbers (called parameters) are adjusted slightly. After billions of adjustments it becomes a strong text predictor.</li>
<li><strong>Instruction tuning.</strong> A pre-trained model completes text but does not naturally follow requests. It is further trained on examples of instructions paired with good responses, so it behaves like an assistant.</li>
<li><strong>Preference tuning.</strong> People or automated systems compare alternative answers, and the model is nudged toward the ones judged better: more helpful, more careful or less harmful.</li>
</ol>
<p>The details vary between providers and change quickly, but this three-stage shape is common. The important point is that the model learns from patterns in text, not from a verified database of facts.</p>'''),
            ('attention', 'Attention: how the model uses context', '''<p>Most modern LLMs use an architecture called the transformer. Its key idea is <strong>attention</strong>, a mechanism that lets the model weigh how relevant every earlier token is when predicting the next one. In the sentence "The trophy did not fit in the suitcase because it was too big", attention helps the model connect "it" with the trophy rather than the suitcase.</p>
<p>You do not need the mathematics to benefit from the intuition: the model considers your whole prompt at once and decides what to focus on. This is why clear, well-organised instructions help, and why burying the key requirement in the middle of a long, messy prompt can hurt.</p>'''),
            ('context-window', 'The context window', '''<p>The <strong>context window</strong> is the maximum number of tokens a model can consider in one go. It includes your instructions, any documents you paste in, the conversation so far and the answer being written. When a conversation exceeds the window, older content has to be dropped or summarised, and the model can no longer "see" it.</p>
<p>Larger windows allow longer documents, but they are not a guarantee of perfect recall. Models can still overlook details buried in very long inputs, and longer inputs cost more and run slower. For important work, ask about specific passages and verify the answers against the source.</p>'''),
            ('hallucinations', 'Why models make things up', '''<p>A "hallucination" is an answer that sounds right but is not supported by facts. It follows directly from how the model works. It is rewarded for producing plausible text, not for checking truth, so when it lacks reliable knowledge it can still produce a fluent guess.</p>
<p>Hallucinations are more likely when you ask for:</p>
<ul>
<li>precise numbers, dates, quotations or citations;</li>
<li>obscure facts, recent events or niche topics;</li>
<li>details about a document the model has not actually been given.</li>
</ul>
<p>Some products reduce the problem by letting the model search the web or retrieve text from your documents before answering. That helps, but it does not remove the need to check anything that matters.</p>'''),
            ('randomness', 'Why you get different answers each time', '''<p>When choosing the next token, a model usually samples from a ranked list of likely options rather than always picking the top one. A setting often called <em>temperature</em> controls how adventurous that sampling is. Lower values give more predictable output, higher values give more varied output. This is why the same prompt can produce different wording on different runs.</p>'''),
            ('using-well', 'How to get better results', '''<p>You cannot change how the model works, but you can change what you give it.</p>
<ul>
<li><strong>State the goal and the audience.</strong> "Explain DNS to a non-technical manager in 150 words" beats "explain DNS".</li>
<li><strong>Provide the material.</strong> Paste the text you want summarised or the data you want analysed instead of relying on the model's memory.</li>
<li><strong>Show an example.</strong> One sample of the format you want often works better than a paragraph of description.</li>
<li><strong>Set constraints.</strong> Length, tone, what to include and what to avoid.</li>
<li><strong>Ask it to show its work</strong> on reasoning tasks, then check the steps.</li>
<li><strong>Review before you rely.</strong> Treat output as a fast first draft from a capable but unreliable assistant.</li>
</ul>'''),
            ('privacy', 'Privacy and data handling', '''<p>When you type into a hosted AI service, your text is sent to the provider. Whether it can be retained or used to improve models depends on the provider, the plan and your settings, so read the data policy before pasting anything confidential. As a habit, remove personal data, credentials and client secrets from prompts unless you are certain how they are handled.</p>'''),
        ],
        'faq': [
            ('Do large language models understand what they say?', 'They model patterns in language very well, and that can look like understanding. Whether it counts as understanding in a human sense is debated, but in practice you should treat the output as plausible text that needs checking, not as verified knowledge.'),
            ('Are LLMs the same as search engines?', 'No. A search engine retrieves existing pages. An LLM generates new text from learned patterns. Some products combine both, so the model can cite retrieved sources, but the two are different mechanisms.'),
            ('Can an LLM learn from my conversation?', 'Within a single conversation it can use what you have written because it is in the context window. Whether your chats are used to train future models depends on the provider and your settings, so check their policy.'),
            ('How big is "large"?', 'Large language models have billions of parameters and are trained on very large text collections. The exact sizes vary by model and are not always published.'),
        ],
        'tools': ['ai-context-calculator', 'text-summarizer-basic', 'word-counter'],
    },
    {
        'slug': 'json-vs-yaml-vs-xml-vs-csv',
        'topic': 'ai-technology',
        'subtopic': 'software-developer-ecosystem',
        'title': 'JSON vs YAML vs XML vs CSV: Which Data Format Should You Use?',
        'description': 'Compare JSON, YAML, XML and CSV: strengths, weaknesses, common pitfalls and a simple rule for choosing the right data format for your project.',
        'intro': '''<p>Every application eventually has to store data in a file or send it to another system. The four formats you will meet most often are JSON, YAML, XML and CSV. They overlap enough that people argue about them, yet each has a clear sweet spot.</p>
<p>This guide compares them side by side, points out the mistakes that cause real bugs and finishes with a simple way to choose.</p>''',
        'takeaways': [
            'Use JSON for APIs and data exchange between programs.',
            'Use YAML for human-edited configuration, and watch its whitespace and type-guessing traps.',
            'Use XML when you need documents with mixed content, namespaces or strict schemas.',
            'Use CSV for flat tables you want to open in a spreadsheet. It has no types and no nesting.',
        ],
        'sections': [
            ('overview', 'The four formats at a glance', '''<table>
<thead><tr><th>Format</th><th>Structure</th><th>Comments</th><th>Best for</th></tr></thead>
<tbody>
<tr><td>JSON</td><td>Nested objects and arrays</td><td>No</td><td>APIs, app data, browser and server exchange</td></tr>
<tr><td>YAML</td><td>Nested, indentation-based</td><td>Yes</td><td>Configuration files people edit by hand</td></tr>
<tr><td>XML</td><td>Nested tags and attributes</td><td>Yes</td><td>Documents, feeds, enterprise integrations</td></tr>
<tr><td>CSV</td><td>Flat rows and columns</td><td>No</td><td>Spreadsheets and tabular exports</td></tr>
</tbody>
</table>'''),
            ('json', 'JSON: the default for data exchange', '''<p>JSON (JavaScript Object Notation) represents data as objects (key-value pairs), arrays, strings, numbers, booleans and null. It is compact, easy for programs to parse in virtually every language and strict enough that parsing errors are easy to detect.</p>
<p><strong>Strengths:</strong> universal support, small and predictable syntax, clear data types.</p>
<p><strong>Weaknesses:</strong> no comments, no trailing commas, every key and string needs double quotes, and large numbers can lose precision in some languages. Hand-editing is tedious for big files.</p>
<p>When a JSON file will not parse, the cause is usually a missing comma, a trailing comma or single quotes. Paste it into a <a href="/tool/tools/json-formatter">JSON formatter</a> to see exactly where it breaks, or try <a href="/tool/tools/json-repair">JSON Repair</a> for common mistakes.</p>'''),
            ('yaml', 'YAML: readable configuration', '''<p>YAML aims to be easy for humans to read and write. It uses indentation instead of braces, allows comments and supports the same kinds of structures as JSON. It is widely used for configuration, such as CI pipelines and container definitions.</p>
<p><strong>Strengths:</strong> very readable, supports comments, concise for nested configuration.</p>
<p><strong>Weaknesses:</strong></p>
<ul>
<li><strong>Whitespace matters.</strong> A wrong indent changes the meaning, or breaks the file. Use spaces, never tabs.</li>
<li><strong>Type guessing.</strong> Unquoted values can be interpreted as other types. In YAML 1.1, words like <code>no</code> or <code>off</code> may be read as booleans, which has caused the well-known "Norway problem" where the country code NO becomes false. Quote ambiguous strings.</li>
<li><strong>Complexity.</strong> Features like anchors and multi-document files are powerful but easy to misuse.</li>
</ul>
<p>Need to move between the two? A <a href="/tool/tools/yaml-json-converter">YAML to JSON converter</a> helps you check that a config means what you think it means.</p>'''),
            ('xml', 'XML: structure for documents', '''<p>XML wraps data in named tags and attributes. It is verbose, but that verbosity supports features the others lack: namespaces to avoid name clashes, schemas that validate structure strictly, and mixed content where text and markup interleave, as in documents.</p>
<p><strong>Strengths:</strong> strong validation, mature tooling, ideal for document-like data, and still common in feeds, office file formats and enterprise or government integrations.</p>
<p><strong>Weaknesses:</strong> verbose, heavier to parse and harder to read than JSON for plain data. A <a href="/tool/tools/xml-formatter">XML formatter</a> makes large files bearable to inspect.</p>'''),
            ('csv', 'CSV: simple tables', '''<p>CSV stores one record per line with values separated by commas. Every spreadsheet program can open it, which makes it the standard export format for tabular data.</p>
<p><strong>Strengths:</strong> tiny, universal, perfect for rows and columns.</p>
<p><strong>Weaknesses:</strong> no data types (everything is text until a program guesses), no nesting, and several subtle traps:</p>
<ul>
<li>Values containing commas or line breaks must be wrapped in quotes, and quotes inside must be doubled.</li>
<li>Different tools use different delimiters (comma, semicolon, tab) and encodings.</li>
<li>Spreadsheets may silently reformat values, such as dropping leading zeros from IDs or turning gene names into dates.</li>
</ul>
<p>If a file is messy, the <a href="/tool/tools/csv-cleaner">CSV Cleaner</a> can tidy common problems before you import it.</p>'''),
            ('choose', 'A simple way to choose', '''<ol>
<li><strong>Will programs exchange it?</strong> Use JSON.</li>
<li><strong>Will a person edit it often, with comments helpful?</strong> Use YAML, carefully quoted, or JSON if you can live without comments.</li>
<li><strong>Is it a document or must it satisfy a formal schema or an existing standard?</strong> Use XML.</li>
<li><strong>Is it a flat table meant for a spreadsheet or analysis tool?</strong> Use CSV.</li>
</ol>
<p>If you are unsure, start with JSON. It is supported everywhere, and converting later is usually straightforward.</p>'''),
            ('mistakes', 'Common mistakes to avoid', '''<ul>
<li>Putting comments in JSON. They are not allowed, so use a "_comment" field or switch to YAML.</li>
<li>Using YAML for data that machines write and read. Prefer JSON for generated files.</li>
<li>Opening and re-saving CSV in a spreadsheet, which can change values without warning.</li>
<li>Mixing tabs and spaces in YAML.</li>
<li>Choosing XML out of habit when the data is a simple object.</li>
</ul>'''),
        ],
        'faq': [
            ('Is YAML a superset of JSON?', 'Valid JSON is generally valid YAML 1.2, so most JSON files can be read by a YAML parser. The reverse is not true, because YAML has many features JSON lacks.'),
            ('Why is JSON more common than XML for web APIs?', 'It is lighter, simpler to read, and maps directly to the objects and arrays used in most programming languages.'),
            ('Can CSV hold nested data?', 'Not directly. You can flatten nested data into columns or store a JSON string in a cell, but at that point JSON is usually a better fit.'),
            ('Which format is fastest?', 'It depends on the parser and the data. For most applications readability, tooling and correctness matter more than raw parsing speed.'),
        ],
        'tools': ['json-formatter', 'yaml-json-converter', 'xml-formatter', 'csv-cleaner', 'json-repair'],
    },
    {
        'slug': 'hashing-vs-encryption-vs-encoding',
        'topic': 'ai-technology',
        'subtopic': 'software-developer-ecosystem',
        'title': 'Hashing vs Encryption vs Encoding: The Difference Explained',
        'description': 'Hashing, encryption and encoding are often confused. Learn what each one does, when to use it and which mistakes lead to real security problems.',
        'intro': '''<p>Developers and non-developers alike mix up hashing, encryption and encoding. They all turn data into something that looks different, but they solve different problems, and using the wrong one is a classic security mistake. Storing passwords with Base64, for example, protects nothing.</p>
<p>This guide gives each concept a clear definition, a comparison table and practical rules for when to use which.</p>''',
        'takeaways': [
            'Encoding changes the format of data so systems can handle it. Anyone can reverse it, and it provides no secrecy.',
            'Hashing produces a fixed-size fingerprint and cannot be reversed. It is used for integrity checks and, with the right algorithms, for passwords.',
            'Encryption hides data and can be reversed only with the right key.',
            'Never store passwords with plain encoding, encryption you can decrypt, or fast general-purpose hashes.',
        ],
        'sections': [
            ('comparison', 'The difference in one table', '''<table>
<thead><tr><th></th><th>Encoding</th><th>Hashing</th><th>Encryption</th></tr></thead>
<tbody>
<tr><td>Purpose</td><td>Make data usable by another system</td><td>Create a fingerprint of data</td><td>Keep data secret</td></tr>
<tr><td>Reversible?</td><td>Yes, by anyone</td><td>No (one-way)</td><td>Yes, with the key</td></tr>
<tr><td>Needs a key?</td><td>No</td><td>No (HMAC uses one)</td><td>Yes</td></tr>
<tr><td>Output size</td><td>Grows with input</td><td>Fixed</td><td>Roughly input size plus overhead</td></tr>
<tr><td>Examples</td><td>Base64, URL encoding</td><td>SHA-256, bcrypt, Argon2</td><td>AES, RSA</td></tr>
</tbody>
</table>'''),
            ('encoding', 'Encoding: changing the format', '''<p>Encoding converts data from one representation to another so it can travel safely through a system that expects a certain format. <strong>Base64</strong> turns binary data into plain text characters so it can sit inside JSON or an email. <strong>URL encoding</strong> replaces unsafe characters in a web address with percent codes.</p>
<p>There is no secret. If you can see Base64 text, you can decode it instantly. Try it yourself with the <a href="/tool/tools/base64">Base64 tool</a> or the <a href="/tool/tools/url-encoder">URL encoder</a>. Treat encoding as packaging, never as protection.</p>'''),
            ('hashing', 'Hashing: a one-way fingerprint', '''<p>A hash function takes any input and produces a fixed-length output, called a hash or digest. The same input always gives the same output, a tiny change in the input produces a completely different output, and you cannot work backwards from the hash to the original data.</p>
<p>Common uses include:</p>
<ul>
<li><strong>Integrity checks.</strong> Publish the SHA-256 hash of a download so users can verify the file was not altered.</li>
<li><strong>Deduplication.</strong> Identical files produce identical hashes.</li>
<li><strong>Digital signatures and data structures.</strong> Hashes sit inside many security systems.</li>
</ul>
<p>Not all hash functions are equally safe. MD5 and SHA-1 have known collision weaknesses and should not be used for security purposes, whereas the SHA-2 family, such as SHA-256, remains widely used. You can generate and compare digests with the <a href="/tool/tools/hash-generator">Hash Generator</a>.</p>'''),
            ('passwords', 'Hashing passwords is a special case', '''<p>Websites should never store your password itself. They store a hash and compare the hash of whatever you type at login. But a plain, fast hash such as SHA-256 is the wrong tool, because attackers can test billions of guesses per second against stolen hashes.</p>
<p>Password storage should use a deliberately slow algorithm built for the job, such as <strong>Argon2</strong>, <strong>bcrypt</strong> or <strong>scrypt</strong>, with a unique random <strong>salt</strong> for each password. The salt ensures that two users with the same password get different hashes and defeats precomputed lookup tables. Use a well-reviewed library instead of writing this yourself.</p>'''),
            ('encryption', 'Encryption: secrecy with a key', '''<p>Encryption scrambles data so that only someone with the correct key can read it. There are two families:</p>
<ul>
<li><strong>Symmetric encryption</strong> (for example AES) uses the same key to encrypt and decrypt. It is fast and used for files, disks and most data in transit once a connection is set up.</li>
<li><strong>Asymmetric encryption</strong> (for example RSA or elliptic-curve systems) uses a public key to encrypt and a private key to decrypt. It solves the problem of sharing keys, and underlies HTTPS certificates and signatures.</li>
</ul>
<p>The strength of encryption depends on keeping the key secret and on using a modern, well-reviewed algorithm. Inventing your own scheme is almost always a mistake.</p>'''),
            ('hmac', 'A related tool: HMAC and signed tokens', '''<p>Sometimes you need to prove that data came from someone who knows a secret and was not changed. An <strong>HMAC</strong> combines a hash function with a secret key to produce that proof. It is how many APIs sign webhooks, and how JSON Web Tokens can be signed. You can inspect the readable parts of a token with the <a href="/tool/tools/jwt-decoder">JWT Decoder</a>, remembering that a token's contents are encoded, not encrypted, unless it is specifically an encrypted token.</p>'''),
            ('rules', 'Practical rules', '''<ol>
<li>Need data to travel in a different format? <strong>Encode</strong>.</li>
<li>Need to verify that data has not changed, or to store passwords? <strong>Hash</strong>, using SHA-256 for integrity and a password-hashing algorithm for passwords.</li>
<li>Need to keep data secret but readable later? <strong>Encrypt</strong>, with a modern algorithm and carefully protected keys.</li>
<li>Do not use encoding as security, and do not use fast hashes for passwords.</li>
</ol>'''),
        ],
        'faq': [
            ('Is Base64 encryption?', 'No. Base64 is encoding. Anyone can decode it without a key, so it offers no confidentiality.'),
            ('Can a hash be reversed?', 'Not mathematically, but weak or common inputs can be found by guessing and checking, which is why passwords need slow hashes and salts.'),
            ('Why is MD5 considered broken?', 'Researchers can produce two different inputs with the same MD5 hash, called a collision, so it cannot be trusted where tampering is a concern.'),
            ('What is the difference between a hash and a checksum?', 'A checksum detects accidental errors and is often simple. A cryptographic hash is designed to resist deliberate tampering as well.'),
        ],
        'tools': ['hash-generator', 'base64', 'url-encoder', 'jwt-decoder', 'password-generator'],
    },
    {
        'slug': 'open-source-licenses-explained',
        'topic': 'ai-technology',
        'subtopic': 'cybersecurity-open-source',
        'title': 'Open Source Licenses Explained: MIT, Apache, GPL and How to Choose',
        'description': 'A practical guide to open source licenses: permissive vs copyleft, how MIT, Apache 2.0, GPL and AGPL differ, and how to choose or comply with one.',
        'intro': '''<p>Almost every modern project depends on open source code, and every piece of that code comes with a licence. The licence decides what you may do with it: use it commercially, modify it, keep your own changes private or ship it inside a product. Getting this wrong can mean legal trouble or a forced rewrite, and getting it right takes less effort than most people expect.</p>
<p>This guide explains the main licence families and the popular licences within them, and offers a simple way to choose one for your own project. It is general information, not legal advice.</p>''',
        'takeaways': [
            'No licence does not mean free to use. By default, code without a licence is all rights reserved.',
            'Permissive licences (MIT, BSD, Apache 2.0) allow broad reuse with light conditions.',
            'Copyleft licences (GPL, AGPL) require derivative work to be shared under similar terms.',
            'For your own project, MIT or Apache 2.0 are common, low-friction choices.',
        ],
        'sections': [
            ('basics', 'What an open source licence does', '''<p>Copyright law gives creators exclusive rights over their work. An open source licence grants other people specific permissions in advance, usually to use, copy, modify and distribute the code, in return for following certain conditions. Those conditions are the whole difference between licences.</p>
<p>The Open Source Initiative maintains a list of licences that meet the open source definition. Licences that restrict commercial use or certain fields are not open source, even if the code is publicly visible.</p>'''),
            ('two-families', 'Two families: permissive and copyleft', '''<p><strong>Permissive licences</strong> let you do almost anything, including using the code in closed-source commercial products, provided you keep the copyright notice and licence text. <strong>Copyleft licences</strong> add a requirement: if you distribute a work based on the code, you must release your version under the same or a compatible licence. The goal is to keep the code and its descendants open.</p>'''),
            ('popular', 'The licences you will meet most', '''<table>
<thead><tr><th>Licence</th><th>Type</th><th>Key points</th></tr></thead>
<tbody>
<tr><td>MIT</td><td>Permissive</td><td>Very short. Do almost anything, keep the copyright and licence notice. No explicit patent grant.</td></tr>
<tr><td>BSD (2 and 3-clause)</td><td>Permissive</td><td>Similar to MIT. The 3-clause version adds a rule against using the authors' names to endorse your product.</td></tr>
<tr><td>Apache 2.0</td><td>Permissive</td><td>Includes an explicit patent grant and requires noting changes. Common in larger projects.</td></tr>
<tr><td>MPL 2.0</td><td>Weak copyleft</td><td>Copyleft applies per file. Changes to MPL files must be shared, but you can combine them with other code.</td></tr>
<tr><td>LGPL</td><td>Weak copyleft</td><td>Designed for libraries. You can link to it from other software under conditions, but changes to the library itself must be shared.</td></tr>
<tr><td>GPL (v2, v3)</td><td>Strong copyleft</td><td>Distributed derivative works must be released under the GPL, with source available.</td></tr>
<tr><td>AGPL v3</td><td>Strong copyleft</td><td>Like GPL, and extends the requirement to software offered over a network, such as a hosted service.</td></tr>
</tbody>
</table>'''),
            ('patents', 'Why the patent grant matters', '''<p>Copyright and patents are separate rights. Someone could contribute code and later claim patent rights over it. Apache 2.0 and GPL v3 include explicit patent licences, which gives users more certainty. MIT and BSD are silent on patents, which is fine for many small projects but is one reason larger organisations often prefer Apache 2.0.</p>'''),
            ('using', 'Using other people\'s open source safely', '''<ol>
<li><strong>Know what you depend on.</strong> List direct and indirect dependencies and their licences. Most package managers can produce this report.</li>
<li><strong>Keep the notices.</strong> Almost every licence requires you to keep the copyright notice and licence text. Many sites collect them on a credits or licence page.</li>
<li><strong>Check copyleft before you ship.</strong> If you distribute software that includes GPL code, or offer AGPL code as a network service, understand the sharing obligations first.</li>
<li><strong>Treat unlicensed code as off limits.</strong> If a repository has no licence file, you do not have permission to reuse it.</li>
<li><strong>Keep dependencies updated.</strong> Maintained projects fix security issues. Abandoned ones become a liability.</li>
</ol>'''),
            ('choosing', 'Choosing a licence for your project', '''<ul>
<li><strong>You want maximum adoption with minimal fuss:</strong> MIT.</li>
<li><strong>You want the same, plus patent protection and clear contribution terms:</strong> Apache 2.0.</li>
<li><strong>You want improvements to stay open:</strong> GPL v3 for applications, or LGPL for libraries.</li>
<li><strong>You run a hosted service and do not want others to host a closed fork:</strong> AGPL v3.</li>
</ul>
<p>Add a <code>LICENSE</code> file at the root of your repository and mention the licence in your README. Resources such as choosealicense.com walk through the decision in more detail.</p>'''),
            ('not-software', 'Licences for things that are not code', '''<p>Creative Commons licences suit articles, images and other creative works, not software. If you publish both code and content, use a software licence for the code and a Creative Commons licence for the content. On Logrith, the credits for libraries used in the browser tools are collected on the <a href="/pages/license">licence page</a>.</p>'''),
        ],
        'faq': [
            ('Can I use MIT-licensed code in a commercial product?', 'Yes. The MIT licence allows commercial use, modification and distribution as long as you include the copyright notice and licence text.'),
            ('Does using GPL software force me to open-source my own code?', 'It depends on how you use it. If you distribute a combined work that is a derivative of GPL code, the GPL requires you to release it under the GPL. Running unmodified GPL software internally generally does not trigger that. Check with a qualified lawyer for your specific situation.'),
            ('What happens if a project has no licence?', 'By default the author keeps all rights, so you are not allowed to copy, modify or distribute it without permission.'),
            ('Is open source free of charge?', 'Usually you can obtain it without paying, but "open source" is about the freedoms the licence grants, not the price.'),
        ],
        'tools': ['hash-generator', 'password-strength', 'image-privacy-cleaner'],
    },
    {
        'slug': 'strong-passwords-and-passphrases-guide',
        'topic': 'ai-technology',
        'subtopic': 'cybersecurity-open-source',
        'title': 'Strong Passwords and Passphrases: What Actually Works',
        'description': 'How to create passwords that resist attack: why length beats complexity, how passphrases work, and how to set up a password manager and two-factor authentication.',
        'intro': '''<p>Most advice about passwords is outdated, confusing or both. People are told to add symbols, change them every ninety days and memorise a different one for every site, which is not possible for a human. The result is predictable: reused passwords and small variations of the same word.</p>
<p>Modern guidance, including the digital identity guidelines published by NIST, has moved toward a simpler idea: make passwords long and unique, use a password manager, and add a second factor. This guide shows how.</p>''',
        'takeaways': [
            'Length and uniqueness matter more than clever substitutions.',
            'A passphrase of several random words is strong and easier to remember.',
            'Use a password manager so every account has its own unique password.',
            'Turn on two-factor authentication, starting with your email.',
        ],
        'sections': [
            ('what-attackers-do', 'How passwords actually get stolen', '''<p>Understanding the real threats explains the advice.</p>
<ul>
<li><strong>Credential stuffing.</strong> Attackers take email and password pairs leaked from one site and try them on others. If you reuse a password, one breach exposes many accounts. This is the most common problem for ordinary users.</li>
<li><strong>Phishing.</strong> A convincing fake login page captures whatever you type, however strong the password.</li>
<li><strong>Guessing and cracking.</strong> Attackers test common passwords and, if they obtain a database of hashed passwords, try enormous numbers of guesses offline.</li>
<li><strong>Malware.</strong> Software on your device can record keystrokes or steal saved data.</li>
</ul>
<p>Notice that a "complex" eight-character password such as <code>P@ssw0rd!</code> helps against none of the first, second or fourth threats, and little against the third because attackers know these patterns.</p>'''),
            ('length', 'Why length beats complexity', '''<p>The strength of a password is its unpredictability, often measured in bits of entropy. Each extra random character multiplies the number of possibilities an attacker must try. Adding length scales the difficulty far more than swapping an <em>a</em> for an <em>@</em>, because humans substitute in predictable ways.</p>
<p>NIST's guidelines (SP 800-63B) recommend allowing long passwords, discourage forced composition rules such as "must include a symbol" and discourage mandatory periodic changes unless there is evidence of compromise. Recent revisions also set higher minimum lengths where a password is the only authentication factor. Check the current text for exact numbers if you are setting policy.</p>
<p>To see how a password scores, try the <a href="/tool/tools/password-strength">Password Strength checker</a>. It runs in your browser, but as a habit, test patterns rather than your real passwords.</p>'''),
            ('passphrases', 'Passphrases: strong and memorable', '''<p>A passphrase is a password made of several random words, such as <em>correct-horse-battery-staple</em>, the famous example from a well-known comic about password strength. If the words are chosen randomly from a large list, the result is both strong and easier to remember than a jumble of symbols.</p>
<p>The maths is simple. A word list of 7,776 words, as used by the Diceware method, gives about 12.9 bits of entropy per word. Six words give roughly 77 bits, which is far beyond practical guessing. The key word is <em>random</em>: a favourite quote or a song lyric is much weaker than words picked by dice or a generator.</p>
<p>Use the <a href="/tool/tools/passphrase-generator">Passphrase Generator</a> to create one, and the <a href="/tool/tools/password-generator">Password Generator</a> for long random strings when a site needs them.</p>'''),
            ('manager', 'Use a password manager', '''<p>You cannot remember dozens of unique long passwords, and you should not try. A password manager stores them in an encrypted vault protected by one strong master passphrase, fills them in on the right sites and generates new ones.</p>
<ol>
<li>Choose a reputable manager. Built-in options in browsers and operating systems are better than reusing passwords, and dedicated managers add features such as sharing and breach alerts.</li>
<li>Create a long, random master passphrase and memorise it. Write it down once and keep the paper somewhere safe at home if you need a backup.</li>
<li>Start with your most important accounts: email, banking, cloud storage and anything that can reset other accounts.</li>
<li>Let the manager generate a unique password for each site and replace old ones as you log in.</li>
</ol>
<p>A manager that fills credentials only on the correct web address also helps against phishing, because it will not fill a fake domain.</p>'''),
            ('mfa', 'Add a second factor', '''<p>Two-factor authentication (2FA) requires something beyond the password, so a stolen password alone is not enough. Not all second factors are equal:</p>
<table>
<thead><tr><th>Method</th><th>Protection</th><th>Notes</th></tr></thead>
<tbody>
<tr><td>SMS codes</td><td>Basic</td><td>Better than nothing, but vulnerable to SIM-swap attacks and phishing.</td></tr>
<tr><td>Authenticator app codes</td><td>Good</td><td>Codes generated on your device. Can still be phished in real time.</td></tr>
<tr><td>Passkeys and security keys</td><td>Strongest</td><td>Phishing-resistant because they are tied to the real website.</td></tr>
</tbody>
</table>
<p>Prioritise your primary email account, because password resets for everything else usually go there.</p>'''),
            ('checklist', 'A practical checklist', '''<ul>
<li>Unique password for every account, generated and stored by a manager.</li>
<li>A long random passphrase as the master password.</li>
<li>2FA on email, financial accounts and anything important, using an app or passkey where offered.</li>
<li>Check whether your email appears in known breaches using a trusted service such as Have I Been Pwned, then change affected passwords.</li>
<li>Be suspicious of urgent messages asking you to log in. Navigate to the site yourself instead of clicking links.</li>
<li>Keep devices and apps updated.</li>
</ul>'''),
        ],
        'faq': [
            ('How long should a password be?', 'Longer is better. For passwords you must memorise, use a passphrase of at least five or six random words. For everything else, let a manager generate a long random string, commonly 16 characters or more.'),
            ('Should I change my passwords regularly?', 'Current guidance generally advises against forced periodic changes. Change a password when there is a sign it has been exposed, such as a breach notification.'),
            ('Are password managers safe?', 'A well-designed manager encrypts your vault with your master password, and using one is widely considered safer than reusing passwords. Protect it with a strong master passphrase and 2FA.'),
            ('Is it safe to test my password on an online checker?', 'Prefer checkers that run entirely in your browser, and avoid typing your real passwords into any tool you do not trust. Testing a similar pattern is safer.'),
        ],
        'tools': ['password-strength', 'passphrase-generator', 'password-generator', 'hash-generator'],
    },
]
