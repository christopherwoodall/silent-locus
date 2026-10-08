# schemas/transluce-api.md

Transluce Findings tracker integration under `data/transluce-api/`.

## `LEDGER.md` — daily ingest record

- Running record of daily ingest runs (`transluce-daily-ingest`,
  07:40 CDT) of the tracker into the corpus.
- Per run: raw pull path + finding count + sha256; prior snapshot;
  new findings by `created_at` with ids; per-finding overlap
  assessments grep-verified against the corpus.
- Pulls are read-only via `tl.py`
  (`~/workspace/skills/transluce/bin/tl.py`, Secure Vault surrogate).
  Note: `tl.py findings` returns only the first 25; `tl.py export json`
  truncates at 200KB — paginate `GET /api/findings` for full pulls.

## `raw/` — finding pulls

- `findings-list-YYYYMMDD.json` — full pull per ingest date.
- `findings-list.json` — latest snapshot (rolling).
- `schema-v3.json` — tracker schema as of last check.
- `PROVENANCE.md` — retrieval record for the pulls.

## `SCHEMA.md` / `README.md`

- `SCHEMA.md` — the common two-layer schema: Transluce findings
  (analyst conclusions) x our observation corpus (records).
- `README.md` — findings pulled so far; definitions: finding,
  observation, dead-drop, beacon, epoch, fingerprint.

## Subdirs

- `submissions/` — filing drafts + submissions LEDGER (see
  schemas/submissions.md).
- `urlquery-reports/`, `webhook-site/`, `deaddrop-grammar/`,
  `bounty-watch/`, `yourls-space/`, `swarm-traces/`, `wildclaw/` —
  per-lane evidence and analysis, each with its own FINDINGS/README
  and `raw/` captures.
- `epoch-clock/` — epoch-nonce clock analysis tooling.
