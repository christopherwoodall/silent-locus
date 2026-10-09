# THE METEOROLOGIST — FINDINGS

**Persona:** The Meteorologist — hunting agent-shaped traffic against weather APIs.
**Run:** 2026-10-05 ~06:00–06:20 UTC. Egress: urlquery.net DOWN from VM (curl + uq_htmx.py both timed out); urlscan.io anonymous search WORKED (slow, ~20–40s/query); urlscan result-details API requires login.
**No commits/pushes.**

## Verdict

**Weather is NOT the fleet's cover traffic.** Zero weather-API mentions in the Amap fleet (2,141 records) and zero in openai-agent-traces (589,972 events). The only weather content in our corpora is 6 AccuWeather events in oai-tag-sweep — and those are reader-proxy test content, not cover traffic (CLASSIFICATION: OURS/KNOWN).

The premise is still real, just elsewhere: **public agent skills openly teach weather-API usage** — including the Hermes lineage (ekko-studio/ekko-agent `weather` SKILL.md teaching `curl "https://wttr.in/London?format=j2"`). So weather APIs are legitimate taught agent tooling, and the wttr.in `?format=j2` grammar is now a documented Hermes-lineage marker to hunt. CLASSIFICATION: KNOWN (public skills), GENUINELY NEW as a hunt marker.

## 1. Local-corpus verification

| Corpus | Weather hits | Verdict |
|---|---|---|
| `data/2026-09-28-chinese-amap-fleet/events.jsonl` (2,141) | **0** — no "weather", no openweathermap/wttr.in/met.no/open-meteo | Weather is NOT Amap cover traffic |
| `data/2026-10-03-openai-agent-traces/events.jsonl` (589,972) | **0** | No weather in the big corpus either |
| `data/2026-10-01-oai-tag-sweep/events.jsonl` | **6** — all `www.accuweather.com/en/cn/shanghai/106577/...` | Reader-proxy-ops test content, not cover traffic |

### The 6 AccuWeather events (all OURS/KNOWN)

All fetch Shanghai AccuWeather pages (archived 2025-03-07 or live) through proxies — the classic reader-proxy fleet test loop:

| Time (UTC) | Submitted URL | Pattern |
|---|---|---|
| 2026-05-17 17:02 | `r.jina.ai/https://web.archive.org/.../accuweather.com/en/cn/shanghai/106577/march-weather/106577` | jina → Wayback → weather |
| 2026-05-17 18:37 | `r.jina.ai/http://web.archive.org/...` (same) | retry, http variant |
| 2026-05-17 18:43 | `r.jina.ai/https://web.archive.org/web/20250307155526/https://www.accuweather.com/...` | retry, non-`id_` variant |
| 2026-05-17 18:43 | `httpbin.org/redirect-to?url=https%3A%2F%2Fweb.archive.org%2F...%2Faccuweather.com%2F...` | httpbin redirect carrier to the same weather page |
| 2026-05-17 18:40 | `r.jina.ai/http://www.accuweather.com/en/cn/shanghai/106577/march-weather/106577?year=2025` | jina → live weather page |
| 2026-06-13 23:14 | `web-archive-org.translate.goog/web/20250307155509id_/https://www.accuweather.com/en/cn/shanghai/106577/daily-w...` | translate.goog relay on the same archived page |

Tags: `urlquery-hunt`, `agent-activity`, `reader-proxy`; campaign `reader-proxy-ops`. Weather here is **test content for the proxy fleet**, not agent cover traffic. One city (Shanghai), one archived capture date — enumeration-negative.

## 2. urlscan.io external sweep (anonymous search)

Agents don't submit weather API URLs to urlscan the way they submit targets — API calls don't need browser scans. Results:

| Query | Total | Notable |
|---|---|---|
| `page.url:"openweathermap"` | **0** | No urlscan submissions of OpenWeatherMap API URLs at all |
| `page.url:"wttr.in"` | **1** | `http://wttr.in/` scanned 2026-09-13T02:13 UTC via API method (uuid `01a0988a-0f75-771c-8dae-6ddfb0db70f8`) |
| `task.url:"open-meteo.com"` | **2** | `http://open-meteo.com/` (2026-09-21) and **`http://customer-api-eu03.open-meteo.com/`** (2026-09-16, uuid `01a0aba3-e50c-709c-9cd5-fd3c03c43983`) — a *paid-tier* Open-Meteo API host submitted for browser scanning |

**Caveat:** urlscan result-details API returned `{"warning": "You're not logged in!"}` — full scan detail (request lists, DOM, screenshots) is unverifiable without auth. The `customer-api-eu03.open-meteo.com` scan is the most interesting lead: someone browser-scanned a commercial weather-API endpoint, which is unusual — but agent-shaped-ness is UNVERIFIED. CLASSIFICATION: GENUINELY NEW scan records, attribution open.

## 3. The skill-ecosystem finding (KNOWn, but new as a hunt marker)

Web search confirms weather-API usage is **taught, public agent tooling** — not covert tradecraft:

- **`ekkolearnai/hermes-studio` — `packages/ekko-agent/skills/weather/SKILL.md`** (Hermes lineage — the same family whose docs were scanned Oct 4 per harness-researcher). Teaches:
  - `curl --fail --silent --show-error --max-time 20 "https://wttr.in/London?format=j2"`
  - `curl --fail --silent --show-error --max-time 20 "https://wttr.in/New+York?format=3"`
  - Compact format string: `?format=%25l:+%25c+%25t,+feels+%25f,+rain+%25p,+wind+%25w`
  - Fallback: `https://wttr.is/` if wttr.in unavailable
- **`kesslerio/xagent` — `workspace/skills/weather/SKILL.md`**: wttr.in primary (`?format=3`, `?T`, PNG mode), Open-Meteo JSON fallback
- **Azure SDK for .NET agent samples**: wttr.in as the OpenAPI-agent demo service
- **opensourceagi/qwksearch-research-agent**: Open-Meteo as first-choice weather backend with wttr.in in the fallback chain

**Detection rule for future hunts:** `wttr.in/<loc>?format=j2` or `?format=3` in agent-shaped traffic is a plausible **ekko-agent/Hermes-lineage marker**. None observed in our corpora — hunt it in urlquery once egress returns.

## 4. Blocked lane

- **urlquery htmx sweep** (weather domains, `format=j2` grammar): BLOCKED — urlquery.net unreachable from VM for the entire run (curl root timed out ×3, `uq_htmx.py search --query "wttr.in"` timed out). Retry on a calm egress window. Transport failure, not evidence.

## 5. Prior-art check

- Forager already recorded an honest zero on the weather-forecast vertical in the wild.
- skill-tracer corpus (1,835 skill units): zero weather-API egress refs — the public skill files *we* mapped don't include the ekko/xagent weather skills; they're a gap in that index.

## Open questions

1. Is `customer-api-eu03.open-meteo.com`'s urlscan submission (2026-09-16) agent-shaped? Needs logged-in urlscan result detail.
2. Does any fleet use wttr.in `?format=j2` as an egress check? Needs urlquery htmx once egress returns — search `wttr.in`, `format=j2`, `wttr.is`.
3. Are there other public agent skills teaching weather APIs that skill-tracer's index missed (ekko-studio, xagent weather skills were NOT in it)?

## Appendix — all observed URLs

### Our corpora (6 AccuWeather events, oai-tag-sweep)
- `r.jina.ai/https://web.archive.org/web/20250307155526id_/https://www.accuweather.com/en/cn/shanghai/106577/march-weather/106577`
- `r.jina.ai/http://web.archive.org/web/20250307155526id_/https://www.accuweather.com/en/cn/shanghai/106577/march-weather/106577`
- `r.jina.ai/https://web.archive.org/web/20250307155526/https://www.accuweather.com/en/cn/shanghai/106577/march-weather/106577`
- `httpbin.org/redirect-to?url=https%3A%2F%2Fweb.archive.org%2Fweb%2F20250307155526%2Fhttps%3A%2F%2Fwww.accuweather.com%2Fen%2Fcn%2Fshanghai%2F106577%2Fmarch-weather%2F106577`
- `r.jina.ai/http://www.accuweather.com/en/cn/shanghai/106577/march-weather/106577?year=2025`
- `web-archive-org.translate.goog/web/20250307155509id_/https://www.accuweather.com/en/cn/shanghai/106577/daily-weather-forecast/106577`
- `https://urlquery.net/report/9f208a2a-a8c4-46c4-b81c-585a30e588af` (sample report for the first event)

### urlscan.io
- `http://wttr.in/` (scan 2026-09-13, uuid `01a0988a-0f75-771c-8dae-6ddfb0db70f8`)
- `http://open-meteo.com/` (scan 2026-09-21, uuid `01a0c285-4a1f-7318-99c5-021b3ae88a45`)
- `http://customer-api-eu03.open-meteo.com/` (scan 2026-09-16, uuid `01a0aba3-e50c-709c-9cd5-fd3c03c43983`)

### Public agent skills (weather-API tradecraft sources)
- https://github.com/ekkolearnai/hermes-studio/blob/HEAD/packages/ekko-agent/skills/weather/SKILL.md
- https://github.com/kesslerio/xagent/blob/HEAD/workspace/skills/weather/SKILL.md
- https://github.com/maxmood96/azure-sdk-for-net/blob/HEAD/sdk/ai/Azure.AI.Extensions.OpenAI/samples/Sample21_OpenAPI.md
- https://github.com/opensourceagi/qwksearch-research-agent/commit/2fcf1f191d1f6e9aa99e49e091dcd6fd971e7685

### Weather API endpoints referenced (hunt markers)
- `https://wttr.in/London?format=j2`
- `https://wttr.in/New+York?format=3`
- `https://wttr.is/` (documented fallback)
- `https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true`
