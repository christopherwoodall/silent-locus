# Manifest — agent-bypass forum hunt (STAGED, not filed)

Date of work: 2026-10-29.
Status: staged for the parent. No Factum writes made. No push made.
The parent pushes and verifies.

## Deliverables in reports/agent-bypass-forum-hunt/

- REPORT.md — ranked hits with grade, evidence path, and what
  would upgrade or kill each. Sections: REPORTED (21),
  DISCUSSED (4), mechanisms (9), pattern observation (1),
  appendix (9), killed and excluded (14), honest nulls,
  novelty, coverage, pivots, byte gaps, evidence index,
  coordinator decisions.
- hits.json — 58 entries: 21 REPORTED, 4 DISCUSSED,
  9 MECHANISM, 1 PATTERN, 9 APPENDIX, 14 KILLED. Every entry
  carries grade, source URLs, evidence paths, and novelty status.
  Count by section, not by grade: 30 entries carry grade
  REPORTED across sections (21 executed acts + 9 mechanisms).
  D02 carries a grade_detail field for its split grade.
  Appendix pointers A02, A04, A06 and all KILLED entries carry
  empty evidence lists by design (title-only pointers and
  killed items hold no bytes). All non-empty evidence paths
  verified to exist on disk at manifest time.
- MANIFEST.md — this file.
- SHA256SUMS — checksums for the deliverables in this directory
  plus every file under data/lanes/agent-bypass-forum-hunt/raw/.
  Stored paths are relative to the repository root. Verify with:
  `sha256sum -c reports/agent-bypass-forum-hunt/SHA256SUMS`
  run from the repository root. Do not run it from the report
  directory: the stored paths will not resolve there.
- adversarial-review.md — adversarial pass (30 fixes; applied
  by the coordinator, with two recorded dissents: item 10 kept
  REPORTED because the /proc dodge is attested in both versions,
  and item 9 kept ranked with a single-source flag).
- verifier-report.md — independent re-fetch verdict:
  SHIP-WITH-FIXES. Its counts reflect the pre-review snapshot
  (REPORTED 24, appendix 6); the coordinator applied its fixes
  and the adversarial moves after it, so current counts are
  REPORTED 21, appendix 9. Its checksum result (628 OK at the
  time) is superseded by the regenerated SHA256SUMS below.

## Raw evidence in data/lanes/agent-bypass-forum-hunt/raw/

- hn/ — 252 files (Algolia captures, 12 full thread dumps,
  4 linked-article text captures with provenance, provenance
  + sha256 sidecars).
- reddit/ — 22 files (press and aggregator captures, provenance
  + sha256 sidecars, lane SHA256SUMS).
- forums/ — 13 files (LessWrong and DEV captures, provenance
  + sha256 sidecars).
- github/ — 80 files (issue and comment JSON, search JSON,
  lane SHA256SUMS.txt, provenance).
- pivots/ — 270 files (urlquery, urlscan, crt.sh, GitHub
  search and repo captures, provenance + sha256 sidecars).
- Total: 637 raw files.

## Working notes in reports/agent-bypass-forum-hunt/working/

- hn-lane.md, reddit-lane.md, forums-lane.md, github-lane.md,
  pivots.md, linguist.md, cryptologist.md, plus the HN lane's
  fetch and triage scripts and screen/triage outputs.
- Working notes are lane evidence of method, not deliverables.
  They are committed with the deliverables for provenance.

## Verification method

- hits.json parsed as JSON; entry counts and ID uniqueness
  checked; every non-empty evidence path checked against disk
  (0 missing at manifest time).
- REPORT.md headings checked against hits.json IDs.
- SHA256SUMS generated fresh from disk at manifest time and
  verified with sha256sum -c (0 failures).
- Lane-side checksums (per-file .sha256 sidecars, lane
  SHA256SUMS files) were verified by the lanes at capture time;
  the verifier agent re-fetched bytes behind every citation
  independently, and the coordinator re-verified counts and
  paths after applying verifier and adversarial fixes.
- Path convention: REPORT.md uses shortened raw/ paths.
  Prepend data/lanes/agent-bypass-forum-hunt/ to get the
  repository path used in hits.json.

## Known limits carried into the manifest

- No OBSERVED items. Every ranked item is SECONDARY.
- Reddit items rest on press coverage; no Reddit thread was
  read directly (403, not routed around).
- HN October sweep gap for 28 terms; 8 large threads not
  fully fetched; legacy-tree grep incomplete.
- All non-Reddit novelty is PARTIAL at best.
- No reporter was contacted. Transcript requests need a human
  decision.
