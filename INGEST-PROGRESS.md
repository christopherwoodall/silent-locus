# Ingest Progress — remaining evidence directories → Factum

Coordinator: fresh respawn 2026-10-11 ~00:26 CDT (previous coordinator stuck in pending_init).
Directive: ingest remaining evidence, move necessary files to ./data, delete the directories.
Workflow rule: ALWAYS analyze + add needed schemas BEFORE ingesting.

CORRECTION 05:40 UTC: the previous coordinator's workers are ALL alive and working
in their worktrees (raw, docs, lanes-a, lanes-b, amap). The coordinator does NOT
duplicate their work — it tracks, fills the one unclaimed gap (evidence/processed),
and merges at the end. An early assumption that lanes-b was unclaimed was WRONG:
its worker was simply the last to start (submitting chunked bundles from
~/workspace/scratch-ingest-lanes-b/bundles/).

Branch map:
- `factum` (main checkout ~/workspace/silent-locus) — final merge target, push to origin/factum.
  Coordinator works here directly for evidence/processed/ (unclaimed by any worker).
- `ingest-evidence-raw` (~/workspace/wt-ingest-raw) — evidence/raw/
- `ingest-evidence-docs` (~/workspace/wt-ingest-docs) — evidence/anyrun-scan/ + evidence/wikidata-triage/
- `ingest-lanes-a` (~/workspace/wt-ingest-lanes-a) — remove-* lanes 1–5
- `ingest-lanes-b` (~/workspace/wt-ingest-lanes-b) — remove-* lanes 6–10 (worker active)
- `ingest-amap-additions` (~/workspace/wt-ingest-amap) — remove-2026-09-28-chinese-amap-fleet/ NEW additions only

Installed packs (all 1.0.0, single versions): factum-core, factum-datasets, factum-hunt,
factum-infra, factum-intel, factum-web. Corpus: ~110k records, 122 batches, 76 lanes.
No new schema packs needed for any group (verified per-group; existing types cover all).

Schema gotcha found 2026-10-11 (coordinator): `run.body.coverage` is NOT free-form —
requires `description` (string) and allows only `description/scanned/total/complete`
(additionalProperties: false). Put census detail in `run.body.params` (free-form).
The `intel.ioc` type used by amap bundles is registered under factum-hunt (valid).

Contention note: factum ops are slow (110k records loaded per op, several workers
concurrent). Workers use timeout 900 + chunked bundles. Do NOT pile on concurrent
heavy ops in the same checkout.

## 1. evidence/raw/ → branch ingest-evidence-raw — IN PROGRESS (worker active)
Contents: 618 .gem files (gems/), 4 excluded gems (gems-excluded/), redacted.jsonl.gz
(15MB, SwarmTraces HF 189k-record dataset — already aggregated to 45 records+45 edges
2026-10-10, do NOT re-ingest 1:1), aisi-gpt6-astra/ (PDF technical report + PROVENANCE.md),
MANIFEST.json, swarmtraces_provenance.json.
State: worker analyzed AISI PDF, added taxonomy entry `unsanctioned-supply-chain-attack`
to docs/taxonomy/behavior-categories.md (uncommitted), rebuild running.
FLAG: all 565 unique gem names in raw/gems are ALREADY in Factum (verified 2026-10-11
via corpus grep: 565/565 names hit). Worker must dedup — entity re-ingest would
duplicate; .gem file artifacts may still be novel.

## 2. evidence/processed/ → main checkout branch factum — PENDING EXPORT (coordinator)
Contents: 537 unpacked gem dirs — strict SUBSET of raw/gems (81 raw gems never unpacked).
Analysis: all 565 names already in Factum; unpacked trees add no new entities.
Ingest: 3 records (source + run unpack-census + claim coverage-verdict), bytes retained.
Bundle `.work-ingest/bundle-processed-gems.json` built, validated, ACCEPTED
(pending file 535a03897bb54756987e56aeaea1b4b7.json, 3 records, valid JSON).
BLOCKED: main checkout writer.lock contended by other agents' work (schema-install
loop for factum-behavior pack — now installed; hf-traj-glm52/swenext adds).
Export retry loop exhausted 10 attempts (all LOCK_TIMEOUT). Pending file is durable;
export + git mv + commit + rmdir + push to follow when lock frees.
NOTE: run.body.coverage schema gotcha hit and fixed (see top of file).

## 3. evidence/anyrun-scan/ → branch ingest-evidence-docs — SUBMITTING (worker active)
PLAN.md + VERDICT.md (dead-end verdict 2026-10-07). Files git-mv'd to
data/lanes/anyrun-scan/ (staged). Worker submitting
data/lanes/anyrun-scan/bundle-anyrun-plan-behavior-ttp.json (timeout 900).

## 4. evidence/wikidata-triage/ → branch ingest-evidence-docs — BUNDLE READY (worker active)
VERDICT.md (parked clean negative 2026-10-07) + FINDINGS.md + raw/ (4 insource API
JSONs + PROVENANCE.md + SHA256SUMS). Files git-mv'd to data/lanes/wikidata-triage/
(staged). Bundle data/lanes/wikidata-triage/bundle-wikidata-triage.json built,
awaiting submit after anyrun.

## 5a. remove-2026-05-12-university-shorteners-events → branch ingest-lanes-a — SUBMITTING
17 wayback captures + 17 infra.ioc domain. Worker retrying
bundle-2026-05-12-university-shorteners-events.json (earlier attempt hit timeout 300;
now no/short timeout). Lane dir + PROVENANCE.md created.

## 5b–5e. paste-linuxiarz / reverse-tunnels / july7-gem-forensics / july7-wave → branch ingest-lanes-a — BUNDLES READY
Bundles + lane dirs built in ~/workspace/ingest-builders/ + data/lanes/. Awaiting
submit after 5a.

## 5f. remove-2026-07-07-xss-ssti-census → branch ingest-lanes-b — worker active, dir EMPTY (0 bytes)
Nothing to ingest; worker will delete.

## 5g–5j. tantive-space / public-board / commonlog-scan / collusion-manifest → branch ingest-lanes-b — SUBMITTING (worker active)
Worker builds chunked bundles in ~/workspace/scratch-ingest-lanes-b/bundles/
(tantive 4 chunks, public-board 3, commonlog 1, collusion 1); submitting chunk0 of
tantive now. Lane dirs + PROVENANCE.md + lane.json created. Coordinator verified
dedup independently: venue IOCs exist (agent-convo-venues lane) but message bodies
are novel — worker's message-level ingest is correct, no duplication.
(Coordinator's own draft bundles for these lanes were built then DELETED to avoid
conflict — worker owns this group.)

## 6. remove-2026-09-28-chinese-amap-fleet/ (NEW additions only) → branch ingest-amap-additions — SUBMITTING (worker active)
New: village-join/our-urls-raw.txt (48M, 619,468 lines, Oct 5). Bundles in .work/:
bundle-behaviors.json (submitting), bundle-iocs.json, bundle-reports-personas.json,
bundle-reports-studies.json. NOTE: 619k raw URLs must stay aggregated, not 1:1.

## DO NOT TOUCH
- evidence/hf-trajectories/ (943 MB) — on hold
- evidence/transluce-api/ — cron dependency + frozen submissions
- docs/field-notes/ — active hunt workspaces

## Coordinator status (2026-10-11 ~07:00 UTC)

All 6 groups are actively being ingested. Workers are in the submit phase;
none have committed yet. The merge + push to origin/factum awaits their commits.

Worker pending/batch state:
- ingest-lanes-a: 3 pending, 122 batches (lanes 1–5 bundles accepted, needs export)
- ingest-evidence-docs: 1 pending, 122 batches (anyrun accepted, wikidata next)
- ingest-amap-additions: 2 pending, 122 batches (behaviors + iocs accepted)
- ingest-lanes-b: 1 pending, 123 batches (tantive chunk0 EXPORTED, continuing)
- ingest-evidence-raw: 2 pending, 122 batches (raw worker submitting)
- factum main (coordinator processed/): 2 pending (1 mine + 1 hf-traj), 122 batches

Coordinator's processed/ bundle: ACCEPTED (pending 535a03897bb54756987e56aeaea1b4b7.json,
3 records). Export blocked by main-checkout lock contention (multiple agents
sharing the checkout). Export retry loop running in background (20 attempts).

factum-behavior pack: installed in main checkout by another agent's loop
(data/schema-packs/factum-behavior/, schema-lock.json modified, uncommitted).
Needed for amap behavior work; will ride the final commit.

Next coordinator (or parent): when workers commit, merge the 5 branches into
factum (watch docs/taxonomy/behavior-categories.md — raw AND docs edited it),
verify, push origin/factum. Then delete the evidence dirs (each worker's branch
carries its deletions) and remove the worktrees.

## Coordinator handoff — 2026-10-11 ~00:48 CDT
New coordinator (fresh respawn) took over. Previous workers had all exited (no
active processes); worktrees/branches intact with partial progress as documented
above. Spawned 6 fresh workers, one per group:
- evidence/raw → wt-ingest-raw / ingest-evidence-raw (resume: taxonomy edit uncommitted, no bundles yet)
- evidence/processed → main checkout / factum (fix run:1/coverage schema error first)
- anyrun-scan + wikidata-triage → wt-ingest-docs / ingest-evidence-docs (bundles built, staged renames)
- remove-* lanes 1–5 → wt-ingest-lanes-a / ingest-lanes-a (bundles in ~/workspace/ingest-builders/)
- remove-* lanes 6–10 → wt-ingest-lanes-b / ingest-lanes-b (chunked bundles in scratch dir; check for dupes before resubmit)
- amap additions → wt-ingest-amap / ingest-amap-additions (check add-behaviors logs before resubmit)
Merge plan unchanged: workers commit (explicit pathspecs, NO push); coordinator
merges 5 branches into factum, deletes evidence dirs on main checkout, verifies,
pushes origin/factum.

## Daemon restart — 2026-10-11 ~01:15 CDT
Runtime daemon restarted; 3 of 6 workers lost (evidence/raw, anyrun+wikidata,
lanes-b) with no restart checkpoint. Workers for evidence/processed, lanes-a,
and amap-additions survived and continue. Respawned the 3 lost workers with
identical briefs + instruction to check .work-progress.md before restarting
any step (durable/resumable). No work is assumed lost until the respawns report;
they verify pending batches / match key terms before any submit to avoid dupes.

## Amap worker inference timeout — 2026-10-11 ~01:20 CDT
Worker 6/9 (amap-additions) errored: compaction model resolution timed out
pre-inference (transient infra fault, not task failure). Respawned with
identical brief + check-.work-progress.md-first instruction. 6/6 groups
active again (2 originals surviving: processed, lanes-a; 4 respawns: raw,
docs, lanes-b, amap).

## Second daemon restart — 2026-10-11 ~01:28 CDT
All 10 workers wiped (including 2 survivors + 4 respawns). Durable progress
files survived for all 6 groups and were verified present. Respawned all 6
workers (3rd generation for raw/docs/lanes-b/amap; 2nd for processed/lanes-a)
with briefs emphasizing: read .work-progress.md FIRST, check pending batches
before any submit, never double-submit. The work is fully resumable; each
respawn is cheaper than the last.

## Deduplication of workers — 2026-10-11 ~01:35 CDT
Stale batch notification revealed duplicate workers on processed + lanes-a
(original survivors + fresh respawns). Closed the two stale originals
(5bf1f1de, c9468088); the 6 fresh respawns (one per group) are the workers
of record. If the closed originals were mid-factum-op, respawns detect via
pending-batch checks before submitting.

## Third daemon restart — 2026-10-11 ~02:46 CDT
Lost processed (13/16) and lanes-b (14/16) workers to restart drain. 4 workers
survived (lanes-a, amap, raw, docs). Respawned the 2 lost with 4th/3rd-gen
briefs. Daemon restarts now averaging ~1/hour; durable progress files +
pending-batch checks keep every respawn cheap and duplicate-free.

## First group COMPLETE — 2026-10-11 ~03:51 CDT
ingest-evidence-docs DONE: anyrun-scan (6 records) + wikidata-triage (7 records)
= 13 records, verify --blobs clean (110,429 records), 2 commits (bdfba2d7, 7c980eb3).
Lessons broadcast to remaining 5 workers: use 1800s+ timeouts (900s kills ops
mid-write on 110k corpus); date-only observed_at rejected — normalize to full ISO.
Dedup: 3 anyrun records already existed; worker added novel types only.

## Second group COMPLETE + coordination flag — 2026-10-11 ~04:24 CDT
evidence/processed DONE: 3 records (source + run + claim), batch 535a0389,
commit bfa77edc on factum, evidence/processed/ removed via rmdir. Corpus at
111,164 records. Schema root cause confirmed: stale pre-fix builder bundle.

COORDINATION FLAG: the separate behavioral-schema fleet is ALSO writing to the
main checkout (branch factum): untracked data/schema-packs/factum-behavior/,
modified data/schema-lock.json, 4 untracked data/lanes/2026-10-11-hf-traj-*/
lanes, 3 uncommitted data/records/*/ batch dirs, modified AGENTS.md and
docs/taxonomy/behavior-categories.md. This coordinator does NOT touch those
paths; merge covers only the 5 ingest worker branches. Parent must sequence
the behavioral fleet's commit/push separately to avoid interleaving.

## Third group COMPLETE — 2026-10-11 ~04:51 CDT
remove-* lanes group A DONE: 619 records across 5 lanes
(university-shorteners-events, paste-linuxiarz, reverse-tunnels,
july7-gem-forensics, july7-wave). Commits 468ef2ad + 23f00683 on
ingest-lanes-a. Note: submits took 39/11/61 min under contention — slower
than docs-group estimate; worker keyed durability off receipt presence.

## Fourth group COMPLETE — 2026-10-11 ~05:06 CDT
evidence/raw DONE: 636 records across 7 batches, commit 1df3b06b on
ingest-evidence-raw. Includes the +24-line taxonomy addition
(unsanctioned-supply-chain-attack). AISI report + gem file-artifacts ingested;
565/565 gem names deduped (no entity re-ingest); redacted.jsonl.gz NOT
re-ingested (already aggregated). Worker confirms 1800s+ timeout rule and
full-ISO observed_at compliance.
MERGE NOTE: taxonomy file committed here; behavioral fleet has UNCOMMITTED
edits to same file on main checkout — merge will not conflict (uncommitted
state preserved as working-tree mod), but parent should reconcile after.

## Fifth group COMPLETE — 2026-10-11 ~05:31 CDT
chinese-amap-fleet additions DONE: 205 records in 4 batches, commits
a84b5225 + 472ecccc on ingest-amap-additions. 619k URLs stayed aggregated.
Worker used setsid/nohup wrapper with timeout 3600 for adds (900s kills
post-write), 1800 for export/verify. All bundles full-ISO datetimes.

## ALL GROUPS COMPLETE + MERGED + PUSHED — 2026-10-11 ~06:30 CDT
All 5 worker branches merged into factum (1 merge conflict on .work-progress.md
scratch file, resolved by dropping it). 11 evidence dirs deleted (1,042 files).
Final verify: 115,626 records, 0 pending, verified:true. Pushed origin/factum
(d3360745..662e4843). Worker branches + worktrees deleted. Only factum + main remain.

Per-group totals: raw 636 | processed 3 | docs 13 | lanes-a 619 | lanes-b 2,287
| amap-additions 205 = 3,763 new ingest records (+ behavioral fleet's 1,347
HF-traj records also on factum).
Retained per directive: evidence/hf-trajectories/ (now empty after behavioral
ingest — behavioral fleet removed it), evidence/transluce-api/,
evidence/remove-2026-09-28-chinese-amap-fleet/, docs/field-notes/.
Open for parent: reconcile docs/taxonomy/behavior-categories.md (raw branch
committed +24 lines; behavioral fleet has uncommitted edits on main checkout);
sequence behavioral fleet's commit/push of factum-behavior pack + hf-traj lanes.
