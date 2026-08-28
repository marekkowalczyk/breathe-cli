---
title: 'Breathe CLI — Safety & Acceptance Tests'
subtitle: 'Reference document for a paced-breathing terminal app'
author: 'Marek Kowalczyk (spec by Claude, for Claude Opus 4.6)'
date: 2026-07-29
version: 1.8
target_platform: 'macOS 10.14.6 (Mojave)'
target_runtime: 'Python 3.7+ stdlib only'
status: 'implementation complete — this document retains safety constraints and acceptance tests'
---

## 1. Purpose

This document preserves the safety constraints and acceptance tests for
`breathe.py`. The code is the authority for behaviour; this file exists
to keep the non-negotiable safety rationale and the manual test suite in
one place where they won't be eroded by incremental changes.

For implementation constraints, see `CLAUDE.md`.

## 2. Safety constraints

These are load-bearing design constraints, not features to be added
later. They rule out whole categories of functionality.

**C1. No breath retention.** The app must never prompt for a hold phase.
Valid ratios are inhale:exhale only. If a user tries to pass a
three-number ratio (e.g. `4-7-8`), the app rejects with a clear error
referencing the safety rationale.

**C2. No rapid breathing.** The app must not allow total breath cycles
shorter than 8 seconds (i.e. >7.5 bpm). Hyperventilation-adjacent
patterns mobilise catecholamines — the opposite of the vagal intent.

**C3. Visible warning signs.** The safety screen (`--safety`) lists the
specific stop-session symptoms: lightheadedness, palpitations, tingling
in hands or face.

**C4. Graceful interruption.** The session can be ended at any moment
by a single keypress or `Ctrl+C`. Exit must always succeed — no stuck
animation loops, no terminal left in a broken state.

**C5. Pre-session settle.** Every session begins with a 3-second
countdown during which the user can settle, close other apps, or abort
without having "missed" any breaths.

**C6. Goal-word shorthand stays inside the safe envelope.** The
order-free `breathe quick calm` style shorthand (`GOAL_DURATION_WORDS`,
`GOAL_RATIO_WORDS` in `breathe.py`) only ever resolves to fixed,
pre-validated duration/ratio pairs — the same constraints (C1, C2) still
apply, and ambiguous or conflicting word combinations (e.g. `breathe
quick long`) are rejected with an explicit error rather than guessed.

### Rejected inputs (with explicit safety messaging)

| User input | Response |
|------------|----------|
| `--ratio 4-7-8` | Error: "Three-number ratios imply a breath hold. This app does not support breath retention. See `breathe --safety`." |
| `--ratio 2-2` | Error: "Total breath cycle must be ≥ 8 seconds (no rapid breathing)." |
| `--ratio foo` | Error: "Ratio must be in the form `inhale-exhale` (e.g. `5-5` or `4-6`)." |
| `--duration 0` | Error: "Duration must be 1–60 minutes." |
| `--duration 120` | Error: "Duration must be 1–60 minutes." |

## 3. Acceptance tests

Manual tests, no framework required. Run in order.

### 3.1 Smoke tests

1. `breathe --help` prints help and exits 0.
2. `breathe --version` and `breathe -v` print `breathe {VERSION} {RELEASED}` (matching `version_string()` in `breathe.py`: semver plus minute-precision local datetime) and exit 0.
3. `breathe --safety` prints the safety block and exits 0.
4. `breathe --list-presets` prints the preset table **and** the goal-word vocabulary (driven by `GOAL_*` maps), then exits 0.
4a. `breathe -h` / `--help` epilog lists every goal word (`quick`/`long`, `calm`/`energize`) with effects — not only a cryptic example.
5. `breathe -d 1` runs for ~60 seconds, renders breath animation, exits cleanly with `completed` status.
5a. During a session on a wide enough terminal, the footer shows dim key hints on the left and a right-aligned `VERSION · RELEASED` stamp (same constants as `version_string()`, without the `breathe` prefix). On a very narrow terminal the stamp may drop entirely; hints must remain.
6. `breathe --preset morning` starts a 10-minute 5-5 session. `Ctrl+C` during the first minute exits within 1 second and the terminal is fully usable (prompt returns on its own line, cursor visible, no leftover colour).
6a. `breathe --preset night` starts a 20-minute 3-7 session (header shows `night · 3-7 · …`).
6b. `breathe --list-presets` includes a `night` row (20 min, 3s-7s).

### 3.2 Safety-rejection tests

7. `breathe -r 4-7-8` exits non-zero with the three-number ratio error message.
8. `breathe -r 2-2` exits non-zero with the "cycle must be ≥ 8 seconds" error.
9. `breathe -d 0` exits non-zero with the duration-range error.
10. `breathe -d 120` exits non-zero with the duration-range error.

### 3.3 Degradation tests

11. With `NO_COLOR=1 breathe -d 1`, the session renders without ANSI colour and still completes.
12. `breathe -d 1 | cat` (non-TTY stdout) prints a warning, runs for 60 seconds, and prints a summary — without an animated frame loop.
13. Rename `/usr/bin/afplay` temporarily (or `chmod -x`), run `breathe -d 1`: startup warns about audio fallback, session runs, bell is heard at phase transitions.
14. Repeat test 13 with `breathe --quiet -d 1`: no startup warning is printed, session runs normally with bell fallback.

### 3.4 Runtime-control tests

15. During a session, pressing `space` freezes the bar and countdown at their current positions and the header shows `‖`. Pressing `space` again resumes: the bar resets to the beginning of INHALE and the countdown snaps back to the last completed cycle boundary. The interrupted cycle does not count toward breaths. If you pause for 30 seconds during a 1-minute session, the session should take ~90 seconds wall-clock to complete (completed breathing time is still exactly 60 seconds).
16. During a session, pressing `s` toggles the mute indicator `🔇` and stops/restores sound without pausing.
17. During a session, pressing `q` exits with `ended early (user)` status within 1 second.

### 3.5 Terminal-restoration test

18. Inject a deliberate `raise RuntimeError('boom')` inside the render loop. Run the app. Confirm: summary prints, then traceback, then prompt returns on its own line with cursor visible and no lingering colour codes.

### 3.6 Time-of-day default test

19. Run `breathe` with no arguments at different times of day (or call `preset_for_hour`). Verify:
    - 22:00–05:59: header shows `night · 3-7 · 20:00 ...` (counting down)
    - 06:00–11:59: header shows `morning · 5-5 · 10:00 ...` (counting down)
    - 12:00–16:59: header shows `midday · 4-6 · 20:00 ...` (counting down)
    - 17:00–21:59: header shows `evening · 4-6 · 15:00 ...` (counting down)

### 3.7 Session logging tests

20. `breathe -d 1` completes. Check `~/.breathe_log.csv` exists, has a header row and one data row with correct fields. `completion_pct` is `100`, `status` is `completed`.
21. `breathe -d 1`, then `Ctrl+C` after ~10 seconds. Log has a new row with `status` = `ended early (user)` and `completion_pct` < 100.
22. `breathe --no-log -d 1` completes. Log file row count has not increased.
23. `breathe --log` prints the log file path and exits 0.
24. Delete `~/.breathe_log.csv`, run `breathe --log`: prints path with "(no sessions logged yet)".
25. `chmod 000 ~/.breathe_log.csv`, run `breathe -d 1`: session completes normally, stderr shows a one-line warning about logging failure. Restore permissions afterwards.

### 3.8 Goal-word shorthand tests

26. `breathe quick calm` and `breathe calm quick` both start a 3-minute 4-6 session — order does not change the result.
27. `breathe quick long` exits non-zero with a "Conflicting duration words" error.
28. `breathe quick -n` (a goal word combined with a flag) falls through to argparse's normal "unrecognized arguments" error rather than silently applying `quick` and ignoring `-n`.
