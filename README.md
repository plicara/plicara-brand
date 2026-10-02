<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="logo/mark-colour-dark.svg" />
  <img src="logo/mark-colour.svg" alt="Plicara Labs" width="96" />
</picture>

# plicara-brand

**The Plicara Labs brand, as code.**

</div>

---

Tokens, marks, the logo set, and the generators that draw them. Everything
here is generated: each directory has a README and a build script, and the
committed SVGs and rasters are the scripts' output. **Change the script,
never the SVGs.**

```
logo/     house mark, lockups, avatars, favicon, raster exports  (build.py)
marks/    one paper-plane glyph per model, plus the generator    (generate.py)
tokens/   palette, schemes and typesets as CSS custom properties
          and JSON                                               (build.py)
```

This repository was split out of the lab's private notebook with its history
(`git subtree split`), so the drawings carry their own record of how they got
this way.

## The contract

This repo is a **producer**. Consumers copy files out of it and check the
copies:

- [`plicara.github.io`](https://github.com/plicara/plicara.github.io)
  vendors the tokens, the mark set and the plane glyphs via its
  `tools/vendor.py`; its `vendor-parity` CI job fails when the copies drift
  from this repo. If a vendored file needs to change, change it **here** and
  run `--sync` there.

Two audits keep this repo honest on its own:

- `tokens/build.py` audits the hand-written `tokens.css` against the palette
  and the fill guards, and fails on any WCAG pairing that stops clearing AA.
- `tokens/print.py` audits its press palette against the token palette on
  import: a name the two share must mean the same hex, and a hex they share
  must carry a token-side name. One word, one colour.

## Building

```
make setup
make build
```

`make setup` also runs `npm ci --ignore-scripts`. `node_modules/` is committed on purpose: it vendors the two font packages the build draws from, so a rebuild needs no network and cannot drift with an upstream release. The lockfile pins them; `npm ci` restores the same tree.

Outputs are byte-reproducible; a clean rebuild that changes any committed
file is a bug in the scripts or an intended design change, never noise. The `Build and audit` workflow enforces this: it rebuilds on every push and fails on any diff. One exception: `logo/png/social-card-1200x630.png` sets its caption in the system monospace font, so it is excluded from the check until the caption is drawn as outlines.

## What this is not

The brand *rules* — naming, voice, usage, accessibility, the decision log —
live in the lab's private notebook (`docs/brand.md` there), not here. This
repo is the buildable half: values and drawings. If a value here seems to
contradict a rule, the notebook wins and the fix lands here second.

## License

All rights reserved. These are trademarks-in-use of Plicara Labs; the
repository is public so that consumers can vendor and verify, not so the
identity can be reused.

## Working in this repository

Project metadata and research context live in [.plicara/README.md](.plicara/README.md); agent constraints live in [AGENTS.md](AGENTS.md). Use `make setup` and `make check` for the default local environment and verification. Expensive experiments, model downloads, and publication are separate explicit steps. Project status is authoritative in `.plicara/project.yaml`; no central board update is required.
