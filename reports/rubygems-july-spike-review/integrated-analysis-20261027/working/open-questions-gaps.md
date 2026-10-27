# Open questions + gaps — RubyGems July 2026 spike set

Lane: OPEN-QUESTIONS + GAPS, integrated analysis, 2026-10-27.
Scope note: this lane RECOMMENDS only. Corpus-ingest decisions belong to
the operator. Nothing here pushes, writes to Factum, or changes another
worker's files.

Terms, defined on first use:

- Corpus: the set of records kept for study.
- Lane: one work set inside the corpus.
- Dashboard: the third-party review tool that made the CSV. Its labels
  are UPSTREAM claims, not our findings.
- Haiku: the model judge that gave levels in the CSV. pkg-review-1 and
  pkg-review-2 are two prompt versions of that judge.
- OAST: out-of-band testing. A callback service records a hit when a
  link is fetched. The CSV holds only the link string, not the hit log.
- Webhook: a URL that records a hit when visited. Same limit as OAST.
- Receipt: a log entry that proves a callback arrived, with time,
  source, path token, and payload.
- Yanked: one version removed while the gem still lives.
- Tombstoned: the gem is gone from the live registry (API 404).
- Shape-only: a claim about name, timing, and metadata shape. It is
  not a claim about code behavior, severity, or actor.

Base numbers used here, from REPORT.md and the live census:

- CSV: 533 rows. 330 names are NEW to us. 203 were already known.
- New names: Andrey78 129, Prvaz12_mars 113, monib110 68, plus 20
  small-author names. The three big batches form one combinatorial
  grammar: 310 rows, zero name overlap, 10 x 10 x 10 word product.
- Scored rows: 464 under pkg-review-1, 20 under pkg-review-2, 49 with
  no scoring at all.
- Payload-string rows: 82. Out-of-band rows: 48 combined (29 OAST,
  19 webhook by substring, no overlap).
- Live census: 23 API-live, 510 gone. 48 reconciled artifact URLs.
  327 CSV rows have no source URI. Among tombstoned gems, 66 rows have
  a source URI that the census did not check. That 66 includes one
  internal metadata-address URI deliberately not fetched.
- v2 July-7 wave: 24 rows. 11 are in the CSV. 13 are absent. All 13
  absent rows are window-test gems.

## 1. Recommendations on the four open questions

### (a) Do the 330 new names join the corpus as a July mass-generation lane?

RECOMMEND — split the set. Operator decides.

- Admit the 310 combinatorial batch rows now, as a SHAPE-ONLY lane.
  Grade it shape-only, not agent activity and not severity.
- Keep the 20 small-author names OUT of that lane. Keep them as
  dashboard-only pointers for now.

Reasons:

- The shape evidence is strong and needs no code. Three authors, one
  day each, tight bursts (median gaps 41–48 seconds), one strict
  grammar, zero dependencies on most rows, and university-template
  summaries. None of the three author strings appears in our prior
  lane files or gem notes.
- "Wait for gem code" is not a usable gate for the batch. The sampled
  batch names are already gone from the registry, and Diffend holds
  stubs with no computed diffs. Waiting would block the lane forever.
- The 20 small names do not share the shape. The file itself notes
  they point to ordinary gems, and live checks found real gems among
  them. Putting them in a mass-generation lane would pollute the lane.
- NEW does not equal campaign. The lane label must say "mass-generated
  shape" and must not say "agent-made" or "malicious".

Cost and risk:

- Cost is low. This is metadata-only ingest. No code fetch is needed
  for a shape claim.
- Risk is overclaim, not cost. If the lane is labeled beyond shape,
  it will be read as agent or severity evidence. Mitigation: label
  every lane record shape-only, and keep the code gap open beside it.
- Risk of the other choice: leaving all 330 as pointers only would
  hide a clean, dated, counted batch shape from the corpus for no
  gain, since code recovery is already unlikely.

What the live census adds:

- The census confirms the batch window is closed for sampled names:
  registry 404, Diffend stub only. That supports shape-only ingest
  now rather than waiting for code.
- The census split (23 live, 510 gone) confirms most of the set is
  historical metadata, not live behavior. A shape lane is the honest
  form for historical metadata.
- The census also supports splitting out the 20: live, real gems sit
  in that small set, not in the batch shape.

### (b) Re-run the 464 pkg-review-1 rows under pkg-review-2 before reusing any severity claim?

RECOMMEND — yes, re-run before any severity reuse. Operator decides.

Reasons:

- Calibration shifted, not just scores. Version 1: high 82.1%,
  medium 1.1%. Version 2: high 20%, medium 50%, critical 30%.
  That is a different judge, not a refined one.
- Identical shapes flip across versions. Combinatorial-only rows are
  Haiku high on 111 version-1 rows but medium on all 5 version-2
  rows. Combinatorial-plus-shared rows are high on 178 version-1
  rows but medium on 4 of 5 version-2 rows.
- Version 1 is not even self-consistent. Identical tester shapes get
  different version-1 levels (for example, within one numbered series,
  some rows critical and some high). A re-run cannot fix that alone,
  but reuse without a re-run would freeze the inflated version-1
  distribution as if it were a finding.
- No version-1 row has a score. Any score claim for a version-1 row
  is unsupported today. Only the 20 version-2 rows have scores, and
  their score bands are empty in two ranges (46–61, 73–87), so no
  threshold is testable yet.

Cost and risk:

- Cost is moderate: model re-review of 464 rows of metadata. No live
  fetch and no code fetch is needed for this step.
- Risk of re-running: version 2 may also prove unstable on a larger
  set. Mitigation: keep version-1 labels beside version-2 labels.
  Never overwrite version 1 silently. Report both, and check
  consistency on matched shapes before any severity claim is reused.
- Risk of NOT re-running: high. Reused version-1 "high" labels would
  overstate severity by roughly four times the version-2 high rate,
  on a judge that already disagrees with the dashboard on 81.8% of
  scored rows.
- Scope limit: a re-run fixes calibration only. It does not fix the
  missing code gap or the missing callback receipts. Severity after
  a re-run is still metadata severity, not impact.

What the live census adds:

- Nothing on calibration. Live or gone status is independent of a
  Haiku level. The census does not validate any score.
- The census does set the frame: most rows are tombstoned, so the
  re-run reviews historical metadata, not live behavior. That frame
  must stay attached to any re-run result.

What may still be reused without a re-run:

- Broad shape sort only (mass_generated vs registry_test_or_probe
  as a rough sort), labeled UPSTREAM and weakened by known flips.
  Levels and scores may not be reused until the re-run lands.

### (c) Did any OAST / webhook callback ever arrive?

RECOMMEND — treat as UNRESOLVED. Claim neither QA nor exfiltration. Operator decides.

Reasons:

- The file holds homepage strings only. A string proves a link was
  published. It does not prove the link was fetched, by whom, or
  with what payload.
- QA vs exfiltration is therefore indistinguishable on this file.
  A QA self-test and a real exfiltration hit can carry the same
  homepage string. Only a receipt separates them.
- Absence of a public receipt is not proof that no callback arrived.
  OAST and webhook inboxes are private to the token holder. We cannot
  see them from public data.

What receipt would settle it:

- One receipt per distinct callback endpoint token, not one receipt
  for the whole set. The set has 6 distinct OAST hosts and 9 distinct
  webhook UUID paths. Each token needs its own log entry.
- Each receipt must show: time of hit, source address or host, path
  token hit, and headers or body if any. Time and source matter most:
  a single self-test hit from a QA source reads differently from
  repeated hits from varied external sources.
- Even a receipt does not prove exfiltration content by itself. A hit
  with no payload proves a fetch, not data theft. A hit with payload
  would need separate review. A receipt also does not prove who ran
  the fetch: registry link-following, a crawler, a QA harness, and a
  victim browser can all produce a hit.

Who holds it:

- The OAST service operator holds OAST hit logs for its hosts.
- The webhook inbox owner holds webhook hit logs for each UUID path.
  That owner is presumably the publisher or QA author. We do not
  know the owner from the CSV, and this lane does not pursue owner
  identity.
- The registry operator would hold link-following logs only if the
  registry itself followed the links. No such log is in the file,
  and no public registry log of this kind is cited here.

Cost and risk:

- Cost of a public-data answer: low, and the answer is already known:
  no receipt is in public reach. Further public searching will not
  close this.
- Cost of a private receipt: high to unobtainable. It needs the token
  holder or the service operator, and there is no authorized contact
  path in this task.
- Risk of probing: DO NOT fetch live OAST or webhook homepage URLs
  to "test" them. Our own fetch would create a callback and pollute
  the very log that would settle the question. This is the main
  operational risk in this question.
- Risk of claiming either side: claiming QA without a receipt
  understates a possible exfiltration channel; claiming exfiltration
  without a receipt overstates a possible self-test. Both errors
  change the verdict. The honest grade is UNRESOLVED.

What the live census adds:

- Zero on receipts. The census reconciled 48 artifact URLs. Artifact
  availability is not callback receipt. The two "48" counts (48
  out-of-band rows, 48 artifact URLs) are different sets and must not
  be conflated.
- The census does add a restraint model: one internal
  metadata-address URI was deliberately not fetched. That same
  restraint applies here: do not fetch callback endpoints, and do
  not fetch internal metadata addresses, to check for a hit.

### (d) What explains the 13 v2 July-7 window-test gems absent from the CSV?

RECOMMEND — treat as an open scope question, not as a finding. Operator decides.

Candidate explanations, in test order:

1. Different source cut. The CSV export may be built from a list
   (JFrog list plus rule-firing rows) while the v2 window-test set
   is built from a time-window scan regardless of rule fire. A
   window-test gem that fired no dashboard rule would then be absent
   from the CSV entirely, not merely unscored.
2. Narrower dashboard window. The dashboard window may end earlier,
   start later, or cut at a different hour boundary than the v2
   window. If the 13 cluster at a window edge, the edge explains them.
3. Author or shape filter. If the 13 share an author or name shape
   outside the CSV's main July-7 probe batch, a filter on batch or
   probe shape could exclude them while keeping the tester batch.
4. Export snapshot timing. The CSV may freeze an earlier export
   state than v2. This is weaker than the first three, because the
   CSV already holds 204 July-7 rows, so July 7 is not missing in
   general — only this subset is missing.

What check would confirm the explanation:

- Build one local comparison table for the 13 absent rows, the 11
  shared July-7 rows, and the 192 wave-null JFrog July-7 rows. Use
  only fields already held: name, author, first-published time,
  v2 grade and wave, and any dashboard-rule or JFrog-list membership.
  No live fetch is needed for this step.
- Test each candidate against that table: timestamp distribution
  against the CSV window edges; rule-fire presence for the 13;
  author and shape distribution for the 13 versus the shared 11;
  JFrog-list membership for the 13.
- The explanation is confirmed only if one candidate fits all 13
  and the others fail. A partial fit (for example, edge timing fits
  some but not all) means the explanation is mixed or still open.
- Until that table is built, do NOT assume the 13 are unimportant,
  and do NOT backfill them into CSV counts. Their absence is a scope
  signal, not a verdict about them.

Cost and risk:

- Cost is low. The check is local comparison work.
- Risk of assuming an explanation now: high for scope. If the cut
  was rule-based, then the CSV is a rule-filtered view, and any
  "July-7 total" drawn from the CSV alone understates the window.
  If the cut was time-based, the understatement is bounded to the
  edge. The check decides which scope error applies.

What the live census adds:

- As scoped, nothing. The census covers CSV rows. The 13 are outside
  the CSV, so they are outside the census as described. The census
  therefore neither explains nor closes this gap.
- A cheap extension exists: check live existence of the 13 by
  registry API name lookup only (no payload fetch, no callback
  endpoint fetch). That would add live or gone status for the 13,
  but existence alone would NOT explain why the dashboard omitted
  them. Do not present an existence check as an explanation check.

## 2. Remaining gaps: what each BLOCKS and what would CLOSE it

| Gap | What it BLOCKS | What would CLOSE it |
|---|---|---|
| Gem code for yanked gems never fetched. Diffend stubs hold no code. Gems are gone from the index. | Code behavior for the 82 payload-string rows, and for the batch rows. Any backdoor, SSRF-execution, XSS-firing, or agent-behavior claim. Any upgrade from shape to behavior or impact. Severity stays metadata-only. | Recovery of actual gem bytes from a preserved mirror, with a hash match to the registry version — or a documented exhaustive negative: every plausible mirror checked, no bytes found, code marked UNRECOVERABLE, and all claims permanently capped at metadata-only. A Diffend stub alone does not close this. |
| 66 tombstoned source URIs unchecked in the census. Source URI present, not checked. Includes one internal metadata-address URI deliberately not fetched. | Source-repo corroboration for those 66 rows: whether the repo exists, matches the gem name, and holds code or behavior. This is the second path to code where gem bytes are gone. | Safe read-only HEAD or GET per URI, recording status and repo existence, for the 65 checkable URIs. Exclude from fetching: the internal metadata-address URI (stays unchecked by design, with reason recorded), and any URI that is itself an OAST or webhook callback endpoint (fetching it would fabricate a hit). The gap closes at 65 checked plus 1 explicitly excluded, not at 66 fetched. |
| 327 names with no source URI at all (61.4% of the CSV). | Any source-repo verification for most of the set. Haiku claims that a "source repo name matches" cannot be checked for these rows. Code cannot be fetched through a source repo even if a gem returned. | Registry API metadata re-check for the live subset (23 live gems may still carry a source URI). For tombstoned gems, the same re-check documents absence. The close condition is a documented re-check plus a marked remainder: source-absent. Source absence is itself a shape signal. Never invent a URI to fill this gap. |
| 49 unscored rows (dashboard coverage hole). Includes 6 monib110 batch rows. July 8–10 have zero scored rows. | Any aggregate severity or category claim over all 533 rows. The denominator is broken: scored n is 484, not 533. Date-trend claims break for July 8–10. Batch completeness breaks for monib110. | A dashboard re-export with scoring for the 49, or a same-prompt re-review of the 49 under pkg-review-2 with an explicit coverage note. Until then, report scored (484) and unscored (49) separately. Never impute a level for an unscored row. Never read empty as safe. |
| CSV withdrawn flag vs live state: no per-row rule yet. Flag is True on all 533 rows, but live gems exist among them. | Any per-row "removed", "yanked", or "gone" claim. The flag as written overstates removal and hides the version-level truth. | A stated per-row rule, applied to all 533 rows: gem-removed (API 404 for all versions); version-yanked (CSV latest version absent, other versions live); gem-live (CSV latest version live). The census live or gone split (23 live, 510 gone) is the starting point, but the 23 live rows need version-level checks, not gem-level only. Example already observed: one live gem's CSV latest version is absent while an older version survives. The flag must be described in all downstream text as an export descriptor, not as registry state. |

## 3. Ranked gaps: what most changes the verdict if closed

Rank order is by verdict change if closed, not by ease of closing.

1. Gem code for yanked gems — it alone can prove or kill behavior,
   backdoor, and impact claims that are today metadata-only.
2. 66 unchecked tombstoned source URIs — they are the remaining path
   to code or behavior where gem bytes are gone.
3. Withdrawn flag vs live state, per-row rule — it corrects a false
   universal removal claim across all 533 rows and fixes every
   downstream "gone" count.
4. 49 unscored rows — closing it fixes the severity denominator and
   the July 8–10 and monib110 completeness holes, but not behavior.
5. 327 names with no source URI — closing it mostly confirms absence
   for tombstoned gems, since no live record remains to supply a URI.

Note on the callback receipt gap (question (c) above): a genuine
receipt would rank near the top on verdict change, since it alone
separates QA from exfiltration. It is not ranked with the five gaps
above because it is not closable from public data: the receipt sits
in private inboxes held by others, and probing the endpoints would
pollute the evidence. Rank it as high-impact but unclosable here,
not as next work.
