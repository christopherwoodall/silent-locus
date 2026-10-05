# NIGHT OWL — human-vs-machine time analysis

Persona: hunt on the clock. Agents don't sleep; humans do. Burst clusters plotted by
hour-of-day (UTC) and day-of-week; operator timezone inferred from active hours.

## Data sources
- `new-fleets/raw/jmail_world.json` (72 reports, the jmail.world auditor)
- `events.jsonl` (2,141 records) joined to true submission dates from `raw/page_*.json`,
  `raw/gaode/*.json`, `raw/lanes/*.json` (2,000 matched — NOTE: earlier plots that used
  `@timestamp` directly were collection-biased; true-date join changes little, see caveat)
- `raw/lanes/urlscan/*.json` (418 urlscan.io records from the uqscan urlscan lane)
- `live-monitor/LOG.md` (museum family timestamps)
- `writeup-idph-iowa.md` (June IDPH burst dates)

## 1. jmail.world auditor — the "overnight metronome" is a Monday-morning work session in Asia

- 72 reports, **Sun 2026-10-04 23:54 UTC → Mon 2026-10-05 03:58 UTC**, median gap 3.0 min
  (33 gaps exactly 3.0 min; 7 same-minute doubles; one 4-report minute at 00:33 UTC).
- The metronome is machine cadence. The *window placement* is the fingerprint:

| Operator TZ | Local window | Reading |
|---|---|---|
| UTC+8 (Beijing/Singapore/Taipei) | **Mon 07:54 → 11:58** | Monday-morning work session |
| UTC+9 (Tokyo/Seoul) | Mon 08:54 → 12:58 | Monday-morning work session |
| UTC+1 (Central Europe) | Mon 00:54 → 04:58 | Deep night — machine-only |
| UTC-4 (US Eastern) | Sun 19:54 → 23:58 | Sunday evening |

- Asia-TZ reading is suspiciously clean: starts at start-of-workday, runs exactly 4 hours,
  stops before lunch. Either a human kicked it off Monday morning, or a cron is scheduled
  for Asia work hours. Europe reading = pure machine; US reading = Sunday-evening hobbyist.
- 12/72 reports routed through `cachedview.nl` (archive-oracle-as-fetch-proxy) — the 4-in-one-minute
  cluster at 00:33 UTC is the proxy parallelizing fetches, not the auditor speeding up.
- Verdict: **machine execution inside a human-plausible Asia workday window**. Scheduled
  detection/verification workload, not interactive.

## 2. Known operator corpus (2,000 true submission dates) — human-modulated machine

Hour-of-day (UTC), true submission dates:

```
 0   65 |  5  151 | 10  188 | 15   41 | 20   71
 1   47 |  6  139 | 11  156 | 16   28 | 21   61
 2   31 |  7  105 | 12  123 | 17   64 | 22   44
 3   86 |  8  128 | 13  144 | 18   72 | 23   36
 4  109 |  9   63 | 14   30 | 19   18 |
```

Read in **UTC+8 (Beijing)**: twin peaks 13:00–16:00 and 18:00–21:00 local; dip at 17:00
(dinner); dip 22:00–00:00 (bedtime); floor 02:00–04:00 (deep sleep, hour 19 UTC = 03:00
Beijing = 18 reports, the global minimum). That is a **human workday shape** — afternoon
plus evening session, dinner break, sleep at night — with machine execution filling the hours.

Read in other TZs the shape breaks: UTC+1 gives a 10:00 dip mid-morning (no lunch/dinner
logic); UTC-4 puts both peaks in deep night/early morning. **UTC+8 fits best.**

- Activity at *every* UTC hour (no true zero) = the machine never fully stops; the human
  modulates intensity. Human-assisted fleet, not lights-out autonomous.
- Same reading from the urlscan.io lane (418 records): flat 24/7 with peak at 13:00 UTC
  (= 21:00 Beijing, inside the evening peak).

## 3. Museum family — Sunday evening + Monday morning (Asia)

From `live-monitor/LOG.md` (UTC → Beijing):
- 2026-10-04 10:17 ×5 (same-minute parallel burst) → **Sun 18:17** — evening session
- 2026-10-04 14:01 → **Sun 22:01** — late evening
- 2026-10-05 02:31, 02:33 → **Mon 10:31/10:33** — morning session
- 2026-10-05 03:16 ×2 → **Mon 11:16** — morning session

Same shape as the main corpus: evening + morning Asia workday. The 5-report same-minute
burst is machine parallelism; the session placement is human.

## 4. Weekend behavior — machines don't take weekends

- **IDPH Iowa burst**: 48 reports **Sat 2026-06-20 / Sun 2026-06-21** — full weekend operation.
- **AIHW June strand** (`uqtag=AGEDATA23`): 2026-06-20 — Saturday.
- **Current activity**: Sun Oct 4 / Mon Oct 5 — weekend into workweek, no dip.
- Day-of-week for the corpus is collection-biased (1,749/2,000 on Sunday = collection
  window), so no fleet-level weekend conclusion from the corpus — but the two anchored
  historical bursts (IDPH, AIHW) both ran on weekends. **No weekend dip observed anywhere.**
- Dream swarm (different actor, for contrast): Wed Jul 1 → Sat Jul 4 — workdays into
  weekend, consistent with a human-directed offensive op.

## 5. Comparison: tronzap test-matrix (different actor)

Sep 26 burst, ~40 scans in 2 hours (per `urlscan-lhr/FINDINGS.md`) — a compressed test
matrix, plus one tunnel scanned ~daily (27×, monitoring pattern). No hour-of-day recovered
(raw not retained in that lane — gap noted). Shape reads as a human pentester's scripted
run + a watcher, distinct from our operator's sustained workday modulation.

## Fingerprint summary

| Signal | Known operator (Amap fleet) | jmail.world auditor |
|---|---|---|
| Cadence | Bursty, parallel same-minute clusters | 3.0-min metronome |
| Active hours (UTC) | All 24h, peaks 05–08 / 10–13 | 23:54–03:58 only |
| Asia-TZ reading | Afternoon + evening, dinner dip, night sleep | Mon 07:54–11:58 work session |
| Inferred operator TZ | **UTC+8** (best fit) | UTC+8 (best fit) or US-Eve |
| Weekend | No dip (IDPH/AIHW ran Sat/Sun) | n/a (single 4h run) |
| Human vs machine | Machine execution, human-modulated hours | Machine execution, human-scheduled window |

## Leads / open questions
1. The **dinner dip** (09:00 UTC = 17:00 Beijing) in the operator corpus is the most
   human tell in the dataset. Worth re-testing as more dated reports accumulate —
   if the dip survives at scale, operator TZ = UTC+8 is strong.
2. jmail auditor's Monday-morning-Asia window + metronome + detection workload =
   possibly a **researcher or security vendor's scheduled audit**, not a threat actor.
   The US-Eastern Sunday-evening reading keeps the hobbyist hypothesis alive.
3. Tronzap Sep-26 burst hour-of-day not recovered — if raw urlscan data is re-pulled,
   add it here for the three-actor comparison.
4. htmx endpoint throttled during this session (timeouts after ~6 queries at 6s spacing);
   museum/pandalegacy/probe2-start timing pulls deferred.

## Method note
`@timestamp` in `events.jsonl` ≈ submission date for recent records but the safe join is
`labels.report_id` → raw file `date` fields (2,000/2,141 matched). Day-of-week across the
full corpus is dominated by the Oct 4–5 collection window — do not cite it as a fleet
property; use only anchored historical bursts (IDPH, AIHW) for weekend claims.
