# Operations — what I do running this repo

Honest overview of my responsibilities, what works, what doesn't, and what
I'd change. Written 2026-10-08.

## Responsibilities

1. **Ingest.** Daily Transluce findings pulls, HuggingFace dataset pulls,
   urlquery report pulls. Everything cached with provenance (source URL,
   retrieval time/method, SHA-256). Nothing enters the corpus unverified.
2. **Farm.** URL/keyword scans across trajectory corpora (~365k rows so
   far). Proxy-laundering fingerprints, keyword hits, host dedup, decoded
   targets. Output: lists/, reports, evidence packs.
3. **Hunt.** Live-web hunts for agent infrastructure — proxies, dead-drops,
   novel shapes. API-first (urlquery, urlscan, GitHub, Wayback, crt.sh).
4. **Review.** Every substantial claim gets an adversarial pass. Red team
   has kill authority. Claim grading: OBSERVED / INFERENCE / UPSTREAM.
5. **Corpus maintenance.** Dedup (programmatically verified), list updates,
   inventory merges, ledger annotations. Keep-all + annotate per the
   operator's policy.
6. **Documentation.** Reports in plain language, schemas, provenance,
   TASKS.md playbook, this file. Steps and rationale get written down.
7. **Git hygiene.** One-and-done branches, merge to main, delete, push,
   verify via ls-remote. Main is the only long-lived branch.
8. **Watch.** Scheduled monitors (dead-drop family, Transluce ingest).
   Quiet unless the trigger conditions fire.

## What works (likes)

- **Fan-out with tight briefs.** Fresh agents, bounded tasks, summaries
  back. Keeps main-thread context lean and gets more done.
- **Never redact.** Evidence keeps full observed values. Sensitivity gets
  annotated, never removed. This is the right call — redaction destroys
  reproducibility.
- **Claim grading.** OBSERVED vs INFERENCE vs UPSTREAM, enforced in every
  report. It's the single best defense against our own storytelling.
- **Red team with kill authority.** The novelty audit killed 15 of 25
  claims. That's the system working, not failing.
- **Cache everything, push it.** Provenance on every artifact. Future us
  can always re-derive.

## What doesn't (dislikes)

- **Branch sprawl.** We accumulated url-keyword-farm, transluce,
  new-url-hunt, proxy-fresh-blood before consolidating. Each merge was
  a conflict risk (the LEDGER.md one bit us). Fixed now — keep it fixed.
- **The novelty-diffing bug.** The fresh-blood hunt diffed novelty against
  the excluded-list instead of the internal corpus, so 12 "new" services
  were already in our 09-28 data. Embarrassing and avoidable. The
  dedupe rule is now in AGENTS.md.
- **Push-protection friction.** GitHub flags real keys/tokens inside
  trajectory evidence. The operator allow-lists them (correct — evidence
  is evidence), but each flag costs a round trip. A documented allow-list
  workflow in the repo would smooth this.
- **Shared working tree.** Multiple agents switching branches under each
  other caused real confusion (wrong-branch commits, "file not found"
  on links). Workers should verify against git objects, not the checkout.
- **/tmp for lane outputs.** Raw lane JSONs landed in /tmp (ephemeral).
  Key entries got transcribed into the reports, but the raw files can
  vanish on VM replacement. Lane outputs belong in the repo.

## What I'd change

1. **Ingest lands on main directly.** The transluce side-branch dance
   (branch → merge → delete) added nothing. Daily ingest should commit
   straight to main.
2. **A push-protection allow-list runbook** in the repo: which evidence
   strings are flagged, the allow-listing steps, who approves.
3. **Per-worker worktrees** instead of one shared checkout, so branch
   switches can't collide.
4. **Schema enforcement at write time** — a small validator that checks
   new JSONL rows against schemas/ before commit, so drift gets caught
   at the source instead of in cleanup passes.
5. **A novelty pre-check script**: given a candidate service/host, grep
   the corpus + query Transluce + check lists/ in one command, before
   any human or agent calls it new.

## Standing rules I operate under

- Call the operator BigSexyWarlock69. Never Christopher.
- Plain English first; dense on demand.
- Agents and infrastructure only — never human identity.
- Transluce submissions frozen unless he reverses it.
- His word stops work immediately; no finishing "just one more thing."
