# BCP search trajectories — evidence index

Lane: `bcp-search-trajectories`. Dataset rev:
`af778a3994cfcb30a8a9ab5abcbcb7c7fcbf645f`.
Raw bytes: `data/lanes/bcp-search-trajectories/raw/`.
Manifest: `raw/MANIFEST.json`. License note: `raw/LICENSE.note`.

Trajectory id convention: `<run>:predictions.jsonl line <N>`,
1-based file line. Reviewer B cited 0-based rows ("idx"); add 1
for the file line. Reviewer A/C cited 1-based lines already.

| Finding | Trajectory | File path + sha256 | Step range |
|---|---|---|---|
| BCP-A-001 | glm51:predictions.jsonl line 266 | `raw/glm51/predictions.jsonl` · `c54a544e37464484a7ad8b38e408987ddf6c1c885304012d6a6ab1cec3158bed` | 0-based msgs 95-114 (quote at msgs[114]) |
| BCP-A-002 | glm51:predictions.jsonl line 12 | `raw/glm51/predictions.jsonl` · `c54a544e37464484a7ad8b38e408987ddf6c1c885304012d6a6ab1cec3158bed` | 0-based msgs 22-87 (hits at 22,33,43,45,48,52,57,64,72,80) |
| BCP-A-003 | ds4pro:predictions.jsonl (corpus-wide; exemplars line 9, line 266) | `raw/ds4pro/predictions.jsonl` · `98ef95fc174bdcdbba3308767e4fffa197b4dc70e94234210aafd5cadf0230af` | corpus-wide; line 9 0-based msgs 4,6; line 266 0-based msgs[90] |
| BCP-A-004 | ds4pro:predictions.jsonl line 362 | `raw/ds4pro/predictions.jsonl` · `98ef95fc174bdcdbba3308767e4fffa197b4dc70e94234210aafd5cadf0230af` | 0-based msgs 43-72 (Wayback plans at 43,57,66,72; URL invention at msg53) |
| F-B1 | gpt-oss-120b-high:predictions.jsonl lines 79, 91, 247, 266, 461, 652, 690, 740 (0-based idx78, idx90, idx246, idx265, idx460, idx651, idx689, idx739) | `raw/gpt-oss-120b-high/predictions.jsonl` · `0e943e1b0d844986beb0beed12f809dcc9dd6ec039d9534c6804ef603bd1910d` | 1-based turns: idx78 t10 (find), idx90 t10 (watch), idx246 t26 (find {docid,pattern}), idx265 t21 (find), idx460 t9 (find), idx651 t7 (find), idx689 t51 (find {docid,pattern}), idx739 t27 (find_in_document) |
| F-B2 | gpt-oss-120b-high:predictions.jsonl line 342 (idx341); kimi26:predictions.jsonl line 95 (idx94) | gpt-oss file · `0e943e1b0d844986beb0beed12f809dcc9dd6ec039d9534c6804ef603bd1910d`; kimi26 file · `1d1e84c50615a12004ba717285c0cdbf94e41211ad798f298f2db5e19fe7a13c` | gpt-oss 1-based turns 35,40,43,49,50,56,59,60,61,64,65,67,70,73 (14 attempts); kimi26 turn 54 |
| F-B3 | gpt-oss-120b-high:predictions.jsonl line 458 (idx457) | `raw/gpt-oss-120b-high/predictions.jsonl` · `0e943e1b0d844986beb0beed12f809dcc9dd6ec039d9534c6804ef603bd1910d` | turn 33 (final turn; 33 turns total; termination=answer) |
| F-B4 | kimi26:predictions.jsonl line 101 (idx100) | `raw/kimi26/predictions.jsonl` · `1d1e84c50615a12004ba717285c0cdbf94e41211ad798f298f2db5e19fe7a13c` | 1-based turns 51-89 (31 identical queries; 13 strictly consecutive) |
| BCP-C-001 | tongyi-dr:predictions.jsonl line 741 | `raw/tongyi-dr/predictions.jsonl` · `4d06ffe541344d4c2e0f36f5680a3446a031403b15591887805520130a382320` | 1-based line 741, msgs 2-232; key reasoning at model_calls turn 23 |
| BCP-C-002 | tongyi-dr:predictions.jsonl line 1 | `raw/tongyi-dr/predictions.jsonl` · `4d06ffe541344d4c2e0f36f5680a3446a031403b15591887805520130a382320` | model_calls turns 1-10 (assistant messages empty) |
| BCP-C-003 | tongyi-dr:predictions.jsonl line 351 | `raw/tongyi-dr/predictions.jsonl` · `4d06ffe541344d4c2e0f36f5680a3446a031403b15591887805520130a382320` | model_calls turns 34-37 (0-based msgs 67-75 for tool returns) |
| BCP-C-004 | tongyi-dr:predictions.jsonl line 351 | `raw/tongyi-dr/predictions.jsonl` · `4d06ffe541344d4c2e0f36f5680a3446a031403b15591887805520130a382320` | model_calls turns 35-37 |
| BCP-C-005 | tongyi-dr:predictions.jsonl line 21 | `raw/tongyi-dr/predictions.jsonl` · `4d06ffe541344d4c2e0f36f5680a3446a031403b15591887805520130a382320` | model_calls turns 8, 12, 25, 26, 28, 30 + final prediction (43 turns) |
| BCP-C-006 | tongyi-dr:predictions.jsonl line 560 | `raw/tongyi-dr/predictions.jsonl` · `4d06ffe541344d4c2e0f36f5680a3446a031403b15591887805520130a382320` | model_calls turns 41-53 |
| BCP-X-001 | glm51 corpus-wide (830 rows) vs ds4pro corpus-wide (830 rows); exemplars glm51 lines 12, 85, 93, 313, 338, 459, 672 | glm51 file · `c54a544e37464484a7ad8b38e408987ddf6c1c885304012d6a6ab1cec3158bed`; ds4pro file · `98ef95fc174bdcdbba3308767e4fffa197b4dc70e94234210aafd5cadf0230af` | corpus-wide aggregate |

Notes:

- All paths are repo-relative to `data/lanes/bcp-search-trajectories/`.
- sha256 values are the pinned-revision file hashes from
  `raw/MANIFEST.json` (also verified at ingest build time, gate G3).
- `qwen35-35b-a3b/predictions.jsonl`
  (`4c0d3925b49d34d560286e5e0e35ecf0f95feca6994b79bb243aee32dc1c3076`,
  277,075,664 bytes) was reviewed with zero findings filed.
- Source URLs follow the pattern
  `https://huggingface.co/datasets/liuqi6777/bcp_search_agent_trajectory/resolve/af778a3994cfcb30a8a9ab5abcbcb7c7fcbf645f/<run>/predictions.jsonl`.
