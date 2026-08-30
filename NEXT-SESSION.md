# Next Session

Handoff baton for the next cold start — **not** the product backlog.

- **Backlog:** [GitHub Issues](https://github.com/marekkowalczyk/breathe-cli/issues) (see `CLAUDE.md` → Tracking & handoff).
- **This file:** blocking context, decisions not to reopen, process recall aids, and **links** to open issues.
- **Do not** duplicate issue bodies here; **do not** file handoff notes as Issues.

**Canonical repo:** public [`breathe-cli`](https://github.com/marekkowalczyk/breathe-cli). Private `marekkowalczyk/breathe` is archived. Local clone: `~/repos/breathe-cli`.

**Install split:** PATH `breathe` = Homebrew Cellar (last tag); tip = `python3 breathe.py` or `breathe-dev` (see `CLAUDE.md` → Testing). Session footer shows dim `VERSION · RELEASED` right-aligned. Pip: `pip install breathe-cli` (auto-publishes from GitHub Release — see `CLAUDE.md` § Releases).

Auto-select: 22:00–05:59 → `night`, 06–11 → `morning`, 12–16 → `midday`, 17–21 → `evening`. Goal words: duration `quick`/`long`; feel `train`/`calm`/`sleep` (5-5 / 4-6 / 3-7). Retired `energize` errors with a pointer to `train`. Science: https://marekkowalczyk.github.io/breathe-cli/science/

## Completed last session

- Trusted Publishing workflow + `check-version-sync.sh`; README PyPI install + badges (PyPI / Homebrew / MIT / Show HN).
- Show HN audit → parked [#28](https://github.com/marekkowalczyk/breathe-cli/issues/28) (HRV closed-loop); no other new issues; no HN necro update.
- Cursor GitHub MCP wired via process env PAT (`gh auth token`); smoke create/close #29.

## Immediate

Unpushed commits exist — **push when authorized** (README + close artifacts). Then next product slice: **#23** (Linux vs macOS-only for homebrew/core). Lightest UX otherwise: #14.

## Carried over

Pointers only:

- **[Milestone: homebrew/core](https://github.com/marekkowalczyk/breathe-cli/milestone/1)**
  - [GH #23](https://github.com/marekkowalczyk/breathe-cli/issues/23) — Linux vs macOS-only
  - [GH #24](https://github.com/marekkowalczyk/breathe-cli/issues/24) — formula token
  - [GH #25](https://github.com/marekkowalczyk/breathe-cli/issues/25) — `brew audit --new --strict`
  - [GH #26](https://github.com/marekkowalczyk/breathe-cli/issues/26) — submit core PR
  - [GH #27](https://github.com/marekkowalczyk/breathe-cli/issues/27) — post-merge bumps + tap deprecation
- [GH #14](https://github.com/marekkowalczyk/breathe-cli/issues/14) — time progress bar visibility
- [GH #15](https://github.com/marekkowalczyk/breathe-cli/issues/15) — cycle-count progress bar
- [GH #16](https://github.com/marekkowalczyk/breathe-cli/issues/16) — design: scope multi-mode
- [GH #17](https://github.com/marekkowalczyk/breathe-cli/issues/17) — night dimmer TUI
- [GH #18](https://github.com/marekkowalczyk/breathe-cli/issues/18) — night quieter audio
- [GH #19](https://github.com/marekkowalczyk/breathe-cli/issues/19) — pre-commit hook for `RELEASED`
- [GH #21](https://github.com/marekkowalczyk/breathe-cli/issues/21) — `breathe stats`
- [GH #22](https://github.com/marekkowalczyk/breathe-cli/issues/22) — idea: GUI (macOS + Windows)
- [GH #28](https://github.com/marekkowalczyk/breathe-cli/issues/28) — idea: HRV closed-loop biofeedback (parked)

Community issues (#4–#11 linux/golang/etc.) unchanged.

## Current state

| | |
|---|---|
| Tests | `python3 -m unittest test_breathe -q` |
| Tip version | `python3 breathe.py -v` |
| Brew release | `breathe -v` |
| Backlog | GitHub Issues / [homebrew/core milestone](https://github.com/marekkowalczyk/breathe-cli/milestone/1) |

## Process notes

- **Wrap-up → session-close skill** — see `CLAUDE.md` § Session close. Housekeeping ship ≠ close.
- **No live URL until remote has the tip** — see `CLAUDE.md` § Releases.
- **PyPI:** GitHub Release → `publish.yml` (Trusted Publishing); confirm Actions green before claiming `pip` is updated. Keep `VERSION` ↔ `pyproject.toml` in sync (`./scripts/check-version-sync.sh`).
- **Cursor GitHub MCP:** Dock launch often lacks `GITHUB_PERSONAL_ACCESS_TOKEN`. Relaunch with `open -a Cursor --env GITHUB_PERSONAL_ACCESS_TOKEN="$(gh auth token)"`. `gh` keyring ≠ MCP. Fallback: `gh issue create`.
- One issue = one shippable slice; one commit = one concern.
- Push only when authorized; smoke tip with `python3 breathe.py`, not PATH `breathe`.
- Releases: `./scripts/suggest-release.sh`; never auto-tag.
- **HN:** do not necro old Show HN with status dumps; optional under-comment reply only.
