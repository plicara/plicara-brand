"""Rasterise the logo set and build the social card.

SVG is the source of truth; these are the PNGs for the places that cannot take
one — GitHub and Hugging Face org avatars, apple-touch icons, Open Graph and
Twitter cards, slide decks.

    pip install cairosvg
    python3 export.py

Outputs land in png/. Regenerate rather than editing them.
"""

import os

import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "png")
os.makedirs(OUT, exist_ok=True)

NIGHT = "#163B4E"
BUTTER = "#F3DC7C"
WASHI = "#FAF6ED"

# (source svg, output name, pixel size, background or None for transparent)
JOBS = [
    ("avatar-night.svg", "avatar-night-1024.png", 1024, None),
    ("avatar-night.svg", "avatar-night-512.png", 512, None),
    ("avatar-butter.svg", "avatar-butter-512.png", 512, None),
    ("avatar-sumi.svg", "avatar-sumi-512.png", 512, None),
    ("mark-butter.svg", "mark-butter-512.png", 512, None),
    ("mark-sumi.svg", "mark-sumi-512.png", 512, None),
    ("favicon.svg", "favicon-32.png", 32, None),
    ("favicon.svg", "favicon-64.png", 64, None),
    ("touch-icon.svg", "apple-touch-icon-180.png", 180, None),
]


def render(src, dst, size, bg=None):
    cairosvg.svg2png(
        url=os.path.join(HERE, src),
        write_to=os.path.join(OUT, dst),
        output_width=size,
        output_height=size,
        background_color=bg,
    )
    print(f"  {dst:34s} {size}px")


def social():
    """1200x630 Open Graph card: lockup on night, centred, generous margin."""
    lockup = open(os.path.join(HERE, "lockup-horizontal-dark.svg")).read()
    inner = lockup[lockup.index(">", lockup.index("<svg")) + 1:lockup.rindex("</svg>")]
    inner = inner.replace("<title>Foothills Labs</title>", "")
    vb = lockup.split('viewBox="')[1].split('"')[0].split()
    w, h = float(vb[2]), float(vb[3])

    W, H = 1200, 630
    scale = 700.0 / w                       # lockup occupies ~58% of the width
    x, y = (W - w * scale) / 2, (H - h * scale) / 2 - 44

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}">'
        f'<rect width="{W}" height="{H}" fill="{NIGHT}"/>'
        f'<g transform="translate({x:.1f} {y:.1f}) scale({scale:.4f})">{inner}</g>'
        f'<text x="{W / 2}" y="{H - 214}" fill="{BUTTER}" text-anchor="middle" '
        f'font-family="monospace" font-size="19" letter-spacing="5.2">'
        f'BENCHMARKS FIRST, THEN MODELS</text>'
        f'<rect x="0" y="{H - 12}" width="{W}" height="12" fill="{BUTTER}"/>'
        f'</svg>'
    )
    path = os.path.join(OUT, "social-card-1200x630.png")
    cairosvg.svg2png(bytestring=svg.encode(), write_to=path,
                     output_width=W, output_height=H)
    print(f"  {'social-card-1200x630.png':34s} {W}x{H}")


if __name__ == "__main__":
    print("raster exports")
    for src, dst, size, bg in JOBS:
        render(src, dst, size, bg)
    social()
    print(f"\nwrote {OUT}")
