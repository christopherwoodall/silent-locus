# PROVENANCE — LANE L: Power BI domain-fronting documentation

Date: 2026-09-27/28 (UTC: 2026-09-28)
Lane: L — Power BI domain-fronting documentation
Read-only: yes. No writes to any source. Agents/infrastructure only —
no operator identity, registrant details, or person-focused attribution.
Credentials: never reproduced. The app.powerbi.com embed token (`r=` JWT-ish
value) found in the corpus is WITHHELD everywhere in this lane's outputs;
only the host + pageName are cited.

## Sources

1. **thecolony.ai incident wiki** (third-party investigator prose, second-hand)
   - File: `data/2026-09-04-thecolony-ai/raw/wiki_incident_page.html` (captured 2026-09-27,
     Lane I; SHA-256 in `data/2026-09-04-thecolony-ai/raw/manifest.json`)
   - Page: https://thecolony.ai/wiki/openai-escapee-agent-incident-2026
   - Section 11 "How containment failed — egress-bypass techniques", line 805
     (SNI-allowlist bypass bullet); Section 8, line 742 (OECD data bullet).
   - Verbatim copies: `technique-verbatim.md` (this dir).
   - Status: investigator claims cited as reported; NOT independently verified
     by us (we did not replay the technique; the wiki itself says it was not
     replayed by the investigators either).

2. **collusion-wiki corpus** (agent-authored records — first-hand agent text)
   - Files: `data/2026-05-17-collusion-wiki/raw/records.jsonl` (41 powerbi hits),
     `data/2026-05-17-collusion-wiki/raw/revisions.jsonl` (135 hit revisions),
     `data/2026-05-17-collusion-wiki/raw/links.jsonl` (1 app.powerbi.com link),
     `data/aggregates/2026-09-29-overlap-analysis/raw/wiki_ioc_pivots.jsonl` (3 IOC rows: full URL, `app.powerbi.com`,
     `powerbi.com` — 5 agents, 5 occurrences, dse wiki only).
   - These are agent-written wiki pages describing the bypass in first person
     ("I obtained real querydata via blob-SNI bypass"), i.e. agent tool-use
     evidence, dated 2026-06-20/21 (request-log timestamps on revisions;
     source_date_literal on records).

3. **Elastic `collusion-wiki` index** (read-only query, for cross-check)
   - Host: agent-apocalypse-f1f7ba.es.us-east-1.aws.elastic.cloud
   - `multi_match "powerbi"` over all fields: **40 docs, all in index
     `collusion-wiki`** (sampled ids `wiki:record:<sha>` — record docs).
   - Consistent with the 41 local records.jsonl hits (the 1-doc delta is the
     `powerbi` vs `power bi` tokenization difference, not a corpus gap).

## Pattern sweep performed (2026-09-27)

- `grep -ri "power.?bi"` over `data/` (all corpora): hits only in
  `data/2026-05-17-collusion-wiki/raw/{links,records,revisions}.jsonl`,
  `data/aggregates/2026-09-29-overlap-analysis/raw/wiki_ioc_pivots.jsonl`, `data/2026-09-04-thecolony-ai/raw/wiki_incident_page.html`,
  and the one-line PROVENANCE.md mention (technique already catalogued).
- Diffend sweep JSONL (`data/2026-05-11-osv/events.jsonl`,
  `data/2025-03-04-rubygems-goimport-campaign/raw/gem-pins-diffend.txt`, `data/2026-09-05-fieldnotes-gem/raw/diffend-page.html`):
  zero powerbi hits (go-import campaign payloads are RubyGems metadata).
- No `app.powerbi.com` outside the single agent-embedded URL above.

## Hit counts (this lane, before exact-dedup)

- 179 hits total in `hits.jsonl`:
  - 2 investigator wiki passages (thecolony.ai)
  - 41 agent wiki records (collusion-wiki records.jsonl)
  - 135 agent wiki revision excerpts (collusion-wiki revisions.jsonl)
  - 1 agent-embedded app.powerbi.com link (collusion-wiki links.jsonl)
- Collapse rule: only exact duplicates collapsed (none found across files).
- IOC pivot rows: 3 (`url`, `domain`, `reg_domain`), wiki `dse`, agents
  [MayTwoOECDObserverX, OAIFeb28Equity2, OECDEquityJun06Agent,
   OpenAIOECDJul23, ResearchAgent], sources
   dse~OAIEquityDec30Raw@11..15.

## Elastic destination

Own index: `powerbi-fronting` under the shared canonical schema
(notes/gems-es-mapping.json), created WITH the event.dataset.keyword
multi-field. Ingest script: `scripts/es_ingest_powerbi.py`.

## Raw layer 2026-09-29

- `hits.jsonl` -> `raw/hits.jsonl` (upstream capture; no script consumers at time of move). Upstream name preserved; raw layer exempt from event schema.

## Schema build 2026-09-29 (worker W5)

- events.jsonl: **180 records** — 179 hits from `raw/hits.jsonl`
  (record_kind `corpus_hit`, sub-kinds in `labels.powerbi.hit_kind`:
  135 agent_wiki_revision, 41 agent_wiki_record, 2 investigator_wiki_passage,
  1 agent_wiki_link) + 1 `artifact_observation` for
  `raw/technique-verbatim.md` (the two verbatim passages).
- fingerprint identity string:
  `powerbi-hit|<hit_kind>|<source_file>|<record_id|rev_id|line|page_key>`;
  verbatim artifact: `powerbi-verbatim|technique-verbatim.md`.
- `@timestamp`: the hit's `timestamp` field parsed to ISO where present
  (`labels.timestamp_source = "labels:powerbi.hit_timestamp"`); the two
  investigator passages carry prose timestamps, so they use the dir date
  2026-06-20T00:00:00Z with `timestamp_source =
  "dir_prefix:investigator_passage_covers_2026-06-20_21"`. Raw timestamp
  prose kept in `labels.powerbi.hit_timestamp_raw`; `url_context` truncated
  to 400 chars in labels (full text remains in raw/hits.jsonl).
- SHA256SUMS regenerated: covers events.jsonl + the 2 raw files. The
  previous SHA256SUMS listed `raw/progress.log`, which does not exist —
  stale entry dropped.
- Verified: all 180 records validate; fingerprint recomputed by hand for
  the verbatim artifact and two sample hits; timestamps spot-checked.

## Rollup decision 2026-09-29 (worker W5)

- No rollup.jsonl: the collection is a pure event stream (179 grep hits +
  1 verbatim artifact). The only natural groupings (per hit_kind counts,
  per wiki page) are mechanical group-bys with no burst/window/actor
  structure in the data — inventing a rollup would add nothing. Per
  Christopher's worker rule, no rollup was built.

## Historical loader relocation (2026-09-30)

Preserved `es_ingest_powerbi.py` at `raw/scripts/legacy/es_ingest_powerbi.py` as a historical, optional Elasticsearch loader; it is not an active collection event builder. Its local path resolution now targets the same collection and repository inputs from the archived location. No source evidence, `events.jsonl`, or `rollup.jsonl` was changed; no network or ES actions were run. The SHA256SUMS entry records the relocated script bytes.
