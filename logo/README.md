# Logo files

**The house mark is Foothills Refolded, in the chalk colourway** — two
pleated-paper ranges (the duck-egg one peeks through the front valleys; ranges
recede, crowns cannot), rose/butterscotch/emerald facets under the line, duck-egg back range, set
off-register. Sources: `candidates/candidate-e3-foothills-refolded.svg`
(line drawing) and `candidates/mark-foothills-chalk[-dark].svg` (colour
construction), both generated. All earlier candidates and colourways stay
in `candidates/` for the record.

Two constraints from the device screens, both binding on any future
revision: **the paper-plane silhouette in side view is Telegram's mark** (no
candidate was ever one, by construction), and **the mark must never be
composed as a skyline over horizontal colour bands, nor set in a rectangular
label lockup** — those are the configurations Patagonia enforces. Full
reasoning: [`../../next_steps/trademark.md`](../../next_steps/trademark.md).

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

The faceted two-layer construction lives in `build.py` and the device screen
has been run against this mark (v2,
[`../../next_steps/trademark.md`](../../next_steps/trademark.md)). One build
item is still open: a dedicated **reduced cut** (`MARK_SRC_SM`) for below
~24 px — drop the back range and carry more stroke. Until it exists, the
small cut reuses the full drawing.

## Which file

| Use | File |
| --- | --- |
| The mark, in colour | `mark-colour.svg` (light grounds), `mark-colour-dark.svg` (dark grounds) |
| Anything you can style with CSS | `mark.svg` — monoline, takes `currentColor` |
| Single-colour reproduction | `mark-butterscotch.svg`, `mark-chalk.svg`, `mark-sumi.svg`, `mark-emerald.svg` |
| Below ~40 px | `mark-small*.svg` — heavier monoline stroke |
| GitHub org, Hugging Face, social | `avatar-night.svg` (default) or `avatar-chalk.svg` (colour), `avatar-butterscotch.svg` (monoline) |
| Browser tab | `favicon.svg` — rounded night tile, butterscotch border |
| Wide spaces: site header, slide footer | `lockup-horizontal-*.svg` |
| Squarer spaces: cards, README badges | `lockup-compact-*.svg` |
| Centred: README hero, title slide, print | `lockup-vertical-*.svg` |
| Anywhere SVG is not accepted | `png/` — see below |

Lockup suffixes: `-dark` (colour mark, chalk wordmark), `-light` (colour
mark, sumi wordmark), `-mono` (all butterscotch, monoline — for a dark panel or
single-colour reproduction). The wordmark is **lowercase**: `foothills labs`.

## Rasters

SVG is the source of truth. `png/` covers the places that cannot take one:

| File | For |
| --- | --- |
| `avatar-night-1024.png`, `-512.png` | GitHub org, Hugging Face org, social profile |
| `avatar-chalk-512.png`, `avatar-butterscotch-512.png` | Alternate grounds |
| `mark-colour-512.png`, `mark-colour-dark-512.png` | Transparent colour mark, decks and docs |
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
- **Minimum size 16 px.** A dedicated reduced cut for below ~24 px is still
  to be drawn; until then the small cut reuses the full drawing, which is why
  the favicon runs dense at tile sizes.
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

`butterscotch #E7A63E` · `sumi #26292B` · `chalk #EDF1F0` · `night #1E3C40` ·
`emerald #2F6E70` · `rose #EE93A9`

Butterscotch is the accent colour and a fill, never an ink — text on it is
always `--fh-on-butterscotch`. Full palette, misuse rules and the reasoning:
[`../../docs/brand.md`](../../docs/brand.md).
