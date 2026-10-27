# STATS/SCHEMA census — rubygems-july-2026-spike-operator-20261027.csv

Source: `data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv`
SHA-256 (verified before census): 765ee2f24e6ec1a191c66faee030aaea8586cc4a0cdde1bee4c0668a0f0f3ce0
Method: recomputed by script `census.py`; log `census.log`; machine-readable `census.json`. All totals reconcile to 533.
Note on markup-like author strings: exact values are preserved in census.json (derived verbatim from the CSV). This report counts them by shape and does not reproduce payload-like strings in prose.

## 1. Schema / per-column census

| column | distinct (non-empty) | empty | non-empty | type / notes |
|---|---|---|---|---|
| name | 533 | 0 | 533 | text, all unique |
| latest_version | 33 | 0 | 533 | text, 33 values |
| versions_in_window | 12 | 0 | 533 | integer 1–25, mean 1.28, median 1 |
| first_published_utc | 523 | 0 | 533 | timestamp, 523 distinct |
| last_published_utc | 524 | 0 | 533 | timestamp, 524 distinct |
| authors_declared | 46 | 0 | 533 | text, 46 distinct values |
| summary | 224 | 0 | 533 | text, 224 distinct |
| homepage_uri | 81 | 100 | 433 | text/URL, 81 distinct + 100 empty |
| source_code_uri | 204 | 327 | 206 | text/URL, 204 distinct + 327 empty |
| runtime_dependencies | 8 | 0 | 533 | integer 0–22, mean 0.16, median 0 |
| withdrawn | 1 | 0 | 533 | boolean text, 1 value only |
| dashboard_rule_level | 4 | 49 | 484 | categorical, 4 values + 49 empty |
| dashboard_rules | 73 | 49 | 484 | categorical string, 73 distinct + 49 empty |
| haiku_level | 4 | 49 | 484 | categorical, 4 values + 49 empty |
| haiku_score | 7 | 513 | 20 | numeric, present on 20 rows only; range 42–92, mean 62.2, median 53.5 |
| haiku_category | 3 | 49 | 484 | categorical, 3 values + 49 empty |
| haiku_agent_activity | 3 | 49 | 484 | categorical, 3 values + 49 empty |
| haiku_prompt_version | 2 | 49 | 484 | categorical, 2 values + 49 empty |
| haiku_reason | 484 | 49 | 484 | free text, 484 distinct (one per non-empty row) + 49 empty |
| doc_id | 533 | 0 | 533 | text, all unique, 0 empty |

Column totals check: every column sums to 533 (empty + non-empty). No column other than the eight dashboard/haiku fields and homepage/source has empties.

### Categorical distributions (full)

**withdrawn:** True=533

**dashboard_rule_level:** medium=193; critical=151; low=121; =49; high=19

**haiku_level:** high=385; critical=80; =49; medium=15; low=4

**haiku_category:** mass_generated=305; registry_test_or_probe=178; =49; unclear=1

**haiku_agent_activity:** possible=461; =49; likely=18; no_sign=5

**haiku_prompt_version:** pkg-review-1=464; =49; pkg-review-2=20

**runtime_dependencies:** 0=509; 1=9; 2=6; 3=4; 4=2; 17=1; 5=1; 22=1

**haiku_score (20 non-empty rows):** =513; 45=6; 88=5; 42=4; 72=2; 68=1; 92=1; 62=1

**summary:** 224 distinct values, 0 empty. **homepage_uri:** 82 distinct incl. empty; 81 non-empty distinct, 100 empty. **source_code_uri:** 205 distinct incl. empty; 204 non-empty distinct, 327 empty (61.4% empty). **haiku_reason:** 485 distinct incl. empty; 484 non-empty, each unique to its row.

**Credential-shaped scan (presence/count only, values never copied):** 7 cells matched a broad credential-keyword pattern — 5 in summary, 2 in haiku_reason. These are pattern matches only (keyword-shaped), not confirmed secrets; no values are reproduced here or in census.json summaries beyond counts.

## 2. Per-author batch structure

Distinct authors_declared values: 46. Top 4 account for 410/533 (76.9%): Andrey78 129, Prvaz12_mars 113, tester 100, monib110 68. Remaining 42 distinct values account for 123 rows.

Plain (non-markup) author counts, descending:

- Andrey78: 129
- Prvaz12_mars: 113
- tester: 100
- monib110: 68
- t: 20
- SR: 13
- Test: 10
- T: 8
- test: 7
- Tester: 5
- testingbear: 5
- attacker: 4
- fusagiko / takayamaki: 4
- Testing Buffalo: 3
- Panther: 3
- apexhunter: 3
- Apex Black: 2
- Security Researcher: 2
- A2: 2
- Salvador Fuentes Jr: 2
- Marlen Brunner: 2
- Oscar Segura: 2
- Hugo Antonio Sepulveda Manriquez: 1
- Ribose Inc.: 1
- Gerald Bauer: 1
- Testing: 1
- Testing Kangaroo: 1
- audit: 1
- attackerpython: 1
- Apex Black Assessment: 1
- <%25= 7*7 %>: 1
- Testing Wolf: 1
- Guy Boertje: 1
- Tiny Bubble Company: 1
- Gabi Jack: 1
- Lachlan Young: 1
- Ebling Mis: 1
- Atelier Mirai: 1
- Igor: 1

Markup/template-shaped author values: 7 distinct values, 9 rows total. By shape (prefix-first classification): script-tag 3 distinct / 4 rows; img-tag 1 distinct / 1 row; template/expression-tag 2 distinct / 3 rows; long-fuzzing-list 1 distinct / 1 row. Plain author values: 39 distinct / 524 rows. Exact markup values are in census.json; they are not reproduced in this report's prose.

| author | rows | first publish (first_published_utc) | last publish (max last_published_utc) | per-day (first publish) | max in 60 min | max in 10 min | max in 5 min | median gap (s) | min gap (s) | gaps <60s | gaps <300s | name len min–max (mean) | first==last rows |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Andrey78 | 129 | 2026-07-06 00:27:26 | 2026-07-06 17:07:53 | {'2026-07-06': 129} | 88 @ 2026-07-06 07:03:22 | 16 @ 2026-07-06 07:32:35 | 8 @ 2026-07-06 07:03:22 | 41.0 | 37.0 | 110 | 118 | 11–16 (13.57) | 129 |
| Prvaz12_mars | 113 | 2026-07-13 17:58:20 | 2026-07-13 19:35:05 | {'2026-07-13': 113} | 68 @ 2026-07-13 18:04:46 | 16 @ 2026-07-13 18:20:23 | 8 @ 2026-07-13 18:04:46 | 43.0 | 37.0 | 96 | 112 | 11–16 (13.62) | 113 |
| tester | 100 | 2026-07-07 03:12:23 | 2026-07-07 07:28:04 | {'2026-07-07': 100} | 37 @ 2026-07-07 06:02:47 | 22 @ 2026-07-07 06:35:50 | 15 @ 2026-07-07 06:37:05 | 38.0 | 0.0 | 57 | 85 | 10–246 (21.52) | 92 |
| monib110 | 68 | 2026-07-12 10:25:46 | 2026-07-12 11:25:15 | {'2026-07-12': 68} | 68 @ 2026-07-12 10:25:46 | 14 @ 2026-07-12 10:59:29 | 7 @ 2026-07-12 10:25:46 | 48.0 | 42.0 | 60 | 67 | 12–15 (13.69) | 68 |
| t | 20 | 2026-07-07 07:15:29 | 2026-07-07 07:45:30 | {'2026-07-07': 20} | 20 @ 2026-07-07 07:15:29 | 19 @ 2026-07-07 07:15:29 | 16 @ 2026-07-07 07:15:29 | 15.0 | 0.0 | 15 | 18 | 16–23 (19.75) | 20 |
| SR | 13 | 2026-07-07 03:15:08 | 2026-07-07 07:44:48 | {'2026-07-07': 13} | 9 @ 2026-07-07 06:20:51 | 6 @ 2026-07-07 06:20:51 | 3 @ 2026-07-07 06:20:51 | 168.5 | 31.0 | 3 | 9 | 19–28 (23.15) | 4 |
| Test | 10 | 2026-07-07 06:35:30 | 2026-07-07 06:44:39 | {'2026-07-07': 10} | 10 @ 2026-07-07 06:35:30 | 10 @ 2026-07-07 06:35:30 | 6 @ 2026-07-07 06:39:15 | 37.0 | 12.0 | 6 | 9 | 18–29 (21.6) | 10 |
| T | 8 | 2026-07-07 04:03:46 | 2026-07-07 07:44:45 | {'2026-07-07': 8} | 6 @ 2026-07-07 06:48:46 | 4 @ 2026-07-07 06:48:46 | 4 @ 2026-07-07 06:48:46 | 533.0 | 38.0 | 1 | 3 | 8–100 (25) | 8 |
| test | 7 | 2026-07-07 04:53:38 | 2026-07-07 15:17:18 | {'2026-07-07': 7} | 3 @ 2026-07-07 06:35:52 | 1 @ 2026-07-07 04:53:38 | 1 @ 2026-07-07 04:53:38 | 1953.0 | 851.0 | 0 | 0 | 16–20 (17.57) | 6 |
| Tester | 5 | 2026-07-07 03:56:58 | 2026-07-07 04:05:05 | {'2026-07-07': 5} | 5 @ 2026-07-07 03:56:58 | 5 @ 2026-07-07 03:56:58 | 4 @ 2026-07-07 03:56:58 | 65.0 | 45.0 | 2 | 3 | 17–19 (18.6) | 5 |
| testingbear | 5 | 2026-07-07 04:41:42 | 2026-07-07 06:20:44 | {'2026-07-07': 5} | 4 @ 2026-07-07 04:41:42 | 2 @ 2026-07-07 05:19:30 | 2 @ 2026-07-07 05:19:30 | 1134.0 | 101.0 | 0 | 1 | 13–15 (13.6) | 4 |
| attacker | 4 | 2026-07-07 03:24:35 | 2026-07-07 04:43:20 | {'2026-07-07': 4} | 3 @ 2026-07-07 04:39:14 | 3 @ 2026-07-07 04:39:14 | 3 @ 2026-07-07 04:39:14 | 245.0 | 1.0 | 1 | 2 | 17–22 (19.5) | 4 |
| fusagiko / takayamaki | 4 | 2026-07-08 13:39:10 | 2026-07-13 11:17:06 | {'2026-07-08': 4} | 4 @ 2026-07-08 13:39:10 | 4 @ 2026-07-08 13:39:10 | 3 @ 2026-07-08 13:44:23 | 11.0 | 10.0 | 2 | 2 | 8–20 (14) | 0 |
| Testing Buffalo | 3 | 2026-07-07 03:17:26 | 2026-07-07 06:51:57 | {'2026-07-07': 3} | 1 @ 2026-07-07 03:17:26 | 1 @ 2026-07-07 03:17:26 | 1 @ 2026-07-07 03:17:26 | 6435.5 | 3867.0 | 0 | 0 | 12–13 (12.33) | 2 |
| Panther | 3 | 2026-07-07 03:21:01 | 2026-07-07 06:53:12 | {'2026-07-07': 3} | 2 @ 2026-07-07 05:59:52 | 1 @ 2026-07-07 03:21:01 | 1 @ 2026-07-07 03:21:01 | 6365.5 | 3200.0 | 0 | 0 | 15–26 (19.67) | 2 |
| apexhunter | 3 | 2026-07-07 05:09:41 | 2026-07-07 06:07:20 | {'2026-07-07': 3} | 3 @ 2026-07-07 05:09:41 | 1 @ 2026-07-07 05:09:41 | 1 @ 2026-07-07 05:09:41 | 1729.5 | 927.0 | 0 | 0 | 19–26 (22.33) | 3 |
| Apex Black | 2 | 2026-07-07 03:03:09 | 2026-07-07 07:38:25 | {'2026-07-07': 2} | 1 @ 2026-07-07 03:03:09 | 1 @ 2026-07-07 03:03:09 | 1 @ 2026-07-07 03:03:09 | 8943.0 | 8943.0 | 0 | 0 | 13–19 (16) | 0 |
| Security Researcher | 2 | 2026-07-07 03:10:44 | 2026-07-07 03:23:17 | {'2026-07-07': 2} | 2 @ 2026-07-07 03:10:44 | 1 @ 2026-07-07 03:10:44 | 1 @ 2026-07-07 03:10:44 | 753.0 | 753.0 | 0 | 0 | 19–30 (24.5) | 2 |
| [script-tag author string: distinct value, see census.json] | 2 | 2026-07-07 03:43:10 | 2026-07-07 04:04:16 | {'2026-07-07': 2} | 2 @ 2026-07-07 03:43:10 | 1 @ 2026-07-07 03:43:10 | 1 @ 2026-07-07 03:43:10 | 1266.0 | 1266.0 | 0 | 0 | 13–19 (16) | 2 |
| A2 | 2 | 2026-07-07 05:25:28 | 2026-07-07 06:00:09 | {'2026-07-07': 2} | 2 @ 2026-07-07 05:25:28 | 1 @ 2026-07-07 05:25:28 | 1 @ 2026-07-07 05:25:28 | 2081.0 | 2081.0 | 0 | 0 | 23–25 (24) | 2 |
| [template/expression-tag author string: distinct value, see census.json] | 2 | 2026-07-07 06:53:06 | 2026-07-07 07:25:48 | {'2026-07-07': 2} | 2 @ 2026-07-07 06:53:06 | 1 @ 2026-07-07 06:53:06 | 1 @ 2026-07-07 06:53:06 | 1962.0 | 1962.0 | 0 | 0 | 11–13 (12) | 2 |
| Salvador Fuentes Jr | 2 | 2026-07-08 15:58:30 | 2026-07-08 17:09:45 | {'2026-07-08': 2} | 2 @ 2026-07-08 15:58:30 | 2 @ 2026-07-08 15:58:30 | 2 @ 2026-07-08 15:58:30 | 37.0 | 37.0 | 1 | 1 | 9–12 (10.5) | 0 |
| Marlen Brunner | 2 | 2026-07-08 23:02:59 | 2026-07-09 18:00:46 | {'2026-07-08': 2} | 2 @ 2026-07-08 23:02:59 | 1 @ 2026-07-08 23:02:59 | 1 @ 2026-07-08 23:02:59 | 3418.0 | 3418.0 | 0 | 0 | 16–23 (19.5) | 0 |
| Oscar Segura | 2 | 2026-07-09 01:16:08 | 2026-07-11 14:35:15 | {'2026-07-09': 2} | 1 @ 2026-07-09 01:16:08 | 1 @ 2026-07-09 01:16:08 | 1 @ 2026-07-09 01:16:08 | 51403.0 | 51403.0 | 0 | 0 | 11–21 (16) | 1 |
| Hugo Antonio Sepulveda Manriquez | 1 | 2026-07-06 15:41:28 | 2026-07-08 13:02:23 | {'2026-07-06': 1} | 1 @ 2026-07-06 15:41:28 | 1 @ 2026-07-06 15:41:28 | 1 @ 2026-07-06 15:41:28 | None | None | 0 | 0 | 9–9 (9) | 0 |
| Ribose Inc. | 1 | 2026-07-06 15:46:37 | 2026-07-07 00:59:56 | {'2026-07-06': 1} | 1 @ 2026-07-06 15:46:37 | 1 @ 2026-07-06 15:46:37 | 1 @ 2026-07-06 15:46:37 | None | None | 0 | 0 | 6–6 (6) | 0 |
| Gerald Bauer | 1 | 2026-07-06 17:01:45 | 2026-07-07 12:43:07 | {'2026-07-06': 1} | 1 @ 2026-07-06 17:01:45 | 1 @ 2026-07-06 17:01:45 | 1 @ 2026-07-06 17:01:45 | None | None | 0 | 0 | 14–14 (14) | 0 |
| Testing | 1 | 2026-07-07 03:06:27 | 2026-07-07 05:31:23 | {'2026-07-07': 1} | 1 @ 2026-07-07 03:06:27 | 1 @ 2026-07-07 03:06:27 | 1 @ 2026-07-07 03:06:27 | None | None | 0 | 0 | 19–19 (19) | 0 |
| Testing Kangaroo | 1 | 2026-07-07 03:10:01 | 2026-07-07 07:15:24 | {'2026-07-07': 1} | 1 @ 2026-07-07 03:10:01 | 1 @ 2026-07-07 03:10:01 | 1 @ 2026-07-07 03:10:01 | None | None | 0 | 0 | 17–17 (17) | 0 |
| audit | 1 | 2026-07-07 03:10:37 | 2026-07-07 18:13:42 | {'2026-07-07': 1} | 1 @ 2026-07-07 03:10:37 | 1 @ 2026-07-07 03:10:37 | 1 @ 2026-07-07 03:10:37 | None | None | 0 | 0 | 19–19 (19) | 0 |
| attackerpython | 1 | 2026-07-07 03:23:28 | 2026-07-07 03:23:28 | {'2026-07-07': 1} | 1 @ 2026-07-07 03:23:28 | 1 @ 2026-07-07 03:23:28 | 1 @ 2026-07-07 03:23:28 | None | None | 0 | 0 | 21–21 (21) | 1 |
| Apex Black Assessment | 1 | 2026-07-07 03:23:32 | 2026-07-07 03:23:32 | {'2026-07-07': 1} | 1 @ 2026-07-07 03:23:32 | 1 @ 2026-07-07 03:23:32 | 1 @ 2026-07-07 03:23:32 | None | None | 0 | 0 | 29–29 (29) | 1 |
| [script-tag author string: distinct value, see census.json] | 1 | 2026-07-07 03:39:07 | 2026-07-07 03:39:07 | {'2026-07-07': 1} | 1 @ 2026-07-07 03:39:07 | 1 @ 2026-07-07 03:39:07 | 1 @ 2026-07-07 03:39:07 | None | None | 0 | 0 | 18–18 (18) | 1 |
| [img-tag author string: distinct value, see census.json] | 1 | 2026-07-07 04:17:05 | 2026-07-07 04:17:05 | {'2026-07-07': 1} | 1 @ 2026-07-07 04:17:05 | 1 @ 2026-07-07 04:17:05 | 1 @ 2026-07-07 04:17:05 | None | None | 0 | 0 | 18–18 (18) | 1 |
| [script-tag author string: distinct value, see census.json] | 1 | 2026-07-07 04:50:39 | 2026-07-07 04:50:39 | {'2026-07-07': 1} | 1 @ 2026-07-07 04:50:39 | 1 @ 2026-07-07 04:50:39 | 1 @ 2026-07-07 04:50:39 | None | None | 0 | 0 | 20–20 (20) | 1 |
| [long-fuzzing-list author string: distinct value, see census.json] | 1 | 2026-07-07 06:37:01 | 2026-07-07 06:37:01 | {'2026-07-07': 1} | 1 @ 2026-07-07 06:37:01 | 1 @ 2026-07-07 06:37:01 | 1 @ 2026-07-07 06:37:01 | None | None | 0 | 0 | 20–20 (20) | 1 |
| [template/expression-tag author string: distinct value, see census.json] | 1 | 2026-07-07 07:25:50 | 2026-07-07 07:25:50 | {'2026-07-07': 1} | 1 @ 2026-07-07 07:25:50 | 1 @ 2026-07-07 07:25:50 | 1 @ 2026-07-07 07:25:50 | None | None | 0 | 0 | 11–11 (11) | 1 |
| <%25= 7*7 %> | 1 | 2026-07-07 07:25:52 | 2026-07-07 07:25:52 | {'2026-07-07': 1} | 1 @ 2026-07-07 07:25:52 | 1 @ 2026-07-07 07:25:52 | 1 @ 2026-07-07 07:25:52 | None | None | 0 | 0 | 11–11 (11) | 1 |
| Testing Wolf | 1 | 2026-07-07 15:13:31 | 2026-07-07 17:15:01 | {'2026-07-07': 1} | 1 @ 2026-07-07 15:13:31 | 1 @ 2026-07-07 15:13:31 | 1 @ 2026-07-07 15:13:31 | None | None | 0 | 0 | 12–12 (12) | 0 |
| Guy Boertje | 1 | 2026-07-07 16:14:42 | 2026-07-08 11:21:36 | {'2026-07-07': 1} | 1 @ 2026-07-07 16:14:42 | 1 @ 2026-07-07 16:14:42 | 1 @ 2026-07-07 16:14:42 | None | None | 0 | 0 | 9–9 (9) | 0 |
| Tiny Bubble Company | 1 | 2026-07-09 17:48:34 | 2026-07-09 17:48:34 | {'2026-07-09': 1} | 1 @ 2026-07-09 17:48:34 | 1 @ 2026-07-09 17:48:34 | 1 @ 2026-07-09 17:48:34 | None | None | 0 | 0 | 17–17 (17) | 1 |
| Gabi Jack | 1 | 2026-07-09 23:48:22 | 2026-07-11 23:50:31 | {'2026-07-09': 1} | 1 @ 2026-07-09 23:48:22 | 1 @ 2026-07-09 23:48:22 | 1 @ 2026-07-09 23:48:22 | None | None | 0 | 0 | 10–10 (10) | 0 |
| Lachlan Young | 1 | 2026-07-10 10:41:37 | 2026-07-10 12:56:05 | {'2026-07-10': 1} | 1 @ 2026-07-10 10:41:37 | 1 @ 2026-07-10 10:41:37 | 1 @ 2026-07-10 10:41:37 | None | None | 0 | 0 | 17–17 (17) | 0 |
| Ebling Mis | 1 | 2026-07-10 13:58:21 | 2026-07-10 13:58:21 | {'2026-07-10': 1} | 1 @ 2026-07-10 13:58:21 | 1 @ 2026-07-10 13:58:21 | 1 @ 2026-07-10 13:58:21 | None | None | 0 | 0 | 17–17 (17) | 1 |
| Atelier Mirai | 1 | 2026-07-12 12:02:06 | 2026-07-12 12:02:06 | {'2026-07-12': 1} | 1 @ 2026-07-12 12:02:06 | 1 @ 2026-07-12 12:02:06 | 1 @ 2026-07-12 12:02:06 | None | None | 0 | 0 | 12–12 (12) | 1 |
| Igor | 1 | 2026-07-12 21:27:43 | 2026-07-12 21:27:43 | {'2026-07-12': 1} | 1 @ 2026-07-12 21:27:43 | 1 @ 2026-07-12 21:27:43 | 1 @ 2026-07-12 21:27:43 | None | None | 0 | 0 | 16–16 (16) | 1 |

Overall timing: first publish 2026-07-06, last first-publish 2026-07-13 (full per-day below). Overall per-day (first_published_utc): 2026-07-06=132; 2026-07-07=204; 2026-07-08=8; 2026-07-09=4; 2026-07-10=2; 2026-07-12=70; 2026-07-13=113

Overall hour-of-day (UTC, first_published_utc): 00=1; 01=3; 02=2; 03=39; 04=27; 05=37; 06=70; 07=118; 08=29; 10=36; 11=33; 12=1; 13=5; 15=7; 16=1; 17=10; 18=65; 19=45; 21=1; 23=3

Name length overall: min 6, max 246, mean 16.29, median 14. Length distribution: {'6': 1, '8': 2, '9': 3, '10': 2, '11': 8, '12': 44, '13': 105, '14': 129, '15': 60, '16': 15, '17': 16, '18': 15, '19': 61, '20': 24, '21': 7, '22': 15, '23': 11, '24': 1, '25': 1, '26': 5, '27': 1, '28': 1, '29': 2, '30': 1, '100': 1, '109': 1, '246': 1}. Pattern counts only: names containing a digit 136; names containing underscore 39; hyphen-count distribution {'2': 380, '1': 23, '0': 43, '3': 86, '4': 1}.

## 3. Version patterns

latest_version distribution (33 values): 0.0.1=452; 0.1.0=19; 0.0.2=13; 1.0.0=10; 2026.0713.1900=4; 0.1.1=3; 0.0.5=2; 0.0.3=2; 0.4.0=2; 0.5.2=2; 0.5.3=2; 1.5.10=1; 2.1.3=1; 0.9.0=1; 0.1.5=1; 2.0.2=1; 0.0.14=1; 9.9.9=1; 0.3.5=1; 0.0.6=1; 0.2.0=1; 0.0.00000000000000000000000000000000000000000000000000=1; 0.0.4=1; 0.0.11=1; 0.0.9=1; 0.4.1=1; 999999.999999.999999=1; 0.4.6=1; 1.3.13=1; 3.2.18=1; 3.0.0.rc2=1; 1.3.0=1; 0.1.0.pre.4=1

versions_in_window distribution: 1=491; 2=22; 4=5; 3=4; 5=3; 9=2; 12=1; 21=1; 11=1; 25=1; 6=1; 8=1

Single-version rows (versions_in_window=1): 491. Multi-version rows: 42. Rows where first_published_utc == last_published_utc: 491.

## 4. Cross-tabs (highlights; full tables in census.json under xt)

### authors_declared x haiku_category

- Andrey78 × mass_generated: 129
- Prvaz12_mars × mass_generated: 113
- monib110 × (empty): 6
- monib110 × mass_generated: 61
- monib110 × unclear: 1
- tester × mass_generated: 2
- tester × registry_test_or_probe: 98

### authors_declared x haiku_agent_activity

- Andrey78 × possible: 129
- Prvaz12_mars × possible: 113
- monib110 × (empty): 6
- monib110 × possible: 62
- tester × likely: 7
- tester × possible: 93

### authors_declared x dashboard_rule_level

- Andrey78 × low: 64
- Andrey78 × medium: 65
- Prvaz12_mars × low: 53
- Prvaz12_mars × medium: 60
- monib110 × (empty): 6
- monib110 × low: 4
- monib110 × medium: 58
- tester × critical: 93
- tester × high: 3
- tester × medium: 4

### haiku_prompt_version x haiku_category

-  × (empty): 49
- pkg-review-1 × mass_generated: 295
- pkg-review-1 × registry_test_or_probe: 168
- pkg-review-1 × unclear: 1
- pkg-review-2 × mass_generated: 10
- pkg-review-2 × registry_test_or_probe: 10

### haiku_prompt_version x haiku_agent_activity

-  × (empty): 49
- pkg-review-1 × likely: 16
- pkg-review-1 × no_sign: 5
- pkg-review-1 × possible: 443
- pkg-review-2 × likely: 2
- pkg-review-2 × possible: 18

Main-author cross-tab detail:
- Andrey78 (129): category mass_generated 129; activity possible 129; rule level medium 65 / low 64; prompt pkg-review-1 123 / pkg-review-2 6; haiku_level high 121 / medium 8.
- Prvaz12_mars (113): category mass_generated 113; activity possible 113; rule level medium 60 / low 53; prompt pkg-review-1 111 / pkg-review-2 2; haiku_level high 111 / medium 2.
- tester (100): category registry_test_or_probe 98 / mass_generated 2; activity possible 93 / likely 7; rule level critical 93 / medium 4 / high 3; prompt pkg-review-1 91 / pkg-review-2 9; haiku_level critical 58 / high 41 / medium 1.
- monib110 (68): category mass_generated 61 / empty 6 / unclear 1; activity possible 62 / empty 6; rule level medium 58 / empty 6 / low 4; prompt pkg-review-1 60 / empty 6 / pkg-review-2 2; haiku_level high 58 / empty 6 / medium 3 / low 1.
- Prompt × category: pkg-review-1 → mass_generated 295, registry_test_or_probe 168, unclear 1; pkg-review-2 → mass_generated 10, registry_test_or_probe 10; empty prompt → empty category 49.
- Prompt × activity: pkg-review-1 → possible 443, likely 16, no_sign 5; pkg-review-2 → possible 18, likely 2; empty prompt → empty activity 49. Note: all 20 pkg-review-2 rows are split 10/10 across categories, and no pkg-review-2 row is no_sign.
- Dashboard rule level overall: medium 193, critical 151, low 121, high 19, empty 49. Haiku level overall: high 385, critical 80, medium 15, low 4, empty 49.
- Author × category / activity / rule-level for the remaining author values: see census.json xt tables. The three large non-empty authors (Andrey78, Prvaz12_mars, tester) have zero empty dashboard/haiku rows; all 49 empty-field rows come from monib110 (6) plus the smaller-author set (43).

### dashboard_rules — FULL frequency table (73 distinct strings + empty)

- Group: combinatorial names; Group: shared text: 183
- Group: combinatorial names: 119
- (empty): 49
- Group: combinatorial names; Group: name series; Group: owner burst; Group: template batch; Package: numbered name; Package: placeholder author; Package: placeholder text: 29
- Group: owner burst; Group: template batch; Package: numbered name; Package: placeholder text; Package: probe name; Package: short author: 9
- Group: owner burst; Group: template batch; Package: numbered name; Package: oob url; Package: placeholder text; Package: probe name; Package: short author: 7
- Group: owner burst; Package: oob url; Package: placeholder author; Package: probe name: 6
- Group: combinatorial names; Group: name series; Group: owner burst; Group: template batch; Package: numbered name; Package: placeholder author: 6
- Group: owner burst; Group: template batch; Package: numbered name; Package: placeholder author; Package: placeholder text: 6
- Group: owner burst; Package: numbered name; Package: oob url; Package: placeholder author: 6
- Group: owner burst; Package: numbered name; Package: short author: 5
- Group: combinatorial names; Group: name series; Group: owner burst; Package: numbered name; Package: oob url; Package: placeholder author; Package: test name: 4
- Group: combinatorial names; Group: name series; Group: owner burst; Group: template batch; Package: numbered name; Package: placeholder author; Package: placeholder text; Package: test name: 4
- Group: combinatorial names; Group: name series; Group: owner burst; Group: template batch; Package: numbered name; Package: placeholder author; Package: placeholder text; Package: probe name: 4
- Group: owner burst; Group: template batch; Package: oob url; Package: placeholder author; Package: test name: 4
- Group: template batch; Package: placeholder author: 4
- Group: owner burst; Group: template batch; Package: placeholder author; Package: placeholder text; Package: test name: 3
- Group: owner burst; Package: placeholder author; Package: test name: 3
- Group: owner burst; Package: oob url; Package: placeholder author; Package: test name: 3
- Group: owner burst; Group: template batch; Package: placeholder author; Package: placeholder link: 3
- Group: owner burst; Package: numbered name; Package: probe name; Package: short author: 3
- Group: name series; Group: owner burst; Group: template batch; Package: placeholder author; Package: placeholder text: 3
- Group: owner burst; Group: template batch; Package: placeholder text; Package: short author; Package: test name: 3
- Group: owner burst; Package: placeholder author; Package: placeholder text; Package: probe name: 3
- Group: name series; Group: owner burst; Group: template batch; Package: numbered name; Package: placeholder text; Package: probe name; Package: short author: 3
- Group: owner burst; Package: numbered name; Package: placeholder text; Package: short author: 2
- Package: markup; Package: probe name: 2
- Group: combinatorial names; Group: name series; Group: owner burst; Package: numbered name; Package: placeholder author; Package: test name: 2
- Group: owner burst; Package: placeholder text; Package: short author; Package: test name: 2
- Group: combinatorial names; Package: probe name: 2
- Package: markup; Package: oob url; Package: probe name: 2
- Group: owner burst; Group: template batch; Package: oob url; Package: placeholder author; Package: probe name: 2
- Group: owner burst; Group: template batch; Package: oob url; Package: placeholder author: 2
- Group: owner burst; Group: template batch; Package: placeholder author; Package: placeholder link; Package: probe name: 2
- Group: combinatorial names; Group: name series; Group: owner burst; Package: markup; Package: numbered name; Package: placeholder author: 2
- Group: owner burst; Package: numbered name; Package: placeholder author: 2
- Group: shared text: 2
- Group: name series; Package: numbered name; Package: placeholder link; Package: test name: 1
- Group: name series; Package: numbered name; Package: test name: 1
- Group: combinatorial names; Group: name series; Group: owner burst; Package: numbered name; Package: oob url; Package: placeholder author; Package: placeholder text; Package: test name: 1
- Package: oob url; Package: probe name: 1
- Package: placeholder link; Package: placeholder text; Package: probe name: 1
- Group: owner burst; Package: numbered name; Package: placeholder text; Package: short author; Package: test name: 1
- Package: markup; Package: numbered name: 1
- Group: combinatorial names; Group: name series; Package: markup; Package: numbered name; Package: test name: 1
- Group: combinatorial names; Group: name series; Group: owner burst; Group: template batch; Package: numbered name; Package: placeholder author; Package: placeholder link: 1
- Group: combinatorial names; Group: owner burst; Package: markup; Package: oob url; Package: placeholder author; Package: probe name: 1
- Group: owner burst; Package: placeholder author; Package: probe name: 1
- Group: owner burst; Package: numbered name; Package: placeholder author; Package: placeholder text: 1
- Group: owner burst; Package: placeholder text; Package: short author: 1
- Group: owner burst; Package: oob url; Package: placeholder author: 1
- Group: owner burst; Group: template batch; Package: placeholder author; Package: placeholder text; Package: probe name: 1
- Group: combinatorial names; Group: owner burst; Package: oob url; Package: placeholder author; Package: test name: 1
- Group: owner burst; Package: markup; Package: oob url; Package: placeholder author; Package: test name: 1
- Package: numbered name; Package: placeholder text; Package: short author; Package: test name: 1
- Package: numbered name; Package: probe name; Package: short author: 1
- Group: combinatorial names; Group: owner burst; Group: template batch; Package: oob url; Package: placeholder author; Package: test name: 1
- Group: owner burst; Package: numbered name; Package: placeholder text; Package: probe name; Package: short author: 1
- Group: combinatorial names; Group: owner burst; Package: numbered name; Package: oob url; Package: placeholder author; Package: probe name: 1
- Group: combinatorial names; Group: owner burst; Package: placeholder author; Package: placeholder text; Package: probe name: 1
- Group: owner burst; Package: numbered name; Package: oob url; Package: placeholder author; Package: probe name: 1
- Group: owner burst; Group: template batch; Package: placeholder author; Package: placeholder text; Package: random name: 1
- Group: combinatorial names; Group: owner burst; Package: numbered name; Package: oob url; Package: placeholder author; Package: test name: 1
- Group: combinatorial names; Group: name series; Group: owner burst; Package: numbered name; Package: placeholder author: 1
- Group: owner burst; Package: numbered name; Package: oob url; Package: placeholder author; Package: test name: 1
- Group: owner burst; Group: template batch; Package: placeholder text; Package: short author: 1
- Group: combinatorial names; Group: owner burst; Package: numbered name; Package: oob url; Package: placeholder author: 1
- Group: combinatorial names; Group: owner burst; Group: template batch; Package: numbered name; Package: placeholder text; Package: short author; Package: test name: 1
- Group: combinatorial names; Group: name series; Package: markup; Package: placeholder text; Package: probe name: 1
- Group: combinatorial names; Group: name series; Package: placeholder text; Package: probe name: 1
- Group: combinatorial names; Group: name series; Package: probe name: 1
- Group: owner burst; Package: numbered name; Package: short author; Package: test name: 1
- Group: combinatorial names; Group: owner burst; Package: numbered name; Package: short author: 1
- Group: combinatorial names; Package: markup; Package: numbered name; Package: placeholder author; Package: probe name: 1


## 5. doc_id pattern

Format: `rubygems:<name>@<version>` for all 533 rows. Distinct: 533, duplicates: 0, empty: 0. Name part equals row name: 533/533. Version part equals latest_version: 530/533. The 3 mismatches are: apex-platform-test (latest 0.1.0, doc_id version 0.1.0-java), jrjackson (latest 0.5.2, doc_id version 0.5.2-java), shirobai (latest 2026.0713.1900, doc_id version 2026.0713.1900-x86_64-linux) — i.e. doc_id carries a platform suffix the latest_version column does not.

## 6. Empty-field analysis (the 49 rows)

The same 49 rows are empty in ALL eight dashboard/haiku fields (dashboard_rule_level, dashboard_rules, haiku_level, haiku_score, haiku_category, haiku_agent_activity, haiku_prompt_version, haiku_reason): 49. No row is partially empty on those fields; no non-empty-category row lacks haiku_reason.

Empty rows by author: monib110 6, testingbear 5, fusagiko / takayamaki 4, apexhunter 3, Apex Black 2, Security Researcher 2, Testing Buffalo 2, Panther 2, Salvador Fuentes Jr 2, Marlen Brunner 2, Oscar Segura 2, plus 1 row each for 17 further distinct author values (14 plain + 1 img-tag + 1 long-fuzzing-list + 1 template/expression-tag). Total distinct author values among empty rows: 28 (25 plain + 3 markup-shaped). None of the 49 is Andrey78, Prvaz12_mars, or tester.

Empty rows by first-publish date: 2026-07-06=3; 2026-07-07=24; 2026-07-08=8; 2026-07-09=4; 2026-07-10=2; 2026-07-12=8

Empty rows: withdrawn True 49/49. versions_in_window: 1=29; 2=8; 4=4; 3=2; 5=2; 12=1; 25=1; 6=1; 8=1. latest_version: 0.0.1=19; 0.1.0=4; 2026.0713.1900=4; 0.0.5=2; 0.4.0=2; 0.5.2=2; 0.5.3=2; 0.1.1=2; 1.5.10=1; 2.1.3=1; 0.9.0=1; 0.1.5=1; 0.0.14=1; 0.4.1=1; 0.4.6=1; 1.3.13=1; 3.2.18=1; 3.0.0.rc2=1; 1.3.0=1; 0.1.0.pre.4=1

Empty rows: runtime_dependencies 0=26; 1=9; 2=5; 3=4; 4=2; 17=1; 5=1; 22=1. Homepage distinct 24 (16 empty homepage within the 49); source distinct 15; summary distinct 46; name length 6–30.

Other empties (not part of the 49 set): homepage_uri empty 100 rows total (so 51 non-empty-field rows also lack homepage); source_code_uri empty 327 rows total (so 278 non-empty-field rows also lack source).

## Reconciliation

- Total rows: 533. Header + 533 data rows. Name distinct 533, doc_id distinct 533, no duplicate names or doc_ids.
- withdrawn: True 533/533.
- Correction to the brief's category numbers: haiku_category is mass_generated 305 + registry_test_or_probe 178 + unclear 1 + empty 49 = 533. The brief omitted the single 'unclear' row (giga-pure-tool, monib110, 2026-07-12). All other brief numbers reconcile exactly.

- haiku_category: mass_generated=305; registry_test_or_probe=178; (empty)=49; unclear=1 (sum 533)
- haiku_agent_activity: possible=461; (empty)=49; likely=18; no_sign=5 (sum 533)
- haiku_prompt_version: pkg-review-1=464; (empty)=49; pkg-review-2=20 (sum 533)
- dashboard_rule_level: medium=193; critical=151; low=121; (empty)=49; high=19 (sum 533)
- haiku_level: high=385; critical=80; (empty)=49; medium=15; low=4 (sum 533)

## Files

- census.py (script), census.log (full output), census.json (machine-readable tables), make_report.py (this report generator), report.md (this file)
