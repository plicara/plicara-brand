# Model glyphs

One glyph per model, each a **stylised drawing of its paper plane** — a top
view with a thick sumi outline and a orange fill set deliberately
off-register, the loose screen-print look of the illustration style
([`../../docs/brand.md` § Illustration](../../docs/brand.md#illustration-and-imagery)).

The canon, by tier:

| Glyph | Model | Character |
| --- | --- | --- |
| `plane-glider` | glider (es: planeador) | wide span, gentle sweep — the plane that stays up |
| `plane-delta` | delta (es: delta) | one triangle, no waste — nearly all wing |
| `plane-canard` | canard (es: canard) | small wings forward, big wing aft — steers before it glides |
| `plane-hammer` | hammer (es: martillo) | a locked, weighted nose — the most folds, the longest throw |

These are drawings, not fold diagrams. A fold-count-equals-tier construction
was considered and dropped: fold counts would have been self-authored
authority, decoration pretending to be data. The drawings stay simple and
charming instead — that is the brand argument, not a compromise on it.

## Which file

| Use | File |
| --- | --- |
| Light grounds (cream, white, mist) | `plane-{name}.svg` — sumi outline, orange fill |
| Dark grounds (night, print) | `plane-{name}-dark.svg` — cream outline, orange fill |
| Below ~40 px | `plane-{name}-small.svg` — heavier line, centre fold only, fill on-register |
| Styled with CSS | `plane-{name}-mono.svg` — `currentColor` outline, no fill |

`glyphs.json` carries the family metadata (tiers, naming axes, notes).

## The generator

Everything here is written by `generate.py` — geometry authored as clean
symmetric polygons in code, with the hand-drawn character applied as
**deterministic low-frequency wobble**, seeded per glyph. Re-running the
script produces byte-identical output on any machine; that is checked, not
hoped. Change the code, not the SVGs.

```
python3 generate.py
```

No dependencies beyond the standard library.

## Rules

- The glyphs are the models'. The house mark is the lab's — never use a plane
  glyph as the org mark, and never use the house mark on a model card where a
  glyph belongs.
- Outline is sumi on light grounds, cream on dark. Orange is the only fill,
  and it never carries text ([`brand.md` § Colour](../../docs/brand.md#colour)).
- Keep the tilt. Every plane sits at the same slight nose-up angle; a glyph
  straightened to the grid reads as a different system.
- New models get new common plane designs (bulldog, swallow, …) by a decision
  recorded in the brand log — and `dart` stays reserved-unused.
