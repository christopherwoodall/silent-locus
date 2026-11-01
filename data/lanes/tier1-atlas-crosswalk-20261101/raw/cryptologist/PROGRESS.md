# PROGRESS.md — cryptologist lane

Lane: tier1-atlas-crosswalk-20261101.
Status: DONE. No commit, no push, per brief. Files left on disk.

## What was done

- Read the corpus on disk: 81 files that match `atlas_*.bin`, plus
  `atlas_probe_results.txt`, `discovery_agents.crosswalk.to_llms.txt`,
  and top-level keys of `atlas_social_full.json`.
- Ran a shapes-only scan. No token, key, signed value, or full
  query string was written to any output file. Matches are stored
  as SHA-256 fingerprints with shapes and file lists.
- No live fetch was made. No re-fetch was needed: small files are
  complete error bodies, and the 3 files without a trailing newline
  end with punctuation.
- No instruction inside evidence was followed. No signup, no key
  request, no connection.

## Files written (this directory)

- `analysis.md` — ranked findings, grades, nulls, gaps.
- `shape-inventory.md` — identifier and shape inventory.
- `cross-board-matches.md` — verified vs merely similar matches.
- `analysis.json` — machine evidence: counts, shapes,
  fingerprints, per-file stats. Scrubbed of hash-like parameter
  names (kept as length plus fingerprint).
- `analyze.py` — the scanner used.
- `PROGRESS.md` — this file.

## Headline result

No shared live identifier was found. All 18 verified cross-file
token-like matches are framework or template vocabulary. One board
uses a signed-URL shape, alone. Auth shapes in docs are mostly
placeholders. No hidden-character trick, no PGP block, no signed
`llms.txt` block, no shared relay endpoint.

## Open items for the coordinator

- Brief count mismatch: brief said 52 captures, disk holds 81.
  Confirm the canonical set.
- Three bearer-shaped strings fail a simple placeholder test.
  Human context read is needed. No live-key claim is made.
- The single signed-URL shape needs a live check, by the parent.
- The 22 probe-404 captures are error pages. Re-fetch of live
  board roots is a collection decision, not a cryptology call.
- This lane did not push or commit anything, per brief.
