# Logo files

**The house mark is Foothills Refolded, in the beacon colourway** — two
pleated-paper ranges (the duck-egg one peeks through the front valleys; ranges
recede, crowns cannot), teal/rust/orange facets under the line on light grounds — lifted to
slate/orange/apricot on dark ones, because no facet colour in this palette
reads on both — pale-teal back range, set off-register. Sources: `candidates/candidate-e3-foothills-refolded.svg`
(line drawing) and `candidates/mark-foothills-beacon[-dark].svg` (colour
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
[`../../next_steps/trademark.md`](../../next_steps/trademark.md)).

**Every cut draws the same mountains**: three peaks in front, two behind. The
small cut — `mark-small*.svg`, `mark-colour-small*.svg` and the **favicon** —
differs from the full drawing in **stroke weight alone** (~1.65x), never in
what is drawn.

An earlier rule dropped the back range below ~24 px, on the theory that the
rear peaks broke into stray pixels and the valleys silted up. Measured at
30 px they do not: the back peaks hold their fill and the valleys stay open,
they just need the line a weight heavier. The cost of that rule was two logos
in circulation — a hero with two ranges, a header and tab with one — while
the touch icon and OG card carried the full drawing all along. The reduced cut
is retired; `candidates/candidate-e3r-foothills-reduced.svg` and
`candidates/mark-foothills-*-reduced[-dark].svg` stay for the record.

If a size ever does need a reduced cut, cut it in **all** the surfaces at that
size — header, favicon and touch icon together — or the mark becomes two marks
again.

## Which file

| Use | File |
| --- | --- |
| The mark, in colour | `mark-colour.svg` (light grounds), `mark-colour-dark.svg` (dark grounds) |
| Anything you can style with CSS | `mark.svg` — monoline, takes `currentColor` |
| Single-colour reproduction | `mark-orange.svg`, `mark-cream.svg`, `mark-sumi.svg`, `mark-teal.svg` |
| Below ~40 px | `mark-small*.svg` (monoline), `mark-colour-small*.svg` (colour) — same drawing, heavier stroke |
| GitHub org, Hugging Face, social | `avatar-night.svg` (default) or `avatar-cream.svg` (colour), `avatar-orange.svg` (monoline). **Unbordered on purpose** — see below |
| Personal page, slide, app tile | `avatar-cream-bordered.svg` (paper ground) or `avatar-night-bordered.svg` (dark). Rounded tile, accent rule around it |
| Transparent, drop on any ground | `mark-colour.svg` (light grounds), `mark-colour-dark.svg` (dark) |
| Browser tab | `favicon.svg` — rounded night tile, orange border |
| Wide spaces: site header, slide footer | `lockup-horizontal-*.svg` |
| Squarer spaces: cards, README badges | `lockup-compact-*.svg` |
| Centred: README hero, title slide, print | `lockup-vertical-*.svg` |
| Anywhere SVG is not accepted | `png/` — see below |

Lockup suffixes: `-dark` (colour mark, cream wordmark), `-light` (colour
mark, sumi wordmark), `-mono` (all orange, monoline — for a dark panel or
single-colour reproduction). The wordmark is **lowercase**: `foothills labs`.

## Rasters

SVG is the source of truth. `png/` covers the places that cannot take one:

| File | For |
| --- | --- |
| `avatar-night-1024.png`, `-512.png` | GitHub org, Hugging Face org, social profile |
| `avatar-cream-bordered-1024.png`, `-512.png` | Bordered paper tile — personal pages, slides, app icons |
| `avatar-night-bordered-1024.png`, `-512.png` | The same on the dark ground |
| `mark-colour-1024.png`, `mark-colour-dark-1024.png` | Transparent mark at print size |
| `avatar-cream-512.png`, `avatar-orange-512.png` | Alternate grounds |
| `mark-colour-512.png`, `mark-colour-dark-512.png` | Transparent colour mark, decks and docs |
| `favicon-16.png`, `favicon-32.png`, `favicon-64.png` | Browser tab fallback where SVG is not supported |
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
- **Do not use a bordered tile as an org avatar.** The rounded rectangle's
  corners fall outside the inscribed circle, so a circular mask cuts the rule
  into four arcs. The bordered cuts are for surfaces that keep the square:
  personal pages, slides, app icons. For GitHub and Hugging Face use
  `avatar-night.svg`, which has no border for exactly this reason.
- **Minimum print size** is 14 mm for the full cut on typical coated offset
  and 5.2 mm for the small cut — measured by `printsize.py`, not guessed.
  Below ~15 mm, print the small cut; business-card scale is the small cut.
  Uncoated and screen print are dirtier: 27.9 mm and 10.3 mm respectively.
- **Minimum size 16 px**, and below ~40 px use the small cut — the same
  drawing with a heavier line, not a simplification you may improvise. Do not
  reach for a lighter stroke at small sizes: the line, not the drawing, is
  what fails first.
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

`orange #EE8B33` · `ink #05192B` · `cream #FAEBD3` · `teal #31606D` ·
`rust #6A2A12` · `paleteal #C3D5DA`

Orange is the accent colour. On dark grounds it is also an ink (7.1:1); on
the cream paper it manages 2.1:1, so there it is a fill and nothing else, and
text on it is always `--fh-on-orange`. Rust is the light-ground accent
ink. Full palette, misuse rules and the reasoning:
[`../../docs/brand.md`](../../docs/brand.md).
