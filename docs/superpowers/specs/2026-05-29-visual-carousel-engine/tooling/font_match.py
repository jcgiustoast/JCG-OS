#!/usr/bin/env python3
"""Definitively identify Juan's headline font: crop his real headline, render the same
words in each candidate font, stack for visual comparison."""
import os, subprocess, sys
OUT = r"C:\Users\jcgiu\Documents\JCG-OS\.superpowers\brainstorm\pdf-pages"
PDF = r"C:\Users\jcgiu\Downloads\1766137890132.pdf"
def ensure(p,i=None):
    try: __import__(i or p)
    except ImportError: subprocess.check_call([sys.executable,"-m","pip","install","-q",p])
ensure("PyMuPDF","fitz"); ensure("Pillow","PIL")
import fitz
from PIL import Image, ImageDraw, ImageFont

# Hi-res crop of his page-13 headline
doc = fitz.open(PDF)
pix = doc[12].get_pixmap(dpi=200)
p13 = os.path.join(OUT,"p13-hi.png"); pix.save(p13)
im = Image.open(p13).convert("RGB"); W,H = im.size
his = im.crop((0, int(H*0.27), W, int(H*0.66)))
his_w = 1000
his = his.resize((his_w, int(his.height*his_w/his.width)), Image.LANCZOS)

FB = r"C:\Users\jcgiu\Documents\Asteroi Branding\Identidad\Tipografías\Big Shoulders Text"
FA = r"C:\Users\jcgiu\Documents\Asteroi Branding\Identidad\Tipografías\Archivo"
cands = [
    ("Big Shoulders Black",     os.path.join(FB,"BigShouldersText-Black.ttf")),
    ("Big Shoulders ExtraBold", os.path.join(FB,"BigShouldersText-ExtraBold.ttf")),
    ("Archivo Black",           os.path.join(FA,"Archivo-Black.ttf")),
]
text = "Las 3 Herramientas"
rows = []
for label, path in cands:
    strip = Image.new("RGB",(his_w, 150),(211,255,78))  # verde bg like his slide
    d = ImageDraw.Draw(strip)
    f = ImageFont.truetype(path, 96)
    d.text((20, 18), text, font=f, fill=(10,10,10))
    d.text((20, 128), label, font=ImageFont.load_default(), fill=(60,60,60))
    rows.append(strip)

# stack: his crop on top, then candidates
total_h = his.height + sum(r.height for r in rows) + 40*4
canvas = Image.new("RGB",(his_w, total_h),(30,30,30))
y=20
# label his
canvas.paste(his,(0,y));
d=ImageDraw.Draw(canvas);
y += his.height + 8
d.text((20,y),"^ HIS ACTUAL (page 13)",fill=(255,255,255)); y+=32
for r in rows:
    canvas.paste(r,(0,y)); y += r.height + 40
canvas.save(os.path.join(OUT,"font-match.png"))
print("done -> font-match.png")
