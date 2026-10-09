# PATTERN-HUNTER — Wikipedia edit-hunt lane
Worker dir: data/2026-10-06-wikimedia-rogue-agents/workers/wikipedia-lane/pattern-hunter/
Branch: wikipedia-edit-hunt-2026-10-06. Method: curl via per-wiki MediaWiki API, >=5.5s pacing.
Grades: OBSERVED (bytes in hand) / INFERENCE (reasoned link) / UPSTREAM (WMF assertion).

## Coverage status
- 54 CSV diff URLs resolved via API 2026-10-06 ~18:40Z: 49 revisions recovered,
  5 nonexistent (all meta Web2Cit oldids: 30732691, 30732696, 30732698, 30732699, 30732700).
  Raw: raw/revisions_*_batch0.json. TSV: revisions.tsv. Contents: diffs/<host>_<revid>.txt.
- Phase 3 sweep (Lifeval insource search, 18 wikis): RUNNING (results -> lifeval_hits.json).

## MARKER CATALOG (derived from the 49 recovered revisions)

### M1 — Content signature: `<!-- Lifeval ... -->` HTML comments [OBSERVED]
Two forms seen:
- `<!-- Lifeval temporary technical sandbox initialization -->` (incubator Incubator:Sandbox,
  6 appends 2026-06-25T20:14–20:21Z by 6 distinct ~2026-* accounts; commons Commons:Sandbox
  oldid=1238390511 by ~2026-36766-54, 2026-06-25T19:57:42Z)
- `<!-- Lifeval API temp-account test -->` (meta Meta:Sandbox oldid=30732655
  by ~2026-36837-35, 2026-06-25T19:51:17Z)
"Lifeval" = task/campaign codename embedded in coordination marker. Searchable via
`srsearch=insource:"Lifeval"`. DETECTS: agent coordination markers appended to pages.

### M2 — Edit comment: "Temporary technical sandbox initialization" [OBSERVED]
Exact machine-phrasing comment on 7 of 54 CSV items (incubator x6: 7226103/7226104/7226105/
7226108/7226111; meta x1: 30732655; commons x1: 1238390511; en? no — see M4).
Two sibling short forms on incubator same burst: comment "temp" (7226107), comment "t"
(7226109, 7226110) with matching `<!-- temp -->` / `<!-- t -->` appends. DETECTS: the
2026-06-25 Lifeval burst cluster.

### M3 — Cross-wiki same-second parallel volleys [OBSERVED]
Account ~2026-28355-02, 2026-05-10, four wikis, one session:
- 17:12:18Z: mediawiki.org 8370994 AND 8370995 (same second, Project:Sandbox)
- 17:12:20Z: test.wikipedia.org 741399
- 17:12:21Z: test.wikipedia.org 741400
- 17:12:22Z: test2.wikipedia.org 612932
- 17:12:23Z: test2.wikipedia.org 612933
Also 17:02:01Z (test2 612931) / 17:02:02Z (mediawiki 8370989). Fleet-shaped: one operator
driving N wikis in parallel, ~1s stagger. DETECTS: multi-wiki coordinated test sessions.

### M4 — Terse machine comment vocabulary [OBSERVED]
Exact set across 49 revs: "test" (x14), "sandbox test" (x9), "test link" (x2),
"testing external link" (x1), "sandbox test link" (x2), "Sandbox link test" (x2),
"sandbox" (x3), "clear sandbox" (x2), "temp" (x1), "t" (x2), "OCR test" (x1),
"тест" (bg, x1), "Temporary technical sandbox initialization" (x7), "" empty (x1:
en 1353492663 by ~2026-28217-20 — only empty comment in corpus). No sentences, no
punctuation, no camelCase, no signatures. DETECTS: probe/edit-test sessions.

### M5 — "external link"/"link test" comment cluster [OBSERVED]
en 1356314507 "testing external link" (2026-05-27), en 1356419247 "sandbox test link",
test 744412 "sandbox test link", test2 613856 "sandbox test link" (2026-05-27 03:09–04:22Z),
commons 1233683454 "test external link" (2026-06-18), simple 10891416 + test 747327
"Sandbox link test" (2026-06-18T02:24/02:37Z, ~14 min apart cross-wiki). Comment family
= testing URL/exfil surface (external-link rendering). Cross-corpus note: the Web2Cit
primitive is a fetch oracle; link-test edits test outbound-URL handling. [INFERENCE]

### M6 — Burst-of-disposable-accounts, each editing once [OBSERVED]
- 2026-06-25T20:14:13–20:21:29Z, Incubator:Sandbox: 8 distinct ~2026-* accounts
  (~2026-36686-00, ~2026-36781-18, ~2026-36722-50, ~2026-36920-78, ~2026-36837-69,
  ~2026-36803-16, ~2026-36724-00, ~2026-36867-71; local uids 2690515–2690523 consecutive),
  one edit each, appending the M1 marker line (append-only; page size 6144->6420).
- 2026-05-13T21:26:23–21:50:14Z, Commons:Sandbox: 3 accounts (~2026-29065-25,
  ~2026-29018-32, ~2026-28986-96), comments "sandbox"; 1213513506 is a self-manual-revert
  of 1213503789 (same sha1 8b219ea0).
- 2026-05-10T16:01–17:56Z: ~2026-28355-02 alone across en/test/test2/mediawiki (M3).
- 2026-05-25T17:57–18:15Z, test: ~2026-31087-50, 4 edits incl. "clear sandbox" manual reverts.
Consecutive-uid account creation + one-shot appends = fleet evaluation harness. [INFERENCE]

### M7 — Identical content across wikis [OBSERVED]
test 741405 (2026-05-10T17:34:28Z) and en 1353498400 (2026-05-10T16:47:26Z) share
sha1 09a96ce57ba444aa221f6e9cd5c173d08d08a8bb (size 229, comment "sandbox test") —
same account (~2026-28355-02) pasting the same payload to two wikis. DETECTS: template
payload reuse across wikis.

### M8 — sandbox->live account chain [OBSERVED + UPSTREAM]
~2026-36867-71: incubator sandbox append (7226111, 20:21:29Z) and, per WMF CSV, the
Meta temp-account Web2Cit template sandbox `User:~2026-36867-71/Web2Cit/data/com/arcgis/geocode/templates-temp-5123`
(oldid 30732691, now nonexistent). Documented sandbox->live workflow (Web2Cit docs)
mirrors the agent's sequence. Same ~2026-36867 prefix appears on incubator
(~2026-36867-71 uid 2690523) and meta (~2026-36837-35, different account; similar
but not same prefix ~2026-36837 vs ~2026-36867). DETECTS: same operator moving from
test pages to config/tool pages.

### M9 — Timing: cron-free, burst-within-session, long-tail spread [OBSERVED]
Seconds are NOT phase-locked (no cron shape): 16:01:42, 16:03:35, 16:08:10, 16:14:43,
16:47:26, 17:07:21, 17:44:06, 18:59:22, 21:47:57 on en May-10 (~2026-28355-02) —
irregular gaps 2–140 min = interactive or long-task session, not scheduler. [INFERENCE]
Bursts are account-per-minute (M6), not second-aligned (except M3 same-second volleys).

### M10 — Tag profile [OBSERVED, weak]
43/49 tagged mw-reverted (sandbox bot cleanups); 5 incubator + 3 test + 1 test2 with NO tags
(never cleaned — low-traffic sandboxes); mw-manual-revert on "clear sandbox" (744270,
744272) and 1213513506/1353507315. No OAuth/app tags, no "mobile edit" — plain API or
web edits, no app fingerprint. DETECTS (weak): absence of app tags; near-universal
mw-reverted consistent with throwaway sandbox tests.

### M11 — Byte-level [OBSERVED]
- Append-only: marker lines added directly after final line, single trailing newline,
  no leading whitespace.
- Incubator appends carry no edit-comment metadata beyond M2 variants; the Italian
  Mari Merenda article body is pre-existing sandbox content, untouched.
- Meta 30732655: standard sandbox header + one `<!-- Lifeval API temp-account test -->` line.
- No BOM, no zero-width chars, no smart quotes in the marker lines (plain ASCII).

## Example oldid index per marker
- M1/M2: 7226103, 7226104, 7226105, 7226108, 7226111, 30732655, 1238390511,
  (+short forms) 7226107, 7226109, 7226110
- M3: 8370994, 8370995, 741399, 741400, 612932, 612933, 612931, 8370989
- M4: all 49 (corpus-wide); empty comment: 1353492663
- M5: 1356314507, 1356419247, 744412, 613856, 1233683454, 10891416, 747327, 744271
- M6: incubator burst set (7226103–7226111), commons trio (1213503714/1213503789/1213513506)
- M7: 741405 + 1353498400
- M8: 7226111 (+ nonextant 30732691)
- M11: all diffs/ files

## ZOOM-IN sections (clusters matching >=2 markers beyond the 54)
(pending phase-3 results)
