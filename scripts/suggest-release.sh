#!/usr/bin/env bash
# Suggest a GitHub tag+release when breathe.py VERSION is ahead of the latest v* tag.
# Suggestion only — never tags or creates a release. Always exits 0.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

VERSION="$(sed -n "s/^VERSION = '\\(.*\\)'$/\\1/p" breathe.py | head -n 1)"
if [[ -z "$VERSION" ]]; then
  echo "suggest-release: could not read VERSION from breathe.py" >&2
  exit 0
fi

LATEST_TAG="$(git tag -l 'v*' --sort=-v:refname | head -n 1 || true)"
if [[ -z "$LATEST_TAG" ]]; then
  echo "Release due: VERSION is $VERSION; no v* tags found."
  echo "  Suggest (after user authorizes a release):"
  echo "    git tag \"v${VERSION}\" && git push origin \"v${VERSION}\""
  echo "    gh release create \"v${VERSION}\" --title \"v${VERSION}\" --generate-notes"
  exit 0
fi

LATEST_VER="${LATEST_TAG#v}"

if [[ "$VERSION" == "$LATEST_VER" ]]; then
  echo "Nothing to release: VERSION $VERSION matches tag $LATEST_TAG."
  exit 0
fi

# sort -V: highest version last
HIGHER="$(printf '%s\n%s\n' "$LATEST_VER" "$VERSION" | sort -V | tail -n 1)"

if [[ "$HIGHER" == "$VERSION" ]]; then
  echo "Release due: VERSION $VERSION is ahead of latest tag $LATEST_TAG."
  echo "  Suggest (after user authorizes a release):"
  echo "    git tag \"v${VERSION}\" && git push origin \"v${VERSION}\""
  echo "    gh release create \"v${VERSION}\" --title \"v${VERSION}\" --generate-notes"
  exit 0
fi

echo "Nothing to release: latest tag $LATEST_TAG is ahead of VERSION $VERSION (check VERSION bump)."
exit 0
