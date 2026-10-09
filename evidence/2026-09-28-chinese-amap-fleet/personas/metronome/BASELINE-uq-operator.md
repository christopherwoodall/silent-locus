# TIMING EXCLUSION BASELINE — the known uq operator (Chinese Amap fleet)

**Dataset:** `../events.jsonl` (read-only; never modified by this analysis) — 2,141 records,
2026-09-28 20:57:23Z → 2026-10-05 01:12:40Z (~6.7 days).
**Built:** 2026-10-04 (UTC ~2026-10-05). Script: `build_baseline.py`; profile: `baseline_profile.json`.

---

## 1. The exclusion spec (the whole point of this file)

A candidate run is **PROBABLY the known uq operator** if it matches **ANY** of the
timing rules below. Matching none of them is reason to treat it as a NEW swarm;
matching a timing rule only *admits* the candidate — grammar/domain evidence
(`uqscan=`, `uqresearch=`, `uqcors`, `uqlhr` tunnel probes, `httpbun` staged
programs) is still required to *attribute* it.

| # | Rule | Basis |
|---|------|-------|
| E1 | **Burst-dominant, irregular cadence.** Within an active session, median inter-arrival gap 3–40 s, with 46 % of all gaps ≤ 15 s and 71 % ≤ 60 s, but **no metronomic run** (CV < 0.3 over ≥ 10 consecutive gaps) anywhere in the corpus. | 2,140 gaps: med 13 s, p25 3 s, p75 53 s. Zero qualifying regular runs, corpus-wide AND per-family. |
| E2 | **Session structure: one giant campaign window.** A single session of 1,000–2,000 submissions spanning ~24–26 h, separated from smaller satellite sessions (20–65 subs each) by ≥ 30 min idle gaps. Only 23 sessions in 6.7 days; 1 session holds 89 % of traffic. | Sessionized at 30 min idle: n=1,902 (25.4 h), next-largest n=63. |
| E3 | **Burst clusters > 20/hour.** The operator does 43–190 subs/hour for many consecutive hours (up to ~14 h straight), peaking 03:00–14:00 UTC. A sustained > 20/hour window with amap-uqscan majority is in-profile. | 15 non-overlapping > 20/hour windows; top: 190/hour 2026-10-04 09:57 UTC. |
| E4 | **Mild parallelism, ≤ 3 distinct targets per minute.** Same-minute submissions to different targets occur (71 min in corpus), max 3 distinct targets in one minute. 4+ distinct targets in a single minute is OUT of profile. | per-minute distinct-target counts: 1→791, 2→67, 3→4, ≥4→0. |
| E5 | **24/7 with a diurnal peak, not business-hours.** Activity every UTC hour (min 19/hour at 19:00 UTC, max 191 at 10:00 UTC); Beijing-time peak 18:00–23:00 CST is weak (peak hours span the clock). A strict 9–5 weekday pattern is OUT of profile. | Hour-of-day table, §2. |
| E6 | **Family-specific cadences.** amap-uqscan med-gap ~22 s; amap-plain ~37 s; amap-otheruq ~71 s; httpbun-staging ~138 s (all Oct 4); httpbin-staging ~174 s; livecodes-staging ~12.8 min med-gap; hrefli-relay ~51 s (hrefli med 51 s *within its own sequence*, spread over hours). A staging family (httpbun/httpbin/livecodes) with sub-5 s cadence is OUT of profile. | §7. |
| E7 | **No long regularity.** The operator's *most* regular 12-submission stretch ever observed still has CV ≈ 0.46. A candidate run with near-constant gaps (CV < 0.3 over ≥ 10 consecutive submissions) is evidence of a DIFFERENT operator — this is the strongest timing exclusion in the file. | Exhaustive sliding-window + greedy search, CV < 0.3 and CV < 0.5, all families. |

**Strong exclusion-negatives** (timing shapes never seen from this operator):
- strict metronome (E7 contrapositive);
- 4+ distinct targets submitted in the same minute;
- staging-surface families firing faster than ~1/min sustained;
- activity confined to a single 9–5 weekday window with zero off-hours traffic;
- gaps > 12 h occurring *inside* an active campaign day (the 3 longest gaps are 10.5–32.8 h, all between campaign sessions).

---

## 2. Activity curve — submissions per hour-of-day

UTC first column; Beijing (UTC+8) second. The operator never sleeps: every UTC
hour has ≥ 19 submissions. Peak traffic 05:00–13:00 UTC (13:00–21:00 CST) —
evening-heavy in China time, but the tail is fat all night.

| UTC hr | n | CST hr | n | UTC hr | n | CST hr | n |
|--------|---|--------|---|--------|---|--------|---|
| 00 | 65 | 08 | 65 | 12 | 135 | 20 | 135 |
| 01 | 47 | 09 | 73 | 13 | 155 | 21 | 154 |
| 02 | 32 | 10 | 74 | 14 | 47 | 22 | 146 |
| 03 | 87 | 11 | 19 | 15 | 67 | 23 | 109 |
| 04 | 111 | 12 | 74 | 16 | 47 | 00 | 128 |
| 05 | 154 | 13 | 61 | 17 | 73 | 01 | 68 |
| 06 | 146 | 14 | 47 | 18 | 74 | 02 | 191 |
| 07 | 109 | 15 | 39 | 19 | 19 | 03 | 165 |
| 08 | 128 | 16 | 65 | 20 | 74 | 04 | 135 |
| 09 | 68 | 17 | 47 | 21 | 61 | 05 | 155 |
| 10 | 191 | 18 | 47 | 22 | 47 | 06 | 47 |
| 11 | 165 | 19 | 87 | 23 | 39 | 07 | 67 |

Read as: UTC 10:00 = 18:00 CST → 191 submissions. No UTC hour is empty;
peak:hour-to-trough ratio ≈ 10:1 (191 vs 19). **Inference: not a human
9–5 shift; either 24/7 automated fleet or multiple shifts. Do NOT infer
"Chinese timezone" from timing alone — the curve is campaign-shaped, with
89 % of traffic in one 25-hour window.**

---

## 3. Inter-arrival gap distribution

n = 2,140 gaps. min 0 s, max 32.8 h (118,008 s), **median 13 s**, mean 249 s
(mean ≫ median = burst/idle mixture).

| Bin | Count | Share | Interpretation |
|-----|-------|-------|----------------|
| ≤ 5 s | 605 | 28.3 % | rapid-fire bursts, 167 exactly 0 s |
| 5–15 s | 376 | 17.6 % | steady intra-burst cadence |
| 15–60 s | 513 | 24.0 % | slower bursts / interleaved tasks |
| 1–5 min | 378 | 17.7 % | task-switching lulls |
| 5–30 min | 79 | 3.7 % | between task families |
| 30 min–2 h | 14 | 0.7 % | session breaks |
| 2–12 h | 5 | 0.2 % | overnight/weekend idles |
| > 12 h | 3 | 0.1 % | between campaign days |

Log-modes: 10⁰ s = 798, 10¹ s = 857, 10² s = 282, 10³ s = 29 → **bimodal
operating cadence**: 1–60 s while active, minutes-to-hours while idle.

---

## 4. Metronomic runs: NONE (the headline result)

Exhaustive search for near-constant spacing — sliding windows of 8–12
submissions at CV < 0.3 / < 0.5, plus greedy extension, run both on the full
submission sequence AND within each task family (uqscan, amap-plain,
amap-otheruq, httpbun, httpbin, livecodes, hrefli):

- **Corpus-wide, CV < 0.3 over ≥ 10 consecutive: 0 runs.**
- Per-family, CV < 0.3 over ≥ 10 consecutive: 0 runs in every family.
- Most regular stretch ever observed: 12 submissions, mean gap 67.6 s, CV 0.46
  (mixed httpbun/uqscan, Oct 4) — fails the bar by a wide margin.

**Implication for the hunt:** the uq operator is bursty but irregular — its
gaps are driven by task scheduling, not a timer. If the metronome lane finds
a clean metronomic run, that is evidence of a DIFFERENT operator, not this one.
(Per BigSexyWarlock69's anomaly rule: "doesn't fit the frame is a lead, never
a negative" — a regular cadence with uq grammar would be a *novel finding*.)

---

## 5. Burst clusters — top 15 non-overlapping > 20/hour windows

All from the Oct 3–4 campaign (windows in UTC):

| Window (UTC) | n/hour | Top families |
|--------------|--------|--------------|
| 2026-10-04 09:57 | 190 | uqscan 107, plain 53, uq 10 |
| 2026-10-04 12:27 | 169 | uqscan 88, plain 60, httpbin 8 |
| 2026-10-04 04:57 | 164 | uqscan 96, plain 55, uqresearch 5 |
| 2026-10-04 10:57 | 160 | uqscan 73, plain 50, uqtarget 12 |
| 2026-10-04 05:57 | 135 | uqscan 82, plain 45, uqresearch 2 |
| 2026-10-04 07:57 | 134 | uqscan 84, plain 44 |
| 2026-10-04 06:57 | 106 | uqscan 75, plain 16, httpbin 6 |
| 2026-10-04 03:57 | 101 | uqscan 63, plain 36 |
| 2026-10-04 17:27 | 86 | uqscan 41, plain 25, uqmobile 4 |
| 2026-10-04 13:27 | 78 | plain 30, uqscan 25, uqresearch 8 |
| 2026-10-04 14:57 | 63 | httpbun 22, uqscan 22, plain 5 |
| 2026-10-04 02:57 | 62 | uqscan 36, plain 26 |
| 2026-10-04 08:57 | 58 | uqscan 29, plain 20, livecodes 5 |
| 2026-10-04 19:57 | 47 | uqscan 23, plain 21, httpbun 2 |
| 2026-10-04 15:57 | 43 | httpbun 19, uqscan 14, plain 6 |

Signature shape: bursts are **uqscan-majority with a plain-scan minority**
(~2:1 ratio) plus occasional staging-family sprinkles. Staging families
(httpbun/httpbin/livecodes) NEVER form their own > 20/hour window.

---

## 6. Parallel-execution signature

Targets = submitted_domain (amap/httpbun.com/httpbin.org/livecodes.io/
href.li/baidu.com/webhook.site/gaode.com).

- Minutes with > 1 distinct target: **71**
- Max distinct targets in one minute: **3** (only 4 minutes reach 3)
- Distribution: 1 target/min → 791 min; 2 → 67; 3 → 4; **≥ 4 → 0**
- Parallel minutes usually pair amap.com with a staging domain
  (e.g., httpbun + amap in the same minute) — staging and scanning run
  concurrently but from a thin concurrency pool.

**Verdict: low-parallelism operator.** ~3 concurrent workers max. A swarm with
10+ distinct targets per minute is a different beast.

---

## 7. Task-family timing profiles

Families classified by submitted_domain + uq grammar in the note
(see `build_baseline.py::classify`). Gap stats are within-family
(inter-arrival of that family's own submissions).

| Family | n | Within-family med gap | Mean gap | UTC peak hours | Active span |
|--------|---|-----------------------|----------|----------------|-------------|
| amap-uqscan (tagged fleet scans) | 1,019 | 22 s | 7.0 min | 10, 5, 6 | Sep 30 → Oct 5 |
| amap-plain (untagged scans) | 819 | 37 s | 10.9 min | 13, 5, 10 | Sep 28 → Oct 5 |
| amap-otheruq (36 minor grammars) | 162 | 71 s | 35 min | 11, 10, 13 | Sep 30 → Oct 4 |
| httpbun-staging (base64 staged programs) | 65 | 138 s | 5.6 min | 15, 16, 14 | Oct 4 only |
| httpbin-staging (base64 payloads) | 27 | 174 s | 19.4 min | 12, 13, 7 | Oct 4 only |
| livecodes-staging (staged HTML/JS) | 26 | 766 s (12.8 min) | 3.7 h | 13, 9, 22 | Sep 30 → Oct 4 |
| hrefli-relay | 19 | 536 s (8.9 min) | 29.6 min | 11, 12, 17 | Oct 4 only |
| baidu-transpage probes | 3 | 6.2 h | 3.1 h | 6, 12 | Oct 4 only |
| webhook-deaddrop | 1 | — | — | 15 | Oct 4 only |

Notes:
- **Scan families run ~10× faster than staging families.** uqscan med-gap
  22 s vs livecodes-staging 766 s. Staging is careful, hand-rolled work;
  scanning is fleet fire.
- **Staging families all cluster on Oct 4** (the staging-push day): httpbun
  20:11→~21:30 UTC (14:57 and 15:57 bursts), livecodes spread Sep 30–Oct 4.
- amap-otheruq's 162 notes carry 36 minor grammars: `uqresearch` 39,
  `uq` 31, `uqtarget` 19, `uqhost` 7, `uqretry` 6, `uqcors` (bare, no `=`),
  `uqmobile`, `uqfresh`, `uqdirect`, `uqmobilefull`, `uqe2e`, `uqperf`,
  `uqwasm`, `uqws`, etc. (full census in `baseline_profile.json`).
- fleet_tag values rotate per batch (943 distinct, e.g.
  `research20261004d`, `target20261004a`, `1790733601`) — tags are
  date-batches, not operator IDs.

---

## 8. Day-of-week pattern — CAVEAT: corpus too short to trust

| Day | UTC | Beijing |
|-----|-----|---------|
| Mon | 38 | 302 |
| Tue | 3 | 20 |
| Wed | 150 | 38 |
| Thu | 64 | 169 |
| Fri | 0 | 10 |
| Sat | 4 | 2 |
| Sun | 1,882 | 1,600 |

**Do NOT cite a "Sunday operator" pattern.** The corpus spans only
2026-09-28 (Mon) → 2026-10-05 (Mon); the Sunday spike is the single 25-hour
campaign session (Oct 3 23:52Z → Oct 5 01:12Z), not a weekly rhythm. Day-of-week
is UNINFORMATIVE for this operator until ≥ 2 full weeks are collected.

---

## 9. Reproducibility

- `build_baseline.py` — parser + all statistics; writes `baseline_profile.json`
  (full numeric profile) and was run with events.jsonl read-only.
- Corpus window bias: 89 % of records sit in one session; re-baseline after
  the next campaign lands — the median-gap numbers are dominated by Oct 3–4.
- Raw gap list, session boundaries, and the metronome-search parameters are
  all in the script; re-run cost is seconds.

---

## 10. One-paragraph summary for the hunt

The known uq operator is a **low-parallelism (~3 workers), burst-irregular
scanning fleet**: it fires amap scans in 3–40 s bursts for ~25 h straight,
then goes quiet for days; inter-arrival median 13 s; active every hour of
day; zero metronomic runs anywhere in the corpus (its most regular stretch
is CV 0.46). Staging work (httpbun/httpbin/livecodes base64 programs) is a
separate, slower rhythm (~2–13 min between submits) interleaved in the same
campaign day. **For the metronome hunt: a clean regular cadence is evidence
of a NEW operator, not this one — unless it also carries uq grammar, in
which case treat it as an off-frame lead.**
