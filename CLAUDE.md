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

**Released vs tip (agents: use tip for product checks):** On this machine, plain `breathe` is the **Homebrew** install (`marekkowalczyk/breathe` tap → Cellar), i.e. the last tagged release. It does **not** reflect uncommitted or untagged tip. For any CLI smoke after code changes (`-v`, `-h`, presets, safety errors, TUI), invoke the repo file — never assume PATH `breathe` is tip:

```
python3 breathe.py -v
python3 breathe.py -h
# or, if configured in the user's shell:
breathe-dev -v
```

Do **not** `brew link` the clone over Cellar, and do not overwrite `/opt/homebrew/bin/breathe` with a repo symlink — that fights `brew upgrade`. After a release ships, the user upgrades with `brew upgrade breathe` (tap must be trusted: `brew trust marekkowalczyk/breathe`).

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

## Versioning

`breathe -v` / `--version` prints both constants from `breathe.py`:

```
breathe {VERSION} {RELEASED}
```

example: `breathe 1.10 2026-08-28T09:50`

| Constant | Shape | Meaning |
|---|---|---|
| `VERSION` | semver (`MAJOR.MINOR.PATCH`) | Product version; bump when shipping user-visible behaviour |
| `RELEASED` | local wall time, minute precision (`YYYY-MM-DDTHH:MM`) | When this tip was cut — **no** seconds, **no** timezone |

**Keep both current — non-negotiable on ship:**

1. Every **product** commit that ships to `master` (user-visible behaviour) updates **`RELEASED`** in the same commit as any **`VERSION`** bump.
2. Update **`VERSION`** whenever the change is user-visible product behaviour (new preset, CLI flag, bugfix users notice).
3. A short atomic series may stamp `RELEASED` on the product commit; a following process-only commit in the same push need not re-touch `breathe.py`. Before push, the tip’s `breathe -v` must still show a `RELEASED` that matches the ship wall-clock (± a few minutes).
4. Do **not** hardcode the version string in README/spec acceptance text — reference `VERSION` / `RELEASED` / `version_string()` (same “no derivable numbers in docs” rule).
5. Git tags (`v1.10`) track `VERSION` only; `RELEASED` is the human-readable “when” for `-v`.

## Releases

Tag + GitHub Release track `VERSION` (`v{VERSION}`). **Suggest only — never auto-tag or `gh release create` without explicit user authorization to publish a release.**

After product commits that bump `VERSION`, after any other **significant** product ship (user-visible tip ahead of the latest tag), and on session close, run:

```
./scripts/suggest-release.sh
```

- If `VERSION` is ahead of the latest `v*` tag, **propose a release in chat right away** (tag + `gh release create` + Homebrew formula bump) — do not wait for session close. Also note it under NEXT-SESSION **Immediate** on close if still unreleased.
- If tags match, no action.
- Creating the tag/release still requires the user to authorize a release publish (same spirit as push authorization).
- **Docs audit before close** after a fold, release, or user-visible TUI/CLI change: check `README.md` and the [`homebrew-breathe`](https://github.com/marekkowalczyk/homebrew-breathe) tap README against tip (presets, install/`brew trust`, display chrome). Do not wait for the user to ask whether docs are current.
- **No live URL or install claim until the serving remote has the tip.** Do not tell the user a GitHub Pages path, release URL, or `brew install`/`upgrade` path is ready until the commit (and Pages rebuild, if applicable) is on the remote that serves it. Claiming `/science/` before push caused a user-visible 404 (2026-08-30); same class as docs lagging the ship (2026-08-28).

## Commits

**One commit = one concern** — same spirit as one issue = one concern. Prefer a short series of
atomic commits over one bundled ball.

**Commit when the chunk is done — don’t wait to be asked.** As soon as a meaningful atomic
unit of work is finished and verified (tests/smoke that matter for that change), create the
commit. Do not leave completed slices sitting uncommitted until “commit”, “close”, or
end-of-session. If the next slice is unrelated, commit first, then start the next.

| Do | Don't |
|---|---|
| Commit each finished atomic chunk immediately | Batch several finished concerns into one late commit |
| One logical change per commit (rename **or** policy **or** close) | Mix product behaviour with constitution edits “while we’re here” |
| Imperative subject ≤ ~72 chars (“Rename preset long to midday”) | Vague subjects (“updates”, “wip”, “fix stuff”, “misc”) |
| Body explains **why** (1–3 lines) when the why isn’t obvious | Body that restates the diff or lists every file |
| Match / cite a GH issue when the work was issue-tracked | Stuff five issues into one commit message |
| Split when `git diff --stat` shows unrelated clusters | Squash unrelated work to “save” commit count |

**Still ask before push** unless the user already authorized publishing. Committing locally ≠ publishing.

**Push is authorized when the user clearly asks to publish**, including shorthand such as:
`push`, `commit and push`, `close, commit, push`, `ship it`, or `publish`. That authorization
covers the current unpushed batch on the branch being discussed — not a standing license for
later sessions. If only `commit` / `close` is said, commit (and close) but **do not** push.

**Prefixes (fixed where used)**

- `close:` — session-close artifacts only (`AAR.md` / `NEXT-SESSION.md`, maybe a tiny policy promote).
- No other required prefixes; plain imperative is the default.

**Before `git commit`:** scan the staged set — if you need “and also” in the subject, unstage and split.

## File layout

```
breathe.py                 # the app (single file)
test_breathe.py            # automated tests (stdlib unittest)
breathe-cli-spec.md        # safety constraints and acceptance tests
CLAUDE.md                  # this file (constraints + project policy)
AAR.md                     # after-action / process lessons
NEXT-SESSION.md            # session handoff baton (not a backlog)
scripts/suggest-release.sh # VERSION vs latest v* tag; suggest tag+release only
```

## Tracking & handoff (GitHub Issues policy)

**GitHub Issues are the only product backlog.** Bugs, enhancements, and scoped feature
ideas live there — not in markdown trackers. There is no `TODO.md`; do not recreate one.

| Artifact | Role | Put here | Do not put here |
|---|---|---|---|
| **GitHub Issues** | Durable product work | Bugs, enhancements, acceptance criteria, open design questions for a feature | Session diary, process tips, machine-local notes |
| **`NEXT-SESSION.md`** | Cold-start handoff for the next agent/human | What’s blocking, decisions not to relitigate, process recall aids, **links** to open issues, current version/test state | A second copy of the backlog; issue bodies; long feature specs |
| **`AAR.md`** | Process Of Ongoing Improvement | What went well/badly, durable process lessons (promote load-bearing ones into `CLAUDE.md`) | Open feature lists |

**When to open an issue (before coding)**

Issues are for durable product work — **not** a ticket for every keystroke. Prefer filing
**before** implementation when any of these hold; otherwise ship and mention in the session
close / AAR if useful.

| Open an issue first when… | Skip the issue when… |
|---|---|
| Scope could grow (“and also”, open design forks) | One short commit, no open questions |
| Work should survive this session / cold-start handoff | Typo, flag alias, doc sync with code just shipped |
| Acceptance criteria or safety touchpoints matter | Pure process/doc edits to `CLAUDE.md` / AAR / NEXT-SESSION |
| You’re choosing among approaches worth recording | Rename/reorder already decided in chat (optional issue *after* for history) |
| Deferred slice of a larger idea (sibling of a closed umbrella) | Accidental / probe noise (close `not_planned`, don’t backlog it) |

**Rule of thumb:** if you’d write more than half a page of plan, or the work could become two
PRs, file first (one concern each). If you’d finish in one obvious commit, just ship — don’t
replace under-scoping with issue theater.

**Lifecycle**

1. **Open** — follow the filing checklist below; link siblings; one concern only.
2. **Implement** — stay inside **In**; if scope grows, split a new issue before coding the extra.
3. **Close** — on ship (`completed`); comment with version/`RELEASED` tip if useful. Umbrellas that
   were split → `not_planned` with pointers (see #3 → #8/#9).
4. **Handoff** — surviving open work appears in `NEXT-SESSION.md` as **issue links only**.

Do **not** migrate `NEXT-SESSION.md` itself into Issues — handoff context is not issue-shaped.

**Issue hygiene for this repo**

**One issue = one concern = one shippable slice.** If an issue needs “and also”, split it before filing.
Cross-link siblings; never merge unrelated acceptance criteria into one body.

| Good (one concern) | Bad (split these) |
|---|---|
| Fix time-bar visibility (`draw_progress` glyphs/dim) | Fix time-bar visibility **and** add cycle-count bar |
| `caffeinate` during session + cleanup in `finally` | Display sleep **and** dimmer night TUI |
| Night preset: 3–7 ratio + auto-select window | Preset **and** dim UI **and** quieter audio |
| Quieter `afplay` volume when `preset_name == 'night'` | Dimmer colours **and** quieter audio |

**Filing checklist**

1. **Title** — verb + single deliverable (“Prevent display sleep during session”, not “Night mode improvements”).
2. **Problem** — one paragraph; the user-visible failure or gap.
3. **Scope** — explicit **In** / **Out**; “Out” names sibling issues if they exist.
4. **Acceptance** — checklist testable in one PR; no “consider” or “TBD” items (resolve or move to a design issue).
5. **Related** — links only; no duplicate specs.

**When scope grows**

- **During triage:** split immediately; close the umbrella with `state_reason: not_planned` and pointers to new issues (see closed #3 → #7/#8/#9 lesson).
- **Epics are discouraged.** If work is inherently multi-phase (e.g. multi-mode architecture), file a **design/scoping** issue whose *only* deliverable is a written decision + child issue list — not implementation acceptance criteria mixed in.
- **Do not** track session handoff, process tips, or “nice to have later” as issues unless there is a concrete deliverable.

**Session close**

When the user signals wrap-up (“close”, “done for today”, “archive this session”, “that’s a wrap”, etc.), **run the session-close skill** (global `session-close`, unless a project-local skill replaces/overlays it). Do **not** treat push/tag/Homebrew alone as a close.

Required outcomes:

- Rewrite `NEXT-SESSION.md` (don’t append). Carried-over = **pointers to open issue numbers** only; prune closed ones.
- AAR entry with user corrections named; recurrence labelled; lessons dispositioned.
- Promote durable process lessons into `CLAUDE.md` (this file), not only into the AAR.
- `close:` commit for close artifacts (+ tiny policy promotes). Push only if authorized.
- Baton pass **in chat**: next action, blockers, promotions made.

**Safety & labels**

- Keep safety constraints (no retention, cycle ≥ 8s, terminal restore) explicit when a change could touch them.
- Labels: `bug` / `enhancement` as appropriate; acceptance checklists in the body when useful.
