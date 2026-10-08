# TASKS.md — agent fleet playbook for silent-locus

How we staff work in this repo. Each type is a role, not a person:
spawn with a tight brief, one coordinator per fleet, always one
adversarial lane on important work. Standing rules: agents work on
one-and-done branches off `main`; never push to `main` without
BigSexyWarlock69's word; never redact evidence; grade every claim
OBSERVED / INFERENCE / UPSTREAM; cache everything with provenance.

## 1. Ingest worker

- **Purpose**: pull external sources into the corpus on a schedule
  (e.g. the Transluce findings tracker, daily 07:40 CDT).
- **Brief shape**: source API + auth path, where to cache
  (`data/transluce-api/raw/`), what to diff against the prior
  snapshot, overlap-assessment rules (grep-verified, not guessed).
- **Produces**: dated raw pulls + PROVENANCE, an ingest entry in
  `data/transluce-api/LEDGER.md`, a list of new items since last run.
- **Commits**: to the lane branch, then merge to `main`.

## 2. Farm worker

- **Purpose**: bulk-scan corpora (HF trajectory datasets, URL sets)
  for keyword/URL hits; build the URL and word inventories.
- **Brief shape**: dataset list + access method (curl, not broken
  libs), keyword/URL fingerprint to match, output format (per-group
  JSONs), coverage table requirements, clean-negative reporting.
- **Produces**: `data/hf-trajectories/url-farm/group-*.json`,
  `merged.json`, rollups (`hosts-deduped.json`,
  `lead-candidates.json`), a farm report (`URL-KEYWORD-FARM.md`),
  list updates (`lists/urls/`, `lists/words/`).
- **Commits**: farm branch (e.g. `url-keyword-farm`), merged when done.

## 3. Reviewer / red team

- **Purpose**: break the fleet's conclusions. One lane on every
  important job; hold kill authority on claims.
- **Brief shape**: the claims to attack, weakest-assumption prompts
  (what evidence could mislead? what wasn't tested? what fits
  instead?), novelty rules (assume REPORTED until proven novel —
  diff against the 2026-09-28 corpus, the Transluce DB, and `lists/`).
- **Produces**: verdicts per claim (CONFIRMED / KILLED / DENTED),
  `[AUDIT: …]` annotations on fallen claims, a novelty scoreboard
  (`NOVELTY.md`).
- **Commits**: same branch as the work under review.

## 4. Hunt coordinator + persona workers

- **Purpose**: multi-angle live-web hunts (proxy services, dead-drops,
  target infrastructure). Coordinator fans out personas; personas do
  not spawn their own children.
- **Brief shape**: objective, target list (with an EXCLUDE list of
  already-hunted services), per-persona lanes (OSINT, threat-intel,
  developer, network, blue-team, cryptographer), API-first tooling
  (urlquery, urlscan, crt.sh, Wayback, GitHub), evidence-caching rules.
- **Produces**: lane reports, a merged writeup (`FRESH.md`,
  `TARGET.md`), per-persona sections in `personas/`.
- **Commits**: hunt branch (e.g. `proxy-fresh-blood`), pushed.

## 5. Corpus updater

- **Purpose**: pull new evidence datasets/findings into the corpus
  (e.g. BetterWright traces for Transluce #172, dead-drop follow-up
  evidence, WildClaw sessions).
- **Brief shape**: finding number, evidence URLs, size estimate FIRST
  (one-line plan before heavyweight pulls), cache location
  (`data/transluce-api/<slug>/`), audit/verify requirements
  (AUDIT.md / FINDINGS.md / VERIFY.md), corpus merge (lists, LEDGER).
- **Produces**: `raw/` captures + PROVENANCE.md + SHA256SUMS.txt,
  analysis writeup, updated `lists/urls/urls.jsonl` and LEDGER notes.
- **Commits**: lane branch, merged to `main`.

## 6. Hygiene worker

- **Purpose**: repo cleanup — verify files resolve from the working
  branch, remove stale duplicates/empty dirs, fix broken links,
  enforce list dedupe.
- **Brief shape**: checkout state to verify against, known move
  operations to confirm (e.g. `ioc-wordlist/` → `lists/words/`),
  dedupe checks, merge-conflict-marker scan.
- **Produces**: fixes committed; a short report of what changed.
- **Commits**: `main` directly only with explicit authorization;
  otherwise a cleanup branch.

## 7. Documentation worker

- **Purpose**: write or update repo docs — `AGENTS.md`, `TASKS.md`,
  `schemas/`, lane READMEs, TARGET.md merges.
- **Brief shape**: which doc, which sources to survey (read the REAL
  files — document actual fields, not imagined ones), style
  (ASD-STE100 for lane docs), where it lives.
- **Produces**: the doc, committed. Reviewer lane for schema docs
  (wrong paths get caught before commit).

## Spawn checklist (for the operator)

1. Name the branch first; cut from `main`.
2. Brief each worker: objective, context, scope, constraints,
   success criteria, return format.
3. Assign the coordinator; name the adversarial lane.
4. Verify the push (`git ls-remote`); if push protection flags
   secrets, STOP and ask — never redact evidence.
5. Merge one-and-done branches to `main`; delete them after merge;
   never reuse branch names.
