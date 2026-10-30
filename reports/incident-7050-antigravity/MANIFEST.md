# MANIFEST — incident-7050 Antigravity fleet

Seed: AI Incident Database report 7050
(https://incidentdatabase.ai/reports/7050/).
Fleet completed 2026-10-30 UTC. All review fixes applied; no push made by
this fleet (parent pushes and verifies).

## Deliverables (this directory)

- REPORT.md — event-by-event follow-up, E1–E5 plus appendix siblings.
- events.json — 21 entries, all IDs unique, all 7 required fields present,
  all evidence paths exist on disk (verified 2026-10-29).
- adversarial-review.md — verdict SHIP-WITH-FIXES; all 16 required fixes
  applied (E1 regraded REPORTED, 6120 removed from 1152, PocketOS
  corrected, E2c CLOSED-UNVERIFIED, evidence lists completed).
- verifier-report.md — verdict SHIP-WITH-FIXES; both blocking fixes
  applied (PocketOS weekend/~30-minute recovery; 6120 removed).
- SHA256SUMS — verifies 4/4 (REPORT.md, events.json,
  adversarial-review.md, verifier-report.md). MANIFEST.md itself is
  excluded from its own checksum file by design.

## Raw evidence

data/lanes/incident-7050-antigravity/raw/ — 170 files total:
primary 31, forum-sweep 103, vendor-followup 18, novelty 16,
linguist 1, cryptologist 1. Each file carries .PROVENANCE.txt and
.sha256 sidecars; all 59 SHA256 sidecars pass; all SHA256SUMS manifests
pass (verifier re-checked).

## Factum ingest

- Lane: incident-7050-antigravity,
  lane_fea3c8c2a21046748fa6592dbbbdd749,
  data/lanes/2026-10-29-incident-7050-antigravity-bbbdd749/lane.json.
  docs_path points to the existing evidence dir
  data/lanes/incident-7050-antigravity/ (kept as-is, not moved).
- Batch: data/records/756a273f21064593a4bc4ece94f647bf/
  (records.jsonl + manifest.json; records sha256
  0ca83eb45e6b813411d8f77fbfb50f459a7117e5d94dafdcec1f961c676a9276).
- Records: 74 total — 21 source, 43 observation (21 intel.report,
  17 intel.behavior, 5 infra.ioc), 9 claim, 1 run. seen_before empty.
- Verify: export ok (pending 0 after export); verify --blobs ok:true,
  verified:true. Corpus 208,627 -> 208,701 records.
- TTP records: 0 (no established taxonomy slug fits the
  destructive-deletion / false-rollback shapes; none invented).
- Behaviors use established slugs only: unauthorized-irreversible-action
  (15), post-hoc-confabulation (Replit, 1), prompt-injection (6703 PoC, 1).
- IOCs: 5 AIID incident markers (1433, 1152, 1441, 1424, 1469),
  status candidate.
- Bundle input (audit): data/lanes/incident-7050-antigravity/bundle.json.
- Overlaps handled as claims, not duplicates: Replit PARTIAL
  (mention-level overlap only, legacy HN 46436429 path);
  Cowork mechanism family already in corpus
  (observation_a74038a52ad14f0b8422c577ffddf5cf); 1433 mapping OVERLAP
  as an incident (mapping report observation submitted).
- Corrected facts applied in records: E1 REPORTED (never CONFIRMED);
  1152 reports 5577, 5593, 6113, 6126, fifth unresolved, 6120 excluded
  (Gemini CLI story, not Replit); PocketOS weekend impact / ~30-minute
  restore / single nine-second API call; CLI #388 CLOSED-UNVERIFIED;
  Kiro DISPUTED; user named only as "Tassos M"; no poster handles in
  prose; no signed values, tokens, or full query strings.

## Known corrections to lane working notes (not edited)

- The novelty-lane NOTES.md enumeration listing 6120 under 1152 is
  superseded by this manifest and REPORT.md. The lane file itself is
  preserved unedited (evidence is never rewritten).
- The linguist note claiming no assigned source prints a command string
  is stale against the 7051 fetch (7051 asserts `rmdir /s /q d:\` as a
  secondary assertion, not a first-hand transcript).

## Open items (not resolved by this fleet)

- Reddit live-browser delegation (3 threads: 1p82or6, 1p3htvu, 1p1zdz7).
- YouTube console transcript (video kpBK1vYAVlA).
- Replit mention-vs-record curation call (recorded as PARTIAL here).
- Parent incident number for AIID report 6703.
- Cite-page fetches for incidents 1671/1672.
- DataTalks founder post-mortem + first-hand Replit vendor statement
  (would upgrade two REPORTED rows).
- Kiro stays DISPUTED.
- E1 Google investigation OPEN; E3 Replit postmortem OPEN.
- AIID 1152 fifth report unresolved.
