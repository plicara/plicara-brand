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

HERE = os.path.dirname(os.path.abspath(__file__))

# The CHALK palette. Descended from the founder's pastel card, with two
# deliberate moves away from Anthropic's identity, which pairs a warm cream
# ground with a terracotta accent:
#
#   1. The paper is COOL. Chalk sits at b* 0.0 on the yellow-blue axis;
#      the warm cream it replaces sat at +4.8, against Anthropic's +4.1 —
#      close enough (dE2000 2.0) that no viewer could separate them.
#   2. The warm accent is ROSE, not coral. Rose is dE2000 20 from
#      terracotta; the coral it replaces was 11.5, the same family.
#
# Butterscotch, duck egg and smoke came through from the card unchanged —
# none of them is anywhere near Anthropic's palette. Night/slate,
# print/drafting and plum are DERIVED: dark grounds and a light-ground
# series ink a six-pastel card cannot supply.
PALETTE = {
    "butterscotch": ("#E7A63E", "The one hot colour. A fill, never an ink. The glyph fill and the accent of both dark schemes."),
    "rose":         ("#EE93A9", "Cool-leaning pink. A fill and a panel ground; never an ink. Replaces the card's coral, which sat in terracotta's family."),
    "chalk":        ("#EDF1F0", "Cool paper white. The light ground, and text on the dark ones."),
    "white":        ("#FFFFFF", "Ground of notepad; surfaces on chalk."),
    "mist":         ("#DCE6E6", "Raised cool surface. Tiles, table rows, code blocks."),
    "duckegg":      ("#CBDFD4", "Pale green. Second chart series on the dark grounds."),
    "smoke":        ("#9DACBA", "Blue-grey. Recessive detail and rules; never body text."),
    "emerald":      ("#2F6E70", "Emerald sea, darkened for ink duty. The accent ink on light grounds; a panel ground on dark."),
    "plum":         ("#8E4763", "Derived: rose fired dark. Second chart series on the light grounds."),
    "sumi":         ("#26292B", "Cool near-black, like ink that has dried. Primary text on light; the outline colour of every drawing."),
    "night":        ("#1E3C40", "Derived from emerald sea: deep water. Primary dark ground."),
    "slate":        ("#23464A", "Raised surface on night."),
    "print":        ("#2E3A42", "Derived from smoke: smoked slate. Dark ground for benchmarks and tools."),
    "drafting":     ("#38444C", "Raised surface on print."),
}

# Four schemes, paired by area of the lab. Twilight/Cel carry the lab and the
# models; Blueprint/Notepad carry benchmarks and tools.
SCHEMES = {
    "twilight":  dict(mode="dark", area="lab, models", typeset="warm",
                      bg="#1E3C40", surface="#23464A", text="#EDF1F0",
                      text_muted="#A7C4C2", rule="#33585C", accent="#E7A63E",
                      accent_on="#26292B", series_1="#EE93A9", series_2="#CBDFD4",
                      panels=["emerald", "rose"]),
    "cel":       dict(mode="light", area="lab, models", typeset="warm",
                      bg="#EDF1F0", surface="#FFFFFF", text="#26292B",
                      text_muted="#5C6668", rule="#DBE4E3", accent="#2F6E70",
                      accent_on="#FFFFFF", series_1="#2F6E70", series_2="#8E4763"),
    "blueprint": dict(mode="dark", area="benchmarks, tools", typeset="technical",
                      bg="#2E3A42", surface="#38444C", text="#FFFFFF",
                      text_muted="#AEBCC6", rule="#46525B", accent="#E7A63E",
                      accent_on="#26292B", series_1="#CBDFD4", series_2="#EE93A9"),
    "notepad":   dict(mode="light", area="benchmarks, tools", typeset="technical",
                      bg="#FFFFFF", surface="#DCE6E6", text="#26292B",
                      text_muted="#4F5A5C", rule="#C9D8D8", accent="#2F6E70",
                      accent_on="#FFFFFF", series_1="#2F6E70", series_2="#8E4763"),
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

GROUNDS = ["night", "slate", "print", "drafting", "chalk", "white", "mist",
           "duckegg", "emerald", "rose", "butterscotch"]

# Hot fills and their text guards. A fill is a colour that holds text but must
# never set it; the on-colour is the only ink allowed on top of it. The
# butterscotch fill is also the standing exception to "one accent per scheme" —
# it stays constant in every scheme, including Cel and Notepad, whose accent
# ink is emerald.
FILLS = {
    "butterscotch": {"on": "sumi", "standing_exception": True},
    "rose":         {"on": "sumi", "standing_exception": False},
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
    return bad


def build():
    tokens = {
        "$schema": "https://design-tokens.github.io/community-group/format/",
        "meta": {
            "name": "Foothills Labs",
            "source": "docs/brand.md",
            "note": "Generated by assets/tokens/build.py. Edit docs/brand.md, then regenerate.",
            "palette": "chalk",
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
