# Lane F — proxy-primitive sweep (2026-09-27)

Sweeps longcat's 207-domain-audit proxy primitives — `pure.md`,
`api.cors.lol`, `corsmirror.com`, Google Docs Viewer `gview` — across our
own corpora, catching URL-encoded variants (`pure%2emd`, `pure%252emd`,
double-encoded hosts).

## Result: 1,522 hits after exact-duplicate collapse

| primitive | hits | distinct URLs |
|---|---|---|
| pure.md | 753 | 723 |
| api.cors.lol | 318 | 208 |
| gview | 290 | 187 |
| corsmirror.com | 161 | 81 |

Per-hit: primitive, source record, `laundered_target` (best-effort parse of
the wrapped URL), `first_seen_effective` (earliest revision `write_date`
containing the exact URL; present on 1,091/1,522). Corpus-window first-seen:
**2026-05-26 → 2026-06-20**.

Data: `data/proxy-primitives/hits.jsonl` + `PROVENANCE.md`.
Elastic: index **`proxy-primitives`**, 1,522 docs, shared canonical schema,
`event.dataset.keyword` multi-field declared at creation (verified in live
mapping). Scripts: `scripts/sweep_proxy_primitives.py` (ES + raw grep),
`scripts/extract_wiki_proxy_urls.py` (structured wiki extraction, merge,
dedup), `scripts/es_ingest_proxy_primitives.py` (--create/--load/--verify).

## Where the hits live

- **Wiki corpus, not the gem corpus.** All real primitive URLs come from
  `data/collusion-wiki/` (links, revisions, records, pivot products).
  The gem corpus (`gem-ioc-log/hits`, JFrog CSV, Diffend sweep, graph
  files) has **zero** primitive URLs — only gem-name fragments
  `zjgview5`, `zrgview1`, `zrgview2` (zz-grammar names), flagged
  `record_kind=gem-name-fragment`, not proxy use.
- Pivot rows are ~entirely **dse** (820) with a trace of probier (7).

## Key findings

1. **Nested laundering is the norm, not the exception.** 152 pure.md hits
   wrap *another* proxy — `pure.md/r.jina.ai/...`, `pure.md/md.succ.ai/...`,
   and chains through `jqp.vercel.app` (jq API) on the outside:
   `jqp.vercel.app → pure.md → r.jina.ai → sec.gov`. Proxy primitives stack
   like protocol layers; a single-hop blocklist misses the traffic.
2. **Cross-primitive nesting**: `corsmirror.com/v1?url=https://pure.md/...`
   and pure.md wrapping `api.cors.lol` URLs (107 cors.lol-as-target rows) —
   the agents treat these as interchangeable, composable transports.
3. **Top laundered targets**: SEC EDGAR county JSON (`www.sec.gov`, 112),
   College of Charleston IIIF/library image servers (138 combined),
   Yahoo Finance query APIs (81), `md.succ.ai` (64, itself a proxy).
   Mundane public data endpoints, repeatedly re-fetched through different
   proxy stacks — consistent with eval-task data-gathering loops, not
   targeted intrusion.
4. **gview is real in the corpus**: 187 distinct viewer URLs (the 204-count
   in longcat's note is the same order; delta is dedup/encoding variants),
   first seen 2026-05-26.
5. **ES index blind spot (method note)**: the `collusion-wiki` ES index
   withholds raw URLs (`labels.url_withheld=true`), so ES-side primitive
   queries return 0 for pure.md/cors.lol/corsmirror despite the URLs being
   in the source dumps. The local gz files are authoritative; do not cite
   ES counts as coverage for URL-content questions.

## Open

- Per-URL first-seen is a corpus-snapshot lower bound, not internet-wide
  first use; 431 hits carry no timestamp (truncated URLs / annotations).
- Truncated URLs in the released dump (`http://api.cors.lol/?url=https:%2`)
  have unrecoverable targets — null `laundered_target`.
- July-7 wave + webhook dead-drop IOCs (JFrog report) not yet swept against
  these primitives; the `thecolony-ai` index (27 docs) was not swept either
  (out of lane scope — small, but cheap to add).
