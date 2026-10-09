# EU Shodan Sweep — Agent Harness Traces

**Date:** 2026-10-05 | **Method:** Shodan API (`~/workspace/skills/shodan/bin/shodan.py`) only — `count` + `search` + `host`. Zero candidate hosts opened, fetched, or probed. All observations are Shodan stored banners/HTML.

**Scope:** hosts geolocated/org-attributed to Europe (DE/FR/NL/AT/CH/IT/ES/PL; EU orgs Hetzner, OVH, Scaleway, IONOS).

**Already covered (excluded from "new"):** the 14 shodan-chat-transcripts rows + IREN cluster (all in IP_LOG), the exposed-instance-hunt rows, OpenClaw 21k global census (KNOWN). Overlap re-hits below are annotated OURS, not re-reported.

**Evidence grades:** OBSERVED = in Shodan output. INFERENCE = interpretation. NULL = zero-count dork.

## Dork results (40 dorks: 18 nonzero, 22 null)

### Harness grammars — DE / Hetzner (OBSERVED counts)

| Dork | Count | Disposition |
|---|---|---|
| `http.html:".claude/projects" country:DE` | 1 | → row 1 |
| `http.html:".codex/sessions" country:DE` | 1 | OURS (195.62.49.85, prior row 7, in IP_LOG) |
| `http.html:"checkpoint_id" country:DE` | 2 | → row 2 (same host, ports 8000+443) |
| `http.html:".aider.chat.history.md" country:DE` | 0 | NULL |
| `http.html:".gemini/tmp" country:DE` | 0 | NULL |
| `http.html:".continue/sessions" country:DE` | 1 | → row 3 |
| `http.html:".claude.json" country:DE` | 12 | → row 6 (cluster) |
| `http.html:".claude/projects" org:Hetzner` | 2 | OURS (46.225.209.102, 46.225.51.127 — prior rows 2, 3) |
| `http.html:".codex/sessions" org:Hetzner` | 1 | OURS (46.225.88.73 — prior row 1) |
| `http.html:"checkpoint_id" org:Hetzner` | 2 | same host as DE hit (49.13.162.93) |
| `http.html:"saoudrizwan.claude-dev/tasks" country:DE` | 0 | NULL |
| `http.title:"Index of" ".claude" country:DE` | 0 | NULL |

### Harness grammars — FR / NL / OVH / Scaleway / IONOS / AT / CH / PL / IT / ES

| Dork | Count | Disposition |
|---|---|---|
| `http.html:".claude/projects" country:FR` | 0 | NULL |
| `http.html:".codex/sessions" country:FR` | 0 | NULL |
| `http.html:".claude/projects" org:OVH` | 0 | NULL |
| `http.html:".codex/sessions" org:OVH` | 1 | → row 4 (OVH CA tin, .fr domain) |
| `http.html:".claude/projects" country:NL` | 0 | NULL |
| `http.html:".codex/sessions" country:NL` | 0 | NULL |
| `http.html:"checkpoint_id" country:FR` | 0 | NULL |
| `http.html:".aider.chat.history.md" country:FR` | 0 | NULL |
| `http.html:".claude.json" country:FR` | 1 | → row 5 |
| `http.html:".claude/projects" org:Scaleway` | 0 | NULL |
| `http.html:".codex/sessions" org:Scaleway` | 0 | NULL |
| `http.html:".claude/projects" org:IONOS` | 0 | NULL |
| `http.html:".claude/projects" country:AT` | 0 | NULL |
| `http.html:".codex/sessions" country:AT` | 0 | NULL |
| `http.html:".claude/projects" country:CH` | 0 | NULL |
| `http.html:".claude/projects" country:PL` | 0 | NULL |
| `http.html:".claude/projects" country:IT` | 0 | NULL |
| `http.html:".claude/projects" country:ES` | 0 | NULL |
| `http.html:".codex/sessions" country:IT` | 0 | NULL |
| `http.html:".codex/sessions" country:ES` | 0 | NULL |

### EU chat-frontend census (OBSERVED counts, KNOWN products — title match ≠ missing auth)

| Dork | Count |
|---|---|
| `http.title:"OpenClaw" country:DE` | 2,200 |
| `http.title:"OpenClaw" port:18789 country:DE` | 1,194 |
| `http.title:"OpenClaw" country:FR` | 318 |
| `http.title:"Open WebUI" country:DE` | 2,747 |
| `http.title:"Open WebUI" country:FR` | 761 |
| `http.title:"LibreChat" country:DE` | 422 |
| `http.title:"SillyTavern" country:DE` | 73 |
| `http.html:".openclaw/agents" country:DE` | 5 (KNOWN product copy — nervix.ai, contynu.com, clawcat.com + 2; verified on 94.130.141.5: mail/Odoo box, not agent infra) |

## Candidate table (slim; full IPs preserved per no-redaction rule)

| # | IP | Port | Title (Shodan) | Grammar hit | Org / Country | Timestamp | Class |
|---|----|------|----------------|-------------|---------------|-----------|-------|
| 1 | 5.189.174.98 | 4321 | (none) | `.claude/projects` | Contabo GmbH / DE | 2026-09-15 | GENUINELY NEW |
| 2 | 49.13.162.93 | 8000 | (none) | `checkpoint_id` | Hetzner / DE | 2026-10-01 | GENUINELY NEW |
| 3 | 188.245.207.145 | 3000 | "Kora — Your personal, free AI desktop experience" | `.continue/sessions` | Hetzner / DE | 2026-09-28 | GENUINELY NEW |
| 4 | 148.113.247.201 | 443 | "code.benoitguivarch.fr" | `.codex/sessions` | OVH (vps.ovh.ca CA tin; .fr domain) | 2026-09-22 | GENUINELY NEW (low-confidence, geo-borderline) |
| 5 | 51.91.99.32 | 9090 | "Directory listing for /" | `.claude.json` | OVH SAS / FR | 2026-09-08 | GENUINELY NEW |
| 6 | .claude.json DE cluster (12) | various | "Directory listing for /" (most) | `.claude.json` | Contabo/Hetzner/DpkgSoft / DE | 2026-09-05 → 2026-10-05 | GENUINELY NEW (cluster) |

**Row 6 full IP list (OBSERVED):** 173.249.40.221:8080, 37.60.248.174:8080, 86.48.1.215:8877, 49.13.86.146:8099, 109.205.177.91:80, 38.242.194.175:8888, 49.12.43.92:9080, 207.180.193.40:8080, 144.91.67.10:8092, 45.10.160.35:9091, 150.241.106.107:8877, 116.202.96.244:18081.

## Notes on candidates (INFERENCE, unverified — Shodan stored observations only)

- **Row 1 (5.189.174.98:4321):** Contabo DE VPS (`vmi3275742.contaboserver.net`), ports 22 + 4321 only. Unusual high port serving a page whose HTML contains `.claude/projects` — INFERENCE: Claude Code project/session surface exposed on a nonstandard port. No page title.
- **Row 2 (49.13.162.93):** Hetzner DE (`static.93.162.13.49.clients.your-server.de`), ports 22/80/443/8000. nginx on 80 (404) and 443; port 8000 has no product/title but `checkpoint_id` in HTML — same port+grammar shape as the IREN checkpoint cluster (also port 8000). INFERENCE: checkpointed-agent session surface behind an nginx-fronted box.
- **Row 3 (188.245.207.145:3000):** Hetzner DE, "Kora — Your personal, free AI desktop experience" page contains `.continue/sessions`. Box also runs Ncat http proxy :443, PostgreSQL :5432, SSH on 22+2222. INFERENCE: AI desktop-app host leaking Continue.dev session paths in its served HTML; Ncat proxy is operator-tooling-shaped (echoes letss.win Ncat :2083, which counsel graded human/pentester).
- **Row 4 (148.113.247.201:443):** OVH CA tin (`vps-024164f0.vps.ovh.ca`) serving a `.fr` domain title; nginx on 80 (404) and 443. Geo-borderline: OVH is a French company and the operator domain is French, but the metal is Canadian — logged here with the caveat rather than claimed as EU. The `.codex/sessions` HTML hit is the only agent-shaped signal; title is a personal code domain — lowest-confidence lead in the table.
- **Row 5 (51.91.99.32:9090):** OVH FR VPS (`vps-a05749d0.vps.ovh.net`) running Python SimpleHTTPServer with an open `Directory listing for /` whose index contains the `.claude.json` filename — exposed Claude Code config surface. The box is a busy dev/test rig: Selenium Grid :4444, Portainer :9443, MongoDB :27017, Minecraft :25565, "TAF" :4400. INFERENCE: dev's working directory (with Claude Code config) accidentally served.
- **Row 6 (DE .claude.json cluster):** 12 hosts, 8× Contabo + 3× Hetzner + 1× DpkgSoft, all DE-geolocated, all with `.claude.json` in served HTML, mostly on odd high ports (8080/8877/8888/8099/9080/9091/8092/18081). Spot-checked: 173.249.40.221:8080 = SimpleHTTPServer "Directory listing for /" (box also runs Easypanel :443/:3000); 116.202.96.244:8080+:18081 = both "Directory listing for /". INFERENCE: a common recipe (dev VPS + Python http.server on a high port) leaking `.claude.json` filenames across a dozen DE boxes. Scanned 2026-09-05 → 2026-10-05 — ongoing, not a stale snapshot.

## Overlap annotations (OURS — not re-reported)

- `195.62.49.85:8123` ("Codex Messenger Login", proxy.ru) re-hit under `country:DE` as IT-GARAGE Labs Limited — prior study row 7, in IP_LOG.
- `46.225.88.73:443` ("Agent Relay") re-hit under `org:Hetzner` — prior study row 1, in IP_LOG.
- `46.225.209.102:3000` + `46.225.51.127:3000` ("Claude Projects", "RuntimeGuard") re-hit under `.claude/projects org:Hetzner` — prior study rows 2–3, in IP_LOG.

## Nulls (first-class, 22)

FR/NL/AT/CH/PL/IT/ES harness grammars all zero; Scaleway and IONOS zero; `.aider.chat.history.md` and `.gemini/tmp` zero across DE and FR; `saoudrizwan.claude-dev/tasks` DE zero; `Index of`+`.claude` DE zero. The EU harness-grammar signal concentrates in DE (Contabo/Hetzner) + OVH FR — nothing in southern/eastern EU or the Alps.

## Follow-ups (for parent agent)

1. Rows 1–6 are IP_LOG candidates (rows 1, 2, 3, 5, 6 as LEAD; row 4 as WATCHLIST with geo caveat).
2. Row 6 cluster: 12 DE boxes, same grammar — worth a passive re-sweep in a week; new members are high-value.
3. OpenClaw EU facet: DE 1,194 gateways on :18789 + FR 318 — operator-cluster faceting (by org) could find EU operator groups.
4. The user suspected EU traces — confirmed: the DE signal is real and concentrated on budget VPS providers (Contabo/Hetzner).
