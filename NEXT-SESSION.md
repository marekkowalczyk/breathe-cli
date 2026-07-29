# Next Session

Installed on this machine: `breathe` symlinked at `/opt/homebrew/bin/breathe` → repo's `breathe.py`, so `git pull` updates the installed command with no reinstall step.

Decided and closed: bare `breathe`'s time-of-day auto-preset selection stays as-is (see AAR 2026-07-29). Don't relitigate without a concrete usage complaint.

## Open items

- **Session progress bar — cycle count** (TODO #8) — time-based bar (#4) is done. This one tracks completed breath cycles. Watch the 700-line cap (currently 688 lines).
- **Breathing modes beyond vagal tone** (TODO #14) — significant architectural change; scope out before starting. Single-file constraint may be the binding limit.
