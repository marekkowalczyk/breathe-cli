---
layout: default
title: The science behind Breathe CLI
permalink: /science/
---

# The science behind Breathe CLI

Breathe CLI paces slow breathing for cardiac vagal tone support. It is a **habit tool**, not a medical device: it does not diagnose, treat, or monitor disease, and it does not replace care from your clinician.

For install and usage, see the [product home](https://marekkowalczyk.github.io/breathe-cli/).

## Mechanism

Resonance breathing — paced breathing near **six breaths per minute** (a 10-second cycle) — is among the better-studied non-pharmacological ways to engage cardiac vagal pathways.

The chain is physiological, not mystical:

1. Slow paced breathing amplifies **respiratory sinus arrhythmia (RSA)** — the natural rise and fall of heart rate with each breath.
2. Larger RSA reflects stronger **vagal (parasympathetic) outflow** to the heart.
3. That outflow trains the **baroreflex** and tends to shift autonomic balance away from chronic sympathetic dominance.

Around 0.1 Hz (~6 breaths/min) is also where many adults show a **cardiovascular resonance** peak in heart-rate variability research: breathing, heart rate, and blood-pressure oscillations line up so baroreflex stimulation is especially strong. Individual “resonance frequency” can sit a little below or above 6 bpm; this app uses a fixed ~6 bpm protocol that matches the clinical slow-breathing literature it cites, not a sensor-guided personal RF assessment.

## Why this matters in HFrEF / CHF

In heart failure with reduced ejection fraction (HFrEF), sympathetic overdrive is both a symptom and a driver of progression. Trials of slow breathing in chronic heart failure (CHF) have shown improvements in **baroreflex sensitivity**, oxygen saturation, and exercise tolerance — sometimes after a single session, with further gains when practice is daily over weeks.

That evidence motivates a low-friction daily habit. It does **not** mean breathing replaces guideline-directed medical therapy, devices, or follow-up. Effects vary; this app cannot predict individual clinical outcomes.

## How presets map to the literature

All named presets keep a **10-second cycle → 6 breaths/min**. What changes is duration and inhale:exhale balance.

| Preset | Duration | Ratio (in–ex) | Intent | Literature anchor |
|--------|----------|---------------|--------|-------------------|
| `morning` | 10 min | 5–5 | Equal phases; daily baseline | Habit-sized morning bout; acute RSA/baroreflex effects appear within a short paced session |
| `midday` | 20 min | 4–6 | Longer exhale; main daytime train | Within the common ~15–20 min training-bout band; CHF home device-guided work is often ~15 min × 2/day (this app runs one session per invoke) |
| `evening` | 15 min | 4–6 | Sympathetic wind-down | Matches common single-session CHF / evening slow-breathing length (e.g. Laborde 15 min) |
| `night` | 20 min | 3–7 | Stronger exhale bias before sleep | Tsai 2015 pre-sleep 6 cpm, 3–7, ~20 min |

Goal-word feel axis (same ratios, duration chosen separately): `train` → 5–5, `calm` → 4–6, `sleep` → 3–7. Custom sessions stay inside the same envelope: each phase 3–10 s, **total cycle ≥ 8 s**.

## Safety physiology (why the app refuses some patterns)

Several popular breathing-app features are excluded on purpose:

- **No breath retention (kumbhaka).** Holds raise intrathoracic pressure and can provoke vasovagal syncope or arrhythmia risk in cardiac patients. Three-number ratios such as `4-7-8` are rejected.
- **No rapid breathing.** Cycles shorter than 8 seconds move toward hyperventilation and catecholamine mobilisation — opposite of the vagal goal.
- **Continuous inhale ↔ exhale.** There is no prompted pause between phases, matching continuous paced protocols in the cited clinical work.

Stop immediately if you feel lightheadedness, palpitations, or tingling in the hands or face. Run `breathe --safety` for the in-app safety screen.

## What this app claims — and what it does not

**Supports:** a consistent, timed practice of slow continuous breathing at ~6 bpm, with presets aligned to published protocol shapes.

**Does not:** measure heart rate, HRV, SpO₂, or blood pressure; find your personal resonance frequency; provide biofeedback; or claim to reverse heart failure. For true HRV biofeedback you need appropriate sensors and a clinician- or researcher-guided protocol (Lehrer / Vaschillo tradition).

## Key references

- Bernardi L, Porta C, Spicuzza L, et al. [Slow breathing increases arterial baroreflex sensitivity in patients with chronic heart failure.](https://doi.org/10.1161/hc0202.103311) *Circulation*. 2002;105(2):143-145. — Baroreflex and CHF; primary clinical anchor for slow 6 bpm practice.
- Bernardi L, Sleight P, Bandinelli G, et al. [Effect of rosary prayer and yoga mantras on autonomic cardiovascular rhythms.](https://doi.org/10.1136/bmj.323.7327.1446) *BMJ*. 2001;323:1446. — ~6 breath/min rhythms and autonomic cardiovascular effects.
- Lehrer PM, Gevirtz R. [Heart rate variability biofeedback: how and why does it work?](https://doi.org/10.3389/fpsyg.2014.00756) *Front Psychol*. 2014;5:756. — Resonance, RSA, and baroreflex framing for paced breathing / HRVBF.
- Vaschillo EG, Vaschillo B, Lehrer PM. [Characteristics of resonance in heart rate variability stimulated by biofeedback.](https://doi.org/10.1023/B:APBI.0000026635.08453.0a) *Appl Psychophysiol Biofeedback*. 2004;29(3):159-166. — Cardiovascular resonance near ~0.1 Hz (context for fixed ~6 bpm pacing; this app does not run RF assessment).
- Tsai HJ, Kuo TB, Lee GS, Yang CC. [Efficacy of paced breathing for insomnia: Enhances vagal activity and improves sleep quality.](https://doi.org/10.1111/psyp.12333) *Psychophysiology*. 2015;52(3):388-396. — Pre-sleep ~6 cpm; informs `night` (3–7, ~20 min).
- Laborde S, et al. [Influence of a 30-Day Slow-Paced Breathing Intervention Compared to Social Media Use on Subjective Sleep Quality and Cardiac Vagal Activity.](https://doi.org/10.3390/jcm8020193) *J Clin Med*. 2019;8(2):193. — Multi-week slow breathing, sleep, and cardiac vagal activity.

← [Back to Breathe CLI](https://marekkowalczyk.github.io/breathe-cli/)

Personal project by [Marek Kowalczyk](https://orcid.org/0009-0008-3874-6736).
