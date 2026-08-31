# Breathe CLI

[![PyPI](https://img.shields.io/pypi/v/breathe-cli)](https://pypi.org/project/breathe-cli/)
[![Homebrew](https://img.shields.io/badge/homebrew-tap-orange)](https://github.com/marekkowalczyk/homebrew-breathe)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Show HN](https://img.shields.io/badge/Show%20HN-discussion-orange)](https://news.ycombinator.com/item?id=48340315)

A terminal app that paces resonance breathing for vagal tone training. macOS primary; Linux and Windows secondary (community-maintained). Single file, no dependencies.

```
$ breathe

  evening · 4-6 · 14:32   [●]

                   IN

          ██████████████░░░░░░░░░░░░░░░░

  space pause · s mute · q quit          VERSION · RELEASED
```

Footer is dim: key hints on the left, `VERSION · RELEASED` right-aligned (same values as `breathe -v`, without the `breathe` prefix). Narrow terminals drop the stamp before clipping hints.

## Elevator statement

For people who want a reliable daily resonance-breathing habit — including those managing HFrEF / CHF or simply training vagal tone — most breathing apps are either wellness theatre (holds, rapid patterns, gamification) or too fiddly to start. **Breathe CLI** is a single-file terminal pacer: open a shell, run `breathe`, follow the bar at ~6 breaths per minute. You get a clinically shaped, safety-constrained session with almost no setup (omakase defaults by time of day; flags when you care). Unlike phone mindfulness apps or DIY timers, it refuses unsafe patterns, restores the terminal always, and stays install-light (stdlib only, macOS primary).

## Why this exists

Resonance breathing — slow, paced breathing at around 6 breaths per minute — amplifies respiratory sinus arrhythmia (RSA) and engages cardiac vagal pathways. That matters especially in HFrEF / CHF, where sympathetic overdrive worsens disease; clinical slow-breathing work (e.g. Bernardi) motivates a daily habit tool, not a medical device.

Open a terminal, run `breathe` (omakase), follow the bar.

**[The science behind Breathe CLI](science.md)** — mechanism, preset ↔ literature map, safety physiology, and the full annotated bibliography (canonical references live there so they do not drift from this README).

## Design choices

This app is deliberately constrained. Several common breathing-app features are excluded for safety and focus:

**No breath retention.** Breath holds (kumbhaka) raise intrathoracic pressure and can trigger vasovagal syncope or arrhythmia in cardiac patients. The app rejects three-number ratios like `4-7-8` with an explicit safety error.

**No rapid breathing.** Patterns faster than 7.5 bpm (cycles shorter than 8 seconds) move toward hyperventilation territory and mobilise catecholamines — the opposite of the vagal intent. The app enforces a minimum cycle length of 8 seconds.

**No breath holds between phases.** There is no pause between inhale and exhale. The breath is continuous, matching the protocol in the clinical literature.

**Immediate exit, always.** Pressing `q` or `Ctrl+C` ends the session within one frame. The terminal is always restored — cursor, colours, input mode — even if the app crashes. The `finally` block that does this is the most important code in the file.

**No dependencies.** Single Python file, stdlib only. Nothing to install, nothing to break. Runs on the Python that ships with macOS.

**No curses.** Direct ANSI escape codes only. The curses library has edge cases with non-default terminals on macOS Mojave.

**Omakase by default.** Run `breathe` with no arguments and the app picks a time-of-day preset (chef’s choice). The countdown shows what was chosen; `q` aborts before the session starts. Flags, presets, and goal words are the substitutions when you want control. The *omakase* framing follows [DHH](https://world.hey.com/dhh)’s [Omakase Computing](https://learn.omacom.io/3/omacom/76/omakase-computing) / [Omacom](https://learn.omacom.io/) — curated defaults without forbidding overrides; not affiliated.

## Requirements

- **macOS (primary)** — `/usr/bin/afplay` + system sounds (maintainer-tested)
- **Linux / Windows (secondary)** — community-tested only. The maintainer has no Linux or Windows machines; please report audio/wake bugs with OS + player details
- Python 3.7+

## Installation

**Homebrew (recommended):**

```bash
brew tap marekkowalczyk/breathe
brew trust marekkowalczyk/breathe   # once — Homebrew requires tap trust
brew install breathe
```

Upgrade after a release: `brew upgrade breathe`.

**PyPI:**

```bash
pip install breathe-cli
```

Upgrade after a release: `pip install -U breathe-cli`. macOS is primary (`afplay`); Linux/Windows are secondary (see Requirements).

**Not the same project:** unrelated packages reuse similar names on other registries — e.g. the npm [`breathe-cli`](https://www.npmjs.com/package/breathe-cli) and the crates.io [`breathe`](https://crates.io/crates/breathe) crate. This app is Python-only; install via Homebrew or PyPI as above.

**From source** (development tip — does not replace the Homebrew binary on `PATH`):

```bash
git clone https://github.com/marekkowalczyk/breathe-cli.git
cd breathe-cli
python3 breathe.py -v
```

Plain `breathe` on `PATH` is the Cellar install. To smoke-test unreleased tip, run `python3 breathe.py` from the clone (see `CLAUDE.md` → Testing). Do not symlink the clone over `/opt/homebrew/bin/breathe` — that fights `brew upgrade`.

## Usage

### No arguments — omakase (time-of-day)

```bash
breathe
```

With no arguments, the app picks a preset based on the time of day (omakase / chef’s choice — see [Design choices](#design-choices)):

| Time of day  | Preset    | Duration | Ratio | BPM |
|--------------|-----------|----------|-------|-----|
| 06:00–11:59  | morning   | 10 min   | 5s-5s | 6   |
| 12:00–16:59  | midday    | 20 min   | 4s-6s | 6   |
| 17:00–21:59  | evening   | 15 min   | 4s-6s | 6   |
| 22:00–05:59  | night     | 20 min   | 3s-7s | 6   |

All presets target 6 breaths per minute. Names follow time of day (`morning` → `midday` → `evening` → `night`). The `morning` preset uses equal inhale/exhale (5-5). The `midday` and `evening` presets use a longer exhale (4-6) for sympathetic wind-down. The `night` preset uses a stronger exhale bias (3-7), matching the pre-sleep 6 cpm protocol studied for insomnia (Tsai et al. 2015).

### Presets

```bash
breathe --preset morning    # 10 min, 5s-5s
breathe --preset midday     # 20 min, 4s-6s (main training session)
breathe --preset evening    # 15 min, 4s-6s
breathe --preset night      # 20 min, 3s-7s (pre-sleep calming)
breathe --list-presets       # presets + goal-word vocabulary
```

### Goal words

Order-free shorthand when you don't want presets or raw minutes/ratios.
Discoverable via `breathe -h` (epilog) and `breathe --list-presets`.

```bash
breathe quick calm       # 3 min, 4-6 ratio
breathe calm quick       # same as above — order doesn't matter
breathe quick            # 3 min, default 5-5 ratio
breathe train            # default 10 min, 5-5 ratio
breathe long sleep       # 20 min, 3-7 ratio
```

An order-free shorthand for people who don't want to think in minutes and
ratios. Each word sets one independent axis:

| Axis     | Words                         | Effect                                      |
|----------|-------------------------------|---------------------------------------------|
| Duration | `quick`, `long`               | 3 min, or 20 min                            |
| Feel     | `train`, `calm`, `sleep`      | 5-5, 4-6, or 3-7 ratio                      |

Words can appear in any order and combine freely across axes. Two words
for the same axis (e.g. `breathe quick long`) is rejected as an explicit
error rather than silently picking one. The retired word `energize` fails
with a message pointing to `train` — equal 5-5 is training, not arousal.
Goal words don't combine with flags — use `--duration`/`--ratio` directly
if you need `--no-sound`, `--quiet`, etc. alongside a custom session.

### Custom sessions

```bash
breathe --duration 5                # 5 minutes, default 5-5 ratio
breathe --ratio 4-6                 # default 10 minutes, 4-6 ratio
breathe --duration 12 --ratio 4-6   # 12 minutes, 4-6 ratio
```

Duration: 1–60 minutes (rounded up to complete breath cycles). Ratio: inhale and exhale each 3–10 seconds, total cycle >= 8 seconds.

### Flags

| Flag              | Short | Description                                |
|-------------------|-------|--------------------------------------------|
| `--preset NAME`   | `-p`  | Use a named preset                         |
| `--duration MIN`  | `-d`  | Session length in minutes (1–60)           |
| `--ratio IN-EX`   | `-r`  | Breath ratio, e.g. `5-5` or `4-6`         |
| `--no-sound`      | `-n`  | Disable audio cues                         |
| `--sound-player`  |       | Linux audio player command (auto-detected) |
| `--quiet`         | `-q`  | Suppress startup warnings                  |
| `--no-log`        |       | Don't log this session                     |
| `--log`           |       | Print log file path and exit               |
| `--safety`        |       | Print safety information and exit          |
| `--list-presets`  |       | Print presets and goal words, then exit    |
| `--version`       | `-v`  | Print version and exit                     |

### Runtime keys

During a session:

| Key       | Action                                                            |
|-----------|-------------------------------------------------------------------|
| `space`   | Pause / resume. Resume restarts from the beginning of INHALE.     |
| `s`       | Toggle sound mute.                                                |
| `q`       | Quit immediately. Terminal is restored.                           |
| `Ctrl+C`  | Same as `q`.                                                      |

### The display

```
  morning · 5-5 · 09:12   [●]        <- preset, ratio, countdown, status

                   IN                <- current phase: IN (cyan) or OUT (green)

          ████████████████░░░░░░░░░░░░░░  <- breath bar (fills on inhale, drains on exhale)

  space pause · s mute · q quit          VERSION · RELEASED
                                         ^ controls (dim)     ^ tip stamp (dim, right)
```

The status indicator shows `●` during breathing, `‖` when paused, and `🔇` when muted. The footer stamp matches `VERSION` and `RELEASED` from `breathe.py` (see `-v`).

The countdown timer tracks completed breathing time only. If you pause for 30 seconds during a 1-minute session, the session takes ~90 seconds of wall-clock time to complete — the timer doesn't advance while paused.

During an interactive session the display stays awake (macOS / Windows / Linux best-effort, no dependencies). Normal dimming and screensaver return when the session ends. If stay-awake cannot be acquired, a calm stderr line appears before the TUI (hidden by `--quiet`) and the summary adds a short Note.

## Linux audio

Linux has no single standard way to play a sound, so Breathe CLI probes for a player and falls back gracefully. **Not smoke-tested by the maintainer** (community-verified only).

1. **Player** — the first of `paplay`, `pw-play`, `aplay`, `ffplay`, `cvlc` found on your `PATH`. Override with `--sound-player CMD` or the `BREATHE_SOUND_PLAYER` env var.
2. **Sounds** — the freedesktop theme (`/usr/share/sounds/freedesktop/stereo/message.oga` for inhale, `complete.oga` for exhale). Override with `BREATHE_SOUND_INHALE` / `BREATHE_SOUND_EXHALE` (any file your player accepts).
3. **Fallback** — if no player or sound file is found, Breathe CLI uses the terminal bell, exactly as before.

```bash
# Use a specific player and custom cues
BREATHE_SOUND_INHALE=~/sounds/in.wav \
BREATHE_SOUND_EXHALE=~/sounds/out.wav \
breathe --sound-player paplay
```

Most desktop distros ship `paplay` (PulseAudio) or `pw-play` (PipeWire) and the freedesktop sounds, so audio usually works with no configuration.

## Session logging

Each session appends a row to `~/.breathe_log.csv`:

```
date,time,preset,ratio,duration_target_s,duration_actual_s,breaths,completion_pct,status
2026-05-30,07:15:02,morning,5-5,600,600,60,100,completed
2026-05-30,19:30:14,evening,4-6,900,420,42,46,ended early (user)
```

Use `--no-log` to skip logging for a session. Use `--log` to see the log file path.

## Testing

Automated tests cover logic and arithmetic (formatting, ratio parsing, safety rejections, preset invariants, countdown calculation):

```bash
python3 -m unittest test_breathe -v
```

TUI behaviour (rendering, animation, terminal restoration) is covered by the manual acceptance tests in `breathe-cli-spec.md`.

## Safety

Run `breathe --safety` for the full safety screen. The short version:

**Stop immediately** if you experience lightheadedness, palpitations, or tingling in your hands or face.

This app deliberately does not support breath retention, rapid breathing, or any pattern not grounded in the slow-breathing clinical literature. These constraints are enforced in the code and cannot be overridden.

## License

Personal project by [Marek Kowalczyk](https://orcid.org/0009-0008-3874-6736).
