# Evidence index — swe-agent-nebius-trajectories ingest

Every entry below is a navigation pointer, not a new evidence claim.
Byte-level evidence lives in the raw captures and the Factum records.

## Lane directory

`data/lanes/swe-agent-nebius-trajectories/`

| File | What it is |
|---|---|
| `raw/train-00000-of-00012.parquet` | Source bytes, 6,670 rows, sha256 `5a395e8c…067a13` |
| `raw/train-00006-of-00012.parquet` | Source bytes, 6,670 rows, sha256 `fcad81ec…37c` |
| `raw/train-00010-of-00012.parquet` | Source bytes, 6,669 rows, sha256 `419e02da…36b12` |
| `raw/train-*.parquet.sha256` | Per-file checksum sidecars |
| `raw/train-*.parquet.PROVENANCE.txt` | Retrieval method (curl -L), UTC time, URL, revision |
| `raw/MANIFEST.json` | Sample provenance: URLs, sizes, sha256, label stats, wire-up check |
| `raw/LICENSE.note` | License facts: API card `cc-by-4.0`; README verbatim CC-BY-4.0; per-repo-license caveat; Llama 3.1 output-license notice |
| `SAMPLING-PLAN.md` | Sampling design (cluster sample, 1.5 GB cap, strata, gaps) |
| `sample-manifest.json` | Exact rfilenames, download URLs, sizes, LFS sha256, stratum labels |
| `PROVENANCE.txt` | How every sampling-plan fact was obtained |
| `working/verified-findings.json` | 15 findings with verifier_note, grade PRIMARY |
| `working/adversarial-kills.json` | 2 kills (A-012 duplicate, B-004 false premise), overlap verdict, coverage gaps |
| `working/reviewer-A-findings.json`, `working/reviewer-B-findings.json` | Pre-verifier reviewer outputs |
| `working/reviewer-A-kills.json`, `working/reviewer-B-kills.json` | Reviewer-phase kill lists |
| `working/b-scan*.py`, `working/prescan*.py`, `working/loops.py` | Reviewer scan scripts (hits-*.json outputs beside them) |
| `build_factum_bundle.py` | Bundle builder (94 records) |
| `validate_batch.py` | Independent validator (10 checks, re-derived from originals) |
| `bundle-swe-agent-nebius.json` | Submitted Factum bundle |

## Per-finding byte pointers

Raw bytes are local-only (gitignored). Full sha256 values:

- `train-00000-of-00012.parquet`: `5a395e8c7bb8ddc4b8f4d268506b3a0e2cf9b5ec3922600117322fe788067a13`
- `train-00006-of-00012.parquet`: `fcad81ec5704cb2dc8502a70a1a6cd86a7032227d8de7a613d904636ee53337c`
- `train-00010-of-00012.parquet`: `419e02daa099343e73d45d298b64e574ee012398ebbe19e5798526e5f1336b12`

| Finding | File (lane `raw/`) | Row | File sha256 (first 12) | Steps | instance_id |
|---|---|---|---|---|---|
| A-001 | train-00010-of-00012.parquet | 296 | 419e02daa099 | 12–14 | pydantic__pydantic-3547 |
| A-002 | train-00010-of-00012.parquet | 316 | 419e02daa099 | 12–14 | pydantic__pydantic-4224 |
| A-003 | train-00006-of-00012.parquet | 283 | fcad81ec5704 | 15–18 | mapbox__cligj-14 |
| A-004 | train-00006-of-00012.parquet | 2008 | fcad81ec5704 | 22–29 | perrygeo__python-rasterstats-287 |
| A-005 | train-00006-of-00012.parquet | 684 | fcad81ec5704 | 56 | scikit-hep__particle-494 |
| A-006 | train-00000-of-00012.parquet | 5695 | 5a395e8c7bb8 | 22–26 | iterative__dvc-4623 |
| A-007 | train-00000-of-00012.parquet | 3061 | 5a395e8c7bb8 | 2–796 | iterative__dvc-7497 |
| A-008 | train-00000-of-00012.parquet | 3948 | 5a395e8c7bb8 | 4–782 | iterative__dvc-9000 |
| A-009 | train-00000-of-00012.parquet | 3477 | 5a395e8c7bb8 | 18–82 | treasure-data__td-client-python-44 |
| A-010 | train-00006-of-00012.parquet | 3109 | fcad81ec5704 | 60–63 | pydantic__pydantic-3177 |
| A-011 | train-00006-of-00012.parquet | 3109 | fcad81ec5704 | 64–70 | pydantic__pydantic-3177 |
| B-001 | train-00006-of-00012.parquet | 4827 | fcad81ec5704 | 20–26 | streamlink__streamlink-3019 |
| B-002 | train-00006-of-00012.parquet | 6358 | 5a395e8c7bb8 | 28–31 | streamlink__streamlink-1696 |
| B-003 | train-00010-of-00012.parquet | 5526 | 419e02daa099 | 8 | auth0__auth0-python-195 |
| B-005 | train-00006-of-00012.parquet | 5277 | fcad81ec5704 | 58 | aesara-devs__aesara-854 |

Row index = 0-based row within the parquet file. A-010 and A-011 are two
behavior arcs in one trajectory row (3109). All quotes in REPORT.md were
verified verbatim against these bytes with an independent pyarrow re-read
on 2026-10-17.

## Open lead (unverified, not filed)

- `asottile__pyupgrade-380`, `raw/train-00006-of-00012.parquet` row 3796,
  target false, exit `submitted`: agent ran `rm -r src pyupgrade.py`,
  deleting the repo's own main source file, then submitted. Byte
  verification still owed.

## Factum records (batch id pending submit)

- Source, run, snapshot, 3 artifacts: search `tags.lane =
  swe-agent-nebius-trajectories` with the matching record kind.
- Per finding: `intel.behavior` with `tags.finding_id = <id>`; per
  trajectory: `dataset.record` with `tags.file` + `tags.row_index`; per
  tool sequence: `behavior.tool_sequence` with `tags.finding_id = <id>`.
- Edges: `supports` from finding and tool-sequence to the trajectory
  record; `related_to` from the run to the trajectory record.
