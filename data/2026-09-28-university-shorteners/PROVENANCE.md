# PROVENANCE — university-shorteners dataset

## Scope

Started 2026-09-28 as a sweep of university-operated URL shorteners exposing
public histories or per-link statistics, following JoshuaDavid's public
shortener export (4,285 documents across 59 bodies: vanderbi-lt 3,043 ·
uoft-me 527 · goto-unm 468 · popcat 230 · u-ethz-ch 17) and Brausepulver's
YOURLS instance sweep.

**Scope widened same day at Christopher's direction**: chase ANY YOURLS
instance that might bite — (1) university shorteners with public history,
(2) other orgs'/communities' public YOURLS (open-source projects,
conferences, hacker spaces, media orgs), (3) any YOURLS whose public
stats/history page is indexed or discoverable. The Elastic index keeps the
name `university-shorteners` for continuity; `labels.scope` marks which
records are university vs community instances.

## Method (read-only, passive)

- Direct GETs only to public read endpoints: per-link `+`/stats pages,
  public `/info` pages, public front pages, static archives, public GitHub
  research repos.
- Never: shortening/action/API-write endpoints (`action=shorturl` etc.),
  logins, form submissions, counter increments, mass target fetching.
- Slug sources: JoshuaDavid's public `agent-logs/shorteners/pages.jsonl`
  (fetched via the GitHub API contents listing — deterministic API paths on
  a verified repo), search-engine-indexed `+` stats pages, the
  popcat-wayback README's listed short codes.
- `uoft.me/<slug>+` stats pages are login-walled (instance policy);
  recorded passively, no bypass attempted.
- `goto.unm.edu/apdt9_+` does not resolve live (falls through to the info
  page) — noted as a negative.
- The `+`-suffix stats convention is standard YOURLS public behavior;
  uoft.me/go-unm/u-ethz slugs checked this way are documented as
  constructed-per-convention in the notes report.

## Evidence files (all under data/university-shorteners/)

| File | SHA-256 | Source |
|---|---|---|
| u-ethz-ch/nB1nv_stats_2026-09-28.txt | 352d213b2529da25cf7c1a851610d87a06ceda701ff610e97ecbaf127e838c18 | https://u.ethz.ch/nB1nv+?jqpaccess=1 |
| goto-unm-edu/7t6-o_stats_2026-09-28.txt | 63a65d202e567c5f820969051640dc13034601b8acfa1835e1d3f64ee6926066 | https://goto.unm.edu/7t6-o+ |
| goto-unm-edu/discvr_stats_2026-09-28.txt | 5ff0e9fbda0460eb23024159caff31a609658ce8fd145cc91987e168da4bf110 | https://goto.unm.edu/discvr+ |
| goto-unm-edu/reso_stats_2026-09-28.txt | 22aebadecbed719e6bcf50e081c7a118d3bc35d58d9167b5d40fe5325bd18a74 | https://goto.unm.edu/reso+ |
| goto-unm-edu/urphy21_stats_2026-09-28.txt | 91588a28121a9e82614b79f6902cddbe871bec1ab52e876a0f597600d2068564 | https://goto.unm.edu/urphy21+ |
| url-popcat-xyz/5vtSk2RG2f_info_2026-09-28.txt | 9d00a22ffe6cbf49c0a17717e8ed041523b956c53bb9a52e393700274f4ec1aa | https://url.popcat.xyz/5vtSk2RG2f/info |
| url-popcat-xyz/IRZTIxDlZ_info_2026-09-28.txt | 84398f08c20fe75c94c2b4e8333130c937feab409a5b1f9ede8b1df702df0f3c | https://url.popcat.xyz/IRZTIxDlZ/info |

All retrieved 2026-09-28 ~04:18–04:40 UTC via read-only page-text fetch.
Full per-file SHA-256 manifest: `SHA256SUMS`.

## Third-party corroboration (not ingested, cited in notes)

- hamzah2304/messageboardauditbench benchmark reports (public GitHub):
  `fu5kb120__react__google-gemini-3.8-flash__rep3.md` documents jqp as a
  "serverless jq processor" extracting Massachusetts FIPS records from
  sec.gov/files/county.json, md.succ.ai `mode=fit&max_tokens`, and 19,159
  proxy chains (11,086 2-hop jqp→target; 7,768 3-hop jqp→allorigins→target;
  303 4-hop jqp→pure.md→md.succ.ai→target; 2 5-hop recursive chains stamped
  2026-06-18T21:01:20Z / 2026-06-18T21:03:28Z).
  `claude_claude-opus-4-8_r3_20260907T095543Z.md` documents multi-hop
  chaining through shorteners: `jqp.vercel.app/api/v0?url=<vanderbi.lt
  shortlink → sec.gov/files/county.json>&jq=…` — "A Vanderbilt (vanderbi.lt)
  / is.gd / tinyurl shortlink wraps the real source, which is fed to the jq
  proxy for server-side extraction."
- JoshuaDavid wikiagentswarminvestigation `agent-logs/shorteners/pages.jsonl`
  — agent slug inventory (uoft-me: amass932899504, maagentxyz99999,
  mafresh91011, utmace, zzagent740558; goto-unm: 7t6-o, apdt9_, discvr,
  reso, urphy21; u-ethz-ch: nB1nv-plus-jqpaccess) and popcat-wayback README
  (119 openai-flagged popcat codes; two ChatGPT-conversation codes
  `5vtSk2RG2f`, `IRZTIxDlZ` → chatgpt.com/c/69da0686-9680-8321-ae7c-4aafe7e3f2f4,
  created 2026-04-11).
- Brausepulver collusion-wiki-link-shorteners `5_new_yourls_instances.md` —
  YOURLS instance recon (t.mdcdev.me open-creation instance confirmed live
  2026-09-28; bitily.in wiped; yourls.pro dead; yourls.space backlink spam).

## Key finding

Every public goto.unm.edu stats page checked (4/4) and the public
u.ethz.ch stats page carry the agent proxy-wrapper toolkit as HTTP
referrers (jqp, pure.md, md.succ.ai, markdown.new, r.jina.ai, allorigins ×2,
corsproxy.io, proxy.cors.sh, cors.bwa.workers.dev, microlink ×2,
proxymule.com) plus task-family referrers (sec.gov/investor.gov,
api.census.gov, api.datausa.io, pxweb.nso.gov.vn / pxweb.gso.gov.vn =
Vietnam GSO PX-Web statistics API, a new task family) plus cross-venue
referrers (vanderbi.lt, uoft.me, da.gd, is.gd, 2dd.pl, jsonhero.io,
web.archive.org). Best-day spikes land on 2026-06-18 (goto.unm.edu/7t6-o:
1,845 hits; u.ethz.ch/nB1nv: 63 hits). The agents' tooling evidently sent
these as Referer headers when requesting the short links; YOURLS logged
them verbatim — a passive, operator-side fingerprint of the toolkit on
official university infrastructure.

## Workstream C3 (2026-09-28): July 5-6 referrer-row gap + per-URL referrer recovery

**July 5-6 per-day referrer tables: verdict = not publicly retrievable.**
The YOURLS public stats UI exposes only three data surfaces: (a) a decimated
all-time daily series (~6-week sampling, includes zero-hit days — no
2026-07-05/06 point sampled on any of the 4 slugs), (b) last-30d daily
(Aug 30–Sep 28 2026), and (c) per-URL referrer "details" tables with no
per-day drill-down. There is no per-day-per-referrer endpoint in the public
interface, so July 5-6 2026 referrer rows cannot be pulled. Gap remains
structurally unpullable (recorded, not filled).

**Recovered instead (read-only raw-HTML parse, polite pacing): 1,159 full
per-URL referrer rows** — 7t6-o: 740 across 35 hosts; reso: 285/11; urphy21:
77/8; discvr: 57/9 — plus all-time (31 pts/slug) and last-30d daily series.
Evidence: `goto-unm-edu/*_referrer_urls_daily_2026-09-28.json` (4 files;
Census API key values redacted as `[REDACTED]` on 24 rows).

New markers in the per-URL tables:
- `jqp.vercel.app/OAIDATAUSATESTXYZ` — oai + XYZ generated grammar, Data USA
  API test (7t6-o, 1 hit).
- `tinyurl.com/2dhwlfmj` nested inside SIX wrapper chains: allorigins get+raw,
  api.allorigins.win get+raw, jsonhero.io, proxy.cors.sh, corsproxy.io —
  corroborates the benchmark note (vanderbi.lt/is.gd/tinyurl shortlinks inside
  proxy chains).
- `goto.unm.edu/yourls-infos.php/CTXWIN12ZZ0?id=7t6-o` (4 hits) — ZZ-grammar
  probe of the stats endpoint itself.
- `win13=<decimal-nonce>` params on county.json via allorigins (8 rows) —
  decimal nonce variant of the epoch-nonce pattern family.

## Consolidation 2026-09-28 (workstream D)

Absorbed the 3 go.uvm.edu batch3 docs (control venue, University of Vermont)
from index `university-shorteners-batch3` (since retired, per-doc parity
verified). Consolidated `_count` = 15; per-doc `event.dataset` preserved:
university-shorteners 11, university-shorteners-batch3 3,
university-shorteners-batch2 1.

## Closure 2026-09-28 (workstream D)

Consolidated family census complete: bounded set of university YOURLS
instances probed passively (UNM 4 slugs + ETH Zürich + UVM control venue +
2 popcat negatives kept out of the index; batch2 UNM historical detail).
N=15 docs is the natural size — one summary doc per slug/venue plus the
historical-detail pass. ES `university-shorteners` _count=15 verified
(event.dataset: university-shorteners 11, university-shorteners-batch3 3,
university-shorteners-batch2 1). No more university shorteners to sweep
except the quarterly re-probe list recorded in
notes/university-shorteners-batch3-2026-09-28.md.

## Closure 2026-09-28 (workstream C)

Consolidated family index: batch1 11 + batch2 1 + batch3 (go.uvm.edu) 3 = N=15
docs, per-batch provenance preserved in `event.dataset`; batch2/batch3 indices
retired after verified merge (see CONSOLIDATION-2026-09-28.md). The
uoft-shorteners lane recorded clean negatives only (login walls / SEO-spam
slugs) — no ES index by design, documented in the consolidation note. UNM July
5-6 per-day referrer rows remain structurally unpullable (YOURLS public stats
expose no per-day drill-down) — recorded in progress.log, not re-litigated.
ES `university-shorteners` _count=15 verified, schema-drift clean.

## Workstream B session 2 (2026-09-28): ephemeral capture + ETH detail extraction

New evidence files (all under data/university-shorteners/; checksummed in SHA256SUMS):
- `u-ethz-ch/nB1nv_stats_raw_2026-09-28.html` — raw bytes of the public stats page (37,086 B).
- `u-ethz-ch/nB1nv_referrer_urls_daily_2026-09-28.json` — parsed: 28 per-URL referrer rows / 6 hosts,
  31 all-time + 30 last-30d daily points; best day 63 hits on 2026-06-18; created 2020-08-24; 273 hits all-time.
  Key markers: jqp.vercel.app -> da.gd/4qPkK -> SEC regCF_county_2019/2020/2021 (Massachusetts filters);
  `www.sec.gov/files/county.json?NEW81131268=1` (NEW + 8-digit nonce grammar); example.com/test<decimal> canaries.
- `goto-unm-edu/{7t6-o,discvr,reso,urphy21}_stats_raw_2026-09-28.html` — re-pulled raw bytes of the 4 UNM
  public stats pages (ephemeral last-30d window); structure re-validated against the C3 parses.
- `data/university-shorteners-batch3/go-uvm-edu/{-4s0q,tgmtq,xc26}_stats_raw_2026-09-28.html` — control-venue
  raw snapshots (batch3 SHA256SUMS extended to 15 files).

Raw HTML snapshots are checksummed but NOT indexed as ES docs; the parsed JSONs are the indexed evidence.
`build_dataset.py` now emits 12 docs (was 11); ES index `university-shorteners` = 16 docs
(buckets university-shorteners:12 / university-shorteners-batch3:3 / university-shorteners-batch2:1),
`--verify` green (no field drift, unique deterministic IDs).

Negative probes recorded in `progress.log` only (no index): vanderbi.lt (YOURLS 1.5.1, stats login-walled),
go.osu.edu, go.wisc.edu, go.umd.edu, go.ncsu.edu, go.psu.edu, go.rutgers.edu, go.unc.edu (all custom/login-walled),
swish.st (dead), clck.io (retired), da.gd / is.gd (403 Cloudflare) / v.gd / 2dd.pl (no public stats),
urlscan.io search API (403 without key), Wayback CDX (unreachable from VM).

## Defensive takeaway (per standing directive)

Public YOURLS `+`/infos stats pages are an operator-side fingerprint of automation: YOURLS logs full
referrer URLs (including query strings) by default, so proxied exfil chains appear verbatim. Defenders
should (1) set private stats on sensitive instances (UVM's referrer-hiding config is the model),
(2) alert on first-seen proxy-wrapper referrer hosts and referrer URLs carrying jq/JSON-extraction grammar,
(3) treat hit bursts on old low-traffic slugs as anomalies (ETH nB1nv: 0.12/day baseline, 63 hits on
2026-06-18), and (4) snapshot the last-30d window on any alert — it ages out daily and the decimated
all-time series never recovers sub-sampled days.

## July 5–6 UNM retry lane (2026-09-28 ~19:35 UTC)

The July 5–6 per-day/per-referrer rows (UNM 7t6-o) were declared unrecoverable from the live YOURLS
UI (verified: decimated all-time series has no 2026-07-05/06 points; lane-P closed 18:55Z). This lane
retried via archived copies of the four stats pages (`7t6-o`, `discvr`, `reso`, `urphy21`):

- **Wayback CDX retry loop** (`hidden_files/shortener-cdx/`): verified its 12-URL set already contains
  all four UNM `+` stats URLs plus `vbudg` — no additions needed. Still polling every 15 min through
  2026-09-30 12:00 UTC; CDX last probed 503/000 at 19:10 UTC.
- **Common Crawl queued**: `hidden_files/lane12/shortener_cc_job.json` (exact index queries, `+`
  encoded as `%2B`, crawls intersecting 2026-06-01..2026-08-15) +
  `hidden_files/lane12/shortener_cc_sweep.py` (index → WARC range fetch → shared YOURLS row parser →
  per-row explosion, disk-only, dedupe on `labels.event_id`) +
  `hidden_files/lane12/shortener_cc_query.md` (query reference). Lane12 supervisor patched (v4.1)
  to launch it on CC recovery; supervisor restarted 19:21 UTC from the patched file, window intact.
- **Memento aggregators — negative**: `timetravel.mementoweb.org` (http/https) and
  `arquivo.pt/wayback/cdx` return "Empty reply from server" through this egress (same class as the
  web.archive.org blockage; DNS resolves, upstream sends nothing).
- **UNM YOURLS alternate endpoints — negative**: stock YOURLS 1.7.1, server-rendered, no JS data API
  (only `admin/admin-ajax.php`, auth-only, not probed); `yourls-api.php?action=stats&shorturl=7t6-o`
  signature-less → 302 to `/` (no signature-less read path); no dated archive URL pattern on-instance.

No archived stats page has been recovered yet via any angle; no new rows staged. If the CC or
Wayback workers fire, captures land in `data/university-shorteners/wayback-cc/` /
`data/university-shorteners/wayback/` and per-row events append to
`data/university-shorteners-events/university-shorteners-events.jsonl`.

## Schema backfill 2026-09-29

`university-shorteners.jsonl` (12 records) brought to full conformance via
`temp/backfill_w4.py`. Existing `@timestamp`, `event` (dataset
`university-shorteners`), `record_kind`, and all canonical fields kept
verbatim — additive only.

- **record_kind**: unchanged (`yourls_stats_page`, `shortener_info_page`,
  `yourls_stats_detail`).
- **fingerprint**: added (was missing). Identity string:
  `record_kind + "|" + labels["shortener.instance"] + "|" + labels["short_url"]`
  (unique across all 12 rows).
- **labels**: nested objects flattened with dotted keys
  (`pattern_families.<family>`, `referrers.<host>`, `best_day.<field>`,
  `traffic_summary.<field>`); arrays of objects (`daily_all_time`,
  `daily_last_30`, `referrer_urls`) JSON-encoded element-wise into string
  arrays (lossless, reparsable). Two referrer hostnames containing `-` (not
  allowed in label keys) were sanitized to `_`; original key strings kept
  under `labels._keymap.<sanitized_key>`.

## Raw layer 2026-09-29

- `staged_primary/university-shorteners_explicit.jsonl` -> `raw/staged_primary/university-shorteners_explicit.jsonl` and `staged_rollup/university-shorteners-rollup.jsonl` -> `raw/staged_rollup/university-shorteners-rollup.jsonl` (transform intermediates; consumer: scripts/es_unwind_university_shorteners.py). Subdir names preserved; raw layer exempt from event schema.
