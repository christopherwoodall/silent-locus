# Hunt methodology

## Terms used here

- **PRIMARY**: evidence we collected ourselves, with a provenance triple. Findings rest on PRIMARY.
- **SECONDARY**: cited reports or context. SECONDARY supports, but never proves, a finding.
- **Observed**: we saw the bytes. This is the strongest basis for a claim.
- **Inference**: we concluded it from what we saw. An inference is weaker than an observation.
- **Upstream**: someone else reported it. An upstream claim is only as strong as its source.
- **Novelty**: the check that a behavior has not been reported before. A behavior already reported is overlap, not a new finding.
- **Corpus**: the catalog and lists we already hold. The novelty check searches the corpus first.
- **Tracker**: an outside findings tracker we check for prior reports, where one is configured. No tracker is configured in this profile. Novelty queries are read-only, never submissions.

## Grades

Grade every claim. A claim with no grade is not ready to ship.

- **Ungraded**: filed, but not yet assessed. A novel observation below the confidence cap is filed as ungraded. It is never dropped and never auto-promoted. It waits for Counsel.
- **Observed**: the bytes were seen directly, with provenance.
- **Inference**: the claim is a conclusion from observed bytes, not the bytes themselves.
- **Upstream**: the claim comes from someone else's report. Upstream claims never auto-promote. They enter the kanban as ungraded and wait for local Counsel.

Grade describes the basis of the claim, not a guarantee of truth. An observed claim can still be misread. An upstream claim can still be right. The grade tells the reader how the claim was made.

## PRIMARY / SECONDARY rule

Findings rest on PRIMARY only.

- PRIMARY evidence: we fetched it, we kept the exact bytes, we recorded the provenance triple and the hash. See `evidence-capture.md`.
- SECONDARY evidence: a cited report, a summary, a quote from someone else's work. Use it for context and for leads. Never use it as the sole basis for a finding.

If a claim has only SECONDARY support, it is not a finding. It is a lead. File it as a lead, grade it upstream, and collect PRIMARY evidence before you promote it.

A finding always has a claim behind it, and the claim always has PRIMARY evidence behind it. No stage is skipped.

## Novelty checks

Check novelty before you call any behavior NEW. Novelty is unestablished until the checks below are complete. A failed or incomplete check blocks a confident novelty conclusion.

Run these checks, in order:

1. Search the catalog for the behavior, the marker term, and the key identifiers. Search by exact term and by near match. An exact-match-only search is not enough.
2. Search the operational lists for the same terms. Lists hold known markers, known hosts, and known inventories.
3. Search the legacy internal corpus, where one exists on the instance, for the same terms.
4. Query the findings tracker, where one is configured, for the same behavior. No tracker is configured in this profile, so this step is skipped until one is configured. Any novelty query is read-only, never a submission.
5. Record every search: what you searched, the scope, the coverage, and the result. A search with no record did not happen.

Rules for the result:

- Previously reported behavior is overlap, not a new finding. Record the prior report as the citation. Do not claim it as new.
- No match under the reported query and scope means "not found in that scope". It does not prove that no one, anywhere, reported it. State the scope with the result.
- Do not invent a prior-report citation when overlap has not been found. Do not invent a novelty claim when the checks are incomplete.
- A novel observation below the confidence cap is still filed as ungraded. Novelty beats the confidence cap for filing. The cap beats novelty for promotion. A novel, low-confidence item is filed, never dropped, never auto-promoted.

## Patterns of behavior, not strings

Judge patterns of behavior, not strings alone. A string match alone is weak evidence. Strong evidence is a pattern across observations.

Score these patterns:

- Burst timing: many related actions in a short window.
- Tag-grammar evolution: marker terms that change in a structured way over time.
- Target-side joins: joins on the target host or target IP of the scanned object, never on submitter traits. Submitter traits (who submitted a report, with what agent or account) are never used for attribution.
- Relay shapes: traffic that moves through the same chain of hosts or services.
- Dead-drop lifecycles: endpoints that appear, receive data, and go cold on a schedule.
- Time-of-day windows: activity that clusters in the same hours.
- Cross-board beacons: the same marker that appears on more than one board or surface.

A string-only match is downgraded in review. A string match plus a behavior pattern is stronger. A behavior pattern with PRIMARY bytes behind it is the basis for a claim.

## The promotion path

An item moves observation to claim to finding. Three stages, three transitions, each fired by a named actor:

1. Observation to claim: the Linguist lane writes a claim row, linked to the observation and its evidence.
2. Claim to finding: Counsel gives a promote verdict with a mandatory reason. The Ledger then writes the finding row.
3. Any stage to dismissed: Counsel gives a dismiss verdict with a mandatory reason, or the operator dismisses it directly.

No stage is skipped. A finding always has a claim and a Counsel verdict behind it. Every dismissal records a reason. No silent dismissals.

## Adversarial review

Before a finding ships, attack it:

- What assumption is weakest?
- What evidence could mislead?
- What did we fail to test?
- What other explanation fits the evidence?
- What would make this conclusion false?

If the attack finds a real flaw, fix it or downgrade the claim. Do not ship around a known flaw.

## What not to do

- Do not call a pattern match confirmed behavior. See `triage.md`.
- Do not promote similarity into corroboration or identity without evidence.
- Do not treat a scanner hit as a finding. A hit is a candidate. Triage decides what it is.
- Do not hunt human identity. Scope is agents and agent infrastructure only.
- Do not use a finding from another operator's import as a local finding. Imported findings are force-graded upstream, tagged with the source operator, and wait for local Counsel.
