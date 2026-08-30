# Roadmap candidates (not yet issues)

Captured 2026-08-30. Convert selected items into GitHub Issues later (one concern each; see `CLAUDE.md` → Tracking & handoff). This file is **not** the backlog — Issues are.

## Philosophy filter (what “fits”)

From README / `CLAUDE.md` / the spec, good roadmap items tend to:

- Keep **one file, stdlib, no deps**
- Stay inside the **safety envelope** (no holds, no rapid cycles, always restore the terminal)
- Serve a **daily open-loop habit**, not a medical device or sensor product
- Prefer **soft-fail degradation** over hard requirements
- Prefer **science → product**, one shippable slice per issue

### Already well-covered (do not re-file)

| Theme | Issues |
|---|---|
| homebrew/core | #23–#27 (milestone) |
| TUI polish | #14, #15, #17, #18 |
| `breathe stats` | #21 |
| Multi-mode design | #16 |
| Parked GUI / HRV | #22, #28 |
| Community Linux sound | #4, #6, #7 |
| Screenshots | #9 |
| Alt patterns research | #8 |
| Go rewrite (community Q) | #11 |

---

## High fit (CLI product, small surface)

### 1. `breathe doctor` (or `--check`)

Report audio backend, display-wake, TTY/colour/`NO_COLOR`, log path, Python version; never abort a session. Helps #23 and support without becoming a config system.

### 2. Machine-readable session summary (`--json`)

One JSON object to stdout on exit and/or for stats consumers — Shortcuts, scripts, #21. Unix-y; no UI bloat.

### 3. macOS accessibility cues via `say` (opt-in)

Spoken IN/OUT for eyes-closed / low-vision use. Fits “macOS tools we already spawn” (`afplay`/`caffeinate`) and clinical accessibility better than a second visual chrome.

### 4. man page + formula `test do` beyond `--version`

Process/distribution craft that feeds #25/#26; also makes the tool feel finished on Homebrew.

### 5. README / science “habit scaffolding” without a daemon

Documented LaunchAgent / Shortcuts / cron recipes (“run `breathe` at 07:30”). Habit is the product goal; in-app schedulers fight the single-file ethos. **Docs only.**

### 6. Named-pattern safety rejections

If someone passes folklore names (`box`, `4-7-8` as a word, Wim Hof–ish flags), reject with the same safety rationale as three-number ratios. Strengthens C1/C2 without adding patterns (#8 stays research → usually “document why not”).

### 7. Log schema version / forward-compat for #21

Tiny header or documented column contract so `stats` doesn’t paint you into a corner. Process/product hygiene, not a feature.

### 8. Terminal resize / narrow-layout hardening

Footer stamp already drops on narrow terminals; focused “don’t corrupt the frame on SIGWINCH / tiny panes” matches “terminal is sacred” better than more chrome.

---

## Medium fit (docs / trust / discovery)

### 9. Screenshot / asciinema refresh

Still open as #9; treat as release hygiene after TUI changes (#14/#15), not a forever backlog orphan. (May just prioritize #9 rather than a new issue.)

### 10. Annual or milestone literature pass on `/science/`

Explicit issue: re-check Bernardi/Tsai/Laborde claims and preset map. Matches “science before product” and prevents citation drift.

### 11. Stronger “not a medical device / not diagnostic” pass

On `--safety`, README, and science page — especially with HFrEF framing and parked #28. Trust and scope control, not features.

### 12. Official Windows *CLI* stance (decision issue)

Wake path already has Win32; audio is bell-ish. Separate from GUI #22: either document “works degraded” or “unsupported.” Helps #23 thinking without promising Linux sound QoL.

---

## Lower priority / reach without #22

### 13. Apple Shortcuts / shell-script recipe pack

Docs only — “normie” adjacent without a GUI codebase. May merge with #5.

### 14. zsh/bash completion for presets + goal words

Polish; only if it stays a tiny static file or generated snippet, not a completion framework.

---

## Keep off the roadmap (or leave parked)

| Temptation | Why it fights the repo |
|---|---|
| Config files, themes, plugin sounds | Breaks “no config / nothing to break” |
| Accounts, sync, streaks-as-gamification | Wrong product shape; #21 should stay read-only summary |
| Implementing #8 as new modes / holds | Spec §2 forbids the interesting ones |
| Shipping #28 as BLE-in-`breathe.py` | Different product; keep design-first or out-of-tree |
| Go rewrite (#11) as *your* plan | Community question; identity is the constrained Python file |
| Always-on reminders / agents inside the app | Daemon + state; docs/LaunchAgent are enough |
| Clinical dashboards / “share with your cardiologist” | Medical-device gravity |

---

## Suggested first filings (if only a few)

1. `breathe doctor`
2. Opt-in `say` cues
3. man page (tied to homebrew/core)
4. Named unsafe-pattern rejections
5. Science literature refresh cadence

When filing: verb + single deliverable title; explicit **In** / **Out**; testable acceptance checklist; link siblings (#21, #23–#27, #8, #9, #22, #28 as relevant).
