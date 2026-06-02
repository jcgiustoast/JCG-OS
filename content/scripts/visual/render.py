import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup, escape
from PIL import Image
from playwright.sync_api import sync_playwright

from content.scripts.visual.piece import parse_pipes, parse_bars

_TPL_DIR = Path(__file__).parent / "templates"
_ASSETS_DIR = Path(__file__).parent / "assets"
SCALE = 3.6  # 300x375 CSS px * 3.6 = 1080x1350 export


def _env():
    env = Environment(
        loader=FileSystemLoader(str(_TPL_DIR)),
        autoescape=select_autoescape(enabled_extensions=("j2",)),
    )
    env.filters["pipes"] = parse_pipes
    env.filters["bars"] = parse_bars
    env.filters["nl2br"] = _nl2br
    return env


def _nl2br(value):
    r"""Escape text and convert an author's literal '\n' into <br>."""
    return Markup("<br>".join(escape(part) for part in str(value).split("\\n")))


def render_html(piece):
    """Render a Piece into a single self-contained HTML string (CSS inlined)."""
    theme_css = (_TPL_DIR / "theme.css").read_text(encoding="utf-8")
    return _env().get_template("base.html.j2").render(slides=piece.slides, theme_css=theme_css)


def render_piece(piece, out_dir):
    """Render every slide to out_dir/image-NN.png at 1080x1350. Returns list of Paths."""
    out_dir = Path(out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    assets_dst = out_dir / "assets"
    if assets_dst.exists():
        shutil.rmtree(assets_dst)
    shutil.copytree(_ASSETS_DIR, assets_dst)

    (out_dir / "index.html").write_text(render_html(piece), encoding="utf-8")

    paths = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_context(device_scale_factor=SCALE).new_page()
        page.goto((out_dir / "index.html").as_uri())
        page.wait_for_timeout(300)  # let webfonts settle
        slides = page.locator(".slide")
        for i in range(slides.count()):
            dst = out_dir / f"image-{i + 1:02d}.png"
            slides.nth(i).screenshot(path=str(dst))
            paths.append(dst)
        browser.close()
    return paths


def bundle_pdf(png_paths, out_dir):
    """Combine PNGs (in order) into out_dir/bundle.pdf. Returns the Path."""
    out_dir = Path(out_dir)
    imgs = [Image.open(p).convert("RGB") for p in png_paths]
    pdf = out_dir / "bundle.pdf"
    imgs[0].save(pdf, save_all=True, append_images=imgs[1:])
    return pdf
