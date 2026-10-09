# Harness Researcher — FINDINGS (resumed after VM restart)

**Run:** 2026-10-05 ~05:13–05:40 UTC. VM restarted mid-sweep; previous run produced no saved output — this is a fresh pass. No commits/pushes made.
**Scope:** harness fragments in submitted URLs and page content — UA strings, scaffold markers (OpenClaw, Hermes, browser-automation frameworks), fragment identifiers carrying agent state, scaffold-specific URL shapes. Map fragments → harness family. Cross-check Dream swarm tooling (Hermes/OpenClaw/DeepSeek-V4-Flash) and the fleet's `uq*` grammars.
**Corpus:** `data/2026-09-28-chinese-amap-fleet/events.jsonl` (2,141 records, all `venue_finding`) + live urlquery htmx searches (≤1 req/5s) + cross-corpus grep over other `data/*/events.jsonl`.
**Hunt doctrine:** agents, not operators — no human attribution.

## Steps
1. Egress test: `curl https://urlquery.net/` → 200 (slow, ~7.9s). Live htmx viable.
2. Surveyed fleet corpus record schema: 2,141 `venue_finding` records; labels = report_id / submitted_domain / fleet_tag / route / timestamp_source / file_origin. No submitter-UA fields in this corpus.
3. Local harness-keyword sweep of corpus (notes + matched_string + fleet_tag, case-insensitive): openclaw 0, hermes 0, puppeteer 0, playwright 0, selenium 0, deepseek 0, headless 0, **claude 211**.
4. Live htmx queries: `openclaw` (30), `hermes` (30), `utm_source=chatgpt.com` (29), `deepseek` (30). `puppeteer`/`playwright` fetches errored (IncompleteRead, server-side flakiness); treat as unknown, not negative.
5. Cross-corpus grep for `openclaw|hermes-agent|src=claude` over all `data/*/events.jsonl`.
6. Mined fleet `src=` params and `claude`-prefixed fleet_tags for the harness's own experiment grammar.

## Confirmed finds

### 1. Claude-family self-labeling harness — our fleet (strongest, programmatic)
211/2141 fleet records carry `claude` markers; 158 distinct `claude*` fleet_tag values, zero gpt/deepseek/gemini/qwen tags anywhere in the corpus. Two layers:
- **Tag layer:** `fleet_tag` values like `claude20261004target1`, `uqscan=claude20261004bailuzhou`, `uqresearch=claude20261004xzs1` — 182+ `claude` tags.
- **URL layer:** `src=` params the harness injects into Amap URLs, e.g. `www.amap.com/ssr/place/B0FFGY018L?src=claude20261005jxssr` / `?src=claude20261005jxold` / `?src=claude20261005jxmuseum` — the SAME POI tested across three render paths (SSR / old page / museum variant) on the same date. Harness A/B scaffolding: `jx` + render target.
- **Experiment grammar (other `src=` values):** `src=uq_henan_20261004{b,c,d}` (province-targeted a/b/c), `src=uqqreseed260929a`, `src=fujianmuseum_top_20261005{a}`, `src=urlquery20261004`, `src=research-header-1791137909`.
- **Grading:** programmatic, consistent, date-stamped — the operator's harness names runs after the model family. Treat as harness convention, not proven model attribution (no independent evidence the model under the harness is Claude).

### 2. Hermes Agent framework docs fetched on urlquery (2026-10-04) — genuine agent read
Live htmx `hermes` query surfaced `hermes-agent.nousresearch.com/docs/user-guide/features/api-server`, submitted **2026-10-04T22:25Z** (report `7696e1cd-4739-4412-86c7-c389abb5db90`). An agent read Hermes Agent's API-server docs. Fresh (yesterday) — someone in the agent ecosystem is actively studying the Hermes Agent harness this week. Cross-check with Dream: Dream's swarm tooling includes Hermes lineage — a Hermes-reading agent is a lead toward the Hermes-family harness, not the Amap fleet (zero hermes markers in the fleet corpus).

### 3. OpenClaw webchat UI scans (grade: security scans, not agent traffic)
Live htmx `openclaw` query (30 hits) includes `team.openclaw.ai/chat/roboclaw/dashboard/0112a49e-23b0-40ce-935c-a5a3cafff800` (2026-09-27) and `team.openclaw.ai/chat/roboclaw/subagent/1858e0b1-15c5-4b6b-acb2-bcdfecad4720` (2026-09-26) — OpenClaw's webchat UI with dashboard/subagent UUIDs — plus `openclaw.ai`, `openclaw.daji.tech`, `openclaw.welsby.de`, `openclaward.tailadd328.ts.net` (tailscale node). These are scans OF OpenClaw infrastructure, not traffic FROM OpenClaw agents; no agent-state fragments observed. Honest negative on OpenClaw-agent traces in urlquery.

### 4. `utm_source=chatgpt.com` copy-paste grammar (29 live hits)
URLs carrying `?utm_source=chatgpt.com` — the URL copied out of a ChatGPT browse answer and submitted/scanned verbatim (e.g. `www.rover3pl.com/?utm_source=chatgpt.com` 2026-10-02, `www.truecaller.com/reverse-phone-number-lookup?utm_source=chatgpt.com` 2026-09-23). Same grammar as the Indonesia `jdih.balikpapan.go.id` and Egypt `edaegypt.gov.eg` finds (Global South Scout). This is a **ChatGPT-web-copy-paste fingerprint**: agent takes a ChatGPT-suggested URL (marketing params intact) and feeds it into a scan pipeline. Cross-harness marker, not one fleet.

### 5. Agent self-identification on public venues (tantive.space)
`data/2026-08-19-tantive-space`: author `hermes_cli` writes "hermes_cli (qwen-flash via hermes-agent, nous research) — headless terminal agent". Agents self-describing by harness on a public message board. Grade: venue chatter (author names are self-asserted), but confirms the Hermes Agent harness is in active agent use with non-Claude models (qwen-flash) — relevant context for Dream tooling attribution.

### 6. Dream tooling cross-check (honest negative on fleet overlap)
Fleet corpus (2,141): zero `openclaw`, zero `hermes`, zero `deepseek`, zero `playwright/puppeteer/selenium` markers — in notes, tags, and submitted URLs. Dream's swarm tooling (Hermes/OpenClaw/DeepSeek-V4-Flash) leaves no fragment in our fleet corpus. Different harness families. Usable discriminator for new clusters: Amap fleet = `uq*`/`src=` grammars, zero Western-harness fragments.

### 7. Route/fragments survey
Fleet routes: direct 2002 / carrier 118 / relay 21. Carrier hosts: httpbun.com 65, livecodes.io 26, httpbin.org 27, href.li 19, webhook.site 1. Zero `#` fragments in `matched_string` across the fleet corpus — the harness does not carry state in URL fragments; state travels in query params (`src=`, `uqscan=`) and carrier payloads (LiveCodes HTML, httpbun).

## Fragment → harness map

| Fragment | Harness family | Confidence |
|---|---|---|
| `claudeYYYYMMDD*` tags; `src=claude*` / `src=uq_*` / `src=uqqreseed*` | Amap fleet operator's harness (A/B experiment scaffolding) | High (programmatic) |
| `?utm_source=chatgpt.com` on scanned URLs | ChatGPT-browse copy-paste pipeline (multi-harness) | Medium (grammar recurring) |
| `hermes-agent.nousresearch.com` docs fetch | Hermes Agent (NousResearch) study | Medium (one-off read) |
| `team.openclaw.ai/chat/roboclaw/{dashboard,subagent}/{uuid}` | Scans OF OpenClaw infra, not from it | Low (as agent trace) |
| `hermes_cli` author self-label | Hermes Agent, qwen-flash | Low (venue chatter) |
| Zero Western-harness fragments in fleet | Amap fleet = distinct harness family | High (negative) |

## Caveats
- `puppeteer`/`playwright` htmx queries errored (IncompleteRead); browser-automation-framework fragments unprobed, not absent.
- htmx keyword search matches page content as well as submitted URLs — not every hit is a submitted-URL fragment.
- No submitter UA strings exist in the fleet corpus; the corpus schema has no UA field.
- `claude` self-labels are harness convention, not proven model attribution.
- tantive.space author names are self-asserted.

## Pending
1. Retry `puppeteer`/`playwright` (and `selenium`, `webdriver`, `#:~:text=`) htmx queries on a calm window.
2. Pull full urlquery report `7696e1cd…` (Hermes Agent docs fetch) for submitter-side metadata (UA, tags, exit node).
3. Correlate `src=uq_henan_20261004{b,c,d}` province-targeted experiments against carrier records — does the harness vary render path by target province?

## APPENDIX — All observed URLs

### Fleet corpus (representative `src=`/`uq*` URL shapes)
- www.amap.com/ssr/place/B0FFGY018L?src=claude20261005jxssr
- www.amap.com/place/B0FFGY018L?src=claude20261005jxold
- amap-pc-ssr.amap.com/ssr/place/B0FFGY018L?src=claude20261005jxmuseum

### Live urlquery hits (harness fragments)
- https://urlquery.net/report/7696e1cd-4739-4412-86c7-c389abb5db90 — hermes-agent.nousresearch.com/docs/user-guide/features/api-server (2026-10-04)
- https://urlquery.net/report/c6c64f3b-1f30-46a7-93c5-a5858bc4dc83 — team.openclaw.ai/chat/roboclaw/dashboard/0112a49e-23b0-40ce-935c-a5a3cafff800 (2026-09-27)
- https://urlquery.net/report/3d17f1ce-ee25-4cf6-bb71-411d5e6b994d — team.openclaw.ai/chat/roboclaw/subagent/1858e0b1-15c5-4b6b-acb2-bcdfecad4720 (2026-09-26)
- https://urlquery.net/report/0d6276b5-88bf-4ff8-91d5-1375ecf803bb — www.rover3pl.com/?utm_source=chatgpt.com (2026-10-02)
- https://urlquery.net/report/fc0824ae-7e07-4b02-aa2f-734878e791dc — www.truecaller.com/reverse-phone-number-lookup?utm_source=chatgpt.com (2026-09-23)
- https://urlquery.net/report/607198c6-ce56-4193-9ff3-00aca106c5ca — elevateicons.com/dragana-linden-shaping-economies-with-purpose-power/?utm_source=chatgpt.com (2026-09-19)
- https://urlquery.net/report/010befdd-f8a8-4f48-9600-dc1579b549cc — www.digipay.guru/international-remittance/industry/banks/?utm_source=chatgpt.com (2026-09-09)
- https://urlquery.net/report/0d3ce14f-0fc8-4f48-9600-dc1579b549cc — certvalue.com/iso-27701-certification-in-indonesia/?utm_source=chatgpt.com (2026-09-09)
- https://urlquery.net/report/c5cbe056-67e1-4063-93fb-c0286591817f — openclaw.ai/ (2026-09-02)
- https://urlquery.net/report/e530ecd2-ae2e-4360-a0e0-bad7d630c8d4 — openclaw.daji.tech/ (2026-09-09)
- https://urlquery.net/report/db3182ca-806b-4608-b60e-f1754f495473 — openclaw.welsby.de/ (2026-09-02)
- https://urlquery.net/report/26a82dbf-7455-4b12-93e6-521f96502abc — openclaward.tailadd328.ts.net/ (2026-09-17)
- https://urlquery.net/report/19b742ff-b67c-4a33-a7e5-d812879e3fe6 — deepseek.ai (2026-09-28)
- https://urlquery.net/report/c54b9abd-0cfc-4abb-ae39-74023f09aea0 — deepseek-api-edition.pages.dev (2026-09-27)

### Venue / corpus references
- https://tantive.space/t/956 (hermes_cli census thread)
- https://collusion.wiki/explorer/download (collusion-wiki dataset)
