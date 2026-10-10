# INGEST_NOTES — 2026-10-05-thecolony-ai (lane 3: K4be/linuxiarz deep dive)

## Mapping decisions

Legacy `record_kind` -> Factum type, one record per legacy row (22 rows):

| legacy kind | count | Factum mapping |
|---|---|---|
| relay_paste | 20 | `infra.message` observation |
| paste_day_burst | 2 | claim record (basis OBSERVED, subject=@run) |

- Observation mapping (precedes from paste-archive-gap / iowacollab-pastes):
  venue = `paste.linuxiarz.pl` / `pastebin.k4be.pl`; message_id = actual paste
  id (never an internal id); body = verbatim body bytes from raw/bodies;
  author = paste.author_label (k4be rows only; linuxiarz labels empty);
  posted_at = legacy @timestamp (k4be: api_paste_created_field, confirmed;
  linuxiarz: 2026-09-04T00:00:00Z thread-analysis dating, weaker — flagged in
  tags.timestamp_source); provenance = source_url; trust = untrusted-user-content.
- Title lives in tags.paste.title (infra.message has no title field).
  One linuxiarz row (0977e8cb) has title None — tag omitted, not invented.
- 10 empty-body rows ingested metadata-only: body = "" (byte-identical to the
  0-byte source file), tagged body_status metadata-only.
- tags.lane = "thecolony-ai" (date prefix stripped per lane-tag convention).
  Note: the earlier 2026-09-04-thecolony-ai recon lane used the dated tag
  "2026-09-04-thecolony-ai" — zero collision, but the two conventions coexist.
- Claim note = legacy rollup description, byte-identical (validator-checked);
  value.labels verbatim; subject = @run (claims cannot cite source records).
- Run: run_kind=extraction, tool=build_ingest.py (lane3-colony-bullfincher),
  coverage 22/22 complete. Source locator points at the NEW lane path
  data/lanes/2026-10-05-thecolony-ai/events.jsonl (moved, not evidence/).
- No edges at ingest (SKILL.md rule; edge building is a separate pass).
- Authorship note quirk (preserved verbatim): every linuxiarz row's
  authorship_note ends with "[body NOT recovered in source export;
  metadata-only record]" — but 7 of 17 rows DO carry bodies. Lane-level
  annotation, kept as-is; the body_status tag on the 10 empty rows disambiguates.

## Dedup

`match --text <id> --mode fuzzy` for all 20 paste ids: zero pre-submit matches.
`bullfincher.io`: zero. `paste.linuxiarz.pl`: 4 hits from the
2026-05-17-iowacollab-pastes lane (different paste ids df40f1f1, 538faa12,
34cb12da, d379207f — venue overlap only, not dupes). `pastebin.k4be.pl`:
2 anna.fyi venue hits from paste-archive-gap (message text mentions k4be —
not dupes). In-batch message_ids unique. `seen_before` empty on submit.

## Batch

Batch fea95fe1fe4048c9bcba822926807c3f: 20 infra.message + 2 claims + 1 run +
1 source. `verify --blobs` ok (8 missing artifacts belong to a sibling
worker's pending batch, not this one). `verify` ok: 1478 records.

## Cleaner — PASS

20/20 observations tagged lane=thecolony-ai; message_ids unique; no manually
set factum.* tags (factum.author auto-stamped); grade OBSERVED on all; every
body byte-identical to raw/bodies (sha256 + size re-checked); run/source/claims
tagged and subject-resolved.

## Adversarial validator — PASS (one documented caveat)

- A1 type collision (intel.report vs infra.message): no — individual paste
  messages match infra.message; precedents agree.
- A2 term mapping: message_id is the paste's own id within the venue (real
  identifier, not internal).
- A3 timestamps: no invented times; weaker linuxiarz dating flagged.
- A4 verbatim: build-time sha256 assertion + cleaner re-verification.
- A5 empty bodies: explicit metadata-only tags, not dropped.
- A6 dedup: documented above; note "not_found" is scoped to structured records.
- A7 no edges at ingest: confirmed (0 edge records in batch).
- A8 lane tag: "thecolony-ai" has zero prior records; no merge with the
  2026-09-04-thecolony-ai recon lane.
- Caveat: validator was run by the ingesting agent, not an independent agent;
  recommend a red-team re-check if the lane feeds edge-building.

## Root causes found

- Pre-existing: `SHA256SUMS` in the lane pack does not match PROVENANCE.md
  (current sha feff0541934e8fd388aa5f3a77c2b18cef113aab08611cf7fae334cdd7b78c2e
  vs recorded 75a1281e...). The file's own "Round 2 correction" note says it
  was edited (1 -> 10 metadata-only rows) after checksums were recorded;
  mtimes predate this ingest. Left as-is: the correction is self-documented
  in the file; regenerating the manifest would rewrite evidence.
- None in Factum tooling for this lane. One operational note: `lane edit
  --tags` REPLACES the full tag set (scope was silently dropped on first edit
  and re-added). Sibling workers editing lane tags should pass the complete
  intended set.
