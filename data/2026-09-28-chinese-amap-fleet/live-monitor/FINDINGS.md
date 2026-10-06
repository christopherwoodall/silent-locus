# FINDINGS — live-monitor lane (Chinese Amap fleet)

*Poll log: `LOG.md`. Monitor: `monitor*.py`, detached loop (survives agent death).*

## Purpose
Continuous urlquery htmx polling (`url.domain:amap.com`, `url.domain:gaode.com`, limit 30, recency-sorted) to detect new fleet scan reports as they land. Started 2026-10-05 01:27 UTC; ~20–30 min cadence.

## Baseline (Poll 0, 01:27 UTC)
- amap.com total_hits 1977 (up from 1975 at 01:12) — fleet ACTIVE at monitor start.
- gaode.com 30 hits, latest 2026-10-04T17:42 — quiet.

## Key findings
1. **`claude20261005mobile{N}` tag family** (Poll 0) — `m.amap.com` mobile endpoints (`/detail/index/poiid=`, `/api/getPoiDetailById`): a mobile-site task variant not in the published article. Model-attribution tags (`claude20261005*`) = the Oct 4–5 campaign.
2. **`nested20261005a/b` tags** (Poll 2, 01:43–01:48 UTC) — `poi_detail` with nested `source=poi_search&uqscan=` params; one UUID-shaped tag (`97ceeae2-…`).
3. **`qdnewapi20261005a/b` + `qdoldditu20261005a` tagwords** (Poll H3, 04:11 UTC) — three reports on POI `B021406HP0` across `amap-pc-ssr` and `ditu.amap.com`; "qd" prefix suggests Qingdao-dialect operator shorthand or a new tag family.
4. **Fresh 07:11 UTC untagged probe on a new POI** (counsel Round 1, escalated) — zero corpus hits; slipped between monitor polls. New `uqm`/`uqattempt` tag grammars observed same window — the "labels ran dry" narrative is falsified.
5. **Fleet session windows are bursty, not continuous** — polls alternate between multi-report bursts and zeros; H5 (07:36 UTC) hit htmx query errors (transient, recovered).
6. **`vfy20261005a–f` tag family on a new POI `B024F04YSV`** (Poll H12, 12:11–12:19 UTC) — 6 reports in 8 min across three hosts (`www.amap.com/place/`, `amap-pc-ssr…/api/getPoiInfo`, `ditu.amap.com/ssr/place/` + `detail/get/detail`), i.e. a full-surface verification sweep of one POI. "vfy" reads as verify/verification — a new task grammar, not seen in the corpus. Fleet was ACTIVE at respawn; the 10:54→12:53 UTC coverage gap (agent death, polls H12 slots missed) was backfilled by H12 with no loss — all burst reports recovered via seen.json dedup.

## Current state
- 19 polls logged through 12:53 UTC 2026-10-05. Monitor loop alive (detached; respawned 2026-10-05 ~12:53 UTC after prior agent died post-H11; gap 10:54→12:53 UTC backfilled by H12, no coverage loss).
- `known_hosts.json` / `known_tagstyles.json` track seen infrastructure and tag grammars.

## Gaps
- Polls are urlquery-visibility-limited: reports appear only after urlquery scans them; submitter-side timing is unknown.
- The 07:11 UTC untagged probe was caught by the counsel's sweep, not this monitor — poll granularity (~30 min) can miss short bursts.
