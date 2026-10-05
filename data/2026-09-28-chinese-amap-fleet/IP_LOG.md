# AGENT INFRASTRUCTURE IP LOG

*Started 2026-10-05 per BigSexyWarlock69: log IPs for agents/infrastructure we find. Agents and infra only — never human attribution. Every entry carries provenance and an evidence grade.*

| IP | ASN / Host | Role | First seen | Provenance | Grade |
|---|---|---|---|---|---|
| 178.63.67.106 | Hetzner AS24940 | webhook.site app infra (fleet inbox `6ddc559e` + fresh inbox `3b5027e4`) | 2026-10-05 | urlquery report metadata, dead-drop-diver | OBSERVED (service infra, KNOWN) |
| 62.234.187.97 | Tencent Cloud Beijing AS45090 | self-hosted Httpbun :8080 + "New API" LLM gateway :3000 | 2026-10-05 | Shodan stored observations, c2-pattern-analyst | LEAD (zero corpus hits) |
| 95.169.18.20 | IT7 Networks AS25820 | letss.win self-hosted Httpbun :8443 | 2026-10-05 | Shodan, c2-pattern-analyst + cert-sleuth (independent) | LEAD (corroborated 2x) |
| 207.57.145.214 | NTT AS1054 | letss.win self-hosted Httpbun :8443 | 2026-10-05 | Shodan, c2-pattern-analyst + cert-sleuth (independent) | LEAD (corroborated 2x) |
| 160.19.212.117 | Vietnam residential | self-hosted webhook.site clone + LLM tooling | 2026-10-05 | Shodan stored observations, c2-pattern-analyst | LEAD |
| 43.153.6.76 | Tencent (via Cloudflare challenge) | jina.orz.fit — jina-reader-like | 2026-10-05 | Shodan, cert-sleuth | LEAD |
| 47.84.112.179 | Alibaba | jina.qingchuan.cloud — jina-reader-like | 2026-10-05 | Shodan, cert-sleuth | LEAD |
| 43.108.48.133 | Alibaba SG | relay.woaifei.com — relay/jina-like | 2026-10-05 | Shodan, cert-sleuth | LEAD |
| 139.45.201.13 | RETN | presents jina.ai cert (not jina infra) | 2026-10-05 | Shodan, cert-sleuth | LEAD (single pivot) |
| 128.140.75.138 | Hetzner AS24940 | Ollama :443, hostname `sp-agent-2-bzc.kube.smartpromotion.az` (agent-named kube service) | 2026-10-05 | Shodan stored observations, exposed-instance-hunt | LEAD |
| 149.130.187.39 | Oracle Corporation | Ollama :443, hostname `agent.agendatucitavisual.com` | 2026-10-05 | Shodan stored observations, exposed-instance-hunt | LEAD |
| 100.29.190.103 | Amazon Technologies Inc. | Flowise :443, hostname `quycapp-agente.quycapp.co` (agent-builder, "agente" naming) | 2026-10-05 | Shodan stored observations, exposed-instance-hunt | LEAD |
| 75.146.94.94 | Comcast Cable (residential ISP) | OpenClaw control-UI :18789 (full agent control surface) | 2026-10-05 | Shodan stored observations, exposed-instance-hunt | LEAD (residential ISP — review keep/drop) |
| 119.91.57.121 | Tencent Cloud Beijing | llama.cpp :1234 (LM Studio default port) | 2026-10-05 | Shodan stored observations, exposed-instance-hunt | LEAD |
| 1.92.91.104 | Huawei Public Cloud | Dify :80 (representative of ~3k indexed Dify population) | 2026-10-05 | Shodan stored observations, exposed-instance-hunt | LEAD |

## Rules
- New entries append with date, provenance (persona/report), and grade.
- Grades: OBSERVED (our scan bytes) / PUBLIC SOURCE (linked) / LEAD (infra-shaped, uncorroborated) / KNOWN (documented service infra).
- An IP graduates from LEAD when it appears in scan corpora or a second independent source.
- Never add person-linked IPs. Infrastructure only.
