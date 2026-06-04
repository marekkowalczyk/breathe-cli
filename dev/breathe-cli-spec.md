---
title: 'Breathe CLI — Safety & Acceptance Tests'
subtitle: 'Reference document for a paced-breathing terminal app'
author: 'Marek Kowalczyk (spec by Claude, for Claude Opus 4.6)'
date: '2026-06-03'
version: 2.0
target_platform: 'macOS 10.14.6 (Mojave) & Windows 11'
target_runtime: 'Python 3.7+ stdlib only'
status: 'implementation complete — this document retains safety constraints and acceptance tests'

> **Version 2.0 change:** Optional short breath hold (≤4 s) is now supported
> via the `--hold` flag on the new `coherence` preset. All previous safety
> rationale is preserved; the hold is a property of the preset, not a free
> parameter. See §2 C1.
---

## 1. Purpose

This document preserves the safety constraints and acceptance tests for
`breathe.py`. The code is the authority for behaviour; this file exists
to keep the non-negotiable safety rationale and the manual test suite in
one place where they won't be eroded by incremental changes.

For implementation constraints, see `../CLAUDE.md`.

## 2. Safety constraints

These are load-bearing design constraints, not features to be added
later. They rule out whole categories of functionality.

**C1. Optional short breath hold.** A `--hold N` flag is supported only
on the `coherence` preset, with N in 0–4 seconds (the `coherence` preset
itself uses 4 s). Holds longer than 4 s cross into Valsalva territory
and have no clinical evidence base in HFrEF. The flag is rejected:

- with N > 4 (any preset),
- when combined with a preset other than `coherence`,
- when combined with a custom `--ratio` (hold is a property of the
  preset, not a free parameter).

The hold is rendered as a discrete `HOLD` phase between INHALE and
EXHALE, with a single terminal-bell cue at phase entry. There is no
hold after EXHALE — the breath cycle is IN → HOLD → EXHALE, three
phases. No three-number `--ratio` form is supported; users wanting a
hold must use `--preset coherence`.

**C2. No rapid breathing.** The app must not allow total breath cycles
shorter than 8 seconds (i.e. >7.5 bpm). Hyperventilation-adjacent
patterns mobilise catecholamines — the opposite of the vagal intent.
The total cycle includes the hold (e.g. `coherence` 4-4-4 = 12 s = 5
bpm, well above the 8 s floor).

**C3. Visible warning signs.** The safety screen (`--safety`) lists the
specific stop-session symptoms: lightheadedness, palpitations, tingling
in hands or face.

**C4. Graceful interruption.** The session can be ended at any moment
by a single keypress or `Ctrl+C`. Exit must always succeed — no stuck
animation loops, no terminal left in a broken state.

**C5. Pre-session settle.** Every session begins with a 3-second
countdown during which the user can settle, close other apps, or abort
without having "missed" any breaths.

### Rejected inputs (with explicit safety messaging)

| User input | Response |
|------------|----------|
| `--hold 5` | Error: "Hold must be 0–4 seconds (no clinical evidence for longer holds in HFrEF)." |
| `--hold 2 --preset balanced` | Error: "Hold is supported only on the `coherence` preset." |
| `--ratio 4-6 --hold 2` | Error: "Hold cannot be combined with a custom ratio. Use `--preset coherence`." |
| `--ratio 2-2` | Error: "Total breath cycle must be ≥ 8 seconds (no rapid breathing)." |
| `--ratio 4-7-8` | Error: "Ratio must be in the form `inhale-exhale` (e.g. `5-5` or `4-6`). To add a hold, use `--hold N` with the `coherence` preset." |
| `--ratio foo` | Error: "Ratio must be in the form `inhale-exhale` (e.g. `5-5` or `4-6`)." |
| `--ratio 3-7` | Error: "Exhale must not exceed twice the inhale (no clinical evidence for extreme ratios). See README.md for details." |
| `--duration 0` | Error: "Duration must be 1–60 minutes." |
| `--duration 120` | Error: "Duration must be 1–60 minutes." |

## 3. Acceptance tests

Manual tests, no framework required. Run in order.

### 3.1 Smoke tests

1. `breathe --help` prints help and exits 0.
2. `breathe --version` prints `breathe 2.0` and exits 0.
3. `breathe --safety` prints the safety block and exits 0.
4. `breathe --list-presets` prints the preset table and exits 0.
5. `breathe -d 1` runs for ~60 seconds, renders breath animation, exits cleanly with `completed` status.
6. `breathe --preset balanced` starts a 10-minute 5-5 session. `Ctrl+C` during the first minute exits within 1 second and the terminal is fully usable (prompt returns on its own line, cursor visible, no leftover colour).

### 3.2 Safety-rejection tests

7. `breathe -r 4-7-8` exits non-zero with the ratio-format error (the hold is now passed via `--hold`, not a three-number ratio).
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

19. Run `breathe` with no arguments at different times of day (or mock `time.localtime`). Verify:
    - Before noon: header shows `balanced · 5-5 · 10:00 ...` (counting down)
    - 12:00–16:59: header shows `extended · 4-6 · 20:00 ...` (counting down)
    - 17:00+: header shows `calm · 4-6 · 15:00 ...` (counting down)

### 3.7 Session logging tests

20. `breathe -d 1` completes. Check `~/.breathe_log.csv` exists, has a header row and one data row with correct fields. `completion_pct` is `100`, `status` is `completed`.
21. `breathe -d 1`, then `Ctrl+C` after ~10 seconds. Log has a new row with `status` = `ended early (user)` and `completion_pct` < 100.
22. `breathe --no-log -d 1` completes. Log file row count has not increased.
23. `breathe --log` prints the log file path and exits 0.
24. Delete `~/.breathe_log.csv`, run `breathe --log`: prints path with "(no sessions logged yet)".
25. `chmod 000 ~/.breathe_log.csv`, run `breathe -d 1`: session completes normally, stderr shows a one-line warning about logging failure. Restore permissions afterwards.

### 3.8 Hold-validation tests

26. `breathe --hold 5` exits non-zero with "Hold must be 0–4 seconds".
27. `breathe --hold -1` exits non-zero with the same hold-range error.
28. `breathe --preset balanced --hold 2` exits non-zero with "Hold is supported only on the `coherence` preset."
29. `breathe --preset extended --hold 4` exits non-zero with the same message.
30. `breathe -r 4-6 --hold 2` exits non-zero with "Hold cannot be combined with a custom ratio. Use `--preset coherence`."
31. `breathe -d 1 --hold 2` (custom duration with custom hold) exits non-zero with the same message.

### 3.9 Coherence preset state-machine tests

32. `breathe --preset coherence` starts a 10-minute 4-4-4 session. The header shows `coherence · 4-4-4 · 10:00 ...` (counting down). The phase display cycles through `INHALE → HOLD → EXHALE → INHALE ...` in 4-second beats; the bar fills during INHALE, holds a full static bar during HOLD (no animation), and drains during EXHALE.
33. During a coherence session, listen at each phase transition: a single terminal-bell cue is audible on entry to HOLD. There is no bell on entry to INHALE or EXHALE (those use the existing `afplay` / `winsound` cues).
34. During a coherence session, press `space` while the phase is `HOLD`. The header shows `‖`, the bar freezes at full, and the countdown freezes. Press `space` again: the bar resets to the beginning of INHALE, the countdown snaps back to the last completed-cycle boundary, and the interrupted HOLD is not counted. (Pause from HOLD must resume to INHALE, never to HOLD — HOLD is a transient state.)
35. `breathe --preset coherence` runs to completion in 10 minutes (50 cycles of 12 s). `~/.breathe_log.csv` gains a row with `preset=coherence`, `ratio=4-4-4`, `breaths=50`, `completion_pct=100`, `status=completed`.
