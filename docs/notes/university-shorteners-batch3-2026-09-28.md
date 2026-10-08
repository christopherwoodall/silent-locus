# University-shortener / YOURLS sweep, batch 3 — 2026-09-28 (workstream B)

Batches 1–2 swept goto.unm.edu (5 pages), u.ethz.ch, url.popcat.xyz,
vanderbi.lt (passive), uoft.me + t.mdcdev.me (passive), goto.ucr.edu
(login-walled), lnk.mcla.edu / go.aim.edu (403), da.gd / is.gd / 2dd.pl /
fooabc.com (community). This batch covers NEW venues only; batches 1–2
untouched.

## Hit (3 docs in `university-shorteners-batch3`, live-fetched 2026-09-28)

### UVM — go.uvm.edu (University of Vermont, YOURLS 1.10.3) — a CONTROL venue
- Public `+` stats pages confirmed OPEN on 9 live slugs. Indexed `~`
  preview pages on the two 2013 slugs (`go.uvm.edu/-4s0q~`,
  `go.uvm.edu/tgmtq~`); freshest doc-sourced slug `xc26` (created
  2026-09-24, UVM cross-country team store) also has live public stats.
- Slugs indexed as docs: `-4s0q` (2013 Safari Books link, 266 hits
  all-time), `tgmtq` (2013 UVM security-blog link, 334 hits all-time),
  `xc26` (1 hit). Six more doc-sourced slugs (may3, vtpitchchallenge,
  myuvm, sublet, phcourses, vk62t) checked live — all clean, recorded in
  progress.log, not indexed.
- **Zero agent-toolkit markers, zero task-family markers on every page.**
- Sources: https://go.uvm.edu/-4s0q+ , https://go.uvm.edu/tgmtq+ ,
  https://go.uvm.edu/xc26+
- **KEY CAVEAT: UVM's public stats expose traffic statistics + traffic
  LOCATION only. The "Traffic Sources" (referrers) section is owner-only —
  per UVM's own KB article `url-shortener-go-uvm-edu` (updated 2026-04-09),
  referrers are listed under "View link statistics", which requires a UVM
  NetID + Duo MFA login at /admin.** So go.uvm.edu confirms the
  public-`+`-stats surface on a fourth university instance, but it CANNOT
  leak the agent proxy-stack referrer fingerprint. Indexed as a control
  (public-stats venue), not a fingerprint hit. This also explains why the
  UVM docs were found via the blocklist + indexed preview pages rather
  than via agent referrer pivots.

## Clean negatives (5, in data/university-shorteners-batch3/negative-probes/)

| Venue | Scope | Finding |
|---|---|---|
| go.sjf.edu (St. John Fisher) | university | Root → 302 → www.sjf.edu homepage. **Shortener retired**; no stats surface. |
| s.wnmu.edu (W. New Mexico) | university | DNS dead (no A record). |
| linktest.lse.ac.uk (LSE) | university | 403. Inaccessible. |
| test.yourls.org | community | Official YOURLS test instance unreachable (corroborates brausepulver). |
| 1aas.com | community | YOURLS live, front page public ("Top 10 Links"), but `gum+` (top link, 19k clicks) → **login wall**. Stats login-walled, instance policy. Content is SEO/backlink-farm spam (t.mdcdev.me profile). |

## Cross-dataset connections (new since batch 2)

1. **Stats-policy taxonomy emerging across the four university YOURLS.**
   UNM (referrers public) and ETH (referrers public, peak-day spikes) are
   the fingerprint-leaking class; UVM (referrers owner-only) and UCR
   (`+` pages login-walled entirely) are the locked class. The fingerprint
   technique works only on the leaking class — currently 2/4 universities.
   When hunting new venues, the first test is the stats policy, not just
   whether YOURLS is installed.
2. **UVM creation requires NetID + Duo MFA** (per the UVM KB) — same
   restricted-creation model as UCR. The agents would need compromised or
   shared credentials to plant links here; no evidence of planted links
   was found (no June-2026 spikes, no agent grammars).
3. **go.sjf.edu is the second retired university shortener on record**
   (the first: bitily.in, wiped). University shortener domains churn —
   today's negative can be a dead end or a parked domain tomorrow; worth
   re-probing on a quarterly cadence alongside the saturated-community
   list (yourls.space/biz, hko.nu, yourls.pro).

## Dataset

data/university-shorteners-batch3/: 3 evidence files (go-uvm-edu/) +
5 negative-probe files + pattern-sweep.json + PROVENANCE.md + SHA256SUMS
+ progress.log + build_dataset.py. Ingest:
scripts/es_ingest_university_shorteners_batch3.py
(index `university-shorteners-batch3`, 3 docs,
event.dataset.keyword verified, zero unexpected top-level fields).

## Corrections to existing datasets (this lane)

- data/uoft-shorteners/PROVENANCE.md Sources table listed only 4 of the 7
  t.mdcdev.me evidence files; added the 3 missing rows
  (bayanescortdiyarbakr401683_plus, hkigaprw_plus, i2mrjnck_plus). No data
  files were changed — docs-only fix.

## Open threads

- t.mdcdev.me remains open-creation with no agent slugs seen (passive).
- Quarterly re-probe list: go.sjf.edu, bitily.in, the saturated community
  instances — domain churn is real in this space.
- Future venue hunting: the blocklist→probe→search-index pipeline works;
  next sources to try are other public shortener blocklists and
  `"Statistics for" "YOURLS"` title-indexed pages on fresh edu domains.

## Consolidation 2026-09-28 (workstream D)

Merged into the consolidated `university-shorteners` ES index (canonical
deterministic `_id`, per-doc parity verified); `university-shorteners-batch3`
index retired. Consolidated `_count` = 15. `scripts/es_ingest_university_shorteners_batch3.py`
is retained for provenance but is no longer the live ingest path — the
canonical script is `scripts/es_ingest_university_shorteners.py`, which only
loads the base JSONL; batch3 docs were merged via a one-off deterministic bulk
load (same ID scheme).
