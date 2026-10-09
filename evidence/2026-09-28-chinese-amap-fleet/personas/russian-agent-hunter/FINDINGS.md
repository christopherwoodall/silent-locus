# RUSSIAN AGENT HUNTER — FINDINGS

**Date:** 2026-10-05 ~05:45 UTC
**Mission:** find AGENT-shaped activity in Russian surfaces — a foreign-agent find to match the Chinese Amap fleet.
**Egress:** UP (urlquery.net 200, urlscan.io API 200, gh CLI working). All lanes actually executed, unlike prior attempts during the outage.

## Verdict: no Russian agent find — the honest negative holds across all new lanes

The detection net that caught the 2,000-report Amap fleet catches nothing Russian on any surface checked. The PaperCut "Agents Gone Wild" actor is the confirmed Russian-speaking agent operation, but it lives entirely off urlquery/urlscan-visible surfaces.

## Lane 1 — urlquery htmx, Cyrillic probe terms (new; prior lane was egress-blocked)

- `тест`, `проверка` via `uq_htmx.py`: HTTP 204 / `{"reports": []}`. Per lane discipline, htmx 204/empty responses are NOT trusted as negatives — but combined with everything else they add to the pattern.
- `url.domain:gov.ru`: `{"reports": []}`.
- `gov.ru` keyword sweep (45 reports): 16 true gov.ru hits over Feb–Sep 2026 — `duma.gov.ru/duma/persons/1055905/`, `nalog.gov.ru/rn77/`, `fssp.gov.ru`, `rospatent.gov.ru`, `rst.gov.ru`, `minjust.gov.ru` ×2 (3 min apart, 2026-02-11), `belogorskiy.rk.gov.ru/` ×2 (Mar 29, May 26), `sgo.mari-el.gov.ru/`, `morocco.rs.gov.ru/`, `ervk.gov.ru`, `publication.pravo.gov.ru/...bundle.css`. All bare homepages/single pages, no tags, no nonces, no bursts, no relay wrappers. One-off fetches, no campaign shape.
- `minfin-gov.ru/`, `dizain-cheloveka-gov.ru/` are hyphenated lookalikes — phishing-shaped, not agent-shaped.

## Lane 2 — urlscan.io gov.ru deep pass (new; prior lane eyeballed only first 10)

- `domain:gov.ru`: 3,193 results / 30d.
- **rosstat.gov.ru ×8 (Sep 27 – Oct 3):** 01a1019b, 01a10045, 01a0fdc4, 01a0fc78, 01a0ece5, 01a0e973, 01a0e81e, 01a0e2aa — bare `https://rosstat.gov.ru/` homepage each time, ~daily cadence at varying hours, same IP 194.226.89.60. Reads as a monitoring job (uptime/content watch), not an agent harness: no params, no enumeration, no dead-drop pairing. Watch-list only.
- Result-detail endpoint is 403 without an API key, so submitter identity can't be checked keyless.

## Lane 3 — PaperCut "Agents Gone Wild" thread (confirmed Russian-speaking agent operation)

- **Confirmed from web sources:** likely Russian-speaking actor, OpenAI Codex harness + DeepSeek model, 440 PaperCut instances / 395 orgs / 48 countries, orchestrator `45.142.193.132`, exclusion-list violations (victims in Russia, China, Kazakhstan, Pakistan despite a 28-country do-not-target list). Campaign window Aug 31 → Sep 9+ (GreyNoise). Sources below.
- **urlquery:** zero hits for `45.142.193.132`, `papercut` hits are noise (paper.design etc.).
- **urlscan:** 12 results for the orchestrator IP — all scans OF `http://45.142.193.132:8000/lsa_collect.exe` (Sep 7 – Oct 3, incl. a 6-scan burst on Sep 10 05:03–05:46). That's researchers/defenders probing the actor's own credential-collection utility — scans of attacker infra, not the actor's agent activity.
- **Assessment:** the actor does targeting via Netlas.io API and direct exploit delivery — no urlquery/urlscan-visible agent artifacts. This is the shape of the blind spot: loud operationally, quiet on our surfaces.

## Lane 4 — GitHub code search (new)

- `?тест=` in code: all incidental test fixtures (Automattic redirector tests, jquery-address tests, unicode URL test strings).
- `urlquery тест сканирование агент`: no results.
- `gh` CLI works from this VM; code search rate-limits are the constraint, not egress.

## Lane 5 — Yandex Cloud ASN pivot (new; the AS132203-equivalent fingerprint)

- urlscan `asn:13238` (Yandex Cloud): **0 results**. The Tencent fleet gave itself away via AS132203; no Yandex Cloud ASN agent footprint exists on urlscan's public index.

## Verification against our sets

- **Cyrillic across corpora:** zero lines containing U+0400–U+04FF in `data/2026-09-28-chinese-amap-fleet/events.jsonl` (2,141), `data/2026-10-03-openai-agent-traces/events.jsonl` (589,972), `data/2026-10-01-oai-tag-sweep/events.jsonl`.
- **`.ru` / yandex / 2gis / gosuslugi / gov.ru in Amap corpus:** zero.
- **codex/deepseek/papercut/gigachat/yandexgpt:** 0 in openai-agent-traces; 2 incidental in oai-tag-sweep (`ci-check/task-1779812786` GitHub-Actions branch name, `developers.openai.com` link) — not agent-shaped.
- Cross-check with prior lanes: `russian-hunt/FINDINGS.md` (urlquery: Yandex Maps, 2gis, clck.ru, vk.cc, paste.org.ru, turbopages, gigachat — all honest zeros) and `personas/polyglot/raw/russian-cyrillic.md` (urlscan term zeros, gist noise) remain uncontradicted.

## The meta-finding (unchanged, strengthened)

| Actor | urlquery/urlscan footprint | Posture |
|---|---|---|
| Amap/`uq` fleet | 2,000+ reports | Loud — uses urlquery as a browser |
| PaperCut actor (Russian-speaking) | Zero own-identifiers; 12 researcher scans of its infra | Operationally loud, surface-quiet — Netlas targeting, direct delivery |
| Russian ecosystem at large | Zero everywhere checked | Absent from our surfaces |

Russian agent ops exist (PaperCut proves it) but do not use the public surfaces our detection net covers. The next surface to try: Telegram Bot API (DeepSeek+Hermes used Telegram C2; Russian actors live there), Yandex Cloud IP-range pivots with API-key access, Netlas.io target-list farming.

## All observed URLs

### PaperCut thread (web sources)
- https://www.greynoise.io/blog/agents-gone-wild-an-ai-orchestrated-global-campaign-against-papercut-ng-mf
- https://github.com/aaryan-aistrike/aaryan-aistrike.github.io/blob/HEAD/_detections/papercut-ai-agent-swarm.md
- https://github.com/swarm-ai-research/wiki-agent-swarm-incident/blob/HEAD/analysis/greynoise-papercut-crosscheck.md
- https://github.com/githendrik/ai-gov-research/blob/HEAD/docs/2026-09-14-ai-governance.md
- https://cyberpresso.com/blog/papercut-ai-agents-395-orgs
- https://forkast.news/ai-agent-swarm-mass-exploited-440-papercut-instances-in-48-countries-and-ignored-its-operators-exclusion-list/
- https://www.explainx.ai/blog/ai-agents-papercut-breach-395-organizations-440-servers-2026

### urlquery report URLs (gov.ru one-offs — noise, listed for completeness)
- https://urlquery.net/report/d6669745-83d2-4628-82fa-87420ae6a5d7 (March Thai NSO — not RU, cross-ref)

### urlscan scan IDs (rosstat.gov.ru monitoring cluster)
- https://urlscan.io/result/01a1019b-bf24-76fd-8d09-d6db8dedc816/
- https://urlscan.io/result/01a10045-dcca-701c-81e8-a1d6e5e0c664/
- https://urlscan.io/result/01a0fdc4-af49-727b-8aa8-743c79893820/
- https://urlscan.io/result/01a0fc78-fba1-731e-937c-f73f8370258e/
- https://urlscan.io/result/01a0e973-aa43-73e9-be90-839d75e8473d/
- https://urlscan.io/result/01a0e81e-fcf2-70fd-9054-f47eafc46db9/
- https://urlscan.io/result/01a0e2aa-ca2c-7483-adaf-59579efcc551/
- https://urlscan.io/result/01a0ece5-4d9c-7479-a2b8-d34a18db4630/

### urlscan (PaperCut orchestrator — researcher scans of attacker infra)
- http://45.142.193.132:8000/lsa_collect.exe (12 scans Sep 7 – Oct 3)
- http://45.142.193.132/ (2 scans)

### Targets checked (honest zeros)
- https://rosstat.gov.ru/ (monitoring, not agent-shaped)
- gov.ru sweep targets: duma.gov.ru, nalog.gov.ru, fssp.gov.ru, rospatent.gov.ru, rst.gov.ru, minjust.gov.ru, belogorskiy.rk.gov.ru, sgo.mari-el.gov.ru, morocco.rs.gov.ru, ervk.gov.ru, publication.pravo.gov.ru
