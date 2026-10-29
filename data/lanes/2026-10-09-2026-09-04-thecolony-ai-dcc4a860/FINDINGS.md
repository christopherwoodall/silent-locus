# Findings

Grade claims OBSERVED, UPSTREAM, or INFERENCE.

## What the lane holds (57 Factum records)

- 10 `intel.report` (OBSERVED): the 10 investigator posts exist at their
  thecolony.ai URLs with the recorded titles, authors, colonies, and dates.
  The posts themselves are third-party analysis — cited as reported
  (UPSTREAM), not verified here.
- 9 `web.capture` (OBSERVED): thecolony.ai `/api/v1/search` result sets for
  9 queries (METR, centaur, eval, jina, jsonhero, "openai agents", proxy,
  rmn.re, swarm).
- 6 `reachability.check` (OBSERVED): RubyGems oracle GETs on the
  `ulinkqy8py3mp` probe family — 3 packages "could not be found", 2 geminfo
  responses empty/unexpected, owner listing empty. All yanked as of
  2026-09-28.
- 6 `web.capture` (OBSERVED): for-agents page, 2 wiki pages,
  `/api/v1/colonies` (45 colonies), `/api/v1/instructions`, `feed.rss`.
- 24 `claim` (OBSERVED): pattern-battery counts over the collected corpus —
  19 patterns with hits (jqp 38, allorigins 48, is.gd 44, jina 22, da.gd 21,
  serveo/pinggy 27, counterapi 19), 5 clean negatives (zz/oai/go-import/
  web_hooks absent from the investigators' vocabulary).

## Notes for edge building

- The investigators' vocabulary is incident-descriptive, not
  campaign-grammatical. The shared toolkit shows up instead (jina, jqp,
  allorigins, da.gd, serveo/pinggy, counterapi, vanderbi.lt).
- One 10-digit epoch nonce: 1781641854 (DemoWiki "[API bridge 1781641854]"
  by OpenAIDataBridge, 2026-06-16).
- The counter-API covert channel had ONE KEY STILL LIVE at capture time
  (verified 2026-09-28: langr5backup4813_CA=4, _TX=2) — per the incident
  wiki, cited as reported.
- PROVENANCE.md documents a capture-time CRLF normalization affecting 6
  text files; affected records carry a `raw_file_note` tag. The observed
  values are unaffected.
