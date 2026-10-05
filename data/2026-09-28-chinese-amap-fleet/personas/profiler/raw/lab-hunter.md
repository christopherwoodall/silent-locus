# LAB-HUNTER — urlquery submitter harness-experiment sweep
**Date:** 2026-10-04 · **Run by:** lab-hunter subagent · **Task:** find OTHER operators' public harness R&D on urlquery.net (the Amap fleet's `uqscan=`/`uqtag=` grammar is mapped; hunt other fleets testing in public)

## Collection caveat (IMPORTANT — biases everything below)
- VM egress was dead this whole session: `uq_htmx.py` (urllib) timed out, `curl` to urlquery.net AND to example.com timed out, DNS resolved urlquery.net to `198.18.241.58` (198.18/15 = benchmark sink). Ping 100% loss.
- All findings below came via **Google-indexed urlquery.net report pages** (`browser.search` `site:urlquery.net/report …` + `browser.open` on verbatim returned URLs).
- Consequence: this sweep sees only what Google crawled/indexed (skews old, misses fresh bursts, misses unindexed recent reports). **A live pass over the htmx endpoint from working egress is still owed** — re-run the marker list with `uq_htmx.py` when egress returns, especially: `httpbun`, `webhook.site`, `trycloudflare`, `uqupload`, `provenance-test`, `canary`, `view-docu-ns`, `eval-stdin.php`, `phpinfo.php`, single-char query params.
- Google snippets give report titles = submitted URLs, plus "Related reports" bursts (date/minute, URL, IP, ASN) — enough for burst-timing and URL-template analysis, not for submitter UA/referer (those live in full report pages; spot-checked one — the AIHW/httpbun one — and the fetched text was truncated to fingerprints).

## Method
~14 `site:urlquery.net/report` searches with harness markers: `httpbun`, `httpbin`, `webhook.site`, `localhost.run`, `lhr.life`, `ngrok`, `trycloudflare`, `beeceptor`, `pipedream`, `requestbin`-adjacent (`uqlab`, `uqupload`, `labtest`, `sandbox`), `?test=`, `?debug=`, `debug=true`, `poc`, `e2e`, `-test-`, `canary`, `staging.`, `dev`-adjacent, `example.com`, `playwright`, `harness`, `agent-task`, `evals`, `eval-stdin.php`, `uqq`/`oqscan`/`aqscan` copycat-grammar probes.

---

## FIND 1 — `uq-provenance-test` singleton (STRONGEST harness marker in the sweep)
- **Submitted URL:** `example.com/?uq-provenance-test-dc9fdbc9-c1d6-4ed8-b550-bb5b9a64b292`
- **When:** 2026-09-19 01:25 UTC · **Resolved IP:** 172.66.147.243 #13335 CLOUDFLARENET (example.com edge)
- **Context burst (same submitter run, 01:14 → 01:33):**
  - 01:14 `appwrite.io/verify-email?redirect=%2Faccount&userId=…&secret=3c7bd71…&expire=2026-09-19T02%3A13…`
  - 01:19 `paralino.app/verify?userId=6aade2d4…&secret=47fcec8…&expire=…`
  - 01:25 `example.com/?uq-provenance-test-<uuid>`
  - 01:33 `grosats.com/reset-password?userId=6aa848025c…&secret=a25b876f…&expire=2026-09-19T02%3A32…`
- **Read:** a run of password-reset-token verification scans (phishing kit verification or a researcher testing captured phishing URLs in a sandbox). Mid-run the submitter inserted a **control probe** — a UUID-stamped parameter on example.com — explicitly named `uq-provenance-test`: "what does urlquery record about this submission." This is exactly the Amap-operator-style "tests its harness in public" behavior, but a different actor and a different grammar.
- **Assessment:** one-off harness experiment, NOT a fleet (single indexed instance). Log as a harness-experiment specimen. Follow-up: htmx search `provenance-test` live for siblings (the UUID suggests a series).

## FIND 2 — synthetic telemetry URL `view-docu-ns1.web.app` (anomaly lead — fabricated test input?)
- **Submitted URL:** `view-docu-ns1.web.app/?bmF0YWxpZXJAc3V6eS5jb20=&media_priority=audio&risk_score=low&feature_pack=security&country_code=DE&locale=ja-JP&platform_type=tv&entry_priority=high&handoff_token=5kVxjTihH1&pipeline_stage=canary&ref=adaptive&client_version=v1.23.0&pipeline_id=pipe-992&timezone=Asia/Tokyo&cdn_region=eu-central&ad_variant=control&client_channel=internal&session_id=a2bcf6f3-0a68-4251-9cc8-4a2fd69d1fdf&prompt=none&secure_context=true&runtime_track=opt&ui_skin=neon&flow_variant=hybrid&partnerID=…`
- **Report:** https://urlquery.net/report/624a77f1-dd1d-4d0f-b46f-fd10bb645fe0 (crawled ~89 days before 2026-10-04)
- **Read:** 23+ mixed-typed query params (identity, locale, pipeline/canary flags, feature flags, `prompt=none`). First param is base64 `bmF0YWxpZXJAc3V6eS5jb20=` = `natalxer@suzy.com`. Hostname `view-docu-ns1.web.app` — "ns1" implies a numbered series that never appeared again in the index.
- **Two readings:** (a) an agent/fabricator generating a synthetic deep-link as scan input to test what a sandbox captures; (b) a human dev testing a document-viewer deep link. The mix of realistic locale telemetry + `prompt=none` + `pipeline_stage=canary` smells machine-generated.
- **Assessment:** singleton anomaly, LEAD per doctrine ("doesn't fit the frame = a lead"). Follow-up: live htmx search `view-docu-ns` and `flow_variant` for ns2/ns3 siblings.

## FIND 3 — eval-stdin.php burst, Spanish ISP (TRONZAP-ADJACENT — different actor, same grammar)
- **Probe:** `194.224.0.87/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php` (+ truncated `eval-stdin.ph` variant), 2026-08-19 02:05 and 2026-08-20 03:21 UTC, IP 194.224.0.87 #3352 Telefonica de España
- **Context burst (same run):** legit Spanish civic/university sites — `otaf.ayto-fuenlabrada.es/ovt/EXPR/280586/AFUENLABRADA/homenoauth/pag3`, `icg.es`, `atriga.gal` (tax info pages), `race.es`, `accv.es/encuentra-tu-pru`, `federado.ffmadrid.es`, `81.42.247.62:8085/sshd`
- **Read:** identical SHAPE to the known tronzap case (agent-shaped vuln-assessment run mixing real browse targets with a CVE probe URL), but a different actor/region (Spain/Telefonica vs TRON energy-rental). The `eval-stdin.php` = phpunit CVE-2017-9841 probe — same probe tronzap used.
- **Reports:** https://urlquery.net/report/37041096-65ec-4849-952a-de0cc3ad0859 and https://urlquery.net/report/d8fe03e9-357d-4044-9b7f-ef28b39a3506
- **Assessment:** treat as a tronzap-adjacent LEAD, not a negative. Worth a dedicated sweep: live htmx for `eval-stdin.php` across all submitters to enumerate how many independent actors run this grammar.

## FIND 4 — `fromtop.pages.dev` secret-enumeration burst (scanner-shaped, likely one run)
- **Burst:** 2026-08-26 09:28–09:32 (4 min): `/.env`, `/.env.backup`, `/.env.production`, `/config.php`, `/actuator/env`, `/.env.local`; plus `/9876543210admin/phpinfo.php` (2026-03-10 and 2026-09-06) and `/staging`, `/api/docs`, `/www` probes
- **Read:** classic automated secret-path enumeration against one Cloudflare Pages dev site. Burst timing = automated scanner. No cross-target fleet behavior; URL template = off-the-shelf wordlist, not a custom lab grammar.
- **Assessment:** one-off security research/scanner, NOT agent-lab-shaped. Honest negative for fleet purposes; kept as a burst-timing specimen.

## FIND 5 — mixed-minute burst on HiJackThis report (anomalous target mix)
- **Burst:** 2026-09-22 20:40 (same minute): `polymarket-perps-evidence.pages.dev`, `sb-invoices-old.castineapps.com`, `sb-invoices-old.castineapps.com/auth/login/local`, `deltarune.com`
- **Read:** one submitter scanning four unrelated targets in one minute — an "evidence" page, an invoice-app login flow (sandbox/local auth path — sandbox-y), and a game site. Mixed target mix is agent/researcher multi-URL run-shaped, but no repeated grammar.
- **Assessment:** weak lead. `sb-invoices-old.castineapps.com/auth/login/local` smells like a sandbox login-flow test. Follow-up only if siblings surface.

---

## Honest negatives (markers that returned noise or nothing)
- **ngrok / trycloudflare:** ~100% malware/phishing noise — Ngrok-hosted RAT droppers (`ngrok-v3-stable-windows-386.zip`, `/xampp/ngrok.exe` TH sinkholed), TryCloudFlare phishing (Instagram login phishing, `.lnk`→DavWWWRoot exfil, `captcha.php` panels). NOT agent labs. Drop these markers.
- **httpbin / httpbun:** dominated by the known Transluce corpus — e.g. https://urlquery.net/report/41806a91-7ce0-48f8-9109-48598a589211 (`httpbun.com/base64/…` packing an HTML form POSTing creds to `urlquery.net/user/signup` with `aihw1781872240@gmail.com`) and https://urlquery.net/report/1ee69d3e-6629-4ccf-8da5-b8f1f544b3cc (`httpbin.org/base64/…` → vizprod.aihw.gov.au exfil script POSTing to `webhook.site/18f9a554-2cbe-4bc2-bf71-bbcf1ef69cdc`). Known incident, no new fleet.
- **webhook.site:** fresh dead-drop reports are mostly in the AIHW corpus or threat-researcher scans; no new systematic fleet-shaped dead-drop grammar surfaced in the index.
- **localhost.run / lhr.life / beeceptor / pipedream / uqlab / uqupload / labtest / sandbox / "debug=true" / "debug=1" / playwright / harness / agent-task / evals / uqq / oqscan / aqscan:** zero indexed hits (honest zero — may be unindexed rather than absent).
- **poc / ?test= / -test- / e2e:** exploit binaries, firmware tools, benign dev artifacts — no lab grammar.
- **staging.:** mostly malware bursts (`www.staging.xn--80afcqcj2arf9a8i.com`) and unrelated staging hosts — no systematic fleet.
- **lab.:** Mozi botnet `/i` droppers + HostLAB Bilisim game-cheat hosting — malware noise, not labs.
- **example.com:** one real harness marker (FIND 1) plus scanner sanity checks (`example.com/api/data`, `ftp@example.com/`).

## Retry/backoff log (parent instruction 2026-10-04 ~23:41 CDT)
- 23:29–23:40 CDT: `uq_htmx.py` (urllib) → URLError timeout ×2; curl→urlquery.net and curl→example.com → 60s/30s timeouts; DNS gave urlquery.net=198.18.241.58; ping 100% loss. Site had been reachable ~1h earlier (parent). Treating as transient outage/throttle: backing off 25 min, then one patient retry (120s curl timeout, 30s connect) + one small htmx query before deciding. All findings above are from Google-cached report pages (collection caveat stands).

## Recommendations for next lab-hunter run (when egress is back)
1. Live htmx: `provenance-test`, `view-docu-ns`, `flow_variant`, `eval-stdin.php`, `phpinfo.php`, single-char params (`?a=`, `?x=`, `?q=`), `canary`, `uqtag`-style prefixes with NON-amap grammar (`uq<3-letter>` where 3rd letter ≠ scan/tag/vnc).
2. Pull full report pages for FIND 1 and FIND 2 to recover submitter UA / submit tags — the Google snippets don't carry them.
3. Enumerate all `eval-stdin.php` submitters (FIND 3's grammar) to count independent actors running tronzap-shaped assessment runs.
4. Consider Wayback CDX for `urlquery.net/report/*` pages to timestamp first/last appearance of new markers.
