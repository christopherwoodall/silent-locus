# FINDINGS — 2026-09-05-termina-digital

Short evidence summary for the termina.digital incident-DB recovery.
Full provenance is in PROVENANCE.md. Claims are graded OBSERVED unless noted.

## Recovery

- The termina.digital /db/ (cited by thecolony.ai on 2026-09-05 as a
  downloadable incident JSONL database) was dark on 2026-09-28: /db/ 404,
  /db/llms.txt 503 ("public exports are temporarily unavailable").
- The DB lived on **swarm.termina.digital**, not the main domain. Wayback CDX
  for swarm.termina.digital* gave 115 rows (captures 2026-09-05 → 2026-09-18).
- 99 files recovered: incidents, campaigns, clusters, venues, actors,
  trackers, about/api/claims/evidence/tips/scan/summary pages, llms.txt,
  search-config.json, graph.json, search index.
- 3 permanent wayback failures: bogus `/db/index.html)` CDX row,
  `/db/page/dse/` directory artifact, `/db/search.html?q=xinhai` 404.
- The public tarball `agent-pastes-2026-09-08.tar.gz` is a 43-byte HTTP-503
  placeholder (live and in Wayback). Nothing further is retrievable.

## Sweep battery (21 patterns over 97 files)

High-signal hits:

- `oai_prefix`: 581 hits across 12 files (top: human_dse_284.html 245,
  graph.json 310).
- `epoch_nonce`: 1,279 hits across 18 files (top: human_dse_284.html 947,
  graph.json 282).
- `zz_word`: 227 hits across 3 files.
- `webhook`: present (venue/actor pages); `jina`, `jqp`, `allorigins`,
  `proxymule`, `da_gd`, `is_gd`, `bitily`, `vanderbilt`, `countapi`,
  `rmn_re`, `md_succ`, `markdown_new` also hit.
- Zero hits: `tryzz`, `go_import`, `chunk_markers`, `gmail`, `tty_bitty`.

## Attribution scope

The DB is a third-party investigator artifact (ai-safety-lab / rowan+fable).
Claims inside are cited as reported with the DB's own status words. No
operator identity pursued.
