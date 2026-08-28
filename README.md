# Breathe CLI

A terminal app that paces resonance breathing for vagal tone training. macOS only, single file, no dependencies.

```
$ breathe

  evening · 4-6 · 14:32   [●]

                INHALE

          ██████████████░░░░░░░░░░░░░░░░

  space pause · s mute · q quit
```

## Why this exists

Resonance breathing — slow, paced breathing at around 6 breaths per minute — is one of the few non-pharmacological interventions shown to improve cardiac vagal tone. The mechanism is straightforward: slow breathing amplifies respiratory sinus arrhythmia (RSA), the natural heart-rate variation linked to the breath cycle. Stronger RSA means stronger vagal outflow, which in turn improves baroreceptor sensitivity and shifts autonomic balance away from sympathetic dominance.

This matters most for people with heart failure with reduced ejection fraction (HFrEF), where sympathetic overdrive is both a symptom and an accelerant of disease progression. Bernardi et al. demonstrated that slow breathing at 6 bpm improves oxygen saturation and exercise tolerance in CHF patients, with effects visible after a single session and cumulative benefits over weeks of daily practice.

This app is a habit tool that makes daily practice frictionless: open terminal, run `breathe`, follow the bar. It is not a medical device.

### Key references

- Bernardi L, Porta C, Spicuzza L, et al. ["Slow breathing increases arterial baroreflex sensitivity in patients with chronic heart failure."](https://doi.org/10.1161/hc0202.103311) *Circulation*. 2002;105(2):143-145.
- Bernardi L, Sleight P, Bandinelli G, et al. ["Effect of rosary prayer and yoga mantras on autonomic cardiovascular rhythms."](https://doi.org/10.1136/bmj.323.7327.1446) *BMJ*. 2001;323:1446.
- Lehrer PM, Gevirtz R. ["Heart rate variability biofeedback: how and why does it work?"](https://doi.org/10.3389/fpsyg.2014.00756) *Front Psychol*. 2014;5:756.
- Tsai HJ, Kuo TB, Lee GS, Yang CC. ["Efficacy of paced breathing for insomnia: Enhances vagal activity and improves sleep quality."](https://doi.org/10.1111/psyp.12333) *Psychophysiology*. 2015;52(3):388-396. (pre-sleep 6 cpm, 3–7, ~20 min)
- Laborde S, et al. ["Influence of a 30-Day Slow-Paced Breathing Intervention Compared to Social Media Use on Subjective Sleep Quality and Cardiac Vagal Activity."](https://doi.org/10.3390/jcm8020193) *J Clin Med*. 2019;8(2):193.

## Design choices

This app is deliberately constrained. Several common breathing-app features are excluded for safety and focus:

**No breath retention.** Breath holds (kumbhaka) raise intrathoracic pressure and can trigger vasovagal syncope or arrhythmia in cardiac patients. The app rejects three-number ratios like `4-7-8` with an explicit safety error.

**No rapid breathing.** Patterns faster than 7.5 bpm (cycles shorter than 8 seconds) move toward hyperventilation territory and mobilise catecholamines — the opposite of the vagal intent. The app enforces a minimum cycle length of 8 seconds.

**No breath holds between phases.** There is no pause between inhale and exhale. The breath is continuous, matching the protocol in the clinical literature.

**Immediate exit, always.** Pressing `q` or `Ctrl+C` ends the session within one frame. The terminal is always restored — cursor, colours, input mode — even if the app crashes. The `finally` block that does this is the most important code in the file.

**No dependencies.** Single Python file, stdlib only. Nothing to install, nothing to break. Runs on the Python that ships with macOS.

**No curses.** Direct ANSI escape codes only. The curses library has edge cases with non-default terminals on macOS Mojave.

## Requirements

- macOS (uses `/usr/bin/afplay` for audio cues)
- Python 3.7+

## Installation

```bash
# Clone or download breathe.py, then:
chmod +x breathe.py

# Option A: run directly
./breathe.py

# Option B: symlink into your PATH
ln -s "$(pwd)/breathe.py" /usr/local/bin/breathe
breathe
```

## Usage

### No arguments — time-of-day auto-select

```bash
breathe
```

With no arguments, the app picks a preset based on the time of day:

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
breathe --preset midday     # 20 min, 4s-6s (full Bernardi protocol dose)
breathe --preset evening    # 15 min, 4s-6s
breathe --preset night      # 20 min, 3s-7s (pre-sleep calming)
breathe --list-presets       # show the table
```

### Goal words

```bash
breathe quick calm       # 3 min, 4-6 ratio
breathe calm quick       # same as above — order doesn't matter
breathe quick            # 3 min, default 5-5 ratio
breathe energize         # default 10 min, 5-5 ratio
```

An order-free shorthand for people who don't want to think in minutes and
ratios. Each word sets one independent axis:

| Axis     | Words                | Effect                          |
|----------|-----------------------|----------------------------------|
| Duration | `quick`, `long`       | 3 min, or 20 min                |
| Feel     | `calm`, `energize`    | 4-6 ratio, or 5-5 ratio          |

Words can appear in any order and combine freely across axes. Two words
for the same axis (e.g. `breathe quick long`) is rejected as an explicit
error rather than silently picking one. Goal words don't combine with
flags — use `--duration`/`--ratio` directly if you need `--no-sound`,
`--quiet`, etc. alongside a custom session.

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
| `--quiet`         | `-q`  | Suppress startup warnings                  |
| `--no-log`        |       | Don't log this session                     |
| `--log`           |       | Print log file path and exit               |
| `--safety`        |       | Print safety information and exit          |
| `--list-presets`  |       | Print preset table and exit                |
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

                INHALE                <- current phase (cyan) or EXHALE (green)

          ████████████████░░░░░░░░░░░░░░  <- breath bar (fills on inhale, drains on exhale)

  space pause · s mute · q quit       <- available controls
```

The status indicator shows `●` during breathing, `‖` when paused, and `🔇` when muted.

The countdown timer tracks completed breathing time only. If you pause for 30 seconds during a 1-minute session, the session takes ~90 seconds of wall-clock time to complete — the timer doesn't advance while paused.

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
