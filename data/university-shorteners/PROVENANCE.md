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
