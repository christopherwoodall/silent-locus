# INGEST.md — 2026-09-27-gem-public-intel

Ingested into Factum 2026-10-10 (UTC) on branch factum-shaping.
Factum lane: `2026-09-27-gem-public-intel` (lane_2b845315d02c4bfdb69b5014ca86ce41).
Batch: cb9608e4c3b3440eaad125cb92780872.

## Records (22 total, all tagged {"lane": "2026-09-27-gem-public-intel", "basis": "upstream"})

- 11 `intel.report`: one per public source on the GemStuffer campaign
  (Socket, Nightingale/rubyhack.ai, RubyGems blog, GHSA-9j48-x3c3-mrp2,
  The Hacker News, The Register, HivePro TA2026130, vibe-coding-security,
  orca-ai-incident-archive, Picus Security, Sep 11-18 press wave).
- 11 `source`: one per report (web locators; The Register locator is
  "(via advisory citations)" verbatim from the evidence).

Each report carries verbatim `summary` (byte-identical `source.claims`),
`lab` (publisher), `report_date` (only where the evidence gives a clean
YYYY-MM-DD; fuzzy dates stay verbatim in the `source.date` tag), and
`url` (only where the evidence gives a real URL).

No edges created during ingest (separate pass). Author auto-stamped by
Factum (subagent-gem-public-intel-ingest). No blobs: sources are web
locators, no bytes captured in this lane.

The recurring note "no public source mentions the go-import meta-tag
payload layer, the dead-drop chatter, or our specific gem names" is an
inventory-level claim about the whole set; it is preserved in the
PROVENANCE.md, not repeated on every record.

## Dedup

`match --text --mode fuzzy` on all 11 candidate identifiers before submit
(GemStuffer, gemstuffer, Nightingale rubyhack, Socket gemstuffer,
GHSA-9j48-x3c3-mrp2, gem-public-intel, socket.dev/blog/gemstuffer,
orca-ai-incident-archive, vibe-coding-security): zero matches except
`r.jina.ai`, which hit one `infra.proxy_chain` observation in lane
`2018-05-09-paste-archive-gap` (actual proxy usage, different record type
and substance — not a duplicate). Batch-internal dedup: 11 unique source
locators. `seen_before` empty on submit.

## Cleaner — PASS

Checked live records after submit: lane tag on all 22; basis=upstream on
all 22; schema/type consistent (urn:factum:intel:report:1); 11 verbatim
summaries preserved; 11 distinct sources referenced; 11 legacy fingerprints
cover all 11 legacy events; titles from evidence descriptions (not
URL-derived); observed_at 2026-09-27 with time_basis legacy_documented;
no edge records; no manually set factum.* tags.

## Adversarial validator — PASS

- A1 dedup coverage: PASS. r.jina.ai hit is a type/substance mismatch, not a dupe.
- A2 category collision: PASS. intel.report is the registered type for
  public reporting; no behavior/ttp overlap.
- A3 title source: PASS. Titles are verbatim evidence descriptions, not
  derived from URL slugs or page fetches.
- A4 report_date: PASS. Fuzzy dates ("2026-05-13 / 2026-09-12", "~2026-09-15",
  "2026-09", "2026-05", "2026-09-11 (upd. 09-15)") omitted from report_date
  and preserved verbatim in the source.date tag. No invented dates.
- A5 evidence scope: PASS. Summaries are byte-identical publisher claims,
  graded UPSTREAM, not endorsed.
- A6 no edges at ingest: PASS.
- A7 author: PASS. factum.author auto-stamped by Factum from the bundle
  actor; nothing set manually.

## Provenance chain

- Legacy: evidence/remove-2026-09-27-gem-public-intel/ (PROVENANCE.md,
  SHA256SUMS, events.jsonl, raw/gem-public-intel-2026-09-27.md — original
  files unchanged).
- Working copies: this directory (lane documents + raw note).
- Batch export: data/records/cb9608e4c3b3440eaad125cb92780872/
