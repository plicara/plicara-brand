"""Minimum print size for the mark, measured rather than guessed.

Two things kill a line drawing on press, and they pull in opposite
directions:

    ink spread    ink wicks outward from every stroke, so the white channels
                  the drawing encloses get eaten from both sides. Heavier
                  strokes make this WORSE.
    line hold     a stroke below roughly 0.15 mm breaks up on coated offset
                  and vanishes on uncoated. Heavier strokes make this BETTER.

So the minimum size is the larger of the two limits, and the two cuts of the
mark land in different regimes. Both carry the same drawing — the small cut
differs in stroke weight alone — but that weight moves it between regimes:
the full cut is counter-limited throughout (its tightest counter is the wedge
where a back-range peak meets the front slope), while the small cut's heavier
line holds where the full one breaks up, and it only becomes counter-limited
on the dirtier processes. That is why the small cut is also the PRINT cut
below ~15 mm, arrived at from the opposite direction to the screen argument.

Method: render the monoline cut, label every enclosed counter, and take the
largest inscribed circle in each (a Euclidean distance transform of the
background). A counter survives ink spread s per side while its inscribed
radius exceeds s. Slivers under 0.02% of the artboard are ignored — they are
rasteriser noise at acute junctions, not features.

    pip install cairosvg pillow numpy scipy
    python3 printsize.py
"""

import io
import os

import cairosvg
import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
N = 2000        # render resolution
BOX = 64.0      # artboard units
SLIVER = 0.0002  # fraction of the render below which a counter is noise

# (file, stroke in artboard units, label)
CUTS = [("mark.svg", 1.7, "full"),
        ("mark-small.svg", 1.7 * 1.65, "small")]

# (ink spread per side mm, minimum holding line mm, label)
PROCESSES = [(0.05, 0.15, "coated offset, good"),
             (0.10, 0.20, "coated offset, typical"),
             (0.20, 0.30, "uncoated / screen print")]


def tightest_counter(path):
    """Inscribed radius, in artboard units, of the tightest real counter."""
    src = open(path).read().replace("currentColor", "#000000")
    png = cairosvg.svg2png(bytestring=src.encode(), output_width=N,
                           output_height=N, background_color="#FFFFFF")
    ink = np.array(Image.open(io.BytesIO(png)).convert("L")) < 128
    lab, n = ndimage.label(~ink)
    outer = lab[0, 0]
    edt = ndimage.distance_transform_edt(~ink)
    radii = [edt[lab == i].max() * BOX / N
             for i in range(1, n + 1)
             if i != outer and (lab == i).sum() >= N * N * SLIVER]
    return min(radii)


def main():
    print(f"{'cut':9s} {'process':24s} {'counter':>9s} {'stroke':>8s} "
          f"{'MINIMUM':>9s} {'stroke there':>13s}")
    for fn, stroke, cut in CUTS:
        r = tightest_counter(os.path.join(HERE, fn))
        print(f"{cut:9s} tightest counter: inscribed radius {r:.3f}u "
              f"(channel {2 * r / BOX * 100:.2f}% of the box)")
        for spread, minline, label in PROCESSES:
            h_counter = spread / (r / BOX)
            h_stroke = minline / (stroke / BOX)
            h = max(h_counter, h_stroke)
            limit = "counter" if h_counter > h_stroke else "stroke"
            print(f"{'':9s} {label:24s} {h_counter:6.1f}mm {h_stroke:7.1f}mm "
                  f"{h:7.1f}mm {stroke / BOX * h:10.2f}mm   {limit}-limited")


if __name__ == "__main__":
    main()
