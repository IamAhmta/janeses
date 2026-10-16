#!/usr/bin/env python3
"""
Builds the 5 HTML pages from src/pages/*.html + shared partials (nav, footer, head).

    python tools/optimize-images.py     # first: resize + convert photos to WebP
    python tools/build-site.py          # then: build pages

* Edit text in  src/pages/*.html  (shared nav/footer live in this file), then re-run.
* {{img:name|alt text|size-preset|flags}}  inserts a responsive <img> (srcset, width/height, lazy).
* The build FAILS if the same photo is used twice anywhere on the site.
"""
import json, re, os, glob, sys

SITE = "https://www.janeses.com"          # <-- change to your real domain
PHONE_1, PHONE_1_INTL = "+234 803 889 3499", "2348038893499"
EMAIL = "janesesconcept@gmail.com"
ADDRESS = "Suite 5 &amp; 6, Sunny Peace Plaza, Bida Bidi, Zaria Road, Jos"
IG = "https://www.instagram.com/janeses_concepts"

M = json.load(open("images/manifest.json"))
SIZES = {
    "heroarch": "(min-width:992px) 440px, 340px",
    "half":     "(min-width:992px) 560px, 100vw",
    "arch":     "(min-width:992px) 460px, 90vw",
    "card":     "(min-width:992px) 380px, (min-width:576px) 50vw, 100vw",
    "wide":     "(min-width:992px) 1100px, 100vw",
    "promo":    "(min-width:992px) 420px, 80vw",
    "story":    "(min-width:992px) 520px, 100vw",
    "deal":     "(min-width:992px) 520px, 90vw",
    "portrait": "(min-width:992px) 420px, 80vw",
}
# videos in /videos (width, height); each has NAME.mp4 + NAME-poster.webp
VIDEOS = {
    "bridal-gown-and-bouquet": (352, 640), "bridal-tiara": (640, 352), "bridal-bride-to-be-robe": (368, 656),
    "bridal-traditional-attire": (368, 656), "bridal-coral-beads": (368, 656),
    "drinks-vanilla-strawberry-testimonials": (576, 1024),
}

def video(name, title):
    w, h = VIDEOS[name]
    return (f'<figure class="vid{" vid-land" if w > h else ""}"><video controls preload="none" playsinline poster="videos/{name}-poster.webp" '
            f'width="{w}" height="{h}" aria-label="{title}"><source src="videos/{name}.mp4" type="video/mp4">Your browser can\'t play this video.</video>'
            f'<figcaption>{title}</figcaption></figure>')
used = {}

def img(name, alt, size="half", flags=""):
    if name not in M:
        sys.exit(f"ERROR: image '{name}' not found in images/manifest.json")
    used[name] = used.get(name, 0) + 1
    m = M[name]; ws = m["widths"]
    srcset = ", ".join(f"images/{name}-{w}.webp {w}w" for w in ws)
    fl = [f.strip() for f in flags.split(",") if f.strip()]
    eager = "eager" in fl
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    cls = next((f[4:] for f in fl if f.startswith("cls=")), "")
    pos = next((f[4:] for f in fl if f.startswith("pos=")), "")
    style = f' style="object-position:{pos}"' if pos else ""
    cls_attr = f' class="{cls}"' if cls else ""
    return (f'<img src="images/{name}-{ws[-1]}.webp" srcset="{srcset}" sizes="{SIZES.get(size, size)}" '
            f'width="{m["w"]}" height="{m["h"]}" alt="{alt}" {load} decoding="async"{cls_attr}{style}>')

def full(name):
    return f'images/{name}-{M[name]["widths"][-1]}.webp'

SVG_WA = '<svg width="28" height="28" viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.87.5 3.62 1.44 5.13L2 22l5.11-1.55c1.44.79 3.09 1.24 4.85 1.24h.01c5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2zm5.78 14.16c-.24.68-1.4 1.32-1.93 1.4-.5.08-1.13.11-1.83-.11-.42-.13-.96-.31-1.65-.6-2.91-1.26-4.81-4.16-4.96-4.35-.14-.19-1.18-1.57-1.18-3s.75-2.13 1.02-2.42c.26-.29.57-.36.77-.36h.55c.18 0 .41-.02.62.48.24.58.81 2 .88 2.15.07.15.11.32.02.51-.09.19-.14.31-.28.48-.14.17-.29.37-.42.5-.14.14-.28.29-.12.57.16.29.71 1.17 1.53 1.9 1.05.94 1.94 1.24 2.22 1.38.28.14.45.12.61-.07.17-.19.7-.82.89-1.1.19-.29.38-.24.63-.14.26.1 1.65.78 1.94.92.28.14.47.21.54.33.07.12.07.68-.17 1.36z"/></svg>'

def head(meta):
    title, desc, path = meta["title"], meta["description"], meta["path"]
    pre = ""
    if meta.get("preload"):
        n = meta["preload"]; ws = M[n]["widths"]
        srcset = ", ".join(f"images/{n}-{w}.webp {w}w" for w in ws)
        pre = (f'<link rel="preload" as="image" href="images/{n}-{ws[-1]}.webp" imagesrcset="{srcset}" '
               f'imagesizes="{SIZES["heroarch"]}" fetchpriority="high">\n')
    schema = ""
    if meta.get("schema") == "home":
        schema = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "EventPlanningBusiness",
  "name": "Janeses Integrated Services Ltd",
  "url": "{SITE}/",
  "image": "{SITE}/images/logo-black-og.jpg",
  "description": "Premium one-stop event solutions provider: catering, custom cakes, bridal services, event decoration, drinks and event essentials in Jos, Nigeria.",
  "telephone": "+{PHONE_1_INTL}",
  "email": "{EMAIL}",
  "address": {{"@type": "PostalAddress", "streetAddress": "Suite 5 & 6, Sunny Peace Plaza, Bida Bidi, Zaria Road", "addressLocality": "Jos", "addressRegion": "Plateau", "addressCountry": "NG"}},
  "founder": {{"@type": "Person", "name": "Janet Olajumoke Aiyenigba", "jobTitle": "Founder & CEO"}},
  "areaServed": "Nigeria",
  "sameAs": ["{IG}", "https://www.instagram.com/janesesbridesparlor", "https://www.instagram.com/janeses_cakes"]
}}
</script>
'''
    return f'''<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="Event Planner Nigeria, Catering Services Nigeria, Wedding Services Nigeria, Event Decoration Nigeria, Cakes Nigeria, Event Planner Jos">
<link rel="canonical" href="{SITE}/{'' if path == 'index.html' else path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Janeses Integrated Services Ltd">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/images/logo-black-og.jpg">
<meta property="og:url" content="{SITE}/{'' if path == 'index.html' else path}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0B3A22">
<link rel="icon" type="image/webp" href="images/logo-mark-375.webp">
{pre}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Inter:wght@400;500;600&family=Cormorant+Garamond:ital@1&display=swap" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.3/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
<link rel="stylesheet" href="css/extras.css">
<link rel="stylesheet" href="css/theme.css">
{schema}'''

def nav(active):
    items = [("home", "index.html", "Home"), ("about", "about.html", "About Us"), ("services", "services.html", "Services"), ("training", "training.html", "Training"),
             ("portfolio", "portfolio.html", "Portfolio"), ("contact", "contact.html", "Contact")]
    lis = "\n".join(f'      <li><a href="{h}"{" class=\"active\" aria-current=\"page\"" if k == active else ""}>{t}</a></li>' for k, h, t in items)
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<nav class="jan-nav" aria-label="Main">
  <div class="container-xl nav-inner">
    <a href="index.html" class="jan-brand" aria-label="Janeses Integrated Services Ltd, home">
      <img src="images/logo-mark-375.webp" alt="" width="44" height="44" decoding="async">
      <span class="jan-brand-text">Janeses<span>Integrated Services Ltd</span></span>
    </a>
    <ul class="jan-links" id="janLinks">
{lis}
      <li class="nav-cta-mobile"><a href="contact.html" class="btn-jan btn-gold btn-sm-jan">Book a Consultation</a></li>
    </ul>
    <div class="nav-cta-wrap">
      <a href="contact.html" class="btn-jan btn-gold btn-sm-jan nav-cta">Book a Consultation</a>
      <button class="jan-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="janLinks"><span></span><span></span><span></span></button>
    </div>
  </div>
</nav>
'''

def footer():
    return f'''<footer class="jan-footer">
  <div class="container-xl">
    <div class="row g-4">
      <div class="col-lg-4">
        <a href="index.html" class="jan-brand mb-3 d-inline-flex" aria-label="Janeses, home">
          <img src="images/logo-mark-375.webp" alt="" width="44" height="44" loading="lazy" decoding="async">
          <span class="jan-brand-text">Janeses<span>Integrated Services Ltd</span></span>
        </a>
        <p class="mt-3" style="font-size:.9rem;">Your one-stop shop for premium event and lifestyle services in Jos, Nigeria.</p>
        <div class="social-row mt-3">
          <a href="{IG}" aria-label="Instagram" target="_blank" rel="noopener"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1"/></svg></a>
          <a href="https://wa.me/{PHONE_1_INTL}" aria-label="WhatsApp" target="_blank" rel="noopener"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M21 11.5a8.5 8.5 0 01-12.5 7.5L3 20l1.1-5.4A8.5 8.5 0 1121 11.5z"/></svg></a>
        </div>
      </div>
      <div class="col-lg-2 col-6">
        <h5>Services</h5>
        <ul>
          <li><a href="services.html#catering">Catering</a></li>
          <li><a href="services.html#cakes">Custom Cakes</a></li>
          <li><a href="services.html#bridal">Bridal Services</a></li>
          <li><a href="services.html#decorations">Decorations</a></li>
          <li><a href="services.html#drinks">Drinks</a></li>
          <li><a href="services.html#essentials">Event Essentials</a></li>
        </ul>
      </div>
      <div class="col-lg-2 col-6">
        <h5>Quick Links</h5>
        <ul>
          <li><a href="index.html">Home</a></li>
          <li><a href="about.html">About Us</a></li>
          <li><a href="training.html">Training</a></li>
          <li><a href="portfolio.html">Portfolio</a></li>
          <li><a href="locations.html">Our Locations</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="index.html#kit" data-open-kit class="text-gold">Free Planning Kit</a></li>
        </ul>
      </div>
      <div class="col-lg-4">
        <h5>Contact</h5>
        <ul>
          <li>{ADDRESS}</li>
          <li><a href="tel:+{PHONE_1_INTL}">{PHONE_1}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 Janeses Integrated Services Ltd. All rights reserved.</span>
      <span>Your One-Stop Shop for Premium Services</span>
      <span class="credit">Designed &amp; Built by <a href="https://www.mrahmedgrowthsolutions.com.ng/" target="_blank" rel="nofollow noopener noreferrer">MR AHMED GROWTH SOLUTIONS</a></span>
    </div>
  </div>
</footer>

<a href="https://wa.me/{PHONE_1_INTL}" class="wa-float" target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp">{SVG_WA}</a>

<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.3/js/bootstrap.bundle.min.js" defer></script>
<script src="js/script.js" defer></script>
<script src="js/extras.js" defer></script>
'''

def render(path):
    raw = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
    meta = dict(l.split(": ", 1) for l in m.group(1).splitlines() if ": " in l)
    body = m.group(2)
    body = re.sub(r"\{\{img:([a-z0-9-]+)\|([^|}]*)\|([^|}]+)(?:\|([^}]*))?\}\}",
                  lambda k: img(k.group(1), k.group(2), k.group(3), k.group(4) or ""), body)
    body = re.sub(r"\{\{video:([a-z0-9-]+)\|([^}]*)\}\}", lambda k: video(k.group(1), k.group(2)), body)
    body = re.sub(r"\{\{full:([a-z0-9-]+)\}\}", lambda k: full(k.group(1)), body)
    body = body.replace("{{PHONE_1}}", PHONE_1).replace("{{PHONE_1_INTL}}", PHONE_1_INTL)\
               .replace("{{EMAIL}}", EMAIL).replace("{{ADDRESS}}", ADDRESS)
    promo_js = ('<script src="js/promos-data.js" defer></script>\n<script src="js/images-manifest.js" defer></script>\n'
                '<script src="js/promos.js" defer></script>\n') if "data-promos" in body else ""
    html = (f'<!DOCTYPE html>\n<html lang="en">\n<head>\n{head(meta)}</head>\n<body>\n'
            f'{nav(meta["active"])}\n<main id="main">\n{body}\n</main>\n{footer()}{promo_js}</body>\n</html>\n')
    out = meta["path"]
    open(out, "w", encoding="utf-8").write(html)
    print("built", out)

for p in sorted(glob.glob("src/pages/*.html")):
    render(p)

# promo images (js/promos-data.js) count too, so a promo can never repeat a photo used elsewhere
for n in re.findall(r'image\s*:\s*["\']([a-z0-9-]+)["\']', open("js/promos-data.js", encoding="utf-8").read()):
    if n not in M: sys.exit(f"ERROR: promo image '{n}' not found in images/manifest.json")
    used[n] = used.get(n, 0) + 1

dups = {k: v for k, v in used.items() if v > 1}
unused = [k for k in M if k not in used and not k.startswith("logo")]
print(f"\n{len(used)} photos placed on pages.")
if unused: print("not placed on any page:", ", ".join(unused))
if dups:
    sys.exit("ERROR: photos used more than once: " + ", ".join(f"{k} x{v}" for k, v in dups.items()))
print("OK: every photo is used exactly once.")
