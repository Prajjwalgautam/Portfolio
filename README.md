# Prajwal Gautam · Portfolio

**Live site: [prajjwalgautam.com.np](https://prajjwalgautam.com.np)**

I'm Prajwal Gautam, an AI engineer, full-stack and app developer, and growth marketer based in Kathmandu, Nepal.
This repo holds my personal portfolio website.

## What the site does

- **A face made of 9,105 skill cards.** Each card carries one real skill. They follow your cursor, and as you scroll they
  reshape into a code symbol, a spinning galaxy of my six services, a career helix, the logos of my live projects and a wave.
- **A loader that "dispatches" my name.** The letters spin on a 3D ring, then fly into place as the page headline.
- **My work, sorted.** Websites, apps and video sit in one curved carousel you can drag, scroll or filter.
- **An "Ask me" button.** Clients write a message once and send it by email or WhatsApp.
- **14 service pages**, one for each thing people search for (AI engineer in Nepal, SEO expert, app developer,
  AI video, Google & Meta ads, AEO, real estate and jewellery marketing, SaaS motion design and more).

## Built with

- **Three.js (WebGL)** for the card animation, with custom shaders
- **Lenis** for smooth scrolling
- Plain **HTML, CSS and JavaScript**. There is no framework and no build step in the browser.
- **Python** to generate the pages from one template
- Fonts: Sofia Sans and Spline Sans Mono from Google Fonts

## Folder guide

```
index.html          Home page (generated: don't edit by hand)
services/           One folder per service page (generated)
guides/             Answer-first articles, e.g. "What are AEO and GEO?" (generated)
work/               Nepal Bhoomi case study (generated)
assets/             Photo, project logos and the social-share image
sitemap.xml         Page list for Google (generated)
robots.txt          Lets search engines and AI crawlers read the site (generated)
llms.txt            Plain-text summary for AI assistants like ChatGPT and Perplexity (generated)
CNAME               Points GitHub Pages at prajjwalgautam.com.np

source/             Everything used to build the site
  build_site.py     Run this to rebuild all pages
  service_pages.py  The words on the 14 service pages
  service_extra.py  Extra sections and FAQs for the service pages
  guides.py         The words in the guides
  templates/
    page.html       Home page layout, styles and interactions
    card-engine.html  The 3D card animation (WebGL)
  data/
    face-cards.b64  The face, stored as card positions and colours

docs/
  seo-keyword-research.md   Notes on the top 5 Google results for 10 keywords
```

## Making changes

1. Edit the text or layout:
   - Home page wording and data (services, experience, projects, FAQ) live at the top of `source/build_site.py`.
   - Service page wording lives in `source/service_pages.py`; guides live in `source/guides.py`.
   - Layout, colours and animations live in `source/templates/page.html`.
2. Rebuild the site:
   ```bash
   python3 source/build_site.py
   ```
3. Open `index.html` in a browser to check it, then commit and push. GitHub Pages publishes it automatically.

## Search and AI visibility

Every page has its own keyword-led title and description, structured data (Person, Service, FAQ, breadcrumbs),
social-share tags and a canonical link. `llms.txt` and `robots.txt` make the site easy for AI search tools to read and quote.

## Contact

- Email: [prajolgautam1234@gmail.com](mailto:prajolgautam1234@gmail.com)
- WhatsApp: [+977 984-8137372](https://wa.me/9779848137372)
- LinkedIn: [in/prajjwal-gautam](https://www.linkedin.com/in/prajjwal-gautam/)
