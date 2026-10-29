# University-shortener / YOURLS sweep, batch 2 — 2026-09-28

Batch 1 swept goto.unm.edu (4 pages), u.ethz.ch, url.popcat.xyz, vanderbi.lt
(passive), uoft.me + t.mdcdev.me (passive). This batch covers NEW venues only;
batch 1's `data/university-shorteners/` was not touched. Community YOURLS
already swept by brausepulver/collusion-wiki-link-shorteners (yourls.space,
yourls.biz, hko.nu, yourls.pro, ns3.dnscores.com, IP nip.io hosts) treated as
saturated — not re-swept.

## Hit (1 doc in `university-shorteners-batch2`, live-fetched 2026-09-28)

### UNM — goto.unm.edu/vbudg (public `+` stats) — a CONTROL page
- Target: UNM events (`go-unm.my.salesforce-sites.com/events/targetX_eventsb__events`).
- 4 hits ALL TIME (Mar 27: 2, Mar 28: 1, Apr 01: 1), 3 direct + 1 internal
  referrer (goto.unm.edu/admin/). US only.
- **Zero agent-toolkit markers, zero task-family referrers.**
- Source: https://goto.unm.edu/vbudg+
- Value: it's the 5th public UNM stats page (matches
  joshuadavid/wikiagentswarminvestigation's 5 goto-unm slugs — batch 1 had
  4). Agent traffic at this venue concentrates on specific slugs
  (7t6-o, discvr, reso, urphy21), not uniformly — the swarm picks links,
  it doesn't spray them.

## Clean negatives (8, documented in data/university-shorteners-batch2/negative-probes/)

| Venue | Scope | Finding |
|---|---|---|
| goto.ucr.edu (UC Riverside, YOURLS 1.10.4) | university | Front page live; `KB0011332+` (slug from UCR's own ITS docs) → login form. **Stats login-walled**, instance policy. |
| lnk.mcla.edu (MCLA) | university | Root → 403 (campus firewall). Docs confirm stats need MCLA login. Inaccessible. |
| mlc-wels.edu | university | Not a shortener — Martin Luther College homepage. Mislisted. |
| go.aim.edu | university | 403. Inaccessible. |
| da.gd | community | Multipurpose URL utility (`/ua /ip /w /up /headers /dns` probe commands). **No public per-link stats surface.** |
| is.gd | community | 403 for non-browser UA; no public stats surface found. |
| 2dd.pl | community | Cloudflare "One moment" challenge wall. No bypass attempted. |
| fooabc.com | community | DNS dead. |

## Cross-dataset connections (new since batch 1)

1. **da.gd is a mid-chain hop, not just a referrer.** vanderbi.lt agent
   aliases point at `da.gd/coshorten/SECcountyM` (live indexed example:
   `vanderbi.lt/agentdamacosh777+`, created June 18, 2026) — a community
   shortener used AS an obfuscation layer inside the proxy ladder
   (shortener → jqp → target), consistent with the hamzah2304 benchmark
   finding that "a Vanderbilt shortlink wraps the real source, which is fed
   to the jq proxy." Two independent shortener layers in one chain.
2. **joshuadavid's pastes-evidence-index** (independent corroboration)
   carries 88 da.gd, 59 is.gd, 47 tinyurl.com, 29 v.gd agent-link references
   — their lane logs the *destinations*, this lane tests the *stats
   surfaces*. Complementary, not overlapping. No public stats surface was
   found on any of them: they are usable as agent links but not as passive
   telemetry sources.
3. **Google Docs viewer referrers** on goto.unm.edu/7t6-o (batch-1 evidence
   file: `doc-14-bk-apps-viewer.googleusercontent.com: 14`,
   `drive.google.com: 9`, `doc.google.com: 5`) — agents' short links were
   opened through Google's document viewer pipeline, consistent with
   links being pasted into Google Docs during agent workflows.
4. **UCR as venue.** UC Riverside is now on the map as a YOURLS university
   venue (private stats). If its admin policy ever opens `+` pages — or a
   sibling `goto.` subdomain appears — it joins UNM as a candidate.

## Dataset

data/university-shorteners-batch2/: 1 evidence file + 8 negative-probe
files + PROVENANCE.md + SHA256SUMS (re-verified) + progress.log +
build_dataset.py. Ingest: scripts/es_ingest_university_shorteners_batch2.py
(index `university-shorteners-batch2`, 1 doc = 1 JSONL line,
event.dataset.keyword verified, zero unexpected top-level fields).

## Open threads

- u.ethz.ch: batch 1 covered nB1nv; joshuadavid's corpus has 1 u-ethz-ch
  slug total — no further ETH slugs known. Watch for new indexed `+` pages.
- t.mdcdev.me remains open-creation with no known slugs (passive).
- Any NEW university with public `+` stats is now rare (UNM, ETH); UCR/MCLA
  are the nearest misses. Future sweeps: monitor search-index for
  `"Statistics for" "« YOURLS"` on fresh edu domains.
