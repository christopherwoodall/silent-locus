# PROVENANCE — data/2026-05-11-july6-staging/

Lane P: July-6 staging check for the SwarmTraces agent-hunt (2026-09-28, ~03:55 CDT).

## Question
July-7 XSS/SSTI gem wave (215 pkgs / 333 releases, 2026-07-07 03:03:09Z–18:13:42Z) is the
fourth dated run in the ~17-day series (May 12, May 29, June 18, July 7). Every prior run
was preceded ~48h by a staging signature. Is there a July 5–6 staging signature?

## Sources (all read-only; nothing submitted, fetched live, or executed)
| # | Source | Retrieval date | What was read | SHA-256 |
|---|--------|----------------|---------------|---------|
| 1 | data/2026-05-17-collusion-wiki/raw/events.jsonl.gz (frozen lane export, in-repo) | 2026-09-28 | 318 delete events 2026-07-05/06; per-day/window recomputed locally | see repo SHA256SUMS |
| 2 | data/2026-05-17-collusion-wiki/raw/revisions.jsonl.gz (in-repo) | 2026-09-28 | creation revisions of forward-named pages (June-18 timestamps) | see repo SHA256SUMS |
| 3 | data/2021-10-30-demowiki/raw/demowiki_crawl.json (in-repo) | 2026-09-28 | substring scan for July dates (zero) | n/a |
| 4 | data/2016-12-28-rmn-re-history/raw/slug_evolution.jsonl (in-repo) | 2026-09-28 | July slug creation dates; grammars | n/a |
| 5 | ES index collusion-wiki (read-only _search) | 2026-09-28 | 318 docs @timestamp 2026-07-05..07; cross-check of file counts | n/a (remote) |
| 6 | ES index rubygems-goimport-campaign | 2026-09-28 | 0 docs July 5–6; 250 docs May 10–11 (wave=may-12) | n/a (remote) |
| 7 | ES index july7-wave | 2026-09-28 | 0 docs July 5–6 (9 wave docs all July 7) | n/a (remote) |
| 8 | ES index timeline-anchors | 2026-09-28 | 0 docs July 5–6; comparator anchors (June 16, May 27) | n/a (remote) |
| 9 | ES index proxy-primitives | 2026-09-28 | 0 docs published_at July 4–8 | n/a (remote) |
| 10 | ES index webhook-deaddrops, gem83-reconciliation, iowacollab-pastes | 2026-09-28 | 0 docs July 5–6; iowa dated doc = June 16 wave | n/a (remote) |
| 11 | ES index ludism-wikis | 2026-09-28 | 31 docs, none July | n/a (remote) |
| 12 | data/2026-09-28-university-shorteners/events.jsonl | 2026-09-28 | 7 summary docs, no per-day July breakdown | n/a |
| 13 | data/2018-05-09-paste-archive-gap/*.jsonl | 2026-09-28 | no July 5–6 references | n/a |

## Corpus dates
- Corpus window: 2026-03-07 → 2026-09-14. Swarm run dates in UTC.

## Verdict
NOT EMPTY. July 5–6 staging signal = the dse wiki admin's 318-page deletion sweep
(239 on July 5, 79 on July 6), removing agent-created SEC/county/bridge pages from the
June-18 era — venue hygiene immediately before the July-7 wave. Seven deleted pages
carried forward-looking July/Oct names; four have confirmed June-18 creation revisions.
Every other surface (wiki writes, shorteners, proxy toolkit, registry, comms) is a NULL
read in the window — recorded, not filled.

## Files
- hits.jsonl — 11 records (2 staging_signal, 1 venue-preclaim, 5 null_read, 3 comparator)
- manifest.sha256 — SHA-256 of hits.jsonl
- progress.log — lane log
- PROVENANCE.md — this file

## Closure 2026-09-28 (workstream D)

Bounded question answered: July 5–6 staging signal for the July-7 wave.
N=11 docs (2 staging_signal + 1 venue-preclaim + 5 null_read + 3 comparator)
is the complete cross-surface check — every named surface swept, one verdict
each. ES `july6-staging` _count=11 verified. **Theory update (lane R):** the
July 5–6 admin deletion sweep is mid-campaign hygiene, NOT a pre-run staging
modality — this lane's "staging signal" verdict is superseded by
notes/admin-deletions-2026-09-28.md; kept as evidence of the check, not the
interpretation. The lane-P follow-up (July 5–6 per-day referrer rows on
goto.unm.edu) was closed by C3 as structurally impossible — YOURLS public
stats have no per-day-per-referrer endpoint
(notes/workstream-c3-2026-09-28.md).

## Schema backfill 2026-09-29

`hits.jsonl` was already schema-shaped; `temp/backfill_w3.py` only added the
missing fingerprint.

- record_kind: `staging_signal` (pre-existing, kept verbatim).
- fingerprint: sha256 of `labels.doc_id`.
- @timestamp, event, labels, and all other fields preserved verbatim.
