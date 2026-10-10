# Burst analysis — temp-account creation bursts, 9 wikis, Apr–Sep 2026

**Worker:** BURST-ANALYSIS · **Branch:** `wikipedia-edit-hunt-2026-10-06` · **Date:** 2026-10-07
**Evidence cache:** `burst-analysis/raw/` (this dir) — `bursts.json`, `events.npz`, `detect_bursts.py`,
`shape_pass1.py`, `shape_pass2.py`, per-burst `uids-*.json` / `contribs-burst-*.json` / `logevents-*.json` /
`rev-*.json`, `PROVENANCE.txt`, `detect_v3.log` / `detect_v4.log` / `pass2.log`.

## Method

Parsed all 24 `newusers-*.jsonl` files (6,982,622 lines → 4,088,327 logid-deduped `~2026-*` events;
bgwiki uses the localized namespace `Потребител:` — handled). Sliding windows 10-min / 1-hour / 1-day
per wiki; flag threshold = max(min_n, 8 × mean rate in window), min_n = 4 / 12 / 40. Greedy non-overlap
within a size, cross-size merge prefers the smallest window. Result: **13 bursts** (down from 5,486
under a median-based baseline that fired on noise).

**Retracted approach (honest negative on method):** v2 tried "ordinal runs" on the `~2026-<POOL>-<SEQ>`
name structure assuming POOL was a global creation counter. It is not — POOL ∈ [10002,99998] is a
time-bucketed pool (~70 accounts/pool, ~3.4 pools/10 min globally), non-monotonic in creation time.
The 182,496 "runs" it produced were spurious (incl. t0>t1 artifacts). Dropped; detection rests on
time windows only. Near-consecutive-UID geometry (criterion 3) was then measured properly via
`list=users` per burst, with interlopers named via `list=logevents`.

Contrib checks: `list=usercontribs` batched (≤50 users/request), paced ≥5s between requests, across
all 9 wikis for candidate accounts. Revision content fetched for edits found.

## Ranked bursts (by incident shape, not size)

### HIGH

**H1 — mediawiki.org, 2026-05-21 00:40–01:39Z, 33 temp accounts (three sub-clusters)**
Shape score: **HIGH** — matches 4 of 5 incident criteria; the missing one is Web2Cit.

- **00:40:39Z — the sandbox edit.** `~2026-30432-02` (uid 18396895) created and, **in the same
  second**, edited `Project:Sandbox`: comment `sandbox test`, added text `Temporary sandbox test.`,
  tagged `mw-reverted`. The comment is verbatim Lifeval M2 vocabulary (`sandbox test` ×9 in the
  incident corpus); the added text is the same machine-phrased family as `Temporary technical
  sandbox initialization`; `mw-reverted` matches the incident's 43/49 tag rate. One edit, then
  dormant (criterion 2 ✓).
- **01:13:18–01:13:56Z — 13 accounts in 38 seconds**, uids 18396941–18396954: **12-of-13
  consecutive with one named-human interloper**, `Wildwind75` (uid 18396951, created 01:13:49Z
  mid-burst, confirmed via `list=logevents`). This is the *corrected* M6 geometry exactly
  (Lifeval: 8-of-9 with `Dayerhonda`; here 12-of-13 with `Wildwind75`).
- **01:38:15–01:39:45Z — 18 accounts**, uids 18396979–18396997: 11-run + 7-run with one
  named-human interloper, `Jheanovivia` (uid 18396990, created 01:39:29Z). Same geometry again.
  (One account in this window, `~2026-30385-94`, is a pre-existing temp account — created earlier
  on enwiki, edited there 00:56:28Z with a human-shaped comment — that merely *visited*
  mediawiki.org mid-burst; counted in the window but not fleet.)
- All other burst accounts: **zero edits on all 9 wikis** (checked en, meta, commons, incubator,
  mediawiki, simple, test, test2, bg).
- No Web2Cit-adjacent edits (criterion 4 absent).

Assessment: same campaign family as Lifeval, one month earlier (May campaign window: M3 volley
05-10, commons 3-acct 05-13, this 05-21, Lifeval 06-25). Sandbox-test behavior + incident vocab +
twin interloper-bracketed uid runs = fleet evaluation harness signature. Attribution to the same
operator is INFERENCE; the shape match is OBSERVED.

Example diffs:
- https://www.mediawiki.org/w/index.php?diff=8383593 — Project:Sandbox, `~2026-30432-02`, "Temporary sandbox test." / comment "sandbox test"
- https://en.wikipedia.org/w/index.php?diff=1355289333 — contrast: the human-shaped enwiki edit by `~2026-30385-94` (NOT fleet)

### MEDIUM

**M1 — test.wikipedia.org, 2026-05-10 17:47:30–18:41:00Z, 13 temp accounts**
Shape score: **MEDIUM** — perfect fleet-creation geometry, zero behavioral evidence.

- Uids **73872–73884: 13-of-13 consecutive, zero interlopers** — a cleaner run than the incident's
  8-of-9 (criterion 3 at full marks).
- **Zero edits by all 13 accounts on all 9 wikis** (usercontribs checked everywhere incl. bgwiki).
  Criteria 1, 2, 4, 5 cannot score — creation-only burst.
- Lead: same day and same name-pool family as the M3 volley account `~2026-28355-02`
  (pools 28236–28431 vs 28355; M3 edits 17:02–17:23Z across mediawiki/test/test2, this burst
  created 17:47–18:41Z). Plausibly the same operator's account-provisioning run — or an aborted
  session. Without a single edit it cannot clear HIGH.

### LOW

**L1 — Commons, 2026-09-30 10:54–11:04Z, 26 temp accounts**
Shape score: **LOW** — uid span 55 for 26 accounts (no run); only 2 of 26 edited, both
human-shaped Wikibase label edits on file pages (`the sculpture is made by Uwe Maroske
(1951-2020)`; `david hockeah hoose` — sic). Logged-out humans, not fleet.

## Known / acknowledged (not scored)

- **Incubator 2026-06-25 20:14–20:21Z, 8 accounts** — the Lifeval M6 burst. Detector caught it
  exactly (validates the pipeline). Not re-analyzed.
- **mediawiki.org 2026-05-18 cluster** (5× 10m + 2× 1h temp bursts, n=8–25) — the resolved CLEAN
  NEGATIVE: human translate-a-thon, 383 accounts/4h mostly named
  (see `wikipedia-lane/ACCOUNT-29822-53-WRITEUP.md`, `wikipedia-lane/reviewers/REVIEWER-2.md`
  claim 3). The temp-account spike is its side effect. Cited, not re-litigated.

## Honest negatives (no incident-shaped bursts)

- **bgwiki, simplewiki, test2wiki** — no bursts above threshold at any window size.
- **enwiki, metawiki** — no bursts above threshold. **Limitation:** on these wikis an 8-account
  coordinated burst is undetectable against baseline (10-min thresholds: enwiki 487, metawiki 707
  temp creations). Absence of bursts here is *not* evidence of absence of fleet activity; the
  lane's vocab sweep (marker-based, all wikis) is the complementary control and came back
  incident-contained.
- **incubatorwiki** — nothing beyond the known Lifeval burst.

## Bottom line

**Yes — one burst matches the Lifeval incident shape: mediawiki.org 2026-05-21 (H1, HIGH).**
A second, behaviorally silent but geometrically perfect fleet-creation burst exists on testwiki
2026-05-10 (M1, MEDIUM), temporally and pool-adjacent to the known M3 volley. No other
incident-shaped bursts found on any of the 9 wikis, Apr–Sep 2026.
