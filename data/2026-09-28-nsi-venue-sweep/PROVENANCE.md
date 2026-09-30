# PROVENANCE — nsi-venue-sweep (2026-09-28)

National-stats venue pattern sweep: does the swarm drink from other national
statistical institute endpoints beyond the known ones (Vietnam GSO PX-Web,
Iceland PX-Web, UK ONS, US Census/DataUSA)? Triggered by 8 anna.fyi pastes
showing the "Statistical reference 1" thread pulling Bulgaria NSI infostat
table 54.

## Method
1. Corpus domain census: extracted every `https?://` URL from `data/**/*.jsonl`
   and `data/**/*.txt` (679 unique domains), filtered for statistics/NSI
   keywords, then verified each candidate in its source file with context.
2. Read-only live probes (plain HTTPS GET, research UA, no auth, no
   submissions) against candidate API roots to confirm unauthenticated JSON.
3. Web research: documented PX-Web deployments (Statistics Sweden's PX-Web
   software), Bulgaria NSI open-data/Infostat access notes (third-party
   developer docs), UNCTADstat API shape.
4. Negative sweeps: re-grep of the merged domain list for other PX-Web hosts,
   headline economics APIs, and r.jina.ai-laundered inner domains.

## Sources (all inside this repo unless noted)
- `data/2026-05-17-collusion-wiki/raw/{links,records,revisions}.jsonl` — wiki evidence
- `data/2018-05-09-paste-archive-gap/raw/bodies/anna.fyi/*.txt` — the 8 "Statistical reference 1" pastes
- `data/2026-05-12-university-shorteners-events/events.jsonl` — shortener referrer rows
- Live probes: datasets.cbs.nl, unctadstat-api.unctad.org, site-test.nsi.bg, www.nsi.bg (2026-09-28)
- Web: janbrus/pxwebapi-skills PX-Web installation inventory (GitHub); atanasster/electionsbg NSI access notes (GitHub)

## What was NOT done
- No hosted Elastic writes (freeze in effect); no submissions, accounts, or logins.
- No crawler beyond single read-only GETs of public API roots/endpoints already
  named in our corpus or in public developer documentation.

## Output
- `hits.jsonl`: 12 documents, `record_kind=stats_api_target`,
  `event.dataset=nsi-venue-sweep`, canonical schema (notes/gems-es-mapping.json).
  9 positive/corroroboration hits, 3 bounded negatives.
- Built by `build_dataset.py` (deterministic fingerprints).

## Chain of custody
Lane run 2026-09-28 ~15:05-15:25 CDT. All evidence paths are relative to the
repository root. No absolute home-directory paths in any artifact.

## raw/-missing exception 2026-09-29

2026-09-29: no raw/ layer — cross-corpus census: evidence is preserved in sibling
raw/ layers (collusion-wiki raw/, paste-archive-gap raw/bodies/anna.fyi/,
university-shorteners events); the live probes were ephemeral read-only API
checks recorded inline. Verified: no raw/ files ever committed in git history;
no stray evidence files on disk; SHA256SUMS green. Ratified as a canonical-layout
exception.
