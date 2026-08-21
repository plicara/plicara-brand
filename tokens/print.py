"""Match the Plicara Labs palette to print: CIELAB, process CMYK, Pantone.

Screen is the source of truth for this brand — the palette was chosen in sRGB
and the tokens are hex. This script derives the print side of it, and it is
deliberately honest about which parts are measurements and which are
approximations:

    CIELAB          exact, computed from the hex. This is the number to put on
                    a print order. Lab is device-independent, it is what a
                    press operator actually chases, and it does not expire the
                    way a Pantone licence does.
    CMYK            a real ICC separation through a SWOP-class profile, with
                    the round-trip error reported. Where the round-trip DeltaE
                    is large the colour is OUT OF GAMUT for process printing
                    and no CMYK recipe will reach it — say so rather than
                    print a recipe that lies.
    Pantone         nearest neighbours by DeltaE2000, from a community dataset
                    of sRGB approximations of the Solid Coated library. This
                    is a SHORTLIST FOR EYE-MATCHING AGAINST A PHYSICAL GUIDE,
                    not a specification. Pantone's own Lab measurements are
                    licensed and are not in this repository.

Inputs:

    pip install coloraide pillow
    # a CMYK ICC profile; Artifex's open SWOP profile works and is what the
    # committed numbers were generated with:
    #   ghostpdl/iccprofiles/default_cmyk.icc
    # and the Pantone Solid Coated hex list:
    #   github.com/brettapeters/pantones -> pantone-coated.json
    python3 print.py <cmyk.icc> <pantone-coated.json>

Writes print.json beside this file. Regenerate rather than editing it.
"""

import json
import os
import sys

from coloraide import Color
from PIL import Image, ImageCms

HERE = os.path.dirname(os.path.abspath(__file__))

# A curated subset of the token palette plus the mark's facet colours — not
# every token belongs on a press. `role` is why the colour is here at all.
#
# NAMES ARE NOT FREE HERE. This file once called #829AA1 "slate" while the
# token source called it "smoke" and had its own slate at #132538 — one word,
# two colours, and a printer cross-referencing the brand guide would have
# mixed the wrong ink. The audit below now fails the build on any divergence
# from PALETTE in build.py, so a rename lands in both files or in neither.
PALETTE = [
    ("orange",   "#EE8B33", "the one hot colour; accent ink on dark, fill on light"),
    ("rust",     "#6A2A12", "accent ink on light grounds, and a mark facet"),
    ("teal",     "#31606D", "the cool counterweight"),
    ("sumi",     "#05192B", "the dark ground, and the ink on light grounds"),
    ("cream",    "#FAEBD3", "the warm paper — the light ground"),
    ("warmwhite","#FFF9EF", "raised surface on the cream ground"),
    ("paleteal", "#C3D5DA", "the back range of the mark; not a screen token"),
    ("peach",    "#FFCDAA", "the dark cut's hot facet, and a series; not a screen token"),
    ("smoke",    "#829AA1", "derived mid; muted detail"),
    ("mist",     "#DEEAEE", "raised cool surface on white"),
    ("duckegg",  "#9ABCC6", "first chart series on the dark grounds"),
    ("drafting", "#1D3E47", "raised surface on the tools ground"),
]

# The audit: every name this file shares with the token source must mean the
# same hex, and every hex it shares must be called by a token-side name for
# that hex (sumi and night share a value upstream; either name is honest).
# Colours print carries that the screen does not — the mark facets — must
# not reuse a token name for something else.
def _audit_against_tokens():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "tokens_build", os.path.join(HERE, "build.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    tokens = {name: hexstr.upper() for name, (hexstr, _) in mod.PALETTE.items()}
    by_hex = {}
    for name, hexstr in tokens.items():
        by_hex.setdefault(hexstr, set()).add(name)
    problems = []
    for name, hexstr, _ in PALETTE:
        hexstr = hexstr.upper()
        if name in tokens and tokens[name] != hexstr:
            problems.append(f"{name}: print says {hexstr}, tokens say {tokens[name]}")
        if hexstr in by_hex and name not in by_hex[hexstr]:
            problems.append(
                f"{hexstr}: print calls it {name}, tokens call it "
                f"{'/'.join(sorted(by_hex[hexstr]))}")
    if problems:
        raise SystemExit("print.py disagrees with build.py:\n  " + "\n  ".join(problems))

_audit_against_tokens()


def lab(hexstr, space="lab-d65"):
    c = Color(hexstr).convert(space)
    return [round(v, 2) for v in c[:3]]


def de2000(a, b):
    return round(Color(a).delta_e(Color(b), method="2000"), 2)


def separate(hexes, icc):
    """sRGB -> CMYK -> sRGB through an ICC profile, relative colorimetric+BPC.

    Returns (cmyk_percent, round_trip_hex) per input. The round trip is the
    point: it is the only way to say whether the separation is faithful.
    """
    srgb = ImageCms.createProfile("sRGB")
    cmyk = ImageCms.getOpenProfile(icc)
    n = len(hexes)
    src = Image.new("RGB", (n, 1))
    src.putdata([tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) for h in hexes])
    fwd = ImageCms.buildTransform(
        srgb, cmyk, "RGB", "CMYK",
        renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC,
        flags=ImageCms.Flags.BLACKPOINTCOMPENSATION)
    back = ImageCms.buildTransform(
        cmyk, srgb, "CMYK", "RGB",
        renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC,
        flags=ImageCms.Flags.BLACKPOINTCOMPENSATION)
    mid = ImageCms.applyTransform(src, fwd)
    out = ImageCms.applyTransform(mid, back)
    res = []
    for cmyk_px, (r, g, b) in zip(mid.get_flattened_data(),
                                  out.get_flattened_data()):
        # littlecms writes ink coverage directly: 0 = no ink, 255 = 100%.
        # (Pillow's own RGB->CMYK convert() is inverted; this is not that.
        # Checked against the endpoints: white -> 0/0/0/0, red -> 0/100/100/0.)
        res.append(([round(v / 2.55) for v in cmyk_px],
                    f"#{r:02X}{g:02X}{b:02X}"))
    return res


def pantone_table(path):
    rows = json.load(open(path))
    out = []
    for r in rows:
        name = r["pantone"]
        if not name.endswith("-c"):
            continue
        pretty = "PANTONE " + name[:-2].upper().replace("-", " ") + " C"
        out.append((pretty, r["hex"].upper()))
    return out


def main():
    icc = sys.argv[1] if len(sys.argv) > 1 else None
    pms_path = sys.argv[2] if len(sys.argv) > 2 else None
    if not icc or not pms_path:
        sys.exit(__doc__)

    hexes = [h for _, h, _ in PALETTE]
    sep = separate(hexes, icc)
    pms = pantone_table(pms_path)
    prof = ImageCms.getOpenProfile(icc).profile.profile_description

    entries = []
    print(f"{'token':13s} {'hex':8s} {'CMYK':>18s} {'dE':>5s}  nearest Pantone")
    for (token, hexstr, role), (cmyk, rt) in zip(PALETTE, sep):
        gap = de2000(hexstr, rt)
        near = sorted(((de2000(hexstr, ph), pn, ph) for pn, ph in pms))[:3]
        entries.append({
            "token": token,
            "hex": hexstr,
            "role": role,
            "lab_d65": lab(hexstr, "lab-d65"),
            "lab_d50": lab(hexstr, "lab"),
            "cmyk": cmyk,
            "cmyk_roundtrip_hex": rt,
            "cmyk_delta_e_2000": gap,
            "in_process_gamut": gap <= 2.0,
            "pantone_candidates": [
                {"name": pn, "approx_hex": ph, "delta_e_2000": d}
                for d, pn, ph in near
            ],
        })
        c = "/".join(str(v) for v in cmyk)
        print(f"{token:13s} {hexstr} {c:>18s} {gap:>5.1f}  "
              f"{near[0][1]} (dE {near[0][0]})")

    doc = {
        "note": "Generated by print.py. Lab is exact; CMYK is an ICC "
                "separation with its round-trip error reported; Pantone is a "
                "shortlist to eye-match against a physical guide, derived "
                "from community sRGB approximations, NOT from Pantone's "
                "licensed Lab data.",
        "cmyk_profile": prof,
        "cmyk_intent": "relative colorimetric with black point compensation",
        "gamut_threshold_delta_e_2000": 2.0,
        "colours": entries,
    }
    with open(os.path.join(HERE, "print.json"), "w") as fh:
        json.dump(doc, fh, indent=2)
        fh.write("\n")
    bad = [e["token"] for e in entries if not e["in_process_gamut"]]
    print(f"\nprofile: {prof}")
    print("out of process gamut: " + (", ".join(bad) if bad else "none"))
    print("wrote print.json")


if __name__ == "__main__":
    main()
