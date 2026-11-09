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

# Palette: three pillar colours, used only as small marks. Keep these in sync with --build/--create/--grow in page.html.
BUILD, CREATE, GROW = '#7B8CFF', '#F2334B', '#E8B04A'

# Six skill groups. They colour the arms of the spinning card galaxy and fill the card labels.
CATS = [
 dict(name='AI Engineering', word='AI', c='#8C9BFF', pillar='build',
      skills=['LLM Integrations','Prompt Engineering','AI Automation','AI Research','AI Image Gen','AI Scriptwriting']),
 dict(name='Full-Stack', word='CODE', c='#6F80F5', pillar='build',
      skills=['TypeScript','Next.js & React','Node.js','PHP & Laravel','PostgreSQL & MySQL','Tailwind CSS']),
 dict(name='Apps & APIs', word='APPS', c='#B3BCFF', pillar='build',
      skills=['Android Apps','Web Apps','REST APIs','Khalti Payments','Auth, 2FA & OAuth','Prisma & Drizzle']),
 dict(name='Video & Motion', word='VIDEO', c=CREATE, pillar='create',
      skills=['AI Video','Motion Graphics','SaaS Animation','Blender 3D','Color Grading','Remotion']),
 dict(name='SEO & AEO', word='SEO', c=GROW, pillar='grow',
      skills=['Technical SEO','AEO & GEO','Keyword Research','SEO Content','Market Research','Audience Analytics']),
 dict(name='Ads & Brand', word='GROWTH', c='#F3CD86', pillar='grow',
      skills=['Google Ads','Meta Ads','Growth Marketing','E-commerce Marketing','Branding','Graphic Design']),
]

# The one services section: Build is the core, Create and Grow are add-ons. Each item links to its service page.
PILLARS = [
 dict(k='build', label='Build', badge='Core service', h='AI-powered websites, web apps and mobile apps.',
      p='From database and API to the screen your customers use, with sign-in, payments, dashboards and AI built in.',
      items=[('AI features & automation','ai-engineer-nepal'),('Full-stack web development','full-stack-developer-nepal'),
             ('Mobile & web apps','app-developer-nepal'),('Business websites','web-developer-kathmandu'),('Hire me as your AI developer','hire-ai-developer')],
      proof='<b>Proof:</b> Nepal Bhoomi platform, Zylux admin, Laravel HRMS, Sayapatri payments'),
 dict(k='create', label='Create', badge='Add-on', h='Launch videos and motion.',
      p='Product explainers, UI animation and short-form video, made faster with AI and code.',
      items=[('AI video production','ai-video-production'),('Motion design for SaaS','saas-motion-design')],
      proof='<b>Proof:</b> Nepal Bhoomi property films, The 195 Project, a sonic logo'),
 dict(k='grow', label='Grow', badge='Add-on', h='Get found, then get customers.',
      p='Search, AI answers and ads, tracked every month.',
      items=[('SEO','seo-expert-nepal'),('AEO & AI search','aeo-geo-expert'),('Google & Meta ads','google-meta-ads-expert-nepal'),
             ('Growth marketing','growth-marketing-consultant'),('Branding','branding-digital-marketing-nepal')],
      proof='<b>Proof:</b> Nepal Bhoomi SEO and monthly growth reports'),
]

# Who it's for: what I deliver per industry, in each pillar. Listed once, here only.
INDUSTRIES = [
 dict(n='Real estate', tag='Every day · Nepal Bhoomi', slug='real-estate-marketing-nepal',
      build='Listing platforms, admin and lead capture', create='Property films and reels', grow='Lead ads and local SEO'),
 dict(n='E-commerce', tag='Sayapatri, Zylux', slug='full-stack-developer-nepal',
      build='Online stores, Khalti payments, admin dashboards', create='Product videos', grow='Meta ads and product SEO'),
 dict(n='SaaS & tech', tag='Product teams', slug='saas-motion-design',
      build='AI features, dashboards and APIs', create='Explainers and UI animation', grow='AEO and launch campaigns'),
 dict(n='Education', tag='Fitfutures, study abroad', slug='app-developer-nepal',
      build='E-learning and school platforms', create='Explainers and shorts', grow='YouTube SEO'),
 dict(n='Jewellers', tag='Dedicated package', slug='jewellery-marketing-nepal',
      build='Catalogue websites', create='Macro product films and 3D renders', grow='Festive and wedding-season ads'),
 dict(n='Food & travel', tag='EBhojanalaya, The 195 Project', slug='seo-expert-nepal',
      build='Ordering apps', create='Travel films', grow='Local SEO, Google Maps and AEO'),
]

JOBS = [
 dict(co='Nepal Bhoomi', logo='NB', c=CREATE, where='Lazimpat, Kathmandu', title='Platform Developer &amp; Digital Lead', now=1,
      pts=['Co-built the <b>Nepal Bhoomi platform</b>: Next.js API, PostgreSQL, React admin, 2FA, Google sign-in and audit logging.',
           'Built a <b>code-driven video pipeline</b> (Remotion + Python AI: Whisper captions, upscaling, background removal, tracking) for branded property reels.',
           'Run SEO, audience research, ad tracking and <b>monthly growth reports</b>; designed the brand’s <b>sonic logo</b>.']),
 dict(co='Ek Ra Sunya Inc.', ini='ES', c=BUILD, where='Balkumari, Lalitpur', title='Backend Developer',
      pts=['Shipped payments, shipping and currency features on the live <b>Sayapatri e-commerce platform</b>.',
           'Integrated <b>Khalti checkout</b> and <b>MailQuote</b> real-time shipping rates.',
           'Added <b>live exchange rates</b> with USD to AUD base-currency pricing.']),
 dict(co='Uno Technology', ini='UT', c=BUILD, where='Gyaneshwor, Kathmandu', title='Full-Stack Web Developer',
      pts=['Built a <b>Laravel HRMS</b>: JWT auth, OTP password reset by email, attendance check-in/out, tasks, admin and employee roles.',
           'Built <b>Fitfutures</b>, an e-learning and school management platform with progress tracking and reports.',
           'Built <b>First Math</b>, a maths and science game with three levels per subject and live scoring.']),
 dict(co='Freelance', ini='FL', c=CREATE, where='Remote · worldwide', title='Video Producer &amp; Motion Designer',
      pts=['Promotional and explainer videos for <b>schools and study-abroad consultancies</b> on IELTS, GRE, SAT and applications.',
           'Long podcasts and interviews cut into <b>captioned short-form clips</b>.',
           '<b>The 195 Project</b> documentary episodes with Blender 3D scenes, plus an <b>AI-made educational YouTube channel</b>.']),
]
WORK = [
 dict(k='web', name='Nepal Bhoomi', logo='NB', type='Real-estate company · live', desc='Live property platform for houses, land, apartments and commercial space across Kathmandu Valley. I co-built it and run its video and SEO.', stack='Next.js · Video · SEO', live='https://www.nepalbhoomi.com'),
 dict(k='web', name='Nepal Bhoomi Platform', ini='NB', type='Full-stack · co-built', desc='Next.js API with Prisma and PostgreSQL (Supabase), React + Tailwind site and admin. 2FA, Google sign-in, email verification, refresh-token theft detection, rate limiting, audit logs and row-level security across 20+ data models.', stack='Next.js · Prisma · PostgreSQL · React', repo='https://github.com/rookhit/Complete-realestate-project'),
 dict(k='web', name='Slugforge Studio', logo='SF', type='Creative studio · live', desc='Live website for a creative studio offering editing, AI video, motion graphics, branding, web development and digital marketing.', stack='Web design · 3D · Motion', live='https://slugforge.vercel.app'),
 dict(k='web', name='Zylux Commerce Admin', ini='ZX', type='Next.js 15 dashboard', desc='Commerce admin with Clerk sign-in, products, categories, orders and users, TanStack data tables and Recharts sales overview, on Drizzle ORM and Neon Postgres.', stack='Next.js 15 · React 19 · TypeScript', repo='https://github.com/Prajjwalgautam/Zylux-Task'),
 dict(k='web', name='Sayapatri E-commerce', ini='SE', type='Online store · Ek Ra Sunya', desc='E-commerce backend features: Khalti checkout, MailQuote shipping rates and live USD to AUD base-currency pricing.', stack='PHP · Laravel · REST APIs', st='Client project'),
 dict(k='web', name='Laravel HRMS', ini='HR', type='HR platform · Uno Technology', desc='JWT auth, OTP password reset by email, employee records, attendance check-in and check-out, tasks and role-based dashboards.', stack='Laravel · JWT · MySQL', repo='https://github.com/Prajjwalgautam/HRM-system-checkin-checkout'),
 dict(k='web', name='Fitfutures', ini='FF', type='E-learning · Uno Technology', desc='E-learning and school management platform with lessons, resources, progress tracking, admin dashboards and reports.', stack='HTML · CSS · JS · PHP', st='Client project'),
 dict(k='web', name='Role-Based Commerce Admin', ini='RC', type='Admin & user system', desc='Admin and user dashboards with JWT authentication, OTP email password reset, profile management and catalogue CRUD.', stack='PHP · JWT · Bootstrap', repo='https://github.com/Prajjwalgautam/Ecommerce-Admin-User-management-system'),
 dict(k='web', name='EBhojanalaya', ini='EB', type='Food ordering app', desc='Online food ordering: menus, cart and orders with a React front end and a Node.js server.', stack='React · Node.js', repo='https://github.com/Prajjwalgautam/Food-Delivery-system'),
 dict(k='web', name='This Portfolio', ini='PG', type='WebGL · SEO · AEO', desc='9,105 instanced WebGL skill cards that morph on scroll, a 3D text loader, a curved carousel and 14 SEO and AEO service pages.', stack='Three.js · GLSL · Python build', repo='https://github.com/Prajjwalgautam/Portfolio'),
 dict(k='app', name='AI Discipline Coach', ini='DC', type='Android app', desc='Habit and discipline coach for Android, built privacy-first: no internet permission and no data collected. Privacy policy published for Google Play.', stack='Android', priv='https://prajjwalgautam.github.io/discipline-coach-privacy/'),
 dict(k='app', name='Activity Companion', ini='AC', type='Social activity app', desc='Find people for hikes, rides, cafes, sports and events. Matching by activity, interests, area and time, with ID verification and safety tools.', stack='Mobile app', st='In development'),
 dict(k='app', name='First Math', ini='FM', type='Quiz game · Uno Technology', desc='Maths and science game with easy, medium and hard modes for each subject, sign-in and live points.', stack='PHP · JavaScript', repo='https://github.com/Prajjwalgautam/Project--First_Math'),
 dict(k='vid', name='Nepal Bhoomi Films', logo='NB', type='Property video series', desc='Property videos and reels: scripted, edited, graded, captioned for SEO and published, with monthly performance reports.', stack='Remotion · AI video · SEO', live='https://www.nepalbhoomi.com'),
 dict(k='vid', name='Remotion Video Engine', ini='RV', type='Programmatic video system', desc='Videos built from code: Remotion with Python AI tools for Whisper captions, upscaling, background removal and tracking, plus resumable renders.', stack='Remotion · TypeScript · Python', st='Internal tool'),
 dict(k='vid', name='The 195 Project', ini='195', type='Documentary series', desc='Documentary-style country episodes with Blender 3D scenes, edited in Remotion. Episode 11: Turkey, the country in layers.', stack='Blender · Remotion', st='Series'),
 dict(k='vid', name='Nepal Bhoomi Sound', logo='NB', type='Sonic branding & music', desc='A 4–6 second sonic logo on madal, sarangi and bansuri for every video, and an AI-produced Dohori brand song with an animated video in production.', stack='Suno · AI video · Sound design', st='Brand audio'),
 dict(k='vid', name='Slugforge Productions', logo='SF', type='Studio video services', desc='Editing, podcast repurposing, colour grading, AI-assisted video and motion graphics.', stack='Editing · Grading · AI video', live='https://slugforge.vercel.app'),
 dict(k='vid', name='Study-Abroad Content', ini='SA', type='Freelance · education', desc='Explainers on IELTS, GRE, SAT and study-abroad applications, plus podcasts cut into shorts.', stack='Short-form · Motion', st='Freelance'),
]
for w in WORK: w['c1'] = CREATE if w['k'] == 'vid' else BUILD

FAQ = [
 ("What does Prajwal Gautam do?", "Prajwal Gautam is an AI engineer and full-stack developer in Kathmandu, Nepal. He builds AI-powered websites, web apps and mobile apps, and offers launch video, motion design, SEO, AEO and ads as add-ons, so one person can take a product from code to customers."),
 ("Which programming languages and frameworks do you use?", "TypeScript and JavaScript with Next.js, React and Node.js; PHP with Laravel; Python for AI and automation; SQL with PostgreSQL and MySQL; and GLSL for WebGL. On mobile I build Android and web apps. If your project needs a stack I don't use, I'll tell you before we start."),
 ("Can you build an AI-powered website or app for my business?", "Yes. I build with Next.js, React, Node.js, Laravel and PostgreSQL, add AI features such as language-model integrations, assistants and automations, and secure them with proper sign-in, 2FA and audit logs."),
 ("What is AEO and do you offer it?", "AEO, Answer Engine Optimization, makes your business the answer that ChatGPT, Perplexity, Gemini and Google AI Overviews give. Yes: I add structured data, llms.txt, answer-first content and consistent citations, and track AI mentions monthly."),
 ("Do you make motion design and animation for SaaS?", "Yes. I build product explainers, UI animations and launch videos, often in Remotion so they can be re-rendered when your product changes, plus Blender 3D and WebGL."),
 ("Which industries do you work with?", "Real estate (every day at Nepal Bhoomi), e-commerce, SaaS and tech, education, jewellers, and food and travel. The table in the Services section shows what I deliver for each."),
 ("How much does a project cost?", "Every project gets a fixed-price quote after a free 20-minute call. SEO, AEO, ads and content are usually monthly retainers. You always see the price before work starts."),
 ("How do I start a project with you?", "Message me on WhatsApp at +977 984-8137372 or email prajolgautam1234@gmail.com with a short description of your goal. I reply within one working day, Nepal time (UTC+5:45)."),
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
    eng = eng.replace('900 ${fs}px Unbounded, "Arial Black", sans-serif', '600 ${fs}px "Instrument Sans", Arial, sans-serif')
    R("let fs=46; const t=k.s.toUpperCase();", "let fs=52; const t=k.s.toUpperCase();")
    # no heartbeat monitor on the page any more: keep the pulse, skip the drawing
    R("const ecg=$('ecg'), eg=ecg.getContext('2d');", "const ecg=null, eg=null;")
    R("U.uBeat.value=reduce?0:bt; $('bpm').textContent=Math.round(bpm);", "U.uBeat.value=reduce?0:bt; if(!ecg) return;")
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
    eng = eng.replace("#ff2e4d", "#F2334B").replace("hex('#bcc2cb')", "hex('#b9b7b2')").replace("blue=hex('#3d6bff')", "blue=hex('#7B8CFF')").replace("deep=hex('#16205a')", "deep=hex('#2a3170')")
    a = eng.index("function layoutOf(name){"); b = eng.index("/* --- atlas --- */")
    eng = eng[:a] + """function layoutOf(name){
  const m=isMobile(), fx=Math.min(halfW-6.6,6.8);
  if(name==='face') return m?{o:[0,-halfH*.1,0],s:.66}:{o:[halfW*.4,-1.2,0],s:.88};
  if(name==='face2') return m?{o:[0,halfH-8.4,0],s:.8}:{o:[-fx,-.4,0],s:1};
  if(name==='code') return m?{o:[0,halfH*.55,0],s:.5}:{o:[halfW*.48,halfH*.3,0],s:.72};
  if(name==='galaxy') return m?{o:[0,-halfH*.38,0],s:.5}:{o:[halfW*.45,halfH*.18,0],s:.82};
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
    R("if(e.target.closest('a,button,input,textarea,.glass')) return;", "if(e.target.closest('a,button,input,textarea,.glass,.car,.codebox,summary')) return;")
    return eng

# ------------------------------------------------------------------ fragments
def lg(o):
    if o.get('logo'):
        cls = 'light' if o['logo'] == 'NB' else 'dark'; alt = 'Nepal Bhoomi logo' if o['logo'] == 'NB' else 'Slugforge Studio logo'
        return f'<div class="lg {cls}"><img src="{{{{IMG_{o["logo"]}}}}}" alt="{alt}" width="112" height="112" loading="lazy"></div>'
    return f'<div class="lg" style="--c1:{o.get("c1") or o.get("c") or BUILD}"><span>{o["ini"]}</span></div>'

def page_main(svc_link):
    letters = lambda w: ''.join(f'<span class="mc">{ch}</span>' for ch in w)
    mega_html = f'<span class="sr">Prajwal Gautam</span><span class="mega" aria-hidden="true">{letters("Prajwal")} {letters("Gautam")}</span>'
    def pillar(p):
        items = ''.join(f'<li><a href="{svc_link(slug)}">{E(t)}<span aria-hidden="true">↗</span></a></li>' for t, slug in p['items'])
        return (f'<article class="pillar glass {p["k"]} rv"><div class="pillar-top"><span class="label"><i></i>{p["label"]}</span><span class="badge">{p["badge"]}</span></div>'
                f'<h3>{E(p["h"])}</h3><p>{E(p["p"])}</p><ul class="svc-list">{items}</ul><p class="proofline">{p["proof"]}</p></article>')
    pillars = ''.join(pillar(p) for p in PILLARS)
    inds = ''.join(f'<tr><th scope="row"><a href="{svc_link(d["slug"])}">{E(d["n"])}</a><small>{E(d["tag"])}</small></th>'
                   f'<td data-h="Build">{E(d["build"])}</td><td data-h="Create">{E(d["create"])}</td><td data-h="Grow">{E(d["grow"])}</td></tr>' for d in INDUSTRIES)
    def job(j):
        now = '<span class="now">NOW</span>' if j.get('now') else ''
        pts = ''.join(f'<li>{p}</li>' for p in j['pts'])
        return (f'<article class="job glass" style="--c:{j["c"]}"><div class="job-top">{lg(j)}<div><h3>{E(j["co"])}{now}</h3>'
                f'<div class="t">{j["title"]}</div><div class="w">{j["where"]}</div></div></div><ul>{pts}</ul></article>')
    jobs = ''.join(job(j) for j in JOBS)
    panels = []
    for i, w in enumerate(WORK):
        st = '<span class="live-dot">● Live</span>' if w.get('live') else f'<span>{E(w.get("st","Android app" if w.get("priv") else "Code on GitHub"))}</span>'
        link = (f'<a href="{w["live"]}" target="_blank" rel="noopener">Open live ↗</a>' if w.get('live') else
                f'<a href="{w["repo"]}" target="_blank" rel="noopener">GitHub ↗</a>' if w.get('repo') else
                f'<a href="{w["priv"]}" target="_blank" rel="noopener">Privacy policy ↗</a>' if w.get('priv') else '<a href="#contact">Ask me ↗</a>')
        n = f'{i+1:02d}'
        panels.append(f'<article class="panel" data-k="{w["k"]}" style="--c1:{w["c1"]}" aria-label="{E(w["name"])}"><div class="p-top">{st}<span>{n}</span></div>'
                      f'<div class="p-mid">{lg(w)}<h3>{E(w["name"])}</h3><span class="p-type">{E(w["type"])}</span><p class="p-desc">{E(w["desc"])}</p></div>'
                      f'<div class="p-foot"><span class="stk">{E(w["stack"])}</span>{link}</div></article>')
    faq = ''.join(f'<details class="qa"><summary><h3>{E(q)}</h3><span aria-hidden="true">+</span></summary><p>{E(a)}</p></details>' for q, a in FAQ)
    cnt = {k: sum(1 for w in WORK if w['k'] == k) for k in ('web','app','vid')}
    t = open(os.path.join(ROOT, 'templates', 'page.html')).read()
    rep = {'{{MEGA}}': mega_html, '{{PILLARS}}': pillars, '{{INDUSTRIES}}': inds, '{{JOBS}}': jobs, '{{PANELS}}': ''.join(panels), '{{FAQ}}': faq,
           '{{N_ALL}}': str(len(WORK)), '{{N_WEB}}': str(cnt['web']), '{{N_APP}}': str(cnt['app']), '{{N_VID}}': str(cnt['vid']),
           '{{CATS_JSON}}': json.dumps([dict(name=c['name'], word=c['word'], c=c['c'], skills=c['skills']) for c in CATS]),
           '{{ENGINE}}': engine()}
    for k, v in rep.items():
        assert k in t, k; t = t.replace(k, v)
    return t

# ------------------------------------------------------------------ SEO head
DESC = "Prajwal Gautam is an AI engineer and full-stack developer in Kathmandu, Nepal. He builds AI-powered websites, web apps and mobile apps, with launch video, SEO, AEO and ads as add-ons, for real estate, e-commerce, SaaS and jewellery brands worldwide."
TITLE = "Prajwal Gautam – AI Engineer & Full-Stack Developer in Nepal"
KNOWS = sorted({s for c in CATS for s in c['skills']} | {"Artificial intelligence engineering","Answer Engine Optimization (AEO)","Generative Engine Optimization (GEO)","Motion design","SaaS product animation","Real estate marketing","Jewellery marketing","Graphic design","Next.js","TypeScript","PostgreSQL","Remotion","Blender","Full-stack web development","Mobile app development","AI video production","Search engine optimization","Google Ads","Meta Ads","Growth marketing","E-commerce marketing","Branding","Laravel","PHP","Node.js","React","Django","Python","JavaScript","SQL","Three.js","WebGL"})

def person():
    return {"@type":"Person","@id":SITE+"#person","name":"Prajwal Gautam","alternateName":["Prajjwal Gautam"],"url":SITE,
      "image":SITE+"assets/prajwal-gautam.webp","jobTitle":"AI Engineer & Full-Stack Developer","description":DESC,
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
<meta name="theme-color" content="#F3F2EF">
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
:root{--paper:#F3F2EF;--ink:#121316;--ink-2:#2B2D33;--night:#0D0E11;--dim:#5F6168;--accent:#F2334B;--line:rgba(18,19,22,.12);
--sans:"Instrument Sans",system-ui,-apple-system,"Segoe UI",sans-serif;--serif:"Instrument Serif",Georgia,serif;--mono:"Spline Sans Mono",ui-monospace,Menlo,monospace;color-scheme:light}
*{box-sizing:border-box}html{background:var(--paper)}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:17.5px;line-height:1.65;-webkit-font-smoothing:antialiased;padding-left:max(20px,env(safe-area-inset-left,0px));padding-right:max(20px,env(safe-area-inset-right,0px))}
a{color:inherit}:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.wrap{max-width:1160px;margin:0 auto}
.nav{display:flex;justify-content:space-between;align-items:center;gap:16px;padding-block:18px;font-size:14px}
.nav a{text-decoration:none}.nav .brk{display:flex;gap:24px;color:var(--dim)}.nav .brk a:hover{color:var(--ink)}
.pg{font-weight:600;font-size:15px;display:flex;gap:10px;align-items:center}.pg i{width:8px;height:8px;border-radius:50%;background:var(--accent)}
.hire{font-weight:600;padding:9px 16px;border-radius:999px;background:var(--ink);color:var(--paper)}
.crumbs{font-family:var(--mono);font-size:11.5px;color:var(--dim);padding-block:22px 0}.crumbs a{text-decoration:none}.crumbs a:hover{text-decoration:underline}
.paren{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--dim);margin:0 0 10px}
h1,h2,h3{font-weight:500;letter-spacing:-.03em;text-wrap:balance}
h1{margin:10px 0 0;font-size:clamp(42px,6.4vw,92px);line-height:1;letter-spacing:-.04em}
.lede{font-size:clamp(19px,1.7vw,24px);line-height:1.45;max-width:40ch;margin:24px 0 0;color:var(--ink-2)}
.by{font-family:var(--mono);font-size:11px;color:var(--dim);margin-top:22px;text-transform:uppercase;letter-spacing:.06em}
.btns{display:flex;gap:10px;flex-wrap:wrap;margin-top:26px}
.btn{display:inline-flex;gap:8px;align-items:center;padding:12px 20px;border-radius:999px;border:1px solid var(--line);text-decoration:none;font-weight:600;font-size:15px}
.btn:hover{border-color:var(--ink)}
.btn.hot{background:var(--accent);border-color:var(--accent);color:#fff}
section{padding-block:clamp(48px,8vh,88px);border-top:1px solid var(--line)}
section:first-of-type{border-top:0}
.cols{display:grid;grid-template-columns:minmax(0,.75fr) minmax(0,1.25fr);gap:clamp(20px,4vw,64px)}
h2{margin:0;font-size:clamp(30px,3.4vw,48px);line-height:1.08}
.prose p{margin:0 0 16px;max-width:64ch}
.offers{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 28px;border-top:1px solid var(--line)}
.offers div{padding:20px 0;border-bottom:1px solid var(--line)}
.offers h3{margin:0 0 6px;font-size:19px;font-weight:600;letter-spacing:-.015em;line-height:1.25}
.offers p{margin:0;color:var(--ink-2);font-size:16px}
ul.proof{margin:0;padding:0;list-style:none;display:grid;gap:12px}
ul.proof li{padding-left:22px;position:relative;max-width:64ch}ul.proof li::before{content:"↗";position:absolute;left:0;color:var(--accent)}
ol.steps{margin:0;padding:0;list-style:none;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;counter-reset:s}
ol.steps li{border-top:1.5px solid var(--ink);padding-top:14px;counter-increment:s}
ol.steps li::before{content:"0" counter(s);font-family:var(--mono);font-size:11px;color:var(--accent)}
ol.steps h3{margin:8px 0 6px;font-size:18px;font-weight:600;line-height:1.25}
ol.steps p{margin:0;font-size:15px;color:var(--ink-2)}
.chips{display:flex;flex-wrap:wrap;gap:8px}.chips span{font-family:var(--mono);font-size:12.5px;padding:7px 12px;border-radius:999px;border:1px solid var(--line)}
details{border-bottom:1px solid var(--line)}details:first-of-type{border-top:1px solid var(--line)}
summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;gap:16px;align-items:center;padding:18px 2px}
summary::-webkit-details-marker{display:none}summary h3{margin:0;font-size:18.5px;font-weight:500;line-height:1.3}
summary span{font-size:20px;transition:transform .3s;color:var(--dim)}details[open] summary span{transform:rotate(45deg);color:var(--accent)}
details p{margin:0;padding:0 2px 18px;max-width:64ch;color:var(--ink-2)}
.cta{background:var(--night);color:#F1F0ED;border-radius:22px;padding:clamp(28px,5vw,56px);border:0;margin-block:40px}
.cta h2{font-size:clamp(34px,4.4vw,64px);line-height:1.04}.cta h2 span{font-family:var(--serif);font-style:italic;font-weight:400;color:var(--accent)}
.cta .lines{display:grid;gap:4px;margin-top:22px;font-family:var(--mono);font-size:14px;color:#9A9DA6}.cta .btn{border-color:rgba(241,240,237,.25)}.cta .btn:hover{border-color:#F1F0ED}
.rel a{display:grid;grid-template-columns:minmax(0,1fr) 30px;gap:12px;align-items:center;padding:16px 4px;border-bottom:1px solid var(--line);text-decoration:none}
.rel a:first-child{border-top:1px solid var(--line)}
.rel h3{margin:0;font-size:clamp(20px,2vw,28px);line-height:1.15}
.rel a:hover{color:var(--accent)}
footer{padding-block:32px 56px;border-top:1px solid var(--line);font-size:13px;color:var(--dim);display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px}
footer a{text-decoration:none}footer a:hover{color:var(--ink)}
@media (max-width:860px){.cols{grid-template-columns:minmax(0,1fr)}.offers{grid-template-columns:minmax(0,1fr)}ol.steps{grid-template-columns:repeat(2,minmax(0,1fr))}.nav .brk{display:none}}
@media (max-width:480px){ol.steps{grid-template-columns:minmax(0,1fr)}}
"""

def page_service(s, home, svc_link, assets):
    url = f"{SITE}services/{s['slug']}/"
    crumbs = [{"@type":"ListItem","position":1,"name":"Home","item":SITE},{"@type":"ListItem","position":2,"name":"Services","item":SITE+"#services"},{"@type":"ListItem","position":3,"name":s['kw'],"item":url}]
    graph = [
      {"@type":"WebPage","@id":url+"#webpage","url":url,"name":s['title'],"description":s['desc'],"inLanguage":"en","dateModified":TODAY,
       "isPartOf":{"@id":SITE+"#website"},"breadcrumb":{"@id":url+"#crumbs"},"about":{"@id":url+"#service"},"author":{"@id":SITE+"#person"}},
      {"@type":"Service","@id":url+"#service","name":s['kw'],"serviceType":s['short'],"description":s['desc'],"url":url,
       "provider":{"@id":SITE+"#person"},"areaServed":[{"@type":"Country","name":"Nepal"},"Worldwide"],
       "hasOfferCatalog":{"@type":"OfferCatalog","name":s['short'],"itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":n,"description":d}} for n, d in s['offers']]}},
      {"@type":"BreadcrumbList","@id":url+"#crumbs","itemListElement":crumbs},
      {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in s['faq']]},
      {"@type":"Person","@id":SITE+"#person","name":"Prajwal Gautam","url":SITE,"jobTitle":"AI Engineer & Full-Stack Developer",
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&family=Instrument+Serif:ital@0;1&family=Spline+Sans+Mono:wght@400&display=swap">
<script type="application/ld+json">{ld}</script>
<style>{SVC_CSS}</style>
</head>
<body>
<div class="wrap">
<nav class="nav" aria-label="Main"><a class="pg" href="{home}"><i aria-hidden="true"></i>Prajwal Gautam</a><span class="brk"><a href="{home}#services">Services</a><a href="{home}#work">Work</a><a href="{home}#about">About</a></span><a class="hire" href="{home}#contact">Hire me</a></nav>
<nav class="crumbs" aria-label="Breadcrumb"><a href="{home}">Home</a> / <a href="{home}#services">Services</a> / <span aria-current="page">{E(s['kw'])}</span></nav>
<header style="padding-block:30px 60px">
  <p class="paren">(Service) · {E(s['short'])}</p>
  <h1>{E(s['kw'])}</h1>
  <p class="lede">{E(s['lede'])}</p>
  <div class="btns"><a class="btn hot" href="mailto:prajolgautam1234@gmail.com?subject={E(s['kw'])}%20project">Start a project</a><a class="btn" href="https://wa.me/9779848137372" target="_blank" rel="noopener">WhatsApp me</a><a class="btn" href="{home}#work">See my work</a></div>
  <p class="by">By Prajwal Gautam · AI engineer &amp; full-stack developer · Kathmandu, Nepal · Updated November 2026</p>
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
<div class="cta"><p class="paren" style="color:#9A9DA6">Hire me</p><h2>Got a {E(s['short'].lower())} project? <span>Let’s ship it.</span></h2>
<div class="lines"><span>prajolgautam1234@gmail.com</span><span>WhatsApp +977 984-8137372</span><span>Kathmandu, Nepal · UTC+5:45 · replies within one working day</span></div>
<div class="btns"><a class="btn hot" href="https://wa.me/9779848137372" target="_blank" rel="noopener">WhatsApp me</a><a class="btn" href="mailto:prajolgautam1234@gmail.com">Email me</a></div></div>
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
            "## What he does", "- Main role: AI engineer and full-stack developer (websites, web apps, mobile apps, APIs, AI features)",
            "- Add-on: video and motion (AI video production, motion design for SaaS)", "- Add-on: growth (SEO, AEO/GEO, Google and Meta ads, branding)",
            "- Industries: real estate, e-commerce, SaaS and tech, education, jewellers, food and travel", "",
            "## Service pages"] + [f"- [{s['kw']}]({SITE}services/{s['slug']}/): {s['desc']}" for s in SERVICES] + ["",
            "## Experience"] + [f"- {j['co']} ({j['where']}): {html.unescape(j['title'])}. " + ' '.join(re.sub('<[^>]+>', '', p) for p in j['pts']) for j in JOBS] + ["",
            "## Live projects", "- [Nepal Bhoomi](https://www.nepalbhoomi.com): real-estate platform; video, SEO and growth.", "- [Slugforge Studio](https://slugforge.vercel.app): creative studio website and video services.", "",
            "## Languages", "- Code: TypeScript, JavaScript, PHP, Python, SQL, GLSL", "- Frameworks: Next.js, React, Node.js, Laravel, Prisma, Three.js", "- Spoken: English, Nepali, Hindi", "",
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
    a = a.replace('{{HEAD}}', '<title>Prajwal Gautam Portfolio</title>\n<meta name="claude:viewport-fit-sides" content="cover">').replace('{{FACE}}', face)
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
