# Adversarial review — integrated analysis, July 2026 RubyGems spike set

## Draft verdict: NO-SHIP

The adversarial lane reviewed the five working lanes plus the prior
review and the reconciled census, by fresh recomputation from the
CSV and census JSONs. Its full draft (509 lines) is preserved at
`working/adversarial-review-draft.md`. Its verdict on the draft
was NO-SHIP, with 20 numbered fixes. This file records each fix
and its disposition in REPORT.md. No fix was left unaddressed.

## Dispositions

1. **Disproof language.** Applied. Every "is not agent activity"
   sentence now reads "is not established as agent activity on
   this evidence." "Probe-shaped cluster" replaces bare
   "probe cluster" as a fact; probe intent is graded INFERENCE.
2. **"Abandoned residue" upgrade.** Applied. Headings now read
   "listing residue (INFERENCE, unproven against
   still-referenced fixture)" with the settling discriminator
   stated.
3. **testgem-mini rank and landing.** Applied. Rank corrected
   (4th of 23, highest of the 2 test-named). Class changed to
   "test-named, use UNEXPLAINED." Dependents check run for
   this report (zero reverse dependents, §3.3) and
   download-by-version fetched (even spread across 5 July-7
   versions). Neither promotes it to legit.
4. **"Continued maintenance" blanket.** Applied and then
   earned where possible. Version publish dates fetched for
   all 23 live gems (live-version-dates-20261027.json).
   Report now splits 13 dated post-July versus 10 without.
   Blanket maintenance language is gone.
5. **CSV-latest equals live-latest.** Corrected to 4 of 23,
   first-census latest field cited by name. Reconciled JSON
   latest-field incompleteness stated.
6. **Version-loss list.** Published in full (at least 9
   gems) with the yanked-as-inference caveat and the
   platform-duplicate caveat. jrjackson field conflict
   resolved in favor of the versions endpoint (0.5.5,
   October 21, 2026).
7. **Survivor rule collapse.** Applied. Report states
   honestly that classification is name plus summary
   self-description with other data as context only, and
   marks minitest-hashdiff and testgem-mini UNCERTAIN.
8. **117 versus 105.** Applied. Neither is quoted as a
   positive "probe-descriptive" count. Report quotes the
   earned residual form (203 minus 86) with its rule, and
   records 105 as irreproducible plus the 33-row hole.
9. **Linguist method underspecified.** Applied. Report
   states the 203 / 20 split rests on manual judgement and
   cannot be reproduced from a printed signal list alone.
   Grade is OBSERVED-shape-plus-judgement.
10. **Apex 114.** Applied. 115 substring (114 prefixed)
    used throughout; 114 as a substring count never appears
    except in this corrections log.
11. **YAML / tar collisions.** Applied. Report always pairs
    the word-signal count with the document-shape count
    (YAML-word 4 / document 0; tar-wording 3 / traversal
    string 0). Bare quoting is banned in the text.
12. **SSRF field attribution, webhook count.** Applied.
    SSRF split is 23 homepage cells plus source and
    summary rows as detailed in §5; webhook is 19 homepage
    cells.
13. **Public-IP trap.** Applied. The 10 public-IP homepages
    are split out everywhere and never called internal
    targets.
14. **"66 unchecked source URIs" false.** Applied. Gap
    deleted. True statement published (§8): 196 of 196
    present tombstoned source URIs checked, 1 excluded by
    design, 313 tombstoned rows with no URI. Gaps re-ranked
    without it.
15. **"Split" recommendation unsafe.** Applied. Admission
    narrowed to names, grammar, timing, and dates only,
    with source and homepage fields stripped or flagged
    pattern-derived. Grade string required inside each
    record. The held-out 20 (containing 18 of 23 live gems)
    are addressed explicitly.
16. **pkg-review-2 unconditional.** Applied. Recommendation
    is now CONDITIONAL on a concrete severity-reuse
    decision, scope 513, all label sets preserved,
    matched-shape check first.
17. **"Further public searching will not close this"
    overclaim.** Applied. Bounded language used: no receipt
    found in the public sources checked; receipts sit in
    private inboxes. Do-not-probe restraint kept.
18. **"Sampled batch names" understatement.** Applied.
    Full-census figures used (310 of 310 combinatorial,
    100 of 100 tester gone).
19. **Artifact denominators.** Applied. Every artifact
    sentence cites field and denominator. The 48
    out-of-band rows versus 49 artifact URLs different-sets
    note travels with both numbers.
20. **First-census leakage.** Applied. Draft grepped for
    superseded figures. Only reconciled figures ship, plus
    the ship-time jrjackson refresh, each labelled as such.

## Shell gone/stub caveat — downstream impact (reviewer's assessment, adopted)

Real, but no downstream count depends on the wrong reading:
all counts that matter use content, not the label. Wording
fixes applied: "Diffend gone = 1" never appears without
"no-diff = 510, redirect-status = 28" beside it, and the
tombstoned labelled-stub count (509) is kept distinct from
the all-533 stub line.

## What survived attack (reviewer's list, adopted)

Prior verdicts (a)–(e); combinatorial 310; university
template 309; placeholders 86; epoch names 34; `ssrf-*`
prefix 23; cryptologist union arithmetic; shell taxonomy;
callback UNRESOLVED; jrjackson dominance (94.3%); blank
≠ safe caution (21 of 23 live rows are blank-field rows).

## Open quality gate

No second independent adversarial pass re-ran after the
fixes were applied. The dispositions above are the
coordinator's application of the reviewer's fix list,
checked against the reviewer's recomputed count table.
A re-pass is recommended before any outward-facing use of
this report, but it is not a blocker the operator asked to
gate on: the operator ordered the integrated analysis, and
this file discloses the gate's state plainly.
