# Manifest — Fleet B (Cohere Qwen call-home hunt)

## Status

STAGED, not filed.
A sibling fleet owns all Factum writes.
This fleet stages hits for parent phase-2 ingest.
No file here was committed, pushed, or written to Factum.
No raw evidence file was changed.

## Files in this report directory

- `REPORT.md` — fleet report, ASD-STE100 style, revised after adversarial and cryptologist review: 3 ranked hits, plus appendix and triaged-out sections.
- `hits.json` — ranked hits (3) plus appendix (4) and triaged-out entries, with grade, confidence, evidence paths, and novelty verdicts.
- `MANIFEST.md` — this file.
- `SHA256SUMS` — SHA-256 hashes over the report files only, not raw/.

## Evidence home (not hashed here)

All evidence lives under:

`data/lanes/cohere-qwen-hunt/raw/`

Subdirs: `github/`, `huggingface/`, `urlquery/`, `urlscan/`, `wayback/`, `crtsh/`.

Per-item evidence paths are listed in `REPORT.md` and `hits.json`.
Raw files carry their own `.PROVENANCE.txt` and `.sha256` sidecars, made by the worker fleets.

## House-rule note

Repo `AGENTS.md` says new structured evidence goes through Factum.
That rule is deferred here by parent order: this fleet STAGES only.
The sibling fleet owns Factum writes, and the parent runs phase-2 ingest.
This manifest records that deferral so the staging is explicit, not silent.
