# Next Session

Handoff baton for the next cold start — **not** the product backlog.

- **Backlog:** [GitHub Issues](https://github.com/marekkowalczyk/breathe-cli/issues) (see `CLAUDE.md` → Tracking & handoff).
- **This file:** blocking context, decisions not to reopen, process recall aids, and **links** to open issues.
- **Do not** duplicate issue bodies here; **do not** file handoff notes as Issues.

**Canonical repo:** public [`breathe-cli`](https://github.com/marekkowalczyk/breathe-cli) (private `breathe` folded in and archived). Local clone path: `~/repos/breathe-cli`.

**Install split:** PATH `breathe` = Homebrew release; tip = `python3 breathe.py` or shell alias `breathe-dev` (see `CLAUDE.md` → Testing). Agents must not smoke-test via PATH `breathe` after code changes.

Auto-select: bare tip maps 22:00–05:59 → `night`, 06–11 → `morning`, 12–16 → `midday`, 17–21 → `evening`. Goal-word `long` still means 20 min duration. Version string: `python3 breathe.py -v` (tip) vs `breathe -v` (brew).

## Immediate

No release overdue if tip `VERSION` matches latest `v*` tag (`./scripts/suggest-release.sh`). Optional: [#19](https://github.com/marekkowalczyk/breathe-cli/issues/19) RELEASED pre-commit hook.

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
| Tip version | `python3 breathe.py -v` (not PATH `breathe`) |
| Brew release | `breathe -v` |
| Backlog | GitHub Issues on breathe-cli |

## Process notes

- **One issue = one shippable slice; one commit = one concern** — see `CLAUDE.md`.
- **Commits** — commit each finished chunk without waiting; **push** only when authorized. See `CLAUDE.md` § Commits.
- **Releases:** run `./scripts/suggest-release.sh` after `VERSION` bumps / session close.
- **Smoke-test tip CLI non-TTY with** `python3 breathe.py -d 1` (not PATH `breathe`).
