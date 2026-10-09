# METRONOME — Timing-only findings (resumed run, post-VM-restart)

Persona: hunt purely on TIME. Language is noise; cadence is signal.
Goal: discriminate **scheduled-script cadence** from **interactive-agent cadence** in observed submission timestamps.

Scope: local corpora (Amap fleet, jmail campaign, webhook-deaddrops) + live urlquery htmx crawl of 13 dead-drop/relay/paste services (polling below). urlscan.io + OTX probed as secondary cadence surfaces.

Builds on cultural-anthropologist-ea (Labour Day silence, Golden Week trough, 996-shaped rhythm) — not duplicated here. This report adds the cadence layer underneath: what the *gaps between submissions* say about the scheduler.

## 1. Headline: the scheduler-discrimination test works

urlquery report submission times resolve to the second. Two clocks are visible in our data:

| | jmail (script/cron baseline) | Amap fleet (agent) |
|---|---|---|
| n reports | 72 | 1,970 |
| second-==0 share | **1.000** (every single one) | 0.018 |
| modal inter-arrival gap | 180 s (share 0.46) | 0 s (share 0.17) |
| gap CV | 0.94 | 13.87 |
| parallel (≥3 distinct tags same minute) | 0 | **153 minutes** |
| gap histogram peak | 1–5 min | <10 s |
| second-of-minute distribution | phase-locked | uniform (χ²=58.9, df=59, p≈0.48) |

**Reading:** jmail is a wall-clock scheduler firing on minute boundaries with a ~3-minute period (60/180/360 s variants) — a cron-shaped script. The Amap fleet never touches second boundaries, submits in same-second volleys across ≥3 distinct task tags within the same minute, and its gap CV of 13.9 is heavy-tailed human/machine-interactive jitter: median gap 12 s, p90 167 s, max 32.8 h (the Oct 2 Golden Week silence). These are not the same kind of machine.

## 2. Amap fleet burst shapes (Oct 4 super-run)

Sliding 30-min windows, ≥10 submissions:

| window start (UTC) | reports | within-burst gap CV |
|---|---|---|
| 2026-10-04 08:23 | 110 | 1.44 |
| 2026-10-04 09:59 | 106 | 1.69 |
| 2026-10-04 12:52 | 98 | 1.28 |
| 2026-10-04 11:21 | 94 | 1.74 |
| 2026-10-04 05:21 | 93 | 1.81 |

Within-burst CV stays >1.2: bursts are dense but internally irregular — a parallel swarm with jittered per-worker pacing, not a metronomic batch. Same-second duplicate gaps (155 zero-second pairs) are parallel-worker collisions, not retries (no retry grammar in URLs).

## 3. Per-tag cadence (top tag groups, Oct 4)

| tag | n | median gap | CV | span (UTC) |
|---|---|---|---|---|
| research20261004 | 9 | 3,429 s | 0.83 | 03:37 → 13:04 |
| target20261004a | 8 | 3,822 s | 1.35 | 03:41 → 20:40 |
| research20261004b | 6 | 1,699 s | 0.80 | 09:47 → 13:33 |
| claude20261004target1 | 4 | 9,751 s | 0.53 | 03:10 → 11:51 |

Every named tag group: zero second-boundary hits, CV 0.5–1.7, spans of many hours with sparse irregular submissions. These read as long-lived interactive sessions (an agent working a task), not scheduled ticks.

## 4. Second-of-minute uniformity (fleet-level jitter proof)

1,970 fleet submissions across 60 second-bins: χ² = 58.9, df = 59, p ≈ 0.48 — indistinguishable from uniform. Bin counts 18–48 vs expected 32.8. **No wall-clock phase-locking at any granularity**: minute-boundary share 0.0005. A cron or `sleep`-loop scheduler cannot produce this; jittered interactive submission can.

## 4b. Task-nonce epochs = dispatch-time markers (museum family, live-monitor)

Two observed fan-outs carry epoch nonces inside the tagwords, minted seconds before the urlquery submission:

- 2026-10-04 10:16:14Z nonce `1791108974` → 5 submissions at 10:17:00Z for one POI (`B01730HZRE`) across 5 endpoints (mobile/www/place/api/infosearch), tagwords `henanmuseum-{mobile,www,place,api,info}-1791108974`. **Delta: 46 s** (task dispatch → submission).
- 2026-10-05 03:42:46.193/47.417/48.959Z nonces (`17911717661939` etc., epoch-ms ×10) → 3 submissions at 03:43:00Z for POI `B03DF05V64`. **Deltas: 12–14 s**, nonces 1.2 s apart (sequential per-request minting within one task run).

Reading: the nonce is minted when the agent builds each request; the gap to submission is agent execution + sandbox run + submit latency. Same-minute multi-endpoint fan-out of one POI = a single task probing in parallel. A cron scheduler would show round, regular, aligned ticks — these show irregular, per-request, sub-minute dispatch. **The nonce-to-submission delta is a scheduler discriminator: jittered 10–60 s deltas = interactive agent; ~0 s or exactly-periodic deltas = scripted submitter.**

## 5. Poller lane: dead-drop/relay service timing on urlquery (LIVE CRAWL — COMPLETE)

3-pass htmx crawl of 13 services completed 2026-10-05 06:00 UTC (60 s between calls; uq-operator markers excluded; sibling overlap tolerated). Totals: webhook.site 20, ntfy.sh 6, requestbin 0, pipedream 49, telegra.ph 50, file.io 23, 0x0.st 36, paste.rs 42, rentry 50, hastebin 22, temp.sh 46, catbox.moe 50, filebin.net 23. Analysis: `raw/analyze_poller.py` → `poller_analysis.json`.

**Result: honest negative for scheduled dead-drop beaconing.** Zero metronomic runs on any service (≥8 consecutive gaps, CV<0.3). All services: sparse, irregular submissions (median gaps hours-to-days, CV 0.9–2.7). Only parallel signatures: paste.rs (2 minutes, 3–4 distinct URLs) and temp.sh (1 minute, 3 URLs) — one-off bursts, not schedules.

Notables:
- webhook.site submissions carry `?r=` nanosecond-epoch nonces (`?r=1782070800983511679` → 2026-06-21T19:40Z; submission 2026-06-24; another submitted 07-07). The nonce predates submission by days — it is embedded in the *scanned URL* (minted by whoever built it), not by the urlquery submitter. Agents re-scan URLs with stale nonces.
- requestbin.com: zero hits — service is defunct; expected.
- tz-inference on these sets is noise (sparse data, 0.5–0.7 in-window shares); no timezone claims made.

**Reading:** the operator's dead-drop usage (e.g. the Baxia beacon the Contrarian found) does not appear as periodic urlquery submissions. Dead-drops are used event-wise, not beaconed on a schedule — or their urlquery footprint is elsewhere.

## 6. Secondary surfaces

- **urlscan.io:** anonymous search works (no API key) except leading-wildcard regex. `page.domain:webhook.site` → 63 scans / 30 days — too sparse for cadence. `task.url:"uqscan="` → 0 hits. urlscan is not a cadence surface for this fleet.
- **OTX:** reachable (200). No per-second timestamped cadence data exposed for these indicators; not pursued.
- **webhook-deaddrops corpus** (2026-05-12): n=17 over 4.5 months — too sparse for cadence (median gap 7.8 min, CV 2.67, second-0 share 0.88 is suggestive of aligned submissions but n is too small to grade).

## Caveats

- The jmail script-baseline is the local 72-report window (`new-fleets/raw/jmail_world.json`), not the full 872-report/64 h campaign described in the cachedview report — the second-0 = 1.0 result is exact within the window but should be re-run against the full set.
- urlquery `date` fields are the *report submission* times, not the agent's scan times — all cadence claims are about submitter behavior on urlquery, which is one step removed from the agent's own scheduler. The museum nonce analysis (tag epochs vs submission) bridges this gap for the two observed fan-outs.

## Evidence grading

| Finding | Grade |
|---|---|
| jmail = wall-clock scheduler (second-0 = 1.0, 180 s mode) | **confirmed** (72 local reports) |
| Amap fleet = interactive jittered agents (uniform seconds, CV 13.9, 153 parallel-tag minutes) | **confirmed** (1,970 reports) |
| Oct 4 bursts = irregular parallel swarm, not batch job (within-burst CV >1.2) | **high confidence** |
| Per-tag sessions = long-lived interactive (hours, sparse, unaligned) | **high confidence** |
| Second-of-minute uniformity = no wall-clock phase-locking (χ²=58.9, df=59) | **confirmed** |
| Task-nonce epochs = dispatch markers; nonce→submission deltas 12–46 s (museum fan-outs) | **confirmed** (live-monitor LOG, 2 fan-outs) |
| Dead-drop relay cadence on urlquery: no metronomic runs on 13 services; sparse event-wise use | **confirmed negative** (417 reports, 3-pass live crawl) |
| webhook.site `?r=` ns-epoch nonces predate submission by days (embedded in scanned URL) | **confirmed** (2 cases) |

## Method notes

- Timestamps are urlquery report submission `date` fields (second resolution, verified non-truncated: Amap dates show non-zero seconds).
- Amap corpus @timestamp is normalization time; real event time comes from raw/page_*.json report dates.
- No commits/pushes. Hunt agents, not operators.
- Scripts: `raw/fetch_poller.py`, `raw/fetch_poller2.py` (completion fetch, 06:00 UTC), `raw/egress_watcher.py`, `raw/analyze_poller.py` (→ `poller_analysis.json`), `raw/cadence_profiler.py` (→ `raw/cadence_profile.json`).

## Observed URLs (task-relevant)

- https://urlquery.net/api/htmx/search/ (crawl endpoint)
- https://urlscan.io/api/v1/search/?q=page.domain%3Awebhook.site (63 results / 30 d)
- Dead-drop/relay domains queried: webhook.site, ntfy.sh, requestbin.com, pipedream.net, telegra.ph, file.io, 0x0.st, paste.rs, rentry.co, hastebin.com, temp.sh, catbox.moe, filebin.net
- Observed dead-drop submission URLs (samples):
  - https://webhook.site/00f36f21-d00e-48b3-9456-8bf532e8c863?x=0
  - https://webhook.site/441b7745-1087-463e-b539-984a2ee3ea65?r=1782070800983511679
  - https://webhook.site/c1bf6b38-d6ea-4446-b17e-5f6c7a1cb357?r=1782071176301141190
  - https://0x0.st/8x5t.ps1, https://0x0.st/8zda.txt, https://0x0.st/X3ar.txt
  - https://paste.rs/8g83M, https://paste.rs/lVaj6
  - https://hastebin.com/share/vetuqukipo.bash, https://hastebin.com/share/mejinexufi.perl
  - https://temp.sh/wKwll/2.zip, https://temp.sh/Ykibi/8.1.5.zip
