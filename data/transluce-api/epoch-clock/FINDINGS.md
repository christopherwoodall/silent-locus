# Finding #147 — epoch-clock fingerprint: reconstruction + replication attempt

Date: 2026-10-07. Analyst: subagent (parent coordinator owns commits/pushes).
Read-only on cached data. Nothing redacted. Grades: OBSERVED / INFERENCE / UPSTREAM.

## 1. Transluce #147's method (reconstructed from findings-list.json, ≤5 lines)

1. YOURLS shortener keywords embed Unix epoch seconds as suffixes (e.g. `ag0secdata1781802293` → 1781802293).
2. Compare the embedded epoch against the link's creation timestamp from the venue's own public link-log API (rmn.re log, yourls.space API) — the venue where the actor created the marker, not a third-party scanner.
3. June 18 (rmn.re): embedded epoch ≈ creation time (1 s earlier) → naming tool used a live clock.
4. Sep 29–Oct 3 (yourls.space): links created two days apart all embed the SAME epoch 1779995045 (= 2026-05-28 19:04:05 UTC, one day after the May-27 prefill probe) → frozen clock, but the shared marker-word-plus-epoch naming convention links the two venue clusters to one naming tool.
5. The fingerprint is tooling-level (naming convention + clock behavior), explicitly NOT provider attribution; June→September linkage rests on it, May-27/Aug-9 venues tie in by label similarity only. Evidence links: rmn.re log, yourls.space stats API, Wayback CDX for yourls.pro/admin, findings #39/#57/#124/#130.

## 2. Replication attempt on our cache

### 2a. Input inventory (OBSERVED)

- Counsel's proposed inputs — (a) `zz=oai<digits>` / `oai<digits>` / `_oai=<digits>` nonces plus (b) observed timestamps — do NOT co-occur in our urlquery caches: `data/2025-12-04-urlquery-marker-sweep` (975 events) and `data/2026-09-28-chinese-amap-fleet` (2,141 events) have report timestamps but ZERO `oai<digits>` occurrences (grep-verified). The nonces live in `data/2026-10-03-openai-agent-traces/events.jsonl` (Arquivo.pt CDX captures, 589,972 rows): 14,940 rows carry `zz=oai<digits>` (nonce = `oai` + 10-digit epoch seconds + 7-digit suffix, e.g. `oai17816845870756322` → epoch 1781684587), all `record_kind=arquivo_pt_capture`, all `labels.incident=doe-crdc` (Jun-17 DoE cluster, confirmed dsqa_250 traffic).
- Correction to counsel's design (INFERENCE): the urlquery *submission* timestamp is the wrong comparator — the submitter is usually not the marker creator. #147's actual comparator is the marker-venue's own creation/observation time. Our closest cached analog is the Arquivo.pt capture timestamp (third-party observation of the marker-bearing URL, like #147's venue logs).

### 2b. Counsel-variant test: nonce-epoch minus observed-timestamp (OBSERVED, N=14,940, full population)

delta = nonce_epoch − arquivo.pt capture_epoch, seconds:

| stat | value (s) |
|---|---|
| N | 14,940 |
| min / max | −50.0 / 0.0 |
| p1 / p5 / p25 | −24 / −7 / −2 |
| p50 (median) / p75 / p95 / p99 | −2 / −1 / −1 / −1 |
| mean / stdev | −2.87 / 4.06 |
| within ±60 s | 14,940 (100%) |

Nonce-epoch span 2026-06-17 07:31:59→11:46:46 UTC tracks capture span 07:32:01→11:46:49 UTC across the full 4h14m incident window — nonces minted live throughout, never frozen.

### 2c. #147-direct test on cached rmn.re venue log (OBSERVED)

`data/2016-12-28-rmn-re/raw/link_table_decoded_2026-09-27.json` (764-row venue capture, per-link `created` + `ip` + `clicks`): 94 slugs carry 10-digit epoch suffixes. Raw delta = epoch − created(as UTC) clusters at −14,400 s ± 58 s. The venue log renders in UTC+4 (INFERENCE, forced): `ag0secdata1781802293` embeds 1781802293 = 2026-06-18 17:04:53 UTC while the log shows `created: Jun 18, 2026 21:04` — exactly +4 h. Against #147's asserted creation time of 17:04:54 UTC (UPSTREAM), the delta is **1 second: a live clock at creation**, replicating #147's June claim byte-exact on our independent cache. The 7 ag0-family rows in our capture match #147's listed June-18 keywords (ag0rmn, ag0rmntest, ag0viewer6043, ag0refresh4293, ag0secdata1781802293…).
The September half (yourls.space frozen epoch 1779995045, Sep 29–Oct 3) is NOT testable on our cache — no yourls.space log is cached and no new collection was performed per constraints.

## 3. Verdict

**KILL the counsel's clock-skew fingerprint hypothesis for the Jun-17 DoE dsqa_250 cluster.** Kill condition met on the "collapse" branch: deltas are not uniform/random — they collapse to the observation clock (median −2 s, 100% within 60 s, causal direction nonce-before-capture, tracking over 4+ hours). The nonces are live-clock minting; there is no consistent non-zero launcher/container skew to fingerprint. (A −3 s offset vs. an archive crawler is crawl latency plus ordinary clock disagreement — #147 itself reads a 1 s delta as "live clock," not skew — and is unattributable to provider infra.)

**KEEP (verified) #147's June live-clock claim.** It replicates exactly on our cached rmn.re log: `ag0secdata1781802293` = 1 s before #147's asserted creation time.

**OPEN (UPSTREAM-only): #147's September frozen-epoch claim** (1779995045 shared across Sep 29–Oct 3 yourls.space links). Untested — no cached venue log; needs the yourls.space public API pull from #147's evidence_links.

## 4. Most actionable lead

Run the identical epoch-minus-created test against the **yourls.space public link-log API** (`https://yourls.space/yourls-api.php?action=stats&format=json`, #147 evidence_link, already pulled 2026-10-03 per #147's Preservation note — request the cached zip/CSV from Transluce or re-pull) to verify/falsify the frozen-epoch 1779995045 claim on the Sep 29–Oct 3 cluster. If the September deltas cluster at ≈ −10.7M s (May-28 epoch vs Sep-29 creation) with near-zero spread, the fingerprint holds and the tooling link June→September is confirmed; if they scatter or sit at ≈0, #147's core linkage fails. Secondary: our rmn.re cache holds 94 epoch slugs vs. the 9 ag0 links #147 enumerates — diff the sets for coverage gaps.

## 5. Method notes for reuse

- Nonce form: `zz=oai` + 10-digit epoch seconds + 7-digit suffix (suffix looks like sub-second/random; first-10-digits split validated: all 14,940 in 2026 range, deltas causal).
- Venue logs that render local time will shift deltas by whole hours — calibrate with one known-true pair (as #147's ag0secdata1781802293 did here) before reading skew.
- Counsel's urlquery-submission-timestamp comparator should be retired: submitters ≠ marker creators, and our urlquery caches carry no oai nonces at all.
