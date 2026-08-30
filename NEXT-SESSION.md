# Next Session

Handoff baton for the next cold start — **not** the product backlog.

- **Backlog:** [GitHub Issues](https://github.com/marekkowalczyk/breathe-cli/issues) (see `CLAUDE.md` → Tracking & handoff).
- **This file:** blocking context, decisions not to reopen, process recall aids, and **links** to open issues.
- **Do not** duplicate issue bodies here; **do not** file handoff notes as Issues.

**Canonical repo:** public [`breathe-cli`](https://github.com/marekkowalczyk/breathe-cli). Private `marekkowalczyk/breathe` is archived. Local clone: `~/repos/breathe-cli`.

**Install split:** PATH `breathe` = Homebrew Cellar (last tag); tip = `python3 breathe.py` or `breathe-dev` (see `CLAUDE.md` → Testing). Session footer shows dim `VERSION · RELEASED` right-aligned.

Auto-select: 22:00–05:59 → `night`, 06–11 → `morning`, 12–16 → `midday`, 17–21 → `evening`. Goal words: duration `quick`/`long`; feel `train`/`calm`/`sleep` (5-5 / 4-6 / 3-7). Retired `energize` errors with a pointer to `train`.

## Completed last session

- Science GitHub Pages page (`/science/`) + session-summary URL; ORCID on science + `_config.yml`.
- Feel-axis redesign (`train`/`calm`/`sleep`); midday label → “Main training session”; durations kept.
- Display stay-awake during sessions (#13, earlier on tip).
- Filed [#22](https://github.com/marekkowalczyk/breathe-cli/issues/22) — idea: native GUI (“normie”) app for **macOS + Windows** only (no Linux GUI).
- Closed #20 (goal-word design). Released **v1.13.0**; Homebrew formula bumped.

## Immediate

Nothing blocking. Next product slices from Carried over (#14 progress bar visibility is the lightest UX win).

## Carried over

Pointers only:

- [GH #14](https://github.com/marekkowalczyk/breathe-cli/issues/14) — time progress bar visibility
- [GH #15](https://github.com/marekkowalczyk/breathe-cli/issues/15) — cycle-count progress bar
- [GH #16](https://github.com/marekkowalczyk/breathe-cli/issues/16) — design: scope multi-mode
- [GH #17](https://github.com/marekkowalczyk/breathe-cli/issues/17) — night dimmer TUI
- [GH #18](https://github.com/marekkowalczyk/breathe-cli/issues/18) — night quieter audio
- [GH #19](https://github.com/marekkowalczyk/breathe-cli/issues/19) — pre-commit hook for `RELEASED`
- [GH #21](https://github.com/marekkowalczyk/breathe-cli/issues/21) — `breathe stats` summary from session log
- [GH #22](https://github.com/marekkowalczyk/breathe-cli/issues/22) — idea: GUI app (macOS + Windows)

Community issues on this repo (#4–#11 linux/golang/etc.) are separate and unchanged.

## Current state

| | |
|---|---|
| Tests | `python3 -m unittest test_breathe -q` |
| Tip version | `python3 breathe.py -v` |
| Brew release | `breathe -v` |
| Backlog | GitHub Issues on breathe-cli |
| Science | https://marekkowalczyk.github.io/breathe-cli/science/ |

## Process notes

- **One issue = one shippable slice; one commit = one concern** — see `CLAUDE.md`.
- **Commits** — commit each finished chunk without waiting; **push** only when authorized (`push` / `ship it` / `close, commit, push`).
- **Releases:** `./scripts/suggest-release.sh` after `VERSION` bumps / session close; never auto-tag. Docs audit (README + tap README) before close after fold/release/TUI — see `CLAUDE.md` § Releases.
- **Smoke-test tip** with `python3 breathe.py …` (not PATH `breathe`).
