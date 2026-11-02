"""Rasterise the logo set and build the social card.

SVG is the source of truth; these are the PNGs for the places that cannot take
one — GitHub and Hugging Face org avatars, apple-touch icons, Open Graph and
Twitter cards, slide decks.

    pip install cairosvg
    python3 export.py

Outputs land in png/. Regenerate rather than editing them.
"""

import os
import random
import sys

import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "png")
os.makedirs(OUT, exist_ok=True)

# Cut paper (tokens/tokens.css).
KRAFT = "#F4EFE4"
INK = "#171512"
MUTED = "#5C554A"
FIRED = "#EE6A26"

# (source svg, output name, pixel size, background or None for transparent)
JOBS = [
    ("avatar-night.svg", "avatar-night-1024.png", 1024, None),
    ("avatar-night.svg", "avatar-night-512.png", 512, None),
    ("avatar-cream.svg", "avatar-cream-512.png", 512, None),
    ("avatar-orange.svg", "avatar-orange-512.png", 512, None),
    ("mark-colour.svg", "mark-colour-1024.png", 1024, None),
    ("mark-colour.svg", "mark-colour-512.png", 512, None),
    ("mark-colour-dark.svg", "mark-colour-dark-1024.png", 1024, None),
    ("avatar-cream-bordered.svg", "avatar-cream-bordered-1024.png", 1024, None),
    ("avatar-cream-bordered.svg", "avatar-cream-bordered-512.png", 512, None),
    ("avatar-night-bordered.svg", "avatar-night-bordered-1024.png", 1024, None),
    ("avatar-night-bordered.svg", "avatar-night-bordered-512.png", 512, None),
    ("mark-colour-dark.svg", "mark-colour-dark-512.png", 512, None),
    ("favicon.svg", "favicon-16.png", 16, None),
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


def torn_rect(x, y, w, h, amp=3.2, step=9.0, seed=7):
    """A rectangle with hand-torn edges, as a polygon path.

    The site tears its blocks with an SVG displacement filter; cairosvg does
    not run feDisplacementMap, so the card draws the tear as geometry instead.
    Seeded, so a rebuild gives the same edge."""
    rnd = random.Random(seed)
    pts = []

    def edge(x0, y0, x1, y1):
        n = max(2, int(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5 / step))
        dx, dy = (x1 - x0) / n, (y1 - y0) / n
        # unit normal, pointing out of the block
        ln = (dx * dx + dy * dy) ** 0.5
        nx, ny = dy / ln, -dx / ln
        for i in range(n):
            j = rnd.uniform(-amp, amp)
            pts.append((x0 + dx * i + nx * j, y0 + dy * i + ny * j))

    edge(x, y, x + w, y)
    edge(x + w, y, x + w, y + h)
    edge(x + w, y + h, x, y + h)
    edge(x, y + h, x, y)
    return "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in pts) + " Z"


def _inner(name):
    src = open(os.path.join(HERE, name)).read()
    inner = src[src.index(">", src.index("<svg")) + 1:src.rindex("</svg>")]
    vb = src.split('viewBox="')[1].split('"')[0].split()
    return (inner.replace("<title>Plicara Labs</title>", ""),
            float(vb[2]), float(vb[3]))


def social():
    """1200x630 Open Graph card, in the cut-paper hand of the site's hero.

    Kraft ground; a torn fired block carrying the site's question in Hedvig,
    in ink (cream on fired is 2.9:1 and fails); the mark to its right; the
    wordmark under it. Every glyph is an outline, so the PNG does not depend
    on what fonts the build machine has."""
    sys.path.insert(0, HERE)
    sys.argv = sys.argv[:1]
    import build  # noqa: E402  (fonts and shaping live there)

    serif = build.static_hedvig()
    sans = build.static_figtree(600)

    W, H = 1200, 630
    BX, BY, BW, BH = 72, 88, 720, 400
    lines = ["How do we know", "an AI system", "works?"]
    SIZE, LEAD = 76.0, 1.06
    meta = "independent AI research"

    heads = []
    for i, t in enumerate(lines):
        d, _ = build.shape(serif, t, SIZE, tracking=-0.02)
        heads.append(f'<path transform="translate({BX + 52} '
                     f'{BY + 156 + i * SIZE * LEAD:.1f})" d="{d}"/>')
    md, _ = build.shape(sans, meta, 22.0, tracking=0.04)

    block = torn_rect(BX, BY, BW, BH)
    shadow = torn_rect(BX + 7, BY + 9, BW, BH, seed=11)

    mark, mw, mh = _inner("mark-colour.svg")
    MS = 250.0
    mx, my = 880, BY + (BH - MS) / 2 - 10

    # The lockup would repeat the mark; set just the word, in Figtree.
    wd, wadv = build.shape(build.static_figtree(700), "plicara labs", 40.0)

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}">'
        f'<rect width="{W}" height="{H}" fill="{KRAFT}"/>'
        f'<path d="{shadow}" fill="{INK}" fill-opacity="0.10"/>'
        f'<g transform="rotate(-1.2 {BX + BW / 2} {BY + BH / 2})">'
        f'<path d="{block}" fill="{FIRED}"/>'
        f'<path transform="translate({BX + 54} {BY + 66})" d="{md}" '
        f'fill="{INK}"/>'
        f'<g fill="{INK}">{"".join(heads)}</g></g>'
        f'<g transform="translate({mx} {my:.1f}) scale({MS / mw:.4f})">'
        f'{mark}</g>'
        f'<path transform="translate({mx + (MS - wadv) / 2:.1f} {my + MS + 62:.1f})" '
        f'd="{wd}" fill="{INK}"/>'
        f'<path transform="translate({BX + 54} {H - 56})" '
        f'd="{build.shape(sans, "plicara.github.io", 20.0, tracking=0.02)[0]}" '
        f'fill="{MUTED}"/>'
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
