# Provenance — disk-corpora worker cache (LIFEVAL cross-corpus sweep)

**Cached at:** 2026-10-06T23:20:00-05:00 · **By:** disk-corpora worker
**Method:** read-only `rg -i` grep of `~/workspace/silent-locus/data/` (excl. `.git`,
excl. `2026-10-06-wikimedia-rogue-agents/wikipedia-lane/`) + `~/workspace/muse-home/projects/`.
Corpus files were NOT modified.

## Primary hits cached (cross-corpus survivors)

| cache file | bytes | sha256 | record |
|---|---|---|---|
| `disk-corpora-dse-willkommenimwiki-23.json` | 6599 | `4725c924b00309009b60218846557e2bd9aad2dfc0978fd584dc93501f7cd535` | dse~WillkommenImWiki@23 — full record, `change_summary: "sandbox link test"`, 2026-06-18T17:38:50Z, body_len 4825 (SEC county.json link-farm body) |
| `disk-corpora-dse-willkommenimwiki-13.json` | 1469 | `9428a492c3745de488d3b4adf801f6416942b1931f65a53781a6530fdb1026d0` | dse~WillkommenImWiki@13 — metadata-only record, `change_summary: "sandbox link test"`, 2026-06-18T19:38:00+01:00 |

## Source files (sha256 at retrieval time)

| source path (repo-relative) | sha256 |
|---|---|
| `2026-05-17-collusion-wiki/raw/revisions.jsonl` | `60df4a515178230aa952d9f64f6215aea4bd95ab2f05e31e484cf9b887e3f793` |
| `2026-09-28-chinese-amap-fleet/personas/pastebin-plunderer/raw/deep-dive/lane3-colony-bullfincher/ref/run1/agent-logs/prowiki/revisions.jsonl` | `60df4a515178230aa952d9f64f6215aea4bd95ab2f05e31e484cf9b887e3f793` (byte-identical duplicate of the collusion-wiki copy — one underlying record, two on-disk copies) |
| `2026-09-28-chinese-amap-fleet/personas/pastebin-plunderer/raw/deep-dive/lane3-colony-bullfincher/ref/run1/agent-logs/dse/revisions.jsonl` | `cd8a95d51adce94e091c972e38fe8b7935366d77a1b44b5eaa40694b83cba62c` |

**Wiki identity:** `wiki: "dse"` = `wikiservice.at/dse` (per
`.../lane3-colony-bullfincher/THECOLONY.md:97`, which lists `wikiservice.at/dse`
among the colony's target surfaces).

**Zero-caches (honest zeros, nothing cached):**
- `"Lifeval temporary technical sandbox initialization"`, `"Lifeval API temp-account test"`,
  standalone `"Lifeval"`, `"Temporary technical sandbox initialization"` — **zero hits outside the
  wikipedia lane's own worker artifacts** across the entire 1.8G data dir and `~/workspace/muse-home/projects/`.
- WMF evidence CSV cache (`2026-10-06-wikimedia-rogue-agents/raw/openai-wikimedia-edits-2026-10-04.csv`):
  zero hits on every string — the marker vocabulary does not appear in WMF's own evidence file.
- Tokyo Gas sponsor noise: zero on-disk hits anywhere (it existed only in the lane's live
  `insource:"Lifeval"` search JSON: `pattern-hunter/raw/search_lifeval_en_wikipedia_org.json`,
  football-sponsor tables — `[[Tokyo Gas|Lifeval]]`).

Sibling-worker files already in `raw/` (`q01`–`q10`, `probe_*`, `control_*`, `search_page.html`)
belong to the web-search worker — not touched.
