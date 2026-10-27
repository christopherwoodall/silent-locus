# Cross-surface pivots and novelty — lane 4

## Terms

- Pivot: one kept item searched on a different surface.
- Surface: one place searched. The surfaces here are urlquery, GitHub
  issues, GitHub code, urlscan, and crt.sh.
- SECONDARY: evidence from a third party. It is not first-hand capture.
- POSSIBLE: the shape is plausible but thin or bounded.
- Overlap: a result that repeats a known item or the item itself.
  Overlap adds zero independent weight. It is never corroboration.
- Self: a search that returns the kept item itself. Self is a kind of
  overlap. It adds zero independent weight.
- Neutral: the surface adds nothing and kills nothing for the item.
- Sample null: nothing in the fetched sample matches. The full set was
  not read. A sample null is not a set null.
- Factum: the local structured evidence store. Match queries read it.
  They do not write to it.
- Tracker snapshot: the latest Transluce findings list file saved in
  the tracker raw dir. It is a snapshot, not a live tracker query.

## Task and scope

This lane pivots 17 kept items across other surfaces. It does not rank.
The coordinator ranks.

The 17 items are: the broad-hunt 10, the HN 3, the HN appendix 2, and
the 2 leads (SharedRoot and Bedrock DNS).

Grades stay SECONDARY by default. No pivot here upgrades a POSSIBLE
item to confirmed. No pivot here kills a kept item outright.

This lane records no poster names. Model and tool names from sources
are in scope. Notes carry host names and path shapes only. No signed
query strings, signatures, tokens, or credential-shaped values appear
in notes. Raw captures keep full bytes. Each capture has a provenance
sidecar and a hash sidecar.

## Method

All work is read-only. No POST was used anywhere. No login was used
except the existing GitHub auth. No Shodan was used. No Factum writes
were made. No Transluce submission was made. No commit, push, or
branch switch was made.

- urlquery: public API search through the existing scanner CLI.
  Limit 10 rows per query. Detail was fetched for 3 rows only: the
  routify bare-host row, one vendor support row, and one vendor labs
  home row. Other items had no candidate row to detail-check, or
  their sample rows were clearly unrelated.
- GitHub: read-only GET through the existing auth. Issues search
  needs an issue qualifier, so issues queries carry it. PR-origin
  items get a second, labelled PR-side query. Code search is
  unquoted token match in most cases. Limit 5 rows per query.
- urlscan: public anonymous search. Metadata only. The window is the
  last 30 days. Detail is login-gated. The gate was not bypassed.
  No urlscan row here rests on detail.
- crt.sh: certificate search for named hosts only. Five hosts were
  checked. A 502 or an unsupported pattern would be UNCHECKABLE, not
  zero. No such case hit this lane. The exact routify host returned
  an empty list. That is a checkable zero for certs.
- Factum: exact-match and fuzzy queries per key term, limit 5.
  The lock flag was placed before the subcommand, as ordered.
  No lock block hit this lane.
- lists: grep over the 533-line URL inventory.
- Tracker: grep over the latest snapshot file, dated 2026-10-27.
- Legacy trees: grep over the legacy evidence tree and over the
  other lane's raw tree, for cross-lane overlap.

## Coverage counts

- Pivot rows: 91 rows in pivot-results.tsv. That is 17 items times 5
  surfaces (85), plus 3 PR-side rows, plus 3 urlquery detail rows.
- urlquery searches: 17. Fetched rows: 10 or fewer per query.
  Totals of 0, 1, 4, and 5 are fully fetched. Larger totals are
  sample-only.
- urlscan searches: 17. Size 20 per query. All but one returned 0.
  The one hit is a vendor home page.
- crt.sh hosts: 5. Named hosts only. Other items have no host, so
  their crt.sh row is N/A, not zero.
- GitHub queries: 37. That is 17 issues, 3 PR-side, and 17 code.
  Fetched rows: 5 per query at most.
- Factum queries: 58. That is 29 key terms times 2 modes.
- urlquery detail rows: 3.
- GitHub quota: no block hit this lane. Search calls left were 26
  after a mid-run check. One early failure was a query shape error,
  not a block. The issues endpoint needs an issue qualifier. The
  first run lacked it and returned 422. The rerun fixed it. That is
  not a rate limit.

## Headline

No pivot adds independent corroboration for any kept item. No pivot
kills any kept item outright.

- Rows that add: 0.
- Rows that kill: 0.
- Rows that are neutral: 66.
- Rows that are overlap or self: 13. That is 6 OVERLAP plus 7 SELF.
- Rows that are N/A for crt.sh: 12. These are items with no host.

That pattern is the finding. The kept items survive unchanged. They
do not gain weight from other surfaces.

Two notes need care:

- The MCP Toolbox wild-reach extension stays unsupported. That is
  the same state as the HN report. It is not a new kill. The
  mechanism itself is untouched by these pivots.
- The Bedrock DNS item stays killed from the broad hunt. These
  pivots do not resurrect it. No primary source was fetched here,
  so this lane adds no new verdict on it. The primary fetch stays
  open.

## Pivot summary per item

Each line gives the row total for that item, plus its adds and
kills (both zero throughout). Overlap, self, and N/A rows are
named in the text because they must not be read as support.
Row totals match pivot-results.tsv exactly.

- AMOS (Field Effect): adds 0, kills 0, rows 6. urlquery has no
  AMOS post row. GitHub samples are digests and skill docs. urlscan
  has only the vendor home page. Certs prove the host is real only.
- Zenity AgentCorruption: adds 0, kills 0, rows 6. GitHub code
  is archive mirrors of the same posts. That is overlap, not
  support. urlscan zero is window-limited. It cannot kill the
  October post.
- LifeSciences#345: adds 0, kills 0, rows 5. GitHub issues
  returns the item itself. Code matches are other repos with the
  same function name. All other surfaces are zero.
- CorbanuTerminal#876: adds 0, kills 0, rows 6. GitHub issues
  gives same-repo follow-ups, not the item. The PR-side query
  gives a probe retry item. The item itself is missed because its
  title lacks the word unshare. That is a query limit.
- guidance#1498: adds 0, kills 0, rows 5. GitHub issues returns
  the item itself. Code matches are generic validators elsewhere.
- Project-Bootstrap-Protocol#108: adds 0, kills 0, rows 5.
  GitHub code is own-repo files. Issues sample is unrelated, so
  the issues result is a sample null, not a set null.
- ms-agent#1020: adds 0, kills 0, rows 6. The PR-side query
  returns the item itself. The code sample holds an own-repo
  reader file. urlquery total is loose and its sample is unrelated.
- Wingman#278: adds 0, kills 0, rows 5. GitHub issues returns
  the item itself. Code matches are name collisions. urlquery
  total is loose and its sample is unrelated.
- hermes-agent#108236: adds 0, kills 0, rows 6. No GitHub
  sample holds the PR itself. Samples are ecosystem chatter and
  name collisions. urlquery total is loose and its sample is noise.
- OpenSkynet#77: adds 0, kills 0, rows 5. Issues is a true
  zero. Code matches are generic functions elsewhere. urlquery
  is a true zero.
- Routify sighting (HN 49535519): adds 0, kills 0, rows 6.
  urlquery repeats the known bare-host row. GitHub issues repeats
  Fleet B overlap. The third issues row is a different project
  with a similar name. Its body was not read. It must not be
  conflated with the Fleet B item. Code is guard artifacts only.
  Certs for the exact host are zero. No pivot pairs the model
  with the host outside HN and Cohere.
- MCP Toolbox (HN 49429926): adds 0, kills 0, rows 5. GitHub
  issues is CVE tracking only. Code proves the tool is real
  only. No wild exploitation appears on any surface.
- Cowork (HN 46622328): adds 0, kills 0, rows 5. GitHub issues
  shows egress allowlist bugs. That is a different mechanism
  from the key-mismatch upload. Code is word collisions. The
  mechanism itself is not tested by generic pivots. See the
  novelty note for Cowork, which is separate from pivots.
- Sheets workbook (appendix): adds 0, kills 0, rows 5. GitHub
  code is HN-derived mirrors that repeat the HN title. That is
  overlap, not support. Certs prove the vendor host is real only.
- GitLost (appendix): adds 0, kills 0, rows 5. GitHub code
  holds a downstream archive of the same PoC. That is overlap.
  Issues holds one downstream mention as a cautionary tale.
  Title level only. Not an independent incident.
- SharedRoot (lead): adds 0, kills 0, rows 5. urlquery and
  issues are true zeros. Code is word collisions. Certs prove
  the summary host exists only. The chain itself is still
  untested. The primary report read stays open.
- Bedrock DNS (lead): adds 0, kills 0, rows 5. urlquery total
  is loose and its sample is unrelated. Code holds different
  AgentCore DNS work. Title level only. Do not conflate it with
  the killed summary. The primary fetch stays open.

## Novelty verdicts

Check completeness comes first. FULL means all four checks ran:
Factum exact plus fuzzy, legacy evidence trees, tracker snapshot,
and lists. PARTIAL would name the missing check. No item here is
PARTIAL. Every item below is FULL on check completeness.

FULL does not mean new. It means the checks ran. The result column
says what the checks found.

Factum exact-match result is the same for all 17 items: NO-HIT.
No exact key term matched any Factum record.

Factum fuzzy result needs care. Fuzzy match is loose alignment.
Most fuzzy hits are word fragments, not the item. A fuzzy hit
counts as substance only when the matched value holds the full
key term and the item's own shape. Only two items meet that bar.

- AMOS: FULL. Factum exact NO-HIT. Fuzzy noise only. Lists
  NO-HIT. Tracker NO-HIT. Legacy NO-HIT. No prior record of
  this item in the four checks.
- Zenity: FULL. Factum exact NO-HIT. Fuzzy noise only. Lists
  NO-HIT. Tracker NO-HIT. Legacy NO-HIT. No prior record of
  this item in the four checks.
- LifeSciences#345: FULL. Factum exact NO-HIT. Fuzzy noise
  only. Lists NO-HIT. Tracker NO-HIT. Legacy NO-HIT. No prior
  record of this item in the four checks.
- CorbanuTerminal#876: FULL. Factum exact NO-HIT. Fuzzy holds
  one related containment note that names the sandbox tool.
  That note is not the Corbanu item. Lists NO-HIT. Tracker
  NO-HIT. Legacy NO-HIT. No prior record of this item itself.
- guidance#1498: FULL. Factum exact NO-HIT. Fuzzy noise only.
  Lists NO-HIT. Tracker has two generic uses of the word
  guidance in unrelated findings. That is not the guidance
  library item. Legacy NO-HIT. No prior record of this item.
- Project-Bootstrap-Protocol#108: FULL. Factum exact NO-HIT.
  Fuzzy noise only. Lists NO-HIT. Tracker NO-HIT. Legacy
  NO-HIT. No prior record of this item in the four checks.
- ms-agent#1020: FULL. Factum exact NO-HIT. Fuzzy holds one
  trajectory dataset note that names the model host. That
  note is not the fetch-safety PR. Lists NO-HIT. Tracker
  NO-HIT. Legacy NO-HIT. No prior record of this item itself.
- Wingman#278: FULL. Factum exact NO-HIT. Fuzzy noise only.
  Lists NO-HIT. Tracker NO-HIT. Legacy NO-HIT. No prior
  record of this item in the four checks.
- hermes-agent#108236: FULL. Factum exact NO-HIT. Fuzzy holds
  a dataset aggregation note that names a traces dataset.
  That note is not the approval-gap PR. Lists NO-HIT. Tracker
  NO-HIT. Legacy NO-HIT. No prior record of this item itself.
- OpenSkynet#77: FULL. Factum exact NO-HIT. Fuzzy noise only.
  Lists NO-HIT. Tracker NO-HIT. Legacy NO-HIT. No prior
  record of this item in the four checks.
- Routify sighting: FULL, with a prior record. Factum exact
  NO-HIT. Factum fuzzy is a substance HIT for the host: the
  Cohere enrichment lane holds the seed host and path. That
  is prior-seed overlap, not the HN witness. The HN witness
  itself has no Factum record. Lists NO-HIT. Tracker NO-HIT.
  Legacy holds the host only as a search term in broad-hunt
  scripts, not as a sighting. So the host is known. The HN
  witness is not in the four checks.
- MCP Toolbox: FULL. Factum exact NO-HIT. Fuzzy noise only.
  The CVE term has no exact hit and only fragment fuzzy hits.
  Lists NO-HIT. Tracker NO-HIT. Legacy NO-HIT. No prior
  record of this item in the four checks.
- Cowork: FULL, with a prior mechanism record. Factum exact
  NO-HIT. Factum fuzzy holds a record in the anthropic agent
  tradecraft lane that describes the same shape: workspace
  files read, provider file API called with an attacker key,
  files land in the attacker account. That is the same
  mechanism family as the HN item. It is not proof that the
  record is the same incident. The coordinator must judge
  whether that record kills novelty for the mechanism. Lists
  NO-HIT. Tracker NO-HIT. Legacy NO-HIT.
- Sheets workbook: FULL. Factum exact NO-HIT. Fuzzy holds
  generic prompt-injection theme notes. None is the Sheets
  workbook PoC. Lists NO-HIT. Tracker NO-HIT. Legacy NO-HIT.
  No prior record of this item in the four checks.
- GitLost: FULL. Factum exact NO-HIT. Fuzzy noise only. Lists
  NO-HIT. Tracker NO-HIT. Legacy NO-HIT. No prior record of
  this item in the four checks.
- SharedRoot: FULL. Factum exact NO-HIT. Fuzzy noise only.
  Lists NO-HIT. Tracker NO-HIT. Legacy NO-HIT. No prior
  record of this item in the four checks.
- Bedrock DNS: FULL. Factum exact NO-HIT. Fuzzy holds one
  theme-adjacent ransomware PoC note. That note is not a
  Bedrock DNS item. Lists NO-HIT. Tracker NO-HIT. Legacy
  NO-HIT. No prior record of this item in the four checks.

Novelty summary: 15 items have no prior record of the item
itself in the four checks. Routify has a prior host record
from the seed lane. Cowork has a prior mechanism record in
the tradecraft lane. Both are flagged, not hidden.

## Sampling limits, stated plainly

- urlquery: only 10 rows per query were fetched. A total of
  494, 465, 686, or 901 is a loose multi-term total, not a
  count of matching incidents. Samples for those totals are
  unrelated. Detail was fetched for 3 rows only.
- GitHub: only 5 rows per query were fetched. A total of
  48,384 or 318,976 is a loose token total, not a count of
  matching incidents. Comment text was not fetched. Full
  files were not read. Code fragments only were screened.
- urlscan: only the last 30 days are searchable without
  login. Every urlscan zero here is window-limited. None
  kills an older claim. Detail was never fetched.
- crt.sh: only 5 named hosts were checked. All other items
  have no host, so crt.sh cannot speak for them.
- Factum: only 5 matches per term and mode were returned,
  and only 3 sample values per result were inspected for
  substance. A deeper sample could hold a match this lane
  missed. That limit applies to every fuzzy verdict above.
- Tracker: the snapshot file is dated 2026-10-27. It is not
  a live tracker query. Findings after that snapshot are
  not covered.
- Legacy: the legacy evidence tree now holds mainly the
  Transluce API inventory plus a README. Other legacy lanes
  live in Factum or in lane raw dirs. The cross-lane raw
  grep covers the other hunt lane only.

## Failures and fixes

- GitHub issues 422 on the first run: the issues endpoint
  needs an issue qualifier. The first 17 issues queries
  failed with that error. No file was saved for them. The
  rerun added the qualifier and succeeded. No quota was lost
  to a block.
- Pivot script crash on a zero-total urlquery result: the
  script treated a null report list as a list. The fix
  treats null as empty. The run resumed from disk. No query
  was repeated for finished items.
- No GitHub rate block. No Factum lock block. No crt.sh
  502. No urlscan transport failure in the final run. The
  first manual urlscan probe was slow but returned.

## Open items

- Fetch the primary SharedRoot report and answer who issued
  the unshare call. Pivots cannot answer it.
- Fetch the primary source behind the Bedrock DNS summary,
  then judge it. Pivots cannot resurrect or re-kill it.
- Read bodies for the third routify issues row (different
  project, similar name) before any use. Title level only.
- Read bodies for the GitLost downstream mention and the
  Cowork allowlist bugs before any use. Title level only.
- urlscan detail stays login-gated. The "who scans, with
  what method" question for the seed bucket is still open.
- The Cowork prior mechanism record needs a coordinator
  call: same incident, or same mechanism in a different
  incident. This lane does not decide it.

## Evidence paths

- Raw captures and working summaries:
  data/lanes/agent-egress-deep-dive/raw/cross-surface-pivots/
- Provenance sidecars and hashes in the same dir:
  one .PROVENANCE.txt and one .sha256 per capture file,
  plus SHA256SUMS. All 82 files verify OK.
- Pivot table: reports/agent-egress-deep-dive/working/pivot-results.tsv
- This note: reports/agent-egress-deep-dive/working/cross-surface-pivots.md
- Scripts used: run_pivots.py, run_github.py,
  run_github_pr.py, run_factum.py, make_provenance.py,
  all in the raw dir above.
- Tracker snapshot used:
  data/lanes/2026-10-09-transluce-intel/raw/findings-list-20261027T115816Z.json
- Lists file used: lists/urls/urls.jsonl (533 lines)
