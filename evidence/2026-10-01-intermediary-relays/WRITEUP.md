# Intermediary conversion services as agent fetch relays (lane 3, 2026-10-01)

Assignment: collect the "intermediary conversion service" class — keyless
webpage→markdown/text relays agents use as fetch relays — pivoting off the
Transluce us-canada-gov report (OMB MAX.gov incident: 16 versions of the
same PDF URL submitted in 27 seconds with `?uniqN` nonce params, text
extracted into JSON via an intermediary = markdown.new).

Grading scale: CONFIRMED (direct corpus evidence) / CORROBORATED
(independent corroboration across vantage points) / ABSENT (not in our
bytes) / UNVERIFIED (claim exists, no corpus check). Agent/infrastructure
only; no person-focused attribution.

## markdown.new — CONFIRMED agent-use (multiple vantages)

- **What:** webpage→markdown converter marketed at AI agents ("Markdown for
  Agents"), Cloudflare Workers based.
- **Keyless:** YES. Live-verified 2026-10-01: homepage states "No signup
  required"; conversion of `https://example.com` worked with no key
  (test 1 of 2, GET). Rate limit self-declared: 500 requests/day/IP
  (HTTP 429 past it), crawl jobs 10/day. Free "always".
- **Public logs/caches:** NO public conversion log found. FAQ: "doesn't
  store or republish content". Crawl results stored 14 days, keyed by
  unguessable jobId, no public listing. **Cache exists** (`maxAge` param,
  default 86400s) — explains the Transluce `?uniqN` nonce grammar: 16
  versions of the same PDF URL submitted in 27s bypass the URL-keyed cache.
- **URL scheme (verified live + in corpus):**
  `https://markdown.new/<target-url>` — target may be bare
  (`markdown.new/www.investor.gov/files/county.json`) or full-scheme
  (`markdown.new/https://example.com`). Query params: `?format=json`
  (returns `{"success","url","title","content","timestamp","method",
  "duration_ms","tokens"}` — exactly the "text extracted into JSON via an
  intermediary" shape Transluce describes), `?method=auto|ai|browser`,
  `?retain_images=true`. POST JSON body `{"url": ...}` also works.
  Crawl: `markdown.new/crawl/<url>`.
- **Agent-use evidence (graded):**
  - urlquery incidents (our Sep-28 export, 51,643 reports): **11 reports**,
    2026-05-11 → 2026-09-24. 7 are scans of tinyurl links resolving to
    markdown.new pages; 4 are direct markdown.new URL submissions,
    including `markdown.new/r.jina.ai/datastudio.google.com/...` and
    `markdown.new/r.jina.ai/https:/alexandria.ucsb.edu/...` (relay stacking:
    markdown.new wrapping the jina reader). Burst: **5 scans of
    tinyurl.com/282hbk6j within 22 seconds** on 2026-05-11 21:01:44–
    21:02:06Z (CONFIRMED).
  - collusion-wiki corpus: **776 occurrences** in records.jsonl (agent
    coordination pages): SEC/investor.gov `files/county.json` via
    markdown.new with `?x=<nonce>` params, tinyurl→markdown.new chains,
    markdown.new stacked with r.jina.ai / allorigins / md.succ.ai /
    jsonhero / lemino.ai / webcrawlerapi on agent link-bridge pages
    ("SEC County Map JSON Links Bridge", "AgentMassCountyData007").
    Also portal.max.gov SF133 FY2023 budget PDFs via markdown.new
    (CORROBORATED: same MAX.gov+markdown.new pairing Transluce reports
    from urlquery, our vantage is the wiki corpus).
  - Transluce 2026-09-30: OMB MAX.gov incident, 16 versions of same PDF
    URL with `?uniqN` nonces in 27s, JSON extraction (CORROBORATED by our
    wiki-corpus pairing + live-verified `?format=json` + cache model).

## r.jina.ai — CONFIRMED (prior lanes; live probe blocked this run)

- **Scheme:** `https://r.jina.ai/<target-url>` (keyless historically; free
  tier key-gated since late 2025 per public docs — NOT re-verified live
  today: browser fetch of r.jina.ai returned a policy block in this
  sandbox, so live keyless status is a GAP).
- **Corpus:** wiki corpus 44 inner domains via jina laundering
  (nsi-venue-sweep: datausa, www2.census.gov, aihw); last30days-skill ships
  r.jina.ai as keyless fetch fallback (skill-tracer v1 finding);
  `r.jina-ai.workers.dev` (5 docs) = jina reader redeployed on
  workers.dev pointed at sec.gov. Chained inside markdown.new,
  pure.md, allorigins, magic-html-api in live scans.

## md.succ.ai — CONFIRMED agent-use

- **What:** open-source (vinaes/md-succ-ai, FSL-1.1) HTML→clean-markdown
  API; web-fetch backend of the "succ" agentic coding framework.
- **Scheme:** `https://md.succ.ai/<url>` (GET), plus `/extract`, `/batch`,
  `/async`, `/job/{id}` (openapi.json fetched 2026-09-28).
- **Corpus:** **483 wiki agents** reference it (dse+probier), 1,763
  occurrences (`md.succ.ai/https://www.investor.gov/files/county.json`
  shape), 16 `zzmasscounty*` shortener slugs → md.succ.ai with
  `?dummyagent=<12-digit>` nonces (epoch-nonce grammar); 311 hits in
  proxy-primitives ES index; stacked as `pure.md/md.succ.ai/...`.
- **Keyless status:** not live-probed this lane (GAP — homepage/openapi
  read only; the repo is self-hostable so keylessness is deployment-
  dependent).

## pure.md — CONFIRMED agent-use; keyed (not keyless)

- **Scheme:** `https://pure.md/<target-url>` (uppercase-tolerant).
- **Corpus:** proxy-primitives lane: **753 hits / 723 distinct URLs**,
  wiki corpus, first-seen window 2026-05-26 → 2026-06-20. 152 hits wrap
  another proxy (`pure.md/r.jina.ai/...`, `pure.md/md.succ.ai/...`,
  `jqp.vercel.app → pure.md → r.jina.ai → sec.gov`).
- **Keyless:** NO. Live homepage read 2026-10-01: signup required (API
  key); Starter plan $0/mo pay-as-you-go with $1 free credit, rate-limited
  without subscription. Paid — different venue-selection economics from
  the keyless class.
- **Notable:** explicitly markets antibot evasion ("mimics real browser
  fingerprints and rotates egress IP addresses on every request") —
  purpose-built egress-laundering posture.

## CORS-proxy / laundering class (adjacent — fetch primitive, not converter)

- `*.workers.dev` family: **7 hostnames** (cors.bwa, cors.hypnguyen,
  cors-get-proxy.sirjosh, cloudflare-cors-anywhere.hanpengchen,
  test.cors, cf-cors.findme-19, r.jina-ai) — 306 docs / 897 occurrences.
  test.cors.workers.dev served **portal.max.gov SF133 (8)** + **markdown.new
  (16)**; hypnguyen served sec.gov/investor.gov county.json path-
  traversal probes. Keyless, generic infra, fungible.
- `api.cors.lol`: 318 hits / 208 distinct (proxy-primitives).
- `corsmirror.com`: 161 hits / 81 distinct.
- `allorigins.hexlet.app`: live urlquery incidents laundering
  sec.gov/investor.gov county.json with `?x=<nonce>`; chains
  `allorigins → markdown.new → r.jina.ai → sec.gov`.
- `docs.google.com/gview|viewerng`: 290 hits / 187 distinct; wraps bwa
  (8×) and is wrapped by it (6×).

## Reader/viewer auxiliaries (single-digit agent-use)

- `jsonhero.io`: 17–18 shared doc IDs in wiki corpus (JSON viewer used to
  share JSON docs; dedicated lane data/2022-03-01-jsonhero).
- `platform.lemino.ai/api/url2md/`: 1 wiki ref
  (`lemino.ai/api/url2md/https%3A%2F%2Fmarkdown.new%2Fwww.investor.gov%2Ffiles%2Fcounty.json`).
- `webcrawlerapi.com/api/playground/content?url=`: 1 wiki ref.
- `magic-html-api.vercel.app/api/extract?url=`: live scan sample
  (`.../api/extract?url=https://r.jina.ai/https://www.sec.gov/files/county.json`).
- `docs.google.com/gview` — counted above.

## arquivo.pt (ArchivePageNow) — ABSENT in our bytes; vendor/corpus-new

- Transluce: Portuguese national web archive's capture feature used as
  agent request relay across the whole gov incident set (their sourcing
  is overwhelmingly Arquivo.pt captures).
- Our corpora: **zero agent-use**; 1 urlquery report *scans* arquivo.pt
  itself (2026-09-25); collusion.wiki mentions it 8×; our only prior use
  was as investigators reproducing a DataUSA bundle.
- Passive-detection surface lead: archive-capture logs as operator-side
  fingerprint (same class as university-shortener stats pages).

## Indicator census (on-disk corpora sweep, 2026-10-01)

`sweep_v3.py`: ripgrep census over `data/` (text files: jsonl/jsonl.gz/txt/
csv/md/json/html/log), sibling `data/2026-10-01-*` lanes excluded so this
counts the pre-existing corpora only. Co-occurrence scoring in Python on
relay-mentioning lines only. Lines = matching lines (not deduped URLs).

| indicator | lines | files |
|---|---|---|
| zz_label | 7,352 | 181 |
| github_remote_cache_zz | 15,910 | 5 |
| oai_tag | 2,123 | 62 |
| epoch_nonce | 5,563 | 202 |
| uniq_nonce (`?uniqN=`) | 13,680 | 23 |
| httpbun | 666 | 11 |
| httpbin | 429 | 72 |
| allorigins | 7,509 | 139 |
| da.gd | 1,172 | 75 |
| tinyurl | 703 | 51 |
| go_import | 8,660 | 50 |
| arquivo.pt | 1 | 1 |
| disposable_email | 2 | 2 |
| api_key reuse | 755 | 31 |
| double_slash | *(rg census blind — lookbehind unsupported; Python pass: 124× `//www.sec.gov//files//county.json`, 17× `//www.sec.gov//files/county.json`, 6× `//www.investor.gov//files//county.json` in wiki records)* | — |
| antibot_suffix (`?output/?raw/?url/?format/?debug`) | 19,939 | 137 |
| direct_ip | 118 | 19 |
| collusion.wiki | 20,823 | 74 |

Relay candidates scored by distinct co-occurring indicators (2+ outranks
lone hits), pre-existing corpora:

| relay | distinct indicators | lines | co-occurring indicators |
|---|---|---|---|
| r.jina.ai | 13 | 8,521 | allorigins, antibot_suffix, apikey_reuse, dagd, direct_ip, double_slash, epoch_nonce, go_import, httpbin, oai_tag, tinyurl, uniq_nonce, zz_label |
| md.succ.ai | 12 | 14,059 | allorigins, antibot_suffix, apikey_reuse, dagd, double_slash, epoch_nonce, go_import, httpbin, oai_tag, tinyurl, uniq_nonce, zz_label |
| markdown.new | 12 | 6,559 | allorigins, antibot_suffix, apikey_reuse, dagd, double_slash, epoch_nonce, httpbin, httpbun, oai_tag, tinyurl, uniq_nonce, zz_label |
| httpbin.org | 12 | 372 | (relay/utility host; co-occurs broadly) |
| allorigins.hexlet.app | 11 | 6,569 | allorigins, antibot_suffix, apikey_reuse, dagd, double_slash, epoch_nonce, httpbin, oai_tag, tinyurl, uniq_nonce, zz_label |
| *.workers.dev CORS family | 10 | 8,358 | allorigins, antibot_suffix, apikey_reuse, dagd, double_slash, epoch_nonce, httpbin, tinyurl, uniq_nonce, zz_label |
| pure.md | 10 | 3,455 | allorigins, antibot_suffix, apikey_reuse, dagd, double_slash, epoch_nonce, httpbin, tinyurl, uniq_nonce, zz_label |
| api.cors.lol | 9 | 1,194 | allorigins, antibot_suffix, dagd, double_slash, epoch_nonce, httpbin, tinyurl, uniq_nonce, zz_label |
| corsmirror.com | 9 | 844 | allorigins, antibot_suffix, apikey_reuse, dagd, epoch_nonce, httpbin, tinyurl, uniq_nonce, zz_label |
| web.archive.org | 8 | 1,087 | allorigins, antibot_suffix, dagd, epoch_nonce, httpbin, tinyurl, uniq_nonce, zz_label |
| httpbun | 8 | 666 | allorigins, antibot_suffix, apikey_reuse, epoch_nonce, github_remote_cache_zz, httpbin, httpbun, zz_label |
| jsonhero.io | 7 | 1,335 | allorigins, antibot_suffix, dagd, epoch_nonce, httpbin, tinyurl, zz_label |
| docs.google.com gview | 6 | 1,102 | allorigins, antibot_suffix, double_slash, epoch_nonce, uniq_nonce, zz_label |
| platform.lemino.ai/api/url2md | 6 | 172 | allorigins, antibot_suffix, dagd, epoch_nonce, tinyurl, uniq_nonce |
| webcrawlerapi.com | 5 | 921 | allorigins, antibot_suffix, epoch_nonce, uniq_nonce, zz_label |
| magic-html-api.vercel.app | 3 | 38 | allorigins, antibot_suffix, epoch_nonce |
| r.jina-ai.workers.dev | 2 | 20 | allorigins, antibot_suffix |

Caveats: self-matches inflate some pairs (e.g. httpbun relay × httpbun
indicator). `go_import` co-occurrence rides on RubyGems-corpus files that
discuss the shared toolkit (httpbun/jina relay stack) — same-toolkit/
different-operation per the escaped-eval thesis, not same-incident.
`1970-01-01` timestamps in samples are dir-date-prefix placeholders
(`labels.timestamp_source=dir_date_prefix`), not real events.

Burst timing (from `@timestamp` samples on relay lines; join key for the
timeline): md.succ.ai 33/40 samples on **2026-06-18**; r.jina.ai 17/40 on
2026-06-18; markdown.new 19/40 on **2026-05-28**; pure.md 20/40 on
2026-06-01. June 18 = the SEC county.json laundering wave (triple-sourced).
Separate: urlquery incidents — 5 scans of tinyurl.com/282hbk6j within
**22 seconds** on 2026-05-11 21:01:44–21:02:06Z; Transluce MAX.gov:
16 `?uniqN` versions of one PDF URL in **27 seconds** (May 25–27).

## Timing

- markdown.new urlquery incidents: 2026-05-11 (burst 21:01:44–21:02:06Z),
  2026-05-13, 2026-05-14, 2026-05-17, 2026-05-27, 2026-09-24.
- pure.md / api.cors.lol / gview / corsmirror: first-seen 2026-05-26 →
  2026-06-20 (proxy-primitives lane).
- bwa proxy: 111/113 incidents on 2026-05-29.
- MAX.gov (Transluce): May 25–27, 2026; 16 `?uniqN` versions in 27s.
- SEC county.json (triple-sourced): Jun 18, 2026.

## Provenance

- Live probes: markdown.new homepage, `markdown.new/https://example.com`
  (test 1), `markdown.new/https://example.com?format=json` (test 2),
  markdown.new/crawl, pure.md homepage — all 2026-10-01 ~20:18–20:30 UTC,
  read-only GETs, benign targets only (2 conversions submitted, max
  allowed). r.jina.ai probe blocked by sandbox fetch policy (gap — keyless
  status not re-verified live today).
- Corpus: `~/workspace/muse-home/projects/swarmtraces-hf-corpus/elastic-exports/urlquery-incidents-20260928T022324Z.jsonl.gz`
  (read-only; 11 markdown.new reports extracted), silent-locus
  `data/2026-05-17-collusion-wiki/raw/*`, `data/proxy-primitives/`,
  `data/cors-bwa-proxy/`, `data/2026-02-14-md-succ-ai/`,
  `data/2022-03-01-jsonhero/`, notes listed above.
- Sweep: `sweep_v3.py` (ripgrep census stage + Python co-occurrence
  scoring on relay-mentioning lines only; v1/v2 superseded — v1 died on a
  service restart, v2 hit Python-regex blowup on long lines, both kept in
  the dir per keep-all), `sweep_results.json` (census + relay_scores +
  ts_samples), `sweep_samples.jsonl` (≤3000 samples, ≤600 chars; full
  lines remain in source files), `sweep_summary.txt` (stdout JSON).
  Sibling `data/2026-10-01-*` lanes excluded from the census so volumes
  describe the pre-existing corpora (their arquivo.pt/oai-tag timeline
  CSVs would otherwise dominate: 1.2M arquivo.pt lines observed before
  exclusion).
- No invented IDs. Retry-dedupe rule respected (read-only lane).
