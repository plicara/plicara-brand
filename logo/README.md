# Logo files

**The house mark is the sheet; the cut is being chosen.** The sheet
direction won (*the lab is the sheet; the planes belong to the models* — the
direct heir of the summit-less Siwalik logic), and four cuts of it live in
[`candidates/`](candidates/): `a-sheet` (full crease pattern), `a2-sheet-quiet`
(centre fold and first creases), `a3-sheet-square` (the origami square) and
`a4-sheet-jaunty` (strongest tilt, loosest line). The retired b/c/d candidates
stay in the directory for the record. Until the cut is picked, `a-sheet` is
wired into the pipeline provisionally so every derived asset stays buildable;
the quiet and square cuts hold a 16 px tile, so the reduced cut will come
from one of them.

The one hard constraint, from the similarity screen: **the paper-plane
silhouette in side view is Telegram's mark.** None of the candidates is one,
by construction.

Everything here is generated. The candidate drawings come from
`candidates/generate.py` (same deterministic wobble as the model glyphs);
`build.py` reframes the chosen drawing, bakes colour variants, and composes
the lockups with the wordmark converted to outlines (no font dependency);
`export.py` rasterises. Nothing is hand-edited — change the scripts, not the
output.

```
python3 candidates/generate.py
python3 build.py [path/to/archivo-latin-wdth-normal.woff2]
python3 export.py
```

When the mark is chosen: point `MARK_SRC` in `build.py` at the final drawing,
draw it a proper reduced cut (`MARK_SRC_SM`), regenerate, and re-run the
trademark screen ([`../../next_steps/trademark.md`](../../next_steps/trademark.md)).

## Which file

| Use | File |
| --- | --- |
| Anything you can style with CSS | `mark.svg` — takes `currentColor` |
| Dark ground | `mark-butter.svg` or `mark-washi.svg` |
| Light ground | `mark-sumi.svg` (maximum contrast) or `mark-magenta.svg` (Cel accent) |
| Below ~40 px | `mark-small*.svg` — heavier stroke (provisional: same drawing) |
| GitHub org, Hugging Face, social | `avatar-night.svg` (default), or `-butter` / `-sumi` / `-royal` |
| Browser tab | `favicon.svg` — rounded night tile, butter border |
| Wide spaces: site header, slide footer | `lockup-horizontal-*.svg` |
| Squarer spaces: cards, README badges | `lockup-compact-*.svg` |
| Centred: README hero, title slide, print | `lockup-vertical-*.svg` |
| Anywhere SVG is not accepted | `png/` — see below |

Lockup suffixes: `-dark` (butter mark, washi wordmark), `-light` (magenta
mark, sumi wordmark), `-mono` (all butter — for a dark panel or single-colour
reproduction). The wordmark is **lowercase**: `foothills labs`.

## Rasters

SVG is the source of truth. `png/` covers the places that cannot take one:

| File | For |
| --- | --- |
| `avatar-night-1024.png`, `-512.png` | GitHub org, Hugging Face org, social profile |
| `avatar-butter-512.png`, `avatar-sumi-512.png` | Alternate grounds |
| `mark-butter-512.png`, `mark-sumi-512.png` | Transparent mark, decks and docs |
| `favicon-32.png`, `favicon-64.png` | Browser tab fallback where SVG is not supported |
| `touch-icon.svg` | Source for the apple-touch icon: square ground (iOS rounds it), pre-rounded border so the mask does not clip it |
| `apple-touch-icon-180.png` | iOS home screen |
| `social-card-1200x630.png` | Open Graph and Twitter card |

`favicon.svg` is preferred over the PNGs wherever the browser will take it.

## Rules

- **Clear space** on every side is one fold-panel width. The mark files
  already carry it inside the artboard, so a flush box is correct.
- **The avatars are circle-safe.** GitHub and Hugging Face mask org avatars
  into circles; the avatars keep the whole drawing inside the inscribed
  circle. Do not reduce their padding to make the mark look bigger in a
  square preview — the square preview is not where it will be seen.
- **Minimum size 16 px.** (The final mark gets a real reduced cut for below
  ~40 px; the provisional mark reuses the full drawing and is the reason the
  favicon currently runs dense.)
- **Lockups carry a heavier mark** so it holds its own beside 800-weight
  letterforms. That is optical weight matching, not a second mark.
- **Do not** rotate it, add a third colour, place it on a busy photograph, or
  outline the wordmark.
- **Standalone surfaces use the lockups**, never a retyped name — decks,
  social, print, README heroes, anywhere the name appears without page
  context. The lockups carry outlines, so nothing needs the font installed.
- **In-page headers are the exception**: a page header may set the name in
  the surface's display face beside the mark — Fraunces on warm pages,
  Archivo on technical ones, lowercase either way. In-page, the mark carries
  the identity; the letterforms follow the register the page is already in.
- The wordmark is Archivo (Omnibus-Type) at `wght` 800, `wdth` 125, converted
  to paths. Archivo is SIL Open Font Licence 1.1; the OFL covers the baked
  outlines and does not extend to the rest of this repository.

## Colours

`butter #F3DC7C` · `sumi #2B2422` · `washi #FAF6ED` · `night #1F292E` ·
`magenta #B92D77` · `royal #2F3BB3`

Butter is the accent colour and a fill, never an ink — text on it is always
`--fh-on-butter`. Full palette, misuse rules and the reasoning:
[`../../docs/brand.md`](../../docs/brand.md).
