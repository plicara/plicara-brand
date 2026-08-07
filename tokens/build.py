"""Generate tokens.json, including the full contrast matrix.

The palette lives here and in tokens.css; docs/brand.md is the prose that
explains it. Change all three together.

    python3 build.py

Contrast is WCAG 2.1 relative luminance. Every pairing the brand sanctions for
text clears AA (4.5:1); the pairs that fail are ground-on-ground combinations
that are never text, plus signal on a light ground, which is the reason for the
"signal is a fill, not an ink" rule.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

PALETTE = {
    "lichen":  ("#C2DC2F", "The one hot colour. A fill, never an ink. Pantone 584 C is the closest solid coated match."),
    "ink":     ("#0C1110", "Near-black with a green cast. Primary dark ground; primary text on light."),
    "basalt":  ("#171E1A", "Raised surface on ink. Tiles, table rows, code blocks."),
    "moss":    ("#39441F", "Deep olive. Model cards and editorial panels. A ground, not a second accent."),
    "alpine":  ("#12688F", "Glacier-lake blue. Second ground and the anchor for chart series."),
    "scree":   ("#8C9689", "Grey with a green bias. Secondary text, rules, axis labels."),
    "glacier": ("#9CC7D8", "Pale cyan. Second chart series and recessive detail."),
    "paper":   ("#F2F3EC", "Warm off-white. Light ground; primary text on dark."),
    "white":   ("#FFFFFF", "Surfaces on the light ground."),
    "shadow":  ("#414A6B", "Atlas: Imhof's shadow violet. Accent ink on the warm light ground."),
    "bistre":  ("#7C6A52", "Atlas: rock brown. First chart series on the warm light ground."),
    "ochre":   ("#CE9B45", "Atlas: warm light. Highlight fill."),
    "vellum":  ("#EDE6D6", "Atlas: warm paper ground."),
}

# Four schemes, paired by area of the lab. Glacier/Atlas carry the lab and the
# models; Signal/Field carry benchmarks and tools.
SCHEMES = {
    "glacier": dict(mode="dark", area="lab, models", typeset="warm",
                    bg="#072430", surface="#0E3646", text="#EAF3F5",
                    text_muted="#93B7C4", rule="#17475C", accent="#C2DC2F",
                    accent_on="#0C1110", series_1="#1C7FA8", series_2="#9CC7D8"),
    "atlas":   dict(mode="light", area="lab, models", typeset="warm",
                    bg="#EDE6D6", surface="#F7F3E8", text="#221F1C",
                    text_muted="#5C5340", rule="#D6CBB4", accent="#414A6B",
                    accent_on="#EDE6D6", series_1="#7C6A52", series_2="#BCD4DC"),
    "signal":  dict(mode="dark", area="benchmarks, tools", typeset="technical",
                    bg="#0C1110", surface="#171E1A", text="#F2F3EC",
                    text_muted="#8C9689", rule="#26302A", accent="#C2DC2F",
                    accent_on="#0C1110", series_1="#12688F", series_2="#9CC7D8"),
    "field":   dict(mode="light", area="benchmarks, tools", typeset="technical",
                    bg="#F2F3EC", surface="#FFFFFF", text="#0C1110",
                    text_muted="#5D665C", rule="#D6D9CE", accent="#39441F",
                    accent_on="#F2F3EC", series_1="#12688F", series_2="#39441F"),
}

# Both typesets set headings in sentence case; uppercase belongs to the mono
# label role alone. Both declare "case" explicitly — one declaring and one
# silent is how this drifted the first time.
TYPESETS = {
    "warm": {
        "display": {"family": "Fraunces", "weight": 600,
                    "settings": {"opsz": 96, "SOFT": 24, "WONK": 1},
                    "case": "sentence"},
        "body":    {"family": "Newsreader", "weight": 400, "opsz": 18},
        "data":    {"family": "JetBrains Mono", "weight": 400,
                    "numeric": "tabular-nums"},
        "use": "the lab and the models",
    },
    "technical": {
        "display": {"family": "Archivo", "weight": 800,
                    "settings": {"wght": 800, "wdth": 125}, "case": "sentence"},
        "body":    {"family": "Archivo", "weight": 400, "width": 100},
        "data":    {"family": "JetBrains Mono", "weight": 400,
                    "numeric": "tabular-nums"},
        "use": "benchmarks and tools",
    },
}

GROUNDS = ["ink", "basalt", "moss", "alpine", "paper", "white", "lichen", "vellum"]

# Hot fills and their text guards. A fill is a colour that holds text but must
# never set it; the on-colour is the only ink allowed on top of it. The lichen
# fill is also the standing exception to "one accent per scheme" — it stays
# constant in every scheme, including Atlas.
FILLS = {
    "lichen": {"on": "ink", "standing_exception": True},
    "ochre":  {"on": "ink", "standing_exception": False},
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
