# Slow passive swarm crawl — CT + package tripwire, 2026-10-16

Run by: CT+PACKAGE HUNTER executor. Passive only. ~28 public read-API calls.
Raw bytes: `raw/` (each file has a `.PROVENANCE.txt`: source URL, UTC time,
method, SHA-256). Collector: `collect.py`.

## Candidates (agent-shaped, published Nov 2025+, unreported in our corpus)

### 1. dsh-ntfy-remote (npm) — DeepSeek-harness agents on an ntfy dead-drop
- What: npm package `dsh-ntfy-remote@1.1.1`. Bridges every DSH (DeepSeek
  Harness) session to an ntfy topic: phone push, phone replies, approval
  and question relay. Pub/sub dead-drop as the agent command channel.
- Agent-shaped: ntfy topic is the dead-drop; phone replies become agent
  inputs. This is the ExploitGym-shaped pattern (agents + dead-drop
  control channel), openly packaged.
- Dates: created 2026-09-12T02:32:55.374Z, modified 2026-09-16T12:57:20.973Z
  (registry time.created/time.modified).
- Registry record: keywords include dsh, deepseek-harness, ntfy, approval;
  repo git+https://github.com/tongwoojun/dsh-ntfy-remote.git; no deps.
- API: https://registry.npmjs.org/dsh-ntfy-remote
- Why unreported: no match in `lists/` or the amap-fleet evidence; outside
  the Amap / OAI / Anthropic fleets (DeepSeek provider).
- Evidence: raw/npm_doc_dsh-ntfy-remote.json (+ PROVENANCE.txt)
- Grade: PRIMARY (registry bytes we fetched). Confidence: MODERATE. Caveat:
  openly published dev tooling, not covert incident evidence.

### 2. @4ier/pi-ntfy (npm) — pi coding agent with inbound ntfy command channel
- What: `@4ier/pi-ntfy@0.2.2`. pi extension: subscribes to an ntfy topic and
  turns incoming notifications into agent turns (the inbound half of
  pi <-> ntfy).
- Agent-shaped: same dead-drop command-channel shape, inbound direction.
- Dates: created 2026-09-26T00:39:54.335Z, modified 2026-09-26T10:02:17.892Z.
- Registry record: keywords pi, pi-extension, ntfy, agent, automation;
  repo git+https://github.com/4ier/pi-ntfy.git.
- API: https://registry.npmjs.org/@4ier%2Fpi-ntfy
- Why unreported: no corpus match; pi-harness ecosystem, not a known fleet.
- Evidence: raw/npm_doc_4ier_pi-ntfy.json (+ PROVENANCE.txt)
- Grade: PRIMARY. Confidence: LOW-MODERATE. Caveat: openly published tool;
  not tied to any incident.

## Killed leads (one line each)

- npm "swarm-agent"/"agent-coordinator" searches (140k+ each): top-20 hits
  are all legitimate agent frameworks (MCP servers, LangGraph, claude-flow)
  — benign dev tooling, no dead-drop/C2 markers.
- Rare markers hysandbox-ats / uqscan= / uqframe= / uqtag= / akbkyowd9geqr98:
  ZERO hits on npm (5 queries), RubyGems (5 queries), crt.sh (3 queries),
  PyPI RSS (100 recent releases) — honest-zero baseline, mirrors the
  reduced tripwire in scripts/scanners/packages.py.
- crt.sh %.serveo.net: last cert 2018-12-18 — service dead, no recent use.
- crt.sh %.ngrok.io: last cert 2019-08-31 — pattern dead (ngrok moved on).
- crt.sh %.localhost.run: only 2 recent labels (v2.admin.*) — benign admin.
- crt.sh %.webhook.site (3309 rows): kpayredteam/zabbix/btcps instances are
  long-lived named dead drops on daily/monthly renewal cadences — human
  pen-test/monitoring shape, no agent markers, not novelty.
- dead_drop_h7p2j1: 2023 piracy spam ("Download EPUB..."), random-suffix
  name — old spam, not agent-shaped.
- @zojize/dead-drop: steganographic JS-AST encoding (2026-04), published
  research tool with repo — dual-use but no swarm link.
- clawauth: 2026-02 OAuth dead-drop for agent workflows — legit dev tool.

## Honest-zero surfaces (signal, not failure)

No rare-marker hits anywhere = the known fleets are NOT staging on npm,
RubyGems, PyPI RSS, or CT identities. Dead tunnel cert patterns (serveo,
ngrok.io) show no agent-shaped re-use.
