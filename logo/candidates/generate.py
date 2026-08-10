"""House-mark candidates for the paper rebrand. Pick one, then wire it into
../build.py as MARK_SRC; the rest of the pipeline is unchanged.

Four candidates, all deliberately NOT a paper-plane silhouette in side view —
that drawing belongs to Telegram:

    a. the sheet       unfolded sheet, dart crease pattern, no plane.
                       "The lab is the sheet; the planes belong to the models."
    b. the first fold  one corner folded across to the centre line — the
                       moment a sheet starts becoming a plane.
    c. head-on         the dart seen from the front: wing dihedral and keel,
                       three strokes. Echoes the old three-ridge mark.
    d. paper foothills accordion-pleated strip whose profile is low hills —
                       the old silhouette, refolded out of paper.

Same rules as every mark in this repo: generated, deterministic, monoline,
round caps. The wobble is the same hand as ../../marks/generate.py.

    python3 generate.py
"""

import math
import os

OUT = os.path.dirname(os.path.abspath(__file__))

VIEW = 512.0
STROKE = 15.0
SUMI = "#2B2422"
BUTTER = "#E7A63E"  # butterscotch


def _seed(name):
    return sum(ord(c) * (i + 7) for i, c in enumerate(name))


def _wobble(pts, name, amplitude=0.5, step=3.0, closed=False):
    s = _seed(name)
    dense = []
    seq = pts + [pts[0]] if closed else pts
    for (x0, y0), (x1, y1) in zip(seq, seq[1:]):
        d = math.hypot(x1 - x0, y1 - y0)
        n = max(2, int(d / step))
        for i in range(n):
            t = i / n
            dense.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
    if not closed:
        dense.append(seq[-1])
    out = []
    total = len(dense)
    for i, (x, y) in enumerate(dense):
        u = i / total * math.tau
        w = (math.sin(u * 3 + s) + 0.6 * math.sin(u * 7 + s * 1.7)) * amplitude
        if i == 0 or (not closed and i == total - 1):
            w = 0.0
        j = (i + 1) % total
        k = (i - 1) % total
        tx, ty = dense[j][0] - dense[k][0], dense[j][1] - dense[k][1]
        tl = math.hypot(tx, ty) or 1.0
        out.append((x - ty / tl * w, y + tx / tl * w))
    return out


def _smooth(pts, closed=False):
    def pt(i):
        if closed:
            return pts[i % len(pts)]
        return pts[max(0, min(len(pts) - 1, i))]

    n = len(pts) if closed else len(pts) - 1
    d = [f"M {pts[0][0]:.2f} {pts[0][1]:.2f}"]
    for i in range(n):
        p0, p1, p2, p3 = pt(i - 1), pt(i), pt(i + 1), pt(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0)
        d.append(f"C {c1[0]:.2f} {c1[1]:.2f} {c2[0]:.2f} {c2[1]:.2f} "
                 f"{p2[0]:.2f} {p2[1]:.2f}")
    if closed:
        d.append("Z")
    return " ".join(d)


def _tx(pts, tilt):
    a = math.radians(tilt)
    c, s = math.cos(a), math.sin(a)
    out = []
    for x, y in pts:
        dx, dy = x - 50.0, y - 50.0
        out.append((((dx * c - dy * s) + 50.0) * VIEW / 100.0,
                    ((dx * s + dy * c) + 50.0) * VIEW / 100.0))
    return out


# Each candidate: closed outline(s), open crease lines, tilt, and optionally
# "amp" — the wobble amplitude, where more is looser.
CANDIDATES = {
    "a-sheet": {
        "tilt": -6,
        "closed": [[(24, 10), (76, 10), (76, 90), (24, 90)]],
        "open": [
            [(50, 10), (50, 90)],
            [(50, 12), (26, 44)], [(50, 12), (74, 44)],
            [(50, 12), (30, 88)], [(50, 12), (70, 88)],
        ],
        "note": "the unfolded sheet: dart crease pattern, no plane",
    },
    # --- sheet variants, cut after the sheet direction was picked ----------
    # a2: the dart's first folds only. Quieter, and the small-cut answer —
    # three creases survive a 16 px tile where five turn to mush.
    "a2-sheet-quiet": {
        "tilt": -6,
        "closed": [[(24, 10), (76, 10), (76, 90), (24, 90)]],
        "open": [
            [(50, 10), (50, 90)],
            [(50, 12), (26, 48)], [(50, 12), (74, 48)],
        ],
        "note": "the sheet, quiet: centre fold and first creases only",
    },
    # a3: the origami square — both diagonals and the centre fold meeting in
    # the middle. Reads craft rather than letterhead.
    "a3-sheet-square": {
        "tilt": -5,
        "closed": [[(19, 19), (81, 19), (81, 81), (19, 81)]],
        "open": [
            [(21, 21), (79, 79)], [(79, 21), (21, 79)],
            [(50, 19), (50, 81)],
        ],
        "note": "the origami square: diagonals and centre crease",
    },
    # a4: the quiet sheet thrown off true — strongest tilt, loosest line.
    # Maximum levity while staying a sheet.
    "a4-sheet-jaunty": {
        "tilt": -14,
        "amp": 0.75,
        "closed": [[(26, 12), (74, 12), (74, 88), (26, 88)]],
        "open": [
            [(50, 12), (50, 88)],
            [(50, 14), (28, 48)], [(50, 14), (72, 48)],
        ],
        "note": "the sheet, jaunty: more tilt, looser line",
    },
    # --- distinctiveness round: a plain rect with lines is file-icon
    # territory. Each of these makes the drawing unmistakably ours, a
    # different way.
    # e1: the creases fold the monogram. A plausible crease pattern that is
    # also a lowercase f — the mark says the name without a letterform.
    "e1-monogram": {
        "tilt": -6,
        "closed": [[(26, 10), (74, 10), (74, 90), (26, 90)]],
        "open": [
            [(63, 21), (53, 15), (45, 25), (45, 83)],
            [(34, 41), (59, 41)],
        ],
        "note": "the monogram sheet: creases that fold a lowercase f",
    },
    # e2: the sheet growing a wing. One panel has already folded past the
    # edge — the silhouette stops being a rectangle, the story is mid-fold.
    "e2-wing": {
        "tilt": -4,
        "closed": [[(22, 16), (62, 16), (62, 88), (22, 88)],
                   [(62, 24), (94, 36), (62, 58)]],
        "open": [
            [(42, 16), (42, 88)],
        ],
        "note": "the sheet growing a wing: one fold already past the edge",
    },
    # e3: the foothills, refolded — taller, with the pleat returns landing
    # on a visible base strip. Says the lab's name in folded paper; the one
    # silhouette nobody else is near.
    "e3-foothills-refolded": {
        "tilt": 0,
        "closed": [[(8, 74), (20, 44), (33, 58), (50, 28), (67, 52),
                    (81, 42), (92, 74)]],
        "open": [
            [(20, 44), (28, 74)],
            [(50, 28), (59, 74)],
            [(81, 42), (87, 74)],
            # the second range, behind: only the arcs that peek above the
            # front profile are drawn (endpoints sit on the front slopes).
            # Ranges recede; crowns do not — this is what kills the crown
            # read.
            [(27, 52), (34, 40), (41, 45)],
            [(61, 43), (70, 34), (75, 46)],
        ],
        "note": "the foothills refolded: two pleated-paper ranges, no plane",
    },
    "b-first-fold": {
        "tilt": -6,
        "closed": [[(18, 10), (40, 10), (82, 52), (82, 90), (18, 90)],
                   [(40, 10), (82, 52), (40, 52)]],
        "open": [],
        "note": "one corner folded to the centre — a sheet becoming a plane",
    },
    "c-head-on": {
        "tilt": 0,
        "closed": [],
        "open": [
            [(8, 34), (50, 56), (92, 34)],
            [(50, 56), (45, 84)],
            [(50, 56), (55, 84)],
        ],
        "note": "the dart head-on: dihedral and keel, three strokes",
    },
    "d-paper-foothills": {
        "tilt": 0,
        "closed": [[(8, 76), (22, 46), (36, 62), (52, 36), (68, 58),
                    (82, 44), (92, 76)]],
        "open": [
            [(22, 46), (30, 76)],
            [(52, 36), (61, 76)],
            [(82, 44), (88, 76)],
        ],
        "note": "the foothills, refolded: pleated paper in profile",
    },
}


def _paths(cand, name):
    amp = cand.get("amp", 0.5)
    ds = []
    for i, poly in enumerate(cand["closed"]):
        pts = _wobble(poly, f"{name}-c{i}", amplitude=amp, closed=True)
        ds.append(_smooth(_tx(pts, cand["tilt"]), closed=True))
    for i, line in enumerate(cand["open"]):
        pts = _wobble(line, f"{name}-o{i}", amplitude=amp, step=4.0)
        ds.append(_smooth(_tx(pts, cand["tilt"])))
    return ds


def _svg(ds, colour, fill_n=0, title=""):
    body = []
    for d in ds[:fill_n]:
        body.append(f'<path d="{d}" fill="{BUTTER}" stroke="none" '
                    f'transform="translate(13 10)"/>')
    body.append(f'<g fill="none" stroke="{colour}" stroke-width="{STROKE}" '
                f'stroke-linecap="round" stroke-linejoin="round">'
                + "".join(f'<path d="{d}"/>' for d in ds) + "</g>")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {VIEW:.0f} {VIEW:.0f}" role="img" '
            f'aria-label="{title}">\n' + "\n".join(body) + "\n</svg>\n")




# --- the chosen mark: foothills refolded — colourways -----------------------
# The pleats give the mark four facets, and the facets take flat colour
# patches under the line — the two-layer construction, now with a Memphis
# temperature. Every way is 2-3 colours from the brand palette, nothing
# outside it.

PAL = {
    # pastel palette (2026-08-10, palette card): the live set
    "coral": "#F7A283", "butterscotch": "#E7A63E", "emerald": "#376F71",
    "duckegg": "#CBDFD4", "smoke": "#9DACBA", "blush": "#F7DDD3",
    "sumi": "#2B2422", "washi": "#FAF6ED",
    # retired 90s-anime hues, kept so the historical colourways still build
    "butter": "#F3DC7C", "magenta": "#B92D77", "teal": "#3EB7C6",
    "blossom": "#F0A7C0", "lilac": "#C9A9E2",
}

# Facets of e3-foothills-refolded, left to right, split at the pleat returns.
E3_FACETS = [
    [(8, 74), (20, 44), (28, 74)],
    [(20, 44), (33, 58), (50, 28), (59, 74), (28, 74)],
    [(50, 28), (67, 52), (81, 42), (87, 74), (59, 74)],
    [(81, 42), (92, 74), (87, 74)],
]

# The back range's visible regions: each closes down along the front slopes
# through the valley point, so no ground shows beneath the peeking peak.
E3_BACK_FILLS = [
    [(27, 52), (34, 40), (41, 45), (33, 58)],
    [(61, 43), (70, 34), (75, 46), (67, 52)],
]
E3_BACK_LINES = [
    [(27, 52), (34, 40), (41, 45)],
    [(61, 43), (70, 34), (75, 46)],
]

# facet colours cycle F1..F4; "back" fills the second range; line colour per
# ground. ADOPTED: seaglass (pastel palette). The 90s-anime ways below it are
# history and still build.
COLOURWAYS = {
    "seaglass": dict(f=["coral", "butterscotch", "emerald", "coral"],
                     back="duckegg", light="sumi", dark="washi",
                     note="ADOPTED. coral, butterscotch, emerald facets, "
                          "duck-egg back range: the pastel card"),
    "butter": dict(f=["butter", "butter", "butter", "butter"], back="butter",
                   light="sumi", dark="washi",
                   note="the control: all butter, two colours"),
    "arcade": dict(f=["magenta", "butter", "teal", "magenta"], back="teal",
                   light="sumi", dark="washi",
                   note="retired 2026-08-10 with the anime palette"),
    "sunset": dict(f=["blossom", "butter", "blossom", "butter"], back="blossom",
                   light="sumi", dark="washi",
                   note="blossom and butter alternating: warm, soft"),
    "cool":   dict(f=["teal", "lilac", "teal", "lilac"], back="lilac",
                   light="sumi", dark="washi",
                   note="teal and lilac: the cool half of the reference"),
    "neon":   dict(f=["magenta", "magenta", "magenta", "magenta"], back="magenta",
                   light="sumi", dark="teal",
                   note="magenta mass, teal line on dark: the arcade sign"),
}


def colourways():
    cand = CANDIDATES["e3-foothills-refolded"]
    name = "e3-foothills-refolded"
    ds = _paths(cand, name)
    back_line_ds = [_smooth(_tx(_wobble(l, f"{name}-o{i+3}", amplitude=0.45,
                                        step=4.0), cand["tilt"]))
                    for i, l in enumerate(E3_BACK_LINES)]
    front_ds = [d for d in ds if d not in back_line_ds]
    for way, cfg in COLOURWAYS.items():
        backs = []
        for i, poly in enumerate(E3_BACK_FILLS):
            pts = _wobble(poly, f"{name}-b{i}", amplitude=0.4, closed=True)
            d = _smooth(_tx(pts, cand["tilt"]), closed=True)
            backs.append(f'<path d="{d}" fill="{PAL[cfg["back"]]}" '
                         f'stroke="none" transform="translate(13 10)"/>')
        facets = []
        for i, poly in enumerate(E3_FACETS):
            pts = _wobble(poly, f"{name}-f{i}", amplitude=0.4, closed=True)
            d = _smooth(_tx(pts, cand["tilt"]), closed=True)
            facets.append(f'<path d="{d}" fill="{PAL[cfg["f"][i]]}" '
                          f'stroke="none" transform="translate(13 10)"/>')
        facets = backs + [
            f'<g fill="none" stroke="LINE" stroke-width="{STROKE}" '
            f'stroke-linecap="round" stroke-linejoin="round">'
            + "".join(f'<path d="{d}"/>' for d in back_line_ds) + "</g>"
        ] + facets
        for ground, linecol in (("", cfg["light"]), ("-dark", cfg["dark"])):
            strokes = (f'<g fill="none" stroke="{PAL[linecol]}" '
                       f'stroke-width="{STROKE}" stroke-linecap="round" '
                       f'stroke-linejoin="round">'
                       + "".join(f'<path d="{d}"/>' for d in front_ds) + "</g>")
            svg = (f'<svg xmlns="http://www.w3.org/2000/svg" '
                   f'viewBox="0 0 {VIEW:.0f} {VIEW:.0f}" role="img" '
                   f'aria-label="Foothills Labs — {way} colourway">\n'
                   + "\n".join(facets).replace("LINE", PAL[linecol])
                   + "\n" + strokes + "\n</svg>\n")
            with open(os.path.join(OUT, f"mark-foothills-{way}{ground}.svg"),
                      "w") as fh:
                fh.write(svg)
        print(f"wrote mark-foothills-{way}[-dark].svg")


def main():
    for name, cand in CANDIDATES.items():
        ds = _paths(cand, name)
        title = f"Foothills Labs house-mark candidate: {cand['note']}"
        with open(os.path.join(OUT, f"candidate-{name}.svg"), "w") as fh:
            fh.write(_svg(ds, "currentColor", title=title))
        with open(os.path.join(OUT, f"candidate-{name}-butter.svg"), "w") as fh:
            fh.write(_svg(ds, SUMI, fill_n=len(cand["closed"]), title=title))
        print(f"wrote candidate-{name}[-butter].svg")


if __name__ == "__main__":
    main()
    colourways()
