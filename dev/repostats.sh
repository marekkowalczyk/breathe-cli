#!/usr/bin/env bash
# repostats — pull GitHub metrics for the current repo, output structured
# markdown to stdout.
#
# Usage: repostats
#
# Must be run from inside a git repo with a GitHub remote.
# Requires: gh (GitHub CLI), jq, git
#
# Output is a self-contained markdown section (## YYYY-MM-DD) with a metrics
# table. Designed to be piped, appended, or consumed by other tools.

set -euo pipefail

GH="${GH:-gh}"

# --- Detect repo ---
REMOTE_URL=$(git remote get-url origin 2>/dev/null) || {
  echo "ERROR: Not in a git repo or no 'origin' remote." >&2
  exit 1
}

if [[ "$REMOTE_URL" =~ github\.com[:/]([^/]+)/([^/.]+)(\.git)?$ ]]; then
  OWNER="${BASH_REMATCH[1]}"
  REPO="${BASH_REMATCH[2]}"
else
  echo "ERROR: Could not parse GitHub owner/repo from: $REMOTE_URL" >&2
  exit 1
fi

FULL_REPO="$OWNER/$REPO"

# --- Pull data (repo, issues, PRs) ---
REPO_JSON=$($GH api "repos/$FULL_REPO" 2>/dev/null) || {
  echo "ERROR: gh api call failed. Are you authenticated?" >&2
  exit 1
}

ISSUES_JSON=$($GH issue list --repo "$FULL_REPO" --state all --limit 1000 \
  --json state --jq 'group_by(.state) | map({(.[0].state): length}) | add // {}' 2>/dev/null) || ISSUES_JSON='{}'

PRS_JSON=$($GH pr list --repo "$FULL_REPO" --state all --limit 1000 \
  --json state --jq 'group_by(.state) | map({(.[0].state): length}) | add // {}' 2>/dev/null) || PRS_JSON='{}'

# --- Extract fields ---
STARS=$(echo "$REPO_JSON" | jq -r '.stargazers_count')
FORKS=$(echo "$REPO_JSON" | jq -r '.forks_count')
SUBSCRIBERS=$(echo "$REPO_JSON" | jq -r '.subscribers_count')
LANGUAGE=$(echo "$REPO_JSON" | jq -r '.language // "n/a"')
LICENSE=$(echo "$REPO_JSON" | jq -r '.license.spdx_id // "n/a"')
CREATED=$(echo "$REPO_JSON" | jq -r '.created_at' | cut -dT -f1)
PUSHED=$(echo "$REPO_JSON" | jq -r '.pushed_at' | cut -dT -f1)
DESCRIPTION=$(echo "$REPO_JSON" | jq -r '.description // "n/a"')
TOPICS=$(echo "$REPO_JSON" | jq -r '(.topics // []) | join(", ")')

ISSUES_OPEN=$(echo "$ISSUES_JSON" | jq -r '.OPEN // 0')
ISSUES_CLOSED=$(echo "$ISSUES_JSON" | jq -r '.CLOSED // 0')
PRS_OPEN=$(echo "$PRS_JSON" | jq -r '.OPEN // 0')
PRS_MERGED=$(echo "$PRS_JSON" | jq -r '.MERGED // 0')
PRS_CLOSED=$(echo "$PRS_JSON" | jq -r '.CLOSED // 0')

TODAY=$(date +%Y-%m-%d)

# --- Output structured markdown ---
cat <<EOF
## $TODAY — $FULL_REPO

> $DESCRIPTION

| Metric | Value |
|---|---|
| Stars | $STARS |
| Forks | $FORKS |
| Open issues | $ISSUES_OPEN |
| Closed issues | $ISSUES_CLOSED |
| Open PRs | $PRS_OPEN |
| Merged PRs | $PRS_MERGED |
| Closed PRs | $PRS_CLOSED |
| Subscribers | $SUBSCRIBERS |
| Language | $LANGUAGE |
| License | $LICENSE |
| Created | $CREATED |
| Last push | $PUSHED |

**Topics:** $TOPICS
EOF
