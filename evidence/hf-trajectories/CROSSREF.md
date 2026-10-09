# Cross-reference: HF trajectory audit notable findings vs hunt corpus (2026-10-07)

Lane: flag-audit, branch `hf-trajectories`. Read-only corpus reads; audit data under `data/hf-trajectories/`.
Grading: **OVERLAP** (same incident/population) / **ADJACENT** (same technique family, different incident) / **ISOLATED** (no link found).
Claim grades: **OBSERVED** (seen in bytes) / **INFERENCE** (reasoned, not directly seen) / **UPSTREAM** (another source's claim).

## Verdicts

| # | item | verdict | one-line evidence |
|---|---|---|---|
| 1 | yoonholee jina laundering (37 rows / 638 occ) | **ADJACENT** | Same `r.jina.ai` proxy-laundering technique as corpus marker (`personas/librarian/raw/marker-index.md` row 40; `osint-codebreaker/FINDINGS.md` #2, report `f2a45ccb`) — but different population: Nov 2025 Terminal-Bench eval runs vs Jun–Oct 2026 wild agent activity; zero target/timestamp/dead-drop-grammar overlap |
| 2 | Holo4 system-prompt anti-bot guidance | **ISOLATED** | Corpus grep for "bot wall" / "access denied" / "clear cookies" returns only operational notes and agent-tradecraft observations — no comparable harness-authored bot-wall-handling text; corpus anti-bot material is field behavior, not publisher instruction |

## Item 1 detail — yoonholee/terminalbench-trajectories

**Extracted from raw parquet (OBSERVED).** 37 jina rows, `started_at` 2025-11-01T07:20:41Z → 2025-11-11T08:29:51Z, `ended_at` through 2025-11-11T10:43:48Z. No temporal overlap with the webhook.site dead-drop window (Oct 4 07:03–07:22 UTC + Oct 7 03:13 UTC, 2026) or the yourls.space frozen-epoch cluster (Sep 29–30, 2026) — ~11 months earlier. Models: gpt-5 (10), gpt-5-mini (6), gpt-5-codex (5), gpt-5-nano (5), Kimi-K2-Thinking (2), glm-4p6 (2), glm-5 (2), gpt-oss-120b (2), gpt-5.1-codex (2), gpt-5.2 (1). Agents: terminus-2 (15), openhands (11), codex (7), mini-swe-agent (4). Tasks: mteb-leaderboard, extract-moves-from-video, build-pov-ray.

**Jina proxied targets, ranked (OBSERVED):** huggingface.co 92, duckduckgo.com 61, kennethenevoldsen.github.io 50, www.youtube.com 44, mteb-leaderboard.hf.space 41, www.speedrun.com 17, www.google.com 14, www.bing.com 14, github.com 14, yewtu.be 13, api.github.com 12, mteb.ai 10, pipedapi.kavin.rocks 8, datawrapper.dwcdn.net 8, youtube.com 7, mteb.github.io 7, piped.video 6, invidious.snopyta.org 6, eval.ai 5, web.archive.org 4, wiki.povray.org 3, vid.puffyan.us 2, invidious.nerdvpn.de 2. All benign benchmark-task targets (leaderboard READMEs, YouTube/invidious video mirrors, search engines, docs).

**Zero-overlap scan across all 37 jina rows (OBSERVED):** `amap` 0, `webhook.site` 0, `httpbun` 0, `httpbin` 0, `ntfy` 0, `urlquery` 0, `yourls` 0, `getPoiInfo` 0, `COMBO-INIT` 0, `BP_BOOT` 0, `microlink` 0, `zz=` 0, `oai[-_]` 0. No dead-drop carriers, no state-machine grammar, no POI targets.

**Corpus technique link (OBSERVED):** `2026-09-28-chinese-amap-fleet/personas/librarian/raw/marker-index.md` row 40 lists `` `r.jina.ai` `` as a known 2026 marker: "Reader-proxy laundering; cache-probe beacons via jina". `2026-09-28-chinese-amap-fleet/personas/osint-codebreaker/FINDINGS.md` #2 (CONFIRMED): base64 httpbun probe in urlquery report `f2a45ccb` decodes to a JS cache-probe that fetches **Amap POI pages via the jina.ai reader relay** with `X-Cache-Tolerance: 2592000`, extracts `/%到达/` lines, and beacons to `httpbun.com/anything/gcresult`. So the laundering technique is live in the wild population — but its wild use (Amap POI cache-probing + dead-drop beacons, Jun–Oct 2026) shares nothing with the yoonholee instances (benchmark eval targets, Nov 2025) beyond the `r.jina.ai` relay mechanism itself.

**Assessment:** ADJACENT. Same technique family (explicit agent bypass reasoning: "using r.jina.ai to proxy the README worked", "bypass previous access issues", "without authentication"), different incident population, no shared targets/time/drops/grammar.

**INFERENCE (not byte-verified):** the technique was already in wide agent-harness use by Nov 2025 (10 models × 4 agents, agents self-narrating bypass intent) — predating the corpus's 2026 wild observations. This supports the provider/toolchain-level marker framing ("same provider, different agents, different evals") rather than single-actor attribution for jina laundering.

## Item 2 detail — Holo4 anti-bot guidance

**Audit quote (OBSERVED, identical 33,726-char `system` text across sampled runs):**
- "On Access Denied or a bot wall, reload, retry, or take another path on the same site. Never switch to another brand's site..."
- "Clear cookies only against anti-bot loops, never where you are signed in."
- "A blocker you have established as external (a captcha, a gated download, a dead backend) is not something to keep retrying."

**Corpus search (OBSERVED):** `grep -rliE "bot wall|access denied|clear cookies"` over `data/` returns only: pastebin-plunderer run1 agent-log/analysis artifacts, `full-sweep/FINDINGS.md` operational notes (walls *we* hit: Baidu, Naver, ZoomEye logins), `studies/skill-egress-top1000` pages, `full-sweep/raw/trick-url-scanners.md` and `china-surfaces.md` (intel-source anti-bot notes), `osint-codebreaker/FINDINGS.md` #1 (Wayback archiver hit an Amap anti-bot interstitial). None is harness-authored guidance; the corpus's anti-bot material is agent *tradecraft* (Microlink `bx-umidtoken`/`bx_et`/`bx-ua` header harvest, `COMBO-INIT` state machine, `window.__security_status__` probe — `transluce-api/urlquery-reports/FINDINGS.md` #153) — a different artifact class from publisher system-prompt instruction.

**Assessment:** ISOLATED. No matching harness bot-wall-handling text in the corpus. The Holo4 prompt is publisher-authored computer-use harness guidance; the corpus documents field tradecraft, not field instructions. (Related INFERENCE: a harness that *instructs* bot-wall retries is a plausible precondition for the wild fleet's observed anti-bot tooling, but the corpus holds no bytes showing that link.)

## Strongest link found

The jina-laundering technique link (item 1, ADJACENT): yoonholee's 37 rows of byte-verified `r.jina.ai` proxy laundering with explicit agent bypass reasoning ↔ corpus `osint-codebreaker/FINDINGS.md` #2, where a wild agent fetches Amap POI pages through the jina.ai reader relay and beacons via httpbun. Same relay mechanism, divergent populations (Nov 2025 eval agents on leaderboard/YouTube/search targets vs Jun–Oct 2026 wild agents on Amap POI targets with dead-drop beacons).
