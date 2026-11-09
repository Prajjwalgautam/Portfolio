#!/usr/bin/env python3
"""
Builds the whole website from the template and the content files.

Run it from anywhere:
    python3 source/build_site.py

What it writes into the repo root:
    index.html                         the home page
    services/<name>/index.html         one page per service (14 pages)
    sitemap.xml, robots.txt, llms.txt  for Google and AI search engines

It also writes a preview copy into source/preview/ (ignored by git).
"""
import json, html, os, re, shutil
from service_pages import SERVICES, BY_SLUG, PROCESS

ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(ROOT)
SITE = "https://prajjwalgautam.com.np/"
E = html.escape
TODAY = "2026-11-09"

CATS = [
 dict(name='AI Engineering', word='AI', c='#FF8A3D', slug='ai-engineer-nepal', h='AI Engineering &amp; Automation',
      blurb='AI built into the product: language-model features, assistants, automations and AI-powered content pipelines that save your team hours.',
      proof='A Remotion + Python AI video pipeline (Whisper captions, upscaling, background removal, tracking) at Nepal Bhoomi',
      skills=['LLM Integrations','Prompt Engineering','AI Automation','AI Research','AI Image Gen','AI Scriptwriting']),
 dict(name='Full-Stack', word='CODE', c='#4D7BFF', slug='full-stack-developer-nepal', h='Full-Stack Web Development',
      blurb='Secure, fast web platforms from database to pixel: auth, admin panels, payments and dashboards.',
      proof='Nepal Bhoomi platform (Next.js, PostgreSQL, 2FA), Zylux admin (Next.js 15), Laravel HRMS',
      skills=['TypeScript','Next.js & React','Node.js','PHP & Laravel','PostgreSQL & MySQL','Tailwind CSS']),
 dict(name='Apps & APIs', word='APPS', c='#9B7BFF', slug='app-developer-nepal', h='App Development &amp; Integrations',
      blurb='Mobile and web apps with sign-in, payments and live data wired in properly, built privacy-first.',
      proof='AI Discipline Coach (Android), Khalti and shipping APIs for Sayapatri at Ek Ra Sunya',
      skills=['Android Apps','Web Apps','REST APIs','Khalti Payments','Auth, 2FA & OAuth','Prisma & Drizzle']),
 dict(name='AI Video & Motion', word='VIDEO', c='#F2334B', slug='ai-video-production', h='AI Video &amp; Motion Design',
      blurb='Scroll-stopping video and SaaS-style motion, made faster with AI and code: scripts, 3D, edits, grading and sound.',
      proof='Nepal Bhoomi property films, The 195 Project with Blender 3D, a brand sonic logo',
      skills=['AI Video','Motion Graphics','SaaS Animation','Blender 3D','Color Grading','Remotion']),
 dict(name='SEO & AEO', word='SEO', c='#2BC6E8', slug='aeo-geo-expert', h='SEO, AEO &amp; Marketing Research',
      blurb='Rank on Google and become the answer in ChatGPT, Perplexity and Google AI Overviews.',
      proof='SEO and keyword research at Nepal Bhoomi; this site’s schema, llms.txt and 14 keyword pages',
      skills=['Technical SEO','AEO & GEO','Keyword Research','SEO Content','Market Research','Audience Analytics']),
 dict(name='Ads, Growth & Brand', word='GROWTH', c='#2EE6A6', slug='google-meta-ads-expert-nepal', h='Ad Campaigns, Growth &amp; Branding',
      blurb='Paid campaigns, brand systems and graphics that turn attention into customers, measured every month.',
      proof='Ad tracking and monthly growth reports at Nepal Bhoomi; Nepal Bhoomi sonic branding',
      skills=['Google Ads','Meta Ads','Growth Marketing','E-commerce Marketing','Branding','Graphic Design']),
]
ROLES = ["AI engineer","full-stack developer","app developer","AI video producer","motion designer","SEO & AEO specialist","ad campaign strategist","growth marketer","brand strategist","marketing researcher"]
JOBS = [
 dict(co='Nepal Bhoomi', logo='NB', c='#F2334B', where='Lazimpat, Kathmandu', title='Video, Design, Growth &amp; Platform', now=1,
      pts=['Built a <b>code-driven video pipeline</b> (Remotion + Python AI: Whisper captions, upscaling, background removal, tracking) for branded <b>property reels</b>.',
           'Co-built the <b>Nepal Bhoomi platform</b>: Next.js API, PostgreSQL, React admin, 2FA, Google sign-in and audit logging.',
           'Own SEO captions, audience research, ad tracking and <b>monthly growth reports</b>; designed the brand’s <b>sonic logo</b>.']),
 dict(co='Freelance', ini='FL', c1='#F2334B', c2='#3a0812', c='#F2334B', where='Remote · worldwide', title='AI Video Producer &amp; Motion Designer',
      pts=['Promotional and explainer videos for <b>schools and study-abroad consultancies</b> on IELTS, GRE, SAT and applications.',
           'Long podcasts and interviews cut into <b>captioned short-form clips</b>.',
           '<b>The 195 Project</b> documentary episodes with Blender 3D scenes, plus an <b>AI-made educational YouTube channel</b>.']),
 dict(co='Ek Ra Sunya Inc.', ini='ES', c1='#4D7BFF', c2='#0a1440', c='#4D7BFF', where='Balkumari, Lalitpur', title='Backend Developer',
      pts=['Shipped payments, shipping and currency features on the live <b>Sayapatri e-commerce platform</b>.',
           'Integrated <b>Khalti checkout</b> and <b>MailQuote</b> real-time shipping rates.',
           'Added <b>live exchange rates</b> with USD to AUD base-currency pricing.']),
 dict(co='Uno Technology', ini='UT', c1='#4D7BFF', c2='#0a1440', c='#4D7BFF', where='Gyaneshwor, Kathmandu', title='Full-Stack Web Developer',
      pts=['Built a <b>Laravel HRMS</b>: JWT auth, OTP password reset by email, attendance check-in/out, tasks, admin and employee roles.',
           'Built <b>Fitfutures</b>, an e-learning and school management platform with progress tracking and reports.',
           'Built <b>First Math</b>, a maths and science game with three levels per subject and live scoring.']),
]
WORK = [
 dict(k='web', name='Nepal Bhoomi', logo='NB', c1='#8a1f4a', type='Real-estate company · live', desc='Live property platform for houses, land, apartments and commercial space across Kathmandu Valley. I run its video, design, SEO and growth.', stack='Website · AI video · SEO · Ads', live='https://www.nepalbhoomi.com'),
 dict(k='web', name='Nepal Bhoomi Platform', ini='NB', c1='#b8892d', c2='#3a1424', type='Full-stack · co-built', desc='Next.js API with Prisma and PostgreSQL (Supabase), React + Tailwind site and admin. 2FA, Google sign-in, email verification, refresh-token theft detection, rate limiting, audit logs and row-level security across 20+ data models.', stack='Next.js · Prisma · PostgreSQL · React', repo='https://github.com/rookhit/Complete-realestate-project'),
 dict(k='web', name='Slugforge Studio', logo='SF', c1='#6b4cff', type='Creative studio · live', desc='Live website for a creative studio offering editing, AI video, motion graphics, branding, web development and digital marketing.', stack='Web design · 3D · Motion', live='https://slugforge.vercel.app'),
 dict(k='web', name='Zylux Commerce Admin', ini='ZX', c1='#2BC6E8', c2='#05303c', type='Next.js 15 dashboard', desc='Commerce admin with Clerk sign-in, products, categories, orders and users, TanStack data tables and Recharts sales overview, on Drizzle ORM and Neon Postgres.', stack='Next.js 15 · React 19 · TypeScript', repo='https://github.com/Prajjwalgautam/Zylux-Task'),
 dict(k='web', name='Sayapatri E-commerce', ini='SE', c1='#FF8A3D', c2='#4a1d05', type='Online store · Ek Ra Sunya', desc='E-commerce backend features: Khalti checkout, MailQuote shipping rates and live USD to AUD base-currency pricing.', stack='PHP · Laravel · REST APIs', st='Client project'),
 dict(k='web', name='Laravel HRMS', ini='HR', c1='#4D7BFF', c2='#0a1440', type='HR platform · Uno Technology', desc='JWT auth, OTP password reset by email, employee records, attendance check-in and check-out, tasks and role-based dashboards.', stack='Laravel · JWT · MySQL', repo='https://github.com/Prajjwalgautam/HRM-system-checkin-checkout'),
 dict(k='web', name='Fitfutures', ini='FF', c1='#2EE6A6', c2='#063a2a', type='E-learning · Uno Technology', desc='E-learning and school management platform with lessons, resources, progress tracking, admin dashboards and reports.', stack='HTML · CSS · JS · PHP', st='Client project'),
 dict(k='web', name='Role-Based Commerce Admin', ini='RC', c1='#9B7BFF', c2='#1e1050', type='Admin & user system', desc='Admin and user dashboards with JWT authentication, OTP email password reset, profile management and catalogue CRUD.', stack='PHP · JWT · Bootstrap', repo='https://github.com/Prajjwalgautam/Ecommerce-Admin-User-management-system'),
 dict(k='web', name='EBhojanalaya', ini='EB', c1='#F2334B', c2='#3a0812', type='Food ordering app', desc='Online food ordering: menus, cart and orders with a React front end and a Node.js server.', stack='React · Node.js', repo='https://github.com/Prajjwalgautam/Food-Delivery-system'),
 dict(k='web', name='This Portfolio', ini='PG', c1='#F2334B', c2='#0c0c0e', type='WebGL · SEO · AEO', desc='9,105 instanced WebGL skill cards that morph through ten states on scroll, a 3D text loader, a curved carousel and 14 SEO and AEO service pages.', stack='Three.js · GLSL · Python build', repo='https://github.com/Prajjwalgautam/Portfolio'),
 dict(k='app', name='AI Discipline Coach', ini='DC', c1='#F2334B', c2='#3a0812', type='Android app', desc='Habit and discipline coach for Android, built privacy-first: no internet permission and no data collected. Privacy policy published for Google Play.', stack='Android', priv='https://prajjwalgautam.github.io/discipline-coach-privacy/'),
 dict(k='app', name='Activity Companion', ini='AC', c1='#FF8A3D', c2='#4a1d05', type='Social activity app', desc='Find people for hikes, rides, cafes, sports and events. Matching by activity, interests, area and time, with ID verification and safety tools.', stack='Flutter · mobile', st='In development'),
 dict(k='app', name='First Math', ini='FM', c1='#E8C547', c2='#4a3400', type='Quiz game · Uno Technology', desc='Maths and science game with easy, medium and hard modes for each subject, sign-in and live points.', stack='PHP · JavaScript', repo='https://github.com/Prajjwalgautam/Project--First_Math'),
 dict(k='vid', name='Nepal Bhoomi Reels', logo='NB', c1='#8a1f4a', type='Property video series', desc='Property videos and reels: scripted, edited, graded, captioned for SEO and published, with monthly reports.', stack='Remotion · AI video · SEO', live='https://www.nepalbhoomi.com'),
 dict(k='vid', name='Remotion Video Engine', ini='RV', c1='#4D7BFF', c2='#0a1440', type='Programmatic video system', desc='Videos built from code: Remotion with Python AI tools for Whisper captions, upscaling, background removal and tracking, plus resumable renders.', stack='Remotion · TypeScript · Python', st='Internal tool'),
 dict(k='vid', name='The 195 Project', ini='195', c1='#E8C547', c2='#4a3400', type='Documentary series', desc='Documentary-style country episodes with Blender 3D scenes, edited in Remotion. Episode 11: Turkey, the country in layers.', stack='Blender · Remotion', st='Series'),
 dict(k='vid', name='Nepal Bhoomi Sound', logo='NB', c1='#2EE6A6', type='Sonic branding & music', desc='A 4–6 second sonic logo on madal, sarangi and bansuri for every video, and an AI-produced Dohori brand song with an animated video in production.', stack='Suno · AI video · Sound design', st='Brand audio'),
 dict(k='vid', name='Slugforge Productions', logo='SF', c1='#6b4cff', type='Studio video services', desc='Editing, podcast repurposing, colour grading, AI-assisted video and motion graphics.', stack='Editing · Grading · AI video', live='https://slugforge.vercel.app'),
 dict(k='vid', name='Study-Abroad Content', ini='SA', c1='#9B7BFF', c2='#1e1050', type='Freelance · education', desc='Explainers on IELTS, GRE, SAT and study-abroad applications, plus podcasts cut into shorts.', stack='Short-form · Motion', st='Freelance'),
]
FAQ = [
 ("What does Prajwal Gautam do?", "Prajwal Gautam is an AI engineer, full-stack and app developer, AI video producer and motion designer, and SEO, AEO and growth marketer based in Kathmandu, Nepal. He builds AI-powered websites and apps, produces video, and runs SEO, ads and branding for businesses worldwide."),
 ("What is AEO and do you offer it?", "AEO, Answer Engine Optimization, makes your business the answer that ChatGPT, Perplexity, Gemini and Google AI Overviews give. Yes: I add structured data, llms.txt, answer-first content and consistent citations, and track AI mentions monthly."),
 ("Which industries do you work with?", "Real estate (daily, at Nepal Bhoomi), education and study-abroad consultancies, e-commerce and retail, restaurants and travel, and I offer dedicated packages for jewellers and SaaS companies."),
 ("Do you make motion design and animation for SaaS?", "Yes. I build product explainers, UI animations and launch videos, often in Remotion so they can be re-rendered when your product changes, plus Blender 3D and WebGL."),
 ("Can you build an AI-powered website or app for my business?", "Yes. I build with Next.js, React, Node.js, Laravel and PostgreSQL, add AI features such as language-model integrations, assistants and automations, and secure them with proper sign-in, 2FA and audit logs."),
 ("Which programming languages and frameworks do you use?", "TypeScript and JavaScript with Next.js, React and Node.js; PHP with Laravel; Python for AI and automation; SQL with PostgreSQL and MySQL; and GLSL for WebGL. If your project needs a stack I don't use, I'll tell you before we start."),
 ("How much does a project cost?", "Every project gets a fixed-price quote after a free 20-minute call. SEO, AEO, ads and content are usually monthly retainers. You always see the price before work starts."),
 ("How do I start a project with you?", "Email prajolgautam1234@gmail.com or message me on WhatsApp at +977 984-8137372 with a short description of your goal. I reply within one working day, Nepal time (UTC+5:45)."),
]
SLASH = [('AI Engineering','ai-engineer-nepal'),('Full-Stack &amp; Apps','full-stack-developer-nepal'),('AI Video &amp; Motion','saas-motion-design'),('SEO, AEO &amp; Ads','aeo-geo-expert'),('Growth &amp; Branding','growth-marketing-consultant')]
INDUSTRIES = [
 dict(n='Real Estate', tag='Proven · Nepal Bhoomi', line='Property reels, listing platforms and lead ads that sell land and homes.', chips=['Property reels','Listing sites','Lead ads','Sonic branding'], slug='real-estate-marketing-nepal'),
 dict(n='Jewellers', tag='Package for jewellers', line='Macro product films, 3D renders, graphics and wedding-season campaigns that make every piece shine.', chips=['Macro video','3D renders','Catalogues','Festive ads'], slug='jewellery-marketing-nepal'),
 dict(n='SaaS &amp; Tech', tag='Remotion · Blender · WebGL', line='Explainers, UI motion and launch videos, built from code so every product update re-renders.', chips=['Explainers','UI animation','Launch videos','3D & WebGL'], slug='saas-motion-design'),
 dict(n='E-commerce', tag='Proven · Sayapatri, Zylux', line='Stores, payments, admin dashboards and the ads and SEO that fill the cart.', chips=['Online stores','Khalti','Dashboards','Meta ads'], slug='growth-marketing-consultant'),
 dict(n='Education', tag='Proven · Fitfutures, freelance', line='E-learning platforms and study-abroad explainers that students and parents trust.', chips=['E-learning','Explainers','Shorts','YouTube SEO'], slug='ai-video-production'),
 dict(n='Food &amp; Travel', tag='Proven · EBhojanalaya, The 195 Project', line='Ordering systems, food and travel reels, and local SEO and AEO for Maps and AI search.', chips=['Ordering apps','Travel films','Local SEO','AEO'], slug='seo-expert-nepal'),
]

# ------------------------------------------------------------------ engine
def engine():
    s = open(os.path.join(ROOT, 'templates', 'card-engine.html')).read()
    eng = s[s.index('/* ================= WebGL ================= */'):s.rindex('})();')]
    def R(a, b, cnt=1):
        nonlocal eng
        assert eng.count(a) == cnt, (eng.count(a), a[:70]); eng = eng.replace(a, b)
    R("$('bootTxt').textContent='3D unavailable ·'; return;", "window.__engineReady=true; return;")
    R("{canvas, antialias:false, powerPreference:'high-performance'}", "{canvas, antialias:false, alpha:true, powerPreference:'high-performance'}")
    R("renderer.setClearColor(0x04060f,1);", "renderer.setClearColor(0x000000,0);")
    R("const N=raw.length/5; $('nCards').textContent=N.toLocaleString('en-US');", "const N=raw.length/5;")
    eng = eng.replace('Unbounded, "Arial Black", sans-serif', '"Sofia Sans Extra Condensed", "Arial Narrow", sans-serif')
    R("let fs=46; const t=k.s.toUpperCase();", "let fs=60; const t=k.s.toUpperCase();")
    # sharper card labels: draw the skill atlas at 2x and filter it anisotropically
    R("atlas.width=1024; atlas.height=1440; const atlasTex=new THREE.CanvasTexture(atlas);",
      "atlas.width=2048; atlas.height=2880; const atlasTex=new THREE.CanvasTexture(atlas); atlasTex.anisotropy=renderer.capabilities.getMaxAnisotropy();")
    R("g.clearRect(0,0,1024,1440);", "g.setTransform(2,0,0,2,0,0); g.clearRect(0,0,1024,1440);")
    R("  const cc=CATC[ci];\n  return fromPoints(pts,W,H,24,1.6,(p,k)=>{ const own=data[k*4+2]===ci;",
      "  const cc=ci>=0?CATC[ci]:hex('#0C0C0E');\n  return fromPoints(pts,W,H,24,1.6,(p,k)=>{ const own=ci>=0&&data[k*4+2]===ci;")
    R("  galaxy:galaxy(), helix:helix(), wave:wave(),", """  galaxy:galaxy(), helix:helix(), wave:wave(), dust:dust(),""")
    R("const STATES={", """function dust(){ const P=new Float32Array(N*3), C=new Float32Array(N*3); const g=hex('#bcc2cb');
  for(let k=0;k<N;k++){ P.set([(rnd(k*2.1)-.5)*120,(rnd(k*3.3)-.5)*70,-22-rnd(k*4.7)*40],k*3); const red=rnd(k*7.7)<.015; const l=.82+.25*rnd(k*5.5);
    C.set(red?[.95,.2,.29]:[g[0]*l,g[1]*l,g[2]*l],k*3); }
  return {P,C,kind:1,size:.11}; }
const STATES={""")
    R("  CATS.forEach((c,i)=>STATES['w'+i]=textShape(c.word,i));", "  CATS.forEach((c,i)=>STATES['w'+i]=textShape(c.word,i)); STATES.code=textShape('</>',-1);")
    R("  drawAtlas(); ready=true; lastPair='';", "  drawAtlas(); ready=true; lastPair=''; window.__engineReady=true;")
    eng = eng.replace("#ff2e4d", "#F2334B")
    a = eng.index("function layoutOf(name){"); b = eng.index("/* --- atlas --- */")
    eng = eng[:a] + """function layoutOf(name){
  const m=isMobile(), fx=Math.min(halfW-6.6,6.8);
  if(name==='face') return m?{o:[0,halfH*.02,0],s:.78}:{o:[halfW*.04,-1.7,0],s:.9};
  if(name==='face2') return m?{o:[0,halfH-8.4,0],s:.8}:{o:[-fx,-.4,0],s:1};
  if(name==='code') return m?{o:[0,halfH*.55,0],s:.5}:{o:[halfW*.48,halfH*.3,0],s:.72};
  if(name==='galaxy') return m?{o:[0,3,0],s:.62}:{o:[halfW*.3,0,0],s:1};
  if(name==='helix') return m?{o:[0,halfH*.5,0],s:.5}:{o:[0,halfH*.42,0],s:Math.min(1,(halfW*2*.92)/26)};
  if(name==='wave'||name==='dust') return {o:[0,0,0],s:1};
  if(name==='nb'||name==='sf') return m?{o:[0,halfH*.42,0],s:.75}:{o:[halfW*.4,0,0],s:1};
  if(name[0]==='w') return m?{o:[0,halfH*.45,0],s:Math.min(1,(halfW*2*.94)/24)}:{o:[0,halfH*.38,0],s:Math.min(1.1,(halfW*2*.9)/24)};
  return {o:[0,0,0],s:1};
}

""" + eng[b:]
    a = eng.index("let composer=null, bloom=null;"); b = eng.index("function layout(){")
    eng = eng[:a] + "let composer=null;\n" + eng[b:]
    R(" const cur=anchors[Math.min(anchors.length-1,Math.round(sTarget))].c; chapLinks.forEach(a=>a.classList.toggle('on',a.dataset.c===cur));", "")
    R("  if(!reduce){ U.uIntro.value=Math.min(1,t/3); }", "  U.uIntro.value = reduce?1:(window.__introT0? Math.min(1,(performance.now()-window.__introT0)/2600) : 0);")
    R("  const shown=Math.round(N*Math.min(1,U.uIntro.value)); $('bootN').textContent=shown.toLocaleString('en-US'); if(U.uIntro.value>=1) $('bootTxt').textContent='Live ·';\n", "")
    R("else if(kind<1.5){ p=rY(uTime*.08)*p;", "else if(kind<1.5){ p=rY(uTime*.3)*p;")
    R("  float roll=arc*fract(r*3.7)*6.28;", "  float gx=(uKindA>.5&&uKindA<1.5?1.-e:0.)+(uKindB>.5&&uKindB<1.5?e:0.);\n  yaw+=gx*uTime*(.7+r*1.6); float roll=arc*fract(r*3.7)*6.28+gx*sin(uTime*.9+r*20.)*.5;")
    # Adaptive quality: if a device can't hold ~40 fps, lower the render resolution step by step and drop the glass blur.
    R("  if(composer) composer.render(); else renderer.render(scene,camera);\n  requestAnimationFrame(frame);",
      "  if(composer) composer.render(); else renderer.render(scene,camera);\n  perfCheck(dt,t);\n  requestAnimationFrame(frame);")
    R("const clock=new THREE.Clock(); let lastT=0;",
      "const clock=new THREE.Clock(); let lastT=0;\n"
      "const PR=[Math.min(devicePixelRatio, isMobile()?1.5:1.75), 1.25, 1, .8]; let prLvl=0, pSum=0, pN=0;\n"
      "function perfCheck(dt,t){ if(t<4||document.hidden) return; pSum+=dt; pN++; if(pN<90) return; const avg=pSum/pN; pSum=0; pN=0;\n"
      "  if(avg>1/40 && prLvl<PR.length-1){ prLvl++; if(PR[prLvl]<PR[0]){ renderer.setPixelRatio(PR[prLvl]); layout(); } document.documentElement.classList.add('lite'); } }")
    R("progress=y/Math.max(1,document.documentElement.scrollHeight-innerHeight);", "progress=y/Math.max(1,docH-innerHeight);")
    R("  anchors[0].y=0;\n}", "  anchors[0].y=0; docH=document.documentElement.scrollHeight;\n}")
    R("function readScroll(){", "var docH=document.documentElement.scrollHeight; addEventListener('resize',()=>{docH=document.documentElement.scrollHeight});\nfunction readScroll(){")
    R("eg.strokeStyle='#F2334B';", "eg.strokeStyle='#ffffff';")
    R("if(e.target.closest('a,button,input,textarea,.glass')) return;", "if(e.target.closest('a,button,input,textarea,.glass,.car,.codebox,summary')) return;")
    return eng

# ------------------------------------------------------------------ fragments
def lg(o):
    if o.get('logo'):
        cls = 'light' if o['logo'] == 'NB' else 'dark'; alt = 'Nepal Bhoomi logo' if o['logo'] == 'NB' else 'Slugforge Studio logo'
        return f'<div class="lg {cls}"><img src="{{{{IMG_{o["logo"]}}}}}" alt="{alt}" width="112" height="112" loading="lazy"></div>'
    return f'<div class="lg" style="--c1:{o.get("c1","#4D7BFF")};--c2:{o.get("c2","#0b1024")}"><span>{o["ini"]}</span></div>'

def page_main(svc_link):
    mega = ''.join(f'<span class="mc">{ch}</span>' for ch in 'PRAJWALGAUTAM')
    mega_html = f'<span class="sr">Prajwal Gautam – </span><span class="mega" id="mega" aria-hidden="true">{mega}</span>'
    slash = ''.join(f'<li><a href="{svc_link(slug)}">{t}</a></li>' for t, slug in SLASH)
    legend = ''.join(f'<a href="{svc_link(c["slug"])}" style="--c:{c["c"]}"><i></i>{E(c["name"])}</a>' for c in CATS)
    cats = ''.join(f'''<section class="cat" data-state="w{i}" data-theme="night" data-label="(02) Services · {E(c['name'])}" style="--c:{c['c']}" aria-labelledby="cat{i}"><div class="cat-card glass">
 <div class="cat-top"><span><b>{i+1:02d}</b> / 06 · Service</span><span>{len(c['skills'])} skills</span></div>
 <h2 class="cat-h" id="cat{i}">{c['h']}</h2><p>{c['blurb']}</p><div class="chips">{''.join(f'<span>{E(s)}</span>' for s in c['skills'])}</div>
 <p class="proof">Proof: <em>{c['proof']}</em></p><a class="more" href="{svc_link(c['slug'])}">{E(BY_SLUG[c['slug']]['kw'])} →</a></div></section>''' for i, c in enumerate(CATS))
    jobs = ''.join(f'''<article class="job glass" style="--c:{j['c']}"><div class="job-top">{lg(j)}<div><h3>{E(j['co'])}{'<span class="now">NOW</span>' if j.get('now') else ''}</h3><div class="t">{j['title']}</div><div class="w">{j['where']}</div></div></div><ul>{''.join(f'<li>{p}</li>' for p in j['pts'])}</ul></article>''' for j in JOBS)
    panels = []
    for i, w in enumerate(WORK):
        st = '<span class="live-dot">● Live</span>' if w.get('live') else f'<span>{E(w.get("st","Android app" if w.get("priv") else "Code on GitHub"))}</span>'
        link = (f'<a href="{w["live"]}" target="_blank" rel="noopener">Open live ↗</a>' if w.get('live') else
                f'<a href="{w["repo"]}" target="_blank" rel="noopener">GitHub ↗</a>' if w.get('repo') else
                f'<a href="{w["priv"]}" target="_blank" rel="noopener">Privacy policy ↗</a>' if w.get('priv') else '<a href="#contact">Ask me ↗</a>')
        panels.append(f'''<article class="panel" data-k="{w['k']}" style="--c1:{w.get('c1','#4D7BFF')}" aria-label="{E(w['name'])}"><div class="p-top">{st}<span>{i+1:02d}</span></div><div class="p-mid">{lg(w)}<h3>{E(w['name'])}</h3><span class="p-type">{E(w['type'])}</span><p class="p-desc">{E(w['desc'])}</p></div><div class="p-foot"><span class="stk">{E(w['stack'])}</span>{link}</div></article>''')
    rows = ''.join(f'''<a class="rowl" href="{svc_link(s['slug'])}"><span class="n">{i+1:02d}</span><h3>{E(s['kw'])}</h3><span class="d">{E(' · '.join(n for n, _ in s['offers'][:3]))}</span><span class="ar" aria-hidden="true">↗</span></a>''' for i, s in enumerate(SERVICES))
    faq = ''.join(f'<details class="qa"><summary><h3>{E(q)}</h3><span aria-hidden="true">+</span></summary><p>{E(a)}</p></details>' for q, a in FAQ)
    foot_a = ''.join(f'<a href="{svc_link(s["slug"])}">{E(s["kw"])}</a>' for s in SERVICES[:7])
    foot_b = ''.join(f'<a href="{svc_link(s["slug"])}">{E(s["kw"])}</a>' for s in SERVICES[7:])
    inds = ''.join(f'''<a class="ind" href="{svc_link(d['slug'])}"><span class="ind-tag">({i+1:02d}) {E(d['tag'])}</span><h3>{d['n']}</h3><p>{E(d['line'])}</p><span class="chips">{''.join(f'<span>{E(c)}</span>' for c in d['chips'])}</span><span class="ind-go">{E(BY_SLUG[d['slug']]['kw'])} ↗</span></a>''' for i, d in enumerate(INDUSTRIES))
    cnt = {k: sum(1 for w in WORK if w['k'] == k) for k in ('web','app','vid')}
    t = open(os.path.join(ROOT, 'templates', 'page.html')).read()
    rep = {'{{MEGA}}': mega_html, '{{MEGA_FOOT}}': ''.join(f'<span>{c}</span>' for c in 'PRAJWALGAUTAM'),
           '{{SLASH}}': slash, '{{LEGEND}}': legend, '{{JOBS}}': jobs, '{{PANELS}}': ''.join(panels),
           '{{ROWS}}': rows, '{{INDUSTRIES}}': inds, '{{FAQ}}': faq, '{{FOOT_A}}': foot_a, '{{FOOT_B}}': foot_b,
           '{{N_ALL}}': str(len(WORK)), '{{N_WEB}}': str(cnt['web']), '{{N_APP}}': str(cnt['app']), '{{N_VID}}': str(cnt['vid']),
           '{{CATS_JSON}}': json.dumps([dict(name=c['name'], word=c['word'], c=c['c'], skills=c['skills']) for c in CATS]),
           '{{ROLES_JSON}}': json.dumps(ROLES), '{{ENGINE}}': engine()}
    # the MEGA token sits inside an h1 that already has a mega span in the template; replace that whole span
    t = t.replace('<span class="mega" id="mega" aria-label="Prajwal Gautam">{{MEGA}}</span>', '{{MEGA}}')
    for k, v in rep.items():
        assert k in t, k; t = t.replace(k, v)
    return t

# ------------------------------------------------------------------ SEO head
DESC = "Prajwal Gautam is an AI engineer, full-stack and app developer, AI video and motion designer, and SEO, AEO, ads and growth marketer in Kathmandu, Nepal, working with real estate, jewellery, SaaS and e-commerce brands worldwide."
TITLE = "Prajwal Gautam – AI Engineer, Full-Stack & App Developer, Growth Marketer in Nepal"
KNOWS = sorted({s for c in CATS for s in c['skills']} | {"Artificial intelligence engineering","Answer Engine Optimization (AEO)","Generative Engine Optimization (GEO)","Motion design","SaaS product animation","Real estate marketing","Jewellery marketing","Graphic design","Next.js","TypeScript","PostgreSQL","Remotion","Blender","Full-stack web development","Mobile app development","AI video production","Search engine optimization","Google Ads","Meta Ads","Growth marketing","E-commerce marketing","Branding","Laravel","PHP","Node.js","React","Django","Python","JavaScript","SQL","Three.js","WebGL"})

def person():
    return {"@type":"Person","@id":SITE+"#person","name":"Prajwal Gautam","alternateName":["Prajjwal Gautam"],"url":SITE,
      "image":SITE+"assets/prajwal-gautam.webp","jobTitle":"AI Engineer, Full-Stack & App Developer, Growth Marketer","description":DESC,
      "email":"mailto:prajolgautam1234@gmail.com","telephone":"+977-9848137372",
      "address":{"@type":"PostalAddress","addressLocality":"Kathmandu","addressRegion":"Bagmati","addressCountry":"NP"},
      "alumniOf":[{"@type":"CollegeOrUniversity","name":"New Summit College, Tribhuvan University"},{"@type":"EducationalOrganization","name":"Kathmandu Model College"}],
      "worksFor":{"@type":"Organization","name":"Nepal Bhoomi","url":"https://www.nepalbhoomi.com"},
      "knowsAbout":KNOWS,"knowsLanguage":["English","Nepali","Hindi"],
      "sameAs":["https://www.linkedin.com/in/prajjwal-gautam/","https://github.com/Prajjwalgautam"]}

def head_main():
    graph = [
      {"@type":"ProfilePage","@id":SITE+"#profile","url":SITE,"name":TITLE,"dateModified":TODAY,"mainEntity":{"@id":SITE+"#person"},"inLanguage":"en"},
      person(),
      {"@type":"ProfessionalService","@id":SITE+"#service","name":"Prajwal Gautam – AI, Development & Growth Services","url":SITE,"image":SITE+"assets/og-image.jpg",
       "description":DESC,"founder":{"@id":SITE+"#person"},"telephone":"+977-9848137372","email":"prajolgautam1234@gmail.com",
       "address":{"@type":"PostalAddress","addressLocality":"Kathmandu","addressCountry":"NP"},"areaServed":["Nepal","Worldwide"],
       "hasOfferCatalog":{"@type":"OfferCatalog","name":"Services","itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":s['kw'],"url":f"{SITE}services/{s['slug']}/","description":s['desc']}} for s in SERVICES]}},
      {"@type":"WebSite","@id":SITE+"#website","url":SITE,"name":"Prajwal Gautam","inLanguage":"en","publisher":{"@id":SITE+"#person"}},
      {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in FAQ]},
      {"@type":"ItemList","name":"Projects by Prajwal Gautam","itemListElement":[{"@type":"ListItem","position":i+1,"item":{"@type":"CreativeWork","name":w["name"],"description":w["desc"],"creator":{"@id":SITE+"#person"},**({"url":w.get("live") or w.get("repo")} if (w.get("live") or w.get("repo")) else {})}} for i, w in enumerate(WORK)]},
    ]
    ld = json.dumps({"@context":"https://schema.org","@graph":graph}, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(TITLE)}</title>
<meta name="description" content="{E(DESC)}">
<meta name="author" content="Prajwal Gautam">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{SITE}">
<meta name="theme-color" content="#EDEEF0">
<meta property="og:type" content="profile"><meta property="og:site_name" content="Prajwal Gautam">
<meta property="og:title" content="{E(TITLE)}"><meta property="og:description" content="{E(DESC)}">
<meta property="og:url" content="{SITE}"><meta property="og:image" content="{SITE}assets/og-image.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="en_US">
<meta property="profile:first_name" content="Prajwal"><meta property="profile:last_name" content="Gautam">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(TITLE)}">
<meta name="twitter:description" content="{E(DESC)}"><meta name="twitter:image" content="{SITE}assets/og-image.jpg">
<meta name="geo.region" content="NP-BA"><meta name="geo.placename" content="Kathmandu"><meta name="geo.position" content="27.7172;85.3240"><meta name="ICBM" content="27.7172, 85.3240">
<link rel="icon" href="assets/slugforge-logo.webp" type="image/webp">
<link rel="alternate" type="text/plain" href="{SITE}llms.txt" title="LLM summary">
<script type="application/ld+json">{ld}</script>"""

# ------------------------------------------------------------------ service pages
SVC_CSS = """
:root{--paper:#EDEEF0;--ink:#0C0C0E;--night:#07080A;--dim:#5d6068;--accent:#F2334B;--line:rgba(12,12,14,.14);
--disp:"Sofia Sans Extra Condensed","Arial Narrow",Impact,sans-serif;--cond:"Sofia Sans Condensed","Arial Narrow",sans-serif;--body:"Sofia Sans","Noto Sans Devanagari",system-ui,sans-serif;--mono:"Spline Sans Mono",ui-monospace,Menlo,monospace;color-scheme:light}
*{box-sizing:border-box}html{background:var(--paper)}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);font-size:18px;line-height:1.6;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
a{color:inherit}:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.wrap{max-width:1200px;margin:0 auto}
.nav{display:flex;justify-content:space-between;align-items:center;gap:16px;padding-block:18px;font-family:var(--mono);font-size:13px}
.nav a{text-decoration:none}.nav .brk{display:flex;gap:22px}.nav .brk a::before{content:"[ ";opacity:.5}.nav .brk a::after{content:" ]";opacity:.5}
.crumbs{font-family:var(--mono);font-size:12px;color:var(--dim);padding-block:22px 0}.crumbs a{text-decoration:none}.crumbs a:hover{text-decoration:underline}
.paren{font-family:var(--mono);font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--dim);margin:0 0 10px}
h1{margin:10px 0 0;font-family:var(--disp);font-weight:900;text-transform:uppercase;font-size:clamp(58px,10.5vw,168px);line-height:.82;letter-spacing:-.005em;text-wrap:balance}
.lede{font-size:clamp(20px,1.9vw,27px);line-height:1.35;max-width:36ch;margin:26px 0 0;font-weight:500}
.by{font-family:var(--mono);font-size:12px;color:var(--dim);margin-top:22px;text-transform:uppercase;letter-spacing:.04em}
.btns{display:flex;gap:10px;flex-wrap:wrap;margin-top:26px}
.btn{display:inline-flex;gap:8px;align-items:center;padding:13px 20px;border-radius:999px;border:1px solid var(--ink);text-decoration:none;font-weight:600;font-size:15px}
.btn.hot{background:var(--accent);border-color:var(--accent);color:#fff}
section{padding-block:clamp(48px,9vh,96px);border-top:1px solid var(--line)}
section:first-of-type{border-top:0}
.cols{display:grid;grid-template-columns:minmax(0,.75fr) minmax(0,1.25fr);gap:clamp(20px,4vw,64px)}
h2{margin:0;font-family:var(--disp);font-weight:900;text-transform:uppercase;font-size:clamp(40px,5vw,76px);line-height:.88;text-wrap:balance}
.prose p{margin:0 0 16px;max-width:64ch}
.offers{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0;border-top:1px solid var(--line)}
.offers div{padding:20px 18px 20px 0;border-bottom:1px solid var(--line)}
.offers h3{margin:0 0 6px;font-family:var(--cond);font-weight:800;font-size:24px;text-transform:uppercase;line-height:1}
.offers p{margin:0;color:#34363c;font-size:16px}
ul.proof{margin:0;padding:0;list-style:none;display:grid;gap:12px}
ul.proof li{padding-left:22px;position:relative;max-width:64ch}ul.proof li::before{content:"↗";position:absolute;left:0;color:var(--accent)}
ol.steps{margin:0;padding:0;list-style:none;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;counter-reset:s}
ol.steps li{border-top:2px solid var(--ink);padding-top:14px;counter-increment:s}
ol.steps li::before{content:"0" counter(s);font-family:var(--mono);font-size:12px;color:var(--accent)}
ol.steps h3{margin:8px 0 6px;font-family:var(--cond);font-weight:800;font-size:22px;text-transform:uppercase;line-height:1}
ol.steps p{margin:0;font-size:15px;color:#34363c}
.chips{display:flex;flex-wrap:wrap;gap:8px}.chips span{font-family:var(--mono);font-size:13px;padding:7px 12px;border-radius:999px;border:1px solid var(--line)}
details{border-bottom:1px solid var(--line)}details:first-of-type{border-top:1px solid var(--line)}
summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;gap:16px;align-items:center;padding:18px 2px}
summary::-webkit-details-marker{display:none}summary h3{margin:0;font-family:var(--cond);font-weight:700;font-size:22px;line-height:1.15}
summary span{font-size:22px;transition:transform .3s}details[open] summary span{transform:rotate(45deg);color:var(--accent)}
details p{margin:0;padding:0 2px 18px;max-width:64ch;color:#2f3137}
.cta{background:var(--night);color:#EDEEF0;border-radius:24px;padding:clamp(28px,5vw,56px);border:0;margin-block:40px}
.cta h2{font-size:clamp(46px,6vw,96px)}.cta h2 span{color:var(--accent)}
.cta .lines{display:grid;gap:6px;margin-top:22px;font-family:var(--mono);font-size:16px}.cta .btn{border-color:#EDEEF0}
.rel a{display:grid;grid-template-columns:minmax(0,1fr) 30px;gap:12px;align-items:center;padding:18px 4px;border-bottom:1px solid var(--line);text-decoration:none}
.rel a:first-child{border-top:1px solid var(--line)}
.rel h3{margin:0;font-family:var(--disp);font-weight:900;text-transform:uppercase;font-size:clamp(28px,3.4vw,52px);line-height:.9}
.rel a:hover{color:var(--accent)}
footer{padding-block:40px 60px;border-top:1px solid var(--line);font-family:var(--mono);font-size:12px;color:var(--dim);display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px}
footer a{text-decoration:none}footer a:hover{text-decoration:underline}
@media (max-width:860px){.cols{grid-template-columns:minmax(0,1fr)}.offers{grid-template-columns:minmax(0,1fr)}ol.steps{grid-template-columns:repeat(2,minmax(0,1fr))}.nav .brk{display:none}}
@media (max-width:480px){ol.steps{grid-template-columns:minmax(0,1fr)}}
"""

def page_service(s, home, svc_link, assets):
    url = f"{SITE}services/{s['slug']}/"
    crumbs = [{"@type":"ListItem","position":1,"name":"Home","item":SITE},{"@type":"ListItem","position":2,"name":"Services","item":SITE+"#find"},{"@type":"ListItem","position":3,"name":s['kw'],"item":url}]
    graph = [
      {"@type":"WebPage","@id":url+"#webpage","url":url,"name":s['title'],"description":s['desc'],"inLanguage":"en","dateModified":TODAY,
       "isPartOf":{"@id":SITE+"#website"},"breadcrumb":{"@id":url+"#crumbs"},"about":{"@id":url+"#service"},"author":{"@id":SITE+"#person"}},
      {"@type":"Service","@id":url+"#service","name":s['kw'],"serviceType":s['short'],"description":s['desc'],"url":url,
       "provider":{"@id":SITE+"#person"},"areaServed":[{"@type":"Country","name":"Nepal"},"Worldwide"],
       "hasOfferCatalog":{"@type":"OfferCatalog","name":s['short'],"itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":n,"description":d}} for n, d in s['offers']]}},
      {"@type":"BreadcrumbList","@id":url+"#crumbs","itemListElement":crumbs},
      {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in s['faq']]},
      {"@type":"Person","@id":SITE+"#person","name":"Prajwal Gautam","url":SITE,"jobTitle":"AI Engineer, Full-Stack & App Developer, Growth Marketer",
       "sameAs":["https://www.linkedin.com/in/prajjwal-gautam/","https://github.com/Prajjwalgautam"]},
    ]
    ld = json.dumps({"@context":"https://schema.org","@graph":graph}, ensure_ascii=False)
    offers = ''.join(f'<div><h3>{E(n)}</h3><p>{E(d)}</p></div>' for n, d in s['offers'])
    proof = ''.join(f'<li>{E(p)}</li>' for p in s['proof'])
    steps = ''.join(f'<li><h3>{E(a)}</h3><p>{E(b)}</p></li>' for a, b in PROCESS)
    tools = ''.join(f'<span>{E(t)}</span>' for t in s['tools'])
    faq = ''.join(f'<details><summary><h3>{E(q)}</h3><span aria-hidden="true">+</span></summary><p>{E(a)}</p></details>' for q, a in s['faq'])
    rel = ''.join(f'<a href="{svc_link(r, True)}"><h3>{E(BY_SLUG[r]["kw"])}</h3><span aria-hidden="true">↗</span></a>' for r in s['related'])
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(s['title'])}</title>
<meta name="description" content="{E(s['desc'])}">
<meta name="author" content="Prajwal Gautam">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Prajwal Gautam">
<meta property="og:title" content="{E(s['title'])}"><meta property="og:description" content="{E(s['desc'])}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}assets/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="NP-BA"><meta name="geo.placename" content="Kathmandu">
<link rel="icon" href="{assets}slugforge-logo.webp" type="image/webp">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sofia+Sans+Extra+Condensed:wght@900&family=Sofia+Sans+Condensed:wght@700;800&family=Sofia+Sans:wght@400;500;600&family=Spline+Sans+Mono:wght@400&display=swap">
<script type="application/ld+json">{ld}</script>
<style>{SVC_CSS}</style>
<script>/* always open a service page at the top */if(!location.hash){{try{{history.scrollRestoration="manual"}}catch(e){{}}scrollTo(0,0);addEventListener("DOMContentLoaded",()=>scrollTo(0,0));addEventListener("load",()=>scrollTo(0,0));addEventListener("pageshow",()=>scrollTo(0,0))}}</script>
</head>
<body>
<div class="wrap">
<nav class="nav" aria-label="Main"><a href="{home}">[ PG ] Prajwal Gautam</a><span class="brk"><a href="{home}#services">Services</a><a href="{home}#work">Work</a><a href="{home}#about">About</a></span><a href="{home}#contact" style="text-decoration:underline">Contact ↗</a></nav>
<nav class="crumbs" aria-label="Breadcrumb"><a href="{home}">Home</a> / <a href="{home}#find">Services</a> / <span aria-current="page">{E(s['kw'])}</span></nav>
<header style="padding-block:30px 60px">
  <p class="paren">(Service) · {E(s['short'])}</p>
  <h1>{E(s['kw'])}</h1>
  <p class="lede">{E(s['lede'])}</p>
  <div class="btns"><a class="btn hot" href="mailto:prajolgautam1234@gmail.com?subject={E(s['kw'])}%20project">Start a project</a><a class="btn" href="https://wa.me/9779848137372" target="_blank" rel="noopener">WhatsApp me</a><a class="btn" href="{home}#work">See my work</a></div>
  <p class="by">By Prajwal Gautam · AI Engineer, Full-Stack &amp; App Developer, Growth Marketer · Kathmandu, Nepal · Updated November 2026</p>
</header>
<main>
<section class="cols"><p class="paren">(Overview)</p><div class="prose">{''.join(f'<p>{E(p)}</p>' for p in s['intro'])}</div></section>
<section class="cols"><h2>{E(s['what_h'])}</h2><div class="prose">{''.join(f'<p>{E(p)}</p>' for p in s['what'])}</div></section>
<section><h2 style="margin-bottom:26px">{E(s['short'])} services</h2><div class="offers">{offers}</div></section>
<section class="cols"><h2>Proof from real work</h2><div><ul class="proof">{proof}</ul><div class="btns"><a class="btn" href="https://www.nepalbhoomi.com" target="_blank" rel="noopener">nepalbhoomi.com ↗</a><a class="btn" href="https://slugforge.vercel.app" target="_blank" rel="noopener">Slugforge Studio ↗</a></div></div></section>
<section><h2 style="margin-bottom:26px">How we work together</h2><ol class="steps">{steps}</ol></section>
<section class="cols"><h2>Tools &amp; languages</h2><div class="chips">{tools}</div></section>
<section class="cols"><h2>How much does it cost?</h2><div class="prose">{''.join(f'<p>{E(p)}</p>' for p in s['cost'])}</div></section>
<section class="cols"><h2>Frequently asked questions</h2><div>{faq}</div></section>
<div class="cta"><p class="paren" style="color:#8d919b">(Contact)</p><h2>Let’s talk about your <span>{E(s['short'].lower())}</span> project.</h2>
<div class="lines"><span>prajolgautam1234@gmail.com</span><span>WhatsApp +977 984-8137372</span><span>Kathmandu, Nepal · UTC+5:45 · replies within one working day</span></div>
<div class="btns"><a class="btn hot" href="mailto:prajolgautam1234@gmail.com">Email me</a><a class="btn" href="https://wa.me/9779848137372" target="_blank" rel="noopener">WhatsApp ↗</a><a class="btn" href="https://www.linkedin.com/in/prajjwal-gautam/" target="_blank" rel="noopener">LinkedIn ↗</a></div></div>
<section><p class="paren">(Related services)</p><div class="rel">{rel}</div></section>
</main>
<footer><span>© 2026 Prajwal Gautam · Kathmandu, Nepal</span><span><a href="{home}">Home</a> · {' · '.join(f'<a href="{svc_link(x["slug"], True)}">{E(x["short"])}</a>' for x in SERVICES)}</span></footer>
</div>
</body>
</html>
"""

# ------------------------------------------------------------------ build
def build():
    face = open(os.path.join(ROOT, 'data', 'face-cards.b64')).read()
    # ---- site
    site_link = lambda slug, from_svc=False: (f"../{slug}/" if from_svc else f"services/{slug}/")
    main = page_main(site_link)
    main = main.replace('{{HEAD}}', head_main()).replace('{{FACE}}', face)
    main = (main.replace('{{IMG_NB}}', 'assets/nepal-bhoomi-logo.webp').replace('{{IMG_SF}}', 'assets/slugforge-logo.webp')
                .replace('{{IMG_PHOTO}}', 'assets/prajwal-gautam.webp'))
    assert '{{' not in main, re.findall(r'\{\{[A-Z_]+\}\}', main)[:5]
    open(os.path.join(REPO, 'index.html'), 'w').write(main)
    for s in SERVICES:
        d = os.path.join(REPO, 'services', s['slug']); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w').write(page_service(s, '../../', site_link, '../../assets/'))
    urls = [SITE] + [f"{SITE}services/{s['slug']}/" for s in SERVICES]
    open(os.path.join(REPO, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        ''.join(f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>{"1.0" if u==SITE else "0.8"}</priority></url>\n' for u in urls) + '</urlset>\n')
    open(os.path.join(REPO, 'robots.txt'), 'w').write(f"""User-agent: *
Allow: /

# AI search and answer engines are welcome
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Bingbot
Allow: /

Sitemap: {SITE}sitemap.xml
""")
    llms = ["# Prajwal Gautam", "", f"> {DESC}", "", "Website: " + SITE, "",
            "## Roles", "- AI Engineer", "- Full-Stack Web Developer", "- App Developer (mobile and web)", "- AI Video Producer",
            "- SEO and AEO/GEO Specialist (AI search optimization) and Marketing Researcher", "- Motion Designer (SaaS product animation, 3D)", "- Industries: real estate, jewellery, SaaS and tech, e-commerce, education, food and travel", "- Google Ads and Meta Ads Campaign Strategist", "- Growth, E-commerce and Brand Marketer", "",
            "## Service pages"] + [f"- [{s['kw']}]({SITE}services/{s['slug']}/): {s['desc']}" for s in SERVICES] + ["",
            "## Experience"] + [f"- {j['co']} ({j['where']}): {html.unescape(j['title'])}. " + ' '.join(re.sub('<[^>]+>', '', p) for p in j['pts']) for j in JOBS] + ["",
            "## Live projects", "- [Nepal Bhoomi](https://www.nepalbhoomi.com): real-estate platform; video, SEO and growth.", "- [Slugforge Studio](https://slugforge.vercel.app): creative studio website and video services.", "",
            "## Languages", "- Code: PHP, JavaScript, Python, SQL, HTML/CSS", "- Frameworks: Laravel, Node.js, React, Django, Three.js", "- Spoken: English, Nepali, Hindi", "",
            "## Education", "- BSc CSIT, New Summit College, Tribhuvan University", "- +2 Science, Kathmandu Model College", "",
            "## Contact", "- Email: prajolgautam1234@gmail.com", "- Phone & WhatsApp: +977 984-8137372 (https://wa.me/9779848137372)", "- LinkedIn: https://www.linkedin.com/in/prajjwal-gautam/",
            "- GitHub: https://github.com/Prajjwalgautam", "- Location: Kathmandu, Nepal (UTC+5:45); works with clients worldwide", ""]
    open(os.path.join(REPO, 'llms.txt'), 'w').write('\n'.join(llms))

    # ---- artifact (multi-file)
    art = os.path.join(ROOT, 'preview'); shutil.rmtree(art, ignore_errors=True); os.makedirs(os.path.join(art, 'assets'))
    for f in ['nepal-bhoomi-logo.webp', 'slugforge-logo.webp', 'prajwal-gautam.webp']:
        shutil.copy(os.path.join(REPO, 'assets', f), os.path.join(art, 'assets', f))
    art_link = lambda slug, from_svc=False: (f"../{slug}/index.html" if from_svc else f"services/{slug}/index.html")
    a = page_main(art_link)
    a = a.replace('{{HEAD}}', '<title>Prajwal Gautam Portfolio</title>').replace('{{FACE}}', face)
    a = (a.replace('{{IMG_NB}}', 'assets/nepal-bhoomi-logo.webp').replace('{{IMG_SF}}', 'assets/slugforge-logo.webp').replace('{{IMG_PHOTO}}', 'assets/prajwal-gautam.webp'))
    a = a.replace('</head>\n<body data-theme="paper">\n<script>document.documentElement.classList.add(\'js\')</script>',
                  '<script>document.documentElement.classList.add(\'js\');document.body.dataset.theme=\'paper\'</script>')
    a = a.replace('</body>\n</html>\n', '')
    assert '<body' not in a and '</head>' not in a
    open(os.path.join(art, 'index.html'), 'w').write(a)
    for s in SERVICES:
        d = os.path.join(art, 'services', s['slug']); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w').write(page_service(s, '../../', art_link, '../../assets/'))
    wc = {s['slug']: len(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', page_service(s, '/', site_link, '/'), flags=re.S)).split()) for s in SERVICES}
    print('built. service page word counts:', wc)

if __name__ == '__main__':
    build()
