#!/usr/bin/env python3
"""Build a self-contained slide-library HTML: inline fonts + (downscaled) images as base64.
Runs on the host (via Bash) so no base64 enters the model context."""
import base64, re, sys, io, subprocess

SESSION = r"C:\Users\jcgiu\Documents\JCG-OS\.superpowers\brainstorm\483-1780045608"
CONTENT = SESSION + r"\content"
SRC_HTML = CONTENT + r"\slide-library-v4-src.html"
OUT_HTML = CONTENT + r"\slide-library-v4.html"
ASSETS = CONTENT + r"\assets"

try:
    from PIL import Image
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "Pillow"])
    from PIL import Image

def b64_file(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def font_uri(path):
    ext = path.lower().rsplit(".", 1)[-1]
    mime = {"otf": "font/otf", "ttf": "font/ttf", "woff": "font/woff", "woff2": "font/woff2"}[ext]
    return f"data:{mime};base64,{b64_file(path)}"

def img_uri(path, max_w):
    im = Image.open(path)
    if im.width > max_w:
        h = int(im.height * max_w / im.width)
        im = im.resize((max_w, h), Image.LANCZOS)
    buf = io.BytesIO()
    if path.lower().endswith(".png"):
        im.save(buf, format="PNG", optimize=True)
        mime = "image/png"
    else:
        im = im.convert("RGB")
        im.save(buf, format="JPEG", quality=72, optimize=True)
        mime = "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(buf.getvalue()).decode()}"

html = open(SRC_HTML, encoding="utf-8").read()

# Map every asset reference -> data URI
fonts = {
    "archimoto-heavy.otf", "archimoto-black.otf", "archimoto-bold.otf", "archimoto-extrabold.otf",
    "archimoto-medium.otf", "archimoto-regular.otf",
    "archivo-regular.ttf", "archivo-medium.ttf", "archivo-bold.ttf", "archivo-extrabold.ttf", "archivo-black.ttf",
    "bigshoulders-black.ttf", "bigshoulders-extrabold.ttf",
}
img_maxw = {"space-1.jpg": 760, "asteroid-1.png": 320, "asteroid-2.png": 320, "asteroid-3.png": 320, "noise.jpg": 240}

count = {"font": 0, "img": 0, "miss": 0}

def replace(m):
    rel = m.group(1)              # e.g. ./assets/fonts/archimoto-heavy.otf
    name = rel.rsplit("/", 1)[-1]
    if name in fonts:
        count["font"] += 1
        return "url(%s)" % font_uri(ASSETS + "\\fonts\\" + name)
    if name in img_maxw:
        count["img"] += 1
        return "url(%s)" % img_uri(ASSETS + "\\" + name, img_maxw[name])
    count["miss"] += 1
    return m.group(0)

html = re.sub(r"url\('(\./assets/[^']+)'\)", replace, html)

# keep title in sync so we can tell versions apart
html = html.replace("<title>Slide Library v4</title>", "<title>Slide Library v4 — matched</title>")

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"fonts inlined: {count['font']}, images inlined: {count['img']}, unresolved: {count['miss']}")
print(f"output size: {len(html)/1024:.0f} KB -> {OUT_HTML}")
