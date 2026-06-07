# Next Session

Python v1.9 is feature-frozen (bugfixes only). Go v2 is the next major work.

## Carried over

- **Windows test coverage** — `test_breathe.py` has no tests for Windows-specific code paths. Low priority.
- **TODO #8 (cycle progress bar), #15 (BREATHE_BPM)** — both deferred to Go v2 if pursued.
- **Go v2 scaffold** — set up Go module, port state machine, TUI, audio, CLI flags, safety checks, logging, tests. Use branches and PRs.
- **Repo layout transition** — move Python files to `v1-python/`, set up Go project at root. Same repo, keep stars and history.

## Completed last session (2026-06-08)

- [x] ~~TODO #17–23~~ — ideas backlog: anxiety protocol, visual testing, log analysis, screensaver prevention, brown noise audio, embedded audio, public roadmap voting
- [x] ~~GitHub metrics snapshot~~ — 275 stars, 11 forks, 5k unique visitors/14d

## New — research items when ready

- **TODO #17 (anxiety protocol)** — research breathing patterns for acute anxiety; decide if it fits current safety model or needs #14's per-mode guardrails
- **TODO #21 (brown noise)** — research real-time audio synthesis in Go, volume envelope as breathing cue
- **TODO #22 (embedded audio)** — research Go audio libraries (Oto, Beep) for cross-platform playback without system deps
- **External PR #5 (coherence preset)** — review; note it adds a hold phase which conflicts with Python v1 safety constraints
- **Community issues #4, #6, #7** — all about Linux sound support; Go v2 resolves this naturally
