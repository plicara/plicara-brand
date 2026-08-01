"""Generate contour-ring glyphs for the Foothills Labs model family.

The rule, and the whole point of the system:

    Each summit is drawn as an island. Sea level is the frame.
    Contour interval is a constant 1,500 m across the entire family.
    Ring count is therefore elevation / 1,500 — the glyph's complexity
    IS the model's capability tier, by construction, not by decoration.

    Everest gets five rings. Kosciuszko gets one.

Spot heights (the filled dots) mark named summits, as they would on a map.
Mountains with more than one named top get more than one dot — Elbrus's twin
cones, Denali's North and South Peaks, Aconcagua's south summit.

Each mountain is a small synthetic height field shaped to follow the real
mountain's character. Contours come out of marching squares, get resampled to
an even arc length, and are emitted as smooth closed cubic-bezier paths.
"""

import json
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path as MPath

N = 420
CI = 1500.0  # contour interval, metres
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

xs = np.linspace(0.0, 1.0, N)
X, Y = np.meshgrid(xs, xs)


def blob(cx, cy, amp, sx, sy, rot=0.0, p=2.0):
    """Generalised gaussian. p<2 gives a sharp cone, p>2 a flat-topped shield."""
    dx, dy = X - cx, Y - cy
    c, s = math.cos(rot), math.sin(rot)
    u = (dx * c + dy * s) / sx
    v = (-dx * s + dy * c) / sy
    r = np.sqrt(u * u + v * v) + 1e-9
    return amp * np.exp(-(r ** p))


def _blur1d(a, k, axis):
    rad = int(3 * k)
    t = np.arange(-rad, rad + 1)
    w = np.exp(-(t ** 2) / (2.0 * k * k))
    w /= w.sum()
    pad = [(0, 0), (0, 0)]
    pad[axis] = (rad, rad)
    ap = np.pad(a, pad, mode="edge")
    out = np.zeros_like(a)
    for i, wi in enumerate(w):
        sl = [slice(None), slice(None)]
        sl[axis] = slice(i, i + a.shape[axis])
        out += wi * ap[tuple(sl)]
    return out


def noise(seed, scale, amp):
    """Smooth low-frequency field. Kept light — this is a map, not terrain."""
    rng = np.random.default_rng(seed)
    a = rng.normal(size=(N, N))
    a = _blur1d(_blur1d(a, scale, 0), scale, 1)
    a /= np.abs(a).max()
    return amp * a


def resample(poly, n):
    p = np.asarray(poly, dtype=float)
    if np.allclose(p[0], p[-1]):
        p = p[:-1]
    d = np.sqrt(((np.roll(p, -1, axis=0) - p) ** 2).sum(axis=1))
    cum = np.concatenate([[0.0], np.cumsum(d)])
    total = cum[-1]
    if total <= 0:
        return p
    targets = np.linspace(0.0, total, n, endpoint=False)
    idx = np.clip(np.searchsorted(cum, targets, side="right") - 1, 0, len(p) - 1)
    seg = np.where(d[idx] > 0, (targets - cum[idx]) / np.where(d[idx] > 0, d[idx], 1), 0)
    nxt = (idx + 1) % len(p)
    return p[idx] + (p[nxt] - p[idx]) * seg[:, None]


def catmull(pts, prec=2):
    n = len(pts)
    f = lambda v: f"{round(v, prec):g}"
    d = [f"M{f(pts[0][0])} {f(pts[0][1])}"]
    for i in range(n):
        p0, p1, p2, p3 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = p1 + (p2 - p0) / 6.0
        c2 = p2 - (p3 - p1) / 6.0
        d.append(f"C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}")
    d.append("Z")
    return "".join(d)


def polyline(pts, prec=2):
    f = lambda v: f"{round(v, prec):g}"
    return "M" + "L".join(f"{f(x)} {f(y)}" for x, y in pts)


def contours(H, levels, pad=0.06, samples=40, min_pts=24):
    """Contour paths in a 0-100 box, inset by `pad` so nothing touches the edge."""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cs = ax.contour(X, Y, H, levels=levels)
    lo, span = pad * 100.0, (1 - 2 * pad) * 100.0
    out = []
    for lvl in cs.get_paths():
        got = []
        for poly in lvl.to_polygons(closed_only=True):
            if len(poly) < min_pts:
                continue
            n = max(18, min(samples, len(poly) // 3))
            rs = resample(poly, n)
            rs = lo + rs * span
            rs[:, 1] = 100.0 - rs[:, 1]
            got.append(catmull(rs))
        out.append(got)
    plt.close(fig)
    return out


def place(cx, cy, pad=0.06):
    """Map a field coordinate into the same inset 0-100 box."""
    lo, span = pad * 100.0, (1 - 2 * pad) * 100.0
    return round(lo + cx * span, 2), round(100.0 - (lo + cy * span), 2)


# --- the mountains -----------------------------------------------------------
# Fields are stylised, not surveyed. Summit elevations and the named secondary
# tops are real; the shapes follow each mountain's actual character.

def f_everest():
    """Sharp asymmetric pyramid — three ridges off a small, steep summit."""
    h = blob(0.50, 0.52, 1.00, 0.105, 0.098, 0.0, 1.15)
    h += blob(0.655, 0.665, 0.60, 0.235, 0.052, -0.72, 1.35)   # NE ridge
    h += blob(0.325, 0.455, 0.56, 0.215, 0.050, 0.40, 1.35)    # W ridge
    h += blob(0.565, 0.315, 0.52, 0.052, 0.205, 0.10, 1.35)    # SE ridge
    h += blob(0.665, 0.395, 0.20, 0.070, 0.070, 0.0, 1.8)      # South Col
    return h + noise(11, 13, 0.020)


def f_aconcagua():
    """Long massif, main summit north, a distinct south summit below it."""
    h = blob(0.465, 0.615, 1.00, 0.150, 0.165, 0.10, 1.5)
    h += blob(0.545, 0.360, 0.86, 0.120, 0.130, 0.0, 1.55)     # south summit
    h += blob(0.500, 0.490, 0.44, 0.215, 0.230, 0.0, 2.2)      # shared massif
    h += blob(0.285, 0.640, 0.30, 0.150, 0.080, 0.35, 1.9)     # west shoulder
    return h + noise(23, 14, 0.022)


def f_denali():
    """Vast footprint, two named summits, long buttresses off the south side."""
    h = blob(0.470, 0.470, 1.00, 0.135, 0.130, 0.0, 1.5)       # South Peak
    h += blob(0.610, 0.620, 0.93, 0.115, 0.110, 0.0, 1.5)      # North Peak
    h += blob(0.520, 0.530, 0.56, 0.290, 0.265, 0.2, 2.4)      # massif
    h += blob(0.330, 0.335, 0.30, 0.140, 0.105, 0.55, 1.9)     # SW buttress
    return h + noise(31, 14, 0.020)


def f_kilimanjaro():
    """Shield volcano — broad, near-circular, flat-flanked. Mawenzi stands off
    to the east and clears 4,500 m, so it closes its own ring."""
    h = blob(0.455, 0.485, 1.00, 0.235, 0.225, 0.0, 3.0)
    h += blob(0.760, 0.605, 0.62, 0.062, 0.058, 0.0, 1.5)      # Mawenzi
    h += blob(0.255, 0.395, 0.42, 0.075, 0.065, 0.3, 1.8)      # Shira
    return h + noise(43, 15, 0.016)


def f_elbrus():
    """Twin volcanic cones, near-equal, on one shared base."""
    h = blob(0.370, 0.560, 1.00, 0.108, 0.104, 0.0, 1.45)      # west summit
    h += blob(0.625, 0.455, 0.96, 0.104, 0.100, 0.0, 1.45)     # east summit
    h += blob(0.500, 0.505, 0.62, 0.255, 0.215, 0.0, 2.6)      # shared shield
    return h + noise(57, 14, 0.018)


def f_vinson():
    """A long ridge massif — high aspect ratio, summit toward one end."""
    h = blob(0.500, 0.500, 0.66, 0.335, 0.090, 0.42, 2.1)
    h += blob(0.625, 0.585, 1.00, 0.110, 0.078, 0.42, 1.5)     # summit
    h += blob(0.350, 0.420, 0.72, 0.095, 0.070, 0.42, 1.6)     # subsidiary top
    return h + noise(67, 14, 0.018)


def f_kosciuszko():
    """Broad and gentle. One ring, and that is the whole point."""
    h = blob(0.500, 0.500, 1.00, 0.280, 0.255, 0.3, 2.2)
    h += blob(0.610, 0.400, 0.26, 0.150, 0.130, 0.0, 2.2)
    return h + noise(79, 16, 0.026)


def f_siwalik():
    """Foothills. Long parallel ridges, running off the frame — no summit."""
    ridge = Y * 8.4 + 0.35 + 1.25 * np.sin(X * 2.4 + 0.7) + 0.45 * np.sin(X * 5.1)
    h = 0.5 + 0.5 * np.sin(ridge)
    return h + noise(83, 22, 0.22)


MOUNTAINS = [
    dict(key="everest", name="Everest", local="Chomolungma / Sagarmāthā",
         continent="Asia", elev=8849, role="Flagship", field=f_everest,
         dots=[(0.50, 0.52, 3.2)]),
    dict(key="aconcagua", name="Aconcagua", local="Aconcagua",
         continent="South America", elev=6961, role="Spanish-language", field=f_aconcagua,
         dots=[(0.465, 0.615, 3.0), (0.545, 0.360, 2.1)]),
    dict(key="denali", name="Denali", local="Denali (Koyukon)",
         continent="North America", elev=6190, role="Reserved", field=f_denali,
         dots=[(0.470, 0.470, 3.0), (0.610, 0.620, 2.2)]),
    dict(key="kilimanjaro", name="Kilimanjaro", local="Kilimanjaro",
         continent="Africa", elev=5895, role="Fast tier", field=f_kilimanjaro,
         dots=[(0.455, 0.485, 3.0), (0.760, 0.605, 1.9)]),
    dict(key="elbrus", name="Elbrus", local="Elbrus / Mingi Taw",
         continent="Europe", elev=5642, role="Reserved", field=f_elbrus,
         dots=[(0.370, 0.560, 2.7), (0.625, 0.455, 2.7)]),
    dict(key="vinson", name="Vinson", local="Vinson Massif",
         continent="Antarctica", elev=4892, role="Reserved", field=f_vinson,
         dots=[(0.625, 0.585, 2.8), (0.350, 0.420, 2.0)]),
    dict(key="kosciuszko", name="Kosciuszko", local="Kosciuszko / Targangil",
         continent="Oceania", elev=2228, role="Reserved", field=f_kosciuszko,
         dots=[(0.500, 0.500, 3.0)]),
]

STROKE = 2.6


def svg_body(rings, dots):
    body = [f'<path d="{d}"/>' for level in rings for d in level]
    body += [f'<circle cx="{x}" cy="{y}" r="{r}" fill="currentColor" stroke="none"/>'
             for x, y, r in dots]
    return "".join(body)


def wrap(body, stroke=STROKE):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" '
        f'height="100" fill="none" stroke="currentColor" stroke-width="{stroke}" '
        f'stroke-linejoin="round" stroke-linecap="round">{body}</svg>'
    )


data = []
for m in MOUNTAINS:
    H = m["field"]()
    H = (H - H.min()) / (H.max() - H.min()) * m["elev"]   # field in metres
    n_rings = int(m["elev"] // CI)
    levels = [CI * (i + 1) for i in range(n_rings)]
    rings = contours(H, levels)
    dots = [place(x, y) + (r,) for x, y, r in m["dots"]]
    with open(os.path.join(OUT, f"contour-{m['key']}.svg"), "w") as fh:
        fh.write(wrap(svg_body(rings, dots)))
    # Reduced cut for avatars and favicons: outermost ring, summit dots, heavier
    # stroke. Below about 32px the full ring stack fills in and stops reading.
    small_dots = [(x, y, r * 1.5) for x, y, r in dots]
    with open(os.path.join(OUT, f"contour-{m['key']}-small.svg"), "w") as fh:
        fh.write(wrap(svg_body(rings[:1], small_dots), stroke=5.6))
    closed = sum(len(l) for l in rings)
    data.append({**{k: m[k] for k in ("key", "name", "local", "continent", "elev", "role")},
                 "rings": n_rings, "closed": closed, "paths": rings, "dots": dots,
                 "small": [rings[0]], "smallDots": small_dots})
    print(f"{m['name']:12s} {m['elev']:>5} m   rings {n_rings}   closed contours {closed}   dots {len(dots)}")

# Siwalik — open ridge lines, no summit, no dot
Hs = f_siwalik()
Hs = (Hs - Hs.min()) / (Hs.max() - Hs.min())
fig = plt.figure(); ax = fig.add_subplot(111)
cs = ax.contour(X, Y, Hs, levels=[0.46, 0.74])
sw = []
for lp in cs.get_paths():
    verts, codes = lp.vertices, lp.codes
    if codes is None:
        chunks = [verts]
    else:
        starts = np.flatnonzero(codes == MPath.MOVETO)
        bounds = list(starts) + [len(verts)]
        chunks = [verts[a:b] for a, b in zip(bounds, bounds[1:])]
    for poly in chunks:
        if len(poly) < 120:
            continue
        p = np.asarray(poly)
        p = 6.0 + p * 88.0
        p[:, 1] = 100.0 - p[:, 1]
        step = max(1, len(p) // 34)
        sw.append(polyline(p[::step]))
plt.close(fig)
with open(os.path.join(OUT, "contour-siwalik.svg"), "w") as fh:
    fh.write(wrap("".join(f'<path d="{d}"/>' for d in sw)))
print(f"{'Siwalik':12s}     —      ridge lines {len(sw)}")

data.append(dict(key="siwalik", name="Siwalik", local="Śivālik Hills", continent="Asia",
                 elev=None, role="Pre-release", rings=len(sw), closed=0,
                 paths=[sw], dots=[], small=[sw[::2]], smallDots=[]))

with open(os.path.join(OUT, "glyphs.json"), "w") as fh:
    json.dump(data, fh)
print("\nwrote", OUT)
