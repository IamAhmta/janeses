#!/usr/bin/env python3
"""
Generates css/theme.css : the Janeses lemon-green brand theme.

It reads the ORIGINAL css/style.css and css/extras.css (which are never edited),
re-maps every hard-coded colour (navy -> deep green, blue -> leaf green, gold -> lemon),
and appends a flat, restrained finish (no glows / glass blur / hover-lift / glossy shadows).

    python tools/build-theme.py

To go back to the earlier navy/gold look, remove the  <link ... theme.css>  line
(in tools/build-site.py -> head()) and rebuild. Nothing else depends on it.
"""
import re

# ------------------------------------------------------------------ palette
DEEP, DEEP_800, DEEP_700 = "#0B3A22", "#124A2C", "#1B5C38"   # from the brand flyer's dark green (#083820)
LEAF, LEAF_600           = "#1D7A3B", "#166330"              # logo green (links / secondary)
LEMON, LEMON_HOVER       = "#B5DB12", "#A3C80A"              # from the flyer's lemon (#B0D800 / #B8E020)
LEMON_TEXT               = "#4B7A00"                         # lemon family dark enough for text on white
LEMON_100, LEMON_50      = "#F2F9CC", "#F7FBE3"

HEX = {
    "#0f172a": DEEP, "#16213b": DEEP_800, "#1e293b": DEEP_700,
    "#2563eb": LEAF, "#1d4ed8": LEAF_600,
    "#f59e0b": LEMON, "#d97f06": LEMON_TEXT, "#fdf0d5": LEMON_100, "#fff8ea": LEMON_50, "#6b5320": "#3F5A12",
    "#64748b": "#5C6B60", "#f8fafc": "#F6F8F2", "#eef1f6": "#E6EBE0", "#edf1f7": "#E9EEE3",
    "#c7d0df": "#C3CCBC", "#dce3f0": "#D8E5DB",
    "#b9c2d6": "#B8C9BC", "#cbd5e8": "#D2E1D6", "#e4e9f3": "#E5EEE7",
    "#9fb0cc": "#9DB5A3", "#93a2c0": "#9DB5A3", "#8394b3": "#8DA896",
}
RGB = {  # rgba(r,g,b,a) triples
    (15, 23, 42): (11, 58, 34), (37, 99, 235): (29, 122, 59),
    (245, 158, 11): (181, 219, 18), (8, 12, 24): (5, 20, 12),
}

def recolour(v):
    v = re.sub(r"#[0-9a-fA-F]{3,8}\b", lambda m: HEX.get(m.group(0).lower(), m.group(0)), v)
    def rgba(m):
        parts = [p.strip() for p in m.group(2).split(",")]
        try: t = tuple(int(float(x)) for x in parts[:3])
        except ValueError: return m.group(0)
        if t in RGB:
            parts[:3] = [str(x) for x in RGB[t]]
            return f"{m.group(1)}({','.join(parts)})"
        return m.group(0)
    return re.sub(r"(rgba?)\(([^)]*)\)", rgba, v)

# ------------------------------------------------------------------ tiny CSS walker
def split_top(s, sep):
    out, depth, q, cur = [], 0, None, ""
    for ch in s:
        if q:
            cur += ch
            if ch == q: q = None
            continue
        if ch in "\"'": q = ch; cur += ch; continue
        if ch == "(": depth += 1
        if ch == ")": depth -= 1
        if ch == sep and depth == 0: out.append(cur); cur = ""
        else: cur += ch
    if cur.strip(): out.append(cur)
    return out

def blocks(s):
    """yield (prelude, body) for top-level blocks"""
    i, n = 0, len(s)
    while i < n:
        j = s.find("{", i)
        if j == -1: break
        depth, k = 1, j + 1
        while k < n and depth:
            if s[k] == "{": depth += 1
            elif s[k] == "}": depth -= 1
            k += 1
        yield s[i:j].strip(), s[j + 1:k - 1]
        i = k

def overrides(css, wrap=None):
    out = []
    for pre, body in blocks(css):
        if pre.startswith("@media") or pre.startswith("@supports"):
            inner = overrides(body, pre)
            if inner: out.append(f"{pre}{{\n{inner}\n}}")
        elif pre.startswith("@"):
            continue                                # keyframes, font-face, ...
        else:
            changed = []
            for d in split_top(body, ";"):
                if ":" not in d: continue
                prop, val = d.split(":", 1)
                nv = recolour(val)
                if nv != val: changed.append(f"{prop.strip()}:{nv.strip()}")
            if changed: out.append(f"{pre}{{ {'; '.join(changed)}; }}")
    return "\n".join(out)

src = ""
for f in ("css/style.css", "css/extras.css"):
    src += re.sub(r"/\*.*?\*/", "", open(f, encoding="utf-8").read(), flags=re.S) + "\n"
auto = overrides(src)

# ------------------------------------------------------------------ hand-written finish
MANUAL = f"""
/* =========================================================
   FLAT, PROFESSIONAL FINISH
   No glows, glass blur, hover-lift or glossy shadows.
   ========================================================= */
:root{{
  --shadow-soft: 0 1px 2px rgba(8,34,20,.10), 0 4px 14px -8px rgba(8,34,20,.25);
  --shadow-card: 0 1px 2px rgba(8,34,20,.08);
}}
body{{ background:#fff; }}

/* flat surfaces: replace gradients/glows with solid brand colours */
.hero{{ background:var(--navy); }}
.page-head::before, .cta-band::before, .promo::before, .jingle-card::before{{ display:none; }}
.cta-band{{ background:var(--navy); }}
.kit-section{{ background:var(--navy); }}
.kit-side{{ background:var(--navy); }}
.svc-img-ph{{ background:var(--slate-200); }}

/* nav: solid, no glass */
.jan-nav.scrolled{{ background:var(--navy); backdrop-filter:none; -webkit-backdrop-filter:none; box-shadow:0 1px 0 rgba(255,255,255,.10); }}
.kit-modal{{ backdrop-filter:none; -webkit-backdrop-filter:none; background:rgba(5,20,12,.72); }}

/* buttons: crisp colour change on hover, no lift or glow */
.btn-jan{{ transition:background-color .18s ease, color .18s ease, border-color .18s ease; }}
.btn-gold:hover{{ background:{LEMON_HOVER}; color:var(--navy); transform:none; box-shadow:none; }}
.btn-navy:hover{{ background:var(--royal-600); color:#fff; transform:none; }}
.chip:hover{{ transform:none; }}
.svc-card:hover, .prog-card:hover, .loc-card:hover{{ transform:none; box-shadow:none; border-color:var(--royal); }}
.hero-kit-card:hover, .jingle-play:hover, .hero-kit-card{{ transform:none; }}
.k-card:hover img, .pf-item:hover img{{ transform:none; }}

/* quieter motion */
.wa-float{{ animation:none; box-shadow:0 2px 8px rgba(0,0,0,.25); }}
.reveal{{ transform:translateY(12px); transition:opacity .5s ease, transform .5s ease; }}
@keyframes rise{{ from{{ transform:translateY(10px); }} to{{ transform:none; }} }}

/* shadows: soft and minimal */
.kit-cover{{ box-shadow:none; }}
.lb img{{ box-shadow:none; }}
.hero-arch .arch-frame, .svc-img-ph.arch, .deal-img, .loc-card.primary, .prog-card.featured, .float-badge, .hero-kit-card{{ box-shadow:var(--shadow-soft); }}

/* notice promo layout (js/promos-data.js, layout "notice") */
.promo-notice-wrap{{ padding:28px 0 0; }}
.promo-notice{{ display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:20px; background:var(--gold); color:var(--navy); padding:28px 36px; border-radius:16px; }}
.promo-notice .eyebrow{{ color:var(--navy); margin-bottom:6px; }}
.promo-notice .eyebrow::before{{ background:var(--navy); }}
.promo-notice h2{{ color:var(--navy); font-size:1.5rem; margin:0 0 4px; }}
.promo-notice p{{ color:var(--navy); margin:0; }}
.promo-notice .btn-gold{{ background:var(--navy); color:#fff; }}
.promo-notice .btn-gold:hover{{ background:var(--navy-700); color:#fff; }}

/* ---------- Training: sticker / polaroid photo frames ---------- */
.story-img{{ background:#fff; padding:10px 10px 0; border-radius:3px; box-shadow:0 1px 2px rgba(0,0,0,.14), 0 8px 18px -10px rgba(0,0,0,.4); }}
.story-img img{{ border-radius:2px; box-shadow:none; display:block; }}
.story-img figcaption{{ margin:0; padding:10px 6px 14px; text-align:center; color:var(--slate); }}
.chapters > .chapter:nth-child(odd)  .story-img:nth-child(odd){{ transform:rotate(-1.8deg); }}
.chapters > .chapter:nth-child(odd)  .story-img:nth-child(even){{ transform:rotate(1.4deg); }}
.chapters > .chapter:nth-child(even) .story-img:nth-child(odd){{ transform:rotate(1.8deg); }}
.chapters > .chapter:nth-child(even) .story-img:nth-child(even){{ transform:rotate(-1.4deg); }}
@media (prefers-reduced-motion:reduce){{ .story-img{{ transform:none !important; }} }}

/* ---------- About: founder + journey ---------- */
.founder-feature{{ display:grid; grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr); gap:56px; align-items:center; margin-top:64px; }}
.founder-portrait .svc-img-ph.arch{{ margin:0 auto; }}
.founder-name{{ font-size:clamp(1.8rem,3vw,2.5rem); margin:0 0 4px; }}
.founder-role{{ font-family:var(--font-display); font-weight:600; font-size:.95rem; color:var(--royal); margin-bottom:18px; }}
.founder-closing{{ border-left:3px solid var(--gold); padding-left:16px; color:var(--navy); font-weight:500; }}
@media (max-width:991px){{ .founder-feature{{ grid-template-columns:1fr; gap:32px; }} }}
.journey{{ margin-top:80px; }}
.journey-head{{ margin-bottom:26px; }}
.journey-steps{{ list-style:none; margin:0; padding:0; display:grid; grid-template-columns:repeat(4,1fr); gap:0 28px; }}
.journey-steps li{{ position:relative; padding-top:26px; border-top:2px solid var(--slate-200); }}
.journey-steps li::before{{ content:""; position:absolute; top:-2px; left:0; width:44px; height:2px; background:var(--gold); }}
.j-no{{ display:block; font-family:var(--font-accent); font-style:italic; font-size:1.5rem; line-height:1; color:var(--gold-600); margin-bottom:8px; }}
.journey-steps h4{{ font-size:1.02rem; margin:0 0 6px; }}
.journey-steps p{{ font-size:.9rem; margin:0; }}
@media (max-width:991px){{ .journey-steps{{ grid-template-columns:1fr 1fr; row-gap:34px; }} }}
@media (max-width:560px){{ .journey-steps{{ grid-template-columns:1fr; }} }}

/* labels on dark sections use lemon; on light sections they use the dark leaf-lemon */
.bg-navy .eyebrow, .promo .eyebrow, .cta-band .eyebrow, .hero .eyebrow{{ color:var(--gold); }}
.step-no{{ color:var(--gold-600); }}

/* footer text must stay readable on the dark green */
.jan-footer p{{ color:#B8C9BC; }}

/* ---------- Footer credit ---------- */
.footer-bottom .credit a{{ color:var(--gold); font-weight:600; letter-spacing:.02em; }}
.footer-bottom .credit a:hover{{ text-decoration:underline; color:var(--gold); }}
"""

header = ("/* =========================================================\n"
          "   theme.css : Janeses lemon-green brand theme (GENERATED by tools/build-theme.py)\n"
          "   Loaded after style.css and extras.css, which are left untouched.\n"
          "   Remove the <link> to this file to return to the earlier navy/gold look.\n"
          "   ========================================================= */\n")
open("css/theme.css", "w", encoding="utf-8").write(header + auto + "\n" + MANUAL)
print("css/theme.css written:", len(auto.splitlines()), "recoloured rules +", MANUAL.count("{"), "finish rules")
