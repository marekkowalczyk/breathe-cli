# After Action Review

Continuous improvement log. Each session ends with a brief review: what went well, what didn't, what to change. This is the POOGI (Process Of Ongoing Improvement) record for this project.

## 2026-09-03 — iPhone + eyes-closed Issues; AISDLC on #34

Filed [#34](https://github.com/marekkowalczyk/breathe-cli/issues/34) (native iPhone app, parked) and [#35](https://github.com/marekkowalczyk/breathe-cli/issues/35) (CLI eyes-closed / stronger audio cues). User then required [AISDLC](https://academy.claude.com/courses/ai-native-sdlc-playbook) for building the app — encoded as process on #34 (intent → spec → plan → evals → human production gate). Pruned the roadmap `say` candidate into #35’s “already covered” table. No product code. Measured at close: 85 tests OK; tip `1.14.0 2026-08-31T09:29`; VERSION sync OK; nothing to release; unpushed 0 before this close commit.

**What went well:**
- **File-only held** — Issues + issue-body process edit only; no Xcode scaffold, no CLI flag work.
- **One concern each** — iPhone (#34) separate from desktop GUI (#22); eyes-closed CLI (#35) separate from night audio/dim (#17/#18).
- **Process constraint landed on the Issue** — AISDLC rules live where the next agent will open the ticket, not only in chat.

**What didn't go well:**
- Nothing material; short park session. (No user correction.)

**What we'll do differently:**
- When the user attaches a build process (e.g. AISDLC) to a parked product idea: update that Issue’s body with stage table + hard gates in the same turn — do not invent a parallel doc in the wrong repo. **Process note.**
- After filing a roadmap candidate as an Issue: prune `ROADMAP-CANDIDATES.md` in the same session (or the close) so the park file does not re-suggest already-filed work. **Process note** (reinforces existing “delete or prune after filing”).

---

## 2026-08-31 (PM) — Finish-clock + progress-bar issues only

Diagnosed session time-bar “behind / uneven” as likely `round()` + coarse `BAR_WIDTH` quantization (not countdown drift); brainstormed estimated finish clock time. **User correction:** file Issues only — do not implement. Filed [#32](https://github.com/marekkowalczyk/breathe-cli/issues/32) (finish clock) and [#33](https://github.com/marekkowalczyk/breathe-cli/issues/33) (progress feel). No product code. Measured at close: 85 tests OK; tip `1.14.0 2026-08-31T09:29`; VERSION sync OK; nothing to release; prior close commit had been sitting unpushed.

**What went well:**
- **Diagnose before filing** — suspected quantization documented in #33 so the next agent does not “fix” non-drift.
- **One concern each** — finish clock and progress feel as sibling Issues, cross-linked to #14/#15.

**What didn't go well:**
- **User correction — “Only file as issues; don't do anything with them.”** Scope lock was clear; agent had been in design mode and needed the hard stop made explicit.
- Previous session’s `close:` commit was still unpushed at this session’s start (publish lag).

**What we'll do differently:**
- When the user says file-only / park / don’t implement: open Issues (or refuse product edits) and stop — no design-doc commit, no code, no “while we’re here.” **Process note.**
- On session open, if the hook shows unpushed commits, surface them before new work — don’t wait for the next close. **Process note** (reinforces existing push-authorization habit).

---

## 2026-08-31 — PRs, Linux sound, omakase, v1.14.0 release

Triaged open PRs (#5 closed → speculative [#30](https://github.com/marekkowalczyk/breathe-cli/issues/30); #10 superseded by tip port). Recorded macOS-primary / Linux+Windows secondary (community-only). Re-implemented Linux sound from #10 (@kenlacroix); closed #4/#6/#7/#23. Enshrined bare-`breathe` omakase in `CLAUDE.md`/README with DHH/Omacom credit. Filed [#31](https://github.com/marekkowalczyk/breathe-cli/issues/31) (opt-in menu interview). Elevator statement in README. Shipped **v1.14.0** (tag, GitHub Release, PyPI green, Homebrew bump + tap README). Measured at close: 85 tests OK; tip and PATH `breathe` both `1.14.0 2026-08-31T09:29`; VERSION sync OK; tags match; unpushed 0 before this close commit.

**What went well:**
- **Port stale community PR onto tip** instead of merging a conflicted branch — credit left intact; faster than rebase theatre.
- **C1-hostile PR closed with a parked speculative issue (#30)** — “not for now / stays vagal” without discarding the idea or leaving a dirty PR open.
- **User held release for Tahoe smoke** then authorized — correct gate; Cellar and tip match after brew bump.
- **Tap README audited with the formula bump** — platform/omakase wording landed with the ship (docs-audit rule held).

**What didn't go well:**
- **User correction — Linux wanted, not deferred:** first #10 reply gated merge on #23 alone; user then said they want Linux support. Stance + tip port followed, but the first comment understated the product intent.
- **Menu-interview issue (#31) sat as a draft** until end-of-day leftovers — original item 2 of the session opener.
- Typed release as `v1.14.01` — agent correctly shipped `v1.14.0` to match `VERSION` (near-miss on semver drift).

**What we'll do differently:**
- When the owner states a platform intent (“I want Linux support”), update constitution + ship or schedule the port in the same decision thread — do not leave the only public signal as “blocked on homebrew/core.” **Process note.**
- Safety-violating community PRs: close as not-planned-*for-now* + file a speculative parked issue in the same breath (pattern from #5→#30). **AAR only** (first clean occurrence).
- Session openers with numbered lists: finish each item or park it as an Issue before the next — don’t leave “file later” drafts overnight. **Process note.**

---

Philosophy-aligned roadmap brainstorm against open Issues / README / spec; saved as `ROADMAP-CANDIDATES.md` for later one-concern issue filing (not a second backlog). Measured: 77 tests OK; tip/brew `1.13.0 2026-08-30T21:02`; VERSION sync OK; nothing to release.

**What went well:**
- **Candidates file, not Issues yet** — brainstorm stays durable without flooding the backlog or recreating `TODO.md`; convert when ready (one concern each).
- **Anti-roadmap called out** — config/accounts/holds/BLE-in-file explicitly out of scope, so later filing stays filtered.

**What didn't go well:**
- Nothing material; short planning session.

**What we'll do differently:**
- When a multi-slice roadmap brainstorm is worth keeping but not ready to file: park in `ROADMAP-CANDIDATES.md` (or delete after filing), never in `NEXT-SESSION.md` as a backlog dump. **Process note.**

---

## 2026-08-30 (late+) — Name-collision note (npm / crates); push handoff

README Installation now states npm [`breathe-cli`](https://www.npmjs.com/package/breathe-cli) and crates.io [`breathe`](https://crates.io/crates/breathe) are unrelated — this app is Python via Homebrew/PyPI. Measured: 77 tests OK; tip/brew `1.13.0`; nothing to release.

**What went well:**
- **One calm sentence under install** — enough to stop wrong-registry installs without a comparison table.

**What didn't go well:**
- Nothing material; small doc follow-through after the user flagged the npm collide (and earlier the Rust one).

**What we'll do differently:**
- When a same-name package appears on another registry, add a README “not the same project” line at install time — do not wait for a support ticket. **Process note.**

---

## 2026-08-30 (late) — Display stay-awake (#13); PATH vs tip; hold release for manual test

Designed and shipped session-scoped display-idle inhibit in `breathe.py` (cross-platform stdlib: macOS `caffeinate`, Windows `SetThreadExecutionState`, Linux `systemd-inhibit`), with calm acquire-failure notices. [#13](https://github.com/marekkowalczyk/breathe-cli/issues/13) closed. Tip later moved to **v1.13.0** (other sessions); feature is on current tip. Measured this close: 77 tests OK; `python3 breathe.py -v` and PATH `breathe -v` both `1.13.0 2026-08-30T21:02`; VERSION sync OK; unpushed 0.

**What went well:**
- **Kept stdlib / single-file** — OS backends behind acquire/release; no wake library; failure never aborts the session.
- **Failure UX matched soft-fail tone** — stderr like audio fallback + summary `Note:`; `--quiet` suppresses the startup line.
- **User held release for manual test** — correct gate before tag; later evening tip/brew already at 1.13.0 with the feature in history.

**What didn't go well:**
- **User correction — PATH `breathe` still showed 1.11.1** while tip was 1.12.0. Install split is documented, but the agent did not remind at the moment of the VERSION bump / “test this” handoff.
- Workspace root was missing `repos/breathe`; real clone is `breathe-cli` (same as earlier today).
- GitHub MCP could not comment/close #13 from this agent (403); issue closed by another path.

**What we'll do differently:**
- **Recurring (2nd):** PATH Cellar vs tip. After any tip `VERSION` bump (and before asking the user to “try it”), say once: smoke with `python3 breathe.py -v`, not PATH `breathe`. Already in `CLAUDE.md` § Testing — **reinforce as process note** (chat habit), not a new CLAUDE section.
- Prefer `~/repos/breathe-cli` as Cursor root for product work (AAR only — situational).

---

## 2026-08-30 (evening) — PyPI publish path, README install/badges, HN park #28, GitHub MCP

Caught PyPI stuck behind tip; shipped Trusted Publishing (`publish.yml`) + version-sync check; README gained `pip install breathe-cli` and badges (PyPI / Homebrew / MIT / Show HN). Audited Show HN thread — no must-create product issues; parked HRV biofeedback as [#28](https://github.com/marekkowalczyk/breathe-cli/issues/28). Wired Cursor GitHub MCP via `open -a Cursor --env GITHUB_PERSONAL_ACCESS_TOKEN="$(gh auth token)"` (read/write verified). Measured: 77 tests OK; tip `breathe 1.13.0 2026-08-30T21:02`; VERSION matches tag; unpushed work exists (README + this close).

**What went well:**
- **Install channels documented together** — Homebrew recommended, PyPI present, live version badge — closes the discoverability gap that left pip at 1.9.
- **HN triage stayed disciplined** — mapped themes to existing issues; only durable new idea filed (#28); no necro status dump on the thread.
- **MCP diagnosis before rabbit hole** — PAT existed via `gh` keyring but Cursor never saw it; `--env` relaunch fixed it without inventing a second token.

**What didn't go well:**
- **PyPI lag unnoticed for months** until this session — GitHub/Homebrew had a release habit; pip did not.
- **GitHub MCP 403/timeouts** looked like “auth broken” when the real failure was under-scoped / unset `GITHUB_PERSONAL_ACCESS_TOKEN` in the Cursor process; `gh` still worked, which masked the split.

**What we'll do differently:**
- **Releases always include the PyPI path** — already in `CLAUDE.md` § Releases (Trusted Publishing); confirm Actions green before claiming pip is updated. (AAR reinforces; no new CLAUDE edit.)
- **Cursor GitHub MCP:** launch with `GITHUB_PERSONAL_ACCESS_TOKEN` in the process env (`open -a Cursor --env …="$(gh auth token)"`); do not assume `gh` keyring auth is enough. **Process note** in NEXT-SESSION (machine-local; not promoted to CLAUDE).
- **HN:** no top-level necro updates on old Show HN threads; optional reply under a specific ask only. **AAR only.**

## 2026-08-30 — Science page, feel-axis, v1.13.0, homebrew/core milestone; proper close

Published `/science/` + session-summary URL; ORCID on science/`_config.yml`. Feel-axis → `train`/`calm`/`sleep` (retired `energize`); preset durations kept; midday “Bernardi full dose” claim dropped. Closed #20. Parked GUI as #22 (macOS+Windows only). Shipped **v1.13.0** + Homebrew bump. Opened milestone [homebrew/core](https://github.com/marekkowalczyk/breathe-cli/milestone/1) with #23–#27. First wrap-up was housekeeping-only; user caught the missing proper session-close — this entry completes it. Measured: 77 tests OK; tip `breathe 1.13.0 2026-08-30T21:02`; tag matches; unpushed 0.

**What went well:**
- **Science page as canonical bibliography** stopped README/science citation drift; ORCID attached where it was missing.
- **Feel-axis kept, words fixed** — research-aligned without dropping the model; loud retirement of `energize`.
- **Duration review stayed honest** — kept 10/20/15/20 with rationale instead of citation cosplay.
- **Milestone for homebrew/core** (not one mega-issue) matched one-concern policy; GUI stayed a parked idea.

**What didn't go well:**
- **User correction — science 404:** agent told the user `/science/` was the live URL before `science.md` was committed/pushed.
- **User correction — incomplete close:** asked whether a proper session close had been done; housekeeping AAR/NEXT existed but skill §§4–5/§9 (recurrence, promotion, baton) were skipped until they asked.
- Workspace opened on missing `repos/breathe`; real clone is `breathe-cli`.

**What we'll do differently:**
- **Recurring (2nd):** publish-before-reporting. 2026-08-28 was docs lag until the user asked “are docs up to date?”; today was claiming a Pages URL before push. **Promoted → `CLAUDE.md` § Releases** (no live URL / install claim until tip is on the remote that serves it).
- **Run the session-close skill on wrap-up** (user asked to remember). **Promoted → `CLAUDE.md` § Session close** — housekeeping ship ≠ close; baton pass in chat required.
- Prefer opening `~/repos/breathe-cli` before product work when Cursor root is stale (AAR only — situational).

## 2026-08-28 — Fold private into public breathe-cli; brew path; footer stamp

Folded private `breathe` into public [`breathe-cli`](https://github.com/marekkowalczyk/breathe-cli) (PR #12, LICENSE kept, private product won). Migrated backlog to public #13–#20; archived private repo; local clone retargeted to `~/repos/breathe-cli`. Tagged **v1.11** then **v1.11.1**; Homebrew formula bumped both times. Documented PATH `breathe` (Cellar) vs tip (`python3 breathe.py` / `breathe-dev`). Shipped discreet footer `VERSION · RELEASED`. Filed [#21](https://github.com/marekkowalczyk/breathe-cli/issues/21) (`breathe stats`). Synced README / spec / AAR / tap README after user asked whether docs were current. 69 tests OK; tip matches tag v1.11.1.

**What went well:**
- **Kept public identity for stars:** merge into `breathe-cli` (not rename/delete) preserved community issues and Homebrew URL.
- **Conflict policy locked before merge:** private product + public LICENSE; avoided force-push.
- **Install split written into CLAUDE.md** once brew and tip diverged — agents have an explicit smoke-test rule.

**What didn't go well:**
- **User had to ask “are all docs up to date?”** after the fold and footer ship — README still taught clone/symlink and `INHALE`; tap README still showed `--preset calm`. Product and process docs lagged the ship.
- **Homebrew friction was under-documented at first** (tap trust, link overwrite of an old repo symlink) — fixed in README/CLAUDE only after the user hit the errors.

**What we'll do differently:**
- **After any fold, release, or user-visible TUI/CLI change:** before session close, diff tip against `README.md` and `marekkowalczyk/homebrew-breathe` README (presets, install, display chrome). Do not wait for the user to audit. Promoted to `CLAUDE.md` § Releases.

## 2026-08-28 (morning) — Version string + RELEASED policy; `-v` short flag

Added `-v` for `--version`, then `RELEASED` (minute-precision local datetime) beside
`VERSION` so `breathe -v` prints `breathe {VERSION} {RELEASED}`. Documented keep-both-
current policy in `CLAUDE.md` § Versioning. Filed [#19](https://github.com/marekkowalczyk/breathe-cli/issues/19)
(was private breathe#10 before the fold into public `breathe-cli`)
for a pre-commit hook to stamp `RELEASED` mechanically (`VERSION` stays human). Tests cover
format + `version_string()`.

**What went well:**
- **Scoped the hook as a separate issue** instead of bundling it into the versioning change
  — one-concern policy held.
- **Policy before automation:** CLAUDE.md Versioning is the source of truth; #19 is the
  mechanical follow-through, not a substitute for the rule.

**What didn't go well:**
- Nothing material; short session.

**What we'll do differently:**
- When a value is pure wall-clock stamp, prefer filing an automation issue (#19) over
  relying on recall alone — same disposition ladder as session-close §5.

## 2026-08-28 — Night preset + auto-night (v1.9), GitHub backlog, issue hygiene

Shipped `night` preset (20 min / 3–7, Tsai-style pre-sleep 6 cpm) and `preset_for_hour`
so bare `breathe` auto-selects night for 22:00–05:59 (fixes midnight→morning). Migrated
`TODO.md` to GitHub Issues; strengthened one-concern policy in `CLAUDE.md` after #3 proved
over-scoped; split deferred night UX into private #8/#9 (now public
[#17](https://github.com/marekkowalczyk/breathe-cli/issues/17) dim TUI /
[#18](https://github.com/marekkowalczyk/breathe-cli/issues/18) quiet audio). 59/59 tests
passing. `v1.9` tip was later tagged/released on public `breathe-cli` (and superseded by later releases through v1.11.1).

**What went well:**
- **Science before product:** night ratio/duration locked from Tsai/Laborde evidence before
  coding; only distinct 6 bpm option at stronger E-bias is 3–7.
- **#3 lesson applied quickly:** user flagged over-broad scoping; policy rewritten with
  examples and checklist; #7 split same session instead of letting compound issues linger.
- **Pure helper for auto-select:** `preset_for_hour()` is unit-tested — no wall-clock
  dependency in tests.

**What didn't go well:**
- **#3 was filed as one issue** (preset + auto + dim + audio) — classic “and also” trap;
  close comment alone would have lost deferred work without follow-up #8/#9
  (public #17/#18 after the fold).
- **Accidental #1 test issue** left open from auth probing until backlog hygiene pass.

**What we'll do differently:**
- **One issue = one shippable slice** — promoted to `CLAUDE.md` (loaded every session).
  Split before filing; close umbrellas with pointers. Epics only as design/scoping issues (#6
  reframed).

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
