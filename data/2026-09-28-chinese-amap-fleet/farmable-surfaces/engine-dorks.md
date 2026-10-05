# Engine dorks on under-farmed engines (2026-10-04)

Marker sweep for the 10-month `uq`-grammar operator campaign (lhr.life probe
harness, IDPH/AIHW health-data task families, Amap fleet) across the engines
Google-dork v2 didn't cover: **Bing, Brave, Mojeek, Marginalia**.

**Bottom line: no new traces.** Three of four engines are hard-blocked from this
environment; Marginalia answered 5 of 11 dorks (all honest zeros) and challenged
the other 6. Nothing indexed anywhere outside what Google/DDG already surfaced.

## Engine status

| Engine | Endpoint | Status | Evidence |
|---|---|---|---|
| Bing | `bing.com/search?q=` | **UNUSABLE — anti-bot decoy SERPs** | 6 probes: same query returns different unrelated result sets across requests. `q=uqscan` → butcher shops ("51,900 results"), then Pornhub/Reddit threads on retry; `q="uqscan="` → NZ real-estate listings; `q="sub_poi_navi"` → Subway sandwich shops; `q="ZZZNew"` → ChatGPT/Copilot pages (DDG shows TikTok/YouTube usernames for the same dork). Cookie jar + full browser headers did not fix it. Hit counts are fabricated; results do not correspond to the query. |
| Brave | `search.brave.com/search?q=` | **BLOCKED — HTTP 429 on the very first request** | Treated as hard stop; no retries, no alternate Brave endpoints. |
| Mojeek | `mojeek.com/search?q=` | **BLOCKED — JS CAPTCHA challenge** | "JavaScript is required to complete this challenge. Please enable it and reload the page." Not passable via curl. |
| Marginalia | `old-search.marginalia.nu/search?query=` | **PARTIAL — adaptive JS wait gate** | 5/11 dorks answered (all zero hits), 6/11 challenged. Gate: wait page issues an `sst` token via `location.replace('/search?query=…&sst=S-…')`; token fetch succeeds only with the wait page as `Referer` and several seconds' delay. Pass rate degraded over the run (adaptive tightening after repeated probing). `marginalia-search.com` and `search.marginalia.nu` both serve the same gate; `old-search.marginalia.nu` is the text-browser path. |

## Marginalia results (the only engine that answered)

11 operator-marker dorks, 20s pacing, one token-retry per dork.

| # | Dork | Status | Hits |
|---|---|---|---|
| 1 | `"uqscan="` | blocked (challenge persisted) | — |
| 2 | `"uqcors.html"` | blocked (challenge persisted) | — |
| 3 | `"uqtag="` | blocked (challenge persisted) | — |
| 4 | `"sub_poi_navi"` | ok | **0** |
| 5 | `is.gd "uqscan"` | ok | **0** |
| 6 | `is.gd "?x="` | blocked (challenge persisted) | — |
| 7 | `lhr.life "probe.html"` | ok | **0** |
| 8 | `lhr.life "uqcors"` | blocked (challenge persisted) | — |
| 9 | `"mark=" "validation=v" "TimeTrendData"` | blocked (challenge persisted) | — |
| 10 | `"AGE115EXTRACT1"` | ok | **0** |
| 11 | `"MassCountyData"` | ok | **0** |

**New traces: none.** The 5 answered dorks are honest zeros — Marginalia's small-web
index contains no pages with these markers. The 6 blocked dorks are unknowns, not
zeros; they skew toward the highest-value markers (`uqscan=`, `uqcors.html`,
`uqtag=`, the IDPH grammar), which is unfortunate but not evidence of anything.

## Honest zeros (Marginalia, verified)

- `"sub_poi_navi"` — 0. The Amap fleet's POI-navigation probe parameter has no small-web footprint.
- `is.gd "uqscan"` — 0. No short-link pages carrying the `uqscan` tag.
- `lhr.life "probe.html"` — 0. The operator's probe pages aren't indexed by Marginalia (expected: ephemeral localhost.run tunnels, and Marginalia doesn't crawl them).
- `"AGE115EXTRACT1"` — 0. The AIHW aged-care extract tag appears nowhere in the small-web index.
- `"MassCountyData"` — 0. Same for the Massachusetts county-data marker.

Caveat: Marginalia is a keyword index of the non-commercial small web (blogs, tilde
sites, wikis). It does not index GitHub, pastebins, or urlquery.net well, so a zero
here mainly rules out forum/blog/wiki discussion of the markers — which is exactly
the "under-farmed" surface this sweep was for.

## Method

- curl HTML endpoints, browser UA, per-engine markup parsing (script: `engine-dorks-runner.py`, raw log: `engine-dorks.jsonl`, this dir).
- Bing poison check: 6 probes with distinct queries; determinism test (`q=uqscan` twice → disjoint unrelated result sets) confirms decoy behavior, not a real index.
- Brave: single 429 → stopped per rate-limit policy, no retry.
- Mojeek: CAPTCHA on first response → stopped.
- Marginalia: `sst` token + `Referer` + 8s delay, one retry, 20s inter-dork pacing (their notice asks bots not to barrage).
- NOT pushed (per task brief).

## Open / follow-ups

- The 6 Marginalia-blocked dorks could be retried in a later session after the gate cools down — highest value: `"uqscan="`, `"uqcors.html"`, `"mark=" "validation=v" "TimeTrendData"`.
- If a residential IP or headed browser becomes available, Bing/Brave/Mojeek deserve a re-run; Bing's decoy behavior in particular may be IP-reputation-gated.
- Marginalia's main UI (`marginalia-search.com`) serves the same wait gate; the old-UI token trick is documented in-page as the manual-proceed path for non-JS clients, not a bypass.
