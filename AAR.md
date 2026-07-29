# After Action Review

Continuous improvement log. Each session ends with a brief review: what went well, what didn't, what to change. This is the POOGI (Process Of Ongoing Improvement) record for this project.

## 2026-07-29 — Goal-word shorthand, v1.8 release, pure/impure section headers

Two commits since the last close: goal-word shorthand (`breathe quick calm`, order-free,
falls through to argparse for anything unrecognized) plus a version bump and doc-drift
cleanup, then a comment-only pass adding pure/impure section headers. `v1.8` tagged,
released on GitHub, and the tag later moved to include the section-header commit. 57/57
tests passing, tree clean, nothing unpushed.

**What went well:**
- **The goal-word feature was scoped by explicit question before any code**, not assumed:
  preset-alongside-vs-replace, conflict handling, vocabulary size, and timing were each
  asked and answered before `try_parse_goal_words` was written, keeping the vocabulary to
  the agreed 2×2 rather than growing organically.
- **Caught real open loops before tagging** rather than tagging on request alone: version
  not bumped, a stale "25 manual tests" count in two docs, and a pre-existing spec/code
  version mismatch were all found and flagged, and the user chose to fix all three before
  release.
- **The "no derivable numbers in docs" principle got applied immediately**, not just
  written down: the spec's own `--version` acceptance test was rephrased to reference the
  `VERSION` constant instead of a literal string, in the same pass that added the rule.
- **The 700-line cap flagged as worth revisiting back on 2026-05-15 ("the file is already
  well past the 500-line target") was actually revisited this session** — removed from
  `CLAUDE.md` at the user's request, rather than continuing to spend effort on cosmetic
  compaction against a cap nobody had re-examined in two months.

**What didn't go well:**
- **Repo confusion: an unrelated project's work (`meds`) got initiated in the middle of
  this `breathe` session**, and had to be untangled afterward with a separate partial
  close in that repo. The user named this as their own mistake, not a correction of me,
  but it cost a full detour and a scoped close to unwind — worth naming here since it's
  exactly the kind of cross-project drift a close is supposed to catch.
- **A CLI smoke test hit the 120-second background timeout** because it ran `breathe`'s
  non-TTY path with default (multi-minute) durations instead of a short custom one — had
  to kill the backgrounded process and re-verify by calling `try_parse_goal_words`
  directly instead of shelling out to the full CLI.

**What we'll do differently:**
- **If a request names or clearly concerns a different project/repo than the one the
  session is rooted in, say so and confirm before doing any work there**, rather than
  proceeding inline and sorting out the scope afterward with a partial close. First
  occurrence of this specific drift in this repo's history — process note, not yet a rule.
- **When smoke-testing a CLI's non-TTY path, always pass a short explicit duration
  (`-d 1` or shorter via a custom ratio) — never rely on defaults**, which can run
  multiple minutes and blow past a background command's timeout. Mechanical: check the
  command includes `-d` before backgrounding it.

## 2026-07-29 — Install on new machine; bare-invocation design review

**What went well:**
- Install verification was thorough before symlinking: checked Python version, `afplay` presence, both sound files, and ran the full test suite (42 tests, all passing) rather than assuming stdlib-only + macOS-only meant no verification was needed
- Talked through the bare-`breathe`-invocation design question (time-of-day auto-preset vs. fixed default vs. Unix-help-first convention) with explicit options and tradeoffs before touching anything

**What didn't go well:**
- Nothing notable — no code changed this session, no corrections needed

**What we'll do differently:**
- Nothing process-wise. Decision of record: bare `breathe` keeps auto-selecting preset by time of day; the existing 3-2-1 countdown (which displays the selected preset/duration and accepts `q`) was judged sufficient as a confirmation window. Revisit only if the midday `long` (20 min) default turns out to not match actual usage patterns.

## 2026-05-15 — Add session logging and TODO items

**What went well:**
- Spec-first workflow worked smoothly again — caught the out-of-scope constraint before writing code, amended the spec cleanly, then implemented from it
- Implementation was straightforward and fit within the 700-line cap (exactly 700)
- Testing confirmed logging works correctly in both normal and `--no-log` paths

**What didn't go well:**
- The 700-line hard cap required significant time spent on cosmetic line-count trimming (collapsing blank lines, compacting docstrings, extracting `_die()` helper). The feature itself was ~30 lines but fitting it required touching 15+ unrelated spots
- TODO.md had accumulated structural issues (duplicate `## Bugs` headers, item #2 not marked done) — should have been caught at the end of the previous session

**What we'll do differently:**
- When approaching the 700-line cap, consider whether the cap should be revisited in the spec rather than spending effort on cosmetic compaction. The file is already well past the 500-line target
- Always clean up TODO.md during the close checklist, not just when adding items

## 2026-05-26 — Go rewrite analysis + countdown timer (v1.4)

**What went well:**
- Six Thinking Hats analysis was a good lightweight way to evaluate a rewrite idea without wasting implementation effort — concluded "not worth it" with clear reasoning
- Spec-first workflow continues to work well: amended spec to v1.4 before touching code
- The countdown change was surgically small (one line of logic) and required no new architecture
- Caught the 701-line cap violation immediately and fixed by inlining the computation

**What didn't go well:**
- Hit the 700-line cap on a trivial +1 line change — the cap is now fully consumed and any future feature will face the same friction

**What we'll do differently:**
- Nothing process-wise — this session was clean. The line cap issue is a known constraint already tracked in TODO and prior AAR

## 2026-05-26 — State machine refactor, pause-resume reset (v1.5)

**What went well:**
- Visual testing workflow — asking user to run and inspect the TUI was far more effective than scripting pty captures, which wasted time and tokens
- The state machine refactor landed clean: net -5 lines, simpler mental model, and the pause-resume behavior works correctly
- Iterative design through conversation: the elapsed time model evolved through three rounds of feedback (wall-clock minus pauses → completed breathing time → smooth countdown with snap-back) and each round sharpened the design

**What didn't go well:**
- First attempt at pause-resume (flag-based break out of nested loops) caused a 4-second overshoot bug and had to be fully reverted — should have recognized the nested loop structure was the root problem earlier instead of trying to patch it
- Spent significant tokens on programmatic pty capture that produced no useful output — the app needs a real terminal

**What we'll do differently:**
- For TUI changes, always ask the user to run and visually verify — never attempt programmatic terminal capture (already saved to memory)
- When a feature requires breaking out of multiple loop levels with flags, treat that as a design smell and consider restructuring first

## 2026-05-30 — Bug fix round (#6, #10, #12), audio refactor, spec slimdown (v1.6)

**What went well:**
- Bug investigation was efficient — read the code, identified root causes from structure (stale frame on `continue`, `int()` truncation, missing final render), fixed with minimal changes
- Sound debugging was systematic — tested both audio backends independently, quickly isolated AudioToolbox as the silent failure, swapped priority
- Refactoring removed 65 lines (711→646) by dropping dead code (AudioToolbox) rather than cosmetic compaction — the right kind of line reduction
- Spec slimdown was overdue and landed well — 785→108 lines, keeping only the load-bearing parts (safety constraints, acceptance tests)

**What didn't go well:**
- Didn't flag the spec's post-hoc drift proactively — the user had to ask "what's the value of keeping this?" before I surfaced it
- After slimming the spec, missed stale cross-references in CLAUDE.md until explicitly asked to check other documents

**What we'll do differently:**
- After any structural change, proactively scan all docs for stale references and coordination issues
- When a document is being maintained post-hoc rather than driving work, flag that to the user as a potential simplification opportunity

## 2026-05-30 — Bug #13 fix, automated test suite (v1.7)

**What went well:**
- Debug logging to a file was the breakthrough — after four failed attempts based on code reading, instrumenting the actual runtime exposed the root cause in minutes
- The fix was simple and correct once the real problem was identified: two lines at config time to round `duration_s` up to a whole number of cycles
- Test suite infrastructure (42 tests) now exists, covering all logic and arithmetic paths including the bug #13 fix

**What didn't go well:**
- Spent five fix attempts patching symptoms (display rounding, phase offsets, stepped countdown) without questioning whether the inputs to the loop were correct — classic fixation on the wrong abstraction level
- Failed to ship tests alongside the fix — user had to remind me, which is a basic engineering discipline failure
- The `replace_all` for `session_s` clobbered unrelated `session_start_time` variables — careless use of a blunt tool

**What we'll do differently:**
- When designing flags or parameters that interact, always validate logical consistency at config time — the `-d`/`-r` inconsistency was introduced at the design level and haunted us for several rounds of failed fixes. Inputs that must be coordinated should be coordinated before they reach the runtime loop
- When a bug survives multiple fix attempts, stop and instrument — add debug logging and observe actual values instead of reasoning from code alone
- Always ship tests with code changes, never as a follow-up
- When using replace_all, grep for collateral matches first
