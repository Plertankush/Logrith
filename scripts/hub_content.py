"""Editorial content for the Logrith topic hubs.

Each top-level topic has three sub-topics. `build_hubs.py` turns this data into
the static pages: /<topic>/ and /<topic>/<subtopic>. Edit text here, then run

    python3 scripts/build_hubs.py

Keep every claim general and checkable: these pages are guides to a subject,
not news. Tool slugs must exist under /tool/ (the build script checks).
"""

SITE = 'https://logrith.in'

TOPICS = [
    {
        'slug': 'ai-technology',
        'title': 'AI & Developer Tools',
        'icon': 'cpu',
        'tagline': 'How AI and developer tools work, and how to use them well.',
        'meta': 'Practical guides to AI tools, developer workflows, data formats, security and open source for people who build things with software.',
        'intro': [
            'Most of what people build today involves AI, data and code in some combination. This section explains how those pieces work so you can choose tools with confidence: what a language model can and cannot do, how data formats and APIs fit together, and how to keep what you build secure.',
            'Each guide is paired with free browser tools you can use straight away, such as a JSON formatter, a regex tester or the AI context calculator. We explain the idea first and keep jargon to a minimum.',
        ],
        'subtopics': [
            {
                'slug': 'artificial-intelligence-ml',
                'title': 'Artificial Intelligence & ML',
                'icon': 'sparkles',
                'summary': 'How machine learning and large language models work, what they are good and bad at, and how to use AI tools sensibly in real projects.',
                'intro': [
                    'Artificial intelligence is a broad label. In practice most of what people use today is machine learning: software that learns patterns from examples instead of following hand-written rules. Large language models, image generators and recommendation systems are all variations on that idea, trained on very different data for very different jobs.',
                    'Understanding the basics changes how you use these systems. A language model predicts likely text; it does not look facts up unless it is connected to a source. That single idea explains why it can write fluent prose, why it sometimes states false things confidently and why good prompts and good checks matter.',
                ],
                'topics': [
                    'How language models are trained and why they produce errors',
                    'Tokens, context windows and what they mean for long documents and cost',
                    'Prompting habits that improve results: context, examples, constraints',
                    'Choosing between hosted AI services, open models and simple rules',
                    'Evaluating AI output: spot checks, test sets and human review',
                    'Privacy and data handling when you send text to an AI service',
                ],
                'concepts': [
                    ('Token', 'The small chunk of text a model reads and writes. Usage limits and pricing are usually counted in tokens, not words.'),
                    ('Context window', 'The amount of text a model can consider at once, including your prompt and its own reply.'),
                    ('Hallucination', 'A fluent but unsupported answer. It is a property of how the model generates text, so checking matters for facts, numbers and citations.'),
                    ('Fine-tuning vs prompting', 'Prompting changes the instructions you give a model. Fine-tuning changes the model itself and needs examples and effort. Most projects should start with prompting.'),
                ],
                'tools': ['ai-context-calculator', 'resume-analyzer', 'text-summarizer-basic', 'website-speed-analyzer'],
                'start': 'Start with a small, low-risk task you already do by hand, such as summarising meeting notes or drafting a first outline. Compare the AI result with your own, note what it gets wrong and decide what a reviewer must always check. That habit scales better than any single prompt trick.',
            },
            {
                'slug': 'software-developer-ecosystem',
                'title': 'Software & Developer Ecosystem',
                'icon': 'code',
                'summary': 'Guides to the tools, formats and practices developers rely on: APIs, data formats, web performance, debugging and day-to-day workflow.',
                'intro': [
                    'Most software work is not writing new algorithms. It is moving data between systems, reading other people\'s formats, tracking down why something fails and keeping a codebase understandable. The developer ecosystem is the collection of formats, tools and conventions that make that possible.',
                    'This sub-topic explains those building blocks: how JSON and YAML differ, what an HTTP status code is telling you, why regular expressions are both powerful and risky, and how web performance is measured. The goal is fluency, so you can read an error message and know where to look next.',
                ],
                'topics': [
                    'Data formats in practice: JSON, YAML, XML and CSV, and converting between them',
                    'Reading HTTP status codes and API errors',
                    'Regular expressions: when to use them and when to parse instead',
                    'Web performance basics: what slows a page down and how to measure it',
                    'Hashing, encoding and encryption: three different things',
                    'Habits that keep code readable for the next developer',
                ],
                'concepts': [
                    ('API', 'A defined way for one program to ask another for data or an action, usually over HTTP.'),
                    ('Encoding vs hashing vs encryption', 'Encoding changes representation and is reversible by anyone. Hashing is one-way. Encryption is reversible only with a key.'),
                    ('Idempotent request', 'A request that has the same effect whether it is sent once or many times, which makes retries safe.'),
                    ('Technical debt', 'The future cost of a shortcut taken today. It is acceptable when chosen deliberately and tracked.'),
                ],
                'tools': ['json-formatter', 'regex-tester', 'http-status-code-lookup', 'yaml-json-converter', 'sql-formatter', 'cron-expression-builder'],
                'start': 'Pick the data format you handle most, paste a real sample into a formatter and learn what each error message means. Reading failures calmly is the most transferable skill in software.',
            },
            {
                'slug': 'cybersecurity-open-source',
                'title': 'Cybersecurity & Open Source',
                'icon': 'shield-check',
                'summary': 'Practical security for individuals and small teams, plus how open source licensing and projects work and how to depend on them safely.',
                'intro': [
                    'Most security incidents for small teams and individuals come from ordinary causes: reused passwords, unpatched software, leaked keys and convincing phishing messages. Good security is mostly consistent habits, not exotic tools.',
                    'Open source sits underneath almost everything you use. Knowing how licences differ, how to judge whether a project is maintained and how to keep dependencies updated is now a basic part of building anything on the web.',
                ],
                'topics': [
                    'Passwords, passphrases and password managers: what actually helps',
                    'Two-factor authentication and the weak points of each method',
                    'Spotting phishing and social-engineering attempts',
                    'Keeping secrets such as API keys out of code and screenshots',
                    'Open source licences explained: permissive vs copyleft',
                    'Choosing and updating open source dependencies safely',
                ],
                'concepts': [
                    ('Entropy', 'A measure of how unpredictable a password is. Length usually matters more than clever substitutions.'),
                    ('Least privilege', 'Giving an account or key only the access it needs, so a leak does limited damage.'),
                    ('Permissive vs copyleft', 'Permissive licences allow broad reuse with few conditions. Copyleft licences require derivative work to stay open under similar terms.'),
                    ('Supply-chain risk', 'The risk that a library you depend on, or one of its dependencies, is compromised or abandoned.'),
                ],
                'tools': ['password-strength', 'password-generator', 'passphrase-generator', 'hash-generator', 'jwt-decoder', 'image-privacy-cleaner'],
                'start': 'Do three things this week: move your important accounts to unique passwords from a manager, turn on two-factor authentication for email, and check that no keys or tokens sit in public repositories or screenshots.',
            },
        ],
    },
    {
        'slug': 'startups-business',
        'title': 'Build & Ship',
        'icon': 'rocket',
        'tagline': 'Turning an idea into a small, working product.',
        'meta': 'Guides for solo builders and small teams: validating a product idea, building and pricing a SaaS tool, and understanding the money behind it.',
        'intro': [
            'Most small products fail before they reach customers, not after. This section covers the practical middle: testing whether an idea is worth building, shipping a first version of a software product and understanding the pricing and money behind it.',
            'It is written for solo builders and small teams who use AI and modern tools to ship faster. The guides favour checklists, worked examples and honest trade-offs over hype.',
        ],
        'subtopics': [
            {
                'slug': 'startup-ideas-validation',
                'title': 'Startup Ideas & Validation',
                'icon': 'lightbulb',
                'summary': 'How to generate startup ideas, test demand before building and decide whether an idea deserves your time and money.',
                'intro': [
                    'A good idea is a problem plus a person who feels it strongly enough to act. Validation is the work of checking both before you invest months of effort. It is cheaper to be disproved by ten conversations than by a finished product nobody opens.',
                    'The most reliable early signals are behavioural: someone gives you time, a deposit, a signed intent or a repeat visit. Compliments, likes and polite interest are weak signals and should be treated as such.',
                ],
                'topics': [
                    'Finding problems worth solving: your own work, communities and complaints',
                    'Customer interviews: questions that avoid leading people',
                    'Landing-page and waitlist tests and how to read the results',
                    'Sizing a market without inflated numbers',
                    'Competitor research: what existing alternatives teach you',
                    'Deciding when to build, pivot or stop',
                ],
                'concepts': [
                    ('Problem-solution fit', 'Evidence that a specific group has a real problem and that your approach addresses it.'),
                    ('Minimum viable product', 'The smallest version that lets you learn whether people want the outcome. It is a learning tool, not a low-quality launch.'),
                    ('Smoke test', 'A cheap test, such as a page describing a product that does not yet exist, to measure real interest.'),
                    ('Willingness to pay', 'Whether people will exchange money, time or effort for the solution, which is stronger evidence than agreement.'),
                ],
                'tools': ['random-name-generator', 'acronym-generator', 'slug-generator', 'qr-generator', 'percentage-calculator'],
                'start': 'Write down one problem, name who has it and find five of those people to talk to this week. Ask about the last time the problem happened and what they did, not whether they would like your idea.',
            },
            {
                'slug': 'saas-product-building',
                'title': 'SaaS & Product Building',
                'icon': 'package',
                'summary': 'How to plan, build and ship a software-as-a-service product: scoping, pricing, onboarding and keeping customers.',
                'intro': [
                    'Software-as-a-service sells ongoing access rather than a one-time copy. That changes the economics: revenue arrives monthly, so retention matters as much as acquisition, and a product that people stop using will eventually stop paying.',
                    'Building one well means scoping tightly, shipping early, listening to usage and pricing in a way that matches the value delivered. This sub-topic covers each stage with an emphasis on small teams and solo founders.',
                ],
                'topics': [
                    'Scoping a first version you can ship in weeks',
                    'Choosing a stack: boring technology and when it is the right call',
                    'Pricing models: flat, tiered, usage-based and how to test them',
                    'Onboarding that gets a new user to value quickly',
                    'Measuring retention, churn and activation',
                    'Support, documentation and feedback loops',
                ],
                'concepts': [
                    ('MRR', 'Monthly recurring revenue: the predictable subscription revenue you expect each month.'),
                    ('Churn', 'The share of customers or revenue lost over a period. Small differences compound heavily over time.'),
                    ('Activation', 'The point at which a new user first experiences the core value of the product.'),
                    ('Usage-based pricing', 'Charging according to consumption, which aligns cost with value but makes revenue less predictable.'),
                ],
                'tools': ['json-formatter', 'cron-expression-builder', 'uuid-generator', 'http-status-code-lookup', 'website-speed-analyzer', 'css-gradient-generator'],
                'start': 'Write the one sentence describing the outcome your product delivers, list the fewest features needed to deliver it and cut everything else from version one. Ship it to a handful of users and watch what they do.',
            },
            {
                'slug': 'business-models-finance-operations',
                'title': 'Business Models, Finance & Operations',
                'icon': 'bank',
                'summary': 'Understand how businesses make money: revenue models, margins, cash flow, pricing maths and running operations efficiently.',
                'intro': [
                    'A business model is the answer to a simple question: who pays, for what, and why does the maths work? Many struggling companies have a product people like but economics that do not add up. Understanding margins, cash flow and unit economics early prevents that.',
                    'Operations is the quieter half: the processes, tools and habits that let you deliver consistently as you grow. This sub-topic pairs the concepts with calculators for the arithmetic founders do constantly.',
                ],
                'topics': [
                    'Common business models: subscription, marketplace, services, ads, licensing',
                    'Gross margin, net margin and why they differ',
                    'Cash flow versus profit and how companies run out of money',
                    'Pricing maths: discounts, taxes, fees and break-even',
                    'Loans, interest and the real cost of borrowing',
                    'Simple operating routines for small teams',
                ],
                'concepts': [
                    ('Unit economics', 'The revenue and cost attached to a single customer or order, used to judge whether growth is healthy.'),
                    ('Gross margin', 'Revenue minus the direct cost of delivering it, expressed as a share of revenue.'),
                    ('Cash flow', 'The timing of money moving in and out. A profitable business can still fail if cash arrives too late.'),
                    ('Break-even point', 'The volume at which revenue covers all costs.'),
                ],
                'tools': ['emi-calculator', 'compound-interest-calculator', 'gst-calculator', 'percentage-calculator', 'discount-stacking-calculator', 'salary-hourly-converter', 'loan-affordability-calculator', 'currency-converter'],
                'start': 'Take your most important product or service and write one line of unit economics: what a customer pays, what it costs you to serve them and what is left. If you cannot fill that line in, that is the first thing to find out.',
            },
        ],
    },
]
