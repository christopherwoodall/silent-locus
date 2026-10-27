# LINGUIST lane — rubygems July 2026 spike file

Source file: `data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv`
SHA-256: `765ee2f24e6ec1a191c66faee030aaea8586cc4a0cdde1bee4c0668a0f0f3ce0`
Rows checked: 533. All rows say `withdrawn=True`.
Date span in file: 2026-07-06 00:27:26 to 2026-07-13 19:35:05.
The CSV was read only. It was not changed.
Counts below were recomputed from the CSV. No credential values are copied here.
A scan for secret-shaped patterns found zero `sk-`, `ghp_`, `github_pat_`, or `xox` strings.
Word hits for `api`, `key`, and `token` are prose words in summaries and reasons, not values, so they are counted only and not quoted.

## 0. Headline for the adversarial lane

The file does NOT speak with one voice about agents.

- The label column says `haiku_agent_activity=possible` for 461 rows and `likely` for 18 rows.
- The reason prose behind those labels almost never asserts agent involvement.
- All 38 reasons that use the word `agent` are in the probe/test group, and most of them deny, hedge, or limit the agent claim.
- No reason for the 310-row combinatorial group uses the word `agent` at all.
- The strongest reason wording is `automation`, `scripted`, and `bulk`, not `agent`.
- So: the file's agent-activity labels run ahead of its own reason text. Treat `possible`/`likely` as labels to test, not as findings.

## 1. Naming grammar, per author batch

### 1a. The combinatorial group — Andrey78, Prvaz12_mars, monib110 (310 rows, zero name overlap)

All three authors use the exact same three-slot template, with a hyphen separator:

`[size word] - [quality word] - [container word]`

Slot 1 (10 words, same set in all three): giga, hyper, mega, micro, mini, nano, piko, super, tiny, ultra.
Slot 2 (10 words, same set in all three): clean, fast, lite, max, pro, pure, quick, safe, sharp, smart.
Slot 3 (10 words, same set in all three): box, gem, hub, kit, lib, mod, pkg, rb, sys, tool.

That is 10 x 10 x 10 = 1,000 possible names. The file uses 310 of them, with no name repeated across authors and no name repeated inside the file at all (0 duplicate names in 533 rows).

- Andrey78: 129 rows, all 3-token hyphen names. Example names: mini-sharp-hub, ultra-fast-box, mini-fast-rb, mega-max-tool, super-max-kit.
- Prvaz12_mars: 113 rows, all 3-token hyphen names. Example names: piko-max-gem, piko-lite-mod, mini-sharp-lib, hyper-lite-tool, ultra-fast-hub.
- monib110: 68 rows, all 3-token hyphen names. Example names: micro-pure-box, piko-fast-kit, ultra-clean-mod, hyper-smart-lib, hyper-clean-kit.

Slot counts are near-uniform, not skewed to one word. For Andrey78, slot 1 ranges from 8 (tiny, hyper) to 18 (nano); slot 3 ranges from 9 (rb, lib) to 21 (tool). The same flat shape holds for the other two authors. This is a word-list product, not a natural vocabulary curve.

Single-day bursts: Andrey78 all on 2026-07-06, monib110 all on 2026-07-12, Prvaz12_mars all on 2026-07-13. The shared word lists plus single-day bursts are the file's strongest same-template signal, even though the author strings differ.

Haiku split for this group: mass_generated 303 (Andrey78 129, Prvaz12_mars 113, monib110 61), unclear 1 (monib110), blank 6 (monib110). The 6 blank monib110 rows have no dashboard rules either, so the file makes no Haiku or dashboard claim about them.

### 1b. tester (100 rows) — the apex-black family, plus fuzz and underscore variants

Separator: hyphen 70, underscore 30.
Shape counts: word-word-word-NUM 61, word-word-word 23, word-word-word-word 5, word-word-WORDNUM-NUM 3, word-WORDNUM-word 3, word-word-word-NUMWORD 3, word-word-word-WORDNUM 1, word-word 1.

- First token is `apex` in 95 of 100 rows.
- Second token is `black` in 68 rows.
- Third-token vocab is test/probe work: test 22, fuzz 21, internal 5, race 5, probe 4, plus ipv6, dns, self, backend, and similar.
- The strict `apex-black-test-NNN` sub-series inside `tester` is only 11 rows (numbers 012, 013, 017, 020–024, 031–033, with gaps). The wider `apex-black-test` series across author strings is 14 rows: tester 11, plus 1 each under `Testing`, `audit`, and a markup-shaped author string. So the series is not contained by one author value.
- Underscore names (30 rows) are mostly `apex_*` forms, e.g. apex_ssrf_test_v2 shape and apex_*_test shapes.
- Numbered names: 136 of 533 rows in the whole file contain a digit; 125 end in a digit.
- Outliers in this batch: one 100-character repeated-letter name, one very long repeated-letter suffix name, and names built from separator and character probes (newline, pipe, dash, comma shapes).

Haiku split: registry_test_or_probe 98, mass_generated 2. Agent activity: possible 93, likely 7.

### 1c. t (20 rows) — ssrf probe series with hash suffixes

All hyphen names. First token is `ssrf` in 19 of 20 rows (the 20th is an apex-black name).
Template: `ssrf - [target word] - [8-hex suffix]`, with variants `ssrf-portNNNN-[hex]`, `ssrf-ipN-[hex]`, and `ssrf-chain-[a/b]-[suffix]`.
Suffix shapes: 8-hex 18 rows, epoch-style 10-digit 1 row, other 1 row.
Summary is the bare word `testing` in 19 of 20 rows. Haiku: all 20 registry_test_or_probe; agent activity possible 17, likely 3.

### 1d. SR (13), Test (10), A2 (2), apexhunter (3), Security Researcher (2) — epoch-suffix probes

These authors share one template: `[probe words] - [10-digit epoch-style number]`.
- SR: 13 of 13 end in an epoch-style number. Shapes: word-word-NUM 9, word-NUM 2, wordNUM-NUM 1, word-word-word-NUM 1. Probe words: ssrf, webhook, portscan, internal, payload, unauthorized, chainproof.
- Test: 10 of 10 end in an epoch-style number. Shapes: word-word-NUM 4, word-NUM 4, word-word-word-NUM 2. Probe words: ssrf, noko (Nokogiri), timeout, large-html, nullbyte, badhtml, deepnest, formtable.
- A2: 2 of 2 epoch-suffix. apexhunter: 2 of 3 epoch-suffix. Security Researcher: 2 of 2 epoch-suffix. Apex Black Assessment: 1 of 1 epoch-suffix.
- All SR and Test rows are registry_test_or_probe. Agent activity: SR possible 9 / likely 4; Test possible 9 / likely 1.

### 1e. Short and placeholder author strings — T, test, Tester, testingbear

- T (8 rows): shapes word-word-word 5, single token 1 (a repeated-letter string), word-word 1, word-word-NUM 1. Names are mostly `test-*` forms plus `seed-gem`. Summary is the single letter `T` in all 8 rows. All 8 registry_test_or_probe; agent possible 6 / likely 2.
- test (7 rows): shapes word-word-word 6, word-word-word-NUM 1. Names start with `attacker` in 5 rows. All 7 registry_test_or_probe; agent possible 7.
- Tester (5 rows): all word-word-word `test-*` names (security, path-traversal, deep-traversal, symlink, oidc-publisher shapes). All 5 registry_test_or_probe; agent possible 5.
- testingbear (5 rows): all underscore `apex_*` names (self_ssrf, dep_test, tar_test, pub_test, trav_depth shapes). All 5 have blank Haiku and blank dashboard rules. The file makes no Haiku claim about them.

### 1f. Markup-shaped and template-expression author strings (9 rows)

Shape only, values not reproduced here:
- Script-tag-shaped author strings: 4 rows (three distinct strings, counts 2, 1, and 1).
- Image-tag-shaped author string: 1 row.
- Template-expression author strings (the `7*7` family, three spellings): 4 rows.
Their package names are ordinary probe shapes (xss, ssti, test, numbered). Their summaries are markup-shaped or template-expression-shaped in most cases. This is a rendering-probe grammar, not a library-naming grammar: the payload is placed in the author and summary fields themselves.

### 1g. One 151-author row, and the long tail of real-looking names

- One row has an `authors_declared` value that is a list of 151 author tokens (tester plus author1 through author150 with a fuzzing suffix). Counted as 1 distinct author value, it is really a fuzzing input. The package name follows the apex-black-fuzz shape and the summary is `Test`. Haiku and dashboard fields are blank.
- Distinct `authors_declared` values in the file: 46. That count hides the 151-author row, so it is not a count of real people or accounts.
- Long tail, 1–4 rows each, with content-bearing names and summaries: shirobai family (4 rows, one stem plus three suffix variants), rubocop-metz / metz-scan (2), jira-api pair (2), ecoportal pair (2), and singletons such as rosett-ai, edoxen, sportdb-parser, jrjackson, pico_phone, minitest-hashdiff, intranet-pictures, query-stream, talk_to_your_app, rails-agent-stack. These names do not follow the combinatorial, apex, ssrf, or epoch templates. Most of them have blank Haiku fields (see section 5).

## 2. Summary-text census

Distinct summary strings: 224 in 533 rows. No summary is empty (0 empty summaries). Short summaries (12 characters or fewer): 98 rows.

### 2a. The university-research template — 309 rows, 116 distinct X values

Template: `University research based on <X>`, where X is a known Ruby gem name.
- Andrey78: 129 of 129 rows use this template.
- Prvaz12_mars: 112 of 113 rows use it; the 1 exception uses the shorter form `Research based on cuba` (no `University` word).
- monib110: 68 of 68 rows use it.
- No other author uses this template.
- Most X values repeat 3 times (69 of 116 values); 40 repeat twice, 5 repeat 4 times, 2 occur once. The top X values (rack, json, bundler, rake, rails) occur 4 times each. Andrey78 alone uses all 116 X values (103 once, 13 twice within his own batch), so the other two authors' X sets are subsets of his.
- 118 summary strings are shared across more than one author value, and almost all of them are this template. The shared set is the evidence for the dashboard rule `Group: shared text` (185 rows: Andrey78 65, Prvaz12_mars 60, monib110 60).

Linguist note: the template asserts a university link, but the file contains no university name, no paper, and no link that supports it. The claim inside the summary is self-asserted text, not a verified fact in the file. The summary X also never matches the package name: the name is a size-quality-container product, while X is an unrelated existing gem. Haiku reasons repeatedly call this `unrelated`, `mismatched`, `incoherent`, or `copied`.

### 2b. Bare placeholders — 86 rows

Exact strings, with counts:
- `Test`: 54 rows (tester 49, plus SR 2, Tester 1, A2 1, and the 151-author row 1).
- `testing`: 19 rows (all t).
- `T`: 9 rows (T 8, plus one template-expression author row).
- `test`: 4 rows (test 3, Testing Wolf 1).
These four strings are the whole placeholder core. They carry no project content. They pair with placeholder author strings (tester, test, T, SR) in the dashboard rule `Package: placeholder author` (122 rows) and `Package: placeholder text` (92 rows).

### 2c. Test/probe-descriptive summaries — 105 rows

These name the test in plain words. They are content-bearing about intent, not about a library function. Frequent shapes:
- `Testing link verification SSRF`: 26 rows (all tester).
- `Testing internal service access`: 4 rows (tester).
- `Testing SSRF in verify link job`, `Testing redirect following`, `Testing Nokogiri parsing of ...`, `Testing Faraday timeout`, `Testing Nokogiri with ...` (Test, 1 row each, 10 distinct strings).
- `Testing dependency resolution` (2 rows, testingbear), `Testing tar traversal`, `File write test`, `Deep traversal payload` (testingbear).
- SSRF / webhook / port-scan / traversal / tenant / cross-account / owner-injection wordings (SR, Tester, test, Panther, apexhunter, attacker, and others, mostly 1 row each).
- Self-asserted assessment wordings (2 rows, Security Researcher): one says the gem was pushed as part of an authorized security assessment; one calls a gem a proof-of-impact gem. One further row (Apex Black Assessment) says it was pushed via a scope-escalated legacy key. These are claims made by the summary text itself. The file does not verify authorization, scope, or impact. Flag for the adversarial lane: do not upgrade a summary's self-description into a verified assessment.

### 2d. Markup-shaped summaries — 8 rows in first-match classification, 14 rows containing a tag or template substring

First-match classification (section 2 header order) puts 8 rows here: summaries that are themselves markup or template expressions, not descriptions. They pair with markup-shaped authors and probe names (xss, ssti). Counted by shape only here. They are rendering probes: the text is the test. A looser count — any summary containing a `<script`, `<img`, `<svg`, or `7*7` substring — is 14 rows, because 6 more such summaries were first classified as test/probe-descriptive (they also contain test words).

### 2e. Long descriptive summaries — 13 rows, apparently real-library text

These read like normal library descriptions (multi-sentence, specific function, named tools or frameworks). They belong to the long-tail authors in section 1g, plus one tester row with a long RDoc-style summary. Most of these rows have blank Haiku fields and zero or more runtime dependencies (see section 4). The file does not claim they are fake, and their text does not match the probe or combinatorial templates. Do not sweep them into the mass-generated or probe counts.

### 2f. Repeated strings beyond the templates

- The most repeated summary in the file is `Test` (54 rows), then `Testing link verification SSRF` (26), then `testing` (19), then `T` (9).
- Outside the university template, only three summary strings cross author values: `Test`, `T`, and one markup-shaped string shared by a markup author and tester.
- Summary reuse is therefore concentrated in exactly two places: the university template (shared across the three combinatorial authors) and the bare placeholders (shared across the probe authors).

## 3. Haiku reason rhetoric — claim classes

484 rows have a Haiku reason; 49 rows have none (same 49 rows with blank Haiku category and blank dashboard rules). Distinct reason strings: 485 counting the blank as one value, 484 non-empty. Reasons are near-unique: mass_generated has 305 rows and 305 distinct reasons, so Haiku does not reuse a fixed verdict sentence. It rewrites the same claim set per row.

First-match clustering of the 484 non-empty reasons (a reason can hit several classes; this counts its first class only):
- Batch/combinatorial, no probe or agent word: 272.
- Registry probe/test: 126.
- Automated/scripted, no agent word: 46.
- Agent word present: 38.
- Other: 2.

Keyword hits across all 484 reasons (multi-label, substring counts): batch 266, burst 128, combinatorial 329, template 68, placeholder 67, MFA 289, publisher 195, generic summary 82, unrelated summary 162, zero dependencies 311, version 0.0.1 148, single/one author phrasings 122 combined, coordinated 56, SSRF 92, out-of-band 42, callback 35, webhook 23, deception 12, lookalike 10.

### Class A — Mass generation / combinatorial batch (the combinatorial group)

Verbatim quotes (copied from the file):

> "Part of 129 packages published together with combinatorial names (word-list pattern like ultra-fast-box, mega-max-tool). Single author Andrey78, zero deps, unrelated summary mentioning rack-mini-profiler, source repo name matches but batch is strong signal."

> "Part of 129 packages published together with combinatorial names (mini/mega/super/giga + generic words), all from one author Andrey78, MFA off, no publisher handle, version 0.0.1, summary unrelated to name and copied from shoulda-matchers."

Rhetoric pattern: batch size + name pattern + single author + zero deps + MFA off + no publisher + version 0.0.1 + summary unrelated to name. The source-repo match is named and then discounted as `weak evidence` or a `weak counter-signal`. The word `mass` itself is rare in reasons (2 hits); the claim is carried by `batch`, `combinatorial`, and the numbers, not by the word `mass_generated` from the category label.

Batch-size numbers in reasons do not always match file row counts. Andrey78 reasons say 129 (matches 129 rows). Prvaz12_mars reasons say 113 (matches 113 rows). monib110 reasons say 60, but the file has 68 monib110 rows. Tester reasons say 101, 71, or about 100, but the file has 100 tester rows. One Andrey78 reason says 134, not 129. The adversarial lane should not quote a reason's batch number without checking it against the CSV.

### Class B — Automated / scripted batch publishing (no agent word)

Verbatim quotes:

> "Part of 134-package batch from one author with combinatorial names (adjective-adjective-noun) and shared summary; zero deps, homepage only a profile, no source link, mismatched summary. Strong automation signal."

> "Part of a 129-package batch of combinatorial names (word-list style like mini-max-pkg) under a single declared author with no MFA, zero dependencies, and a summary mismatched to the name, suggesting bulk automated publishing."

Rhetoric pattern: `automation signal`, `automated`, `scripted`, `bulk automated publishing`, `script-generated`. Count: 48 reasons contain an `automat*` word; 46 of them do not contain the word `agent`. Automation is the file's preferred mechanism word. It is asserted from batch shape (size, single author, template names, zero deps), not from any log, timing, or tool trace in the file.

### Class C — Registry probe / test artifact (the probe group)

Verbatim quotes:

> "Name ssrf-test with numbered suffix, summary 'SSRF PoC', no links, 0 deps, short author 'SR', no MFA. Burst of 13 packages by same owner with names like unauthorized-test, portscan, internal-scan suggests registry probing."

> "14 numbered 'apex-black-test' packages published together, authors 'Testing', no publisher handle, no MFA. Links point to localhost admin and cloud metadata endpoints, and the summary states an SSRF test, so this probes the registry and link-following."

Rhetoric pattern: probe word in the name + probe word in the summary + link shape (loopback, metadata, callback, bare IP) + burst size + placeholder author. The inference step is explicit: name plus summary plus link shape `suggests` / `reads as` probing. The file does not contain a probe result, a callback receipt, or a registry response, so `probing` here means `probe-shaped submission`, not `proven probe outcome`.

### Class D — Placeholder author / placeholder text / template batch

Verbatim quotes:

> "Burst of 13 packages by author SR with probe-like names (ssrf-test, portscan, internal-scan, unauthorized-test), placeholder summary 'Test', no links or deps, and numbered timestamp name. Looks like registry probing, not a real library."

> "Part of 129 combinatorially named packages published together under one handle, with generic word-list names, zero dependencies, and version 0.0.1. Summary mismatches the name and is shared-text templated. Source link points to a same-named repo, a weak counter-signal."

Rhetoric pattern: `placeholder` marks an author or summary as a stand-in, not a real identity or description. `Templated` marks a summary as copied or generated from a pattern. Both words do evidential work: they turn repetition into an intent claim (test or bulk) rather than coincidence.

### Class E — No deception / no lookalike (mostly pkg-review-2)

Verbatim quotes:

> "Part of a 129-package batch with combinatorial names (adjective-adjective-noun) published together; single-author profile with no MFA and zero dependencies. Summary is a generic claim with no real project detail. No clear deception signals."

> "Part of a 129-package batch with combinatorial names (giga-lite-hub, mini-fast-rb style) from a single author. Has a source link to a matching GitHub repo and a non-empty summary, which argues against deception. No dependencies, version 0.0.1, MFA not required."

This class matters because it limits the mass-generation claim: bulk plus generic does not equal deception in Haiku's own wording. Only 12 reasons use the word `deception` and 10 use `lookalike`, and most of those uses are negations (`no clear deception`, `not a lookalike`, `no lookalike of a popular package`). The file contains no claim that any package impersonates a named popular package.

### Class F — Agent involvement: asserted vs merely describing mass generation

This is the key split. Flag it for the adversarial lane.

Agent-word reasons: 38 of 484 (7.9%). All 38 are registry_test_or_probe rows. Zero mass_generated reasons use the word `agent`.

Breakdown of the 38:
- Agent activity label possible: 29. Likely: 7. No_sign: 2.
- Deny or hedge the agent claim: the large majority. Repeated closings: `no explicit agent markers`, `no agent metadata`, `no explicit agent signal`, `no clear agent markers`, `no clear agent sign`, `agent use only possible`, `agent origin unclear`, `not clearly agent-driven`, `agent use not clearly indicated`, `no direct agent sign`.
- Positive or near-positive agent wording: only a few, and all are still hedged or inferred from batch shape, not from an agent trace:
  - `agent-style pattern` (apex_link_tracker, likely).
  - `agent-style batch testing likely` (apex_link_es, likely).
  - `Agent signal is inferred from batch pattern` (ssrf-gemslist, likely).
  - `agent use is plausible given the systematic batch` (apex_inject2_test, likely).
  - `agent use is plausible but not certain` (apex_webhook_capture, likely; ssrf-redirect-test, likely).
  - `agent use only possible from scripting` (apex-black-fuzz-051, possible).
- One reason explicitly separates script from agent: for test-many-files, `batch looks scripted, not an agent` (activity still listed as possible).
- 30 reasons use a `no ... agent` phrasing (including the 2 no_sign rows and 28 possible rows). So the reason text contradicts or weakens the `possible` label in at least 28 cases.

Verbatim quotes (agent class, hedging and positive ends):

> "Name apex-black-test-017 is numbered within a batch of about 100 packages published together under author 'tester' with null publisher handle, placeholder summary 'Test', no links, and zero dependencies. Looks like registry probing; no agent metadata."

> "Part of a batch of 71 numbered 'apex-black-test' packages with no links, no dependencies, and no publisher handle. Summary and author fields hold XSS-style markup, which looks like a probe of the registry. Not clearly agent-generated."

> "Part of 101-package owner burst and 18-package template batch under author 'tester', homepage is localhost 127.0.0.1:9200, summary probes SSRF, names like apex_homepage_ssrf suggest registry probing; agent-style batch testing likely."

> "Name follows a templated ssrf-* probe batch (19 names in template batch, 28 in owner burst) with placeholder summary 'testing', author 't', null publisher, no deps, and homepage only a generic rubygems link. Agent signal is inferred from batch pattern."

Consequence: no reason in the file asserts `an agent did this` as a plain fact. The strongest agent wording is `agent-style`, `agent-like`, `plausible`, or `inferred from batch pattern`. The 18 `likely` rows are all probe rows (tester 7, SR 4, t 3, T 2, Testing 1, Test 1), and even their reasons mostly say `probing` first and agent second, if at all: only 7 of the 18 likely rows contain the word `agent` in their reason.

Also note: 5 non-empty reasons are cut off mid-sentence in the CSV itself (they do not end with a period, and one ends mid-word). One of them is a pkg-review-2 reason that ends mid-word. Quote those reasons only up to the cut, and do not complete them.

### Class G — The single unclear row, and the 49 blank rows

Unclear row (monib110, giga-pure-tool shape), verbatim:

> "Three packages published together with shared text and generic names (giga-pure-tool, giga-clean-box, mega-sharp-tool), zero dependencies, 0.0.1 version, MFA off. Summary is unrelated to name; link points to own profile and repo, so not clearly deceptive."

Note the batch number here is 3, not 68 or 60. Haiku's own batch framing for this author is inconsistent across rows.

Blank rows: 49 rows have no Haiku category, level, score, activity, prompt, or reason, and no dashboard rules. They include testingbear (5), the shirobai family (4), the jira/ecoportal/rubocop pairs, most long-tail singletons, the 151-author fuzz row, and 6 monib110 rows. For these rows the file claims only: name, version, dates, author string, summary, link shapes, dependency count, and withdrawn status. Any mass/probe/agent claim about a blank row would be new, not file-sourced.

## 4. homepage_uri / source_code_uri / runtime_dependencies — shapes only

### homepage_uri shapes (533 rows)

- rubygems.org profile page for the author string: 303 rows. In all 303, the profile name equals the `authors_declared` value. This is the default shape for the combinatorial group and much of the probe group.
- Empty: 100 rows (tester 47, SR 13, T 8, Tester 5, and the long tail; the combinatorial authors have no empty homepages).
- rubygems.org other/gem pages: 36 rows combined (other 24, gems page 12).
- Out-of-band callback shape (webhook.site with a UUID path): 19 rows.
- Random-subdomain callback shape (a random-looking subdomain with an oast-style suffix plus a path): 22 rows, plus 4 more rows with similar random-subdomain shapes under other suffixes.
- Bare-IP host: 13 rows. Loopback: 5 rows. Link-local metadata-IP shape: 2 rows. Internal/metadata-shaped host: 4 rows.
- Code-host profile/repo pages: 15 rows (github shape). Placeholder example host: 1 row.
- Homepage equals source_code_uri in 10 rows.

### source_code_uri shapes (533 rows)

- Empty: 327 rows. Empty by author: tester 99 of 100, t 20 of 20, SR 13 of 13, Test 10 of 10, T 8 of 8, test 7 of 7, Tester 5 of 5, testingbear 5 of 5, plus the long tail. Combinatorial authors are the exception: Andrey78 has a source link in 78 of 129 rows, Prvaz12_mars in 67 of 113, monib110 in 46 of 68.
- Code-host owner/repo shape: 201 rows. In every combinatorial source row, the owner equals the author string and the repo name equals the package name (78 + 67 + 46 = 191 rows). Across all non-empty source rows, repo name equals package name in 198 of 206 rows.
- Random-subdomain callback shape: 2 rows. Code-host alternatives (gitlab, bitbucket shapes): 2 rows. Internal/metadata-shaped host: 1 row.

Linguist note: the source-link pattern is two-sided. A matching owner/repo name is the file's only `real project` counter-signal, and Haiku calls it weak or mildly reassuring. But the same match is exactly what a template generator would produce (owner + package name), so the shape alone cannot separate a real repo from a generated one. The cryptologist owns payload and repo-content questions; this lane claims only the shape.

### runtime_dependencies (count field, not names)

- 0 dependencies: 509 rows.
- 1 or more: 24 rows. Those 24 are almost all long-tail or testingbear rows (for example, one row with 17, one with 22, the rest 1–5). No combinatorial, tester, t, SR, Test, T, test, or Tester row has more than 0 dependencies, except one Prvaz12_mars row with 2 and a short non-university summary.
- So `zero dependencies` is a true shape claim for the mass group (304 of 305 rows; the exception is the one Prvaz12_mars row with 2 dependencies) and for the probe group (178 of 178 rows), and a false generalization if applied to the whole 533 rows (blank rows are 26 of 49 at zero dependencies).

### Versions (for the naming lane, not a claim about intent)

- Version 0.0.1: 452 rows (all 305 mass_generated rows, 127 probe rows, 19 blank rows, 1 unclear row).
- Other versions: 81 rows, including 0.1.0 (19), 0.0.2 (13), 1.0.0 (10), and fuzz/edge shapes (an all-zero long version, a 999999 version, a date-stamped version, a release-candidate version).
- All combinatorial rows are 0.0.1. Multi-version rows (versions_in_window above 1): 42 rows, concentrated in the long tail.

## 5. Dashboard rules vs Haiku labels — a second voice, and it disagrees on level

Dashboard rule hits (multi-label, 484 rows with rules, 49 blank):
Group: combinatorial names 372; Group: shared text 185; Group: owner burst 158; Package: placeholder author 122; Package: numbered name 115; Group: template batch 100; Package: placeholder text 92; Group: name series 66; Package: probe name 59; Package: oob url 48; Package: short author 43; Package: test name 41; Package: markup 12; Package: placeholder link 8; Package: random name 1.

Dashboard rule level vs Haiku level (same rows, different grades):
- Dashboard low (121 rows) maps to Haiku high in 111 rows.
- Dashboard medium (193 rows) maps to Haiku high in 188 rows.
- Dashboard critical (151 rows) maps to Haiku critical in 73 and Haiku high in 76.
- Only the 49 blank rows agree trivially (blank on both).
So the two grading voices in the same file disagree on severity for most rows. Do not cite one level as if it were the file's single grade.

Category vs dashboard overlap:
- mass_generated (305) overlaps combinatorial names in 302 rows and shared text in 184 rows, and almost nothing else.
- registry_test_or_probe (178) overlaps owner burst 156, placeholder author 120, numbered name 115, template batch 98, placeholder text 90, combinatorial names 70, name series 64, probe name 59.
- 70 rows carry the combinatorial-names dashboard rule but are not mass_generated (they are probe rows with combinatorial-looking names). 3 mass_generated rows carry no combinatorial-names rule. Category and dashboard rule are related but not identical claims.

Prompt versions: pkg-review-1 464 rows, pkg-review-2 20 rows, blank 49. The 20 pkg-review-2 rows are the no-deception class in section 3E (10 mass_generated, 10 probe). Their rhetoric is calmer: `no clear deception`, `mildly reassuring`, `bulk pattern without clear deception`. Prompt version changes the rhetoric, not just the grade: pkg-review-2 reasons hedge more and assert less.

## 6. Claim inventory — every distinct claim the file makes

`OBSERVED` = stated directly by a CSV field value. `LABEL` = a dashboard or Haiku grade. `INFERENCE` = a reason's reading of the fields. `SELF-ASSERTED` = text inside a summary or author string, not verified by the file. `ABSENT` = the file makes no such claim.

1. All 533 packages are withdrawn. (OBSERVED, withdrawn field.)
2. All 533 were first published between 2026-07-06 and 2026-07-13. (OBSERVED, date fields.)
3. The three combinatorial authors published single-day bursts: Andrey78 on 2026-07-06, monib110 on 2026-07-12, Prvaz12_mars on 2026-07-13. (OBSERVED.)
4. The named probe authors published single-day bursts on 2026-07-07 (tester, t, SR, Test, T, test, Tester, testingbear). (OBSERVED.)
5. 310 package names are products of one shared 10 x 10 x 10 word list. (OBSERVED pattern; the `mass generation` reading of it is INFERENCE.)
6. Those 310 names never repeat, across or inside authors. (OBSERVED.)
7. 309 summaries use the `University research based on X` template, with 116 distinct X values. (OBSERVED.)
8. Summary X never matches the package name in the combinatorial group. (OBSERVED pattern; `unrelated` / `copied` is INFERENCE.)
9. The university link in those summaries is real. (ABSENT. The file contains no university name or source. Do not treat the template as proof.)
10. 86 summaries are bare placeholders (`Test` 54, `testing` 19, `T` 9, `test` 4). (OBSERVED.)
11. 105 summaries describe a test or probe in plain words (SSRF, webhook, traversal, tenant, Nokogiri, and similar). (OBSERVED wording; test intent is INFERENCE from wording plus name plus link shape.)
12. 8 summaries are markup or template-expression shapes, not descriptions. (OBSERVED shape.)
13. 13 summaries are long, specific library descriptions. (OBSERVED wording; `real library` is INFERENCE and is not claimed by Haiku for most of these rows, which are blank.)
14. Some summaries claim an authorized security assessment, proof-of-impact, or a scope-escalated key push. (SELF-ASSERTED only. Not verified in the file.)
15. 509 rows have zero runtime dependencies; 24 rows have 1 or more. (OBSERVED count field; dependency names are not in the file.)
16. 452 rows are version 0.0.1; all combinatorial rows are 0.0.1. (OBSERVED.)
17. 303 homepages are rubygems.org profile pages matching the author string; 100 homepages are empty; the rest are callback, IP, loopback, metadata, code-host, or placeholder shapes. (OBSERVED shape.)
18. 327 source links are empty; 206 are present, and in 198 of those the repo name equals the package name. (OBSERVED shape.)
19. A matching source repo name is weak evidence for a real project. (INFERENCE, Haiku's own wording: `weak evidence`, `weak counter-signal`, `mildly reassuring`.)
20. Dashboard rules fire as listed in section 5 (combinatorial names, shared text, owner burst, placeholder author/text, numbered name, template batch, name series, probe name, oob url, short author, test name, markup, placeholder link, random name). (LABEL.)
21. Haiku categories: mass_generated 305, registry_test_or_probe 178, unclear 1, blank 49. (LABEL.)
22. Haiku agent activity: possible 461, likely 18, no_sign 5, blank 49. (LABEL. Reason text supports it weakly or not at all; see section 3F.)
23. Batch publishing was automated or scripted. (INFERENCE, 48 `automat*` reasons; no log or timing evidence in the file.)
24. Probe-shaped rows probed the registry or its link handling. (INFERENCE from name plus summary plus link shape; no probe result or callback receipt in the file.)
25. Bulk plus generic does not equal deception, and no package is shown to impersonate a named popular package. (INFERENCE, mostly negations in reasons; no lookalike target is named.)
26. Batch sizes are 129, 113, 60, 101, 71, 28, 19, 13, and similar numbers as stated in individual reasons. (INFERENCE numbers, and several disagree with CSV row counts: monib110 reasons say 60 vs 68 rows; tester reasons say 101/71 vs 100 rows; one Andrey78 reason says 134 vs 129 rows.)
27. The 49 blank rows are mass-generated, probe, or agent-related. (ABSENT. The file claims nothing of the kind about them.)
28. The 46 author values are 46 people or accounts. (ABSENT and misleading: one value is a 151-token fuzz list, several values are placeholder words or markup shapes, and the same name series spans several author values.)
29. Any package's code does anything (exfiltrates, scans, exploits, or functions as described). (ABSENT. The file has no code, no dependency names, and no execution result. That is outside this lane and outside this file.)
30. Any author is a human, a bot, or an agent. (ABSENT as fact. The file has author strings and Haiku hedges only.)

## 7. What to hand the adversarial lane

- Test the agent labels against the reason text, not the other way round: 461 possible + 18 likely labels vs 38 agent-word reasons, most of them denials or hedges, and zero agent-word reasons in the mass_generated group.
- Test every reason batch number against the CSV: monib110 60 vs 68, tester 101/71 vs 100, one Andrey78 134 vs 129.
- Test the dashboard-vs-Haiku level split: dashboard low rows are Haiku high in 111 of 121 cases.
- Test the `university research` template as an unverified self-assertion, not as affiliation evidence.
- Test the self-asserted assessment rows as claims inside summaries, not as verified authorization.
- Keep the 49 blank rows and the 13 long-descriptive rows out of the mass/probe totals unless new evidence puts them there.
- Keep the source-repo match as a weak, two-sided shape: it fits both a real repo and a template generator.
