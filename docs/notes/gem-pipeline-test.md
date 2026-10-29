# Gem pipeline test report — 2026-09-27

> **Provenance:** the gem tooling/data here serve our own independent
> Diffend-sourced collection (the RubyGems go-import campaign) — **NOT**
> part of the SwarmTraces dataset.

Scripts: `scripts/fetch_gems.py` (download + SHA-256 verify + log),
`scripts/mine_gems.py` (static tar extraction + IOC regex mining + graph emit).

## Burst-gem availability finding (blocks the intended test)

The two example burst gems from the task brief do **not** exist on rubygems.org:

- `tryf3zz` → `GET /api/v1/gems/tryf3zz.json` → **404** ("This rubygem could not be found.")
- `wandsworthprobe1778551714` → **404**

This corroborates the screenshot-site question: Christopher's screenshots show a
RubyGems search UI whose footer reads "Merad Software" with "Last diff"
timestamps — that is **not rubygems.org**. The burst gems live on whatever that
site is (site identification is with the rescan agent). The pipeline below was
therefore validated on real rubygems.org gems instead; the bulk target list
lands with the rescan.

## Test run (3 real gems, latest versions)

| gem | version | size | SHA vs API | files | IOC values | nodes | edges |
|---|---|---|---|---|---|---|---|
| oai | 1.3.0 | 60,416 B | match | 89 | 0 | 90 | 89 |
| json | 3.0.2 | 104,448 B | **MISMATCH** (see below) | 23 | 1 | 25 | 24 |
| thor | 1.5.0 | 56,832 B | match | 42 | 0 | 43 | 42 |

Totals: 158 graph nodes, 155 graph edges, 6 log records, 1 IOC hit record.
All outputs validate as JSONL (0 malformed lines).

## SHA-256 mismatch on json-3.0.2 (flagged correctly)

- versions API `sha`: `2afafb9c…1d4c3d0`
- downloaded bytes: `8e6d7e7b…25e73` (recomputed twice; file is a valid POSIX tar)
- The pipeline's `sha_mismatch: true` flag fired as designed. Likely benign
  (re-pushed gem / API metadata lag for a 2026-09-09 release), but any bulk run
  must quarantine `sha_mismatch` gems for review before mining — do not silently
  proceed on mismatched bytes.

## The single IOC hit: false-positive characterization

- `json-3.0.2 / CHANGES.md:530` → `zz-token` = **`zzak`**, from contributor email
  `e@zzak.io` in the changelog.
- Verdict: textbook false positive. Tuning note for the bulk run: the zz-token
  regex (`zz` + 2 chars) is too loose for changelog/email contexts — consider
  requiring ≥3 trailing chars or excluding `@`-adjacent matches. Left as-is for
  now (keep-all + annotate: the hit is logged with confidence, tuning later).

## Safety checks passed

- No `gem install`, no execution of extracted content (tarfile read + text grep only).
- Tar traversal filter active (no absolute/`..` members accepted).
- Binary files content-skipped (null-byte probe); native-extension logging path
  exercised — 0 native artifacts in the 3 test gems (published gems ship ext/
  source, not compiled .so).
- 500-gem cap refusal path present in fetch_gems.py (not triggered in test).

## Outputs

- `data/gem-ioc-log.jsonl` — download + extraction records (6)
- `data/gem-ioc-hits.jsonl` — per-file IOC hits (1)
- `data/gem-graph-nodes.jsonl` / `data/gem-graph-edges.jsonl` — hunt-schema
  JSON (id/label/type/subtype/description/first_seen/last_seen/source_url/
  confidence; source/target/relation/evidence_url/notes), merge-ready.

## Readiness for bulk run

READY pending two inputs: (1) the rescan's target list + correct download source
for the burst gems (not rubygems.org), (2) a decision on sha_mismatch handling
(quarantine recommended). ES mapping drafted at `notes/gems-es-mapping.json`;
no ingest performed.
