# Logo files

The house mark is **Siwalik** — open ridge bands, no summit. The lab is the
foothills; the summits belong to the models. It is the same drawing as
`../marks/contour-siwalik.svg`, reframed with proper clear space.

Rebuild everything with `python3 build.py` (see the header of that file for
dependencies). Nothing here is hand-edited — change `build.py`, not the SVGs.

## Which file

| Use | File |
| --- | --- |
| Anything you can style with CSS | `mark.svg` — takes `currentColor` |
| Dark ground | `mark-signal.svg` |
| Light ground | `mark-moss.svg` (quiet) or `mark-ink.svg` (maximum contrast) |
| On a signal or moss panel | `mark-paper.svg` |
| Below ~32 px | `mark-small.svg` — three bands instead of six |
| GitHub org, Hugging Face, social | `avatar-ink.svg` (default), or `-signal` / `-moss` / `-alpine` |
| Browser tab | `favicon.svg` — 32 px artboard, reduced cut, ink ground |
| Wide spaces: site header, slide footer | `lockup-horizontal-*.svg` |
| Squarer spaces: cards, README badges | `lockup-compact-*.svg` |
| Centred: README hero, title slide, print | `lockup-vertical-*.svg` |

Lockup suffixes: `-dark` (signal mark, paper wordmark), `-light` (moss mark, ink
wordmark), `-signal` (all one colour — for placing on a moss or alpine panel, or
anywhere a single-colour reproduction is needed).

## Rules

- **Clear space** on every side is the height of one ridge band. The mark files
  already carry it inside the artboard, so a flush `64×64` box is correct.
- **Minimum size 20 px** for the reduced cut, 32 px for the full cut.
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
