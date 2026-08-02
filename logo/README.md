# Logo files

The house mark is **Siwalik** — four ridge bands, no summit. The lab is the
foothills; the summits belong to the models.

It is **constructed, not sampled.** The seven summit glyphs are contoured from
height fields by `../marks/generate.py`, and their irregularity is the point —
it is data. A logo is not data. So the mark is drawn: one master curve, three
true parallel offsets at constant perpendicular distance, ends trimmed to a
shared range. The bands stay evenly spaced everywhere, including where the curve
steepens, which simple vertical copies would not do.

`build.py` also writes `../marks/contour-siwalik.svg` from the same geometry at
the family's stroke weight, so the model sheet and the logo cannot drift apart.

Rebuild everything with `python3 build.py` (see the header of that file for
dependencies). Nothing here is hand-edited — change `build.py`, not the SVGs.

## Which file

| Use | File |
| --- | --- |
| Anything you can style with CSS | `mark.svg` — takes `currentColor` |
| Dark ground | `mark-signal.svg` |
| Light ground | `mark-moss.svg` (quiet) or `mark-ink.svg` (maximum contrast) |
| On a signal or moss panel | `mark-paper.svg` |
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
- **One shape at every size.** There is no reduced cut — the mark holds from
  16 px to poster. The favicon carries slightly more stroke, which is optical
  sizing, not a second drawing.
- **Minimum size 16 px.**
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
