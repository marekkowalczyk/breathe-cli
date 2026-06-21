# Breathe CLI

[![PyPI version](https://img.shields.io/pypi/v/breathe-cli)](https://pypi.org/project/breathe-cli/)
[![Python 3.7+](https://img.shields.io/pypi/pyversions/breathe-cli)](https://pypi.org/project/breathe-cli/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Homebrew](https://img.shields.io/badge/homebrew-tap-orange)](https://github.com/marekkowalczyk/homebrew-breathe)
[![Hacker News](https://img.shields.io/badge/HN-discussion-orange)](https://news.ycombinator.com/item?id=48340315)

A terminal app that paces resonance breathing for vagal tone training. macOS and Windows 11, single file, no dependencies.

```
$ breathe

  calm · 4-6 · 14:32   [●]

                INHALE

          ██████████████░░░░░░░░░░░░░░░░

  space pause · s mute · q quit
```

## Why this exists

Resonance breathing — slow, paced breathing at around 6 breaths per minute — is one of the few non-pharmacological interventions shown to improve cardiac vagal tone. The mechanism is straightforward: slow breathing amplifies respiratory sinus arrhythmia (RSA), the natural heart-rate variation linked to the breath cycle. Stronger RSA means stronger vagal outflow, which in turn improves baroreceptor sensitivity and shifts autonomic balance away from sympathetic dominance.

This matters most for people with heart failure with reduced ejection fraction (HFrEF), where sympathetic overdrive is both a symptom and an accelerant of disease progression. Bernardi et al. (1998) demonstrated that slow breathing at 6 bpm improves oxygen saturation and exercise tolerance in CHF patients, with effects visible after a single session. A follow-up study (Bernardi et al. 2002) showed that slow breathing also increases arterial baroreflex sensitivity in CHF — a marker strongly associated with prognosis.

This app is a habit tool that makes daily practice frictionless: open terminal, run `breathe`, follow the bar. It is not a medical device.

### The science in brief

**Why 6 breaths per minute?** The cardiovascular system has a resonance frequency — typically between 4.5 and 6.5 bpm in adults — at which heart rate oscillations are maximally amplified (Vaschillo et al. 2006). Breathing at or near this frequency produces the largest RSA swings, which drive the strongest vagal training stimulus. Individual resonance frequency varies and can only be identified precisely with HRV biofeedback hardware. Without it, 6 bpm is the best population-level default: it sits at the centre of the typical range and matches the rate used in the CHF clinical trials (Bernardi et al. 1998, 2002).

**Why a longer exhale in the `calm` and `extended` presets?** Cardiac vagal efferent activity is gated to the respiratory cycle — vagal outflow is stronger during expiration than inspiration. A longer exhale (4s in, 6s out) extends the phase of peak vagal drive within each breath, biasing the autonomic balance further toward parasympathetic tone (Russo et al. 2017, Lehrer & Gevirtz 2014). The total cycle is still 10 seconds (6 bpm). The `balanced` preset uses equal timing (5-5) as a neutral baseline; the `calm` and `extended` presets use the exhale-weighted ratio for parasympathetic emphasis.

**Why these safety constraints?** See the [Design choices](#design-choices) section below. Each constraint maps to a specific physiological risk that is elevated in cardiac patients.

### Finding your resonance frequency

The presets use 6 bpm because it works well for most people and matches the clinical trial protocols. But individual resonance frequency varies — typically between 4.5 and 6.5 bpm — and breathing at *your* resonance frequency produces a stronger vagal training stimulus than breathing at the population average (Vaschillo et al. 2006).

If you have HRV biofeedback hardware, you can find your personal optimum. If you don't, the 6 bpm default is a good choice — consistent daily practice matters more than nailing the exact frequency.

#### What you need

- A chest-strap heart rate monitor (e.g. Polar H10, Garmin HRM-Pro). Wrist-based optical sensors are not accurate enough for beat-to-beat HRV.
- Software that displays real-time R-R intervals or HRV metrics: [Kubios](https://www.kubios.com), [Elite HRV](https://elitehrv.com), [HRV4Training](https://www.hrv4training.com), or a dedicated biofeedback system.

#### Protocol

Run this test sitting upright in a quiet room, at the same time of day you normally practice. The whole procedure takes about 30 minutes.

1. **Baseline** (2 min). Breathe normally. Let your heart rate settle. Start your HRV recording.
2. **Test rate 1: 6.0 bpm** (3 min). Run `breathe --ratio 5-5 -d 3 --no-log`. Follow the pacer. At the end, note the average RMSSD (or, if your software shows a live heart rate trace, note how wide the oscillations are — peak-to-trough in bpm).
3. **Rest** (1–2 min). Breathe normally.
4. **Test rate 2: 5.5 bpm** (3 min). Run `breathe --ratio 5-6 -d 3 --no-log`. Note the same metric.
5. **Rest** (1–2 min).
6. **Test rate 3: 5.0 bpm** (3 min). Run `breathe --ratio 6-6 -d 3 --no-log`. Note the same metric.
7. **Rest** (1–2 min).
8. **Test rate 4: 4.6 bpm** (3 min). Run `breathe --ratio 6-7 -d 3 --no-log`. Note the same metric.

**Interpreting results:** The rate that produces the highest RMSSD, the highest LF power in the HRV spectrum, or the visibly widest heart rate oscillations is your resonance frequency. If two adjacent rates are close, pick the slower one — it's more comfortable for long sessions.

**Limitations:** Phase durations are whole seconds, so only certain BPMs are representable: 4.6, 5.0, 5.5, 6.0, 6.7, 7.5 bpm. Your true resonance might fall between two testable rates. Pick the closest one. The difference in training effect between 5.0 and 5.5 bpm is small.

#### Using your frequency

Once you know your frequency, use `--ratio` to match it:

```bash
breathe --ratio 6-7    # 13s cycle = 4.6 bpm
breathe --ratio 6-6    # 12s cycle = 5.0 bpm
breathe --ratio 5-6    # 11s cycle = 5.5 bpm
breathe --ratio 5-5    # 10s cycle = 6.0 bpm (default)
```

You can also add exhale emphasis at your resonance frequency:

```bash
breathe --ratio 5-7    # 12s cycle = 5.0 bpm, exhale-weighted
breathe --ratio 4-7    # 11s cycle = 5.5 bpm, exhale-weighted
breathe --ratio 4-8    # 12s cycle = 5.0 bpm, strong exhale emphasis
```

### References

- Bernardi L, Spadacini G, Bellwon J, et al. ["Effect of breathing rate on oxygen saturation and exercise performance in chronic heart failure."](https://doi.org/10.1016/S0140-6736(97)10341-5) *Lancet*. 1998;351(9112):1308-1311.
- Bernardi L, Porta C, Spicuzza L, et al. ["Slow breathing increases arterial baroreflex sensitivity in patients with chronic heart failure."](https://doi.org/10.1161/hc0202.103311) *Circulation*. 2002;105(2):143-145.
- Bernardi L, Sleight P, Bandinelli G, et al. ["Effect of rosary prayer and yoga mantras on autonomic cardiovascular rhythms."](https://doi.org/10.1136/bmj.323.7327.1446) *BMJ*. 2001;323:1446.
- Vaschillo EG, Vaschillo B, Lehrer PM. ["Characteristics of resonance in heart rate variability stimulated by biofeedback."](https://doi.org/10.1007/s10484-006-9009-3) *Appl Psychophysiol Biofeedback*. 2006;31(2):129-142.
- Lehrer PM, Gevirtz R. ["Heart rate variability biofeedback: how and why does it work?"](https://doi.org/10.3389/fpsyg.2014.00756) *Front Psychol*. 2014;5:756.
- Russo MA, Santarelli DM, O'Rourke D. ["The physiological effects of slow breathing in the healthy human."](https://doi.org/10.1183/20734735.009817) *Breathe*. 2017;13(4):298-309.

## Design choices

This app is deliberately constrained. Several common breathing-app features are excluded for safety and focus:

**No breath retention.** Breath holds (kumbhaka) raise intrathoracic pressure via a Valsalva-like mechanism and can trigger vasovagal syncope or arrhythmia in cardiac patients. The Bernardi protocols use continuous breathing with no hold phases. The app rejects three-number ratios like `4-7-8` with an explicit safety error.

**No rapid breathing.** Patterns faster than 7.5 bpm (cycles shorter than 8 seconds) move toward hyperventilation territory, reducing arterial CO2 and mobilising catecholamines — the opposite of the vagal intent (Russo et al. 2017). The app enforces a minimum cycle length of 8 seconds.

**No breath holds between phases.** There is no pause between inhale and exhale. The breath is continuous, matching the protocol in Bernardi et al. (1998, 2002).

**Immediate exit, always.** Pressing `q` or `Ctrl+C` ends the session within one frame. The terminal is always restored — cursor, colours, input mode — even if the app crashes. The `finally` block that does this is the most important code in the file.

**No dependencies.** Single Python file, stdlib only. Nothing to install, nothing to break.

**No curses.** Direct ANSI escape codes only. The curses library has edge cases with non-default terminals on macOS Mojave.

## Requirements

- macOS (uses `/usr/bin/afplay`), Windows 11 (uses `winsound`), or Linux (auto-detects a sound player — see [Linux audio](#linux-audio))
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

| Time of day  | Preset      | Duration | Ratio | BPM |
|--------------|-------------|----------|-------|-----|
| Before noon  | `balanced`  | 10 min   | 5s-5s | 6   |
| 12:00–16:59  | `extended`  | 20 min   | 4s-6s | 6   |
| 17:00+       | `calm`      | 15 min   | 4s-6s | 6   |

All presets target 6 breaths per minute. The `balanced` preset uses equal inhale/exhale (5-5) as a neutral baseline. The `calm` and `extended` presets use a longer exhale (4-6), which emphasises vagal activation during the expiratory phase. The time-of-day auto-select picks `calm` in the evening as a default — but you can use any preset at any time.

### Presets

```bash
breathe --preset balanced    # 10 min, 5s-5s
breathe --preset calm        # 15 min, 4s-6s
breathe --preset extended    # 20 min, 4s-6s (full Bernardi protocol dose)
breathe --list-presets        # show the table
```

### Custom sessions

```bash
breathe --duration 5                # 5 minutes, default 5-5 ratio
breathe --ratio 4-6                 # default 10 minutes, 4-6 ratio
breathe --duration 12 --ratio 4-6   # 12 minutes, 4-6 ratio
```

Duration: 1–60 minutes (rounded up to complete breath cycles). Ratio: inhale and exhale each 3–10 seconds, total cycle >= 8 seconds, exhale at most 2x inhale.

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
| `--list-presets`  |       | Print preset table and exit                |
| `--version`       |       | Print version and exit                     |

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
  balanced · 5-5 · 09:12   [●]       <- preset, ratio, countdown, status

                INHALE                <- current phase (cyan) or EXHALE (green)

          ████████████████░░░░░░░░░░░░░░  <- breath bar (fills on inhale, drains on exhale)

  space pause · s mute · q quit       <- available controls
```

The status indicator shows `●` during breathing, `‖` when paused, and `🔇` when muted.

The countdown timer tracks completed breathing time only. If you pause for 30 seconds during a 1-minute session, the session takes ~90 seconds of wall-clock time to complete — the timer doesn't advance while paused.

## Linux audio

Linux has no single standard way to play a sound, so Breathe CLI probes for a player and falls back gracefully:

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
2026-05-30,07:15:02,balanced,5-5,600,600,60,100,completed
2026-05-30,19:30:14,calm,4-6,900,420,42,46,ended early (user)
```

Use `--no-log` to skip logging for a session. Use `--log` to see the log file path.

## Testing

Automated tests cover logic and arithmetic (formatting, ratio parsing, safety rejections, preset invariants, countdown calculation):

```bash
python3 -m unittest test_breathe -v
```

TUI behaviour (rendering, animation, terminal restoration) is covered by 25 manual acceptance tests in `dev/breathe-cli-spec.md`.

## Safety

Run `breathe --safety` for the full safety screen. The short version:

**Stop immediately** if you experience:

- **Lightheadedness or dizziness** — this usually means you are breathing too deeply, not too fast. Reduce the depth of each breath while keeping the same rhythm. The pacer sets the *timing*; you control the *volume*. If it persists, stop the session.
- **Palpitations** — stop, note the time, mention it at your next cardiology visit.
- **Tingling in hands or face** — a hyperventilation signal. Stop and return to normal breathing.

This app deliberately does not support breath retention, rapid breathing, or any pattern not grounded in the slow-breathing clinical literature. These constraints are enforced in the code and cannot be overridden. See [The science in brief](#the-science-in-brief) and [Design choices](#design-choices) for the clinical rationale.

## Disclaimer

This app is not a medical device. It does not diagnose, treat, cure, or prevent any disease or condition. Always consult your physician before starting a breathing practice, especially if you have a cardiac or respiratory condition. Use entirely at your own risk. The author assumes no liability for any adverse effects arising from the use of this software. By using this app you acknowledge that you understand and accept these terms.

## Roadmap

**Universal breathing patterns** — The app currently supports inhale-exhale only (no holds), by design. We're scoping a DSL for arbitrary four-phase patterns (`inhale-hold-exhale-hold`) that would enable box breathing, 4-7-8 relaxation, and other research-backed protocols while keeping the current cardiac-safe mode and its safety constraints intact. See [`dev/breathing-dsl-spec.md`](dev/breathing-dsl-spec.md) for the draft spec and [`dev/breathing-dsl-versions.md`](dev/breathing-dsl-versions.md) for the version plan — feedback welcome via [issues](https://github.com/marekkowalczyk/breathe/issues).

## License

MIT License. See [LICENSE](LICENSE) for the full text.

Created by [Marek Kowalczyk](https://orcid.org/0009-0008-3874-6736).
