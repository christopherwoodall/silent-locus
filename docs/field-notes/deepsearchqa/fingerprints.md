# DeepSearchQA question fingerprints (hunt primitives)

How to hunt: grep agent-traffic logs, urlquery reports, Arquivo.pt capture
parameters, wiki pages, and search-query trails for the exact strings below
(`grep -F`, fixed-string). These are distinctive multi-word phrases taken
verbatim from the published question set — they do not occur in ordinary text.

qid scheme: `dsqa_<NNN>` = **0-based** row index in DSQA-full.csv order.
Verified: Transluce's "dsqa_250" == row index 250, the June-17 DoE
civilrightsdata.ed.gov question (see collections/deepsearchqa/README.md).

Full rows (verbatim question text + tags) live in
`collections/deepsearchqa/data/questions.jsonl` — 900 rows, 49 with a
`gov-data` tag. Use it as the authoritative fingerprint list.

## Priority fingerprints

### F1 — the confirmed DoE incident (dsqa_250)
Question verbatim (Education / Single Answer):
> "Using data from civilrightsdata.ed.gov for the 2017-2018 school year,
> determine which of the following states - South Carolina, North Carolina,
> Georgia, or Virginia - had the highest ratio of full-time equivalent school
> counselors to students reported as victims of race-related harassment or
> bullying."

Grep patterns (fixed-string, any one is enough):
```
full-time equivalent school counselors to students reported as victims of race-related harassment or bullying
civilrightsdata.ed.gov
```

### F2 — CDC WONDER mortality (dsqa_506)
> "For the years 2018-2023 which census region of the united states had the
> lowest number of weekend deaths in Inpatient medical facilities for 15-24
> year olds attributed to drug or alcohol induced causes and verified by
> autopsy, according to https://wonder.cdc.gov/?"

```
weekend deaths in Inpatient medical facilities
wonder.cdc.gov
```

### F3 — BEA GDP/income (dsqa_319)
> "Based on data available at bea.gov, tell me which of the following
> states–California, Florida, New York, Texas–exceeded both 1,000,000 in real
> gross domestic product (GDP) (millions of chained 2017 dollars) and
> 1,250,000 in disposable personal income (millions of current dollars) in
> 2020."

```
millions of chained 2017 dollars
disposable personal income
bea.gov
```

### F4 — NYSED graduation rates (dsqa_059)
> "Based on information located on data.nysed.gov, consider ny state
> graduation rate data for high school students as of August 2023. ..."

```
data.nysed.gov
graduation rate data for high school students as of August 2023
```

### F5 — Youth Risk Behavior / CDC WONDER (dsqa_757)
> "According to the information linked in wonder.cdc.gov find the youth risk
> behavior trends ... Youth Risk Behavior Survey Data Summary & Trends Report
> 2013-2023 ..."

```
Youth Risk Behavior Survey Data Summary & Trends Report 2013-2023
Experiencing Violence section
```

### F6 — trade.gov tourism + national parks (dsqa_684)
> "Which of the 10 most visited states by overseas visitors in 2023 (based on
> trade.gov data) have no congressionally designated National Park's within
> their borders..."

```
10 most visited states by overseas visitors in 2023
no congressionally designated National Park
```

## Hunting notes

- Transluce attributed the DOJ/OJJDP incident only "plausibly" to another
  DeepSearchQA question; **no OJJDP-specific question exists in the set** (0
  hits for "ojjdp"/"juvenile justice" — crime-flavored rows dsqa_260, dsqa_829,
  dsqa_844 are tagged `gov-fbi`, not justice-dept). Do not claim a DOJ match.
- Also valuable as search-term fingerprints: bare `.gov` hostnames rarely seen
  outside these questions (e.g. `tea.texas.gov`, `irma.nps.gov`,
  `planetarynames.wr.usgs.gov`).
- The whole set is Apache-2.0, public, ungated — safe to redistribute within
  the repo.
