"""Generate the paper-plane glyphs for the Foothills Labs model family.

The rule, and the whole point of the system:

    Each model is a paper plane, drawn simply: a top view, a thick sumi
    outline, and a butter fill that sits deliberately off-register — the
    loose screen-print look of the illustration style. The drawings are
    stylised, not fold diagrams; charm is the point, complexity is not.

    glider < delta < canard < hammer, by capability tier.

Nothing here is hand-edited SVG. The geometry is authored below as clean
symmetric polygons; the hand-drawn character — the wobble in the line — is
applied by deterministic low-frequency noise, seeded per glyph, so re-running
this script always produces byte-identical output. Change the code, not the
files.

Outputs, per plane:
    plane-{name}.svg        sumi outline + butter fill, for light grounds
    plane-{name}-dark.svg   washi outline + butter fill, for dark grounds
    plane-{name}-small.svg  heavier line, centre fold only, for < 40 px
    plane-{name}-mono.svg   currentColor outline, no fill, for CSS styling

plus glyphs.json, the family metadata.
"""

import json
import math
import os

OUT = os.path.dirname(os.path.abspath(__file__))

SUMI = "#2B2422"
WASHI = "#FAF6ED"
BUTTER = "#F3DC7C"

VIEW = 512.0           # artboard
STROKE = 17.0          # main outline, ~3.3% of the artboard
STROKE_FOLD = 11.0     # interior fold lines
STROKE_SMALL = 30.0    # reduced cut
OFFSET = (14.0, 11.0)  # butter fill misregistration, in artboard units
TILT = -7.0            # degrees; the whole drawing sits slightly nose-up

# --- geometry -------------------------------------------------------------
# Design space is 0..100, y down, nose at the top, centre line at x = 50.
# Each plane gives the RIGHT half of its silhouette from nose to tail;
# the left half is mirrored. Fold lines are given whole.

PLANES = {
    # The trainer. Wide span, gentle lines, the biggest wing area.
    "glider": {
        "tier": 1,
        "half": [(50, 16), (60, 28), (94, 56), (96, 68), (91, 71),
                 (60, 66), (57, 84), (50, 86)],
        "folds": [
            [(50, 16), (50, 86)],
            [(56, 30), (59, 66)],
            [(44, 30), (41, 66)],
        ],
        "note": "wide span, gentle sweep — the plane that stays up",
    },
    # The classic wide triangle; fast, direct, nearly all wing.
    "delta": {
        "tier": 2,
        "half": [(50, 8), (93, 80), (92, 86), (52, 76), (50, 76)],
        "folds": [
            [(50, 8), (50, 76)],
            [(50, 12), (63, 80)],
            [(50, 12), (37, 80)],
        ],
        "note": "one triangle, no waste — nearly all wing",
    },
    # Fore-planes ahead of the main wing; the unusual silhouette.
    "canard": {
        "tier": 3,
        "half": [(50, 8), (56, 18), (71, 26), (58, 34), (57, 44),
                 (89, 72), (90, 82), (58, 76), (55, 92), (50, 93)],
        "folds": [
            [(50, 8), (50, 93)],
            [(54, 20), (56, 44)],
            [(46, 20), (44, 44)],
            [(56, 48), (60, 74)],
            [(44, 48), (40, 74)],
        ],
        "note": "small wings forward, big wing aft — steers before it glides",
    },
    # The heavy one. Blunt locked nose, short broad wings, dense folds.
    "hammer": {
        "tier": 4,
        "half": [(50, 14), (63, 15), (70, 22), (72, 36), (91, 62),
                 (92, 74), (60, 66), (57, 86), (50, 88)],
        "folds": [
            [(50, 14), (50, 88)],
            [(38, 18), (62, 18)],
            [(35, 30), (65, 30)],
            [(57, 34), (60, 64)],
            [(43, 34), (40, 64)],
        ],
        "note": "a locked, weighted nose — the most folds, the longest throw",
    },
}


# --- the hand in the line ---------------------------------------------------

def _seed(name):
    return sum(ord(c) * (i + 7) for i, c in enumerate(name))


def _wobble_polyline(pts, name, amplitude=0.7, step=3.0, closed=False):
    """Resample a polyline and push points off the line with smooth noise.

    Deterministic: the phases come from the glyph name, never from a RNG
    state, so output is byte-stable across runs and machines.
    """
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
        if i == 0 or (not closed and i == total):
            w = 0.0
        j = (i + 1) % total
        k = (i - 1) % total
        tx, ty = dense[j][0] - dense[k][0], dense[j][1] - dense[k][1]
        tl = math.hypot(tx, ty) or 1.0
        out.append((x - ty / tl * w, y + tx / tl * w))
    return out


def _smooth_path(pts, closed=False):
    """Catmull-Rom through the points, emitted as cubic beziers."""

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


# --- assembly ---------------------------------------------------------------

def _transform(pts):
    """Design space (0..100) -> artboard (512), tilted around the centre."""
    a = math.radians(TILT)
    c, s = math.cos(a), math.sin(a)
    out = []
    for x, y in pts:
        dx, dy = x - 50.0, y - 50.0
        rx, ry = dx * c - dy * s, dx * s + dy * c
        out.append(((rx + 50.0) * VIEW / 100.0, (ry + 50.0) * VIEW / 100.0))
    return out


def _silhouette(plane, name, amplitude=0.7):
    half = plane["half"]
    mirrored = [(100.0 - x, y) for x, y in reversed(half)
                if abs(x - 50.0) > 1e-9]
    outline = half + mirrored
    return _smooth_path(_transform(
        _wobble_polyline(outline, name, amplitude=amplitude, closed=True)),
        closed=True)


def _fold_paths(plane, name, amplitude=0.45):
    out = []
    for i, line in enumerate(plane["folds"]):
        pts = _wobble_polyline(line, f"{name}-fold-{i}", amplitude=amplitude,
                               step=4.0)
        out.append(_smooth_path(_transform(pts)))
    return out


def _svg(body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {VIEW:.0f} {VIEW:.0f}" role="img" '
            f'aria-label="{title}">\n{body}\n</svg>\n')


def _stroke_attrs(width, colour):
    return (f'fill="none" stroke="{colour}" stroke-width="{width:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round"')


def glyph(name, plane, ink, with_fill=True, small=False):
    amp = 0.9 if small else 0.7
    sil = _silhouette(plane, name, amplitude=amp)
    parts = []
    if with_fill:
        dx, dy = (0.0, 0.0) if small else OFFSET
        parts.append(f'  <path d="{sil}" fill="{BUTTER}" stroke="none" '
                     f'transform="translate({dx:.0f} {dy:.0f})"/>')
    w = STROKE_SMALL if small else STROKE
    parts.append(f'  <path d="{sil}" {_stroke_attrs(w, ink)}/>')
    folds = _fold_paths(plane, name)
    keep = folds[:1] if small else folds
    fw = STROKE_SMALL * 0.62 if small else STROKE_FOLD
    for d in keep:
        parts.append(f'  <path d="{d}" {_stroke_attrs(fw, ink)}/>')
    title = f"{name} — Foothills Labs model glyph"
    return _svg("\n".join(parts), title)


def main():
    meta = {}
    for name, plane in sorted(PLANES.items(), key=lambda kv: kv[1]["tier"]):
        files = {
            f"plane-{name}.svg": glyph(name, plane, SUMI),
            f"plane-{name}-dark.svg": glyph(name, plane, WASHI),
            f"plane-{name}-small.svg": glyph(name, plane, SUMI, small=True),
            f"plane-{name}-mono.svg": glyph(name, plane, "currentColor",
                                            with_fill=False),
        }
        for fn, svg in files.items():
            with open(os.path.join(OUT, fn), "w") as fh:
                fh.write(svg)
        meta[name] = {
            "tier": plane["tier"],
            "note": plane["note"],
            "files": sorted(files),
        }
        print(f"wrote plane-{name}[-dark|-small|-mono].svg")

    with open(os.path.join(OUT, "glyphs.json"), "w") as fh:
        json.dump({
            "family": "paper planes",
            "order": "tier — glider < delta < canard < hammer",
            "regional_axis": "a specialised model takes the plane's name in "
                             "the language of its specialisation: hammer -> "
                             "martillo (Spanish)",
            "checkpoints": "pre-release checkpoints are {name}-preview",
            "style": "thick sumi outline, butter fill set off-register; "
                     "drawn by this script, never by hand",
            "glyphs": meta,
        }, fh, indent=2)
        fh.write("\n")
    print("wrote glyphs.json")


if __name__ == "__main__":
    main()
