# AIID full-site — Factum ingest report (incidents + behaviors + claims)

Executor: Factum ingest worker (aiid-full-site lane). Scope: incidents,
behaviors, and claims ONLY. IOC records are a separate later batch and were
NOT ingested here. Nothing in this section was committed or pushed; that is
the coordinator's call.

## Reconciled counts

- Snapshot (AIID weekly snapshot 2026-10-26 10:15): 1,777 incidents.
- Ingested in this batch: 1,775 incidents.
- Excluded overlaps (NOT ingested, no records created): 2 — see below.
- Post-snapshot scope gap (OUT of scope, unknown IDs, never fetched): 5.
- HTTP-404 report pages (fetched lane gap, incidents still ingested): 5.
- Extraction files used: 889 in `extracted/e1-1-900/` + 886 in
  `extracted/e2-901-1788/` = 1,775 JSON files. (Directory listings show 890
  and 887 entries because each directory also holds a `SUMMARY.md`.)

## Batch

- Batch id: `fc09b8bfbd7b4d719e070fed0d5c4d49`
- Batch path: `data/records/fc09b8bfbd7b4d719e070fed0d5c4d49/`
  (`records.jsonl` + `manifest.json`; manifest record count 5,379 and
  `records_sha256` recomputed locally — match confirmed).
- `records.jsonl` size: 5,558,810 bytes.
- Actor: `agent:aiid-full-site-factum-ingest`.
  Idempotency key: `aiid-full-site-ingest-v1`.
- Lane object: `lane_ad9dd8e545bc47bf8007615750bff4ff`, created 2026-10-30
  at `data/lanes/2026-10-30-aiid-full-site-50bff4ff/lane.json`
  (validated: id shape, tags, docs_path all correct). Its `docs_path` tag
  points at the existing evidence dir `data/lanes/aiid-full-site/`. The
  evidence dir was NOT moved, renamed, or deleted, and no `lane.json` was
  placed inside it — the lane object lives in its own dated directory and
  links to the evidence dir via `docs_path`, per the brief's adaptation.
- Corpus before: 208,745 records (129 lanes, 0 pending, index not stale).
- Corpus after: 214,124 records. Delta: +5,379 exactly.

## Record total and breakdown by kind

Total: 5,379 records.

- Sources: 1,775 — one per incident, locator
  `https://incidentdatabase.ai/cite/<id>`, source_type `aiid-cite`,
  platform `AI Incident Database`, title verbatim from extraction.
- Observations: 1,829, all with `tags.lane = aiid-full-site` and
  `tags.grade = SECONDARY`:
  - `intel.report`: 1,775 — one per incident. Summary = the incident's
    extracted behavior texts joined verbatim. `observed_at` = the AIID
    incident date, `time_basis = source_metadata`. `cached_path` points at
    the fetched incident page
    (`data/lanes/aiid-full-site/raw/fetch/<lane>/incident-<id>.html`).
  - `intel.behavior`: 1 — incident 1395, category
    `proxy-network-fraudulent-accounts`, description verbatim from
    extraction. This is the ONLY extracted behavior carrying an established
    slug.
  - `intel.ttp`: 53 — one per extracted TTP entry, across 42 incidents,
    18 distinct slugs, all present in `docs/taxonomy/ttp-taxonomy.md` and
    `docs/taxonomy/behavior-categories.md`. Each TTP record's description
    states only the slug-to-incident linkage and that the mechanism
    description is not in the extraction; no mechanism text was invented.
- Claims: 1,775 — one per incident, basis `UPSTREAM`, property
  `aiid_incident`, value = the AIID cite URL. Subject = the incident's
  observation, cites = that same observation only. Claims never cite
  source-kind records (schema forbids it); the source link lives in
  `observation.body.source`.

Behavior accounting: 2,864 behaviors were extracted in total. 2,863 carry
slug `none-established` and appear ONLY inside their incident observation's
summary text — no behavior/TTP record was created for them and no slug was
invented. The 1 slugged behavior is counted above.

## Overlap handling

Excluded, with pointer (no records created for either):

- Incident 1152 (Replit) — already ingested by the incident-7050 fleet,
  Factum batch `756a273f`, lane `incident-7050-antigravity`.
- Incident 1433 (Antigravity) — same prior ingest, same batch, same lane.

Both were already absent from the extraction set (verified: no
`1152.json` / `1433.json` in either extraction directory, and no
`cite/1152` or `cite/1433` string anywhere in the exported batch).

PARTIAL incidents (mention-level overlap only, no full prior record) were
ingested FULLY, per the reconciled scope: 1424, 1441, 1469, 373, 16, 46,
68, 1178. All 8 cite URLs are present as sources in this batch.

Dedup note: a per-record `factum match` sweep was NOT run (1,775 queries
at ~6 s each, and the novelty lane's method bars that sweep). Dedup rests
on the novelty verdicts' scan (exact cite-URL / report-URL / full-title
grep over exported Factum batches, legacy evidence, all other lanes, and
the URL inventory) plus within-batch cite-URL uniqueness (1,775 distinct
source locators, verified on the exported file).

## Unfetched gaps

Post-snapshot gap (5, OUT of scope): the live site counted 1,782 incidents
on 2026-10-29 against the snapshot's 1,777. The 5 added incidents have
unknown IDs, were never fetched, and are NOT in this batch. A newer
snapshot or fresh site count must name them first.

HTTP-404 report pages (5): the linked report page returned 404 during
fetch, so that report's content is absent from the extraction basis. The
incidents themselves were still ingested from their incident pages and
remaining reports:

- Report 3447 — incident 3.
- Report 2587 — incident 464.
- Report 3205 — incident 530.
- Report 3875 — incident 665.
- Report 3916 — incident 668.

Press-article gap (applies to every record): linked press articles were
NOT fetched. That is why every observation and claim here is graded
SECONDARY / basis UPSTREAM: AIID is a curated database, and nothing in
this batch is an observation of press content.

## Size-rule outcome

Operator rule (2026-10-17): if the exported `records.jsonl` exceeds
~80 MB, records stay local-only and are NOT handed to the coordinator for
commit. This batch's `records.jsonl` is 5,558,810 bytes (~5.3 MB), well
under the threshold, so the size rule is NOT triggered. The batch is
commit-eligible. It was NOT committed or pushed by this executor, per the
brief — commit/push is the coordinator's decision.

## Validation

- Independent re-derivation validator (re-read the extraction JSONs, not
  the builder's structures): PASS — 5,379 records reconcile to 1,775
  incidents; every record carries `tags.lane = aiid-full-site`; every
  behavior text appears verbatim in its observation summary; every claim
  cites an observation only; zero IOC records; zero records for 1152/1433.
- Exported-file check: manifest record count 5,379, manifest record IDs
  exactly equal the `records.jsonl` IDs, SHA-256 match confirmed.
- `factum verify --blobs`: ok = true, verified = true, records = 214,124,
  pending = 0. The corpus-wide missing-artifact list holds 1,737 entries,
  of which 0 belong to this batch (this batch contains 0 artifact records
  and 0 non-empty observation `files` lists); those 1,737 are pre-existing
  local-only artifacts from other lanes.
- No submitter, editor, or author personal name was added by this executor.
  Incident titles and behavior texts are preserved verbatim from extraction;
  some AIID titles themselves name public figures as AIID titles them.
  Adversarial correction: the blanket reading is false for behavior texts —
  two behavior texts retain subject names that are not title words
  (incident 901, a first name of a harmed party; incident 1512, a full
  subject name), so behavior texts are not proven name-free. Record identifiers
  are AIID incident IDs and cite URLs only. No signed values, tokens, or
  full query strings appear in any record.

## IOC batch (infra.ioc records)

Executor: Factum IOC-record ingest worker (aiid-full-site lane). Scope:
IOC records ONLY, under the EXISTING lane aiid-full-site. Nothing in this
section was committed or pushed; that is the coordinator's call.

### Batch

- Batch id: `32bb59c709f6423a8e043c640f5b80a3`
- Batch path: `data/records/32bb59c709f6423a8e043c640f5b80a3/`
  (`records.jsonl` + `manifest.json`; manifest record count 10,595 and
  `records_sha256` recomputed locally — match confirmed:
  `e51fe30b68bbaf54622a2487a574e98ed60e5d4454cecdd1cafc068cb98a1282`).
- `records.jsonl` size: 10,502,848 bytes (~10.0 MB).
- Actor: `agent:aiid-full-site-ioc-ingest`.
  Idempotency key: `aiid-full-site-ioc-ingest-v1`.
- Lane: the EXISTING lane object
  `lane_ad9dd8e545bc47bf8007615750bff4ff` at
  `data/lanes/2026-10-30-aiid-full-site-50bff4ff/lane.json`
  (re-validated through `lane show` before submission: id shape, tags,
  docs_path all correct). The lane object was NOT edited and no new lane
  was created. Its scope tag still reads "IOCs are a separate batch" —
  this batch is that separate batch.
- Corpus before: 214,124 records (0 pending).
- Corpus after: 224,719 records. Delta: +10,595 exactly.
- Builder script: `reports/aiid-full-site/build-ioc-bundle.py`.
  Submitted bundle: `reports/aiid-full-site/ioc-bundle.json` (8,447,519
  bytes, 10,595 records: 1 source + 10,594 observations).
- Every mutating Factum command used `--lock-timeout 5400` before the
  subcommand. Each one took minutes on this corpus (add ~8 min, export
  ~10 min, verify ~6 min) because every one rebuilds the ~1 GB
  SQLite/FTS projection. That is normal here, not a hang.

### Record total and breakdown by kind

Total: 10,595 records.

- Sources: 1 — the AI Incident Database itself, locator
  `https://incidentdatabase.ai/`, source_type `aiid-full-site`. Every
  observation cites it. No per-IOC source records were created; the
  per-IOC incident and report provenance lives in each observation's
  provenance string.
- Observations: 10,594, all `infra.ioc`
  (`urn:factum:infra:ioc:1`), all with `tags.lane = aiid-full-site` and
  `tags.grade = SECONDARY`:
  - url: 7,955
  - domain: 2,147
  - hash: 326
  - file_path: 68
  - ip: 56
  - model: 23
  - model_or_tool: 14
  - tool: 5

Count note: the brief's "587 + full_set" wording does NOT mean 11,181
records. The ranked set (587 entries) is a SUBSET of the full set
(10,594 distinct kind+value pairs). Ranked values number 577 distinct
values because 10 values appear under 2 kinds (for example ChatGPT as
both `model` and `model_or_tool`). Ingested total is 10,594 IOC
observations. The 587 ranked entries are flagged in their records with
`tags.ranked_agent_relevant = true` and their `rank_reason` in the
provenance string; all other observations carry
`tags.ranked_agent_relevant = false`.

### Field mapping

- `term`: the iocs.json value, verbatim. No value was changed, cut, or
  redacted.
- `category`: the iocs.json kind, verbatim (url, domain, hash,
  file_path, ip, model, model_or_tool, tool). `tags.kind` duplicates it.
- `provenance`: "AIID full-site snapshot 2026-10-26 10:15; AIID incident
  IDs: <full list>; AIID report pages: <full URLs,
  https://incidentdatabase.ai/reports/<id> each>." Ranked entries add
  their rank_reason. Low-confidence entries add a low-confidence flag
  note. Provenance was verified exactly (see Validation).
- `status`: high -> `active` (6), medium -> `active` (8,247), low ->
  `candidate` (2,341). The exact confidence is always preserved in
  `tags.confidence` (high 6, medium 8,247, low 2,341), so no
  low-confidence IOC was upgraded: low stays `candidate` +
  confidence `low`. Status totals: active 8,253, candidate 2,341.
- `observed_at`: `2026-10-26T10:15:00Z` for every observation, with
  `time_basis = source_metadata`. This is the AIID snapshot stamp. The
  source stamp carries no timezone; the `Z` rendering exists only to
  satisfy the date-time format, and it is noted here rather than hidden.
  Adversarial note: the `Z` still asserts UTC, and the `:00` seconds are
  padding — the stamp gives hour and minute only. Treat the value as a
  snapshot label, not a precise UTC instant.
  One snapshot time is used because each IOC aggregates many incidents
  with different dates — no single incident date applies.
- All 74 distinct URLs that carry a query string use the `?params=name1,name2`
  form only, with two narrow verbatim exceptions noted in IOC-REPORT.md:
  one URL keeps `=` in a path segment, and one `?params=` entry carries a
  path-like value, not a parameter name (incident 1162). No query value, token,
  or signed value is carried. URL
  path-embedded redirect encodings were kept verbatim under the
  never-redact rule; they are public redirect paths, not credentials.

### Dedup: 0 skipped

Method: direct scan of `data/records/` (214,124 records at scan time),
not per-record `factum match` calls. Three passes: (1) every record
whose line mentions incidentdatabase.ai or aiid, checked for a ranked
term; (2) every infra.ioc record in the corpus (41,593), checked for a
ranked term whatever its provenance; (3) every record mentioning the
spelled-out "AI Incident Database" plus a ranked term. Same term + same
AIID provenance would have meant a skip. Result: 0 skips.

Near-hits reviewed and NOT skipped, with reasons:

- 3 existing infra.ioc records share a ranked term but carry NON-AIID
  provenance, so under the brief's rule they are new sightings, not
  dupes, and the AIID sightings were ingested: `github.com` (lane
  `2026-10-11-hf-traj-hermes`, batch `307d9654e63b49368288b4bd3eb6697c`,
  HF-traces aggregation) and `twitter.com` (same lane and batch), and
  `GPT-4o` (lane `2026-10-11-openai-blog-intel`, batch
  `8f3ed80b8fbb415a8fe399d6fb836d75`, OpenAI system cards).
- 1 same-term non-IOC record: `Claude Code` appears in an
  `intel.behavior` record (`observation_458b6f695b2a4662b05a0424accb920b`,
  lane `incident-7050-antigravity`, batch `756a273f21064593a4bc4ece94f647bf`,
  provenance "AIID incident 1424"). That is a behavior record, not an
  IOC sighting, and it does not cover this batch's 23-incident
  `Claude Code` (tool) aggregation. It is logged here, not treated as a
  skip.
- The prior incident batch in this lane contains 0 IOC records, so no
  overlap could come from it.

### Size-rule outcome

Operator rule (2026-10-17): if the exported `records.jsonl` exceeds
~80 MB, records stay local-only and are NOT handed to the coordinator for
commit. This batch's `records.jsonl` is 10,502,848 bytes (~10.0 MB),
well under the threshold, so the size rule is NOT triggered. The batch
is commit-eligible. It was NOT committed or pushed by this executor,
per the brief — commit/push is the coordinator's decision.

### Validation

- Independent re-derivation validator (re-read iocs.json, not the
  builder's structures): PASS — 0 mismatches across all 10,594
  observations. Every term, category, confidence tag, status mapping,
  ranked flag, and rank_reason matches iocs.json; every provenance
  string's incident-ID list and report-URL list matches iocs.json
  exactly; every record carries `tags.lane = aiid-full-site`; every
  observation cites the single shared AIID source record; every
  observation has an empty `files` list.
- Exported-file check: manifest record count 10,595, manifest receipt
  record IDs exactly equal the `records.jsonl` IDs, SHA-256 match
  confirmed, `seen_before` empty (no byte-exact dupes).
- `factum verify --blobs`: ok = true, verified = true, records =
  224,719, pending = 0. The corpus-wide missing-artifact list holds
  1,737 entries — the same pre-existing count as the incident batch
  report — of which 0 belong to this batch (this batch contains 0
  artifact records and 0 non-empty observation `files` lists).
- No personal names were added by this executor. Record identifiers are
  AIID incident IDs and report URLs only. No signed values, tokens, or
  full query strings appear in any record.
- Schema check before submission: `schema assigned observation infra.ioc`
  confirmed `infra.ioc` at `urn:factum:infra:ioc:1`, and the bundle was
  built from the `template --type infra.ioc --bare` scaffold. No type
  name was guessed.

## Coordinator decision O1 (adversarial open fix): ACCEPT with disclosure

The two behavior-text name residues in batch fc09b8bfbd7b4d719e070fed0d5c4d49 (line 2669, incident 901: first name of a harmed party; line 4522, incident 1512: full name of an academic subject) are ACCEPTED as published incident-description text, with this disclosure. Reasons: the names name incident subjects in verbatim AIID description text, not submitter, editor, or author identities, and no identity was pursued to obtain them; the project rule is never to redact evidence, so scrubbing verbatim text would break fidelity; re-ingest would need retraction plus a full re-ingest for 2 lines out of 5,379 records while the same text stays in the preserved raw HTML. The claim in this report is qualified accordingly: no submitter, editor, or author names were added; title and description words are verbatim AIID text.
