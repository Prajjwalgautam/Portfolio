# Guides: answer-first articles for questions people type into Google and ask AI tools.
# Each one opens with a short, quotable answer (the part ChatGPT, Perplexity and AI Overviews lift),
# then explains it, then links to the matching service. Facts only from real projects; no invented numbers.

GUIDES = [
 dict(slug='what-is-aeo-geo',
  title='What Are AEO and GEO? A Plain-English Guide for Businesses in Nepal',
  desc='AEO and GEO explained simply: how to get your business quoted by ChatGPT, Perplexity and Google AI Overviews, and how they differ from SEO. A practical guide from Kathmandu.',
  h1='What are AEO and GEO?',
  answer='AEO (Answer Engine Optimization) makes your content the answer that AI tools and voice assistants quote. GEO (Generative Engine Optimization) makes AI tools such as ChatGPT, Gemini and Perplexity recognise and recommend your business by name. Both build on SEO, which gets your website ranked in Google and Bing.',
  sections=[
   ('SEO, AEO and GEO side by side', [
     'Think of them as three goals for the same website. SEO gets you ranked: your page appears when someone searches. AEO gets you quoted: an AI tool lifts your answer into its reply. GEO gets you recommended: when someone asks an AI tool who to hire, your name comes up.',
     'They overlap. AI answers often draw on pages that already rank, so a site with weak SEO rarely wins at AEO or GEO.'],
    [('SEO', 'Search Engine Optimization', 'Ranked in Google and Bing results'),
     ('AEO', 'Answer Engine Optimization', 'Quoted in AI answers and featured snippets'),
     ('GEO', 'Generative Engine Optimization', 'Recognised and recommended by name in AI tools')]),
   ('Why this matters for businesses in Nepal now', [
     'More buyers now start with a question to an AI tool instead of a list of links: "Who builds real-estate websites in Kathmandu?" or "Best SEO expert in Nepal". The tool picks a few names and pages. If your facts are unclear or missing, it picks someone else.',
     'Many Nepali businesses still have thin websites with no structured data and inconsistent details across Facebook, Google Maps and directories. That makes this an early window: clear, consistent businesses stand out quickly.'], None),
   ('How AEO works: write the answer first', [
     'AI tools quote short, direct answers. Put a 40 to 60 word answer right under each question heading, then explain. Use the exact wording people search for, such as "How much does a website cost in Kathmandu?", as headings.',
     'Mark up your questions and answers with FAQ structured data, keep pages fast, and make sure crawlers like GPTBot, ClaudeBot and PerplexityBot are allowed in robots.txt.'], None),
   ('How GEO works: be the same everywhere', [
     'AI tools trust facts they can confirm in several places. Your name, what you do, your city, your website and your best work should read the same on your site, LinkedIn, GitHub, Google Business Profile and any directory.',
     'On your site, structured data (Person or Organization, Service, FAQ) tells machines exactly who you are. An llms.txt file gives AI tools a plain-text summary. A short "disambiguating description" helps when other people share your name.'], None),
   ('A simple checklist you can start today', [], None),
  ],
  checklist=['Verify your site in Google Search Console and Bing Webmaster Tools, and submit your sitemap.',
             'Add an answer-first FAQ to every service page, with FAQ structured data.',
             'Allow AI crawlers in robots.txt and publish an llms.txt summary.',
             'Use one name, one description and one website link on every profile.',
             'Each month, ask ChatGPT, Perplexity and Gemini the questions your buyers ask, and note who they name.'],
  faq=[('Is AEO the same as SEO?', 'No. SEO is about ranking a page in search results. AEO is about having your answer quoted by AI tools and featured snippets. They work best together.'),
       ('How long do AEO and GEO take?', 'On-site changes take days. Being named by AI tools usually takes one to three months, because the tools need to see consistent facts about you in several trusted places.'),
       ('Can a small business in Nepal do AEO?', 'Yes. The basics, which are clear answers, structured data and consistent profiles, cost little and matter more than budget.')],
  related=['aeo-geo-expert','seo-expert-nepal']),

 dict(slug='get-business-on-google-nepal',
  title='How to Get Your Business on Google in Nepal: Free Step-by-Step Guide',
  desc='Get your Nepali business found on Google and Bing for free: Search Console, sitemaps, Google Business Profile and the fixes that matter. Steps tested on a live Kathmandu site.',
  h1='How to get your business on Google in Nepal',
  answer='Verify your website in Google Search Console, submit your sitemap, request indexing for your main pages, and create a Google Business Profile. Then import the site into Bing Webmaster Tools. All of this is free and takes about an hour; your pages usually start appearing within days.',
  sections=[
   ('Step 1: Check whether Google already knows your site', [
     'Search Google for site:yourdomain.com. If nothing appears, Google has not indexed your site yet, and no amount of keyword work will help until it does.'], None),
   ('Step 2: Verify your site in Google Search Console', [
     'Go to search.google.com/search-console, add your site as a URL-prefix property, and verify it. The simplest method is uploading the small HTML file Google gives you to the root of your site. Keep that file there permanently, because Google rechecks it.'], None),
   ('Step 3: Submit your sitemap and request indexing', [
     'Your sitemap.xml lists every page you want found. Submit it under Sitemaps. Then use URL inspection on your most important pages, such as your home page and main service pages, and click Request indexing. Requesting the same page again does not speed it up.'], None),
   ('Step 4: Add Bing, which also feeds AI search', [
     'In Bing Webmaster Tools, choose Import from Google Search Console. It copies your site and sitemap in one click. Bing results power Microsoft Copilot and DuckDuckGo and feed into ChatGPT search, so this step matters for AI visibility too.',
     'If your site supports IndexNow, it can notify Bing and other engines the moment a page changes.'], None),
   ('Step 5: Create a Google Business Profile', [
     'A Google Business Profile puts you on Google Maps and in "near me" searches. Service businesses without a shop can choose a service area such as the Kathmandu Valley instead of showing a street address. Use the same name, phone number and website as on your site.'], None),
   ('Step 6: Fix what stops pages from ranking', [], None),
  ],
  checklist=['One clear H1 per page that uses the words people search for.',
             'A page title under about 60 characters, starting with the main keyword.',
             'A meta description that answers the search in one or two sentences.',
             'Fast loading on mobile data, with compressed images.',
             'Real text that Google can read, not only images or animations.'],
  faq=[('How long does it take to appear on Google in Nepal?', 'After you submit a sitemap and request indexing, pages usually appear within a few days to two weeks. Ranking well for competitive searches takes longer.'),
       ('Do I have to pay Google to appear in search?', 'No. Organic search listings are free. Google Ads are a separate, paid option.'),
       ('Does a .com.np domain rank in Nepal?', 'Yes. A .np domain is a clear local signal, and it ranks for searches worldwide too.')],
  related=['seo-expert-nepal','web-developer-kathmandu']),

 dict(slug='hire-ai-engineer-nepal',
  title='How to Hire an AI Engineer in Nepal: A Practical Checklist',
  desc='What an AI engineer does, what to ask before you hire one in Nepal, and how a first AI project should run. A checklist from a Kathmandu AI engineer and full-stack developer.',
  h1='How to hire an AI engineer in Nepal',
  answer='Hire an AI engineer who can show working software, not only demos: ask for a live project, check they can connect AI to your own data and systems, agree a small first project with a fixed price, and make sure you will own the code, prompts and data at the end.',
  sections=[
   ('What an AI engineer actually does', [
     'An AI engineer turns AI models into working software: choosing a model, writing and testing prompts, connecting the model to your documents or customer data, building the screen people use, and keeping costs and errors under control.',
     'For most businesses that means a support assistant that answers from your own content, an automation that moves data between apps, or AI features inside an existing website or app.'], None),
   ('Six questions to ask before you hire', [], None),
  ],
  checklist=['Can you show me a live project, not only a demo or a screenshot?',
             'How will you connect the AI to our data, and what data leaves our systems?',
             'What will it cost to run each month, not only to build?',
             'How will we test that the answers are correct and on-brand?',
             'Who owns the code, the prompts and the data when the project ends?',
             'Can you also build the website or app the feature lives in?'],
  extra=[
   ('Start with a small first project', [
     'A good first AI project takes two to six weeks and solves one clear problem, such as answering the ten most common customer questions or drafting a weekly report. It proves the value before a larger budget is spent.'], None),
   ('Why Nepal is a good place to hire', [
     'Kathmandu has a growing pool of developers who work in English with clients abroad. The time zone (UTC+5:45) overlaps with Asia, the Middle East, Europe and Australia, and rates are usually lower than in the US or Europe for the same quality of work.'], None),
  ],
  faq=[('Do I need a data scientist or an AI engineer?', 'For most business projects, an AI engineer. Data scientists build and train models from scratch; AI engineers use existing models to build products, which is what most businesses need.'),
       ('Freelancer or agency?', 'A freelancer is usually faster and cheaper for focused projects, and you speak to the person writing the code. An agency suits very large projects with many people.'),
       ('Can an AI engineer work on my existing website?', 'Yes, if they are also a web developer. Ask which frameworks they have shipped, such as Laravel, Node.js or Next.js.')],
  related=['ai-engineer-nepal','hire-ai-developer']),

 dict(slug='real-estate-marketing-nepal-guide',
  title='Real Estate Marketing in Nepal: What Works Online',
  desc='What actually sells property online in Nepal: short videos, fast listing pages, quick WhatsApp replies, local SEO and lead ads. Lessons from building the Nepal Bhoomi platform.',
  h1='Real estate marketing in Nepal: what works online',
  answer='In Nepal, property sells online through short videos on Facebook, Instagram and TikTok, fast listing pages with a clear price and location, quick replies on WhatsApp, local SEO for areas such as Kathmandu, Lalitpur and Bhaktapur, and lead ads that send enquiries straight to your team.',
  sections=[
   ('Video comes first', [
     'Buyers scroll before they search. A 30 to 60 second property video with the price, location and three best features does more than a gallery of photos. Consistent branding, such as the same intro, captions and a short sound logo, makes a series recognisable.',
     'Building the videos partly in code, as with Remotion, lets a small team publish often without starting from a blank timeline each time.'], None),
   ('Listing pages that convert', [
     'Every video should lead to a fast page with the price, area, road access, map location, photos and a one-tap WhatsApp button. Slow pages lose buyers on mobile data.'], None),
   ('Local SEO for Kathmandu Valley areas', [
     'People search by place: "land for sale in Budhanilkantha", "house for rent in Lalitpur". Pages and video titles that use these place names, plus a Google Business Profile, catch these searches.'], None),
   ('Lead ads and tracking', [
     'Meta lead ads work well for property because the form is pre-filled and quick. Track every enquiry to the ad and video that brought it, and move budget to what produces real site visits.'], None),
   ('Trust and security', [
     'Buyers and sellers share phone numbers and documents. A property platform should protect them: secure sign-in, two-factor authentication for staff and an audit log of changes. The Nepal Bhoomi platform was built this way.'], None),
  ],
  checklist=['Publish short property videos every week with price and location in the first seconds.',
             'Link each video to a fast listing page with a WhatsApp button.',
             'Use area names in page titles, video titles and captions.',
             'Run lead ads with tracking, and reply to enquiries within minutes.',
             'Keep a monthly report of enquiries, visits and sales by channel.'],
  faq=[('Which social media is best for property in Nepal?', 'Facebook and Instagram reach the most buyers; TikTok works well for short property tours. Use the same video across all three.'),
       ('Do I need a website if I sell on Facebook?', 'Yes. A website with listings ranks on Google, builds trust and keeps your enquiries when social reach drops.'),
       ('Can you build a property listing website?', 'Yes. Prajwal Gautam co-built the Nepal Bhoomi real-estate platform and builds listing sites with admin panels and enquiry tracking.')],
  related=['real-estate-marketing-nepal','ai-video-production']),

 dict(slug='nextjs-vs-laravel-nepal',
  title='Next.js vs Laravel for a Business Website or Web App in Nepal',
  desc='Next.js or Laravel for your website or web app? A plain comparison of speed, SEO, hosting, hiring and cost, from a developer who has shipped production systems in both.',
  h1='Next.js vs Laravel: which should you choose?',
  thead=('Framework','Built on','Best at'),
  answer='Choose Next.js for fast, SEO-friendly websites and modern web apps with rich interfaces. Choose Laravel when your team already works in PHP, you need cheap shared hosting, or the project is mostly forms, records and admin work. Both are solid; the team that maintains it matters more than the framework.',
  sections=[
   ('The short comparison', [], [
     ('Next.js', 'React framework (JavaScript or TypeScript)', 'Very fast pages, strong SEO, rich interfaces; hosting on Vercel or a Node server'),
     ('Laravel', 'PHP framework', 'Fast to build admin-heavy systems; runs on low-cost PHP hosting common in Nepal')]),
   ('When Next.js is the better choice', [
     'Pick Next.js for marketing sites that must rank on Google, products with interactive screens, and projects that may grow into a mobile app sharing the same backend. The Nepal Bhoomi platform uses a Next.js API with PostgreSQL for these reasons.'], None),
   ('When Laravel is the better choice', [
     'Pick Laravel when your hosting is a standard PHP plan, your team knows PHP, or the system is mainly records, forms and reports, such as an HR or school system. I built a Laravel HR system and the Laravel payment and shipping features of the Sayapatri e-commerce platform; this kind of work is quick to build and easy to host in Laravel.'], None),
   ('What matters more than the framework', [], None),
  ],
  checklist=['Who will maintain the code after launch, and what do they know?',
             'Where will it be hosted, and what does that cost each month?',
             'Does it need to rank on Google, or is it an internal tool?',
             'Will a mobile app share the same data later?'],
  faq=[('Is Laravel outdated?', 'No. Laravel is actively developed and widely used, especially for admin-heavy systems and PHP hosting.'),
       ('Is Next.js good for SEO?', 'Yes. It can render pages on the server, so search engines and AI crawlers see full content quickly.'),
       ('Can you move a Laravel site to Next.js later?', 'Yes, often step by step: keep Laravel as the backend API and build a Next.js front end on top.')],
  related=['full-stack-developer-nepal','web-developer-kathmandu']),
]
