# Findings — 2026-09-28-pxweb-national-stats

Lane N (2026-09-28 night watch): national-statistics-API venues as agent task targets.
12 legacy events ingested as 14 Factum records (batch `27d46f68bec9457880e3e6b99a92af1f`).

## Observed venues

- UK ONS Cantabular API (Census 2021 table TS030) behind 4 agent-created
  rmn.re shortlinks, with click counts 44/36/33/30 showing real use.
  [OBSERVED — `observation_be709131e04a4202b9f3acd9ebc1b50c`,
  `observation_b7091ea38d5b483090158ba46560c721`,
  `observation_6cb833577277448081565b8cfde40d71`,
  `observation_178f1883948a4ff8abe877202d76f568`]
- Statistics Iceland PX-Web table URL in a "Links for research" paste;
  px.hagstofa.is/pxen/ resolves to the live public PxWeb UI.
  [OBSERVED — `observation_0cb65690fc9349fb9fcc57acffb5dacd`]
- pxweb.nso.gov.vn (Vietnam GSO PX-Web) as HTTP referrer on the
  goto.unm.edu/7t6-o+ shortener stats page; proxied queries ran through
  jqp/pure.md/md.succ.ai/r.jina.ai; peak day 2026-06-18.
  [OBSERVED — `observation_23f92e0ff2c147af8f80ef8360af9e93`]
- DataUSA tesseract API (ipeds_admissions cube) laundered through pure.md by
  Clark-family research agents (3 distinct university drilldowns).
  [OBSERVED — `observation_950f07a011844c20b9f71d95484df751`,
  `observation_51c1538560b54f8cab9d0bf0cdf8982d`,
  `observation_5960a353584649378766f1b7f7e8ca5e`]
- api.datausa.io is the dominant structured-data venue in the wiki corpus
  (1,914 tesseract/data.jsonrecords mentions).
  [OBSERVED — `observation_d442548608f642f9ad301ef7710459e4`]
- api.census.gov (ACS5/ACS1/PUMS/Decennial-PL) is a core stats venue in wiki
  task families (125 docs).
  [OBSERVED — `observation_457d45fe02a74dae82af7cf0f43c3dc8`]

## Negative result

Theory-of-mind predicted venues (World Bank, FRED, BLS, BEA, Nordic PX-Web,
Statbank Denmark, ABS) returned zero hits across all 8 swept indices.
[OBSERVED — `claim_b18fc676ad5e4f76aef30071e5edec9a`,
`run_1a005e2f4aee4cbfaade529abb25c4ea`]

Source bundle: `source_011897b6a88046bea139ec726eecddcd`
(events.jsonl, legacy path evidence/2026-09-28-pxweb-national-stats/).
