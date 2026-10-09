# LANE 2 — Passive exposed-instance hunt: agent/inference infrastructure

*Date: 2026-10-05. STRICTLY PASSIVE: Shodan stored observations + web search only. No candidate was connected to, probed, authenticated against, or fetched. Agents and infrastructure only — no human/operator identity work.*

## Method

1. Read `~/workspace/skills/shodan/SKILL.md`; used the curl-based CLI `~/workspace/skills/shodan/bin/shodan.py` (`count` / `search` / `host`). Shodan had intermittent timeouts — all queries used generous timeouts and succeeded with retries.
2. Shodan queries, in order:
   - Inference endpoints: `product:"Ollama" port:11434` → **13,734** indexed; agent-flavored refinements (`openhermes`, `functionary`, `gorilla`, `nexusraven` → 0 each; `"agent"` → 6); `product:"Ollama" hostname:"agent"` → 2; `product:"Ollama" http.title:"Claude"` → 0; `http.title:"Ollama"` → 154; `http.title:"LM Studio"` → 15.
   - Other servers: `product:"llama.cpp"` → 1,781 (426 on :8080); `port:1234 "lmstudio"` → 6; `port:8000 "vllm"` → 3; `product:"Jan"` → 1; `port:7860 product:"Gradio"` → 0; `port:7860 "gradio"` → 0 (text-generation-webui not fingerprinted).
   - Agent builders: `http.title:"OpenClaw"` → 33,669; `http.title:"Flowise"` → 4,047; `http.title:"Dify"` → 2,964 (2,982 in sample pull); `http.title:"Langflow"` → 2,994; `http.title:"n8n"` → 292; `http.title:"ComfyUI"` → 187,977; `http.title:"RAGFlow"` → 1,662; `port:18789` → 198,478 (raw port count, mostly non-OpenClaw — not a clean signal).
   - Follow-ups: full host records for the 2 "agent"-hostname Ollama instances and the top `vllm` match to verify keyword context.
3. Web searches for: exposed-Ollama research (found Mysterium VPN Sep-2026 census + SentinelOne/Censys Jan-2026 study — corroboration), `intitle:"index of" ".claude"` (polluted, GitHub hits only), aider.chat.md exposure, OpenClaw state exposure, gist transcripts, S3 buckets with agent state, Docker Hub baked agent state.

## Lead table (Shodan-indexed, uncorroborated unless noted)

| IP / URL | What it is | Grade | Provenance |
|---|---|---|---|
| 128.140.75.138 :443 (Hetzner) | Ollama, hostname `sp-agent-2-bzc.kube.smartpromotion.az` — agent-named k8s service | LEAD | Shodan stored obs, 2026-09-27 |
| 149.130.187.39 :443 (Oracle) | Ollama, hostname `agent.agendatucitavisual.com` | LEAD | Shodan stored obs, 2026-09-16 |
| 100.29.190.103 :443 (AWS) | Flowise, hostname `quycapp-agente.quycapp.co` — agent-builder endpoint, "agente" naming | LEAD | Shodan stored obs, 2026-10-05 |
| 75.146.94.94 :18789 (Comcast residential) | OpenClaw control-UI default port — full agent control surface | LEAD (residential ISP — review keep/drop) | Shodan stored obs, 2026-10-05 |
| 119.91.57.121 :1234 (Tencent Beijing) | llama.cpp banner on LM Studio's default port — inference endpoint | LEAD | Shodan stored obs, 2026-09-30 |
| 1.92.91.104 :80 (Huawei Cloud) | Dify — representative of ~3k indexed Dify population | LEAD | Shodan stored obs, 2026-10-05 |
| 144.76.75.252 :8000 (Hetzner, meschkat-it.de) | matched `port:8000 "vllm"` but host record shows no product/banner/title evidence | WEAK (not logged) | Shodan stored obs, 2026-09-30 |

All 6 strong leads appended to `../IP_LOG.md` (rows verified absent from existing log first; none overlapped).

## Corroborated public-source context (no new IPs)

- **Mysterium VPN Research, Sep 2026** ([letsdatascience.com](https://letsdatascience.com/news/scan-finds-36769-exposed-self-hosted-ai-endpoints-d9c8104c)): 36,769 self-hosted AI endpoints via public scanning index — 18,529 Open WebUI, 6,935 Ollama ("Ollama is running" banner), 5,223 agent-builder endpoints (Flowise, n8n, ComfyUI, Dify, RAGFlow, Langflow, Open WebUI Pipelines); only 2.02% with auth challenges. Cloud Security Alliance repeated the 36,769 figure 2026-09-15. → CONFIRMS our Shodan-derived agent-builder populations are real and mostly unauthenticated.
- **SentinelOne + Censys, Jan 2026** (via [securityaffairs.com](https://securityaffairs.com/198898/ai/the-ai-supply-chain-has-a-security-problem-and-much-of-it-is-sitting-on-the-open-internet.html)): ~175,000 publicly exposed Ollama hosts across 130 countries; ~half with tool-calling capability (code execution, API access); vLLM 4,880 endpoints with only 3 showing auth.
- **OpenClaw exposure wave** ([dev.to](https://dev.to/dishant0406/openclaw-broke-the-internet-900-malicious-plugins-followed-now-nvidia-has-an-answer-53b5)): OpenClaw hit 34,168 GitHub stars in 48h; researchers scanned 18,000 exposed OpenClaw instances; ~900 malicious skills in registry; Kaspersky/Bitdefender advisories. Shodan shows 33,669 `http.title:"OpenClaw"` hits — consistent order of magnitude.
- **NemoClaw CVE-2026-65105** ([cyera.com](https://www.cyera.com/research/nemoclaw-one-website-visit-to-hijack-your-ai-agent)): OpenClaw deployer binding Ollama to 0.0.0.0:11434, exploitable via DNS rebinding — mechanism note for how agent infra becomes exposed.

## Honest nulls

- **`intitle:"index of" ".claude"` open directories**: web search returned only GitHub repo content (CLAUDE.md files in public repos), no indexed open web directories of `.claude/` dirs. No leads.
- **aider chat logs / `.codex/sessions` / cline task files exposed**: query polluted by scam/spam index content; no documented open-directory exposures found.
- **GitHub gists of pasted agent transcripts**: gists found are voluntarily-shared tooling (OpenClaw agent templates, Claude Code session converters), not leaked/transcript exposures. Null for the exposure surface.
- **Public S3 buckets with agent state**: no indexed evidence found (results were unrelated vendor stories — Claude Code source-map leak, Writer AI WriteOut flaw).
- **Docker Hub images with baked-in agent state**: no documented exposures via search; related finding only — `psyb0t/docker-claudebox` is an agent-execution container with `--permission-mode bypassPermissions` + Docker socket mount by design (high risk IF exposed, but a design choice, not an exposure).

## Open threads

1. **Agent-flavored Ollama sweep at scale**: the `"agent"` keyword yielded only 6/13,734 Ollama instances. The model-list surface (`/api/tags`) is not indexed by Shodan — agent-shaped model sets (openhermes, functionary, gorilla, dolphin-function-calling) would need active probing, which is out of scope (passive only). Flag as a *passive-only* dead end.
2. **OpenClaw :18789 population**: `port:18789` = 198,478 raw — too noisy; `http.title:"OpenClaw"` (33,669) is the cleaner signal but may include false-positive title matches. De-dup/verify against the Mysterium census numbers if a fresh public dataset appears.
3. **text-generation-webui / Gradio**: zero fingerprintable population in Shodan (`port:7860 product:"Gradio"` = 0). TGWebUI instances blend into generic Gradio/HTTP — passive-only blind spot.
4. **vLLM on :8000**: 3 keyword hits, none with banner evidence in host records; likely hidden behind nginx/reverse proxies. Passive-only blind spot.
5. **Residential OpenClaw (75.146.94.94)**: logged as LEAD with caveat — review whether residential-ISP control-UIs stay in the IP log (prior lanes logged a Vietnam residential IP, so kept with note).
