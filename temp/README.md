# temp/ — agent scratch space

Working scripts the agent wrote while analyzing or validating the repo live
here so Christopher can review exactly what was run. Nothing in here is part
of the pipeline; the real, permanent tools live in `scripts/`.

- `audit_collections.py` — the read-only audit used to design the naming
  schema: cross-checks every `data/` entry against records' `event.dataset`,
  `scripts/local_es_manifest.json`, and (historically) the snapshot.

Run from repo root: `python3 temp/audit_collections.py`
