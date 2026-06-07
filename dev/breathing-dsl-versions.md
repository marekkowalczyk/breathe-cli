# Breathing Pattern DSL — Version Plan

**Status:** Draft — not yet approved for implementation
**Date:** 2026-06-07
**Parent:** TODO #14 · Spec: [`breathing-dsl-spec.md`](breathing-dsl-spec.md)

## Constraints

- File is at 777 lines (cap 700, hard cap was 700 — needs decision).
- State machine is `INHALE`/`EXHALE`/`PAUSED` — no concept of holds.
- Internal config is `(inhale_s, exhale_s)` — two-phase only.
- Each version must leave all existing tests passing and ship
  independently. No version depends on a later version.

## Versions

### v2.0 — Line budget and internal four-phase model

**User-visible change:** None.

**Work:**
- Decide on line cap: raise to 900? 1000? Or accept that this feature
  requires splitting into modules (breaks single-file constraint)?
- Trim dead weight from the file to buy room.
- Refactor internal config from `(inhale_s, exhale_s)` to
  `(inhale_s, hold1_s, exhale_s, hold2_s)` with holds pinned to 0.
- `--ratio 4:6` maps to `(4, 0, 6, 0)` internally.
- All existing tests pass unchanged.

**Why first:** Everything else builds on the four-phase data model.
Doing it separately isolates refactoring risk from feature risk.

**Interacts with:** TODO #15 (`BREATHE_BPM`) — the env var logic
should produce four-phase tuples, not two-phase.

---

### v2.1 — `--pattern` flag and parser

**User-visible change:** New `--pattern "4-0-6-0"` flag as an
alternative to `--ratio 4:6`. Holds must still be zero.

**Work:**
- Parse four-number `I-H1-E-H2` syntax from `--pattern` flag.
- Well-formedness errors with clear messages (wrong phase count,
  invalid numbers, etc.).
- Reject non-zero holds with existing safety error.
- Reject `--pattern` + `--ratio` (conflict, same as `--preset` +
  `--ratio`).
- Unit tests for parser: valid inputs, malformed inputs, safety
  rejections.

**Why next:** Proves the parser in isolation. No state machine
changes, no TUI changes, no new behaviour — just a new input path
that produces the same internal config.

---

### v2.2 — Hold phases in the state machine and TUI

**User-visible change:** `--pattern "4-7-8-0"` works. Hold phases
are displayed and paced.

**Work:**
- Add `HOLD_IN` and `HOLD_OUT` states to the state machine.
- State transitions: `INHALE` -> `HOLD_IN` -> `EXHALE` -> `HOLD_OUT`
  -> `INHALE`. Zero-duration holds are skipped (no state entered).
- TUI: "HOLD" label with a distinct colour. Bar stays static
  (filled after inhale, empty after exhale) during holds.
- Audio: decide on hold cue — silence, distinct tone, or tick.
- Per-mode safety: introduce cardiac-safe mode vs. universal mode.
  - Cardiac: `H1 == 0`, `H2 == 0` (existing behaviour).
  - Universal: `H1 <= 30s`, `H2 <= 30s`, total cycle >= 8s.
- Pause during hold: resume restarts from `INHALE` (same as today).
- Elapsed time / countdown accounts for hold durations in cycle
  length.
- Update logging: `ratio` column format for four-phase patterns
  (e.g. `4-7-8-0` instead of `4-6`).

**Why here:** Smallest step that delivers visible new functionality.
Everything before this is plumbing; this is the feature.

**Risk:** This is the largest single step. The state machine is the
most delicate code in the file. Consider splitting into sub-steps:
- 2.2a: state machine + TUI (cardiac mode only, holds still
  rejected)
- 2.2b: enable holds in universal mode

---

### v2.3 — Named presets for new patterns

**User-visible change:** `--preset box`, `--preset relaxation`,
etc.

**Work:**
- Add preset definitions:
  - `box` -> `5-5-5-5` (box breathing)
  - `relaxation` -> `4-7-8-0` (Weil 4-7-8)
  - Existing presets (`balanced`, `calm`, `extended`) map to
    four-phase with zero holds.
- `--list-presets` shows expanded table with four-phase patterns.
- Presets imply their mode (cardiac-safe vs. universal) — no
  separate `--mode` flag needed.
- Update time-of-day auto-select: keep current presets as defaults
  (all cardiac-safe). New presets are opt-in only.

**Why separate:** Pure sugar on top of v2.2. Low risk, high user
value. Good candidate for the first "Show HN update" (TODO #16).

**Interacts with:** TODO #8 (cycle progress bar) — new presets
with holds have longer cycles, progress bar math changes.

---

### v2.4 — Repetition counts

**User-visible change:** `10(4-0-6-0)` runs exactly 10 cycles.

**Work:**
- Extend parser: optional count prefix + parenthesized pattern.
- Count governs session length; `--duration` must not be specified
  when count is present (conflict is an error — see spec §5.1).
- Completion percentage and countdown based on count, not duration.
- Logging: record target count and actual count.

**Why here:** First grammar extension beyond the base four-number
pattern. No chaining complexity yet — single segment only.

---

### v2.5 — Chaining

**User-visible change:** `5(4-0-6-0)+10(5-5-5-5)` runs two
segments in sequence.

**Work:**
- Extend parser: `+` operator joining segments.
- Session state tracks current segment index + cycle within segment.
- Transition cue between segments (visual indicator, brief pause
  TBD).
- Progress display: show overall progress across all segments, or
  per-segment? Needs design decision.
- `--duration` conflicts with any chain that has counts (spec §5.1).
- Logging: record full pattern string, total cycles across segments.

**Why last among core features:** Most complex interaction surface —
segment sequencing, cross-segment progress tracking, transition UX.
Each prior version is a prerequisite.

---

### v2.6 — Phase modifiers (airway, depth)

**User-visible change:** `4m-0-6n-0` shows "IN (mouth)" /
"OUT (nose)" in the TUI.

**Work:**
- Extend parser: letter suffixes on phase numbers.
- Modifier conflicts are parse errors (`4nm`, `4ds`).
- TUI: show modifier annotations on the phase label.
- Modifiers are display-only — the pacer can't enforce nose vs.
  mouth. They serve as coaching cues.

**Why last:** Lowest priority. Nice to have, not load-bearing. The
DSL is fully functional without modifiers.

---

## Dependency graph

```
v2.0  Line budget + four-phase model
  |
  v
v2.1  --pattern flag + parser
  |
  v
v2.2  Hold phases in state machine + TUI    <-- first user-visible feature
  |
  v
v2.3  Named presets (box, relaxation, ...)   <-- good "Show HN" moment
  |
  v
v2.4  Repetition counts  10(...)
  |
  v
v2.5  Chaining  ... + ...
  |
  v
v2.6  Modifiers  4m, 6n, 5nd
```

## Open decisions before starting

1. **Line cap.** 777 lines today, cap is 700. This feature will add
   200-400 lines. Options: raise cap to ~1100, split into modules
   (breaks single-file constraint), or aggressive trimming + the cap
   increase.
2. **Single-file constraint.** If the parser alone is 100+ lines,
   the single-file model may not survive. Decide before v2.1.
3. **Mode flag vs. implicit mode.** Is `--mode cardiac` a flag, or
   is it implicit from the preset/pattern? Decide before v2.2.
4. **Hold TUI design.** Colour, label, bar behaviour during holds.
   Decide before v2.2.
5. **Audio cues for holds.** Silence, ticks, or a distinct tone.
   Decide before v2.2.
