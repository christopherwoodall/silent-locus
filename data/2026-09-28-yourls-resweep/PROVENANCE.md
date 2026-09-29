# PROVENANCE — 2026-09-28-yourls-resweep dataset

## Scope

Second-pass re-sweep of public university/org URL-shortener stats pages
(2026-09-28, ~20:00 UTC), ~16h after the morning sweeps (batches 1–3,
uoft/t.mdcdev.me passive). Covers: (1) re-probe of every known surface for
new slugs/rows; (2) t.mdcdev.me deep passive enumeration; (3) hunt for NEW
public YOURLS instances (universities first, then org/community); (4) an
addendum fold-in: 15 agent-grammar popcat slugs (`oaicbs220`–`oaicbs227`,
`oaifilt700`–`oaifilt706`) from the nsi-venue-sweep lane (commit b8b2719),
tied to the Statistics Netherlands CBS 83779NED OData task family.

## Method (read-only, passive)

- Direct GETs only to public read endpoints: per-link `+` stats pages,
  `/info` pages (popcat custom shortener), front pages, robots.txt.
- curl with 3s pacing between requests, single retry, browser UA. No
  logins, no form submissions, no API-write endpoints, no link creation
  (t.mdcdev.me open-creation form never exercised), no challenge solving.
- New-slug sources: joshuadavid/wikiagentswarminvestigation
  `agent-logs/shorteners/pages.jsonl` (11 popcat slugs, all probed) and the
  nsi-venue-sweep lane's 15 CBS slugs. No slugs were guessed.
- New-venue hunt: search-engine sweeps (`"Statistics for" YOURLS`,
  `site:edu "Powered by YOURLS"`, `site:t.mdcdev.me`), the investigator's
  shortener corpus (hosts: vanderbi-lt, uoft-me, goto-unm, popcat,
  u-ethz-ch — no new hosts), brausepulver's saturated instance list,
  hagezi blocklist issues. Candidates probed: umsl.edu/go (404 — retired),
  minifyurl.co (empty reply — unreachable).
- uoft.me: one GET confirming the `+` stats login wall still stands
  (passive only). vanderbi.lt: not re-probed (restricted; lane closed
  2026-09-28 with DONE marker).

## Key findings

1. **15 agent-grammar popcat slugs LIVE with click counts** (the tripwire
   firing): `oaicbs220`–`oaicbs227` (51–65 views each) walk the CBS
   83779NED OData discovery surface (MeasureCodes, GeslachtCodes,
   KenmerkenVanPersonenCodes, PeriodenCodes, Dimensions, Properties,
   $metadata, Observations?$top=10); `oaifilt700`–`oaifilt706` (36–39
   views each) run filtered Observations queries ($filter=Geslacht ×4
   identical targets, $filter=KenmerkenVanPersonen, $top=100&$filter,
   $top=5). All created 2026-05-14 — two days after the May-12 gem burst.
   ~700 combined views. Shortener-as-URL-blackboard, same pattern as
   vanderbi.lt.
2. **2 new numeric popcat slugs** (`/1`: 385 views → tenor.com GIF,
   created 2023-02-24; `/2`: 146 views → speedtest.net, created
   2022-08-04). Pre-cohort user content — controls, not swarm.
3. **Known YOURLS surfaces static**: UNM 7t6-o +5 hits (2523→2528, all
   direct — referrer tables byte-identical), discvr +1, urphy21 +2, reso/vbudg/
   ETH/UVM/t.mdcdev.me all unchanged. **Zero new referrer hosts and zero
   changed host counts on every page** — no new proxy-ladder or
   task-family referrers since morning.
4. **t.mdcdev.me deep passive**: no public listing, no sitemap.xml (404),
   robots.txt reveals nothing (standard YOURLS disallows), search index
   carries only the root page. Slug enumeration remains limited to
   previously-known slugs; all three re-probed slugs unchanged, referrers
   self-only, zero swarm markers.
5. **No new YOURLS venues found.** umsl.edu/go 404s (retired);
   minifyurl.co unreachable; hagezi issues surfaced only spam shortener
   domains; no new edu YOURLS in search indexes.

## Contents

- `raw/evidence/` — 43 raw captures (UNM×5, ETH×1, UVM×3, popcat×19,
  t.mdcdev.me×6 incl. frontpage/robots/sitemap, uoft×1, plus fetch/diff/
  build scripts), each with SOURCE/RETRIEVED/HTTP_STATUS header.
- `events.jsonl` — 31 explicit-event docs
  (`yourls_stats_page` observations; shared-schema top-level fields,
  dataset-specific info under `labels`, deterministic `event_id`).
  No referrer-row docs: zero new referrer rows observed anywhere.
- `pattern-sweep.json` — per-file pattern-family hits (proxy-wrapper,
  task-family, agent-grammar). Hits are the already-known UNM/ETH
  referrer rows plus the 15 new CBS slugs — no novel families.
- `fetch_resweep.py`, `diff_resweep.py`, `build_resweep.py` — lane tooling.
- `SHA256SUMS`, `progress.log`.

## Elastic

Disk only. Hosted-Elastic writes are frozen (ELASTIC_WRITE_PAUSE); the
JSONL is staged for the local-push script whenever the pause lifts. Not
ingested anywhere.

## Guards honored

- Read-only throughout; no submissions, uploads, accounts, logins, forms,
  posts, counter increments, or link creation.
- No absolute home-directory paths in docs/logs (project-relative only).
- No credentials touched or reproduced.
- Commit with explicit pathspecs; push to origin/main.

## Schema backfill 2026-09-29

`events.jsonl` was already schema-shaped;
`temp/backfill_w3.py` only added the missing fingerprint and normalized
empty nested dicts in labels.

- record_kind: `yourls_stats_page` (pre-existing, kept verbatim).
- fingerprint: sha256 of `labels.event_id`
  (e.g. `yourls:goto.unm.edu:7t6-o:page:2026-09-28-resweep`).
- event.dataset `yourls-resweep` (registered dataset_override for this
  series) preserved verbatim — NOT renamed to the directory slug.
- @timestamp, event.created, and all other fields preserved verbatim.
- `labels.changed_referrer_host_counts_vs_morning`: empty objects `{}` (all
  31 rows — zero changed referrer counts) normalized to `null` to satisfy
  the flat-labels rule (no data lost; the empty object carried no entries).
