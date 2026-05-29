#!/usr/bin/env python3
"""High-res render of PDF cover + a weight-comparison strip of Archimoto weights
so we can match the exact weight Juan used."""
import os, subprocess, sys
PDF = r"C:\Users\jcgiu\Downloads\1766137890132.pdf"
OUT = r"C:\Users\jcgiu\Documents\JCG-OS\.superpowers\brainstorm\pdf-pages"
os.makedirs(OUT, exist_ok=True)
def ensure(p, i=None):
    try: __import__(i or p)
    except ImportError: subprocess.check_call([sys.executable,"-m","pip","install","-q",p])
ensure("PyMuPDF","fitz"); ensure("Pillow","PIL")
import fitz
from PIL import Image, ImageDraw, ImageFont

doc = fitz.open(PDF)
pg = doc[0]
pix = pg.get_pixmap(dpi=200)
cover = os.path.join(OUT, "cover-hi.png")
pix.save(cover)
im = Image.open(cover).convert("RGB")
W,H = im.size
print("cover hi-res:", im.size)
# crop headline band (top ~38%) and footer band (bottom ~14%)
im.crop((0, int(H*0.06), W, int(H*0.42))).save(os.path.join(OUT,"cover-headline.png"))
im.crop((0, int(H*0.84), W, H)).save(os.path.join(OUT,"cover-footer.png"))

# Build a weight comparison: render "SECRETO" in several Archimoto weights
FDIR = r"C:\Users\jcgiu\Documents\Asteroi Branding\Identidad\Tipografías\Archimoto V00"
weights = [
    ("Light",    "Owlking Project - Archimoto V00 Light.otf"),
    ("Regular",  "Owlking Project - Archimoto V00 Regular.otf"),
    ("Medium",   "Owlking Project - Archimoto V00 Medium.otf"),
    ("SemiBold", "Owlking Project - Archimoto V00 SemiBold.otf"),
    ("Bold",     "Owlking Project - Archimoto V00 Bold.otf"),
    ("ExtraBold","Owlking Project - Archimoto V00 ExtraBold.otf"),
    ("Black",    "Owlking Project - Archimoto V00 Black.otf"),
    ("Heavy",    "Owlking Project - Archimoto V00 Heavy.otf"),
]
strip = Image.new("RGB", (1100, 90*len(weights)+20), (12,12,14))
d = ImageDraw.Draw(strip)
y = 10
for label, fn in weights:
    try:
        f = ImageFont.truetype(os.path.join(FDIR, fn), 56)
    except Exception as e:
        print("skip", label, e); continue
    d.text((20, y+10), label.ljust(10), font=ImageFont.load_default(), fill=(150,150,150))
    d.text((180, y), "EL SECRETO", font=f, fill=(176,132,211))
    y += 90
strip.save(os.path.join(OUT, "weight-compare.png"))
print("done: cover-headline.png, cover-footer.png, weight-compare.png")
