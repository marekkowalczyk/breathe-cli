# Next Session

Handoff baton for the next cold start — **not** the product backlog.

- **Backlog:** [GitHub Issues](https://github.com/marekkowalczyk/breathe/issues) (see `CLAUDE.md` → Tracking & handoff).
- **This file:** blocking context, decisions not to reopen, process recall aids, and **links** to open issues.
- **Do not** duplicate issue bodies here; **do not** file handoff notes as Issues.

Installed on this machine: `breathe` symlinked at `/opt/homebrew/bin/breathe` → repo's `breathe.py`, so `git pull` updates the installed command with no reinstall step.

Auto-select (v1.10): bare `breathe` maps 22:00–05:59 → `night`, 06–11 → `morning`, 12–16 → `midday`, 17–21 → `evening`. Preset names are chronological time-of-day; goal-word `long` still means 20 min duration. `breathe -v` prints `VERSION` + `RELEASED`.

## Immediate

Nothing blocking. Run `./scripts/suggest-release.sh` — if it reports a release due, tag+`gh release create` only after the user authorizes a release. Optional: implement [#10](https://github.com/marekkowalczyk/breathe/issues/10) (RELEASED pre-commit hook).

## Completed last session

- ~~Rename preset `long` → `midday`; chronological preset order~~
- ~~Issue-opening policy + atomic commit policy~~ — `CLAUDE.md` Tracking & handoff / Commits

## Carried over

Pointers only — canonical detail is on each issue:

- [GH #2](https://github.com/marekkowalczyk/breathe/issues/2) — prevent display sleep during session
- [GH #4](https://github.com/marekkowalczyk/breathe/issues/4) — time progress bar visibility
- [GH #5](https://github.com/marekkowalczyk/breathe/issues/5) — cycle-count progress bar
- [GH #6](https://github.com/marekkowalczyk/breathe/issues/6) — design: scope multi-mode
- [GH #8](https://github.com/marekkowalczyk/breathe/issues/8) — night dimmer TUI
- [GH #9](https://github.com/marekkowalczyk/breathe/issues/9) — night quieter audio
- [GH #10](https://github.com/marekkowalczyk/breathe/issues/10) — pre-commit hook for `RELEASED`

## Current state

| | |
|---|---|
| Tests | `python3 -m unittest test_breathe -q` |
| Version | `breathe -v` |
| Backlog | GitHub Issues |

## Process notes

- **One issue = one shippable slice; one commit = one concern** — see `CLAUDE.md`.
- **When to open an issue** — file first if scope can fork or must survive the session; skip for one-commit obvious fixes.
- **Commits** — atomic, imperative subjects, why in the body; **commit each finished chunk without waiting to be asked**. **Push** only when the user authorizes publish (`push`, `ship it`, `close, commit, push`, …) — that covers the current unpushed batch, not later sessions. See `CLAUDE.md` § Commits.
- **Versioning:** `RELEASED` with product/`VERSION` bumps; prefer [#10](https://github.com/marekkowalczyk/breathe/issues/10) once hooked.
- **Releases:** after `VERSION` bumps / on session close, run `./scripts/suggest-release.sh` (see `CLAUDE.md` § Releases). Never auto-tag.
- **Smoke-test CLI non-TTY with `-d 1`**, never default duration.
- **Don't restate derivable numbers in docs** — reference `VERSION` / `RELEASED` / tests.
