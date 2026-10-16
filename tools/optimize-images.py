#!/usr/bin/env python3
"""
Janeses image optimizer.

    pip install pillow
    python tools/optimize-images.py

Put original photos (jpg / jpeg / png / webp) in  images-src/
Optimized WebP files are written to                images/
Each photo gets up to three widths (480 / 800 / 1280, never upscaled, files are named
by real pixel width) plus name-og.jpg for the names listed in OG_FOR (WhatsApp / Facebook previews).
images/manifest.json records every photo's size so pages can set width/height.
"""
import os, glob, json
from PIL import Image, ImageOps

SRC, OUT = "images-src", "images"
WIDTHS = [480, 800, 1280]
QUALITY = 78
QUALITY_FOR = {"combo-deal-final": 88}   # text-heavy artwork needs higher quality
OG_FOR = {"logo-black"}   # only these get a 1200px JPG for link previews

# Crops in original pixels: (left, top, right, bottom).
CROPS = {
    "event-aisle":         (0, 0, 744, 985),     # remove phone-camera caption strip
    "hall-decor":          (0, 0, 562, 745),     # remove phone-camera caption strip
    "food-jollof":         (0, 0, 850, 1280),    # remove TikTok icon column
    "food-ofada":          (0, 0, 840, 1280),    # remove TikTok icon column
    "food-jollof-chicken": (0, 600, 715, 1225),  # foreground plate only (no phone, no TikTok icons)
    "gown-detail":         (0, 216, 607, 1080),  # gown only (removes emoji overlay)
    "cake-fruit-basket":   (0, 130, 1118, 1240), # remove Instagram header/footer bars from screenshot
}
# Rotation in degrees counter-clockwise, applied before cropping (for sideways phone photos).
ROTATE = {"gift-name-boxes": 90}

# Extra derived files: output name -> (source name, crop box)
DERIVED = {
    "logo-mark": ("logo", (455, 115, 830, 480)),  # square emblem for nav/footer/favicon
    "logo-full": ("logo", (320, 110, 960, 710)),  # logo without surrounding white space
}

os.makedirs(OUT, exist_ok=True)
manifest = {}

def save_set(img, name):
    img = ImageOps.exif_transpose(img).convert("RGB")
    w, h = img.size
    sizes = sorted(set([t for t in WIDTHS if t < w] + [min(w, WIDTHS[-1])]))
    for tw in sizes:
        th = round(h * tw / w)
        img.resize((tw, th), Image.LANCZOS).save(
            f"{OUT}/{name}-{tw}.webp", "WEBP", quality=QUALITY_FOR.get(name, QUALITY), method=6)
    if name in OG_FOR:
        ow = min(1200, w)
        img.resize((ow, round(h * ow / w)), Image.LANCZOS).save(
            f"{OUT}/{name}-og.jpg", "JPEG", quality=82, optimize=True, progressive=True)
    manifest[name] = {"w": w, "h": h, "widths": sizes}

files = []
for ext in ("jpg", "jpeg", "png", "webp"):
    files += glob.glob(f"{SRC}/*.{ext}")

for path in sorted(files):
    name = os.path.splitext(os.path.basename(path))[0]
    img = Image.open(path)
    if name in ROTATE:
        img = img.rotate(ROTATE[name], expand=True)
    if name in CROPS:
        img = img.crop(CROPS[name])
    save_set(img, name)
    for out_name, (src_name, box) in DERIVED.items():
        if src_name == name:
            save_set(Image.open(path).crop(box), out_name)
    print("optimized:", name)

with open(f"{OUT}/manifest.json", "w") as f:
    json.dump(manifest, f, indent=1)
with open("js/images-manifest.js", "w") as f:   # lets js/promos.js build responsive <img> tags
    f.write("window.JANESES_IMAGES = " + json.dumps(manifest, separators=(",", ":")) + ";\n")
print("done —", len(manifest), "images")
