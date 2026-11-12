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
        'title': 'AI & Technology',
        'icon': 'cpu',
        'tagline': 'Artificial intelligence, software and the digital ecosystem.',
        'meta': 'Plain-English guides to artificial intelligence, software development, cybersecurity and open source: what the technology does, how it works and how to use it.',
        'intro': [
            'Technology moves quickly, but the questions people ask about it are remarkably stable. What does this system actually do? What can go wrong? Is it worth learning, building on or paying for? This section answers those questions for three areas that shape most modern products: artificial intelligence, the software and developer ecosystem, and security and open source.',
            'Each sub-topic below opens with the core ideas in plain language, lists the questions we cover and links to free browser tools you can try while you read. We aim for explanations a working professional can act on, not announcements to skim.',
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
        'title': 'Startups & Business',
        'icon': 'rocket',
        'tagline': 'Building companies, products and businesses.',
        'meta': 'Guides for founders and operators: validating startup ideas, building SaaS products, and understanding business models, finance and operations.',
        'intro': [
            'Most new businesses fail for ordinary reasons: they build something few people need, price it badly or run out of cash before they learn. This section is about reducing those risks with simple, repeatable thinking. It covers how to test an idea cheaply, how to build and ship a software product, and how to understand the money behind a business.',
            'The guides are written for first-time founders and small teams. They favour clear frameworks, worked examples and the calculators you actually need over inspirational stories.',
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
    {
        'slug': 'marketing-growth',
        'title': 'Marketing & Growth',
        'icon': 'megaphone',
        'tagline': 'Growing products, audiences and brands.',
        'meta': 'Guides to SEO and content marketing, social media and the creator economy, and branding, sales and growth for small teams and independent builders.',
        'intro': [
            'Building something useful is only half the work; people also have to find it. Marketing is the discipline of being easy to find, easy to understand and easy to trust. This section covers the three channels that matter most to independent builders: search and content, social platforms and creators, and the brand and sales work that turns attention into customers.',
            'The emphasis is on durable practices over tricks. Search engines, platforms and audiences change, but clear writing, honest positioning and consistent publishing keep paying off.',
        ],
        'subtopics': [
            {
                'slug': 'seo-content-marketing',
                'title': 'SEO & Content Marketing',
                'icon': 'search',
                'summary': 'How search engines evaluate pages, how to plan and write content that earns traffic, and how to build a site Google and readers trust.',
                'intro': [
                    'Search engine optimisation is the practice of making your pages easy for search engines to understand and genuinely useful to the people who find them. The two goals are the same in the long run: engines reward pages that satisfy readers.',
                    'Content marketing is the publishing side. You answer real questions in depth, build a library over time and let search bring a steady audience. It is slower than ads, but the work compounds.',
                ],
                'topics': [
                    'Keyword research: intent, difficulty and realistic targets',
                    'On-page basics: titles, descriptions, headings, internal links, canonical tags',
                    'Technical SEO: crawlability, sitemaps, speed and structured data',
                    'Writing content that is original and useful rather than padded',
                    'E-E-A-T: experience, expertise, authoritativeness, trust',
                    'Measuring progress with Search Console and analytics',
                ],
                'concepts': [
                    ('Search intent', 'What the searcher actually wants: an answer, a comparison, a tool or a purchase. Content must match it.'),
                    ('Canonical tag', 'A tag telling search engines which URL is the preferred version of a page, which prevents duplicate-content confusion.'),
                    ('Internal linking', 'Links between your own pages, which help readers and crawlers discover and understand related content.'),
                    ('Thin content', 'Pages that add little unique value. Expanding them with real substance is better than hiding them.'),
                ],
                'tools': ['slug-generator', 'word-counter', 'character-counter', 'website-speed-analyzer', 'markdown-to-html', 'url-deduplicator', 'favicon-generator'],
                'start': 'Choose ten questions your audience genuinely asks, write one thorough answer for the most common and publish it. Then check Search Console after a few weeks to see which queries it starts to appear for.',
            },
            {
                'slug': 'social-media-creator-economy',
                'title': 'Social Media & Creator Economy',
                'icon': 'users',
                'summary': 'How creators build audiences and income: platform basics, content planning, community and the realistic ways creators earn.',
                'intro': [
                    'The creator economy is the set of businesses built on personal audiences: writers, video makers, educators and independent builders who earn directly from the people who follow them. Each platform rewards different habits, so understanding how a platform distributes content matters more than copying a format.',
                    'Sustainable creator income usually comes from several sources over time: advertising, sponsorships, products, services and memberships. Audience trust is the asset that supports all of them.',
                ],
                'topics': [
                    'Choosing a primary platform and a consistent format',
                    'Planning content around a repeatable series',
                    'Writing hooks, captions and descriptions that earn attention',
                    'Community: replying, listening and turning followers into customers',
                    'Monetisation paths: ads, sponsorships, digital products, memberships',
                    'Avoiding burnout with a realistic publishing rhythm',
                ],
                'concepts': [
                    ('Hook', 'The opening line or frame that gives a viewer a reason to keep going.'),
                    ('Engagement rate', 'The share of viewers who react, comment or share, which signals how well content resonates.'),
                    ('Owned audience', 'People you can reach directly, such as an email list, rather than only through a platform\'s algorithm.'),
                    ('Content pillar', 'A recurring theme your content returns to, which makes your focus clear to new followers.'),
                ],
                'tools': ['image-crop', 'image-resize', 'meme-generator', 'qr-generator', 'random-color-palette-generator', 'fancy-text-generator', 'image-compressor'],
                'start': 'Pick one platform and one format, publish a small batch on a fixed schedule for a month and review what people actually watch or share. Adjust the format based on that, not on guesses.',
            },
            {
                'slug': 'branding-sales-growth',
                'title': 'Branding, Sales & Growth',
                'icon': 'trending-up',
                'summary': 'Positioning, brand identity, simple sales processes and growth loops that help a small business win and keep customers.',
                'intro': [
                    'A brand is the set of expectations people have of you. Clear positioning, a consistent look and honest communication make those expectations easy to form and easy to meet. For a small business, good branding is mostly clarity: who you serve, what you do better and why that matters.',
                    'Sales and growth turn attention into revenue. Most small businesses do better with a simple, repeatable process than with elaborate funnels, and they grow fastest when customers come back and recommend them.',
                ],
                'topics': [
                    'Positioning: who you are for, and who you are not for',
                    'Visual identity basics: colour, type, logo and consistency',
                    'Writing a clear value proposition',
                    'A simple sales process: lead, conversation, proposal, follow-up',
                    'Pricing conversations and handling objections',
                    'Growth loops: referrals, content, product-led sharing',
                ],
                'concepts': [
                    ('Positioning', 'The specific place your product holds in a customer\'s mind compared with the alternatives.'),
                    ('Value proposition', 'A short statement of the outcome you deliver and why it is better than other options.'),
                    ('Conversion rate', 'The share of people at one stage, such as visitors, who take the next step, such as signing up.'),
                    ('Growth loop', 'A cycle where each customer or piece of output helps bring in the next, such as sharing a result with a visible link.'),
                ],
                'tools': ['color-converter', 'random-color-palette-generator', 'css-gradient-generator', 'favicon-generator', 'image-color-picker', 'percentage-calculator', 'qr-generator'],
                'start': 'Write one sentence that finishes "We help ___ do ___ so they can ___." Test it with five customers. If they cannot repeat it back, simplify it before you design anything.',
            },
        ],
    },
]
