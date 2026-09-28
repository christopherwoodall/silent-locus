# Recon E — rmn.re YOURLS shortener infrastructure (2026-09-27)

Passive recon only. No logins, no brute-forcing, no short-link mass resolution.
All facts verified 2026-09-28 ~02:40 UTC unless noted.

## 1. Service status: LIVE and fully open

- `http://rmn.re/` and `https://rmn.re/` both serve the YOURLS public front page.
  Fetched live 2026-09-28: **"Display 1 to 15 of 764 URLs. Overall, tracking 764
  links, 84,022 clicks, and counting!"**
- The public index exposes, per link, with **no authentication**: short slug,
  full original URL, creation date, creator **IP address**, click count.
- The **admin interface is reachable without login**:
  `https://rmn.re/admin/index.php?search_in=all&sort_by=timestamp&sort_order=desc&page=2&perpage=15&total_pages=6&search`
  renders the full link table (verified page 2 live). Search engines index the
  admin pages, confirming long-term open exposure.
- Per-link public stats pages: `https://rmn.re/<slug>+` (e.g. `https://rmn.re/he+`,
  `http://rmn.re/hc+`, `https://rmn.re/hj+` — all indexed with full traffic stats).
- `yourls-api.php` exists: bare GET returns HTTP 400 (YOURLS's normal
  "missing action" response — endpoint present and reachable).
- Homepage banner: *"Dear Users ATTENTION!!! Porn and malicious links will be
  deleted due our 'Terms Of Use' conditions. For any question email:
  support@rmn.re"*
- Link-count drift shows **active current use**: 753 links / 78,178 clicks
  (search-engine cache) → 757 / 79,939 (2026-09-06, per
  swarm-ai-research/wiki-agent-swarm-incident) → **764 / 84,022** (live fetch).
  The shortener is still growing today.

## 2. DNS notes

- Sandbox resolver returns `198.18.30.117` for rmn.re (RFC 2544 benchmarking
  range — egress sinkhole, not the real address).
- Direct queries to 8.8.8.8 / 1.1.1.1 / 9.9.9.9 were REFUSED by the egress proxy.
- Liveness confirmed through the browser egress path instead. No NS/MX/TXT
  obtainable from this environment; treat as unverified, not as evidence of
  suspension.
- Cert history (crt.sh): not retrievable from here — no verbatim crt.sh URL
  available via search; HTTPS is served (live cert details not inspected).

## 3. Campaign-relevant slugs on the live front page (page 1)

| slug | target | clicks |
|---|---|---|
| `zzmasscounty` | `http://zzmasscounty` | 53 |
| `fieldnotes` | `https://public-board.com/llms.txt` | 42 |
| `centaurinvitation` | `https://thecolony.ai/for-agents` | 27 |
| `strangeanchor` | `https://strangeanchor.khazars.wiki/index.html` | 28 |
| `lx` | `https://example.org/agent-verify-test` | 27 |

Agent-board surfaces (`public-board.com/llms.txt`, `thecolony.ai/for-agents`,
a `.wiki` host) sit on the same open shortener as the campaign slugs.

## 4. The 192 viz.aihw.gov.au short-link targets (from preserved log)

Source: `data/wiki_shortener_detail.json` (499 entries). **Do not mass-resolve;
analysis below is from the preserved log targets only.**

- **All 192 target one Tableau workbook**: `PBSdashboardallATC1-ATC2medicines-Agegroup`
  (PBS = Pharmaceutical Benefits Scheme medicines dashboard) on `viz.aihw.gov.au`.
- **All created in a ~10h burst: 2026-06-17 05:49:50Z → 15:32:37Z.**
- Export-format variants of the same dashboard:
  `.pdf` (120), `.png` (45), bare view (9), `.csv` (3), `.xlsx` (1),
  `.twb` workbook downloads (4 variants), `bootstrapSession/sessions/` endpoints (2).
- **Parameter-surface fuzzing**: dozens of parameter-name variants for the same
  LGA/State filters — `LGA`, `Parameters.LGA`, `LGA_NAME21`, `LGA_NAME_2023`,
  `LGA_NAME_2021`, `State/Territory`, `Jurisdiction`, `Parameters.Jurisdiction`,
  `Parameters.Select an LGA:`, `Parameters.Select medicine group ATC Level 2`,
  plus Tableau embed params (`:showVizHome`, `:toolbar`, `:showTabs`, `:refresh`,
  `:size`, `:embed`, `:apiID`, `:loadOrderID`, `:format`, `:render`). Systematic
  probing of the workbook's parameter names, not casual linking.
- **Beacon marker**: one slug (`pbsweb95618278`, 22 clicks) carries
  `bridge=pbsweb95618278` — the short-link slug echoed back as a query parameter.
- Slug grammar: 2-letter prefix + digits (`sb`×40, `lb`×15, `fb`×15, `zz`×12,
  `pa`×10, `ct`×9, …) plus format-descriptive slugs (`zpng233166`, `zcsv891673`,
  `pbsweb95618278`, `meth53675634`).
- Creator ip16s: Azure ranges (`20.69`, `20.165`, `20.29`, `20.9`) and `57.154`.
- 5,679 total clicks across the 192; top slugs 37–41 clicks each; none at zero.

## 5. Assessment

- rmn.re is a **fully open YOURLS install doubling as a public ledger**: every
  link, target, creator IP, and click count is world-readable, and the admin
  panel needs no login. It is actively used right now.
- The 192-link AIHW burst is the shortener side of the hunt's AIHW
  medicines-dashboard thread (Tableau export beacons + parameter fuzzing +
  slug-echo bridge param), timestamped 2026-06-17.
- vanderbi.lt (per swarm-ai-research/wiki-agent-swarm-incident) is the
  corpus-verified YOURLS for the DSE wiki export; rmn.re is the parallel,
  uncorroborated-by-export instance — but it is live, open, and holds
  campaign-grammar slugs.

## Source URLs

- http://rmn.re/ (live front page, fetched 2026-09-28)
- https://rmn.re/admin/index.php?search_in=all&sort_by=timestamp&sort_order=desc&page=2&perpage=15&total_pages=6&search (open admin, fetched live)
- https://rmn.re/he+ , http://rmn.re/hc+ , https://rmn.re/hj+ (public per-link stats, indexed)
- https://github.com/swarm-ai-research/wiki-agent-swarm-incident/commit/aea40cfee81475736a8bdb31c04f0f784e0bafda (rmn.re noted as live open YOURLS admin, 2026-09-06)
- data/wiki_shortener_detail.json (499-entry preserved log)
