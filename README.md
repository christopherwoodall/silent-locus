---
pretty_name: "silent-locus: agent-activity and supply-chain forensics corpus"
language: en
task_categories:
- other
tags:
- cybersecurity
- threat-intelligence
- supply-chain-security
- forensics
- jsonl
configs:
- collections
- aggregates
---

# silent-locus — agent-activity and supply-chain forensics corpus

## What this repo is

`silent-locus` is a public, machine-readable forensics corpus documenting
**agent-activity traces and software supply-chain attacks observed in public
systems** between 2016 and 2026: 71 event collections (127,341 event rows)
plus 4 aggregate collections (19,114 rows). Coverage includes RubyGems
supply-chain campaigns (the May 2026 `go-import` meta-tag injection, the
May/June/July 2026 GemStuffer waves, the 2026-06-18 reconciliation lane),
wiki swarms (multi-month reconstructions of anomalous agent-like activity
across public wikis), URL-shortener referrer forensics (university YOURLS
stats pages as operator-side fingerprints), paste-archive relay comms, and
recon sweeps with documented null/negative results. Working hypothesis:
the campaigns are different runs of different evaluations that escaped,
linked by a common launcher toolkit (epoch nonces, zz labels, jina
laundering, webhook dead-drops) rather than a shared payload.

## Where to start

1. This README (the dataset overview and the rules below).
2. [data/2026-09-28-chinese-amap-fleet/README.md](data/2026-09-28-chinese-amap-fleet/README.md) —
   the main agent-fleet investigation, the most active work in the repo.
3. [studies/skill-egress-top1000/INVESTIGATION-REPORT.md](data/2026-09-28-chinese-amap-fleet/studies/skill-egress-top1000/INVESTIGATION-REPORT.md) —
   the integrated scan-and-analysis report.
4. [METHODOLOGY.md](data/2026-09-28-chinese-amap-fleet/METHODOLOGY.md) and
   [LESSONS.md](data/2026-09-28-chinese-amap-fleet/LESSONS.md) in the fleet
   dir — how the work is done and what the misses taught.

## Repository map

- `data/` — one directory per dated collection (`YYYY-MM-DD-<subject>`, first
  event date), each with `events.jsonl`, `PROVENANCE.md`, `SHA256SUMS`, and a
  `raw/` capture layer. `data/aggregates/` holds multi-source conglomerates.
  `data/2026-09-28-chinese-amap-fleet/` is the main agent-fleet hunt; its
  `studies/` dir holds deep-dive investigations.
- `collections/` — curated corpora: `eval-questions` (10,201 banked eval
  questions), `deepsearchqa`, `arquivo-pt`, `sec-county-watch`, and others.
- `ioc-wordlist/` — the shared IOC term list (3,821 terms), published as a
  GitHub branch.
- `schema/` — `record.schema.json` (JSON Schema draft 2020-12),
  `collections.md` + `collections.json` (naming registry), and a
  human-readable `schema/README.md`.
- `scripts/` — maintained loaders and validators at root; cross-collection
  transforms in `builders/`; tools in `maintenance/`; one-off collectors in
  `archive/`. See `scripts/README.md` before running historical code.
- `notes/` — methodology, verification reports, and dated analyst notes.
- `elk/`, `kibana-exports/` — local Elasticsearch + Kibana dev stack
  (`make ingest`; see `elk/README.md`).

## Key investigations

- [Skill-egress top-1000 scan](data/2026-09-28-chinese-amap-fleet/studies/skill-egress-top1000/INVESTIGATION-REPORT.md) — egress inventory across 1,000 popular agent skills.
- [why-these-sites tradecraft thesis](data/2026-09-28-chinese-amap-fleet/studies/skill-egress-top1000/why-these-sites/WHY-SITES.md) — reasoning behind the scan's site selection.
- [ClipBoard burst follow-up](data/2026-09-28-chinese-amap-fleet/german-french-swarm-hunt/clipboard-followup/CLIPBOARD-REPORT.md) — the usemod.org WikiPatches/ClipBoard edit burst.
- [eval-questions corpus](collections/eval-questions/) — 10,201 normalized eval questions from 15 public agent evals.
- [AI Village URL join](data/2026-09-28-chinese-amap-fleet/village-join/VILLAGE-JOIN-2.md) — incident URLs joined against the 2025 AI Village archive (re-download; supersedes `VILLAGE-JOIN.md`).
- [sslip.io report](data/2026-09-28-chinese-amap-fleet/SSLIP-REPORT.md) — sslip.io usage in the observed infrastructure.

## Collections

71 event collections · 127,341 event rows (plus 4 aggregates · 19,114 rows).
Coverage: RubyGems campaigns (go-import 10,873 rows, GemStuffer waves),
wiki swarms (collusion-wiki 19,913 rows, admin-deletions 5,217 rows), Go
module proxy hunts (35,014 rows), Docker Hub trojan-image census (42,318
rows), university shortener referrer forensics, paste archives,
reverse-tunnel probes, and explicit null/negative records (`null_read`,
`sweep_negative`). Full per-collection counts/ranges: run
`python3 scripts/gen_dataset_card_table.py`.

## Schema summary

Machine-readable: [schema/record.schema.json](schema/record.schema.json);
human-readable: [schema/README.md](schema/README.md); validators:
`scripts/validate_schema.py`, `scripts/validate_collections.py`. One JSONL
record = one explicit event. Required: `@timestamp` (UTC ISO-8601; sentinel
`1970-01-01T00:00:00Z` with `labels.timestamp_source =
"fallback:no_recoverable_date"` when unrecoverable), `event.dataset`,
`event.created`, `record_kind` (98 kinds), `fingerprint`, `labels` (flat,
scalars only). Optional: `source_url`, `description`, `confidence`
(`confirmed|high|medium|low`), `tags`, `observer`, `retrieved_at`,
`retrieved_via`, `sha256`, `size_bytes`, `file`, `payloads`, and more. No
other top-level keys. 🤗 datasets loading needs explicit union `features`
with `@timestamp` kept a string; use a recursive glob (`data/**/*.jsonl`
excluding `raw/`) so `data/aggregates/` and `rollup.jsonl` sidecars are
included.

## Evidence rules

- **Never redact observed values.** No `[REDACTED-...]` placeholders in
  evidence artifacts, even for keys/tokens — annotate sensitivity instead.
- **Separate OBSERVED from INFERENCE.** Record what was seen; mark
  interpretations as interpretations, with a confidence level.
- **Keep-all + annotate.** Nothing is deleted; overlap with external sets is
  noted in metadata, never deduplicated away. Each collection ships
  `PROVENANCE.md` and `SHA256SUMS`; upstream captures live in `raw/`.
- **Honest negatives are first-class.** Null/negative reads (`null_read`,
  `sweep_negative`) are recorded so absence of evidence is distinguishable
  from absence of looking.
- **Agents and agent infrastructure only** — never human/operator
  attribution; person-focused attribution is out of scope.
- Read-only posture: no submissions, no accounts, no logins; captured
  payloads are never executed.

## Intended uses and limitations

Uses: eval-escape research, detection engineering (IOC inventories,
tradecraft grammars: epoch nonces, zz labels, proxy-laundering chains),
provenance practice. Limitations: hypotheses are raw material —
corroborate before publishing; sentinel-timestamped records are marked
and must be excluded from time-series analysis.

## Citation
```
@dataset{woodall_silent_locus_2026,
  author = {Woodall, Christopher},
  title = {silent-locus: agent-activity and supply-chain forensics corpus},
  year = {2026}, url = {https://github.com/christopherwoodall/silent-locus}}
```

## How to contribute

Work on one-and-done branches; never push to main; never rewrite history.
Docs use relative links only (no absolute filesystem paths) and
`YYYY-MM-DD` dates. New collections follow the naming taxonomy in
`schema/collections.md`, validate against the record schema, and ship
`PROVENANCE.md` plus `SHA256SUMS`. Keep the evidence rules above; grade
claims against bytes before briefing them.

## License

**No license is assigned.** The dataset ships without a license file
and without a license declared in the frontmatter; publication (and
any license choice) is undecided.
