# lists/ — canonical hunt lists

Consolidated 2026-10-08 on branch `url-keyword-farm`. Two lists, one home.

## Contents

| Path | What | Source |
|---|---|---|
| `words/wordlist.txt` | IOC search terms, one per line (`#` = comment/section) | Built 2026-10-03 from all hunt lanes; farm additions 2026-10-08 |
| `words/wordlist.json` | Same terms + metadata (`term`, `category`, `provenance`, `added_utc`, `status`, `note`). Superset of the txt: noisy/FP terms live here only (`status != active`). | Same |
| `words/staging/` | Staging area for candidate terms | — |
| `words/README.md` | Original wordlist readme | — |
| `urls/urls.jsonl` | URL inventory, one JSON object per line: `url`, `canonical`, `finding_id`, `submitter`, `source_field`, `status`, `corpus_path` (+ `tier`, `occurrences` on farm-added rows) | Transluce crawl (139 rows) + HF trajectory farm (182 tiered URLs, 2026-10-08) |

## Canonical-location notes

- `lists/words/` was `ioc-wordlist/` (moved 2026-10-08; contents unchanged).
- `lists/urls/urls.jsonl` is the canonical URL list. A legacy copy remains at
  `data/transluce-api/url-inventory.jsonl` because active code references it
  (`data/transluce-api/crawl_urls.py`,
  `data/2026-09-28-chinese-amap-fleet/personas/codebreaker/raw/mine_url_inventory.py`)
  and several docs cite the path. New URLs go in `lists/urls/`; do not edit the
  legacy copy.

## How to add entries

- **Words:** append the term to `words/wordlist.txt` under the right `# SECTION`
  (or add a new section), and append a JSON object to `words/wordlist.json`
  with `term`, `category`, `provenance`, `added_utc` (UTC, ISO-8601), `status`
  (`active`), `note`. Record where the term came from in `provenance`.
- **URLs:** append one JSON object per line to `urls/urls.jsonl` with the schema
  above. `submitter` = your lane/agent name, `source_field` = where it was found,
  `status` = `NEW`.

## Dedupe rule

- `wordlist.txt`: one term per line, exact-match dedupe (case-sensitive).
  Verified 2026-10-08: zero duplicates.
- `wordlist.json`: dedupe on `term` (exact match). Verified 2026-10-08: zero
  duplicates.
- `urls.jsonl`: dedupe on `url` (exact match). Verified 2026-10-08: zero
  duplicates.

Re-verify after any bulk add:

```bash
grep -v '^#' lists/words/wordlist.txt | grep -v '^$' | sort | uniq -d | wc -l
python3 -c "
import json
ts=[json.loads(l)['term'] for l in open('lists/words/wordlist.json') if l.strip()]
print('json dups:', len(ts)-len(set(ts)))
us=[json.loads(l)['url'] for l in open('lists/urls/urls.jsonl') if l.strip()]
print('url dups:', len(us)-len(set(us)))"
```

Both must print 0.
