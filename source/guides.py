# Guides: answer-first articles for questions people type into Google and ask AI tools.
# Each one opens with a short, quotable answer (the part ChatGPT, Perplexity and AI Overviews lift),
# then explains it, then links to the matching service. Facts only from real projects; no invented numbers.
# Headings and FAQs follow what the top 5 Google results cover for each topic (see docs/seo-keyword-research.md).
import datetime
YEAR = datetime.date.today().year

GUIDES = [
 dict(slug='what-is-aeo-geo',
  title=f'AEO vs GEO vs SEO: What’s the Difference? A Plain-English Guide ({YEAR})',
  desc='What AEO and GEO mean, how they differ from SEO, and how to get your business cited by ChatGPT, Perplexity, Gemini and Google AI Overviews. Practical steps from Kathmandu.',
  h1='What are AEO and GEO?',
  answer='AEO (Answer Engine Optimization) makes your content the answer that AI tools, featured snippets and voice assistants quote. GEO (Generative Engine Optimization) makes AI tools such as ChatGPT, Gemini and Perplexity cite and recommend your brand by name. Both build on SEO, which gets your website ranked in Google and Bing.',
  sections=[
   ('AEO vs GEO vs SEO: what’s the difference?', [
     'Think of them as three goals for the same website. SEO gets you ranked: your page appears when someone searches. AEO gets you quoted: an answer engine lifts your answer into a featured snippet, a voice reply or an AI Overview. GEO gets you cited and recommended: when someone asks a generative AI tool who to hire, your brand comes up.',
     'They overlap. AI answers often draw on pages that already rank, so a site with weak SEO rarely wins at AEO or GEO.'],
    [('SEO', 'Search Engine Optimization', 'Ranked in Google and Bing results'),
     ('AEO', 'Answer Engine Optimization', 'Quoted in featured snippets, voice answers and AI Overviews'),
     ('GEO', 'Generative Engine Optimization', 'Cited and recommended by ChatGPT, Gemini, Perplexity and Copilot')]),
   ('Why this matters for businesses in Nepal now', [
     'More buyers now start with a question to an AI tool instead of a list of links: "Who builds real-estate websites in Kathmandu?" or "Best SEO expert in Nepal". The tool picks a few names and pages to cite. If your facts are unclear or missing, it cites someone else.',
     'Many Nepali businesses still have thin websites with no structured data and different details on Facebook, Google Maps and directories. That makes this an early window: clear, consistent brands gain visibility quickly.'], None),
   ('How AEO works: write the answer first', [
     'Answer engines quote short, direct answers. Put a 40 to 60 word answer right under each question heading, then explain. Use the exact questions people search for, such as "How much does a website cost in Kathmandu?", as your headings.',
     'Mark up questions and answers with FAQ schema, use lists and tables where they help, keep pages fast, and allow AI crawlers such as GPTBot, ClaudeBot and PerplexityBot in robots.txt.'], None),
   ('How GEO works: be cited, be consistent', [
     'Generative AI tools trust facts they can confirm in several places. Your name, what you do, your city, your website and your best work should read the same on your site, LinkedIn, GitHub, Google Business Profile and directories.',
     'On your site, structured data (Person or Organization, Service, FAQPage) tells machines exactly who you are. An llms.txt file gives AI tools a plain-text summary. A short description that sets you apart helps when other people share your name.'], None),
   ('Why E-E-A-T matters for AI answers', [
     'Google’s quality guidelines talk about Experience, Expertise, Authoritativeness and Trust (E-E-A-T). AI tools favour the same signals: a named author, real projects, first-hand examples, clear contact details and pages that are kept up to date. Generic content written for keywords gets cited less than content that shows real work.'], None),
   ('How to measure AEO and GEO', [
     'For AEO, watch Google Search Console for impressions on question searches and for featured snippets. For GEO, ask ChatGPT, Perplexity, Gemini and Copilot the questions your buyers ask each month, and note whether your brand is named or your pages are cited. Track the same questions over time.'], None),
   ('A checklist you can start today', [], None),
  ],
  checklist=['Verify your site in Google Search Console and Bing Webmaster Tools, and submit your sitemap.',
             'Add an answer-first FAQ to every service page, with FAQ schema.',
             'Allow AI crawlers in robots.txt and publish an llms.txt summary.',
             'Use one name, one description and one website link on every profile.',
             'Each month, ask the main AI tools your buyers’ questions and note who they cite.'],
  faq=[('Is AEO the same as SEO?', 'No. SEO is about ranking a page in search results. AEO is about having your answer quoted in featured snippets, voice answers and AI Overviews. They work best together.'),
       ('Where do AI answer engines get their information?', 'From web pages they crawl or search in real time, often pages that already rank in Google or Bing, plus trusted sources such as directories, news sites and profiles like LinkedIn.'),
       ('Do I need separate strategies for ChatGPT, Perplexity and Gemini?', 'Mostly no. The same foundations work across them: clear answers, structured data, consistent facts and being mentioned on trusted sites. Check each one, because they cite different sources.'),
       ('Can I block AI crawlers?', 'Yes, in robots.txt. But blocking them means AI tools cannot read or cite your pages, so most businesses that want to be found should allow them.'),
       ('How long do AEO and GEO take?', 'On-site changes take days. Being cited by AI tools usually takes one to three months, because the tools need to see consistent facts about you in several places.')],
  related=['aeo-geo-expert','seo-expert-nepal']),

 dict(slug='get-business-on-google-nepal',
  title='How to Get Your Business on Google & Google Maps in Nepal (Free Guide)',
  desc='Get your Nepali business on Google Search and Google Maps for free: Google Business Profile (Google My Business), Search Console, reviews and local SEO for Kathmandu.',
  h1='How to get your business on Google in Nepal',
  answer='Create and verify a free Google Business Profile so you appear on Google Maps, then verify your website in Google Search Console and submit your sitemap. Keep your name, address and phone number the same everywhere, ask customers for reviews, and import your site into Bing Webmaster Tools. All of this is free.',
  sections=[
   ('Step 1: Check whether Google already knows you', [
     'Search Google for your business name, and for site:yourdomain.com if you have a website. Also search Google Maps. If nothing appears, Google has not found you yet, and keyword work will not help until it does.'], None),
   ('Step 2: Create your Google Business Profile (Google My Business)', [
     'Google Business Profile, still often called Google My Business or GMB, is what puts you on Google Maps and in the local "3-pack" for searches like "property agent near me" or "web developer Kathmandu". Go to google.com/business, search for your business name, and claim it if it already exists or create it if not.',
     'Choose the most accurate primary category, then add secondary categories. Service businesses without a shop can set a service area such as the Kathmandu Valley instead of showing a street address.'], None),
   ('Step 3: Verify your profile', [
     'Google asks you to verify before the profile goes fully live. Depending on your business, it may offer a phone or text code, email, a short video of your premises, or a postcard. Use the options Google shows you; a video usually needs to show your signboard, your workspace and proof you manage the business.'], None),
   ('Step 4: Fill in everything and add photos', [
     'Add your hours, phone number (a mobile number you also use on WhatsApp works), website, services or products, and a description that says what you do and where. Upload real photos of your office, team and work. Complete profiles get more clicks and calls.'], None),
   ('Step 5: Get reviews and reply to them', [
     'Reviews are one of the strongest local ranking signals. Ask happy customers for a review with your short review link, and reply to every review, good or bad, politely. Recent reviews count more than old ones.'], None),
   ('Step 6: Keep your NAP consistent', [
     'NAP means name, address and phone number. Use exactly the same details on your website, Google Business Profile, Facebook page and Nepali directories. Mismatched details confuse Google and AI tools about who you are.'], None),
   ('Step 7: Verify your website in Search Console and Bing', [
     'In Google Search Console, add your site and verify it, for example by uploading the small HTML file Google gives you to your site’s root. Keep that file there permanently. Submit your sitemap.xml and request indexing for your most important pages.',
     'Then open Bing Webmaster Tools and choose Import from Google Search Console. Bing powers Microsoft Copilot and DuckDuckGo results and feeds ChatGPT search, so this matters for AI visibility too.'], None),
   ('Step 8: Fix what stops pages from ranking', [], None),
  ],
  checklist=['One clear H1 per page that uses the words people search for, including your city.',
             'A page title under about 60 characters, starting with the main keyword.',
             'A meta description that answers the search in one or two sentences.',
             'Fast loading on mobile data, with compressed images.',
             'Real text Google can read, not only images, and a page for each main service or area.'],
  faq=[('How long does it take to appear on Google in Nepal?', 'A verified Google Business Profile can appear on Maps within days. Website pages usually appear within a few days to two weeks after you submit a sitemap. Ranking well for competitive searches takes longer.'),
       ('Is Google My Business free in Nepal?', 'Yes. Google Business Profile (formerly Google My Business) is free. Google Ads are a separate, paid option.'),
       ('Can I use a WhatsApp number on Google Business Profile?', 'Yes. Use a phone number customers can call; a mobile number you also use for WhatsApp works, and you can link WhatsApp in your website and posts.'),
       ('Should I put keywords in my business name?', 'No. Use your real business name. Adding keywords that are not part of your real name breaks Google’s guidelines and can get the profile suspended.'),
       ('Does a .com.np domain rank in Nepal?', 'Yes. A .np domain is a clear local signal and still ranks for searches worldwide.')],
  related=['seo-expert-nepal','web-developer-kathmandu']),

 dict(slug='hire-ai-engineer-nepal',
  title='How to Hire an AI Engineer in Nepal: Checklist, Questions & Costs',
  desc='What an AI engineer does, what to put in your project brief, questions to ask and how pricing works when you hire an AI engineer in Nepal. From a Kathmandu AI engineer.',
  h1='How to hire an AI engineer in Nepal',
  answer='Hire an AI engineer in Nepal who can show live, working projects, not only demos. Write a short project brief, ask how they will connect AI to your own data, agree a small first project with a fixed quote, and make sure you own the code, prompts and data at the end.',
  sections=[
   ('What does an AI engineer do?', [
     'An AI engineer turns AI models into working software: choosing a model, writing and testing prompts, connecting the model to your documents or customer data through an API, building the screen people use, and keeping running costs and errors under control.',
     'Companies usually hire one for four things: building an MVP of a new AI product, adding AI features to an existing website or app, building AI into a mobile app, or automating repetitive work such as reports, emails and data entry.'], None),
   ('What to put in your project brief', [
     'A one-page brief gets you faster, more accurate quotes. Include the problem you want solved, who will use it, what data the AI should use, where it will live (your website, an app, WhatsApp or internal tools), your deadline, and how you will know it works.'], None),
   ('Questions to ask before you hire', [], None),
  ],
  checklist=['Can you show me a live project, not only a demo or a screenshot?',
             'How will you connect the AI to our data, and what data leaves our systems?',
             'What will it cost to run each month, not only to build?',
             'How will we test that the answers are correct and on-brand?',
             'Who owns the code, the prompts and the data when the project ends?',
             'Can you also build the website or app the feature lives in?'],
  extra=[
   ('What sets a strong AI engineer apart', [
     'Look for someone who ships complete products, not only models: a portfolio with live links, solid web or app development skills, care for security and user data, and plain explanations of trade-offs. An engineer who tells you when AI is the wrong tool is worth more than one who says yes to everything.'], None),
   ('How much does it cost to hire an AI engineer in Nepal?', [
     'It depends on scope, not on a fixed hourly rate. A focused first project, such as a support assistant trained on your own content, costs far less than a full AI product. Ask for a fixed quote per phase. Rates in Nepal are usually lower than in the US or Europe for the same quality of work.'], None),
   ('Freelancer, agency or hiring platform?', [
     'A freelance AI engineer is usually faster and cheaper for focused projects, and you speak directly to the person writing the code. An agency suits very large projects that need many people. Hiring platforms help you compare profiles but add fees; hiring directly avoids them.'], None),
   ('Start with a small first project', [
     'A good first AI project takes about two to six weeks and solves one clear problem. It proves the value before a larger budget is spent. Nepal’s time zone (UTC+5:45) overlaps with clients in Asia, the Middle East, Europe and Australia.'], None),
  ],
  faq=[('Do I need a data scientist or an AI engineer?', 'For most business projects, an AI engineer. Data scientists research and train models; AI engineers use existing models to build products, which is what most businesses need.'),
       ('What is the difference between hiring a freelance AI engineer and an agency in Nepal?', 'A freelancer is usually faster and cheaper, and you work directly with the developer. An agency adds project managers and more people, which suits large projects.'),
       ('Can an AI engineer work on my existing website or app?', 'Yes, if they are also a web or app developer. Ask which frameworks they have shipped, such as Laravel, Node.js, React or Next.js.'),
       ('How do I hire Prajwal Gautam?', 'Send a short brief by email to prajolgautam1234@gmail.com or on WhatsApp at +977 984-8137372. You get a reply within one working day and a fixed quote for the first phase.')],
  related=['ai-engineer-nepal','hire-ai-developer']),

 dict(slug='real-estate-marketing-nepal-guide',
  title=f'Real Estate Digital Marketing in Nepal: What Works Online ({YEAR})',
  desc='What sells property online in Nepal: property videos, listing websites, Facebook and Instagram ads, WhatsApp Business, local SEO and lead tracking. Lessons from Nepal Bhoomi.',
  h1='Real estate marketing in Nepal: what works online',
  answer='In Nepal, property sells online through short videos on Facebook, Instagram and TikTok, a fast listing website with clear price and location, Facebook and Instagram lead ads, quick replies on WhatsApp Business, and local SEO for areas such as Kathmandu, Lalitpur and Bhaktapur. Track every lead back to the ad that brought it.',
  sections=[
   ('Start with a professional property website', [
     'Social media brings attention; a website keeps it. Every listing needs its own fast page with price, area, road access, map location, photos, video and a one-tap WhatsApp button. Slow pages lose buyers on mobile data. A website also ranks on Google and builds trust when social reach drops.'], None),
   ('Video comes first on social media', [
     'Buyers scroll before they search. A 30 to 60 second property video with the price, location and three best features does more than a gallery of photos. Consistent branding, such as the same intro, captions and a short sound logo, makes a series recognisable.',
     'Building videos partly in code, as with Remotion, lets a small team publish often without starting from a blank timeline each time. That is how Nepal Bhoomi produces its property reels.'], None),
   ('Facebook, Instagram and Google ads', [
     'Facebook and Instagram lead ads work well for property because the form is pre-filled and quick, and you can target by location and interests. Google Ads catch people actively searching, such as "land for sale in Kathmandu". Start small, then move budget to the ads that bring real site visits, not just clicks.'], None),
   ('WhatsApp Business for real estate', [
     'Most property conversations in Nepal end up on WhatsApp. Use WhatsApp Business for a business profile, quick replies and labels for each lead. Broadcast lists and Status updates share new listings with interested buyers who have saved your number. Reply within minutes: slow replies lose leads.'], None),
   ('Local SEO for Kathmandu Valley areas', [
     'People search by place: "land for sale in Budhanilkantha", "house for rent in Lalitpur". Area pages, listing titles and video titles that use these place names, plus a Google Business Profile with reviews, catch these searches.'], None),
   ('Measure what brings sales', [], None),
   ('Trust and security', [
     'Buyers and sellers share phone numbers and documents. A property platform should protect them: secure sign-in, two-factor authentication for staff and an audit log of changes. The Nepal Bhoomi platform was built this way.'], None),
  ],
  checklist=['Leads per week, by channel (ads, website, WhatsApp, walk-ins).',
             'Cost per lead and cost per site visit for each ad.',
             'Reply time on WhatsApp and calls.',
             'Which areas, property types and videos bring the most enquiries.',
             'A one-page monthly report the owner can read in five minutes.'],
  faq=[('Which digital platform is most effective for real estate in Nepal?', 'Facebook and Instagram reach the most buyers, and WhatsApp is where deals are discussed. A listing website and Google searches bring serious buyers. The best results come from using them together.'),
       ('How can local SEO help Nepali real estate agents?', 'Local SEO puts your listings and Google Business Profile in front of people searching for property in a specific area, such as Lalitpur or Bhaktapur, at the moment they are looking.'),
       ('Do I need a website if I sell on Facebook?', 'Yes. A website with listings ranks on Google, builds trust and keeps your enquiries coming when social reach drops.'),
       ('Can you build a property listing website?', 'Yes. Prajwal Gautam co-built the Nepal Bhoomi real-estate platform and builds listing sites with admin panels and enquiry tracking.')],
  related=['real-estate-marketing-nepal','ai-video-production']),

 dict(slug='nextjs-vs-laravel-nepal',
  title=f'Next.js vs Laravel ({YEAR}): Which Is Better for Your Website or Web App?',
  desc='Next.js or Laravel? A plain comparison of SEO, performance, hosting, hiring, mobile apps and cost, from a developer in Nepal who has shipped production systems in both.',
  h1='Next.js vs Laravel: which should you choose?',
  thead=('', 'Next.js', 'Laravel'),
  answer='Choose Next.js for fast, SEO-friendly websites and interactive web apps, especially if a React Native mobile app may follow. Choose Laravel for back-end-heavy systems such as admin panels, forms, records and APIs, or when you need low-cost PHP hosting. You can also combine them: a Laravel API with a Next.js front end.',
  sections=[
   ('Next.js vs Laravel at a glance', [
     'They are not exact rivals. Next.js is a React framework that started on the front end and now handles servers and APIs too. Laravel is a full PHP back-end framework that can also render pages.'],
    [('Language', 'JavaScript or TypeScript (React)', 'PHP'),
     ('Strongest at', 'Front end, fast pages, interactive interfaces', 'Back end, business logic, admin panels, APIs'),
     ('SEO', 'Server-side rendering (SSR) and static generation (SSG)', 'Server-rendered pages; good for SEO'),
     ('Hosting', 'Vercel, serverless or a Node.js server', 'Low-cost shared PHP hosting or a VPS'),
     ('Mobile app later', 'Shares React skills with React Native', 'Works as the API for any mobile app')]),
   ('When Next.js is the better choice', [
     'Pick Next.js when SEO and speed are critical, such as marketing sites that must rank on Google, when the product has rich interactive screens, or when a React Native mobile app may share the same code skills later. The Nepal Bhoomi platform uses a Next.js API with PostgreSQL for these reasons.'], None),
   ('When Laravel is the better choice', [
     'Pick Laravel when the system is mainly records, forms, roles and reports, when you need to ship a solid back end fast, or when your hosting is a standard PHP plan. Laravel includes authentication, queues, email and database tools out of the box.',
     'I built a Laravel HR system and the Laravel payment and shipping features of the Sayapatri e-commerce platform; this kind of work is quick to build and easy to host in Laravel.'], None),
   ('Can you use Laravel and Next.js together?', [
     'Yes. A common setup keeps Laravel as the back-end API (data, users, payments) and builds the front end in Next.js for speed and SEO. It is also a good way to modernise an existing Laravel site step by step instead of rewriting it.'], None),
   ('Questions to ask before choosing', [], None),
  ],
  checklist=['Is SEO critical, or is this an internal tool?',
             'Who will maintain the code after launch, and what do they know?',
             'Where will it be hosted, and what will that cost each month as traffic grows?',
             'Will a mobile app share the same data later?',
             'How complex is the back-end logic?'],
  faq=[('Is Next.js better than Laravel?', 'Neither is better overall. Next.js is stronger for front-end speed and SEO; Laravel is stronger for back-end logic and quick admin-heavy systems.'),
       ('Is Laravel outdated?', 'No. Laravel is actively developed and widely used, especially for business systems and APIs.'),
       ('Is Next.js good for SEO?', 'Yes. It renders pages on the server or at build time, so search engines and AI crawlers see full content quickly.'),
       ('Can you move a Laravel site to Next.js later?', 'Yes, often step by step: keep Laravel as the back-end API and build a Next.js front end on top.')],
  related=['full-stack-developer-nepal','web-developer-kathmandu']),
]
