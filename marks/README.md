# Model glyphs

One mark per model, generated from a synthetic height field. The rules that
govern them are in [`../../docs/brand.md`](../../docs/brand.md); the reasoning
is in [`../../docs/brand-rationale.md`](../../docs/brand-rationale.md).

These are **product marks, not the org mark.** The lab's logo is Siwalik, in
[`../logo/`](../logo/).

## The rule

> Each summit is drawn as an island, seen from directly above.
> Contour interval is a constant **1,500 m**.
> Ring count is therefore **elevation ÷ 1,500**.

Complexity tracks tier by construction. Nobody decides how elaborate Everest's
mark should be next to Kosciuszko's — the elevation decides, and it decides the
same way every time a summit is added.

| Model | Elevation | Rings | Notes |
| --- | ---: | ---: | --- |
| Everest | 8,849 m | 5 | Three ridge arms off a steep summit |
| Aconcagua | 6,961 m | 4 | Main summit plus the south summit |
| Denali | 6,190 m | 4 | North and South Peaks, huge footprint |
| Kilimanjaro | 5,895 m | 3 | Shield volcano; Mawenzi closes its own ring |
| Elbrus | 5,642 m | 3 | Twin cones on a shared base |
| Vinson | 4,892 m | 3 | Long ridge massif |
| Kosciuszko | 2,228 m | 1 | Broad and gentle. One ring is the point |
| Siwalik | — | — | No summit, no dot. Open ridge bands |

**Spot-height dots** mark named summits, as they would on a map. Elbrus's twin
cones get two, Denali's North and South Peaks get two, Aconcagua's south summit
gets a second. They are also what keeps otherwise-similar footprints apart at
small sizes.

Kilimanjaro carries one closed ring that is not a tier signal: Mawenzi, its
eastern peak, clears 4,500 m and so closes a contour of its own. That is true at
this interval, and it makes the fast tier the most recognisable mark in the set.

## Files

```
contour-<name>.svg          full cut, stroke 1.75
contour-<name>-small.svg    reduced cut, stroke 4.4 — below about 32 px
generate.py                 the generator
```

Marks take `currentColor`, so they inherit from CSS and need no per-colour
variants. Nothing here is hand-edited — change `generate.py` and rerun it.

```
pip install numpy matplotlib
python3 generate.py
```

The generator builds a small height field per mountain, extracts contours with
marching squares, resamples each to an even arc length, and emits smooth closed
cubic-bezier paths. It is deterministic: same input, same SVG.

Siwalik is generated here too, and `../logo/build.py` reframes that same drawing
into the logo set — so the model sheet and the org mark cannot drift apart.

## What is real and what is not

**Real:** every summit elevation, every named secondary top, the continent
assignments, and Mawenzi clearing 4,500 m.

**Not real:** the shapes. Each field is tuned by hand to follow the mountain's
character — sharp pyramid, shield volcano, twin cones, long ridge — but it is
not SRTM, ASTER, or any other elevation dataset.

Deriving them from real elevation data is roughly an afternoon of work and
should happen before any of this is public. It is the difference between a
system that is *true* and one that is merely *consistent*. Until then, do not
describe the glyphs as derived from survey data.

## Known weak spot

Denali and Elbrus read close at small sizes — both are ovals with two spot
heights. They are genuinely similar footprints, so this may be honest rather
than wrong, but it is the first thing to fix if the family ever needs tightening.
