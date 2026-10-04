Logrith

Logrith is a free, browser-based collection of practical tools designed to make everyday digital tasks faster, simpler, and easier to access.

"Visit Logrith" (https://logrith.in) · "GitHub Repository" (https://github.com/Plertankush/Logrith)

---

Overview

Logrith brings a broad collection of focused web utilities into one platform.

Instead of using a different website for every small task, users can use Logrith for calculations, conversions, text processing, developer utilities, image operations, PDF operations, general utilities, and selected AI-assisted features.

The product is designed around a simple principle:

«A useful tool should be easy to find, easy to understand, and quick to use.»

Logrith is intentionally lightweight and web-first. The current production website is primarily built using standard web technologies, reusable components, shared assets, individual tool pages, category pages, supporting content, and SEO infrastructure.

The platform is continuously evolving as new tools are added and existing implementations are improved.

---

What Logrith contains

Logrith currently organizes its utilities into several major areas.

Calculate & Convert

Tools for calculations, comparisons, conversions, and everyday numerical tasks.

Examples include:

- Percentage Calculator
- GST Calculator
- EMI Calculator
- Simple Interest Calculator
- Compound Interest Calculator
- Age Calculator
- Unit Converter
- Currency Converter
- Time Zone Converter
- Number Base Converter
- Discount Calculator
- Tip and Bill Split tools
- Salary and hourly conversion
- Typing-speed calculations
- Other calculation utilities

---

Text & Generators

Utilities for writing, transforming, comparing, cleaning, and generating text.

Examples include:

- Word Counter
- Character Counter
- Case Converter
- Text Diff Checker
- Duplicate Line Remover
- Slug Generator
- Lorem Ipsum Generator
- Random Name Generator
- Random Number Generator
- Text Reverser
- Markdown Previewer
- Number to Words Converter
- Morse Code Translator
- NATO Phonetic Alphabet Converter
- Fancy Text Generator
- Citation Generator
- Other text utilities

---

Developer Tools

Practical tools for developers and technical users.

Examples include:

- JSON Formatter
- JSON Validator
- JSON Minifier
- Base64 Encoder / Decoder
- URL Encoder / Decoder
- Hash Generator
- UUID Generator
- Regex Tester
- Password Generator
- CSS-related utilities
- Data conversion tools
- Developer-oriented formatting utilities
- Other small development helpers

The goal of this category is not to replace a complete development environment. It is to provide quick utilities for common tasks that are often solved repeatedly during development.

---

Image & PDF Tools

Browser-based tools for common image and document operations.

Image tools

Examples include:

- Image Converter
- Image Compressor
- Image Resize
- Image Crop
- Image Rotate and Flip
- Image to Base64
- Favicon Generator
- Image Watermark
- Image Color Picker
- SVG to PNG
- Photo Resizer
- Other image utilities

PDF tools

Examples include:

- PDF Merge
- PDF Split
- PDF to JPG
- JPG to PDF
- PDF Rotate
- PDF Compressor
- PDF Page Remover
- PDF Watermark
- PDF Password Protection
- PDF to Text
- Other PDF utilities

Where practical, these utilities are designed around browser-side processing so that simple operations can be performed directly on the user's device.

---

Utilities

General-purpose tools that do not belong to a single technical category.

Examples include:

- Password Strength Checker
- QR Code Generator
- Barcode Generator
- Passphrase Generator
- Browser Information Lookup
- Unit Price Comparator
- Payment Fee Calculator
- Countdown Timer
- World Clock
- Coin Flip and Dice Roller
- Random Team Generator
- File Size Converter
- Color Palette Generator
- Text Expander and Snippet tools
- Other general utilities

---

AI Tools

Logrith also includes selected tools where AI-assisted analysis can provide additional value.

Examples include:

- Resume Analyzer
- Website Analysis utilities
- Other focused AI-assisted tools

AI is treated as one part of the broader Logrith utility platform rather than the entire identity of the product.

---

How Logrith is built

Logrith is AI-coded

One of the most important characteristics of this repository is the development process.

Logrith is an AI-coded / AI-assisted software project.

The project is not presented as a traditional software product where the founder manually writes every line of code.

Instead, the founder defines the product and uses AI-assisted coding as an implementation layer.

The development model can be summarized as:

Founder → Product idea → Roadmap → Requirements → AI-assisted implementation → Review → Testing → Iteration → Deployment

This approach is intentional and is part of the project's identity.

---

The founder's role

The founder is responsible for product direction and final decisions.

That includes:

- Defining what Logrith should become
- Identifying problems worth solving
- Selecting tools to build
- Defining categories
- Designing the information architecture
- Defining user flows
- Writing requirements
- Defining the roadmap
- Prioritizing work
- Reviewing implementations
- Finding bugs and weaknesses
- Deciding what should be rebuilt
- Deciding what should ship
- Maintaining the product
- Planning future iterations

The founder does not claim that every line of code was individually handwritten.

The project instead uses a founder-led product process combined with AI-assisted implementation.

---

What AI-assisted coding is used for

AI-assisted development can be used throughout the implementation process.

Typical uses include:

- Generating initial page structures
- Implementing HTML, CSS, and JavaScript
- Creating repetitive utility interfaces
- Refactoring repeated code
- Debugging implementation problems
- Improving responsive behavior
- Iterating on layouts
- Working through implementation alternatives
- Creating supporting documentation
- Handling repetitive development work
- Translating product requirements into code
- Helping investigate bugs
- Producing first-pass implementations for new utilities

The result is then reviewed, tested, and iterated.

AI-generated code is not considered automatically correct.

Generated implementations can contain incorrect assumptions, bugs, weak accessibility, poor edge-case handling, browser inconsistencies, unnecessary complexity, or performance issues.

For that reason, AI is treated as a development accelerator rather than as an autonomous replacement for product judgment or engineering review.

---

Vibe coding, honestly documented

Logrith can be described as a vibe-coded project, but this should not be interpreted as:

«“One prompt generated the entire product automatically.”»

That is not the development process behind the repository.

The actual process is iterative.

A typical feature may go through:

1. Product requirement
2. User problem definition
3. Functional specification
4. Initial implementation
5. Visual review
6. Functional testing
7. Bug discovery
8. Refinement
9. Refactoring
10. Deployment
11. Post-deployment iteration

The founder remains responsible for determining whether the implementation actually solves the intended problem.

This makes the repository an example of founder-led product development with AI-assisted coding.

---

Why use AI-assisted development?

Logrith contains many focused utilities.

A conventional workflow can require a substantial amount of repetitive engineering work for each additional tool.

A new utility may need:

- A page
- A user interface
- Input handling
- Validation
- Output handling
- Responsive behavior
- Error states
- Accessibility considerations
- Navigation
- Metadata
- Documentation
- Testing

AI-assisted coding makes this repetitive work substantially faster to prototype and iterate.

It allows a small founder-led project to spend more time on:

- Product decisions
- User needs
- Information architecture
- Quality review
- Experimentation
- Roadmap development

and less time on repetitive boilerplate.

The goal is not to remove engineering discipline.

The goal is to increase the amount of useful product work that one founder can execute.

---

Architecture

The current Logrith website follows a relatively simple static-web structure.

A simplified view of the repository is:

.
├── assets/
│   ├── css/
│   ├── js/
│   ├── svg/
│   └── ...
├── blog/
├── categories/
├── components/
├── pages/
├── tools/
├── index.html
├── 404.html
├── load-components.js
├── robots.txt
├── sitemap.xml
├── sitemap-blog.xml
├── sitemap-pages.xml
├── sitemap-tools.xml
└── site.webmanifest

The exact structure may change as the platform evolves.

---

"index.html"

The main Logrith landing page and tool discovery surface.

It contains the primary navigation and grouped presentation of available utilities.

---

"tools/"

Individual utility pages.

Each page is intended to solve a focused task without requiring the user to navigate through a large application.

---

"categories/"

Category pages used to organize related utilities.

Categories make it easier for users to discover groups of tools rather than searching for every utility individually.

---

"pages/"

Supporting product and information pages.

These pages provide additional context around the platform and its ecosystem.

---

"components/"

Reusable website components.

The purpose of shared components is to keep repeated sections consistent while reducing unnecessary duplication.

---

"assets/"

Shared static resources such as:

- CSS
- JavaScript
- SVG icons
- Images
- Other front-end assets

---

"blog/"

Articles and supporting content.

The blog exists both as informational content and as another discovery surface for users looking for solutions to specific digital tasks.

---

Technology approach

The current production website is intentionally lightweight.

The codebase primarily uses:

- HTML
- CSS
- JavaScript
- Browser APIs
- Client-side processing where practical
- Reusable website components
- Static assets

The project does not introduce a large application architecture merely for the sake of complexity.

Technology decisions are based on the task being solved.

For a small browser utility, a simple implementation can often be more appropriate than a large application stack.

This may evolve in the future as the product requirements change.

---

Browser-first design

A core principle of Logrith is browser-first processing.

When a utility can reliably perform its operation directly in the browser, client-side processing is preferred.

This can apply to:

- Image processing
- Text transformations
- Calculations
- Conversions
- Formatting
- Encoding
- Decoding
- Other lightweight operations

Browser-side processing can reduce unnecessary network dependency and can make simple utilities faster and more private.

However, different tools can have different technical requirements.

Therefore, browser-first should be understood as a development preference rather than a claim that every single feature behaves identically.

---

Privacy approach

Privacy is an important product consideration for Logrith.

The preferred approach for tools that can work locally is to process user-provided data in the browser whenever practical.

This is particularly relevant to:

- Images
- PDF files
- Text
- Calculations
- Conversions
- Other local transformations

The project also aims to avoid unnecessary account requirements for basic utilities.

At the same time, privacy claims should always correspond to actual implementation behavior.

If a feature depends on a network request, external service, analytics, or another remote system, that behavior should be considered separately.

The repository therefore treats privacy as an engineering requirement rather than as a blanket marketing claim.

---

Product principles

1. Utility over complexity

Tools should solve a specific task without forcing users through unnecessary workflows.

2. Browser-first where practical

When a reliable client-side implementation exists, it is generally preferred.

3. Low friction

Users should be able to access simple utilities with minimal unnecessary setup.

4. Clear organization

The platform should make it easy to discover related tools.

5. Consistency

Individual tools should feel like parts of the same product.

6. Iteration

A shipped tool is not necessarily a finished tool.

The implementation may be improved, rewritten, replaced, or removed as the product evolves.

7. Real product feedback

Roadmap decisions should increasingly be informed by actual usage, technical findings, and observed user needs.

---

Development workflow

A typical Logrith development cycle looks like this:

1. Identify the problem

The founder starts with a specific task or user need.

2. Define the product requirement

The intended behavior, inputs, outputs, and user experience are specified.

3. Define the implementation direction

The founder determines how the feature should fit within the existing product structure.

4. AI-assisted implementation

AI is used to accelerate coding and repetitive implementation work.

5. Review

The resulting code and interface are inspected for correctness, usability, and consistency.

6. Test

The feature is tested against normal inputs, invalid inputs, edge cases, and device/browser behavior where relevant.

7. Iterate

Problems are fixed and the implementation is refined.

8. Deploy

The updated product is published.

9. Continue improving

Real usage and future roadmap decisions determine what happens next.

---

Quality and testing

AI-assisted development makes review and testing particularly important.

Depending on the utility, testing can include:

- Normal inputs
- Empty inputs
- Invalid inputs
- Edge cases
- Large inputs
- Mobile layouts
- Desktop layouts
- Browser compatibility
- File downloads
- Generated output files
- Navigation
- Error messages
- Accessibility
- Performance
- Privacy-related behavior

Testing depth depends on the complexity and potential impact of the feature.

---

Roadmap

The Logrith roadmap is intentionally founder-led.

The roadmap describes product direction rather than locking the project into a permanent technical architecture.

Near term

- Improve existing utilities
- Fix inconsistent tool behavior
- Improve mobile usability
- Improve accessibility
- Improve validation and error states
- Strengthen shared components
- Reduce unnecessary code duplication
- Improve page performance
- Improve internal navigation
- Improve tool discovery
- Expand useful documentation
- Improve repository documentation

---

Medium term

- Add more genuinely useful tools
- Improve existing categories
- Standardize common tool patterns
- Make new tools faster to implement
- Improve internal architecture
- Strengthen testing practices
- Improve performance across the platform
- Improve technical SEO
- Review older implementations
- Replace weak or unnecessary utilities
- Expand focused AI-assisted utilities where they provide clear user value

---

Longer term

The long-term goal is not simply to accumulate a large number of random utilities.

The direction is to build a coherent utility platform.

That means improving:

- Discovery
- Organization
- Reusability
- Quality
- Performance
- Reliability
- Documentation
- Maintainability

The number of tools is less important than whether the overall platform remains useful and easy to navigate.

---

What the roadmap does not mean

The roadmap is not a guarantee that every listed feature will be implemented exactly as written.

Product requirements can change.

Technical constraints can change.

User behavior can change.

Some ideas may be dropped.

Some features may be redesigned.

Some categories may be reorganized.

The roadmap exists to communicate the direction of the project rather than to freeze it.

---

Project status

Logrith is an active and evolving project.

The live website and repository can change as new utilities are added, bugs are fixed, implementations are refactored, and product priorities change.

The repository may contain a mixture of:

- Established production code
- New implementations
- Older implementations
- Refactoring work
- Experiments
- Supporting files
- SEO infrastructure
- Documentation

Not every part of the codebase should therefore be considered the final architectural form.

---

Running Logrith locally

Clone the repository:

git clone https://github.com/Plertankush/Logrith.git
cd Logrith

The site should be served using a local HTTP server.

For example, with Python:

python -m http.server 8000

Then open:

http://localhost:8000

Running through HTTP is recommended instead of opening "index.html" directly because the project uses relative resources and browser behavior that is more reliable when served from a local web server.

Any equivalent static web server can be used.

---

Contributing

Logrith is currently a founder-led project.

The repository is public, but public visibility does not automatically mean that every architectural decision or roadmap item is open to unrestricted changes.

Bug reports and useful technical feedback are welcome.

A strong issue report should include:

- The affected tool or page
- What happened
- What was expected
- Steps to reproduce
- Browser information where relevant
- Device information where relevant
- Example inputs or outputs
- Screenshots when useful

Feature proposals are more useful when they first explain the user problem and then describe the proposed implementation.

---

Reporting bugs

When reporting a bug, try to provide enough information to reproduce it.

Example:

Tool:
Image Compressor

Problem:
The downloaded file is larger than the expected output.

Steps:
1. Open the tool
2. Upload a specific image
3. Set compression target
4. Download result

Expected:
The resulting file should remain below the requested target where technically possible.

Actual:
The output exceeds the target.

Clear reproduction steps make debugging significantly easier.

---

License

No open-source license is currently specified for this repository.

Until a license is added, the code should not be assumed to be freely reusable, redistributable, or commercially exploitable.

The absence of a license means that normal copyright protections still apply.

---

Ownership

Logrith is created and maintained by Plert Ankush.

The project is part of a broader founder-led effort around software, AI-assisted development, web products, and building practical technology products.

Links

- Website: https://logrith.in
- GitHub profile: https://github.com/Plertankush
- Repository: https://github.com/Plertankush/Logrith

---

Founder & development model

Logrith is intentionally being built in a way that is different from the traditional startup development model.

There is no claim here that a large engineering organization manually produces every line of the product.

Instead, the project is driven by a founder who owns the product direction.

The founder defines:

What to build.
Why to build it.
Who it is for.
How it should be organized.
What the roadmap should be.
What should change.
What is ready to ship.

AI-assisted coding is then used to turn those decisions into working software.

This allows implementation speed to increase without giving up product direction.

---

Why this repository is public

The repository is public because the development process itself is part of the project.

Logrith is not only a collection of web utilities.

It is also an ongoing experiment in:

- Founder-led product development
- AI-assisted software development
- Rapid iteration
- Lightweight web architecture
- Browser-first utilities
- Building and maintaining a real public product with a small team footprint

The repository provides visibility into the actual implementation rather than only showing the finished website.

---

Final note

Logrith is a practical utility platform in progress.

It is built around focused tools, a lightweight web architecture, browser-first processing where practical, and a founder-led roadmap.

Most importantly, the repository is transparent about its development model:

«Logrith is AI-coded, but founder-directed.»

The founder defines the product.

The roadmap defines the priorities.

AI-assisted coding accelerates implementation.

Testing and review determine what ships.

And the product continues to evolve from there.

---

Logrith — Practical tools, built for the web.

© Plert Ankush
