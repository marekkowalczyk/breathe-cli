# Breathe CLI — Issues & Ideas

## Open

### 8. Session progress bar (cycle count)
Add a second horizontal bar below the breath bar that tracks
cycle-count progress (completed cycles / total expected cycles).
Same width as the breath bar, identical visual style, but fills
gradually based on breath count rather than phase. Separate the
two bars with ~5 px (blank lines or spacing) so they're close
but visually distinct. Requires adjusting layout row calculations.
Note: this is related to but distinct from enhancement #4 (which
tracks elapsed time); this one tracks completed breath cycles.

### 14. Breathing modes beyond vagal tone
Broaden the app to support multiple breathing purposes (e.g. focus,
relaxation, box breathing) as distinct modes. Current safety
guardrails (no retention, no rapid breathing, ≥8s cycle) apply to
the vagal/HFrEF mode only. Other modes would define their own
constraints — e.g. box breathing would allow holds but enforce its
own limits. This is a significant architectural change: mode
selection, per-mode presets, per-mode guardrails, and updated
safety messaging. The single-file constraint may become the
binding limit.

**Status: scoping.** A domain-specific language (DSL) for specifying
arbitrary breathing patterns is being designed. Four-phase model
(`I-H1-E-H2`), phase modifiers (airway, depth), chaining, named
presets, and two-layer validation (syntax + safety).
- Spec: [`breathing-dsl-spec.md`](breathing-dsl-spec.md)
- Version plan: [`breathing-dsl-versions.md`](breathing-dsl-versions.md)

### 15. Personal resonance frequency (`BREATHE_BPM`)
Allow the user to declare their individual resonance frequency so
that presets auto-adjust. Preferred mechanism: env var
`BREATHE_BPM=5.2` (user sets it in their shell profile; no config
file needed, consistent with the no-config-files constraint).

**Ratio computation from BPM:**
- Target cycle = `round(60 / bpm)` seconds (integer phases only).
- `balanced`: split evenly; if odd cycle, shorter inhale
  (e.g. 11s → 5-6).
- `calm`/`extended`: exhale-weighted split, maintaining
  exhale <= 2x inhale (e.g. 12s → 4-8, 11s → 4-7).
- Validate that the computed ratio still passes all safety checks
  (phase bounds 3–10s, cycle >= 8s, exhale <= 2x inhale).
  Reject with a clear error if the requested BPM produces an
  invalid ratio.

**Interaction with other flags:**
- `--preset` + `BREATHE_BPM`: preset picks the style (balanced
  vs exhale-weighted) and duration; BPM overrides the ratio.
- `--ratio` + `BREATHE_BPM`: explicit `--ratio` wins (user
  override). Print a note: "Using explicit ratio; ignoring
  BREATHE_BPM."
- `--preset` + `--ratio`: already rejected; no change.

**Line budget:** ~30–40 lines for the env var read, validation,
ratio computation, and preset adjustment. Current file is ~780
lines. Python v1 is feature-frozen (see #14 version plan); this
feature would land in Go v2 if pursued.

**Caveats:**
- Integer-only phase durations mean not every BPM maps cleanly.
  4.8 bpm → 12.5s cycle → rounds to 12s (5.0 bpm). Document
  this: "actual BPM may differ slightly from requested."
- The resonance frequency finding protocol (README) should
  recommend testing at rates the app can actually represent
  (whole-second ratios), not arbitrary decimal BPMs.

### 16. HN Show thread update: universal breathing patterns
Post an update to the [Show HN thread](https://news.ycombinator.com/item?id=48340315)
announcing universal breathing pattern support and the DSL.
**Blocked by:** #14 (DSL implementation) — need working code users
can actually try, not just a spec. Post when `--pattern` ships in
a release.

## Done

### ~~13. Countdown hits 00:00 one exhale-phase early~~ FIXED (v1.7)
`duration_s` was not always a multiple of `cycle_s`. Fix: round
`duration_s` up to a whole number of cycles at config time.

### ~~6, 10, 12. Bug fixes and audio refactor~~ DONE (v1.6)
Sound cue sync, end-of-session rendering, inhale bar rounding,
AudioToolbox removal. 711 → 646 lines.

### ~~3. README.md~~ DONE (v1.6)
### ~~4. Session progress bar (time-based)~~ DONE (v1.6)
### ~~5. Shorter phase labels (IN/OUT)~~ DONE (v1.6)
### ~~11. State machine refactor and pause-resume reset~~ DONE (v1.5)
### ~~7. Replace count-up timer with countdown~~ DONE (v1.4)
### ~~9. Session logging to disk~~ DONE (v1.3)
### ~~2. Time-of-day-aware default preset~~ DONE (v1.2)
### ~~1. Audio cues drift out of sync with breath cycle~~ FIXED (v1.1)
