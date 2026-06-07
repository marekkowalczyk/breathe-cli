# Next Session

Python v1.9 is feature-frozen (bugfixes only). Go v2 is the next major work.

## Carried over

- **Windows test coverage** — `test_breathe.py` has no tests for Windows-specific code paths. Low priority.
- **TODO #8 (cycle progress bar), #15 (BREATHE_BPM)** — both deferred to Go v2 if pursued.

## Completed last session (2026-06-07)

- [x] ~~Triage HN feature requests~~ — #14 fully scoped
- [x] ~~DSL spec~~ — `dev/breathing-dsl-spec.md` written: four-phase model, EBNF grammar, modifiers, chaining, presets, two-layer validation
- [x] ~~Version plan~~ — `dev/breathing-dsl-versions.md`: v2.0–v2.7 with Go rewrite strategy
- [x] ~~Line cap decision~~ — resolved: freeze Python v1, rewrite in Go v2
- [x] ~~README roadmap section~~ — links to spec and version plan
- [x] ~~TODO #16~~ — HN update item added, blocked by #14
- [x] ~~Publication ideas~~ — written to `~/repos/system/owner-inbox/2026-06-07-breathe-dsl-design-session-publication-ideas.md`

## New — next steps for Go v2

- **Decision: Go experience level** — open question #1 in version plan. Affects timeline.
- **Start v2.0: Go scaffold + Python v1 feature parity** — set up Go module, port state machine, TUI, audio, CLI flags, safety checks, logging, tests. This is the foundation. Use branches and PRs (not push-to-master).
- **Validate against Python acceptance tests** — all 25 manual tests from spec §3 must pass the Go binary before moving to v2.1+.
- **Repo layout transition** — move Python files to `v1-python/`, set up Go project at root. Same repo, keep stars and history.
- **Open decisions before v2.3** — mode flag vs. implicit mode, hold TUI design, audio cues for holds. See version plan.
- **Linux support** — Go makes it trivial. Audio is the main question (PulseAudio? ALSA? No sound by default?).
