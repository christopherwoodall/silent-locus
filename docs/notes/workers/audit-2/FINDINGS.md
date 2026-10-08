# Audit-2 findings — wikipedia top-500 infra scan (2026-10-06)

Worker: AUDIT-WORKER-2. Chunk: `data/2026-10-06-wikipedia-top500-infra-scan/raw/audit-chunks/audit-2.tsv` (122 articles, ranks 253–377).

Method:
- LOCAL: every line of `raw/revisions/<rank>.jsonl` parsed as JSON; checked `article`/`rank` fields, timestamps non-increasing, revids decreasing.
- API ground truth: `action=query&prop=revisions&titles=<t>&rvlimit=1&rvdir=newer&rvstart=2020-01-01T00:00:00Z&rvprop=ids|timestamp` → oldest in-window revision; compared to file's min timestamp. BROKEN = empty file while API returns a revision. TRUNCATED = file min_ts >1 day newer than API oldest.
- Repairs: full re-pull (`rvprop=user|timestamp|ids|comment|tags|size`, rvlimit=500, rvdir=older, rvstart=2026-10-07T00:00:00Z, rvend=2020-01-01T00:00:00Z, rvcontinue to exhaustion), temp+fsync+atomic rename, then re-verified.
- HTTP via curl only, User-Agent `silent-locus-top500-scan/1.0 (research)`, ≥5.2s pacing on en.wikipedia.org.

## Totals
- Articles checked: 122
- Verified OK: 121
- Repaired: 1
- Total API calls to en.wikipedia.org: 126

## Repairs
- rank 277 "Jessica Pegula": BROKEN (file was empty, 0 lines) — API confirmed revisions exist (oldest in-window 2020-01-08T16:51:32Z); full re-pull → 1831 revisions, min ts 2020-01-08T16:51:32Z, re-verified timestamps non-increasing (reverify_ok=True).

## Per-article verdicts
| rank | article | file lines | verdict | api oldest ts | note |
|---|---|---|---|---|---|
| 253 | Gal Gadot | 2970 | OK | 2020-01-02T05:28:32Z |  |
| 254 | List of Tamil films of 2026 | 1474 | OK | 2025-01-17T04:02:36Z |  |
| 255 | Dakota Johnson | 1246 | OK | 2020-01-03T16:44:41Z |  |
| 256 | Zoe Saldaña | 1487 | OK | 2020-01-03T00:08:51Z |  |
| 257 | Lili Reinhart | 433 | OK | 2020-01-07T22:44:36Z |  |
| 258 | Weapons (2025 film) | 2630 | OK | 2023-03-09T17:13:07Z |  |
| 259 | Bayeux Tapestry | 732 | OK | 2020-01-01T10:46:57Z |  |
| 260 | Aaron Rodgers | 1537 | OK | 2020-01-01T15:26:16Z |  |
| 261 | Nahui Ollin | 60 | OK | 2020-11-07T06:02:37Z |  |
| 262 | Andy Williams (guitarist) | 225 | OK | 2020-12-31T04:03:23Z |  |
| 263 | Manchester City F.C. | 2894 | OK | 2020-01-01T03:30:22Z |  |
| 264 | Monster (American TV series) | 370 | OK | 2024-09-06T02:34:15Z |  |
| 265 | Pink (singer) | 1509 | OK | 2020-01-01T00:58:05Z |  |
| 266 | Michael J. Fox | 1643 | OK | 2020-01-02T09:26:45Z |  |
| 267 | Verity (film) | 401 | OK | 2021-11-02T21:03:23Z |  |
| 268 | Xi Jinping | 2952 | OK | 2020-01-03T17:39:55Z |  |
| 269 | Bonnie Blue | 861 | OK | 2024-12-29T21:36:43Z |  |
| 270 | Brad Pitt | 828 | OK | 2020-01-03T00:23:56Z |  |
| 271 | Carrot Top | 748 | OK | 2020-01-18T16:19:35Z |  |
| 272 | Equal Earth projection | 211 | OK | 2020-01-24T19:42:15Z |  |
| 273 | Robert De Niro | 927 | OK | 2020-01-01T04:58:16Z |  |
| 274 | Christian Bale | 774 | OK | 2020-01-06T14:06:29Z |  |
| 275 | The Mandalorian and Grogu | 1191 | OK | 2020-05-24T08:30:17Z |  |
| 276 | Carlos Alcaraz | 4289 | OK | 2020-02-15T22:25:09Z |  |
| 277 | Jessica Pegula | 0 | REPAIRED | 2020-01-08T16:51:32Z | 0->1831 |
| 278 | The Love Hypothesis (film) | 165 | OK | 2025-10-20T05:56:11Z |  |
| 279 | Adéla (singer) | 736 | OK | 2024-12-08T03:55:13Z |  |
| 280 | 2026 Men's European Volleyball Championship | 675 | OK | 2023-07-20T12:33:23Z |  |
| 281 | India | 5092 | OK | 2020-01-01T05:55:08Z |  |
| 282 | Iva Jovic | 591 | OK | 2024-01-26T08:47:09Z |  |
| 283 | Money in the Bank (2026) | 228 | OK | 2025-05-23T00:04:03Z |  |
| 284 | George W. Bush | 1840 | OK | 2020-01-12T08:18:50Z |  |
| 285 | Richard O'Sullivan | 211 | OK | 2020-01-04T08:44:01Z |  |
| 286 | Bruce Willis | 809 | OK | 2020-01-03T18:46:12Z |  |
| 287 | Stuart Fails to Save the Universe | 469 | OK | 2024-07-14T17:26:57Z |  |
| 288 | Presley Gerber | 139 | OK | 2026-09-21T07:52:43Z |  |
| 290 | I'm Game (film) | 297 | OK | 2026-07-24T16:23:02Z |  |
| 291 | Sunny Balwani | 505 | OK | 2020-01-01T13:11:12Z |  |
| 292 | Miku Martineau | 58 | OK | 2025-05-22T13:08:46Z |  |
| 293 | I, Robot (film) | 506 | OK | 2020-01-01T15:12:51Z |  |
| 294 | Andrew Garfield | 1142 | OK | 2020-01-01T19:24:28Z |  |
| 295 | Alix Earle | 439 | OK | 2023-08-13T17:12:03Z |  |
| 296 | Freddie Mercury | 1277 | OK | 2020-01-02T15:56:08Z |  |
| 297 | Dancing with the Stars (American TV series) | 1823 | OK | 2020-01-01T17:16:56Z |  |
| 298 | Ezra Frech | 132 | OK | 2020-05-28T12:02:26Z |  |
| 299 | Project Hail Mary (film) | 2356 | OK | 2020-03-29T20:11:51Z |  |
| 300 | Celine Dion | 1275 | OK | 2020-01-01T12:19:56Z |  |
| 302 | 2026 US Open – Women's singles | 651 | OK | 2026-08-23T12:13:29Z |  |
| 303 | Kenneth Walker III | 604 | OK | 2021-09-18T19:50:33Z |  |
| 304 | Katie Taylor | 984 | OK | 2020-01-04T22:41:28Z |  |
| 305 | Florence Pugh | 1786 | OK | 2020-01-01T08:58:12Z |  |
| 306 | Steve Jobs | 1162 | OK | 2020-01-08T04:22:37Z |  |
| 307 | Emmy Rossum | 458 | OK | 2020-01-30T17:38:38Z |  |
| 308 | Aaron Pierre (actor) | 511 | OK | 2020-09-27T22:16:10Z |  |
| 309 | The Early Spring | 73 | OK | 2026-01-08T21:15:41Z |  |
| 310 | Dungeon Crawler Carl | 384 | OK | 2024-12-18T03:26:48Z |  |
| 311 | To Catch a Predator | 553 | OK | 2020-01-07T06:26:39Z |  |
| 312 | Queen Victoria | 1166 | OK | 2020-01-12T05:50:01Z |  |
| 313 | Yom Kippur | 598 | OK | 2020-01-02T22:23:24Z |  |
| 314 | 2026 FIFA World Cup | 6747 | OK | 2020-01-02T06:20:38Z |  |
| 315 | Tilcayo | 386 | OK | 2026-09-17T17:52:39Z |  |
| 316 | The Blood of Dawnwalker | 239 | OK | 2024-07-10T03:39:32Z |  |
| 317 | UEFA Nations League | 1206 | OK | 2020-01-18T19:51:41Z |  |
| 318 | Kyle Chandler | 239 | OK | 2020-01-09T23:31:12Z |  |
| 319 | Scarlett Johansson | 1256 | OK | 2020-01-01T12:03:42Z |  |
| 320 | Barack Obama | 2964 | OK | 2020-01-01T16:35:22Z |  |
| 321 | Tom Hardy | 1416 | OK | 2020-01-02T14:04:23Z |  |
| 323 | Kenneth Branagh | 966 | OK | 2020-01-04T16:29:35Z |  |
| 324 | Brothers (2026 TV series) | 101 | OK | 2025-04-08T04:26:06Z |  |
| 325 | Emma Navarro | 805 | OK | 2020-01-27T20:20:11Z |  |
| 326 | Vinnie Jones | 550 | OK | 2020-01-01T15:24:50Z |  |
| 327 | Wordle | 1723 | OK | 2022-01-01T00:07:55Z |  |
| 328 | Gary Oldman | 536 | OK | 2020-01-01T03:02:56Z |  |
| 329 | 2026 Yemen offensives | 801 | OK | 2026-09-07T15:40:28Z |  |
| 330 | David Bale | 92 | OK | 2020-01-11T02:28:33Z |  |
| 331 | Grand Theft Auto VI | 2414 | OK | 2022-02-11T04:11:05Z |  |
| 332 | Harry Shum Jr. | 400 | OK | 2020-01-01T08:40:09Z |  |
| 333 | Adults (TV series) | 265 | OK | 2025-05-24T16:51:25Z |  |
| 334 | Erling Haaland | 3932 | OK | 2020-01-01T04:49:26Z |  |
| 335 | HTTP cookie | 250 | OK | 2020-01-06T20:16:26Z |  |
| 336 | Pornhub | 582 | OK | 2020-01-01T05:58:22Z |  |
| 337 | Todd Beamer | 259 | OK | 2020-01-15T21:57:39Z |  |
| 338 | Wiki | 446 | OK | 2020-01-19T10:35:54Z |  |
| 339 | Miss World 2026 | 971 | OK | 2025-05-09T07:59:43Z |  |
| 340 | Suicide of Bill Conradt | 287 | OK | 2023-01-06T20:48:43Z |  |
| 341 | Clint Eastwood | 1359 | OK | 2020-01-02T05:26:46Z |  |
| 342 | Jyothika | 701 | OK | 2020-01-06T20:50:53Z |  |
| 343 | Keanu Reeves | 1148 | OK | 2020-01-01T14:32:53Z |  |
| 344 | Charles Harrelson | 228 | OK | 2020-05-05T23:19:52Z |  |
| 345 | Morgan Freeman | 636 | OK | 2020-01-20T04:06:43Z |  |
| 346 | 2026 Russian legislative election | 451 | OK | 2021-09-21T08:27:14Z |  |
| 347 | Collapse of the World Trade Center | 702 | OK | 2020-01-04T19:34:41Z |  |
| 348 | Supergirl (2026 film) | 1248 | OK | 2020-05-07T22:29:22Z |  |
| 349 | Olivia Rodrigo | 3497 | OK | 2020-01-19T00:55:29Z |  |
| 350 | Unabomber (film) | 106 | OK | 2026-04-26T19:55:09Z |  |
| 351 | Josh Allen | 3869 | OK | 2020-01-01T20:59:50Z |  |
| 352 | East of Eden (novel) | 203 | OK | 2020-01-09T09:00:44Z |  |
| 353 | All Out (2026) | 201 | OK | 2026-07-13T23:33:16Z |  |
| 354 | The Vvaan: Force of the Forrest | 235 | OK | 2026-09-10T17:40:48Z |  |
| 355 | XXX: Return of Xander Cage | 458 | OK | 2020-01-02T14:53:42Z |  |
| 356 | Google Chrome | 802 | OK | 2020-01-03T16:52:10Z |  |
| 357 | Harald V | 1175 | OK | 2020-01-03T15:27:22Z |  |
| 358 | XHamster | 733 | OK | 2020-01-04T02:36:02Z |  |
| 359 | China | 5208 | OK | 2020-01-03T21:37:05Z |  |
| 360 | Odyssey | 895 | OK | 2020-01-01T22:07:58Z |  |
| 361 | Jaxson Dart | 643 | OK | 2021-05-27T03:42:12Z |  |
| 362 | List of presidents of the United States | 1648 | OK | 2020-01-03T14:47:39Z |  |
| 363 | The Shards (TV series) | 274 | OK | 2025-07-21T08:50:56Z |  |
| 364 | 2026 US Open (tennis) | 578 | OK | 2025-09-30T19:52:10Z |  |
| 365 | Al-Qaeda | 1417 | OK | 2020-01-06T01:16:05Z |  |
| 366 | Daisy Ridley | 544 | OK | 2020-01-04T02:56:29Z |  |
| 367 | Toy Story 5 | 2119 | OK | 2020-03-08T23:54:55Z |  |
| 368 | Henry VIII | 967 | OK | 2020-01-08T09:28:46Z |  |
| 369 | Travis Kelce | 2715 | OK | 2020-01-03T18:47:49Z |  |
| 370 | Awarapan 2 | 782 | OK | 2025-12-16T09:57:03Z |  |
| 371 | Welles Crowther | 283 | OK | 2020-03-19T23:25:31Z |  |
| 372 | 2026 Berlin state election | 297 | OK | 2023-06-19T08:13:13Z |  |
| 373 | Ryan Reynolds | 1190 | OK | 2020-01-06T18:24:53Z |  |
| 374 | 2026 United States Senate elections | 4925 | OK | 2020-11-08T00:21:52Z |  |
| 375 | Asian Games | 624 | OK | 2020-02-06T01:48:12Z |  |
| 376 | Hayley Williams | 1198 | OK | 2020-01-05T10:23:38Z |  |
| 377 | United States midterm election | 151 | OK | 2020-01-01T09:57:43Z |  |
