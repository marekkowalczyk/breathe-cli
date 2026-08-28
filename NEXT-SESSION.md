# Next Session

Handoff baton for the next cold start — **not** the product backlog.

- **Backlog:** [GitHub Issues](https://github.com/marekkowalczyk/breathe-cli/issues) (see `CLAUDE.md` → Tracking & handoff).
- **This file:** blocking context, decisions not to reopen, process recall aids, and **links** to open issues.
- **Do not** duplicate issue bodies here; **do not** file handoff notes as Issues.

**Canonical repo:** public [`breathe-cli`](https://github.com/marekkowalczyk/breathe-cli) (private `breathe` folded in and archived).

Installed on this machine: `breathe` symlinked at `/opt/homebrew/bin/breathe` → repo's `breathe.py`, so `git pull` updates the installed command with no reinstall step.

Auto-select: bare `breathe` maps 22:00–05:59 → `night`, 06–11 → `morning`, 12–16 → `midday`, 17–21 → `evening`. Goal-word `long` still means 20 min duration. `breathe -v` prints `VERSION` + `RELEASED`.

## Immediate

Run `./scripts/suggest-release.sh` — release due if `VERSION` ahead of latest public tag. Tag/`gh release` only after user authorizes. Optional: [#19](https://github.com/marekkowalczyk/breathe-cli/issues/19) RELEASED pre-commit hook.

## Carried over

Pointers only — canonical detail is on each issue (migrated from private breathe):

- [GH #13](https://github.com/marekkowalczyk/breathe-cli/issues/13) — prevent display sleep during session (was private #2)
- [GH #14](https://github.com/marekkowalczyk/breathe-cli/issues/14) — time progress bar visibility (was #4)
- [GH #15](https://github.com/marekkowalczyk/breathe-cli/issues/15) — cycle-count progress bar (was #5)
- [GH #16](https://github.com/marekkowalczyk/breathe-cli/issues/16) — design: scope multi-mode (was #6)
- [GH #17](https://github.com/marekkowalczyk/breathe-cli/issues/17) — night dimmer TUI (was #8)
- [GH #18](https://github.com/marekkowalczyk/breathe-cli/issues/18) — night quieter audio (was #9)
- [GH #19](https://github.com/marekkowalczyk/breathe-cli/issues/19) — pre-commit hook for `RELEASED` (was #10)
- [GH #20](https://github.com/marekkowalczyk/breathe-cli/issues/20) — design: rethink goal-word vocabulary (was #11)

Community issues on this repo (#4–#11 linux/golang/etc.) are separate and unchanged.

## Current state

| | |
|---|---|
| Tests | `python3 -m unittest test_breathe -q` |
| Version | `breathe -v` |
| Backlog | GitHub Issues on breathe-cli |

## Process notes

- **One issue = one shippable slice; one commit = one concern** — see `CLAUDE.md`.
- **Commits** — commit each finished chunk without waiting; **push** only when authorized. See `CLAUDE.md` § Commits.
- **Releases:** run `./scripts/suggest-release.sh` after `VERSION` bumps / session close.
- **Smoke-test CLI non-TTY with `-d 1`**.
