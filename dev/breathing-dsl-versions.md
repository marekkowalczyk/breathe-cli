# Breathing Pattern DSL — Version Plan

**Status:** Draft — not yet approved for implementation
**Date:** 2026-06-07
**Parent:** TODO #14 · Spec: [`breathing-dsl-spec.md`](breathing-dsl-spec.md)

## Strategy: Python v1 freeze, Go v2

**Python (`breathe.py`) = v1.x** — feature-frozen, bugfixes only. The
cardiac-safe resonance breathing pacer. Stays on PyPI. The code and
tests serve as the living spec / reference implementation for the Go
rewrite.

**Go = v2.x** — the universal breathing pacer with the DSL. Same repo
(`marekkowalczyk/breathe-cli`). Ships as a single compiled binary.

**Why Go:**
- Single binary, zero runtime dependencies. Solves the install-friction
  vs. single-file tension permanently — multiple source files compile
  to one binary.
- Cross-compilation: macOS, Windows, Linux from one `go build`.
- Distribution: `brew install`, `go install`, or download from GitHub
  Releases.
- No Python version issues, no pip, no venv.
- Fast startup, no interpreter overhead.
- Split into as many files as readability demands.

**Why same repo:**
- Keeps the stars, forks, issue history, and community.
- Users discover v2 naturally.
- Python v1 moves to a `v1-python/` archive directory.

**What the Python code provides for the Go rewrite:**
- Exact behaviour spec: state machine, render loop, timing logic.
- Safety rules and their rationale.
- Test cases: every unit test and manual acceptance test translates
  directly.
- Edge cases already discovered and handled (pause/resume snap-back,
  countdown rounding, audio subprocess management).

## Repo layout (after transition)

```
breathe-cli/
  cmd/breathe/          # Go main package
  internal/
    parser/             # DSL parser + well-formedness validation
    safety/             # safety rules (per-mode)
    config/             # session config, presets
    tui/                # terminal rendering, ANSI, state machine
    audio/              # platform audio (macOS/Windows/Linux)
  go.mod
  go.sum
  README.md
  LICENSE
  v1-python/            # archived Python v1
    breathe.py          # reference implementation (frozen)
    test_breathe.py     # reference tests
  dev/
    breathe-cli-spec.md
    breathing-dsl-spec.md
    breathing-dsl-versions.md  # this file
    TODO.md
    ...
```

## Versions

### v1.x — Python (current, feature-frozen)

**Status:** Stable. Bugfixes only. No new features.

The existing app: cardiac-safe resonance breathing pacer, single-file
Python, stdlib only. Remains on PyPI as `breathe-cli`.

---

### v2.0 — Go scaffold + parity with Python v1

**User-visible change:** Same app, now a Go binary. All v1 features
work identically.

**Work:**
- Go module, project structure, build tooling.
- Port the state machine (`INHALE`/`EXHALE`/`PAUSED`).
- Port TUI rendering (ANSI escape codes, no-flicker rewrite).
- Port audio (macOS `afplay`, Windows `winsound` equivalent).
- Port CLI flags: `--preset`, `--ratio`, `--duration`, `--no-sound`,
  `--quiet`, `--no-log`, `--log`, `--safety`, `--list-presets`,
  `--version`.
- Port session logging (CSV).
- Port all safety checks (min cycle, max phase, exhale ratio).
- Port pause/resume with snap-back.
- Translate `test_breathe.py` to Go tests.
- Run Python manual acceptance tests (spec §3) against the Go binary.
- Graceful exit: `q`, `Ctrl+C`, terminal restoration in all cases.
  The `defer` block is the most important code in the binary.

**Why first:** Feature parity before new features. If the Go version
can't pass all 25 manual acceptance tests, nothing else matters.

**Release:** `v2.0.0` on GitHub Releases. Homebrew tap. Python v1
archived to `v1-python/`.

---

### v2.1 — Internal four-phase model

**User-visible change:** None.

**Work:**
- Internal config from `(inhale, exhale)` to
  `(inhale, hold1, exhale, hold2)` with holds pinned to 0.
- `--ratio 4:6` maps to `(4, 0, 6, 0)` internally.
- All tests pass unchanged.

**Why here:** Foundation for everything that follows. Trivial in Go
since we're already building the data structures fresh.

Note: in practice this may be folded into v2.0 since we're building
from scratch anyway. Kept as a separate logical step for clarity.

---

### v2.2 — `--pattern` flag and parser

**User-visible change:** New `--pattern "4-0-6-0"` flag. Holds must
still be zero.

**Work:**
- Parse four-number `I-H1-E-H2` syntax.
- Well-formedness errors with clear, positional messages.
- Reject non-zero holds with safety error.
- Reject `--pattern` + `--ratio` (conflict).
- Parser unit tests: valid, malformed, safety rejections.

**Why separate:** Proves the parser in isolation. No state machine
changes yet.

---

### v2.3 — Hold phases in the state machine and TUI

**User-visible change:** `--pattern "4-7-8-0"` works. Hold phases
are displayed and paced.

**Work:**
- Add `HOLD_IN` and `HOLD_OUT` states.
- State transitions: `INHALE` -> `HOLD_IN` -> `EXHALE` -> `HOLD_OUT`
  -> `INHALE`. Zero-duration holds are skipped.
- TUI: "HOLD" label, distinct colour, bar stays static during holds.
- Audio: decide on hold cue (silence, distinct tone, or tick).
- Per-mode safety: cardiac-safe (no holds) vs. universal (holds
  allowed, `H1 <= 30s`, `H2 <= 30s`, cycle >= 8s).
- Pause during hold: resume restarts from `INHALE`.
- Countdown accounts for hold durations.
- Logging: four-phase format in ratio column.

**Risk:** Largest single step. Consider sub-steps:
- 2.3a: state machine + TUI (cardiac mode only, holds still rejected)
- 2.3b: enable holds in universal mode

---

### v2.4 — Named presets for new patterns

**User-visible change:** `--preset box`, `--preset relaxation`, etc.

**Work:**
- Preset definitions: `box` -> `5-5-5-5`, `relaxation` -> `4-7-8-0`.
- Existing presets map to four-phase with zero holds.
- `--list-presets` shows expanded table.
- Presets imply their mode (cardiac-safe vs. universal).
- Time-of-day auto-select: keeps current cardiac-safe defaults.

**Good candidate for the Show HN update (TODO #16).**

---

### v2.5 — Repetition counts

**User-visible change:** `10(4-0-6-0)` runs exactly 10 cycles.

**Work:**
- Parser: optional count prefix + parenthesized pattern.
- Count governs session length; `--duration` must not be specified
  when count is present (conflict is an error — spec §5.1).
- Completion percentage and countdown based on count.
- Logging: target and actual count.

---

### v2.6 — Chaining

**User-visible change:** `5(4-0-6-0)+10(5-5-5-5)` runs two segments
in sequence.

**Work:**
- Parser: `+` operator joining segments.
- Session state tracks current segment + cycle within segment.
- Transition cue between segments (visual indicator, brief pause).
- Progress: overall vs. per-segment (design decision needed).
- `--duration` conflicts with chains that have counts (spec §5.1).
- Logging: full pattern string, total cycles across segments.

---

### v2.7 — Phase modifiers (airway, depth)

**User-visible change:** `4m-0-6n-0` shows "IN (mouth)" /
"OUT (nose)" in the TUI.

**Work:**
- Parser: letter suffixes on phase numbers.
- Conflict detection (`4nm`, `4ds`).
- TUI: modifier annotations on phase label.
- Display-only — coaching cues, not enforced.

**Lowest priority.** DSL is fully functional without modifiers.

---

## Dependency graph

```
v1.x  Python (frozen, bugfixes only)

v2.0  Go scaffold + feature parity with Python v1
  |
  v
v2.1  Internal four-phase model (may fold into v2.0)
  |
  v
v2.2  --pattern flag + parser
  |
  v
v2.3  Hold phases in state machine + TUI    <-- first new feature
  |
  v
v2.4  Named presets (box, relaxation, ...)   <-- Show HN moment
  |
  v
v2.5  Repetition counts  10(...)
  |
  v
v2.6  Chaining  ... + ...
  |
  v
v2.7  Modifiers  4m, 6n, 5nd
```

## Open decisions before starting

1. **Go experience.** Does the author have Go fluency, or is this
   also a learning project? Affects timeline estimates.
2. **Mode flag vs. implicit mode.** Is `--mode cardiac` a flag, or
   is it implicit from the preset/pattern? Decide before v2.3.
3. **Hold TUI design.** Colour, label, bar behaviour during holds.
   Decide before v2.3.
4. **Audio cues for holds.** Silence, ticks, or a distinct tone.
   Decide before v2.3.
5. **PyPI deprecation.** When v2.0 ships, does `breathe-cli` on
   PyPI get a deprecation notice pointing to the Go binary? Or
   does it stay as-is for Python users who prefer it?
6. **Homebrew formula.** New formula for the Go binary, or update
   the existing tap?
7. **Linux support.** Go makes Linux trivial. Add it in v2.0 or
   defer? Audio is the main question (PulseAudio? ALSA? No sound
   on Linux by default?).
