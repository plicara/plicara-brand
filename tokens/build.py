"""Generate tokens.json, including the full contrast matrix.

The palette lives here and in tokens.css; docs/brand.md is the prose that
explains it. Change all three together.

    python3 build.py

Contrast is WCAG 2.1 relative luminance. Every pairing the brand sanctions for
text clears AA (4.5:1) — including the accent on a raised surface, which the
previous palette missed. The pairs that fail are ground-on-ground combinations
that are never text, plus the pastel fills on light grounds, which is the
reason for the "a pastel is a fill, not an ink" rule.
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

# The HARBOUR palette. Descended from the founder's pastel card, with two
# deliberate moves away from Anthropic's identity, which pairs a warm cream
# ground with a terracotta accent (docs/brand.md logs the measurements):
#
#   1. The IDENTITY WARM is a golden cream, not a bone: b* +13.5 against
#      their +4.1, dE2000 7.2 from their bone where the pastel card's cream
#      was 2.0 — below what a viewer can resolve. Page-ground duty moved to
#      PAPER (2026-08-23): the same cast at 60% of the saturation and 3 L*
#      lighter, after the full-strength cream proved a glaring reading
#      surface. Paper is dE2000 3.8 from their bone — nearer than cream,
#      still resolvable, and the accent and artwork that made the pastel
#      adjacency an accident no longer travel with it.
#   2. The warm accent is RUST, not coral. Rust is dE2000 14.9 from
#      terracotta; the coral it replaces was 12.4, the same family.
#
# Orange, duck egg and smoke came through from the card unchanged —
# none of them is anywhere near Anthropic's palette. Night/slate,
# print/drafting and apricot are DERIVED: dark grounds and a light-ground
# series ink a six-pastel card cannot supply.
PALETTE = {
    "orange": ("#EE8B33", "The one hot colour, and the accent INK of the dark schemes only. On the paper ground it manages 2.3:1, so on light grounds it is a fill and nothing else — that asymmetry is the reason the guard token exists."),
    "rust":         ("#6A2A12", "Burnt rust. The accent ink on light grounds (9.9:1 on paper) and a facet of the mark. Keeps the token name so nothing downstream has to move."),
    "cream":        ("#FAEBD3", "The identity warm, b* +13.5 — a golden cream, deliberately not a bone: Anthropic's is +4.1. Text on the dark grounds, the guard on rust, and the avatar ground. No longer the page ground; that is paper."),
    "paper":        ("#FDF5E6", "The light ground: the cream's cast at 60% of the saturation (b* +8.2) and 3 L* lighter. Took over page duty from the full-strength cream, which glared at page size (2026-08-23). dE2000 3.8 from Anthropic's bone — above the 2.0 a viewer can resolve."),
    "white":        ("#FFFFFF", "Ground of notepad."),
    "mist":         ("#DEEAEE", "Raised cool surface on white. Tiles, table rows, code blocks."),
    "duckegg":      ("#9ABCC6", "Pale teal. First chart series on the dark grounds."),
    "smoke":        ("#829AA1", "Derived mid. Recessive detail and rules; never body text."),
    "teal":      ("#31606D", "The cool counterweight. Chart series on light grounds; a panel ground on dark."),
    "apricot":         ("#FFB881", "Derived: the hot colour lifted. Second chart series on the dark grounds."),
    "sumi":         ("#05192B", "Near-black navy. Primary text on light; the outline colour of every drawing."),
    "night":        ("#05192B", "The primary dark ground. Same value as sumi: the ink and the ground are one colour, which is what makes the cream sit so far forward."),
    "slate":        ("#132538", "Raised surface on night."),
    "print":        ("#082C35", "Deep teal. Dark ground for benchmarks and tools."),
    "drafting":     ("#1D3E47", "Raised surface on print. Sits at L*24 and no higher: the accent has to clear 4.5 on top of it."),
    "warmwhite":    ("#FFFDF9", "Raised surface on the paper ground. Lighter than the paper, not whiter than it — retuned with the ground, or the two would sit 1 L* apart and every tile would vanish."),
}

# Four schemes, paired by area of the lab. Twilight/Cel carry the lab and the
# models; Blueprint/Notepad carry benchmarks and tools.
SCHEMES = {
    "twilight":  dict(mode="dark", area="lab, models", typeset="warm",
                      bg="#05192B", surface="#132538", text="#FAEBD3",
                      text_muted="#9CB5BC", rule="#25364A", accent="#EE8B33",
                      accent_on="#05192B", series_1="#9ABCC6", series_2="#FFB881",
                      panels=["teal", "rust"]),
    "cel":       dict(mode="light", area="lab, models", typeset="warm",
                      bg="#FDF5E6", surface="#FFFDF9", text="#05192B",
                      text_muted="#436974", rule="#E5D5BB", accent="#6A2A12",
                      accent_on="#FAEBD3", series_1="#31606D", series_2="#6A2A12"),
    "blueprint": dict(mode="dark", area="benchmarks, tools", typeset="technical",
                      bg="#082C35", surface="#1D3E47", text="#FFFFFF",
                      text_muted="#9CB5BC", rule="#395760", accent="#EE8B33",
                      accent_on="#05192B", series_1="#FFB881", series_2="#9ABCC6"),
    "notepad":   dict(mode="light", area="benchmarks, tools", typeset="technical",
                      bg="#FFFFFF", surface="#DEEAEE", text="#05192B",
                      text_muted="#436974", rule="#CADADF", accent="#6A2A12",
                      accent_on="#FAEBD3", series_1="#31606D", series_2="#6A2A12"),
}

# Both typesets set headings in lowercase; uppercase belongs to the mono
# label role alone. Both declare "case" explicitly — one declaring and one
# silent is how this drifted the first time.
TYPESETS = {
    "warm": {
        "display": {"family": "Fraunces", "weight": 600,
                    "settings": {"opsz": 96, "SOFT": 24, "WONK": 1},
                    "case": "lower"},
        "body":    {"family": "Newsreader", "weight": 400, "opsz": 18},
        "data":    {"family": "JetBrains Mono", "weight": 400,
                    "numeric": "tabular-nums"},
        "use": "the lab and the models",
    },
    "technical": {
        "display": {"family": "Archivo", "weight": 800,
                    "settings": {"wght": 800, "wdth": 125}, "case": "lower"},
        "body":    {"family": "Archivo", "weight": 400, "width": 100},
        "data":    {"family": "JetBrains Mono", "weight": 400,
                    "numeric": "tabular-nums"},
        "use": "benchmarks and tools",
    },
}

GROUNDS = ["night", "slate", "print", "drafting", "paper", "cream", "white", "mist",
           "duckegg", "teal", "rust", "orange"]

# Hot fills and their text guards. A fill is a colour that holds text but must
# never set it; the on-colour is the only ink allowed on top of it. The
# orange fill is also the standing exception to "one accent per scheme" —
# it stays constant in every scheme, including Cel and Notepad, whose accent
# ink is rust.
FILLS = {
    "orange": {"on": "sumi", "standing_exception": True},
    "rust":         {"on": "cream", "standing_exception": False},
}

# Pairings the brand sanctions for text, checked per scheme. The accent is
# included at body threshold on purpose: it is documented as an *ink*, so a
# link set in it on a raised tile has to clear 4.5 like any other text.
TEXT_ROLES = {"text": 4.5, "text_muted": 4.5, "accent": 4.5}
SERIES_ROLES = {"series_1": 3.0, "series_2": 3.0}


def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_colour):
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    return round((max(la, lb) + 0.05) / (min(la, lb) + 0.05), 2)


def audit_css():
    """Check tokens.css against this file — the two drift, and it ships.

    tokens.json is generated from here; tokens.css is written by hand. Nothing
    used to compare them, so the audit could pass with every sanctioned pairing
    clear while the CSS that browsers actually load said something else.

    That is not hypothetical. The harbour repaint moved rust from a pale pink
    to a burnt rust and correctly set FILLS["rust"]["on"] = cream here, but
    tokens.css kept `--pl-on-rust: #05192B` from when rust was pink — near-black
    text on rust, 1.65:1, shipped and audited green.

    Checks the flat `--pl-<name>` declarations and the `--pl-on-<fill>` guards.
    Scheme blocks are var() indirections and are left to the pairing audit.
    """
    path = os.path.join(HERE, "tokens.css")
    if not os.path.exists(path):
        return ["tokens.css is missing"]
    css = open(path).read()
    bad = []
    for name, (value, _) in PALETTE.items():
        m = re.search(rf"^\s*--pl-{re.escape(name)}:\s*(#[0-9A-Fa-f]{{6}})\s*;",
                      css, re.M)
        if m and m.group(1).upper() != value.upper():
            bad.append(f"tokens.css --pl-{name}={m.group(1)} but palette says {value}")
    for fill, cfg in FILLS.items():
        want = PALETTE[cfg["on"]][0]
        m = re.search(rf"^\s*--pl-on-{re.escape(fill)}:\s*(#[0-9A-Fa-f]{{6}})\s*;",
                      css, re.M)
        if not m:
            bad.append(f"tokens.css has no --pl-on-{fill} guard")
        elif m.group(1).upper() != want.upper():
            got = m.group(1)
            bad.append(f"tokens.css --pl-on-{fill}={got} ({contrast(got, PALETTE[fill][0])}:1) "
                       f"but the guard is {cfg['on']} {want} "
                       f"({contrast(want, PALETTE[fill][0])}:1)")
    return bad


def audit():
    """Every sanctioned pairing, checked. Returns a list of failures."""
    bad = []
    for name, sc in SCHEMES.items():
        for ground in ("bg", "surface"):
            for role, need in {**TEXT_ROLES, **SERIES_ROLES}.items():
                r = contrast(sc[role], sc[ground])
                if r < need:
                    bad.append(f"{name}.{role}_on_{ground}={r} (needs {need})")
    for fill, cfg in FILLS.items():
        r = contrast(PALETTE[fill][0], PALETTE[cfg["on"]][0])
        if r < 4.5:
            bad.append(f"fill {fill} holds {cfg['on']} at only {r}")
    return bad + audit_css()


def build():
    tokens = {
        "$schema": "https://design-tokens.github.io/community-group/format/",
        "meta": {
            "name": "Plicara Labs",
            "source": "docs/brand.md",
            "note": "Generated by tokens/build.py. Edit docs/brand.md, then regenerate.",
            "palette": "harbour",
            "colourway": "beacon",
        },
        "color": {k: {"value": v[0], "comment": v[1]} for k, v in PALETTE.items()},
        "contrast": {},
        "font": {
            "display": {"value": "Fraunces",
                        "comment": "Variable: opsz 9-144, wght 100-900, SOFT, WONK. SIL OFL."},
            "body": {"value": "Newsreader",
                     "comment": "Variable: wght 200-800, opsz 6-72. SIL OFL."},
            "sans": {"value": "Archivo",
                     "comment": "Variable: wght 100-900, wdth 62-125. SIL OFL."},
            "mono": {"value": "JetBrains Mono",
                     "comment": "Apache-2.0. Shared by both typesets — the through-line."},
        },
        "scheme": SCHEMES,
        "typeset": TYPESETS,
        "fill": {
            name: {
                "value": PALETTE[name][0],
                "on": PALETTE[cfg["on"]][0],
                "on_ratio": contrast(PALETTE[name][0], PALETTE[cfg["on"]][0]),
                "standing_exception": cfg["standing_exception"],
            }
            for name, cfg in FILLS.items()
        },
    }

    # Contrast per scheme, generated so the guide never asserts a stale number.
    tokens["scheme_contrast"] = {}
    for name, sc in SCHEMES.items():
        tokens["scheme_contrast"][name] = {
            f"{fg}_on_{ground}": {
                "ratio": contrast(sc[fg], sc[ground]),
                "aa_body": contrast(sc[fg], sc[ground]) >= 4.5,
            }
            for ground in ("bg", "surface")
            for fg in ("text", "text_muted", "accent", "series_1", "series_2")
        }

    for fg in PALETTE:
        row = {}
        for bg in GROUNDS:
            if fg == bg:
                continue
            r = contrast(PALETTE[fg][0], PALETTE[bg][0])
            row[bg] = {"ratio": r, "aa_body": r >= 4.5, "aa_large": r >= 3.0}
        tokens["contrast"][fg] = row

    failures = audit()
    tokens["meta"]["audit"] = "all sanctioned pairings clear AA" if not failures else failures

    path = os.path.join(HERE, "tokens.json")
    with open(path, "w") as fh:
        json.dump(tokens, fh, indent=2)
        fh.write("\n")
    print(f"wrote {path}")
    if failures:
        print("AUDIT FAILURES:")
        for f in failures:
            print("  " + f)
    else:
        print("audit: every sanctioned pairing clears AA")
    return tokens


if __name__ == "__main__":
    build()
