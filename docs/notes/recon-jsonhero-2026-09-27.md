# Recon Lane F — jsonhero.io (2026-09-27)

## Verdict

**Adopted public utility, same as jqp/md.succ.ai — but a different usage shape.** jsonhero.io is the Trigger.dev team's open-source JSON explorer (not a proxy). The swarm doesn't route traffic through it; it uses it as a **shared pastebin for structured data**: agents POST fetched JSON to jsonhero.io's document API, get back a shareable `/j/<id>` link, and deep-link to specific record paths (`?path=regCF_county_2021.91`) inside wiki revisions. It's the swarm's collaborative scratchpad for county-record datasets.

## Service facts

- **What:** "JSON Hero — a beautiful JSON viewer for the web." Column/tree/editor views, string-content inference (dates, images, colors, URLs), auto JSON Schema, fuzzy search, VS Code plugin. Source: https://jsonhero.io
- **Code:** https://github.com/triggerdotdev/jsonhero-web — Apache 2.0, created 2022-03-01, 10,879 stars, actively maintained (last push 2025-11-28). Not archived.
- **Document-creation API (unofficial, documented in README):** `POST https://jsonhero.io/api/create.json` with `{"title": ..., "content": {...}, "readOnly": false, "ttl": 3600}` → `{"id": "...", "location": "https://jsonhero.io/j/<id>"}`. TTL is optional — documents without it persist. This is almost certainly how the agents minted their 17–18 shared docs programmatically.
- **Deep-link grammar:** `/j/<id>?path=<dotted.path>` — "Easily sharable URLs with path support" is a headline feature.

## Swarm usage (from the collusion.wiki corpus)

- **Scale:** ~2,400 URL occurrences across corpus dumps (2,272 corpus hits per the jqp lane's count), 17–18 unique shared document IDs, 4 named agents (`A`, `Agent`, `MassSecWin12`, `TexasWikiHelper`) across **dse + probier** wikis. Zero gem-corpus overlap (`cross_corpus_gem: false`).
- **Content:** the deep links overwhelmingly target `regCF_county_<year>.<record>` paths — county-record JSON documents (SEC county data, consistent with the June-18 SEC-task burst the jqp lane documented). Top paths: `regCF_county_2021.91`, `regCF_county_2021.81`, `regCF_county_2019.46`, plus `regCF_county_filters.*`.
- **View probing:** agents also hit alternate endpoints on their docs — `/j/<id>.json`, `/j/<id>/tree`, `/j/<id>/editor`, `.json?test=1` — exercising the view/API surface, not just reading.
- **Role in tradecraft:** jqp.vercel.app = live fetch/transform proxy; md.succ.ai = reader proxy; **jsonhero.io = persistent shared state**. The three form a pipeline: fetch via proxy → stash structured results in a shareable JSON Hero doc → deep-link records from wiki pages. Different task family, same launcher toolkit.

## Hunt implications

- **jsonhero.io `/j/<id>` links are greppable agent-state artifacts.** Any public text containing `jsonhero.io/j/` + `?path=` with campaign grammars is a potential swarm trace — same detection logic as the jqp adoption surface, but for stored data rather than proxied traffic.
- **The document API has no auth** (per README). TTL-less docs persist; the 17–18 corpus doc IDs may still resolve live. (Not probed — left for a deliberate follow-up decision.)
- **Sibling class:** jsonformatter.curiousconcept.com and codebeautify.org (flagged by the jqp lane) are the same adoption class — JSON utilities agents may stash data in.

## Files

- `data/jsonhero/PROVENANCE.md` — separate dataset provenance (kept out of collusion-wiki)
- `data/jsonhero/repo_metadata.json` — triggerdotdev/jsonhero-web metadata (GitHub API, 2026-09-28)
- `data/jsonhero/usage_patterns.json` — 17 doc IDs, path-param rollup, view-suffix breakdown from corpus dumps

## Scope

Read-only throughout (corpus greps, one homepage read, GitHub API metadata). No live document fetches, no operator identity pursued.
