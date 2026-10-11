# PROVENANCE — lane 2026-10-11-deepmind-interactions-api

IOC Family E: DeepMind Interactions API surface + model identifiers + eval-awareness strings.
Ingest worker session: 2026-10-11. Branch: ingest-dm-interactions.

## Source material (as assigned)

- /tmp/google-ai-hunt/ — Google AI/developer/security blog scrape, 34 posts Nov 2025 → Oct 2026 (FINDINGS.md, PROVENANCE.md with curl retrieval lines + sha256, text extracts, raw/ HTML, interactions.openapi.json).
- /tmp/gemini-cards-hunt/ — Gemini system cards & safety reports (FINDINGS.md 93 lines, PROVENANCE.tsv with URL/retrieval-time/file/sha, PDFs/TXTs, fairwind.txt).
- /tmp/deepmind-hunt/ — deepmind.google pages (raw/ HTML, text/ extracts, PROVENANCE.tsv).

## Incident: /tmp wiped mid-task

The VM cleaned /tmp during this ingest run (first noticed 2026-10-11 ~16:10 UTC).
All three source dirs were gone; a deep filesystem search found no copies.
Re-fetched dirs that appeared later in /tmp (gtg-hunt, gtig, interactions-hunt,
skillchain-hunt) are other workers' lanes — NOT the same material, not touched.

Retained bytes preserved here (copied verbatim from the session before the wipe):
- raw/google-ai-hunt-FINDINGS.md — full text of /tmp/google-ai-hunt/FINDINGS.md (read in full this session).
- raw/google-ai-hunt-PROVENANCE.md — full text of /tmp/google-ai-hunt/PROVENANCE.md (read in full; retrieval timestamps 2026-10-11T15:43–15:48Z, method curl -sSL, sha256 per file).
- raw/gemini-cards-hunt-FINDINGS.md — full text of /tmp/gemini-cards-hunt/FINDINGS.md (read in full this session).

The two deepmind-hunt PROVENANCE.tsv and the gemini-cards PROVENANCE.tsv were
NOT fully read before the wipe (only file listings seen) — no records were
built on them.

## Grading policy used

- All submitted records are graded UPSTREAM or INFERENCE — the raw source bytes
  (blog HTML, PDFs, openapi.json) were lost before lane copy, so nothing here is
  self-OBSERVED by this worker.
- Verbatim strings (model IDs, API endpoint paths, header names, tool strings,
  eval-awareness quotes) are preserved byte-exact from the FINDINGS texts.
- Records whose terms come ONLY from the parent task brief's extraction list
  (CTI-MCQ, CTI-RCM, Online-Mind2Web, GDPval-AA, lyria-3-5, sec-gemini) are
  graded INFERENCE with provenance "parent-task extraction list; not
  re-verified against source extracts (lost)".
- DeepMind-hunt file-name-only items (agent-payments protocol, GTIG) got NO
  records — file names are not observations of content.
- Behavioral records are graded INFERENCE with section cites to the FINDINGS docs.
- The PageBreak RCE-validator beacon-mimicry caution is recorded as a claim
  (analyst note), NOT as IOCs. No IOCs were filed for PageBreak validator
  traffic.

## Recommended follow-up

Re-run the three hunts with raw/ written STRAIGHT into data/lanes/ (never /tmp),
then upgrade these records' provenance/grades and fill the deepmind-hunt gap
(AP2 agent-payments protocol, GTIG reports, sec-gemini).

## Claim grades

No claim is graded OBSERVED. Grades used: UPSTREAM (term string seen in an
upstream hunt doc, exact bytes preserved) and INFERENCE (analyst synthesis or
task-brief-only terms).

Nothing was redacted. No edges were created during ingest.
