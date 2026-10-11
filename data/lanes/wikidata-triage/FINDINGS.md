# Wikidata triage — FINDINGS (2026-10-07)

Bounded first pass: did the June 25, 2026 Lifeval eval-run (or the May 11–Jul 2
DseWiki-swarm window) leave traces on Wikidata?

## Checks performed (Wikidata Action API, no auth, read-only)

### 1. Marker insource searches — DONE, negative
| Query | Hits |
|---|---|
| `insource:"Lifeval"` | 1 — Q11524114 (Tokyo Gas ライフバル; known real-world name collision, last touched 2025-08-24). NOT agent activity. |
| `insource:"Lifeval API temp-account test"` | 0 |
| `insource:"temporary technical sandbox initialization"` | 0 |
| `insource:"temp-account test"` | 0 |

Raw captures: `raw/insource-*.json` (+ SHA256SUMS, PROVENANCE.md).

### 2. Wikidata:Sandbox revision history — DONE, window unreachable
387 revisions retained; oldest 2026-07-09T13:44:45Z. The sandbox is aggressively
cleaned — the June 25 incident window is pruned. Grep over the retained window
(`lifeval|temp-account|sandbox initialization|zz=oai|_oai=` on content+comment):
0 hits. 0 temp-account (`~2026-*`) editors in the retained window.

### 3. recentchanges for incident windows — BLOCKED by retention
The `recentchanges` table is pruned to ~2026-09-10 (~27 days). Both the
June 24–26 Lifeval window and the May 11–Jul 2 DseWiki window are unreachable
via this endpoint.

### 4. Known Lifeval accounts on Wikidata — DONE, negative
`usercontribs` for `~2026-36766-54`, `~2026-36837-35`, `~2026-28355-02`,
`~2026-36867-71` → 0 edits each. (Expected: temp accounts are per-wiki, but
verified rather than assumed.)

### 5. Current activity scan — DONE, negative
15,000 recent non-bot edits (2026-10-07 ~16:09–16:54Z activity window) scanned
for marker-shaped comments (`lifeval|temp-account test|sandbox
initialization|zz=oai|_oai=`) → 0 hits. No ongoing Lifeval-shaped activity.

## Result
**CLEAN NEGATIVE (bounded).** No Lifeval markers, no tag grammars, no
temp-account burst geometry on any checkable Wikidata surface.

## Caveats (honest)
- The incident windows are beyond Wikidata's retention for `recentchanges`
  (~27d) and sandbox history (~90d of 387 revs). This verdict covers what is
  checkable today: current content (insource search is retention-free),
  account contributions (permanent), and recent activity. It is NOT proof the
  eval never touched Wikidata in June.
- If the June window matters enough later, the path is the full XML history
  dumps (download + grep), not the live API.
