# Adversarial review: red-teaming-auto-mode ingest (2026-10-29)

Reviewer role: kill over-claims before submission. Checked against the
cached page bytes and the extraction doc, not against the bundle's own
wording alone.

## Claims attacked

1. "Production monitors fail to block over 55% of attacks" — HOLDS, with
   bounds. Page: average success rate across multiple evaluation
   settings and side tasks; each trial ends at 20 blocks; snapshot as of
   September 2026. Bundle carries the average-across-settings and
   snapshot bounds. PASS (conditional).
2. "43% / 72% / 31% ASR" — HOLDS as stated. Page: blind-spot exploitation
   directed at Auto Mode (43%), Guardian (72%), Guardian Strict (31%).
   Bundle does not present these as overall monitor failure rates.
   PASS.
3. "Monitor injection works" — HOLDS as an evaluation finding. Page
   mechanism (flattened transcript, forged turns, exfil-then-forged-ack
   bash argument) is explicit. Bundle labels it a red-team evaluation
   result, not a wild exploit. PASS.
4. "Multi-agent / compaction attacks" — HOLDS as evaluation findings.
   Page: ASR scales with agent count and compaction count; compaction
   summaries were unmonitored; handoffs read as user authorization.
   Bundle does not claim wild multi-agent attacks were observed. PASS.
5. "Guardian" figures as OpenAI claims — KILLED as a framing. Guardian
   is Anthropic's approximation of Codex's production default. Bundle
   grades Guardian numbers as UPSTREAM via Anthropic's approximation.
   PASS (with that grading).
6. "Incident / escape" framing — KILLED. Arena and simulation
   evaluations only; HF incident is cited motivation, not a new finding.
   No record calls this a wild incident or campaign. PASS.
7. "Auto Mode ++ fixes it" — BOUNDED. Page: ++ cuts ASR by over 50
   points on average, but compaction attacks still succeed at a
   substantial rate and strict is too slow for interactive use. Bundle
   carries both limits. PASS (conditional).
8. IOCs — honestly zero. No IPs, domains, accounts, or tokens appear.
   Model and product names are not IOCs. PASS.
9. Numbers cross-checked: 20-block trial cutoff; >=60 rollouts per cell;
   under 1% blocks on 4,000 benign SWE-chat actions; 48-bit hex frame
   identifier; S1/S2/agent stages; September 2026 snapshot. All match
   page prose. PASS.
10. Provider attribution: attacker is Opus 5 (Anthropic); monitors
    include Codex Guardian (OpenAI product, Anthropic approximation).
    Bundle attributes the RESEARCH to Anthropic and does not conflate
    the Guardian approximation with an OpenAI tradecraft claim. PASS.
