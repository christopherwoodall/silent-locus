# COLLECT.md — 2026-09-28 Chinese Amap fleet

## Coverage
| Query | API total_hits | Saved | Pages |
|---|---|---|---|
| `url.domain:amap.com` 2026-09-28→2026-10-05 | 1,974 | 1,970 | 20 |
| `url.domain:gaode.com` 2026-09-28→2026-10-05 | 30 | 30 | 1 |
| `url.domain:httpbun.com` (infra) | 65 | 65 | 1 |
| `url.domain:livecodes.io` (infra) | 26 | 26 | 1 |
| `url.domain:href.li` (infra) | 19 | 19 | 1 |
| 7 cited full reports | — | 7 | — |
| **events.jsonl** | — | **2,110 records** | — |

## Gaps
- 4-report shortfall on amap.com (1,974 vs 1,970): fleet still active; new reports arrived during pagination, or API dedup. Not re-fetched.
- Relay-wrapped fleet reports (r.jina.ai, microlink, translate.goog submitted URLs) are NOT in the domain sweep — they carry non-Amap domains. Partially covered via follow-up keyword searches; full enumeration needs the article's survey method (not reproduced).
- webhook.site inboxes: only 3 submitted to urlquery in-window; the 14 inboxes in the report came from webhook.site's public API, not urlquery. Not collected here.
- `uqscan`/`uqtag` keyword searches hit urlquery's relevance cap; tag census (932 distinct) is from submitted URLs only.
- One early infra-collection invocation overwrote `page_000.json` across three queries; re-collected into per-query subdirs (authoritative).

## Fleet activity vs article
Article: 2,048 Amap reports 28 Sep–4 Oct (their broader survey count). Ours: 2,000 amap+gaode reports 28 Sep–5 Oct (domain-sweep count). Consistent within survey-methodology difference.
