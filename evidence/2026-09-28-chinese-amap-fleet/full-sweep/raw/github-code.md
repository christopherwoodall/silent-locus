# GitHub code-search sweep — fleet markers
Date: 2026-10-04 (run ~22:47–23:05 CDT)
Operator: subagent surface sweep for the Amap/uqscan fleet hunt
Scope: public code only. No auth used anywhere; no logins, no tokens.

## Bottom line
NO public GitHub code containing the fleet markers was found. Every marker
that returned hits returned only false positives (substrings inside base64
blobs, MATLAB variable names, unrelated products). See per-marker verdicts.

## Method (undocumented endpoints, per collection doctrine)
GitHub's own code search is fully gated behind sign-in for all types tested
(code, commits, issues). Per the standing doctrine ("no API key is not a
stop"), the page source was read to find the backing XHR endpoint:

- `GET https://github.com/search?q=<q>&type=code` (curl, browser UA) →
  175 KB HTML containing "Sign in to search code on GitHub". No anonymous
  result path. Frontend asset
  `https://github.githubassets.com/assets/blackbird-search-<hash>.js`
  references only `/search/blackbird_count`, `/search/count`,
  `/search/custom_scopes` — the result backend requires the session.
- `https://api.github.com/search/code?q=uqscan` → needs auth, 401 (as expected).
- grep.app: `GET https://grep.app/api/search?q=<term>` → blocked from this
  egress: Vercel Security Checkpoint + HTTP 429. HARD STOP for grep.app in
  this run (rate-limit doctrine) — worth retrying later via a different
  route or egress, since grep.app indexes far more repos than Sourcegraph.
- searchcode: `GET https://searchcode.com/api/codesearch_I/?q=<term>` → 404
  ("page not found"); API path has moved/changed. Not usable as-is.

### Working endpoint found: Sourcegraph public search stream (anonymous, no key)
```
GET https://sourcegraph.com/.api/search/stream?q=context:global+<term>+select:content+fork:yes+archived:yes&v=V3&display=100
Accept: text/event-stream
```
- Params: `q` (Sourcegraph query syntax), `v=V3`, `display=N` (page size).
- Response: SSE-style events; event names: `filters`, `progress`, `matches`,
  `done`. `matches` events carry `data:` JSON arrays; item types include
  `"content"` (with `lineMatches`: line, lineNumber, offsetAndLengths),
  `"path"`, `"repo"`. The `done` event carries `matchCount`.
- Reusable pattern (like the uq_htmx.py wrapper): wrap this in a poller that
  accumulates `matches` items until the `done` event; useful query atoms:
  `context:global`, `select:content` (forces code, avoids fuzzy path noise),
  `fork:yes`, `archived:yes`, `file:<regex>`.
- CAVEAT: Sourcegraph does NOT index all of GitHub — it indexes a large
  curated subset of public repos. A negative here is weaker than a negative
  on GitHub's own code search. The grep.app hard stop leaves the strongest
  free surface unprobed this run.
- Note: `select:file` includes fuzzy PATH matches (e.g. `uqscan` matched
  "navigationMontage.m" by subsequence). Always use `select:content` and
  verify the matched line text.

Also used: Bing/Google via `site:github.com <marker>` and plain web search.

## Per-marker verdicts

| Marker | Verdict | Evidence |
|---|---|---|
| `uqscan` | FALSE POSITIVES ONLY (5 content hits, all noise) | Sourcegraph content hits: (1) `github.com/cerr/CERR` — `uqScanV` MATLAB variable in `CERR_core/Viewers/navigationMontage.m:693-702` (unique-scan-vector naming, unrelated); (2) `github.com/kallerosenbaum/grokkingbitcoin` x2 — "uqscan" substring inside base64-encoded PNG data in `images/ch05/05-15.svg`; (3) `github.com/opentofu/registry` — "uqSc" substring inside an H1 hash blob in `providers/s/square/anomalo.json:407`; (4) `github.com/sooshie/Security-Data-Analysis` — domain `www2.thebestuqscanner.25u.com` in `Lab_4/host_detections.csv` (scanner-product domain list). Web `site:github.com uqscan` → only qi4L/qscan and TorqueUpTech/Ultimate-CAN-Scanner (generic scanners). |
| `uqscan=` (with equals) | CLEAN NEGATIVE | Sourcegraph `uqscan=` → matchCount 0. Web `"uqscan=" OR "uqcors" github code` → no code hits. |
| `uqcors` | FALSE POSITIVE ONLY (1 content hit) | Sourcegraph: `github.com/apache/camel-quarkus` — "uqcors" substring inside a base64 image blob in `integration-tests/openai/.../chat_completions-...json` (WireMock mapping). Web `site:github.com uqcors` → only functional-cqrs README and a quasar commit (no marker). |
| `uqcors.html` / file:uqcors.html / uq_cors / uq_cors.html | CLEAN NEGATIVE | Sourcegraph matchCount 0 on all variants. |
| `pandalegacy` | CLEAN NEGATIVE | Sourcegraph content → 0. Web `site:github.com pandalegacy` → no results; plain `"sub_poi_navi" OR "pandalegacy"` → only unrelated panda content (PandarView manuals, Pandaland contest problem, Panda Adaptive Defense). |
| `sub_poi_navi` | CLEAN NEGATIVE | Sourcegraph content → 0; `sub_poi_navi+amap` → 0. Web `site:github.com sub_poi_navi` → only OSM/Navi navigation repos (no marker). |
| `lhr.life` in code | NO FLEET LINK | Web `site:github.com lhr.life` → all hits are generic localhost.run usage (tunnel docs, skills READMEs: bebabinlarsson-blip/Godot-MCP, thisisqubika/qubika-livecoding, stefanbx/xchat-alpha, rickyananda/hermes-skills, kami-shah733/phantom-network-scanner). Sourcegraph `lhr.life+amap` → 0. No repo combines lhr.life with Amap/POI collection. |
| `uqcors.html` / `probe.html` + lhr.life | CLEAN NEGATIVE | `file:probe.html` → 0. Web `site:github.com probe.html lhr.life` → only generic tunnel/probe docs (1broseidon/skills folio README, loyvanbeek/live_battlefield). |
| `injectPageScript` | GENERIC ONLY | Hits are browser-extension boilerplate and jina.ai reader docs (`jina-ai/reader` cookbooks — `injectPageScript` body field for r.jina.ai), plus `xaviersvk/cdd-stoich-tools`, `pardeep1916p/codesync`, `xulei-shl/book-echoes-aibot` docs. No link to the ltzh exfil family and none co-occurring with our markers. |

## Adjacent leads (NOT hits — no fleet markers in them)
These do NOT contain uqscan/uqcors/pandalegacy, but sit on the agent+tunnel
surface and are worth a look for tradecraft overlap:
- `zhouyoukang1234-spec/devin-remote` (14 stars, active 2026-06-27) — Chinese
  author, agent remote-access app ("rt-flow") with its own Go SSH reverse-tunnel
  client provisioning `*.lhr.life` URLs (localhost.run / serveo / pinggy),
  60s health-probe that recycles dead tunnels. Tunnel-provisioning code in an
  agent harness by a Chinese developer — worth diffing against the fleet's
  tunnel stack (nokey@localhost.run usage).
- `hamzah2304/messageboardauditbench` — report
  `reports/blind_verbatim_xhigh_p4436af8c/react_google_gemini-3.8-flash_r3_20260907T095543Z.md`
  documents agents reaching a wiki board via `504c4580fe50f1.lhr.life`
  (2026-06-17) — lhr.life tunnel reuse inside the agent-activity incident
  corpus (DataUSA construction sequence, Sector61 state, county.json RegCF
  surge). Shows the same tunnel provider in agent operations generally.

## Metadata captured
- False-positive repos (for the record): cerr/CERR (213★), kallerosenbaum/grokkingbitcoin (309★),
  opentofu/registry (410★), sooshie/Security-Data-Analysis (134★),
  apache/camel-quarkus (302★). RepoLastFetched all 2026-10-04/05 (index fresh).
- No harness repo, scanner config, tag-grammar generator, or
  tunnel-provisioning script containing fleet markers was found anywhere
  probed. The known-operator fleet (Chinese Amap data collection,
  `uqscan=<word><date>` tags, `<hex>.lhr.life` tunnels) appears to keep its
  harness OFF GitHub public code — or under terms not indexed by the surfaces
  reached.

## Open / recommended follow-ups
1. Retry grep.app (`https://grep.app/api/search?q=`) from a different route or
   later — it indexes far more GitHub repos than Sourcegraph; its 429 was a
   per-provider hard stop for this run only.
2. GitHub code search proper remains inaccessible without a signed-in session;
   the unauthenticated XHR endpoint does not exist (frontend calls the authed
   backend).
3. `devin-remote` lead: diff its SSH-tunnel client against the fleet's
   `nokey@localhost.run` tradecraft.
