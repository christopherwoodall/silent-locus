# German/French swarm hunt — EUROSWARM (2026-10-05)

**Verdict: no German or French agent swarm was found.** 16 workers across
3 waves (DE/FR linguists, TLD sweepers, CT miners, archive divers, Shodan
infra tracking, GitHub mining, plus a statistician). 70+ clean urlquery
pivots, encoded layer clean (1,031 base64 blobs, 173,768 hex strings, 5,948
tag values), CT/TLD/infra/archive sweeps all negative. The arithmetic
dissolves the thesis: at DE/FR's ~5–8% world AI share and ~7–8 observed
agent operations globally, P(observing zero) ≈ 0.55–0.67 — zero is the modal
outcome, not an anomaly. One lead survives, unresolved and narrowed (below).

## Key files

| File | Contents |
|---|---|
| [EUROSWARM-ASSESSMENT.md](EUROSWARM-ASSESSMENT.md) | Full assessment: thin evidence-for pile, heavy evidence-against pile, the statistician's verdict, and the precise bound of the negative |
| [COORDINATOR.md](COORDINATOR.md) | Running log of the 16 workers across 3 waves (builds on prior `german-hunt/`, `french-hunt/`, `cross-swarm-vocab/`, `personas/german-archaeologist/` work) |
| [clipboard-followup/CLIPBOARD-REPORT.md](clipboard-followup/CLIPBOARD-REPORT.md) | Follow-up on the surviving lead (below) |
| workers/ | Per-worker `FINDINGS.md` for each of the 16 workers |

## The surviving lead: usemod.org WikiPatches/ClipBoard burst

6,848 anonymous edits 2026-05-23 → 2026-05-31 on
`https://www.usemod.org/cgi-bin/wiki.pl?WikiPatches/ClipBoard`, from five OVH
hosts (Canada + France), blank edit summaries, revisions purged, page
reverted to a 2009 stub ~2 min after the last edit. Agent-shaped geometry;
the recovered final state was a pharma-spam line
("Struggling with allergies? ... mnsmiles.com/prednisone/"), making the
pure spam-bot reading the current frontrunner. No burst content survives in
any public archive (Wayback, Arquivo.pt, Common Crawl all exhausted);
Wikiwix holds archive tokens behind a browser-only render wall — the one
open recovery surface, needing a live browser.
