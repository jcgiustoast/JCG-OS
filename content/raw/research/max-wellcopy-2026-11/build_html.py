import base64, glob, io, os, re, sys
import markdown

S = sys.argv[1]          # scratchpad/max
OUT = sys.argv[2]        # output html path
md = open(os.path.join(S, "playbook.md"), encoding="utf-8").read()
fm, body = re.match(r"^---\n(.*?)\n---\n(.*)$", md, re.S).groups()

try:
    from PIL import Image
except ImportError:
    Image = None

def data_uri(path, width=420):
    if Image:
        im = Image.open(path).convert("RGB")
        if im.width > width:
            im = im.resize((width, int(im.height * width / im.width)))
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=72)
        raw = buf.getvalue()
    else:
        raw = open(path, "rb").read()
    return "data:image/jpeg;base64," + base64.b64encode(raw).decode()

def find_image(url):
    m = re.search(r"instagram\.com/(?:reel|p)/([\w-]+)", url)
    if m:
        p = os.path.join(S, "instagram", "thumbs", m.group(1) + ".jpg")
        return p if os.path.exists(p) else None
    m = re.search(r"watch\?v=([\w-]+)", url)
    if m:
        g = glob.glob(os.path.join(S, "youtube", "thumbnails", "*_" + m.group(1) + ".jpg"))
        return g[0] if g else None
    m = re.search(r"tiktok\.com/@\w+/video/(\d+)", url)
    if m:
        g = glob.glob(os.path.join(S, "tiktok", "raw", "covers", "*_" + m.group(1) + ".jpg"))
        return g[0] if g else None
    return None

used = set()
def link_html(url, label=None):
    full = url if url.startswith("http") else "https://" + url
    img = find_image(full)
    text = label or re.sub(r"^https?://(www\.)?", "", full)
    if len(text) > 48 and not label:
        text = text[:45] + "…"
    if img:
        key = img
        thumb = f'<img class="thumb" src="{data_uri(img)}" alt="">' if key not in used else ""
        used.add(key)
        return f'<a class="post" href="{full}" target="_blank">{thumb}<span>{text} ↗</span></a>'
    return f'<a class="post" href="{full}" target="_blank"><span>{text} ↗</span></a>'

# existing markdown links [t](url)
body = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", lambda m: link_html(m.group(2), m.group(1)), body)
# bare platform urls
pat = re.compile(r"(?<![\w/.\"=])((?:https?://)?(?:www\.)?(?:instagram|x|tiktok|youtube|linkedin)\.com/[^\s|)·,<\"]+)")
body = pat.sub(lambda m: link_html(m.group(1)), body)
# local image paths like instagram\thumbs\X.jpg -> drop (thumb already shown with link) or embed if not used
def local_img(m):
    p = os.path.join(S, *m.group(1).split("\\"))
    if os.path.exists(p) and p not in used:
        used.add(p)
        return f'<img class="thumb" src="{data_uri(p)}" alt="">'
    return "✓ shown"
body = re.sub(r"`?((?:instagram|youtube|tiktok)\\[\w\\.\-]+\.jpg)`?", local_img, body)

body = re.sub(r"(?m)^([^|\n].*)\n(\|)", r"\1\n\n\2", body)
html_body = markdown.markdown(body, extensions=["tables", "sane_lists"])

# gallery appendix
gal = []
def add(title, paths, width=420):
    cells = "".join(f'<figure><img src="{data_uri(p, width)}" alt=""><figcaption>{os.path.basename(p)}</figcaption></figure>' for p in paths)
    gal.append(f"<h3>{title}</h3><div class='gallery'>{cells}</div>")
add("Instagram highlights (his sales page: Me → Results → Free Stuff → Work w/ Me)", sorted(glob.glob(os.path.join(S, "instagram", "story_frames", "*.jpg"))), 300)
add("Instagram covers and slides", sorted(glob.glob(os.path.join(S, "instagram", "thumbs", "*.jpg"))), 300)
add("YouTube thumbnails (top 10 long, recent, Shorts)", sorted(glob.glob(os.path.join(S, "youtube", "thumbnails", "*.jpg"))), 420)
recent_tt = sorted(glob.glob(os.path.join(S, "tiktok", "raw", "covers", "2026-*.jpg")))[-12:]
add("TikTok covers (latest 12)", recent_tt, 260)
add("YouTube contact sheet (all long-video thumbnails)", [os.path.join(S, "youtube", "contact_sheet_long.jpg")], 1200)

meta = dict(re.findall(r"^(\w+):\s*(.*)$", fm, re.M))
css = """
:root{--bg:#fafafa;--fg:#1d1d22;--muted:#666;--card:#fff;--line:#e3e3e8;--accent:#6b4bd8;--head:#f1eefb}
@media (prefers-color-scheme:dark){:root{--bg:#141418;--fg:#e8e8ee;--muted:#a0a0aa;--card:#1d1d23;--line:#33333c;--accent:#a58cff;--head:#26223a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 -apple-system,Segoe UI,Inter,Roboto,sans-serif}
main{max-width:1100px;margin:0 auto;padding:32px 16px 80px}
h1{font-size:2rem;margin:.2em 0}h2{margin-top:2.4em;padding-top:.6em;border-top:2px solid var(--line)}h3{margin-top:1.8em}
blockquote{margin:0;padding:10px 16px;background:var(--head);border-radius:8px;color:var(--fg)}
.meta{color:var(--muted);font-size:.9rem}
table{border-collapse:collapse;width:100%;margin:14px 0;font-size:.92rem;display:block;overflow-x:auto}
th,td{border:1px solid var(--line);padding:7px 9px;vertical-align:top;text-align:left}
th{background:var(--head)}td{background:var(--card)}
a{color:var(--accent)}a.post{display:inline-flex;flex-direction:column;gap:4px;text-decoration:none;max-width:220px}
a.post span{text-decoration:underline;word-break:break-all;font-size:.85rem}
img.thumb{width:160px;max-width:100%;border-radius:6px;border:1px solid var(--line)}
.gallery{display:flex;flex-wrap:wrap;gap:12px}.gallery figure{margin:0;max-width:300px}
.gallery img{width:100%;border-radius:6px;border:1px solid var(--line)}figcaption{font-size:.75rem;color:var(--muted)}
nav{position:sticky;top:0;background:var(--bg);padding:8px 0;border-bottom:1px solid var(--line);font-size:.85rem;z-index:2;overflow-x:auto;white-space:nowrap}
nav a{margin-right:14px}
"""
# nav from h2
ids = []
def h2id(m):
    t = re.sub("<.*?>", "", m.group(1)); i = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
    ids.append((i, t)); return f'<h2 id="{i}">{m.group(1)}</h2>'
html_body = re.sub(r"<h2>(.*?)</h2>", h2id, html_body)
nav = "<nav>" + "".join(f'<a href="#{i}">{t}</a>' for i, t in ids) + '<a href="#gallery">Image gallery</a></nav>'

doc = f"""<!doctype html>
<!--
{fm}
-->
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Max Wellcopy Playbook</title><meta name="description" content="{meta.get('description','')}">
<style>{css}</style></head><body><main>
<p class="meta">author: claude · created {meta.get('created')} · updated {meta.get('updated')} · confidence {meta.get('confidence')}</p>
{nav}
{html_body}
<h2 id="gallery">Image gallery (saved references)</h2>
<p class="meta">Saved from his public profiles on 2026-11-25 for private study. Click any linked post above for the original.</p>
{''.join(gal)}
</main></body></html>"""
open(OUT, "w", encoding="utf-8").write(doc)
print("ok", OUT, round(len(doc)/1e6, 2), "MB", "images inline:", len(used), "PIL:", bool(Image))
