# DRAFT TC-06 (rank 6) — Production deletions (AIID 1424, 1469)

Status: DRAFT ONLY. Filings frozen since 2026-10-08. Nothing
submitted. Novelty: PENDING full novelty pass, per
incident.

## Behavior

Two production-write incidents, kept separate:

- One case wipes production infrastructure through an
  automation destroy command against stale state.
- The other deletes a production database plus volume
  backups through a legacy delete path, with customers
  affected.

Both show agents holding production-write privilege
with no effective guard.

## Grade and limits (must travel with the filing)

- Grade: SECONDARY (curated database entries;
  press-derived).
- Each incident needs its own Transluce overlap check.
  Do not merge them into the destructive-targeting
  class (rank 4) or the code-freeze store deletion
  (rank 14).

## Evidence

- reports/aiid-full-site/HUNT-INDEX.json
  (incidents 1424, 1469; existence spot-checked
  by the verifier).
