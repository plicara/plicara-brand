# Logo files

The house mark is **Siwalik** — three ridge bands, no summit. The lab is the
foothills; the summits belong to the models.

It is contoured out of a height field by `../marks/generate.py`, exactly like
the seven summit glyphs, and the slight irregularity that comes with that is
deliberate. The lines are not perfectly parallel, the pairs converge and part,
the ends do not align. That is the character — it reads as drawn rather than
generated, and a sanitised version of it was tried and thrown away.

The weight is where the discipline goes instead. Stroke is a constant **2.6% of
the artboard** on the full cut, which keeps every paired line clearly separate
at every size. Heavier than that and the pairs close up against each other,
which is what makes an organic mark look unclean rather than characterful.

Rebuild the SVGs with `python3 build.py` and the rasters with
`python3 export.py` (see each file's header for dependencies). Nothing here is
hand-edited — change the scripts, not the output.

Rules, palette and misuse: [`../../docs/brand.md`](../../docs/brand.md).

## Which file

| Use | File |
| --- | --- |
| Anything you can style with CSS | `mark.svg` — takes `currentColor` |
| Dark ground | `mark-lichen.svg` |
| Light ground | `mark-moss.svg` (quiet) or `mark-ink.svg` (maximum contrast) |
| On a signal or moss panel | `mark-paper.svg` |
| Below ~40 px | `mark-small*.svg` — three lines instead of six, heavier stroke |
| GitHub org, Hugging Face, social | `avatar-ink.svg` (default), or `-lichen` / `-moss` / `-alpine` |
| Browser tab | `favicon.svg` — rounded ink tile, bold lichen border, reduced cut |
| Wide spaces: site header, slide footer | `lockup-horizontal-*.svg` |
| Squarer spaces: cards, README badges | `lockup-compact-*.svg` |
| Centred: README hero, title slide, print | `lockup-vertical-*.svg` |
| Anywhere SVG is not accepted | `png/` — see below |

Lockup suffixes: `-dark` (lichen mark, paper wordmark), `-light` (moss mark, ink
wordmark), `-mono` (all one colour, in lichen — for placing on a moss or alpine
panel, or anywhere a single-colour reproduction is needed).

## Rasters

SVG is the source of truth. `png/` covers the places that cannot take one:

| File | For |
| --- | --- |
| `avatar-ink-1024.png`, `-512.png` | GitHub org, Hugging Face org, social profile |
| `avatar-lichen-512.png`, `avatar-moss-512.png` | Alternate grounds |
| `mark-lichen-512.png`, `mark-moss-512.png` | Transparent mark, decks and docs |
| `favicon-32.png`, `favicon-64.png` | Browser tab fallback where SVG is not supported |
| `touch-icon.svg` | Source for the apple-touch icon: square ground (iOS rounds it), pre-rounded border so the mask does not clip it |
| `apple-touch-icon-180.png` | iOS home screen |
| `social-card-1200x630.png` | Open Graph and Twitter card |

`favicon.svg` is preferred over the PNGs wherever the browser will take it.

## Rules

- **Clear space** on every side is the height of one ridge band. The mark files
  already carry it inside the artboard, so a flush `64×64` box is correct.
- **Tiled cuts share one corner geometry.** Avatars carry the favicon's corner
  ratio (21.875% — `rx` 112 at 512), so every square-ground cut of the mark
  rounds the same way. Avatars carry no border, unlike the favicon: they live
  under the circular masks GitHub and Hugging Face apply, and a rect border
  gets clipped mid-line by that mask.
- **The avatars are circle-safe.** GitHub and Hugging Face mask org avatars into
  circles, and the band ends sit where an inscribed circle cuts. `avatar-*.svg`
  keeps the whole drawing inside that circle with 37 px of clearance at 512.
  Do not reduce their padding to make the mark look bigger in a square preview —
  the square preview is not where it will be seen.
- **Two cuts.** The full six-line cut down to about 40 px; below that the
  reduced three-line cut, which drops one line of each pair and carries more
  stroke. Same drawing, fewer lines — not a different mark.
- **Minimum size 16 px**, reduced cut.
- **Lockups carry a heavier mark** (3.7% rather than 2.6%) so it holds its own
  beside 800-weight caps. That is optical weight matching, not a second mark.
- **Do not** rotate it, add a third colour, place it on a busy photograph, or
  outline the wordmark.
- **Standalone surfaces use the lockups**, never a retyped name — decks,
  social, print, README heroes, anywhere the name appears without page context.
  The lockups carry outlines, so nothing needs the font installed.
- **In-page headers are the exception**: a page header may set the name in the
  surface's display face beside the mark — Fraunces on warm pages, Archivo on
  technical ones, sentence case either way. In-page, the mark carries the
  identity; the letterforms follow the register the page is already in.
- The wordmark is Archivo (Omnibus-Type) at `wght` 800, `wdth` 125, converted to
  paths. Archivo is SIL Open Font Licence 1.1; the OFL covers the baked outlines
  and does not extend to the rest of this repository.

## Colours

`lichen #C2DC2F` · `ink #0C1110` · `moss #39441F` · `paper #F2F3EC` ·
`alpine #12688F`

Lichen is the accent colour; **Signal** is the name of a scheme (dark, for
benchmarks and tools). The colour was called signal before the schemes existed,
and the `--fh-signal` token survives as a legacy alias — new work should say
lichen.

Full palette, misuse rules and the reasoning: [`../../docs/brand.md`](../../docs/brand.md).
