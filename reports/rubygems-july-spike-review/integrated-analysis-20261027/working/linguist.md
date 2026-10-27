# LINGUIST lane — July 2026 RubyGems spike set (names + summaries only)

Scope and method. Source is the preserved operator CSV only:
`data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv`
(533 rows). This lane used the `name` and `summary` columns only for
taxonomy. Homepage, source, author, dashboard, and Haiku columns were
NOT used to assign a test type. Author values appear below only as a
cross-check against the prior review's batch counts, never as the
definition of a family. No payload was executed. No credential-shaped
value and no full canary token is reproduced here; canaries are
described by shape only. Counts below were recomputed from the CSV
for this lane, not copied from the prior review.

Grade key. OBSERVED = the string is present in the preserved CSV.
INFERENCE = my reading of what the string signals; the CSV proves the
string, not the intent, the execution, or the actor. UPSTREAM = a
dashboard or Haiku label from the CSV; this lane does not reuse those
labels as findings.

## 1. Family taxonomy (name + summary only)

Total 533 = 310 + 203 + 20. The three parts are disjoint by construction
below and sum exactly.

| Family (my label) | Count | Defining shape (name + summary) |
|---|---|---|
| A. Combinatorial mass-generation | 310 | Name matches `[size]-[quality]-[container]` from a strict 10 x 10 x 10 word product; all 10 words occur in each slot. Summary is almost always the university template (see below). |
| B. Probe / test family ("apex" family in the brief) | 203 | Not combinatorial, and not an ordinary descriptive gem. Name or summary signals a test, probe, scan, or named attack class (SSRF, XSS, traversal, cross-tenant, and the rest in section 2). Includes the placeholder-summary rows. |
| C. Small-author ordinary gems | 20 | Name is a project-like name and summary is ordinary descriptive library prose, with no test/probe signal in name or summary. |

Cross-checks (author field only, not the definition):

- Family A splits 129 / 113 / 68 across the three batch author values
  named in the prior review, and no combinatorial name carries any
  other author value. First-publish dates are one day per batch:
  July 6, July 13, July 12 respectively.
- Family B is entirely first-published July 7 (203 of 203).
- Family C is spread across July 6–12, with only 1 row on July 7.
  That July-7 ordinary row is the one real-library name the prior
  review already flagged as new to us.

### Family A detail (OBSERVED)

- 310 names, zero overlap between the three batches, 310 distinct
  names out of 1,000 possible combinations.
- Summary template `University research based on <X>`: 309 rows,
  116 distinct X values. The X values are existing gem/library names;
  no university is named in any summary, and X never matches the
  package's own name.
- The one off-template row: a combinatorial name whose summary reads
  `Research based on <X>` with the word "University" missing. So the
  template count (309) is one less than the family count (310). That
  row is still family A by name grammar.
- Reading: the template asserts a university link. That assertion is
  INFERENCE-free as a string (OBSERVED) and unverified as a fact
  (no university, source, or affiliation string exists in the CSV).

### Family B detail (OBSERVED shapes)

- Placeholder summaries only: 86 rows — `Test` 54, `testing` 19,
  `T` 9, `test` 4. All 86 sit in family B. A placeholder summary
  carries no test-type signal by itself; family B membership for
  those rows rests on the probe-shaped name (see generic row in
  section 2).
- Descriptive (non-placeholder) summaries in family B: 117 rows.
  See the reconciliation flag in section 4 for the prior review's
  different "probe-descriptive" figure.
- Name shapes inside family B:
  - Substring `apex` in the name: 115 rows (all in family B; none
    in families A or C). Of these, 73 are `apex-black-*` names.
  - `apex-black-test-NNN` strict series: 14 rows cross-author,
    11 of them under the author value `tester`.
  - 10-digit epoch suffix on the name (`-<10 digits>`): 34 rows.
    This is wider than the two author groups the prior review
    highlighted (13 + 10 = 23); 11 further epoch-suffixed probe
    names carry other author values.
  - `ssrf-*` prefix: 23 rows total. Of the 20 rows under author
    value `t`, 19 are `ssrf-*` (18 with an 8-hex suffix, 1 with an
    epoch suffix) and 1 is an `apex-black-noko-*` name.
  - Fuzz / long / boundary names: one name is a 100-character
    repeated-letter string; one is a long repeated-letter suffix
    on an `apex-black-long-*` name; one author value is a 151-token
    comma list of fuzz author tokens on a single row. These are
    length/boundary shapes, not test-type claims.

### Family C detail (OBSERVED)

- 20 rows. Summaries are multi-sentence library descriptions
  (parsers, linters, API clients, a Rails agent stack, a phone
  library, a test helper). No name or summary in this family
  contains a test, probe, SSRF, XSS, traversal, or tenant word.
- INFERENCE, weak-to-moderate: these read as ordinary published
  gems swept into the same export window, not as probes. The CSV
  alone cannot prove they are benign; it proves only that their
  names and summaries carry no probe signal. "Ordinary" is my
  label, not the data's.

### Other shapes found (no fourth family needed)

- Markup-as-identifier: 9 rows carry a script/image/template string
  as the author value. This lane excludes the author column from
  test-type assignment, so those rows are counted in family B only
  where their name or summary independently signals a probe. The
  author-column payloads are a separate lane's count and must not
  be added to the section 2 totals.
- No go-import, VCS, jina, or council string occurs in any name or
  summary in this set (OBSERVED, name+summary scope only).

## 2. Apex / probe taxonomy (family B, n = 203)

### 2a. Primary partition (single label per row, sums to 203)

Priority order applied in this sequence, so a row with two signals
lands in the first matching bucket: (1) self-asserted
authorization/impact claim, (2) exfil canary, (3) parser/page
attack, (4) SSRF/internal reach, (5) registry abuse,
(6) webhook callback only, (7) generic placeholder. The order is
my convention; a different order would move rows between buckets
3–6 without changing the non-exclusive counts in 2b.

| Primary bucket (my label) | Count | What puts a row here (name or summary) |
|---|---|---|
| SSRF / internal reach | 66 | SSRF wording, link-verification wording, metadata wording, internal-service or backend-IP wording, localhost or internal-host wording, redirect wording, port scan, or an `ssrf-*` name. |
| Generic / placeholder probe | 55 | Placeholder summary (`Test`/`testing`/`T`/`test`) and no specific test-type signal in name or summary beyond a probe-series name (`apex-black-*`, `fuzz`, `ipv6`, `dns`, `self`, `probe`, `multi`, `edge`, `size`, `long`, and similar segments). Test type is UNSPECIFIED on name+summary evidence, not "no test". |
| Parser / page attack | 36 | XSS image/svg error-handler shapes in the summary, XSS wording, template-arithmetic strings (`7*7` in mustache/ERB/dollar forms), YAML anchor/tag shapes, tar wording, regexp wording, Nokogiri/Faraday parsing wording, or RDoc-markup wording. |
| Registry abuse | 34 | Cross-tenant / cross-account / cross-tenant-write wording, file-write wording, traversal or symlink wording, owner-injection or ownership wording, OIDC or auth-bypass or OTP/MFA wording, yank-scope wording, audit-revalidation wording, race wording, job/platform/version-requirement/dependency-resolution wording, or crafted-paths wording. |
| Exfil canary | 6 | Exfil/leaked/payload-leak/canary wording, or a pipe-separated summary whose fields are a word, a version, a platform, and a placeholder checksum label. See shape notes below. |
| Self-asserted authorization / impact | 3 | See 2c. |
| Webhook callback only | 3 | Webhook fire / payload / capture wording with no SSRF, exfil, or parser signal in name or summary. |
| Total | 203 | |

### 2b. Non-exclusive signal counts (name OR summary; rows counted once per signal, totals exceed 203)

These are the safer numbers to quote, because they do not depend on
my priority order.

| Signal (name or summary contains it) | Count | Grade |
|---|---|---|
| Word `ssrf` | 58 | OBSERVED string; SSRF intent is INFERENCE |
| Link-verification wording | 29 | OBSERVED; includes "verify link job" wording |
| Internal / backend reach wording (internal service, backend IP, metadata, localhost, internal host) | 13 | OBSERVED; reach is INFERENCE (no receipt in CSV) |
| XSS word (`xss` in name or summary) | 14 | OBSERVED |
| XSS markup shape in summary only (image/svg error-handler shapes) | 10 | OBSERVED; matches the prior review's summary-shape count |
| Template-arithmetic strings (`7*7` forms) | 4 | OBSERVED; SSTI/template intent is INFERENCE |
| YAML signal (name word `yaml`, or YAML anchor/tag shapes in summary) | 4 | OBSERVED string; YAML-attack reading is INFERENCE, and weakest for the two rows whose summaries are only `T` or a template string — there the name alone carries the signal |
| Tar wording (tar traversal, malformed tar name, corrupt-tarball summary) | 3 | OBSERVED |
| Regexp wording | 1 | OBSERVED |
| Parser wording (Nokogiri parsing, deeply nested / null-byte / broken HTML, Faraday timeout) | 9 | OBSERVED |
| Cross-tenant / cross-account wording | 7 | OBSERVED; cross-tenant effect is INFERENCE |
| File-write wording | 1 | OBSERVED |
| Traversal / symlink wording | 7 | OBSERVED |
| Webhook wording | 7 | OBSERVED; callback receipt is NOT in the CSV |
| Exfil / leaked / payload-leak / canary wording | 5 | OBSERVED |
| OIDC / auth-bypass / OTP / MFA wording | 4 | OBSERVED |
| Race wording | 8 | OBSERVED |
| Yank / owner wording | 3 | OBSERVED |
| Placeholder summary only | 86 | OBSERVED |

Parser/page sub-note. The 4 template-arithmetic rows are: one
mustache-form template-injection summary, and three bare template
strings (two ERB forms, one dollar form). The prior review's "4 SSTI"
count is the same 4 rows on name+summary evidence. The YAML rows and
the template rows overlap by name in one case (a YAML-named gem
whose summary is an ERB template string); that row is counted in
both non-exclusive signals and once in the primary partition.

Registry-abuse sub-note. Cross-tenant wording (7) plus file-write
wording (1) plus traversal/symlink wording (7) overlap on one row
(a tar-traversal name counted under both tar and traversal). The
primary registry bucket (34) also absorbs race, OIDC, auth-bypass,
OTP/MFA, yank, ownership, audit, job, platform, version-requirement,
dependency-resolution, and crafted-paths rows that carry no
cross-tenant or traversal word. None of these strings proves a
push, write, or traversal succeeded; they prove the words were
published in the metadata.

### 2c. Exfil canaries — shape only

Six primary-bucket rows, five shape families (one shape occurs
twice in name form only):

- Shape 1 (summary): a webhook exfil label followed by a token
  built as a word prefix plus a 10-digit epoch. Token value NOT
  reproduced.
- Shape 2 (summary): a single lowercase leaked-content label plus
  a 10-digit epoch. Token value NOT reproduced.
- Shape 3 (summary): a chain description naming SSRF through a
  backend to a canary. No token value present.
- Shape 4 (summary): a short "payload leak" version label. No
  token value present.
- Shape 5 (summary): pipe-separated fields — a word, a version
  number, a platform word, and an uppercase placeholder checksum
  label naming a target framework. Checksum label NOT reproduced.
- Shape 6 (name only): names containing an exfil segment
  (`exfil` in the name) whose summaries are link-verification or
  label-epoch strings. These rows sit in the SSRF primary bucket
  under the priority order, not in the exfil primary bucket; they
  are counted in the exfil non-exclusive signal only via the name.

INFERENCE: the epoch-suffixed label shapes look like per-run
canary markers designed to be matched against a callback log.
Whether any callback arrived is NOT in this CSV and is not claimed
here. Homepage/source canary strings are out of scope for this
lane and are not counted above.

### 2d. Self-asserted "authorized assessment" claims

Three rows, all INFERENCE-free as strings and unverified as facts:

- 2 rows explicitly claim an authorized / assessment
  proof-of-impact status in the summary (one uses the words
  "authorized security assessment"; one uses "security assessment
  proof-of-impact"). No authorizing party, scope, or permission
  string appears in either summary.
- 1 further row claims a push via a scope-escalated legacy API
  key. That is a mechanism claim, not an authorization claim, and
  is counted separately from the 2 above. No key value appears
  in the name or summary, and none is reproduced here.

Grade for all three: OBSERVED as self-description; authorization
itself is UNPROVEN on this file. The brief's "two authorized
assessment claims" is the first pair; the key-escalation row is
the third related claim the prior review already separated out.

## 3. Grading summary

| Claim | Grade | Basis |
|---|---|---|
| Family sizes 310 / 203 / 20 | OBSERVED | Recomputed from name+summary patterns; sums to 533 |
| Combinatorial grammar 10 x 10 x 10, all slots full | OBSERVED | Name pattern, verified per slot |
| University template 309, 116 X values, no university named | OBSERVED | Summary pattern |
| Probe test-type counts (2a, 2b) | OBSERVED strings; INFERENCE intent | Strings are in the CSV; success, execution, victim, and actor are not |
| "Ordinary gems" (family C) | INFERENCE (weak-to-moderate) | Absence of probe signal in name+summary, not proof of benignity |
| "Mass-generated" as a family name | My label for an OBSERVED shape | Batch + grammar + template; no agent or automation evidence in name+summary |
| "Apex family" as a family name | My label, following the brief | The CSV's own words are `apex`, `test`, `probe`, `ssrf`, etc.; "apex family" is not a string in the data |
| Dashboard levels, Haiku levels/categories, agent-activity labels | UPSTREAM, not used | This lane did not use those columns for any count |
| Any agent attribution, severity, or impact | UNPROVEN on this file | No model, harness, prompt, code, download, victim, or callback receipt in name+summary |

## 4. Contradictions / reconciliation flags vs the prior review

1. Apex-substring count: 115, not 114. Recomputed: 115 names
   contain the substring `apex`, all inside family B, none in
   families A or C. The brief's "114 apex names" is off by one
   on this definition. If the brief meant a narrower definition
   (for example apex-prefixed names only), it should be stated;
   apex-prefixed names (dash or underscore) in family B are also
   not 114 on any prefix rule I tried.
2. "Apex first token on 95" for the `tester` author value: holds
   only under a loose prefix reading. Recomputed: 95 of 100
   `tester` rows have names starting with `apex` (68 dash-form
   `apex-black-*`, 27 underscore-form `apex_*`); strict
   dash-token `apex-*` gives 68, and "black second" gives 68.
   Recommend the coordinator quote "95 apex-prefixed (68
   `apex-black-*`)" rather than "first token".
3. Probe-descriptive summary count: 117, not 105. Recomputed:
   family B rows with a non-placeholder summary number 117
   (203 minus 86 placeholders). The prior review's "105"
   probe-descriptive rows has no definition in the report that
   reproduces 117 minus 12, so the 12-row gap is unresolved.
   Do not reuse 105 without a stated rule. (The 10 markup-only
   summaries and the pipe-separated checksum summary are
   plausible exclusions under a keyword rule, but they account
   for at most 11, not 12, on the rules I tested.)
4. No other hard contradiction found. Verified as stated:
   combinatorial 310; university template 309; strict
   `apex-black-test-NNN` 14 cross-author / 11 under `tester`;
   `ssrf-*` 19 of 20 under author value `t` (18 hex, 1 epoch);
   epoch-suffixed names 13 of 13 for SR and 10 of 10 for `Test`;
   placeholder summaries 86 (54 / 19 / 9 / 4); XSS markup shape
   in summary 10; template-arithmetic summaries 4; 20 ordinary
   names. The epoch pattern (34 rows) and the `ssrf-*` prefix
   (23 rows) are both wider than the author-scoped figures in
   the prior review; that is an extension, not a contradiction.
5. Scope warning, not a contradiction: the prior review's
   payload total (82 rows) counts homepage, source, and author
   columns. This lane's totals count name+summary only and are
   therefore smaller by design. Do not compare the two totals
   directly.

## 5. What this lane cannot say

- Whether any probe, SSRF, XSS, traversal, or push succeeded.
- Whether any callback, exfiltration, or leak was received.
- Whether any author value is a person, a team, a script, or
  an agent. The CSV's name+summary columns contain no such
  evidence, and this lane makes no such claim.
- Whether family C gems are benign. Only that they carry no
  probe signal in name or summary.

Method note for reproducibility. Combinatorial test: split the
name on `-`, require exactly 3 parts, each part in the fixed
10-word slot list. Ordinary test: name not combinatorial AND
summary is descriptive library prose with no test/probe/attack
word from the section 2b signal list. Probe test: the remainder.
Primary partition order is stated in section 2a; non-exclusive
counts in 2b do not depend on that order.
