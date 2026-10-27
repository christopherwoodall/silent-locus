# Integrated analysis: July 2026 RubyGems spike set

## Terms used here

- **OBSERVED**: our own bytes, kept with provenance. A live fetch, a
  preserved file, a count recomputed from a source file.
- **INFERENCE**: a reading drawn from observed bytes. It can be wrong.
- **UPSTREAM**: a third-party claim. Dashboard labels and Haiku labels
  are UPSTREAM. They are quoted as labels, never as our findings.
- **Tombstone page**: a RubyGems gem page that renders for a dead gem.
  It shows a yanked or not-hosted notice. It is not a live package.
- **Diffend stub**: a Diffend page with no computed diff content. It is
  not proof a gem is gone, and it holds no code.
- **Artifact URL**: a URL with live content behind it under the stated
  rule (RubyGems page only if the API says the gem is live; Diffend
  page only if it holds full diff content; source repo only if it
  answers 200 and is a code host). Counts always name their field and
  denominator.

## 0. Consolidated verdict

The July set is a third-party dashboard export of 533 registry rows,
not our own observation. The live census of 2026-10-27 does not change
any prior verdict. 510 rows are gone from the RubyGems API, including
the whole 310-row combinatorial mass batch and all 100 tester rows.
The 23 survivors split into 18 ordinary gems, 3 probe listings, and
2 test-named listings.

What it is: a July mass-generation shape, plus a July-7 probe-shaped
cluster, plus ordinary gems that fell in the same dashboard window.

What it is not, on this evidence: it is not established as agent
activity. No model, harness, prompt, tool call, session artifact, gem
code, callback receipt, or victim exists anywhere in the file or the
census. Absence of actor evidence does not disprove an agent
publisher. It proves only that this evidence cannot name one.

It is not a severity-graded incident. Dashboard and Haiku severity
labels conflict with each other and shift with prompt version. They
are shape labels, not grades.

It is not a GemStuffer or JFrog finding. The file is silent on that
picture, and no survivor links to it.

## 1. Verdict tests: prior review vs live census

All prior verdicts STAND. No verdict is upgraded. The deciding live
datum is named for each.

| Prior verdict | Result | Deciding live datum |
|---|---|---|
| (a) CSV is a third-party dashboard export, not our observation | STANDS | Census checks names only. 21 of 23 live rows have blank dashboard and Haiku fields. CSV latest matches live latest on only 4 of 23 (first-census latest field; see §3). |
| (b) July-7 verdict: NO CHANGE | STANDS | Only 6 of 204 July-7 rows are live (jrjackson, 3 probes, 2 test-named). 198 are gone, including all 100 tester rows. No code, receipt, or actor evidence arrived. |
| (c) GemStuffer / JFrog picture: NO CHANGE | STANDS | Census adds registry presence only. No survivor links to that picture. |
| (d) Andrey78 batch = mass-generated shape only, no agent evidence, no severity | STANDS | Full census, not a sample: Andrey78 129 of 129, Prvaz12_mars 113 of 113, monib110 68 of 68 are API-404. Removal reason is unknown, so no severity follows. Transience is corroborated. Nothing is upgraded. |
| (e) Agent activity UNPROVEN | STANDS | No model, harness, tool call, or prompt anywhere. Probe download counts (515, 550, 1,282) name no downloader. A shirobai release on census day proves a release, not an agent. |
| (f) 203 of 533 known via the JFrog list only, 330 new | STANDS, with caution | Census does not re-derive overlap. Caution: 21 of 23 live rows are blank-field rows (of 49 blank total). Blank means neither safe nor gone. |

## 2. The July set, by family

Families are disjoint and sum to 533. They were recomputed from the
CSV name and summary columns. The split of the 40 blank-field
descriptive non-combinatorial rows into 20 ordinary and 20
probe-shaped rests on manual judgement (see the grade note). A
replicator following only a printed signal list cannot reproduce the
20 / 20 split exactly. That limit is stated, not hidden.

| Family (our label) | Count | Defining shape |
|---|---|---|
| A. Combinatorial mass-generation | 310 | `[size]-[quality]-[container]`, strict 10 x 10 x 10 word product. Batches: Andrey78 129 on July 6, Prvaz12_mars 113 on July 13, monib110 68 on July 12. One day each. |
| B. Probe / test ("apex") family | 203 | Not combinatorial, not ordinary. Name or summary signals a test, probe, or attack class. All first-published July 7. |
| C. Small-author ordinary gems | 20 | Project-like name plus ordinary descriptive library prose. No probe signal in name or summary. |

Family A detail (OBSERVED): "University research based on X"
summaries on 309 rows, 116 distinct X values, no university ever
named. One combinatorial row breaks the template ("Research based
on…" without "University"). The university link is self-asserted
text only.

Family B detail (OBSERVED): placeholder summaries 86 (`Test` 54,
`testing` 19, `T` 9, `test` 4). The other 117 family-B rows carry
non-placeholder summaries. That 117 is a residual (203 minus 86), not
a positive probe-signal count. Probe-ness of the 117 rests on name
plus summary judgement, not on a counted signal. The prior review's
105 "probe-descriptive" figure is reproduced by no tested rule, and
the prior review's own partition leaves a 33-row hole (309 + 86 +
105 = 500, not 533). Neither 117 nor 105 may be quoted as a
positive "probe-descriptive" count. The earned form is the residual
sentence above.

Apex count correction: names containing substring `apex` = 115, all
in family B. The prior review's 114 matches no rule (dash-only
prefix 80, dash-or-underscore prefix 112, tester-only apex-prefix
95). Names starting with `apex` = 114. Quote "115 substring, 114
prefixed." For tester rows, quote "95 apex-prefixed (68
`apex-black-*` dash-form, 27 underscore-form)."

Family B single-label buckets (one label per row, priority order in
the working notes): SSRF / internal reach 66, generic placeholder
probe 55, parser / page attack 36, registry abuse 34, exfil canary
6, self-asserted authorization / impact 3, webhook callback only 3.
The 55 generic rows (placeholder summary plus a series name only,
such as ipv6 / dns / fuzz segments) are not split further here.
Splitting them by name segment is open work, not done work.

Grade note: family sizes are OBSERVED-shape-plus-judgement, not
pure OBSERVED. The grammar (310) is a strict product and is exact.
The 203 / 20 split inherits the ordinary-set judgement. Date
corroboration helps but does not replace the rule: family C spans
July 6–12 with exactly 1 July-7 row (jrjackson); family B is
entirely July 7.

## 3. The survivor set: 23 live gems

RubyGems API status is the authority for index membership. Both
censuses agree: 23 live, 510 gone. The reconciled census gave
Diffend full 18, RubyGems-only 5, Diffend-only 0, and 48 unique
artifact URLs. A ship-time refresh (2026-10-27, this report) found
jrjackson's Diffend page backfilled to full content (35 arrow
version-pairs, latest pair dated October 21, 2026). That is live
drift, not a census error: both censuses correctly recorded stub
at census time. Current figures at ship time: Diffend full 19,
RubyGems-only 4, Diffend-only 0, unique artifact URLs 49 (23
RubyGems pages + 19 Diffend pages + 7 unique live repo URLs).
Per-gem entries on the reconciled `artifact_urls` field are 50 for
live gems and 51 across all rows (the gone klondikemarlen gem
shares the marlens repo URL). The pre-reconciliation
`artifact_urls_uniform` field (51 / 49, still holding the 2
excluded callback endpoints) must not be quoted.

### 3.1 Classification

Classification is name plus summary self-description, with version,
download, and source data as context only. The working rule was
stated as five-factor, but the factors do not discriminate the
close calls, so the honest rule is single-criterion. Two close
calls are marked UNCERTAIN below rather than forced.

| Class | Count | Members and basis |
|---|---|---|
| Legit / ordinary | 18 | Functional summaries, multi-version histories, live repos where present. Includes jrjackson (50 versions, 10,508,353 downloads, 94.3% of all live downloads) and the shirobai family (4 gems). |
| Probe | 3 | apex-black-test-011 (v9.9.9), apex-oidc-probe, apex-blk-test-final. Single version each, no live repo, Diffend stub after adjudication. |
| Test-named | 2 | test_gem_kangaroo (8 versions, all July 7) and testgem-mini (see §3.3). |

Close calls: minitest-hashdiff is classed legit on name and
summary despite a probe profile (1 version, Diffend stub, no
source) — the same profile as all 3 probes. testgem-mini beats
it on every non-summary factor yet is classed the other way.
Both are UNCERTAIN under any honest rule. The class counts stand
as stated, with that uncertainty attached.

### 3.2 What survival means, with dated evidence

Version publish dates were fetched for all 23 live gems from the
RubyGems versions endpoint for this report (file
live-version-dates-20261027.json). The censuses dropped dates,
so no maintenance sentence was earned before this fetch. Now:

- **Dated post-July releases (13 gems, OBSERVED):** eco-helpers
  (latest September 29, 2026), ecoportal-api-graphql (September
  29), jrjackson (October 21), metz-scan (October 4),
  pico_phone (October 10; 42 of its 55 versions are post-July),
  query-stream (August 6), rosett-ai (August 14), rubocop-metz
  (October 4), shirobai family (4 gems, all October 26),
  talk_to_your_app (September 23). For these 13, continued
  maintenance is OBSERVED, not inferred.
- **No post-July release visible (10 gems):** the 3 probes (all
  single July-7 versions), edoxen (latest July 22), intranet-pictures
  (latest February 2025), marlens-jira-api (latest July 14),
  minitest-hashdiff (single July-10 version), sportdb-parser
  (latest July 6), test_gem_kangaroo (all July 7),
  testgem-mini (all July 7). For these, the earned claim is
  continued availability only.

Continued *use* is INFERENCE for every class. Download counts
are cumulative, not dated. The distinguisher still missing for
use is downloads by version and date, dependents, and repo
commits.

### 3.3 testgem-mini: test-named, use UNEXPLAINED

testgem-mini is reclassified from "test residue" to "test-named,
use UNEXPLAINED." Rank correction: it is 4th of all 23 live gems
by downloads and highest of the 2 test-named gems, not
second-highest in any grouping. New observed evidence, fetched
for this report: all 5 versions were published within 5 minutes
on July 7; downloads spread evenly across versions (about 5,800
to 9,400 each, census total 34,151); the RubyGems
reverse-dependencies page lists zero dependents. Burst timing
plus even spread plus zero dependents point away from organic
use. They do not settle the mechanism. Mirror pulls, CI reuse,
and harness loops are hypotheses, not findings. The count blocks
a residue landing. It does not promote the gem to legit.

### 3.4 Version-loss table (OBSERVED absence, yanked as INFERENCE)

CSV latest is absent from the census versions list for at least
9 live gems: apex-blk-test-final (0.0.5), edoxen (2.1.3; no 2.x
live), intranet-pictures (3.0.0.rc2; only rc1 live),
sportdb-parser (0.9.0), testgem-mini (0.4.6),
talk_to_your_app (0.1.0.pre.4; pre.7 and pre.3 live, pre.4 not),
eco-helpers (3.2.18; 3.2.23 and 3.2.14 live),
ecoportal-api-graphql (1.3.13), query-stream (1.3.0).
"Absent from the census versions list" is OBSERVED. "Yanked" is
INFERENCE pending a list-completeness check: census version
lists carry platform-duplicate rows (pico_phone's 55-entry list),
so they are not plain distinct-version lists.

jrjackson field conflict, resolved: the gem-endpoint latest
field says 0.3.8, but the versions endpoint reaches 0.5.5,
dated October 21, 2026, and Diffend's latest pair agrees
(0.5.5-java, October 21). The versions endpoint is
authoritative. Never quote 0.3.8 bare.

CSV-latest equals live-latest on 4 of 23 (first-census latest
field, cited by name): apex-black-test-011, apex-oidc-probe,
minitest-hashdiff, test_gem_kangaroo. The reconciled JSON's
latest field is null for many live gems and was not used for
this count.

### 3.5 Survivor meaning per class

- **Legit (18):** continued availability for all; dated
  continued maintenance for 13 (§3.2). They survive because
  they are real projects with post-July versions or long
  histories, not because the July spike validated them.
- **Probe (3):** listing residue (INFERENCE, unproven against
  still-referenced fixture). Observed bytes are single July-7
  versions, stub Diffend, no live repo, and no post-July
  version. What would settle it: a post-July version,
  download-by-date, dependents, or a callback receipt. None
  exists. The word abandoned is not used as fact here.
- **Test-named (2):** test_gem_kangaroo is a July-7 burst
  fixture (8 versions in about 4 hours). testgem-mini is
  UNEXPLAINED per §3.3. Neither is evidence of agent
  activity, and neither is promoted to legit.

## 4. The apex family: full profile

114 names sit in the July CSV under a narrow reading; 115 carry
substring `apex` (see §2 for the exact rule). The v2 export
holds 116 apex rows: all 115 CSV names plus apex-hijack-probe-a1 (see §4.4).
The family below is family B (203 rows) viewed through its apex
core: every apex-substring name sits in family B.

### 4.1 Taxonomy by test type (single label per row)

| Test type | Count | Shape |
|---|---|---|
| SSRF / internal reach | 66 | Link-verification wording, internal and backend targets, chain SSRF to a canary. |
| Generic placeholder probe | 55 | Placeholder summary plus a series name only. Test type unspecified on name plus summary. |
| Parser / page attack | 36 | XSS markup, template arithmetic, YAML-word, tar-wording, regexp, parser wording (Nokogiri / Faraday). |
| Registry abuse | 34 | Cross-tenant push and write tests, file-write test, traversal and symlink wording, race and yank wording. |
| Exfil canary | 6 | Webhook exfil labels with epoch tokens, leaked-content labels, chain-to-canary wording, pipe-separated checksum-label rows. Shapes only; no token value is reproduced here. |
| Self-asserted authorization / impact | 3 | See §4.3. |
| Webhook callback only | 3 | Webhook wording with no other test signal. |

Non-exclusive signal counts (name OR summary): SSRF word 58;
link-verification wording 29; internal / backend wording 13;
XSS word occurrences 14 across 10 rows (occurrence count, not
row count); template-arithmetic forms 4; YAML-word signal 4;
tar wording 3; regexp 1; parser wording 9; cross-tenant wording
7; file-write 1; traversal / symlink wording 7; webhook wording
7; exfil / leaked / canary wording 5; OIDC / auth-bypass / OTP /
MFA wording 4; race 8; yank / owner 3.

### 4.2 The empty-shell code finding

Code pulled for the live apex gems (parent pulls, read-only
RubyGems downloads, re-pullable):

- apex-oidc-probe 0.1.1: one file, lib/test.rb, 7 bytes. A
  comment that says test. Nothing else.
- apex-blk-test-final 0.0.1: one file, lib/test_apex_gem.rb,
  43 bytes. An empty module plus a version string. Nothing else.
- apex-black-test-011 v9.9.9: live, author "audit", summary
  "audit-revalidation." Code not separately pulled; its Diffend
  page is stub-class (no diff content).

No real code, no dependencies, no executables in the two pulled
gems. Implication, graded: for the live apex gems, the
"payload" lives in metadata (name, summary, homepage and
source links), not in code. That reading is OBSERVED for the
two pulled gems and INFERENCE for the yanked remainder, whose
code was never fetched (their Diffend pages are stubs holding
no code, and the gems are gone from the index). A metadata
string proves a string was published. It does not prove
execution, a callback, a victim, or an agent author.

apex-oidc-probe's source link is github.com/attacker/repo.
That path reads as a placeholder, not a real repo. It is
graded as placeholder-style (INFERENCE from the path shape),
not as a verified dead link.

### 4.3 Self-asserted authorization claims: UNPROVEN

Three rows carry self-asserted claims, all OBSERVED as
self-description and UNPROVEN as authorization:

- 2 rows claim authorized-assessment / proof-of-impact status.
  Neither summary names an authorizing party or a scope string.
- 1 row claims a push via a scope-escalated legacy API key.
  That is a mechanism claim, not authorization. No key value
  is present anywhere in the file.

Never quote these as verified assessment work. Never quote the
key-push claim as proof a key was misused. The file holds words
about keys, not keys and not receipts.

### 4.4 The apex-hijack-probe-a1 exception

apex-hijack-probe-a1 sits outside the July CSV (v2 only, wave
other-probe-family). Author "audit", first seen 2026-07-07.
September triage graded it a separate probe family: distinct
author and naming, no campaign fingerprints. It is also
captured in the July-7 forensics lane (Diffend HTML). It must
not be folded into the apex tester batch, and it must not be
counted in CSV-based apex totals. Set arithmetic, recomputed
for this report: CSV substring-apex names 115, all present in
v2; v2 apex names 116 (the 115 plus hijack-probe-a1).

## 5. Payload shapes: what strings prove and do not prove

Counts below were recomputed from the CSV by the cryptologist
lane and confirmed by the verifier, with two corrections to the
prior review. Every shape proves at most that a metadata
string was published. None proves execution, callback receipt,
victim, exfiltration, or agent authorship. The CSV holds no gem
code, no rendered-page HTML, and no receiver log.

| Shape | Rows | Prove / not-prove |
|---|---|---|
| OAST callback URL | 29 | Proves a callback identifier was published. 6 full hosts, 4 base domains, 1 host carrying 22 of 29 rows, mostly ssrf_linkback-like first path segments. Does not prove a fetch, a receipt, or data theft. |
| Webhook callback URL | 19 | All in homepage cells (prior review's "18 by homepage host" is corrected to 19). 9 distinct path tokens, reuse-heavy. Does not prove a receipt. |
| SSRF-shape rows | 25 | 24 link-field rows plus 1 summary-text row. Split: 14 internal link-field rows (10 IP-internal shapes plus 4 internal hostnames), 10 public-IP homepages, 1 summary-text localhost URL. The prior review's "24 homepage rows" is corrected: homepage cells are 23, and one further row carries its URL only in summary text. Public-IP homepages must never be quoted as "internal targets." Plain http scheme (12 rows) proves nothing alone. |
| XSS markup in summary | 10 | Image-tag shapes 7, alert calls 8, onerror 6, svg 3, onload 3 (overlapping); script-tag 0 in the scan set. Proves a test string was published. Does not prove rendering or execution. |
| SSTI / template in summary | 4 | Double-brace 1, dollar-brace 1, ERB angle-percent 2. Same fence as XSS. |
| Payload in author field | 9 rows, 2 author-only | Includes the file's only document.cookie shape (author field only). Summary proof does not transfer to the author render path. |
| YAML-word signal | 4 rows; YAML document shape 0 | Word signal in name or summary only. No document marker, no anchor or alias structure, no tag in any metadata field. Never quote bare "YAML 4." |
| Tar wording | 3 rows; tar-traversal string 0 | Wording only. No traversal string (`../`, encoded, backslash) in any scanned field. Never quote bare "tar 3." |
| Code strings (curl, wget, eval, os.system, subprocess), go-import, jina | 0 each | Zero in scanned fields only. This does not clear gem code or served HTML, which are not in the CSV. |

Union arithmetic: 29 + 19 + 25 + 10 + 4 = 87, minus the
4-row OAST-and-XSS overlap = 83 scan-set rows (prior review
said 82; the correction is the SSRF row count 24 to 25).
Including the author field: 85 rows (prior review said 84).
Out-of-band rows (OAST plus webhook, no overlap) = 48. That
48 is a different set from the 49 artifact URLs at ship time.
Never print the two 48s (or 49) in one paragraph without the
different-sets note.

Canary assessment (shapes only, no values reproduced):
a canary is an identifier whose only function is appearing in
a receiver log (OAST subdomain or path, webhook path token).
A canary in a public CSV is not a leak. Only the receiver log
says spent versus unspent. Real secrets are absent:
service-prefix shapes 0, key=value shapes 0, bearer shapes 0.
Token, api-key, and checksum wording appears on 7 summary rows
as words about tokens, not tokens. One summary cell carries a
FAKE_-prefixed shape with checksum wording: synthetic by
construction, not a leaked checksum. Epoch-suffixed names (34,
10-digit time-shaped) and hex-8-suffixed names (18, 32 bits)
are batch and run correlators, not secrets. One author cell
carries a 151-token fuzz list (next-longest author cell: 4):
a field-fuzzing shape, not 151 authors.

Upgrade evidence per shape (the exact artifact that would
lift "published string" to "observed behavior"):
- OAST: operator receiver log (timestamped DNS or HTTP hit
  for that identifier), stronger with a renderer log tying the
  fetch to a gem-page render.
- Webhook: bucket request log for that path token (or its
  "no requests" state). That single fact decides QA versus
  exfiltration.
- SSRF: target or intermediary request log showing a fetch
  attempt, plus response evidence for impact.
- XSS: rendered-page capture or DOM dump proving the field
  rendered unescaped; stronger with an execution receipt
  (dialog capture, cookie arrival, CSP report).
- SSTI: rendered output showing the evaluated result instead
  of the literal expression; stronger with an engine error log.
- Author-field payloads: same proof for the author render path
  specifically.
- YAML, traversal, regexp: cannot be upgraded from this CSV
  at all. They need gem tarball or gemspec bytes inspected
  statically, read-only.

## 6. The tombstone / Diffend shell phenomenon

Page status proves nothing on either host. That is the whole
phenomenon, and it has two halves.

### 6.1 Shell taxonomy: four things that must stay separate

- **Page renders.** A RubyGems page returning 200 means the
  route renders. Dead gems get a tombstone page instead of a
  404 (soft-404): "Yanked by rubygems-security-team", "not
  currently hosted", or owner-removed / name-reserved. Page
  status must never be used as a live or dead signal.
- **API membership.** The RubyGems API (200 versus 404 for
  the gem name) is the authority for index membership. Only
  this decides live versus gone.
- **Diffend content.** A Diffend page renders for the name
  whether the gem lives or not. A stub (about 5.6 KB, no
  computed diff) means no diff was computed. It does not prove
  the gem is gone: jrjackson was API-live and Diffend-stub at
  census time. A full diff is a historical record of versions
  Diffend once saw. It does not prove the gem is live today
  or downloadable.
- **Code availability.** Only a gem file, a matching repo
  tag or commit, or a matching file tree proves code is
  recoverable. No page, repo URL, diff, or collector alone
  passes.

### 6.2 Counts (recomputed; labels and content kept apart)

- Total 533. API live 23, API gone 510. RubyGems page 200
  on all 533.
- Tombstone pages: 510 (one per API-gone name).
- Diffend among the 510 tombstoned: labelled stub 509,
  labelled gone 1 (klondikemarlen-jira-api, redirects to the
  Diffend index). Functional no-diff content: 510 of 510.
- Diffend status among the 510 tombstoned: 200 on 482,
  redirect (302) on 28. The 27 redirect pages labelled stub
  and the 1 labelled gone are functionally identical
  (no diff content). Never print "Diffend gone = 1" without
  "no-diff = 510, redirect-status = 28" beside it.
  Recommended future rule: redirect-to-index counts as gone
  (gone 28, 200-stub 482), applied uniformly. Relabelling is
  a future-census decision, not a blocker here, because every
  count that matters uses content, not the label.
- At ship time (after the jrjackson backfill): Diffend full
  19, Diffend no-diff 514 across all 533 (513 labelled stub
  plus 1 labelled gone). Live-on-both 19, RubyGems-only 4,
  Diffend-only 0.
- Caveat on tombstone sub-types: only 259 of 510 tombstone
  rows carry an explicit page-text note. The rest rest on API
  404 plus page 200, not on row-by-row text reads. Sub-type
  (security-yanked, not-hosted, owner-removed) must be
  stated only where text was actually read; otherwise write
  "tombstone, sub-type unread."

### 6.3 The single true live mirror

klondikemarlen-jira-api: gem API-404, Diffend gone, but its
declared source repo (github.com/klondikemarlen/jira-api)
answers 200. The plain explanation: it is also the declared
source of the live sibling gem marlens-jira-api (API-live, 5
versions, latest July 14, 2026; same author and summary in
the CSV). The repo lives because the sibling project lives.

It does not prove the dead gem's code is recoverable. A
shared declared source URI is metadata, not provenance, and
repo HEAD today is not July code. The proving check is:
fetch tags and history read-only, find a tag or commit for
klondikemarlen-jira-api 0.1.1 (or a gemspec rename commit
preserving the 0.1.1 tree), and match its file contents or
hashes to the published gem. Until then: "repo live;
recovery unproven." It is one of 7 unique live repo URLs,
shared by 2 gem rows. Do not double-count it, and do not
count it as a live gem.

### 6.4 The 2 live OAST collectors (excluded as artifacts)

apex-black-test-013 (SSRF-test gem, 0.0.1) and xss-test-gem
("SSRF Callback", 0.3.5) are both API-404 and Diffend-stub,
and their OAST endpoints answer 200. A collector answering
200 proves only that the canary listener still resolves and
serves today. It proves no callback receipt, no
exfiltration, and no QA verdict. Names and summaries state
probe intent, not a result.

The receipt that would settle it: the operator's OAST
session interaction log for that exact canary subdomain,
showing an inbound request in the July probe window with
source, path, headers, and payload — filtered to exclude
later visitors, including census probes themselves, which
can hit a live canary. Without that log: "listener alive;
no callback receipt; QA and exfiltration unproven." Do not
re-poll the canaries to "check again." A new poll pollutes
the very log that could settle the question.

### 6.5 Per-row rule block (use this going forward)

```
1. LIVE — API 200 for the gem name. Page, Diffend, and CSV
   flag do not change this.
2. GEM-REMOVED — API 404 for the gem name. Record "removed /
   not in index", never "yanked" on this alone. Page 200 is
   a tombstone; sub-type only if text was actually read
   (security-yanked / not-hosted / owner-removed-reserved,
   else "tombstone, sub-type unread").
3. VERSION-YANKED — only within a LIVE gem: a version absent
   from the current API versions list but shown to have
   existed in an older record. A gem-level API 404 is NOT
   version-yanking.
4. WITHDRAWN (CSV) — dataset flag only. Quote as "CSV
   withdrawn=True (July-window flag)" beside the current API
   status. It never overrides API status.
5. DIFFEND — content class only (full / stub / gone). It
   never changes RubyGems status.
6. SOURCE — code-host 200 = candidate location only. OAST
   200 = listener live, NOT an artifact, NOT a callback.
   Neither changes gem status.
7. CODE AVAILABILITY — "recoverable" needs a gem file, a
   matching repo tag or commit, or a matching file tree.
   No page, repo URL, diff, or collector alone passes.
```

## 7. Open questions, each with a recommendation

The operator decides. Each item below is a recommendation,
not a decision.

### 7.1 (a) The 330 new names: corpus lane or dashboard pointers?

**Recommend: SPLIT, with the admission narrowed.** Admit the
310 combinatorial batch rows as a shape-only lane carrying
names, grammar, timing, and first-publish dates ONLY. Strip
source_uri and homepage-profile fields, or store them flagged
as "pattern-derived, unverified, repo dead on census": all
191 present source URIs on the admitted set are exactly the
mechanical github.com/<author>/<name> pattern, consistent
with dashboard-generated links, not observed repos, and the
census found tombstoned GitHub sources dead. Every lane
record must carry the grade string "shape-only, not agent
activity, not severity" in the record itself, not in a
covering note — otherwise a later citation upgrades shape to
campaign by dropping the grade.

Admit the 20 small-author names as ordinary-gem records on
their own terms, or state explicitly that the corpus
criterion is shape-only and the 20 are excluded for that
reason — not because they are unverified. They are the most
verified rows in the set: the held-out 20 contain 18 of the
23 live gems, while the admitted set contains zero live
gems. A rule that admits dead shapes and holds out live
projects must say so plainly.

Live-census contribution, stated at full strength: the
census covered all 533 names, not a sample. All 310
combinatorial rows are API-404 (129 / 129, 113 / 113,
68 / 68) and all 100 tester rows are API-404. "Wait for
code" would block the shape lane forever, since the gems
are gone and Diffend holds stubs only. A shape lane is the
honest form for historical metadata.

### 7.2 (b) Re-run the pkg-review-1 rows under pkg-review-2?

**Recommend: CONDITIONAL, not unconditional.** Run it only
when a concrete severity-reuse decision is pending. Scope is
513 (464 v1 rows plus the 49 unscored rows), not 464: the
49 are part of the denominator problem and must not be
omitted from the fix. Preserve all three label sets
(dashboard, v1, v2 — never overwrite). Run a matched-shape
consistency check on v2 before any v2 label is quoted.

Why conditional: v2 is unproven at n = 20, with empty score
bands (46–61, 73–87) and matched-shape flips as large as
v1's (combinatorial-only: high on 111 v1 rows, medium on
all 5 v2 rows). Re-running may replace one unstable
distribution with another. It fixes calibration only: it
does not fix missing code or missing receipts, so
post-re-run severity is still metadata severity. And no
integrated verdict awards a severity verdict, so the re-run
currently gates no live decision. Otherwise, freeze v1 as
UPSTREAM with the calibration warning attached, and spend
the effort on the version-date work in §3 (already done
for the 23 live gems).

Meanwhile, broad shape sort may be reused. Levels and scores
may not.

### 7.3 (c) Did any OAST / webhook callback ever arrive?

**Recommend: treat as UNRESOLVED. Claim neither QA nor
exfiltration.** The file holds 48 homepage strings only
(29 OAST, 19 webhook by substring, no overlap). A string
proves a link was published, not that it was fetched, by
whom, or with what payload. QA testing and exfiltration
predict the identical string, so the question is undecidable
from this file.

The receipt that would settle it: one log entry per
distinct endpoint token (6 OAST hosts, 9 webhook UUID paths)
showing time, source, path token, and headers or body. A
single QA self-test hit reads differently from repeated
external hits, and even a hit without payload proves a
fetch, not data theft. Holders: the OAST service operator
and the webhook inbox owner (presumably the publisher or
QA author; identity is not pursued here), plus the registry
operator only if the registry itself followed links.

Bounded language: no receipt was found in the public
sources checked. Receipts sit in private inboxes held by
others. Do not probe the endpoints: our fetch would
fabricate a callback and pollute the settling log. The
live census adds zero to receipts — its 49 artifact URLs
are a different set from the 48 out-of-band rows and must
not be conflated — but its deliberately unfetched internal
metadata-address URI models the same restraint.

### 7.4 (d) The 13 v2 July-7 window-test gems absent from the CSV

**Recommend: treat as an open scope question, not a
finding.** Candidates in test order: (1) different source
cut — CSV built from the JFrog list plus rule-firing rows,
versus v2 time-window scan regardless of rule fire; (2)
narrower dashboard window edge; (3) author or shape filter
outside the tester probe batch; (4) weaker: export snapshot
timing (July 7 is not generally missing — 204 CSV rows —
only this subset is).

Confirming check, low cost and local only: one comparison
table for the 13 absent versus the 11 shared July-7 rows
versus the 192 wave-null JFrog July-7 rows, on name,
author, first-publish time, v2 grade and wave, rule-fire,
and JFrog membership. An explanation counts only if it
fits all 13. Do not assume importance away, and do not
backfill CSV counts. Live-census contribution: as scoped
to CSV rows it covers none of the 13, so it neither
explains nor closes this. An API existence check for the
13 would add live or gone status but would not explain
the omission.

## 8. Gaps that remain, re-ranked

The earlier draft's "66 unchecked tombstoned source URIs"
gap is DELETED. It was false: 65 of the 66 rows labelled
unchecked have no source URI at all, and only 1 is
genuinely excluded (the internal metadata-address URI).
The true statement replaces it: tombstoned source URIs
checked 196 of 196 present (192 dead, 3 live: 1 repo
mirror plus 2 OAST listeners); 1 URI deliberately
excluded; 313 tombstoned rows have no URI and belong to
the source-absence gap. No "fetch 65 URIs" instruction
survives. Ranks below exclude that gap.

| Rank | Gap | Blocks | Closes |
|---|---|---|---|
| 1 | Gem code for yanked gems never fetched. Diffend stubs hold no code. Gems are gone from the index. | Code behavior for the 83 payload rows and batch rows; any backdoor, SSRF-execution, XSS-firing, or agent-behavior claim; any upgrade from shape to behavior or impact. | Gem bytes from a preserved mirror with hash match to the registry version — or a documented exhaustive negative, after which claims stay permanently capped at metadata-only. |
| 2 | Withdrawn flag versus live state, per-row rule. | Any per-row "removed / yanked / gone" claim. Hides version-level truth (live gems carry yanked versions; CSV flag says withdrawn on all 533). | The §6.5 rule, applied to all 533 rows: gem-removed (API 404 all versions) versus version-yanked (CSV latest absent, other versions live) versus gem-live. Flag described downstream as an export descriptor, not registry state. |
| 3 | 49 unscored rows (including 6 monib110 batch rows; July 8–10 have zero scored rows). | Any aggregate severity or category claim over 533 rows (scored n is 484, not 533); date trends for July 8–10; monib110 batch completeness. | Dashboard re-export scoring the 49, or same-prompt pkg-review-2 re-review of the 49 with a coverage note. Until then report 484 scored and 49 unscored separately. Never impute. Never read empty as safe. |
| 4 | 327 names with no source URI (61.4%). | Source-repo verification for most of the set; checking Haiku "source repo name matches" claims; code via source even if a gem returned. | Registry API metadata re-check for the 23 live gems; for tombstoned gems, a documented absence — never an invented URI. Source absence is itself a shape signal. |

A genuine callback receipt (question 7.3) would rank near
the top on verdict change, but it is high-impact yet
unclosable from public data (private inboxes, and probing
would pollute the evidence). It is not ranked as next work
for that reason.

## 9. Corrections log (what changed against prior documents)

Every number below was recomputed for this report. "Prior"
means the July spike review (REPORT.md) or the live
censuses, as named.

- Apex names: 114 → 115 substring (114 prefixed). Prior
  114 matches no rule.
- Probe-descriptive summaries: prior 105 irreproducible
  under every tested rule. Earned form: 117 non-placeholder
  summaries in family B (residual 203 − 86), with the
  residual rule stated. Prior partition hole: 309 + 86 +
  105 = 500, leaving 33 rows unaccounted.
- SSRF-shape rows: 24 → 25 (24 link-field rows plus 1
  summary-text row). Homepage cells 23, not 24.
  Public-IP homepages inside the set: 10, never "internal
  targets."
- Payload union: 82 → 83 scan-set rows; 84 → 85 including
  the author field. Cause: the SSRF correction above.
- Webhook: "18 by homepage host" → 19 homepage cells.
- YAML: word signal 4 rows, document shape 0 rows. Tar:
  wording 3 rows, traversal string 0 rows. Bare "YAML 4"
  and "tar 3" are banned from this report.
- XSS word: 14 is an occurrence count across 10 rows, not
  a row count.
- CSV-latest equals live-latest: 3 → 4 of 23 (first-census
  latest field; test_gem_kangaroo was missed).
- Diffend full at census time: first census 22, reconciled
  18 (4 probe and test pages adjudicated stub-class, about
  5.7 KB, no diff content). At ship time: 19 (jrjackson
  backfilled). RubyGems-only: first census 1, reconciled
  5, ship time 4. Artifact URLs unique: first census 52,
  reconciled 48, ship time 49.
- "66 unchecked source URIs" gap: deleted as false (§8).
- Tombstone Diffend labels: labelled gone 1, redirect
  status 28, no-diff content 510. The label split is not
  a content split.
- v2 apex rows: 116 (115 CSV names plus
  apex-hijack-probe-a1), not 115.
- "Sampled batch names gone" → full-census figures:
  combinatorial 310 of 310 gone, tester 100 of 100 gone.
- Disproof language removed: "is not agent activity" →
  "is not established as agent activity on this evidence."
- "Abandoned residue" → "listing residue (INFERENCE,
  unproven against still-referenced fixture)."
- testgem-mini: rank corrected (4th of 23, highest of the
  2 test-named); class changed to test-named, use
  UNEXPLAINED.
- Maintenance: blanket "continued maintenance" replaced
  by the dated split in §3.2 (13 dated post-July, 10 not).

## 10. Method, limits, and files

Method: read-only GET and HEAD only (curl; python httpx is
broken on this VM). No login, no account, no POST, no
sessions. No fetched payload was executed. No
credential-shaped value and no full canary token is
reproduced in any deliverable (shapes and counts only).
No Factum writes. No Transluce or other report
submissions. No OAST or webhook callback URL was fetched
at any stage. The internal metadata-address URI was never
fetched.

Limits that survive this report: gem code for yanked gems
is still unfetched (§8 rank 1). Callback receipts are
still private (§7.3). The 203 / 20 family split rests on
manual judgement (§2). The 117 figure is a residual, not
a positive signal count (§2). Classification of the 2
close-call survivors is UNCERTAIN (§3.1). The adversarial
review below was NO-SHIP on its draft; this report applies
its 20 fixes, and the verifier's blocking fixes, but no
second independent adversarial pass re-ran after the
fixes. That re-pass is the one quality gate still open.

Files in this directory (all staged, none pushed):

- REPORT.md — this report.
- findings.json — numbered findings with grade and
  evidence paths.
- adversarial-review.md — the NO-SHIP draft review plus
  disposition of each fix.
- verifier-report.md — the SHIP-WITH-FIXES verification
  plus the ship-time refresh.
- live-urls-refreshed-20261027.txt — 49 artifact URLs at
  ship time (reconciled 48 plus jrjackson Diffend).
- live-version-dates-20261027.json — version publish
  dates and per-version downloads for the 23 live gems,
  fetched for §3.2.
- MANIFEST.md, SHA256SUMS.
- working/ — lane notes, adversarial draft, verifier
  draft (audit trail, not deliverables).
