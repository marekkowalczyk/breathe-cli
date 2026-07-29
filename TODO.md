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

## Done

### ~~15. Goal-word shorthand (`breathe quick calm`)~~ DONE (v1.8)
Order-free keyword args mapping to duration/ratio without requiring
knowledge of presets or ratio syntax. `GOAL_DURATION_WORDS`
(`quick`/`long`) and `GOAL_RATIO_WORDS` (`calm`/`energize`) are
independent axes resolved by `try_parse_goal_words()`; anything it
doesn't fully recognize falls through to normal argparse unchanged.
Conflicting or repeated words on the same axis are rejected explicitly
(never silently guessed). See spec §2 C6 and §3.8.

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
