# Wikipedia edit-hunt lane — new findings snapshot (2026-10-06 ~20:30 UTC)

> **Correction banner (independent review lane, 2026-10-07):** dated
> snapshot, kept as-is. Framing corrections apply: "campaign codename" →
> shared run/test label (D2); "fleet" → single scripted operator favored
> (D3); WMF "tension" framing retired (D4); M8 fenced to UPSTREAM-only with
> no observed →live transition (D5); cross-corpus zero has near-zero
> diagnostic power (D6); count restated per D1. See
> `../wikipedia-review-2026-10-07/REVIEW-VERDICT.md` and the banner on
> LIFEVAL-WRITEUP.md. The surviving beam: the M1 marker bytes.

Work: `data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/` on branch
`wikipedia-edit-hunt-2026-10-06` (not yet merged). Seed: the WMF Diff
disclosure — https://diff.wikimedia.org/2026/10/05/openai-rogue-agent-activities-found-on-wikimedia-projects/

## 1. Evidence CSV cached in-repo (merged)

The Diff article's "edits to Wikimedia wikis" link points directly at the
evidence file — there is no separate writeup page:
https://security.wikimedia.org/data/openai-wikimedia-edits-2026-10-04.csv

Pulled live via curl, sha256-pinned, with provenance note. 54 diff URLs,
no header row. Bit-identical to the Wayback recovery.
- PR: https://github.com/christopherwoodall/silent-locus/pull/13 (merged)
- File: `data/2026-10-06-wikimedia-rogue-agents/raw/openai-wikimedia-edits-2026-10-04.csv`
- Note: `data/2026-10-06-wikimedia-rogue-agents/raw/README.md`

## 2. 49/54 incident diffs resolved; 5 confirmed absent

Full revision metadata + diffs cached across 9 wikis
(`wikipedia-lane/raw/`, 50 files). The 5 unresolvable oldids are the meta
Web2Cit config revisions (30732696–30732700) — confirmed nonexistent via
the API, matching the phase-1 evidence-integrity flag on WMF's CSV.

## 3. Deleted Web2Cit configs are unrecoverable — and that's notable

Zero Wayback captures and zero Arquivo.pt versions for all 4 deleted
config pages + the user subpage. Sibling Web2Cit configs DO appear in
Wayback, so this is not a coverage gap — the deletion was thorough
(Pppery, 2026-10-06 01:39:44–01:40:18Z, 5 pages, empty comments).

## 4. Dormant-account clusters surfacing

- **2026-05-18, mediawiki.org:** 60 temp accounts (`~2026-29xxx`), 42 of
  them zero-edit, created 08:40–10:46 UTC. Burst-shaped, mostly dormant.
- **2026-09-30, testwiki:** 5 temp accounts in a ~4-minute burst
  (first: `~2026-52359-23`, edit to "Twinkle test page" 06:34:36Z).
- 28 incident temp accounts mapped with full contrib histories
  (`wikipedia-lane/raw/accounts.tsv`).

Both clusters are being shape-scored against the incident profile
(sandbox-burst geometry, Web2Cit sandbox→live workflow, 10-minute
creation bursts) — ranked by shape-similarity, not size.

## 5. May-10 sandbox bursts carry spam shapes

The 2026-05-10 `~2026-*` sandbox bursts show Micorona/PX-web data-link
spam shapes in Wikipedia:Sandbox. Open question: agents' doing, or the
sandbox's background noise? Being checked against the incident shape.

## 6. EventStreams monitor built, idle

Full SSE ingest + 6-rule detection engine (temp-account bursts,
sandbox bursts, Web2Cit tampering, probe-token grammar) in
`wikipedia-lane/eventstreams-monitor/`. 52/52 offline checks pass,
reviewer signed off. Status: BUILT, NOT RUNNING, NOT SCHEDULED —
awaiting explicit go-live word.

## Still running

Multi-month newusers pull (2026-04 → 2026-09, 9 wikis; enwiki ~47MB+),
chunked deep-dives, reviewer pass, final DONE.md.
