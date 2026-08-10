"""Generate tokens.json, including the full contrast matrix.

The palette lives here and in tokens.css; docs/brand.md is the prose that
explains it. Change all three together.

    python3 build.py

Contrast is WCAG 2.1 relative luminance. Every pairing the brand sanctions for
text clears AA (4.5:1); the pairs that fail are ground-on-ground combinations
that are never text, plus the pastel fills on light grounds, which is the
reason for the "a pastel is a fill, not an ink" rule.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# The six reference colours (coral, blush, butterscotch, smoke, duck egg,
# emerald sea) were sampled from the founder's palette card. Emerald is
# darkened one step so it can serve as the light-scheme accent ink; night,
# slate, print, drafting and clay are DERIVED — dark grounds and a
# light-ground series ink that a six-pastel card cannot supply — and are
# marked as such.
PALETTE = {
    "butterscotch": ("#E7A63E", "The one hot colour. A fill, never an ink. The glyph fill and the accent of both dark schemes."),
    "coral":        ("#F7A283", "Warm pastel. A fill and a panel ground; never an ink."),
    "blush":        ("#F7DDD3", "Pale warm pink. Raised surface on the cel ground."),
    "duckegg":      ("#CBDFD4", "Pale green. Raised surface on notepad; second series on dark."),
    "smoke":        ("#9DACBA", "Blue-grey. Recessive detail and rules; never body text."),
    "emerald":      ("#376F71", "Emerald sea, darkened a step. The accent ink on light grounds; a panel ground on dark."),
    "sumi":         ("#2B2422", "Warm near-black, like ink that has dried. Primary text on light; the outline colour of every drawing."),
    "washi":        ("#FAF6ED", "Warm paper white. Light ground; primary text on dark."),
    "white":        ("#FFFFFF", "Ground of notepad; surfaces on washi."),
    "clay":         ("#B85C40", "Derived: coral fired dark. Second chart series on light grounds."),
    "night":        ("#22474A", "Derived from emerald sea: deep water. Primary dark ground."),
    "slate":        ("#2D5559", "Raised surface on night."),
    "print":        ("#333E48", "Derived from smoke: smoked slate. Dark ground for benchmarks and tools."),
    "drafting":     ("#3E4A55", "Raised surface on print."),
}

# Four schemes, paired by area of the lab. Twilight/Cel carry the lab and the
# models; Blueprint/Notepad carry benchmarks and tools.
SCHEMES = {
    "twilight":  dict(mode="dark", area="lab, models", typeset="warm",
                      bg="#22474A", surface="#2D5559", text="#FAF6ED",
                      text_muted="#AFC9C5", rule="#3B6165", accent="#E7A63E",
                      accent_on="#2B2422", series_1="#F7A283", series_2="#CBDFD4",
                      panels=["emerald", "coral"]),
    "cel":       dict(mode="light", area="lab, models", typeset="warm",
                      bg="#FAF6ED", surface="#FFFFFF", text="#2B2422",
                      text_muted="#6E6259", rule="#E8DCD2", accent="#376F71",
                      accent_on="#FFFFFF", series_1="#376F71", series_2="#B85C40"),
    "blueprint": dict(mode="dark", area="benchmarks, tools", typeset="technical",
                      bg="#333E48", surface="#3E4A55", text="#FFFFFF",
                      text_muted="#AEBCC8", rule="#4C5A66", accent="#E7A63E",
                      accent_on="#2B2422", series_1="#CBDFD4", series_2="#F7A283"),
    "notepad":   dict(mode="light", area="benchmarks, tools", typeset="technical",
                      bg="#FFFFFF", surface="#CBDFD4", text="#2B2422",
                      text_muted="#525E60", rule="#DCE6DE", accent="#376F71",
                      accent_on="#FFFFFF", series_1="#376F71", series_2="#B85C40"),
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

GROUNDS = ["night", "slate", "print", "drafting", "washi", "white", "blush",
           "duckegg", "emerald", "coral", "butterscotch"]

# Hot fills and their text guards. A fill is a colour that holds text but must
# never set it; the on-colour is the only ink allowed on top of it. The
# butterscotch fill is also the standing exception to "one accent per scheme" —
# it stays constant in every scheme, including Cel and Notepad, whose accent
# ink is emerald.
FILLS = {
    "butterscotch": {"on": "sumi", "standing_exception": True},
    # Coral clears nothing as an ink anywhere (1.86:1 on washi) but holds
    # sumi at 7.58:1 — a fill and a panel ground, with the same railing.
    "coral":        {"on": "sumi", "standing_exception": False},
}


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


def build():
    tokens = {
        "$schema": "https://design-tokens.github.io/community-group/format/",
        "meta": {
            "name": "Foothills Labs",
            "source": "docs/brand.md",
            "note": "Generated by assets/tokens/build.py. Edit docs/brand.md, then regenerate.",
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

    path = os.path.join(HERE, "tokens.json")
    with open(path, "w") as fh:
        json.dump(tokens, fh, indent=2)
        fh.write("\n")
    print(f"wrote {path}")
    return tokens


if __name__ == "__main__":
    build()
