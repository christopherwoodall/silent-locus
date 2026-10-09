# Lead watch 2026-10-05 — tronzap + ZeroSSL re-poll
**Lane D (Lane D, full-sweep coordinator task; depth 2, no subagents spawned).**
**Pulled:** 2026-10-05 ~12:45–13:10 UTC (07:45–08:10 CDT).
Prior state: `raw/lead-urlscan-tronzap.md`, `raw/lead-zerossl-followup.md` (2026-10-05 earlier today), `raw/lead-radar-tunnel.md`.
Scope: agents/swarms only — no human/operator identity work. Raw dumps: `raw/ct_lhrlife_watch_2026-10-05.json`, `raw/us_tag_87270ca9ac10_2026-10-05.json`, `raw/us_domain_onlytron_2026-10-05.json`, `raw/us_tag_xq-recon-probe_2026-10-05.json`, `raw/us_domain_lhr-life_<YYYY-MM-DD>.json` ×6, `raw/us_domain_tronzap_<YYYY-MM-DD>.json` ×6.

## Verdicts (one line each)
- **ZeroSSL lead:** NOTHING NEW since Oct 3. 1 new tunnel-name cert overall: `3281cb5f73b0c2.lhr.life`, **Let's Encrypt** (not ZeroSSL), issued 2026-10-05T09:00:46Z. ZeroSSL count frozen at the 7 names from the earlier lane. No new multi-CA / RSA+ECC experimentation since the Oct 2–3 cluster.
- **Tag `87270ca9ac10`:** NOTHING NEW. Still exactly 7 scans, all 2026-09-29 — but one new detail recovered: the tagged sweep includes **`dev.onlytron.com`** (a different domain than tronzap.com).
- **tronzap.com new scans:** NONE Sep 30 → Oct 5 (0/day × 6 days). Sep-29 follow-on remains the latest activity.
- **Sep-29 tunnels liveness:** UNANSWERED (VM egress proxy intercepts DNS → 198.18.0.x; HTTPS 502 on all 3). Not a negative.
- **crt.sh:** STILL DOWN (HTTP 502, fast-fail). One check only, per brief.

---

## 1. CertSpotter re-poll — `*.lhr.life` tunnel-name issuance (2026-10-03 → now)

Endpoint (documented in prior lane; reused verbatim):
`GET https://api.certspotter.com/v1/issuances?domain=lhr.life&include_subdomains=true&expand=dns_names&expand=issuer` + page 2 via `after=`.
Result: page 1 = 42 records (41 prior lane), page 2 = `[]` (same as prior lane; history still starts 2026-05-31). Deduped by `tbs_sha256`: **41 records → only ONE new tunnel-name cert since the prior lane's pull**.

### New cert (first and only new since Oct 3)
| first seen (not_before) | name | issuer | pubkey | detail |
|---|---|---|---|---|
| 2026-10-05T09:00:46Z | `3281cb5f73b0c2.lhr.life` | **Let's Encrypt, CN=YR1** | `c40317452149ad020684ef0515975e6cc2246f4cfaa52af6d81eb6d8c21f799c` (fresh, single-use) | single-SAN, `not_after` 2027-01-03, `revoked:false`, CT id `17596783160`, `tbs_sha256` `aa4db432956c3bd9be361ee3858528fc127c0113529f3d0bded27b4b43f76e6c` |

### Pattern comparison
- **No new ZeroSSL issuance since 2026-10-03T00:00:00Z** (the `0418f1e395a48e` / `92f1f5cd378431` dual certs remain the latest ZeroSSL records). The Oct 2–3 experimentation cluster (dual RSA+ECC ×2 names, LE→ZeroSSL switch, 3-CA name `93ca25e80716ce`) has NOT recurred.
- `3281cb5f73b0c2` matches the **baseline single-cert single-CA pattern** (one fresh key, one CA) — the pipeline is still running, but the multi-CA/multi-keytype experimentation appears to have been a bounded Oct 2–3 test run.
- **Pace note vs the prior lane's "~1–2/week":** that figure was ZeroSSL-specific and still holds for ZeroSSL (last: Oct 3). For *any-CA* tunnel-name certs, the last 8 days ran hotter than the Aug–Sep baseline: names on Sep 28 (×2), Sep 30, Oct 2 (×4), Oct 3 (×3), Oct 5 (×1) — roughly **~1/day over the past week** vs ~2–3/week in August (e.g. Aug 3, 9, 11, 13, 14, 19 ×3, 20). The uptick predates the Oct 2–3 CA-mix experiments and continued with today's baseline-pattern LE cert. Read as: issuance volume elevated since ~Sep 28; experimentation (ECC/multi-CA) confined to Oct 2–3.
- Name `3281cb5f73b0c2` is **absent from the 78-name known-fleet list** (`writeup-lhr-life.md`) — 0 hits — and 0 urlquery reports were checked in the prior lane pattern (not re-checked here; the name was issued ~4h before this pull, too fresh for indexes).

## 2. urlscan re-poll — tag `87270ca9ac10` and `domain:tronzap.com` after 2026-09-29

Method: anonymous `GET /api/v1/search/` (polite: 3–4 s spacing, no retries on empty). Verified query syntax: `q=task.tags:87270ca9ac10` (bare hex returns 0). Day-exact `date:YYYY-MM-DD` works; Lucene range `date:[A TO B]` returns 0 (unsupported from this path); trailing wildcards fail (prior lane). No 429/403 encountered.

### Tag `87270ca9ac10` — no new activity, one new detail
Still exactly **7 scans, all 2026-09-29 05:52–05:53 UTC** (`has_more:false`):
`dev-api`, `dev`, `ref`, `devbo/login`, `dev-dash`, `dev-bo`, `tronzap.com` — **plus `dev.onlytron.com`** (05:53:08), which the prior lane's summary did not list (it was captured in the raw search set; it surfaced only in this tag-scoped pull). No scans under this tag after Sep 29. Target family for this actor is therefore **tronzap.com + onlytron.com**, not tronzap.com alone.

### `domain:tronzap.com` — Sep 30 → Oct 5: zero scans
Per-day queries `q=domain:tronzap.com AND date:<day>`, Sep 30 / Oct 1 / Oct 2 / Oct 3 / Oct 4 / Oct 5: **total=0 each**, `has_more:false` each. The Sep-29 follow-on remains the latest known activity. **Coverage limit (explicit):** the anonymous top-100 cap means ~305 of 405 total `domain:tronzap.com` results remain unseen; day-bounded queries only cover the re-poll window. Any pre-Sep-26 tunnel tests or non-lhr.life fetch engines in the older ~305 stay out of reach without a urlscan account.

### `domain:lhr.life` — Sep 30 → Oct 5: 5 scans, all bare roots
| date | scan | tunnel name | notes |
|---|---|---|---|
| 2026-09-30 09:27 UTC | `https://90667af7b6a9f1.lhr.life/` | `90667af7b6a9f1` | persistent Sep-26 tronzap campaign tunnel; liveness-scan cadence ~daily continues |
| 2026-10-02 08:45 UTC | `http://c7a1f824a6efc4.lhr.life/` → eff https | **`c7a1f824a6efc4` (NEW name)** | fresh tunnel infra, bare root, untagged — same "provisioned + liveness-checked" shape as Sep-29 roots |
| 2026-10-02 09:42 UTC | `https://90667af7b6a9f1.lhr.life/` | `90667af7b6a9f1` | second scan same day |
| 2026-10-03 13:29 UTC | `https://90667af7b6a9f1.lhr.life/` | `90667af7b6a9f1` | continues |
| 2026-10-04 13:45 UTC | `https://90667af7b6a9f1.lhr.life/` | `90667af7b6a9f1` | continues |
| 2026-10-05 | — | — | no scan yet (window to 12:52 UTC; prior scans land 09:27–13:45 UTC) |

- `c7a1f824a6efc4`: **absent from the 78-name fleet list** (0 hits in `writeup-lhr-life.md`), absent from all Sep-26/Sep-29 sets, absent from the CertSpotter tunnel-name cert set (no per-subdomain cert — consistent with the localhost.run wildcard-riding fleet model, unlike the ZeroSSL population). This is a NEW tronzap-campaign tunnel provisioned Oct 2, liveness-checked via urlscan, with no pages deployed yet. **Highest-value follow-up in this lane: watch `c7a1f824a6efc4` for page deployment and target.**
- The Sep-29 roots `1881e623217f7c` / `2f102b0544d3b3` show NO further scans since Sep 29 — no pages have deployed on them in urlscan's visible set (prior lane's open question #3: currently answered "no deployment observed").

### Misfit lead (never a negative): a second self-tagged actor on the same target family — `xq-recon` / `xq-recon-probe`
`q=domain:onlytron.com` → 25 results, all 2026-09-29. Composition:
- 04:40:31–04:41:12: 2 untagged scans (`onlytron.com/`, `dev.onlytron.com/`) — prelude.
- 04:41:12–04:41:34: tag **`xq-recon`** — `dev.onlytron.com/`, `onlytron.com/`.
- 04:42:32–04:45:01: tag **`xq-recon-probe`** — 20-scan Laravel recon sweep, ~3 min: `.env`, `.env.example`, `phpinfo.php`, `storage/logs/laravel.log`, `telescope`, `horizon`, `livewire/livewire.js`, `build/manifest.json`, `build/assets/app-DDA5EPQ9.js.map`, `robots.txt`, `api`, `up`, `sitemap.xml`, `_ignition/health-check`, `.git/HEAD`, `404test-xyz`, `admin`, `account.onlytron.com/`, `account.onlytron.com/api`, `api.onlytron.com/`.
- 05:53:08: tag **`87270ca9ac10`** — `dev.onlytron.com/` (the tronzap-campaign actor's subdomain enum, ~70 min later).
- `q=task.tags:xq-recon-probe` → 20 total, **all Sep 29, all onlytron.com family** (`has_more:false`). No tronzap.com scans under this tag.

Read: the `xq-recon-probe` playbook (Laravel Ignition, Livewire, source-disclosure, `.env`/`.git/HEAD` sweep) is the same fingerprint as the Sep-26 direct probes against tronzap.com, but self-labeled differently and aimed at onlytron.com on Sep 29, ending ~70 minutes before the `87270ca9ac10` actor's sweep reached `dev.onlytron.com`. Two candidate readings (both open): (a) same campaign, different self-tag phases; (b) a second actor piggybacking the same target family. Either way, **the target family is now two domains (tronzap.com, onlytron.com) and at least two self-labels (87270ca9ac10, xq-recon-probe)** — the lane's target inventory needs expanding before the Sep-26 38-scan burst is treated as the whole campaign.

## 3. Liveness spot-check — Sep-29 tronzap tunnels (from this VM)
`curl -m 25 https://<name>.lhr.life/` for the 3 Sep-29 follow-on roots:
- `1881e623217f7c.lhr.life` → DNS `198.18.39.179` (egress-proxy interception), HTTPS **502**
- `2f102b0544d3b3.lhr.life` → DNS `198.18.39.180`, HTTPS **502**
- `90667af7b6a9f1.lhr.life` → DNS `198.18.39.181`, HTTPS **502**
Per the standing method note (prior lane §3): this VM's egress proxy intercepts DNS into the 198.18.0.x range, and prior probes showed proxy flakiness (transient `no tunnel` 502 vs `http=000` failures) — **these results are UNANSWERED, never negative.** Tunnel liveness still requires an off-proxy vantage point.

## 4. crt.sh — one check, then done
`GET https://crt.sh/?q=%25.lhr.life&output=json` (single attempt, 30 s timeout) → **HTTP 502 (nginx, fast-fail, 1.9 s)**. crt.sh remains backend-down. The 4 pre-2026 ZeroSSL names (2023-08-17, 2024-05-01, 2024-06-13, 2024-06-29) still cannot be re-verified or named. Do not treat as a negative. CertSpotter continues as the working keyless path, with the documented limitation that its `lhr.life` history starts 2026-05-31.

---

## Method / infra notes
- CertSpotter keyless `api.certspotter.com` healthy (~2 s/call). Pagination `Link: <...?after=...&domain=lhr.life&...>; rel="next"` — relative path drops `/v1`, re-prefix it (per prior lane).
- urlscan anonymous search healthy; no 429/403 this round. Polite pacing held (3–4 s between calls; ~15 calls total). Per-day `date:` queries are the working anonymization of the 100-result cap for new dates.
- New verified query syntax for self-label enumeration: `q=task.tags:<hex>` (documented in urlscan's ElasticSearch-ish syntax; the `task.` prefix is required — bare hex matches nothing).
- The one CertSpotter record id equals the prior lane's pagination `after` marker (`17596783160`), confirming exactly one new record entered the dump since the prior lane's pull — dedupe-by-`tbs_sha256` cross-check passes.
- `uq_htmx.py` workaround (curl for urlquery keyless) not needed this round — no urlquery lookups were in this task's scope.

## Open items (for the parent / future lanes)
1. **NEW tunnel `c7a1f824a6efc4.lhr.life`** (provisioned ~Oct 2, bare-root liveness check) — watch for page deployment and target. Third task family if the target isn't tronzap/onlytron.
2. Expand the campaign's target inventory: onlytron.com is confirmed (both actors); whether the Sep-26 burst's targets extend further (onlytron equivalents of `dash/api/mock`) is untested. An anonymous `domain:onlytron.com` pre-Sep-29 lookback is still inside the 30-day window.
3. Same-or-different-actor question for `xq-recon-probe` vs `87270ca9ac10`: the result-detail 403 block (prior lane §1) remains the binding constraint — POST bodies / tunnel pages for the Sep-26 scans would settle it. Browser-capable or urlscan-account delegation spec unchanged.
4. crt.sh recovery watch: re-fetch `%.lhr.life` when 502s clear; the 4 pre-2026 ZeroSSL names are the gap.
5. Liveness of the Sep-29 roots and the new Oct-2 tunnel needs an off-proxy vantage point (unchanged).
