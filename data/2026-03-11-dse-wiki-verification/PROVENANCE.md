# PROVENANCE — dse-wiki-verification

Lane 23 — DSE-wiki third-party analyses verification (expanded), 2026-09-27/28.
Read-only. Full writeup: `notes/gem-hunt-dse-wiki-verification-2026-09-27.md`.

## Source

- **Cite extraction (§1 of the lane note):** neither GitHub analysis
  (`hamzah2304/messageboardauditbench`, `swarm-ai-research/wiki-agent-swarm-incident`)
  cites individual urlquery report IDs; both were cloned and grepped in full.
  The six concrete urlquery IDs live one hop upstream, in the Transluce article
  (https://transluce.org/agent-activity, 2026-09-23). All six were still live on
  urlquery.net at verification time — zero expiry decay.
- **Retrieval:** live `urlquery.net/report/<id>/json`, 2026-09-28T02:10:57Z,
  Chrome UA, ≥20s pacing (rapid sequential pulls trigger spurious 404s = rate
  limiting, not expiry). Per-report bytes + SHA-256 logged in
  `raw/provenance_cited.json`; report JSONs in `raw/reports/`.
- **Expansion (§2):** indicator sweep over the frozen 51,643-report cache
  (`raw/expansion/cache_indicator_hits.json`) for TTP-adjacent families
  (pp.aihw.gov.au, mail.gw, nmdigital.unm.edu, tok=expt, setsid/nohup,
  wikiservice.at, XSSMARK, random.Random, rmn.re, bridge domains, …) plus
  live HTMX searches (`raw/expansion/search_summary.json`) — all returned
  HTTP 204, which per the lane's own discipline are NOT trusted as negatives.

## The six cited reports

| report_id | cited for | scan date |
|---|---|---|
| `01fd9706-d9d0-42e4-b813-448a541a2571` | Data USA SQLi probe | 2026-05-28 |
| `d6669745-83d2-4628-82fa-87420ae6a5d7` | Thai NSO / pastebin.k4be.pl | 2026-03-11 |
| `6fd6d3cb-2d66-408e-91e4-910352cc0cfc` | Thrill Data theme parks | 2026-05-12 |
| `c08684cc-3da4-4d53-a288-0d014243c075` | GET→POST bridge (httpbin) | 2026-04-27 |
| `1ad9c2e8-96ff-44af-b446-b717bcb995b4` | GET→POST bridge (milankarman) | 2026-04-27 |
| `e044dea5-ca3b-4e3c-9083-f422148ffd77` | GET→POST bridge (blogsflow) | 2026-05-29 |

## Schema normalization 2026-09-29 (worker W3)

- Transform: `temp/build_events_w3_dse_wiki.py` (repo root passed as argv[1]).
- Grain: one record per cited report (6, `record_kind: download`) + one record
  per indicator in the union of both sweep files (15; `corpus_hit` when the
  frozen-cache sweep found hits — 4 indicators — else `corpus_grep_negative`).
  Sweep rows carry both the cache result and the untrusted live-204 result
  (`labels.sweep.live_trusted: false`).
- `@timestamp`: report scan date for downloads
  (`labels.timestamp_source = "labels:report.date"`); the documented lane date
  2026-09-27 for sweep rows (`labels.timestamp_source = "lane:2026-09-27 …"`,
  per-query timestamps absent from raw).
- Fingerprint identity strings:
  - reports: `sha256("dse-wiki-report:<report_id>")`
  - sweeps: `sha256("dse-wiki-sweep:<indicator>")`
  Method verified against the reference: recomputing
  sha256("TheNacken/python-cors-proxy") reproduces
  data/2023-11-14-hfspace-proxies' fingerprint `14c645d9…efbe94` exactly.
- `event.dataset = "2022-12-30-dse-wiki-verification"`;
  `event.created` = build time (UTC).
- No `rollup.jsonl`: this collection is a pure event stream (report
  verifications + sweep queries); no burst/window/per-actor layer is derivable
  without inventing one. Verdicts live in the lane note (§3), not in a rollup.

## Caveats

- Live HTMX search 204s are not trusted negatives (lane discipline); the cache
  sweep stands as the expansion pass.
- The `unm_nmdigital` / `unm_tok_expt` cache hits are title mentions, not probes
  (annotated per record).
