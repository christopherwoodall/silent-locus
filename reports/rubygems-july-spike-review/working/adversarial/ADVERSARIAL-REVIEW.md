# Adversarial review: rubygems-july-2026-spike-operator-20261027.csv

Scope: the CSV only. No live fetch was done. No Factum write was done.
The CSV was not modified (sha256 re-verified after analysis:
765ee2f24e6ec1a191c66faee030aaea8586cc4a0cdde1bee4c0668a0f0f3ce0).
Grades: OBSERVED = recomputed from CSV columns. INFERENCE = reasoned
from those columns, unproven. UPSTREAM = dashboard/Haiku claim only,
never upgraded on dashboard prose alone.

## Method verdict: NOT trustworthy as a severity or agent scoring system

The file is usable as a shape-sorted inventory. It is not usable as
evidence of severity, agent activity, or impact. Three facts kill the
scoring story before any single row is debated:

1. Dashboard level is exactly a rule count, not a risk judgement.
2. Haiku level has no score behind it on 464 of 484 scored rows, and
   its v1 calibration is wildly inflated versus v2.
3. Agent activity is a label applied to probe-shaped rows. The file
   holds no agent-specific evidence at all: no model, no harness, no
   tool calls, no prompts, no gem code, no downloads, no victims,
   no callback receipts, no MFA column, no publisher column.

## 1. Consistency, recomputed

Base counts (OBSERVED): 533 rows, 0 duplicate names, all withdrawn=True.
Authors: Andrey78 129, Prvaz12_mars 113, tester 100, monib110 68,
plus 42 smaller authors. Dates: July 6: 132, July 7: 204, July 8: 8,
July 9: 4, July 10: 2, July 12: 70, July 13: 113. July 11: 0 rows.
Dashboard levels: medium 193, critical 151, low 121, high 19,
empty 49. Haiku levels: high 385, critical 80, medium 15, low 4,
empty 49. Haiku categories: mass_generated 305, registry_test_or_probe
178, unclear 1, empty 49. Agent activity: possible 461, likely 18,
no_sign 5, empty 49. Prompts: pkg-review-1 464, pkg-review-2 20,
empty 49.

### Dashboard level = rule count (OBSERVED, deterministic)

- low: 121/121 rows carry exactly 1 rule.
- medium: 193/193 carry exactly 2 rules.
- high: 19/19 carry exactly 3 rules.
- critical: 151/151 carry 4-8 rules (mean 5.68).
- The same dashboard_rules string never yields two dashboard levels.

So a row is "critical" if four tokens fired, whatever the tokens are.
Example: ownership-test-1783401924 is dashboard critical (numbered
name + placeholder text + short author + test name) while Haiku
rates it low. Rule count is not severity, and quoting a dashboard
level as risk is an overclaim.

### Dashboard vs Haiku agree on only 88 of 484 scored rows (18.2%, OBSERVED)

- Dashboard low (121) -> Haiku high on 111, medium 9, low 1.
- Dashboard medium (193) -> Haiku high on 188, medium 4, low 1.
- Dashboard critical (151) -> Haiku critical 73, high 76, medium 1, low 1.
- Dashboard high (19) -> Haiku critical 7, high 10, medium 1, low 1.

The two systems do not corroborate each other. Haiku upgrades
almost every dashboard low/medium row to high. Either system quoted
alone hides this disagreement.

### Haiku score exists only on the 20 v2 rows (OBSERVED)

- haiku_score is blank on all 464 pkg-review-1 rows and all 49 empty rows.
- v2 scores only: medium 42-45 (n=10), high 62-72 (n=4),
  critical 88-92 (n=6). No score value appears under two levels and
  there are 0 adjacent score-order inversions within n=20.
- But the bands have empty gaps (46-61, 73-87 hold zero rows), so no
  threshold can be tested from this file. "Monotonic" here means
  "20 sorted points do not contradict themselves", not "calibrated".
- Any claim of the form "score X means level Y" for a v1 row is
  unsupported: v1 rows have levels with no scores behind them.

### pkg-review-2 changes calibration, not just scores (OBSERVED)

- v1 levels: high 381/464 (82.1%), critical 74 (16.0%),
  medium 5 (1.1%), low 4 (0.9%).
- v2 levels: medium 10/20 (50%), critical 6 (30%), high 4 (20%), low 0.
- v2 categories are evenly split (mass_generated 10,
  registry_test_or_probe 10); v1 is mass_generated 295,
  registry_test_or_probe 168, unclear 1.
- On matched shapes v2 is inconsistent, not a clean downgrade:
  combinatorial-only rows are Haiku high on 111 v1 rows but medium
  on all 5 v2 rows in the same rule group; combinatorial+shared rows
  are high on 178 v1 rows but medium on 4 of 5 v2 rows, while
  mega-quick-mod (monib110, same rule string, v2) stays high at 62.
  So v2 cannot be treated as superseding v1 until all 464 v1 rows
  are re-run. A v1 "high" and a v2 "medium" on the same shape are
  both in this file, and neither wins on file evidence alone.

### Identical shapes, different Haiku levels (OBSERVED)

- 6 of 23 multi-row author+version+deps+summary groups split
  Haiku level, and the split survives the stricter test of also
  matching homepage/source presence.
- Cleanest within-v1 cases (same author tester, version 0.0.1,
  0 deps, summary "Test", same link presence, v1 only):
  apex-black-ipv6-001 critical vs apex-black-ipv6-002 high;
  apex-black-race-000/002/003/004 critical vs apex-black-race-001 high;
  apex-black-probe-000/002/003 critical vs apex-black-probe-001 high.
  The only visible difference is name tokens. Level here is
  LLM noise, not a rule.
- Category flips too: apex-black-fuzz-006r and apex-black-fuzz-007r
  are labelled mass_generated while sibling "Test"-summary tester
  rows are registry_test_or_probe.
- 377 of 484 scored rows sit in a dashboard_rules string group
  whose Haiku level is not unique (largest: combinatorial-only,
  119 rows split high 111 / medium 8; combinatorial+shared, 183
  rows split high 179 / medium 4). The rule string does not
  determine the Haiku level, and the file records no other
  scoring input that explains the split.

### The 49 empty rows are a coverage hole, not a clean subset (OBSERVED)

All eight scoring columns are empty on exactly the same 49 rows.
They include apparently ordinary gems (rosett-ai, edoxen,
sportdb-parser, the shirobai family, metz-scan, jira-api
variants, ecoportal rows) AND apex probe names AND 6 monib110
combinatorial rows. July 8, 9, and 10 have zero scored rows.
The file gives no reason for emptiness. Any rate computed over
scored rows only (for example "possible on 461 of 484") silently
excludes this mixed set. Empty must never be read as safe,
irrelevant, or unreviewed-by-design.

### Reason prose asserts columns that do not exist (OBSERVED)

The CSV header has no MFA, publisher-handle, code, download,
victim, or callback-receipt column. Yet 355 Haiku reasons assert
"no MFA", "MFA off", "no publisher", or "null publisher".
Those assertions are UPSTREAM and unverifiable from this file.
The same applies to "source link points to a matching repo":
source_code_uri presence can be checked (327/533 rows have it
empty; Andrey78 78/129 present, Prvaz12_mars 67/113, monib110
46/68, tester 1/100), but repo existence, content, and
liveness cannot be checked from this file.

### Batch-size claims in reasons do not share a denominator (OBSERVED)

Dominant claims match file totals (Andrey78 "129-package" x116
claims vs 129 rows; Prvaz12_mars "113-package" x110 vs 113 rows;
SR "13-package" x11 vs 13 rows). But tester claims split
"101-package" (x40) vs "100-package" (x5) against 100 rows for
author tester alone; monib110 claims "60-package" (x54) against
68 rows in the file (62 scored + 6 empty) and one claim says 64;
"t"/"T" claims of "28-package" merge two declared authors
(t 20 + T 8). "Batch of N" in a reason is therefore not a
reproducible count until the grouping rule is stated.

## 2. False-positive shapes: every rule also fires on benign work

Each rule below is a shape token from dashboard_rules. The benign
reading is not exotic; it is the literal reading of the row's own
name and summary.

- Group: combinatorial names (372 rows). Word-list names such as
  mini-sharp-hub, ultra-fast-box, mega-max-tool. Benign fit:
  coursework, scaffold generation, or a naming exercise. The
  summaries themselves say "University research based on X".
- Group: shared text (185 rows). One summary template across a
  batch, e.g. nano-sharp-hub ("University research based on
  rack"). Benign fit: a course template or generator default.
- Group: name series (66 rows). apex-black-test-001, -011, -012.
  Benign fit: numbered test iterations.
- Group: owner burst (158 rows). Many rows, one author, one day.
  Benign fit: a class deadline, a CI run, a bulk test push.
  Andrey78 published 129 rows on July 6 alone (00:27-17:07);
  Prvaz12_mars 113 on July 13 (17:58-19:35); monib110 68 on
  July 12 (10:25-11:25); tester 100 on July 7 (03:12-07:28).
  Burst timing proves bulk publishing, nothing about intent.
- Group: template batch (100 rows). apex-black-test-017/020/021/023,
  summary "Test". Benign fit: a test harness emitting identical
  stubs.
- Package: numbered name (115 rows). apex-black-test-001,
  chainproof-1783394106 (epoch suffix). Benign fit: iteration
  numbering and timestamped test runs.
- Package: placeholder author (122 rows). Author literally
  "tester". Benign fit: a test account doing what its name says.
- Package: placeholder text (92 rows). Summary "Test" or "T".
  Benign fit: a minimal test gem, which needs no real summary.
- Package: probe name / test name (59 / 41 rows). apex-oidc-probe,
  ssrf-port3000-7b3bf122, apex-black-test-001. Benign fit:
  self-declared QA and security testing. A name that says "test"
  is evidence of testing, not of malice.
- Package: oob url (48 rows). Homepage is an out-of-band callback,
  loopback, metadata, or bare-IP address (kinds only; full
  callback addresses are deliberately not reproduced here).
  Benign fit: the same callback mechanism used to verify link
  handling in QA. The file holds the homepage string only. It
  holds no callback receipt, so it cannot distinguish a QA
  callback check from an exfiltration, and cannot show that
  any callback ever arrived.
- Package: short author (43 rows). Authors "t", "T", "SR".
  Benign fit: any short handle. Handle length carries no intent.
- Package: markup (12 rows). Markup/XSS-style strings in summary
  or author fields. Benign fit: XSS test inputs. The file shows
  the input string only. It shows no rendering, execution, or
  victim, so "stored XSS" or "XSS success" is not supported.
- Package: placeholder link (8 rows). Homepage is a loopback,
  example, or generic registry address. Benign fit: scaffold
  defaults left in place.

Consequence: dashboard criticality built from these tokens
inherits all of these false positives. Four benign tokens still
score critical, because critical only means "four tokens fired".

## 3. Agent-activity audit: "possible" 461, "likely" 18, "no_sign" 5

### What, if anything, distinguishes agent activity in this file?

Nothing agent-specific. No reason in the file mentions a model,
a harness, a tool-call sequence, a prompt, or generated code
(checked by word scan of haiku_reason; the only agent-adjacent
words are the labels themselves: "agent-style", "agent-like",
"agent use", "automation"). What the reasons actually cite is:
batch membership, numbered/template names, placeholder author
and summary, and probe wording in the name or summary. Every one
of those also fits a human running a script, a QA engineer, or
a student batch job. Scripted testing is not agent activity,
and the file gives no discriminator between them.

Distribution alone betrays the label (OBSERVED): all 18 "likely"
rows are July 7, all 18 are category registry_test_or_probe,
none comes from the three mass-generated batches (Andrey78,
Prvaz12_mars, monib110). "Likely" tracks membership in the
July-7 probe cluster, not an agent marker. And the boundary is
arbitrary at the edges: 5 "no_sign" rows (apex-oidc-probe,
attacker-hunt-xss, xxstest-1783395545, test-xss-meta,
attacker-xss-admin-1) are the same probe shape as "likely" rows
but got no_sign, including a row Haiku rates low and rows it
rates high. If the same shape yields likely, possible, and
no_sign, the activity column is not measuring a stable property.

### The 18 "likely" rows, tested one by one

Full sanitized table (homepage kinds only, no callback addresses):
likely-audit-table.txt. Summary of the test:

- 16 of 18 are pkg-review-1 (no score); 2 are pkg-review-2
  (ssrf-port3000-7b3bf122, high/72; apex-black-regexp-001,
  critical/88). The "likely" label therefore mostly carries no
  score at all.
- 10 of 18 reasons contain no agent/automation word whatsoever.
  They argue from batch + probe wording only.
- 3 of 18 reasons explicitly hedge ("agent use is plausible but
  not certain" or equivalent): apex_webhook_capture,
  apex_inject2_test, ssrf-redirect-test-1783406163. A hedged
  "likely" is not a finding; it is the reviewer declining to
  commit, while the column records a commit.
- 7 of 18 have an empty homepage AND an empty source link
  (the 100-character "a...a" name, webhook-fire-1783405247,
  internal-scan-1783405777, internal-svc-1783405972,
  webhook-capture-1783406220, seed-gem,
  apex-black-regexp-001).
  For these, "likely" rests on name/summary wording and sibling
  batch membership alone. internal-scan-1783405777 and
  internal-svc-1783405972 do not even have a homepage to probe
  with; their summaries name loopback/internal targets, which
  is a statement of test intent, not an agent fingerprint.
- The strongest-looking rows still fail the agent test:
  apex_link_tracker (webhook callback homepage, SSRF summary)
  proves a probe was published, not that an agent published it.
  apex-black-test-001 (cloud-metadata homepage and source
  fields) has a reason claiming links to "localhost admin and
  cloud metadata endpoints", but the file's homepage/source
  columns show a metadata address, not a localhost-admin
  address: the reason embellishes beyond the columns.
  ssrf-port3000-7b3bf122 (v2, likely, high/72) has a generic
  registry homepage kind and summary "testing"; its v1 twin
  ssrf-port9200-f12bbeb3 is also "likely" with the same shape,
  while sibling ssrf-* rows with identical author/version/
  deps/summary are merely "possible". Nothing in the columns
  separates the likely twins from the possible siblings.
- The two single-letter-summary rows (the 100-character
  "a...a" name, author T, summary "T"; and seed-gem, author T,
  summary "T") are labelled likely on burst membership plus
  "automation" wording or nothing at all. A one-letter summary
  is the weakest possible evidence for any actor claim.

Verdict on the activity column: "possible" is the default label
(461/484 scored rows, 95.2%), "likely" is an unreproducible
upgrade on 18 probe rows, and neither label survives as agent
attribution. Downgrade all 18 to UPSTREAM probe-batch labels.
Agent activity on this file is UNPROVEN, not "possible" in any
evidential sense.

## 4. Kill list (claims that do NOT survive)

K1. Dashboard critical/high means high risk. KILLED by the
rule-count determinism above (OBSERVED). Critical = 4+ tokens.
K2. Haiku high on 385 rows means 385 high-risk packages. KILLED
by v1 inflation (82.1% high), the v2 recalibration on identical
shapes, and within-shape level flips (OBSERVED).
K3. Haiku score is a calibrated risk scale. KILLED as a general
claim: scores exist only on n=20, with untestable gaps between
bands (OBSERVED). Survives only as "within these 20 rows, higher
score sits in a higher band".
K4. pkg-review-2 supersedes pkg-review-1. KILLED: v2 covers 20
rows, changes levels inconsistently on matched shapes, and the
other 464 rows were never re-run (OBSERVED).
K5. Agent activity "possible" (461) or "likely" (18) evidences
agent involvement. KILLED: no agent-specific evidence exists
in the file; the label tracks probe-batch membership and is
hedged or wordless on most "likely" rows (OBSERVED + INFERENCE).
K6. MFA-off / no-publisher-handle findings. KILLED as file
claims: no such columns exist, so none of the 355 assertions
can be checked from this file (OBSERVED). They remain UPSTREAM.
K7. Reason batch sizes are exact counts. PARTLY KILLED:
Andrey78/Prvaz12_mars/SR match file totals, but tester (100 vs
101) and monib110 (60/64 vs 68) do not, and denominators are
unstated (OBSERVED).
K8. Withdrawn means malicious, or means risk is gone. KILLED
both ways: withdrawn=True on all 533 rows including ordinary
gems in the empty set; withdrawal is this export's selection
filter, not a per-row verdict (OBSERVED).
K9. Empty rows are safe or irrelevant. KILLED: the 49 unscored
rows mix ordinary gems, apex probes, and monib110 batch rows,
and July 8-10 have no scored rows at all (OBSERVED).
K10. Out-of-band homepage or metadata/loopback homepage proves
SSRF success, callback receipt, or exfiltration. KILLED: the
file holds the homepage string only, no receipt or execution
evidence (OBSERVED).
K11. Markup in a summary or author field proves XSS execution.
KILLED: the file holds the input string only, no rendering or
victim (OBSERVED).
K12. Mass-generated means agent-generated. KILLED: no generator,
code, or prompt evidence in the file; the summaries
self-describe as university research, which fits human
scripting or coursework equally (OBSERVED + INFERENCE).
K13. The July spike is one campaign or one actor. KILLED from
this file alone: four separate author-date clusters with
different name grammars and summaries, and no shared code,
dependency, or link column connecting them (OBSERVED).
Co-occurrence in one export is not linkage. (Other lanes may
link them; this file does not.)
K14. Placeholder/short author, numbered name, test/probe name,
or burst timing proves malicious intent. KILLED: each is the
literal shape of ordinary testing, QA, and coursework (Section 2).

## 5. Survive list (claims that DO survive, with grades)

S1. Four bulk-publishing clusters exist with the stated counts
and single-day spans (Andrey78 129 on July 6; tester 100 on
July 7; monib110 68 on July 12; Prvaz12_mars 113 on July 13).
Grade: OBSERVED (first/last_published_utc + authors_declared).
S2. The three large batches share a combinatorial adjective-noun
name grammar and a "University research based on X" summary
template; the July-7 tester-family rows share SSRF/probe/test
wording in names and summaries. Grade: OBSERVED (name + summary
columns). This is a shape finding, not an actor finding.
S3. 509/533 rows have 0 runtime dependencies and 452/533 are
version 0.0.1. Grade: OBSERVED (columns are counts/versions
only; dependency identities are not in the file).
S4. All 533 rows in this export are withdrawn. Grade: OBSERVED,
with the scope caveat that this describes the export, not the
live registry and not each row's reason for withdrawal.
S5. July-7 tester-family rows are self-described registry
probes: their names/summaries say SSRF, test, or probe, and
their homepage kinds include loopback, cloud-metadata,
callback, and bare-IP addresses. Grade: OBSERVED as
self-description; INFERENCE (strong) that probing was the
intent; UNPROVEN that any probe succeeded or that any agent
ran it.
S6. Dashboard rule tokens were assigned as recorded in
dashboard_rules (token counts in Section 2). Grade: OBSERVED
that the tokens are present; the tokens' meaning beyond their
names is UPSTREAM.
S7. Haiku categories broadly sort by shape (combinatorial
batches -> mass_generated; July-7 probes ->
registry_test_or_probe). Grade: UPSTREAM labels with
OBSERVED distributional support, weakened by the flips in
Section 1 (fuzz rows, no_sign probes). Usable as a sorting
hint, not a classification.
S8. Haiku v2 scores are ordered within their 20 rows (medium
42-45 < high 62-72 < critical 88-92). Grade: OBSERVED for
those 20 rows only. No wider threshold claim survives.

Nothing in the file survives as agent attribution, severity
grading, or impact. Those three claim classes are all UPSTREAM
at best and contradicted at worst.

## 6. Verdict-change test (default: no change)

July-7 verdict (24 rows in v2): NO CHANGE forced. This file's
July-7 set is 204 rows, of which only 10 are pkg-review-2, and
it adds no new observation type: no gem code, no live registry
state, no callback receipts, no actor evidence. Its July-7
"likely" rows are hedged or wordless probe labels (Section 3).
A wider candidate pool is a scoping question for the parent
lane, not a verdict change. Note: the standing verdict itself
was not re-read here (v1/v2 export files untouched per
constraints), so the parent must confirm the mapping; nothing
in this file forces a change either way.

GemStuffer / JFrog picture: NO CHANGE. The strings GemStuffer,
JFrog, stuffer, typosquat, and backdoor occur zero times across
summary + haiku_reason + dashboard_rules. "Malicious" occurs
once in reason text. Lookalike/deception language in the v2
rows inspected appears as negation ("no lookalike", "no clear
deception"), and no row claims a lookalike target, a
dependency-confusion victim, or a malicious payload. This file
neither supports nor disturbs that picture; it is silent on it.

Andrey78 batch verdict: NO CHANGE. The file corroborates the
batch shape already implied by its own columns (129 rows,
July 6, combinatorial names, university-research summaries,
0 deps, 0.0.1) but its severity labels conflict with each
other on that very batch (dashboard low, Haiku high on v1,
Haiku medium on the 6 sampled v2 rows), and it adds no agent
evidence. The batch survives as mass-generated shape (S2),
not as an agent finding and not at any higher severity.

## 7. Credential-shaped values and sensitive strings

A regex scan flagged 7 field-level credential-shaped hits across
summary and haiku_reason. Presence and count only are reported
here, per instructions; no values are copied, and none is
confirmed as a credential from this file alone (several look
like ordinary words or probe strings that trip a broad pattern).
Separately, the file contains callback addresses and markup
payload strings in homepage/author/summary fields. None are
reproduced in this report or in the sanitized tables; homepage
values are reported by kind only (loopback, cloud-metadata,
callback, bare-IP, registry, example, empty).

## 8. What would actually upgrade these claims

- Re-run all 484 scored rows under pkg-review-2 (or one stated
  prompt) and publish the scoring rubric and thresholds.
- Replace dashboard level with a severity-weighted rule, or drop
  the level and report the tokens.
- Score the 49 empty rows or state why they were excluded.
- Add the missing columns the reasons already assert: MFA,
  publisher handle, gem code hash, callback receipts, and
  execution outcomes. Until then, agent, severity, and impact
  claims from this file stay UPSTREAM.

## Outputs and reproducibility

- This report: reports/rubygems-july-spike-review/working/
  adversarial/ADVERSARIAL-REVIEW.md
- Recomputation scripts (read-only on the CSV):
  analyze.py, analyze2.py, analyze3.py, sanitize.py
- Sanitized tables: likely-audit-table.txt, v2-table.txt,
  burst-spans.txt, combinatorial-split.txt,
  rule-level-consistency.txt, verdict-terms.txt
- All under reports/rubygems-july-spike-review/working/
  adversarial/ (relative to ~/workspace/silent-locus).
- No git add/commit/push. No Factum writes. No changes to the
  agent-egress-deep-dive lane, the staged-tree branch, or any
  v1/v2 export file. CSV sha256 unchanged after analysis.
