# Wayback CDX sweep

Read-only CDX sweep of the Wayback Machine for Transluce-incident URLs.

Motivation: the skill-ladders investigation found agent skills are
archive-first BY INSTRUCTION, and `hemo-web-read` teaches agents to CREATE
captures via `web.archive.org/save/`. Wayback captures would be timestamped
evidence of agent activity.

- `sweep.py` — idempotent, stateful (`state.json`), polite (2s pacing +
  backoff). Run: `python3 sweep.py`
- `data/cdx-log.jsonl` — every CDX request logged
- `data/in-window-captures.jsonl` — captures timestamped Apr–Jul 2026
- `SWEEP-REPORT.md` — findings

Queries: prefix sweeps (`civilrightsdata.ed.gov/api/v1.0/*`,
`recherche-collection-search.bac-lac.canada.ca/ajax/*`, `apps.bea.gov/api/*`),
a `zz=oai`-filtered prefix query, exact queries for `sec.gov/files/county.json`
and the 14 LAC payload URLs, and a seeded random sample of 200 exact
`zz=oai` DoE URLs drawn from the Arquivo.pt distinct set.

Read-only: never submits save requests.
