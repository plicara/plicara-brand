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
SUMI = "#26292B"    # cool near-black
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
    # The REDUCED CUT of the adopted mark, for below ~24 px. The back range
    # is dropped and the line carries more weight: at tile sizes the rear
    # peaks collapse into the front ones and the drawing turns to mush. Same
    # front profile, fewer lines — not a different mark.
    "e3r-foothills-reduced": {
        "tilt": 0,
        "amp": 0.35,
        "closed": [[(8, 74), (20, 44), (33, 58), (50, 28), (67, 52),
                    (81, 42), (92, 74)]],
        "open": [
            [(20, 44), (28, 74)],
            [(50, 28), (59, 74)],
            [(81, 42), (87, 74)],
        ],
        "note": "foothills refolded, reduced cut: front range only, for < 24 px",
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
    # chalk palette (2026-08-10): the live set
    "rose": "#EE93A9", "butterscotch": "#E7A63E", "emerald": "#2F6E70",
    "duckegg": "#CBDFD4", "smoke": "#9DACBA", "mist": "#DCE6E6",
    "plum": "#8E4763", "sumi": "#26292B", "chalk": "#EDF1F0",
    # beetle card (2026-08-10), from the founder's jewel-bug reference.
    # Four hues only, which cannot supply both grounds, so three are derived
    # in LCh from the card itself and recorded as derived, not invented:
    #   seafoam = jade at L*85, chroma x0.45   (a back range must recede)
    #   fern    = moss at L*72, chroma x0.70   (alternate back range)
    #   shell   = jade at L*95, chroma x0.10   (the line on dark grounds)
    "marigold": "#FF9900", "jade": "#00CC99", "moss": "#597931",
    "forest": "#003300",
    "seafoam": "#A4E1C8", "fern": "#A2B883", "shell": "#E6F4EE",
    # --- harbour card, proposed 2026-08-10 -------------------------------
    # ink, teal, cream, orange, rust. Measured against Anthropic BEFORE
    # building: cream is dE2000 7.2 from their bone (washi, which was
    # rejected, was 2.0) and b* +13.5 against their +4.1 — a golden cream,
    # not a bone. Orange is dE 14.9 from terracotta (coral, rejected, was
    # 12.4). The navy and teal anchor it somewhere they do not go. Clears.
    "ink": "#05192B", "hteal": "#31606D", "cream2": "#FAEBD3",
    "horange": "#EE8B33", "rust": "#6A2A12",
    # derived in LCh from the card above, never picked by eye.
    "paleteal": "#C3D5DA", "sand": "#E2C6BC", "apricot": "#FFCDAA",
    "hslate": "#829AA1",
    # --- paper-process palettes, proposed 2026-08-10 ---------------------
    # Not mood boards. Each set is the native ink palette of a real process
    # for putting colour on paper, which is what this mark depicts.
    "risopink": "#FF48B0", "risoblue": "#3D5588", "risoyellow": "#FFE800",
    "prussian": "#0B3C5D", "cyanmid": "#2E7DA6", "tea": "#D9A441",
    "ditto": "#6B4C9A", "dittofade": "#9B8BC4", "mimeoblue": "#4A6FA5",
    "verdigris": "#3E9C8F", "copper": "#B5713C", "oxide": "#22332F",
    "chartreuse": "#C6DE1E", "graphite": "#14161A", "steel": "#8A94A0",
    # derived: back ranges at L*85-87 and low chroma so they recede, and
    # papers at L*96 carrying a trace of the family's hue. All computed in
    # LCh from the hue above them, never picked by eye.
    "risoback": "#CFD4E9", "cyanoback": "#C3D7E7", "cyanopaper": "#F1F4F7",
    "dittoback": "#DDCFED", "dittopaper": "#F5F3F7", "verdback": "#C0DDD8",
    "acidback": "#D5DAE1", "acidpaper": "#F3F4F5", "risopaper": "#FFFFFF",
    # retired pastel-card hues, kept so the historical colourways still build
    "coral": "#F7A283", "washi": "#FAF6ED", "blush": "#F7DDD3",
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
    "chalk": dict(f=["rose", "butterscotch", "emerald", "rose"],
                  back="duckegg", light="sumi", dark="chalk",
                  note="ADOPTED. rose, butterscotch, emerald facets, "
                       "duck-egg back range: the chalk palette. Rose replaces "
                       "coral to clear terracotta's family; the line on dark "
                       "grounds is cool chalk, not warm washi."),
    # --- harbour ways, proposed 2026-08-10 -------------------------------
    "harbor": dict(f=["hteal", "horange", "hteal", "rust"],
              back="paleteal", light="ink", dark="cream2",
              note="the balanced read: teal shoulders, orange centre, rust cap"),
    "ember": dict(f=["rust", "horange", "hteal", "rust"],
             back="sand", light="ink", dark="cream2",
             note="warm-led: rust outer facets running into teal"),
    "tide": dict(f=["hteal", "hteal", "horange", "hteal"],
            back="paleteal", light="ink", dark="cream2",
            note="a teal mass with one hot facet on the right"),
    "kiln": dict(f=["horange", "rust", "horange", "rust"],
            back="sand", light="ink", dark="cream2",
            note="all warm, no cool facet at all"),
    "beacon": dict(f=["hteal", "rust", "horange", "hteal"],
              back="paleteal", light="ink", dark="cream2",
              note="the heat climbs left to right and stops"),
    "flare": dict(f=["horange", "hteal", "horange", "hteal"],
             back="sand", light="ink", dark="cream2",
             note="strict alternation, maximum temperature swing"),
    "saffron": dict(f=["horange", "horange", "hteal", "horange"],
               back="apricot", light="ink", dark="cream2",
               note="orange-dominant, teal the single cool note"),
    "quay": dict(f=["hslate", "horange", "rust", "hslate"],
            back="paleteal", light="ink", dark="cream2",
            note="the derived mid-slate carries the outer facets"),
    "ballast": dict(f=["hteal", "hslate", "hteal", "hslate"],
               back="paleteal", light="ink", dark="cream2",
               note="cool only: the control, no heat anywhere"),
    "ochre": dict(f=["rust", "horange", "apricot", "rust"],
             back="sand", light="ink", dark="cream2",
             note="one warm family in three values"),
    "dusk": dict(f=["ink", "horange", "hteal", "ink"],
            back="paleteal", light="ink", dark="cream2",
            note="deliberate knockout: ink facets vanish into the dark ground, outlined only"),
    "signal": dict(f=["cream2", "horange", "hteal", "cream2"],
              back="apricot", light="ink", dark="cream2",
              note="deliberate knockout the other way: cream facets read as bare paper on light"),
    # --- paper-process ways, proposed 2026-08-10 ------------------------
    "riso": dict(f=["risopink", "risoyellow", "risoblue", "risopink"],
                 back="risoback", light="risoblue", dark="risopaper",
                 note="Risograph's own inks. The mark is ALREADY drawn as "
                      "flat colour sitting off-register under a line — that "
                      "is a riso misregistration. This names the source "
                      "instead of imitating it. No black: riso has none, so "
                      "the line is federal blue."),
    "cyanotype": dict(f=["cyanmid", "tea", "prussian", "cyanmid"],
                      back="cyanoback", light="prussian", dark="cyanopaper",
                      note="the blueprint process, which is a PAPER process: "
                           "Prussian blue ground, white line, one tea-toned "
                           "warm. The brand already has a scheme called "
                           "blueprint; this is that scheme taken seriously."),
    "ditto": dict(f=["ditto", "mimeoblue", "dittofade", "ditto"],
                  back="dittoback", light="ditto", dark="dittopaper",
                  note="spirit-duplicator purple — the aniline violet of "
                       "school handouts. One hue family, three values, no "
                       "hot accent at all. The quietest option here."),
    "verdigris": dict(f=["verdigris", "copper", "verdigris", "oxide"],
                      back="verdback", light="oxide", dark="verdback",
                      note="oxidised copper: patina green against raw metal. "
                           "Warm and cool from one material aging."),
    "acid": dict(f=["chartreuse", "steel", "chartreuse", "steel"],
                 back="acidback", light="graphite", dark="acidpaper",
                 note="near-black, one acid chartreuse, cool grey between. "
                      "Two colours doing all the work; loud in exactly one "
                      "place."),
    # --- beetle card, proposed 2026-08-10 -------------------------------
    # Far more saturated than chalk. Read the audit before adopting one.
    "beetle": dict(f=["marigold", "jade", "moss", "marigold"],
                   back="seafoam", light="forest", dark="shell",
                   note="the literal read of the reference: hot marigold "
                        "outer facets, jade centre, moss under the tall peak"),
    "carapace": dict(f=["jade", "marigold", "jade", "moss"],
                     back="fern", light="forest", dark="shell",
                     note="jade-forward, marigold as the single hot facet — "
                          "closest to the beetle's actual proportions"),
    "elytra": dict(f=["moss", "marigold", "jade", "moss"],
                   back="seafoam", light="forest", dark="shell",
                   note="moss-dominant, the quietest of the four"),
    "scarab": dict(f=["jade", "jade", "marigold", "jade"],
                   back="moss", light="forest", dark="shell",
                   note="a jade shell with one marigold marking, the way the "
                        "insect is actually coloured"),
    "seaglass": dict(f=["coral", "butterscotch", "emerald", "coral"],
                     back="duckegg", light="sumi", dark="washi",
                     note="retired 2026-08-10 — coral and washi read as "
                          "Anthropic's cream-and-terracotta pairing"),
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


def colourway_reduced(way="chalk"):
    """The adopted colourway on the REDUCED cut, for tiles below ~24 px.

    Front range only and a heavier line. The favicon and touch icon use this;
    at tile sizes the back range collapses into the front one and the whole
    drawing turns to mush.
    """
    cand = CANDIDATES["e3r-foothills-reduced"]
    name = "e3r-foothills-reduced"
    cfg = COLOURWAYS[way]
    ds = _paths(cand, name)
    stroke = STROKE * 1.5
    for ground, linecol in (("", cfg["light"]), ("-dark", cfg["dark"])):
        parts = []
        for i, poly in enumerate(E3_FACETS):
            pts = _wobble(poly, f"{name}-f{i}", amplitude=0.3, closed=True)
            d = _smooth(_tx(pts, cand["tilt"]), closed=True)
            parts.append(f'<path d="{d}" fill="{PAL[cfg["f"][i]]}" '
                         f'stroke="none" transform="translate(13 10)"/>')
        parts.append(f'<g fill="none" stroke="{PAL[linecol]}" '
                     f'stroke-width="{stroke}" stroke-linecap="round" '
                     f'stroke-linejoin="round">'
                     + "".join(f'<path d="{d}"/>' for d in ds) + "</g>")
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" '
               f'viewBox="0 0 {VIEW:.0f} {VIEW:.0f}" role="img" '
               f'aria-label="Foothills Labs — reduced cut">\n'
               + "\n".join(parts) + "\n</svg>\n")
        with open(os.path.join(OUT, f"mark-foothills-{way}-reduced{ground}.svg"),
                  "w") as fh:
            fh.write(svg)
    print(f"wrote mark-foothills-{way}-reduced[-dark].svg")


if __name__ == "__main__":
    main()
    colourways()
    colourway_reduced()
