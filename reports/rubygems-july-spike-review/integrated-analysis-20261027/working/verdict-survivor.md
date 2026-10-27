# VERDICT + SURVIVOR lane — July 2026 RubyGems spike set

Lane: verdict + survivor only. No push. No Factum write. No other worker file touched.
Method: read-only recomputation from the three live JSONs and the operator CSV.
No payload executed. No credential-shaped value copied.

## Recomputed census (my own counts, not copied totals)

- Records in each census: 533.
- RubyGems API live: 23. RubyGems API gone (404): 510. Both censuses agree.
- Diffend full, reconciled: 18. All 18 are also API-live.
- Live on both (API + Diffend full): 18.
- Live on RubyGems only (Diffend stub): 5 — apex-black-test-011, apex-blk-test-final,
  apex-oidc-probe, jrjackson, minitest-hashdiff.
- Live on Diffend only: 0.
- Artifact URLs, reconciled txt: 48 unique URLs = 23 RubyGems pages + 18 Diffend pages
  + 7 distinct live source repos. The reconciled JSON counts 49 per-gem artifact
  entries because rubocop-metz and metz-scan share one repo URL. The JSON total of 50
  adds one gone gem's live repo (klondikemarlen-jira-api, gem API-404, repo 200).
  This is a counting difference, not a dispute.
- First census Diffend full was 22. Reconciliation cut 4 to stub (apex-black-test-011,
  apex-oidc-probe, apex-blk-test-final, minitest-hashdiff, each about 5.7 KB, no diff
  content). Probe survival is therefore registry-listing only, with no Diffend diff.
- Total downloads across the 23 live gems, first census: 11,138,862.
  jrjackson alone is 10,508,353 of that, or 94.3 percent. Any download argument that
  does not name jrjackson separately is misleading.
- CSV latest version matches live latest on only 3 of 23 (apex-black-test-011,
  apex-oidc-probe, minitest-hashdiff). The other 20 differ. Most differ because the
  live gem moved past its July window version. Two differ downward in a way that
  means version loss, not progress: apex-blk-test-final CSV 0.0.5, live only 0.0.1;
  edoxen CSV 2.1.3, live latest 0.8.4 with no 2.x version in the live list.
  The CSV is a July-window export, not current state.
- Data quirks, stated not smoothed over:
  - jrjackson: first-census API latest field says 0.3.8, but its versions list
    reaches 0.5.5. Do not quote 0.3.8 as its latest without that note.
  - test_gem_kangaroo and testgem-mini: first census lists 8 and 5 versions;
    reconciled JSON lists only the latest for each. Version counts for these two
    are not reliable from the reconciled JSON alone.
  - The live JSONs carry no version publish dates (except date-encoded shirobai
    version strings). Recency for most survivors can only be inferred from version
    numbers, not observed from dates.

## 1. Verdict test table

| Prior verdict | Result | Deciding live datum |
|---|---|---|
| (a) CSV is a third-party dashboard export, not our observation | STANDS | Live census is our observation, but it checks names against the registry only. It does not turn dashboard levels, rules, or Haiku labels into our findings. 21 of the 23 live rows have blank dashboard/Haiku fields in the CSV, so the dashboard says nothing about most survivors. CSV latest matches live latest on only 3 of 23. |
| (b) July-7 verdict: NO CHANGE | STANDS | July-7 first-publish live gems: 6 of 204 July-7 rows (jrjackson, 3 probes, 2 test gems). 198 July-7 rows are gone, including all 100 tester rows. No new observation type appears: no gem code, no callback receipt, no actor evidence, no download-by-date. A wider candidate pool is still a scoping question, not a verdict change. |
| (c) GemStuffer / JFrog picture: NO CHANGE (file silent on it) | STANDS | The live census adds registry presence only. It contains no GemStuffer, JFrog, stuffer, or backdoor evidence, and no survivor links to that picture. Silence stays silence. |
| (d) Andrey78 batch = mass-generated shape only, NO agent evidence, NO severity verdict | STANDS (transience corroborated, no upgrade) | Andrey78 129 of 129 gone, Prvaz12_mars 113 of 113 gone, monib110 68 of 68 gone: the full 310-row combinatorial set is API-404. That confirms the batch was transient. It does not add agent evidence, code, or a removal reason, so no severity verdict follows. Removal reason is unknown from these JSONs. |
| (e) Agent activity UNPROVEN on this file | STANDS | No live datum shows a model, harness, tool call, prompt, or human-versus-agent actor. The 3 probe survivors prove probe versions are still listed, not who published them. Their downloads (515, 550, 1,282) are counts only; they do not identify a downloader. The shirobai 2026-10-27 releases prove a project released on census day, not that an agent released it. |
| (f) 203 of 533 already known, all via the JFrog list not independent observation; 330 new | STANDS, with a caution added | The live census does not re-derive corpus overlap, so the 203/330 split is untouched by it. The caution: survival concentrates in the CSV's blank-field rows (21 of 23 live are blank-field rows, out of 49 blank rows total). Blank therefore means neither safe nor gone. It is a dashboard-coverage gap, not a risk class. The 330-new side holds most survivors by date (July 6 and July 8-13 live gems), but that is a date pattern, not a new verdict. |

Plain statement: nothing in the live census changes a prior verdict. One verdict
gains corroborating transience (d). No verdict is upgraded. No fresh observed
bytes support an agent claim, a severity grade, or an impact claim.

## 2. Survivor classification (recomputed by me)

Rule used: name + CSV summary + live version count + live downloads + live source
status. A functional summary, a multi-version history, and a live repo point to
legit. A probe/test name or a self-described test summary points to probe/test,
even when downloads are high. Single-version alone does not decide: minitest-hashdiff
is legit by its functional summary, and talk_to_your_app is legit by its functional
summary despite a dead repo link.

| Class | Count | Members (short form) |
|---|---|---|
| Legit / ordinary gems | 18 | eco-helpers, ecoportal-api-graphql, edoxen, intranet-pictures, jrjackson, marlens-jira-api, metz-scan, minitest-hashdiff, pico_phone, query-stream, rosett-ai, rubocop-metz, shirobai, shirobai-performance, shirobai-rails, shirobai-rspec, sportdb-parser, talk_to_your_app |
| Probe | 3 | apex-black-test-011, apex-blk-test-final, apex-oidc-probe |
| Test | 2 | test_gem_kangaroo, testgem-mini |
| Other | 0 | — |
| Total | 23 | Matches the API-live count. No survivor is left unclassified. |

Notes on close calls:

- minitest-hashdiff (legit, not test): one live version 0.1.1, 2,395 downloads,
  Diffend stub after adjudication, but its summary is a functional testing utility
  (hash-diff output on assert failure), not a registry test. The stub means no diff
  artifact, not that the gem is a probe.
- talk_to_your_app (legit, with a caveat): functional MCP-layer summary, live
  versions to 0.3.0, 3,243 downloads, Diffend full, but its source repo answers 404.
  Legit project with a dead repo link. Repo death alone does not make it a probe.
- testgem-mini (test, not legit): 34,151 downloads is the second-highest test-class
  count and far above the probe counts, but name, author "Testing Wolf", and summary
  "test" all point to test. High downloads do not reclassify it. See section 3.
- apex-blk-test-final (probe, version-yanked): CSV latest 0.0.5 is absent live;
  only 0.0.1 survives. Survival here is partial at version level, not gem level.
- jrjackson (legit, dominant): 50 versions, 10,508,353 downloads, Diffend stub.
  The stub is a Diffend-coverage fact, not a legitimacy signal. Its size dominates
  every aggregate, so it is reported separately everywhere.

## 3. What survival means, per class

### Legit (18) — continued availability, and for most, continued maintenance

- OBSERVED: 18 gems answer API 200. 16 of 18 have Diffend full. The 2 exceptions
  are jrjackson (50 versions, Diffend stub, no source) and minitest-hashdiff
  (1 version, Diffend stub, no source); both survive on the API listing alone,
  like the probe class, and are distinguished from it by functional summaries
  and, for jrjackson, a 50-version history. Live latest versions exceed the CSV July latest for most of the
  class (eco-helpers 3.4.0 vs CSV 3.2.18; ecoportal-api-graphql 3.0.0 vs 1.3.13;
  marlens-jira-api 0.7.0 vs 0.5.2; metz-scan and rubocop-metz 0.6.0 vs 0.5.3;
  query-stream 1.4.0 vs 1.3.0; talk_to_your_app 0.3.0 vs 0.1.0.pre.4).
- OBSERVED (strongest recency signal in the set): all 4 shirobai gems carry
  version 2026.1027.0730, dated census day itself, plus 2026.1026.2000 the day
  before. That is a dated version string, not a publish-date field, but it is
  direct evidence of release activity on census day.
- INFERENCE: post-July version numbers mean continued maintenance, not just
  leftover listing. Cumulative downloads do not prove recent use.
- What would distinguish continued use from legacy residue: downloads by version
  and by date, dependent counts, and repo commit activity after July. None of
  those are in the live JSONs. Do not claim "in active use" from cumulative
  downloads alone. jrjackson's 10.5 million downloads are cumulative and may
  predate July by years; the JSONs do not split them by date.
- What survival does NOT mean: it does not clear or condemn the July window
  version. A gem can be legit today and still have had a yanked July version
  (edoxen, intranet-pictures, apex-blk-test-final pattern). Version-level checks
  are needed, not gem-level verdicts.

### Probe (3) — abandoned listing residue, not ongoing activity

- OBSERVED: single live version each (9.9.9, 0.0.1, 0.1.1). No live source repo
  (apex-oidc-probe source answers 404; the other two have no source). Diffend stub
  for all 3 after adjudication: no diff artifact. Downloads 515, 550, 1,282.
- OBSERVED: apex-blk-test-final lost its CSV latest version (0.0.5); only 0.0.1
  remains. That is version-level yanking, observed in the version list.
- INFERENCE: survival means the listing was not fully removed, not that probing
  continues. No post-July version is visible for any of the 3 (CSV latest equals
  live latest for 2 of 3; the third went backward through yanking).
- What would distinguish residue from ongoing probing: a post-July version, a
  callback receipt, or fresh downloads by date. None are present. Downloads at
  this scale are consistent with scanner, mirror, or curious pulls, but that
  explanation is INFERENCE, not observed downloader identity.
- Grade note: "probe" here is a name-and-summary classification (OBSERVED as
  self-description), not proof the probe ever executed or succeeded.

### Test (2) — abandoned test residue, most likely; one high-download anomaly

- OBSERVED: test_gem_kangaroo latest 0.0.14, 1,901 downloads, summary about an
  MFA-level push test. testgem-mini latest 0.4.0, 34,151 downloads, summary "test",
  author "Testing Wolf". Both are Diffend full, so code diffs exist for them,
  unlike the probe class. That is a Diffend-presence fact, not a use fact.
- INFERENCE: both read as test residue left listed after July testing. No actor
  evidence attaches to either.
- INFERENCE with a flag: testgem-mini's 34,151 downloads are anomalously high
  for a gem whose summary is "test". Possible explanations include a dependency,
  a mirror, CI reuse, or a shared test fixture. The JSONs cannot choose between
  them. Do not use the count to promote it to legit, and do not use it to claim
  impact. Extra evidence needed: dependents, download-by-version, and any repo
  or CI reference to the name.
- What would distinguish residue from reuse: version publish dates (absent from
  the JSONs), dependents, and download timing. Without those, "residue" stays
  INFERENCE, though it is the best fit for both names and summaries.

## 4. Consolidated verdict (one paragraph)

The July set is a third-party dashboard export of 533 registry rows, not our
observation, and the live census of 2026-10-27 does not change any prior verdict:
510 rows are gone from the RubyGems API, including the entire 310-row
combinatorial mass batch, and the 23 survivors split into 18 ordinary gems
(including the long-lived jrjackson and the actively releasing shirobai family),
3 probe listings, and 2 test listings, with no new code, callback receipt, or
actor evidence anywhere in the census; what it is, therefore, is a July
mass-generation shape plus a July-7 probe/test cluster plus ordinary gems that
happened to fall in the same dashboard window, and what it is not is agent
activity, a severity-graded incident, or a GemStuffer/JFrog finding, since the
probe survivors are single-version listing residue with no diff artifact and no
live repo, the test survivors are unexplained only in the size of testgem-mini's
download count, and the legit survivors survive because they are real projects
with post-July versions, not because the July spike validated them.
