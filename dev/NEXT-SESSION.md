# Next Session

Python v1.9 is feature-frozen (bugfixes only). Go v2 is the next major work.

## Carried over

- **Windows test coverage** — `test_breathe.py` has no tests for Windows-specific code paths. Low priority.
- **TODO #8 (cycle progress bar), #15 (BREATHE_BPM)** — both deferred to Go v2 if pursued.
- **Go v2 scaffold** — set up Go module, port state machine, TUI, audio, CLI flags, safety checks, logging, tests. Use branches and PRs.
- **Repo layout transition** — move Python files to `v1-python/`, set up Go project at root. Same repo, keep stars and history.

## Completed last session (2026-06-12)

- [x] ~~DDD domain model~~ — `dev/domain-model.md`: ubiquitous language, value objects, single entity (SessionState), domain events, invariants, causalities, separation of concerns, Go v2 adoption note, language/architecture analysis
- [x] ~~`--mode` open question resolved~~ — `SafetyMode` is a `validate()` parameter at config time, not a runtime flag; `cardiac` preset carries its `SafetyConstraints`

## New — ready to start Go v2

The domain model is now the foundation. Recommended sequence for next session:

- **Start Go v2 scaffold** — `go mod init`, project layout per `breathing-dsl-versions.md`, `cmd/breathe/` + `internal/` packages
- **Define Go types first** — translate `dev/domain-model.md` §2 directly into Go structs: `type Seconds int`, `Pattern`, `Segment`, `Session`, `SessionState`
- **Pure functions before TUI** — implement `parsePattern`, `validate`, `cycleDuration`, `nextPhase` as pure functions with tests; no TUI or audio yet
- **External PR #5 (coherence preset)** — review; holds conflict with Python v1 safety constraints but are in scope for Go v2 with `SafetyMode = Universal`

## Research items (when ready)

- **TODO #17 (anxiety protocol)** — research breathing patterns for acute anxiety; decide if it fits current safety model or needs #14's per-mode guardrails
- **TODO #21 (brown noise)** — research real-time audio synthesis in Go, volume envelope as breathing cue
- **TODO #22 (embedded audio)** — research Go audio libraries (Oto, Beep) for cross-platform playback without system deps
- **Community issues #4, #6, #7** — all about Linux sound support; Go v2 resolves this naturally
