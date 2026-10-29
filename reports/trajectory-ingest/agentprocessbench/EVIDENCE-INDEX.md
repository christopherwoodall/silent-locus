# Evidence index — agentprocessbench-trajectories ingest

Every file below is a navigation pointer, not a new evidence claim.
Byte-level evidence lives in the raw captures and the Factum records.

## Lane directory

`data/lanes/agentprocessbench-trajectories/`

| File | What it is |
|---|---|
| `raw/bfcl/test.jsonl` | Source bytes, 250 trajectories, sha256 `6aee0b71…b6fe5` |
| `raw/gaia_dev/test.jsonl` | Source bytes, 250 trajectories, sha256 `f7b75c66…05ce819` |
| `raw/hotpotqa/test.jsonl` | Source bytes, 250 trajectories, sha256 `160eef2d…e6309c57` |
| `raw/tau2/test.jsonl` | Source bytes, 250 trajectories, sha256 `6f22818f…f127e1e95` |
| `raw/manifest.json` | Per-file provenance: source URL, retrieved_at, bytes, sha256 |
| `raw/SHA256SUMS` | Checksums |
| `raw/LICENSE.note` | License facts: API license null; tags `license:mit`; README front matter `license: mit`; no license text ships |
| `raw/README.md` | Dataset card (license: mit front matter; arxiv 2603.14465) |
| `raw/*/test.jsonl.PROVENANCE.txt` | Retrieval method (curl -sL), UTC time, sha256 |
| `verified-findings.jsonl` | 20 findings with verifier_note, novelty=new |
| `review-findings-A.jsonl`, `review-findings-B.jsonl` | Pre-verifier reviewer outputs |
| `review-killed-A.md`, `review-killed-B.md`, `review-killed-verifier.md` | Kill lists with reasons |
| `review-scratch/` | Reviewer working files (scan scripts, candidates) |
| `build_bundle.py` | Bundle builder (tool-call extractor, both serializations) |
| `bundle.json` | Submitted Factum bundle (68 records) |
| `PROGRESS.md` | Ingest step checklist |

## Factum records (batch id pending submit)

68 records, all tagged `lane: agentprocessbench-trajectories`:

| Type | Count | Role in the chain |
|---|---|---|
| source | 4 | One per dataset file URL |
| observation `dataset.snapshot` | 4 | Revision, coverage=complete, row_count=250 |
| observation `behavior.tool_sequence` | 20 | All tool calls per finding trajectory, message-ordered, step labels annotated |
| observation `intel.behavior` | 20 | One classified finding each, cites its tool_sequence |
| claim | 20 | OBSERVED, cites behavior + tool_sequence |

Chain: claim → intel.behavior → behavior.tool_sequence → trajectory
locator → raw bytes. `exhibits`/`uses` edges are NOT submitted (edge
builder pass, separate).

## Reports

| File | What it is |
|---|---|
| `REPORT.md` | This ingest's report (purpose, sources, method, 20 findings, kills, overlap, open questions, coverage) |
| `EVIDENCE-INDEX.md` | This file |

## Taxonomy change

`docs/taxonomy/behavior-categories.md`: added "Eval-derived categories
(AgentProcessBench trajectories, 2026-10)" — eight new slugs:
`injected-directive-compliance`, `unauthorized-irreversible-action`,
`unverified-entitlement`, `tool-protocol-misuse`, `recovery-livelock`,
`barrier-respecting-recovery`, `confabulation-under-retrieval-failure`,
`blind-tool-output-trust`. (`credential-exposure` already existed.)

## Pipeline docs

`scripts/trajectory-pipeline-README.md`: new "Worked example:
AgentProcessBench" section — dataset IDs, the dual tool-call
serialization quirk, step_labels semantics, license note, what worked.
