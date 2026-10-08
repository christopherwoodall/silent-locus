# Recon Lane C — jqp.vercel.app (2026-09-27)

Passive recon on the jq-over-HTTP proxy used by 722 wiki agents across the
dse + fractal wikis. All findings verified 2026-09-28; infrastructure facts
only.

## Verdict up front

`jqp.vercel.app` is **not** custom agent-built infrastructure. It is the
public deployment of the open-source project **sighrobot/jqp** — "A
serverless proxy for filtering JSON using node-jq" — MIT licensed, created
2022-05-14, 16 stars, listed in fiatjaf/awesome-jq. The swarm *adopted* a
public utility as its dominant execution vehicle. That is the stronger
finding: launcher-tradition agents route through public utilities, which
makes their usage visible in public corpora.

- Source repo: https://github.com/sighrobot/jqp (repo `homepage` field points at https://jqp.vercel.app)
- Last repo push: 2023-07-19 (project dormant; deployment still live)
- The corpus-attested branch URL `jqp-git-main-sighrobot.vercel.app` follows Vercel's `<project>-git-<branch>-<team>` pattern; the team slug matches the GitHub account. Consistent deployment provenance.

## Live endpoint behavior (probed once, 2026-09-28T02:47Z)

- `GET /api/v0?url=https://example.com` → **200, body `[]`**, `Content-Type: application/json`
- API per README: `url` (required, URL-encoded JSON/CSV endpoint; repeatable — responses become a jq-addressable array), `jq` (jq-web filter), `debug=true` (echoes params)
- Response headers: Next.js App Router (`Vary: RSC, Next-Router-State-Tree`), `Access-Control-Allow-Origin: *` (deliberately open CORS — the whole point), served from Vercel edge `iad1`, `X-Vercel-Cache: MISS`
- Without `jq` the service returns an empty array; it is live and serving today.

## Role in the swarms (third-party corpus analyses)

- joshuadavid/wikiagentswarminvestigation `analyses/urls/README.md`: `jq_json_relay` category, 21,534 occurrences; jqp.vercel.app 19,255 of them. "Fetches X and runs a jq expression on the response, returning the transformed JSON" — fetch + transform + compact in one request.
  https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/analyses/urls/README.md
- `tasks/sec-regcf-ma-cache/README.md`: "the dominant execution vehicle in this cluster"; burst window 2026-06-18 14:11–22:00 UTC.
  https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/tasks/sec-regcf-ma-cache/README.md
- `tasks/sec-regcf-ma-cache/data-files.md`: 14,341 jq-over-HTTP wrapper URL instances against the SEC county.json endpoints.
  https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/tasks/sec-regcf-ma-cache/data-files.md
- `tasks/url-fetch-proxy-usage/README.md`: defines the **jq-over-HTTP** vocabulary entry; also documents "probe pastes" (agents posting multi-proxy templates to compare which proxies work) and ResourceSpace IIIF as the sole target of the jqp probes in one task family.
  https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/tasks/url-fetch-proxy-usage/README.md
- hamzah2304/messageboardauditbench blind report (react_google_gemini-3.8-flash): documents 2-hop (`jqp`→target, 11,086), 3-hop (`jqp`→allorigins→target, 7,768), 4-hop and two **5-hop recursive chains** with `debug=true`, 2026-06-18T21:01–21:03Z — jqp used both innermost and outermost.
  https://github.com/hamzah2304/messageboardauditbench/blob/HEAD/reports/blind_verbatim_xhigh_p4436af8c/react_google_gemini-3.8-flash_r3_20260907T095543Z.md
- Same repo's GPTBot-IP attribution scan: the string `"jqp.vercel.app"` fired in **48/49 weekly shards** (2025-10-05 → 2026-09-06) — persistent search-index presence.
  https://github.com/joshuadavid/wikiagentswarminvestigation/blob/HEAD/analyses/oai-published-ip-hits/README.md
- swarm-ai-research/wiki-agent-swarm-incident `analysis/sub-swarms.md`: 530 jqp occurrences / 168 distinct URLs as an r.jina.ai wrapper; corroborates 3,235 jqp revisions in the June-18 SEC burst.
  https://github.com/swarm-ai-research/wiki-agent-swarm-incident/blob/HEAD/analysis/sub-swarms.md

## Certificate transparency

- crt.sh exact query for `jqp.vercel.app`: **no individual certificate** (Vercel wildcard coverage; expected for `*.vercel.app` deployments).
- crt.sh `%jqp%` wildcard: only unrelated lookalike domains (e.g. `www.jqp--hafahsooju.xfl--ooow1t3m.xyz`) — no sibling project certs, no action.

## Hunt implications

1. **Adopted-public-utility is a detection surface.** The agents didn't hide their compute; they used a 16-star public proxy with open CORS. Any future eval run using jqp (or its Awesome-jq siblings like jsonhero.io, which also appears in the corpus) is greppable in public text.
2. **The `debug=true` param** echoes request params — corpus chains using it (the 5-hop examples) leak the full inner chain in the response, which is why analysts could reconstruct them.
3. **Sibling-enumeration path**: other jq-over-HTTP / JSON-transform public proxies (jsonhero.io 2,272 corpus hits, jsonformatter.curiousconcept.com, codebeautify.org) are the same adoption class — worth the same passive treatment if they recur.
4. The repo has been untouched since 2023 but the deployment is live — a quiet, unmaintained public utility carrying heavy agent traffic is itself the story.

## Artifacts

Separate dataset: [data/jqp-vercel/](../data/jqp-vercel/) (`PROVENANCE.md`, `repo_metadata.json`, `repo_summary.json`, `endpoint_probe.json`, `endpoint_response_body.txt`).
