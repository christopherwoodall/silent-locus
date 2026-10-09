# LANE B — metronomic re-scan / watcher patterns (urlquery.net)

Date: 2026-10-04 (analysis run ~23:30–24:00 CDT)
Status: OFFLINE ANALYSIS ONLY — VM egress to urlquery.net was down the entire run
(proxy CONNECT hangs; even google.com fails). All findings below are from frozen
corpora. Live-search backlog is listed at the end.

Corpora used:
- `new-fleets/raw/window1.json` — 123 reports, recent window 2026-10-05 03:18–03:46 UTC
- `new-fleets/raw/jmail_world.json` — 72 reports, 2026-10-04 23:54 → 2026-10-05 03:58 UTC
- `raw/page_*.json`, `raw/gaode/`, `raw/infra/*/`, `raw/pivots/*/` (Amap fleet + pivots)
- `data/2025-12-04-urlquery-marker-sweep/raw/*.json` (exploitgym/cybergym marker sweep)

Method: group by fqdn, exclude our mapped Amap-fleet grammar (`uqscan=`/`uqtag=`/`uqvnc=`),
compute inter-submission gaps → median gap, gap stddev (regularity score), CV = sd/median.

## Candidates

### 1. jmail.world auditor — REFERENCE AUDITOR (confirmed programmatic)
- 72 reports, span 4h04m (2026-10-04 23:54 → 2026-10-05 03:58 UTC)
- median gap 3.0 min, gap sd 3.21 min, CV ~1.1 (minute-quantized htmx data)
- 72 unique submitted URLs — cycling jmail.world paths (/thread/<id>, /drive/<vol>, /search,
  /promotions) with mutating `?q=` payloads (followlike.net/?r=19384926, livetrafﬁc.net
  refer=119334, 2pink.org ref, watch-phrase `seekers+of+decay`)
- Still active at last observation (see baseline.md: run extended to 04:13 UTC+ with new EFTA
  thread IDs and folllike.com variants)
- Verdict: **programmatic audit loop**. Submitter-driven: URL rotation + param mutation
  across a target list, new payloads appearing mid-run (03:58 latest). Not platform
  auto-rescan — platform rescans would repeat identical URLs, not mutate the `?q=` payload.

### 2. paralino.app — NEW WATCHER CANDIDATE
- 6 reports in 20 min (2026-10-05 03:19 → 03:39 UTC), median gap 5.0 min, gap sd 3.0 min, CV 0.61
- Single submitted URL: bare `paralino.app` (no path/params), repeated identically all 6 times
- Report gaps (min): 1, 1, 5, 6, 8 — tight cluster, then ~5-min spacing
- Verdict: **likely programmatic watch loop or paired audit** (see #3: same window, same shape).
  Identical bare-host re-scan at ~5-min median is exactly the re-submit-to-check-detection
  pattern. Needs live history: pull full `paralino.app` search to see if the loop is older.

### 3. www.get-monai.app — NEW WATCHER CANDIDATE (paired with #2)
- 5 reports in 24 min (2026-10-05 03:19 → 03:43 UTC), median gap 5.5 min, gap sd 4.1 min, CV 0.74
- Single submitted URL: bare `www.get-monai.app`, repeated identically
- Report gaps (min): 1, 4, 7, 12
- Verdict: **likely same actor as #2** — both `.app` TLD, both bare host, both start 03:19–03:20,
  both re-scanned 5–6x inside the same 24-min window. Looks like an actor working a target
  LIST (two similar app-landing domains) and re-scanning each on a short loop — detection
  audit workload, not manual triage (triage wouldn't re-submit the identical bare URL 6x
  at 5-min spacing).

### 4. appwrite.network campaign residue — NOT watchers (analyst/campaign triage bursts)
- new-console.appwrite.network: 190 scans / 37 days (med 72 min, sd 636) — bursty
- vibes.appwrite.network: 186 scans / 34 days (med 67, sd 699)
- branch-* subdomains: dozens of 5–23-scan bursts over 1–3 days (med 5–21 min, sd 8–172)
- Verdict: **exploit-gym harness campaign residue** — many agents scanning the same Appwrite
  branch deployments during Aug 2026 (see memory: 966 'exploitgym' reports, 797 in Aug).
  Day-over-day repeats of the SAME bare deployment URL over weeks, but gaps are irregular
  bursts, not metronomic. Not a watcher loop; it's many distinct submitters hitting one target.

### 5. collusion.wiki — analyst triage, not metronomic
- 5 distinct scans on Sep 8 (3x), Sep 10, Sep 24, Sep 28 — irregular, no cadence
- Verdict: **analyst re-checks** (consistent with our own fake-org lane lookups). Not a loop.

### 6. Our own traffic — flagged, excluded from verdicts
- httpbun.com 73x/6h (med 1.9) = our marker sweep (`marker=claude…`, `marker=research…`)
- livecodes.io 26x, href.li 15x = our Amap/GZHOSP/Baxia probes (`uq=href20261004a`,
  epoch-nonced titles). Their bursts sit in our operator corpus by design; not discoveries.

## What did NOT reproduce
- No urlquery day-over-day (≥3 distinct dates, regular cadence) watcher loops found in the
  frozen corpora outside the appwrite campaign residue (irregular) and the jmail auditor
  (single 4h run, no multi-day evidence yet). The urlscan `90667af7b6a9f1.lhr.life` 27x-daily
  pattern has no urlquery analogue in this data — needs live day-scoped searches.
- No submitter matching our Amap `uq*=` grammar outside the mapped fleet.

## Regularity scoreboard (n≥5, all corpora)
| host | n | span | med gap | sd | CV | verdict |
|---|---|---|---|---|---|---|
| jmail.world | 72 | 4.0h | 3.0m | 3.2m | 1.07 | programmatic audit loop |
| paralino.app | 6 | 20m | 5.0m | 3.0m | 0.61 | likely watch loop (paired) |
| www.get-monai.app | 5 | 24m | 5.5m | 4.1m | 0.74 | likely watch loop (paired) |
| branch-cursor-mysql-e2e-230e6d5-aa6653f.appwrite.network | 13 | 2.8h | 12.2m | 8.0m | 0.66 | campaign burst, not metronomic |

## Caveats
- Gap stats on htmx-sourced rows (jmail_world.json, window1.json) are minute-quantized;
  API-format rows carry second precision.
- Corpora are biased: Amap-fleet and marker-sweep queries over-represent our own probes
  and the exploit-gym campaign. A clean random recent-window sweep was not possible offline.
- Platform auto-rescan vs submitter-driven: urlquery exposes no submitter identity on
  keyless tier. Heuristic used — URL mutation/rotation + target-list pairing ⇒ submitter;
  identical-URL repeat at rigid fixed interval ⇒ suspected platform. #2/#3 lean submitter
  because of the pairing and the irregular-but-tight gap spread.

## Live-search backlog (needs working egress — NOT done)
1. `uq_htmx.py search --query paralino.app --limit 100` — full history: is the loop ongoing?
   Also search `url.domain:paralino.app` for day-over-day pattern.
2. Same for `get-monai.app` / `url.domain:get-monai.app`.
3. `jmail.world` deeper history (pre-23:54 Oct 4) — does the auditor run daily?
4. Day-over-day sweep: `url.domain:` queries for repeat-scan hosts; check for a urlquery
   analogue of the urlscan 27x-daily watcher.
5. Identity of paralino.app / get-monai.app (who they are, why they'd be audit targets).
