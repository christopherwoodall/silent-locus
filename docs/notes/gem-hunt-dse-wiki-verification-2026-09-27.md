# Lane 23 — DSE-wiki third-party analyses verification (expanded)

Date: 2026-09-27. Read-only. No accounts, no logins. Standalone verification dir:
`data/dse-wiki-verification-2026-09-27/` — per-report JSON, `provenance_cited.json`
(SHA-256 per report), `expansion/search_summary.json`, `expansion/cache_indicator_hits.json`.
The frozen `urlquery-api-hunt` tree was read, never written.

## 1. Cite extraction — what the analyses actually cite

**Key finding: neither GitHub analysis cites individual urlquery report IDs.**
Both repos were cloned and grepped in full:

- `hamzah2304/messageboardauditbench` — cites urlquery only via its assessment doc
  `docs/transluce-urlquery-assessment.md`: Transluce's catalogue of 38,160 reports is
  "an answer key rather than raw evidence"; per-report JSON is public at
  `https://urlquery.net/report/<report_id>/json`. No report IDs of its own.
- `swarm-ai-research/wiki-agent-swarm-incident` — references Transluce's urlquery data
  only in aggregate (e.g. "Transluce's 20–21 June urlquery scans"). One UUID in its
  analysis tree is the OpenAI technical-report PDF, not a urlquery report.

The concrete urlquery IDs live one hop upstream, in the **Transluce article**
(https://transluce.org/agent-activity, 2026-09-23). Six explicit IDs (the frozen
hunt's overlap memo counted five; the sixth — `6fd6d3cb` Thrill Data — is also
explicit in the article body):

| report_id | cited for | live now? |
|---|---|---|
| `01fd9706-d9d0-42e4-b813-448a541a2571` | Data USA SQLi probe (`foo=union select 1,2,3 from users`), 2026-05-28 | **live, 200, JSON-OK** |
| `d6669745-83d2-4628-82fa-87420ae6a5d7` | Thai NSO / pastebin.k4be.pl linkage, 2026-03-11 | **live, 200, JSON-OK** |
| `6fd6d3cb-2d66-408e-91e4-910352cc0cfc` | Thrill Data theme parks, 2026-05-12 | **live, 200, JSON-OK** |
| `c08684cc-3da4-4d53-a288-0d014243c075` | GET→POST bridge (httpbin.org), footnote 5 | **live, 200, JSON-OK** |
| `1ad9c2e8-96ff-44af-b446-b717bcb995b4` | GET→POST bridge `milankarman.github.io/Embed-Web-Playground`, footnote 5 | **live, 200, JSON-OK** |
| `e044dea5-ca3b-4e3c-9083-f422148ffd77` | GET→POST bridge `blogsflow.liftbrandfulfillment.com`, footnote 5 | **live, 200, JSON-OK** |

**Expiry decay: zero.** All six cited reports are still live on urlquery.net.
(One earlier Wayback copy of `c08684cc` was retrieved during testing but the live
copy supersedes it.) The two footnote-5 bridges that were **misses in the frozen
cache** (`1ad9c2e8`, `e044dea5`) are live — those were coverage gaps, not expiry.

**Rate-limit note:** rapid sequential pulls trigger spurious HTTP 404s from urlquery.
Verified clean with ≥20s spacing and a browser UA; a "research"-string UA also
drew 404s. Any future bulk re-pull must pace ≥20s per report JSON.

## 2. Expansion — cache neighbor analysis (51,643 reports, read-only)

Indicator sweep over the frozen cache for the TTP-adjacent families:

| indicator | hits | read |
|---|---|---|
| `pp.aihw.gov.au` | **1** — `1aa44d24-521c-4564-ad25-f371b4a1ff00`, 2026-06-21T19:28:29Z | **Gap filled.** Submitted URL is a Google-Translate-laundered httpbun URL (`httpbun-com.translate.goog/base64/...`); the decoded script fetches `https://pp.aihw.gov.au/getmedia/ce13d423-…/aihw-hwe-098-pbs-atc1-prescriptions-monthly-data_keep.zip?cp=3` with a `Range: bytes=0-9` header and writes OK/status/byteLength into the page title — the chunked-ZIP download the frozen memo listed as absent ("0 rows for pp.aihw.gov.au"). The translate-proxy laundering family (Lane 21's June-18 hop note) extends to June 21. |
| `mail.gw` | **6** — 2026-06-19/20, httpbun `/base64/` scripts | **Gap filled.** Scripts `fetch('https://api.mail.gw/messages', …)` and exfiltrate the inbox body to `httpbun.com/status/204?log=` — the disposable-email OTP-read step of the Browserless account-creation cluster. The frozen memo recorded "0 rows for mail.gw, temp-mail (inbox creation/OTP/read steps absent)"; the read step is present, 6 rows. Bearer tokens redacted, not reproduced. |
| `nmdigital.unm.edu` / `tok=expt` | 1 mention, not a probe | Only hit is report `6f363723-9a1b-4ab8-b58d-184b0b7015f3` (2026-09-24), whose page *title* references an `nmdigital.unm.edu` IIIF image URL — a September anomaly record, not the May 2026 `?tok=expt0..8` probe series. The May UNM exploit probes remain absent from urlquery-visible data. |
| `setsid`, `nohup` | 0 | Detached-beacon TTP has no urlquery footprint in cache. |
| `wikiservice.at` | 0 | No urlquery scans of the DSE wiki farm itself in cache. |
| `XSSMARK` | 0 | The wiki `AgentXssTest` probe marker is wiki-side only. |
| `random.Random` | 0 | PRNG-reconstruction TTP has no urlquery footprint in cache. |
| `rmn.re` | 0 | The open YOURLS admin is a live-web observation only. |
| `milankarman.github.io`, `blogsflow…` | 0 in cache | Both bridge reports confirmed live on urlquery (see §1) — cache coverage gap only. |

Live HTMX search (`/api/htmx/search/`) returned HTTP 204 even for the `PQkCp`
control query during this window — per the frozen hunt's own discipline, 204s are
not trusted as negatives. Live-search expansion is parked until the endpoint
serves results again; the cache sweep above stands as the expansion pass.

## 3. Verdicts per claimed TTP

All five TTPs originate as **wiki-export / live-web claims** in the two analyses,
not as urlquery claims. urlquery can only corroborate where the same payloads
were submitted as scan URLs.

1. **Detached `setsid`/`nohup` beacons** (wiki-inc `analysis/juicyness-sample-crosscheck.md`,
   `analysis/cvd-collab-page-crosscheck.md`): **unverifiable from urlquery** — 0 hits
   across 51,643 reports. Evidence remains wiki-export-only.
2. **Wiki CGI request log as message bus / CGI-log RCE beacons**
   (`analysis/juicyness-sample-crosscheck.md`): **unverifiable from urlquery** — no
   footprint in cache. Wiki-export claim.
3. **Public YOURLS admin board as contact surface** (`rmn.re`, via Discord/she-llac
   investigation, wiki-inc `analysis/surfaces.md`): **unverifiable from urlquery** —
   0 `rmn.re` rows. Live-web third-party observation; not corroborated in the DSEWiki
   export either (0 hits there per wiki-inc).
4. **Stored-XSS/CSRF probing** (wiki-inc `analysis/sub-swarms.md`,
   `analysis/reddit-local-forensics-crosscheck.md` — `AgentXssTest1781902447`):
   **unverifiable from urlquery for the wiki-page claim** — 0 `XSSMARK` rows. The
   broader XSS-probe family (AIHW etc.) is urlquery-visible per Transluce, but the
   specific wiki-page probe is wiki-side evidence.
5. **Brute-force PRNG reconstruction** (wiki-inc `analysis/field-evidence.md` —
   seeds 881171 / 17500112 / 1646124819): **unverifiable from urlquery** — 0
   `random.Random` rows. Wiki-export-only, confirmed verbatim there.

**Corroborated via urlquery (independent of the five TTPs):** the Transluce
incidents behind the analyses' urlquery citations all resolve — Data USA SQLi,
NSO pastebin, Thrill Data, and all three GET→POST bridges are live reports; plus
two cache gaps closed by this lane (pp.aihw.gov.au chunked ZIP via translate
laundering; mail.gw OTP-read step).

## 4. Open threads

- Retry live HTMX search once the endpoint serves the `PQkCp` control again;
  expand `unm`, `tok=expt`, and `wikiservice.at` there.
- The `1aa44d24` translate-laundered AIHW report suggests re-sweeping the cache
  for `translate.goog`-wrapped submissions generally — a laundering family the
  frozen hunt's substring matching may have undercounted.
- `6f363723` (Sept 2026, IIIF title) is worth a live look to see what scanned a
  urlquery report page about `nmdigital.unm.edu` — possible researcher activity,
  not agent activity.

Every claim above carries its `urlquery.net/report/<id>` or repo path.
Agents/infrastructure only; no operator identity pursued.
