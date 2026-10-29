# Ingest notes — 2026-09-09-pixelleak-glow-labs

Ingested 2026-10-10 (UTC) into Factum. Batch `591f291a5d2743d6a126b4e425ed4df2`
(14 records). Builder: `build_factum_bundle.py` (this directory).
Actor: `agent:lane-ingest-2026-09-09-pixelleak-glow-labs`.
Idempotency key: `lane-ingest-2026-09-09-pixelleak-glow-labs-v1`.

## Pre-ingest dedup

`match --text "<term>" --mode fuzzy` against the corpus for pixelleak,
gitshot, _gitshot, glow.io — all returned zero matches. No overlap with
existing Factum records. In-batch dedup by primary key field passed.

## Record mapping (10 legacy events -> 14 records)

| Legacy event | Factum record |
|---|---|
| report_capture (confirmed) | observation `web.capture` (ref cap) |
| disclosure_outreach | event `incident.reported` (ref ev2), occurred 2026-09-09 (basis source_text) |
| technique | observation `infra.dead_drop` (ref dd): service github.com, endpoint_kind other, markers [_gitshot] |
| tooling | observation `infra.package` (ref pkg, name gitshot) + observation `infra.ioc` (ref ioc, term _gitshot, category marker, status active) |
| skill_propagation | event `incident.reported` (ref ev5), occurred raw "early July" (basis source_text) |
| victim_observation (manufacturer) | event `incident.reported` (ref ev6), basis unknown |
| victim_observation (100+ accounts) | event `incident.reported` (ref ev7), basis unknown |
| scale_figures | claim `reported_scale`, basis UPSTREAM, subject @report (ref cl8) |
| lab_repro | event `incident.reported` (ref ev9), basis unknown |
| remediation_guidance | claim `remediation_guidance`, basis UPSTREAM, subject @report (ref cl10) |

Plus provenance spine: 1 `source` (the glow.io URL) + 1 `dataset.snapshot`
(legacy events.jsonl, sha256-verified, row_count 10) + 1 `intel.report`
(the vendor report itself).

All events cite the intel.report observation. No edges created during ingest.

## Decisions and corrections

- **Descriptions byte-identical** to legacy events.jsonl (verified
  programmatically). Legacy record_kinds preserved in
  `tags.legacy_record_kind`.
- **Report quotes restored in full from raw/pixelleak-blog.html.** The legacy
  events.jsonl payloads were truncated mid-sentence (e.g. tooling ends "O",
  lab_repro ends "sweeper"). Full passages sliced from the raw HTML; original
  Unicode punctuation (U+2019, U+2014, curly quotes) preserved. The
  scale_figures and remediation_guidance quotes concatenate multiple verbatim
  passages (each component byte-identical to the extracted source text).
- **Report publication date recovered: 2026-09-29.** The legacy build used the
  fallback sentinel (`timestamp_source=fallback:no_recoverable_date`), but the
  page byline carries `<div class="author-blog-date">September 29, 2026</div>`
  (authors Yoni Gottesman, Noam Kesten) and the HTML head comment reads
  `Last Published: Tue Sep 29 2026 17:03:52 GMT+0000`. Recorded as
  `report_date` on the intel.report with this provenance note.
- **No invented timestamps/URLs/IDs.** Undated events use occurred basis
  `unknown`; the skill-propagation date uses `raw: "early July"` (basis
  source_text) since the schema requires full-date format for on_date.
- **Vendor caveat kept:** Glow Labs sells endpoint-AI runtime protection; the
  13,000+/300+/900+ figures and the Claude Code Opus 5 lab repro are
  vendor-reported, not independently verified. Claims graded UPSTREAM.
- **Artifact retention:** raw bytes (blog HTML + 2 marketing PNGs) moved to
  `data/lanes/2026-09-09-pixelleak-glow-labs/raw/` (git-retained, as before).
  No bytes attached via Factum files[] — no duplication into data/blobs.
- Scope is agents and agent infrastructure. No human/operator identity pursued.

## Files in this directory

- `events.jsonl` — legacy claim-level extraction (10 events), moved as-is.
- `legacy-PROVENANCE.md` — original provenance doc (renamed to avoid clobbering
  the lane stub).
- `SHA256SUMS` — original checksums, moved as-is.
- `raw/` — pixelleak-blog.html + 2 architecture PNGs.
- `build_pixelleak.py` — original single-collection build script.
- `build_factum_bundle.py` — the Factum bundle builder used for this ingest.
