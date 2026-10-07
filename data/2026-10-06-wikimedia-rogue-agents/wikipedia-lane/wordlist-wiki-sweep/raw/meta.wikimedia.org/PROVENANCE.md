# Provenance — wordlist-wiki-sweep raw/meta.wikimedia.org/

- **Method:** MediaWiki Action API `list=search` with
  `srsearch=insource:"<term>"`, `srlimit=50`, `srnamespace=*`,
  `format=json`, `formatversion=2` — 1,148 terms from
  `wordlist-wiki-sweep/search-terms.json` (the Wikipedia-plausible subset
  of the shared IOC wordlist; categories: launcher_toolkit, relays,
  dead_drops, targets, evals). Plus `prop=revisions`
  (`rvprop=ids|timestamp|user|comment|tags`, `rvlimit=200`) on
  Meta:Sandbox, comment substring match (case-insensitive).
- **Collection:** Python urllib (URL-encoded terms), User-Agent
  `silent-locus-wordlist-wiki-sweep/1.0`, paced >=5.5s between requests,
  run 2026-10-07 UTC (run log: RUNLOG.tsv, columns
  n / term / timestamp_utc / http_status / hit_count / error).
- **Files:** `insource-<n>.json` for all 1,148 terms (n indexes the
  `terms` array in search-terms.json); hits AND zeros cached.
  `sandbox-comments-meta.json` (raw revisions), `sandbox-comments-SUMMARY.json`
  (comment matches), `SUMMARY.json` (per-category tally + hit list).
- **Known limitation:** insource: searches CURRENT page content only;
  cleaned sandboxes erase content markers (see ../vocab-sweep/FINDINGS.md).
  Comment grep is a 200-revision spot check, not exhaustive.
- **Scripts:** sweep_meta_insource.py (collection, resumable via RUNLOG.tsv),
  analyze_meta.py (summary + comment grep).
