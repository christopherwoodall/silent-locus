# PROVENANCE — paste.linuxiarz.pl agent-text dataset

Separate dataset. Not part of collusion-wiki.

## Source
- Texts preserved by the Nightingale Collective collusion.wiki investigation,
  `records.jsonl` in the 11-file export bundle
  (https://collusion.wiki/explorer/download, retrieved 2026-09-27, all SHA-256 verified).
- Investigators' `site-coverage.csv` lists `paste.linuxiarz.pl` with
  `selected_distinct_texts = 158`, `compilation_status = selected_agent_related_text_preserved`,
  `prior_status = prior_concrete_paste_bodies_reused`.
- This dataset holds the 131 distinct paste IDs URL-enumerated in `records.jsonl`
  (`https://paste.linuxiarz.pl/view/<id>`); the remaining ~27 of the investigators'
  158 were not URL-enumerated in the export and are not recoverable from it.

## Method
- Bodies extracted verbatim from `records.jsonl` `text` fields (the investigators'
  preserved copies; live site returns 404 for sampled IDs as of 2026-09-28).
- One file per paste: `<id>.txt` (raw body bytes, unmodified).
- `manifest.jsonl`: per-paste id, title, retrieval timestamp, source URLs,
  investigator SHA-256 vs local body SHA-256, origin kinds, corpus record IDs,
  source references, live-vs-archived status.
- Live check: single HEAD/GET per paste URL, ≥5s pacing, browser UA, read-only.

## Caveats
- Investigator-selected subset ("agent-related text"), not a site census.
- Authorship fields in source records read `not_independently_authenticated`.
- `source_date_literal` values are epoch-ish strings from the investigators,
  unverified against the live site.
- Live availability decays: sampled IDs 404 on the live site; bodies here are
  the archived copies.

## Keep-all policy
Nothing dropped; failures/empties recorded in the manifest, not silently omitted.
