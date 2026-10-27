# Ingest notes: how a Hermes catalog record is shaped

## Terms used here

- **Catalog**: the Hermes Postgres store for observations, claims, findings, tags, and kanban status.
- **Record**: one row in the catalog. Each record has one kind, one actor, and one provenance block.
- **Actor**: who or what made the record. The actor is the lane, the scanner, the operator, or Counsel. The actor is always named.
- **Observation**: one cataloged item. It has tags, a grade, and a kanban status.
- **Source**: the place the evidence came from. A source record holds the locator, the retrieval time, and the retrieval method.
- **Lane tag**: a tag that groups records by work lane. Every record in a lane carries the lane tag.
- **Kanban status**: where the observation sits in review. Values: backlog, triaging, analyzing, review, done, dismissed.

## Which store is the Hermes store

The Hermes store is the Hermes instance Postgres catalog. That is the only store this profile writes to.

Factum is the current silent-locus store. Factum is not the Hermes store. Do not write Hermes records to Factum. Do not copy Factum paths, Factum database files, or Factum store layouts into this profile. This profile describes the Hermes record shape only. Where a Hermes instance also runs a silent-locus store, the two stores stay separate, and any move between them is an explicit, operator-approved export, never a silent copy.

No store path is hardwired in this profile. The instance config names the Postgres store at load time. If the config names no store, ingest stops and asks the operator. Never guess a store path.

## Record shape

Every catalog record carries these fields:

- **id**: a stable, unique id for the record.
- **kind**: the record kind. Examples: observation, claim, finding, source, artifact, decision, edge.
- **actor**: who or what made the record. Examples: collector, linguist, counsel, ledger, operator, or a named scanner. The actor is always named. An anonymous record is rejected.
- **observed_at**: when the observed event happened, where the source states it. Do not invent this value. If the source states no time, leave it empty and note the gap.
- **time_basis**: what the `observed_at` value is based on. Examples: source metadata, retrieval time, catalog receive time. Catalog receive time is not source publication time and is not event time. State which one you used.
- **source**: the source record for the evidence. The source holds the locator (usually a URL), the retrieval time, and the retrieval method. The provenance triple lives here and in the evidence files. See `evidence-capture.md`.
- **body**: the observed content, in the shape the record kind requires. Body fields hold evidence. Body fields are never edited in place. A wrong body is superseded by a new record, never edited.
- **tags**: a map of tags. Tags hold grouping and search metadata only. Tags never hold evidence. Every record in a lane carries the lane tag. See "Tags" below.
- **grade**: the claim grade, where the kind takes one. Values: ungraded, observed, inference, upstream. See `hunt-methodology.md`.
- **kanban status**: the review status, where the kind takes one. Values: backlog, triaging, analyzing, review, done, dismissed. Only the operator or Counsel may move an observation between kanban statuses. Each move records the actor, the from-status, the to-status, and the timestamp in the events log.
- **provenance**: the provenance block. It holds the source locator, the retrieval time, the retrieval method, and the sha256 hash of the captured bytes. The provenance block must match the evidence files. If it does not match, ingest stops.

## Tags

Tags group and find records. Tags never carry evidence.

Required tags on every record:

- **lane**: the work lane the record belongs to. Lane names are lowercase with hyphens, with no date. Example: `webhook-deaddrops`. The lane tag groups records for review and for edge building. A record with no lane tag is invisible to lane-scoped review. Reject it at ingest.
- **grade**: the grade, where the record kind takes one. Duplicated in the grade field for search.

Useful tags, where they apply:

- **docs_path**: the path to the lane document or report that discusses the record, relative to the workspace. This is a navigation aid only. It does not create a graph edge.
- **source_kind**: the kind of source, such as a board, a paste archive, or a tracker, where that helps review.
- **sensitivity**: a note that the evidence holds sensitive values, with the type, never the values. See `evidence-capture.md`.

Do not invent new tag names without a reason. If a new tag is needed, record its meaning in the lane document first, then use it.

## Actors and write rules

Different actors write different records. The split is enforced, not advisory.

- The Collector writes source and artifact records. Content-addressed. No update, no delete.
- The Linguist writes claim records, once. A wrong claim is superseded by a new claim row, never edited.
- Counsel writes decision records. A decision holds the verdict and the mandatory reason. Decisions are not rewritable. A wrong verdict is corrected by a new decision row that references the old one.
- The Ledger writes observation and finding rows, after it validates the Counsel verdict. The Ledger writes no finding without a valid Counsel verdict.
- The operator writes kanban moves, dismissals, and approvals. Approvals are signed rows, made through the approval command or the dashboard, in an authenticated session.

Agents never receive database credentials. Agents propose records through a capability-scoped tool API: propose observation, propose tag, propose claim. Deterministic code validates each proposal (schema check, provenance triple present, hash matches the bytes, every field on the writable-field allowlist) and performs the write. Anything else is rejected and logged.

Platform gap, stated plainly: the ship-gate/ingest validator is a Hermes-platform requirement that this profile assumes but does not provide. No validator code ships in this profile. Record the gap at load time, and do not claim ingest validation exists until the platform provides it.

## Ingest steps

1. Capture the evidence with its provenance triple and hash. See `evidence-capture.md`.
2. Dedup before you submit. Search the catalog for the key term and the key identifiers, by exact match and by near match. If the record already exists, skip it and note the overlap. Dedup inside the batch by key field.
3. Build the record: id, kind, actor, observed_at with time_basis, source, body, tags with the lane tag, grade, kanban status, provenance.
4. Validate: schema check, provenance triple present, hash matches the bytes, lane tag present, actor named, grade present where required.
5. Submit through the ingest path. Never hand-edit catalog rows. Never hand-edit stored evidence.
6. Verify: read the record back, check the hash, check the evidence files, check the lane tag. A record that fails verification is not ingested. Fix the input and re-submit.
7. Record the ingest: run id, counts submitted, counts skipped as overlap, and any failures. The ingest record goes in `workspace/state/`. See `workspace/state/README.md`.

## Corrections

Metadata may be corrected with UPDATE: tags, provenance paths, status fields. Evidence may not. Body fields, record ids, record kinds, and timestamps are never edited in place.

If evidence is wrong, submit a retraction record. A retraction holds the target record id and the reason. The original record stays. The retraction explains what changed. Future queries must respect active retractions.

## What ingest never does

- Never writes without a lane tag.
- Never writes a finding without a Counsel verdict and a reason.
- Never writes evidence bytes into the catalog in place of the evidence files. The files are the evidence. The catalog is the index.
- Never deletes evidence. Never redacts evidence values. See `evidence-capture.md`.
- Never uses a hardwired store path. The instance config names the store.
- Never treats Factum as the Hermes store. Factum is the current silent-locus store. The Hermes store is the Hermes instance Postgres catalog.
