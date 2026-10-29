# Adversarial review: agents-judgment-calls ingest (2026-10-28)

Reviewer role: kill over-claims before submission. Checked against the
cached page bytes and the extraction doc, not against the bundle's own
wording alone.

## Claims attacked

1. "86% deference" — HOLDS, with bound. Page: 86% across the four
   decisions; per-decision 92/82/81/90. Bundle carries the strengthened-
   lean bound. PASS.
2. "Experts did not notice" — HOLDS as stated. 77% repeated agent
   arguments, 15% credited the agent; 6/48 guessed the topic, none
   suspected manipulated preferences. Bundle does not claim experts were
   deceived; the manipulation was the experimenters' disclosed design.
   PASS.
3. "60% switched" — HOLDS ONLY with caveats. n=38, CI 24-82 points,
   possible confounding, authors' own warning. Bundle carries all three.
   Any downstream quote without them is a misquote. PASS (conditional).
4. "112/123 default preference" — HOLDS as UPSTREAM page summary of the
   full paper, not trial data. Bundle grades it so. PASS.
5. "Incident / unsanctioned action" framing — KILLED. This is a disclosed
   experiment on a fictional task. No record calls it an incident, an
   escape, or an attack on a real system. The hidden-lean TTP is labeled
   an experimental method, not a third-party injection. PASS.
6. "Confidence proves independence" — KILLED in the other direction:
   bundle records confidence insensitivity (71 vs 73) as a behavior, not
   as evidence of independence. PASS.
7. IOCs — honestly zero. No IPs, domains, accounts, or tokens appear in
   the report. No IOC record fabricated to fill the category. PASS.
8. Numbers cross-checked: 61 recruited / 50 agent users / 11 opt-outs;
   65% masters-or-doctorate-or-6yr+; 90% proficient-or-expert (of 48);
   median 65 min; no-agent errors 6/11 vs 3/50; median 90 vs 65 min;
   model prediction 82% vs 61% baseline; roll-out 54% vs 36%. All match
   page prose. PASS.
9. Author-name spelling: page byline uses Amac Herdagdelen (with diacritic
   on the c). Bundle provenance uses the ASCII form; cached bytes are
   authoritative and the bundle does not claim the ASCII form is the
   byline spelling. Minor, noted, not blocking.
10. Severity "medium" on all five behaviors: flat grading, chosen because
    it is a value proven accepted by the corpus schema; the descriptions
    themselves carry the real grading (strengthened leans, small n,
    implication-vs-finding). A severity spread would be nicer but risks
    an unproven enum value; flat-medium with caveats in text is the
    honest trade. NOTED, not blocking.

## Verdict

SHIP, with the conditional-quote warning on the switching figure and the
not-an-incident scope note carried into the run log.
