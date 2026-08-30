#!/usr/bin/env bash
# Fail if breathe.py VERSION and pyproject.toml version disagree.
# Used by the PyPI publish workflow and before local releases.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PY_VER="$(sed -n "s/^VERSION = '\\(.*\\)'$/\\1/p" breathe.py | head -n 1)"
TOML_VER="$(sed -n 's/^version = "\(.*\)"$/\1/p' pyproject.toml | head -n 1)"

if [[ -z "$PY_VER" ]]; then
  echo "check-version-sync: could not read VERSION from breathe.py" >&2
  exit 1
fi
if [[ -z "$TOML_VER" ]]; then
  echo "check-version-sync: could not read version from pyproject.toml" >&2
  exit 1
fi

if [[ "$PY_VER" != "$TOML_VER" ]]; then
  echo "check-version-sync: mismatch — breathe.py VERSION='$PY_VER' vs pyproject.toml version='$TOML_VER'" >&2
  echo "  Bump both to the same value before tagging / releasing." >&2
  exit 1
fi

echo "check-version-sync: OK ($PY_VER)"
