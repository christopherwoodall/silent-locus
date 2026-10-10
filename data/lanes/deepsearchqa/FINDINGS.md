# Findings — deepsearchqa lane

## Dataset shape (OBSERVED)

- 900 questions. 17 categories. Largest: Politics & Government (148),
  Finance & Economics (132), Geography (95), Education (94), Health (92),
  Science (90).
- Answer types: 584 Set Answer, 316 Single Answer.
- Question IDs are the 0-based CSV row index (`dsqa_N`). This was checked
  against Transluce's public quote of dsqa_250 (row 250 text matches).

## Join keys to incidents (see `join_keys.md` for full detail)

- **dsqa_250 → DoE civilrightsdata.ed.gov incident: CONFIRMED (UPSTREAM).**
  Transluce confirmed the link. Question record:
  `observation_933af451f14248d3821f5871bbc2fa02`. Join keys:
  `civilrightsdata.ed.gov`, `survey_Year_Key=9`, `Measure_Id=130`,
  `State_Id` in {11, 28, 41, 46}. Incident burst: 2026-06-17, 200,000+
  Arquivo.pt captures, ending in a failed `State_Id=1 OR 1=1` SQL-injection
  probe.
- **dsqa_260 → DOJ/OJJDP incident: CANDIDATE, hedged (INFERENCE).**
  Transluce said the retrieved data "plausibly matches a DeepSearchQA
  question" but named no question ID. A full keyword sweep of all 900
  questions found no question that names OJJDP or a 1980–2020 robbery table.
  dsqa_260 is the best byte-level candidate (FBI + National Safety Council,
  1990–2020, robbery among named offenses). Question record:
  `observation_abe7578f9a3f4916a3bde159a740914c`. Do not treat the
  candidate link as an attribution.
- Negative space: no per-question timestamps exist in the dataset, so timing
  corroboration across questions cannot be built from the dataset alone.

## Hunt implication (INFERENCE)

DeepSearchQA is the best fingerprint source among the sibling benchmarks:
900 plain-text hand-made questions with rare entities. BrowseComp is a poor
fingerprint source by design (plain text withheld, encrypted). GAIA,
WebWalkerQA, WideSearch, and xbench/DeepSearch are the natural next
enumerations. See `sibling_benchmarks.md`.
