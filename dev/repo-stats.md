# Repo Stats

Pull GitHub repository metrics, compare with historical data, and log a snapshot.

## Instructions

### 1. Get today's data (deterministic)

Run `repostats` (assumes installed in PATH) from the repo root:

```bash
repostats > /tmp/repostats-today.md
```

Show the output to the user.

### 2. Compare with history (LLM)

Check if `dev/github-metrics.md` exists in the repo.

- **If it exists:** read the most recent entry (the first `## YYYY-MM-DD` section). Compare it with today's data from `/tmp/repostats-today.md`. Write a short `**Notes:**` line (1-2 sentences) highlighting deltas and trends. Example: "+75 stars, +3 forks in 3 days. Star-to-fork ratio stable at ~24:1."
- **If it doesn't exist:** write a `**Notes:**` line marking this as the first snapshot. Example: "First recorded snapshot."

### 3. Assemble and write (deterministic)

Append the `**Notes:**` line to `/tmp/repostats-today.md`. Then:

**If `dev/github-metrics.md` exists** — prepend today's entry after the file header:

```bash
# Find where the first ## entry starts, insert before it
HEADER_END=$(grep -n "^## " dev/github-metrics.md | head -1 | cut -d: -f1)
if [ -n "$HEADER_END" ]; then
  head -n $((HEADER_END - 1)) dev/github-metrics.md > /tmp/repostats-assembled.md
  echo "" >> /tmp/repostats-assembled.md
  cat /tmp/repostats-today.md >> /tmp/repostats-assembled.md
  echo "" >> /tmp/repostats-assembled.md
  tail -n +"$HEADER_END" dev/github-metrics.md >> /tmp/repostats-assembled.md
  mv /tmp/repostats-assembled.md dev/github-metrics.md
fi
```

**If `dev/github-metrics.md` doesn't exist** — create it:

```bash
cat > dev/github-metrics.md <<HEADER
# GitHub Metrics

Periodic snapshots of repo traction. Newest first.

HEADER
cat /tmp/repostats-today.md >> dev/github-metrics.md
```

### 4. Commit

```bash
git add dev/github-metrics.md
git commit -m "Add GitHub metrics snapshot YYYY-MM-DD"
```

### 5. Clean up

```bash
rm -f /tmp/repostats-today.md /tmp/repostats-assembled.md
```
