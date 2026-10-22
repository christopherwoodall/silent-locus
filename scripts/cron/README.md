# scripts/cron/ — per-site monitors

One script per site. Each site script is ~20 lines: it defines a SITE
dict and calls into `sitewatch.py`, the shared library that does all
fetching, state handling, and reporting.

## Layout

- `sites.json` — registry: one entry per site
  `{name, label, urls[], kind, notes}` (+ `feed` for feed-kind sites).
- `sitewatch.py` — shared library. Polite fetch (>=5s spacing, 30s
  timeout), atomic state writes to `state/<name>.json`, `--dry-run` /
  `--json` / `--limit` flags, provenance timestamps. Never raises out
  of a site check; per-URL failures become ERROR results and are also
  reported to the scanner error log.
- `sites/<name>.py` — one per site, generated from `_template.py`.
  Files starting with `_` are not site scripts (run-all skips them).
- `run-all.py` — runs every site script in its own process, serially,
  aggregates NEW/CHANGED/UNCHANGED/ERROR. Exit 1 only on hard errors.
- `state/` — runtime state (gitignored). One JSON per site.

## Kinds

- `listing-hash` — GET each URL, sha256 the body, compare with state.
  For board homepages, channel listings, llms.txt.
- `api-poll` — GET JSON endpoint, sha256 canonicalized JSON, compare.
- `cdx` — Wayback CDX new-capture check for a domain (paste archives).
  `urls` holds bare domains.
- `feed` — IOC feed recent-items check over GET-able sources only.
  `otx-indicators` polls keyless OTX indicator endpoints and reports
  pulse-count changes. `delegate` hands off to
  `scripts/scanners/iocfeeds.py` when present. `skipped` (with reason)
  when there is no keyless GET surface — exits 0, never an error.

## Scheduling suggestion

- `run-all.py` hourly (full sweep is polite but slow: ~40 sites).
- Or split: boards hourly, pastes (cdx) every 6h, feeds hourly.

## Grading

Every hit out of these scripts is SECONDARY until independently
verified (operator grading rule). A CHANGED board page is a lead, not
a finding. Never POST, never log in, never create sessions.
