# FINDINGS.md — Behavioral agent-fleet hunt: Portuguese, Italian, Dutch lanes

Date: 2026-10-04. Tool: `uq_htmx.py search` (undocumented htmx endpoint, `--delay 4` throughout; no 429s hit).
Fingerprint reference: `~/workspace/silent-locus/data/2026-09-28-chinese-amap-fleet/raw/analysis/PATTERN.md`.
Follow-up lead: behavior-hunt/FINDINGS.md §8 — `lhr.life` probe/CORS infrastructure, `uq` tag grammar (`uqscan=`, `uqvnc=`, `/uqcors.html`).

## Method
For each language, ran: (1) map/POI service domains, (2) native tag-grammar shapes `<word>2026`, (3) agentness words × carriers (httpbin/httpbun/webhook.site/jina), (4) native shorteners/pastebins, (5) jina fetch-proxy chains, (6) English tag grammar on language targets, (7) date-burst review, plus (8) lhr.life / uqcors / uq<word>= / probe-tradecast checks from the new lead. A "hit" = systematic, tagged, parallelized, program-shaped activity.

---

## Portuguese — VERDICT: no fleet (honest zero)

- Map/POI: `guiamais.com.br` → 1 report (2026-05-01, bare domain, ordinary scan). `apontador.com.br` → 15: the `api.apontador.com.br/v2/logout?redirectUrl=` URLs (May 2025) are open-redirect phishing abuse (redirects to rasyri.com, bancomontpio.com, slurpmail addresses) and `mini.apontador.com.br` base64 blobs — phishing kits, not agent scans. `viacep.com.br` → 21, all keyword-in-content (unrelated sites). `maplink` → not queried (domain-string searches already saturated); postal API surface shows no systematic scanning.
- Tag grammar: `pesquisa2026`, `busca2026`, `tarefa2026`, `busca202610`, `missao2026` → 0 each.
- Agentness: `agente httpbin/httpbun/webhook.site/r.jina.ai`, `missao httpbin`, `extracao httpbin`, `dados httpbin` → 0 each.
- Shorteners: `encurtador.com.br` → 21 short links over 11 months, 1–2/day max, random codes, no tags, no parallelism — phishing-spam shortener abuse, not a fleet.
- jina chains: `r.jina.ai` ×16 — known Amap fleet relays + 3 Iowa health CSV fetches + newspapers.com (English). Nothing Brazilian/Portuguese.
- English tag grammar: `uqscan .br` → only Amap fleet hits (the `.br` token is effectively ignored); no Portuguese target carries `uqscan=`. `research2026` → 1 unrelated (familylawconsulting.org). `target2026`, `uqtag=`, `uqtag .br` → 0.
- lhr.life/uq-infra lead: `lhr.life` ×80 (2 pages) — all lhr.life subdomains itself, zero Portuguese targets. `uqcors` → 8 = the known Jun-18 lhr.life CORS burst. `uqvnc` → 4 = Amap + AIHW (known). `uqcors .br` style combos not needed: no language targets appeared anywhere in the infra hits.

## Italian — VERDICT: no fleet (honest zero)

- Map/POI: `paginegialle.it` → 24: all keyword-in-content matches on Italian SMB sites (allergen clinics, autofficina, trattoria…) — ordinary browsing, not scans of paginegialle.it. `tuttocitta.it` → 6, old (2023–2025). `immobiliare.it` → 15, keyword-in-content noise. `accorcia.to` → 2 (bare domain, ordinary).
- Tag grammar: `ricerca2026`, `compito2026`, `ricerca202610`, `missione2026`, `verifica2026` → 0 each.
- Agentness: `dati httpbin` → 0. (Italian carrier combos share the `agente` word but were not separately queried; `agente httpbin/httpbun/webhook.site/r.jina.ai` → 0.)
- jina chains: no Italian news/wiki domains on r.jina.ai (`r.jina.ai/h repubblica.it` → 0).
- English tag grammar: `uqscan .it` → 0. `scan2026` → 5 = phishing lures (sharepoint blob "scan2026" scans), unrelated.
- lhr.life/uq-infra lead: zero Italian targets in any `lhr.life`, `uqcors`, `uqvnc`, `uqtag` hit set.

## Dutch — VERDICT: no fleet (honest zero)

- Map/POI: `goudengids.nl` → 1 (`degoudengids.store`, 2026-07-18). `funda.nl` → 6, scattered 2025–2026, ordinary/phishing. `9292.nl` → 3, ordinary. `telefoonboek.nl` → 0. `postnl.nl` → 20: phishing kits (`siayeo.com.sg/.../PostNL/index.php` ×3 on 2026-08-06 — a same-day triplet but a credential-phish, not an agent fleet) + font CDN + Dutch-localized AI chat sites.
- Tag grammar: `zoekopdracht2026`, `taak2026`, `zoek2026` → 0 each.
- Agentness: `missie httpbin`, `extractie httpbin` → 0.
- Shorteners/pastebins: `pastebin.nl` → 0.
- jina chains: `r.jina.ai nu.nl` → 0.
- English tag grammar: `uqscan .nl` → 0.
- lhr.life/uq-infra lead: zero Dutch targets in any `lhr.life`, `uqcors`, `uqvnc`, `uqtag` hit set.

---

## Cross-cutting notes

- **The Amap fleet is still live and visible as the control**: `uqscan` returns the known Chinese Amap tags (`research20261005d`, `wuxizoo20261005a`, `claude20261005mobile1/2` …) dated 2026-10-05 — the grammar-shape checks are working (they find the real fleet), which makes the zeros on the three languages meaningful rather than a search failure.
- **One fleet / one infra hypothesis NOT confirmed on these lanes**: the `lhr.life`/`uqcors.html`/`uqvnc=` infrastructure shows zero Portuguese/Italian/Dutch targets across 80 lhr.life reports, 8 uqcors, 4 uqvnc. The operator's infra exists but does not touch these languages in the visible corpus.
- **Side observations (not fleet hits, logged for honesty)**:
  - `encurtador.com.br/BZkz` + `HYtc` (2026-08-31, 4 min apart) — closest thing to a "burst" in PT lane, but isolated pair, random codes, no tags → phishing, not fleet.
  - `ggsmv-oyaaa-aaaad-qfmxa-cai.icp0.io/Fast-food/Fast_food/combo.html` (2026-05-10) — real `combo.html` URL on Internet Computer hosting; probe-family-adjacent shape, but not language-linked and not on lhr.life. Noted, not claimed.
  - Full-report fetch on urlquery.net was not possible via text fetch (report page returned site home) — classification rests on submitted-URL shape, dates, and count patterns.

## Open follow-ups (for the parent lane, not this subagent)
- A sweep of URL-substring searches (e.g. `/place/`, `?id=B…`) on PT/IT/NL map domains could catch a fleet that doesn't tag — keyword domain search alone can't see tagless systematic scans of these domains' own URLs, though keyword search *does* see URL content, so a same-domain multi-ID burst would have shown as repeated domain strings. Recommend one burst-oriented pass: `site:.br`/`site:.it`/`site:.nl` are not supported; approximate with domain-specific strings + date clustering.
- Other pending language lanes (4) continue elsewhere.
