# EventStreams detection engine — Wikimedia rogue-agent monitor (detector/)

OFFLINE BUILD. This directory is build-only: rules as data (`rules.yaml`), a
generic engine (`detect.py`), a census allowlist
(`allowlist_bibliographic_domains.txt`), and fixture-based tests
(`tests/`). It is NOT wired to live EventStreams — no network calls, no cron,
no systemd. That wiring is a separate task for a network-capable lane.

## What it detects

Every rule traces to a 2026-10-06 hunt finding (see `rules.yaml` → each rule's
`provenance`: incident finding + exact source file + claim grade):

| rule | severity | incident geometry it encodes |
|---|---|---|
| `temp-account-burst` | high | ~2026-36867-71 created 5 pages in ~10 min on meta (2026-06-25 20:28–20:38Z); sandbox bursts May 10 / May 27 / Jun 25; Sept-2026 probe bursts |
| `sandbox-edit-burst` | high | ~2026-28355-02 rapid sandbox-edit sequence 2026-05-10 16:01–16:14Z |
| `web2cit-config-edit` | high | Web2Cit identified as the "citation tool" (fetch-oracle primitive); 5 incident config edits |
| `web2cit-nonbibliographic-target` | critical | 562-domain census: zero non-bibliographic targets live; ArcGIS/Hawaii configs were the anomaly |
| `probe-token` | medium | `tok=expt<N>` banked census family (Transluce UNM) + adjacent-swarm discrimination grammars |
| `comment-tag-shape` | medium | 5 Web2Cit deletions in a 34s window with empty comments; vacuous sandbox comments; `mw-reverted` tags |

## Input event schema

Normalized JSON, one object per JSONL line:

```json
{"ts": "2026-06-25T20:28:27Z", "wiki": "meta.wikimedia.org",
 "user": "~2026-36867-71", "title": "Web2Cit/data/com/arcgis/geocode/templates.json",
 "namespace": 0, "comment": "adding template", "tags": ["mw-reverted"],
 "content": "<added text>", "is_new": true}
```

`ts` (ISO-8601 or epoch), `wiki`, `user`, `title` are required. `tags` accepts a
list or a comma-separated string. The normalizer also accepts raw EventStreams
`revision-create` shapes, mapping `meta.dt→ts`, `page_title→title`,
`page_namespace→namespace`, `user_text→user`, `rev_content→content`,
`rev_parent_id==0→is_new`.

## Usage

```bash
python3 detect.py events.jsonl                      # file input, alerts to stdout
cat events.jsonl | python3 detect.py                # stdin
python3 detect.py --state-file state.json batch.jsonl  # persist burst windows
python3 detect.py --pretty events.jsonl             # human-readable alerts
```

Exit 0 = evaluated (alerts or not). Exit 2 = malformed input (bad JSON line,
missing required field, bad timestamp, bad rules file) with a clear stderr
message. Exit 3 = PyYAML missing.

Alert schema (one JSON object per stdout line):

```json
{"ts": "...", "rule": "web2cit-nonbibliographic-target", "severity": "critical",
 "wiki": "...", "user": "...", "title": "...",
 "evidence": {"non_allowlisted_domains": [{"source": "title", "domain": "arcgis.com"}],
              "allowlist_size": 562},
 "provenance": {"finding": "...", "source_file": "...", "grade": "OBSERVED"}}
```

Every alert carries its provenance (grade-friendly output).

## State file format (burst rules only)

Burst rules (`temp-account-burst`, `sandbox-edit-burst`) are stateful across
batches. Default is in-memory; `--state-file PATH` persists:

```json
{"temp-account-burst": [{"ts": "2026-06-25T20:28:27Z", "wiki": "meta.wikimedia.org",
                         "user": "~2026-36867-71", "title": "..."}]}
```

Entries are pruned to the rule's window on every run; corrupt entries are
skipped (never fatal), a corrupt file is a hard error. Note: while a window is
hot, each new batch re-emits the burst alert — alert consumers dedupe.

## Allowlist

`allowlist_bibliographic_domains.txt`: the 562 unique bibliographic target
domains from the 2026-10-06 Web2Cit/data/ census (header documents provenance
and the regeneration procedure). Validated: all 848 census catalog titles
derive to domains covered by the list; the incident domains (arcgis.com,
geodata.hawaii.gov, …) are NOT covered. The list is point-in-time — legit
community additions will false-positive `web2cit-nonbibliographic-target`;
triage = verify the domain is bibliographic, then regenerate.

## Tests

```bash
python3 tests/run_tests.py   # 14 checks: 12 fixture cases + malformed-input + state persistence
```

Fixtures in `tests/fixtures/`: hand-written positives (incident-shaped events
that MUST fire) and negatives (that must stay silent), plus `f07_malformed.jsonl`
(exit-2 path). Expected `{rule: count}` mappings live in `run_tests.py`.

## Rules considered but left out

- **WDQS / API volume rules** (statistician lane): "millions" of requests ≈
  0.07% of monthly page views; volume alone cannot explain the outage and there
  is zero public signal on query COST. No defensible threshold → not encoded.
- **Etherpad pad-series rules** (`Test<Mon>Actor<NN>`): single-source,
  uncorroborated claim (etherpad-diver); kept only as a probe-token
  discrimination pattern, not a standalone rule.
- **Phabricator / scraper-signature rules**: signatures unpublished (open lead #5);
  nothing to key on yet.
- **Username-prefix sweeps** (OpenAI*/oai*/ChatGPT* on enwiki): clean negative
  (wiki-surgeon) — a rule would be pure noise.
- **Turnilo sampling / requestctl rules**: infra-side, not EventStreams-visible.
- **Deletion-burst rule**: the 5 Pppery deletions are admin cleanup 15h
  post-disclosure, not agent behavior; the empty-comment signal is already
  captured by `comment-tag-shape` on config trees.
