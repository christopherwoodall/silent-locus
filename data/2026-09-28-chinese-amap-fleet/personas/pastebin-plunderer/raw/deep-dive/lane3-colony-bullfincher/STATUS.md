# Lane 3 status (2026-10-05)

## Done
- THECOLONY.md: platform verified (36 colonies / 228 authors / 981 posts,
  earliest 2026-04-03); operator Starsol Ltd ×3 sources; .ai/.cc same
  platform; recruitment-surface verdict = pre-existing, NOT swarm C2
  (investigators' hub; recruitment pastes post-disclosure, investigator-
  authored).
- BULLFINCHER.md: site = exec-comp data site (alive); /sec-proxy = open
  ?url= PDF-to-text fetcher (indexed SEC filings); first seen k4be
  2026-02-26 (Humana 10-K) — earliest proxy gadget in corpus; full
  proxy-gadget family table with first-seen dates.
- Local corpus checks: `data/2026-10-01-oai-tag-sweep/events.jsonl` has
  ZERO bullfincher/thecolony mentions; none in 2026-05-26-paste-linuxiarz
  or 2026-05-27-paste-archive (targeted greps).

## Pending (background)
- proc_f8d99ac0b3f2: full-corpus grep bullfincher|thecolony over
  ~/workspace/silent-locus/data/
- proc_6050b1e0eae5: shallow clone joshuadavid/wikiagentswarminvestigation
  → lane3/ref/run1

## On clone landing
1. grep run1 for bullfincher (all mentions beyond Humana paste?)
2. grep run1/scrape/outputs/thecolony.ai/items.jsonl for swarm markers:
   `pad-`, `Iowa`, `clock.wait(`, `zz=`, `oai` → confirm zero/low
3. Extract recruitment paste records: k4be CentaurAgent → thecolony.ai;
   linuxiarz Perceptual Zephyr → thecolony.ai
   (agent-logs/pastebin-k4be/revisions.jsonl,
    agent-logs/paste-linuxiarz/revisions.jsonl)
4. Extract k4be 5329a841 (Humana + bullfincher sec-proxy, 2026-02-26)

## Ingest decision (criteria)
Ingest under data/2026-10-05-thecolony-ai/ ONLY records that are (a)
agent-authored, (b) absent from our corpora, (c) on-lane (k4be/linuxiarz
paste venues or the lane's proxy-gadget question). Expected: the 2–3
recruitment pastes + the Humana bullfincher paste, each with
PROVENANCE.md, external-overlap annotation (joshuadavid corpus),
events.jsonl, rollup.jsonl, SHA256SUMS. Do NOT bulk-ingest the 981
thecolony.ai RSS posts (third-party dataset, not swarm coordination).
No commits, no pushes, no Elastic writes.

## RESULTS (2026-10-05, clone landed)

### Swarm-marker grep: thecolony.ai public posts — CLEAN
`ref/run1/scrape/outputs/thecolony.ai/items.jsonl` (980 rows, third-party
read-only scrape 2026-09-08): `pad-[0-9]`=0, `Iowa`=0, `clock.wait`=0,
`zz=oai`=0, `thecolony.ai/for-agents`=0. No swarm coordination markers in
thecolony.ai's public content. Combined with the census (1611 posts/197
authors in trailing 168h as of 2026-09-20, smirnovegorv/foragents), this
is a live organic agent community, NOT swarm infrastructure.

### Humana/bullfincher cluster: 3 pastes, not 1 (new detail)
k4be rows with bullfincher sec-proxy URL, all 2026-02-26, all
`api_paste_created_field` timestamps, verdict=swarm:
- `5329a841` 14:49:24Z — source paste (900 B): Humana 10-K stock table +
  `https://bullfincher.io/sec-proxy?url=https%3A%2F%2Fwww.sec.gov%2FArchives%2Fedgar%2Fdata%2F49071%2F000004907116000117%2Fhum-20151231x10k.htm`
- `bd44d381` 14:50:18Z — reformatted summary (590 B)
- `680ec235` 14:52:19Z — second summary (330 B)
Three-minute reformulation ladder = single actor polishing an answer, not
multi-agent coordination. Single-actor-possible caveat stands.

### Perceptual Zephyr: 17 rows in export (not 16 pastes)
`agent-logs/paste-linuxiarz/revisions.jsonl`: 17 rows, all
label=`Perceptual Zephyr`, verdict=swarm, titles `Re: <shortid> — AI agent
message board` (8 Iowa-scene shortids + 8 topic tags + 1 untitled).
Wayback rows: time/write_date null; dated 2026-09-04 via thread-analysis
`wb_timestamp` cluster 17:38–18:14 UTC. Example body (169683a1):
"I am another AI agent reading this paste (Perceptual Zephyr, Solar Pro 4
on Hermes Agent by Nous Research)... dedicated message board for AI agents
at https://thecolony.ai ... The Colony thread about agents using wikis and
paste sites: https://thecolony.ai/post/6165cd4b-9d98-4f56-bca2-d7567a87e767".
One row (`08d6473d`) has body_len 0 in the export — metadata-only.

### CentaurAgent: k4be paste is a byte-identical cross-post
k4be `6b4db783` ("Re: Statistical reference -- invitation for agent",
2026-09-05T07:32:11Z) sha256 =
`901eb93b9f9270ef9767802ef33754683e6c1adead74482a297922cbcbf27127`,
identical to anna.fyi `eba4cc0e` already in
`data/2018-05-09-paste-archive-gap`. NOT new; excluded from ingest.

### Own-corpus checks (confirmed)
- `2026-10-01-oai-tag-sweep/events.jsonl`: 0 bullfincher/thecolony hits.
- No `5329a841`, no `zephyr`, no `bullfincher` in our paste datasets
  (2026-05-26-paste-linuxiarz, 2026-05-27-paste-archive,
  2026-05-17-iowacollab-pastes).
- Already in our corpora (NOT re-ingested): CentaurAgent anna.fyi paste
  (2018-05-09-paste-archive-gap), ColonistOne thecolony.ai profile
  (2026-03-07-march7-rce-modality), termina.digital swarm catalog
  bullfincher mentions (2026-09-05-termina-digital).

## Ingest: data/2026-10-05-thecolony-ai/ (20 events, 2 rollups)
- 17 x linuxiarz Perceptual Zephyr recruitment pastes (2026-09-04)
- 3 x k4be Humana bullfincher sec-proxy pastes (2026-02-26)
Files: PROVENANCE.md, events.jsonl, rollup.jsonl, SHA256SUMS,
raw/rows/*.json (audit copies), raw/bodies/*.txt (byte-exact).
All bodies sha-verified against source rows (build asserts; fails
otherwise). No commits, no pushes, no Elastic writes.

## Recruitment-surface verdict (final)
thecolony.ai = real production agent social network run by **Starsol Ltd**
(UK co. 06002018; 3 independent sources), predating the swarm wave by
~5 months. Recruitment pastes are POST-DISCLOSURE and investigator-
authored (CentaurAgent: OpenCode/Muse-Spark harness; Perceptual Zephyr:
Hermes-family "Solar Pro 4" claim). swarm-ai-research independently files
it under "second-order boards" advertised since disclosure. NOT swarm C2 —
the swarm pointed agents at EXISTING infra, coincidentally; the
advertising wave is post-disclosure capitalisation. Zero swarm markers in
its 980 public posts.
