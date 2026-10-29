# Screening & Scanner Code

Consolidated index of all screening and scanner scripts used in the hunt.

In-repo scripts are symlinks (single source of truth). External connector
CLIs are copies — see PROVENANCE.md for their origin.

## Shodan (agent-harness hunting)

| Script | Origin | Use |
|--------|--------|-----|
| `shodan.py` | copy from custom.legacy-shodan | Host search, host details, result counts. Needs `PYTHONPATH=/opt/muse/skills/custom-connector-setup/bin` for credential surrogate. |

## URLQuery (agent-activity hunting)

| Script | Origin | Use |
|--------|--------|-----|
| `urlquery.py` | copy from custom.legacy-urlquery | URLQuery API client |
| `urlquery-htmx.py` | copy from custom.legacy-urlquery | Frontend XHR endpoint client |
| `urlquery-htmx-curl.py` | copy from custom.legacy-urlquery | Curl-based variant |
| `collect-uq.py` | symlink to ../collect_uq.py | Bulk URLQuery collection |
| `scanners-urlquery.py` | symlink to ../scanners/urlquery.py | Scanner-lane URLQuery module |

## Scanner lane modules

All symlinks to `../scanners/`. Run via `scanners-orchestrator.py`.

| Script | Purpose |
|--------|---------|
| `scanners-orchestrator.py` | Runs the scanner fleet |
| `scanners-common.py` | Shared helpers |
| `scanners-crtsh.py` | crt.sh certificate transparency |
| `scanners-ntfy.py` | ntfy.sh topic checks |
| `scanners-urlscan.py` | urlscan.io |
| `scanners-wayback.py` | Wayback Machine CDX |
| `scanners-packages.py` | Package registry (npm/PyPI/RubyGems) |
| `scanners-dbmining.py` | Database mining helpers |

Scanner docs: `../scanners/README.md`
False-positive lists: `../scanners/FALSE-POSITIVES-*.md`

## Crawlers & scouts

| Script | Target | Use |
|--------|--------|-----|
| `swarm-infra-crawler.py` | ../swarm-infra-crawler.py | Webhook.site creator-IP pivot crawler |
| `trajectory-scout.py` | ../trajectory-scout.py | Trajectory corpus scouting |
| `ip-classifier.py` | ../ip_classifier.py | IP classification helpers |

## Cairn panel crawler agents

Copies from `data/lanes/cairn-panels/working/` (2026-10-19). These are the
fleet worker scripts from the Cairn/Strix/Hermes panel hunt. See PROVENANCE.md.

| Script | Purpose |
|--------|---------|
| `cairn-fetch-panels.py` | Lantern: passive GET profiling of open panels (no POST/login) |
| `cairn-profile-panels.py` | Panel profile extraction and structuring |
| `cairn-harbor-pull.py` | Harbor: Shodan host detail pull |
| `cairn-build-inventory.py` | Host inventory builder from Shodan results |
| `cairn-lantern-fetch.py` | Lantern shard fetch worker |
