# Lane R — admin-deletion recurrence check (2026-09-28)

Dataset: `data/admin-deletions/` (hits.jsonl 5,217 records, PROVENANCE.md,
SHA256SUMS, progress.log, per-day-stats.json). ES index `admin-deletions`:
26 per-day summary docs, canonical shared schema, `event.dataset.keyword`
multi-field at creation, zero schema drift.

Source: `data/collusion-wiki/events.jsonl.gz` (19,913 lines), delete events =
`event_type == "delete"`. ES cross-check: index `collusion-wiki`, docs with
`_id` matching `wiki:event:delete:*`.

## Verdict: sweeps do NOT recur before runs — but the July-6 "sweep" is bigger than lane P saw

Lane P found 318 deletes on July 5–6 (~24h before the July-7 wave) and asked
whether admin deletion sweeps recur before other runs. Answer: **negative** —
no pre-run sweeps exist in the other windows. Instead the full scan reveals
lane P's 318 is the tail of a **continuous 4-week admin deletion campaign**:

- **5,217 delete events**, 2026-06-04 → 2026-07-14, all actor `[Admin1]`
  ip16 `2.202`, wiki `dse`, change_summary "Seite gelöscht.", time_grade
  `reqlog`. 26 active days. 0 exact-duplicate event_ids.
- Campaign proper: **5,215 deletes, 2026-06-18 18:21Z → 2026-07-14 13:56Z**
  (27 days). It starts ON the June-18 run day itself (25 deletes 18:21–18:29Z,
  while the federal-data run was still writing pages) and continues a full week
  AFTER the July-7 wave. The July 5–6 sweep (318) is mid-campaign hygiene, not
  a pre-run signature; 522 more deletes ran DURING the July-7 wave itself.
- Day-by-day family progression reads as systematic venue clearing, cohort by
  cohort: 06-19 Agent/OAI mixes (317), 06-23 Z/ZZ pages (602), 06-24 AgentYahoo
  (267), 06-25 AgentClark (179), 06-26 AgentData/AgentCook (382), 06-28/29 OECD
  (146/88), 06-30 Open/OAI/IHME mixes (440), 07-01..07-05 LoopNextWord sweep
  (248/88/71/59/239), 07-06 AgentMass (79), 07-07 Open/Data/Sector (522),
  07-08 CashierCoord (230), 07-12 CashierCoord/AgentOur (232), 07-13 OECD/AgentCook
  (512), 07-14 AgentOur/AgentTest (149). Admin works afternoon/evening UTC
  sessions of ~2–4h, several per heavy day.

## Null reads (the requested windows — recorded, not filled)

- **2026-05-27..28** (pre-May-29 IHME blitz): **0 deletes** in JSONL and ES.
  (ES: 3,251 docs scanned 2026-05-21..06-01 — all non-delete staging events.)
- **2026-06-15..16** (pre-June-18 run): **0 deletes** in JSONL and ES.
  (ES: 8,611 docs on 06-16, 513 on 06-11..06-16 — no delete `_id`s.)
- **Baseline 2026-06-01..07** (no known run): **2 deletes**, both 2026-06-04
  10:53–10:54Z (`TestFoobaAgent`, `TestAgentXX`) — test-page cleanup, not a sweep.
- Whole pre-campaign span 2026-03-01..2026-06-17: only those 2 June-4 deletes
  (17,772 ES docs scanned). The campaign has a hard start on 2026-06-18.

## Staging-modality table (completed)

| Run | Pre-run window (~48h) | Admin deletions before it? | What was actually there |
|---|---|---|---|
| May 12 gem burst | May 10–11 | **No** (0 events, lane P) | Registry pre-publishing + sandbox probes |
| May 29 IHME blitz | May 27–28 | **No** (0 deletes this lane) | cors.bwa.workers.dev probe + rmn.re epoch marker |
| June 18 federal-data | June 15–16 | **No** (0 deletes this lane) | Iowa comms wave + DemoWiki→dse bridge |
| July 7 XSS/SSTI | July 5–6 | **318 deletes — but NOT a pre-run sweep**: mid-campaign hygiene of a 27-day rolling campaign that started June 18 and ran a week past the wave | Lane P's null reads (no writes/probes anywhere) |

## Theory-of-mind note

The admin is not staging for runs; the admin is **losing a 4-week war of
attrition against agent page spam** and never catching up. Deletions start the
same evening the June-18 run writes (18:21Z vs 18:11Z creations — the admin is
watching the venue live), then grind through page families for a month. The
"venue gets touched two days early" staging frame from lane P still holds for
agent-side signals (probes, bridges, comms), but the July 5–6 cleanup must not
be filed as a staging modality — it's the venue admin's standing operation,
visible in the record as a multi-week campaign with daily session structure.
Detection consequence: a delete burst on the venue is a *campaign-in-progress*
marker, not a run-prediction signal; the reliable early-warning remains
agent-side venue state changes (new bridges, comms waves, probes).
