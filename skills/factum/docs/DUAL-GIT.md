# Absorbed Factum: upstream tracking and local shaping

This document covers the workflow when Factum is absorbed into a host
repository (not a nested clone or submodule) and shaped for local needs
while tracking the upstream project.

## The setup

Two Git locations are in play:

| Location | Purpose |
|---|---|
| Upstream `christopherwoodall/factum` | Canonical Factum source. Read-only for shaping work. |
| Host branch `factum` | Absorbed copy of Factum plus local shaping edits. |

The absorbed copy means the skill's files live directly in the host
repository (e.g. `skills/factum/`). There is no nested `.git`, no submodule
pointer. Diffs are visible in normal host pull requests.

Historical note: shaping previously lived on a separate `factum-shaping`
branch rebased onto a pristine `factum` branch. `factum-shaping` was merged
into `factum` and deleted; there is no pristine/shaping split anymore.
Branch history prior to the merge is preserved in the `factum` branch.

## Why absorb instead of clone or submodule

- **Visible diffs.** Shaping edits show up as normal file diffs in host PRs.
- **Single push.** One `git push` carries skill and corpus changes together.
- **No submodule ceremony.** Other checkouts get the code with a plain clone.

The cost: upstream updates are manual (see below). Do not absorb if the
host needs to track upstream closely with minimal effort — use the
submodule mode from INSTALL.md instead.

## Pulling upstream changes

1. Fetch upstream into a scratch location (do not disturb the absorbed copy):

```bash
git fetch https://github.com/christopherwoodall/factum.git main
```

2. Diff upstream against the host `factum` branch to see what changed:

```bash
git diff factum FETCH_HEAD -- skills/factum/
```

3. Apply the upstream changes on a feature branch off `factum`:

```bash
git checkout -b factum-upstream-sync factum
# Apply upstream changes to skills/factum/ (patch, checkout, or manual merge)
git commit -m "factum: sync to upstream <revision>"
```

4. Push the feature branch and merge it into `factum` through the host's
   normal PR process.

Resolve conflicts in favor of deliberate shaping edits; do not silently
drop upstream fixes.

## Applying shaping changes

Work on a feature branch off `factum`. Commit normally. Push the branch for
review. The host's normal PR process applies.

### Contributing back upstream

Shaping edits that are generally useful belong upstream:

1. Isolate the change on a clean fork/branch containing only the change,
   following that repository's contribution rules.
2. Open a PR against `christopherwoodall/factum`.
3. Once merged upstream, sync (above) and drop the local copy of the change
   if upstream accepted it as-is.

Never push host-specific content (local packs, host paths, credentials)
to upstream.

## Rules

- Shaping edits live on `factum` or feature branches off it. There is no
  separate pristine branch.
- Upstream syncs are manual; review the upstream diff before applying.
- Review the shaping diff before merging — it is the complete list of
  local deviations from upstream.
- Keep credentials out of all locations. Remotes use the host's normal
  credential handling, never embedded tokens.
