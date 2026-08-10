"""Generate tokens.json, including the full contrast matrix.

The palette lives here and in tokens.css; docs/brand.md is the prose that
explains it. Change all three together.

    python3 build.py

Contrast is WCAG 2.1 relative luminance. Every pairing the brand sanctions for
text clears AA (4.5:1); the pairs that fail are ground-on-ground combinations
that are never text, plus butter on a light ground, which is the reason for the
"butter is a fill, not an ink" rule.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

PALETTE = {
    "butter":   ("#F3DC7C", "The one hot colour. A fill, never an ink. The glyph fill and the accent of both dark schemes."),
    "sumi":     ("#2B2422", "Warm near-black, like ink that has dried. Primary text on light; the outline colour of every drawing."),
    "washi":    ("#FAF6ED", "Warm paper white. Light ground; primary text on dark."),
    "white":    ("#FFFFFF", "Surfaces on the light ground."),
    "cream":    ("#F7EBC9", "Raised warm surface on the light grounds. Tiles, table rows, code blocks."),
    "night":    ("#1F292E", "Green-cast charcoal, a garden at dusk. Primary dark ground."),
    "slate":    ("#2C3A40", "Raised surface on night."),
    "jade":     ("#1B6055", "Deep leaf teal. Panel ground on dark pages; can ink on washi."),
    "plum":     ("#4E2338", "Deep wine. Panel ground on dark pages."),
    "teal":     ("#3EB7C6", "First chart series on the dark grounds."),
    "blossom":  ("#F0A7C0", "Soft pink. Second chart series on night; recessive detail."),
    "magenta":  ("#B92D77", "Deep pink. Accent ink on the warm light ground; on dark grounds a fill, never an ink."),
    "royal":    ("#2F3BB3", "Saturated blue. Accent ink and first series on the light grounds."),
    "mint":     ("#63C6A0", "Green. Second chart series on the blueprint ground."),
    "lilac":    ("#C9A9E2", "Pale violet. Recessive detail on dark grounds."),
    "brick":    ("#A8333A", "Warm red. Second chart series on the light grounds."),
    "print":    ("#1B2E63", "Blueprint blue. Dark ground for benchmarks and tools."),
    "drafting": ("#24397A", "Raised surface on print."),
}

# Four schemes, paired by area of the lab. Twilight/Cel carry the lab and the
# models; Blueprint/Notepad carry benchmarks and tools.
SCHEMES = {
    "twilight":  dict(mode="dark", area="lab, models", typeset="warm",
                      bg="#1F292E", surface="#2C3A40", text="#FAF6ED",
                      text_muted="#A0BAB8", rule="#3B4C50", accent="#F3DC7C",
                      accent_on="#2B2422", series_1="#3EB7C6", series_2="#F0A7C0",
                      panels=["jade", "plum"]),
    "cel":       dict(mode="light", area="lab, models", typeset="warm",
                      bg="#FAF6ED", surface="#FFFFFF", text="#2B2422",
                      text_muted="#6E6259", rule="#E3D8C4", accent="#B92D77",
                      accent_on="#FFFFFF", series_1="#2F3BB3", series_2="#A8333A"),
    "blueprint": dict(mode="dark", area="benchmarks, tools", typeset="technical",
                      bg="#1B2E63", surface="#24397A", text="#FFFFFF",
                      text_muted="#A3B1E3", rule="#35509E", accent="#F3DC7C",
                      accent_on="#2B2422", series_1="#3EB7C6", series_2="#63C6A0"),
    "notepad":   dict(mode="light", area="benchmarks, tools", typeset="technical",
                      bg="#FFFFFF", surface="#F7EBC9", text="#2B2422",
                      text_muted="#6E6259", rule="#E0D7C4", accent="#2F3BB3",
                      accent_on="#FFFFFF", series_1="#2F3BB3", series_2="#B92D77"),
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

GROUNDS = ["night", "slate", "jade", "plum", "print", "drafting", "washi", "white", "cream", "butter"]

# Hot fills and their text guards. A fill is a colour that holds text but must
# never set it; the on-colour is the only ink allowed on top of it. The butter
# fill is also the standing exception to "one accent per scheme" — it stays
# constant in every scheme, including Cel and Notepad, whose accent inks are
# magenta and royal.
FILLS = {
    "butter":  {"on": "sumi", "standing_exception": True},
    # Magenta clears AA as an ink on washi but only 2.62:1 on night — on the
    # dark grounds it is a fill, and the guard is what makes that mechanical.
    "magenta": {"on": "white", "standing_exception": False},
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
