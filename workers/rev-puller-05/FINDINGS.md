# rev-puller-05 FINDINGS

- Chunk: `data/2026-10-06-wikipedia-top500-infra-scan/raw/chunks/chunk-05` (ranks 217-255)
- Run started: 2026-10-06T20:45:13Z, ended: 2026-10-06T21:01:20Z
- Wall time: 16m 7s
- Articles attempted: 39, succeeded: 39, failed: 0
- Total revisions cached: 49225
- Output: `data/2026-10-06-wikipedia-top500-infra-scan/raw/revisions/<rank>.jsonl`
- Window per API call: rvstart=2026-10-07T00:00:00Z, rvend=2020-01-01T00:00:00Z, rvlimit=500, rvdir=older
- Pace: >=5s between requests, UA: silent-locus-top500-scan/1.0 (research)

## Per-article revision counts

| rank | article | revisions |
|---|---|---|
| 217 | Anne Hathaway | 1653 |
| 218 | Keri Russell | 556 |
| 219 | Tupac Shakur | 2537 |
| 220 | Jenna Dewan | 412 |
| 221 | Alice Weidel | 721 |
| 222 | european election 2014 | 0 |
| 223 | Bigg Boss (Tamil TV series) season 10 | 1104 |
| 224 | List of highest-grossing Malayalam films | 3291 |
| 225 | Miley Cyrus | 1612 |
| 226 | Labor Day | 501 |
| 227 | Nigella Lawson | 361 |
| 228 | 2026 US Open – Men's singles | 1068 |
| 229 | Stella Lefty | 422 |
| 230 | Coco Gauff | 2162 |
| 231 | Navier–Stokes equations | 483 |
| 232 | Sarah Paulson | 487 |
| 233 | Facebook | 1260 |
| 234 | Andrea Yates | 290 |
| 235 | Mitch McConnell | 1963 |
| 236 | Z-Library | 1115 |
| 237 | Anthony Bourdain | 986 |
| 238 | The Uprising (2026 film) | 321 |
| 239 | List of American films of 2026 | 4610 |
| 240 | Adolf Hitler | 2019 |
| 241 | Charles III | 5468 |
| 242 | Abdul El-Sayed | 697 |
| 243 | Sam Altman | 1684 |
| 244 | Khalid Sheikh Mohammed | 728 |
| 245 | Rebecca Hall | 417 |
| 246 | Sylvester Stallone | 855 |
| 247 | Nance O'Neil | 62 |
| 248 | Verity (novel) | 141 |
| 249 | Qazi Touqeer | 154 |
| 250 | Diana, Princess of Wales | 1709 |
| 251 | The Runner (2026 film) | 189 |
| 252 | Robert Pattinson | 1497 |
| 253 | Gal Gadot | 2970 |
| 254 | List of Tamil films of 2026 | 1474 |
| 255 | Dakota Johnson | 1246 |

## Failures

None.

## Notes

- One JSON object per line: rank, article, revid, parentid, user, timestamp, comment, tags, size.
- A count of -1 in counts.tsv marks a failed article (see errors.log); its JSONL is empty/partial.
