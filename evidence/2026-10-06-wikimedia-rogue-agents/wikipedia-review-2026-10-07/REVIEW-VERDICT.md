# REVIEW-VERDICT — independent audit of the closed wikipedia edit-hunt lane
**Date:** 2026-10-07 · **Lane:** `wikipedia-review-2026-10-07` · **Target branch:** `wikipedia-edit-hunt-2026-10-06`
**Reviewers:** 4 fresh adversarial tracks (claims / evidence+provenance / methods / red team). All held KILL authority. None worked the original lane. Read-only on the closed lane; `revhistory-grep/` (in-flight) untouched.

## Overall verdict: READY-WITH-CAVEATS

The bytes hold. Every surviving factual claim re-checked against cached bytes or live API this pass — 7 of 8 claims HOLD byte-exact, 1 DOWNGRADED on phrasing, **0 new kills** (the 11 prior kills stand). Evidence integrity is clean: CSV sha256 matches, all 113 provenance hashes match, 8/8 sampled diff links resolve with claimed content, 54/54 records present, zero redactions.

What does NOT hold is the writeup's headline *framing*: the red team landed real hits on the gloss the lane put on the bytes. "Campaign codename," "fleet," "in tension with WMF," and the "sandbox→live workflow" reading all outrun the evidence. The finding survives; the packaging needs correction. With the framing downgrades below applied (as corrections to the writeup, not to DONE.md's graded claims), the lane is publication-ready.

## Per-claim verdict table

| # | Claim | Verdict | Grade | Basis |
|---|---|---|---|---|
| 1 | Lifeval marker family: 10 temp accounts, 3 wikis, ~30 min, 2026-06-25 | HOLD (restated) | OBSERVED (bytes) / INFERENCE (coordination, thin sense) | Marker bytes byte-exact in cached revision contents and live diffs (8/8 incubator links 200 with content). **Restatement required:** only 5 accounts authored the full marker as their marginal addition; 3 authored short forms (`<!-- temp -->`, `<!-- t -->`) — the round-1 correction DONE.md §2 glossed over. Burst is 7m16s, not "7 minutes". "Shared run/test label," not "campaign codename" (see downgrade D2). |
| 2 | M3 same-second volleys, `~2026-28355-02`, 4 wikis, 2026-05-10 | HOLD | OBSERVED (machine) | records.json: 8370994+8370995 same second (17:12:18Z); 8370995 = 8370994 + one appended line (167 vs 142 bytes, scripted double-save); test/test2 pairs + 17:02 pair confirmed. |
| 3 | M6 geometry: 8 temps in 8 of 9 UIDs 2690515–2690523; 2690519 = Dayerhonda | HOLD | OBSERVED | Live `list=users` + cached newusers log: Dayerhonda autocreated 20:19:29Z mid-burst. Original "consecutive" claim stays dead. |
| 4 | M8: `~2026-36867-71` → Meta Web2Cit oldid 30732691; 5 oldids nonexistent; 30732697 exists, unrelated | HOLD (fenced) | OBSERVED (Incubator leg) / UPSTREAM single-source (Meta leg) / INFERENCE (workflow) | CSV titles 30732691 to the identical full account name; all five return `badrevids` live; 30732697 = Der-Wir-Ing user page, unrelated. **Fence:** Meta leg rests on ONE uncheckable CSV row — present as UPSTREAM-only. No →live transition observed (see D5). |
| 5 | H1: mediawiki.org 2026-05-21, 33 temps ~1h, genuine rate anomaly | HOLD | OBSERVED (anomaly) / LEAD | May-2026 mean 1.4/p95 3 per 10-min; H1's 13- and 18-account buckets #3/#1 of month. 32 of 33 zero edits. Attribution kills honored. |
| 6 | M1: testwiki 2026-05-10, 13-of-13 consecutive UIDs, zero edits | HOLD | OBSERVED (geometry) / unresolved | UIDs exactly 73872–73884, zero interlopers, window matches. Caveat: all-9-wiki zero-contrib re-verified by reviewers but per-wiki raw JSON not cached for M1. |
| 7 | WMF evidence: CSV sha256, 54 diff URLs, 54/54 in records.json, 49/54 bodies | HOLD | OBSERVED | sha256 byte-exact; 54/54 coverage; missing 5 = the Meta set. Nit: DONE.md's cache path is ambiguous (CSV lives in event-level `raw/`, not `wikipedia-lane/raw/`). |
| 8 | urlquery htmx repair: HX-Current-URL operative; 143 re-read, 128 stood, 15 resurrected | HOLD | OBSERVED | Probe log proves header behavior; exactly 143 reread files; 128/15 tally exact. |
| — | Clean negatives (vocab/ngram/wordlist sweeps) | HOLD | OBSERVED (on searched surfaces) | `srnamespace=*` in all 8 scripts; capture counts exact (54, 81, 10,332); sampling disclosures honest. Wording must use "no leakage detected on searched surfaces," not "incident-contained" (see action item A2). |
| — | Newusers dataset: 24 files, 6,922,622 lines, dedup counts | HOLD | OBSERVED | `wc -l` = 6,922,622 exact; April dup rows documented; resume fragment correctly excluded. Provenance lacks sha256 for the jsonl files (gap, not integrity failure). |

## Kill appendix

**No new kills.** The 11 prior kills (review rounds 1–2) were re-verified against DONE.md's appendix and stand uncontradicted.

## Downgrade appendix (framing corrections — adopt before publication)

- **D1 — "8 accounts appended the exact marker" → restated count.** Byte-exact marker present in all 8 incubator revision contents, but marginal authorship is 5 full-string + 3 short-form. Restate as: *8 incubator accounts carried the Lifeval marker family in one 7m16s burst (5 marginal full-string appends, 3 short-form), plus the exact marker on Commons and the API variant on Meta — 10 accounts total.* Coordination INFERENCE unaffected.
- **D2 — "campaign codename" → "shared run/test label."** The string appears once, one day, one incident, never reused — bytes support a run label, not a persistent campaign identity. The Meta variant (`<!-- Lifeval API temp-account test -->`) reads as a test-case label. Campaign-persistence is unearned INFERENCE.
- **D3 — "fleet" → single scripted operator favored.** The 8 Incubator edits are strictly sequential (~40–80s apart, metronome cadence, zero overlap) — that is one scripted loop iterating sessions, not 8 parallel agents. No byte distinguishes one operator/8 sessions from 8 operators. Multi-agent "fleet" is unproven; "fleet" may remain only as shorthand, never as an established claim.
- **D4 — WMF "tension" framing → footnote.** WMF said no evidence of coordination *among* agents (agent-to-agent, via their systems); the lane has a shared run label across one operator's sessions — coordination *of* sessions by a harness. WMF included the Lifeval oldids in their own CSV; they declined the characterization, didn't miss the bytes. The "tension" is equivocation on "coordination" and should be retired from the headline.
- **D5 — M8 "sandbox→live workflow mirrored" → fenced inference.** The Meta page is `templates-temp-5123` — a template *sandbox*, not live config; the four live-namespace oldids are by unattributed accounts. No →live transition is observed, and no content survives on any of the five oldids. Honest statement: same account edited a userspace Web2Cit template-sandbox page (UPSTREAM, single-source); four live-namespace Web2Cit oldids exist but are unattributed; no →live transition observed.
- **D6 — cross-corpus zero → "not a public string; nothing more."** The zero on disk/urlquery/web is the expected observation for a private run label too — near-zero diagnostic power between competing readings. The noise-kills stand; the privacy gloss goes.

## Link-check results (track 2, curl, research UA, 2026-10-07)

8/8 resolve with claimed content: incubator diffs 7226103, 7226104, 7226105, 7226108, 7226111 (marker present); meta 30732655 (variant marker); commons 1238390511 (marker); mediawiki 8370994 (M3 volley content). Meta oldids 30732691/96/98/99/300 all `badrevids`; 30732697 exists (Der-Wir-Ing, unrelated). CSV sha256 recomputed exact. All 113 PROVENANCE.md hashes match. Zero redaction placeholders in the lane.

## Methods notes (track 3)

5 of 6 checks SUPPORTED on the bytes. One WEAK: leaf FINDINGS.md files headline "incident-contained" instead of the reviewer-approved "no leakage detected on searched surfaces" (action item A2). insource: current-content-only limitation is bold and front-and-center everywhere it matters. Newusers line counts match exactly. htmx patch verified correct with a complete data trail.

## Action items before PR #15 merges

- **A1.** Quarantine/delete the 776 stale zero-padded incubator captures in `wordlist-wiki-sweep/raw/incubator.wikimedia.org/` — CORRECTIONS.md claims they were deleted; they weren't, and they carry the bogus mangled-phrase hit counts. Hazard to future glob-based re-analysis. (Does not affect the verdict; graders skip them.)
- **A2.** Restate the vocab/ngram leaf FINDINGS.md net verdicts as "no leakage detected on searched surfaces" (reviewer-approved wording).
- **A3.** Correct the Lifeval headline framing per D1–D4 (restated counts, run-label, single-operator-favored, WMF tension → footnote). Recommend correction banners on the stale artifacts (FINDINGS-SNAPSHOT-2026-10-06.md, LIFEVAL-WRITEUP.md) rather than rewrites — they are dated.
- **A4.** Fence M8 per D5–D6 (UPSTREAM-only Meta leg, no observed →live transition, deletion = evidence loss).
- **A5.** Backfill sha256 for the 24 newusers jsonl files (~1.4GB, cheap) and fill the `(pending)` block in PROVENANCE.md before calling the lane fully closed.

## Unresolved questions

1. Is "Lifeval" a harness-side run label or a human tester's label? Decidable only with reuse in a second incident or a harness task spec — neither available.
2. The four live-namespace Web2Cit oldids remain unattributed. If ever attributed to the incident accounts, M8's →live reading revives; until then it stays inference.
3. The revhistory-grep job (in-flight, out of scope) may surface cleaned-history markers — its results could strengthen or bound the sweep negatives; re-check A2's wording against its findings when it lands.

## Red-team summary

Strongest surviving thread: the M1 marker bytes — 10 accounts, 3 wikis, ~30 min, identical distinctive string family, absent from WMF's characterization. That is the load-bearing beam; the headline should stand on it alone. Weakest link: M8's Meta leg — one uncheckable CSV row; if wrong, M8 evaporates.

*Review lane: coordinator + 4 tracks, 2026-10-07. Track files: track1-claims.md, track2-evidence.md, track3-methods.md, track4-redteam.md.*
