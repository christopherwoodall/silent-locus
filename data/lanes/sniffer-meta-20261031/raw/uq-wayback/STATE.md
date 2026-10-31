# STATE — URLQUERY/WAYBACK lane, sniffer-meta-20261031

Status: COMPLETE, 2026-10-31 (America/Chicago). All five objectives done.
No commit, no push, no Factum writes — coordinator commits.

## Done

1. Full da.gd pull: 98/98 rows saved, 98 unique IDs.
   Burst verdict: SURVIVES. May 53 + June 31 = 84/98.
   June 21 cluster: 17 in the full set (same as saved-30).
   New: May 19 is the largest day (19 rows, 19:08-21:48 UTC).
   zz 0/98, oai 0/98. Short-code reuse: 15 codes repeat, PQkCp 9.
2. zz flagged row: RESOLVED. Sweep-time conj file has exactly 1 flagged
   row (2026-10-31, truedating.life, root path, tags empty).
   Targeted report re-fetch: flag is in the FINAL redirect landing URL's
   query string (zz= present, value withheld); submitted URL has no
   query and no zz. Redirect-tracking artifact, not agent evidence.
   Fresh re-run of the conj query: total 68260, 0 flagged in new top 30.
3. Bounded T/Z probe: HN Algolia 4/1/7 hits, 0 literal T/Z in text.
   urlquery "T/Z" agent 20996, "T/Z" harness 20070, generic noise on top.
   Verdict: untestable at this scope, stopped, no callsign claim.
4. CDX retry (one round, port 80): domain query SUCCEEDED (HTTP 200,
   50 rows, 47x302, zz 0, oai 0, urlkey-ordered slice — not a burst
   census). zz-filter query FAILED (HTTP 504, no retry beyond the one).
5. No echo-page fetches, no payload decodes (cryptologist lane's job).

## Caveats for the coordinator

- urlquery totals drift between runs (68265 -> 68260); treat counts as
  retrieval-time snapshots.
- CDX 50-row slice must not be cited as a burst distribution.
- Grade throughout: SECONDARY pattern shape only. No behavior verified.
- Task instruction (stage-only, no Factum writes) was followed over the
  repo AGENTS.md Factum default, as in the prior sweep lanes; ingest,
  if any, is the coordinator's call.
