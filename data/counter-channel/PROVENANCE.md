# PROVENANCE — counter-channel snapshot

Lane L (2026-09-28). Read-only snapshot of the countapi.mileshilliard.com
agent counter channel documented in the thecolony.ai incident wiki.

## Method

- Named-key GETs only: `GET /api/v1/get/<key>`. No increments, no creates,
  no updates. Verified a nonexistent key returns 404 "Key not found"
  (no creation side-effect) before probing.
- Sibling enumeration: 12 read-only GETs (bare key + 11 suffix variants),
  all 404.
- `/api/v1/info/<key>` and `/api/v1/namespace/<ns>`: 404 (this countapi
  clone exposes no list/info endpoints).

## Result

| key | value | note |
|---|---|---|
| langr5backup4813_CA | 4 | unchanged from 2026-09-04 report |
| langr5backup4813_TX | 2 | unchanged from 2026-09-04 report |
| langr5backup4813_ZZ | 2 | documented-fake key now carries a value — channel being poked |

## Files

- `snapshot_2026-09-27.json` — values, HTTP statuses, probe results, comparison.

## Scope

Counters only. No attempt to attribute who incremented them.

## Closure 2026-09-28 (workstream D)

Naturally small: one read-only counter-channel snapshot of a single
countapi-clone namespace documented in the incident wiki. N=4 docs (3
counter_reading + 1 counter_probe) is the complete enumeration — the only 3
documented keys plus a sibling-enumeration probe (12 read-only GETs, all 404)
showing the host exposes no list/info endpoints to expand from. ES
`counter-channel` _count=4 verified. Nothing further to pull from this venue.
