# Next Session

v1.9 shipped (GitHub release + PyPI). Added Windows 11 support (community PR #3) and updated pyproject.toml classifiers. Currently 700 lines (at the hard cap).

Writing files (blog post, LinkedIn draft, Medium draft, PUBLISH.taskpaper) moved to `~/repos/writing`.

## Open items

- **Windows test coverage** — `test_breathe.py` has no tests for Windows-specific code paths (winsound selection, msvcrt key polling, console setup). Low priority since these are platform-gated and hard to test on macOS.
- ~~**Triage HN feature requests**~~ — done. Breath holds/4-7-8 (TODO #14) fully scoped: DSL spec, version plan, safety architecture designed. Biofeedback and pomodoro remain out of scope.
- **Session progress bar — cycle count** (TODO #8), **Personal resonance frequency** (TODO #15) — both need line trimming first; file is at 777 lines.

## 2026-06-07 session outcomes

- **DSL spec written** — `dev/breathing-dsl-spec.md`: four-phase model (`I-H1-E-H2`), formal EBNF grammar, phase modifiers (airway, depth), chaining, named presets, two-layer validation (syntax + safety). Duration-vs-count precedence resolved (conflict is an error, §5.1).
- **Version plan written** — `dev/breathing-dsl-versions.md`: v2.0 (internal four-phase model) through v2.6 (modifiers), with dependency graph and open decisions.
- **README roadmap section added** — links to spec and version plan, invites issues.
- **TODO #16 added** — HN Show thread update, blocked by #14 implementation.
- ~~**Line cap decision needed**~~ — resolved: freeze Python at v1.x (bugfixes only), rewrite in Go for v2. Single binary eliminates the line cap and single-file constraints. See `dev/breathing-dsl-versions.md` for the full strategy.
- **Branch/PR workflow** — agreed to use branches and PRs for DSL implementation instead of pushing to master.
