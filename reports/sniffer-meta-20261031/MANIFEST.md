# Manifest — sniffer-sweep meta fleet 2026-10-31

Operator: BigSexyWarlock69. Coordinator commit: this report's commit
(see git log). No push by this fleet. No Factum writes.

## Report dir files

- REPORT.md — consolidated meta report (this fleet's deliverable).
- MANIFEST.md — this file.
- SHA256SUMS — hashes for REPORT.md, MANIFEST.md,
  adversarial-review.md, and verifier-report.md.
- adversarial-review.md — byte-identical copy of the meta
  adversarial review (raw/adversarial/ADVERSARIAL.md).
- verifier-report.md — byte-identical copy of the meta verifier
  report (raw/verifier/VERIFIER.md), including its supplementary
  correction on the Factum status leg.

## Raw lane dirs (data/lanes/sniffer-meta-20261031/raw/)

- meta-analyst/ — FINDINGS.md (corrections C1–C13, re-triage R1–R6,
  pattern scores P1–P8, novelty table N1–N3), STATE.md. Prose only,
  no fetched captures, no sidecars by construction.
- cryptologist/ — FINDINGS.md, STATE.md. Prose only, staged-byte
  re-derivation, no sidecars by construction.
- adversarial/ — ADVERSARIAL.md, STATE.md. Prose only, no sidecars
  by construction.
- committer-rerun/ — FINDINGS.md, STATE.md, STOPPED.txt, run.log,
  run-rerun.sh, 2 capture JSONs with .PROVENANCE.txt + .sha256
  (both pass), err-*.txt files. One 0-byte failed Codex capture
  carries a coordinator-added .sha256 sidecar (hash of the empty
  file) to close the verifier's non-blocking gap item.
- gh4-gh7/ — FINDINGS.md, STATE.md, 22 captures with .PROVENANCE.txt
  + .sha256 (all pass). FINDINGS.md and STATE.md carry passing
  sidecars.
- uq-wayback/ — FINDINGS.md, STATE.md, full 98-row da.gd pull,
  CDX retry files, T/Z probe file, pull script, all with .sha256
  (all pass).
- followups/ — FINDINGS.md, STATE.md, 24 captures with .PROVENANCE.txt
  + .sha256 (all pass at snapshot time; the verifier lane did not
  independently re-verify this lane's claims — see REPORT.md).
- verifier/ — VERIFIER.md, STATE.md. Prose only, no sidecars by
  construction.

## Hash coverage, stated honestly

- Meta tree sidecars: 63 at verifier check time (37 across six
  completed lanes + 26 follow-ups snapshot), 0 failures. With the
  coordinator-added Codex sidecar, capture-lane coverage is complete
  except provenance notes, which are not hashed by design.
- Prose-only lanes (meta-analyst, cryptologist, adversarial,
  verifier) are uncovered by construction: their outputs are prose
  re-derivations from the sweep's own hashed captures, not fetched
  bytes. Do not describe the meta tree as "fully hash-covered"
  without that qualifier.
- Report dir: SHA256SUMS covers the 4 non-SHA256SUMS files.

## Curation notes

- Report-dir review copies were verified byte-identical to their raw
  sources by sha256 comparison before commit.
- Follow-ups lane scrub conflict: its staged HN and Algolia captures
  are scrubbed derivatives (contact values replaced by shape markers),
  and the raw seller-list JSON plus raw log HTML were not staged.
  See REPORT.md evidence fidelity notes. The coordinator did not
  silently accept scrubbed derivatives as full evidence.
- Sweep raw tree presence note (handles, contact addresses,
  credential-like and wallet values) stands separately and is NOT
  part of this commit's scope. The sweep commit was pushed as-is
  per the operator's explicit word. That decision does not transfer
  to this commit, which is staged only and unpushed.
- Other workers' dirty files in the working tree were NOT swept into
  this commit. Explicit pathspecs only.
