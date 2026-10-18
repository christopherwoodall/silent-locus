# Evidence index — InterCode-CTF ingest (2026-10-16/17)

## Review inputs (pre-ingest)

- `data/lanes/intercode-ctf-trajectories/verified-findings.jsonl` —
  18 byte-verified PRIMARY findings (V-001..V-018). Each has id, class,
  dataset, dataset_rev, trajectory_id, steps, quote, grade,
  confidence, why_interesting, source_file, sha256, verifier_note.
- `data/lanes/intercode-ctf-trajectories/working/verifier-kills.md` —
  kill/merge record: 23 findings in, 18 out. 1 outright kill (A-010);
  merges A-002+RB-F010→V-002, A-005+RB-F009→V-003, A-008+RB-F007→V-010,
  A-004 folded into V-003. Reviewer kills K1-K10 + 1-12 upheld.
- `data/lanes/intercode-ctf-trajectories/raw/` — 13 dataset dirs, each
  with `.eval` ZIP journal + `.PROVENANCE.txt` + `.sha256` sidecars,
  `config.json`, chat templates, `DATASET.md`, `LICENSE.note`,
  `MANIFEST.json`.

## Raw bytes (retained, not modified)

- `data/lanes/intercode-ctf-trajectories/raw/<shortname>/logs/inspect_evals/gdm_intercode_ctf/benign.eval`
  — 13 inspect_ai eval ZIP journals (835 samples). Retrieval
  2026-10-17 02:56–03:19 UTC, curl https-get, per-file sha256.
  Example sha256: 70B `814bdeb9e91d7bfd4ae2566c46fc24990f91ec8fc3e86f1c25ccf137548443e0`;
  full list in `raw/MANIFEST.json`.
- `data/lanes/intercode-ctf-trajectories/raw/DATASET.md` — per-dataset
  model/template table (12 benign CTF prompts; devstral has the
  tool-less "helpful, harmless and honest" prompt).
- License: apache-2.0 on all 13 (HF API tag + README frontmatter).

## Ingest artifacts

- `data/lanes/intercode-ctf-trajectories/build_factum_bundle.py` —
  bundle builder (documents record design and dedup anchor).
- `data/lanes/intercode-ctf-trajectories/bundle-intercode-ctf.json` —
  the submitted bundle (sha256
  `854eeb0cdb63266c3aae86d3e2676356c17ee83d8833a27d53348695c66b8621`).
- `data/lanes/intercode-ctf-trajectories/build-report.json` —
  builder counts.
- `data/lanes/intercode-ctf-trajectories/working/add.log` — add retry
  log under sibling lock contention.
- Factum batch: `data/records/<batch>/` (id set at export time).

## Factum records (1,753 total)

| kind | count | note |
|---|---|---|
| source | 13 | one HF dataset each |
| artifact | 13 | one benign.eval ZIP each (sha256+size) |
| run | 1 | scrape, `run-scrape` |
| observation:dataset.snapshot | 1 | lane-wide, 835 rows |
| observation:dataset.record | 835 | lean: sample id, dataset, message/tool-call counts, score — no step content |
| observation:behavior.tool_sequence | 18 | ordered tool calls per unique finding trajectory |
| observation:intel.behavior | 18 | one per finding; taxonomy categories from `docs/taxonomy/` |
| edge | 854 | 835 run→trajectory (`related_to`), 19 finding→trajectory (`supports`) |

Taxonomy: 4 existing categories + 6 new eval-derived categories added
to `docs/taxonomy/behavior-categories.md`
(`guardrail-erosion`, `refusal-absence`, `tool-output-confabulation`,
`generation-silence`, `generation-stall`, `false-capability-denial`).

## Dedup

Direct `data/records/` byte scan for `intercode`,
`gdm_intercode_ctf`, `jordan-taylor-aisi`, lane name: 0 hits. In-batch
dedup anchor `behavior.tool_sequence` + trajectory ID: V-009 and V-010
share d8 sample 56 — one shared tool_sequence record, both findings
edge to it.

## Aggregates without trajectories

V-002 (refusal-absence, 790 samples) and V-003 (banner degradation,
316 samples) are corpus-level: no tool_sequence, no finding edges.
Documented in REPORT.md and in the records' tags.
