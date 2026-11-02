# DarkSwarm ingest — progress

Lane tag: darkswarm-20261101 (TAG-ONLY grouping; no lane object created).
Actor: agent:darkswarm-lane-ingest.
Batch idempotency key: darkswarm-20261101-ingest-v1.

## Inputs read

- work/linguist/CLAIMS.md — 94 claims (OBSERVED 7, REPORTED 81, INFERENCE 6).
- work/adversarial/REVIEW.md — KILL 6, DOWNGRADE 81, STAND 7. Top-20: 0 STAND.
- work/verifier/VERIFICATION.md — assessed 41: VERIFIED 3, PARTIAL 8, CONTRADICTED 0, UNCHECKABLE 30.
- work/crypto/ANALYSIS.md — Distill ledger verdicts, Toro verdicts.
- work/novelty/NOVELTY.md — NEW 6, OVERLAP 4 (surface-only), PENDING 0.
- work/capture/STATUS.md — SauersML/DarkSwarm main HEAD be21462916e9f94ee7ff2ad48eb6c82b92d1617e, 51/51 sha256-verified.

## Pre-submit checks

- factum status: ok:true, initialized, 132 lanes, 225908 records, pending 0, stale false. No malformed lane.json error.
- Collision check: grep over data/records/*/records.jsonl found ZERO records carrying tags.lane=darkswarm-20261101. No data/lanes/darkswarm-20261101/lane.json exists (lane dir holds raw/ + work/ only). Proceeding TAG-ONLY.
- Schema: factum-core claim basis enum is OBSERVED / UPSTREAM / INFERENCE (no REPORTED value). Mapping used: linguist REPORTED -> claim body.basis UPSTREAM (secondary report) with tags.grade="REPORTED" verbatim; linguist INFERENCE -> basis INFERENCE; STAND -> basis OBSERVED. Observation type intel.report (factum-intel) inside body, per schema assigned check.
- Dedup within batch: key field claim_id, unique across the 88 ingested claims (asserted by generator). Cross-corpus: novelty lane ran Factum fuzzy subject checks 2026-11-01 (same corpus commit ff08820); ingester re-runs subject-level fuzzy matches (see below) plus the exported-records grep above.

## Counts planned

- KILLED, excluded entirely (6): C63, C16, C28, C41, C57, C89.
- STAND ingested as basis OBSERVED (7): C01, C02, C03, C44, C55, C92, C93.
- DOWNGRADED ingested with exact adversarial caveat in body.note AND tags.adversarial_caveat (81).
- Total claim records: 88. Plus 1 source record + 1 intel.report observation = 90 records in ONE bundle.
- Verification tags: VERIFIED 3 (C09, C58, C60 — still DOWNGRADED per adversarial review), PARTIAL 8 (C08, C10, C11, C13, C14, C18, C29, C69), UNCHECKABLE 29 ingested (verifier). NOT_ASSESSED by the verifier: 48 claims incl. all 7 STAND. Of those 48, 3 carry crypto-lane verdicts (C40 PARTLY, C42 UNCHECKABLE, C43 PARTLY); 45 carry no lane verification at all.
- NOTE: C40/C42/C43 were not in the verifier's 41; their verification tags come from the crypto lane.

## Dedup (ingester-run)

- Within batch: claim_id unique across 88 (generator assert); claim sentences unique; zero killed-claim text present.
- Exported-records grep for tags.lane=darkswarm-20261101: 0 hits.
- Fuzzy matches run per subject (Synapolis, MoltBunker, musebook, dumate-scout, Distill, Toro, Montelibero, Stellar, PikaSim, Pitch, chuanmen, Lizzie, FlapJax, The Colony, onion): returned matches are heuristic neighbors (AIID records etc.), none a DarkSwarm claim duplicate.
- Distinctive-phrase fuzzy checks (MuseMayor, Faith flock, 15-minute cycle, 162406, 99 TB, dumate-scout, lynxshell, Synapolis, MoltBunker, TV####): zero literal hits in returned match output.
- Consistent with novelty lane's relevance-checked Factum checks (same corpus commit ff08820): only surface overlap (The Colony, onion) — surfaces, not these claim texts.
- SKIPPED OVERLAPS: 0. Nothing skipped.

## Schema check

- `schema assigned observation intel.report` -> ok:true, urn:factum:intel:report:1.
- `schema assigned claim` is not a valid CLI category (observable/observation/event/predicate only) — expected usage error, not a blocker. Claims use core claim schema urn:factum:core:claim:1 per corpus precedent.
- Basis mapping (Factum enum has no REPORTED): linguist REPORTED -> body.basis UPSTREAM + tags.grade="REPORTED" verbatim; INFERENCE -> INFERENCE; STAND -> OBSERVED. No grade was paraphrased away.

## Submission — DONE

- add: ok:true, batch_id 8b87915d91ce4e7284fbbfdb1ad60f60, durability pending, 91 ids (90 bundle records + 1 local-storage artifact), seen_before empty, errors None.
  - source source_b0e103f3cdb5413c95b8d66905fef548
  - observation observation_3132f013d2c94f36a6a37b78a26e9b59 (intel.report, observed_at 2026-11-01T15:36:15Z = HEAD commit time UTC, time_basis source_metadata)
  - artifact artifact_91cfb0a533f44b7fac487c79753599d6 (README.md, sha256 f6f1196361602937c4c6dbe1297c764bc24c6dbfa1b3eb072e9470a829514d81, 16325 bytes, storage local — NOT in data/blobs/)
- export: ok:true, exported ["data/records/8b87915d91ce4e7284fbbfdb1ad60f60"], pending 0. No sibling pending batches existed at export time.
- Exported batch validation (direct file read, no locks): 91 rows = 88 claims + 1 source + 1 observation + 1 artifact. All lane-tagged. Killed ids absent. Basis: UPSTREAM 80, OBSERVED 7, INFERENCE 1. Grade tags: REPORTED 80, OBSERVED 7, INFERENCE 1. All 81 DOWNGRADED carry the exact caveat in both body.note and tags.adversarial_caveat. All claims cite/subject the intel.report observation only (never the source record). Novelty tags: OVERLAP 41, NEW 26, NOT_CHECKED 12, N/A report-text 7, N/A method 2. Verification tags: NOT_ASSESSED 45, UNCHECKABLE 30, PARTIAL 8, VERIFIED 3, PARTLY 2.
- verify --blobs: ok:true, verified:true, records 225999 (225908 + 91), pending 0, state_digest 21d4d847601adf96a669aabf6807e7f6097ec5ac851c2afa93e2bdd8a328eab7 (matches export). Artifacts: 840 verified hashes; 1737 missing corpus-wide (pre-existing local-only bytes from other lanes — MY artifact is NOT in the missing list).
- NO git add/commit/push run (coordinator commits). No other lane dir, batch dir, or .local file touched. No symlinks created.

## Status

- COMPLETE. Batch dir (coordinator: commit this dir only): data/records/8b87915d91ce4e7284fbbfdb1ad60f60/
