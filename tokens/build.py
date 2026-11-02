"""Generate tokens.json, including the full contrast matrix.

Since 2026-11 the system is one scheme, cut paper, in two lights (daylight
and lamplight), with one typeset. The harbour palette stays: the drawings
are outlined in its sumi and filled with its orange.

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
    # --- cut paper (2026-11) -------------------------------------------------
    # The single scheme the site now uses everywhere. Flat, bold paper colours
    # on a kraft ground: the colour arrives as cut-paper blocks and the plane
    # glyphs, not as a second scheme for half the lab.
    "kraft":   ("#F4EFE4", "Cut paper's light ground: an unbleached sheet, warmer and greyer than paper."),
    "linen":   ("#FBF8F1", "Raised surface on kraft. Code blocks, table tiles."),
    "ink":     ("#171512", "Warm near-black. Text on kraft and the guard on every light fill."),
    "umber":   ("#1A1714", "Cut paper's dark ground: the same sheet under lamplight."),
    "bark":    ("#2A2520", "Raised surface on umber."),
    "fired":   ("#EE6A26", "The hot block colour: orange fired a step toward vermilion. A fill only (2.7:1 on kraft), and it holds ink, never cream (2.9:1)."),
    "ember":   ("#C9531A", "Fired, darkened until it reads as a chart series on kraft (3.9:1)."),
    "pine":    ("#0E5E50", "Deep green. The accent ink on kraft (6.7:1) and a block colour that holds cream."),
    "sage":    ("#4FB39E", "Pine lifted for the dark ground. First chart series under lamplight."),
    "pink":    ("#EBAAB9", "Soft pink block. Holds ink; second chart series under lamplight."),
    "butter":  ("#F2CF5B", "Butter yellow block. Holds ink."),
    "stone":   ("#CFC8B8", "Neutral paper grey for the not-counted marks in a chart. Never text."),
    "warmwhite":    ("#FFFDF9", "Raised surface on the paper ground. Lighter than the paper, not whiter than it — retuned with the ground, or the two would sit 1 L* apart and every tile would vanish."),
}

# ONE scheme, cut paper, in two lights (2026-11). The four area schemes and
# their two typesets made the site read as two brands; the lab, the essays and
# the benchmarks now share one ground, one ink and one type system. Daylight is
# the default; lamplight follows the reader's OS into dark mode.
SCHEMES = {
    "daylight":  dict(mode="light", area="everything", typeset="cutpaper",
                      bg="#F4EFE4", surface="#FBF8F1", text="#171512",
                      text_muted="#5C554A", rule="#DDD5C4", accent="#0E5E50",
                      accent_on="#FAEBD3", series_1="#0E5E50", series_2="#C9531A"),
    "lamplight": dict(mode="dark", area="everything", typeset="cutpaper",
                      bg="#1A1714", surface="#2A2520", text="#F1EADB",
                      text_muted="#B3A994", rule="#3A332B", accent="#EE8B33",
                      accent_on="#171512", series_1="#4FB39E", series_2="#EBAAB9"),
}

# One typeset. Display and label roles are lowercase; body text keeps its
# capitals. JetBrains Mono stays for figures and code only.
TYPESETS = {
    "cutpaper": {
        "display": {"family": "Hedvig Letters Serif", "weight": 400,
                    "settings": {"opsz": 24}, "case": "lower"},
        "body":    {"family": "Figtree", "weight": 400},
        "label":   {"family": "Figtree", "weight": 600, "case": "lower"},
        "data":    {"family": "JetBrains Mono", "weight": 400,
                    "numeric": "tabular-nums"},
        "use": "the whole site",
    },
}

GROUNDS = ["kraft", "linen", "umber", "bark", "fired", "pine", "pink", "butter",
           "night", "slate", "print", "drafting", "paper", "cream", "white", "mist",
           "duckegg", "teal", "rust", "orange"]

# Hot fills and their text guards. A fill is a colour that holds text but must
# never set it; the on-colour is the only ink allowed on top of it. The
# orange fill is also the standing exception to "one accent per scheme" —
# it stays constant in every scheme, including Cel and Notepad, whose accent
# ink is rust.
FILLS = {
    "orange": {"on": "sumi", "standing_exception": True},
    "rust":         {"on": "cream", "standing_exception": False},
    "fired":   {"on": "ink", "standing_exception": False},
    "pine":    {"on": "cream", "standing_exception": False},
    "pink":    {"on": "ink", "standing_exception": False},
    "butter":  {"on": "ink", "standing_exception": False},
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
            "palette": "harbour + cut paper",
            "scheme": "cut paper (daylight / lamplight)",
            "colourway": "beacon",
        },
        "color": {k: {"value": v[0], "comment": v[1]} for k, v in PALETTE.items()},
        "contrast": {},
        "font": {
            "display": {"value": "Hedvig Letters Serif",
                        "comment": "Variable: opsz 12-24, wght 400. A soft, bookish serif. SIL OFL."},
            "body": {"value": "Figtree",
                     "comment": "Variable: wght 300-900. Geometric sans for body, labels and UI. SIL OFL."},
            "sans": {"value": "Figtree",
                     "comment": "Alias of body, kept so older consumers of --pl-font-sans resolve."},
            "mono": {"value": "JetBrains Mono",
                     "comment": "Apache-2.0. Figures and code only."},
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
