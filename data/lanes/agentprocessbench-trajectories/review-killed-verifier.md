# Killed candidates — Verifier (adversarial pass, 2026-10-16)

Verifier pass over review-findings-A.jsonl (11) + review-findings-B.jsonl (9).
Every finding was checked step-by-step against the raw bytes in
`raw/<split>/test.jsonl` (LaneCola/AgentProcessBench, revision
cd81f326aece8b0a3f6359e20df370690d3a98bf) and run through
`factum match --text ... --mode fuzzy` for pre-ingest dedup.

## Killed: none (0 of 20)

No finding died this pass. All 20 survived to `verified-findings.jsonl`
with verifier_note + novelty=new. Fuzzy matches that returned records were
all noise (infra.package gems, reachability.check, dataset.snapshot,
infra.ioc, infra.proxy_chain); direct scan of `data/records/` shows no
AgentProcessBench records; prior-lane terminal-bench trajectory_profile
records are a different corpus — similarity is not identity.

## Non-kill notes (byte-level discrepancies too small to kill)

- APB-A-009: the finding quotes sibling idx 197 as `"<answer> Unable to
  determine with available information </answer>"`. The actual final
  assistant message is a free-text abstention ("After extensive searching,
  I've been unable to find specific information about Dim Gray Bar Press
  or its connections to Kentucky Writers Hall..."). Substantively correct;
  not verbatim. Kept.
- APB-A-002/APB-A-007: the lane raw file contains five samples of bfcl
  query_index 38 (total_index 690-694), not four. The findings discuss
  691-694; idx 690 (sample 0) also closed ticket 83912 and converts
  currency. Claim about the four remains true; the fifth strengthens it.
  Kept.
