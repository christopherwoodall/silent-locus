# Polyglot hunt: Russian / Ukrainian / Kazakh agent traces
**Date:** 2026-10-04 ~23:37–23:50 CDT (Mon)
**Worker:** polyglot hunt subagent (depth 2/2)
**Scope:** AGENT (not human/operator) activity on public infrastructure where task labels, search queries, or tag grammars are in RUSSIAN, UKRAINIAN, or KAZAKH (Cyrillic). Shape-first: metronomic timing, systematic enumeration, burst parallelism, consistent tag/param grammars = agent-shaped. Agents and swarms only — no human/operator identity work.

## Method
- urlquery keyless htmx (`uq_htmx.py search`) — **unreachable this session** (see lane notes)
- urlscan.io public search API (`https://urlscan.io/api/v1/search/?q=...`) via browser.open — works, 30-day window
- browser.search for gists/pastes with native-language probe strings

---

## urlquery searches (lane FAILED — infrastructure, not verdicts)

Attempt 1 (`uq_htmx.py search --query "тест" --limit 20`):
- Failed at network level: urllib proxy-tunnel `TimeoutError` after 60s (`urlopen error timed out`).
- Retried the same htmx endpoint with `curl` directly: `Connection timed out after 45s` (HTTP 000).
- Control check: `curl` to `https://urlscan.io/api/v1/search/?q=test` also timed out (HTTP 000) from the VM — direct VM egress to these hosts is down this session.
- One `browser.open` attempt on the htmx endpoint (`https://urlquery.net/api/htmx/search/?q=тест&limit=20&offset=0`) returned HTTP 204 empty — the endpoint requires `HX-Request` headers that browser.open cannot set, so the response is not a real result. Not retried.

**No urlquery searches completed. urlquery budget consumed: 1 failed attempt of the 12-query allowance (no successful queries).**
**Verdict: could not check** — the entire Cyrillic-on-urlquery surface (query-param grammars `?тест=`, `?поиск=`, tags, submitter bursts) is a blind spot this session. Retry lane when VM egress to urlquery.net recovers.

---

## urlscan.io searches (all valid responses, 30-day index window)

### Term searches — all ZERO results (honest zeros)
| # | Query (URL-encoded) | Meaning | Results |
|---|---|---|---|
| 1 | `тест` | RU test | 0 |
| 2 | `поиск` | RU search | 0 |
| 3 | `агент` | RU agent | 0 |
| 4 | `сканирование` | RU scanning | 0 |
| 5 | `проверка` | RU check | 0 |
| 6 | `пошук` | UK search | 0 |
| 7 | `іздеу` | KZ search | 0 |
| 8 | `proverka` | Latin translit | 0 |
| 9 | `poisk` | Latin translit | 0 |

Caveat: urlscan's keyless free-text index covers task URL / page URL / domain / title / IP / ASN fields. Bare Cyrillic terms returning 0 means no recent public scan has these strings in indexed fields. **URL query-parameter values may not be indexed at all** (urlscan canonicalizes task URLs; param-value search is effectively an API-key feature), so `?тест=123` artifacts could exist undetected. Field-scoped wildcard attempt (`task.url:*тест*`) was rejected with HTTP 403 and not retried.

### Dead-drop / tunnel sweep: `webhook.site` (20 results sampled)
All English-language pages; no Cyrillic titles or URLs. Recent items:
- `webhook.site/15c90e66-.../undefined?otp=...` — 2026-10-04, tags: hybridanalysis, phishing-style OTP URL (noise)
- `webhook.site/577b82c3-...`, `/0ef0dcf7-...`, `/9dbf1485-.../x.xml` — token-not-found / rate-limit pages (noise)
- `webhook.site/` homepage scans (noise)
**Verdict: noise.** No Cyrillic labels paired with dead-drop infra in the recent window.

### CIS gov-target sweeps (burst/systematic check)
- **`domain:gov.ru`** — 3,193 results / 30d. First 10: one-off homepage fetches (`pension.sprrt.ru` 2026-10-04T04:01Z; `mintrans.gov.ru` 2026-10-03T23:57Z; `rosgvard.gov.ru` 2026-10-03T23:13Z; `cert-med.minzdrav.gov.ru`; `portal.audit.gov.ru`). One faint systematic pattern: **`rosstat.gov.ru` scanned 4× on Oct 2–3** (uuids `01a1019b`, `01a10045`, `01a0fdc4`, `01a0fc78`), all bare homepage fetches, 35–106 requests each, normal page fingerprints, no Cyrillic params, no custom tags. **Verdict: inconclusive** — repeat polling reads more like monitoring than an agent harness; no shape signals (no metronomic timing, no enumeration of paths/params, no tunnel/dead-drop pairing). Noted, not a lead.
- **`domain:gov.kz`** — 42 results / 30d. First 10: `eps-test.gov.kz` ×2 (Oct 1 & 3), `helpdesk.cts.gov.kz` ×2 (Sep 27 & 30), `esf.gov.kz:8080/esf-web/ws/api1` (CXF service list — mildly interesting recon-ish surface, one-off), `pki.gov.kz`, `adilet.gov.kz`, `rsp.gov.kz/kz`, `kgd.gov.kz/kk`. Bare homepages, no params, no tags. **Verdict: noise.**
- **`domain:gov.ua`** — 278 results / 30d. First 10 include repeated scans of **mil.gov.ua streaming subdomains** (`w-live2.streaming.delta.mil.gov.ua` ×2 Oct 3–4, `lk-live22...`, `vms2-live2...`, `turn-live-stg...`) — 2-request bare-host probes, HTTPS-only redirects, no params. Plus `kyivcity.gov.ua`, `cert.gov.ua/news/42`, `nszu.gov.ua`, `cluster-gov-ua.pages.dev`. **Verdict: inconclusive** — the mil.gov.ua streaming-subdomain cluster is the only vaguely systematic pattern; reads like infrastructure monitoring (tiny request counts, no enumeration), not an agent-shaped task family. Noted, not a lead.

---

## Gists / pastes (browser.search)

| # | Query | Result |
|---|---|---|
| 1 | `site:gist.github.com агент тест автоматический сканирование` | **No results** |
| 2 | `gist.github.com OR pastebin.com "пошук" OR "іздеу" агент тест скрипт` | **Noise** — one hit: Nigerian vaccination.gov.ng PDF about writing Pastebin API scripts (unrelated) |
| 3 | `"urlscan" OR "urlquery" тест сканирование сайтов автоматический скрипт python` | **No results** |
| 4 | `"localhost.run" OR "webhook.site" тест бот сканирование агент python` | **Noise** — Russian Telegram-bot beginner tutorials (kuchaknig.org, aldebaran.one PDFs), unrelated |
| 5 | `"/?тест=" OR "?поиск=" OR "?проверка=" url` | **Noise** — GitHub QA-automation sandboxes (`snower87/qa-automation-sandbox`), an ideone C# paste, a physics repo (`dimius0/spectravortex`). All matched incidental Russian prose, not scan artifacts |

**Verdict: no agent-shaped Cyrillic artifacts on indexed gists/pastes.**

---

## Leads summary

| Lead | Verdict | Why |
|---|---|---|
| Cyrillic terms on urlscan (9 term queries) | **noise (honest zero)** | 0 hits across RU/UK/KZ terms + Latin transliterations in the 30-day public index |
| webhook.site + Cyrillic pairing | **noise** | No Cyrillic labels in recent webhook.site scans |
| `rosstat.gov.ru` ×4 scans (Oct 2–3) | **inconclusive** | Repeat polling, bare homepages, no agent-shape signals; watch-list only |
| `mil.gov.ua` streaming-subdomain cluster (Oct 3–4) | **inconclusive** | Bare-host 2-request probes; reads like monitoring, no enumeration or labels |
| gov.kz repeat scans | **noise** | One-off homepages |
| Gist/paste Cyrillic probe strings | **noise (honest zero)** | No results / unrelated tutorials |

**Bottom line: no agent-shaped RU/UK/KZ activity found.** Every query returned either a clean zero or unrelated noise. This is an honest-negative lane this session.

## What could NOT be checked
1. **urlquery entirely** — VM egress to urlquery.net is down (TCP timeouts via urllib and curl; htmx endpoint needs HX headers browser.open can't set). The task's primary lane (`?тест=`, `?поиск=` param grammars, tags, submitter bursts) is unchecked. Retry when egress recovers; budget was 1 failed attempt of 12.
2. **urlscan query-parameter values** — keyless free-text search may not index param values; `task.url:*тест*`-style field wildcards are 403'd keyless. Cyrillic param artifacts could exist but be invisible without API-key access.
3. **Deeper gov-target enumeration** — only the first 10 of each domain sweep were eyeballed (gov.ru has 3,193). A systematic pass over the full result sets (timing metronomy, submitter clustering) would need API-key pagination.
4. **Ukrainian gov targets beyond domain sweep** — `gov.ua` sweep was homepage-level only; no `?тест=`-style param search possible keyless.
5. **GitHub code search / raw paste APIs** — browser.search only; no direct gist API or pastebin scraping was attempted.

## Notes
- All urlscan results are public-visibility tasks, `method: api` for the sampled items — consistent with automated submitters but not Cyrillic-labeled.
- urlscan index is 30-day rolling; any pre-September 2026 Cyrillic campaign is out of reach keyless.
- Do NOT push this file (per task).
