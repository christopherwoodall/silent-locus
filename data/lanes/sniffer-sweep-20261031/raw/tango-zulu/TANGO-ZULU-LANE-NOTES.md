# TANGO-ZULU lane notes (staged only, not ingested, not committed)

Result: honest zero for rogue-agent / swarm use of "tango zulu" in the November 2025 onward window.
No candidate survives hypothesis testing. Default grade SECONDARY applies to all items below;
none is presented as agent behavior.

## Ranked candidates (all adjudicated noise, none NEW as agent evidence)

1. GitHub code, exact "tango-zulu" (17 hits) — hypotheses tested: codename, callsign, tag grammar.
   Adjudication: noise. Spot-checked items are: a local-business directory entry for the
   Port Gamble fair-trade shop of the same name; a Nostr relay census file dated 2026-10-08
   in which "tango" appears only as one word inside longer hyphenated relay path names,
   never as a "tango-zulu" pair; an email-assistant daily-report file dated 2026-03-25 in
   which "tango" appears inside randomly generated phonetic screenshot filenames, including
   one filename containing the pair as part of a longer random sequence; and a test fixture
   in a multi-agent privacy-attack test suite (a string value, not a live agent act).
   None is a self-declared agent callsign, codename, or tag grammar.
   Grade: DISCUSSED at most for the test fixture; otherwise unrelated noise. Novelty: not new agent evidence.
2. GitHub code, "tangozulu" (83 hits) — mostly expired-domain lists and wordlists for the
   same shop domain, plus data-scraper dumps. Noise. Grade: unrelated. Novelty: not new.
3. GitHub code, "tango_zulu" (21 hits) — mostly duplicated test-fixture files for a
   syntax-highlighting library. Noise. Grade: unrelated. Novelty: not new.
4. GitHub code, tokenized "tango+zulu" (135,424 hits) — NATO alphabet tables and
   translations. Not a phrase search; discarded as a counting artifact. Noise.
5. GitHub issues/PRs, hyphen query (103 issues / 121 PRs) — tokenized matches:
   NATO trainers, aviation weather advisories, radio software. Exact forms "tangozulu"
   and "tango_zulu" score 0 issues / 0 PRs. Noise.
6. Hacker News Algolia — phrase query 0 hits; unquoted variants return 6 and 9 hits,
   none containing the literal phrase (token stemming), all pre-window except one
   2025-01-19 hit that also lacks the phrase. Noise.
7. Web search — hits are aviation (AIRMET Tango/Zulu weather products), amateur-radio
   callsigns, a fictional submarine video classified with the code, the fair-trade shop,
   a 2013 role-play document, and a game profile name. None is agent infrastructure.
   One EVE-game killboard entry uses the words as a game ship name; not agent evidence.
   Noise.
8. Paired-phonetic / "T/Z" pattern — not run as a standalone search: "T/Z" is too
   generic (timezones, ratios, file paths) to adjudicate and would flood the lane.
   Paired-phonetic hits found above (relay paths, random filenames) were already tested
   and failed the callsign/codename hypotheses. Open question, see below.

## Counts by source

- GitHub code: 135,424 tokenized / 17 hyphen / 83 concatenated / 21 underscored.
- GitHub issues: 103 hyphen (tokenized) / 0 concatenated / 0 underscored.
  GitHub PRs: 121 hyphen (tokenized) / 0 / 0.
- Hacker News Algolia: 0 phrase / 6 hyphen / 9 concatenated; 0 true phrase hits.
- urlquery htmx: 0 / 0 / 0 for the three forms.
- Wayback CDX (port 80, bare prefix): [] for "tango-zulu" and "tangozulu" (retry after a
  transient "Temporarily Offline" page); [] for the shop-domain prefix.
- Web search: ~9 + ~8 results reviewed, all noise (see above).

## Novelty checks (read-only, staged only, no Factum writes)

- Factum exact match "tango zulu": not_found, 0 matches.
- Factum fuzzy match "tangozulu": only substring false positives on a different word
  containing "tango"; adjudicated noise.
- lists/ (including lists/urls/), findings.md: 0 matches for "tango".
- Transluce tracker snapshot (latest file, 2026-10-30): 0 matches for "tango".
- Task brief's prior workspace grep: ZERO prior mentions (taken as given; not re-run
  exhaustively — see open questions).

## Failures / open questions

- A full recursive grep of the legacy evidence tree was started, hit very large files,
  and was killed before completion; legacy-tree coverage is therefore incomplete in
  this lane run. The brief's prior zero-mention workspace grep mitigates this, but a
  confident novelty claim should not rest on this lane's legacy grep alone.
- GitHub code-search totals are API totals; only the first page of hyphen hits was
  spot-checked in depth. Remaining hyphen/concatenated hits were triaged by
  repository/path pattern (domain lists, wordlists, test fixtures) and are consistent
  with noise, but were not each opened.
- "T/Z" standalone search not run (too generic); if the coordinator wants it, it
  needs a bounded form (e.g. quoted "T/Z" with an agent/bot context term).
- No Shodan, no package repos, no Docker Hub, no POST/login, no Factum writes,
  no commit — per task constraints. Note: the repo's AGENTS.md default is to submit
  new structured evidence through Factum; this lane followed the task's explicit
  stage-only instruction instead, so ingest (if any) is the coordinator's call.
