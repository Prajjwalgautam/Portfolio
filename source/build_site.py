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
from service_pages import SERVICES, BY_SLUG, PROCESS, MONTH
from service_extra import EXTRA
from guides import GUIDES

ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(ROOT)
SITE = "https://prajjwalgautam.com.np/"
E = html.escape
INDEXNOW_KEY = "44e6f923569aa13fd2c6b6e2b24eafb5"
import datetime
TODAY = datetime.date.today().isoformat()

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
ROLES = ["AI engineer","digital marketing expert","lead generation specialist","social media marketer","full-stack developer","Meta & Google ads expert","app developer","SEO & AEO specialist","AI video producer","brand strategist"]
JOBS = [
 dict(co='Nepal Bhoomi', logo='NB', c='#F2334B', where='Lazimpat, Kathmandu', title='Video, Design, Growth &amp; Platform',
      pts=['Built a <b>code-driven video pipeline</b> (Remotion + Python AI: Whisper captions, upscaling, background removal, tracking) for branded <b>property reels</b>.',
           'Co-built the <b>Nepal Bhoomi platform</b>: Next.js API, PostgreSQL, React admin, 2FA, Google sign-in and audit logging.',
           'Own SEO captions, audience research, ad tracking and <b>monthly growth reports</b>; designed the brand’s <b>sonic logo</b>.']),
 dict(co='DigiTech Kathmandu', ini='DT', c1='#F2334B', c2='#3a0812', c='#F2334B', where='Kathmandu', title='Digital Marketing &amp; Client Relationships',
      pts=['Ran marketing across the department: pitched the company’s <b>website, tech and digital marketing services</b> to international clients and managed those relationships.',
           'Led <b>SEO, AEO and GEO</b> research: competitor analysis for each niche, keyword research and tracking with <b>Google Search Console</b> and <b>Google Keyword Planner</b>.',
           'Planned and researched <b>designs and videos</b> for marketing campaigns, analysing audience and context so each campaign had a clear direction.']),
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
 ("What does Prajwal Gautam do?", "Prajwal Gautam is an AI engineer and digital marketing expert based in Kathmandu, Nepal. He builds AI-powered websites and apps, and runs the marketing that brings customers in: lead generation, social media marketing, Facebook, Instagram and Google ads, branding, video and SEO, for businesses in Nepal and worldwide."),
 ("What is AEO and do you offer it?", "AEO, Answer Engine Optimization, makes your business the answer that ChatGPT, Perplexity, Gemini and Google AI Overviews give. Yes: I add structured data, llms.txt, answer-first content and consistent citations, and track AI mentions monthly."),
 ("Which industries do you work with?", "Real estate (I co-built the Nepal Bhoomi platform), education and study-abroad consultancies, e-commerce and retail, restaurants and travel, and I offer dedicated packages for jewellers and SaaS companies."),
 ("Do you make motion design and animation for SaaS?", "Yes. I build product explainers, UI animations and launch videos, often in Remotion so they can be re-rendered when your product changes, plus Blender 3D and WebGL."),
 ("Can you build an AI-powered website or app for my business?", "Yes. I build with Next.js, React, Node.js, Laravel and PostgreSQL, add AI features such as language-model integrations, assistants and automations, and secure them with proper sign-in, 2FA and audit logs."),
 ("Which programming languages and frameworks do you use?", "TypeScript and JavaScript with Next.js, React and Node.js; PHP with Laravel; Python for AI and automation; PostgreSQL, MySQL and NoSQL databases with Supabase for sign-in and Redis for caching; Vercel for hosting and Cloudflare R2 for photos and video; Claude, ChatGPT and OpenRouter for AI automation; and GLSL for WebGL. If your project needs a stack I don't use, I'll tell you before we start."),
 ("Where is Prajwal Gautam based?", "Prajwal Gautam is based in Kathmandu, Nepal (UTC+5:45) and works with clients in Nepal and worldwide, remotely or on-site in the Kathmandu Valley."),
 ("What has Prajwal Gautam built?", "He co-built the Nepal Bhoomi real-estate platform (Next.js, PostgreSQL, two-factor security), built the Slugforge Studio website, shipped Khalti payments and live currency pricing for the Sayapatri e-commerce platform, and built a Laravel HR system and the Fitfutures e-learning platform."),
 ("How much does a project cost?", "Every project gets a fixed-price quote after a free 20-minute call. SEO, AEO, ads and content are usually monthly retainers. You always see the price before work starts."),
 ("How do I start a project with you?", "Email prajolgautam1234@gmail.com or message me on WhatsApp at +977 984-8137372 with a short description of your goal. I reply within one working day, Nepal time (UTC+5:45)."),
]
SLASH = [('AI Engineering','ai-engineer-nepal'),('Digital Marketing &amp; Leads','digital-marketing-expert-nepal'),('Social Media &amp; Ads','social-media-marketing-nepal'),('Full-Stack &amp; Apps','full-stack-developer-nepal'),('SEO, AEO &amp; AI Video','aeo-geo-expert')]
INDUSTRIES = [
 dict(n='Real Estate', tag='Proven · Nepal Bhoomi', line='Property reels, listing platforms and lead ads that sell land and homes.', chips=['Property reels','Listing sites','Lead ads','Sonic branding'], slug='real-estate-marketing-nepal'),
 dict(n='Jewellers', tag='Package for jewellers', line='Macro product films, 3D renders, graphics and wedding-season campaigns that make every piece shine.', chips=['Macro video','3D renders','Catalogues','Festive ads'], slug='jewellery-marketing-nepal'),
 dict(n='SaaS &amp; Tech', tag='Remotion · Blender · WebGL', line='Explainers, UI motion and launch videos, built from code so every product update re-renders.', chips=['Explainers','UI animation','Launch videos','3D & WebGL'], slug='saas-motion-design'),
 dict(n='E-commerce', tag='Proven · Sayapatri, Zylux', line='Stores, payments, admin dashboards and the ads and SEO that fill the cart.', chips=['Online stores','Khalti','Dashboards','Meta ads'], slug='growth-marketing-consultant'),
 dict(n='Education', tag='Proven · Fitfutures, freelance', line='E-learning platforms and study-abroad explainers that students and parents trust.', chips=['E-learning','Explainers','Shorts','YouTube SEO'], slug='ai-video-production'),
 dict(n='Food &amp; Travel', tag='Proven · EBhojanalaya, The 195 Project', line='Ordering systems, food and travel reels, and local SEO and AEO for Maps and AI search.', chips=['Ordering apps','Travel films','Local SEO','AEO'], slug='seo-expert-nepal'),
]

# Home page FAQ: the questions business owners ask first, then the ones search engines and AI assistants ask about me.
FAQ_BIZ = [
 ("Are you an agency or one person?", "One person covering what an agency covers: strategy, content, social media, ads, SEO and reporting, plus the website or app. You always talk to the person doing the work."),
 ("How much does it cost?", "Marketing is a monthly retainer; websites and apps are a fixed price per project. You get a written quote after a free 20-minute call, before anything starts. Ad spend is paid directly to Meta or Google."),
 ("How soon will I see results?", "Ads can bring enquiries within days. Social media growth and SEO build over two to six months. The first month is mostly setup and testing."),
 ("Do you guarantee leads or sales?", "No honest marketer can. I guarantee a clear plan, steady work and an honest monthly report, and I move budget to what is working."),
 ("Do you work with businesses outside Nepal?", "Yes. I work remotely with clients worldwide, with good time overlap for Asia, the Middle East, Europe and Australia."),
]
FAQ_HOME = FAQ_BIZ + [qa for qa in FAQ if qa[0] in ("What does Prajwal Gautam do?", "Where is Prajwal Gautam based?", "What has Prajwal Gautam built?",
                                                    "What is AEO and do you offer it?", "Which industries do you work with?", "Which programming languages and frameworks do you use?")]
# Real figures only. Leave empty and the Results section stays hidden.
# stats: (value, label, note); quotes: (quote, 'Name · Business, City'). Real client figures and words only.
RESULTS = dict(stats=[], quotes=[])
HOME_WORK = ['Nepal Bhoomi', 'Nepal Bhoomi Platform', 'Slugforge Studio', 'This Portfolio', 'Zylux Commerce Admin', 'Laravel HRMS']

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

# ------------------------------------------------------------------ SEO head
DESC = "AI engineer and digital marketing expert in Kathmandu, Nepal. AI-powered websites and apps, plus lead generation, social media, Google and Meta ads and SEO."
TITLE = "Prajwal Gautam – AI Engineer & Digital Marketing Expert, Nepal"
KNOWS = sorted({s for c in CATS for s in c['skills']} | {"Supabase","Vercel","Cloudflare R2","Redis","MySQL","PostgreSQL","Python","OpenRouter","AI automation","Lead generation","Social media marketing","Client relationship management","Artificial intelligence engineering","Answer Engine Optimization (AEO)","Generative Engine Optimization (GEO)","Motion design","SaaS product animation","Real estate marketing","Jewellery marketing","Graphic design","Next.js","TypeScript","PostgreSQL","Remotion","Blender","Full-stack web development","Mobile app development","AI video production","Search engine optimization","Google Ads","Meta Ads","Growth marketing","E-commerce marketing","Branding","Laravel","PHP","Node.js","React","Django","Python","JavaScript","SQL","Three.js","WebGL"})

def person():
    return {"@type":"Person","@id":SITE+"#person","name":"Prajwal Gautam","alternateName":["Prajjwal Gautam"],"url":SITE,
      "image":SITE+"assets/prajwal-gautam.webp","jobTitle":"AI Engineer & Digital Marketing Expert","description":DESC,
      "disambiguatingDescription":"Kathmandu-based AI engineer, full-stack developer and digital marketing expert (portfolio: prajjwalgautam.com.np) who co-built the Nepal Bhoomi real-estate platform and built the Slugforge Studio website; also known as Prajjwal Gautam.",
      "email":"mailto:prajolgautam1234@gmail.com","telephone":"+977-9848137372",
      "address":{"@type":"PostalAddress","addressLocality":"Kathmandu","addressRegion":"Bagmati","addressCountry":"NP"},
      "alumniOf":[{"@type":"CollegeOrUniversity","name":"New Summit College, Tribhuvan University"},{"@type":"EducationalOrganization","name":"Kathmandu Model College"}],
      "knowsAbout":KNOWS,"knowsLanguage":["English","Nepali","Hindi"],
      "sameAs":["https://www.linkedin.com/in/prajjwal-gautam/","https://github.com/Prajjwalgautam"]}

def head_main():
    graph = [
      {"@type":"ProfilePage","@id":SITE+"#profile","url":SITE,"name":TITLE,"dateModified":TODAY,"mainEntity":{"@id":SITE+"#person"},"inLanguage":"en"},
      person(),
      {"@type":"ProfessionalService","@id":SITE+"#service","name":"Prajwal Gautam – Digital Marketing, AI & Development Services","logo":SITE+"assets/brand/icon-512.png","url":SITE,"image":SITE+"assets/og-image.jpg",
       "description":DESC,"founder":{"@id":SITE+"#person"},"telephone":"+977-9848137372","email":"prajolgautam1234@gmail.com",
       "address":{"@type":"PostalAddress","addressLocality":"Kathmandu","addressCountry":"NP"},"areaServed":["Nepal","Worldwide"],
       "hasOfferCatalog":{"@type":"OfferCatalog","name":"Services","itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":s['kw'],"url":f"{SITE}services/{s['slug']}/","description":s['desc']}} for s in SERVICES]}},
      {"@type":"WebSite","@id":SITE+"#website","url":SITE,"name":"Prajwal Gautam","inLanguage":"en","publisher":{"@id":SITE+"#person"}},
      {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in FAQ_HOME]},
      {"@type":"ItemList","name":"Projects by Prajwal Gautam","itemListElement":[{"@type":"ListItem","position":i+1,"item":{"@type":"CreativeWork","name":w["name"],"description":w["desc"],"creator":{"@id":SITE+"#person"},**({"url":w.get("live") or w.get("repo")} if (w.get("live") or w.get("repo")) else {})}} for i, w in enumerate([w for w in WORK if w["name"] in HOME_WORK])]},
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
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="assets/brand/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/brand/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
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
    x = EXTRA.get(s['slug'], {})
    s = dict(s, faq=list(s['faq']) + list(x.get('faq', [])))
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
      {"@type":"Person","@id":SITE+"#person","name":"Prajwal Gautam","url":SITE,"jobTitle":"AI Engineer & Digital Marketing Expert",
       "sameAs":["https://www.linkedin.com/in/prajjwal-gautam/","https://github.com/Prajjwalgautam"]},
    ]
    ld = json.dumps({"@context":"https://schema.org","@graph":graph}, ensure_ascii=False)
    offers = ''.join(f'<div><h3>{E(n)}</h3><p>{E(d)}</p></div>' for n, d in s['offers'])
    proof = ''.join(f'<li>{E(p)}</li>' for p in s['proof'])
    steps = ''.join(f'<li><h3>{E(a)}</h3><p>{E(b)}</p></li>' for a, b in PROCESS)
    tools = ''.join(f'<span>{E(t)}</span>' for t in s['tools'])
    faq = ''.join(f'<details><summary><h3>{E(q)}</h3><span aria-hidden="true">+</span></summary><p>{E(a)}</p></details>' for q, a in s['faq'])
    rel = ''.join(f'<a href="{svc_link(r, True)}"><h3>{E(BY_SLUG[r]["kw"])}</h3><span aria-hidden="true">↗</span></a>' for r in s['related'])
    who = (f'<section><h2 style="margin-bottom:26px">Who this is for</h2><div class="offers">'
           + ''.join(f'<div><h3>{E(a)}</h3><p>{E(b)}</p></div>' for a, b in x['who']) + '</div></section>') if x.get('who') else ''
    why = (f'<section class="cols"><h2>Why work with me</h2><ul class="proof">' + ''.join(f'<li>{E(w)}</li>' for w in x['why']) + '</ul></section>') if x.get('why') else ''
    tl = (f'<section class="cols"><h2>How long does it take?</h2><div><div class="offers" style="grid-template-columns:minmax(0,1fr)">'
          + ''.join(f'<div style="display:flex;justify-content:space-between;gap:16px"><h3 style="margin:0">{E(a)}</h3><p style="white-space:nowrap">{E(b)}</p></div>' for a, b in x['timeline'])
          + '</div><p style="color:var(--dim);font-size:15px;margin-top:14px">Typical ranges. Your quote gives exact dates.</p></div></section>') if x.get('timeline') else ''
    gs = [g for g in GUIDES if s['slug'] in g['related']]
    gl = ('<section><p class="paren">(Guides)</p><div class="rel">' + ''.join(f'<a href="{home}guides/{g["slug"]}/"><h3>{E(g["h1"])}</h3><span aria-hidden="true">↗</span></a>' for g in gs) + '</div></section>') if gs else ''
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
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="{assets}brand/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{assets}brand/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sofia+Sans+Extra+Condensed:wght@900&family=Sofia+Sans+Condensed:wght@700;800&family=Sofia+Sans:wght@400;500;600&family=Spline+Sans+Mono:wght@400&display=swap">
<script type="application/ld+json">{ld}</script>
<style>{SVC_CSS}</style>
<script>/* always open a service page at the top */if(!location.hash){{try{{history.scrollRestoration="manual"}}catch(e){{}}scrollTo(0,0);addEventListener("DOMContentLoaded",()=>scrollTo(0,0));addEventListener("load",()=>scrollTo(0,0));addEventListener("pageshow",()=>scrollTo(0,0))}}</script>
</head>
<body>
<div class="wrap">
<nav class="nav" aria-label="Main"><a href="{home}" style="text-decoration:none"><span style="display:inline-flex;align-items:center;gap:10px"><img src="{assets}brand/logo.svg" alt="" width="28" height="28" style="border-radius:7px">Prajwal Gautam</span></a><span class="brk"><a href="{home}#services">Services</a><a href="{home}#work">Work</a><a href="{home}#about">About</a></span><a href="{home}#contact" style="text-decoration:underline">Contact ↗</a></nav>
<nav class="crumbs" aria-label="Breadcrumb"><a href="{home}">Home</a> / <a href="{home}#find">Services</a> / <span aria-current="page">{E(s['kw'])}</span></nav>
<header style="padding-block:30px 60px">
  <p class="paren">(Service) · {E(s['short'])}</p>
  <h1>{E(s['kw'])}</h1>
  <p class="lede">{E(s['lede'])}</p>
  <div class="btns"><a class="btn hot" href="mailto:prajolgautam1234@gmail.com?subject={E(s['kw'])}%20project">Start a project</a><a class="btn" href="https://wa.me/9779848137372" target="_blank" rel="noopener">WhatsApp me</a><a class="btn" href="{home}#work">See my work</a></div>
  <p class="by">By Prajwal Gautam · AI Engineer &amp; Digital Marketing Expert · Kathmandu, Nepal · Updated {MONTH}</p>
</header>
<main>
<section class="cols"><p class="paren">(Overview)</p><div class="prose">{''.join(f'<p>{E(p)}</p>' for p in s['intro'])}</div></section>
<section class="cols"><h2>{E(s['what_h'])}</h2><div class="prose">{''.join(f'<p>{E(p)}</p>' for p in s['what'])}</div></section>
<section><h2 style="margin-bottom:26px">{E(s['short'])} services</h2><div class="offers">{offers}</div></section>
{who}
<section class="cols"><h2>Proof from real work</h2><div><ul class="proof">{proof}</ul><div class="btns"><a class="btn hot" href="{home}work/nepal-bhoomi/">Read the Nepal Bhoomi case study</a><a class="btn" href="https://www.nepalbhoomi.com" target="_blank" rel="noopener">nepalbhoomi.com ↗</a><a class="btn" href="https://slugforge.vercel.app" target="_blank" rel="noopener">Slugforge Studio ↗</a></div></div></section>
{why}
<section><h2 style="margin-bottom:26px">How we work together</h2><ol class="steps">{steps}</ol></section>
{tl}
<section class="cols"><h2>Tools &amp; languages</h2><div class="chips">{tools}</div></section>
<section class="cols"><h2>How much does it cost?</h2><div class="prose">{''.join(f'<p>{E(p)}</p>' for p in s['cost'])}</div></section>
<section class="cols"><h2>Frequently asked questions</h2><div>{faq}</div></section>
<div class="cta"><p class="paren" style="color:#8d919b">(Contact)</p><h2>Let’s talk about your <span>{E(s['short'].lower())}</span> project.</h2>
<div class="lines"><span>prajolgautam1234@gmail.com</span><span>WhatsApp +977 984-8137372</span><span>Kathmandu, Nepal · UTC+5:45 · replies within one working day</span></div>
<div class="btns"><a class="btn hot" href="mailto:prajolgautam1234@gmail.com">Email me</a><a class="btn" href="https://wa.me/9779848137372" target="_blank" rel="noopener">WhatsApp ↗</a><a class="btn" href="https://www.linkedin.com/in/prajjwal-gautam/" target="_blank" rel="noopener">LinkedIn ↗</a></div></div>
<section><p class="paren">(Related services)</p><div class="rel">{rel}</div></section>
{gl}
</main>
<footer><span>© 2026 Prajwal Gautam · Kathmandu, Nepal</span><span><a href="{home}">Home</a> · {' · '.join(f'<a href="{svc_link(x["slug"], True)}">{E(x["short"])}</a>' for x in SERVICES)}</span></footer>
</div>
</body>
</html>
"""


# ------------------------------------------------------------------ case study
CASE = dict(
  slug='nepal-bhoomi',
  title='Nepal Bhoomi Case Study – Real-Estate Platform, Video & SEO | Prajwal Gautam',
  desc='How Prajwal Gautam co-built the Nepal Bhoomi real-estate platform in Next.js and PostgreSQL, built a code-driven video pipeline, and runs its SEO and growth reporting.',
  h1='Nepal Bhoomi case study',
  summary='Nepal Bhoomi is a real-estate company in Lazimpat, Kathmandu that sells and rents houses, land, apartments and commercial property across Kathmandu, Lalitpur and Bhaktapur. I co-built its web platform, built the system that produces its property videos, and run its SEO, audience research and monthly growth reports.',
  facts=[('Client','Nepal Bhoomi'),('Industry','Real estate'),('Location','Lazimpat, Kathmandu, Nepal'),('My role','Platform developer and digital lead'),
         ('Stack','Next.js, Prisma, PostgreSQL (Supabase), React, Tailwind, Remotion, Python'),('Live site','nepalbhoomi.com')],
  needs=['A property brand lives or dies on three things: a fast, trustworthy place to show listings, a steady flow of video that makes people stop scrolling, and being found when someone searches for land or a house in the Valley.',
         'Nepal Bhoomi needed all three from a small team, so the work had to be built once and reused every day rather than redone by hand.'],
  blocks=[
    ('The platform', 'co-built with the Nepal Bhoomi team', [
      'A Next.js API with Prisma and PostgreSQL on Supabase, and a React and Tailwind front end and admin panel, across more than 20 data models for properties, enquiries, users and content.',
      'Security built for real customer data: two-factor sign-in, Google sign-in, email verification, refresh-token rotation that detects stolen tokens, account lockout, rate limiting, an audit log and row-level security in the database.',
      'An admin where the team adds and updates listings and handles enquiries without touching code.']),
    ('The video system', 'built and run by me', [
      'Property videos are assembled in code with Remotion, so a new reel reuses the brand’s titles, captions, colours and sound instead of starting from a blank timeline.',
      'Python AI tools handle the slow parts: Whisper for captions, upscaling, background removal and motion tracking, with renders that resume if a long job stops.',
      'A 4–6 second sonic logo on madal, sarangi and bansuri opens and closes every video, so the brand is recognisable by ear.']),
    ('Search and growth', 'run by me', [
      'Video titles, captions and descriptions written for search, so each upload also works as a landing page on YouTube, Facebook and Google.',
      'Audience and market research to decide which areas, property types and price points to film and promote next.',
      'Ad and content tracking rolled into a monthly growth report the owner can read in five minutes.']),
  ],
  learn=['Build the system before the content. Once the platform and the video pipeline existed, every new property cost minutes, not days.',
         'Security is a feature in real estate. Buyers and sellers share phone numbers and documents, so the platform was secured like a finance app from day one.',
         'One person owning code, video and search removes the hand-offs where most small-brand marketing stalls.'],
  faq=[('What did Prajwal Gautam build for Nepal Bhoomi?','He co-built the Nepal Bhoomi web platform (Next.js, Prisma, PostgreSQL on Supabase, React admin), built its code-driven video pipeline with Remotion and Python AI tools, and runs its SEO, audience research and monthly growth reports.'),
       ('Can you build the same for my real-estate business?','Yes. The same approach works for any agency or developer: a listing platform with an admin and lead capture, a video system for property reels, and search and ads tracked monthly. Start with a free 20-minute call.'),
       ('Is Nepal Bhoomi a live website?','Yes. Nepal Bhoomi is live at nepalbhoomi.com and lists houses, land, apartments and commercial property across Kathmandu, Lalitpur and Bhaktapur.')],
  related=['real-estate-marketing-nepal','full-stack-developer-nepal','ai-video-production','seo-expert-nepal'],
)

def page_case(c, home, svc_link, assets):
    url = f"{SITE}work/{c['slug']}/"
    crumbs = [{"@type":"ListItem","position":1,"name":"Home","item":SITE},{"@type":"ListItem","position":2,"name":"Work","item":SITE+"#work"},{"@type":"ListItem","position":3,"name":"Nepal Bhoomi case study","item":url}]
    graph = [
      {"@type":"Article","@id":url+"#article","headline":c['h1'],"description":c['desc'],"url":url,"inLanguage":"en","datePublished":"2026-11-10","dateModified":TODAY,
       "author":{"@id":SITE+"#person"},"publisher":{"@id":SITE+"#person"},"image":SITE+"assets/og-image.jpg","mainEntityOfPage":url,
       "about":{"@type":"Organization","name":"Nepal Bhoomi","url":"https://www.nepalbhoomi.com","address":{"@type":"PostalAddress","addressLocality":"Kathmandu","addressCountry":"NP"}}},
      {"@type":"BreadcrumbList","@id":url+"#crumbs","itemListElement":crumbs},
      {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in c['faq']]},
      {"@type":"Person","@id":SITE+"#person","name":"Prajwal Gautam","url":SITE,"jobTitle":"AI Engineer & Digital Marketing Expert",
       "sameAs":["https://www.linkedin.com/in/prajjwal-gautam/","https://github.com/Prajjwalgautam"]},
    ]
    ld = json.dumps({"@context":"https://schema.org","@graph":graph}, ensure_ascii=False)
    facts = ''.join(f'<div><h3>{E(k)}</h3><p>{E(v)}</p></div>' for k, v in c['facts'])
    blocks = ''.join(f'<section class="cols"><div><h2>{E(h)}</h2><p class="paren" style="margin-top:10px">{E(sub)}</p></div><ul class="proof">{"".join(f"<li>{E(p)}</li>" for p in pts)}</ul></section>' for h, sub, pts in c['blocks'])
    faq = ''.join(f'<details><summary><h3>{E(q)}</h3><span aria-hidden="true">+</span></summary><p>{E(a)}</p></details>' for q, a in c['faq'])
    rel = ''.join(f'<a href="{svc_link(r, True)}"><h3>{E(BY_SLUG[r]["kw"])}</h3><span aria-hidden="true">↗</span></a>' for r in c['related'])
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(c['title'])}</title>
<meta name="description" content="{E(c['desc'])}">
<meta name="author" content="Prajwal Gautam">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:site_name" content="Prajwal Gautam">
<meta property="og:title" content="{E(c['title'])}"><meta property="og:description" content="{E(c['desc'])}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}assets/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="NP-BA"><meta name="geo.placename" content="Kathmandu">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="{assets}brand/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{assets}brand/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sofia+Sans+Extra+Condensed:wght@900&family=Sofia+Sans+Condensed:wght@700;800&family=Sofia+Sans:wght@400;500;600&family=Spline+Sans+Mono:wght@400&display=swap">
<script type="application/ld+json">{ld}</script>
<style>{SVC_CSS}</style>
<script>if(!location.hash){{try{{history.scrollRestoration="manual"}}catch(e){{}}scrollTo(0,0);addEventListener("load",()=>scrollTo(0,0));addEventListener("pageshow",()=>scrollTo(0,0))}}</script>
</head>
<body>
<div class="wrap">
<nav class="nav" aria-label="Main"><a href="{home}" style="text-decoration:none"><span style="display:inline-flex;align-items:center;gap:10px"><img src="{assets}brand/logo.svg" alt="" width="28" height="28" style="border-radius:7px">Prajwal Gautam</span></a><span class="brk"><a href="{home}#services">Services</a><a href="{home}#work">Work</a><a href="{home}#about">About</a></span><a href="{home}#contact" style="text-decoration:underline">Contact ↗</a></nav>
<nav class="crumbs" aria-label="Breadcrumb"><a href="{home}">Home</a> / <a href="{home}#work">Work</a> / <span aria-current="page">Nepal Bhoomi</span></nav>
<header style="padding-block:30px 60px">
  <p class="paren">(Case study) · Real estate</p>
  <h1>{E(c['h1'])}</h1>
  <p class="lede">{E(c['summary'])}</p>
  <div class="btns"><a class="btn hot" href="https://www.nepalbhoomi.com" target="_blank" rel="noopener">Visit nepalbhoomi.com ↗</a><a class="btn" href="https://wa.me/9779848137372" target="_blank" rel="noopener">WhatsApp me</a><a class="btn" href="{home}#work">More work</a></div>
  <p class="by">By Prajwal Gautam · Kathmandu, Nepal · Updated {MONTH}</p>
</header>
<main>
<section><h2 style="margin-bottom:26px">At a glance</h2><div class="offers">{facts}</div></section>
<section class="cols"><h2>What the brand needed</h2><div class="prose">{''.join(f'<p>{E(p)}</p>' for p in c['needs'])}</div></section>
{blocks}
<section class="cols"><h2>What it shows</h2><ul class="proof">{''.join(f'<li>{E(p)}</li>' for p in c['learn'])}</ul></section>
<section class="cols"><h2>Frequently asked questions</h2><div>{faq}</div></section>
<div class="cta"><p class="paren" style="color:#8d919b">(Contact)</p><h2>Want this for your <span>business</span>?</h2>
<div class="lines"><span>prajolgautam1234@gmail.com</span><span>WhatsApp +977 984-8137372</span><span>Kathmandu, Nepal · UTC+5:45 · replies within one working day</span></div>
<div class="btns"><a class="btn hot" href="mailto:prajolgautam1234@gmail.com?subject=Project%20like%20Nepal%20Bhoomi">Email me</a><a class="btn" href="https://wa.me/9779848137372" target="_blank" rel="noopener">WhatsApp ↗</a></div></div>
<section><p class="paren">(Related services)</p><div class="rel">{rel}</div></section>
</main>
<footer><span>© 2026 Prajwal Gautam · Kathmandu, Nepal</span><span><a href="{home}">Home</a> · {' · '.join(f'<a href="{svc_link(x["slug"], True)}">{E(x["short"])}</a>' for x in SERVICES)}</span></footer>
</div>
</body>
</html>
"""

# ------------------------------------------------------------------ guides
def _head(title, desc, url, assets, ld, kind='article'):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="author" content="Prajwal Gautam">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{kind}"><meta property="og:site_name" content="Prajwal Gautam">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}assets/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="NP-BA"><meta name="geo.placename" content="Kathmandu">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="{assets}brand/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{assets}brand/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sofia+Sans+Extra+Condensed:wght@900&family=Sofia+Sans+Condensed:wght@700;800&family=Sofia+Sans:wght@400;500;600&family=Spline+Sans+Mono:wght@400&display=swap">
<script type="application/ld+json">{ld}</script>
<style>{SVC_CSS}{GUIDE_CSS}</style>
<script>if(!location.hash){{try{{history.scrollRestoration="manual"}}catch(e){{}}scrollTo(0,0);addEventListener("load",()=>scrollTo(0,0));addEventListener("pageshow",()=>scrollTo(0,0))}}</script>
</head>
<body>
<div class="wrap">
<nav class="nav" aria-label="Main"><a href="../../" style="text-decoration:none"><span style="display:inline-flex;align-items:center;gap:10px"><img src="{assets}brand/logo.svg" alt="" width="28" height="28" style="border-radius:7px">Prajwal Gautam</span></a><span class="brk"><a href="../../#services">Services</a><a href="../../#work">Work</a><a href="../../guides/">Guides</a></span><a href="../../#contact" style="text-decoration:underline">Contact ↗</a></nav>
"""

GUIDE_CSS = """
.answer{border-left:4px solid var(--accent);background:#fff;padding:20px 24px;border-radius:0 14px 14px 0;font-size:clamp(19px,1.6vw,23px);line-height:1.45;max-width:62ch;margin:26px 0 0;font-weight:500}
.answer b{display:block;font-family:var(--mono);font-size:12px;font-weight:400;letter-spacing:.06em;text-transform:uppercase;color:var(--dim);margin-bottom:8px}
h1.g{font-size:clamp(46px,7vw,112px)}
table.cmp{border-collapse:collapse;width:100%;font-size:16px;margin-top:6px}
table.cmp th,table.cmp td{text-align:left;padding:12px 12px 12px 0;border-bottom:1px solid var(--line);vertical-align:top}
table.cmp th{font-family:var(--mono);font-size:12px;font-weight:400;text-transform:uppercase;color:var(--dim)}
ol.check{margin:0;padding:0 0 0 24px;display:grid;gap:10px;max-width:64ch}ol.check li::marker{color:var(--accent);font-family:var(--mono)}
.glist a{display:grid;grid-template-columns:minmax(0,1fr) 30px;gap:12px;align-items:center;padding:22px 4px;border-bottom:1px solid var(--line);text-decoration:none}
.glist a:first-child{border-top:1px solid var(--line)}.glist h2{font-size:clamp(30px,3.6vw,56px)}.glist p{margin:8px 0 0;color:#34363c;max-width:70ch}
.glist a:hover h2{color:var(--accent)}
"""

def _faq_html(faq):
    return ''.join(f'<details><summary><h3>{E(q)}</h3><span aria-hidden="true">+</span></summary><p>{E(a)}</p></details>' for q, a in faq)

def _cmp(rows, head=('Term','Stands for','Goal')):
    return ('<table class="cmp"><thead><tr>' + ''.join(f'<th>{E(x)}</th>' for x in head) + '</tr></thead><tbody>'
            + ''.join(f'<tr><td><b>{E(a)}</b></td><td>{E(b)}</td><td>{E(c)}</td></tr>' for a, b, c in rows) + '</tbody></table>')

def page_guide(g):
    url = f"{SITE}guides/{g['slug']}/"
    crumbs = [{"@type":"ListItem","position":1,"name":"Home","item":SITE},{"@type":"ListItem","position":2,"name":"Guides","item":SITE+"guides/"},{"@type":"ListItem","position":3,"name":g['h1'],"item":url}]
    graph = [
      {"@type":"Article","@id":url+"#article","headline":g['h1'],"description":g['desc'],"abstract":g['answer'],"url":url,"inLanguage":"en",
       "datePublished":"2026-11-10","dateModified":TODAY,"author":{"@id":SITE+"#person"},"publisher":{"@id":SITE+"#person"},
       "image":SITE+"assets/og-image.jpg","mainEntityOfPage":url,"isPartOf":{"@id":SITE+"#website"},
       "speakable":{"@type":"SpeakableSpecification","cssSelector":[".answer"]}},
      {"@type":"BreadcrumbList","@id":url+"#crumbs","itemListElement":crumbs},
      {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in [(g['h1'], g['answer'])] + g['faq']]},
      {"@type":"Person","@id":SITE+"#person","name":"Prajwal Gautam","url":SITE,"jobTitle":"AI Engineer & Digital Marketing Expert",
       "address":{"@type":"PostalAddress","addressLocality":"Kathmandu","addressCountry":"NP"},
       "sameAs":["https://www.linkedin.com/in/prajjwal-gautam/","https://github.com/Prajjwalgautam"]},
    ]
    ld = json.dumps({"@context":"https://schema.org","@graph":graph}, ensure_ascii=False)
    body = ''
    secs = list(g['sections']) + list(g.get('extra', []))
    for i, (h, paras, table) in enumerate(secs):
        inner = ''.join(f'<p>{E(p)}</p>' for p in paras)
        if table: inner += _cmp(table, g.get('thead', ('Term','Stands for','Goal')))
        if not paras and not table:   # checklist section
            inner = '<ol class="check">' + ''.join(f'<li>{E(c)}</li>' for c in g['checklist']) + '</ol>'
        body += f'<section class="cols"><h2>{E(h)}</h2><div class="prose">{inner}</div></section>'
    rel = ''.join(f'<a href="../../services/{r}/"><h3>{E(BY_SLUG[r]["kw"])}</h3><span aria-hidden="true">↗</span></a>' for r in g['related'])
    more = ''.join(f'<a href="../{o["slug"]}/"><h3>{E(o["h1"])}</h3><span aria-hidden="true">↗</span></a>' for o in GUIDES if o is not g)
    return _head(g['title'], g['desc'], url, '../../assets/', ld) + f"""<nav class="crumbs" aria-label="Breadcrumb"><a href="../../">Home</a> / <a href="../">Guides</a> / <span aria-current="page">{E(g['h1'])}</span></nav>
<header style="padding-block:30px 50px">
  <p class="paren">(Guide)</p>
  <h1 class="g">{E(g['h1'])}</h1>
  <p class="answer"><b>Short answer</b>{E(g['answer'])}</p>
  <p class="by">By Prajwal Gautam · AI engineer and digital marketing expert, Kathmandu · Updated {MONTH}</p>
</header>
<main>
{body}
<section class="cols"><h2>Frequently asked questions</h2><div>{_faq_html(g['faq'])}</div></section>
<div class="cta"><p class="paren" style="color:#8d919b">(Need a hand?)</p><h2>Want this done <span>for you</span>?</h2>
<div class="lines"><span>prajolgautam1234@gmail.com</span><span>WhatsApp +977 984-8137372</span><span>Kathmandu, Nepal · UTC+5:45 · replies within one working day</span></div>
<div class="btns"><a class="btn hot" href="mailto:prajolgautam1234@gmail.com">Email me</a><a class="btn" href="https://wa.me/9779848137372" target="_blank" rel="noopener">WhatsApp ↗</a></div></div>
<section><p class="paren">(Related services)</p><div class="rel">{rel}</div></section>
<section><p class="paren">(More guides)</p><div class="rel">{more}</div></section>
</main>
<footer><span>© 2026 Prajwal Gautam · Kathmandu, Nepal</span><span><a href="../../">Home</a> · <a href="../">Guides</a> · <a href="../../work/nepal-bhoomi/">Nepal Bhoomi case study</a></span></footer>
</div>
</body>
</html>
"""

def page_guides_index():
    url = f"{SITE}guides/"
    graph = [
      {"@type":"CollectionPage","@id":url+"#page","url":url,"name":"Guides by Prajwal Gautam","inLanguage":"en","dateModified":TODAY,"author":{"@id":SITE+"#person"},
       "hasPart":[{"@type":"Article","headline":g['h1'],"url":f"{url}{g['slug']}/"} for g in GUIDES]},
      {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":SITE},{"@type":"ListItem","position":2,"name":"Guides","item":url}]},
    ]
    ld = json.dumps({"@context":"https://schema.org","@graph":graph}, ensure_ascii=False)
    items = ''.join(f'<a href="{g["slug"]}/"><div><h2>{E(g["h1"])}</h2><p>{E(g["answer"])}</p></div><span aria-hidden="true">↗</span></a>' for g in GUIDES)
    desc = 'Plain-English guides on SEO, AEO, GEO, AI engineering, web development and real-estate marketing in Nepal, written from real projects in Kathmandu.'
    h = _head('Guides: SEO, AEO, AI & Web Development in Nepal | Prajwal Gautam', desc, url, '../assets/', ld, 'website')
    h = h.replace('href="../../', 'href="../').replace('href="../guides/"', 'href="./"')
    return h + f"""<nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a> / <span aria-current="page">Guides</span></nav>
<header style="padding-block:30px 50px">
  <p class="paren">(Guides)</p>
  <h1 class="g">Guides</h1>
  <p class="lede">Straight answers to questions businesses in Nepal ask about search, AI and websites, written from real projects.</p>
</header>
<main><section><div class="glist">{items}</div></section></main>
<footer><span>© 2026 Prajwal Gautam · Kathmandu, Nepal</span><span><a href="../">Home</a> · <a href="../work/nepal-bhoomi/">Nepal Bhoomi case study</a></span></footer>
</div>
</body>
</html>
"""

# ------------------------------------------------------------------ home page (business-first layout on the WebGL card engine)
WA_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-3.3-.8-2.8-1.1-4.5-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.3 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1c.2-.3.4-.2.6-.1l2 .9c.3.1.4.2.5.3.1.2.1.7-.1 1.2z"/></svg>'
# the marketing arm of the galaxy carries the marketing skills clients ask for
CATS_V2 = [dict(c, skills=['Lead Generation','Social Media','Meta Ads','Google Ads','Branding','Growth Marketing'], name='Marketing & Leads') if c['word']=='GROWTH' else c for c in CATS]

def engine_v2():
    e = engine()
    def R(a, b):
        nonlocal e
        assert e.count(a) == 1, a[:60]; e = e.replace(a, b)
    R("if(name==='face') return m?{o:[0,halfH*.02,0],s:.78}:{o:[halfW*.04,-1.7,0],s:.9};",
      "if(name==='face') return m?{o:[0,-halfH*2.4,0],s:.64}:{o:[halfW*.5,-1.6,0],s:.86};")
    R("if(name==='galaxy') return m?{o:[0,3,0],s:.62}:{o:[halfW*.3,0,0],s:1};",
      "if(name==='galaxy') return m?{o:[0,halfH*.48,0],s:.6}:{o:[halfW*.58,0,0],s:.8};")
    R("if(name==='nb'||name==='sf') return m?{o:[0,halfH*.42,0],s:.75}:{o:[halfW*.4,0,0],s:1};",
      "if(name==='nb'||name==='sf') return m?{o:[0,halfH*.5,0],s:.6}:{o:[halfW*.48,0,0],s:.95};")
    # after the last section's anchor, move the camera with the page so the last shape scrolls away with its section
    R("function frame(time){\n  if(lenis) lenis.raf(time);",
      "function frame(time){\n  if(lenis) lenis.raf(time);\n  { const last=anchors[anchors.length-1]; const over=last?Math.max(0,scrollY-last.y):0; const cy=-over*(2*halfH)/innerHeight;\n    if(camera.position.y!==cy){ camera.position.y=cy; camera.lookAt(0,cy,0); } }")
    return e

def page_v2(link, case_url, guides_url, img):
    groups = ''.join(f'<div class="group" style="--c:{c["c"]}"><div class="gh"><i></i>{E(c["name"])}<small>{len(c["skills"])} skills</small></div><div class="chips">'
                     + ''.join(f'<span>{E(x)}</span>' for x in c['skills']) + '</div></div>'
                     for c in sorted(CATS_V2, key=lambda c: ['GROWTH','SEO','AI','CODE','APPS','VIDEO'].index(c['word'])))
    t = open(os.path.join(ROOT, 'templates', 'page.html')).read()
    det = lambda items, first=False: ''.join(f'<details{" open" if first and i == 0 else ""}><summary>{E(q)}</summary><p>{E(a)}</p></details>' for i, (q, a) in enumerate(items))
    faq, faq_about = det(FAQ_BIZ, True), det(FAQ_HOME[len(FAQ_BIZ):])
    gcards = ''.join(f'<a class="work gcard" href="{guides_url}{g["slug"]}/"><span class="num">Guide {i+1:02d}</span><h3>{E(g["h1"])}</h3><p>{E(g["answer"][:150].rsplit(" ",1)[0])}…</p><span class="go">Read the guide →</span></a>' for i, g in enumerate(GUIDES[:3]))
    col = lambda h, items: f'<div><h4>{h}</h4>' + ''.join(f'<a href="{u}">{E(n)}</a>' for n, u in items) + '</div>'
    mk = ['digital-marketing-expert-nepal','lead-generation-nepal','social-media-marketing-nepal','google-meta-ads-expert-nepal','seo-expert-nepal','aeo-geo-expert','branding-digital-marketing-nepal','growth-marketing-consultant']
    dv = ['ai-engineer-nepal','hire-ai-developer','full-stack-developer-nepal','web-developer-kathmandu','app-developer-nepal','ai-video-production']
    ind = ['real-estate-marketing-nepal','jewellery-marketing-nepal','saas-motion-design']
    foot = (col('Marketing', [(BY_SLUG[x]['kw'], link(x)) for x in mk]) + col('Development &amp; AI', [(BY_SLUG[x]['kw'], link(x)) for x in dv])
            + col('Industries', [(BY_SLUG[x]['kw'], link(x)) for x in ind] + [('Nepal Bhoomi case study', case_url)])
            + col('Guides', [(g['h1'], f'{guides_url}{g["slug"]}/') for g in GUIDES] + [('All guides', guides_url)]))
    if RESULTS['stats']:
        stats = ''.join(f'<div class="stat"><div class="num">{E(v)}</div><p>{E(l)}</p><small>{E(n)}</small></div>' for v, l, n in RESULTS['stats'])
        quotes = ''.join(f'<figure class="quote"><blockquote>{E(q)}</blockquote><figcaption class="by">{E(who)}</figcaption></figure>' for q, who in RESULTS['quotes'])
        t = t.replace('{{STATS}}', stats).replace('{{QUOTES}}', quotes)
    else:
        t = re.sub(r'<!--RESULTS-->.*?<!--/RESULTS-->', '', t, flags=re.S)
    t = re.sub(r'\{\{L:([a-z0-9-]+)\}\}', lambda m: (BY_SLUG[m.group(1)] and link(m.group(1))), t)
    t = re.sub(r'\{\{W:([a-z0-9-]+)\}\}', lambda m: img['work'] + m.group(1) + '.webp', t)
    rep = {'{{SKILLGROUPS}}': groups, '{{WA_ICON}}': WA_ICON, '{{FAQ}}': faq, '{{FAQ_ABOUT}}': faq_about, '{{GUIDE_CARDS}}': gcards, '{{FOOT_COLS}}': foot, '{{CASE}}': case_url, '{{GUIDES}}': guides_url,
           '{{IMG_NB}}': img['nb'], '{{IMG_LOGO}}': img.get('logo', 'assets/brand/logo.svg'), '{{IMG_SF}}': img['sf'], '{{IMG_PHOTO}}': img['photo'],
           '{{CATS_JSON}}': json.dumps([dict(name=c['name'], word=c['word'], c=c['c'], skills=c['skills']) for c in CATS_V2]),
           '{{ENGINE}}': engine_v2()}
    for k, v in rep.items():
        assert k in t, k; t = t.replace(k, v)
    return t

def build_preview(face):
    out = os.path.join(ROOT, 'preview'); shutil.rmtree(out, ignore_errors=True); os.makedirs(os.path.join(out, 'assets'))
    for f in ['nepal-bhoomi-logo.webp', 'slugforge-logo.webp', 'prajwal-gautam.webp']:
        shutil.copy(os.path.join(REPO, 'assets', f), os.path.join(out, 'assets', f))
    a = page_v2(lambda slug: f'{SITE}services/{slug}/', f'{SITE}work/nepal-bhoomi/', f'{SITE}guides/',
                dict(nb='assets/nepal-bhoomi-logo.webp', sf='assets/slugforge-logo.webp', photo='assets/prajwal-gautam.webp', work=f'{SITE}assets/work/', logo=f'{SITE}assets/brand/logo.svg'))
    a = a.replace('{{HEAD}}', '<title>Prajwal Gautam Portfolio</title>').replace('{{FACE}}', face)
    a = a.replace('</head>\n<body data-theme="paper">', '<script>document.body.dataset.theme="paper"</script>')
    a = a.replace('</body>\n</html>\n', '')
    assert '<body' not in a and '</head>' not in a and '{{' not in a, re.findall(r'\{\{[A-Z_:a-z-]+\}\}', a)[:5]
    a = a.replace('target="_blank" rel="noopener"', 'target="_blank" rel="noopener"')
    open(os.path.join(out, 'index.html'), 'w').write(a)
    return out

# ------------------------------------------------------------------ build
def build():
    face = open(os.path.join(ROOT, 'data', 'face-cards.b64')).read()
    # ---- site
    site_link = lambda slug, from_svc=False: (f"../{slug}/" if from_svc else f"services/{slug}/")
    main = page_v2(lambda slug: f"services/{slug}/", "work/nepal-bhoomi/", "guides/",
                   dict(nb='assets/nepal-bhoomi-logo.webp', sf='assets/slugforge-logo.webp', photo='assets/prajwal-gautam.webp', work='assets/work/'))
    main = main.replace('{{HEAD}}', head_main()).replace('{{FACE}}', face)
    assert '{{' not in main, re.findall(r'\{\{[A-Z_]+\}\}', main)[:5]
    open(os.path.join(REPO, 'index.html'), 'w').write(main)
    for s in SERVICES:
        d = os.path.join(REPO, 'services', s['slug']); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w').write(page_service(s, '../../', site_link, '../../assets/'))
    d = os.path.join(REPO, 'work', CASE['slug']); os.makedirs(d, exist_ok=True)
    case_link = lambda slug, from_svc=False: f"../../services/{slug}/"
    open(os.path.join(d, 'index.html'), 'w').write(page_case(CASE, '../../', case_link, '../../assets/'))
    os.makedirs(os.path.join(REPO, 'guides'), exist_ok=True)
    open(os.path.join(REPO, 'guides', 'index.html'), 'w').write(page_guides_index())
    for g in GUIDES:
        d = os.path.join(REPO, 'guides', g['slug']); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w').write(page_guide(g))
    urls = ([SITE] + [f"{SITE}services/{s['slug']}/" for s in SERVICES] + [f"{SITE}work/{CASE['slug']}/", f"{SITE}guides/"]
            + [f"{SITE}guides/{g['slug']}/" for g in GUIDES])
    open(os.path.join(REPO, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        ''.join(f'  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>{"1.0" if u==SITE else "0.8"}</priority></url>\n' for u in urls) + '</urlset>\n')
    # IndexNow: lets Bing, Yandex, Seznam and Naver know about new or changed pages. The key file must sit at the site root.
    open(os.path.join(REPO, INDEXNOW_KEY + '.txt'), 'w').write(INDEXNOW_KEY)
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
            "## Roles", "- AI Engineer", "- Digital Marketing Expert: lead generation, social media marketing and management, Facebook, Instagram and Google ads", "- Full-Stack Web Developer", "- App Developer (mobile and web)", "- AI Video Producer",
            "- SEO and AEO/GEO Specialist (AI search optimization) and Marketing Researcher", "- Motion Designer (SaaS product animation, 3D)", "- Industries: real estate, jewellery, SaaS and tech, e-commerce, education, food and travel", "- Google Ads and Meta Ads Campaign Strategist", "- Growth, E-commerce and Brand Marketer", "",
            "## Service pages"] + [f"- [{s['kw']}]({SITE}services/{s['slug']}/): {s['desc']}" for s in SERVICES] + ["",
            "## Experience"] + [f"- {j['co']} ({j['where']}): {html.unescape(j['title'])}. " + ' '.join(re.sub('<[^>]+>', '', p) for p in j['pts']) for j in JOBS] + ["",
            "## Live projects", f"- [Nepal Bhoomi](https://www.nepalbhoomi.com): real-estate platform; video, SEO and growth. Case study: {SITE}work/nepal-bhoomi/", "- [Slugforge Studio](https://slugforge.vercel.app): creative studio website and video services.", "",
            "## Guides"] + [f"- [{g['h1']}]({SITE}guides/{g['slug']}/): {g['answer']}" for g in GUIDES] + ["",
            "## Languages", "- Code: PHP, JavaScript, Python, SQL, HTML/CSS", "- Frameworks: Laravel, Node.js, React, Django, Three.js", "- Spoken: English, Nepali, Hindi", "",
            "## Education", "- BSc CSIT, New Summit College, Tribhuvan University", "- +2 Science, Kathmandu Model College", "",
            "## Contact", "- Email: prajolgautam1234@gmail.com", "- Phone & WhatsApp: +977 984-8137372 (https://wa.me/9779848137372)", "- LinkedIn: https://www.linkedin.com/in/prajjwal-gautam/",
            "- GitHub: https://github.com/Prajjwalgautam", "- Location: Kathmandu, Nepal (UTC+5:45); works with clients worldwide", ""]
    open(os.path.join(REPO, 'llms.txt'), 'w').write('\n'.join(llms))

    wc = {s['slug']: len(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', page_service(s, '/', site_link, '/'), flags=re.S)).split()) for s in SERVICES}
    print('built. service page word counts:', wc)
    print('preview:', build_preview(face))

if __name__ == '__main__':
    build()
