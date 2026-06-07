# Breathing Pattern DSL — Feature Specification

**Status:** Draft — conversational design, not yet approved for implementation
**Date:** 2026-06-07

## 1. Motivation

The app currently enforces a strict no-hold, inhale-exhale-only model designed
for HFrEF vagal training. Users have requested support for universal breathing
patterns — box breathing, 4-7-8 relaxation, and other research-backed or
established-practice protocols.

This requires expanding the app from "a cardio-safe breathing pacer" to "a
general breathing pacer that includes a cardio-safe mode." The current no-hold
constraint moves from a global invariant to a per-mode invariant.

To support arbitrary patterns cleanly, we define a small domain-specific
language (DSL) for specifying breathing sessions.

## 2. The four-phase model

Every breath cycle has four phases:

```
I  — Inhale
H1 — Post-inhale hold (retain)
E  — Exhale
H2 — Post-exhale hold (sustain)
```

A pattern specifies the duration of each phase in seconds:

```
I-H1-E-H2
```

Examples:

| Pattern     | Name               | Description                          |
|-------------|--------------------|--------------------------------------|
| `4-0-6-0`  | Cardiac-safe       | No holds, inhale:exhale = 2:3        |
| `4-7-8-0`  | 4-7-8 Relaxation   | Post-inhale hold, no post-exhale     |
| `5-5-5-5`  | Box breathing      | Equal phases                         |
| `4-0-8-0`  | Extended exhale    | 1:2 ratio, no holds                  |

A zero-valued hold phase means "no hold" — the cycle flows directly from one
breathing phase to the next.

## 3. Formal grammar

```ebnf
session     = segment { "+" segment } ;
segment     = [ count ] "(" pattern ")" | [ count ] pattern ;
pattern     = phase "-" phase "-" phase "-" phase ;
phase       = seconds { modifier } ;
seconds     = nonzero_digit { digit } | "0" ;
modifier    = airway | depth ;
airway      = "n" | "m" ;           (* nose, mouth *)
depth       = "d" | "s" ;           (* deep, shallow *)
count       = nonzero_digit { digit } ;
nonzero_digit = "1" | "2" | ... | "9" ;
digit       = "0" | nonzero_digit ;
```

Whitespace is ignored between tokens. The `+` operator chains segments
sequentially.

### 3.1 Bare vs. parenthesized patterns

A segment may omit parentheses when there is no ambiguity:

- `4-0-6-0` — valid bare pattern (single segment, count defaults to
  unlimited/duration-based)
- `10(4-0-6-0)` — 10 repetitions
- `5(4-0-6-0)+10(5-0-10-0)` — chained segments

When a count is present, parentheses are required for clarity.

### 3.2 Defaults

- If no count is given and no duration flag is set, the segment runs
  indefinitely (or until the session's global duration expires).
- If no modifiers are given, defaults are: **nose**, **normal depth**.
- Hold phases (`H1`, `H2`) accept modifiers but their meaning is contextual
  (e.g., `5n` on a hold = hold with airway open through nose vs. closed).

## 4. Phase modifiers

Modifiers are lowercase letter suffixes on a phase's duration number.

### 4.1 Airway modifiers

| Modifier | Meaning |
|----------|---------|
| `n`      | Nose    |
| `m`      | Mouth   |

Example: `10(4m-0-6n-0)` — inhale through mouth, exhale through nose.

### 4.2 Depth modifiers

| Modifier | Meaning  |
|----------|----------|
| `d`      | Deep     |
| `s`      | Shallow  |

Example: `5nd-5-5ms-5` — inhale deep through nose, hold, exhale shallow
through mouth, hold.

### 4.3 Modifier ordering and conflicts

- Multiple modifiers on one phase are concatenated: `4nd` = nose + deep.
- Order does not matter: `4nd` and `4dn` are equivalent.
- Conflicting modifiers are a parse error: `4nm` (both nose and mouth),
  `4ds` (both deep and shallow).

## 5. Chaining and repetition

Sessions can chain multiple segments with `+`:

```
5(4-0-6-0) + 10(5-0-10-0)
```

This means: 5 cycles of 4-0-6-0, then 10 cycles of 5-0-10-0.

The pacer displays a transition cue between segments (details TBD — visual
indicator, optional audio cue, brief pause).

### 5.1 Duration vs. count precedence

Session length can be specified two ways: `--duration` (minutes) and
repetition counts in the pattern (`10(4-0-6-0)`). These can conflict.

**Resolution: conflict is an error.** Consistent with the app's existing
"reject, don't guess" philosophy (e.g. `--preset` + `--ratio` is already
rejected rather than silently picking one).

| Input | Behaviour |
|-------|-----------|
| `--pattern "4-7-8-0" --duration 10` | Duration governs (bare pattern, no count). |
| `--pattern "10(4-7-8-0)"` | Count governs (10 cycles, no duration limit). |
| `--pattern "10(4-7-8-0)" --duration 5` | **Error:** "10 cycles of 4-7-8-0 = 3:10, but --duration is 5:00. Use one or the other." |
| `--pattern "5(4-0-6-0)+10(5-0-10-0)"` | Chain counts govern (5 + 10 cycles). |
| `--pattern "5(4-0-6-0)+10(5-0-10-0)" --duration 20` | **Error:** conflict between chain counts and explicit duration. |

The rule: if any segment in the pattern has an explicit count, `--duration`
must not be specified. If no segment has a count, `--duration` is required
(or the session runs indefinitely until the user quits).

### 5.2 Open questions on chaining

- Is there a maximum number of segments?
- Can segments have different modifier defaults?

## 6. Named presets

Common patterns get human-readable aliases:

| Alias        | Expands to    | Source / tradition            |
|--------------|---------------|-------------------------------|
| `cardiac`    | `4-0-6-0`    | HFrEF vagal training          |
| `box`        | `5-5-5-5`    | Military / stress resilience  |
| `relaxation` | `4-7-8-0`    | Weil 4-7-8 technique          |
| `calm`       | `4-0-8-0`    | Extended exhale, general calm |

Presets are syntactic sugar — they expand to their pattern before parsing.
A preset can be used inside chaining syntax: `5(cardiac)+10(box)`.

## 7. Validation: two layers

### 7.1 Well-formedness (syntax)

Enforced by the parser against the formal grammar. Rejects malformed input
with clear, positional error messages.

Examples of syntax errors:
- `"4-0-6"` — "expected 4 phases, got 3"
- `"4-0-6-0-2"` — "expected 4 phases, got 5"
- `"4nm-0-6-0"` — "conflicting airway modifiers: both nose and mouth"
- `"(4-0-6-0"` — "unmatched parenthesis"
- `"0(4-0-6-0)"` — "repetition count must be >= 1"

### 7.2 Safety (semantics)

Enforced after parsing on the structured representation. Safety rules are
independent of syntax — the parser does not need to know about physiology.

#### 7.2.1 Universal safety rules (all modes)

| Rule                           | Constraint                              |
|--------------------------------|-----------------------------------------|
| Minimum cycle duration         | `I + H1 + E + H2 >= 8s`               |
| Maximum hold duration          | `H1 <= 30s`, `H2 <= 30s` (TBD)        |
| Maximum single phase           | Any phase `<= 60s` (TBD)              |
| Maximum total session duration | TBD                                     |
| Inhale and exhale required     | `I >= 1s`, `E >= 1s`                   |

#### 7.2.2 Cardiac-safe mode rules (additional)

| Rule              | Constraint                                  |
|-------------------|---------------------------------------------|
| No holds          | `H1 == 0`, `H2 == 0`                       |
| No rapid breathing| Total cycle `>= 8s` (inherited from above) |

When running in cardiac-safe mode (e.g., `--mode cardiac` or the `cardiac`
preset), these additional constraints are enforced. Violations produce safety
errors, not syntax errors:

- `"4-7-8-0"` in cardiac mode — "hold phases not allowed in cardiac-safe mode"
- `"1-0-1-0"` — "total cycle 2s is below minimum 8s"

#### 7.2.3 Error message design

Safety errors should:
- Name the specific constraint violated
- Show the offending values
- Suggest a fix when possible
- Never silently clamp or adjust — always reject and explain

## 8. Interaction with existing CLI

### 8.1 Current interface

The app currently accepts:
- `--ratio I:E` (e.g., `--ratio 5:5`)
- `--preset` names
- `--duration` in minutes

### 8.2 Proposed interface

The DSL could be introduced as:
- A new `--pattern` flag: `breathe --pattern "5(4-0-6-0)+10(box)"`
- Or as a positional argument: `breathe "5(4-0-6-0)"`
- Existing `--ratio` and `--preset` flags continue to work and map to the
  DSL internally

### 8.3 Migration path

The existing `--ratio I:E` notation maps cleanly to the DSL:
- `--ratio 4:6` is equivalent to `--pattern "4-0-6-0"`
- Internally, all input paths produce the same parsed representation

## 9. Considered and deferred

These aspects of breathing were considered but deferred from the DSL:

### 9.1 Tempo / rhythm within a phase
Some techniques use stepped inhales (inhale-pause-inhale) or front-loaded
exhales. Too complex for v1 — the pacer assumes steady airflow within each
phase.

### 9.2 Vocalization on exhale
Humming (bhramari), sighing, counted exhale. Relevant for some practices but
hard to pace visually. Could be a modifier in the future (e.g., `6h` for hum).

### 9.3 Posture cues
Sitting, lying, standing. Not a breathing parameter — better handled as
preset metadata or coaching text, not DSL syntax.

### 9.4 Ratio notation
Defining patterns as ratios with a base unit — e.g., `1:0:2:0@4s` meaning
"inhale 4s, exhale 8s." Useful but adds parser complexity. Could be a future
extension.

### 9.5 Progressive sequences / ramps
Patterns that change over time — e.g., start at `4-0-4-0` and gradually
lengthen to `6-0-8-0`. Expressible as long chains but a dedicated ramp syntax
would be cleaner. Deferred.

### 9.6 Belly vs. chest breathing
Diaphragmatic vs. thoracic. A coaching cue, not something the pacer can
enforce or display differently. Better as preset description text.

## 10. Open questions

1. **Max hold durations** — what's physiologically reasonable as an upper
   bound? 30s? 60s? Needs research.
2. **Modifier semantics on holds** — does `5n` on a hold mean "hold with
   airway open through nose" or is it meaningless? Should holds reject
   airway/depth modifiers?
3. **Display changes** — how does the TUI show hold phases? A different
   color? A static bar? "HOLD" text?
4. **Audio cues** — different tones for hold vs. inhale/exhale transitions?
5. **Chain transitions** — pause between segments? Visual cue? How long?
6. ~~**Duration vs. count precedence**~~ — resolved in §5.1: conflict is an error.
7. **Preset extensibility** — can users define custom presets? Or are
   presets hardcoded?
8. **Backwards compatibility** — can the existing `--ratio` flag coexist
   indefinitely, or should it be deprecated?
9. **Mode flag** — is `--mode cardiac` needed, or is it implicit when using
   the `cardiac` preset? What if someone passes `--mode cardiac --pattern
   "4-7-8-0"` — error at parse time?
