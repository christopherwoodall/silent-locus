# BrowseComp-Plus search agents: agents that obey their memory of the tool, not the tool itself

**Status: DRAFT ONLY. Do not submit. (Transluce filing freeze in force, 2026-10-16.)**

## 1. Summary

Five verified findings show search agents fixating on a self-held tool schema instead of the harness's actual behavior: one agent trusted a recalled `query: string[]` schema through 95 consecutive rejections, explaining away its 4 successes as query-content effects; another repaired an int-docid error twice and then made it twice more; a third declared random docid guessing useless, then guessed twice more; a fourth emitted calls to a `find` tool in the same turn it stated the tool does not exist; a fifth passed raw URLs as corpus docids 14 times without adapting — while a kimi26 agent tested the same hypothesis once, cleanly, and stopped. The shared mechanism: a prior-held schema (recalled doc, another harness's toolset, a web mental model) overrules 95+ empirical corrections.

## 2. Corpus and counting unit

- Dataset: `liuqi6777/bcp_search_agent_trajectory` (BrowseComp-Plus questions, Apache-2.0), pinned revision `af778a3994cfcb30a8a9ab5abcbcb7c7fcbf645f`, retrieved 2026-10-17.
- Full corpus: 4,980 trajectories (830 questions x 6 search agents). This writeup reviews the 15 verified PRIMARY findings of the lane and uses 5 of them.
- Counting unit: 5 findings across 5 trajectories (BCP-C-001/002/006 on tongyi-dr rows 741/1/560; F-B1/F-B2 on gpt-oss-120b-high rows idx78/341; F-B2 also cites one kimi26 trajectory).
- Terms: "schema fixation" = the agent keeps acting on its remembered tool interface despite repeated error feedback. "Harness" = the software running the agent. The available tools here are `search` and `visit`; the validator returns plain-text format errors.

## 3. What happened

### BCP-C-001 (tongyi-dr): a self-recalled schema survives 95 rejections

At row 741, the agent called `search` with `query` as an array 95 times. Every array call was rejected:

"[Search] Invalid request format: Input must be a JSON object containing a string 'query' field"

Four string-form calls all succeeded; two calls with the query field missing were rejected. Zero array calls ever succeeded. The agent kept the array form and explained away the successes as query-content effects (model_calls turn 23):

"...failing for all queries except that one. Perhaps the tool only allows a query that includes the phrase "band disband"? Or maybe the search index is limited and we need to include something else? Let's ..."

Its justification was a schema doc it recalled mid-reasoning:

"Actually the doc says: "type search = (_: { // Array of query strings. Include multiple complementary search queries in a single call. query: string[], })". That is correct."

The verifier reframed the original review: that schema text does NOT appear in the harness system prompt (628 characters, no schema text anywhere). It appears only inside the agent's own reasoning. The phenomenon is stronger than first reported: the agent trusted a self-recalled (possibly invented) schema over 95 consecutive empirical rejections, burning most of its 235-message budget on a contradiction of its own making.

### BCP-C-002 (tongyi-dr): repair that does not stick

At row 1, the validator's precise errors let the agent self-repair fast. Turn 1: `search` with array query rejected. Turn 2 reasoning: "The tool expects an object with a "query" field containing string. We gave correct format? Actually we passed an array of strings as query, but spec: query is a single string. Coul..." — then a string query succeeds. Turn 3: `visit {"docid": 18639}` (int) rejected: "[Visit] Invalid request format: Input must be a JSON object containing a string 'docid' field and 'goal'". Turn 4: string docid succeeds.

Then the int-docid error recurred at turns 7 and 9, corrected again at turns 8 and 10. The correction works; the schema learning does not persist even within the same trajectory. Confidence MEDIUM: crisp pattern, mild significance. (Citations are model_calls turns, not messages — tongyi-dr assistant messages are empty strings.)

### BCP-C-006 (tongyi-dr): abandonment declared, then repeated

At row 560, with search failing, the agent started guessing docids. Turn 41 reasoning:

'Search broken. Try using "visit" on docid likely to have info about Bank of Montreal building. Maybe docid 72345? Not sure. But perhaps there is a docid for "Bank of Montreal (Windsor)". Let's try a guess: docid 95321?'

It visited 95321, not 72345. The tool answered: "Successfully visited the docid 95321. ... Lockheed Martin has completed assembly of NOAA's GOES-R weather satellite ..." — irrelevant. Turn 42 reasoning: "The docid 95321 is about GOES satellite; irrelevant. Thus guess docids are not helpful."

Then the agent guessed anyway at turns 43 (50684), 47 (85000), and 53 (16254): "Docid 85000 irrelevant. Thus trying to guess docids is futile." The abandonment was declared and not followed. The final prediction answered from parametric memory — "Art Gallery of Windsor" — against gold "Plains Art Museum". Confidence MEDIUM. The docid space is treated as enumerable; randomness is preferred over rethinking search.

### F-B1 (gpt-oss-120b-high): calling the tool it just said does not exist

Eight trajectories show calls to `find`, `watch`, or `find_in_document` — tools not in this harness (available: search, visit). The strongest instance, idx78 turn 10, states the absence and calls it anyway:

REASONING: "(We need to use a find tool? The system only provides search and visit. There is no find, but I can search again for "Opium: A Portrait of the Heavenly Demon"."

TOOLCALL: `find {}`

TOOL RETURN: "Error: Tool 'find' is not available in this environment. Available tools: [search, visit]. Please use only the available tools to continue."

Elsewhere the calls are well-formed for a different harness: idx246 turn 26 `find {"docid": "60046", "pattern": "single"}`, idx739 turn 27 `find_in_document {"docid": "1620", "snippet": "rapid"}`. The well-formed `{docid, pattern}` shape suggests a real in-document-search tool schema leaking in from another harness. The agent recovered via search each time. (Rows: idx78, idx90, idx246, idx265, idx460, idx651, idx689, idx739; verifier corrected all turn numbers to 1-based.)

### F-B2 (gpt-oss-120b-high + kimi26): URLs as docids — no adaptation vs one clean test

At gpt-oss idx341, the agent passed raw web URLs as the `docid` argument to `visit` 14 times across turns 35-73 (tandfonline pdfdirect, PMC, europepmc, doi.org, ebi.ac.uk variants), never adapting:

visit {"docid": "https://www.tandfonline.com/doi/pdfdirect/10.1080/17474124.2019.1685381"} -> "Failed to visit the docid ... Error: Document '...' not found."

In contrast, kimi26 idx94 turn 54 explicitly hypothesized and tested the tool's semantics once:

"...`visit` takes a `docid` which is a local corpus document id.

Wait, could the `docid` be a URL? Let's test by fetching a known URL as docid. For example, `visit` with docid "https://en.wikipedia.org/wiki/Main_Page"." -> "[visit] Document 'https://en.wikipedia.org/wiki/Main_Page' not found."

One clean experiment, clean failure, no repetition. Same hypothesis, opposite adaptation behavior.

## 4. Evidence

**BCP-C-001.** Trajectory `tongyi-dr:predictions.jsonl` line 741 (1-based), msgs 2-232; key reasoning at model_calls turn 23. Source file: `tongyi-dr/predictions.jsonl`, sha256 `4d06ffe541344d4c2e0f36f5680a3446a031403b15591887805520130a382320`. Evidence link: `https://huggingface.co/datasets/liuqi6777/bcp_search_agent_trajectory/resolve/af778a3994cfcb30a8a9ab5abcbcb7c7fcbf645f/tongyi-dr/predictions.jsonl`. Confidence HIGH. Byte-exact tally: 95 array-form calls (all rejected), 4 string-form (all succeeded), 2 missing-field (rejected), 0 array ever succeeded.

**BCP-C-002.** Trajectory `tongyi-dr:predictions.jsonl` line 1 (1-based), model_calls turns 1-10 (assistant messages empty). Same source file and sha256. Confidence MEDIUM. Tool-call sequence byte-confirmed: turn 1 array-query rejected -> turn 2 string-query succeeds; turn 3 int-docid rejected -> turn 4 string-docid succeeds; int-docid recurs turns 7, 9; corrected turns 8, 10.

**BCP-C-006.** Trajectory `tongyi-dr:predictions.jsonl` line 560 (1-based), model_calls turns 41-53. Same source file and sha256. Confidence MEDIUM. Verifier correction: cited reasoning is at turns 41-42 (not "msgs 82-84"); the visited id was 95321, not the mused-about 72345; repeats at turns 43, 47, 53 after the explicit "not helpful" conclusion.

**F-B1.** Trajectories `gpt-oss-120b-high:predictions.jsonl` 0-based rows idx78 (turn 10), idx90 (turn 10), idx246 (turn 26), idx265 (turn 21), idx460 (turn 9), idx651 (turn 7), idx689 (turn 51), idx739 (turn 27). Source file: `gpt-oss-120b-high/predictions.jsonl`, sha256 `0e943e1b0d844986beb0beed12f809dcc9dd6ec039d9534c6804ef603bd1910d`. Evidence link: `https://huggingface.co/datasets/liuqi6777/bcp_search_agent_trajectory/resolve/af778a3994cfcb30a8a9ab5abcbcb7c7fcbf645f/gpt-oss-120b-high/predictions.jsonl`. Confidence HIGH. All 8 phantom calls confirmed; verifier corrected turn numbers to 1-based.

**F-B2.** Trajectories `gpt-oss-120b-high:idx341` (0-based row), 1-based turns 35, 40, 43, 49, 50, 56, 59, 60, 61, 64, 65, 67, 70, 73 (14 URL-as-docid attempts); plus `kimi26:idx94` (0-based row), 1-based turn 54. kimi26 file: `kimi26/predictions.jsonl`, sha256 `1d1e84c50615a12004ba717285c0cdbf94e41211ad798f298f2db5e19fe7a13c`. Confidence HIGH. 14 attempts confirmed without adaptation; kimi26 quote verbatim.

Review was read-only. No trajectory was replayed and no attack was reproduced.

## 5. Novelty

Checked: local Transluce findings lane (129 files; findings 115-182 included) searched for "browsecomp", "search agent", "fabricat", "schema". The hits are unrelated (#81/#148 ntfy.sh benchmark bursts; #138/#141 eval-agent CAPTCHA fights; #131 wild infra economy; #173 fleet infrastructure). Nothing found covers tool-schema fixation in search agents — agents trusting self-recalled schemas over validator feedback, or emitting calls to nonexistent tools mid-sentence denying their existence. The general phenomenon of LLM tool misuse is documented in the literature, so this is new byte-verified evidence of a known class, not a first discovery.

## 6. Why it matters

The harness is the agent's reality, and the validator's error messages are the cheapest possible teacher — precise, immediate, byte-level. BCP-C-001 shows that teacher losing to a memory: 95 identical rejections could not dislodge one recalled sentence, and the agent instead rewrote its theory of the 4 successes to protect the schema. That is not a capability gap; it is a belief-update failure, and it burned most of a 235-message budget. For harness design the lesson is concrete: when the agent holds a wrong schema, error text alone does not fix it (BCP-C-002 shows even a correct repair does not persist). F-B1 adds the deployment version: an agent whose prior harness had a `find` tool will call it here, correctly state it does not exist, and call it anyway — a cross-harness schema leak that a capabilities manifest (machine-readable tool list the model is forced to consult) would cut. F-B2's contrast pair is the control: kimi26 shows the healthy behavior — one explicit hypothesis, one test, clean stop.

## 7. Uncertainties

- A non-malicious reading: the agents behave like a user with stale documentation. BCP-C-001's "doc" may be a real schema the model saw in training for a sibling system; trusting training memory over 95 errors is a prior-strength problem, not defiance. Ruled out as harness deception — the harness prompt genuinely has no schema text.
- Cannot rule out that part of BCP-C-006's guessing is rational exploration under a dead search tool rather than fixation: probing the ID space once is a legitimate fallback. The finding's weight rests on the declared-abandonment-then-repeated pattern (turns 43, 47, 53 after "not helpful" / "futile"), not on the first guess.
- BCP-C-002 confidence is MEDIUM: a mild observation — repair-without-learning within 10 turns. It earns its place as the lower bound of the family (fixation-lite), not as a standalone claim.
- F-B1's cross-harness leak is an internal attribution hypothesis (the well-formed `{docid,pattern}` args suggest another harness's schema) — not confirmed by the bytes; labeled as hypothesis.

## 8. Impact

- Harm: **No/negligible harm.** Sandbox benchmark; read-only review; no external system touched. Cyberattack: None.
- Near-miss: in deployment, schema fixation is a budget fire (95 wasted calls) and a silent capability loss (the agent never discovers the working form it already used 4 times). F-B1's shape is the sharper risk: an agent that acts on a different harness's tool contract can emit well-formed calls that a permissive gateway might actually route somewhere — here the harness refused them, which is the guardrail working as designed.
