# EU University & Org Infrastructure Hunt

**Date:** 2026-10-05 | **Lane:** RAGTAG LANE 3 — European academic/org infra
**Method:** public sources only — web search (DE/FR/NL/PL/IT), Shodan stored observations (`~/workspace/skills/shodan/bin/shodan.py`), certificate-index attempt (crt.sh, timed out — NULL method). No host probed, no candidate fetched. Public shortener-stats pages: none reachable without a known short URL (YOURLS `+` stats need the short link).
**Evidence grades:** OBSERVED = in Shodan/search output. INFERENCE = interpretation. NULL = checked, nothing agent-shaped.
**Exclusions (already covered):** UNM/ETH Zürich shorteners (university-shorteners index), DSEWiki farm (german-hunt), msgboard.dev/thecolony.ai/litterbox, foragents.site (honeypot rule).

## Headline

The global YOURLS census (84 hosts, Shodan `http.title:"YOURLS"`, 2026-10-05) contains **three live EU-university shorteners** not in our index: Uni Siegen (`u-si.de`), RPTU Kaiserslautern-Landau (`short.zidis.rptu.de`), Université Côte d'Azur (Renater net). Plus a likely Hochschule Rhein-Waal shortener (`hsrw.info`) and a Renater-hosted `url.rezo-rm.fr`. None show agent-shaped use in stored observations — they are new SURFACES, not new catches.

## GENUINELY NEW surfaces (EU academic shorteners)

| # | Domain / IP | Org (Shodan) | Signal | Class |
|---|-------------|--------------|--------|-------|
| 1 | u-si.de / 141.99.2.122 | Universitaet Siegen (DFN) | YOURLS title on `u-si.de` + `u-si.zimt.uni-siegen.de` (ZIMT = uni IT center). Scanned 2026-10-02. | GENUINELY NEW surface |
| 2 | short.zidis.rptu.de / 131.246.122.209 | RPTU Kaiserslautern-Landau | YOURLS title on ZIDiS (teaching-innovation center) shortener subdomain. Scanned 2026-09-15. | GENUINELY NEW surface |
| 3 | 134.59.204.83 (webcom.univ-cotedazur.fr) | UNIVERSITE COTE D'AZUR (Renater) | YOURLS title on univ-cotedazur.fr infra. Scanned 2026-10-03. | GENUINELY NEW surface |
| 4 | hsrw.info / 80.158.76.188 | T-Systems (hsrw = Hochschule Rhein-Waal) | YOURLS title on `hsrw.info`. INFERENCE: Hochschule Rhein-Waal shortener. Scanned 2026-09-05. | GENUINELY NEW surface (INFERENCE on attribution) |
| 5 | url.rezo-rm.fr / 193.48.225.77 | Renater | YOURLS title. `rezo-rm.fr` — likely French research-network shortener. Scanned 2026-09-29. | GENUINELY NEW surface |

## OURS overlap (corroboration, not new)

- **2dd.pl** — Shodan YOURLS instance (82.223.111.176, arsys.es/IONOS ES). Already in our corpus as a top referrer on UNM `goto.unm.edu/7t6-o` (45 hits, proxy-class referrer). Now typed: it is a YOURLS shortener, not just a referrer domain. OVERLAP annotation.

## EU harness-grammar dorks (Shodan, stored observations)

| Dork | DE | FR | Detail |
|------|----|----|--------|
| `http.title:"Jupyter"` | 586 | 277 | academic filter: DE 5 (Stuttgart RUS/NFDI JupyterHub, LRZ :9999, LMU-Klinikum :10000, PH Ludwigsburg project-energise, +1 industrial false positive); FR 3 (CentraleSupélec docker workers odd ports 12578/14524, CNRS in2p3.fr IFB/LAL cloud, ENS Lyon). All KNOWN legit research infra, no agent signal |
| `http.title:"JupyterHub"` | 377 (DE) | — | census only |
| `http.html:".claude/projects"` | 1 | 0 | 5.189.174.98:4321 Contabo VPS — non-academic, off-lane |
| `http.html:".codex/sessions"` | 1 | 0 | 195.62.49.85:8123 proxy.ru — OURS, already in IP_LOG (shodan-chat-transcripts row 7); second-dork corroboration |
| `http.html:"checkpoint_id"` | 2 | — | 49.13.162.93 (Hetzner) :8000 + :443 — non-academic VPS, off-lane |
| `http.html:".aider.chat.history.md"` | 0 | — | NULL |

## Academic paste services (Shodan `http.title:"PrivateBin"` — DE 134, FR 81, NL 27, Renater 0)

| # | Host | Org | Signal | Class |
|---|------|-----|--------|-------|
| 6 | paste02.belwue.de (2001:7c0:0:253::6) | BelWü (Baden-Württemberg state university network) | Institutional paste service for BW universities | GENUINELY NEW surface |
| 7 | privatebin.pks.mpg.de / privatebin.mpipks-dresden.mpg.de (193.174.246.58) | DFN / Max Planck | MPI for Physics of Complex Systems (Dresden) PrivateBin | GENUINELY NEW surface |

Both legit institutional pastebins; no agent-shaped use observable in stored banners — surfaces, not catches.

## Notes

- **vitoux.eu** (37.187.101.45, OVH, FR): personal French self-hosted stack — `notebook.vitoux.eu`, `paste.vitoux.eu`, `wiki.vitoux.eu`, `board.vitoux.eu` on one box. Not academic, not agent-named. Logged as EU infra curiosity; no agent signal in stored banner.
- **go.odisee.be / qr.odisee.be**: Odisee (Belgian hogeschool) shortlink/QR service per their public ICT docs (account-gated). Not YOURLS (custom). Logged as surface.
- **TU Chemnitz Kurz-URL-Dienst**: documented 2015 URZ publication; no current YOURLS title hit in Shodan census. Possibly retired or re-homed. NULL as live surface.
- **TH Nürnberg "Wiki Digitale Lehre"** (leko.service.th-nuernberg.de): live German academic DokuWiki (teaching tools). No agent-shaped content in search snippets. NULL.

## Honest nulls

- crt.sh wildcard queries for `jupyter`/`notebook` under EU academic domains: timed out / non-JSON (rate-limited). Method NULL, not a finding.
- PL/IT/NL web searches for university shorteners: marketing noise only. NULL.
- `http.html:".aider.chat.history.md" country:DE` → 0. NULL.
- `http.html:".claude/projects" country:FR` → 0. NULL.
- `http.title:"PrivateBin" org:"Renater"` → 0. NULL.
- No agent-shaped use observed on ANY of the 7 new EU academic surfaces — they are new watchlist surfaces, not catches. The honest headline: European universities run plenty of agent-USEFUL infra (shorteners, JupyterHubs, pastebins), but zero agent-shaped activity was found on it in this pass.

## Follow-ups

1. YOURLS `+` stats on u-si.de / short.zidis.rptu.de / webcom.univ-cotedazur.fr — needs a known short URL per instance; watch for indexed short links.
2. Jupyter DE/FR academic-org filter (586/277) — pull orgs, flag DFN/Renater/RENATER/GARR/SURFNET/SWITCH/RedIRIS/PSNC nets.
3. Re-run harness-grammar dorks for NL/AT/CH/IT/ES/PL.
