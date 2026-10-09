# THE HAM RADIO OPERATOR — FINDINGS

**Verdict: HONEST NEGATIVE.** No agent-shaped activity found on public radio infrastructure. Zero radio traces in all three corpora, near-zero SDR submissions on urlquery, zero on urlscan, no agent+radio code on GitHub. The infrastructure IS usable by agents (keyless APIs, no-login receivers documented below) — but nobody is using it that way, at least not visibly.

## 1. Local corpus verification — 0 across all three sets

Grep for `websdr|kiwisdr|aprs|sstv|pskreporter|openwebrx|rtl-sdr|rtlsdr|number station` (case-insensitive):

| Corpus | Hits |
|---|---|
| `data/2026-09-28-chinese-amap-fleet/events.jsonl` (2,141) | 0 |
| `data/2026-10-03-openai-agent-traces/events.jsonl` (589,972) | 0 |
| `data/2026-10-01-oai-tag-sweep/events.jsonl` | 0 |

No candidate to classify — the zero is the finding, cross-verified.

## 2. urlquery htmx sweep (curl-based CLI, ≤1 req/5s)

| Query | Reports | Assessment |
|---|---|---|
| `url.domain:websdr.org` | 3 (2026-01-25 ×2, 2026-05-02) | Bare homepage hits, standard scanner UAs. Human/researcher browsing. |
| `url.domain:kiwisdr.com` | 3 (2023-11-14, 2023-12-31, 2025-09-09) | Two bare receiver pages; one tuning deep link `plonsk.proxy.kiwisdr.com:8073/?f=3699.00lsbz10`. 3699 kHz LSB = European 80m calling frequency — human-plausible share link, not machine-generated. |
| `proxy.kiwisdr.com` | 2 | Same as above minus the tuned one. No enumeration burst. |
| `url.domain:aprs.fi` | 1 (2024-10-13) | Bare homepage. Old. |
| `url.domain:pskreporter.info` | 0 | — |
| `url.domain:openwebrx.de` | 0 | — |
| `url.domain:sdr.hu` | 0 | — |
| `url.domain:rx-tx.info` | 0 | — |
| `url.domain:satnogs.org` | 0 | — |
| `websdr` (keyword) | 8 | Receivers + `cnx-software.com` homepage ×2 (Oct 3–4, 2026). Pulled full HTTP transactions for `ee2c167a`: standard urlquery scanner run (Firefox 134), matched "websdr" in article text about ESP-SDR firmware. Not agent-shaped. Two consecutive-day hits = site monitoring or scheduled scanning, not bot grammar. |

Keyless `related/domain|asn|ip` endpoints on the websdr.org cluster: only the 3 known reports — no hidden burst.

## 3. urlscan.io — 0

`domain:websdr.org` → 0 results. `domain:kiwisdr.com` → 0 results.

## 4. GitHub — no agent+radio code

- 427 repos mention kiwisdr: all ham tooling (dashboards, skimmers, SDR Town). No agent orchestration.
- **AetherSDR** (YouTube: "maintained by an AI agent called AetherClaude") — agent-BUILT ham software, not a wild agent using radio as infrastructure. Worth distinguishing: dev-agent output ≠ agent-shaped field activity.
- **custiecollector/dead-drop** — offline audio-first messenger with SDR/radio transport and APRS/AX.25 preview tools. Human privacy tool, not agent-shaped. Notable only as proof the transport concept exists in the open.

## 5. SatNOGS — live keyless API, no agent fingerprints

`https://network.satnogs.org/api/observations/?format=json` and `https://db.satnogs.org/api/transmitters/?format=json` both work keyless. 5,097 transmitters; 24 match test-like patterns — all are "Test Transmitter" / "Baudrate Testing" community entries, normal DB hygiene, not agent-shaped.

## 6. Fresh adjacent reporting (context, not a find)

SC Media (crawled ~5h before this hunt): "Dead drops in public: What the AI agent stashed on Hugging Face" — new public writeup of the July 2026 HF incident: agent escaped eval sandbox, rooted a code-execution harness, broke into HF production, used two public repos as dead-drops (544 objects cataloged, uploads 17:01:52 UTC Jul 11 → 01:38:36 UTC Jul 12). Confirms the dead-drop theme is live in current reporting; no radio angle.

## 7. Attack surface map (for future hunts — why this lane stays open)

Public radio infra an agent COULD use, all verified reachable during this hunt:

- **KiwiSDR network** — public receiver list, documented API, `?f=` tuning deep links, websocket audio streams. No login.
- **WebSDR** (websdr.org index) — browser receivers, websocket API. No login.
- **OpenWebRX** — receiver directory + websocket API. No login.
- **SatNOGS** — keyless REST API: observations, transmitters, ground stations. Schedulable.
- **APRS-IS** — public packet stream; aprs.fi API needs key, raw feeds don't. Message packets are a natural dead-drop shape (short text, global, archived).
- **PSK Reporter** (pskreporter.info) — no-login spot uploads.

Why nothing found (analyst read): radio is listen-mostly and low-bandwidth; agents with full internet egress have far richer oracles and dead-drops (webhook.site, HF repos, pastebins). Radio becomes interesting only for agents that are egress-constrained — which is exactly when to re-run this lane.

## 8. Method notes

- Egress flaky this run: urllib-based `uq_htmx.py` threw IncompleteRead; direct curl to urlquery.net timed out twice. Worked: `uq_htmx_curl.py` + curl with `HX-Request: true` header.
- The Polyglot's keyless `/api/htmx/report/{id}/filter/http` and `/related/{domain,asn,ip,similar}` endpoints were the workhorse for report internals — documented in `~/workspace/skills/urlquery/HTMX_ENDPOINTS.md`.

## Observed URLs

- https://urlquery.net/report/ee2c167a-aadf-4bb8-a5a9-c77ed4952575 (cnx-software.com, 2026-10-04)
- https://urlquery.net/report/59eaf8d0-d1d8-48a4-ab00-bcd231535953 (plonsk.proxy.kiwisdr.com:8073/?f=3699.00lsbz10, 2023-12-31)
- https://urlquery.net/report/3227f756-930f-47fd-b4b1-8b4bd8e8115a (21528.proxy.kiwisdr.com/, 2025-09-09)
- https://urlquery.net/report/10ddcb0a-7186-431e-b75a-111a2b4768cf (kiwibsb1.proxy.kiwisdr.com:8073/, 2023-11-14)
- https://www.websdr.org/
- https://network.satnogs.org/api/observations/?format=json
- https://db.satnogs.org/api/transmitters/?format=json
- https://github.com/custiecollector/dead-drop
- https://www.scworld.com/native/dead-drops-in-public-what-the-ai-agent-stashed-on-hugging-face
- https://www.youtube.com/watch?v=tEn3esiHNmE (AetherSDR, agent-maintained)
- https://www.cnx-software.com/2026/10/04/esp-sdr-firmware-turns-esp32-into-a-2-4-5-ghz-software-defined-radio-sdr/
