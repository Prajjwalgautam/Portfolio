# Prajwal Gautam · Portfolio

**Live site: [prajjwalgautam.com.np](https://prajjwalgautam.com.np)**

I'm Prajwal Gautam, an AI engineer and full-stack developer based in Kathmandu, Nepal.
This repo holds my personal portfolio website.

## What the site does

- **One clear role.** AI engineer and full-stack developer first. Video and marketing are add-ons, not extra job titles.
- **A face made of 9,105 skill cards.** Each card carries one real skill. They follow your cursor and, as you scroll,
  reshape into a code symbol, a spinning galaxy of skills, a career helix, the logos of my live projects and a wave.
- **One services section.** Three pillars (Build, Create, Grow) and a table showing what I deliver for each industry.
- **My work, sorted.** Websites, apps and video in one curved carousel you can drag sideways or filter.
- **A "Hire me" button** in the header that sends the client's message by WhatsApp or email.
- **14 service pages**, one for each thing people search for (AI engineer in Nepal, full-stack developer, app developer,
  SEO, AEO, AI video, SaaS motion design, real estate and jewellery marketing and more).

## Design system

- **Colours:** warm paper `#F3F2EF`, ink `#121316`, night `#0D0E11`, one brand red `#F2334B`.
  Three pillar colours are used only as small marks: Build `#7B8CFF`, Create `#F2334B`, Grow `#E8B04A`.
- **Type:** Instrument Sans for text and headings, Instrument Serif italic for the odd accent word,
  Spline Sans Mono for small labels.

## Built with

- **Three.js (WebGL)** for the card animation, with custom shaders
- **Lenis** for smooth scrolling
- Plain **HTML, CSS and JavaScript**. There is no framework and no build step in the browser.
- **Python** to generate the pages from one template
- Fonts: Instrument Sans, Instrument Serif and Spline Sans Mono from Google Fonts

## Folder guide

```
index.html          Home page (generated: don't edit by hand)
services/           One folder per service page (generated)
assets/             Photo, project logos and the social-share image
sitemap.xml         Page list for Google (generated)
robots.txt          Lets search engines and AI crawlers read the site (generated)
llms.txt            Plain-text summary for AI assistants like ChatGPT and Perplexity (generated)
CNAME               Points GitHub Pages at prajjwalgautam.com.np

source/             Everything used to build the site
  build_site.py     Run this to rebuild all pages
  service_pages.py  The words on the 14 service pages
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
   - Home page wording and data (services, industries, experience, projects, FAQ) live at the top of `source/build_site.py`.
   - Service page wording lives in `source/service_pages.py`.
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
- LinkedIn: [Prajwal Gautam](https://www.linkedin.com/in/prajjwal-gautam/)
