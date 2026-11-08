#!/usr/bin/env python3
"""Builds the portfolio in two flavours from src-v4.html:
   demo/prajwal-jar.html  -> self-contained artifact (data URIs)
   ./index.html + assets  -> deployable site for prajjwalgautam.com.np with full SEO
"""
import json, re, base64, html, io, os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)
SITE = "https://prajjwalgautam.com.np/"
E = html.escape

src = open(os.path.join(ROOT, 'src-v4.html')).read()
def R(a, b, cnt=1):
    global src
    assert src.count(a) == cnt, (src.count(a), a[:80])
    src = src.replace(a, b)

# ---------------------------------------------------------------- data
TITLE_LINE = "AI Engineer · Full-Stack &amp; App Developer · Growth Marketer"
ROLES = ["AI engineer", "full-stack developer", "app developer", "AI video producer", "SEO specialist",
         "ad campaign strategist", "growth marketer", "brand strategist", "marketing researcher"]
CATS = [
 dict(name='AI Engineering', word='AI', c='#ff9a3d', h='AI Engineering &amp; Automation',
      blurb='AI built into the product, not bolted on: language-model features, automations and AI-assisted research that save your team hours.',
      proof='AI-assisted research and content pipelines at Nepal Bhoomi and for freelance clients',
      skills=['LLM Integrations','Prompt Engineering','AI Automation','AI Research','AI Image Gen','AI Scriptwriting']),
 dict(name='Full-Stack', word='CODE', c='#3d6bff', h='Full-Stack Web Development',
      blurb='Fast, responsive websites and web platforms, from database to pixel, built to run a real business.',
      proof='HRMS, Fitfutures and First Math at Uno Technology',
      skills=['HTML & CSS','JavaScript','React','Node.js','PHP & Laravel','MySQL & MongoDB']),
 dict(name='Apps & APIs', word='APPS', c='#8b6bff', h='App Development &amp; Integrations',
      blurb='Mobile and web apps with payments, logins and live data wired in properly.',
      proof='Khalti payments and shipping APIs for Sayapatri at Ek Ra Sunya',
      skills=['Mobile Apps','Web Apps','REST APIs','Khalti Payments','Auth & Roles','Django']),
 dict(name='AI Video', word='VIDEO', c='#ff2e4d', h='AI Video Production',
      blurb='Scroll-stopping video made faster with AI: scripts, visuals, edits, grading and motion.',
      proof='3–4 property videos a day at Nepal Bhoomi, plus an AI-made YouTube channel',
      skills=['AI Video','Video Editing','Motion Graphics','Color Grading','Remotion','Thumbnails']),
 dict(name='SEO & Research', word='SEO', c='#22c3ee', h='SEO &amp; Marketing Research',
      blurb='Research what your customers search for, then rank for it, on Google and in AI answers.',
      proof='SEO captions, keyword research and audience analysis at Nepal Bhoomi',
      skills=['Technical SEO','Keyword Research','SEO Content','Market Research','Audience Analytics','YouTube SEO']),
 dict(name='Ads & Growth', word='GROWTH', c='#2ee6a6', h='Ad Campaigns, Growth &amp; Branding',
      blurb='Paid campaigns, brand and funnels that turn attention into customers, measured every month.',
      proof='Ad performance tracking and monthly growth reports at Nepal Bhoomi',
      skills=['Google Ads','Meta Ads','Growth Marketing','E-commerce Marketing','Branding','Performance Reports']),
]
assert sum(len(c['skills']) for c in CATS) == 36
JOBS = [
 dict(co='Nepal Bhoomi', logo='NB', c='#ff2e4d', where='Lazimpat, Kathmandu', title='Video Editor, Designer &amp; Growth Marketing', now=1,
      pts=['Produce <b>3–4 property videos a day</b>, from script to edit to publishing.','Run SEO captions, content calendars and audience research for buyers.','Track retention and ad performance; present <b>monthly growth reports</b>.']),
 dict(co='Freelance', ini='FL', c1='#ff2e4d', c2='#3a0812', c='#ff2e4d', where='Remote', title='AI Video Producer',
      pts=['Promotional and explainer videos for <b>schools and consultancies</b>.','IELTS, GRE, SAT and study-abroad topics made clear and watchable.','Podcasts cut into shorts, plus an <b>AI-made YouTube channel</b>.']),
 dict(co='Ek Ra Sunya Inc.', ini='ES', c1='#3d6bff', c2='#0a1440', c='#3d6bff', where='Balkumari, Lalitpur', title='Backend Developer',
      pts=['Backend for the <b>Sayapatri e-commerce platform</b>.','Integrated <b>Khalti payments</b> and MailQuote shipping costs.','Live exchange rates with USD to AUD conversion.']),
 dict(co='Uno Technology', ini='UT', c1='#3d6bff', c2='#0a1440', c='#3d6bff', where='Gyaneshwor, Kathmandu', title='Full-Stack Web Developer',
      pts=['A <b>Laravel HRMS</b> with payroll, leave, attendance and dashboards.','<b>Fitfutures</b>, an e-learning and school management system.','<b>First Math</b>, a three-level quiz game with live scoring.']),
]
WORK = [
 dict(k='web', name='Nepal Bhoomi', logo='NB', type='Real-estate company', desc='Live property platform for houses, land, apartments and commercial space across Kathmandu Valley, with a Nepali-language property journal. I run its video, design, SEO and social growth.', stack='Website · AI video · SEO · Ads', live='https://www.nepalbhoomi.com'),
 dict(k='web', name='Slugforge Studio', logo='SF', type='Creative studio', desc='Live website for a creative studio offering video editing, podcast repurposing, colour grading, AI video, motion graphics, branding, web development and digital marketing.', stack='Web design · 3D · Motion', live='https://slugforge.vercel.app'),
 dict(k='web', name='Sayapatri E-commerce', ini='SE', c1='#ff9a3d', c2='#4a1d05', type='Online store · Ek Ra Sunya', desc='E-commerce platform where I built Khalti payments, MailQuote shipping-cost calculation and live USD to AUD currency conversion.', stack='PHP · Laravel · REST APIs', st='Client project'),
 dict(k='web', name='Fitfutures', ini='FF', c1='#2ee6a6', c2='#063a2a', type='E-learning · Uno Technology', desc='E-learning and school management system with lessons, resources, progress tracking, admin dashboards and reporting.', stack='HTML · CSS · JavaScript · PHP', st='Client project'),
 dict(k='web', name='HRMS', ini='HR', c1='#3d6bff', c2='#0a1440', type='HR platform · Uno Technology', desc='Laravel human resource system: employee records, payroll, leave and attendance, with role-based dashboards for admins and staff.', stack='Laravel · PHP · MySQL', repo='https://github.com/Prajjwalgautam/HRM-system-checkin-checkout'),
 dict(k='web', name='Service Marketplace', ini='SM', c1='#8b6bff', c2='#1e1050', type='Freelance services', desc='Connects people with local professionals and freelance services.', stack='React · Node.js · MongoDB', repo='https://github.com/Prajjwalgautam/Ecommerce-Admin-User-management-system'),
 dict(k='web', name='Blood Bank System', ini='BB', c1='#ff2e4d', c2='#3a0812', type='Healthcare', desc='Blood donation and inventory app with donor registration, blood requests and real-time stock.', stack='Node.js · MySQL', st='Case study'),
 dict(k='web', name='Food Ordering', ini='FO', c1='#ff9a3d', c2='#4a1d05', type='Restaurant platform', desc='Menus, orders and deliveries with real-time tracking and payment integration.', stack='Node.js · MySQL', repo='https://github.com/Prajjwalgautam/Food-Delivery-system'),
 dict(k='web', name='Real-Estate Platform', ini='RE', c1='#ffd166', c2='#4a3400', type='Property marketplace', desc='Real-estate listing and search platform built with a collaborator.', stack='Full stack', repo='https://github.com/rookhit/Complete-realestate-project'),
 dict(k='web', name='DashboardUno', ini='DU', c1='#22c3ee', c2='#05303c', type='Admin dashboard', desc='Analytics dashboard UI with charts and reusable components.', stack='Frontend', repo='https://github.com/Prajjwalgautam/DashboardUno'),
 dict(k='app', name='Discipline Coach', ini='DC', c1='#ff2e4d', c2='#3a0812', type='Habit & focus app', desc='Mobile app that coaches daily discipline and habits. The repo hosts its published privacy policy.', stack='Mobile app', repo='https://github.com/Prajjwalgautam/discipline-coach-privacy'),
 dict(k='app', name='Activity Companion', ini='AC', c1='#ff9a3d', c2='#4a1d05', type='Social activity app', desc='Find people to join real-life activities such as hikes, games and events.', stack='Mobile app', st='In development'),
 dict(k='app', name='First Math', ini='FM', c1='#ffd166', c2='#4a3400', type='Quiz game · Uno Technology', desc='Maths and science quiz with Easy, Medium and Hard levels, points by difficulty and live scoring.', stack='HTML · CSS · JavaScript · PHP', repo='https://github.com/Prajjwalgautam/Project--First_Math'),
 dict(k='app', name='Expense Manager', ini='EM', c1='#2ee6a6', c2='#063a2a', type='Personal finance', desc='Tracks spending by category with real-time summaries.', stack='Python · Django · MySQL', repo='https://github.com/Prajjwalgautam/Expense-tracker'),
 dict(k='vid', name='Nepal Bhoomi Reels', logo='NB', type='Property video series', desc='Three to four property videos a day: scripted, edited, captioned for SEO and published across social, with monthly reporting.', stack='AI video · Editing · SEO captions', live='https://www.nepalbhoomi.com'),
 dict(k='vid', name='Slugforge Productions', logo='SF', type='Studio video services', desc='Editing, podcast repurposing, colour grading, AI-assisted video and motion graphics through Slugforge Studio.', stack='Editing · Grading · AI video', live='https://slugforge.vercel.app'),
 dict(k='vid', name='Educational YouTube', ini='YT', c1='#ff2e4d', c2='#3a0812', type='AI-made channel', desc='Educational videos made with AI-assisted scripts, images and visuals, edited with captions, transitions and music.', stack='AI scripting · AI visuals · Editing', st='Channel'),
 dict(k='vid', name='Study-Abroad Content', ini='SA', c1='#3d6bff', c2='#0a1440', type='Freelance · education', desc='Explainers on IELTS, GRE, SAT and study-abroad applications for schools and consultancies, plus podcasts cut into shorts.', stack='Short-form · Motion', st='Freelance'),
]
FAQ = [
 ("What does Prajwal Gautam do?", "Prajwal Gautam is an AI engineer, full-stack and app developer, AI video producer and growth marketer based in Kathmandu, Nepal. He builds AI-powered websites and apps, produces AI video, and runs SEO, ad campaigns and branding for businesses."),
 ("Can you build an AI-powered website or app for my business?", "Yes. I build websites, web platforms and mobile apps with Laravel, Node.js, React and Django, and add AI features such as language-model integrations, automations and AI-assisted content."),
 ("Do you handle SEO and ad campaigns as well as development?", "Yes. I do keyword and market research, technical SEO, SEO content, Google and Meta ad campaigns, and monthly performance reports, so one person covers building the product and growing it."),
 ("Do you produce AI video?", "Yes. I produce 3–4 property videos a day for Nepal Bhoomi, run an AI-made educational YouTube channel, and create promotional and explainer videos for schools and consultancies."),
 ("Do you work with clients outside Nepal?", "Yes. I work remotely with clients worldwide from Kathmandu (UTC+5:45), which overlaps with working hours in Asia, the Middle East, Europe and Australia."),
 ("How do I start a project with you?", "Email prajolgautam1234@gmail.com or call +977 984-8137372 with a short description of your goal. I reply within one working day, Nepal time."),
]

# ---------------------------------------------------------------- html helpers
def lg(o, cls='', LOGOS=None):
    if o.get('logo'):
        lc = 'light' if o['logo'] == 'NB' else 'dark'
        alt = 'Nepal Bhoomi logo' if o['logo'] == 'NB' else 'Slugforge Studio logo'
        return f'<div class="lg {lc} {cls}"><img src="__IMG_{o["logo"]}__" alt="{alt}" width="112" height="112" loading="lazy"></div>'
    return f'<div class="lg {cls}" style="--c1:{o.get("c1","#3d6bff")};--c2:{o.get("c2","#0b1024")}"><span>{o["ini"]}</span></div>'

cats_html = ''.join(f'''<section class="cat" data-state="w{i}" data-c="skills" style="--c:{c["c"]}" aria-labelledby="cat{i}"><div class="cat-card glass">
 <div class="cat-top"><span><b>{i+1:02d}</b> / 06 · Service</span><span>{len(c["skills"])} skills</span></div>
 <h2 class="cat-h" id="cat{i}">{c["h"]}</h2><p>{c["blurb"]}</p><div class="chips">{"".join(f"<span>{E(s)}</span>" for s in c["skills"])}</div>
 <p class="proof">Proof: <em>{c["proof"]}</em></p></div></section>''' for i, c in enumerate(CATS))

jobs_html = ''.join(f'''<article class="job glass" style="--c:{j["c"]}"><div class="job-top">{lg(j)}<div><h3>{E(j["co"])}{'<span class="now">NOW</span>' if j.get("now") else ''}</h3><div class="t">{j["title"]}</div><div class="w">{j["where"]}</div></div></div><ul>{"".join(f"<li>{p}</li>" for p in j["pts"])}</ul></article>''' for j in JOBS)

def items_html():
    out, n = [], {'web':0,'app':0,'vid':0}
    for i, w in enumerate(WORK):
        n[w['k']] += 1
        st = '<span class="st live">● Live</span>' if w.get('live') else f'<span class="st">{E(w.get("st","Code on GitHub"))}</span>'
        links = []
        if w.get('live'): links.append(f'<a class="btn light" href="{w["live"]}" target="_blank" rel="noopener">Open live project ↗</a>')
        if w.get('repo'): links.append(f'<a class="btn" href="{w["repo"]}" target="_blank" rel="noopener">View code on GitHub ↗</a>')
        if not links: links.append('<a class="btn" href="#contact">Ask for a walkthrough</a>')
        private = '' if (w.get('live') or w.get('repo')) else ' Built for a client, so the code is private.'
        short = w['desc'].split('. ')[0].rstrip('.') + '.'
        hid = '' if w['k'] == 'web' else ' hidden'
        out.append(f'''<div class="item" data-k="{w["k"]}" data-type="{E(w["type"])}" data-short="{E(short)}" open-state="0"{hid}><button type="button" aria-expanded="false" aria-controls="d{i}"><span class="n">{n[w["k"]]:02d}</span>{lg(w)}<span><h3>{E(w["name"])}</h3><span class="ty">{E(w["type"])}</span></span>{st}<span class="pl" aria-hidden="true">+</span></button>
<div class="detail" id="d{i}"><div><div class="in"><p>{E(w["desc"])}{private}</p><div class="meta"><span>Built with</span><div>{E(w["stack"])}</div><div class="btns" style="margin-top:8px">{"".join(links)}</div></div></div></div></div></div>''')
    return ''.join(out)

faq_html = ''.join(f'<details class="qa glass"><summary><h3>{E(q)}</h3><span aria-hidden="true">+</span></summary><p>{E(a)}</p></details>' for q, a in FAQ)
legend_html = ''.join(f'<span style="--c:{c["c"]}"><i></i>{E(c["name"])}</span>' for c in CATS)

# ---------------------------------------------------------------- CSS additions
R("@media (max-width:900px){", """
.h1sub{display:block;font-family:var(--mono);font-weight:500;font-size:clamp(12px,1.05vw,15px);letter-spacing:.14em;line-height:1.5;color:var(--snow);-webkit-text-stroke:0;margin-top:22px;text-transform:uppercase}
.tagline{font-family:var(--display);font-weight:900;font-size:clamp(22px,2.4vw,34px);line-height:1;letter-spacing:-.03em;text-transform:uppercase}
.tagline span:nth-child(1){color:var(--blue)} .tagline span:nth-child(2){color:var(--snow)} .tagline span:nth-child(3){color:var(--crimson)}
.cat-h{font-weight:900;font-size:clamp(28px,3.4vw,48px);line-height:.98;text-transform:uppercase}
.faq{padding-block:18vh 6vh;display:grid;gap:26px;max-width:980px}
.faq h2{font-weight:900;font-size:clamp(40px,6vw,96px);line-height:.88;text-transform:uppercase}
.qa{padding:0;overflow:hidden}
.qa summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;gap:16px;align-items:center;padding:22px 24px}
.qa summary::-webkit-details-marker{display:none}
.qa summary h3{font-family:var(--body);font-weight:600;font-size:clamp(16px,1.5vw,20px);letter-spacing:-.01em}
.qa summary span{font-size:22px;color:var(--mute);transition:transform .3s}
.qa[open] summary span{transform:rotate(45deg);color:var(--crimson)}
.qa p{padding:0 24px 22px;color:#cfd5ec;max-width:70ch}
.pulse{display:flex;align-items:center;gap:10px}
.pulse canvas{width:120px;height:28px;display:block}
.pulse b{color:var(--crimson)}
@media (max-width:900px){""")

# ---------------------------------------------------------------- hero
R("""      <div class="eyebrow"><b>●</b> Creative Technologist · Kathmandu, Nepal</div>
      <h1>Prajwal<br><span class="o">Gautam</span></h1>
      <div class="title"><span>I am a</span><span class="sw" id="sw">full-stack developer</span></div>
      <p class="lede">The face on the right is built from <b id="nCards">9,105</b> cards, and every card is a skill I use. Hover to read them. Click to send a shockwave. Then scroll, and watch them become my work.</p>""",
f"""      <div class="eyebrow"><b>●</b> Kathmandu, Nepal · Working worldwide</div>
      <h1>Prajwal<br><span class="o">Gautam</span><span class="h1sub">{TITLE_LINE}</span></h1>
      <div class="tagline" aria-label="Build it. Film it. Grow it."><span>Build it.</span> <span>Film it.</span> <span>Grow it.</span></div>
      <div class="title"><span>I’m your</span><span class="sw" id="sw">{ROLES[0]}</span></div>
      <p class="lede">I engineer AI-powered websites and apps, produce AI video, and run the SEO, ads and branding that bring customers in. The face on the right is <b id="nCards">9,105</b> cards, each one a skill. Hover to read them, click for a shockwave, then scroll.</p>""")

# ---------------------------------------------------------------- galaxy / cats / jobs / work / faq
R("""<p>Every arm is one discipline, coloured to match. Keep scrolling and each arm steps forward and spells its own name.</p>
      <div class="legend" id="legend"></div>""", f"""<p>Six services, one arm each, coloured to match. Keep scrolling and each arm steps forward and spells its name.</p>
      <div class="legend">{legend_html}</div>""")
R("""<div id="cats"></div>""", f"""<div id="cats">{cats_html}</div>""")
R("""<div class="jobs" id="jobs"></div>""", f"""<div class="jobs" id="jobs">{jobs_html}</div>""")
cnt = {k: sum(1 for w in WORK if w['k'] == k) for k in ('web','app','vid')}
R("""data-kind="web">Websites <small></small>""", f"""data-kind="web">Websites <small>{cnt['web']}</small>""")
R("""data-kind="app">Apps <small></small>""", f"""data-kind="app">Apps <small>{cnt['app']}</small>""")
R("""data-kind="vid">Video &amp; Content <small></small>""", f"""data-kind="vid">Video &amp; Content <small>{cnt['vid']}</small>""")
R("""<div class="index" id="index" role="tabpanel" aria-labelledby="tab-web"></div>""", f"""<div class="index" id="index" role="tabpanel" aria-labelledby="tab-web">{items_html()}</div>""")
R("""<div class="row"><div class="lg light" id="nbLogo"></div>""", """<div class="row"><div class="lg light" id="nbLogo"><img src="__IMG_NB__" alt="Nepal Bhoomi logo" width="112" height="112"></div>""")
R("""<div class="row"><div class="lg dark" id="sfLogo"></div>""", """<div class="row"><div class="lg dark" id="sfLogo"><img src="__IMG_SF__" alt="Slugforge Studio logo" width="112" height="112"></div>""")
R("""<img id="portrait" alt="Prajwal Gautam in a black blazer and turtleneck">""", """<img id="portrait" src="__IMG_PHOTO__" width="620" height="823" loading="lazy" alt="Prajwal Gautam, AI engineer and growth marketer, in a black blazer in Kathmandu">""")
R("""<p class="big">I studied Computer Science, shipped Laravel and Node systems for two software companies, then moved into video and marketing for a real-estate brand. Now I do both: I can <em>build your product</em>, <em>film it</em> and <em>grow it</em>, with no hand-offs between agencies.</p>""",
  """<p class="big">I studied Computer Science, shipped Laravel and Node systems for two software companies, then took over video, SEO and growth for a real-estate brand. Today I combine AI engineering, full-stack and app development with AI video, research, ads and branding. I can <em>build your product</em>, <em>film it</em> and <em>grow it</em>, with no hand-offs between agencies.</p>""")
R("""  <section class="contact" id="contact" data-state="face2" data-c="contact">""", f"""  <section class="faq" id="faq" data-state="wave" data-c="about" aria-labelledby="faqh">
    <div class="eyebrow"><b>05</b> Questions</div>
    <h2 id="faqh">FAQ</h2>
    {faq_html}
  </section>

  <section class="contact" id="contact" data-state="face2" data-c="contact">""")
R("""<div class="eyebrow"><b>05</b> Contact</div>""", """<div class="eyebrow"><b>06</b> Contact</div>""")
R("""<p style="color:var(--mute)">Websites, web apps, video and content marketing for businesses in Nepal and abroad. I reply within one working day, Nepal time (UTC+5:45).</p>""",
  """<p style="color:var(--mute)">AI-powered websites and apps, AI video, SEO, ad campaigns and branding for businesses in Nepal and worldwide. I reply within one working day, Nepal time (UTC+5:45).</p>""")
R("""<footer><span>© 2026 Prajwal Gautam · prajjwalgautam.com.np</span><span>9,105 cards · Three.js · Kathmandu</span></footer>""",
  """<footer><span>© 2026 Prajwal Gautam · AI Engineer, Full-Stack &amp; App Developer, Growth Marketer · Kathmandu, Nepal</span><span>prajjwalgautam.com.np</span></footer>""")
R("""<div class="boot" aria-hidden="true"><span id="bootTxt">Assembling</span><b id="bootN">0</b><span>cards</span></div>""",
  """<div class="boot" aria-hidden="true"><span id="bootTxt">Assembling</span><b id="bootN">0</b><span>cards</span><span class="pulse"><canvas id="ecg" width="240" height="56"></canvas><b id="bpm">72</b>bpm</span></div>""")
R("""  <li><a href="#about" data-c="about"><span>About</span></a></li>""", """  <li><a href="#about" data-c="about"><span>About &amp; FAQ</span></a></li>""")

# ---------------------------------------------------------------- JS: replace content/HTML-build block
a = src.index("/* ================= content ================= */"); b = src.index("/* role swapper with scramble */")
cats_js = json.dumps([dict(name=c['name'], word=c['word'], c=c['c'], skills=c['skills']) for c in CATS])
src = src[:a] + """/* ================= content (HTML is static for SEO) ================= */
const CATS=""" + cats_js + """;
const SKILLS=[]; CATS.forEach((c,ci)=>c.skills.forEach(s=>SKILLS.push({s,ci})));
const ROLES=""" + json.dumps(ROLES) + """;
const LOGO_NB="__IMG_NB__", LOGO_SF="__IMG_SF__";
const idx=$('index'), peek=$('peek'); const items=[...idx.querySelectorAll('.item')];
items.forEach(it=>{ const b=it.querySelector('button');
  b.addEventListener('click',()=>{ const op=it.getAttribute('open-state')==='1'; items.forEach(x=>{x.setAttribute('open-state','0');x.querySelector('button').setAttribute('aria-expanded','false')});
    if(!op){ it.setAttribute('open-state','1'); b.setAttribute('aria-expanded','true'); } });
  b.addEventListener('pointerenter',()=>{ peek.innerHTML=it.querySelector('.lg').outerHTML+`<span class="k">${it.dataset.type}</span><p>${it.dataset.short}</p>`; peek.classList.add('on'); });
  b.addEventListener('pointerleave',()=>peek.classList.remove('on')); });
const tabs=[...document.querySelectorAll('[role=tab]')];
tabs.forEach(t=>t.addEventListener('click',()=>{ tabs.forEach(x=>x.setAttribute('aria-selected',String(x===t))); idx.setAttribute('aria-labelledby',t.id);
  items.forEach(it=>{ it.hidden=it.dataset.k!==t.dataset.kind; it.setAttribute('open-state','0'); }); try{ computeAnchors(); }catch(e){} }));
document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',async()=>{
  const v=$(b.dataset.copy).textContent; try{ await navigator.clipboard.writeText(v); b.textContent='Copied'; }
  catch(e){ const r=document.createRange(); r.selectNodeContents($(b.dataset.copy)); getSelection().removeAllRanges(); getSelection().addRange(r); b.textContent='Ctrl+C'; }
  setTimeout(()=>b.textContent='Copy',1600);
}));
document.querySelectorAll('.qa').forEach(d=>d.addEventListener('toggle',()=>{ try{ computeAnchors(); }catch(e){} }));

""" + src[b:]
R("""const FACE_B64="__FACE__", FACE_COLS=84, FACE_ROWS=180;
const LOGO_NB="__LOGO_NB__", LOGO_SF="__LOGO_SF__";""", """const FACE_B64="__FACE__", FACE_COLS=84, FACE_ROWS=180;""")

# ---------------------------------------------------------------- heartbeat
R("uniform float uT,uTime,uIntro,uScA,uScB,uKindA,uKindB,uSizeA,uSizeB,uFaceA,uFaceB,uLens;",
  "uniform float uT,uTime,uIntro,uScA,uScB,uKindA,uKindB,uSizeA,uSizeB,uFaceA,uFaceB,uLens,uBeat;")
R("""  float s=mix(uSizeA,uSizeB,e)*(1.+infl*3.2)*(1.+ring*.8)*mix(.2,1.,it);""",
  """  float s=mix(uSizeA,uSizeB,e)*(1.+infl*3.2)*(1.+ring*.8)*mix(.2,1.,it)*(1.+uBeat*.09);""")
R("""  col+=vec3(1.,.35,.45)*ring*.8 + vec3(.12)*infl;""", """  col+=vec3(1.,.35,.45)*ring*.8 + vec3(.12)*infl + vec3(1.,.18,.3)*uBeat*.07;""")
R("""uMouse:{value:new THREE.Vector2()}, uLens:{value:0},""", """uMouse:{value:new THREE.Vector2()}, uLens:{value:0}, uBeat:{value:0},""")
R("""  $('bar').style.width=(100*y/Math.max(1,document.documentElement.scrollHeight-innerHeight))+'%';""",
  """  progress=y/Math.max(1,document.documentElement.scrollHeight-innerHeight); $('bar').style.width=(100*progress)+'%';""")
R("""let sTarget=0, sSmooth=0;""", """let sTarget=0, sSmooth=0, progress=0, beatPh=0, bpm=72;
const ecg=$('ecg'), eg=ecg.getContext('2d'); let ecgX=0;
function heartbeat(dt){
  bpm+=((72+66*progress)-bpm)*Math.min(1,dt*2); beatPh+=dt*bpm/60; const f=beatPh%1;
  const bt=Math.exp(-Math.pow((f-.06)/.028,2))+.55*Math.exp(-Math.pow((f-.24)/.035,2));
  U.uBeat.value=reduce?0:bt; $('bpm').textContent=Math.round(bpm);
  const W=ecg.width,H=ecg.height; eg.drawImage(ecg,-3,0); eg.clearRect(W-3,0,3,H);
  const y=H*.62 - (Math.exp(-Math.pow((f-.06)/.012,2))*H*.5) + (Math.exp(-Math.pow((f-.09)/.012,2))*H*.22) - Math.exp(-Math.pow((f-.24)/.04,2))*H*.12;
  eg.strokeStyle='#ff2e4d'; eg.lineWidth=2.5; eg.beginPath(); eg.moveTo(W-4,ecgX||y); eg.lineTo(W-1,y); eg.stroke(); ecgX=y;
}""")
R("""  shockT+=dt; U.uShock.value.z=shockT;""", """  shockT+=dt; U.uShock.value.z=shockT; heartbeat(dt);""")

open(os.path.join(ROOT, 'src-v5.html'), 'w').write(src)

# ---------------------------------------------------------------- assets
face = open('/tmp/claude-0/face2.b64').read()
nb = open(os.path.join(ROOT, 'logo-nb.txt')).read().strip()
sf = open(os.path.join(ROOT, 'logo-sf.txt')).read().strip()
photo = open(os.path.join(ROOT, 'photo.txt')).read().strip()

# artifact (self-contained)
art = src.replace('__FACE__', face).replace('__IMG_NB__', nb).replace('__IMG_SF__', sf).replace('__IMG_PHOTO__', photo)
open(os.path.join(ROOT, 'prajwal-jar.html'), 'w').write(art)

# deployable site
os.makedirs(os.path.join(REPO, 'assets'), exist_ok=True)
def save_datauri(uri, path):
    open(path, 'wb').write(base64.b64decode(uri.split(',', 1)[1]))
save_datauri(nb, os.path.join(REPO, 'assets/nepal-bhoomi-logo.webp'))
save_datauri(sf, os.path.join(REPO, 'assets/slugforge-logo.webp'))
save_datauri(photo, os.path.join(REPO, 'assets/prajwal-gautam.webp'))

# OG image 1200x630
og = Image.new('RGB', (1200, 630), (4, 6, 15)); d = ImageDraw.Draw(og)
cut = Image.open('/tmp/claude-0/cut.png').convert('RGBA').crop((150, 360, 640, 1100)); cut.thumbnail((520, 700))
og.paste(cut, (1200 - cut.width - 40, 630 - cut.height), cut)
def font(sz, bold=True):
    for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
        if os.path.exists(p): return ImageFont.truetype(p, sz)
    return ImageFont.load_default()
d.text((64, 150), 'PRAJWAL', font=font(92), fill=(238, 242, 255))
d.text((64, 250), 'GAUTAM', font=font(92), fill=(255, 46, 77))
d.text((66, 370), 'AI Engineer · Full-Stack & App Developer', font=font(30, False), fill=(238, 242, 255))
d.text((66, 412), 'AI Video · SEO · Ads · Growth Marketing', font=font(30, False), fill=(141, 149, 179))
d.text((66, 500), 'prajjwalgautam.com.np · Kathmandu, Nepal', font=font(24, False), fill=(61, 107, 255))
og.save(os.path.join(REPO, 'assets/og-image.jpg'), quality=88)

desc = "Prajwal Gautam is an AI engineer, full-stack and app developer, AI video producer and SEO & growth marketer in Kathmandu, Nepal, building AI-powered websites and apps, ad campaigns and brands for clients worldwide."
knows = ["Artificial intelligence engineering","LLM integration","AI automation","Prompt engineering","Full-stack web development","Laravel","PHP","Node.js","React","Django","MySQL","MongoDB","Mobile app development","REST APIs","Payment gateway integration","Khalti","AI video production","Video editing","Motion graphics","Color grading","Search engine optimization","Technical SEO","Keyword research","Marketing research","Google Ads","Meta Ads","Growth marketing","E-commerce marketing","Branding","Social media marketing","Content strategy"]
person = {"@type":"Person","@id":SITE+"#person","name":"Prajwal Gautam","alternateName":["Prajjwal Gautam","Prajwal Gautam Nepal"],
  "url":SITE,"image":SITE+"assets/prajwal-gautam.webp","jobTitle":"AI Engineer, Full-Stack & App Developer, Growth Marketer","description":desc,
  "email":"mailto:prajolgautam1234@gmail.com","telephone":"+977-9848137372",
  "address":{"@type":"PostalAddress","addressLocality":"Kathmandu","addressRegion":"Bagmati","addressCountry":"NP"},
  "alumniOf":[{"@type":"CollegeOrUniversity","name":"New Summit College, Tribhuvan University"},{"@type":"EducationalOrganization","name":"Kathmandu Model College"}],
  "worksFor":{"@type":"Organization","name":"Nepal Bhoomi","url":"https://www.nepalbhoomi.com"},
  "knowsAbout":knows,"knowsLanguage":["English","Nepali","Hindi"],
  "sameAs":["https://www.linkedin.com/in/prajjwal-gautam/","https://github.com/Prajjwalgautam"]}
service = {"@type":"ProfessionalService","@id":SITE+"#service","name":"Prajwal Gautam — AI, Development & Growth Services","url":SITE,"image":SITE+"assets/og-image.jpg",
  "description":desc,"founder":{"@id":SITE+"#person"},"telephone":"+977-9848137372","email":"prajolgautam1234@gmail.com",
  "address":{"@type":"PostalAddress","addressLocality":"Kathmandu","addressCountry":"NP"},"areaServed":["Nepal","Worldwide"],
  "hasOfferCatalog":{"@type":"OfferCatalog","name":"Services","itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":html.unescape(c["h"]),"description":c["blurb"]}} for c in CATS]}}
website = {"@type":"WebSite","@id":SITE+"#website","url":SITE,"name":"Prajwal Gautam","inLanguage":"en","publisher":{"@id":SITE+"#person"}}
faqld = {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in FAQ]}
projects = {"@type":"ItemList","name":"Projects by Prajwal Gautam","itemListElement":[{"@type":"ListItem","position":i+1,"item":{"@type":"CreativeWork","name":w["name"],"description":w["desc"],"creator":{"@id":SITE+"#person"},**({"url":w["live"]} if w.get("live") else ({"url":w["repo"]} if w.get("repo") else {}))}} for i, w in enumerate(WORK)]}
ld = json.dumps({"@context":"https://schema.org","@graph":[person,service,website,faqld,projects]}, ensure_ascii=False)

title = "Prajwal Gautam | AI Engineer, Full-Stack & App Developer, Growth Marketer in Nepal"
head = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="author" content="Prajwal Gautam">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{SITE}">
<meta name="theme-color" content="#04060f">
<meta property="og:type" content="profile">
<meta property="og:site_name" content="Prajwal Gautam">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{SITE}">
<meta property="og:image" content="{SITE}assets/og-image.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta property="profile:first_name" content="Prajwal"><meta property="profile:last_name" content="Gautam">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{SITE}assets/og-image.jpg">
<meta name="geo.region" content="NP-BA"><meta name="geo.placename" content="Kathmandu">
<link rel="icon" href="assets/slugforge-logo.webp" type="image/webp">
<link rel="preload" as="image" href="assets/prajwal-gautam.webp">
<script type="application/ld+json">{ld}</script>
"""
body_start = src.index('<link rel="preconnect"')
site_src = src[body_start:]
style_end = site_src.index('</style>') + len('</style>')
site = head + site_src[:style_end] + "\n</head>\n<body>\n" + site_src[style_end:] + "\n</body>\n</html>\n"
site = (site.replace('__FACE__', face).replace('__IMG_NB__', 'assets/nepal-bhoomi-logo.webp')
            .replace('__IMG_SF__', 'assets/slugforge-logo.webp').replace('__IMG_PHOTO__', 'assets/prajwal-gautam.webp'))
open(os.path.join(REPO, 'index.html'), 'w').write(site)

open(os.path.join(REPO, 'robots.txt'), 'w').write(f"""User-agent: *
Allow: /

# AI search and answer engines are welcome
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: {SITE}sitemap.xml
""")
open(os.path.join(REPO, 'sitemap.xml'), 'w').write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url>
    <loc>{SITE}</loc>
    <lastmod>2026-11-08</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
    <image:image><image:loc>{SITE}assets/prajwal-gautam.webp</image:loc></image:image>
  </url>
</urlset>
""")
llms = ["# Prajwal Gautam", "", f"> {desc}", "",
        "## Roles", "- AI Engineer", "- Full-Stack Web Developer", "- App Developer", "- AI Video Producer",
        "- SEO Specialist and Marketing Researcher", "- Ad Campaign Strategist (Google Ads, Meta Ads)", "- Growth, E-commerce and Brand Marketer", "",
        "## Services"] + [f"- **{html.unescape(c['h'])}**: {c['blurb']} Skills: {', '.join(c['skills'])}. Proof: {c['proof']}." for c in CATS] + ["",
        "## Experience"] + [f"- **{j['co']}** ({j['where']}): {html.unescape(j['title'])}. " + ' '.join(re.sub('<[^>]+>','',p) for p in j['pts']) for j in JOBS] + ["",
        "## Live projects", "- [Nepal Bhoomi](https://www.nepalbhoomi.com): real-estate platform; video, SEO and growth.", "- [Slugforge Studio](https://slugforge.vercel.app): creative studio website and video services.", "",
        "## Other projects"] + [f"- {w['name']} ({w['type']}): {w['desc']}" for w in WORK[2:]] + ["",
        "## Education", "- BSc CSIT, New Summit College, Tribhuvan University", "- +2 Science, Kathmandu Model College", "",
        "## Contact", "- Email: prajolgautam1234@gmail.com", "- Phone: +977 984-8137372", "- LinkedIn: https://www.linkedin.com/in/prajjwal-gautam/", "- GitHub: https://github.com/Prajjwalgautam",
        "- Location: Kathmandu, Nepal (UTC+5:45); works with clients worldwide", ""]
open(os.path.join(REPO, 'llms.txt'), 'w').write('\n'.join(llms))
print('built', len(art), len(site))
