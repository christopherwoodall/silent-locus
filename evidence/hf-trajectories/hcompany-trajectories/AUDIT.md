# Audit: Hcompany/trajectories (P2 bounded sample)

- Source: `https://huggingface.co/datasets/Hcompany/trajectories` (raw sample under `raw/hcompany-trajectories/`, provenance in `raw/hcompany-trajectories/PROVENANCE.md`)
- Audited: 2026-10-07
- Sample: 50 of 7,368 json trajectory files (even stride across `data/t/`) + README.md + `data/index.json`. Models in sample: Holo4 27B / Holo4 35B A3B. Benchmarks: OSWorld, OSWorld 2, AndroidWorld, AutomationBench, PinchBench, Agents' Last Exam.
- Method: per-file text scan for CAPTCHA/Turnstile/Cloudflare/bot-check encounters and challenge-solved strings; byte-verification discipline (template-default flag ≠ defeat; challenge must appear in tool output/observations with successful fetch); marker grammar hunt. Sharp-pattern grep: `captcha|turnstile|cloudflare|...|webhook.site|ntfy.sh|httpbun|\boai[:-_]` + full-context review of every hit.

## Grading legend
- **OBSERVED**: we saw this in the data.
- **INFERENCE**: we think this is true, but we did not see it directly.

## Headline

**Encounter, no defeat — CLEAN for the defeat lane.** The 50-trajectory sample contains one byte-verified rate-limit encounter (dblp.org) and harness-authored anti-bot guidance in the system prompt. Neither is an unreported CAPTCHA/Turnstile/Cloudflare defeat.

## Evidence

**1. The DBLP rate-limit encounter (OBSERVED)** — `data/t/multi-apps-71-9ae3c867.json` (Holo4 27B, task: export 6 DBLP bibtex entries):
- Steps 6–9: shell `wget` calls to `dblp.org/search/publ/api` hang; agent notes "DBLP seems to be blocked from the shell" and pivots to Chrome.
- Step 16: in-browser `fetch` fails ("Failed to fetch"); agent diagnoses CORS/rate-limit state.
- Step 19: "DBLP is rate-limiting or blocking us now. The connection is being closed. This is a common anti-scraping measure." Agent `sleep 20`s, then **constructs the remaining bibtex entries from parametric knowledge** (not from fetched pages).
- Steps 30–33: `references.bib` written with 6 entries; task scored success — but 3 of 6 entries were model-recalled, not fetched.
- This is a rate-limit **encounter with fallback**, not a challenge defeat: no CAPTCHA/Turnstile/Cloudflare widget was faced or solved; the 3 early API fetches were plain successful HTTP calls; the agent did not evade the limit, it waited and used memory. Does not meet the byte-verified defeat bar (no challenge-solving steps, no post-challenge successful fetch). (OBSERVED)

**2. Harness-authored anti-bot guidance in the system prompt (OBSERVED)** — identical `system` text (33,726 chars) across sampled trajectories includes a `## Browser` section:
- "On Access Denied or a bot wall, reload, retry, or take another path on the same site. Never switch to another brand's site..."
- "Clear cookies only against anti-bot loops, never where you are signed in."
- "A blocker you have established as external (a captcha, a gated download, a dead backend) is not something to keep retrying."
This is publisher-authored harness guidance (present identically in all sampled runs), not an agent-discovered bypass technique and not a defeat. Noted as a harness property: the Holo4 computer-use harness explicitly trains/instructs bot-wall handling. (OBSERVED)

**3. Other hits (all killed):**
- `WebSocketBadStatusException: Handshake status 403 Forbidden` — localhost Chrome DevTools Protocol websocket failure, not a site challenge. (OBSERVED)
- `Permission denied` / `GDBus.Error.AccessDenied` — local file-permission / geolocation-daemon errors in the sandbox. (OBSERVED)
- 5 `B\d{10}[A-Z0-9]{2}` marker candidates: all substrings of sha256 hashes in trajectory metadata (`eb3399000477514315f6b501544a38af1de33206e3d1b950d07eab4ef9299de1`). FP_HEX_BLOB. (OBSERVED)

## Marker grammar

- `oai*` tags: zero. `zz=` params: zero. Dead-drop carriers (webhook.site/ntfy.sh/httpbun): zero. task-oai-NNN / northflank / probe.js: zero. (OBSERVED)

## Verdict: **CLEAN** (sample; P2) — one documented encounter, no defeat
