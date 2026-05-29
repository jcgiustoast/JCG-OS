#!/usr/bin/env python3
"""Render the hand-made carousel PDF to PNGs + a contact-sheet montage for visual study."""
import sys, subprocess, os

PDF = r"C:\Users\jcgiu\Downloads\1766137890132.pdf"
OUT = r"C:\Users\jcgiu\Documents\JCG-OS\.superpowers\brainstorm\pdf-pages"
os.makedirs(OUT, exist_ok=True)

def ensure(pkg, imp=None):
    try:
        __import__(imp or pkg)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pkg])

ensure("PyMuPDF", "fitz")
ensure("Pillow", "PIL")
import fitz
from PIL import Image

doc = fitz.open(PDF)
n = doc.page_count
print(f"pages: {n}")

pages = []
for i in range(n):
    pg = doc[i]
    pix = pg.get_pixmap(dpi=90)
    p = os.path.join(OUT, f"page-{i+1:02d}.png")
    pix.save(p)
    pages.append(p)

# Build contact sheets: 4 columns, thumbnails ~260px wide
cols = 4
thumb_w = 260
ims = [Image.open(p).convert("RGB") for p in pages]
# uniform thumb height based on first page ratio
ratio = ims[0].height / ims[0].width
thumb_h = int(thumb_w * ratio)
ims = [im.resize((thumb_w, thumb_h), Image.LANCZOS) for im in ims]

pad = 12
per_sheet = cols * 4  # 16 per sheet
sheets = []
for s in range(0, len(ims), per_sheet):
    chunk = ims[s:s+per_sheet]
    rows = (len(chunk) + cols - 1) // cols
    W = cols * thumb_w + (cols + 1) * pad
    H = rows * thumb_h + (rows + 1) * pad
    sheet = Image.new("RGB", (W, H), (20, 20, 20))
    for idx, im in enumerate(chunk):
        r, c = divmod(idx, cols)
        x = pad + c * (thumb_w + pad)
        y = pad + r * (thumb_h + pad)
        sheet.paste(im, (x, y))
    sp = os.path.join(OUT, f"contact-sheet-{s//per_sheet+1}.png")
    sheet.save(sp, optimize=True)
    sheets.append(sp)
    print("sheet:", sp, sheet.size)

print("done")
