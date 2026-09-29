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
   - File: `data/thecolony-ai/wiki_incident_page.html` (captured 2026-09-27,
     Lane I; SHA-256 in `data/thecolony-ai/manifest.json`)
   - Page: https://thecolony.ai/wiki/openai-escapee-agent-incident-2026
   - Section 11 "How containment failed — egress-bypass techniques", line 805
     (SNI-allowlist bypass bullet); Section 8, line 742 (OECD data bullet).
   - Verbatim copies: `technique-verbatim.md` (this dir).
   - Status: investigator claims cited as reported; NOT independently verified
     by us (we did not replay the technique; the wiki itself says it was not
     replayed by the investigators either).

2. **collusion-wiki corpus** (agent-authored records — first-hand agent text)
   - Files: `data/collusion-wiki/records.jsonl` (41 powerbi hits),
     `data/collusion-wiki/revisions.jsonl` (135 hit revisions),
     `data/collusion-wiki/links.jsonl` (1 app.powerbi.com link),
     `data/wiki_ioc_pivots.jsonl` (3 IOC rows: full URL, `app.powerbi.com`,
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
  `data/collusion-wiki/{links,records,revisions}.jsonl`,
  `data/wiki_ioc_pivots.jsonl`, `data/thecolony-ai/wiki_incident_page.html`,
  and the one-line PROVENANCE.md mention (technique already catalogued).
- Diffend sweep JSONLs (`data/osv/diffend_sweep_results*.jsonl`,
  `data/gem-pins-diffend.txt`, `data/fieldnotes-gem/diffend-page.html`):
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
