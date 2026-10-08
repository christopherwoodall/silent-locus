# schemas/evidence-packs.md

Evidence capture layout. Two shapes, both require provenance.

## Per-finding evidence dirs

`data/transluce-api/<finding-slug>/` (e.g. `betterwright/`,
`deaddrop-followup/`, `wildclaw-keys/`):
- `raw/` — captured evidence files (HTML pages, API JSON, dataset
  files). Never edited after capture.
- `PROVENANCE.md` — required sections: What (dataset/page identity),
  Source (URL, pinned revision/commit where applicable), Retrieval
  (time, method, tool, rate limits observed), and what changed or
  failed between pulls.
- `SHA256SUMS.txt` — sha256 of every file in `raw/`.
- Analysis writeup at the top level: `AUDIT.md` (dataset audits),
  `FINDINGS.md` (investigation results), or `VERIFY.md` (claim
  verification). Claims graded OBSERVED / INFERENCE.

## `PROVENANCE.md` field rules

- Source URL: exact, copy-pasteable.
- Retrieval time: UTC with timezone stated.
- Retrieval method: tool + auth path (e.g. `curl` per TOOLS.md,
  `uq.py` via Secure Vault surrogate). Never python `huggingface_hub`
  on this VM (broken proxy handling — use curl).
- One row/file per hash in SHA256SUMS. A capture without provenance
  is not evidence.

## Zipped evidence packs

- `data/transluce-api/deaddrop-evidence-pack.zip`,
  `data/hf-trajectories/jina-evidence-pack.zip`,
  `data/hf-trajectories/glm-evidence-pack.zip` — frozen packs attached
  to submissions. Rebuild, don't mutate.
