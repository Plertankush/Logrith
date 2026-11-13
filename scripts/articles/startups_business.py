"""Articles for the Startups & Business topic. Rendered by scripts/build_articles.py."""

ARTICLES = [
    {
        'slug': 'how-to-validate-a-startup-idea',
        'topic': 'startups-business',
        'subtopic': 'startup-ideas-validation',
        'title': 'How to Validate a Startup Idea Without Writing Code',
        'description': 'A step-by-step method to test a startup idea before you build it: customer conversations, smoke tests, pre-sales and clear kill criteria.',
        'intro': '''<p>The most expensive mistake a founder can make is spending months building something nobody wants. Validation is the cheap alternative: a set of small experiments that tell you whether real people have the problem, care enough to act and might pay for a solution, all before you write production code.</p>
<p>This guide gives you a practical sequence you can run in a few weeks, along with the signals to trust and the ones to ignore.</p>''',
        'takeaways': [
            'Validate the problem first, then the solution, then the price.',
            'Trust behaviour (time, money, commitment) over compliments and likes.',
            'Decide what counts as success before you run an experiment.',
            'Be ready to stop or change direction. That is a good outcome of validation.',
        ],
        'sections': [
            ('what', 'What validation really means', '''<p>Validation does not mean getting people to say your idea is good. Friends and strangers are polite, and "I would definitely use that" costs nothing to say. Validation means collecting evidence that a specific group of people has a painful problem and takes real action to solve it.</p>
<p>Think of three questions, answered in order:</p>
<ol>
<li><strong>Problem:</strong> Is this a problem people actually have, often enough to matter?</li>
<li><strong>Solution:</strong> Does your approach solve it better than what they use today?</li>
<li><strong>Willingness to pay:</strong> Will they pay with money, time or effort?</li>
</ol>'''),
            ('define', 'Step 1: Define the customer and the problem', '''<p>Write one clear sentence: <em>"[Specific group] struggles with [specific problem] when [situation]."</em> "Small business owners need marketing" is too vague. "Freelance designers lose hours each month chasing late invoices" is testable, because you can find designers and ask.</p>
<p>A good problem is frequent, painful and already costing people money, time or stress. Look for evidence that they already try to solve it, with spreadsheets, workarounds, paid tools or hired help. Existing effort is one of the best signs a problem is real.</p>'''),
            ('research', 'Step 2: Do desk research', '''<p>Before you talk to anyone, spend a few hours finding out what already exists.</p>
<ul>
<li>Search for the problem in the words customers use, and read forum threads, reviews of existing tools and community posts.</li>
<li>List competitors and alternatives, including non-software ones like agencies and manual processes. Competition is usually a sign of demand, not a reason to quit.</li>
<li>Note what people complain about in reviews. Repeated complaints are product opportunities.</li>
</ul>'''),
            ('talk', 'Step 3: Talk to real people', '''<p>Aim for 10 to 20 conversations with people who match your customer sentence. Ask about their past behaviour, not about your idea: how they handled the problem last time, what it cost, what they tried and what frustrated them. Our guide to <a href="/startups-business/customer-discovery-interviews">customer discovery interviews</a> covers questions to ask and avoid.</p>
<p>You are looking for patterns. If most people describe the problem in similar terms, have tried to fix it and are unhappy with current options, you have a real problem. If they shrug, move on.</p>'''),
            ('smoke', 'Step 4: Run a smoke test', '''<p>A smoke test measures interest in a product that does not exist yet. The most common version is a simple landing page that states the problem, describes the outcome you promise and asks for a clear next step, such as joining a waitlist or pre-ordering.</p>
<ol>
<li>Write a headline that names the customer and the outcome.</li>
<li>Add three to five short benefits, and a single call to action.</li>
<li>Send targeted traffic, for example through communities where your customers gather, direct outreach or a small ad budget.</li>
<li>Measure the share of visitors who take the action.</li>
</ol>
<p>Set the success bar in advance. Conversion rates vary widely by audience and offer, so judge against your own earlier tests and the cost of acquiring each visitor, not against a number you read online. Asking for an email shows mild interest. Asking for a deposit or a booked call shows much more.</p>'''),
            ('manual', 'Step 5: Deliver the outcome manually', '''<p>Before you automate anything, try delivering the result by hand for a few customers. This is often called a concierge or "Wizard of Oz" test. If you plan an invoice-chasing tool, offer to chase invoices yourself for three freelancers using email and spreadsheets.</p>
<p>You learn what the real workflow is, what customers will pay for and which parts are worth automating. If you cannot get three people to try the manual version, software will not fix that.</p>'''),
            ('presell', 'Step 6: Ask for money early', '''<p>Payment is the strongest validation. Offer a pre-order, a paid pilot or a discounted founding-customer plan, and be honest about what is and is not built. Even a small number of paying customers teaches you more than hundreds of waitlist signups. If nobody will pay at any price, find out why before you build.</p>'''),
            ('decide', 'Step 7: Decide with kill criteria', '''<p>Before each experiment, write down what result would make you continue, change direction or stop. For example: "If fewer than 3 of 15 interviewees have tried to solve the problem, I will pick a different problem." Writing the rule first protects you from interpreting every result optimistically.</p>
<p>Possible outcomes are to <strong>proceed</strong> with a small build, <strong>pivot</strong> to a nearby problem you discovered, or <strong>stop</strong> and save months of effort.</p>'''),
            ('mistakes', 'Common validation mistakes', '''<ul>
<li>Asking friends and family, who tend to be supportive rather than honest.</li>
<li>Pitching the idea instead of listening to the problem.</li>
<li>Treating likes, follows and polite interest as demand.</li>
<li>Skipping the pricing question until after the product exists.</li>
<li>Moving the goalposts when the result is disappointing.</li>
</ul>'''),
        ],
        'faq': [
            ('How many customer interviews do I need?', 'Ten to twenty conversations with people who closely match your target customer is a practical starting range. Stop when you stop hearing new patterns.'),
            ('Do I need a prototype to validate an idea?', 'Not at first. Interviews, a landing page and a manual version of the service can all be done without writing code.'),
            ('What is a good landing page conversion rate?', 'It depends heavily on your audience and offer, so there is no universal number. Compare against your own earlier tests and decide your success bar before the test.'),
            ('Is a crowded market a bad sign?', 'Not by itself. Competitors show that people pay to solve the problem. What matters is whether you can serve a specific group better or differently.'),
        ],
        'tools': ['qr-generator', 'percentage-calculator', 'slug-generator'],
    },
    {
        'slug': 'customer-discovery-interviews',
        'topic': 'startups-business',
        'subtopic': 'startup-ideas-validation',
        'title': 'Customer Discovery Interviews: Questions to Ask and Avoid',
        'description': 'How to run customer interviews that reveal the truth: who to talk to, which questions work, which to avoid, and how to turn notes into decisions.',
        'intro': '''<p>Customer interviews are the cheapest, fastest research a founder can do, and they are also easy to do badly. Ask "Would you buy this?" and almost everyone says yes. The answer feels encouraging and tells you almost nothing.</p>
<p>The aim of a discovery interview is to learn about the other person's life, problems and past behaviour, not to pitch. This guide shows how to find people, what to ask, what to avoid and how to turn conversations into decisions.</p>''',
        'takeaways': [
            'Ask about specific past events, not opinions or future intentions.',
            'Do not pitch your idea. Keep the conversation about their world.',
            'Look for actions already taken: time, money and workarounds.',
            'Write notes immediately and look for patterns across interviews.',
        ],
        'sections': [
            ('principles', 'Three principles', '''<ol>
<li><strong>Talk about their life, not your idea.</strong> The moment you describe your product, people try to be nice.</li>
<li><strong>Ask about the past, not the future.</strong> What someone did last week is reliable. What they say they would do next month is not.</li>
<li><strong>Look for commitment.</strong> Compliments are free. Time, money and introductions are not.</li>
</ol>
<p>Rob Fitzpatrick's book <em>The Mom Test</em> popularised these rules and is worth reading in full. The summary here is our own.</p>'''),
            ('who', 'Who to interview', '''<p>Interview people who match the customer you wrote down, not whoever is easiest to reach. Good places to find them include:</p>
<ul>
<li>online communities, forums and social groups where they discuss the problem;</li>
<li>colleagues of colleagues and warm introductions;</li>
<li>direct, short messages to people who publicly talk about the problem;</li>
<li>customers of competing or adjacent products.</li>
</ul>
<p>Keep your request brief and honest: "I am researching how freelancers handle late invoices and would love 20 minutes of your experience. I am not selling anything."</p>'''),
            ('structure', 'A simple interview structure', '''<ol>
<li><strong>Warm up (2 minutes).</strong> Explain the purpose and ask about their role and context.</li>
<li><strong>Explore the problem (10 to 15 minutes).</strong> Ask them to walk through the last time it happened.</li>
<li><strong>Dig into what they do today (5 minutes).</strong> Tools, workarounds, costs and frustrations.</li>
<li><strong>Close (3 minutes).</strong> Ask who else you should talk to and whether you can follow up.</li>
</ol>'''),
            ('questions', 'Good questions and bad questions', '''<table>
<thead><tr><th>Avoid</th><th>Ask instead</th></tr></thead>
<tbody>
<tr><td>Would you use a tool that does X?</td><td>Tell me about the last time you had to deal with X. What happened?</td></tr>
<tr><td>Do you think this is a good idea?</td><td>How do you handle this today? What do you not like about it?</td></tr>
<tr><td>How much would you pay for this?</td><td>What does this problem cost you in time or money each month?</td></tr>
<tr><td>Would you ever buy a product like this?</td><td>Have you tried to fix this before? What did you try?</td></tr>
<tr><td>Don't you hate it when...?</td><td>How do you feel about how that process works?</td></tr>
</tbody>
</table>
<p>Useful follow-ups include "Why?", "What happened next?", "Can you show me?" and "Who else is involved?". Silence is also a tool. Let people finish and add more.</p>'''),
            ('signals', 'Signals worth trusting', '''<ul>
<li><strong>They already pay or spend effort</strong> on a workaround, whether a tool, a freelancer or a spreadsheet they maintain.</li>
<li><strong>They describe the problem emotionally,</strong> with real frustration and specific examples.</li>
<li><strong>They ask when they can try it,</strong> offer to introduce others or agree to a follow-up.</li>
<li><strong>They have looked for solutions</strong> and found the options lacking.</li>
</ul>
<p>Signals to discount: "That sounds cool", "I would probably use that", vague enthusiasm and feature requests without a story behind them.</p>'''),
            ('commitment', 'Ask for a small commitment', '''<p>At the end, test how real the interest is with a proportionate request: a follow-up call, an introduction to a colleague, access to sample data, a pre-order or a deposit. If someone who loved the idea will not spend 15 more minutes or make one introduction, their enthusiasm was polite.</p>'''),
            ('notes', 'Take notes and find patterns', '''<ol>
<li>Record the conversation if the person agrees, or take notes as you go, and write a summary within an hour.</li>
<li>Separate facts (what they did) from opinions and from your interpretations.</li>
<li>Keep a simple table: person, role, problem described, current solution, quotes, commitment.</li>
<li>After ten or so interviews, tag recurring problems and group them. Count how many people mention each one.</li>
</ol>
<p>Patterns across several people matter. A single vivid story does not make a market.</p>'''),
            ('mistakes', 'Mistakes to avoid', '''<ul>
<li>Pitching in the first five minutes.</li>
<li>Asking leading or hypothetical questions.</li>
<li>Talking more than the interviewee.</li>
<li>Only interviewing supportive friends.</li>
<li>Collecting compliments and counting them as evidence.</li>
</ul>'''),
        ],
        'faq': [
            ('How long should a discovery interview be?', 'Twenty to thirty minutes is usually enough. Respect the time you asked for.'),
            ('Should I record the interview?', 'Recording helps you listen, but ask permission first and follow the rules where you and the participant are located. Otherwise take careful notes.'),
            ('Should I pay people for their time?', 'Not required for short conversations with people who care about the problem, though a small thank-you can help when you ask busy professionals for longer sessions.'),
            ('What if people do not have the problem?', 'That is useful information. Either you are talking to the wrong group, or the problem is not painful enough. Adjust your customer definition or choose another problem.'),
        ],
        'tools': ['text-summarizer-basic', 'word-counter', 'random-team-generator'],
    },
    {
        'slug': 'saas-pricing-models-explained',
        'topic': 'startups-business',
        'subtopic': 'saas-product-building',
        'title': 'SaaS Pricing Models Explained: Flat, Tiered, Per-Seat and Usage-Based',
        'description': 'Compare the main SaaS pricing models, learn how to choose a value metric, structure plans and avoid the common pricing mistakes of early-stage products.',
        'intro': '''<p>Pricing is one of the highest-leverage decisions in a software business, and one of the least tested. Founders often pick a number that "feels right", launch and never revisit it. Yet price shapes who signs up, how much you earn per customer and whether the business can survive.</p>
<p>This guide explains the main SaaS pricing models, how to choose what to charge for, how to structure plans and how to improve your pricing over time.</p>''',
        'takeaways': [
            'Price on a value metric that grows as customers get more value.',
            'Three tiers with a clear difference between them is a reliable starting structure.',
            'Early prices are almost always too low. Test and raise them.',
            'Pricing is an ongoing experiment, not a one-time decision.',
        ],
        'sections': [
            ('metric', 'Start with the value metric', '''<p>A <strong>value metric</strong> is the unit you charge for, such as seats, projects, contacts, messages or gigabytes. A good one rises when the customer gets more value and is easy to understand and forecast.</p>
<ul>
<li>An email tool charging per contact aligns with a customer's list growing.</li>
<li>A project management tool charging per user aligns with team size.</li>
<li>A storage product charging per gigabyte aligns with usage.</li>
</ul>
<p>Ask: when a customer is delighted and uses more of our product, what grows? Charge for that.</p>'''),
            ('models', 'The main pricing models', '''<table>
<thead><tr><th>Model</th><th>How it works</th><th>Good for</th><th>Watch out for</th></tr></thead>
<tbody>
<tr><td>Flat rate</td><td>One price, all features</td><td>Simple products with one customer type</td><td>Leaves money on the table from large customers</td></tr>
<tr><td>Tiered</td><td>Several plans with growing limits and features</td><td>Most SaaS products</td><td>Too many tiers confuse buyers</td></tr>
<tr><td>Per seat</td><td>Price per user</td><td>Collaboration and team tools</td><td>Customers may share logins or limit users</td></tr>
<tr><td>Usage-based</td><td>Pay for what you consume</td><td>APIs, infrastructure and AI tools</td><td>Unpredictable bills and revenue</td></tr>
<tr><td>Freemium</td><td>Free plan plus paid upgrades</td><td>Products with strong viral or low cost-to-serve use</td><td>Support and hosting costs for free users, low conversion</td></tr>
<tr><td>Hybrid</td><td>Base subscription plus usage or add-ons</td><td>Products with both fixed and variable costs</td><td>Complexity in explaining the bill</td></tr>
</tbody>
</table>'''),
            ('tiers', 'Structuring tiers', '''<p>A common pattern is three plans, often named something like Starter, Pro and Business.</p>
<ul>
<li><strong>Starter</strong> serves individuals or small teams and covers the core job.</li>
<li><strong>Pro</strong> is the plan you want most customers to pick, with the features and limits a growing team needs.</li>
<li><strong>Business</strong> adds advanced controls, higher limits and support for larger customers.</li>
</ul>
<p>Make the differences meaningful and tied to the value metric. Do not hide the feature everyone needs in the highest tier, and do not create plans so similar that the choice is confusing. Show the plan you recommend visually.</p>'''),
            ('how-to-set', 'How to set the price', '''<ol>
<li><strong>Work out your floor.</strong> Calculate your cost to serve a customer (hosting, support, payment fees) and the margin you need. See our guide to <a href="/startups-business/unit-economics-for-founders">unit economics</a>.</li>
<li><strong>Look at alternatives.</strong> What do customers pay now, including spreadsheets or manual work? Price in relation to the value and the options, not only to competitors.</li>
<li><strong>Ask customers.</strong> Questions such as "At what price would this be so expensive you would not consider it, and at what price would it be a bargain?" give a range, though real purchases are better evidence.</li>
<li><strong>Launch, observe and adjust.</strong> Watch conversion, churn and which plans people choose.</li>
</ol>'''),
            ('annual', 'Monthly, annual and discounts', '''<p>Offering annual billing at a discount, commonly the equivalent of one or two months free, improves cash flow and reduces churn because customers commit for longer. Calculate discounts carefully with a <a href="/tool/tools/percentage-calculator">percentage calculator</a> so you know the effective price. Be cautious with deep, permanent discounts that train customers to wait for sales.</p>'''),
            ('raise', 'When and how to raise prices', '''<p>Early-stage prices are usually too low. Signs that you may be underpriced include almost no pushback, customers saying it is "a steal" and heavy demand you struggle to serve. Raising prices for new customers first is the lowest-risk approach. For existing customers, give notice, explain the added value and consider keeping loyal customers on their current price for a period.</p>'''),
            ('mistakes', 'Common pricing mistakes', '''<ul>
<li>Pricing by cost alone and ignoring the value delivered.</li>
<li>Copying a competitor without understanding their customers or costs.</li>
<li>Launching with many plans and add-ons.</li>
<li>Charging a metric customers cannot predict.</li>
<li>Never revisiting the price.</li>
</ul>'''),
        ],
        'faq': [
            ('What is the best pricing model for a new SaaS product?', 'There is no single best model. A simple tiered subscription priced on a clear value metric works for most early products. Use usage-based pricing when your costs and customer value scale directly with consumption.'),
            ('Should I offer a free plan?', 'Only if the cost to serve free users is low and there is a clear path to upgrade. A free trial is often a safer start for products that need setup.'),
            ('How many pricing tiers should I have?', 'Three is a common default because it makes comparison easy. Start simple and add complexity only when customers ask for it.'),
            ('How often should I change prices?', 'Review pricing regularly, for example once or twice a year, and after major product improvements.'),
        ],
        'tools': ['percentage-calculator', 'discount-stacking-calculator', 'compound-interest-calculator', 'currency-converter'],
    },
    {
        'slug': 'unit-economics-for-founders',
        'topic': 'startups-business',
        'subtopic': 'business-models-finance-operations',
        'title': 'Unit Economics for Founders: Margins, Break-Even and Cash Flow',
        'description': 'Understand gross margin, CAC, LTV, break-even and cash runway with worked examples, so you can tell whether your business model actually works.',
        'intro': '''<p>A business can have happy customers and rising revenue and still fail, because the numbers behind each sale do not work. Unit economics is the discipline of looking at the money in and out for a single customer or order and asking whether growth makes you healthier or poorer.</p>
<p>This guide explains the key terms with simple worked examples. The numbers are illustrative, so replace them with your own.</p>''',
        'takeaways': [
            'Gross margin shows what is left after the direct cost of delivering what you sell.',
            'Compare customer lifetime value with the cost of acquiring a customer.',
            'Break-even tells you the volume you need to cover fixed costs.',
            'Profit and cash are different. Plan your runway around cash.',
        ],
        'sections': [
            ('revenue-cost', 'Revenue, costs and margin', '''<p><strong>Revenue</strong> is what customers pay you. <strong>Cost of goods sold (COGS)</strong>, or cost of revenue for software, is the direct cost of delivering the product: hosting, payment fees, materials, shipping and customer support tied to usage.</p>
<p><strong>Gross margin</strong> = (Revenue minus COGS) divided by Revenue.</p>
<p><em>Example:</em> You sell a subscription for $30 a month. Hosting, payment fees and support cost $6 per customer. Gross profit is $24, so gross margin is 24 ÷ 30 = 80%.</p>
<p>A <a href="/tool/tools/percentage-calculator">percentage calculator</a> makes this quick for any price and cost.</p>'''),
            ('contribution', 'Contribution margin and fixed costs', '''<p><strong>Fixed costs</strong> do not change with each sale: salaries, tools, rent and software subscriptions. <strong>Variable costs</strong> grow with volume. The profit each additional sale contributes toward covering fixed costs is its <strong>contribution margin</strong>, which is price minus variable cost per unit.</p>'''),
            ('breakeven', 'Break-even point', '''<p>Break-even volume = Fixed costs ÷ Contribution margin per unit.</p>
<p><em>Example:</em> Fixed costs are $3,000 a month and each customer contributes $24 after variable costs. Break-even is 3,000 ÷ 24 = 125 customers. Below that you lose money each month, and above it every extra customer adds to profit.</p>
<p>Use this to set realistic targets and to test what happens if you change price or costs.</p>'''),
            ('cac-ltv', 'CAC and LTV', '''<p><strong>Customer acquisition cost (CAC)</strong> is the total sales and marketing spend divided by the number of new customers it won in the same period.</p>
<p><strong>Customer lifetime value (LTV)</strong> estimates the gross profit a customer generates before leaving. A simple version for subscriptions is:</p>
<p>LTV = Monthly revenue per customer × Gross margin ÷ Monthly churn rate.</p>
<p><em>Example:</em> $30 revenue × 80% margin = $24 gross profit a month. If 4% of customers cancel each month, expected lifetime is about 25 months (1 ÷ 0.04), so LTV = 24 ÷ 0.04 = $600.</p>
<p>If CAC is $150, LTV is four times CAC. Many investors look for at least 3 to 1 as a rough rule of thumb, but the right ratio depends on your business and how fast you want to grow. Treat these as estimates, because churn changes as you learn.</p>'''),
            ('payback', 'CAC payback period', '''<p>Payback period = CAC ÷ Monthly gross profit per customer. With a $150 CAC and $24 monthly gross profit, you recover acquisition costs in about 6 months (150 ÷ 24 = 6.25). Shorter payback means you can reinvest faster and need less cash to grow.</p>'''),
            ('cash', 'Profit is not cash', '''<p>Profit is what remains after costs on paper. Cash is what is in the bank. A profitable business can run out of cash if customers pay late, you buy inventory in advance or you pay annual costs up front. Conversely, annual prepayments can make a young company cash-rich before it is profitable.</p>
<p><strong>Burn rate</strong> is the net cash you spend per month, and <strong>runway</strong> is cash in the bank divided by monthly burn. With $18,000 in the bank and a net burn of $3,000 a month, you have six months. Revisit it monthly and decide early what to cut or fix, not in the last month.</p>'''),
            ('borrowing', 'The real cost of borrowing', '''<p>If you finance equipment or growth with a loan, compare the total interest, not only the monthly payment. An <a href="/tool/tools/emi-calculator">EMI calculator</a> shows the total repayable on a loan, and a <a href="/tool/tools/compound-interest-calculator">compound interest calculator</a> shows how savings or debt grow over time. Check whether projected cash flow can cover repayments even in a slow month.</p>'''),
            ('checklist', 'A monthly numbers checklist', '''<ul>
<li>Revenue, COGS and gross margin.</li>
<li>New customers, CAC and payback period.</li>
<li>Churn rate and estimated LTV.</li>
<li>Fixed costs and break-even volume.</li>
<li>Cash in the bank, burn and runway.</li>
</ul>'''),
        ],
        'faq': [
            ('What is a good gross margin?', 'It varies by industry. Software businesses often have high gross margins, while physical products and services usually have lower ones. Compare against similar businesses.'),
            ('Is an LTV to CAC ratio of 3 to 1 required?', 'It is a common rule of thumb, not a law. A lower ratio can work with fast payback or strong cash, and a higher one may mean you are under-investing in growth.'),
            ('What is the difference between revenue and profit?', 'Revenue is total sales. Profit is what remains after subtracting costs. Gross profit subtracts direct costs, and net profit subtracts all costs.'),
            ('How do I estimate churn for a new product?', 'Start with the share of customers who cancel each month once you have a few months of data. Early estimates are rough and should be updated as the data grows.'),
        ],
        'tools': ['percentage-calculator', 'emi-calculator', 'compound-interest-calculator', 'discount-stacking-calculator', 'salary-hourly-converter'],
    },
]
