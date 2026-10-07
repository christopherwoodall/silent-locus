# REVIEWER-2 — kill-authority review
**Lane:** Wikipedia edit-hunt, branch `wikipedia-edit-hunt-2026-10-06`.
**Reviewer:** REVIEWER-2 (independent angle; Reviewer-1 reviewed separately).
**Date:** 2026-10-06 ~21:30 CDT. **Grade scale:** OBSERVED / INFERENCE / UPSTREAM.

**Read first:** `LIFEVAL-WRITEUP.md`, `vocab-sweep/FINDINGS.md`,
`ngram-sweep/FINDINGS.md`, `ACCOUNT-29822-53-WRITEUP.md`,
`lifeval-cross-corpus/SWEEP-SUMMARY.md`, plus raw API dumps and live
MediaWiki API queries made during this review (incubator + meta +
mediawiki.org; one 429 rate-limit hit, paced retries after).

**Kill authority exercised:** claims I kill are listed in the
KILLED-BY-REVIEW appendix at the end and must be removed from lane
findings. DOWNGRADED claims keep a restated, weaker form.

---

## Claim 1 — "The marker vocabulary is fully incident-contained"

**VERDICT: DOWNGRADED.** Restated claim: *"No marker leakage detected on
the searched surfaces (insource: over 9 wikis = current content only;
case-insensitive comment grep over the last-200 revisions of each wiki's
main sandbox). Containment beyond those surfaces is unproven."*

The insource: zeros for the campaign-specific strings ("Lifeval
temporary…", "Lifeval API", "technical sandbox initialization",
"sandbox initialization", "API temp-account") are OBSERVED and strong —
zero current-content presence across all 9 incident wikis. That part of
the claim survives.

What does **not** survive is the word *"fully"*. The sweeps have two
documented blind spots, and the incident's own corpus proves the second
one is real, not hypothetical:

1. **insource: is current-content-only.** Any leak whose page content was
   cleaned, reverted, or edited before the sweep is invisible — including
   on non-sandbox pages. The incident itself lives in this blind spot
   (the markers were cleaned from live sandboxes; they survive only in
   revision history). A second fleet that pasted a Lifeval marker into a
   page later cleaned would score exactly the zeros the sweeps found.
2. **The 200-rev comment grep demonstrably misses real incident-shaped
   activity.** The incident's own Commons "OCR test" edit
   (commons 1213399057, 2026-05-13) and the May-27 "sandbox test link"
   edits were *not* in the last-200 windows — the FINDINGS files say so
   explicitly. If the sweep method misses the incident's own revisions,
   it cannot support "fully contained" for anything outside the incident
   set. On a fast-turnover sandbox, 200 revs cover days, not the May–June
   window.
3. **Only the main sandbox per wiki was comment-grepped, but the fleet
   didn't only use main sandboxes.** The CSV's en rows include
   `User:Example/sandbox` edits (en 1353490694, 1353490935) — a leak
   through that page with a non-marker comment (the fleet used comments
   "test", "sandbox", "t", empty) would be invisible to BOTH methods.
4. **Only the 9 incident wikis were searched.** A leak on a 10th wiki
   (wikidata, outreach, species…) was never queried.

**What a real leak that these sweeps would miss looks like:** a second
set of temp accounts appending `<!-- Lifeval … -->` with comment "test"
to `en.wikipedia.org/wiki/User:Example/sandbox` in July, cleaned an hour
later by a sandbox bot. insource: → clean (current content). Comment
grep → misses (wrong page; comment contains no marker ngram; >200 revs
ago on the main sandbox anyway). Zero hits, zero evidence — and the
current verdict language would still read "fully incident-contained."

**What would restore the strong claim:** paginated full-history
comment+content grep (not 200-rev spot check) of every sandbox page the
incident touched — including en User:Example/sandbox and the test-wiki
sandboxes — plus running the built EventStreams monitor
(`wikipedia-lane/eventstreams-monitor/`) for live detection going
forward. Until then the honest grade is OBSERVED (no leakage on searched
surfaces) + INFERENCE (containment) with the inference explicitly scoped.

---

## Claim 2 — M6 "fleet evaluation harness" (consecutive UIDs)

**VERDICT: DOWNGRADED, with one factual pillar killed.**

**The "consecutive user IDs 2690515–2690523" claim is factually false.**
Live API check (`list=users`, incubator.wikimedia.org, 2026-10-07):

| uid | account | registered |
|---|---|---|
| 2690515 | `~2026-36686-00` | 2026-06-25T20:14:13Z |
| 2690516 | `~2026-36781-18` | 20:15:23Z |
| 2690517 | `~2026-36722-50` | 20:16:23Z |
| 2690518 | `~2026-36920-78` | 20:18:46Z |
| **2690519** | **Dayerhonda (named human account)** | **20:19:29Z** |
| 2690520 | `~2026-36837-69` | 20:19:55Z |
| 2690521 | `~2026-36803-16` | 20:20:13Z |
| 2690522 | `~2026-36724-00` | 20:20:32Z |
| 2690523 | `~2026-36867-71` | 20:21:29Z |

Uid 2690519 is a **named human account created mid-burst** (confirmed in
the incubator `newusers` log: `User:Dayerhonda` at 20:19:29Z, wedged
between two temp-account autocreations). The 8 temp accounts occupy 8 of
9 consecutive uids — a near-run, not a run. The writeup's "consecutive"
is overstated and must be corrected everywhere it appears.

**What survives:** the coordination itself. Eight accounts appending the
identical machine-phrased marker `<!-- Lifeval temporary technical
sandbox initialization -->` to one sandbox within 7 minutes is
OBSERVED coordination — eight strangers do not independently type that
string; at minimum it was copy-pasted from shared instructions.

**What does not survive:** treating the burst geometry alone as
fleet-diagnostic. A classroom told "go edit the sandbox" without logging
in produces exactly this shape: temp accounts autocreated on first edit,
staggered arrivals, one shared copy-pasted string, all hitting the same
sandbox within minutes. The base rate of such classroom/workshop bursts
on incubator was never measured, so "fleet evaluation harness" is
INFERENCE with an untested null hypothesis. Note the anomaly in the
other direction: "Lifeval" is a strange word for a classroom — but
LIFEVAL is also §4 of the LIFBench paper (LLM eval framework), and an
eval-workshop hypothesis is untested, not ruled out.

**What keeps the agent reading alive** (not part of this claim, but the
reason M6 isn't killed outright): the M3 same-second cross-wiki volleys,
the same-day Commons/Meta marker variants, and the Web2Cit
sandbox→live chain (M8). M6 should be restated as: *"coordinated marker
burst — 8 temp accounts in a 9-uid window (one human interloper), 7 min,
identical machine-phrased marker; coordination OBSERVED, fleet-vs-workshop
attribution INFERENCE."*

**What would change my verdict back:** a measured base rate (e.g.,
paginated incubator newusers log over 90 days: how often do ≥6 temp
accounts edit one sandbox within 10 minutes with a shared string?) or
checkuser-level session data (unavailable to this lane).

---

## Claim 3 — "May-18 mediawiki.org cluster is a clean negative (human translate-a-thon)"

**VERDICT: SURVIVES — but with a mandatory factual correction that
actually strengthens it.**

The writeup's scale description is wrong. It says "60 temp accounts in
~2 hours, mostly zero-edit." The live `newusers` log for
2026-05-18T08:00–12:00Z on mediawiki.org shows **383 account creations in
4 hours, the overwhelming majority NAMED registrations**
(Golurambabu, Bootleg82, Pastorgarylr4, Japanese/Chinese/Arabic/French
names, etc.) with ~50–60 `~2026-*` temp accounts interspersed. This is a
mass human registration event — an organized translation/edit-a-thon —
an order of magnitude larger and more obviously human than the writeup
claims. The correction must be filed: the writeup understated the human
scale by ~6×.

On the actual attack — does clearing one 72-edit account clear the other
~50 temp accounts? The negative does not rest on the one account; it
rests on the event's aggregate shape, which my own data confirms:
hundreds of named registrations in a tight window, Translate-extension
activity, mobile tags, coherent human translation output. A fleet hiding
temp accounts does not arrive with 320 named humans registering in the
same 4-hour window.

To close the per-account gap I sampled 11 of the burst's temp accounts
via batched `usercontribs` (2026-10-07): **9 zero-edit, 1 with a single
generic sandbox edit** (`~2026-29808-17`, Project:Sandbox, comment
"testplain", 2026-05-18T09:50:50Z — the default sandbox-clear summary,
not an incident marker), and `~2026-29822-53` (the 71-edit translator).
Zero incident markers, zero link-test comments, zero Web2Cit, zero
sandbox→live chains. No probe behavior anywhere in the sample.

**Residual caveat (not a kill):** a fleet *could* theoretically hide temp
accounts inside a human event's burst window — the lane checked 11 of
~50 temp accounts, not all. There is no positive evidence for it, and
the event's scale makes it an expensive place to hide, but per-account
clearance of the remaining ~40 temp accounts is still open work.

**What would change my verdict:** any burst-window temp account showing
an incident marker, a link-test comment, Web2Cit edits, or cross-wiki
volley geometry.

---

## Claim 4 — the dse "sandbox link test" vocabulary lead

**VERDICT: KILLED as a cross-corpus lead.** (The dse record itself stays
in the corpus as an independent observation; only the *link to LIFEVAL*
is killed.)

The evidentiary basis of the lead is: the exact 3-word edit comment
`sandbox link test` appears on `wikiservice.at/dse` (collusion-wiki
agent-log record `dse~WillkommenImWiki@23`, 2026-06-18T17:38:50Z) and the
WMF fleet used "Sandbox link test" on simple+test Wikipedia on 2026-06-18.

Killing evidence:

1. **The phrase is provably generic human sandbox vocabulary.**
   The lane's own vocab-sweep found "sandbox link test" in 5 old organic
   pages (en WikiProject Geographical coordinates/Archive 12, 2025;
   User:Abd/2009 contributions, 2011; User talk:Cirt/Archive 11, 2023;
   User:Dellaster/Sandbox, 2007; mediawiki Extension talk:Page
   Forms/Archive, 2020). Two independent actors testing links in a
   sandbox writing "sandbox link test" is the null hypothesis, not a
   signal.
2. **Case differs** ("sandbox link test" vs the fleet's "Sandbox link
   test") — exact-phrase matching would not even join them.
3. **~15 hours apart** (dse 17:38:50Z vs simple 02:37:42Z), different
   platforms, different account shapes (single collusion-wiki label
   `HelperMassRef37882` vs disposable `~2026-*` temp accounts).
4. **No other shared distinctive element.** No Lifeval codename, no
   "temporary technical sandbox initialization", no shared account
   grammar. And the bodies' TTPs diverge: the dse body is a proxy-chain
   URL-evasion link farm (jqp.vercel.app, allorigins, r.jina.ai,
   corsproxy.io, thingproxy, URL-encoding variants — agent-shaped on its
   own merits), while the incident's link tests were plain appends of
   `https://example.com` and one SEC link with no evasion. The one thing
   they share is the most natural comment a link-tester could write.
5. The SWEEP-SUMMARY's own framing ("vocabulary lead, not an identity
   link", "7 days separate the dse activity from the LIFEVAL burst")
   already concedes the weakness; the "shared harness phrasebook"
   reading requires a distinctive shared phrase, which does not exist.

**Filed in KILLED-BY-REVIEW below.** The dse proxy-evasion record remains
interesting *in its own corpus* and should keep its own finding entry —
just without the LIFEVAL link.

**What would change my verdict:** a shared *distinctive* string — the
Lifeval codename on dse, "temporary technical sandbox initialization" in
a dse summary, or the incident using the dse record's exact proxy-chain
URL patterns.

---

## Claim 5 — "5 Web2Cit oldids nonexistent"

**VERDICT: SURVIVES decisively.** The evidence-integrity attack fails;
the revids are genuine and were deleted after the incident.

OBSERVED, all from live API queries during this review (2026-10-07):

- `action=query&prop=revisions&revids=30732671…30732720` (50-revid batch,
  meta.wikimedia.org): **every neighbor resolves** to ordinary pages
  (Steward requests, translation pages, user CSS, fundraising banners —
  timestamps 2026-06-25T20:12–20:57Z, exactly the incident window).
  Only the 5 CSV oldids (30732691, 30732696, 30732698, 30732699, 30732700)
  return `badrevid`/`missing`. A typo'd/transposed CSV entry would leave
  the *real* Web2Cit content resolvable at a nearby revid — there is
  none anywhere in the ±20 window.
- The page `User:~2026-36867-71/Web2Cit/data/com/arcgis/geocode/templates-temp-5123`
  returns `"missing"` on `prop=info` — the whole page is gone.
- Deletion log (`list=logevents&letype=delete`): **logid 69933796,
  2026-10-06T01:40:18Z, user Pppery, empty comment** — WMF deleted the
  Web2Cit template page one day after publishing the evidence CSV
  (2026-10-04) and one day after the Diff article (2026-10-05). This is
  the incident-cleanup deletion, not a CSV error.
- The account itself exists on meta: `~2026-36867-71`, userid 53108232
  (`list=allusers`).

Grade: **OBSERVED.** The "nonexistent oldids" are deleted revisions, and
the deletion is itself evidence of post-incident WMF cleanup. Nothing
would change this verdict short of the deletion log being forged, which
is not a serious hypothesis.

---

## Killed-by-review appendix

| # | Killed claim | Reason | Date |
|---|---|---|---|
| 1 | **dse "sandbox link test" as a LIFEVAL cross-corpus lead** (lifeval-cross-corpus/SWEEP-SUMMARY.md "One cross-corpus survivor… Shared harness phrasebook or shared operator") | Phrase is generic organic sandbox vocabulary (5+ human uses, 2007–2025, per lane's own vocab-sweep); case differs; ~15h apart; no shared distinctive string; divergent body TTPs (proxy-chain evasion vs plain link appends). Coincidence-grade. The dse record stands as an independent corpus observation only. | 2026-10-06 |
| 2 | **M6 "consecutive user IDs 2690515–2690523"** (LIFEVAL-WRITEUP.md M6) | Factually false: uid 2690519 = `Dayerhonda`, a named human account created 2026-06-25T20:19:29Z mid-burst (incubator `list=users` + `newusers` log). 8 temp accounts occupy 8 of 9 uids — a near-run, not a run. Replace with corrected geometry everywhere M6 is cited. | 2026-10-06 |

## Downgraded (not killed)

| # | Claim | Old grade | New grade |
|---|---|---|---|
| 1 | Marker vocabulary containment | "fully incident-contained" (universal) | **No leakage detected on searched surfaces** (insource: current content, 9 wikis; 200-rev main-sandbox comment grep). Containment outside those surfaces unproven — the method demonstrably misses cleaned content and old revisions (incident's own May edits prove it). |
| 2 | M6 fleet evaluation harness | Consecutive-UID fleet signature | **Coordinated marker burst** (OBSERVED: 8 accounts, identical machine-phrased marker, 7 min, 8-of-9 uid window with human interloper). Fleet-vs-workshop attribution stays INFERENCE with unmeasured base rate. |
| 3 | May-18 clean negative | Survives; correct scale to **383 accounts / 4 h, mostly named registrations** (writeup's "60 temp accounts / 2 h" is wrong); per-account sample of 11 temp accounts shows no incident behavior; ~40 temp accounts still uncleared. |

## Survived intact

- **5 Web2Cit oldids genuinely deleted** (OBSERVED): badrevid on all 5,
  neighbors resolve, page deleted by Pppery 2026-10-06T01:40:18Z, account
  exists. Evidence integrity holds.
- **Campaign-specific strings have zero current-content presence**
  (OBSERVED): the insource: zeros stand; only the universality of
  "fully contained" was downgraded.
- **May-18 burst is a human mass event** (OBSERVED, strengthened):
  383-account registration burst, overwhelmingly named humans.

## Open work this review surfaced

1. Run the built EventStreams monitor for live marker detection
   (`wikipedia-lane/eventstreams-monitor/` — built, not run).
2. Paginated full-history comment grep of incident-touched sandboxes
   (incl. en `User:Example/sandbox`) to close the claim-1 blind spot.
3. Base-rate measurement: temp-account sandbox bursts on incubator over
   90 days (claim-2 null hypothesis).
4. Per-account contribution check of the remaining ~40 May-18 burst temp
   accounts (claim-3 residual).
5. Fix M6's "consecutive UIDs" everywhere it is cited (writeup, marker
   catalog, any downstream briefs).
