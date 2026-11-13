"""Articles for the Marketing & Growth topic. Rendered by scripts/build_articles.py."""

ARTICLES = [
    {
        'slug': 'technical-seo-checklist-for-small-websites',
        'topic': 'marketing-growth',
        'subtopic': 'seo-content-marketing',
        'title': 'Technical SEO Checklist for Small Websites',
        'description': 'A practical technical SEO checklist: crawling, sitemaps, canonical tags, redirects, structured data, page speed and Search Console, explained for small sites.',
        'intro': '''<p>Great content cannot rank if search engines cannot find, read and understand it. Technical SEO is the set of fixes that make your site easy to crawl and index. For a small site the list is short, most items are one-time jobs and getting them right removes a surprising number of silent problems.</p>
<p>This checklist walks through the essentials in the order we would check them, with the reasons behind each item and the mistakes that cause the most damage.</p>''',
        'takeaways': [
            'Make sure important pages can be crawled and are not accidentally blocked or set to noindex.',
            'Give every page a self-referencing canonical tag and a unique title and description.',
            'When URLs change, use permanent (301) redirects and update internal links and sitemaps.',
            'Use Search Console to submit sitemaps, inspect URLs and watch for errors.',
        ],
        'sections': [
            ('crawl', '1. Let search engines crawl your site', '''<ul>
<li><strong>Check robots.txt.</strong> It lives at <code>/robots.txt</code> and tells crawlers what they may fetch. A stray <code>Disallow: /</code> blocks the whole site. A sensible small-site file allows everything and points to your sitemap.</li>
<li><strong>Look for accidental noindex.</strong> A <code>&lt;meta name="robots" content="noindex"&gt;</code> tag, or an <code>X-Robots-Tag</code> header, keeps a page out of results. These are often left over from development.</li>
<li><strong>Use HTTPS</strong> everywhere and redirect HTTP to HTTPS.</li>
<li><strong>Make navigation crawlable.</strong> Use real links (<code>&lt;a href&gt;</code>) so crawlers can discover pages. Important pages should be reachable within a few clicks from the home page.</li>
</ul>'''),
            ('sitemap', '2. Publish an XML sitemap', '''<p>A sitemap lists the URLs you want indexed. It does not guarantee indexing, but it helps search engines discover pages and notice updates.</p>
<ul>
<li>Include only canonical, indexable URLs that return a 200 status.</li>
<li>Keep <code>lastmod</code> dates accurate and update them only when a page genuinely changes.</li>
<li>Reference the sitemap in robots.txt and submit it in Google Search Console.</li>
<li>For larger sites, split it into several sitemaps listed in a sitemap index.</li>
</ul>'''),
            ('canonical', '3. Set canonical tags', '''<p>The same page can be reachable under several URLs: with and without a trailing slash, with tracking parameters or on different protocols. A canonical tag tells search engines which one is the preferred version so that ranking signals are not split.</p>
<ul>
<li>Add <code>&lt;link rel="canonical" href="https://example.com/page"&gt;</code> to every page, pointing to its own preferred URL.</li>
<li>Use absolute URLs and keep them consistent with your sitemap and internal links.</li>
<li>Never point the canonical of an important page at a different page by mistake. Search engines treat the tag as a strong hint.</li>
</ul>
<p>When we moved Logrith's tools under a new folder, every page's canonical, Open Graph URL, structured data and sitemap entry had to change to the new address. A small script that compares each page's canonical tag with the URL it is served from catches mistakes like this before they ship.</p>'''),
            ('redirects', '4. Redirect moved pages properly', '''<p>If you change a URL, send visitors and crawlers from the old address to the new one with a <strong>301 (permanent) redirect</strong>. This passes most ranking signals and avoids broken links.</p>
<ul>
<li>Redirect straight to the final page, not through a chain of several redirects.</li>
<li>Update internal links to the new URLs rather than relying on redirects forever.</li>
<li>Keep the redirects in place long term.</li>
<li>Do not redirect everything to the home page. Redirect each old URL to its closest equivalent.</li>
</ul>'''),
            ('onpage', '5. Titles, descriptions and headings', '''<ul>
<li>Give every page a unique <code>&lt;title&gt;</code> that describes it in plain words. Keep it roughly within 60 characters so it is not truncated.</li>
<li>Write a unique meta description that summarises the page and invites the click, usually under about 160 characters. It does not directly affect ranking but influences clicks.</li>
<li>Use one clear <code>&lt;h1&gt;</code> and logical <code>&lt;h2&gt;</code> and <code>&lt;h3&gt;</code> headings.</li>
<li>Use short, readable URLs with words, not IDs. A <a href="/tool/tools/slug-generator">slug generator</a> helps.</li>
</ul>'''),
            ('links', '6. Internal links', '''<p>Links between your own pages help crawlers find content and help readers continue. Link from related articles to each other and to relevant tools or product pages using descriptive anchor text, such as "customer interview questions", not "click here". Fix broken internal links, and avoid orphan pages that nothing links to.</p>'''),
            ('schema', '7. Structured data', '''<p>Structured data, usually JSON-LD, describes your page in a standard vocabulary from schema.org. Useful types for small sites include <code>Article</code>, <code>BreadcrumbList</code>, <code>FAQPage</code>, <code>Organization</code> and <code>WebSite</code>. It helps search engines understand your content and can make you eligible for some rich results, though it never guarantees them.</p>
<ul>
<li>Mark up only what is visible on the page.</li>
<li>Validate with the Rich Results Test or the Schema Markup Validator.</li>
<li>Keep URLs inside the markup identical to your canonical URLs.</li>
</ul>'''),
            ('speed', '8. Speed and mobile usability', '''<p>Page experience affects both visitors and rankings. Google's Core Web Vitals describe three measures, with these thresholds for a "good" experience: Largest Contentful Paint within 2.5 seconds, Interaction to Next Paint within 200 milliseconds and Cumulative Layout Shift under 0.1.</p>
<ul>
<li>Compress and correctly size images. An <a href="/tool/tools/image-compressor">image compressor</a> often gives the biggest quick win.</li>
<li>Minify CSS and JavaScript, defer non-essential scripts and avoid loading fonts you do not use.</li>
<li>Set width and height on images to prevent layout jumps.</li>
<li>Test on a real phone. Most browsing happens there.</li>
</ul>
<p>The <a href="/tool/tools/website-speed-analyzer">Website Speed Analyzer</a> gives a quick overview, and PageSpeed Insights and Lighthouse give deeper reports.</p>'''),
            ('search-console', '9. Use Google Search Console', '''<ol>
<li>Verify your site (a domain property covers all subdomains and protocols).</li>
<li>Submit your sitemap and check that it reports success.</li>
<li>Use <strong>URL Inspection</strong> on key pages to see whether they are indexed and to request indexing after major changes.</li>
<li>Review the <strong>Pages</strong> report for reasons URLs are not indexed, such as "Crawled, currently not indexed", "Duplicate without user-selected canonical" or "Page with redirect".</li>
<li>Check <strong>Performance</strong> to see which queries and pages earn impressions and clicks, and use it to guide new content.</li>
</ol>
<p>Indexing takes time, often days or weeks for a new site, and not every page will be indexed. Quality and usefulness of the content strongly influence whether Google chooses to index and show a page.</p>'''),
            ('quick-audit', 'A 15-minute audit you can run today', '''<ul>
<li>Open <code>/robots.txt</code> and <code>/sitemap.xml</code> in a browser and confirm they load.</li>
<li>View the source of three key pages and check the title, description, canonical and robots tags.</li>
<li>Click through your navigation, looking for broken links and redirect chains.</li>
<li>Run a speed test on your home page and your slowest page.</li>
<li>Open Search Console and read the Pages report.</li>
</ul>'''),
        ],
        'faq': [
            ('Do I need an XML sitemap for a small site?', 'It is not mandatory when pages are well linked, but it is easy, helps discovery and gives you useful reporting in Search Console, so it is recommended.'),
            ('Should every page have a canonical tag?', 'Yes. A self-referencing canonical on each indexable page is a common best practice that prevents duplicate-URL issues.'),
            ('How long does it take for a new page to be indexed?', 'It can take from a few days to several weeks. Internal links, a sitemap and useful content help, but there is no guaranteed timeline.'),
            ('Is a meta description a ranking factor?', 'Not directly, but a clear description can improve click-through from search results.'),
        ],
        'tools': ['slug-generator', 'website-speed-analyzer', 'image-compressor', 'url-deduplicator', 'markdown-to-html'],
    },
    {
        'slug': 'sustainable-creator-publishing-system',
        'topic': 'marketing-growth',
        'subtopic': 'social-media-creator-economy',
        'title': 'A Sustainable Publishing System for Creators and Solo Builders',
        'description': 'How to grow an audience without burning out: choose a focus, plan content pillars, batch your work, track meaningful metrics and build an owned audience.',
        'intro': '''<p>Most people who start publishing online stop within a few months. They do not run out of ideas. They run out of energy, because they treat every post as a fresh emergency. Growth rewards consistency over a long period, so the real challenge is designing a way of working you can keep up.</p>
<p>This guide lays out a simple publishing system for creators and solo builders: pick a focus, plan around themes, produce in batches, measure what matters and build an audience you own.</p>''',
        'takeaways': [
            'Pick one platform and one format, and stay with them long enough to learn.',
            'Plan around a few content pillars instead of chasing daily inspiration.',
            'Batch the work and repurpose each idea into several formats.',
            'Build an owned audience such as an email list so you are not dependent on one algorithm.',
        ],
        'sections': [
            ('focus', 'Step 1: Choose a focus', '''<p>Audiences follow people for a reason. Define it in one sentence: who you help and with what. "I explain startup finance to first-time founders in plain language" gives a stranger a reason to follow. "I post about business" does not.</p>
<p>Pick <strong>one primary platform</strong> where your audience already spends time and <strong>one main format</strong> such as short video, written threads, newsletters or long articles. Spreading across five platforms in the first months usually produces five weak channels. Add more only when the first one runs reliably.</p>'''),
            ('pillars', 'Step 2: Define content pillars', '''<p>Content pillars are three to five recurring themes that your content returns to. For a startup writer they might be validation, pricing, tools and lessons from building. Pillars solve the blank-page problem: instead of asking what to post, you ask which pillar needs content this week.</p>
<p>For each pillar, keep a running list of questions your audience asks, mistakes you have seen and examples from your own work. Experience that only you have is the most valuable material you own.</p>'''),
            ('rhythm', 'Step 3: Build a weekly rhythm', '''<p>A rhythm you can sustain beats an ambitious schedule you abandon. A sample week for a solo creator publishing one main piece and a few small ones:</p>
<table>
<thead><tr><th>Day</th><th>Task</th><th>Time</th></tr></thead>
<tbody>
<tr><td>Monday</td><td>Collect ideas, pick the week's topic and outline the main piece</td><td>1 hour</td></tr>
<tr><td>Tuesday</td><td>Write or record the main piece</td><td>2 to 3 hours</td></tr>
<tr><td>Wednesday</td><td>Edit, add visuals, publish the main piece</td><td>1 to 2 hours</td></tr>
<tr><td>Thursday</td><td>Repurpose into short posts or clips</td><td>1 hour</td></tr>
<tr><td>Friday</td><td>Reply to comments, review numbers, note what worked</td><td>1 hour</td></tr>
</tbody>
</table>
<p>Adjust the times to your life, and protect them in your calendar like appointments.</p>'''),
            ('batch', 'Step 4: Batch and repurpose', '''<p>Batching means doing the same kind of task for several pieces at once, which cuts switching costs. Write three outlines in one sitting, record several clips in a row, or design a set of graphics together.</p>
<p>Repurposing turns one idea into many formats. One in-depth article can become a short summary post, a few quote graphics, a video script and a newsletter issue. You are not repeating yourself. Different people prefer different formats and see different channels. Tools such as an <a href="/tool/tools/image-resize">image resizer</a> and an <a href="/tool/tools/image-compressor">image compressor</a> help you reuse one visual across platforms quickly.</p>'''),
            ('hooks', 'Step 5: Write for attention, then deliver', '''<p>On any feed, the first line decides whether someone keeps reading or watching. A good hook promises something specific, such as a result, a surprising fact or a problem the viewer recognises. But the content must deliver on it. Misleading hooks win clicks and lose trust.</p>
<ul>
<li>Lead with the outcome: "How I cut my image sizes by 70% in five minutes".</li>
<li>Use concrete numbers and plain words.</li>
<li>End with a clear next step, whether reading a guide, replying or subscribing.</li>
</ul>'''),
            ('metrics', 'Step 6: Track metrics that matter', '''<p>Follower count is easy to see and a weak guide to progress. More useful signals include:</p>
<ul>
<li><strong>Retention or completion</strong> (how much of a video or article people consume).</li>
<li><strong>Shares and saves,</strong> which show content people found worth passing on.</li>
<li><strong>Replies and messages,</strong> a sign of real connection.</li>
<li><strong>Email signups or clicks</strong> to your own site, which show movement toward an owned audience.</li>
</ul>
<p>Review monthly, not daily. Keep what works, adjust what does not and avoid reacting to a single post.</p>'''),
            ('owned', 'Step 7: Build an audience you own', '''<p>Platforms change their algorithms and rules, and accounts can be lost. An <strong>owned audience</strong>, such as an email list or a website people visit directly, protects you. Offer something useful in exchange for an email address, like a checklist, a template or a short course, and mention it regularly. Even a small, engaged list is more valuable than a large audience you cannot reach.</p>'''),
            ('money', 'How creators earn', '''<p>Most sustainable creator income combines several sources over time:</p>
<ul>
<li><strong>Advertising</strong> on your own site or platform revenue sharing.</li>
<li><strong>Sponsorships and affiliate links,</strong> clearly disclosed, from products you genuinely use.</li>
<li><strong>Digital products</strong> such as templates, guides and courses.</li>
<li><strong>Services,</strong> including consulting and freelancing.</li>
<li><strong>Memberships</strong> for ongoing access to content or a community.</li>
</ul>
<p>Build trust first, then monetise. Income usually follows audience trust, not the other way round.</p>'''),
            ('burnout', 'Avoiding burnout', '''<ul>
<li>Set a publishing pace you can maintain even in a busy month, and treat extra output as a bonus.</li>
<li>Keep a small reserve of finished pieces for weeks when life interferes.</li>
<li>Take planned breaks and tell your audience, which they usually accept.</li>
<li>Stop comparing your first year to someone else's fifth.</li>
</ul>'''),
        ],
        'faq': [
            ('How often should I post?', 'As often as you can maintain with good quality for at least six months. Consistency matters more than volume, and a realistic weekly schedule beats a daily one you abandon.'),
            ('Which platform should I start on?', 'Choose the one where your audience already spends time and where your preferred format fits, then commit to it before adding others.'),
            ('Do I need a niche?', 'A clear focus makes it easier for people to understand why they should follow you. You can broaden gradually as your audience grows.'),
            ('How long until a creator business earns income?', 'It varies widely and often takes many months or longer. Plan for slow growth and keep costs low while you build.'),
        ],
        'tools': ['image-resize', 'image-compressor', 'image-crop', 'qr-generator', 'random-color-palette-generator'],
    },
    {
        'slug': 'how-to-write-a-value-proposition',
        'topic': 'marketing-growth',
        'subtopic': 'branding-sales-growth',
        'title': 'How to Write a Clear Value Proposition (With a Simple Template)',
        'description': 'Learn how to write a value proposition and positioning statement that customers understand, with a template, examples, a five-second test and common mistakes.',
        'intro': '''<p>A visitor lands on your website and decides within seconds whether it is for them. If they cannot tell what you offer, who it is for and why it is better than the alternatives, they leave. A value proposition is the short statement that answers those questions, and it is the foundation of your homepage, your pitch and your branding.</p>
<p>This guide shows how to write one, with a template, examples and a quick test to check that it works.</p>''',
        'takeaways': [
            'A value proposition states who you serve, what outcome you deliver and why you are the better choice.',
            'Customer outcomes matter more than feature lists.',
            'Use the words your customers use, not internal jargon.',
            'Test it: can a stranger explain it back after five seconds?',
        ],
        'sections': [
            ('what', 'What a value proposition is', '''<p>A value proposition is a clear statement of the benefit your product delivers and why a specific customer should choose it over alternatives. It is not a slogan and not a feature list. It is the promise that makes a visitor think "that is for me".</p>
<p>It differs from <strong>positioning</strong>, the place your product holds in a customer's mind relative to other options. Positioning is the strategy and the value proposition is how you express it to customers.</p>'''),
            ('ingredients', 'The four ingredients', '''<ol>
<li><strong>Customer:</strong> who it is for, as specifically as you can.</li>
<li><strong>Problem or need:</strong> what they are trying to get done.</li>
<li><strong>Outcome:</strong> the result they get, ideally measurable or concrete.</li>
<li><strong>Difference:</strong> why this is better than what they use today.</li>
</ol>'''),
            ('template', 'A simple template', '''<p>Start with this sentence and fill the blanks:</p>
<blockquote><p>We help <strong>[customer]</strong> do <strong>[job or outcome]</strong> so they can <strong>[benefit]</strong>, without <strong>[main pain or cost]</strong>.</p></blockquote>
<p>Example: <em>"We help freelance designers send invoices and get paid on time, so they can spend less time chasing clients, without learning accounting software."</em></p>
<p>A more formal version is the positioning statement popularised by Geoffrey Moore in <em>Crossing the Chasm</em>:</p>
<blockquote><p>For <strong>[target customer]</strong> who <strong>[need]</strong>, <strong>[product]</strong> is a <strong>[category]</strong> that <strong>[key benefit]</strong>. Unlike <strong>[alternative]</strong>, our product <strong>[difference]</strong>.</p></blockquote>
<p>Use it as an internal working document. Then turn it into natural language for your homepage.</p>'''),
            ('outcomes', 'Lead with outcomes, not features', '''<p>Features describe what a product has. Benefits describe what the customer gets. Customers buy outcomes.</p>
<table>
<thead><tr><th>Feature-focused</th><th>Outcome-focused</th></tr></thead>
<tbody>
<tr><td>AI-powered scheduling engine</td><td>Book meetings without the back-and-forth emails</td></tr>
<tr><td>256-bit encrypted storage</td><td>Keep client files private, even if a device is lost</td></tr>
<tr><td>Browser-based image compression</td><td>Shrink images in seconds without uploading them anywhere</td></tr>
</tbody>
</table>
<p>Keep the feature as proof, placed after the benefit.</p>'''),
            ('words', 'Use your customers\' words', '''<p>Your own product vocabulary rarely matches your customers'. Go back to your customer interviews, support emails and reviews, and copy the phrases people use to describe their problem. Those phrases will resonate more than clever language, and they are often the words people type into search engines, which helps SEO too. Our guide to <a href="/startups-business/customer-discovery-interviews">customer discovery interviews</a> explains how to collect them.</p>'''),
            ('place', 'Where to use it', '''<ul>
<li><strong>Homepage headline and subheading.</strong> The headline states the outcome, and the subheading adds who it is for and how.</li>
<li><strong>Page titles and meta descriptions.</strong></li>
<li><strong>Social profiles, bios and your email signature.</strong></li>
<li><strong>Pitch decks, sales calls and onboarding emails.</strong></li>
</ul>
<p>Consistency builds recognition. When the same promise appears everywhere, people remember it. A <a href="/tool/tools/character-counter">character counter</a> helps you fit it into titles, descriptions and bios.</p>'''),
            ('test', 'The five-second test', '''<ol>
<li>Show your homepage to someone who matches your customer for five seconds, then hide it.</li>
<li>Ask: what does this company do, who is it for and what would you do next?</li>
<li>If they cannot answer, simplify your wording and test with new people.</li>
</ol>
<p>Five or six people is enough to spot a pattern. If most struggle in the same way, the message needs work.</p>'''),
            ('mistakes', 'Common mistakes', '''<ul>
<li><strong>Being vague:</strong> "The all-in-one platform for modern teams" could be anything.</li>
<li><strong>Using jargon:</strong> words customers do not use or understand.</li>
<li><strong>Trying to speak to everyone,</strong> which makes the message weak for each group.</li>
<li><strong>Listing features</strong> with no outcome.</li>
<li><strong>Making claims you cannot prove,</strong> such as "the best" or "number one" without evidence.</li>
</ul>'''),
            ('identity', 'From message to brand', '''<p>Once the message is clear, the visual identity supports it: a consistent set of colours, fonts and a simple logo used the same way everywhere. Tools like a <a href="/tool/tools/color-converter">colour converter</a> and a <a href="/tool/tools/random-color-palette-generator">palette generator</a> help you pick and document colours. Keep it simple. Consistency matters more than complexity.</p>'''),
        ],
        'faq': [
            ('How long should a value proposition be?', 'One or two sentences. If it takes a paragraph, it is probably unfocused.'),
            ('What is the difference between a value proposition and a tagline?', 'A tagline is a short, memorable phrase for branding. A value proposition explains the specific benefit and for whom, and may be longer and more concrete.'),
            ('Should I have a different value proposition for each customer type?', 'If your customer groups have different needs, yes, you may need separate messages or landing pages for each. Start with the group you serve best.'),
            ('How do I know if my value proposition works?', 'Run the five-second test with people who match your customer, and watch whether your page converts visitors to sign-ups or enquiries after changing the wording.'),
        ],
        'tools': ['character-counter', 'word-counter', 'color-converter', 'random-color-palette-generator'],
    },
]
