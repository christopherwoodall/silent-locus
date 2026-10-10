# AGENT INFRASTRUCTURE IP LOG

*Started 2026-10-05 per BigSexyWarlock69: log IPs for agents/infrastructure we find. Agents and infra only — never human attribution. Every entry carries provenance and an evidence grade.*

| IP | ASN / Host | Role | First seen | Provenance | Grade |
|---|---|---|---|---|---|
| 178.63.67.106 | Hetzner AS24940 | webhook.site's own host IP / urlquery scan-pool node — NOT operator infra (corrected Round 1, jock: report c9104bb8 target IP .106 vs exit IP .153 are different fields) | 2026-10-05 | urlquery report metadata, dead-drop-diver; corrected counsel Round 1 | OBSERVED (service infra, KNOWN) |
| 62.234.187.97 | Tencent Cloud Beijing AS45090 | self-hosted Httpbun :8080 + "New API" LLM gateway :3000 — KILLED as agent-infra Round 1 (personal dev VPS: 48k-star OSS gateway, default nginx page). Do not cite as agent-linked. | 2026-10-05 | Shodan stored observations, c2-pattern-analyst; killed counsel Round 1 (adversary) | KILLED (was LEAD) |
| 95.169.18.20 | IT7 Networks AS25820 | letss.win self-hosted Httpbun :8443 — WOUNDED Round 1: unattributed infra oddity, agent-linkage dead (Ncat :2083 points human/pentester) | 2026-10-05 | Shodan, c2-pattern-analyst + cert-sleuth (independent); wounded counsel Round 1 | WATCHLIST (was LEAD) |
| 207.57.145.214 | NTT AS1054 | letss.win self-hosted Httpbun :8443 — WOUNDED Round 1: unattributed infra oddity, agent-linkage dead | 2026-10-05 | Shodan, c2-pattern-analyst + cert-sleuth (independent); wounded counsel Round 1 | WATCHLIST (was LEAD) |
| 160.19.212.117 | Vietnam residential | self-hosted webhook.site clone + LLM tooling | 2026-10-05 | Shodan stored observations, c2-pattern-analyst | LEAD |
| 43.153.6.76 | Tencent | jina.orz.fit — KILLED as agent infra Round 1 (personal AI-dev domain; agents use only official reader endpoints in 96k events). Watchlist only. | 2026-10-05 | Shodan, cert-sleuth; killed counsel Round 1 (adversary) | KILLED (was LEAD) |
| 47.84.112.179 | Alibaba | jina.qingchuan.cloud — KILLED as agent infra Round 1 (personal AI-dev domain). Farm mapping survives as watchlist (see 120.92.213.103). | 2026-10-05 | Shodan, cert-sleuth; killed counsel Round 1 (adversary) | KILLED (was LEAD) |
| 43.108.48.133 | Alibaba SG | relay.woaifei.com — KILLED as agent infra Round 1 (personal AI-dev domain). Watchlist only. | 2026-10-05 | Shodan, cert-sleuth; killed counsel Round 1 (adversary) | KILLED (was LEAD) |
| 139.45.201.13 | RETN | Self-signed O=Jina AI cert on exposed Supermicro BMC login; real jina.ai = GCP/GTS certs. Imposter — honeypot/misdirection/cover. Zero corpus hits. | 2026-10-05 | Shodan stored observations, counsel Round 1 (thug) | WATCHLIST (was LEAD) |
| 128.140.75.138 | Hetzner AS24940 | Ollama :443, hostname `sp-agent-2-bzc.kube.smartpromotion.az` (agent-named kube service) | 2026-10-05 | Shodan stored observations, exposed-instance-hunt | LEAD |
| 149.130.187.39 | Oracle Corporation | Ollama :443, hostname `agent.agendatucitavisual.com` | 2026-10-05 | Shodan stored observations, exposed-instance-hunt | LEAD |
| 100.29.190.103 | Amazon Technologies Inc. | Flowise :443, hostname `quycapp-agente.quycapp.co` (agent-builder, "agente" naming) | 2026-10-05 | Shodan stored observations, exposed-instance-hunt | LEAD |
| 75.146.94.94 | Comcast Cable (residential ISP) | OpenClaw control-UI :18789 (full agent control surface) | 2026-10-05 | Shodan stored observations, exposed-instance-hunt | LEAD (residential ISP — review keep/drop) |
| 119.91.57.121 | Tencent Cloud Beijing | llama.cpp :1234 (LM Studio default port) | 2026-10-05 | Shodan stored observations, exposed-instance-hunt | LEAD |
| 1.92.91.104 | Huawei Public Cloud | Dify :80 (representative of ~3k indexed Dify population) | 2026-10-05 | Shodan stored observations, exposed-instance-hunt | LEAD |
| 43.173.89.2 | Tencent ACEVILLE | openai.orz.fit — 2nd node in orz.fit farm (jina/openai/openrouter), snake-game decoy page, active 2026-10-04. Zero corpus hits. | 2026-10-05 | Shodan stored observations, counsel Round 1 (thug) | WATCHLIST |
| 120.92.213.103 | Kingsoft Beijing | Open WebUI + `aiapi.qingchuan.cloud` cert — qingchuan LLM-API farm node across 3 Chinese clouds. Zero corpus hits. | 2026-10-05 | Shodan stored observations, counsel Round 1 (thug) | WATCHLIST |
| 8.133.171.245 | Alibaba | qingchuan farm node. Zero corpus hits. | 2026-10-05 | Shodan stored observations, counsel Round 1 (thug) | WATCHLIST |
| 8.148.145.174 | Alibaba | qingchuan farm node. Zero corpus hits. | 2026-10-05 | Shodan stored observations, counsel Round 1 (thug) | WATCHLIST |
| 121.196.245.158 | Alibaba | qingchuan farm node. Zero corpus hits. | 2026-10-05 | Shodan stored observations, counsel Round 1 (thug) | WATCHLIST |
| 46.225.88.73 | Hetzner AS24940 | "Agent Relay" :443 (`.codex/sessions` in HTML); same host runs "Droidrun — AI Mobile Automation Framework" :8081. Three agent-titled Hetzner hosts indexed 2026-10-04/05 — possible shared recipe. UNVERIFIED (Shodan stored observation only). | 2026-10-05 | Shodan stored observations, shodan-chat-transcripts study | LEAD |
| 46.225.209.102 | Hetzner AS24940 | "Claude Projects" :3000 (`.claude/projects` in HTML). UNVERIFIED. | 2026-10-05 | Shodan stored observations, shodan-chat-transcripts study | LEAD |
| 46.225.51.127 | Hetzner AS24940 | "RuntimeGuard" :3000 (`.claude/projects` in HTML). UNVERIFIED. | 2026-10-05 | Shodan stored observations, shodan-chat-transcripts study | LEAD |
| 43.139.127.232 | Tencent Beijing AS45090 | "Remote Codex Workbench" :80 (`.codex/sessions` in HTML). UNVERIFIED. | 2026-10-05 | Shodan stored observations, shodan-chat-transcripts study | LEAD |
| 120.48.48.120 | Baidu | "Codex Web" :8765 (`.codex/sessions` in HTML). UNVERIFIED. | 2026-10-05 | Shodan stored observations, shodan-chat-transcripts study | LEAD |
| 134.209.40.131 | DigitalOcean | "Codex Web" :3001 (`.codex/sessions` in HTML). UNVERIFIED. | 2026-10-05 | Shodan stored observations, shodan-chat-transcripts study | LEAD |
| 195.62.49.85 | proxy.ru | "Codex Messenger Login" :8123 (`.codex/sessions` in HTML; login page implies auth present). UNVERIFIED. | 2026-10-05 | Shodan stored observations, shodan-chat-transcripts study | LEAD |
| 43.134.83.249 | Tencent | Open directory listing :80 serving `.aider.chat.history.md` filename in index HTML — strongest transcript-exposure signal. UNVERIFIED. | 2026-10-05 | Shodan stored observations, shodan-chat-transcripts study | LEAD |
| 207.58.153.134 | SMV/Leaseweb | Open directory listing :8081 serving `.aider.chat.history.md` filename in index HTML. UNVERIFIED. | 2026-10-05 | Shodan stored observations, shodan-chat-transcripts study | LEAD |
| 117.55.229.221 | UberGlobal | "Prompt Recorder" :18081 (`.gemini/tmp` in HTML), hostname `codex.74.11288211.xyz`. UNVERIFIED. | 2026-10-05 | Shodan stored observations, shodan-chat-transcripts study | LEAD |
| 185.195.255.124 | Veganet (TR) | Open Python http.server listing :8000 serving `.claude.json`; also "TedussAI Mainframe" :8002. UNVERIFIED. | 2026-10-05 | Shodan stored observations, shodan-chat-transcripts study | LEAD |
| 49.234.49.58 | Tencent Beijing | Open Python http.server listing :8080 serving `.claude.json`. UNVERIFIED. | 2026-10-05 | Shodan stored observations, shodan-chat-transcripts study | LEAD |
| 178.104.186.30 | Hetzner AS24940 | Open Python http.server listing :8080 serving `.claude.json`. UNVERIFIED. | 2026-10-05 | Shodan stored observations, shodan-chat-transcripts study | LEAD |
| 161.115.132.6, 161.115.128.147, 161.115.128.148, 161.115.128.142, 161.115.132.5 | IREN | Checkpoint cluster: all :8000, all `checkpoint_id` in HTML, scanned 2026-09-20/21. Host-detail lookups failed (API truncation) — unresolved. UNVERIFIED. | 2026-10-05 | Shodan stored observations, shodan-chat-transcripts study | LEAD (cluster) |
| 159.146.96.208 | TurkNet AS12735 (TR) | Seeded identical `PublicBoard` relay pages on nine farm wikis in 90 min on 2026-09-06; same address as ProbierWiki's `AnthropicAgentBeta` handle. Unattributed relay seeder. | 2026-10-05 | wiki-hunt-2 study (public investigator research, surfaces.md) | WATCHLIST |
| 5.189.174.98 | Contabo DE | `.claude/projects` in HTML on bare high port 4321 (ports 22+4321 only). UNVERIFIED. | 2026-10-05 | Shodan stored observations, eu-shodan study | LEAD |
| 49.13.162.93 | Hetzner DE | `checkpoint_id` in HTML on port 8000 (nginx-fronted). Same port+grammar shape as IREN checkpoint cluster — second checkpointed-agent-shaped surface. UNVERIFIED. | 2026-10-05 | Shodan stored observations, eu-shodan study | LEAD |
| 188.245.207.145 | Hetzner DE | "Kora — AI desktop experience" :3000 leaking `.continue/sessions` in HTML; Ncat proxy :443, PostgreSQL :5432. UNVERIFIED. | 2026-10-05 | Shodan stored observations, eu-shodan study | LEAD |
| 148.113.247.201 | OVH (CA tin, .fr domain) | `.codex/sessions` in HTML :443. Geo-borderline: French company/domain, Canadian metal. Lowest-confidence lead. UNVERIFIED. | 2026-10-05 | Shodan stored observations, eu-shodan study | WATCHLIST (geo caveat) |
| 51.91.99.32 | OVH FR | Open Python http.server listing :9090 serving `.claude.json`; busy dev rig (Selenium, Portainer, MongoDB). UNVERIFIED. | 2026-10-05 | Shodan stored observations, eu-shodan study | LEAD |
| 173.249.40.221, 37.60.248.174, 86.48.1.215, 49.13.86.146, 109.205.177.91, 38.242.194.175, 49.12.43.92, 207.180.193.40, 144.91.67.10, 45.10.160.35, 150.241.106.107, 116.202.96.244 | Contabo/Hetzner/DpkgSoft DE | DE `.claude.json` cluster (12 hosts): open directory listings on odd high ports (8080/8877/8888/8099/9080/9091/8092/18081) serving `.claude.json` filenames. Common recipe: dev VPS + Python http.server. Scanned 2026-09-05→2026-10-05, ongoing. UNVERIFIED. | 2026-10-05 | Shodan stored observations, eu-shodan study | LEAD (cluster) |

*Population note 2026-10-05:* `http.title:"OpenClaw"` → 33,679 hosts, 21,142 on default gateway port 18789 (KNOWN open-source product; exposure scale genuinely new). Chat-frontend census: Open WebUI 22,568 · LibreChat 3,251 · SillyTavern 1,541 · ChatGPT-Next-Web 607 · LobeChat 564 · Ollama 154 · Chatbox 118 · KoboldAI 33 · LM Studio 15 (title match ≠ missing auth; census only). Full dork log: `studies/shodan-chat-transcripts/dorks.log`.

## Rules
- New entries append with date, provenance (persona/report), and grade.
- Grades: OBSERVED (our scan bytes) / PUBLIC SOURCE (linked) / LEAD (infra-shaped, uncorroborated) / KNOWN (documented service infra).
- An IP graduates from LEAD when it appears in scan corpora or a second independent source.
- Never add person-linked IPs. Infrastructure only.
