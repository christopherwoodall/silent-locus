# Shodan Chat-Transcript Dork Study

**Date:** 2026-10-05 | **Method:** Shodan API (`~/workspace/skills/shodan/bin/shodan.py`) only — `count` + `search` + `host`. No candidate host was opened, fetched, or probed. All observations are Shodan's stored banners/HTML.

**Evidence grades:** OBSERVED = in Shodan output. INFERENCE = my interpretation. NULL = zero-count dork.

## Headline results

- **~33,679 hosts** serve pages titled "OpenClaw"; **21,142** on port 18789 (OpenClaw's default gateway port), Shodan product-detected as OpenClaw. OBSERVED. OpenClaw gateways host a webchat UI plus session/state endpoints; default binds localhost, so this population is overwhelmingly self-exposed deployments. Class: KNOWN product / GENUINELY NEW exposure scale.
- **Harness-grammar dorks returned small, actionable candidate sets:**
  - `http.html:".codex/sessions"` → 13 hosts (multiple agent-workbench titles)
  - `http.html:".claude/projects"` → 9 hosts (incl. "Claude Projects", "RuntimeGuard")
  - `http.html:".claude.json"` → 110 hosts (open `Directory listing for /` pages serving `.claude.json`)
  - `http.html:"checkpoint_id"` → 8 hosts (IREN port-8000 cluster, MIT research host)
  - `http.html:".aider.chat.history.md"` → 3 hosts (two open directory listings)
  - `http.html:".gemini/tmp"` → 1 host ("Prompt Recorder")
  - `http.html:".openclaw/agents"` → 33 hosts (OpenClaw-ecosystem marketing pages)
  - `http.html:".continue/sessions"` → 4 hosts

## Candidate table (slim; full IPs preserved in evidence per no-redaction rule)

| # | IP | Port | Title (Shodan) | Grammar hit | Org | Timestamp | Class |
|---|----|------|----------------|-------------|-----|-----------|-------|
| 1 | 46.225.88.73 | 443 | Agent Relay | `.codex/sessions` | Hetzner | 2026-10-05 | GENUINELY NEW |
| 2 | 46.225.209.102 | 3000 | Claude Projects | `.claude/projects` | Hetzner | 2026-10-05 | GENUINELY NEW |
| 3 | 46.225.51.127 | 3000 | RuntimeGuard | `.claude/projects` | Hetzner | 2026-10-04 | GENUINELY NEW |
| 4 | 43.139.127.232 | 80 | Remote Codex Workbench | `.codex/sessions` | Tencent Beijing | 2026-10-02 | GENUINELY NEW |
| 5 | 120.48.48.120 | 8765 | Codex Web | `.codex/sessions` | Baidu Beijing | 2026-10-03 | GENUINELY NEW |
| 6 | 134.209.40.131 | 3001 | Codex Web | `.codex/sessions` | DigitalOcean | 2026-09-22 | GENUINELY NEW |
| 7 | 195.62.49.85 | 8123 | Codex Messenger Login | `.codex/sessions` | proxy.ru / Aleksandr Popov | 2026-09-30 | GENUINELY NEW |
| 8 | 43.134.83.249 | 80 | Directory listing for / | `.aider.chat.history.md` | Tencent | 2026-10-04 | GENUINELY NEW |
| 9 | 207.58.153.134 | 8081 | Directory listing for / | `.aider.chat.history.md` | SMV/Leaseweb | 2026-10-04 | GENUINELY NEW |
| 10 | 117.55.229.221 | 18081 | Prompt Recorder | `.gemini/tmp` | UberGlobal | 2026-09-28 | GENUINELY NEW |
| 11 | 185.195.255.124 | 8000 | Directory listing for / | `.claude.json` | Veganet (TR) | 2026-10-05 | GENUINELY NEW |
| 12 | 49.234.49.58 | 8080 | Directory listing for / | `.claude.json` | Tencent Beijing | 2026-10-05 | GENUINELY NEW |
| 13 | 178.104.186.30 | 8080 | Directory listing for / | `.claude.json` | Hetzner | 2026-10-04 | GENUINELY NEW |
| 14 | 161.115.132.6 / .128.147 / .128.148 / .128.142 / .132.5 | 8000 | (unresolved) | `checkpoint_id` | IREN | 2026-09-20/21 | GENUINELY NEW (cluster) |
| 15 | 128.61.240.196 | 8002 | vibeshub · share Claude Code & Codex sessions as replayable traces | `.codex/sessions` | Georgia Tech | 2026-10-05 | KNOWN (public product) |
| 16 | 34.8.130.149 | 443 | DashVox: Voice-First IDE for AI Coding Agents | `.codex/sessions` | Google LLC (dashvox.ai) | 2026-09-28 | KNOWN (public product) |
| 17 | 35.153.188.39 | 443 | Iolit, Get paid for your AI coding sessions | `.codex/sessions` | AWS (iolit.dev) | 2026-09-28 | KNOWN (public product) |
| 18 | 18.116.120.128, 18.217.94.29 | 443 | Forager | `.claude/projects` | AWS | 2026-09-29/30 | KNOWN (public product) |
| 19 | 62.234.187.97 | 8080 | Httpbun | `httpbun` | Tencent Beijing | 2026-10-03 | OURS (already in IP_LOG as watchlist oddity) |
| 20 | 52.38.235.110 | 443 | Coding agent study | `.codex/sessions` | AWS (taesookim.com) | 2026-10-02 | KNOWN (research study) |
| 21 | 128.30.196.23 | 12361 | (unresolved) | `checkpoint_id` | MIT (deep-chungus-9.csail.mit.edu) | 2026-09-13 | KNOWN (research infra) |

## Notes on notable rows (INFERENCE, unverified — no live fetch per OPSEC)

- **Row 1 (46.225.88.73):** port 8081 on same host is titled "Droidrun — The AI Mobile Automation Framework". The `relay.*.sslip.io` hostname suggests an agent-relay service; `.codex/sessions` in the 443 page HTML may be a transcript/session viewer. Agent-shaped, worth IP-log entry.
- **Rows 1–3:** three Hetzner hosts with agent-shaped titles ("Agent Relay", "Claude Projects", "RuntimeGuard") all indexed 2026-10-04/05. Possible common operator or common deployment recipe — correlation only, not attribution.
- **Row 7 (195.62.49.85:8123):** hostname literally `proxy.ru`; "Codex Messenger Login" implies auth is present (login page, not the sessions themselves).
- **Rows 8–9:** open directory listings whose index HTML contains the `.aider.chat.history.md` filename — INFERENCE: the directory serves aider history files publicly. Strongest transcript-exposure signal in the set.
- **Rows 11–13:** open `Directory listing for /` (Python http.server style) with `.claude.json` filenames in the index — exposed Claude Code config surface. Row 11 also runs "TedussAI Mainframe" on 8002.
- **Row 14:** five IREN IPs, all port 8000, all containing `checkpoint_id`, scanned 2026-09-20/21 — cluster-shaped (same org, adjacent netblocks, same port). `checkpoint_id` is harness session-checkpoint vocabulary (Claude Code checkpoints / agent checkpointing). INFERENCE: a checkpointed-agent fleet or checkpoint-serving test range. Host-detail lookups failed for this cluster (truncated API responses); recorded as unresolved, unverified.
- **Row 19 (62.234.187.97):** "Httpbun" title, not a transcript — a self-hosted httpbun copy on the same hobbyist VPS already in our IP log. OURS: overlap annotation only, no new claim. Two other self-hosted Httpbun pairs (`letss.win` on 95.169.18.20:8443 and 207.57.145.214:8443) suggest one operator running httpbun on two VPSes.
- **OpenClaw scale:** `http.title:"OpenClaw"` → 33,679; `+ port:18789` → 21,142. Also `.openclaw/agents` → 33 product/marketing pages (Clawis.ai, Contynu, GoldenClaw, Nervix — the string is product copy, not exposed transcripts; class KNOWN). The 21k figure is the single largest exposed agent-chat surface found; OpenClaw gateways expose session control + webchat, so this population is the highest-priority passive-monitoring target. INFERENCE on exposure risk; counts OBSERVED.

## Nulls (first-class, NULL grade)

- `http.title:"Gradio" chat` → 0
- `http.html:"share.claude"` → 0
- `http.html:"claude.ai/share"` → 0
- `http.title:"Index of" chat transcript` → 0
- `http.title:"Index of" ".jsonl" claude` → 0
- `http.title:"Index of" ".claude"` → 0
- `http.html:"conversations.json" claude` → 0
- `http.html:"oai-tag-sweep"` → 0
- `http.html:"uqscan"` → 0
- `http.html:"saoudrizwan.claude-dev/tasks"` → 0
- `http.html:"aider.chat.history"` → 0 (bare string; the `.md` variant hit 3)
- `http.html:"todo_write"` → 0
- `http.html:"terminal_epoch"` → 0
- `http.title:"text-generation-webui"` → 1

## Noisy dorks (discarded, honest)

- `http.html:"zz="` → 504,968 (JS/CSS noise; unusable)
- `http.title:"Jan"` → 1,249 (matches "January" etc.; unusable as chat-UI dork)
- `http.html:"subagent"` → 71 (corporate pages, skillfm.ai; unusable)
- `http.html:"bx-v"` → 120 (odd high ports, host lookups failed; likely framework artifact — INDETERMINATE, not claimed as fleet marker)

## Chat-frontend census (OBSERVED counts, auth state unknown from Shodan)

Open WebUI 22,568 · LibreChat 3,251 · SillyTavern 1,541 · ChatGPT-Next-Web 607 · LobeChat 564 · Ollama 154 · Chatbox 118 · KoboldAI 33 · LM Studio 15. These are KNOWN open-source UIs; title match does not establish missing auth — recorded as census only, no exposure claim.

## Recommended follow-ups (for parent agent)

1. Append rows 1–14 to the IP log (infrastructure-only provenance, "Shodan stored observation" evidence grade).
2. OpenClaw 21k population: passive facet breakdown (by org/country/asn) to find operator clusters — cheap via `count` + facets.
3. Re-run harness-grammar dorks weekly; new rows are high-value.
4. Row 14 (IREN cluster) deserves a retry of host-detail lookups later (API truncation blocked this pass).
