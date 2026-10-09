# Wikipedia edit-hunt — independent review lane (2026-10-07)

Full adversarial audit of the closed `wikipedia-lane`. Fresh agents only;
none of the original lane workers. Reviewers hold kill authority per
standing directive.

## Scope (read-only on the closed lane; write only here)

- `wikipedia-lane/DONE.md` — every graded claim (OBSERVED / INFERENCE / UPSTREAM)
- `wikipedia-lane/LIFEVAL-WRITEUP.md` — marker bytes, links, geometry
- `wikipedia-lane/reviewers/REVIEWER-3.md`, `REVIEWER-4.md`
- Sweep outputs: `vocab-sweep/FINDINGS.md`, `ngram-sweep/FINDINGS.md`,
  `wordlist-wiki-sweep/FINDINGS.md`, `lifeval-cross-corpus/SWEEP-SUMMARY.md`
- `wikipedia-lane/raw/NEWUSERS-PROVENANCE.md`, cached evidence, `records.json`
- Branch `wikipedia-edit-hunt-2026-10-06` commits + open PR #15
- Out of scope: `revhistory-grep/` (in-flight, separate job — note only)

## Review tracks

1. **Claims audit** — every factual claim in DONE.md re-checked against its
   cited evidence. Verdict per claim: HOLD / DOWNGRADE / KILL.
2. **Evidence & provenance audit** — cached files exist, SHA-256s match,
   diff links resolve, provenance notes complete, no redacted evidence.
3. **Methods audit** — sweep coverage claims (srnamespace, sampling,
   dedup), the urlquery htmx fix, dataset line counts, limitation honesty.
4. **Red team** — one reviewer's sole job is to break the Lifeval finding
   and the M8 chain. Strongest counter-readings, alternative explanations.

## Deliverable

`REVIEW-VERDICT.md` here: per-claim table, kill appendix, link-check
results, and an overall verdict on whether the lane is publication-ready.
Commit to the branch when done; never touch main.
