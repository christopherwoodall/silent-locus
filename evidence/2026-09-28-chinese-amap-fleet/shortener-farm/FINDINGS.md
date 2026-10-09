# Shortener-farm operation — FINDINGS

**Operation:** shortener-farm (coordinator session b88b4a35, 2026-10-05 ~01:05–01:15 CDT)
**Workers:** DISCOVERY (enumeration) + FARMING (stats pulls) — both complete.
**State:** `shortener-farm/targets.txt`, `shortener-farm/hits.jsonl`, `shortener-farm/FARM_LOG.md` — all resumable after VM restart.

## Bottom line
**Zero agent-shaped hits this run.** All 8 seed-list hosts are now gated, blocked, or dead — the public-stats surface is closing everywhere (gating wave following uoft.me/vanderbi.lt). But the discovery worker added **35 new candidates worldwide** (targets.txt now 43 UNTESTED), including a Polr 2 instance on an **Argentine government domain** and a public-interface YOURLS 1.9.2 at Southampton. The farm list is richer than it started; the stats surfaces are just harder to reach.

## DISCOVERY results (evidence-graded)
- **35 new candidates appended to targets.txt**, all UNTESTED, from search-engine dorks only (curl egress dead this run — crt.sh `go.*`/`s.*`/`t.*` enumeration is owed a rerun with live egress).
- **Top farming priorities:**
  1. `links.scba.gov.ar` — Polr 2, **Argentina government** (Suprema Corte de Buenos Aires). Gov-owned, public-analytics posture unknown. HIGH.
  2. `go.soton.ac.uk` — Univ. of Southampton, YOURLS v1.9.2 with **public interface** (v1.9.x predates the gating wave; stats pages may be open).
  3. `utd.link` — Polr 2, UT Dallas.
  4. `go.tssa.nsw.edu.au` — Australian school (nsw.edu.au).
  5. `foss.ntua.gr/s` — NTUA Greece university.
- Long tail: Polr instances (srsh.ir Iran, el.iq, moo.mk, bkn.cx, l.aoe.com, links.macg.io, short.orwa.org, cloudosd.net, dusty.link, retrorgb.link), YOURLS instances (e.vg, lmt.sh, phantomlink.in, qone.eu, monurl.ca, brm.ac, enloire.fr, nord.click, webhop.se, t-s.link, url.itunix.eu), university custom platforms (go.unl.edu, uwat.ca, umsl.edu/go/, lncn.ac), attac.org/l, su.monitorlatino.com, link.oarc.uk, actnow.link, go.brown.edu, kutt.it (low priority — stats private by default).
- Richest source: Archive Team URLTeam wiki (Mr_archive's YOURLS/Polr list); ~60 commercial instances skipped as low farm value.
- Marker-scoped dorks (`zzagent`/`maagent`/`260618`) → 0 hits. Shlink public instances → 0 found. Kutt deployed instances → 0 found.
- Confidence: MEDIUM — candidates are deployment-shaped (readme/index hits), not verified live.

## FARMING results (evidence-graded)
| Host | Status | Finding |
|---|---|---|
| url2go.pro | LIVE-GATED | YOURLS 1.8.2; `yourls-infos.php` → login wall |
| c.pr.gov.br | UNRESOLVABLE | fetch-service resolution failed; needs egress recovery |
| go.unibw.de | LIVE-GATED | custom UniBW plugin, RZ-login required, members-only |
| mailer01.net | DEAD | empty response body |
| catchingtherain.com/s | LIVE-BLOCKED | JS bot-check challenge — needs live-browser pass |
| eccl.es | LIVE-GATED | custom "spaceless" shortener, magic-link login |
| bitily.in | LIVE-BLOCKED | JS bot-check at `/MYLABI/clarksixpdf60091`; Korenblit keywords unverified live |
| da.gd/stats/g | re-check | still "text-based stats endpoint coming soon" |

- **Agent-shaped hits: ZERO.** No accessible stats surface on any seed host → nothing to cross-check against corpora. `hits.jsonl` untouched; no infra-watchlist additions.
- Trend confirmation (HIGH confidence): the public-stats surface is closing everywhere — url2go.pro, go.unibw.de, eccl.es all follow the uoft.me/vanderbi.lt gating wave. Re-check cadence on still-open instances (goto.unm.edu) matters more than one-shot sweeps.

## Open follow-ups (for the parent / future runs)
1. **crt.sh pass owed** — go.*/s.*/t.*/link.* subdomain enumeration on university/gov domains worldwide (blocked by dead egress).
2. **Live-browser pass** for JS-challenged hosts: catchingtherain.com/s, bitily.in (holds known swarm keywords `clarksixpdf60091`, `clarkredir70058`), c.pr.gov.br.
3. **Farm the 43 UNTESTED candidates** in targets.txt once egress returns — links.scba.gov.ar and go.soton.ac.uk first.
4. Watch goto.unm.edu (the Rosetta stone) for the gating wave reaching it.

## All observed URLs
- https://links.scba.gov.ar/ (Polr 2, Argentina government)
- https://go.soton.ac.uk/ (YOURLS 1.9.2 public interface)
- https://utd.link/ (Polr 2, UT Dallas)
- https://go.tssa.nsw.edu.au/
- https://foss.ntua.gr/s
- https://attac.org/l
- https://su.monitorlatino.com/
- https://link.oarc.uk/
- https://actnow.link/
- https://go.brown.edu/
- https://srsh.ir/ https://el.iq/ https://moo.mk/ https://bkn.cx/ https://l.aoe.com/ https://links.macg.io/ https://short.orwa.org/ https://cloudosd.net/ https://dusty.link/ https://retrorgb.link/
- https://e.vg/ https://lmt.sh/ https://phantomlink.in/ https://qone.eu/ https://monurl.ca/ https://brm.ac/ https://enloire.fr/ https://nord.click/ https://webhop.se/ https://t-s.link/ https://url.itunix.eu/
- https://go.unl.edu/ https://uwat.ca/ https://umsl.edu/go/ https://lncn.ac/
- https://kutt.it/
- https://url2go.pro/yourls-infos.php (login-gated)
- https://c.pr.gov.br/ (unresolvable)
- https://go.unibw.de/ (RZ-login)
- https://mailer01.net/ (dead)
- https://catchingtherain.com/s (JS bot-check)
- https://eccl.es/ (magic-link login)
- https://bitily.in/MYLABI/clarksixpdf60091 (JS bot-check)
- https://da.gd/stats/g (coming soon)
- https://goto.unm.edu/ (Rosetta stone — still open, watch for gating)
