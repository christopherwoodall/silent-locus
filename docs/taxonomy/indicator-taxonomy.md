# Indicator taxonomy — 2026-10-01 oai-tag sweep

Status: derived from the 2026-10-01 sweep lane (aggregation, 2026-10-10).
Lane: `oai-tag-sweep`. Source sidecar:
`data/lanes/oai-tag-sweep/events.jsonl` (96,353 annotated events).

## Terms

- **Indicator**: one named regex pattern from `sweep_indicators.py`.
  A "hit" is one annotated event where the pattern matched.
- **Event**: one annotated row in `events.jsonl` (a wiki revision, a
  urlquery report, a RubyGems campaign row, or a Transluce dataset row).
- **Prevalence**: hit count per indicator, per source.
- **Exemplar**: a verbatim evidence snippet copied from the sweep sidecar.

## Sweep coverage

The sweep scanned four frozen sources on 2026-10-01:

| source | records scanned | annotated hits |
|---|---|---|
| frozen:urlquery-incidents | 51,643 | 12,938 |
| frozen:collusion-wiki | 80,434 | 80,434 |
| frozen:rubygems-goimport | 6,619 | 2,972 |
| transluce-dataset | 38,160 rows | 9 |

Total annotated events: 96,353. Events with 2+ indicators: 25,699 (26.7%).
Days with hits in 2+ sources: 58.

Note: every collusion-wiki revision trivially matches `collusion_wiki_ref`
(the corpus cites its own source), so that indicator's wiki count equals the
wiki corpus size. The useful wiki signal is in the other 13 indicators.

## Indicators (15 fired of 18 defined)

| indicator | pattern meaning | total hits | wiki | urlquery | rubygems | transluce |
|---|---|---|---|---|---|---|
| file_suffix_antibot | file suffix (.json/.xml/.csv/.txt/.pdf) or output/raw/url/debug param in URL | 12,501 | 10,271 | 2,193 | 37 | 0 |
| collusion_wiki_ref | literal `collusion.wiki` | 80,439 | 80,434 | 5 | 0 | 0 |
| jina_allorigins_dagd | r.jina.ai, allorigins, or dagd relay host | 7,867 | 4,088 | 2,723 | 1,056 | 0 |
| httpbun_httpbin | httpbin or httpbun probe URL | 7,339 | 123 | 7,213 | 3 | 0 |
| epoch_nonce | 10-digit epoch timestamp (1[78]xxxxxxxx) | 4,756 | 4,138 | 288 | 321 | 9 |
| double_slash_path | `//` inside a URL path (chained converter/proxy URLs) | 4,350 | 3,328 | 59 | 963 | 0 |
| uniq_nonce_param | `?uniq=` / `nonce=` / `_t=` / `cb=` with 6+ digits | 3,070 | 3,019 | 51 | 0 | 0 |
| cors_conversion_proxy | CORS proxy or converter host (workers.dev, corsproxy, googleusercontent, translate.google, ...) | 2,886 | 1,469 | 1,415 | 2 | 0 |
| oai_prefix | token boundary followed by `oai` + word char | 2,662 | 2,026 | 4 | 632 | 0 |
| markdown_new | literal `markdown.new` converter | 2,639 | 2,628 | 11 | 0 | 0 |
| exposed_key_in_url | `apikey=` / `token=` / `secret=` style param in URL | 2,524 | 129 | 2,395 | 0 | 0 |
| goimport_canary | `go-import` meta tag | 1,867 | 0 | 0 | 1,867 | 0 |
| zz_label | token boundary followed by `zz` + word char | 1,141 | 576 | 36 | 529 | 0 |
| arquivo_pt | literal `arquivo.pt` | 9 | 8 | 1 | 0 | 0 |
| direct_ip_route | literal IPv4 host in URL | 9 | 1 | 0 | 8 | 0 |

Defined but never fired (zero hits in all four sources): `webhook_deaddrop`
(A000/ZZEND dead-drop chunks), `github_remote_cache_zz`
(`github-remote-cache/zz`), `disposable_email` (tempmail-style domains).

## Verdicts (verified against bytes, from lane PROVENANCE.md)

- **oai_prefix**: the 4 frozen-urlquery hits are all false positives
  (`OAItest7z645xgm` httpbin probe, `OAIJS1782002787694412133` httpbun probe
  title, `persistent.oaistatic.com` ChatGPT asset domain, `utm_oaid` ad
  param). Zero genuine Transluce-style oai* agent tags in the frozen
  urlquery corpus. The 2,026 wiki hits are genuine DSE-grammar labels
  (e.g. `dse~OAIFlatheadBridgeTestMay24X@45`, `grammar:oai` tags),
  wiki-side, agent-authored. The 632 rubygems hits are oai gem names
  (existing watchlist surface).
- **arquivo_pt**: the 1 urlquery hit is a scan OF the arquivo.pt homepage
  (2026-09-25), not relay use. The 8 wiki hits are Nightingale
  investigation notes documenting our own DataUSA bundle reproduction
  (Jun 16-17). Zero agent relay-use of arquivo.pt in our vantage.
- **markdown_new**: the 11 urlquery hits split into 7 tinyurl-chain scans
  (May 11-13) and 4 agent uses of `markdown.new/r.jina.ai/...` chains
  (May 14 datastudio, May 17 alexandria.ucsb.edu) plus our own
  reproduction (Sep 24) and one May 27 API conversion. The 2,628 wiki
  hits are wiki revisions documenting agent converter use.
- **collusion_wiki_ref**: tautological on the wiki corpus (self-citation);
  the 5 urlquery hits are reports that mention collusion.wiki.

## Factum mapping

Each fired indicator is one `intel.behavior` observation
(`category` = indicator name). No `infra.ioc` records: indicator names are
not concrete IOC values.

Dedup note (2026-10-10): `oai_prefix`, `epoch_nonce`, and `markdown_new`
already exist as `infra.ioc` marker terms in lane
`2026-09-05-termina-digital` (different record type, different lane —
kept; no duplicate submitted). No `intel.behavior` taxonomy for these
indicators existed before this ingest.

## Temporal note

Hit event times span 2025-03-04 (earliest, `oai_prefix`) to 2026-09-27.
Per-indicator first/last seen dates are in the `intel.behavior` records.
The sweep found 1,665 burst minutes with >= 8 hits; the largest was
2026-06-18T20:10 UTC (665 collusion-wiki hits). 58 days had hits in 2+
sources. Day-level hit counts inside known windows are in the lane's
`temporal_overlaps.md`.
