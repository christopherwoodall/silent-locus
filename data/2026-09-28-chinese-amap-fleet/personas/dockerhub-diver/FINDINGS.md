# FINDINGS — DOCKERHUB DIVER

**Started:** 2026-10-05 07:13 UTC
**Brief:** [BRIEF.md](BRIEF.md)
**Method:** DockerHub public API only (`hub.docker.com/v2/`). Metadata/manifest JSONs only — never pull images. LOG URLs, don't hammer (opsec).
**Corpora for cross-reference:**
- `data/2026-09-28-chinese-amap-fleet/events.jsonl`
- `data/2026-10-03-openai-agent-traces/events.jsonl`
- `data/2026-10-01-oai-tag-sweep/events.jsonl`

**Grading:** OURS (in our corpora) / KNOWN (publicly documented) / GENUINELY NEW.

---

## Lane 1 — Registry search

**API status:** `v2/search/repositories/` is DEAD (empty/timeout) — DockerHub deprecated it. Using search-engine `site:` queries + `v2/repositories/{ns}/` API. Egress flaky 07:13–07:19 UTC, recovered ~07:20 UTC.

**Queries run (see `repos.log`):**
- `site:hub.docker.com uqscan OR "zz=oai" agent` → 0 results
- `site:hub.docker.com "webhook.site" "ai agent"` → 0 results
- `site:hub.docker.com ai agent eval harness` → 0 results
- `site:hub.docker.com httpbun OR "jina.ai"` → 1 hit: `remyxai/2603.28376v1`

### Finding 1 — remyxai/2603.28376v1 (KNOWN)
Auto-generated demo image for Alibaba AIDC-AI's Marco-DeepResearch (arXiv 2603.28376, 2026-03-30). 0 stars, 140 pulls, updated 2026-03-31. Entrypoint consumes `JINA_API_KEY` (jina.ai relay tradecraft — corroborates our corpus TTP, not a new trace). Zero corpus hits. **Grade: KNOWN** (public paper demo).
- https://hub.docker.com/r/remyxai/2603.28376v1

### Finding 2 — bdqnghi namespace (KNOWN, fleet-publisher pattern)
212 repos, all agent-eval images (SWE-bench Pro, DeepSWE, Terminal-Bench 3/4, SWE-Together, SWE-Interact, ProgramBench). Burst-pushed 2026-09-12 (machine cadence, all same day). Tag grammar `<org>_1776_<repo>.<sha>`. Documented in `bdqnghi/swe_benchmark_arm` README (arm64 eval images). **Grade: KNOWN** — documented eval infrastructure, but notable as the fleet-publisher SHAPE: one publisher + burst cadence + machine tag grammar.
- https://hub.docker.com/r/bdqnghi/sweap-images (54k pulls)

_Work in progress: alexgshaw namespace check, undocumented-publisher hunt._

### Finding 3 — alexgshaw namespace (KNOWN)
100 repos, terminal-bench task images (`t-bench-*`, `headless-terminal`, `model-extraction-relu-logits`, …). 85/100 pushed 2026-04-03 (burst), 8.6M total pulls. Namespace = Terminal-Bench author. **Grade: KNOWN** — official eval infrastructure.
- https://hub.docker.com/r/alexgshaw/t-bench-python-3-13

### Finding 4 — OpenClaw image ecosystem (KNOWN)
Multiple publishers ship OpenClaw/MoltBot agent images: `openclaw/openclaw` (official), `moltbot/moltbot`, `alpine/openclaw` (mirror of ghcr.io), `openeuler/openclaw`, `gentkit/openclaw`, `fourplayers/openclaw` ("Built for ODIN Fleet"), `ilteoood/docker-harnesses` (7+ harness images: zeroclaw, nullclaw, openclaw, opencode, openfang, picoclaw, claude-code — rebuilt daily/weekly via GitHub Actions). All public/documented. Zero corpus hits. **Grade: KNOWN.** Notable as fleet-publisher SHAPE instances (one publisher, many agent images, machine cadence).

### Finding 5 — ZeroPay x402 A2A (KNOWN, adjacent)
`zeropaydev/zeropay` — self-hosted payment gateway with x402 Agent-to-Agent payment protocol (AI agents settling payments via EIP-3009). Public/documented. Not an agent trace, but a new agent-capability surface (agent commerce infra). Logged for the arg-hunter/librarian. **Grade: KNOWN.**

**Corpus cross-reference:** `bdqnghi`, `alexgshaw`, `ilteoood`, `openclaw`, `docker.io`, `hub.docker.com` → **0 hits in all three corpora**. DockerHub is an unexplored surface for this hunt — no OURS findings exist.

## Lane 2 — Metadata mining

**Method constraint (egress):** `hub.docker.com/v2/` works (repo metadata, READMEs, tags). `registry-1.docker.io/v2/` is UNREACHABLE through this VM's egress proxy (consistent 000/timeout, auth.docker.io token fetch works but blob/manifest fetches die). **Image config/manifest JSON reads are blocked until egress allows registry-1.docker.io.** Logged for the methodology file. No images were pulled.

What WAS readable: full repo descriptions via `v2/repositories/{ns}/{repo}/` (used for remyxai). README text for openclaw images obtained via search-engine cache instead (opsec-friendly).

## Lane 3 — Publisher clustering

| publisher | repos | shape | grade |
|---|---|---|---|
| bdqnghi | 212 | eval images, burst 2026-09-12, `<org>_1776_<repo>.<sha>` tags | KNOWN (documented) |
| alexgshaw | 100 | terminal-bench tasks, burst 2026-04-03 | KNOWN (official) |
| ilteoood | 73 | mixed utils + docker-harnesses agent images, daily/weekly rebuilds | KNOWN (documented) |
| jefzda | (not enumerated) | `sweap-images` — SWE-bench Pro 731 instances | KNOWN (documented) |

**No undocumented fleet publisher found.** Every burst-cadence agent-image publisher located is publicly documented eval/tooling infra.

## Lane 4 — Layer-selective pulls

Blocked by egress (registry-1.docker.io unreachable). No digests logged as decisive; no pulls attempted. **Resume hook:** when egress allows, priority targets: `fourplayers/openclaw` ("ODIN Fleet" — undocumented fleet name), `gentkit/openclaw`, any image whose README references webhook URLs.

## Honest assessment

DockerHub's agent-image population is dominated by **documented public infrastructure**: eval harnesses (terminal-bench, SWE-bench families) and agent-framework demos (OpenClaw ecosystem, CrewAI). The hunt's marker grammars (`uqscan`, `zz=oai`, `webhook.site`+agent) return **zero** on DockerHub's indexed surface. This is a clean negative for the marker-hunt — but DockerHub remains the highest-probability surface for a FUTURE find, because: (a) zero corpus coverage means no one has looked, (b) image configs are the natural place to hardcode webhook/dead-drop URLs, (c) the config-blob lane is still unexecuted (egress-blocked). **Recommendation: re-run Lane 4 when registry-1.docker.io egress is available; that's where a GENUINELY NEW find would live.**

## Null results (first-class)
- `v2/search/repositories/` endpoint is dead — DockerHub killed public search; discovery now requires search engines or namespace enumeration.
- Zero hits for `uqscan`, `zz=oai`, `webhook.site`+agent across indexed DockerHub surface.
- Zero corpus overlap for all DockerHub entities checked.
- No undocumented burst-cadence agent-image publisher found.

