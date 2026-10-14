# Self-Modifier Swarm — Guardrails

**Status:** BUILT, NOT ACTIVATED. Requires BigSexyWarlock69's explicit approval before the cron goes live.

**Purpose:** An autonomous agent that reads error reports from the scanner
infrastructure, fixes bugs slowly and carefully, and proposes enhancements —
without waiting for human prompts.

---

## What it monitors

1. `scripts/scanners/state/error-log.jsonl` — structured errors from all
   scanner modules (via `C.report_error()`)
2. Cron job run outputs — lane failures, timeouts, exceptions
3. Factum ingest rejections — records that failed validation
4. Performance signals — runs exceeding timeout, repeated rate-limit hits

## What it MAY do (autonomous)

- Fix **crashes**: unhandled exceptions, import errors, `None`-dereferences
  where the fix is obvious and minimal (null check, try/except, default value)
- Fix **broken parsing**: regex that no longer matches a changed page format,
  JSON key renames in an API response — when the correct new pattern is
  evident from the error output
- Fix **stale selectors**: CSS/XPath/JSON paths that broke due to upstream
  changes, when the replacement is unambiguous
- **Performance**: add caching where a repeated expensive call is the clear
  bottleneck; reduce redundant API calls
- **Dead code removal**: delete code paths for lanes BigSexyWarlock69 has
  already ordered cut (with the order cited in the commit message)
- **Documentation**: update README/comments to match actual behavior

## What it MAY NOT do (hard boundaries)

- **Never break the factum ingest contract.** Every scanner must keep
  emitting valid factum records. Any change to hit dict shape, bundle
  format, or grading logic goes to the review queue, never auto-applied.
- **Never widen scope.** No new network targets, no new API endpoints,
  no new data exfiltration paths, no new credentials or auth flows.
  A fix that requires talking to a new host is NOT a fix — it's a
  proposal.
- **Never touch counsel verdicts.** Rules cut or demoted by linguist /
  cryptologist / adversarial review (documented in COUNSEL-REVIEW-*.md
  and the morning cron body) stay cut. Re-enabling a cut rule requires
  BigSexyWarlock69's explicit order, not a self-modifier decision.
- **Never modify** `swarm-infra-config.json` detection patterns (IP ranges,
  tag grammars, fingerprints) autonomously. Config changes are proposals.
- **Never touch** the `work`/`main` branch topology. All changes on `work`.
  Never merge, never push to `main`.
- **Never delete** state files, error logs, or evidence. Append-only for
  logs; state mutations only through the established temp-file+rename
  pattern.
- **Never bypass** rate limits. If a fix involves retry logic, it must
  respect the existing backoff and never retry a 429.

## Operating rules

1. **One change per run.** The agent picks the single highest-priority
   error, fixes it, verifies, commits. Then stops. Slow is safe.
2. **Each change committed separately** with a message in this format:
   ```
   self-mod: <module> — <what was broken> → <what changed>

   Error: <error_type> from error-log.jsonl (hash <tb_hash>)
   Rationale: <1-2 sentences on why this fix is correct>
   Verified: <how it was tested>
   ```
3. **Uncertain fixes go to the review queue**, not into code:
   `scripts/scanners/state/proposed-changes/YYYY-MM-DD-<slug>.md`
   Each proposal has: problem, proposed fix, why uncertain, what would
   resolve the uncertainty.
4. **Verify before committing.** Run the affected module's dry-run mode
   (`--dry-run`) after the fix. If no dry-run exists, at minimum
   `python3 -c "import <module>"` must succeed.
5. **If the error log is empty**, the agent may spend the run on a
   single enhancement from its own ideas — subject to the same
   MAY/MAY-NOT boundaries. Enhancements are held to a higher bar:
   when in doubt, propose rather than apply.
6. **Never fix the same traceback_hash twice** in one run. If a fix
   doesn't resolve the error, that's signal — propose, don't iterate.

## Priority order

1. Crashes (scanner dies → no data)
2. Wrong results (scanner runs but emits garbage → bad data)
3. Factum ingest rejections (data collected but not stored → lost data)
4. Performance (slow but correct → delayed data)
5. Enhancements (working fine → could be better)

## Kill switch

BigSexyWarlock69 can stop the self-modifier at any time by:
- Disabling the cron job, OR
- Creating the file `scripts/scanners/state/SELF-MOD-DISABLED`
  (the agent checks for this file first and exits immediately if present)

## Review queue format

`scripts/scanners/state/proposed-changes/YYYY-MM-DD-<slug>.md`:
```markdown
# Proposed: <title>
**Date:** YYYY-MM-DD
**Module:** <module>
**Error hash:** <tb_hash> (or "enhancement")

## Problem
<what's wrong or what could be better>

## Proposed fix
<exact change, with diff if possible>

## Why uncertain
<what could go wrong, what assumption might be false>

## What would resolve it
<what evidence or decision is needed>
```
