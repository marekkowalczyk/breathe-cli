# Next Session

Handoff baton for the next cold start — **not** the product backlog.

- **Backlog:** [GitHub Issues](https://github.com/marekkowalczyk/breathe/issues) (see `CLAUDE.md` → Tracking & handoff).
- **This file:** blocking context, decisions not to reopen, process recall aids, and **links** to open issues.
- **Do not** duplicate issue bodies here; **do not** file handoff notes as Issues.

Installed on this machine: `breathe` symlinked at `/opt/homebrew/bin/breathe` → repo's `breathe.py`, so `git pull` updates the installed command with no reinstall step.

Auto-select (v1.9): bare `breathe` maps 22:00–05:59 → `night` (20 min / 3–7), 06–11 → morning, 12–16 → long, 17–21 → evening. Night UX split: [#8](https://github.com/marekkowalczyk/breathe/issues/8) (dim TUI), [#9](https://github.com/marekkowalczyk/breathe/issues/9) (quiet audio).

## Immediate

Nothing blocking. **Tag and release `v1.9` on GitHub** when ready (`breathe --version` should match tag).

## Completed last session

- ~~Night calming preset + auto-night (v1.9)~~ — `night` 20 min / 3–7; `preset_for_hour`; docs/spec/tests.
- ~~TODO.md → GitHub Issues~~ — backlog policy in `CLAUDE.md`; one-concern hygiene; issues #2–#6, #8–#9 open.
- ~~GH #3 closed~~ — preset/auto shipped; UX → #8, #9.

## Carried over

Pointers only — canonical detail is on each issue:

- [GH #2](https://github.com/marekkowalczyk/breathe/issues/2) — prevent display sleep during session
- [GH #4](https://github.com/marekkowalczyk/breathe/issues/4) — time progress bar visibility
- [GH #5](https://github.com/marekkowalczyk/breathe/issues/5) — cycle-count progress bar (new bar)
- [GH #6](https://github.com/marekkowalczyk/breathe/issues/6) — design: scope multi-mode (no implementation here)
- [GH #8](https://github.com/marekkowalczyk/breathe/issues/8) — night preset: dimmer TUI
- [GH #9](https://github.com/marekkowalczyk/breathe/issues/9) — night preset: quieter audio

## Current state

| | |
|---|---|
| Tests | `python3 -m unittest test_breathe -q` |
| Version | `breathe --version` (expect 1.9) |
| Backlog | GitHub Issues (no `TODO.md`) |

## Process notes

- **One issue = one shippable slice** — see `CLAUDE.md`; split “and also” before filing.
- **When smoke-testing a CLI's non-TTY path, always pass a short explicit duration (`-d 1`).**
- **Don't restate derivable numbers in docs** — reference the source (`VERSION`, test runner, etc.).
