# Provenance — rmn-re

Source table for the rmn.re YOURLS shortener; derived collections are
`rmn-re-history` and `rmn-re-linktable`.

## Source
- **Origin:** `https://rmn.re/` — a fully open YOURLS shortener whose public
  index and admin interface expose every link (short slug, full target URL,
  creation date, creator IP, click count) with no authentication.
- **Collection method:** passive, read-only crawl of the public YOURLS index
  pages (`https://rmn.re/admin/`, 51 pages x 15 links, no login). Per the
  embedded `link_table_2026-09-27_manifest.json`: source
  "https://rmn.re/admin/ (public YOURLS index, no auth)", all 51 expected
  pages fetched OK.
- **Crawled:** 2026-09-27 (per filenames and manifest; facts re-verified live
  2026-09-28 ~02:40 UTC per `notes/recon-rmn-re-2026-09-27.md`: 764 links,
  84,022 clicks at crawl time).
- **Policy:** passive recon only — no logins, no brute-forcing, no
  short-link mass resolution.

## Files
- `link_table_2026-09-27.jsonl` — the 764-link table as crawled, one record
  per link: `slug`, `target`, `created` (raw non-ISO string as displayed),
  `ip` (creator IP), `clicks`.
- `link_table_decoded_2026-09-27.json` — decoded/normalized form of the same
  table.
- `link_table_2026-09-27_manifest.json` — crawl manifest (source URL,
  per-page fetch status, 51/51 pages OK).

## Context
rmn.re is the campaign-relevant open YOURLS instance: its link table holds
campaign-grammar slugs (zz*, 10-digit epoch suffixes, the 192-link
2026-06-17 AIHW Tableau-dashboard burst) alongside agent-board surfaces
(public-board.com, thecolony.ai). Growth curve and per-slug analysis are in
the derived collections' notes.

## Note sources
- `notes/recon-rmn-re-2026-09-27.md` — service status, open-admin exposure,
  campaign-relevant slugs, DNS notes.
- `notes/rmn-re-history-2026-09-27.md` — link-table growth curve from YOURLS
  creation dates (June 2026 burst: +484 slugs).
- `notes/rmn-re-linktable-2026-09-27.md` — link-table structure/derivation.

## Raw layer 2026-09-29

- `link_table_2026-09-27.jsonl` -> `raw/link_table_2026-09-27.jsonl` (upstream capture; scripts consume the decoded JSON instead). Upstream name preserved; raw layer exempt from event schema.
