# Data collections — index of event datasets

This directory holds 84 dated event collections for the agent-incident hunt.
Each collection is a self-contained evidence package: raw observations, a
canonical normalized event file, and provenance notes.

## Naming convention

`data/<YYYY-MM-DD>-<slug>/`

- The date is the **collection start date**, not the incident date — it records
  when this investigation lane opened.
- The slug names the target surface, venue, or incident family
  (e.g. `2026-09-28-chinese-amap-fleet`, `2026-10-01-deepsearchqa`,
  `2026-05-12-university-shorteners-events`).

## What a typical event directory contains

| Path | Contents |
|---|---|
| `raw/` | Source captures exactly as collected (JSON pulls, page scrapes, CSVs). Never edited. |
| `events.jsonl` | One canonical normalized event per line (`record_kind`, `fingerprint`, `labels`, timestamps). |
| `PROVENANCE.md` | Where the data came from, how it was pulled, coverage, and known blind spots. |
| `SHA256SUMS` | Hash manifest for the raw material (when present). |
| `build_events.py` / `build.sh` | The normalizer that produced `events.jsonl` from `raw/` — re-runnable. |
| `*_writeup.md` / writeup files | Analyst writeups of what the lane found. |

Conventions: keep-all, no dedup (overlap is annotated in metadata, not
removed); evidence values are never redacted.

## Flagship collection

- [`2026-09-28-chinese-amap-fleet/`](2026-09-28-chinese-amap-fleet/) — the main
  agent-fleet hunt: investigator personas, multi-lane sweeps (shorteners,
  infra, urlscan, wayback, live monitor), skill-egress supply-chain studies,
  the EUROSWARM German/French hunt, and the integrated investigation report.

## Full directory index

```
2016-12-28-rmn-re
2016-12-28-rmn-re-history
2018-05-09-paste-archive-gap
2021-05-10-vanderbilt-shortener
2021-10-30-demowiki
2022-03-01-jsonhero
2022-05-14-jqp-vercel
2022-08-09-github-forensics
2023-11-14-hfspace-proxies
2025-03-04-rubygems-goimport-campaign
2025-05-15-hf-tampering-check
2025-10-24-pastebin-k4be
2025-12-04-urlquery-marker-sweep
2026-02-01-agent-convo-venues
2026-02-14-md-succ-ai
2026-03-07-march7-rce-modality
2026-03-07-timeline-anchors
2026-03-11-dse-wiki-verification
2026-05-05-gomod-hunt
2026-05-11-july6-staging
2026-05-11-osv
2026-05-12-university-shorteners-events
2026-05-12-webhook-deaddrops
2026-05-17-collusion-wiki
2026-05-17-iowacollab-pastes
2026-05-26-paste-linuxiarz
2026-05-27-paste-archive
2026-06-04-admin-deletions
2026-06-17-reverse-tunnels
2026-06-19-rmn-re-linktable
2026-06-20-powerbi-fronting
2026-07-07-exfil-endpoint-pivot
2026-07-07-july7-gem-forensics
2026-07-07-july7-wave
2026-07-07-xss-ssti-census
2026-07-10-paste-ubuntu-cn
2026-07-21-transfer-test-family
2026-08-10-wayback-gem-capture
2026-08-19-tantive-space
2026-08-21-public-board
2026-08-25-commonlog-scan
2026-09-03-collusion-manifest
2026-09-04-thecolony-ai
2026-09-05-fieldnotes-gem
2026-09-05-termina-digital
2026-09-09-pixelleak-glow-labs
2026-09-12-jsonhero-docs-archive
2026-09-27-gem-negative-lanes
2026-09-27-gem-public-intel
2026-09-27-swarmtraces-verification
2026-09-28-ace-research-ct
2026-09-28-agent-surfaces
2026-09-28-agents-relay-sweep
2026-09-28-api-usa-fbi-ucr
2026-09-28-chinese-amap-fleet
2026-09-28-counter-channel
2026-09-28-dockerhub-trojan-images
2026-09-28-jsonhero-docs
2026-09-28-librariesio-pattern-battery
2026-09-28-ludism-wikis
2026-09-28-nsi-venue-sweep
2026-09-28-open-data-api-venues
2026-09-28-pastebin-cluster-sweep
2026-09-28-pastebin-pivot
2026-09-28-pxweb-national-stats
2026-09-28-university-shorteners
2026-09-28-university-shorteners-batch2
2026-09-28-university-shorteners-batch3
2026-09-28-uoft-shorteners
2026-09-28-worldpoverty-task-family
2026-09-28-yourls-resweep
2026-09-29-forged-flag-hunt
2026-09-29-gem-temporal-pivot
2026-09-29-separate-eval-test
2026-10-01-arquivo-pt
2026-10-01-deepsearchqa
2026-10-01-intermediary-relays
2026-10-01-oai-tag-sweep
2026-10-03-openai-agent-traces
2026-10-05-thecolony-ai
```

Each directory's own README (where present) or `PROVENANCE.md` is the
authoritative description of that lane.
