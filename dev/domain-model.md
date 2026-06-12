# Breathe — Domain Model

**Status:** Draft — produced before Go v2 implementation  
**Date:** 2026-06-12  
**Method:** Domain-Driven Design (DDD) fact map  
**Scope:** Python v1 behaviour + DSL expansion planned for v2

This document captures *what is true about the breathing domain* before any code decisions. It is the language-agnostic specification from which Go types, function signatures, and test cases are derived. Code is the authority for behaviour; this document is the authority for domain vocabulary and invariants.

---

## 1. Ubiquitous Language

One term per concept. Use these terms in code, comments, docs, tests, and conversation — never let alternatives coexist.

| Term | Definition |
|---|---|
| **Phase** | A single named stage of a breath cycle: Inhale, Hold1, Exhale, Hold2 |
| **PhaseDuration** | The duration of one phase, in whole seconds. May be zero (phase absent). |
| **Pattern** | A complete specification of one breath cycle: four PhaseDurations (I, H1, E, H2) |
| **Cycle** | One execution of a Pattern: I → H1 → E → H2. Zero-duration phases are skipped. |
| **Segment** | A Pattern paired with an optional RepetitionCount. The unit of a Session. |
| **RepetitionCount** | The number of times a Segment's Pattern is cycled. Absent = duration-governed. |
| **Session** | An ordered sequence of one or more Segments. The complete breathing prescription. |
| **Preset** | A named alias that expands to a Pattern before parsing. |
| **SafetyMode** | Cardiac-safe or Universal. Determines which SafetyConstraints apply. |
| **SafetyConstraints** | The set of invariants that must hold for a given SafetyMode. |
| **Modifier** | An optional annotation on a PhaseDuration: airway (nose/mouth) or depth (deep/shallow). |
| **SessionState** | The mutable runtime record of an executing Session. |
| **SnapbackPoint** | The start of the most recently begun Cycle; the point to which resume returns. |

**Rejected synonyms:** "breath" for Cycle, "ratio" for Pattern, "block" for Segment, "mode" for SafetyMode (too generic).

---

## 2. Value Objects

Immutable. Defined entirely by their value — two instances with the same values are interchangeable.

```
Value Object: PhaseDuration
  fields: seconds int (>= 0), airway AirwayModifier?, depth DepthModifier?
  note: seconds == 0 means the phase is absent from the Cycle

Value Object: Pattern
  fields: inhale PhaseDuration, hold1 PhaseDuration, exhale PhaseDuration, hold2 PhaseDuration
  note: hold1 and hold2 may be zero; inhale and exhale must be >= 1s

Value Object: Segment
  fields: pattern Pattern, count RepetitionCount?
  note: count absent means the session's --duration flag governs length

Value Object: Session
  fields: segments []Segment (ordered, at least 1)

Value Object: SafetyConstraints
  fields: mode SafetyMode, rules []SafetyRule
  note: determined at config time; not mutable during execution

Value Object: Preset
  fields: name string, pattern Pattern, mode SafetyMode
```

**Go mapping:**

```go
type Seconds     int
type PhaseKind   int  // Inhale, Hold1, Exhale, Hold2
type AirwayKind  int  // Nose, Mouth, Unspecified
type DepthKind   int  // Normal, Deep, Shallow

type PhaseDuration struct {
    Seconds Seconds
    Airway  AirwayKind
    Depth   DepthKind
}

type Pattern struct {
    Inhale, Hold1, Exhale, Hold2 PhaseDuration
}

type Segment struct {
    Pattern Pattern
    Count   int   // 0 = duration-governed
}

type Session []Segment
```

`Seconds` is a named type — the compiler prevents passing a raw `int` where `Seconds` is expected.

---

## 3. Entities

Objects with identity that persists over time. Two entities with the same identity are the same object even if their attributes differ.

```
Entity: SessionState
  identity: session start time (monotonic clock)
  attributes:
    session         Session          — the prescription being executed
    currentSegment  int              — index into session.segments
    currentPhase    PhaseKind        — Inhale | Hold1 | Exhale | Hold2
    cyclesCompleted int              — within current segment
    paused          bool
    snapbackPoint   time.Time        — start of the current (or last completed) cycle
  note: there is at most one SessionState alive at a time
```

There are no other entities. Presets and Patterns are Value Objects — two patterns with identical phase durations are identical. A running session has identity; a description of what to breathe does not.

---

## 4. Domain Events

Things that happen during a session. Named past-tense where possible. In Go: an interface type with one concrete struct per event.

```
SessionStarted        { session Session, startTime time.Time }
PhaseTransitioned     { from PhaseKind, to PhaseKind }
CycleCompleted        { segmentIndex int, cyclesInSegment int }
SegmentCompleted      { segmentIndex int }
SessionCompleted      { }
SessionPaused         { snapbackPoint time.Time }
SessionResumed        { snapbackPoint time.Time }
SessionAborted        { reason string }          — user quit, Ctrl+C, or unhandled error
SafetyViolationRejected { rule string, values map[string]int }   — at config time, before session
ParseError            { message string, position int }           — at config time
```

**Note on SessionAborted:** this event is the signal for terminal restoration. The `defer` block in the Go binary fires unconditionally on this event, regardless of cause. This is the most important code path in the program.

---

## 5. Invariants and Causalities

### 5.1 Invariants — always true

**Well-formedness (parser enforces):**
```
pattern has exactly 4 phases
repetition count >= 1 (if specified)
no conflicting modifiers: NOT (airway == nose AND airway == mouth)
no conflicting modifiers: NOT (depth == deep AND depth == shallow)
```

**Universal safety (SafetyConstraints, all modes):**
```
inhale.seconds >= 1
exhale.seconds >= 1
cycleDuration(pattern) >= 8       — where cycleDuration = I + H1 + E + H2
hold1.seconds <= 30               — TBD: upper bound under research
hold2.seconds <= 30               — TBD: upper bound under research
```

**Cardiac-safe mode (additional):**
```
hold1.seconds == 0
hold2.seconds == 0
```

**Session composition:**
```
if any segment has explicit count → --duration must be absent
if no segment has explicit count → --duration must be present OR session runs indefinitely
```

### 5.2 Causalities — X causes Y

These become the pattern-match branches and validation functions:

```
hold1 > 0 OR hold2 > 0,  mode == cardiac-safe
  → SafetyViolationRejected("hold phases not permitted in cardiac-safe mode", {hold1, hold2})

cycleDuration(pattern) < 8
  → SafetyViolationRejected("cycle below 8s minimum", {cycle: computed})

inhale.seconds < 1
  → SafetyViolationRejected("inhale phase must be >= 1s", {inhale: 0})

exhale.seconds < 1
  → SafetyViolationRejected("exhale phase must be >= 1s", {exhale: 0})

any segment has count AND --duration specified
  → ParseError("use count OR --duration, not both")

currentPhase duration elapsed
  → PhaseTransitioned(current, nextPhase(current, pattern))

all phases in cycle complete
  → CycleCompleted; if cyclesCompleted == segment.count → SegmentCompleted

all segments complete
  → SessionCompleted

'q' keypress OR SIGINT
  → SessionAborted("user quit")

unhandled exception
  → SessionAborted("error: " + message)
```

### 5.3 Rules — how values are computed

These become function signatures:

```
cycleDuration(pattern Pattern) Seconds
  = pattern.inhale.seconds + pattern.hold1.seconds
    + pattern.exhale.seconds + pattern.hold2.seconds

sessionCycles(session Session) int
  = sum(segment.count for each segment)          — only valid if all segments have counts

completionPercent(state SessionState) float
  = (totalCyclesCompleted(state) / targetCycles(state)) * 100

nextPhase(current PhaseKind, pattern Pattern) PhaseKind
  = next non-zero phase in order [Inhale, Hold1, Exhale, Hold2], wrapping to Inhale
  — zero-duration phases are skipped entirely

snapbackPoint(state SessionState) time.Time
  = start time of the most recently begun cycle

countdownRemaining(state SessionState, now time.Time) Seconds
  = targetDuration(state) - elapsed(state, now)
  — elapsed = cyclesCompleted * cycleDuration (does not include paused time or current partial cycle)
```

---

## 6. Separation of concerns

Three concerns that must not be conflated in the implementation:

### 6.1 Pattern (pure data)
A `Pattern` is a description. It has no behaviour, no state, no side effects. Functions that operate on patterns are pure functions. The parser produces patterns; the validator tests them; the state machine consumes them.

### 6.2 SafetyConstraints (pure validation)
Validation is a pure function: `validate(pattern Pattern, mode SafetyMode) []ValidationError`. It takes a pattern and returns errors. It has no side effects and no state. It is called at config time, before any session state is created.

The two validation layers are always separate:
- **Well-formedness** (parser): structural — does this string parse to a valid AST?
- **Safety** (validator): semantic — does this parsed pattern satisfy physiological constraints?

### 6.3 SessionState (mutable, time-dependent)
Only `SessionState` is mutable. The render loop, key input, and audio scheduling operate on it. It is the only entity. It must never appear in pure parsing or validation code.

---

## 7. Adoption in v2

### Why now

Go v2 is a blank slate. This is the best moment to build from the domain model outward rather than from the implementation inward. The Python v1 code was written without an explicit domain model; the resulting tight coupling between the state machine, render loop, and config logic is the main thing to avoid repeating.

### The sequence for Go v2

```
This document (domain model)
        ↓
Go type definitions (Pattern, PhaseDuration, SafetyConstraints, ...)
        ↓
Pure functions (parser, validator, cycleDuration, nextPhase, ...)
        ↓
Tests for pure functions (no TUI, no audio)
        ↓
SessionState + event loop
        ↓
TUI + audio (last, because they are the hardest to test)
```

Building pure functions first means the core domain logic is fully tested before any TUI work begins. The render loop becomes a thin consumer of `SessionState` events.

### What the domain model buys

- **The mode question is resolved:** `SafetyMode` is not a runtime flag — it is a parameter to `validate()` at config time. The `cardiac` preset carries its `SafetyMode`; `--pattern` with explicit holds requires `SafetyMode = Universal`. No `--mode` flag needed.
- **The state machine is bounded:** `SessionState` is the only mutable thing. Everything else is pure. Tests for pure functions need no TUI setup.
- **Invariants are checkpoints:** every invariant in §5.1 becomes a test assertion. The property-based testing approach from `dev/cross-language-spec-research.md` applies directly.
- **`defer` is the only place terminal restoration lives:** `SessionAborted` is the event; the `defer` fires on it unconditionally. This is preserved from Python v1.

### What to resist

- Don't encode `SafetyConstraints` into the parser. The parser's job is well-formedness only.
- Don't put rendering logic in `SessionState`. `SessionState` holds facts; the TUI reads them.
- Don't add `total_paused_time` to `SessionState`. Pause stops the loop; resume resets the cycle (Python v1 behaviour). Elapsed time = `cyclesCompleted * cycleDuration`, nothing else.

---

## 8. Language note: Go vs. Haskell vs. polyglot

### Go is the right choice for breathe v2

The meds project's language-suitability analysis applies here with one key difference: **breathe's domain is mostly operational.** The pure core (parse + validate) is small — perhaps 300 lines of Go. The rest is a real-time event loop, terminal I/O, and audio subprocess management. This is the layer where Go's strengths (explicit error handling, `defer`, fast subprocess management, single static binary) are decisive.

Haskell's advantages (sum types, newtype wrappers, pure-by-default) apply to the domain layer. But the domain layer here is narrow. Haskell would add `IO` monad complexity to the event loop, require `brick` or `vty` for the TUI (breaking the dependency-free goal), and make the `afplay` subprocess management harder to reason about. The learning cost is real; the payoff is proportionally smaller than it would be for meds.

**Where Haskell would help:** the parser and validator. `parsePattern :: Text -> Either ParseError Pattern` and `validate :: Pattern -> SafetyMode -> [ValidationError]` are exactly the kind of pure, total functions Haskell is best at. But these are small enough that well-typed Go suffices.

**Verdict:** Go. The operational shell dominates breathe's complexity in a way it does not dominate meds. Use the domain model to keep the pure core clean; Go's discipline handles the rest.

### Polyglot multikernel: not worth it for breathe

The meds polyglot architecture works because meds has a clean pipeline: `CSV → pure computation → structured output → notification`. The computational core is substantial and genuinely separable.

Breathe's "pipeline" is a real-time event loop. There is no clean decomposition point for a subprocess boundary: the parser runs once at startup, the validator runs once, then the program is a TUI loop forever. Splitting parser/validator into a Haskell subprocess would add JSON IPC overhead and a second toolchain for perhaps 200 lines of pure logic. The process boundary would add complexity without adding capability.

**When this calculus changes:** if breathe ever gains server-mode operation (a REST API for programmatic session control, or a shared session protocol for a mobile companion app), a polyglot architecture becomes appropriate. At that point the domain model defined here becomes the JSON schema at the process boundary — exactly as in the meds architecture. That version of breathe would benefit from a Haskell core engine. The current TUI pacer does not.
