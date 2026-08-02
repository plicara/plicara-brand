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

Rebuild everything with `python3 build.py` (see the header of that file for
dependencies). Nothing here is hand-edited — change `build.py`, not the SVGs.

## Which file

| Use | File |
| --- | --- |
| Anything you can style with CSS | `mark.svg` — takes `currentColor` |
| Dark ground | `mark-signal.svg` |
| Light ground | `mark-moss.svg` (quiet) or `mark-ink.svg` (maximum contrast) |
| On a signal or moss panel | `mark-paper.svg` |
| Below ~40 px | `mark-small*.svg` — three lines instead of six, heavier stroke |
| GitHub org, Hugging Face, social | `avatar-ink.svg` (default), or `-signal` / `-moss` / `-alpine` |
| Browser tab | `favicon.svg` — 32 px artboard, ink ground |
| Wide spaces: site header, slide footer | `lockup-horizontal-*.svg` |
| Squarer spaces: cards, README badges | `lockup-compact-*.svg` |
| Centred: README hero, title slide, print | `lockup-vertical-*.svg` |

Lockup suffixes: `-dark` (signal mark, paper wordmark), `-light` (moss mark, ink
wordmark), `-signal` (all one colour — for placing on a moss or alpine panel, or
anywhere a single-colour reproduction is needed).

## Rules

- **Clear space** on every side is the height of one ridge band. The mark files
  already carry it inside the artboard, so a flush `64×64` box is correct.
- **Two cuts.** The full six-line cut down to about 40 px; below that the
  reduced three-line cut, which drops one line of each pair and carries more
  stroke. Same drawing, fewer lines — not a different mark.
- **Minimum size 16 px**, reduced cut.
- **Lockups carry a heavier mark** (3.7% rather than 2.6%) so it holds its own
  beside 800-weight caps. That is optical weight matching, not a second mark.
- **Do not** rotate it, add a third colour, place it on a busy photograph,
  outline the wordmark, or set the wordmark in anything but Archivo — the
  lockups carry outlines, so nothing needs the font installed.
- The wordmark is Archivo (Omnibus-Type) at `wght` 800, `wdth` 125, converted to
  paths. Archivo is SIL Open Font Licence 1.1; the OFL covers the baked outlines
  and does not extend to the rest of this repository.

## Colours

`signal #D9F224` · `ink #0C1110` · `moss #39441F` · `paper #F2F3EC` ·
`alpine #12688F`

Full palette and the reasoning behind it: [`../../docs/visual-direction.md`](../../docs/visual-direction.md).
