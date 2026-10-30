# Adversarial review — AIID full-site drafts

Role: adversarial reviewer. Job: try to kill the claims in the drafts.
No Factum record was written. No commit was made. No push was made.
No network use. No login. No session. No Shodan use.

Terms used here, defined on first use:

- AIID: Artificial Intelligence Incident Database. A curated public
  database of AI incidents.
- Factum: the local structured evidence store. Records live in
  `data/records/`.
- Batch: one exported set of Factum records, with a manifest file.
- IOC: indicator of compromise. A value that can point to an incident.
  Examples: an IP address, a domain, a file hash.
- TTP: tactics, techniques, and procedures. A short slug names a known
  technique.
- Slug: a short code name for a TTP.
- Grade SECONDARY: content from a curated database, not first-hand
  observation.
- Basis UPSTREAM: a claim that rests on an upstream source, not on
  direct observation.
- Ranked set: the 587 IOC entries flagged as agent-relevant.
- Full set: all 10,594 distinct IOC entries.

## Verdict: SHIP-WITH-FIXES

Ship the drafts only with the fixes in this file, and only after the
coordinator records a decision on the one open batch issue below.
The core counts, the grades, the dedup result, and the scanner fixes
survive attack. The kills are small count errors, one bad batch
citation, one overstated name claim, and one thin budget claim.
Draft fixes for those kills are applied and logged below.

Condition: the coordinator must record, before commit or push, an
accept-or-scrub decision for the two behavior-text name residues
in the incident batch (see open fix O1). The draft disclosure added
to INGEST-REPORT.md does not change the batch bytes. If the
coordinator requires a name-free batch, this verdict becomes
NO-SHIP until re-extraction and re-ingest.

## Kill list

Each claim attacked. Verdict: KILLED, SURVIVES, or WEAKENED.
Evidence is given for each verdict.

### 1. 53 TTP records plus 1 behavior record

Verdict: SURVIVES on the total. KILLED on the distinct-slug count.

Evidence: extraction has 53 TTP entries across 42 incidents. The
batch has 53 `intel.ttp` records and 1 `intel.behavior` record.
The behavior record is incident 1395, slug
`proxy-network-fraudulent-accounts`. That same slug and incident
also appear as one of the 53 TTP entries. This is not a double
count of a TTP entry. It is two record types for one slug
assignment: the behavior record carries the verbatim text, and
the TTP record carries only the slug-to-incident link. Total
behaviors re-derived from extraction: 2,864 (1,524 plus 1,340).
Slugged behaviors: 1. None-established behaviors: 2,863.
Distinct TTP slugs re-derived: 18, not 19. The E2 summary lists
18 slugs and its values sum to 53. INGEST-REPORT.md said 19.
Fix F1 below corrects it.

### 2. Names in records

Verdict: KILLED as a blanket claim. SURVIVES in its narrow form.

Narrow form, which survives: no submitter name, no editor name,
and no author name was added by any executor. Source titles in
the batch match extraction titles exactly (1,775 of 1,775, zero
mismatches). Observation summaries match extraction behavior
texts exactly (zero mismatches). Word hits for "submitter" and
"editor" in the batches are generic words in incident text, not
added names.

Blanket form, which is killed: the claim that only verbatim
incident-title words appear as names is false for behavior
texts. Two behavior texts retain subject names that are not
title words. Incident 901 retains a first name of a harmed
party. Incident 1512 retains a full name of an academic subject.
This review does not reproduce those names. The reason for
omission is the no-names rule for this review itself. The E1
summary warns that its mechanical scrub can miss uncommon
names. The E2 summary did not use the same `[person]` scrub:
E1 has 548 behaviors with `[person]`; E2 has zero. Titles
verbatim do retain their own title words, including words that
name public figures. That part is faithful copying, not added
data, but it must not be described as name-free.

### 3. Snapshot time rendered with Z

Verdict: WEAKENED. Disclosure is present. Precision is overstated.

Evidence: INGEST-REPORT.md states the rendering
`2026-10-26T10:15:00Z` for every IOC observation, states the
source stamp carries no timezone, and states the `Z` exists
only to satisfy the date-time format. That disclosure is real.
It does not cure the overstatement. `Z` asserts UTC, which the
source never stated. The `:00` seconds are padding: the stamp
gives hour and minute only. All 10,594 IOC observations carry
this one value. Fix F4 below adds that warning to the report.
Treat the value as a snapshot label, not a precise UTC instant.

### 4. Config diff confined to 4 hunks

Verdict: SURVIVES on confinement. KILLED on the brief's insertion
count. No file fix was needed for this item.

Evidence: parsed comparison of HEAD against the working file
shows only 2 top-level keys changed (`iocfeeds`, `prcomment`),
and only 4 fields inside them changed (iocfeeds note, OTX list,
prcomment note, prcomment queries). Old OTX list (23) is an exact
prefix of the new list (52). Old queries (10) are an exact prefix
of the new list (11). No `aiid` block was added. Git numstat is
149 insertions and 3 deletions, which is 152 changed lines in
total. The brief phrase "152 insertions / 3 deletions" is wrong.
TOOL-UPDATES.md itself never states 152 insertions, so no edit
to that file was made for this item. Round-trip check: a load
then dump with indent 1 and ASCII escapes reproduces the HEAD
file byte for byte.

### 5. Wordlist

Verdict: SURVIVES in full.

Evidence: wordlist.json parses. Entries: 3,895 before, 3,991
after, gain 96. Duplicate terms: 0. Old entries are an exact
prefix, object for object, of the new file. New active terms:
64. New noisy terms: 32. Wordlist.txt non-comment lines:
3,903 before, 3,967 after, gain 64. The 64 txt adds equal the
64 JSON active adds, in order. All 32 noisy terms are absent
from txt. The pre-existing txt-vs-JSON gap is untouched: 11
lines before (3,903 vs 3,892 active) and 11 lines after
(3,967 vs 3,956 active). Pre-existing terms claimed as already
present were confirmed present before this change: Cursor,
DeepSeek, Cowork.

### 6. Prcomment budget: 11 queries, 55 planned calls, 60 per hour

Verdict: WEAKENED. Safe for this scanner alone. Not safe as a
shared-bucket claim.

Evidence: dry run reproduced: 11 queries, 35 patterns unchanged,
planned calls 55, quota status "budget ok: remaining=59,
need=55". Headroom is only 4 calls. The "remaining=59" value
is a recorded quota from a state file, not a live check at run
time. Any other consumer of the shared unauthenticated bucket
in the same hour can eat that headroom, and one more query
would take the plan to exactly 60. The module fails closed
when the recorded budget cannot cover the plan, so the risk is
a skipped run and starved co-consumers, not a silent overrun.
TOOL-UPDATES.md already warns that no further query should be
added without a budget review. That warning must stay, and the
coordinator must not read "55 inside 60" as a guarantee for
shared use.

### 7. IOC dedup: 0 skips, 3 near-hits

Verdict: SURVIVES for the 3 near-hits. KILLED for one cited
batch id. Fixed below.

Evidence: spot checks in `data/records/` outside the two AIID
batches confirm all 3 near-hits exist with non-AIID provenance:
a domain record for the first near-hit and a domain record
for the second near-hit sit in batch
`307d9654e63b49368288b4bd3eb6697c`, lane
`2026-10-11-hf-traj-hermes`, with HF-traces aggregation
provenance; a model record for the third near-hit sits in the
OpenAI blog lane with system-card provenance. Under the brief's
rule (same term plus same AIID provenance means a skip), all
3 are new AIID sightings, not dupes. The 1 same-term non-IOC
record cited for a tool name was also confirmed: a behavior
record in batch `756a273f21064593a4bc4ece94f647bf`, lane
`incident-7050-antigravity`, with incident 1424 provenance.
That is not an IOC sighting. The cited batch id for the third
near-hit was wrong: INGEST-REPORT.md gave a 33-character id
that matches no directory. The true directory id ends in a
different digit and is one character shorter. Fix F2 below
corrects it. The underlying record exists, so the dedup result
stands; only the citation was bad.

### 8. Corpus arithmetic

Verdict: SURVIVES.

Evidence: incident batch file has 5,379 lines. IOC batch file
has 10,595 lines. Manifest counts match both files. Manifest
SHA-256 values recomputed locally match both manifests
(incident batch and IOC batch). Arithmetic holds: 208,745
plus 5,379 equals 214,124; 214,124 plus 10,595 equals 224,719.
Incident batch breakdown re-derived: 1,775 sources, 1,829
observations (1,775 reports, 53 TTP, 1 behavior), 1,775 claims.
IOC batch breakdown re-derived: 1 source, 10,594 observations
(url 7,955; domain 2,147; hash 326; file_path 68; ip 56;
model 23; model_or_tool 14; tool 5). No other batch is needed
to explain the deltas, and no record for incidents 1152 or
1433 appears in either batch (zero cite strings for both).

### 9. Grade inflation

Verdict: SURVIVES.

Evidence: every record in both batches carries grade
SECONDARY (5,379 of 5,379; 10,595 of 10,595). No record carries
OBSERVED. Every incident claim carries basis UPSTREAM. IOC
status mapping preserves confidence: high 6 maps to active,
medium 8,247 maps to active, low 2,341 maps to candidate, and
the exact confidence stays in tags. All 326 hash records are
low plus candidate, matching the caveat that hash strings are
unverified text copies. All 5 network-address IPs are low
plus candidate. Press domains stay at medium with an explicit
caveat that they are source links, not threat infrastructure;
that is not an upgrade to a threat claim. Ranked flags
re-derived: 587 records flagged true, 10,007 false. Ranked
entries number 587; distinct ranked values number 577, because
10 values appear under 2 kinds. That matches the report.

### 10. Signed values and query strings

Verdict: SURVIVES with 2 narrow exceptions. Fixed in the
reports below. The batch was not changed, under the
never-redact rule.

Evidence: all 74 distinct URLs with a query string use the
`?params=name1,name2` form, and no other `?` form appears in
the batch. No token and no signed value was found. The one
`=` inside a URL path segment is an Amazon ref segment
(`ref=sr_1_1` form), not a query value and not a credential.
One further exception was found: a `?params=` entry for
incident 1162 carries a path-like value, not a parameter
name. That is a parameter-name extraction flaw, not a leaked
value, but the report claim "parameter names only" was
overstated without it. Fixes F3 and F5 below record both
exceptions. Full-set vs batch-set comparison is exact:
10,594 of 10,594 kind-plus-value pairs match, with zero
pairs in either direction unmatched. Provenance incident-id
lists were checked for all 10,594 batch observations against
iocs.json: zero mismatches.

### 11. Scanner F1 and F2 fixes, disabled gate

Verdict: SURVIVES. Both fixes were reproduced independently.

Evidence: `scripts/scanners/aiid.py` now holds
`STATE_VERSION = 2`, a `_snapshot_kind` helper, a
`_entry_key` helper that builds `date|kind` keys, and a
`_split_entry_key` inverse. A synthetic listing with a
tarball and an Excel file for 2026-10-26 now parses to 2
entries, not 1, and a tarball-only URL change yields exactly
`changed = ['2026-10-26|tarball']`. Both degraded branches
in `scan()` are guarded by `if not silent:`, and a
monkeypatched degraded run on a fresh baseline wrote no
state file. Compile passes. Dry run returns zero hits.
A live run refuses with the disabled message, and no
`scripts/scanners/state/aiid*` file exists after either run.
The config file still has no `aiid` block. Current module
size is 29,346 bytes, matching the fix note, not the
pre-fix verification report (25,670 bytes). That difference
is expected: the verification report predates the fix.

### 12. Own attacks beyond the brief

- iocs.json incidents-with-IOCs: KILLED, fixed. The field
  said 1,775. Union of incident ids across the full set is
  1,774. Incident 88 has no IOCs, and extraction confirms
  888 plus 886 incidents with IOCs, which sums to 1,774.
  IOC-REPORT.md itself states 1,775 extraction files and
  1 incident with no IOCs, which implies 1,774, so the
  field contradicted its own report.
- IOC-REPORT.md query count: KILLED, fixed. The report said
  "84 URLs with a query string". Extraction has 84 URL
  mentions with a query string, but only 74 distinct URLs
  after dedup. The report wording read as 74 vs 84 distinct
  URLs. Fixed to state both numbers.
- HUNT-INDEX.json: SURVIVES. Entries: 1,777. Hunt-relevant:
  122. Novelty counts in the index match the novelty file:
  NEW 1,767, OVERLAP 2, PARTIAL 8. The 235 hunt-relevant
  titles in the novelty file use a wider title-only rule;
  the 122 use the narrower index rule. The reports state
  this difference. It is not an error.
- Novelty method: SURVIVES with stated limits. The novelty
  summary already discloses the limits: no full per-record
  Factum sweep, partial case-insensitive lane coverage,
  binary files skipped, title-change risk. NEW means no hit
  in the checked stores, not proof of absence everywhere.
- Extraction summaries: SURVIVES. E1: 889 files, 1,524
  behaviors, 13,896 IOC mentions, 0 TTP. E2: 886 files,
  1,340 behaviors, 7,474 IOC mentions, 53 TTP mappings.
  Mentions sum to 21,370. Dedup table by kind matches
  extraction kinds exactly.
- TOOL-UPDATES.md git-status line: WEAKENED as current
  state. Section 6 says git status showed exactly 3
  modified files after that work. The current tree holds
  many other modified and staged files from other lanes.
  That line may have been true at write time, but the
  coordinator must re-check status at commit time and
  must not take it as current.
- Scanner robustness F4: OPEN, not a blocker for holding
  the module disabled. Same-line date fallback, capped-page
  state overwrite, and binary Excel parsing remain
  unverified on a live page. See open fix O3.

## Fixes applied (before / after)

All edits are to draft reports or draft files only. No raw
fetch evidence was edited. No Factum JSONL was edited. No
other worker's batch was edited.

### F1. Distinct TTP slug count

File: `reports/aiid-full-site/INGEST-REPORT.md`, TTP bullet.

- Before: "19 distinct slugs".
- After: "18 distinct slugs".

### F2. Bad near-hit batch citation

File: `reports/aiid-full-site/INGEST-REPORT.md`, near-hits list.

- Before: batch id `8f3ed80b8fbb415a8fe399d6fb836d7b2`
  (33 characters, matches no directory).
- After: batch id `8f3ed80b8fbb415a8fe399d6fb836d75`
  (the true directory name).

### F3. Query-string count and exceptions

File: `reports/aiid-full-site/IOC-REPORT.md`, dedup note.

- Before: "The 84 URLs with a query string now carry
  parameter names only".
- After: "84 URL mentions with a query string in extraction
  collapse to 74 distinct URLs after dedup; those 74 now
  carry parameter names only", plus the 2 narrow exceptions
  (path-segment `=` and the incident 1162 path-like
  `?params=` value).

### F4. Snapshot-time precision warning

File: `reports/aiid-full-site/INGEST-REPORT.md`, IOC
`observed_at` bullet.

- Before: disclosure that the source stamp carries no
  timezone and `Z` exists only to satisfy the format.
- After: same disclosure, plus: "`Z` still asserts UTC,
  and the `:00` seconds are padding — the stamp gives hour
  and minute only. Treat the value as a snapshot label,
  not a precise UTC instant."

### F5. Same query exceptions in the ingest report

File: `reports/aiid-full-site/INGEST-REPORT.md`, IOC field
mapping bullet.

- Before: "All 74 URLs that carry a query string use the
  `?params=name1,name2` form only."
- After: same sentence qualified to 74 distinct URLs, with
  the 2 narrow exceptions and a pointer to IOC-REPORT.md.

### F6. Incidents-with-IOCs count

File: `reports/aiid-full-site/iocs.json`, counts block.

- Before: `"incidents_with_iocs": 1775`.
- After: `"incidents_with_iocs": 1774`.
- Check after edit: the file still parses as JSON, and the
  counts block otherwise matches re-derived values.

### F7. Name-claim qualification

File: `reports/aiid-full-site/INGEST-REPORT.md`, validation
bullet for the incident batch.

- Before: "No personal names were added by this executor."
- After: "No submitter, editor, or author personal name was
  added by this executor", plus an adversarial correction
  naming incidents 901 and 1512 as the two behavior-text
  residues, without reproducing the names themselves.

### F8. Cron draft schedule (F3 from verification)

File: `reports/aiid-full-site/aiid-scanner-cron-body-DRAFT.md`,
schedule section.

- Before: "Mondays 09:00 America/Chicago", with "weekday of
  publication is not confirmed".
- After: "Mondays 15:00 America/Chicago", with Monday
  confirmed 2026-10-30 from the live snapshots page, and a
  note that no cron job is created by this draft edit.

### F9. Cron draft state description (F1 follow-through)

File: `reports/aiid-full-site/aiid-scanner-cron-body-DRAFT.md`,
state section.

- Before: snapshot entries shown as `{date: {url,
  anchor_hash}}`.
- After: snapshot entries shown as `{date|kind: {url,
  anchor_hash}}` with schema version 2, and a note that a
  version 1 file is quarantined and re-baselined.

## Fixes NOT applied (left for the coordinator)

### O1. Behavior-text name residues in the batch (decision needed)

- File: `data/records/fc09b8bfbd7b4d719e070fed0d5c4d49/records.jsonl`.
- Lines: incident 901 observation at line 2669; incident
  1512 observation at line 4522 (line numbers from the
  exported file as read during this review).
- Why not fixed here: Factum JSONL must not be hand-edited,
  and this brief forbids editing another worker's batch.
  Options for the coordinator: (a) accept the residues with
  the disclosure now in INGEST-REPORT.md, since the text is
  verbatim public AIID description text and no submitter,
  editor, or author name is involved; or (b) order
  re-extraction with scrubbing for those 2 incidents and a
  re-ingest. Do not silently edit the batch.

### O2. Cron creation and scanner enable (operator word needed)

- File: `reports/aiid-full-site/aiid-scanner-cron-body-DRAFT.md`,
  schedule line 9 (now Monday 15:00 Chicago).
- File: `scripts/swarm-infra-config.json` (no `aiid` block).
- Why not fixed here: creating a cron job and adding
  `"aiid": {"enabled": true}` are operator-gated actions.
  The module is safe to hold disabled. Do not enable live
  scanning until the operator orders it.

### O3. Scanner robustness F4 (verify on first live run)

- File: `scripts/scanners/aiid.py`, listing parser and
  fetch-note branches.
- Items: same-line date fallback if date and anchor sit on
  different source lines; capped 2 MB page treated as `ok`
  and replacing full state; binary Excel parsing left to
  the ingest worker. Confirm entry count is sane (not
  zero) and 2026-10-26 yields both tarball and Excel
  entries on the first live run.

### O4. TOOL-UPDATES.md git-status line (stale as current state)

- File: `reports/aiid-full-site/TOOL-UPDATES.md`, section 6,
  line 341.
- Line says git status showed exactly 3 modified files.
  The current tree does not match that. No edit was made
  because the line may have been true at write time.
  The coordinator must re-check status at commit time
  and commit only the intended paths.

### O5. Config insertion count in the parent brief (no file to fix)

- The brief phrase "152 insertions / 3 deletions" does not
  appear in TOOL-UPDATES.md. True numstat is 149
  insertions and 3 deletions. No draft file states the
  wrong number, so no draft edit was made. The coordinator
  should use 149 insertions when citing the diff.
