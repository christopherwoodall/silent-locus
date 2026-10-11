# Discovery scout: paste/drop venues — triage results

Date: 2026-10-03. Read-only, keyless, curl + search-engine dorks.
Scope: agents and agent infrastructure only. Markers probed: `zz=oai`, `openai_research` variants, incident URLs.

## Paste venues

| Venue | Indexable? | Probed? | Verdict |
|---|---|---|---|
| pastes.io | Partial — has `/search?keyword=` but results are JS-rendered | Yes (curl + Google dork) | Search pages render "Search Result - \<term\>" with **zero paste results** for zz=oai, openai_research, oai. Google `site:pastes.io "zz=oai" OR "openai_research"` → 0. Honest zeros; curl can't get past the JS wall for deeper probing. |
| paste.ee | No — `/api` 403s keyless, no public index/search on site | Yes (curl) | Unscourable keyless. Google dork `site:paste.ee ...` → 0. |
| controlc.com | No — no recent/search page (`/recent/` 404s), homepage has no paste index | Yes (curl) | Unscourable via index. Google dork → 0. |
| ix.io | N/A | Yes (curl) | **Dead** — "ix.io is taking a break 🍺" placeholder page. |
| termbin.com | No web index by design (netcat:9999 pastebin) | Partial | HTTP times out from this VM; raw TCP blocked by VM network policy. No web-searchable index exists by design. |
| privatebin.net (and PrivateBin generally) | No — zero-knowledge, no public list by design | Yes (curl) | Unscourable by design. Any agent using PrivateBin leaves no public trace. |

## File drops

| Venue | Listing? | Verdict |
|---|---|---|
| tmpfiles.org | No — `/api` is upload-only docs | No public listing. |
| file.io | No — one-time download links by design | No public listing. |
| transfer.sh | Dead (connection timeout) | Dead. |
| catbox.moe | Unreachable (timeout) | Unreachable from here; no public listing by design anyway (known file host). |

## Request-capture venues

| Venue | Public feed? | Verdict |
|---|---|---|
| webhook.site | No — URLs are private per-token; no public request stream found on homepage | Not a trace source via any public route. (Agents DO use it as a dead-drop — our word list has webhook.site shapes — but its logs are private.) |
| pipedream.com/requestbin | 301s to marketing | No public feed. |

## Code playgrounds / doc viewers

- `docs.google.com/viewer` wrapped incident URLs (`sec.gov/files/county.json`, `civilrightsdata.ed.gov`): Google dork → only benign CRDC documentation PDFs. **Zero incident links.**
- jsfiddle.net / codepen.io agent fetch-code (`r.jina.ai` fetch blocked-url): dork → **0 results.**

## Telegram / Discord

- No keyless public message-search surface exists. Telegram third-party indexes (tgstat, telemetr) need accounts; Discord has no public message index at all. **Out of keyless reach** — would need account-based tooling; flagged, not probed.

## Bottom line

No new paste/drop venue yields a searchable public index with our markers. pastes.io is the only one with a real search UI and it returns honest zeros; everything else is unscourable-by-design, dead, or unreachable. The paste/drop layer is a weaker trace source than the publish-by-default archives — consistent with the hunt's prior.
