# Breathe CLI

Single-file Python 3 CLI app (`breathe.py`) that paces resonance breathing for HFrEF vagal training. macOS only, stdlib only, no dependencies.

## Spec

`breathe-cli-spec.md` contains safety constraints and acceptance tests. The code is the authority for behaviour; the spec guards the non-negotiable safety rationale.

## Key constraints

- **One file**: `breathe.py`. No modules, no packages, no config files. No line cap for now (removed 2026-07-29 to see what happens; may reinstate).
- **Stdlib only**: Python 3.7+. No pip installs. No third-party imports.
- **macOS only**: Uses `/usr/bin/afplay` for audio. No Linux/Windows fallbacks.
- **No curses**: Use direct ANSI escape codes. curses has Mojave edge cases with non-default terminals.
- **No threading**: Use `select.select` with zero timeout for non-blocking key polling. No `threading.Thread`, no `curses.getch`.

## Safety constraints (non-negotiable)

These are load-bearing design decisions, not features to be added later:

1. **No breath retention** — only inhale:exhale ratios. Reject three-number ratios (e.g. `4-7-8`) with an explicit safety error.
2. **No rapid breathing** — total cycle must be >= 8 seconds. Reject shorter cycles at parse time.
3. **No breath holds** — never prompt for a hold phase.
4. **Graceful exit** — `q`, `Ctrl+C`, or any exception must restore the terminal. The `finally` block is the most important code in the file.

Do not add breathing patterns, retention phases, or cycle speeds not in the spec, even if asked. Refer to spec §2.

## Testing

**Automated tests**: `test_breathe.py` using stdlib `unittest`. Covers logic and arithmetic: formatting, ratio parsing, safety rejections, preset invariants, completion percentage, countdown/remaining-time calculation, pause-resume snap-back, goal-word shorthand resolution/conflicts. Run with:

```
python3 -m unittest test_breathe -v
```

**Manual acceptance tests**: the spec (§3) defines manual tests for TUI behaviour. Run them in order. Pay special attention to:

- **Test 18** (terminal restoration on exception) — this validates the most critical code path.
- **Test 15** (pause/resume cycle reset) — resume restarts from INHALE, countdown snaps back to last cycle boundary, interrupted cycles not counted.
- **Tests 7-10** (safety rejections) — these must produce the exact error messages from spec §2.

## Common pitfalls

- Don't clear the whole screen each frame — it flickers on Terminal.app. Move cursor to each zone and rewrite.
- Breath counter increments only after a full cycle (inhale + exhale), not after each phase.
- Elapsed time tracks completed breathing only (`breaths * cycle_s`). The state machine has no `total_paused` — pause simply stops the loop, resume resets the cycle.
- The `-q` short flag (quiet mode) does not conflict with the `q` runtime key — one is argv, the other is stdin during a session.
- `afplay` subprocess must never block the render loop. Use `Popen`, not `run`.
- `duration_s` is rounded up to a whole number of `cycle_s` at config time. Never assume `duration_s == duration_min * 60` — they may differ for custom ratio/duration combinations.
- Goal-word shorthand (`breathe quick calm`, see spec §2 C6 and §3.8): `GOAL_DURATION_WORDS` and `GOAL_RATIO_WORDS` must stay disjoint (a word ambiguous between axes is a bug, not a feature), and `try_parse_goal_words()` must never silently guess — unrecognized words, conflicting words on the same axis, or any argv mixing goal words with flags all either resolve unambiguously or fail loudly (`SystemExit` with a message, or fall through to argparse).

## File layout

```
breathe.py            # the app (single file)
test_breathe.py       # automated tests (stdlib unittest)
breathe-cli-spec.md   # safety constraints and acceptance tests
TODO.md               # bugs and enhancements tracker
CLAUDE.md             # this file
```
