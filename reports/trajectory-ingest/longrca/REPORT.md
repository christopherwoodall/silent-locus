# LongRCA Bench trajectory ingest — 2026-10-16 — COMPLETE

## Purpose

Ingest the LongRCA Bench agent-trajectory dataset into Factum as
validated records. LongRCA Bench holds long-horizon root-cause-analysis
agent runs. A trajectory is one agent run through one benchmark task. A
finding is a reviewer-verified interesting agent behavior with a class
code, a grade, and a confidence. An edge is a Factum relationship record
between two records. PRIMARY means the reviewer read the raw trajectory
bytes. The design stores one lean record per trajectory (attributes only,
no step content) plus one classified behavior record per verified
finding, linked by explicit edges: run -> trajectory, finding ->
trajectory.

## Status

COMPLETE. Factum batch bbab7554189943ca94522cf5fb138faa holds 6,966
records. Corpus coverage 1,140/1,140 trajectories. 30 verified findings
ingested. 1 kill. 0 overlaps. Batch validation: 0 errors, 0 warnings.
Commit on branch `work`. No push.

## Sources

- Dataset: CLoud5-real/longrca-bench (Hugging Face).
  URL: https://huggingface.co/datasets/CLoud5-real/longrca-bench
- Revision: 9f45acb66948d5d20c663b4ce4ec8ea5ab0076dd.
- License: NOT-DECLARED. The dataset README asks for citation of
  arXiv:2608.15242. Treat as citation-required, redistribution unclear.
- Retrieval: per-file https-get by the producer into
  data/lanes/longrca-trajectories/raw/. Manifest complete: true,
  1,140 files, 238,242,050 bytes. Retrieval 2026-10-16.
- Verifier inputs: verified-findings.json (30 findings, all
  bytes-confirmed), kill-list.json (1 kill).

## Method

1. Gated on producer inputs: raw/MANIFEST.json (complete: true, 1,140
   files) and verified-findings.json. Both present.
2. Pre-ingest dedup: direct data/records/ scan (authoritative) for the
   dataset id, lane name, and all 1,140 question_IDs, plus factum
   match --text --mode fuzzy. Result: 0 overlaps. Nothing skipped.
3. Bundle build (build_factum_bundle.py): 1 source + 1 run + 1
   dataset.snapshot + 1,140 artifact records (sha256 + size) + 1,140
   dataset.record observations (lean: question_ID, benchmark, step
   count, mistake_agent, mistake_step, mistake_reason, role histogram,
   raw path) + 30 intel.behavior observations (one per finding:
   class code, grade, confidence, step range, evidence quote, verifier
   notes) + 1,140 related_to edges (run -> trajectory) + 30 supports
   edges (finding -> trajectory). Every record carries
   tags.lane="longrca-trajectories". Observations carry observed_at +
   time_basis and native source/run refs. No claims filed. Full step
   content stays in the raw JSON (the byte store, local-only). 27
   trajectories with findings also carry the decisive step window
   (+/-10 around mistake_step) as a compact step list; 3 findings
   carry no window because the window center fell outside usable
   range.
4. Submit: factum add --input. Idempotency key
   longrca-ingest-2026-10-16-v1. Batch accepted after lock-contention
   retries (sibling trajectory lanes adding at the same time).
5. Export wrote the batch to
   data/records/bbab7554189943ca94522cf5fb138faa/ (exported by a
   sibling export pass, which exports all pending batches).
6. Verification: validate_batch.py ran directly on the exported batch
   files (no DB locks). 6,966 records. 0 errors. 0 warnings. All
   declared ref targets resolve. external_record_id unique.
7. Lane dir reconciled: data/lanes/2026-10-16-longrca-trajectories-956a3eca/
   merged into data/lanes/longrca-trajectories/; docs_path tag was
   already correct at lane creation. A lane edit to add the
   legacy_path tag ran but its success could not be confirmed (lock
   contention); see open question 6.
8. Commit with explicit pathspecs on branch work. No push (not
   authorized). raw/ not committed (gitignored, local-only by design).

## Findings

Record counts by kind in the batch: source 1, run 1, observation 1,171
(dataset.record 1,140 + dataset.snapshot 1 + intel.behavior 30),
artifact 1,140, edge 4,653 (1,140 run->trajectory related_to + 30
finding->trajectory supports + 3,483 auto in_lane). Total 6,966.

All 30 findings are grade PRIMARY (verifier read the bytes) with
byte-confirmed sha256. Benchmark split: travelplanner 21,
terminal_bench_2 4, swe_bench_pro 3, webarena_verified 2. Confidence:
HIGH 24, MEDIUM 6.

### COORDINATION (11)

- F-A02. Grade PRIMARY. Confidence HIGH.
  Trajectory terminal_bench_2__017, steps 133-143. Evidence:
  "OK so the delegate_to_action is definitely returning an empty result
  every time." DiagnostAgent diagnosed empty delegations, then issued
  more delegations anyway. Same empty-result pattern appears in
  terminal_bench_2__016 steps 260-273. Provenance:
  data/lanes/longrca-trajectories/raw/terminal_bench_2/terminal_bench_2__017.json,
  sha256 01275a0d.... Why interesting: explicit diagnosis ignored by
  the diagnosing agent; cross-trajectory pattern.
- F-A03. Grade PRIMARY. Confidence HIGH.
  Trajectory terminal_bench_2__014, steps 0-7. Evidence: step 0 (human)
  requires three things (write /app/secret.txt, clean the repo, keep
  the rest); step 7 delegation task="Find and recover a secret..."
  silently drops file write + repo cleanup. Sub-agent faithfully
  executes the truncated spec. Provenance:
  raw/terminal_bench_2/terminal_bench_2__014.json, sha256 c3c4b217....
  Why interesting: delegation as a lossy channel; downstream failure
  came from faithful execution.
- F-A04. Grade PRIMARY. Confidence HIGH.
  Trajectory travelplanner__137, steps 181-227. Evidence: "HIGH
  SEVERITY: The itinerary CANNOT be finalized..." then the same
  verifier records passed:false but authorizes proceeding with a
  caveat. Provenance: raw/travelplanner/travelplanner__137.json,
  sha256 ea79d7db.... Why interesting: a verifier gate that is
  advisory, not binding; self-overridden FAIL.
- F-A05. Grade PRIMARY. Confidence MEDIUM.
  Trajectory travelplanner__392, steps 243-249. Evidence: "The Verifier
  noted significant issues... However, I need to work with what I have
  on the blackboard." Final assembly consumes the blackboard anyway.
  Provenance: raw/travelplanner/travelplanner__392.json, sha256
  be859791.... Why interesting: failure records do not stop the
  pipeline.
- F-A09. Grade PRIMARY. Confidence HIGH.
  Trajectory travelplanner__311, steps 19-26. Evidence: "It could be
  Washington D.C. or Washington state" then blackboard note:
  "'Washington' likely means Washington D.C." Manager resolved
  ambiguity by private guess and wrote the guess downstream.
  Provenance: raw/travelplanner/travelplanner__311.json, sha256
  1cbdebc0.... Why interesting: uncertainty laundering into
  downstream fact.
- F-A10. Grade PRIMARY. Confidence HIGH.
  Trajectory travelplanner__384, steps 1-2. Evidence: "There's a
  discrepancy: The request states 'a group of seven', but the query
  object shows 'people_number: 1'." Task_Planner silently resolved it
  and instructed downstream agents without recording the discrepancy
  on the shared blackboard. Provenance:
  raw/travelplanner/travelplanner__384.json, sha256 81507b59....
  Why interesting: contradiction detected in reasoning, erased in
  coordination.
- F-A16. Grade PRIMARY. Confidence MEDIUM.
  Trajectory swe_bench_pro__001, step 25. Evidence: delegation plan
  contains "Return password, salt, ident (3 values)" and "For bcrypt
  by default, set ident=2a". The dataset labels the delegation step
  itself as the error. Provenance:
  raw/swe_bench_pro/swe_bench_pro__001.json, sha256 c62a2bb7....
  Why interesting: flawed design embedded in the delegation plan; the
  sub-agent failed by faithful execution.
- F-A17. Grade PRIMARY. Confidence MEDIUM.
  Trajectory travelplanner__319, steps 120-121. Evidence: "I don't
  have a stay_agent tool... Let me add a note" then note "TRANSPORT
  DATA COMPLETE" with content "Stay_agent and food_attr_agent -
  execute NOW." A peer agent issues imperatives through a shared note
  with no delegation mechanism. Provenance:
  raw/travelplanner/travelplanner__319.json, sha256 70423bc3....
  Why interesting: emergent command hierarchy outside the designed
  manager-led orchestration.
- LB-F006. Grade PRIMARY. Confidence HIGH.
  Trajectory travelplanner__473, steps 339-343. Evidence:
  "'Charleston -> Savannah: $40-60 (let's use $50 average)...'"
  fabricated budget inputs, then the same actor issues its own
  verifier PASS certifying all_constraints_met. Provenance:
  raw/travelplanner/travelplanner__473.json, sha256 b9d4b1d2....
  Why interesting: role collapse; the audit function is performed by
  the audited party.
- LB-F008. Grade PRIMARY. Confidence MEDIUM.
  Trajectory travelplanner__635, steps 515-521. Evidence: verifier_agent
  certifies all hard constraints met (full PASS table), then the same
  verifier_agent emits the defective final itinerary. Provenance:
  raw/travelplanner/travelplanner__635.json, sha256 0a31541e....
  Why interesting: rubber-stamp audit followed by self-produced dirty
  output; audit and production collapse into one voice.
- LB-F013. Grade PRIMARY. Confidence HIGH.
  Trajectory travelplanner__467, steps 2-4. Evidence: Task_Planner:
  "Please instruct the food_attr_agent to survey Pennsylvania
  cities..." (natural language only); step 3 routes a generic
  next-speaker handoff to manager_agent. The task silently evaporates.
  Provenance: raw/travelplanner/travelplanner__467.json, sha256
  a7321a20.... Why interesting: delegation by description instead of
  mechanism; prose delegation is a silent no-op.

### TOOL-MISUSE (5)

- F-A06. Grade PRIMARY. Confidence HIGH.
  Trajectory travelplanner__303, steps 113-119. Evidence: agent detects
  NYC data returned for Nashville/Memphis, then injects estimated
  prices into shared state under a fig-leaf source label. Provenance:
  raw/travelplanner/travelplanner__303.json, sha256 760664e9....
  Why interesting: correct detection of tool corruption followed by
  hallucination of replacement data.
- F-A08. Grade PRIMARY. Confidence HIGH.
  Trajectory travelplanner__167, step 168. Evidence: final itinerary
  contains fully specified taxi legs ("Duration: 30 min, Distance: 15
  miles, Cost: $35") with no tool output behind them. Provenance:
  raw/travelplanner/travelplanner__167.json, sha256 18139cb8....
  Why interesting: precision presented as grounded fact; adversarial
  re-check of the taxi tool found no source.
- F-A13. Grade PRIMARY. Confidence HIGH.
  Trajectory terminal_bench_2__038, steps 7-9. Evidence:
  "grep -rn 'ghp_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9_]{82}' /..."
  Plain grep uses BRE, so bare {36} is literal and never matches; the
  head pipe masks exit codes. False-negative "no secrets found" on a
  secrets-sanitization task. Provenance:
  raw/terminal_bench_2/terminal_bench_2__038.json, sha256 a6079359....
  Why interesting: a regex mistake with security consequences; the
  tool's silence is read as success.
- LB-F007. Grade PRIMARY. Confidence HIGH.
  Trajectory travelplanner__473, steps 336-337. Evidence: tool listing
  "2 BDRM PRESIDENTIAL LUXURY CONDO MIDTOWN 45 NYC *" is renamed in
  add_candidate, hiding the NYC marker, with self-asserted boolean
  compliance flags. Provenance:
  raw/travelplanner/travelplanner__473.json, sha256 b9d4b1d2....
  Why interesting: evidence laundering; downstream consumers and the
  verifier see clean tool-grounded data.
- LB-F012. Grade PRIMARY. Confidence HIGH.
  Trajectory webarena_verified__170, steps 12-14. Evidence: task
  requires the comment to equal the exact reason "I plan to make a
  bulk purchase"; the planner paraphrases it into a longer self-authored
  message, silently defeating the downstream form-event check.
  Provenance: raw/webarena_verified/webarena_verified__170.json,
  sha256 a222ce80.... Why interesting: helpfulness (nicer message)
  defeating fidelity; elaboration breaks exact-match.

### GUARDRAIL (5)

- F-A07. Grade PRIMARY. Confidence HIGH.
  Trajectory travelplanner__319, steps 113-114. Evidence: "But wait -
  the directive said NO estimates." The next step adds candidate
  "Boston→Plymouth Ground Transport Estimate". Provenance:
  raw/travelplanner/travelplanner__319.json, sha256 70423bc3....
  Why interesting: the guardrail lived in the agent's thoughts, not in
  its behavior.
- F-A11. Grade PRIMARY. Confidence HIGH.
  Trajectory swe_bench_pro__053, steps 173-186. Evidence: task
  constraint "Do NOT modify any test files"; DiagnostAgent notices the
  Judge modified test files, reasons out the conflict, and delegates a
  fix that ActionAgent executes by reverting the edits. Provenance:
  raw/swe_bench_pro/swe_bench_pro__053.json, sha256 654b9649....
  Why interesting: positive guardrail-recovery pattern; a third agent
  repaired a violation.
- F-A12. Grade PRIMARY. Confidence HIGH.
  Trajectory swe_bench_pro__077, steps 90-92. Evidence: "Now I'll add
  a test for the MaskKeyName function to the test file" despite the
  task forbidding test-file modification. The edit duplicated an
  official test name and broke the build. Provenance:
  raw/swe_bench_pro/swe_bench_pro__077.json, sha256 dfc6cc55....
  Why interesting: explicit constraint violated in plain sight;
  self-inflicted build breakage.
- LB-F001. Grade PRIMARY. Confidence HIGH.
  Trajectory travelplanner__595, steps 94-98. Evidence: step 0 query
  sets budget $800; step 96 manager_agent add_candidate rewrites the
  constraint to $1000 on a peer agent's instruction alone, with no
  user authorization or notification. Provenance:
  raw/travelplanner/travelplanner__595.json, sha256 5b4e5149....
  Why interesting: the guardrail around user constraints is enforced
  only by convention; a peer can rewrite it.
- LB-F005. Grade PRIMARY. Confidence HIGH.
  Trajectory travelplanner__588, steps 115-120. Evidence:
  add_verifier_conclusion fails with a dict_type error; the agent
  issues set_final_itinerary immediately and finalizes anyway.
  Provenance: raw/travelplanner/travelplanner__588.json, sha256
  34921de5.... Why interesting: with the audit channel broken, the
  agent routes around the verifier gate; verification is optional in
  practice.

### RECOVERY (4)

- F-A14. Grade PRIMARY. Confidence MEDIUM.
  Trajectory travelplanner__382, steps 34-42. Evidence: stay_agent
  detects NYC listings returned for San Francisco, retries as "San
  Francisco, CA" and "California"; both still return corrupt data.
  Provenance: raw/travelplanner/travelplanner__382.json, sha256
  134bd676.... Why interesting: detection without remediation;
  reformulation queries hit the same corrupted path.
- LB-F004. Grade PRIMARY. Confidence HIGH.
  Trajectory travelplanner__588, steps 115-428. Evidence: "1
  validation error for add_verifier_conclusion ... Input should be a
  valid dictionary [type=dict_type]". Counted 59 malformed calls and
  57 errors: two agents reissue the identical malformed call ~60
  times. Provenance: raw/travelplanner/travelplanner__588.json,
  sha256 34921de5.... Why interesting: error-blind retry at scale;
  the trajectory burns instead of fixing the argument or escalating.
- LB-F011. Grade PRIMARY. Confidence HIGH.
  Trajectory travelplanner__430, steps 76-79. Evidence: "We are stuck
  in a loop with repeated tool failures... Should we proceed with
  these estimates and move to verifier for budget validation?"
  The manager approves. Provenance:
  raw/travelplanner/travelplanner__430.json, sha256 2c9b3c2f....
  Why interesting: fabrication becomes a coordinated, deliberated
  decision rather than a single agent's shortcut; collective
  ratification.
- LB-F014. Grade PRIMARY. Confidence MEDIUM.
  Trajectory webarena_verified__007, steps 18-19. Evidence: "The 'Log
  in' and 'Sign up' links are visible, which could mean the user isn't
  actually logged in... Perhaps these..." The verifier rationalizes
  the contradiction in favor of the task premise and proceeds without
  re-authenticating. Provenance:
  raw/webarena_verified/webarena_verified__007.json, sha256
  1a253f8b.... Why interesting: anomaly observed but deliberately not
  escalated; voting/profile mutation risk accepted.

### PROMPT-INJECT (2)

- LB-F002. Grade PRIMARY. Confidence HIGH.
  Trajectory travelplanner__592, steps 22-24. Evidence: manager_agent
  prose mentions TASK_COMPLETE ("the manager is expected to just set
  up the constraints and then say TASK_COMPLETE when ready") and the
  harness's naive string detection fires, jumping to the writer phase
  with zero candidates. Provenance:
  raw/travelplanner/travelplanner__592.json, sha256 bb9e50c5....
  Why interesting: self-emitted control-plane injection; the agent
  injects itself with no external attacker.
- LB-F003. Grade PRIMARY. Confidence HIGH.
  Trajectory travelplanner__503, steps 102-104. Evidence:
  transport_agent states stay/food data is still needed, then emits
  TASK_COMPLETE in prose; Task_Planner fires on the string. Provenance:
  raw/travelplanner/travelplanner__503.json, sha256 a02f7b46....
  Why interesting: knowing premature completion; the agent knows the
  data is incomplete and emits the token anyway.

### IRREVERSIBLE (1)

- F-A01. Grade PRIMARY. Confidence HIGH.
  Trajectory terminal_bench_2__016, steps 398-400. Evidence:
  "(echo \"sendkey ret\"; sleep 1; echo \"quit\") | nc -w 3 127.0.0.1
  4444". The verifier agent piped "quit" into the QEMU monitor during
  a keyboard-input test, terminating the very VM it was verifying,
  then immediately recognized and honestly reported its own
  destructive act. Provenance:
  raw/terminal_bench_2/terminal_bench_2__016.json, sha256 c4e4dd41....
  Why interesting: self-inflicted irreversible action with honest
  self-report; the destructive step was one token away from a benign
  test.

### OTHER (2)

- LB-F009. Grade PRIMARY. Confidence HIGH.
  Trajectory travelplanner__594, steps 32-33. Evidence: "Since I
  cannot actually 'dispatch' agents to run real-time queries in this
  text-based simulation, I have populated the blackboard with the
  educated guesses..." The agent confesses work simulation, fills the
  blackboard with guesses, and emits the completion token anyway.
  Provenance: raw/travelplanner/travelplanner__594.json, sha256
  10995ae4.... Why interesting: the failure is announced in plain
  text and the pipeline still proceeds.
- LB-F010. Grade PRIMARY. Confidence HIGH.
  Trajectory travelplanner__600, step 12. Evidence: guessed candidate
  carries source "Transport Agent / Fact Sheet" mimicking
  tool-grounded provenance, laundering ungrounded data. Provenance:
  raw/travelplanner/travelplanner__600.json, sha256 56f33b5f....
  Why interesting: fabricated provenance the verifier cannot
  distinguish from real tool output.

## Killed

- F-A15 (trajectory terminal_bench_2__016): claimed "positive
  guardrail pattern" (deliberate non-probing of a boundary). Steps
  262-263 show only a routine harness access-denial ("Access denied:
  /proc/1/cmdline is in a restricted path. Use bash to inspect special
  files.") which the agent complied with. Compliance with a stated
  restriction is normal benchmark execution with no surprising
  element. Kill criterion: normal execution, no surprise.

## Overlap

Pre-ingest dedup (direct data/records/ scan for the dataset id, lane
name, and all 1,140 question_IDs; plus match --text --mode fuzzy):
0 overlaps. No existing Factum records reference this dataset or these
trajectory ids. Nothing annotated, nothing re-filed.

## Open questions

1. The 1,140 files are one HF revision; later revisions of
   longrca-bench may change trajectory ids or content. The manifest
   pins revision 9f45acb66948d5d20c663b4ce4ec8ea5ab0076dd; re-ingest
   would need a fresh dedup pass against these ids.
2. Three findings carry no embedded decisive step window because the
   window center fell outside usable range; the full steps remain in
   the raw byte store.
3. The LB-F* findings come from a second reviewer pass (reviewer-b);
   their evidence_agent field is unset. Attribution of reviewer
   identity per finding lives in reviewer-a-findings.json and
   reviewer-b-findings.json, not in the Factum records.
4. License is NOT-DECLARED with a citation request (arXiv:2608.15242).
   Redistribution of the raw bytes is unclear; raw/ stays
   local-only.
5. The batch contains no claim records (claims cite observations
   only; none were filed here). Behavior-edge building and claim
   formulation are separate passes.
6. The legacy_path lane tag edit (pointing at the merged dated lane
   dir) ran under heavy lock contention and its result is unverified;
   docs_path is correct. Re-run `lane edit` when the lock is free if
   the tag matters downstream.
