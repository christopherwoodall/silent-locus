# Evidence-lane scanners

Multi-lane crawler swarm for agent-swarm activity. Built 2026-10-14 per
BigSexyWarlock69's order. Every module passed linguist, cryptologist,
and adversarial counsel review before shipping.

Each module follows the shared contract (see `_common.py`):

    scan(since_hours=24, seen_ids=None, dry_run=False) -> list[dict]

CLI: `<module>.py [--since-hours N] [--dry-run] [--json]`
`--dry-run` prints what WOULD be queried and returns no hits; it never
touches the network.

## Modules

| # | Module | Lane ID | Source | Grade |
|---|---|---|---|---|
| 1 | `urlquery.py` | urlquery-amap-watch | urlquery.net API search (authenticated, via `uq.py`) | PRIMARY |
| 2 | *(sibling)* `swarm-infra-crawler.py` | webhook-creator-ip | webhook.site creator-IP extraction | PRIMARY |
| 3 | `ntfy.py` | ntfy-monitor | ntfy.sh JSON poll + Wayback CDX fallback | PRIMARY |
| 4 | `urlscan.py` | urlscan-amap | urlscan.io: getPoiInfo, uqscan=, uqframe= | PRIMARY |
| 5 | `wayback.py` | wayback-infra | Wayback CDX: fleet infra captures (port 80) | PRIMARY |
| 6 | `crtsh.py` | crtsh-certs | crt.sh: %.hysandbox.tencent-cloud.com | PRIMARY |
| 7 | `packages.py` | package-registries | RubyGems/PyPI/npm rare-marker tripwire | SECONDARY |
| 8 | `dbmining.py` | db-url-mining | Our factum/lane data: repurposable surfaces | PRIMARY |

## Hit dict

Every hit carries: `lane`, `observed_at`, `source_url`,
`indicators_matched`, `grade`, `provenance`, `confidence`
(HIGH/MEDIUM/LOW), `summary`, plus module-specific `extra` fields.

### IP classification (standing rule, BigSexyWarlock69)

Every hit that records an IP address carries `ip_classification`, the
dict returned by `ip_classifier.classify_ip` against
`scripts/swarm-infra-config.json`, using the shared cache
`scripts/scanners/state/ip_asn_cache.json`:

- tier 1 `KNOWN_SWARM` — exact IP or CIDR match (highest signal)
- tier 2 `CLOUD_SERVICE` — ASN is a cloud provider (flagged which)
- tier 3 `RESIDENTIAL_VPN_HOSTING`
- tier 4 `UNKNOWN`

Hits with tier 1 or 2 set `"priority": true` — they surface in alerts
and the morning breakdown. A cloud IP where you don't expect one is
signal: it is flagged, never filtered.

## False positives

`FALSE-POSITIVES-*.md` (one per lane) documents, per detection rule,
what benign activity can match and how the scanner mitigates it. Read
them before triaging hits.

## Counsel reviews

- `COUNSEL-REVIEW-linguist.md` — 5 HIGH, 10 MED, 9 LOW pattern fixes
- `COUNSEL-REVIEW-cryptologist.md` — evasion analysis, 25 ranked evasions
- `COUNSEL-REVIEW-adversarial.md` — per-rule KEEP/DEMOTE/CUT verdicts
- `../reports/strategic-counsel-lanes-2026-10-14.md` — lane selection strategy
- `../reports/sandbox-fingerprint-research-2026-10-14.md` — sandbox FP research

Key enforcements: label_grammar cut as emission driver, POI regex
case-insensitive, packages demoted to tripwire, dbmining score demoted
to annotation, urlscan/wayback/crtsh noisy queries cut, uqtag= added
to lane 1. Do NOT re-enable cut rules without his explicit order.

## Orchestrator

`orchestrator.py` runs all lanes with shared dedup state
(`state/orchestrator_seen.json`), writes hits to
`state/morning-hits/hits-<ts>.jsonl`, pre-builds a factum bundle at
`state/morning-hits/bundle-<ts>.json`, prints the morning breakdown.

```bash
python3 orchestrator.py --since-hours 24          # full run
python3 orchestrator.py --dry-run                 # plan only
python3 orchestrator.py --json                    # machine output
```

The bundle is pre-built, not submitted: `factum.py` is too slow for
synchronous use on a 116k-record corpus. The cron worker submits it:
```
python3 ~/workspace/silent-locus/skills/factum/scripts/factum.py \
  --repo ~/workspace/silent-locus add --input <bundle_path>
```

## Schedule

**`swarm-scan-morning`** — daily 10:00 America/Chicago (owned by
`goal:urlquery-agent-activity-hunt`). Runs the orchestrator, submits
hits to factum, delivers the breakdown to the main chat. **Silent on
zero-hit days** (his preference).

## Rate limits

- urlquery: ~3s between API searches; ~11 queries per run; 429-throttled.
- ntfy: ~3s between polls; direct ntfy.sh BLOCKED at egress — module
  logs the gap, falls back to jina relay + Wayback CDX. A gap run emits
  zero hits and must never be read as a clean negative.
- urlscan: ~2s between queries; anonymous API.
- wayback: port 80 CDX; retry with 45-90s spacing on 504s.
- crtsh: 10s between patterns; **429 is a hard stop** (module aborts).
- packages: 0.5-1s between calls; unauthenticated public APIs.
- ipinfo.io ASN lookups: cached; 1s delay on cache miss.

## Config

`~/workspace/silent-locus/scripts/swarm-infra-config.json` — IOCs,
CIDRs, 16 cloud ASNs, tag patterns, per-lane query blocks. Extend as
new swarm infrastructure is identified; document every addition with
a `_comment` note and provenance entry.
