# Review: operator-supplied RubyGems July 2026 spike CSV

## What this file is

A third-party review-dashboard export, not our own observation.
The operator supplied it on 2026-10-27. The preserved copy sits at
`data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv`
(sha256 `765ee2f24e6ec1a191c66faee030aaea8586cc4a0cdde1bee4c0668a0f0f3ce0`).
533 rows plus a header, 285 KB, 20 columns.

Grade rule used throughout: the CSV itself is UPSTREAM (third-party
dashboard claims). A row is OBSERVED-corroborated only where our own
records or a live re-fetch confirm it, cited to both. Nothing in this
report presents a dashboard claim as our finding. No dashboard claim
was upgraded on dashboard prose alone.

## 1. Structure

### Schema census

20 columns: name, latest_version, versions_in_window, first_published_utc,
last_published_utc, authors_declared, summary, homepage_uri, source_code_uri,
runtime_dependencies, withdrawn, dashboard_rule_level, dashboard_rules,
haiku_level, haiku_score, haiku_category, haiku_agent_activity,
haiku_prompt_version, haiku_reason, doc_id.

- Names: 533, all unique. Doc IDs are `rubygems:<name>@<version>` on all
  rows; the version part matches latest_version on 530 of 533, with 3
  platform-suffix mismatches in the doc ID only (java, x86_64-linux).
- Dates: first publish 2026-07-06 00:27:26 to last publish 2026-07-13
  19:35:05. Per-day first-publish counts: July 6 = 132, July 7 = 204,
  July 8 = 8, July 9 = 4, July 10 = 2, July 12 = 70, July 13 = 113.
  No July 11 first-publish rows.
- Withdrawn: True on 533 of 533. This flag describes this export. It does
  not mean gem removal: live checks found live gems among these rows
  (see section 4).
- Versions: latest_version 0.0.1 on 452 rows; 33 distinct values total.
  versions_in_window is 1 on 491 rows, multi-version on 42.
- Dependencies: the runtime_dependencies column is a count, not names.
  Zero on 509 rows, 1–22 on the rest. No dependency names exist in the
  file, so dependency hiding cannot be assessed from it.
- Fields present: summary on all 533 (224 distinct strings); homepage
  empty on 100 rows; source empty on 327 rows (61.4%).
- The same 49 rows are empty in all eight dashboard/haiku fields. No
  partial empties exist across the other seven fields; haiku_score is
  separately empty on all 464 v1 rows while their other fields are
  present. Those 49 mix ordinary gems, apex probes, and 6
  monib110 batch rows, and include all of July 8–10's scored absence:
  July 8–10 have zero scored rows. Empty must never be read as safe.

### Batch structure (OBSERVED counts, shape only)

Each large author publishes on exactly one day, in tight bursts:

| Author | Rows | Day | Tightest burst | Median gap |
|---|---|---|---|---|
| Andrey78 | 129 | July 6 | 88 in 60 min | 41 s |
| Prvaz12_mars | 113 | July 13 | 68 in 60 min | 43 s |
| tester | 100 | July 7 | 37 in 60 min | 38 s |
| monib110 | 68 | July 12 | whole batch in 60 min | 48 s |

The remaining 123 rows span 42 further author values, nearly all July 7.
Author count 46 overstates accounts: one author value is a 151-token
fuzz list on a single row, and 9 rows carry markup or template-expression
strings as the author value.

### Naming grammar (OBSERVED, shape only)

- Combinatorial group, 310 rows, zero name overlap: Andrey78 129,
  Prvaz12_mars 113, monib110 68. All are `[size]-[quality]-[container]`
  from a strict 10 x 10 x 10 word product (1,000 possible names, 310
  used). Slot 1: giga, hyper, mega, micro, mini, nano, piko, super,
  tiny, ultra. Slot 2: clean, fast, lite, max, pro, pure, quick, safe,
  sharp, smart. Slot 3: box, gem, hub, kit, lib, mod, pkg, rb, sys, tool.
- tester, 100 rows: `apex` first token on 95, `black` second on 68.
  The strict `apex-black-test-NNN` series is 11 rows inside tester, 14
  rows cross-author.
- Probe shapes: `ssrf-*` names on 19 of 20 `t` rows (18 with an 8-hex
  suffix, 1 epoch-suffixed);
  `[probe words]-[10-digit epoch]` (SR 13 of 13, Test 10 of 10).
- Summary templates: `University research based on <X>` on 309 rows
  (116 distinct X values; Andrey78 alone uses all 116; Prvaz12_mars
  112 of 113). Bare placeholders on 86 rows (`Test` 54, `testing` 19,
  `T` 9, `test` 4). Probe-descriptive summaries on 105 rows.
  The university link is self-asserted text only: the file holds no
  university name or source, and X never matches the package name.

## 2. What the file claims

### Dashboard rules (UPSTREAM labels)

Rule tokens fired, by count: combinatorial names 372, shared text 185,
owner burst 158, placeholder author 122, numbered name 115, template
batch 100, placeholder text 92, name series 66, probe name 59, oob url
48, short author 43, test name 41, markup 12, placeholder link 8,
random name 1. 73 distinct rule strings, plus 49 empty rows.
Dashboard levels: medium 193, critical 151, low 121, high 19, empty 49.

### Haiku judgments (UPSTREAM labels)

Levels: high 385, critical 80, medium 15, low 4, empty 49.
Categories: mass_generated 305, registry_test_or_probe 178, unclear 1
(giga-pure-tool, monib110, July 12), empty 49.
Agent activity: possible 461, likely 18, no_sign 5, empty 49.
Prompt versions: pkg-review-1 on 464 rows, pkg-review-2 on 20 rows,
empty on 49. Haiku score exists on 20 rows only (the pkg-review-2
rows), values 42–92. The other 513 rows carry levels and labels with
no score behind them.

### Reason rhetoric (UPSTREAM prose, quoted verbatim)

484 non-empty reasons, all 484 distinct. Claim classes: batch /
combinatorial 272, probe / test 126, automated with no agent word 46,
agent-word 38, other 2. Keyword hits across reasons: combinatorial 329,
batch 266, MFA 289, zero-deps 311, unrelated summary 162, SSRF 92,
deception 12, lookalike 10 (mostly negations).

Load-bearing quotes:

Mass generation:
> "Part of 129 packages published together with combinatorial names
> (word-list pattern like ultra-fast-box, mega-max-tool). Single author
> Andrey78, zero deps, unrelated summary mentioning rack-mini-profiler,
> source repo name matches but batch is strong signal."

Automated, no agent word:
> "Part of a 129-package batch of combinatorial names (word-list style
> like mini-max-pkg) under a single declared author with no MFA, zero
> dependencies, and a summary mismatched to the name, suggesting bulk
> automated publishing."

Registry probe:
> "14 numbered 'apex-black-test' packages published together, authors
> 'Testing', no publisher handle, no MFA. Links point to localhost
> admin and cloud metadata endpoints, and the summary states an SSRF
> test, so this probes the registry and link-following."

Agent-word, hedging or denying (the majority of the 38):
> "Name apex-black-test-017 is numbered within a batch of about 100
> packages published together under author 'tester' with null publisher
> handle, placeholder summary 'Test', no links, and zero dependencies.
> Looks like registry probing; no agent metadata."
> "Part of a batch of 71 numbered 'apex-black-test' packages with no
> links, no dependencies, and no publisher handle. Summary and author
> fields hold XSS-style markup, which looks like a probe of the
> registry. Not clearly agent-generated."

Only 38 of 484 non-empty reasons use the word "agent" at all, all 38 on
probe rows, zero on mass-generated rows. 30 reasons use a `no ... agent`
phrasing. One reason says "batch looks scripted, not an agent" while its
label still reads "possible". Only 7 of the 18 "likely" rows contain the
word "agent". No reason asserts plainly that an agent did this.

Reason batch numbers disagree with file counts in places: monib110
reasons say 60 against 68 rows; tester reasons say 101 and 71 against
100 rows; one Andrey78 reason says 134 against 129 rows. Five reasons
are cut off mid-sentence in the CSV itself and must not be completed
when quoted.

The file does not claim: a verified university link, verified
assessment authorization, any package's code behavior, any author's
human / bot / agent identity as fact, or anything about the 49 blank
rows. Two self-asserted assessment summaries (authorized assessment /
proof-of-impact) and one scope-escalated-key-push claim are unverified
in the file and treated as self-asserted only.

## 3. What is independently true

### Payload inventory (OBSERVED in the CSV's own strings)

82 rows carry an out-of-band, IP, XSS, or SSTI string in the
name, summary, homepage, or source columns (author field excluded).
Counting the author field too, the total is 84 rows. The other 451 rows
carry no payload string in the scanned columns; 2 further rows carry a
payload string only in the author field.

- OAST callbacks: 29 rows, 6 distinct OAST hosts, mostly `/ssrf_linkback`
  paths. Webhook.site: 19 rows by substring (18 by homepage host),
  9 distinct UUID paths. OAST and webhook row sets do not overlap;
  combined out-of-band rows = 48.
- SSRF / internal targets: 24 homepage rows, including
  169.254.169.254, metadata.aws.internal, metadata.google.internal,
  instance-data.us-west-2.compute.internal, 127.0.0.1, 10.0.0.1, and two
  public IPs. 12 homepage / source rows use plain http.
- XSS in summary: 10 rows. SSTI in summary: 4 rows
  (`{{7*7}}` / `${7*7}` / ERB shapes). 9 further rows carry a script /
  image / template payload in the author field, including the file's
  only `document.cookie` hit (author field only); 7 of those 9 rows are
  already inside the 82, and 2 are author-only.
- Name-only discipline: of 26 `ssrf-*` / `webhook-*` names, only 12 carry
  an out-of-band or IP homepage; the other 14 have empty or
  rubygems.org-internal homepages. Name shapes were not counted as
  payloads.
- Explicit nones across all 533 rows: go-import tags 0, import paths 0,
  VCS values 0, jina laundering 0, UK council hosts 0, cloud buckets 0,
  curl / wget / eval / os.system / subprocess 0, genuine base64 blobs 0.
- Credential-shaped values: 5–7 cells flagged by keyword patterns
  depending on scan method (`token` / `api key` wording in summaries or
  reasons). Count only. No key-shaped values found, and no value is
  copied into any report. Full bytes stay in the preserved CSV only.

Mechanism check against our known waves:

| Mechanism | Verdict |
|---|---|
| May 2026 go-import to UK council sites via jina, VCS hg/fossil/git/bzr/svn | NO MATCH, 0 on every element |
| June 2026 plain link-posting to a target site | NO MATCH as a distinct mechanism |
| July-7 XSS/SSTI in registry metadata | MATCH (10 XSS + 4 SSTI summaries, 9 payload authors) |
| July-7-adjacent SSRF/OOB in metadata links | MATCH, same family, SSRF/OOB flavour |

Coverage limit: the CSV holds registry metadata strings only — no gem
code, gemspec bytes, or served homepage HTML. A go-import tag lives in
served HTML, so zero here rules it out in this file, not in any gem page
behind these rows. String presence is not execution: whether any XSS
fired or any callback was received is not in this file and was not
checked here.

### Corpus overlap (OBSERVED, recomputed)

203 of 533 names were already known to us; 330 are NEW.

| Source | Known |
|---|---|
| v2 export (3,036 rows) | 203 |
| Lane JSONLs (events.jsonl only; 0 in graph-nodes, iocs-2026-09-27, june18-wayback, ioc-hits) | 203 |
| Notes (docs/notes/gem-*.md, 54 files) | 18, all inside the 203 |
| Any of v2 / lane / notes | 203 |

The v2 set, the events.jsonl set, and the raw JFrog CSV set are exactly
the same 203 names (verified by set equality, `gem.name` extraction on
campaign_specimen records). Overlap therefore
corroborates the JFrog list, not independent lane observation, except
where notes add detail.

Per v2 wave: null-wave JFrog-list rows 192, July-7 11, May-11 0,
May-12 0, June-18 0, March-7 0, other-probe-family 0.
Per v2 grade: overlap 165, third-party-list 38.
Per author: Andrey78 0 of 129 known, Prvaz12_mars 0 of 113, tester 100
of 100, monib110 0 of 68, all other author strings 103 of 123.
Per first-publish date: July 6 = 0 of 132 known, July 7 = 203 of 204,
July 8–13 = 0 known.

The three big batches are entirely new to us. The strings Andrey78,
Prvaz12_mars, and monib110 appear nowhere in the 5 lane files or any
gem note. Factum read-only sampling (30 names) agrees: all 21 sampled
new names not_found; 8 of 9 sampled known names found; xss-test-gem a
near-match candidate but confirmed known via v2, lane, and notes.
Exhaustive Factum matching was not run; the exhaustive local sources
already classify all 533 names.

NEW names (330): Andrey78 129, Prvaz12_mars 113, monib110 68, plus 20
small-author names. The 20 small names carry blank dashboard/haiku
fields and live-registry evidence pointing to ordinary gems. NEW does
not equal campaign. Of the 330, 303 carry mass_generated haiku labels
and 26 have blank haiku fields (mostly the small names).

### July-7 relation: partial overlap, disjoint authors except the probe batch

Our v2 July-7 wave has 24 rows; 11 are in the CSV, 13 are not. The 11
shared names are the July-7 probe / test batch (7 graded campaign + 4
window-test gems). The 13 absent rows are all window-test gems. The
other 192 CSV July-7 rows are v2 wave-null JFrog rows, dominated by
author `tester`. The single CSV July-7 row new to us is jrjackson
(author Guy Boertje) — a real, live gem, not a probe name.

### Live spot-checks (OBSERVED-live, read-only GET, 2026-10-27)

RubyGems API x20, Diffend x10, plus versions-list fetches for the 6
live names. No fetch failed for egress or timeout; every non-200 is a
genuine registry 404. Full bytes saved under
`data/lanes/rubygems-july-spike-review/raw/corroboration/`.

- Mass-batch names sampled (Andrey78, Prvaz12_mars, monib110 samples):
  RubyGems 404 gone; Diffend 200 stub, "no computed diffs". The sampled
  batch names are gone from the registry.
- Overlap probe names (test-apex-gem, xss-test-gem, test-ssti-0,
  apex-black-test-012): RubyGems 404 gone; Diffend returned a generic
  index page for two of them — inconclusive, not absence.
- Still live: apex-blk-test-final, test_gem_kangaroo (overlap, July-7);
  jrjackson, shirobai, sportdb-parser, edoxen (small new names, real
  download counts, real diffs including October 2026 releases).
- Correction to the CSV flag: for live names only individual versions
  were yanked (apex-blk-test-final's CSV latest 0.0.5 is absent from
  the live versions list while 0.0.1 survives).

## 4. Verdict changes: none forced

- **July-7 verdict: NO CHANGE.** The file's July-7 set is 204 rows but
  adds no new observation type — no code, live state, callback
  receipts, or actor evidence. A wider candidate pool is a scoping
  question, not a verdict change.
- **GemStuffer / JFrog picture: NO CHANGE.** GemStuffer, JFrog,
  stuffer, typosquat, and backdoor occur 0 times across summaries,
  reasons, and rules; "malicious" occurs once; lookalike / deception
  language in inspected v2 rows appears only as negation. The file is
  silent on that picture.
- **Andrey78 batch verdict: mass-generated shape only, NO agent
  evidence, NO severity verdict.** The file corroborates batch shape,
  count, and date, but its own severity labels conflict on that batch
  (dashboard low, Haiku high on v1 rows, Haiku medium on sampled v2
  rows) and add no agent evidence. The batch survives as a
  mass-generated shape, not as agent activity.

## 5. Dashboard method assessment: inventory, not evidence

The file works as a shape-sorted inventory, not as evidence of
severity, agent activity, or impact.

- **Dashboard level is exactly a rule count, deterministic.** Low =
  exactly 1 rule (121 of 121), medium = 2 (193 of 193), high = 3 (19 of
  19), critical = 4–8 (151 of 151). The same rule string never yields
  two dashboard levels. "Critical" therefore means "four tokens fired":
  a row can be dashboard critical on numbered name + placeholder text
  + short author + test name while Haiku rates it low.
- **Dashboard and Haiku agree on only 88 of 484 scored rows (18.2%).**
  Dashboard low maps to Haiku high on 111 of 121; dashboard medium to
  Haiku high on 188 of 193; dashboard critical to Haiku critical on
  only 73 of 151.
- **Haiku score exists only on the 20 pkg-review-2 rows** (medium
  42–45, high 62–72, critical 88–92, monotonic within n=20, bands 46–61
  and 73–87 empty). No score threshold is testable, and any score claim
  for a v1 row is unsupported.
- **Prompt version 2 changes calibration, not just scores.** v1: high
  381 of 464 (82.1%), critical 15.9%, medium 1.1%, low 0.9%. v2: medium
  50%, critical 30%, high 20%. On matched shapes it is inconsistent:
  combinatorial-only rows are Haiku high on 111 v1 rows but medium on
  all 5 v2 rows; combinatorial+shared rows are high on 178 v1 rows but
  medium on 4 of 5 v2 rows. Version 2 cannot supersede version 1 until
  all 464 v1 rows are re-run.
- **Identical shapes, different Haiku levels.** 377 of 484 scored rows
  sit in a rule-string group whose Haiku level is not unique. Cleanest
  within-v1 cases (tester, 0.0.1, 0 deps, summary "Test"):
  apex-black-ipv6-001 critical vs -002 high; apex-black-race-000 / 002
  / 003 / 004 critical vs -001 high; apex-black-probe-000 / 002 / 003
  critical vs -001 high. Category flips too (apex-black-fuzz-006r /
  007r labelled mass_generated amid registry_test_or_probe siblings).
- **Reason prose asserts missing columns.** 355 Haiku reasons assert
  "no MFA" / "MFA off" / "no publisher" / "null publisher", but the
  CSV has no MFA or publisher column. All such assertions are UPSTREAM
  and unverifiable here.
- **False-positive shapes.** Every rule also fits benign work:
  combinatorial names + university-template summaries (coursework /
  scaffold); shared text (course template); name series, numbered
  names, template batches (test iterations); owner bursts (class
  deadline / CI run); placeholder author and text (literal test gems);
  probe names (self-declared QA); out-of-band URLs (QA callback checks
  — the file holds only the homepage string, no callback receipt, so QA
  vs exfiltration is indistinguishable); short authors (handle length
  is not intent); markup strings (XSS test inputs — no rendering,
  execution, or victim in the file).
- **Agent activity: UNPROVEN on this file.** All 18 "likely" rows are
  July 7, all registry_test_or_probe, none from the three
  mass-generated batches — "likely" tracks probe-cluster membership,
  not an agent marker. 16 of 18 are pkg-review-1 (no score); 9 of 18
  reasons contain no agent or automation word; 3 hedge with "plausible"
  wording, 2 of them with the exact phrase "plausible but not certain"; 7 have empty homepage and empty
  source. The strongest-looking rows still fail: a probe's publication
  proves a probe was published, not that an agent published it, and one
  "likely" reason claims localhost-admin links while the file's columns
  show a metadata address, not a localhost-admin address. The 5
  "no_sign" rows are the same probe shape. All 18 are downgraded to
  UPSTREAM probe-batch labels. No model, harness, tool call, prompt, gem
  code, download, victim, or callback receipt exists anywhere in the
  file.

Surviving findings, graded: four bulk clusters with counts and dates
(OBSERVED); combinatorial grammar + university-template + July-7 probe
wording (OBSERVED, shape only, not actor); 509 of 533 zero deps and 452
of 533 version 0.0.1 (OBSERVED, counts only); all 533 withdrawn
(OBSERVED, describes this export, not live registry or per-row reason);
July-7 tester-family rows as self-described registry probes (OBSERVED
as self-description; INFERENCE, strong, that probing was intent;
UNPROVEN that any probe succeeded or any agent ran it); dashboard
tokens as recorded (OBSERVED as assignment; meaning UPSTREAM); Haiku
categories as broad shape sort (UPSTREAM, weakened by flips); v2 score
ordering within its 20 rows only (OBSERVED). Nothing survives as agent
attribution, severity grading, or impact.

## 6. Open questions

1. What is the code behavior of the 82 payload-string rows? The CSV
   holds metadata strings only; gem bytes were never fetched here.
2. Did any OAST / webhook callback ever arrive? The file holds homepage
   strings, no receipts. That check decides QA vs exfiltration.
3. Why do 49 rows lack all scoring, including 6 monib110 batch rows?
   Is that a dashboard coverage gap or a different source cut?
4. Should the 464 pkg-review-1 rows be re-run under pkg-review-2 before
   any severity claim is reused? The calibration shift says yes.
5. What are the 330 new names to us — three mass batches plus 20
   ordinary-looking gems? The batches are new shapes, not yet new
   verdicts. Do they join the corpus as a July mass-generation lane, or
   stay as a dashboard-only pointer until code is fetched?
6. What explains the 13 v2 July-7 window-test gems absent from the CSV?
   Different source cut, or a narrower dashboard window?
7. The CSV's withdrawn flag vs live registry state needs a per-row
   rule: version-yanked vs gem-removed must be stated, not assumed.
