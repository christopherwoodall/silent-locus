# Findings — openai-agent-traces

## What this lane is

A census of 589,972 mapped Arquivo.pt CDX traces of agent relay traffic.
The traces cover 10 incident slugs. They run from 2026-04-19 to
2026-06-18. The raw file is 893 MB. We did not ingest each trace. We
counted everything by streaming the file and stored per-slug rollups.

## Main finding

Only 2.5% of the corpus is attributed. 14,940 traces carry `zz=oai<digits>`
in the URL. The lane rule attributes these to OpenAI
(eval family deepsearchqa/dsqa_250). All of them are in the doe-crdc
slug. All were captured on 2026-06-17. The other 575,032 traces (97.5%)
are unattributed relay traffic.

## Numbers

- Corpus: 589,972 traces. Zero duplicate trace IDs. Collections: SAWP5
  (589,915), PATCHING2026 (57).
- Status: 200 (264,868), 302 (276,587), 504 (32,350), 500 (12,928).
- Mime: text/html (328,785), application/json (250,163).
- Peak days: 2026-05-06 (293,898), 2026-06-17 (219,144),
  2026-05-07 (36,496), 2026-06-16 (34,312).
- Marker params: zz (69,477 rows), zzbulk (42,677), prepnonce (27,860),
  bulk (2,812).

Per slug:

- doe-crdc: 250,822 traces, 2026-06-15 to 2026-06-18, civilrightsdata.ed.gov,
  mostly application/json. Holds all 14,940 oai-tagged traces.
- maryland-edstats: 293,898 traces (49.8% of corpus), single day
  2026-05-06 (~6h), 93.5% HTTP 302.
- kansas-kansasmemory: 36,496 traces, single day 2026-05-07 (~3h),
  88.7% HTTP 504 (gateway timeout).
- navy-history: 3,782 traces, 2026-04-22 to 2026-05-18, 57.5% HTTP 404.
- bea-api: 2,988 traces, 2026-06-16 to 2026-06-18. 112 rows carry
  epochish zz values (no oai prefix), 2 carry zz=ours.
- lac-collectionsearch: 982 traces, 2026-05-28 to 2026-06-09,
  Canadian LAC hosts.
- nysed-enrollment: 696 traces, 2026-05-16 to 2026-05-20, 10.8% HTTP 403.
- illinois-iquery: 171 traces, 2026-04-19 to 2026-05-01, 68.4% HTTP 503.
- calaccess: 111 traces, single afternoon 2026-05-26.
- omb-max: 26 traces, single morning 2026-05-26, 92% PDF.

## The zz grammar

The `zz` marker is not only `oai<digits>`. Observed forms:

- `oai<digits>` — 14,940 rows (attributed to OpenAI).
- epochish 19-digit values, e.g. `1781656742855462747` — doe-crdc and
  bea-api (110 rows, no oai prefix, unattributed by the lane rule).
- `a`-prefixed epochish, e.g. `a17816992200`.
- `fill<digits>`, e.g. `fill2639`.
- `g10_` patterns, e.g. `g10_2_52_178`.
- plain numerics, e.g. `335104608`, `116160002`.
- literal labels: `prepfaq` (doe-crdc), `ours` (bea-api, 2 rows).

`zzbulk` (42,677 rows) and `prepnonce` (27,860 rows) appear only in
doe-crdc. Their meaning is not established.

## Grades

All per-slug counts, time ranges, status and mime distributions, and zz
value forms are graded OBSERVED. They cite the `dataset.snapshot`
records. The claim is: the captured bytes have these values. The claim
is not: a named agent made these requests.

The burst-geometry reading (single-day/hour concentration is consistent
with automated relay bursts) is graded INFERENCE. Archive crawl
scheduling is an alternative not ruled out.

## Limits

- The mapper only attributes where `zz=oai<digits>` is present. Epochish
  zz values without the prefix stay unattributed. They may or may not
  share an operator.
- `agent_instance` is never attributed. No row-level evidence exists.
- The 893 MB raw file is local-only (git-ignored). Re-running the
  streaming census needs the local checkout.
- The upstream CDX pull (2026-10-01-arquivo-pt) was ingested as its own
  lane. These records describe the derived mapped corpus, not the raw
  CDX rows.
