# AUDIT-WORKER-3 findings — Wikipedia top-500 infra scan

Quarter: ranks 378–500 (audit-3.tsv), 123 article-entries (rank 433 checked twice: `433.jsonl` = "List of countries by GDP (nominal)", `433_barry_melrose.jsonl` = "Barry Melrose").

Method:
- LOCAL: every line of each `raw/revisions/<rank>.jsonl` parsed as JSON; `article` and `rank` fields verified against the TSV; timestamps verified non-increasing.
- API: one ground-truth call per article (`prop=revisions`, `rvdir=newer`, `rvstart=2020-01-01T00:00:00Z`, `rvlimit=1`) → oldest in-window revision timestamp; compared to the file's minimum timestamp. Verdict rules: empty file + API revision = BROKEN; file min_ts more than 1 day newer than API oldest = TRUNCATED; otherwise OK.
- HTTP: curl only, UA `silent-locus-top500-scan/1.0 (research)`, >=5s pacing between requests.

## Per-article verdicts

| rank | article | file | lines | file min_ts | API oldest ts | verdict |
|-----:|---------|------|------:|-------------|-----------------|---------|
| 378 | Bob Mackie | `378.jsonl` | 336 | 2020-01-14T15:00:31Z | 2020-01-14T15:00:31Z | OK |
| 379 | Conor Benn | `379.jsonl` | 639 | 2020-02-04T20:29:17Z | 2020-02-04T20:29:17Z | OK |
| 380 | Teenage Sex and Death at Camp Miasma | `380.jsonl` | 427 | 2025-05-15T21:51:29Z | 2025-05-15T21:51:29Z | OK |
| 381 | Yemeni civil war (2014–present) | `381.jsonl` | 2063 | 2020-01-08T13:58:44Z | 2020-01-08T13:58:44Z | OK |
| 382 | BRICS | `382.jsonl` | 2898 | 2020-01-01T09:16:11Z | 2020-01-01T09:16:11Z | OK |
| 383 | Robin Williams | `383.jsonl` | 1337 | 2020-01-07T23:30:11Z | 2020-01-07T23:30:11Z | OK |
| 384 | Hannah Waddingham | `384.jsonl` | 883 | 2020-01-05T18:55:51Z | 2020-01-05T18:55:51Z | OK |
| 385 | United Airlines Flight 175 | `385.jsonl` | 1226 | 2020-01-05T01:19:58Z | 2020-01-05T01:19:58Z | OK |
| 386 | Runner (2026 American film) | `386.jsonl` | 201 | 2024-10-24T15:57:25Z | 2024-10-24T15:57:25Z | OK |
| 387 | Madison Beer | `387.jsonl` | 652 | 2020-01-24T05:29:12Z | 2020-01-24T05:29:12Z | OK |
| 388 | Vladimir Putin | `388.jsonl` | 3541 | 2020-01-04T15:12:44Z | 2020-01-04T15:12:44Z | OK |
| 389 | Dennis Haskins | `389.jsonl` | 196 | 2020-01-13T03:58:27Z | 2020-01-13T03:58:27Z | OK |
| 390 | Lamine Yamal | `390.jsonl` | 3382 | 2022-09-06T09:46:27Z | 2022-09-06T09:46:27Z | OK |
| 391 | New York City | `391.jsonl` | 5616 | 2020-01-01T07:33:04Z | 2020-01-01T07:33:04Z | OK |
| 392 | Peter Thiel | `392.jsonl` | 1427 | 2020-01-03T11:59:25Z | 2020-01-03T11:59:25Z | OK |
| 393 | Cat | `393.jsonl` | 1510 | 2020-01-12T19:18:21Z | 2020-01-12T19:18:21Z | OK |
| 394 | Bharatiya Nyaya Sanhita | `394.jsonl` | 1 | 2026-04-02T08:50:59Z | 2026-04-02T08:50:59Z | OK |
| 395 | Sardar 2 | `395.jsonl` | 436 | 2024-07-16T10:47:26Z | 2024-07-16T10:47:26Z | OK |
| 396 | Gable Steveson | `396.jsonl` | 744 | 2020-07-12T22:46:11Z | 2020-07-12T22:46:11Z | OK |
| 397 | Alex Michelsen | `397.jsonl` | 913 | 2022-07-09T13:20:18Z | 2022-07-09T13:20:18Z | OK |
| 398 | Jack Lowden | `398.jsonl` | 400 | 2020-01-01T14:52:53Z | 2020-01-01T14:52:53Z | OK |
| 399 | The Dog Stars (film) | `399.jsonl` | 407 | 2024-11-08T18:08:49Z | 2024-11-08T18:08:49Z | OK |
| 400 | 2026 FIFA ASEAN Cup | `400.jsonl` | 968 | 2026-05-06T20:15:17Z | 2026-05-06T20:15:17Z | OK |
| 401 | Elliot Page | `401.jsonl` | 1472 | 2020-01-06T18:24:31Z | 2020-01-06T18:24:31Z | OK |
| 402 | Bharatiya Sakshya Act, 2023 | `402.jsonl` | 142 | 2023-08-11T09:28:31Z | 2023-08-11T09:28:31Z | OK |
| 403 | Cleopatra | `403.jsonl` | 958 | 2020-01-02T23:29:58Z | 2020-01-02T23:29:58Z | OK |
| 404 | John F. Kennedy | `404.jsonl` | 2230 | 2020-01-03T17:05:24Z | 2020-01-03T17:05:24Z | OK |
| 405 | Ziad Jarrah | `405.jsonl` | 770 | 2020-01-15T00:25:38Z | 2020-01-15T00:25:38Z | OK |
| 406 | George Michael | `406.jsonl` | 1419 | 2020-01-03T16:24:40Z | 2020-01-03T16:24:40Z | OK |
| 407 | Ted Bundy | `407.jsonl` | 1497 | 2020-01-02T03:06:50Z | 2020-01-02T03:06:50Z | OK |
| 408 | Pressure (2026 film) | `408.jsonl` | 341 | 2024-07-19T13:25:30Z | 2024-07-19T13:25:30Z | OK |
| 409 | Cam Skattebo | `409.jsonl` | 418 | 2023-12-03T13:43:09Z | 2023-12-03T13:43:09Z | OK |
| 410 | Taylor Sheridan | `410.jsonl` | 459 | 2020-01-27T22:26:16Z | 2020-01-27T22:26:16Z | OK |
| 411 | Canada | `411.jsonl` | 3643 | 2020-01-01T00:58:01Z | 2020-01-01T00:58:01Z | OK |
| 412 | Israel | `412.jsonl` | 4039 | 2020-01-07T18:23:24Z | 2020-01-07T18:23:24Z | OK |
| 413 | The Blame (TV series) | `413.jsonl` | 66 | 2025-12-30T00:49:11Z | 2025-12-30T00:49:11Z | OK |
| 414 | TNT Sports (United Kingdom) | `414.jsonl` | 919 | 2020-01-01T14:11:15Z | 2020-01-01T14:11:15Z | OK |
| 415 | Sally Field | `415.jsonl` | 477 | 2020-01-02T03:34:25Z | 2020-01-02T03:34:25Z | OK |
| 416 | Chad Powers | `416.jsonl` | 338 | 2024-08-23T23:00:03Z | 2024-08-23T23:00:03Z | OK |
| 417 | Drew Lock | `417.jsonl` | 961 | 2020-01-01T22:20:19Z | 2020-01-01T22:20:19Z | OK |
| 418 | The Love Hypothesis | `418.jsonl` | 169 | 2021-12-21T20:57:18Z | 2021-12-21T20:57:18Z | OK |
| 419 | Mid-Autumn Festival | `419.jsonl` | 899 | 2020-01-05T16:02:23Z | 2020-01-05T16:02:23Z | OK |
| 420 | Haakon VIII | `420.jsonl` | 780 | 2020-01-01T09:09:22Z | 2020-01-01T09:09:22Z | OK |
| 421 | Joey King | `421.jsonl` | 1021 | 2020-01-06T03:19:05Z | 2020-01-06T03:19:05Z | OK |
| 422 | Rosh Hashanah | `422.jsonl` | 570 | 2020-01-08T00:24:14Z | 2020-01-08T00:24:14Z | OK |
| 423 | American Airlines Flight 77 | `423.jsonl` | 767 | 2020-01-02T00:31:13Z | 2020-01-02T00:31:13Z | OK |
| 424 | Russia | `424.jsonl` | 6584 | 2020-01-01T22:10:02Z | 2020-01-01T22:10:02Z | OK |
| 425 | List of Super Bowl champions | `425.jsonl` | 727 | 2020-01-11T01:46:05Z | 2020-01-11T01:46:05Z | OK |
| 426 | Arnold Schwarzenegger | `426.jsonl` | 1404 | 2020-01-09T15:08:11Z | 2020-01-09T15:08:11Z | OK |
| 427 | O. J. Simpson | `427.jsonl` | 1676 | 2020-01-01T19:50:17Z | 2020-01-01T19:50:17Z | OK |
| 428 | Al Pacino | `428.jsonl` | 1399 | 2020-01-03T16:39:19Z | 2020-01-03T16:39:19Z | OK |
| 429 | Dark Matter (2024 TV series) | `429.jsonl` | 463 | 2022-06-19T04:55:52Z | 2022-06-19T04:55:52Z | OK |
| 430 | Bruno Mars | `430.jsonl` | 2117 | 2020-01-02T15:39:01Z | 2020-01-02T15:39:01Z | OK |
| 431 | Trinidad Chambliss | `431.jsonl` | 124 | 2025-09-13T16:55:21Z | 2025-09-13T16:55:21Z | OK |
| 432 | Germany | `432.jsonl` | 3316 | 2020-01-05T17:15:10Z | 2020-01-05T17:15:10Z | OK |
| 433 | Barry Melrose | `433_barry_melrose.jsonl` | 97 | 2020-01-12T00:49:01Z | 2020-01-12T00:49:01Z | OK |
| 433 | List of countries by GDP (nominal) | `433.jsonl` | 1455 | 2020-01-11T17:07:16Z | 2020-01-11T17:07:16Z | OK |
| 435 | Suriya | `435.jsonl` | 860 | 2020-01-01T20:46:21Z | 2020-01-01T20:46:21Z | OK |
| 436 | Barbarian (2022 film) | `436.jsonl` | 976 | 2022-07-27T19:20:46Z | 2022-07-27T19:20:46Z | OK |
| 437 | Dynatrace | `437.jsonl` | 196 | 2020-01-04T20:08:45Z | 2020-01-04T20:08:45Z | OK |
| 438 | Harry Potter (TV series) | `438.jsonl` | 1082 | 2021-09-21T13:42:27Z | 2021-09-21T13:42:27Z | OK |
| 439 | Australia | `439.jsonl` | 3249 | 2020-01-04T09:41:58Z | 2020-01-04T09:41:58Z | OK |
| 440 | Pluribus (TV series) | `440.jsonl` | 1412 | 2022-09-22T20:00:17Z | 2022-09-22T20:00:17Z | OK |
| 441 | Dua Lipa | `441.jsonl` | 2694 | 2020-01-09T15:13:31Z | 2020-01-09T15:13:31Z | OK |
| 442 | Napoleon | `442.jsonl` | 2218 | 2020-01-04T13:33:17Z | 2020-01-04T13:33:17Z | OK |
| 443 | Tim Cook | `443.jsonl` | 454 | 2020-01-14T15:52:23Z | 2020-01-14T15:52:23Z | OK |
| 444 | Navier–Stokes existence and smoothness | `444.jsonl` | 374 | 2020-02-08T15:15:24Z | 2020-02-08T15:15:24Z | OK |
| 445 | Scooter Braun | `445.jsonl` | 912 | 2020-01-15T20:14:00Z | 2020-01-15T20:14:00Z | OK |
| 446 | Jennifer Lawrence | `446.jsonl` | 1431 | 2020-01-10T06:53:42Z | 2020-01-10T06:53:42Z | OK |
| 447 | 2026 | `447.jsonl` | 3534 | 2020-02-03T20:12:37Z | 2020-02-03T20:12:37Z | OK |
| 448 | Ryan Gosling | `448.jsonl` | 619 | 2020-01-17T07:44:50Z | 2020-01-17T07:44:50Z | OK |
| 449 | Kayadu Lohar | `449.jsonl` | 609 | 2022-09-15T09:28:43Z | 2022-09-15T09:28:43Z | OK |
| 450 | 2026 Mecklenburg-Vorpommern state election | `450.jsonl` | 271 | 2022-06-04T18:02:03Z | 2022-06-04T18:02:03Z | OK |
| 451 | The Gentlemen (2019 film) | `451.jsonl` | 849 | 2020-01-01T02:43:43Z | 2020-01-01T02:43:43Z | OK |
| 452 | Hailee Steinfeld | `452.jsonl` | 1693 | 2020-01-01T06:00:54Z | 2020-01-01T06:00:54Z | OK |
| 453 | Jon Bernthal | `453.jsonl` | 765 | 2020-01-02T19:12:58Z | 2020-01-02T19:12:58Z | OK |
| 454 | 2026 MTV Video Music Awards | `454.jsonl` | 349 | 2026-04-20T02:51:43Z | 2026-04-20T02:51:43Z | OK |
| 455 | Jason Sudeikis | `455.jsonl` | 851 | 2020-01-02T00:17:46Z | 2020-01-02T00:17:46Z | OK |
| 456 | Raphinha | `456.jsonl` | 2284 | 2020-02-01T10:12:28Z | 2020-02-01T10:12:28Z | OK |
| 457 | Taylor Hanson | `457.jsonl` | 152 | 2020-02-24T04:38:14Z | 2020-02-24T04:38:14Z | OK |
| 458 | Enzo Fernández | `458.jsonl` | 1910 | 2020-11-01T19:51:48Z | 2020-11-01T19:51:48Z | OK |
| 459 | Millie Bobby Brown | `459.jsonl` | 1915 | 2020-01-02T04:13:32Z | 2020-01-02T04:13:32Z | OK |
| 460 | Lust Stories 3 | `460.jsonl` | 84 | 2026-02-06T04:56:39Z | 2026-02-06T04:56:39Z | OK |
| 461 | Christopher Nolan | `461.jsonl` | 2706 | 2020-01-01T09:21:42Z | 2020-01-01T09:21:42Z | OK |
| 462 | The Pitt | `462.jsonl` | 1791 | 2024-08-19T16:19:01Z | 2024-08-19T16:19:01Z | OK |
| 463 | Clavicular (influencer) | `463.jsonl` | 996 | 2026-01-16T12:54:26Z | 2026-01-16T12:54:26Z | OK |
| 464 | Crew Girl | `464.jsonl` | 63 | 2026-09-07T15:47:28Z | 2026-09-07T15:47:28Z | OK |
| 465 | Elvis Presley | `465.jsonl` | 1858 | 2020-01-06T21:19:23Z | 2020-01-06T21:19:23Z | OK |
| 466 | List of highest-grossing Indian films | `466.jsonl` | 5812 | 2020-01-03T08:43:14Z | 2020-01-03T08:43:14Z | OK |
| 467 | Kylian Mbappé | `467.jsonl` | 3211 | 2020-01-02T16:20:13Z | 2020-01-02T16:20:13Z | OK |
| 468 | Heath Ledger | `468.jsonl` | 779 | 2020-01-04T10:52:30Z | 2020-01-04T10:52:30Z | OK |
| 469 | Chelsea F.C. | `469.jsonl` | 3339 | 2020-01-04T15:11:38Z | 2020-01-04T15:11:38Z | OK |
| 470 | Lewis Pullman | `470.jsonl` | 467 | 2020-01-29T02:06:30Z | 2020-01-29T02:06:30Z | OK |
| 471 | Ariana Grande | `471.jsonl` | 3760 | 2020-01-01T18:19:56Z | 2020-01-01T18:19:56Z | OK |
| 472 | A | `472.jsonl` | 546 | 2020-02-14T00:23:35Z | 2020-02-14T00:23:35Z | OK |
| 473 | George VI | `473.jsonl` | 1911 | 2020-01-01T22:57:25Z | 2020-01-01T22:57:25Z | OK |
| 474 | Margaret Qualley | `474.jsonl` | 831 | 2020-01-04T00:58:12Z | 2020-01-04T00:58:12Z | OK |
| 475 | Pete Hegseth | `475.jsonl` | 2691 | 2020-01-02T04:11:47Z | 2020-01-02T04:11:47Z | OK |
| 476 | Yemen | `476.jsonl` | 1928 | 2020-01-01T10:23:15Z | 2020-01-01T10:23:15Z | OK |
| 477 | Jessica Barden | `477.jsonl` | 247 | 2020-02-03T08:09:21Z | 2020-02-03T08:09:21Z | OK |
| 478 | Alan Cumming | `478.jsonl` | 726 | 2020-01-04T21:37:28Z | 2020-01-04T21:37:28Z | OK |
| 479 | Anthropic | `479.jsonl` | 939 | 2021-01-23T08:11:43Z | 2021-01-23T08:11:43Z | OK |
| 480 | Jing Boran | `480.jsonl` | 127 | 2020-01-02T05:06:06Z | 2020-01-02T05:06:06Z | OK |
| 481 | Lake Ontario | `481.jsonl` | 403 | 2020-01-11T06:44:43Z | 2020-01-11T06:44:43Z | OK |
| 482 | List of Indian films of 2026 | `482.jsonl` | 1321 | 2026-01-11T07:27:56Z | 2026-01-11T07:27:56Z | OK |
| 483 | Joe O'Cearuill | `483.jsonl` | 63 | 2020-10-08T21:45:09Z | 2020-10-08T21:45:09Z | OK |
| 484 | FC Barcelona | `484.jsonl` | 2830 | 2020-01-01T16:59:22Z | 2020-01-01T16:59:22Z | OK |
| 485 | Street Fighter (2026 film) | `485.jsonl` | 500 | 2023-04-27T19:38:13Z | 2023-04-27T19:38:13Z | OK |
| 486 | The Beast in Me (TV series) | `486.jsonl` | 266 | 2024-06-12T17:49:18Z | 2024-06-12T17:49:18Z | OK |
| 487 | Mr. T | `487.jsonl` | 293 | 2020-01-08T21:26:28Z | 2020-01-08T21:26:28Z | OK |
| 488 | Fall 2: Deadpoint | `488.jsonl` | 247 | 2024-02-06T14:58:13Z | 2024-02-06T14:58:13Z | OK |
| 489 | The Scandal (2026 TV series) | `489.jsonl` | 116 | 2025-03-27T12:16:49Z | 2025-03-27T12:16:49Z | OK |
| 490 | Up (film series) | `490.jsonl` | 600 | 2020-01-02T21:37:22Z | 2020-01-02T21:37:22Z | OK |
| 491 | Joely Richardson | `491.jsonl` | 218 | 2020-01-05T23:50:14Z | 2020-01-05T23:50:14Z | OK |
| 492 | Fauda | `492.jsonl` | 319 | 2020-01-11T02:21:34Z | 2020-01-11T02:21:34Z | OK |
| 493 | Billie Lourd | `493.jsonl` | 725 | 2020-01-07T03:06:37Z | 2020-01-07T03:06:37Z | OK |
| 494 | Cooper Manning | `494.jsonl` | 155 | 2020-01-03T23:57:03Z | 2020-01-03T23:57:03Z | OK |
| 495 | Virat Kohli | `495.jsonl` | 4488 | 2020-01-01T13:48:38Z | 2020-01-01T13:48:38Z | OK |
| 496 | One World Trade Center | `496.jsonl` | 461 | 2020-01-02T05:18:16Z | 2020-01-02T05:18:16Z | OK |
| 497 | Natalie Portman | `497.jsonl` | 1074 | 2020-01-10T01:10:07Z | 2020-01-10T01:10:07Z | OK |
| 498 | Silent Hill: Townfall | `498.jsonl` | 138 | 2022-11-15T12:23:46Z | 2022-11-15T12:23:46Z | OK |
| 499 | Worlds Collide (2026) | `499.jsonl` | 242 | 2026-07-16T14:59:09Z | 2026-07-16T14:59:09Z | OK |
| 500 | Sadie Sink | `500.jsonl` | 1606 | 2020-01-10T15:29:54Z | 2020-01-10T15:29:54Z | OK |

## Totals

- Articles verified OK: **123** of 123
- Articles repaired: **0** (none — no BROKEN or TRUNCATED files found; no repairs were necessary)
- API calls made: **123** (ground-truth oldest-revision checks) + 0 repair calls = **123 total**

Notes:
- Every file's minimum timestamp matched the API's oldest in-window revision **to the second** — no truncation, no silent short-writes in this quarter.
- Local JSONL validity, field agreement, and timestamp ordering all passed on all files.
- Raw machine-readable artifacts: `local-check.json`, `api-ground-truth.json`, `ground-truth.log`, `ground-truth.py` (all in `workers/audit-3/`).
