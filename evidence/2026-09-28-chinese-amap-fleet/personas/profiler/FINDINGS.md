# PROFILER — Submitter Behavior Hunt (2026-10-05)

**Mission:** profile urlquery.net SUBMITTERS (not targets) to find undiscovered agent/swarm fleets.
**Method:** keyless htmx crawl (`~/workspace/skills/urlquery/bin/uq_htmx.py`) + local corpus submitter-metadata mining.
**Constraint:** authenticated API (uq.py) 429-throttled / timing out — `settings.useragent` / `settings.exit_node` only available for already-collected corpus reports, not fresh crawls. htmx returns report_id/url/ip/asn/country/date only.
**Doctrine:** metadata tells the story; misfits are leads; agents and swarms only.

---

## 1. Operator baseline — the submitter fingerprint we already know (local corpus, 1,970 reports)

Corpus: `data/2026-09-28-chinese-amap-fleet/raw/page_*.json` (2026-09-28 → 2026-10-05 window).

| Signal | Value | Reading |
|---|---|---|
| `settings.exit_node` | `qguvgzjxzsgb3vs` ×1,945; `31pu2ilhjrkmwpf` ×25 | Two values across the operator's reports — but CORRECTION: exit_node is urlquery's SHARED egress, not submitter infra. Feed submitters (openphish, soteria) land on the same node. Distinctive as a *pattern* (one submitter pinned to 2 nodes across thousands of reports) but absence of other values ≠ absence of other submitters |
| `settings.useragent` | 18 distinct; 1,931× urlquery Firefox-134 default | Shared harness; submitters don't customize scanner UA |
| `settings.access` | 100% public | Nothing hidden |
| `settings.device_type` | 100% desktop | Even mobile-target scans come from desktop profile |

### 1a. Node 2 = the lab node (submitter R&D infrastructure)

25 reports on `31pu2ilhjrkmwpf`. 20 on 2026-09-28 (same POI B000A7O1CU, www/m variants — node smoke test), 1 on 09-30, 4 on 10-04:

- `?oldnodeprobe=1791119665` — EXPLICIT node probe marker
- `?uq=exit`, `?uq=ua` — exit_node / UA test markers (same-minute pair, 10:28)
- `?uqscan=exit31` — node-named tag
- `?uqscan=fjmuseum-alt31-20261004` — "alt31" = alternate node

**Profiler rule:** operators test infrastructure in public. Explicit probe markers (`*nodeprobe*`, `*exit*` tags) are the tell.

### 1b. Weird-UA R&D arm (all on node 1, all 2026-10-04 — peak day)

| Date | UA | URL marker |
|---|---|---|
| 10:24 | `Mozilla/5.0` | `uqscan=bazaar20261004a` |
| 08:29 | `0` | `uqscan=claude20261004mochou` |
| 08:01 | `mobile` | `m.amap.com/detail/index/poiid=B0138027SQ` |
| 06:39 | Googlebot spoof | `?x=uqcustomua20261004` |
| 06:28 | `desktop` | `uqscan=research20261004a` |
| 04:49 | `0` | `uqscan=pandalegacy1791089321` |
| 04:49 | `0` | `uqscan=pandalegacy20261004` |

Markers to watch for in the wild: `bazaar`, `mochou` (莫愁), `claude<date>`, `customua`, `research<date>`, `pandalegacy`, bare `0`/`mobile`/`desktop`/`Mozilla/5.0` UAs, Googlebot spoof, referer `m5.amap.com`, genuine `AMAP/162500 Android/15` UA.

**Key:** the 04:49 pair (9 seconds apart, format variants `pandalegacy1791089321` vs `pandalegacy20261004`) = parallel A/B format test. Same-minute variant pairs are the R&D tell.

## 1c. Background feed submitters on the same egress (not fleets, but the noise floor)

`submit.tags` in corpus: `unknown` ×3 (wantace.com, xianzhiguan.com, erran.eus — bare phishing domains, Oct 4), `openphish` ×1 (meta-vimaro-biz-zeluno-panaki.pages.dev, Oct 2), `soteria` ×1 (eseblt.click, Sep 29 — Android WebView UA, referer "soteria"). All on `qguvgzjxzsgb3vs`, all stock/default UAs. These are threat-intel feed pipelines submitting phishing URLs — the platform's background hum. Confirms exit_node is shared egress: **node clustering alone cannot separate submitters**.

## 1d. Live operator activity — manual/automated interleave (live-monitor, 2026-10-05)

Newest grammar variants from the museum family:
- Bare-epoch `uqscan=17911717674179` (no word prefix)
- New params: `?uqm=1/2/3`, `?uqattempt=0/1`, `?src=manual0/1/2`, `?src=uriapi`
- `user_loc=117.015893,36.661087` geolocation param

**`src=manual<N>` = hand-driven submissions interleaved with automated runs.** Profiler implication: this submitter mixes manual QA with the pipeline — a human-in-the-loop operator, not a pure cron. Manual submissions cluster at 02:13 UTC Oct 5 (switchVersion probes) — QA of a new code path.

---

## 2. Burst-profiler results — COMPLETED (partial; raw/burst-profiler.md)

Method note: egress died mid-run; evidence = 3 homepage snapshots (12 reports each) via runtime-side fetch + targeted searches. Cluster sizes are LOWER BOUNDS. Amap fleet quiet in window.

- **Cluster 1 — "xsph.ru phish-kit sweeper" (highest-confidence single submitter):** ≥6 reports in ≤2 min (2026-10-05 05:04 UTC), `[a-f0-9]{7}.xsph.ru` + `www.` variants, all → 141.8.197.42 (Sprinthost.ru, RU), TDS 2-4. Metronomic burst, 05:04 minute ~100% this kit. Programmatic subdomain enumeration = agent-shaped (takedown-vendor pipeline possible).
- **Cluster 2 — "workers.dev phish-farm harvester":** ≥14 reports across ~35 min in 3 minute-bursts (04:31, 05:03, 05:04). Random-word workers.dev subdomains, bare root paths. Recurring bursts = automated pipeline, machine-like.
- **Cluster 3 — binance blogspot pair + S3:** same-minute www/bare dedup pair (`binance-register.blogspot.com`) + `amazon-connect-*.s3.amazonaws.com` — pipeline tell, low-moderate.
- **Cluster 4 — urldance redirector prober:** same-minute `/7d/` `/8d/` sequential paths (matches geo U1) — namespace-walking signature.
- **Cluster 5 — ddnsgeek dyndns pair:** (matches geo D1) random dyndns + 6-char paths.
- **Clusters 6-7:** feed strays (pages.dev `/dp/` Amazon-pattern phish, replit.app Spanish bank phish, .np singleton).
- **Explicit negatives:** zero Amap grammar in window; bulk of feed = commodity phishing-takedown traffic.

## 3. Tag-profiler results (children: pending)

See `raw/tag-profiler.md`.

## 4. Lab-hunter results — COMPLETED (partial, via Google-indexed report pages; raw/lab-hunter.md)

Method note: egress dead all session; ~14 `site:urlquery.net/report` searches. Skews old/indexed only — live htmx re-run still owed.

- **FIND 1 — `uq-provenance-test-<uuid>` (strongest harness marker):** 2026-09-19 01:25 UTC, `example.com/?uq-provenance-test-dc9fdbc9-c1d6-4ed8-b550-bb5b9a64b292`, mid-run control probe inside a password-reset-token verification burst (appwrite.io, paralino.app, grosats.com verify/reset URLs, 01:14→01:33). Different actor, different grammar than our operator — same "tests harness in public" behavior. One-off, not a fleet; htmx `provenance-test` for siblings when egress returns.
- **FIND 2 — synthetic telemetry URL `view-docu-ns1.web.app`:** 23+ mixed-typed params (`pipeline_stage=canary`, `prompt=none`, base64 email), "ns1" series never seen again. Machine-generated-looking scan input; singleton anomaly = lead.
- **FIND 3 — eval-stdin.php burst, Spanish ISP (tronzap-adjacent):** `194.224.0.87/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php` (phpunit CVE-2017-9841 probe), 2026-08-19/20, Telefonica de España, mixed with legit Spanish civic/university targets. Same SHAPE as tronzap, different actor/region. Reports `37041096-65ec-4849-952a-de0cc3ad0859`, `d8fe03e9-357d-4044-9b7f-ef28b39a3506`.
- **FIND 4 — fromtop.pages.dev secret-enumeration (honest negative):** 4-min `.env`/`.env.backup`/`/config.php` burst — automated scanner, off-the-shelf wordlist, not lab grammar.
- **FIND 5 — mixed-minute burst (weak lead):** 2026-09-22 20:40, `polymarket-perps-evidence.pages.dev` + `sb-invoices-old.castineapps.com/auth/login/local` + `deltarune.com` — one submitter, four unrelated targets, sandbox-login-test smell.
- **Honest negatives:** ngrok/trycloudflare = malware/phishing noise (drop as lab markers); httpbin/httpbun = Transluce corpus (known); webhook.site/lhr.life/beeceptor/pipedream/uqlab/debug/playwright/harness/agent-task/evals = zero indexed hits.

## 5. Geo-profiler results — COMPLETED 2026-10-05 (raw/geo-profiler.md)

**Infra note:** VM egress proxy (hatch-egress-proxy:3128) timed out on ALL hosts from ~23:30 CDT — htmx unusable. Findings rest on homepage text-fetch snapshots + frozen-audit evidence. Non-Amap clusters found:

- **U1 — "urldance" HK phishing-redirector sweep (FRESH, 2026-10-05 04:31 UTC):** `202608.urldance.com/7d/` → 156.225.108.43 and `/8d/` → 156.225.108.42, same minute, AS139057 Edgenext (HK). Date-rotated subdomains on phishing blocklists; `/Nd/` paths read as sequential campaign IDs. Caveat: submitter may be threat-intel scanner, not agent fleet.
- **D1 — "ddnsgeek" gibberish pair (FRESH, 04:31 UTC):** `jehalisipo.ddnsgeek.com/uwojad/`, `dudamu.ddnsgeek.com/jipoco/` — random-word DDNS subdomains + 6-char paths, same minute, HostPapa US. Submitter grammar (gibberish pairs in one minute) is the fingerprint.
- **Q1 — Quidax crypto-ramp probing (2026-09-19 21:54 → 09-20 00:27 UTC, ~2.5h):** reports `960b3314`, `52d9be69`, `f825e84d` — repeated Quidax (Nigerian crypto exchange) buy/sell ramp URLs, HTML-injection-shaped error param, API test scripts, mixed 200/403/redirects. **Strongest non-Amap fleet candidate**: agent-shaped fiat on/off-ramp probing, distinct from Transluce clusters and the Amap fleet.
- **K1 — IEA Korean energy imports (2026-09-16):** `6a86ffff`, `1f724789`, `879360b3` + fetch-code report `b0f6abe3`. KR-focused data retrieval at edge of Transluce's "latest activity".
- **Continuity marker:** same Thai stats-dashboard URL in five Nov-2025 and five Mar-2026 scans — links Nov-2025 origin to Mar-2026 ONCB incident.
- **CHATGPT-marked UNCTAD (2026-05-13):** reports `1368e4a9`, `850d1c01`, `b020bc29` carry `CHATGPT` in URL query params — self-identification marker, not authenticated submitter.

Next: htmx burst reconstruction for U1/Q1 once egress recovers.

## 6. Keyless node-probe hunt (direct)

`oldnodeprobe` / `exit31` / `nodeprobe` searches on urlquery — results pending (htmx slow, backgrounded).

---

## Open gaps (need keyed API or browser)

- `settings.useragent` / `settings.exit_node` for reports OUTSIDE our corpus — keyed API throttled (ua-burst-retry cron handles one attempt/30min).
- Submission method (api vs web) — not in public schema (`submit.meta` null on all 1,970 corpus reports).
- Submitter geography — urlquery publishes no submitter-IP field (MEMORY.md: established).

## Operational note (2026-10-05 ~00:30 CDT)

VM egress proxy (hatch-egress-proxy:3128) timing out on ALL hosts — urlquery htmx, keyed API, and even example.com unreachable. Children told to back off 20-30 min and retry with patience; geo-profiler completed via text-fetch fallbacks + frozen-audit evidence. If egress stays down, the remaining lanes (burst/tag/lab) will report partials from local material.
