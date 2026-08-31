# Next Session

Handoff baton for the next cold start — **not** the product backlog.

- **Backlog:** [GitHub Issues](https://github.com/marekkowalczyk/breathe-cli/issues) (see `CLAUDE.md` → Tracking & handoff).
- **This file:** blocking context, decisions not to reopen, process recall aids, and **links** to open issues.
- **Do not** duplicate issue bodies here; **do not** file handoff notes as Issues.

**Canonical repo:** public [`breathe-cli`](https://github.com/marekkowalczyk/breathe-cli). Private `marekkowalczyk/breathe` is archived. Local clone: `~/repos/breathe-cli`.

**Install split:** PATH `breathe` = Homebrew Cellar (last tag); tip = `python3 breathe.py` or `breathe-dev` (see `CLAUDE.md` → Testing). Session footer shows dim `VERSION · RELEASED` right-aligned. Pip: `pip install breathe-cli` (auto-publishes from GitHub Release — see `CLAUDE.md` § Releases).

**Platform:** macOS primary; Linux/Windows secondary, community-only (maintainer has neither machine). Bare `breathe` = omakase (time-of-day → preset); see `CLAUDE.md` → Default invocation (DHH / Omacom naming credit). Goal words: duration `quick`/`long`; feel `train`/`calm`/`sleep`. Science: https://marekkowalczyk.github.io/breathe-cli/science/

## Completed last session

- Platform stance + Linux sound on tip (**v1.14.0**): probe/`--sound-player`/`BREATHE_SOUND_*`, bell fallback; credit PR #10 / @kenlacroix. Closed #4, #6, #7, #23; superseded PR #10. PR #5 → speculative #30.
- Omakase enshrined in `CLAUDE.md` + README with DHH/Omacom links.
- Filed [#31](https://github.com/marekkowalczyk/breathe-cli/issues/31) (opt-in menu interview).

## Immediate

Nothing blocking. **v1.14.0** released (tag + GitHub Release + PyPI + Homebrew tap bump). Upgrade: `brew upgrade breathe` / `pip install -U breathe-cli`.

Optional next slices: lightest UX **#14**, or homebrew/core **#24** (token) now that #23 leaned (B).

## Carried over

Pointers only:

- **Candidates → Issues later:** [`ROADMAP-CANDIDATES.md`](ROADMAP-CANDIDATES.md) (delete or prune after filing)
- **[Milestone: homebrew/core](https://github.com/marekkowalczyk/breathe-cli/milestone/1)** — #23 closed (lean B); remaining:
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
- [GH #30](https://github.com/marekkowalczyk/breathe-cli/issues/30) — speculative 2.0 coherence / short-hold (parked)
- [GH #31](https://github.com/marekkowalczyk/breathe-cli/issues/31) — opt-in menu interview (do not replace omakase)

Community: #8 research, #9 screenshots, #11 Go rewrite Q — unchanged.

## Current state

| | |
|---|---|
| Tests | `python3 -m unittest test_breathe -q` |
| Tip version | `python3 breathe.py -v` → `1.14.0` |
| Brew release | `breathe -v` → Cellar lags until release |
| Backlog | GitHub Issues / [homebrew/core milestone](https://github.com/marekkowalczyk/breathe-cli/milestone/1) |
| Roadmap park | `ROADMAP-CANDIDATES.md` (not Issues) |

## Process notes

- **Roadmap brainstorm park:** multi-slice ideas worth keeping but not ready to file → `ROADMAP-CANDIDATES.md`; convert to one-concern Issues later; prune/delete the file after. Do not dump into NEXT-SESSION as a backlog.
- **Same-name on another registry:** add a README “Not the same project” line under Installation promptly.
- **After a tip VERSION bump:** remind once to smoke with `python3 breathe.py -v` / `python3 breathe.py …`, not PATH `breathe` (Cellar lags until release + brew upgrade). See `CLAUDE.md` § Testing.
- **Wrap-up → session-close skill** — see `CLAUDE.md` § Session close. Housekeeping ship ≠ close.
- **No live URL until remote has the tip** — see `CLAUDE.md` § Releases.
- **PyPI:** GitHub Release → `publish.yml` (Trusted Publishing); confirm Actions green before claiming `pip` is updated. Keep `VERSION` ↔ `pyproject.toml` in sync (`./scripts/check-version-sync.sh`).
- **Cursor GitHub MCP:** Dock launch often lacks `GITHUB_PERSONAL_ACCESS_TOKEN`. Relaunch with `open -a Cursor --env GITHUB_PERSONAL_ACCESS_TOKEN="$(gh auth token)"`. `gh` keyring ≠ MCP. Fallback: `gh issue create`.
- One issue = one shippable slice; one commit = one concern.
- Push only when authorized; smoke tip with `python3 breathe.py`, not PATH `breathe`.
- Releases: `./scripts/suggest-release.sh`; never auto-tag.
- **HN:** do not necro old Show HN with status dumps; optional under-comment reply only.
