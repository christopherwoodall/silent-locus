# 2026-09-28 Chinese Amap fleet — the main agent-fleet hunt

The central investigation tree for the suspected Chinese agent fleet (Amap /
Gaode task grammar, zz=oai markers, httpbun and dead-drop tradecraft).
`events.jsonl` (2,141 records) is the canonical normalized event file,
built by `build_events.py` from `raw/`.

## Core documents

| File | Contents |
|---|---|
| [PROVENANCE.md](PROVENANCE.md) | Data sources, collection windows, coverage and blind spots |
| [METHODOLOGY.md](METHODOLOGY.md) | The hunt manual — how lanes are run (living file, extended per run) |
| [LESSONS.md](LESSONS.md) | What the hunt found — distilled findings, living file |
| [PERSONA_MANIFEST.md](PERSONA_MANIFEST.md) | The investigator-persona roster and assignments |
| [SSLIP-REPORT.md](SSLIP-REPORT.md) | sslip.io wildcard-DNS exfil/beacon observation report (2026-10-05) |
| [slug-hunt.py](slug-hunt.py) | Cross-archive slug-presence sweep tooling |
| [IP_LOG.md](IP_LOG.md) · [ALL_LINKS.md](ALL_LINKS.md) | Observed IPs and link inventory |
| [RECOVERY.md](RECOVERY.md) | Recovery notes for the lane |
| writeup-idph-iowa.md · writeup-lhr-life.md | Analyst writeups (idph.iowa.gov, lhr.life infra) |

## Subdirectories

| Dir | Contents |
|---|---|
| [personas/](personas/) | Investigator-persona working dirs (e.g. `antiquarian/`, `cert-sleuth/`, `dead-drop-diver/`); each carries a `FINDINGS.md` |
| [raw/lanes/](raw/lanes/) | The lane raw material: `chinese-infra`, `deepseek-hunt`, `eval-hunt`, `github-code`, `osint`, `other-targets`, `urlscan`, `wayback`, `zhipu-hunt` |
| [studies/](studies/) | Deep-study lanes: [skill-egress-top500](studies/skill-egress-top500/), [skill-egress-top1000](studies/skill-egress-top1000/) (the skill-supply-chain egress scans and their why-these-sites link hunt), plus `eu-hunt/`, `msgboard-hunt-2/`, `wiki-hunt-2/`, `shodan-chat-transcripts/`, `WRITEUP-2026-10-05.md` |
| [german-french-swarm-hunt/](german-french-swarm-hunt/) | EUROSWARM — the German/French coordinator swarm hunt; verdict: no DE/FR swarm found. Own README inside |
| [live-monitor/](live-monitor/) | Polling monitors (`monitor.py` + numbered variants, `seen.json`, `LOG.md`, `FINDINGS.md`) |
| [infra-watchlist/](infra-watchlist/) | Standing infrastructure watchlist (`INFRASTRUCTURE-WATCHLIST.md`) |
| [village-join/](village-join/) | UUID-join run against the AI Village manifest (`VILLAGE-JOIN.md`, `VILLAGE-JOIN-2.md`, `WORKLOG.md`) |
| [counsel/](counsel/) | Adversarial review rounds (`CHARTER.md`, `CONTEXT.md`, `FINDINGS.md`, `rounds/`) |
| german-hunt/ · french-hunt/ · russian-hunt/ · spanish-hunt/ | Earlier language/locale-specific hunts (folded into the EUROSWARM assessment) |
| behavior-hunt/ · cross-swarm-vocab/ · dream-taiwan-swarm/ · farmable-surfaces/ · full-sweep/ · harness-logs/ · infra-sweep/ · new-fleets/ · pandalegacy/ · shortener-farm/ · urlscan-lhr/ | Specialized sweep lanes; each holds its own findings and raw pulls |

## Integrated report

The consolidated writeup covering this hunt plus the skill-egress studies and
the usemod.org ClipBoard follow-up lives at
[studies/skill-egress-top1000/INVESTIGATION-REPORT.md](studies/skill-egress-top1000/INVESTIGATION-REPORT.md).
