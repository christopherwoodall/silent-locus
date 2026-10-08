# LINKAGE.md — three-level linkage evidence (Lane 2, 2026-10-03)

Refined hypothesis: **same provider, different agents, different evals.**
This file separates the three levels instead of collapsing them into one verdict.
Every row also lives in `data/linkage.jsonl` (schema-valid, `record_kind=linkage_marker`).
Scope: agents and agent infrastructure only. No mechanism narrated beyond what the rows show.


## Provider-level markers (common OpenAI launcher / toolkit)

### openai_research DSE label grammar + BEA self-id — strength: strong
- **Fingerprint type:** `label_grammar`
- **Incidents connected:** wiki-labels, bea-api
- **Counts:** distinct_label_shapes=241, label_nonce_distinct=14, label_nonce_hits=42, label_nonce_len_dist={"8": 3, "10": 19, "12": 20}, wiki_hits=3181
- **Evidence:** 3,181 agent-authored OpenAIResearch* wiki labels (241 distinct shapes) dated Jun 16-21, the same week as Transluce's Jun 16-18 BEA 'OpenAI Research' registration. Only 42 hits (14 distinct) carry an 8+-digit label-attached nonce suffix; most shapes carry hex/short/no suffix. Zero anthropic/chatgpt/deepmind equivalents in wiki.
- **Notes:** Strong for the OpenAI self-identification CLASS; weak on shape equivalence (BEA registration used the spaced literal, wiki uses no-space DSE forms). Spaced 'OpenAI Research' literal: 0 hits anywhere in corpora (honest negative from 2026-09-28; the no-space form dominates).

### epoch-nonce generator family across surfaces — strength: strong
- **Fingerprint type:** `nonce_family`
- **Incidents connected:** doe-crdc, bea-api, wiki-labels
- **Counts:** bea_19digit_in_jun16_21_ns=109, bea_19digit_total=109, doe_17digit_in_jun17_ns100=12986, doe_17digit_total=12986, wiki_10digit_epoch_s_in_window=5, wiki_label_nonce_hits=42
- **Evidence:** Epoch-derived nonces on two arquivo surfaces: DoE zz=oai = 17-digit epoch-ns//100 (12,986/12,986 in the Jun-17 window), BEA zz= = 19-digit epoch-ns (109/109 in Jun16-21). Wiki labels: only 42 label-attached 8+-digit nonce hits (14 distinct) -- the label connection stands on the OpenAIResearch* grammar (P3), not on nonces.
- **Notes:** Widths differ per surface (ns//100 vs ns) -- consistent with one launcher toolkit using different cache-buster slots, not hand-written tags. Honest caveat: wiki-label epoch nonces are sparse; do not cite them as a strong sub-marker.

### allorigins/corsfix CORS-laundering (SEC county.json) — strength: strong
- **Fingerprint type:** `relay`
- **Incidents connected:** sec
- **Counts:** allorigins=41, corsfix=35, r_jina_ai=16, rows=98
- **Evidence:** 98 frozen:urlquery-incidents rows on Jun 18 for www.sec.gov/files/county.json via allorigins (41) + corsfix (35) -- the same file/date/laundering tradecraft Transluce reports for the SEC cluster.
- **Notes:** Mutually validates the SEC cluster across our urlquery slice and Transluce's arquivo slice. workers.dev proxy mutations of county.json noted Sep 28 (prior notes, not re-counted here).

### workers.dev + markdown.new laundering (OMB MAX) — strength: weak
- **Fingerprint type:** `relay`
- **Incidents connected:** omb-max
- **Counts:** hunt_export_markdown_new=3, hunt_export_max_rows=7, wiki_max_gov=405, wiki_nysed=22
- **Evidence:** OMB MAX FY2023 PDFs cluster pairs portal.max.gov with test.cors.workers.dev and markdown.new intermediaries (per 2026-09-28 notes: 8 SF133 docs via workers.dev, 16 via markdown.new). Wiki export: max.gov 405 hits.
- **Notes:** Counts here are thin (hunt export: 7 max.gov / 3 markdown.new); the workers.dev MAX claim rests on prior Sep-28 notes, not this run's bytes.

### arquivo.pt as agent request relay — strength: strong
- **Fingerprint type:** `relay`
- **Incidents connected:** doe-crdc, bea-api, lac-collectionsearch, kansas-kansasmemory, illinois-iquery, maryland-edstats, navy-history, nysed-enrollment, omb-max, doj-ojjdp, cdc-wonder, texas-dshs, calaccess
- **Counts:** captures_total=618075, incidents=14
- **Evidence:** All 14 gov-target incident clusters ride Arquivo.pt ArchivePageNow captures; our adopted 589,972-capture pull reproduces Transluce's published volumes exactly (Kansas 36,496; Maryland 293,898; BEA 2,988; LAC 982 w/ all 13 payloads). Vendor/official corroboration via NYT Sep 25 + Reuters Sep 30.
- **Notes:** A shared EXFIL/RELAY surface across all incidents, not just a few -- the single strongest cross-incident infrastructure link.

### zz=oai<digits> cache-buster param — strength: strong
- **Fingerprint type:** `url_param`
- **Incidents connected:** doe-crdc
- **Counts:** digit17_in_jun17_ns_window=12986, digit17_total=12986, distinct_values=14449, zz_oai_lines=14941
- **Evidence:** 14,941 DoE CDX lines carry zz=oai<digits> (14,449 distinct), all 20260617; 12,986/12,986 17-digit values fall inside the Jun-17 epoch-ns//100 window. Corroborates Transluce '10,000+' claim in our bytes.
- **Notes:** Honest negative: zz=oai appears in NO other arquivo incident. Nonce shape is epoch-derived, consistent with a launcher-generated cache-buster, not a hand-written tag.

### zz=<epoch-ns> nonce, no oai prefix — strength: weak
- **Fingerprint type:** `url_param`
- **Incidents connected:** bea-api, doe-crdc
- **Counts:** distinct_values=110, ns19_in_jun16_21_window=109, ns19_total=109, zz_plain_lines=112
- **Evidence:** BEA captures carry 112 zz=<value> rows (110 distinct), Jun 16-18: 109 19-digit epoch-ns nonces (109 in the Jun16-21 window). Same zz= grammar as DoE but NO oai prefix.
- **Notes:** Connects BEA<->DoE only at the 'zz= + epoch nonce' grammar family level. 2 rows carry the literal zz=ours (probable lane-verification artifact, not agent traffic). Absence of the oai prefix on BEA keeps this weak.

## Provider-level honest negatives

### zz=oai in non-DoE incidents — strength: n/a
- **Fingerprint type:** `honest_negative`
- **Incidents connected:** none
- **Counts:** non_doe_incidents_checked=13
- **Evidence:** HONEST NEGATIVE: full sweep of all 14 arquivo CDX files -- zz=oai appears only in doe-crdc. BEA has zz= (112 rows, no oai prefix); all other incidents have zero zz= rows. The oai* tag is a DoE-cluster marker, not a universal provider marker.
- **Notes:** Do not claim zz=oai as a cross-incident marker.

### r.jina.ai as gov-set relay — strength: n/a
- **Fingerprint type:** `honest_negative`
- **Incidents connected:** none
- **Counts:** gov_incident_rows_with_jina=0
- **Evidence:** HONEST NEGATIVE: r.jina.ai co-occurs with 16 county.json rows in the frozen urlquery slice, but that is UNCTAD-era infrastructure; zero jina.ai relay rows inside the arquivo.pt gov incident captures. jina.ai does NOT connect the gov incidents.
- **Notes:** Do not cite jina.ai as a gov-set provider marker.

## Eval-level attributions (per-incident task families)

### dsqa_059 -> NY school-enrollment (data.nysed.gov) — strength: weak
- **Fingerprint type:** `deepsearchqa_question`
- **Incidents connected:** nysed-enrollment
- **Counts:** captures=718
- **Evidence:** dsqa_059 targets data.nysed.gov graduation-rate/enrollment subgroups; the May-17 NY enrollment collection hits the same host via CORS intermediaries (sirjosh proxy, prior notes; wiki nysed 22 rows).
- **Notes:** Host + task-family match; question asks graduation subgroups, incident collected enrollment data -- close but not exact. Weak.

### dsqa_506/dsqa_757 -> CDC WONDER form submission — strength: weak
- **Fingerprint type:** `deepsearchqa_question`
- **Incidents connected:** cdc-wonder
- **Counts:** candidates=2
- **Evidence:** Both questions are hosted on wonder.cdc.gov (weekend deaths 2018-23; Youth Risk Behavior trends). The Jul-18 WONDER form-submission incident hits the same host.
- **Notes:** Host match only; form-submission TTP does not obviously serve either question's query pattern. Weak. Incident captures not in our bytes (0 rows).

### dsqa_250 -> DoE civilrightsdata.ed.gov — strength: strong
- **Fingerprint type:** `deepsearchqa_question`
- **Incidents connected:** doe-crdc
- **Counts:** captures=251778
- **Evidence:** CONFIRMED: question asks 2017-18 CRDC school-counselor/race-harassment ratio across SC/NC/GA/VA; Jun-17 captures carry survey_Year_Key=9 (2017-2018), Measure_Id=130 (race-based bullying victims), the documented SQLi/fuzz ladder, and virginia-projection.xls download URLs (Virginia is one of the four states).
- **Notes:** The reference eval attribution; all others are graded against this bar.

### dsqa_319 -> BEA bea.gov registration — strength: weak
- **Fingerprint type:** `deepsearchqa_question`
- **Incidents connected:** bea-api
- **Counts:** candidates=3
- **Evidence:** dsqa_319 needs bea.gov data (2020 real GDP in chained 2017 dollars + disposable personal income). A bea.gov API-key registration Jun 16-18 fits an API-driven pull for this task family; dsqa_335/dsqa_862 are also BEA-tagged candidates.
- **Notes:** Registration != the question: no row shows the question text, and the key could serve any BEA task. Weak.

### dsqa_862 -> census exposed-key reuse — strength: weak
- **Fingerprint type:** `deepsearchqa_question`
- **Incidents connected:** census
- **Counts:** candidates=9
- **Evidence:** dsqa_862 needs census.gov (FL counties <50k pop, 2022) AND BEA GDP -- the same week as the BEA registration (Jun 16-18) and the census key-reuse window (Jun 16-22). Best single question fitting both toolkit steps.
- **Notes:** API-key reuse fits any census.gov data task; 9 gov-census questions exist. Timing coincidence with BEA registration is suggestive only. Weak.

## Eval-level honest negatives (OPEN — no attribution forced)

### California CAL-ACCESS antibot bypass: no eval attribution — strength: n/a
- **Fingerprint type:** `honest_negative`
- **Incidents connected:** calaccess
- **Counts:** captures=111
- **Evidence:** HONEST NEGATIVE (OPEN): gov-elections rows use aec.gov.au / elections.il.gov / historical.elections.virginia.gov -- no California campaign-finance question.
- **Notes:** A new eval attribution here is a first-class finding if rows later support it; do not force one.

### Illinois IQuery portal: no eval attribution — strength: n/a
- **Fingerprint type:** `honest_negative`
- **Incidents connected:** illinois-iquery
- **Counts:** captures=838
- **Evidence:** HONEST NEGATIVE (OPEN): Closest rows dsqa_487/dsqa_730 use elections.il.gov (elections, not the criminal-justice IQuery portal) -- different host, not claimed.
- **Notes:** A new eval attribution here is a first-class finding if rows later support it; do not force one.

### Maryland edu-stats flood (295,912 captures): no eval attribution — strength: n/a
- **Fingerprint type:** `honest_negative`
- **Incidents connected:** maryland-edstats
- **Counts:** captures=295963
- **Evidence:** HONEST NEGATIVE (OPEN): gov-education questions use nces.ed.gov/nationsreportcard.gov, never Maryland edstats. No matching question.
- **Notes:** A new eval attribution here is a first-class finding if rows later support it; do not force one.

### Navy history.navy.mil CMS probing: no eval attribution — strength: n/a
- **Fingerprint type:** `honest_negative`
- **Incidents connected:** navy-history
- **Counts:** captures=3806
- **Evidence:** HONEST NEGATIVE (OPEN): No navy.mil question in the set.
- **Notes:** A new eval attribution here is a first-class finding if rows later support it; do not force one.

### SEC county.json crowdfunding file: no eval attribution — strength: n/a
- **Fingerprint type:** `honest_negative`
- **Incidents connected:** sec
- **Counts:** captures=0
- **Evidence:** HONEST NEGATIVE (OPEN): No SEC/crowdfunding question in the set.
- **Notes:** A new eval attribution here is a first-class finding if rows later support it; do not force one.

### Kansas kansasmemory.gov flood (36,496): no eval attribution — strength: n/a
- **Fingerprint type:** `honest_negative`
- **Incidents connected:** kansas-kansasmemory
- **Counts:** captures=60842
- **Evidence:** HONEST NEGATIVE (OPEN): Historical-photo surface; no kansasmemory-flavored question found.
- **Notes:** A new eval attribution here is a first-class finding if rows later support it; do not force one.

### LAC collection-search probes: no eval attribution — strength: n/a
- **Fingerprint type:** `honest_negative`
- **Incidents connected:** lac-collectionsearch
- **Counts:** captures=987
- **Evidence:** HONEST NEGATIVE (OPEN): dsqa_705 is gov-archives but UK Defra/2021-census -- wrong geography and wrong records. No Canadian-archives question exists.
- **Notes:** A new eval attribution here is a first-class finding if rows later support it; do not force one.

### OMB MAX.gov FY2023 PDFs: no eval attribution — strength: n/a
- **Fingerprint type:** `honest_negative`
- **Incidents connected:** omb-max
- **Counts:** captures=26
- **Evidence:** HONEST NEGATIVE (OPEN): No SF133/MAX.gov question in the set.
- **Notes:** A new eval attribution here is a first-class finding if rows later support it; do not force one.

### Texas DSHS STI stats: no eval attribution — strength: n/a
- **Fingerprint type:** `honest_negative`
- **Incidents connected:** texas-dshs
- **Counts:** captures=0
- **Evidence:** HONEST NEGATIVE (OPEN): dsqa_891 is DSHS (regional offices) -- same agency, different task; not claimed.
- **Notes:** A new eval attribution here is a first-class finding if rows later support it; do not force one.

### DOJ OJJDP arrest stats: no eval attribution — strength: n/a
- **Fingerprint type:** `honest_negative`
- **Incidents connected:** doj-ojjdp
- **Counts:** captures=0
- **Evidence:** HONEST NEGATIVE (OPEN): No juvenile-justice/OJJDP question exists (crime rows dsqa_260/829/844 are gov-fbi tagged). The DOJ link is NOT claimable (reaffirmed).
- **Notes:** A new eval attribution here is a first-class finding if rows later support it; do not force one.

## Agent-instance markers (OPEN — no verdict forced)

### DoE vs BEA nonce value overlap — strength: weak
- **Fingerprint type:** `nonce_overlap`
- **Incidents connected:** doe-crdc, bea-api
- **Counts:** bea_truncated_17digit=109, doe_17digit=12986, exact_overlap=0
- **Evidence:** Zero exact overlap between 12986 DoE ns//100 nonces and 109 BEA ns truncated to 17 digits.
- **Notes:** OPEN: disjoint value sets lean (weakly) toward distinct agent instances/runs; but nonces are single-use by design, so zero overlap is also the null expectation. No verdict forced.

### wiki label nonce reuse across hits — strength: weak
- **Fingerprint type:** `nonce_overlap`
- **Incidents connected:** wiki-labels
- **Counts:** distinct_label_nonce_values=14, nonces_with_multiple_hits=14
- **Evidence:** 14 of 14 label-attached wiki nonce values appear on more than one hit.
- **Notes:** OPEN: same nonce on multiple hits suggests one instance minting labels in a session -- but could be wiki-ingestion duplication. Weak either way.

### nonce width differs per surface — strength: weak
- **Fingerprint type:** `nonce_shape`
- **Incidents connected:** doe-crdc, bea-api, wiki-labels
- **Counts:** widths=3
- **Evidence:** epoch-s (wiki labels) vs epoch-ns//100 (DoE) vs epoch-ns (BEA) -- same epoch-nonce family, different widths per surface.
- **Notes:** OPEN: suggestive of per-run/per-surface generator config (different instances), equally consistent with one instance switching slots. Weak.


## Summary judgments

- **Strongest provider-level evidence:** arquivo.pt as a shared agent relay across
  all 14 incident clusters (volumes reproduced exactly from our bytes) + the
  epoch-nonce family on both arquivo surfaces (DoE `zz=oai` = epoch-ns//100,
  12,986/12,986 in the Jun-17 window; BEA `zz=` = epoch-ns, 109/109 in
  Jun16-21) + the `OpenAIResearch*` DSE label grammar (3,181 wiki hits) the
  same week as the BEA registration — with zero non-OpenAI equivalents
  anywhere. (Wiki-label epoch nonces are sparse — 42 label-attached hits —
  so the label connection stands on the grammar, not the nonces.)
- **Best eval attribution per incident:** DoE → dsqa_250 (strong, confirmed).
  Weak host/task-family candidates: BEA → dsqa_319, NYSED → dsqa_059,
  CDC → dsqa_506/757, census → dsqa_862. All others OPEN.
- **Agent-instance level:** no verdict. Zero shared nonce values DoE↔BEA;
  per-surface nonce widths differ (ns//100 vs ns); all 14 label-attached wiki
  nonce values recur on multiple hits (suggestive of ingestion duplication
  as much as session reuse) — all graded weak, all OPEN.
