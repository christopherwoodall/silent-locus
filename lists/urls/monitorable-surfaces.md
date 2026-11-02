# Monitorable agent-infrastructure surfaces

Generated 2026-10-22. Every domain/service below leaves persistent,
queryable artifacts (listings, APIs, feeds, archives, scan corpora) —
these are monitorable, not mere observables. Pure observables (jina,
shorteners, per-token inboxes) are excluded. Package registries and
Docker Hub excluded per operator (2026-10-22).

Columns: **Type** = kind of service. **Source / connection** = where the
claim comes from (Factum lane + record count, or hunt origin).
**Artifacts** = what we store. **Watch** = which scanner/script polls it.

## Agent boards found by the hourly hunt (2026-10-20 → 2026-10-21)

| Domain | Type | Source / connection | Artifacts | Watch |
|---|---|---|---|---|
| swarmsay.com | Agent board + post office (open API, MCP, agent cards, handle registration) | Hourly slot-0, 2026-10-21; Factum batch d6982046 (PRIMARY) | data/lanes/general-hunt/raw/0/2026-10-21T204103Z/ (llms.txt + index.html + provenance + sha256) | slot-0 baseline |
| commons.dooza.ai | Agent board "Agent Commons" (HTTP/MCP/A2A, job board, rooms, agent card) | Hourly slot-0, 2026-10-21 | data/lanes/general-hunt/raw/0/2026-10-22T024041Z/ | slot-0 baseline |
| robots.wiki | Public agent board (MCP, OpenAPI, skill file, Atom feeds) | Hourly slot-0, 2026-10-20; Factum batch d6982046 (PRIMARY) | data/lanes/general-hunt/raw/0/2026-10-21T024000Z/ | slot-0 baseline |
| agenthaven.org | Agent messaging network (forum + E2E DMs, MCP, hourly witness record) | Hourly slot-0, 2026-10-20; Factum batch d6982046 (PRIMARY) | data/lanes/general-hunt/raw/0/2026-10-21T024000Z/ | slot-0 baseline |
| agentcolony.one | Agent colony (heartbeat-verified agents) | Hourly slot-0, 2026-10-21; Factum batch d6982046 (PRIMARY) | data/lanes/general-hunt/raw/0/2026-10-21T144100Z/ | slot-0 baseline |
| agent-message-board.kyle-hatcher.workers.dev | Zero-trust agent message board (v1 API, hash-chained) | Hourly slot-0, 2026-10-21; Factum batch d6982046 (PRIMARY) | data/lanes/general-hunt/raw/0/2026-10-21T084000Z/ | slot-0 baseline |
| smokesignal-arianaram.pythonanywhere.com | Agent guestboard (unauthenticated posts) | Hourly slot-0, 2026-10-20; Factum batch d6982046 (PRIMARY) | data/lanes/general-hunt/raw/0/2026-10-20T204000Z/ | slot-0 baseline |
| msgboard.dev | Agent board (passphrase-private channels + public mirror, llms.txt) | Hourly slot-0, 2026-10-21; Factum batch d6982046 (PRIMARY) | data/lanes/general-hunt/raw/0/2026-10-21T144100Z/ | slot-0 baseline |

## Tier-1 discovery endpoints (trajectory-domains.md)

| Domain | Type | Source / connection | Artifacts | Watch |
|---|---|---|---|---|
| agentsboard.org | Agent board, llms.txt | trajectory-domains Tier 1; Factum 25 records | endpoint-baseline.json (hash-tracked) | slot-0 baseline, surfacewatch |
| agents-agents-agents.com | Agent board, llms.txt | trajectory-domains Tier 1; Factum 24 records | endpoint-baseline.json | slot-0 baseline, surfacewatch |
| bboard.ai | Agent board, llms.txt | trajectory-domains Tier 1; Factum 36 records | endpoint-baseline.json | slot-0 baseline, surfacewatch |
| agentgateway.pythonanywhere.com | Agent gateway, mcp.json (dead — "Coming Soon") | trajectory-domains Tier 1; Factum 37 records | endpoint-baseline.json | slot-0 baseline, surfacewatch |
| tantive.space | Agent surface, skill.md | trajectory-domains Tier 1; Factum 105 records | endpoint-baseline.json | slot-0 baseline, surfacewatch |
| swarmmemo.com | Agent board | trajectory-domains Tier 1; Factum 17 records | endpoint-baseline.json | slot-0 baseline, surfacewatch |
| messageboardforaiagents.com | Agent board (dark since 2026-10-21) | trajectory-domains Tier 1; Factum 17 records | endpoint-baseline.json | slot-0 baseline, surfacewatch |
| swarm.termina.digital | Agent swarm surface | trajectory-domains Tier 1; Factum 248 records | Factum observations | urlquery/tag scans |
| thecolony.ai | Agent colony | trajectory-domains Tier 1; Factum 57 records | Factum observations | watchlist |
| aiforum.grok.me | Agent forum | trajectory-domains Tier 1; Factum 20 records | Factum observations | watchlist |
| moltbook.com | Agent social network | trajectory-domains Tier 1; Factum 16 records | Factum observations | watchlist |

## Agent boards from the Factum domain audit (2026-10-22)

| Domain | Type | Source / connection | Artifacts | Watch |
|---|---|---|---|---|
| commonlog.ai | Public agent log archive (`/a/<ID>`); coordination content incl. encrypted-messaging docs | Factum 813 records, lane 2026-08-25-commonlog-scan | Factum observations; openapi.json documents `/m`, `/m/{id}`, `/a/{id}`, `/stream` | slot-0 baseline (wired 2026-10-22) |
| jotspot.io | Public agent-conversation board | Factum 19 records, lanes 2026-08-21-public-board, agent-surfaces | Factum observations | slot-0 baseline (wired 2026-10-22) |
| nervesocket.com | Agent surface, `/paste/` | Factum 18 records, lanes 2026-09-03-collusion-manifest, agent-surfaces | Factum observations | slot-0 baseline (wired 2026-10-22; 502 at wiring) |
| public-board.com | Public board (older records, nature to re-verify) | Factum 16 records, lanes 2016-12-28-rmn-re, 2026-02-01-agent-convo-venues | Factum observations | slot-0 baseline (wired 2026-10-22) |
| openagentforum.com | Agent forum, pollable `/channels/<name>/messages/<uuid>/` | Factum 10 records, lanes 2026-02-01-agent-convo-venues, 2026-08-19-tantive-space | Factum observations | slot-0 baseline (wired 2026-10-22) |
| 1f916.ai | Agent forum with public API `/api/record/<user>`, on-chain treasury | Factum 7 records, lanes 2026-08-19-tantive-space, transluce-intel (Transluce #179) | Factum observations | slot-0 baseline (wired 2026-10-22) |
| agentchan.org | Agent imageboard, public threads | Factum 6 records, lanes 2018-05-09-paste-archive-gap, 2026-02-01-agent-convo-venues | Factum observations | slot-0 baseline (wired 2026-10-22) |
| agents-relay.com | Agent relay (DOWN — connection failed 2026-09-28 and 2026-10-22) | Factum 6 records, lanes 2026-02-01-agent-convo-venues, 2026-09-28-agents-relay-sweep | Factum observations | NOT wired (down) |
| universalagentforum.com | Agent forum | Factum 5 records, lanes 2026-08-19-tantive-space, site-captures | Factum observations | slot-0 baseline (wired 2026-10-22) |
| rentahuman.ai | Public agent bounty board (agents hiring humans) | Factum 5 records, lane transluce-intel (Transluce #166/#167/#179) | Factum observations | slot-0 baseline (wired 2026-10-22) |
| bookofbots.com | Agent surface, llms.txt | Factum 5 records, lanes 2026-08-19-tantive-space, site-captures | Factum observations | slot-0 baseline (wired 2026-10-22; llms.txt 301s to absurdtools.com) |
| openwitness.net | Public mirror of 1F916 forum (`/p/`, `/c/`) | Factum 4 records, lane transluce-intel | Factum observations | slot-0 baseline (wired 2026-10-22) |
| openagentchat.net | Agent pulse-check posts (`/p/<slug>`) | Factum 4 records, lane transluce-intel | Factum observations | slot-0 baseline (wired 2026-10-22) |
| agent-community.com | Agent board, public posts | Factum 3 records, lanes 2026-08-19-tantive-space, site-captures | Factum observations | slot-0 baseline (wired 2026-10-22; 500 at wiring) |
| agent-board.juleskreuer.eu | Agent board | Factum 3 records, lanes 2026-08-19-tantive-space, site-captures | Factum observations | slot-0 baseline (wired 2026-10-22) |
| botbook.space | Agent surface, llms.txt | Factum 3 records, lanes 2026-08-19-tantive-space, site-captures | Factum observations | slot-0 baseline (wired 2026-10-22) |
| signpost.public-agents.ai | Agent surface, llms.txt | Factum 3 records, lanes 2026-08-19-tantive-space, site-captures | Factum observations | slot-0 baseline (wired 2026-10-22) |
| messages.directory | Agent message directory | Factum 3 records, lane 2026-08-19-tantive-space | Factum observations | slot-0 baseline (wired 2026-10-22) |
| pursekeeper.dev | Agent `/offers` board | Factum 3 records, lane 2026-08-19-tantive-space | Factum observations | slot-0 baseline (wired 2026-10-22) |
| hermes-agent.nousresearch.com | Live Hermes Agent deployment (docs/messaging endpoints) | Factum 3 records, lanes 2026-08-25-commonlog-scan, 2026-10-11-hf-traj-hermes | Factum observations | slot-0 baseline (wired 2026-10-22) |

## Paste / raw-file archives

| Domain | Type | Source / connection | Artifacts | Watch |
|---|---|---|---|---|
| anna.fyi | Paste archive (`/view/raw/<id>`) | Factum 179 records, lanes 2018-05-09-paste-archive-gap, 2026-05-27-paste-archive | Factum observations | Wayback CDX target (wired 2026-10-22) |
| paste.linuxiarz.pl | Paste archive | Factum 295 records, lanes 2026-05-17-iowacollab-pastes, 2026-05-26-paste-linuxiarz | Factum observations | Wayback CDX target (wired 2026-10-22) |
| pastebin.k4be.pl | Paste archive | Factum 229 records, lanes 2025-10-24-pastebin-k4be, 2026-05-27-paste-archive | Factum observations | Wayback CDX target (wired 2026-10-22) |
| pastebin.tarcseh.me | Paste archive | Factum 25 records, lanes agent-surfaces, site-captures | Factum observations | Wayback CDX target (wired 2026-10-22) |
| paste.rs | Paste archive | Factum 10 records, lane 2026-08-19-tantive-space | Factum observations | Wayback CDX target (wired 2026-10-22) |
| nicepaste.com | Paste archive | Factum 6 records, paste lanes | Factum observations | Wayback CDX target (wired 2026-10-22) |
| paste.ubuntu.org.cn | Paste archive | Factum 5 records, paste lanes | Factum observations | watchlist |
| pastebox.to | Paste archive | Factum 4 records, paste lanes | Factum observations | watchlist |
| tmpfiles.org | Temp file host | Factum 4 records, paste lanes | Factum observations | Wayback CDX target (wired 2026-10-22) |
| infinitypaste.club | Paste archive | Factum 4 records, paste lanes | Factum observations | watchlist |
| porkpad.com / pasteview.com / gritpost.com / gotit.pub / mcbin.dev | Paste archives | Factum 3 records each, lanes 2018-05-09-paste-archive-gap, pastebin-cluster-sweep | Factum observations | watchlist |
| bytebin.lucko.me / bytebin.rkslot.nl | Byte-bin raw hosts | Factum 3 records each, lanes 2026-09-28-chinese-amap-fleet, slow-swarm-crawl | Factum observations | watchlist |
| paste.ee | Paste archive | Hunt watchlist (standing) | Wayback captures | wayback scanner |
| ubuntu paste (paste.ubuntu.com) | Paste archive (cityb dead-drop venue, Transluce #195) | Transluce finding 195 | Factum observations | watchlist |
| rentry.co | Markdown paste host | Hunt watchlist (standing) | — | watchlist |

## Scan corpora & code/dataset hubs

| Domain | Type | Source / connection | Artifacts | Watch |
|---|---|---|---|---|
| urlquery.net | Scan-report corpus (2,341 Factum records) | Hunt primary source; crawler lane | data/lanes/urlquery-*/raw/, scanner state | urlquery scanner (12 query families incl. r.jina.ai/) |
| urlscan.io | Scan corpus | Hunt primary source | scanner state, evidence dirs | urlscan scanner (14 queries incl. domain:r.jina.ai) |
| github.com | Code + issues (596 Factum records) | Hunt primary source | Factum observations | narrow harness lane, reposcout (disabled) |
| huggingface.co | Datasets + models (489 Factum records) | Hunt primary source | Factum observations | reposcout watchlist (disabled), trajectory fleets |

## Certificate / host / archive intel

| Domain | Type | Source / connection | Artifacts | Watch |
|---|---|---|---|---|
| crt.sh | Certificate transparency | Hunt intel source | scanner state, evidence dirs | crtsh scanner (Tier-1/5 domains) |
| shodan.io | Banner/host intel | Cairn hunt phase 1+2 (3,354 hosts, 247 open dashboards) | data/lanes/cairn-panels/, scanner state | shodan scanner (5 count queries + facets) |
| web.archive.org | Web archive (CDX) | Hunt intel source (237 Factum records) | evidence dirs, wayback-baseline.json | wayback scanner (12 targets) |
| Common Crawl index | Web archive index | Proposed 2026-10-22 | — | not yet wired |
| otx.alienvault.com | Threat-intel pulses (keyless indicator API live) | Wired 2026-10-22 (iocfeeds lane 14) | scripts/scanners/state/iocfeeds_seen.json | iocfeeds scanner (21 indicators) |
| urlhaus.abuse.ch | Malicious-URL feed (needs free abuse.ch key — disabled) | Wired 2026-10-22 (documented, not polled) | — | needs API key |
| threatfox.abuse.ch | IOC feed (needs free abuse.ch key — disabled) | Wired 2026-10-22 (documented, not polled) | — | needs API key |

## Wikis, blogs, misc

| Domain | Type | Source / connection | Artifacts | Watch |
|---|---|---|---|---|
| Wikipedia + 9 wikis (MediaWiki APIs) | Wiki revision histories (Lifeval hunt: 8 temp accounts, 1,087 revisions) | Wikipedia AI-edit hunt lane | reports/, Factum observations | revision-history grep method (on demand) |
| swarmcha.se | Intel blog (agent-incident research) | Hunt intel source; Factum 3 records | jina-reader fetches | jina scanner watchlist |
| norforge.com | Intel blog ("Inside Cairn") | Hunt intel source | jina-reader fetches | jina scanner watchlist |
| any.run | Malware sandbox w/ public API (needs key — not wired) | Factum 6 records, lane anyrun-scan | Factum observations | needs API key |
| pkg.go.dev / Go module proxy | Module proxy (ZERO Factum hits — unproven) | Watchlist (no evidence either way) | — | watchlist (unproven) |

## Confirmed-malicious panels (Counsel-verified, passive GET only)

| URL | Type | Source / connection | Artifacts | Watch |
|---|---|---|---|---|
| http://185.242.245.159:8000 | Malicious Cairn panel (4 projects, 2 active) | Cairn phase-2, Counsel MALICIOUS | data/lanes/cairn-panels/ (70 projects, 234 files, 48.7 MB) | cairnwatch (disabled, needs his word) |
| http://31.56.206.187:8000 | Malicious Cairn panel (24 projects, 5 active) | Cairn phase-2, Counsel MALICIOUS | data/lanes/cairn-panels/ | cairnwatch (disabled) |
| http://31.57.47.29:8000 | Malicious Cairn panel (19 projects, 6 active) | Cairn phase-2, Counsel MALICIOUS | data/lanes/cairn-panels/ | cairnwatch (disabled) |
| http://31.59.92.155:8000 | Malicious Cairn panel (23 projects, 5 active) | Cairn phase-2, Counsel MALICIOUS | data/lanes/cairn-panels/ | cairnwatch (disabled) |

## Borderline — operator call pending

| Domain | Type | Source / connection | Note |
|---|---|---|---|
| my.diffend.io | Package-scanner UI (816 Factum records) | Factum lanes (own sweep hit /gems pages) | Scanner service, not a registry — adjacent to excluded package repos |
| rubyhack.ai | Unverified (likely threat-intel blog, 9 records) | GemStuffer timeline lanes | Nature unverified |
| eval.ai | Eval leaderboard platform (4 records) | Factum lanes | Off-mission |
