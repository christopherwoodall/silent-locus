# Lane E — 83-gem June-18 reconciliation (2026-09-27/28)

## What was asked

The thecolony.ai lane (centaur's post) described an 83-gem June-18 segment —
hub-and-spoke around `amdwc56692`, 38,878 downloads — said to reconcile with
the JFrog inventory's June-18 segment. Lane E was to extract the exact 83
names, cross-reference JFrog / Diffend / wiki corpus, and land a
reconciliation dataset.

## Key finding: the thecolony data does NOT contain the 83-name list

centaur's post gives aggregate figures (83 gems, 17:53–20:51Z window,
38,878 downloads, dependency edges) but names only a handful of examples.
The incident-wiki section 3 names examples too (`y----00prx90485`,
`x--00cfmapjson726`, `mapanchorcf202704`, `adep97117`, `ultimate4834`,
`method2088`). The enumerated source — `rubygems.org/api/v1/owners/
ulinkqy8py3mp/gems.json` — now returns `[]` (all 83 yanked; verified
2026-09-28). The September-4 snapshot that centaur enumerated from is not in
our data.

## Reconstruction method (grammar-based, all tool-evidence)

The JFrog GemStuffer report's own window table says June 18 = 83 packages.
The JFrog inventory CSV carries no per-row dates, so the 83 were isolated by
June-family name grammar (families named in centaur's post and the incident
wiki):

- `[a-z]----00proxyNNN` (5), `[a-z]----00prxNNNNN` (18),
  `[a-z]--00cfjsonNNNNN` (22), `[a-z]--00cfmapjsonNNN` (3),
  `[a-z]----00cfproxyNNNNN` (3), `[a-z]--00cfproxyNN` (1),
  `[a-z]---00proxyNN` (1), `[a-z]---00cfshape(s)NNNNN` (3),
  `amdapiNNNNNN` (4), `amdvarNNNNNN` (9), `amdmoreNNNNNN` (5),
  `amdwcNNNNN` (2), `amdNNNN` (1, bare), `adepNNNNNN` (2),
  `mapanchor*` (1), `wctest73410` (1) = **81**
- plus the two grammar-invisible random-suffix names cited in the incident
  wiki (`ultimate4834`, `method2088`) = **83 exactly**

Sanity checks: every other JFrog name containing `00prx/00cf/00proxy/amdwc/
adep/mapanchor/wctest/ultimate/method` is accounted for (zero unassigned);
the only other `amd`-containing names (`lamdoc*`, `sm8230mamd`, `zjiamd3`)
are May-burst names, correctly excluded.

## Cross-reference results

| Source | Coverage |
|---|---|
| JFrog inventory (`rubygems-goimport-campaign`) | **83/83** (all, with Xray IDs + versions) |
| Diffend corpus (618 May gems) | **0/83** — clean wave separation |
| collusion.wiki gem bridge (2026-09-28 explorer download) | **79/83** have full metadata records |
| Our Wayback June metadata (`gem-june18-wayback.jsonl`) | 16/83 |
| thecolony.ai direct name mentions | ~7 example names only |

Notably, the collusion.wiki explorer download (generated 2026-09-28) contains
full gem-metadata records for 79 of the 83 — homepage_uri, info text —
meaning the wiki corpus references far more than the "~23" the thecolony
write-ups claimed. The wiki-side count was a stale figure; our own bridge
artifact is the better evidence. The 4 bridge-missing names:
`amdwc51950`, `wctest73410`, `ultimate4834`, `method2088`.

## Hub-and-spoke: partially corroborated, edges unverified

- `amdwc56692` (hub) is in the JFrog inventory (XRAY-1077977, 0.0.1). ✓
- `amdwc51950` in JFrog inventory with versions `0.0.1;0.0.2` — the ONLY
  multi-version gem in the 83 — matching centaur's "amdwc51950 v0.0.2 declares
  a runtime dependency on amdwc56692" claim exactly. Independent
  corroboration of the spoke claim's version detail. ✓
- `wctest73410` in JFrog inventory (XRAY-1079154). ✓
- The dependency edges themselves have NO tool evidence anywhere: no
  gemspec contents for these gems in Diffend, the JFrog CSV, or the wiki
  bridge. centaur-reported, still open.

## Grammar pattern sweep (see data/gem83-reconciliation/pattern-sweep.txt)

- Zero epoch-style suffixes in the June segment (May corpus uses them
  heavily) — numeric suffixes are short (2–6 digits: 726, 57431, 56692).
- Dash padding is family-specific: 4-dash on proxy/prx/cfproxy, 2-dash on
  cfjson/cfmapjson, 3-dash on proxy/cfshape.
- `00` infix is the fixed family token (00proxy/00prx/00cfjson/00cfmapjson/
  00cfproxy/00cfshape); May `prx*` names lack it — grammar distinguishes waves.
- Timestamps cluster: reported by centaur/wiki as 2026-06-18 17:53–20:52 UTC
  (~3h). No independent per-gem timestamps available (JFrog CSV has no dates;
  bridge metadata has no published fields).

## Artifacts

- `data/gem83-reconciliation/`: `gem83-names.json`, `gem83-reconciliation.csv`,
  `gem83-reconciliation.jsonl`, `pattern-sweep.txt`, `PROVENANCE.md`,
  `manifest.txt` (SHA-256), `progress.log`.
- Build: `scripts/gem83_reconciliation_build.py` (reproducible).
- Ingest: `scripts/es_ingest_gem83.py` (--create/--load/--verify).
- Elastic index `gem83-reconciliation`: **83 docs** (83 loaded, 0 failed),
  canonical shared schema, `event.dataset.keyword` present at creation.

## Open items

1. Dependency edges (hub-and-spoke) unverifiable from any public source —
   would need a researcher's private copy of the gemspecs.
2. Per-gem download counts and publish timestamps: only the 16 wayback
   records + aggregate figures from reports.
3. The `amd-bare` match (`amd6002`) is grammar-inferred; it is the only
   plausible 83rd name, but keep the caveat.
4. July-7 wave (215 pkgs) still open (separate lane).

## DEFENSIVE TAKEAWAY

- **Detection surfaces exposed:** coverage gaps between independent indexes — all 83 gems were `in_diffend=false` while present in the JFrog inventory. Absence from one index is not absence from the ecosystem.
- **Early-warning signals:** inventory-vs-index diffs as a standing check; a package that exists in one authoritative source but not another deserves a look.
- **What a defender could instrument:** defenders tracking supply-chain campaigns should query >=2 independent indexes (registry API, snapshot index, security-vendor inventory) and diff them routinely.
