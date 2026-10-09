# Operating dual Git: upstream Factum and host shaping branches

This document covers the workflow when Factum is absorbed into a host
repository (not a nested clone or submodule) and shaped for local needs
while tracking the upstream project.

## The setup

Three Git locations are in play:

| Location | Purpose |
|---|---|
| Upstream `christopherwoodall/factum` | Canonical Factum source. Read-only for shaping work. |
| Host branch `factum` | Pristine absorbed copy of upstream at a known revision. Never edit directly. |
| Host branch `factum-shaping` (or similar) | Local edits, fixes, and packs. Branched from `factum`. |

The absorbed copy means the skill's files live directly in the host
repository (e.g. `skills/factum/`). There is no nested `.git`, no submodule
pointer. Diffs are visible in normal host pull requests.

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

2. Diff upstream against the pristine `factum` branch to see what changed:

```bash
git diff factum FETCH_HEAD -- skills/factum/
```

3. Update the pristine branch first:

```bash
git checkout factum
# Apply upstream changes to skills/factum/ (patch, checkout, or manual merge)
git commit -m "factum: sync to upstream <revision>"
```

4. Rebase the shaping branch onto the updated pristine branch:

```bash
git checkout factum-shaping
git rebase factum
```

Resolve conflicts in favor of deliberate shaping edits; do not silently
drop upstream fixes.

## Applying shaping changes

### Within the host

Work on `factum-shaping` (or a feature branch off it). Commit normally.
Push the branch for review. The host's normal PR process applies.

### Contributing back upstream

Shaping edits that are generally useful belong upstream:

1. Isolate the change: `git diff factum factum-shaping -- skills/factum/`.
2. Check the change against upstream `main` — it may have moved.
3. Open a PR against `christopherwoodall/factum` from a clean fork/branch
   containing only the change, following that repository's contribution
   rules.
4. Once merged upstream, sync the pristine `factum` branch (above) and
   rebase shaping. Drop the local copy of the change if upstream accepted
   it as-is.

Never push host-specific content (local packs, host paths, credentials)
to upstream.

## Rules

- The `factum` branch is pristine. No edits except upstream syncs.
- Shaping edits live on `factum-shaping` or feature branches off it.
- Upstream syncs rebase shaping; shaping never rewrites `factum` history.
- Review the `factum`..`factum-shaping` diff before merging shaping
  anywhere — it is the complete list of local deviations.
- Keep credentials out of all three locations. Remotes use the host's
  normal credential handling, never embedded tokens.
