# PROVENANCE — 2026-10-05-thecolony-ai ingest (Lane 3)

Genuinely-new agent records for the K4be/linuxiarz paste-corpus deep dive,
extracted from the third-party read-only investigation corpus
`joshuadavid/wikiagentswarminvestigation` (public GitHub; local shallow
clone at
`data/2026-09-28-chinese-amap-fleet/personas/pastebin-plunderer/raw/deep-dive/lane3-colony-bullfincher/ref/run1`,
cloned 2026-10-05). Retrieval method: local file read of the clone —
no live fetching of paste sites, thecolony.ai, or bullfincher.io.

## Records (20)

| # | host | paste id | date (UTC) | what |
|---|---|---|---|---|
| 1–17 | paste.linuxiarz.pl | 08d6473d, 0977e8cb, 0fee83f5, 115ae365, 169683a1, 25c81b19, 3bd538a7, 48d18719, 546740ba, 5a768d76, 77280fdf, 8cfcafeb, bae744b9, cb7def97, e0fde17d, e5410e8e, ebcced74 | 2026-09-04 (thread-analysis dating; site timestamps null, wayback rows) | Perceptual Zephyr recruitment drop: `Re: … — AI agent message board` replies inviting agents to https://thecolony.ai (one links thecolony.ai/post/6165cd4b-9d98-4f56-bca2-d7567a87e767). Post-disclosure, investigator-adjacent — NOT swarm coordination. |
| 18–20 | pastebin.k4be.pl | 5329a841, bd44d381, 680ec235 | 2026-02-26 14:49:24–14:52:19 | Humana 10-K stock-return cluster via `bullfincher.io/sec-proxy?url=…hum-20151231x10k.htm` — earliest proxy gadget in the corpus. |

## Verification / cleaning

- Body bytes verified: recomputed sha256 matches the source row's
  `body_sha256` for all 19 rows that carry one (assertion in
  `build_ingest.py`; build fails otherwise).
- 1 row (`paste-linuxiarz/08d6473d`) has no body in the source export
  (body_len 0) — ingested as metadata-only, noted in its authorship
  annotation.
- No payload execution; bodies stored byte-exact. Unicode/HTML entities
  in source bodies (`\xa0`, `&amp;`) preserved as-is.
- Timestamps: k4be rows carry `api_paste_created_field` (confirmed).
  Linuxiarz rows are wayback-derived (time/write_date null); dated
  2026-09-04 via the run-1 thread analysis (`wb_timestamp` cluster
  17:38–18:14 UTC); `labels.timestamp_source` records the weaker dating.

## Annotations (keep-all + annotate)

- Every event carries `labels.external_overlap` =
  `joshuadavid/wikiagentswarminvestigation agent-logs/…/revisions.jsonl`
  and an `labels.authorship_note`.
- Authorship: Perceptual Zephyr self-identifies as "Solar Pro 4 on
  Hermes Agent by Nous Research" — claim unverified, noted per record.
  Humana cluster: run-1 verdict=swarm, single-actor-possible caveat.
- **Deliberately excluded**: k4be `6b4db783` (CentaurAgent recruitment
  paste, 2026-09-05) — byte-identical (sha256
  `901eb93b9f9270ef9767802ef33754683e6c1adead74482a297922cbcbf27127`)
  to anna.fyi `eba4cc0e` already in
  `data/2018-05-09-paste-archive-gap/raw/bodies/anna.fyi/`. Cross-post,
  not new.
- Related records already in our corpora (NOT duplicated here):
  `data/2018-05-09-paste-archive-gap` (CentaurAgent anna.fyi paste),
  `data/2026-03-07-march7-rce-modality` (ColonistOne thecolony.ai
  profile), `data/2026-09-05-termina-digital` (swarm catalog mentions
  of bullfincher).

## Files

- `raw/rows/<host>~<id>.json` — full source row (audit copy)
- `raw/bodies/<host>_<id>.txt` — body bytes
- `events.jsonl` — 20 canonical records (`record_kind: relay_paste`)
- `rollup.jsonl` — 2 day-bursts (2026-02-26 Humana cluster, 2026-09-04 Zephyr drop)
- `SHA256SUMS` — over events.jsonl, rollup.jsonl, raw/**

Build: `../2026-09-28-chinese-amap-fleet/personas/pastebin-plunderer/raw/deep-dive/lane3-colony-bullfincher/build_ingest.py`
Lane notes: `.../raw/deep-dive/lane3-colony-bullfincher/{THECOLONY,BULLFINCHER,STATUS}.md`
No commits, no pushes, no Elastic writes (write freeze).
