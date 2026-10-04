# Eval-linkage hunt — DeepSearchQA question ↔ incident trace matching (2026-10-03)

**Method:** the dsqa_250 → DoE template (Transluce): match benchmark question entities/parameters against agent traffic. Two tiers: verbatim phrase (`grep -F`) and entity-level (target + task parameters).

**Corpora swept for verbatim phrases:** `/tmp/jdwiki/*/evidence.tsv` (9 task dirs), `collections/fake-org/data/hits.jsonl` (5,862 pattern hits), `data/2026-10-01-arquivo-pt/raw/*.cdx.jsonl.gz` (14 incident files).

## Verbatim results: zero

| Phrase (qid) | jdwiki | fake-org | arquivo raw | Verdict |
|---|---|---|---|---|
| "full-time equivalent school counselors" (dsqa_250) | 0 | 0 | 0 | — (confirmed via Transluce's parameter match, not verbatim) |
| "ACS 5-year estimates subject table" (dsqa_898) | 0 | 0 | 0 | NONE |
| "millions of chained 2017 dollars" (dsqa_319) | 0 | 0 | 0 | NONE |
| "weekend deaths in Inpatient medical facilities" (dsqa_506) | 0 | 0 | 0 | NONE |
| "Youth Risk Behavior Survey Data Summary" (dsqa_757) | 0 | 0 | 0 | NONE |
| "disposable personal income" (dsqa_319) | 0 | 0 | 0 | NONE |

No new verbatim link. dsqa_250 → DoE remains the only confirmed linkage (via Transluce's parameter mapping: survey_Year_Key=9, Measure_Id=130, State_Id values).

## Entity-level results

| Incident | Candidate qid | Match basis | Grade | Evidence |
|---|---|---|---|---|
| DoE civilrightsdata Jun 17 | dsqa_250 | Transluce parameter match | **CONFIRMED** | Prior work; tag `incident-match-doe-20260617` |
| BEA API Jun 16–18 | dsqa_319 | BEA captures hit SAINC4 (personal income) API 11–12× w/ samplekey; question needs disposable personal income + GDP | PLAUSIBLE (weak) | `bea-api.cdx.jsonl.gz`: 3,006 captures, 12 GETDATA (SAINC4), 6 GETDATASETLIST; no SAGDP/GDP table, no 2020 |
| Census ACS Jun 17 | dsqa_898 | Question: ACS 5-year subject table, Galveston TX age groups 2012. Incident pulled `acsdt1y2022-b16001.dat` (1-yr detailed table, language-at-home) | PLAUSIBLE (weak) | Target family (Census ACS) matches; entities don't (B16001 ≠ subject table; 2022 1-yr ≠ 2012 5-yr) |
| Census ACS Jun 17 | dsqa_862 | FL counties + BEA GDP (census.gov + bea.gov) | PLAUSIBLE (weak) | Dual-family overlap only; no entity match |
| CDC WONDER Jul 18 | dsqa_506 / dsqa_757 | WONDER mortality / YRBS entities vs WONDER data-request incident | PLAUSIBLE (target only) | **Our `cdc-wonder.cdx.jsonl.gz` is EMPTY (0 records)** — cannot assess locally; no verbatim |
| NY school enrollment May 17 | dsqa_059 | data.nysed.gov domain match | PLAUSIBLE (weak) | `nysed-enrollment.cdx.jsonl.gz`: 718 captures, **0** graduation/dropout URLs — homepage re-saves only |
| DOJ/OJJDP May 30–31 | dsqa_260 | Robbery stats 1990–2020 (FBI/NSC) vs incident's 1980–2020 robbery table via OJJDP | NONE (borderline) | Question is presidential-first-year comparison, not OJJDP arrest stats |
| DOJ/OJJDP May 30–31 | — | Juvenile-justice question search | NONE | **Re-verified full 900: no "juvenile", no "ojjdp", no "delinquen". Prior "not claimable" verdict stands.** |
| SEC county.json Jun 18 | — | sec.gov/crowdfund/regcf/county.json search | NONE | No SEC crowdfunding question exists (dsqa_163 is EDGAR CIK lookup — different) |
| Australian cluster (AIHW/Medicare/BOCSAR/Vic/NPWS) | dsqa_304 / dsqa_382 | AEC elections / ABS marriage stats | NONE | Incident targets are health/crime/fire data; no elections/marriage-stats match |
| CAL-ACCESS, KansasMemory, MD ed stats, TX DSHS, IL IQuery, OMB MAX, Navy, LAC | — | Domain/entity scan of all 49 gov-data questions | NONE | No matching questions (dsqa_065 tea.texas.gov ≠ TX DSHS STI stats) |

## Sibling benchmarks (BrowseComp/GAIA/AssistantBench)

**Not held locally.** Per `data/2026-10-01-deepsearchqa/sibling_benchmarks.md`: BrowseComp plaintext is intentionally encrypted (anti-leakage by design); GAIA is gated on HF; none are deep-pulled in this repo. DeepSearchQA (900 plaintext questions) is the only fingerprintable set. No matching run possible.

## Tallies

- **CONFIRMED: 1** (dsqa_250 → DoE, prior work)
- **PLAUSIBLE: 5** (dsqa_319→BEA, dsqa_898→Census, dsqa_862→Census/BEA, dsqa_506/757→CDC WONDER, dsqa_059→NY) — all weak, target-family level only, zero verbatim
- **NONE: everything else**, including SEC (no question exists), the Australian cluster, and DOJ/OJJDP (re-verified unclaimable)

## Strongest new link

**dsqa_319 → BEA incident (PLAUSIBLE, weak).** Of all candidates it has the only entity-level overlap beyond bare domain: the June 16–18 BEA traffic includes genuine `apps.bea.gov/api/data` GETDATA calls against TableName=SAINC4 (regional personal income) — the income half of dsqa_319's GDP+disposable-personal-income question. Caveats that keep it at PLAUSIBLE: only 11–12 such calls out of 3,006 captures (rest are page captures + API-key registration attempts), UserID=samplekey (probe, not real key), no GDP table (SAGDP) observed, sample years 2013 not 2020, zero verbatim. It is a lead for targeted follow-up (sweep BEA-adjacent urlquery reports for GDP-table parameters), not a linkage claim.

## Notes

- The confirmed dsqa_250 case worked through *task parameters* (survey_Year_Key, Measure_Id, State_Id), not verbatim text. Future linkage hunts should prioritize parameter/entity extraction from traffic over phrase grep — verbatim text appears nowhere in any swept corpus.
- The empty `cdc-wonder.cdx.jsonl.gz` is itself a finding: our Arquivo lane holds no CDC WONDER captures despite the July 18 incident — a collection gap, not evidence of absence.
