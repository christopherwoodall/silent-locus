# PROVENANCE — hfspace-proxies dataset

**Source:** Hugging Face Hub public Spaces API (`https://huggingface.co/api/spaces`), public
Space repos (README/Dockerfile/app code), and public web search.
**Retrieved:** 2026-09-27/28 (recon lane B).
**Method:** read-only. Hub API `?search=` queries for `cors-proxy`, `cors_proxy`,
`jina`, `reader-proxy`, `proxy`, `markdown-reader`, `web-reader`, `url-to-markdown`,
`jina-reader`, `fetch-markdown`; per-space detail + README fetch; repo file listing;
grep of the collusion-wiki corpus for `*.hf.space` references.

**What this is:** an enumeration of proxy-shaped HF Spaces relevant to the
agent-laundering tradecraft (generic CORS `?url=` shims, jina-reader clones).
15 Spaces staged in `spaces.jsonl`.

**Tie-strength labels** (in `spaces.jsonl`, field `tie_strength`):
- `in_corpus` — the Space URL literally appears in the collusion-wiki corpus
  (1 Space: `TheNacken/python-cors-proxy`, 3 uses).
- `pattern_match` — matches the proxy-shape pattern by name/function only;
  NO evidence of swarm use.

**Keep-all + annotate policy applies:** no records dropped; swarm linkage is
annotated per record, never assumed. Nothing here identifies operators —
Space owners are public Hub usernames as published by Hugging Face.

**Limitations:** Hub search is keyword-based and incomplete; private Spaces are
invisible; app behavior verified by code read only for `TheNacken/python-cors-proxy`
(the rest are shape-matched, shims unverified). Live Spaces change over time —
re-run the Hub queries to refresh.

## Schema backfill 2026-09-29
- Transform: `temp/backfill_w2.py`. Pre-schema flat records brought onto the
  shared schema. Renames: `url` -> `source_url`; `id`, `live`, `sdk`,
  `created`, `modified`, `likes` -> `labels` as `space.id`, `space.live_url`,
  `space.sdk`, `space.created`, `space.modified`, `space.likes`; `shape`,
  `swarm_tie`, `tie_strength` -> `labels` unchanged.
- `@timestamp` = `space.created` (Hub Space creation date, date-only ->
  midnight UTC); `labels.timestamp_source = "labels:space.created"`.
- record_kind: `venue_probe` (enumeration/probe of proxy-shaped HF Spaces as
  potential laundering venues).
- fingerprint identity string: `sha256(space.id)` — the Hub Space id
  (`owner/name`) is the natural unique key.
- event.dataset = `hfspace-proxies`; event.created = backfill run time.
