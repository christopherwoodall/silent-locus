# BrowseComp-Plus search-agent trajectories — 2026-10-17

Lane: `bcp-search-trajectories`. Factum batch: `1a692488a73b4a0584b7d518ed69c3a4` (exported 2026-10-17T21:58Z).

## Purpose

This lane hunts agent behavior in search-agent trajectories. A search
agent is a model that answers hard questions by calling search and
visit tools on a local document corpus. The corpus is BrowseComp-Plus
(browsecomp_plus): 830 questions, 6 model runs, 4,980 trajectories.
The hunt asks: how do search agents fail when the tools work but the
agent does not use them well?

## Sources

- Dataset: `liuqi6777/bcp_search_agent_trajectory` (HuggingFace).
- URL: https://huggingface.co/datasets/liuqi6777/bcp_search_agent_trajectory
- Revision: `af778a3994cfcb30a8a9ab5abcbcb7c7fcbf645f`.
- Retrieved: 2026-10-17T04:36:31Z. Method: https-get (curl).
- License: apache-2.0. Three sources agree: HF API tags
  (`license:apache-2.0`), cardData.license (`apache-2.0`), README
  front matter (`license: apache-2.0`). Recorded in
  `raw/LICENSE.note`.
- Files: 6 run dirs (`ds4pro`, `glm51`, `gpt-oss-120b-high`, `kimi26`,
  `qwen35-35b-a3b`, `tongyi-dr`), each `predictions.jsonl` with 830
  rows. Raw bytes cached under
  `data/lanes/bcp-search-trajectories/raw/` with per-file sha256 in
  `raw/MANIFEST.json` (bytes_match=true, sha256_match=true).
- Models (from `metadata.model_name`): deepseek-v4-pro, glm-5.1,
  openai/gpt-oss-120b, kimi-k2.6, Qwen/Qwen3.5-35B-A3B,
  Alibaba-NLP/Tongyi-DeepResearch-30B-A3B. Dataset field:
  `browsecomp_plus`.

## Method

Scout and scrape ran before this task. Three reviewers split the
runs (A: glm51 + ds4pro, B: gpt-oss-120b-high + kimi26, C: tongyi-dr
+ qwen35). Coverage: 4,980/4,980 trajectories reviewed. One
adversarial reviewer applied the kill criteria from the prompt pack.
One verifier re-checked every surviving finding against the raw
bytes. All corrections were applied to
`data/lanes/bcp-search-trajectories/verified-findings.jsonl`. The
ingest builder (`data/lanes/bcp-search-trajectories/build_bundle.py`)
re-verified every finding's byte-anchors (G1), step counts (G2), and
raw-file sha256 (G3) before writing the bundle.

Key schema facts that shaped the review:

- Rows have no question id. Trajectory id =
  `<run>:predictions.jsonl line <N>` (1-based file line).
- Reasoning lives in `metadata.model_calls[i].response.reasoning`,
  not in `messages[]`. tongyi-dr assistant messages are empty
  strings.
- Tool calls live in `model_calls[i].tool_calls`. Tool returns live
  in `messages[]` with role=tool.
- `answer` is the ground truth. `prediction` is the agent output.
  Confusing the two inverts every finding.
- Tool schema differs by run family: ds4pro/glm51/qwen35 use
  `search(query)` / `visit(docid)`; gpt-oss-120b-high/kimi26/tongyi-dr
  use `search(query)` / `visit(docid,goal)`. tongyi-dr has one
  `visit(goal,url)` outlier.
- `model_calls[].turn` is 1-based. Reviewer B cited 0-based turns;
  all were corrected +1.

## Findings

### BCP-A-001: self-echo-as-evidence — self-seeded "28 years"

- Grade: PRIMARY. Confidence: HIGH.
- Trajectory: glm51:predictions.jsonl line 266, 0-based msgs 95-114.
- Evidence: assistant msg114: "...Jason Smith spent **28 years** in
  music education. <answer>28</answer>". '28 years' occurs 3x in the
  trace, all inside the agent's own search-query strings (model_calls
  turns 36, 37, 43), never as evidence in a returned document.
- Provenance: glm51 predictions URL, retrieved 2026-10-17T02:59:07Z,
  sha256 c54a544e37464484a7ad8b38e408987ddf6c1c885304012d6a6ab1cec3158bed.
- Why interesting: The agent admits the decisive article is not in
  its corpus, then asserts the article's contents anyway. A
  self-seeded hypothesis laundered into a cited fact. Gold was 27.
  The same question in ds4pro line 266 was answered by honest
  abstention.

### BCP-A-002: evidence-blindness-at-giveup — answer in tool text, "No answer found"

- Grade: PRIMARY. Confidence: HIGH.
- Trajectory: glm51:predictions.jsonl line 12, 0-based msgs 22-87.
- Evidence: tool returns (10x): 'name: Jacqueline Cantrelle
  birth_name: Jacqueline Georgette Cantrelle birth_date: 23 09 1925
  birth_place: Paris, France'. Assistant msg85: 'Based on my
  extensive research, let me try one more targeted search to identify
  this person.' Prediction: 'No answer found.'
- Provenance: glm51 predictions URL, sha256
  c54a544e37464484a7ad8b38e408987ddf6c1c885304012d6a6ab1cec3158bed.
- Why interesting: The exact requested fact (full birth name)
  appeared 10 times in the agent's own tool returns, yet the agent
  never acknowledged the candidate and gave up. The agent mentions
  'Cantrelle' in zero non-tool messages. Exemplar instance of the
  aggregate BCP-X-001.

### BCP-A-003: reasoning-delimiter-leakage — `</think>` and DSML tag in visible channel

- Grade: PRIMARY. Confidence: MEDIUM.
- Trajectory: corpus-wide over ds4pro (830 rows). Exemplars: line 9
  (0-based msgs 4, 6), line 266 (0-based msgs[90]).
- Evidence: line 9 msgs[4]/msgs[6] end with '</think>' appended to
  assistant text. Line 266 msgs[90] ends with '</丨DSML丨answer>'.
- Provenance: ds4pro predictions URL, sha256
  98ef95fc174bdcdbba3308767e4fffa197b4dc70e94234210aafd5cadf0230af.
- Why interesting: The model's private reasoning delimiter leaks
  into the user-visible channel in 118/830 rows, and its native
  answer-control tag `<丨DSML丨answer>` in 79/830 rows, conflicting
  with the harness's `<answer>` format. Near-absent in glm51 (1
  row). A genuine distinguishing observable for model attribution.
  This is formatting behavior, not a decision TTP. Confidence is
  MEDIUM after the adversarial reframe.

### BCP-A-004: tool-protocol-misuse — invented URL plus phantom Wayback plans

- Grade: PRIMARY. Confidence: HIGH.
- Trajectory: ds4pro:predictions.jsonl line 362, 0-based msgs 43-72.
- Evidence: msgs[53]: 'The article is likely at a URL like
  `https://www.healthline.com/health/frozen-shoulder`.' msgs[57]:
  'searching for cached versions ... or using the Wayback machine.'
- Provenance: ds4pro predictions URL, sha256
  98ef95fc174bdcdbba3308767e4fffa197b4dc70e94234210aafd5cadf0230af.
- Why interesting: The agent invents a plausible URL from parametric
  memory (never grounded in any returned document) and repeatedly
  plans to use web/Wayback/cached-page tools the harness never
  provided. It does not know its own tool boundary. The invented URL
  appears in 3 tool messages only as echo of the agent's own
  queries, never as evidence.

### F-B1: tool-protocol-misuse — phantom find/watch/find_in_document calls

- Grade: PRIMARY. Confidence: HIGH.
- Trajectory: gpt-oss-120b-high, 0-based rows idx78, idx90, idx246,
  idx265, idx460, idx651, idx689, idx739 (= 1-based lines 79, 91,
  247, 266, 461, 652, 690, 740).
- Evidence: idx78 turn 10 reasoning: 'The system only provides
  search and visit. There is no find' — then TOOLCALL find {}.
  Tool return: "Error: Tool 'find' is not available in this
  environment." idx246 turn 26: find {"docid": "60046", "pattern":
  "single"}.
- Provenance: gpt-oss predictions URL, sha256
  0e943e1b0d844986beb0beed12f809dcc9dd6ec039d9534c6804ef603bd1910d.
- Why interesting: The agent emits calls to tools that do not exist
  in its harness. In the strongest case it states the tool does not
  exist in the same turn it calls it. The well-formed
  {docid,pattern} args elsewhere suggest a real in-document-search
  tool schema leaking in from a different harness. The agent
  recovers cleanly via search each time.

### F-B2: tool-protocol-misuse — raw URLs passed as corpus docid

- Grade: PRIMARY. Confidence: HIGH.
- Trajectory: gpt-oss-120b-high idx341 (= line 342), 1-based turns
  35-73; plus kimi26 idx94 (= line 95) turn 54.
- Evidence: 14 URL-as-docid visit attempts, e.g. turn 73 visit
  {"docid": "https://www.tandfonline.com/doi/pdfdirect/10.1080/17474124.2019.1685381"}
  -> "Failed to visit the docid ... Document '...' not found."
  kimi26 turn 54 reasoning: '`visit` takes a `docid` which is a
  local corpus document id. Wait, could the `docid` be a URL?
  Let's test by fetching a known URL as docid.'
- Provenance: gpt-oss predictions URL (sha256 above); kimi26
  predictions URL, sha256
  1d1e84c50615a12004ba717285c0cdbf94e41211ad798f298f2db5e19fe7a13c.
- Why interesting: gpt-oss repeats the failing pattern 14 times
  with URL variants without adapting. kimi26 runs the same
  hypothesis as one clean experiment and stops. Same error, two
  opposite repair styles. Six more gpt-oss rows show the pattern
  uncited (idx 58, 198, 302, 613, 725, 733).

### F-B3: confabulation-under-retrieval-failure — "Given knowledge anyway"

- Grade: PRIMARY. Confidence: HIGH.
- Trajectory: gpt-oss-120b-high idx457 (= line 458), turn 33 (final
  turn, 33 turns total, termination=answer).
- Evidence: final-turn reasoning: 'Let's verify. Search. ... Ok.
  Given knowledge anyway: Governor Gretchen Whitmer got her
  bachelor's degree from Michigan State University.' Zero tool
  calls follow. 'Whitmer' 0x, 'bachelor' 0x, gold string 0x across
  all tool returns.
- Provenance: gpt-oss predictions URL, sha256
  0e943e1b0d844986beb0beed12f809dcc9dd6ec039d9534c6804ef603bd1910d.
- Why interesting: The agent announces a verification plan, then
  answers from parametric memory with zero tool calls. The pivotal
  fact is entirely ungrounded in the trajectory. It happens to
  match gold, so benchmark scoring cannot see the evidence gap.

### F-B4: recovery-livelock — 31 identical queries, "We are stuck" 38x

- Grade: PRIMARY. Confidence: HIGH.
- Trajectory: kimi26 idx100 (= line 101), 1-based turns 51-89.
- Evidence: the identical query {"query": "theguardian.com/profile
  \"2009\" \"(1)\" \"2014\" \"(2)\""} issued 31 times (13 strictly
  consecutive), identical 5 results each time. Reasoning says 'We
  are stuck' 38 times. termination=incomplete, prediction 'No
  answer found.'
- Provenance: kimi26 predictions URL, sha256
  1d1e84c50615a12004ba717285c0cdbf94e41211ad798f298f2db5e19fe7a13c.
- Why interesting: Metacognition of failure with zero strategy
  adaptation — the anti-pattern of recovery. The agent knows it is
  stuck and keeps doing the identical thing.

### BCP-C-001: schema-fixation-against-evidence — self-recalled schema beats 95 rejections

- Grade: PRIMARY. Confidence: HIGH.
- Trajectory: tongyi-dr:predictions.jsonl line 741, 1-based, msgs
  2-232. Key reasoning at model_calls turn 23.
- Evidence: turn 23 reasoning: 'Actually the doc says: "type search
  = (_: { // Array of query strings. query: string[], })". That is
  correct.' Validator reply, 97 times: "[Search] Invalid request
  format: Input must be a JSON object containing a string 'query'
  field". Tally: 95 array-form calls (all rejected), 4 string-form
  calls (all succeeded), 2 missing-query calls (rejected).
- Provenance: tongyi-dr predictions URL, sha256
  4d06ffe541344d4c2e0f36f5680a3446a031403b15591887805520130a382320.
- Why interesting: The schema text does NOT appear in the harness
  system prompt (628 chars, no schema text). It appears only inside
  the agent's own reasoning. This is not a harness
  schema/validator contradiction — it is the agent trusting a
  self-recalled schema over 95 consecutive empirical rejections,
  explaining away the 4 successes as query-content effects
  ('Perhaps the tool only allows a query that includes the phrase
  "band disband"?'). Stronger than filed. This is the schema-doc
  reframe lesson: always check WHERE the schema text lives before
  blaming the harness.

### BCP-C-002: repair-without-learning — int-docid error fixed, then repeated twice

- Grade: PRIMARY. Confidence: MEDIUM.
- Trajectory: tongyi-dr:predictions.jsonl line 1, model_calls turns
  1-10. Assistant messages are empty; reasoning lives in
  model_calls.
- Evidence: turn 1 search {"query": [array]} rejected; turn 2
  string query succeeds. Turn 3 visit {"docid": 18639} (int)
  rejected ('must be a JSON object containing a string docid field
  and goal'); turn 4 string docid succeeds. The int-docid error
  recurs at turns 7 and 9, corrected again at turns 8 and 10.
- Provenance: tongyi-dr predictions URL, sha256
  4d06ffe541344d4c2e0f36f5680a3446a031403b15591887805520130a382320.
- Why interesting: The validator's precise error messages enable
  self-correction, but the correction does not stick. Error-driven
  repair without schema learning. Confidence is MEDIUM: crisp but
  mild.

### BCP-C-003: transcription-error-cascade — wrong docid transcribed and visited

- Grade: PRIMARY. Confidence: HIGH.
- Trajectory: tongyi-dr:predictions.jsonl line 351, model_calls
  turns 34-37.
- Evidence: turn 34 reasoning: 'The result #4 (Document ID: 65244)
  is interesting.' The preceding tool return lists result #4 as
  'Document ID: 98058'. 65244 never appears in any tool return
  before turn 34 — first occurrence is the agent's own reasoning.
  visit {"docid": "65244"} returns blog comment spam.
- Provenance: tongyi-dr predictions URL, sha256
  4d06ffe541344d4c2e0f36f5680a3446a031403b15591887805520130a382320.
- Why interesting: The agent transcribed the wrong document ID
  (result #4 was 98058), visited an ID that never appeared in any
  tool return, and fetched unrelated blog spam instead of the
  article it had correctly identified. Same incident as BCP-C-004;
  filed separately as the distinct wrong-ID-visit behavior.

### BCP-C-004: transcription-error-cascade — tool-blame and quote misattribution

- Grade: PRIMARY. Confidence: HIGH.
- Trajectory: tongyi-dr:predictions.jsonl line 351, model_calls
  turns 35-37.
- Evidence: turn 35: 'the search tool is returning random unrelated
  content.' Turn 36: 'The article (Document ID: 65244) mentions that
  in December 2010, a secondary school senior trolled her online'
  — real quotes from the 98058 snippet, misattributed to the
  phantom doc 65244 whose fetched content was blog spam. Turn 37:
  re-search finds the real doc.
- Provenance: tongyi-dr predictions URL, sha256
  4d06ffe541344d4c2e0f36f5680a3446a031403b15591887805520130a382320.
- Why interesting: The agent blamed the tool for its own
  transcription error, then laundered real biographical quotes from
  the correct snippet onto the phantom document. Misattribution,
  not invented text. Same incident as BCP-C-003; filed separately
  as the distinct tool-blame plus misattribution behavior.

### BCP-C-005: constraint-abandonment — ships 1913 after its own trace rejects it

- Grade: PRIMARY. Confidence: HIGH.
- Trajectory: tongyi-dr:predictions.jsonl line 21, model_calls turns
  8, 12, 25, 26, 28, 30; 43 turns total.
- Evidence: turn 8: 'So not match.' Turn 12 and 25: 'loser was
  Selby (pro 1999). So doesn't fit.' Final prediction: '**1913**
  ... most notably seen in the 2023 British Open final between Mark
  Williams and Mark Selby' with a constraint-by-constraint
  justification. Gold: 1419.
- Provenance: tongyi-dr predictions URL, sha256
  4d06ffe541344d4c2e0f36f5680a3446a031403b15591887805520130a382320.
- Why interesting: The agent's own trace records the match failing
  the break-pattern, date, and turned-pro constraints, yet it ships
  a confident, elaborately justified answer anyway. Explicit
  constraint abandonment under time pressure — not an unnoticed
  mistake.

### BCP-C-006: declared-abandonment-not-followed — "guessing docids are not helpful", then 3 more guesses

- Grade: PRIMARY. Confidence: MEDIUM.
- Trajectory: tongyi-dr:predictions.jsonl line 560, model_calls
  turns 41-53.
- Evidence: turn 41: guess docid 95321 -> GOES satellite weather
  content. Turn 42: 'Thus guess docids are not helpful.' Turns 43,
  47, 53: guesses 50684, 85000, 16254 anyway ('Docid 85000
  irrelevant. Thus trying to guess docids is futile.'). Final
  answer from parametric memory, wrong ('Art Gallery of Windsor'
  vs gold 'Plains Art Museum').
- Provenance: tongyi-dr predictions URL, sha256
  4d06ffe541344d4c2e0f36f5680a3446a031403b15591887805520130a382320.
- Why interesting: The agent explicitly documents the strategy's
  failure, then repeats it twice more anyway — abandonment declared
  but not followed. Confidence is MEDIUM: mild but crisp.

### BCP-X-001: evidence-blindness-at-giveup — 1 in 3 give-ups held the answer

- Grade: PRIMARY. Confidence: HIGH.
- Trajectory: corpus-wide aggregate. glm51 (830 rows) vs ds4pro
  (830 rows) control. Exemplar: glm51 line 12 (also BCP-A-002).
- Evidence: 81 glm51 predictions contain 'No answer found' (9.8%
  give-up rate). In 27 of those 81, the stripped gold answer
  occurs case-insensitively in the concatenated tool-return text
  (23/81 case-sensitive). Distinctive multi-occurrence exemplars:
  line 12 'Jacqueline Georgette Cantrelle' 20x/10 tool msgs; line
  85 'Chris Jericho' 18x/8; line 93 'Queen Marie of Romania' 26x/7;
  line 313 'Svetlana Gromenkova' 20x/7; line 338 'Norman Naimark'
  13x/12; line 459 'Pirates of the Caribbean' 23x/9; line 672
  'Jagannatha Hora' 17x/4. ds4pro: 6 give-ups (0.72%), 2 of 6 with
  answer in tool text.
- Provenance: glm51 + ds4pro predictions URLs, sha256
  c54a544e37464484a7ad8b38e408987ddf6c1c885304012d6a6ab1cec3158bed
  and 98ef95fc174bdcdbba3308767e4fffa197b4dc70e94234210aafd5cadf0230af.
- Why interesting: One in three of glm51's give-ups had the exact
  gold answer sitting in its own tool returns. The ds4pro control
  is too small-n for a strong cross-model claim, but glm51's
  absolute rate plus its 13.6x higher give-up rate stands as a
  systematic evidence-use gap. ~9 of the 27 are short or noisy
  strings (e.g. line 5 'Red', line 40 '2004'); the listed seven
  are the distinctive multi-occurrence failures.

## Killed

Stage 1 (adversarial review): 0 kills. Three near-kill
adjudications kept with changes: BCP-A-003 reframed as
model-formatting behavior (HIGH->MEDIUM); BCP-C-002 kept as
repair-without-learning (HIGH->MEDIUM); BCP-C-006 kept as
declared-abandonment-not-followed (HIGH->MEDIUM).

Stage 2 (verifier): 0 kills. 12 of 14 surviving candidates needed
corrections (quotes, step ranges, counts, one major reframe on
BCP-C-001); all applied in verified-findings.jsonl.

Reviewer self-kills (spot-checked 3/3, all confirmed correct):

- Reviewer A, ds4pro line 199 "Scott A. Ebers": name occurs once
  inside garbled OCR text — too weak to claim blindness. Kill
  correct.
- Reviewer B, kill 7 (gpt-oss idx 416): cited URL and claims
  verified present in the full tool return — honest citation, not
  fabrication. Kill correct.
- Reviewer C, tongyi-dr row 21 alternate reading: the 2023 British
  Open details ARE in the tool returns — killed as fabrication,
  correctly refiled as constraint abandonment (BCP-C-005).

## Overlap

Pre-ingest dedup: direct scans of `data/records/` for
`bcp_search_agent_trajectory`, `liuqi6777`, all 15 finding ids, and
the lane tag `bcp-search-trajectories` returned zero hits.
Reviewers independently checked for overlap (none found).
`factum match --text` fuzzy probes were attempted but timed out
under sibling-fleet writer-lock contention; direct scans are the
authoritative oracle. 0 overlaps. 0 records skipped.

## Open questions

1. The ds4pro control in BCP-X-001 is too small-n (6 give-ups) for
   a strong cross-model claim. Does glm51's evidence-use gap hold
   against qwen35-35b-a3b, which reviewers did not deep-read?
2. F-B1's well-formed {docid,pattern} args suggest an
   in-document-search tool from a different harness. Which harness
   family does that schema come from?
3. BCP-A-003's `</think>` leakage is a model-attribution
   observable. Does the same leakage appear in other DeepSeek
   trajectory corpora?
4. tongyi-dr assistant messages are empty strings; all reasoning
   is in `model_calls`. Does the evaluation harness even read the
   message channel, or is `messages[]` vestigial here?
5. The qwen35-35b-a3b run was triaged by Reviewer C but produced
   zero findings. Is qwen35 genuinely cleaner, or was the triage
   shallow?

## Factum records

63 records, one batch: 1 source, 1 run, 1 dataset.snapshot, 15
intel.behavior observations, 15 behavior.tool_sequence
observations, 30 edges (run -related_to-> tool_sequence; finding
-supports-> tool_sequence). Every record carries
tags.lane=bcp-search-trajectories. Claims cite observations, never
sources. Build: `data/lanes/bcp-search-trajectories/build_bundle.py`
(G1 quote byte-anchors, G2 step counts, G3 raw sha256 all pass).
