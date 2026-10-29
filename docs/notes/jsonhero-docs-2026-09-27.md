# jsonhero.io shared docs — ingest + inspection (2026-09-27)

Recon lane F found the swarm using jsonhero.io as persistent shared state.
This lane fetched the 17 shared doc IDs, inspected the payloads, and ingested
them as their own dataset + Elastic index.

## Retrieval: 11/17 live, 6/17 dead

- Fetched via `GET https://jsonhero.io/j/<id>.json` (the docs were published to
  jsonhero.io's unauthenticated public document API), paced ≥3s, browser UA.
- urllib hit `IncompleteRead` on larger bodies (egress-proxy streaming artifact);
  curl completed every live doc. Lesson recorded for future fetch lanes.
- Dead (HTTP 500 "Unexpected Server Error", no aggressive retry):
  `S5R1RRn64PLh`, `aB94pTzmWvtl`, `swJMw8b6VwDC`, `qDhAiEHyjXYi`,
  `wANOlosoW5YN`, `1vaGknk7ajC4`. **All 6 are referenced in June-2026 wiki
  revisions** — they were live during the campaign and died since.
- Manifest: `data/jsonhero-docs/manifest.json` (id, URL, status, SHA-256, size,
  corpus occurrence count). PROVENANCE.md alongside.

## Inspection: 4 content families

**Group A — 7 docs, byte-identical (85,889 B):** `yesDZj1nfKfx`, `buvcgpLEU8Dl`,
`2fJbsT54pB5I`, `TVu5XGYbf7Jz`, `54DiK2z9XiQy`, `RVsn7JgZWGfl`, `2EvFizxRzKLN`.
SEC Regulation Crowdfunding county dataset: `regCF_county_methodology`
(EDGAR Form C/C-U methodology text), `regCF_county_filters`, yearly arrays
2019–2024. The corpus `?path=` deep links **resolve** — verified
`regCF_county_2021.91` → `{"code": "us-md-005", "offerings": 10,
"usd": 3067574.52, "color_code": 4}` (a Maryland county record).
The 10-digit numbers in the payload are **SEC CIK identifiers**
(`0000189542`…), not epoch nonces — grammar-battery correction.

**Group B — 2 docs, byte-identical (10,942 B):** `rmRy2sPyWJs1`, `y2k6iLoEGhuA`.
County-boundary GeoJSON (14 features, `hc-transform` = Highcharts map
payload), census.gov attribution. The map layer for the same SEC task.

**`KwQ0rn8weoBu` (1,472 B) — agent-authored extract.** `source`:
`https://www.sec.gov/files/county.json`; `note`: "Direct Massachusetts entries
copied from SEC county map JSON. usd is raw US dollars. Divide by 1000 for map
thousands." `us-ma-*` codes with raw USD amounts. The note field is an agent's
own working annotation — direct evidence of agent authorship of the doc.

**`CXGtP3kgj056` (634 B) — test/probe.** France/Denmark/Belgium/Germany/Italy
`internetPoorFemales` 2018–2020 rows. **Not referenced in any wiki revision**
— a probe doc, not campaign state.

**IOC battery** (jina, md.succ.ai, jqp, webhook, oast, shorteners, go-import,
`<img` beacons): **zero hits** in all 11 payloads. The docs are clean
task data — the tradecraft lives in the fetch layer, not the stored data.

## Shared-state evidence

- 7 different doc IDs carry the **byte-identical** 85,889-byte payload, and 2
  more share the identical GeoJSON — agents re-minting the same dataset under
  new IDs (or re-posting a shared canonical payload). Shared state across
  agents/mints, not 17 independent documents.
- Wiki↔doc cross-reference: **2,273 revision→doc links**
  (`data/jsonhero_doc_links.jsonl`): probier 2,266 / dse 7; agent labels
  publisher-redacted (`''` 1,611 / `A` 592 / `Agent` 63) plus `MassSecWin12`
  (6) and `TexasWikiHelper` (1). Views: plain viewer 2,198, `.json` 28,
  `/tree` 26, `/editor` 21 — agents exercised the API surface, not just reads.
- 16/17 doc IDs appear in wiki revisions (only the probe doc doesn't).

## Cascade

- `https://www.sec.gov/files/county.json` (upstream cited in `KwQ0rn8weoBu`) —
  HTTP 403 bot-block from this network; not retried aggressively. The agents
  fetched it through reader proxies (jqp/md.succ.ai), which is exactly why the
  proxy layer exists. No other cascade-worthy artifacts surfaced (no webhooks,
  no new payloads, no referenced datasets inside the docs).

## Elastic

- Own index **`jsonhero-docs`** (canonical shared mapping,
  `notes/gems-es-mapping.json`; `event.dataset` = `jsonhero-docs`, keyword
  natively; zero new top-level fields, detail in `labels` + `tags`).
- **17 docs confirmed** in index: `status:live` 11
  (`content:regcf` 7, `content:geojson` 2, `content:extract` 1, `content:test` 1),
  `status:dead` 6. One ES doc per jsonhero document; labels carry doc_id,
  sha256, byte size, corpus occurrences, wiki-ref counts, wikis, agent labels.
- Ingest script: `scripts/es_ingest_jsonhero.py` (`--create`/`--load`/`--verify`).

## Files

- `data/jsonhero-docs/` — 11 payloads + `manifest.json` + `PROVENANCE.md`
- `data/jsonhero_doc_links.jsonl` — 2,273 wiki↔doc links
- `scripts/es_ingest_jsonhero.py`, `scripts/fetch_jsonhero_docs.py`
- `notes/jsonhero-docs-2026-09-27.md` (this report)

Scope: agents/infrastructure only. No operator identity pursued.
