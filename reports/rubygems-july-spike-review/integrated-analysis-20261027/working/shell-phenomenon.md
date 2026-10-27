# Shell phenomenon — July 2026 RubyGems spike set

Lane: SHELL-PHENOMENON, integrated analysis, 2026-10-27.
Scope: the 533 names in the operator CSV, as censused 2026-10-27.
Method: read-only recomputation from the reconciled census files.
No push, no Factum write, no payload executed, no other worker's file touched.

Sources recomputed here:

- `live-check-reconciled-20261027/live-urls.json` — 533 keys.
- `live-check-reconciled-20261027/tombstone-diffend-pairs.json` — 510 keys.
- `live-check-reconciled-20261027/RECONCILIATION.md`.
- `live-check-20261027/live-check-summary.md` (first census).
- Operator CSV: `data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv`
  — 533 rows, `withdrawn` = `True` on all 533 rows (verified by recount).

## 1. Shell taxonomy: what each page type IS and IS NOT

A "shell" page is a page that renders with HTTP 200 but carries no live
package, no diff, or no code. The HTTP status is the trap. Both sites do
this. This is a soft-404 pattern: the site answers a request for a dead
name with a success page instead of a 404 page.

### RubyGems gem page (`rubygems.org/gems/<name>`)

- What it IS: proof that the RubyGems web route renders a page for that
  name. Nothing more.
- Tombstone page: a shell page for a dead gem. Observed shapes in this set:
  - "Yanked by rubygems-security-team" (example in first census:
    mini-sharp-hub).
  - "This gem is not currently hosted on RubyGems.org. Yanked versions
    of this gem may already exist." (example: test-apex-gem).
  - Removed-by-owner, name reserved (37 rows carry this page note in
    the reconciled file).
- What it IS NOT evidence of:
  - It is NOT evidence the gem is live, hosted, or downloadable.
  - It is NOT evidence any version still exists.
  - It is NOT evidence of code availability.
- Authority for index membership is the RubyGems API, not the page.
  API 200 = a gem record exists in the index. API 404 = no gem record.
  Page 200 happens in both cases, so page status must never be used
  as a live/dead signal.

### Diffend page (`my.diffend.io/gems/<name>`)

- What it IS: proof that Diffend renders a page for that name, and —
  only when diff rows are present — that Diffend once computed a diff
  between published versions of that gem.
- Stub page: a shell page that contains the marker text
  "There are no computed diffs for this gem." (observed size about
  5.6–5.7 KB, versus about 23.6 KB for an agreed-full page such as
  sportdb-parser). A stub means Diffend shows no computed diff.
- Gone page: in the reconciled labelling, a Diffend URL that redirects
  to the Diffend gems index instead of rendering a gem page.
- What a stub IS NOT evidence of:
  - It is NOT proof the gem is gone. Counter-example in this set:
    jrjackson is API-live (latest 0.3.8, 50 versions) and Diffend-stub.
  - It is NOT proof the gem never existed. It only says Diffend has
    no computed diff to show.
- What a full diff IS NOT evidence of:
  - It is NOT proof the gem is live today. A diff is a historical
    record of versions Diffend once saw. In this set all 18 full-diff
    gems happen to be API-live, and no tombstoned gem has a full diff,
    but that correlation in this set does not turn a diff into a
    live-status check. Live status still comes from the API.
  - It is NOT, by itself, proof of code availability. A diff display
    is not a gem file download.

### Four signals, kept separate

| Signal | Proves | Does not prove |
|---|---|---|
| Page renders (200) | Route + template render | Live package, hosted code, diff, download |
| API membership (200 / 404) | Gem record in / not in the index | That a named version file is downloadable; that a repo holds the code |
| Diff content (rows / stub) | Diffend computed / did not compute a diff | Current live status; code recovery |
| Code availability | Only a gem file, a versioned repo tag/commit, or a matching file tree proves it | Nothing else on this list proves it |

Rule of thumb: a 200 page is a shell until its body is read. Read the
body, then classify by content, not by status.

## 2. Recomputed counts — confirmed, with one labelling caveat

Recomputed directly from the two reconciled JSON files. The pair file's
key set equals exactly the API-404 set (510 keys, no mismatch).
Live-vs-pair Diffend content fields agree on all 510 tombstoned names.

Confirmed counts (labelled content classes):

- Total names: 533.
- RubyGems API live (200): 23. API gone (404): 510. 23 + 510 = 533.
- RubyGems page 200: 533 of 533 — including all 510 API-404 names.
  Tombstone pages: 510.
- Diffend, all 533: full 18; plain stub 510; adjudicated stub 4;
  adjudicated gone 1. Total: 18 + 510 + 4 + 1 = 533.
- Diffend among the 510 tombstoned: stub 509; gone (labelled) 1.
  509 + 1 = 510. Confirmed as labelled.
- Diffend among the 23 API-live: full 18; stub 5 (jrjackson plain stub
  plus apex-black-test-011, apex-oidc-probe, apex-blk-test-final,
  minitest-hashdiff as adjudicated stubs).
- Live on both RubyGems and Diffend: 18. Live on RubyGems only: 5.
  Live on Diffend only: 0.
- Live repo mirrors among tombstoned gems: 1 gem
  (klondikemarlen-jira-api → github.com/klondikemarlen/jira-api).
- Live OAST endpoints among tombstoned gems: 2, excluded as artifacts
  (apex-black-test-013, xss-test-gem). See section 4.
- Reconciled artifact URLs: 48 (down from 52 in the first census).
  The drop is exactly the 4 Diffend pages reclassified full → stub
  in reconciliation; the edoxen repo URL swap (old URL 301 → new URL
  github.com/edoxen/edoxen, 200) changes a URL, not the count.

Caveat 1 — the gone/stub split is a labelling distinction, not an
evidence difference. Among the 510 tombstoned names, 28 Diffend URLs
returned HTTP 302 in the reconciled file, but only 1 of the 28 carries
the "gone" label (klondikemarlen-jira-api). The other 27 carry the
"stub" label with notes such as "redirect to https://my.diffend.io/gems
(redirect-to-index)". Functionally, all 510 tombstoned Diffend URLs
show no diff content: 482 render a 200 stub page, 28 redirect.
So do NOT read "Diffend gone = 1" as "only one Diffend page is
missing". The honest statement is: no-diff-content = 510 of 510
tombstoned; labelled-gone = 1; redirect-status = 28. A future census
should define "gone" once (recommended: redirect-to-index = gone, so
gone would be 28 and 200-stub would be 482) and apply it uniformly.

Caveat 2 — tombstone page text was not verified row by row. In the
reconciled file, 259 of the 510 tombstoned rows carry an explicit
page note (128 removed/yanked notice, 94 not-hosted notice, 37
removed-reserved), and 251 carry no page note. Tombstone status for
all 510 rests on API 404 + page 200, not on a sampled text check of
every row. The first census sampled page text on 3 names in full plus
a 5-name marker check. That is enough to establish the shell pattern,
not to assign a text sub-type to every row.

Caveat 3 — CSV `withdrawn` contradicts live API status. The CSV flags
all 533 rows `withdrawn = True`, yet 23 of those rows are API-live
today. The CSV flag is therefore a dataset flag about the July window
(or about a withdrawal event in that window), NOT a current live-status
field. It must never be quoted as "this gem is removed" for any row
without the current API check. See the per-row rule in section 5.

Cross-check on source liveness (why the tombstone source count is 3):
exactly 3 tombstoned rows have source status 200 — the 1 repo mirror
plus the 2 OAST endpoints. No other tombstoned gem has a live source
URI in this census.

## 3. The single true live mirror: klondikemarlen-jira-api

Facts:

- Gem klondikemarlen-jira-api: API 404 (gone), RubyGems page 200
  (tombstone), Diffend labelled gone (302 to index). CSV: latest
  0.1.1, 2 versions in window, 2026-07-08, author Marlen Brunner,
  source_code_uri github.com/klondikemarlen/jira-api.
- Repo github.com/klondikemarlen/jira-api: source status 200.
- The same repo URL is also the declared source_code_uri of
  marlens-jira-api, which IS API-live (5 versions in the census,
  latest 0.7.0; CSV latest was 0.5.2, so the live gem has moved on
  since the July window). Same author, same summary text in the CSV
  for both gems.

What the live repo means:

- The repo host serves a repo page at that URL today.
- The repo's survival has a plain explanation that needs no survival
  of the dead gem: it is the live sibling gem's declared source repo.
  The repo lives because the sibling project lives, or at least
  because its owner has not removed it.
- It is a candidate location for the dead gem's code, and the only
  repo-mirror candidate among the 510 tombstoned gems.

What it does NOT mean:

- It is NOT proof the klondikemarlen-jira-api gem's code is
  recoverable from that repo.
- A shared declared source_uri is metadata, not a provenance chain.
  It does not show that the repo ever contained a gemspec named
  klondikemarlen-jira-api, a tag or commit for version 0.1.1, or the
  July file tree.
- Repo HEAD today is not July code. HEAD may be marlens-jira-api
  code at 0.7.0 or later, diverged from anything published under the
  klondikemarlen name.

The check that would prove recoverability:

1. Fetch (clone or list remotely) the repo's tags, branches, and
   commit history — read-only, no payload execution.
2. Find a tag or commit for klondikemarlen-jira-api version 0.1.1
   (or a commit history showing a gemspec rename from
   klondikemarlen-jira-api to marlens-jira-api, with the 0.1.1 tree
   intact at the pre-rename commit).
3. Confirm that tree contains the 0.1.1 gemspec and source files,
   and that its file contents match what the published 0.1.1 gem
   contained (file hashes, or a rebuilt gem compared against the
   published gem's recorded hashes, if any survive).
4. Until steps 2–3 pass, the correct statement is: "repo live;
   klondikemarlen code recovery unproven." If no such tag/commit
   exists, the repo does NOT recover the dead gem, even though it
   shares an upstream author and summary.

Counting note: this repo is one of the 7 unique live repo URLs in
the reconciled artifact set, shared by 2 gem rows (1 live, 1
tombstoned). Do not count it twice, and do not count it as a second
live gem — the gem is gone; only the repo page is live.

## 4. The 2 live OAST collectors (excluded as artifacts)

Facts:

- apex-black-test-013: API 404, Diffend stub, RubyGems tombstone page
  200. CSV: 0.0.1, single version, 2026-07-07, author "tester",
  summary "SSRF test with metadata URLs". Source_code_uri:
  http://d966sooa8p5umhpheccg6tnm9at8ix9kh.oast.online/source_code.
  Source status 200.
- xss-test-gem: API 404, Diffend stub, RubyGems tombstone page 200.
  CSV: latest 0.3.5, 21 versions in window, 2026-07-07, author
  "Testing Buffalo", summary "'== SSRF Callback". Source_code_uri:
  https://d96977lq1pkct8do7pn0dh1nbhzygujby.oast.online/ssrf.
  Source status 200.
- Both gems are API-404. Both endpoints are OAST (out-of-band
  application security testing) canary/callback domains, not code
  hosts. That is why reconciliation excludes them from artifacts:
  a collector answering is not a package artifact.

What "collector answering 200" proves:

- The canary subdomain still resolves and the OAST service still
  serves something at that path today.
- Nothing more. A listener being up is not a log of a hit.

What it does NOT prove:

- No callback receipt: a 200 to our census probe does not show that
  any probe target ever called back.
- No exfiltration: it does not show that any data left any target.
- No QA verdict: it does not show whether a probe succeeded, whether
  a target was vulnerable, or whether the probe was even run.
  Both gems' summaries and names say "test" / "SSRF" / "callback",
  which states intent to probe — intent is not a result.
- No timing, no source, no payload: the 200 response carries none of
  these about any historical event.

The receipt that would settle QA vs exfiltration:

- The operator's OAST session interaction log for that exact canary
  subdomain, showing an inbound request received during the probe
  window (July 2026 for these gems), with source, path, headers,
  and any captured payload — correlated to the gem's publish/probe
  time.
- The log must be filtered, not just counted: any later visitor —
  including this census's own HEAD/GET probe — can hit a live canary
  URL, so "the canary was hit at some point" is contaminated
  evidence. Only a hit in the probe window, from a plausible probe
  target (not the census prober, not a later scanner), counts as a
  callback receipt.
- Without that log, the correct statement is: "collector endpoint
  answers 200 today; no callback receipt observed; QA verdict and
  exfiltration both unproven." Do not upgrade a live listener into
  a successful SSRF, and do not downgrade it into "nothing happened"
  either — the log is the missing piece, and its absence is the
  finding.

Future-probe caution: re-polling a canary URL creates new hits in
the operator's log. Do not re-poll OAST endpoints to "check again"
without a reason, and never present a fresh poll's 200 as a fresh
callback.

## 5. Per-row rule — withdrawn vs yanked vs removed vs live

Use this rule block verbatim for every row going forward. No row gets
a status from page status, Diffend content, source status, or the CSV
`withdrawn` flag alone.

```
PER-ROW RULE (July spike set, and any re-check of it)

1. LIVE — RubyGems API returns 200 for the gem name.
   Record: api_status, versions list, latest version.
   Page 200, Diffend content, and CSV withdrawn=True do not change this.

2. GEM-REMOVED (not in index) — RubyGems API returns 404 for the gem name.
   Record as "removed / not in index", never as "yanked" on this alone.
   Its RubyGems page (200) is a tombstone page, not a live page.
   Sub-type only if page text was actually read:
     - "Yanked by rubygems-security-team" -> security-yanked tombstone
     - "not currently hosted" -> not-hosted notice
     - "removed by owner, name reserved" -> owner-removed, name reserved
     - text not read -> "tombstone, sub-type unread" (do not guess)

3. VERSION-YANKED — only within a LIVE gem (API 200): a specific version
   that is absent from the current API versions list, where an older
   record (CSV, Diffend, prior census) shows it once existed.
   A gem-level API 404 is NOT version-yanking. Never write "yanked"
   for a whole gem on an API 404 alone; write "removed" and, if the
   page text supports it, the tombstone sub-type.

4. WITHDRAWN (CSV flag) — a dataset flag, not a status.
   The CSV flags all 533 rows True, including 23 API-live rows.
   Quote it only as "CSV withdrawn=True (July-window flag)", and
   always beside the current API status. It never overrides the API.

5. DIFFEND — record content class only: full / stub / gone (redirect).
   Full, stub, and gone never change the RubyGems status in rules 1–3.
   Live + stub is possible (jrjackson). Tombstoned + full was not
   observed in this set, but if seen, it still does not revive the gem.

6. SOURCE / MIRROR — record host kind + status separately:
   code host 200 = repo page live (candidate code location only);
   OAST/collector 200 = listener live, NOT an artifact, NOT a callback;
   any source 200 never changes the gem status in rules 1–3.
   Code recovery needs the tag/commit/tree check in section 3.

7. CODE AVAILABILITY — "recoverable" requires a gem file, a matching
   repo tag/commit, or a matching file tree. A live page, a live repo
   URL, a full diff, and a live collector each fail this test alone.
```

## Open items for the integrator

- Adopt one definition of Diffend "gone" (recommended: redirect-to-index)
  and relabel the 27 redirect-but-stub rows, or keep the labelled
  counts and always quote the no-diff total (510) beside them.
- Read tombstone page text for the 251 unnoted tombstoned rows before
  assigning any text sub-type to them.
- Run the section 3 tag/commit check on github.com/klondikemarlen/jira-api
  before any claim about klondikemarlen-jira-api code recovery.
- Do not re-poll the 2 OAST endpoints; seek the operator interaction
  log instead, or record "no receipt" as the finding.
