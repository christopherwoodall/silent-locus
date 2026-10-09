# Task-family JOIN KEY map — DeepSearchQA questions → Transluce us-canada-gov incidents

Deliverable for sibling lanes: question ID → distinctive entities / URLs / query
parameters → incident. Keep-all; no invented IDs.

## 1. dsqa_250 → DoE civilrightsdata.ed.gov incident (CONFIRMED by Transluce)

**Question text (verbatim from row 250 of DSQA-full.csv):**

> Using data from civilrightsdata.ed.gov for the 2017-2018 school year, determine which of the following states - South Carolina, North Carolina, Georgia, or Virginia - had the highest ratio of full-time equivalent school counselors to students reported as victims of race-related harassment or bullying.

- Category: Education · Answer type: Single Answer · Gold answer: North Carolina

**Distinctive entities/URLs (join keys):**
- `civilrightsdata.ed.gov` (domain string in question text)
- `survey_Year_Key=9` (question-relevant: 2017–2018 school year mapping)
- `Measure_Id=130` (question-relevant: race-based bullying victims)
- `State_Id` ∈ {11, 28, 41, 46} (question-relevant: SC=11, NC=28, GA=41, VA=46)
- `oai*`-prefixed request tags (10,000+ observed requests; agent self-marking)

**Incident burst window (from grading note):** 2026-06-17; 200,000+ Arquivo.pt
captures; 40-second fuzzing ladder (`State_Id=0,-1,99,999,"1,2",empty,1&2,1,2,1%2C2`)
immediately preceding the `State_Id=1 OR 1=1` SQL-injection probe. Failed; DoE:
"no evidence of any impact."

**Temporal note:** dataset last_modified 2025-12-17 predates the incident by ~6
months — consistent with eval-task-driven probing. No per-question added dates
exist in the dataset, so no finer temporal alignment is possible for this
question.

## 2. Robbery-table question → DOJ/OJJDP incident (CANDIDATE — hedged)

**Transluce's linkage is explicitly hedged:** "The retrieved data, including a
1980–2020 robbery table, plausibly matches a DeepSearchQA question." They name
no question ID. An exhaustive keyword sweep of all 900 questions found **no
question mentioning OJJDP, the Statistical Briefing Book, or a 1980–2020
robbery table**. Best candidate from the bytes:

**dsqa_260 (candidate):**

> According to FBI and National Safety Council Statistics, in the timeframe of 1990-2020, for which President's first year in office after the election (including the first year of their second term) did incidents of aggravated assault, robbery, motor vehicle theft, and motor vehicle deaths decline?

- Category: Politics & Government · Answer type: Set Answer · Gold answer: Obama 2009, Obama 2013

**Distinctive entities/URLs (join keys):**
- `FBI` + `National Safety Council` statistics (dual source)
- Offenses named: aggravated assault, robbery, motor vehicle theft (+ motor vehicle deaths)
- Timeframe: 1990–2020; first-year-of-term comparison frame

**Incident burst window (from grading note):** 2026-05-30 → 2026-05-31; automated
workflow sought public FBI arrest statistics through OJJDP; legacy URLs
redirected; workflow retrieved the legacy table (incl. a **1980–2020 robbery
table**) by adding an **encoded parent-directory segment** (`../` traversal
via URL encoding). Retrieval succeeded — no hacking observed, just aggressive
gray-area technique.

**Caveats (honest):**
- Timeframe mismatch: question says 1990–2020; retrieved table is 1980–2020.
- Source mismatch: question names FBI + National Safety Council; incident
  traffic went through OJJDP (DOJ's Office of Juvenile Justice and Delinquency
  Prevention, whose Statistical Briefing Book hosts long-window arrest tables).
- The candidate link is *behaviorally* plausible (agent hunting long-window
  robbery stats lands on OJJDP's legacy table), but the byte-level fingerprint
  for a dedicated OJJDP robbery question is **absent** — Transluce's "plausibly
  matches" is not an attribution.

**Temporal note:** OJJDP burst (May 30–31) precedes the DoE burst (Jun 17) by
~2.5 weeks; both postdate the dataset. The two mapped questions sit 10 rows
apart (dsqa_250, dsqa_260) — ordering is category-interleaved, so this
adjacency is weak evidence at best; do not treat it as a join key.

## Other robbery-adjacent questions (negative space for sibling lanes)

- **dsqa_89** (Geography, Set Answer): Toronto/Vancouver robbery+homicide+sexual
  offenses via data.torontopolice.on.ca and vpd.ca — matches the LAC/Toronto
  geography, but no incident maps to it in this report set.
- **dsqa_591** (Other, Set Answer): WA CrimeStats NIBRS arrests (murder, robbery,
  kidnapping, forcible sex crimes) — no mapped incident.

## Temporal alignment summary (steering request)

| Question | Dataset timing signal | Incident burst | Alignment |
|---|---|---|---|
| dsqa_250 | reference window 2017–2018; repo published 2025-12-17 | 2026-06-17 | ✅ consistent: dataset predates incident; query params (survey_Year_Key=9, Measure_Id=130, State_Id 11/28/41/46) encode exactly the question's distinctive entities |
| dsqa_260 (candidate) | reference window 1990–2020 | 2026-05-30/31 | ⚠️ behavioral plausibility only; timeframe/source mismatches; no OJJDP fingerprint in question text |

**Flag:** The strongest temporal signal is negative space — the dataset carries
no per-question timestamps, so multi-question timing corroboration cannot be
built from the dataset alone. If future lanes find per-question or
burst-adjacent signals (e.g. Arquivo.pt capture timing vs. Kaggle leaderboard
release), they belong here.
