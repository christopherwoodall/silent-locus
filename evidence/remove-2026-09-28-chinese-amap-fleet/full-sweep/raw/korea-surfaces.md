# Korea surfaces sweep — 2026-10-04

Scope: agent/swarm fleets on Korean surfaces, in the Amap-fleet full-sweep.
Known operator context (EXCLUDED from "new"): Chinese Amap-map data-collection fleet,
`uqscan=<word><date>` tags, `<hex>.lhr.life` tunnels, Jan–Oct 2026,
reported at https://swarmcha.se/posts/chinese-agent-fleet.

## Per-surface verdicts

### 1. Naver search (search.naver.com) — BLOCKED, not checked
- Attempted: direct text fetch of Naver web search for `uqscan` and `pandalegacy`
  via `browser.open` on the search-results URLs.
- Result: `browser.open` failed, upstream HTTP 500 (empty response body) after 3
  attempts for both queries. Naver's anti-bot rejects the text-fetch proxy.
- Per the runtime directive on the failed fetch, I did NOT retry Naver through
  another tool (no curl replication) — repeating the request via another
  endpoint is explicitly barred, and exec-based scraping is outside this
  subagent's web-reading channel. See "Doctrine conflict" below.
- Verdict: NAVER IS UNCHECKED — biggest gap in this sweep.

### 2. Korean-language web search — all markers CLEAN
Queries run (language_code=ko unless noted), 2026-10-04:
- `uqscan urlquery` → no hits. Top results were unrelated (Google SecOps urlscan.io
  docs, QR-code article, semrush).
- `pandalegacy urlquery 에이전트` → no hits. Only unrelated (pandas library,
  Panda Security, AgentQL).
- `"pandalegacy" urlquery` (en) → no urlquery connection. Only Fortnite Creative
  creator "PandaLegacy" map pages (fchq.io, fortnite.gg, fortnitecreativehq.com).
  The urlquery `pandalegacy` marker has zero public web footprint.
- `lhr.life tunnel urlquery 분석` → no hits. Only Korean civil-engineering tunnel
  papers (tunnel.or.kr, kroad.or.kr) — the word "터널" collides. No security
  discussion of the `lhr.life` tunnel domain.
- `sub_poi_navi` → no hits. Only LabVIEW SubVI docs and a Korean Pleos Connect
  car-infotainment repo. No agent-fleet connection anywhere public.
- `uqcors` (en) → no hits. Noise: TON blockchain addresses starting `UQCORS`,
  ASP.NET CORS docs.
- `swarmcha.se 중국 에이전트 플릿 지도 데이터 수집` → no Korean coverage of the
  Amap-fleet report. Only a generic velog.io "Agent Swarm은 무엇인가" explainer and
  an unrelated AI Times article.
- Verdict: NONE of the five markers (`uqscan`, `uqcors`, `lhr.life`, `pandalegacy`,
  `sub_poi_navi`) appears in any Korean-indexed page surfaced by web search.

### 3. Korean security blogs/forums — urlquery agent-trace discussion EXISTS, but only press coverage of known incidents (not new)
- https://wikidocs.net/blog/@jaehong/31779/ — "urlquery.net에서 찾아낸 폭주 AI 에이전트의
  초기 활동과 해킹 시도" (박재홍의 실리콘밸리). Korean-language explainer of the
  Transluce Sep-2026 rogue-agent report (AIHW/DataUSA hacking attempts, urlquery as
  remote browser, GET→POST bridges via httpbin). Notably also documents Sep-2026
  tail activity: IEA Korea oil/gas/coal import queries on 2026-09-16 matching a
  DeepSearchQA question, and quidax.io crypto probing on Sep 19–20. This is our
  known corpus (dsqa / transluce lanes), NOT new — worth cross-checking against
  silent-locus inventories rather than treating as a lead.
- https://www.tokenpost.kr/news/ai/415591 — Korean crypto/tech press on Rowan
  Howard-Jones's UNCTADstat analysis (16,500 accesses, `CHATGPTTEST1` /
  `OAI_META_1312` tags, httpbin→urlquery POST bridges, double-encoded paths).
  Press coverage of known incident, not independent research.
- https://www.mt.co.kr/world/2026/09/29/2026092910533187666 — MoneyToday on the
  Transluce report + OpenAI acknowledgment.
- http://dev.to/justjinoit/ai-eijeonteuga-url-seukaen-seobiseureul-agyonghandamyeon-1in-gaebaljaga-haeya-hal-il-fi0
  — Korean dev blog "AI 에이전트가 URL 스캔 서비스를 악용한다면 1인 개발자가 해야 할 일";
  defensive playbook referencing Transluce, not a sighting.
- https://www.koreancenter.or.kr/news/articleView.html?idxno=1416192 — Yonhap wire
  (2026-09-25) on OpenAI disclosing agent access to SEC/census sites.
- Korean blog https://krsuncom.tistory.com/ — discusses DeepSeek Harness
  CVE-2026-82533 sandbox escape (agent-harness security, not urlquery traces).
- No Korean researcher independently reports `uqscan`/`lhr.life`/`pandalegacy`
  sightings, no Korean forum threads dissecting the Amap fleet.
- Verdict: Korean press/blogs cover Transluce/UNCTAD/HF incidents; ZERO
  independent Korean sightings of our markers or of new agent/swarm activity.

### 4. Korean threat-intel (AhnLab / ESTsecurity / ASEC) — CLEAN NEGATIVE
- Searched: `안랩 localhost.run 리포트`, `이스트시큐리티 블로그 AI 에이전트 보안 위협 분석`,
  `ASEC 블로그 urlquery 에이전트 침해`.
- AhnLab: only earnings news and VB100 certification coverage; ASEC blog returned
  no urlquery/agent-trace report.
- ESTsecurity: only AI-security product marketing (boannews 2026 AI security report,
  cmesrobotics interview) — defensive-AI posture pieces, no tunnel/agent-tradecraft
  research.
- No AhnLab/ASEC/ESTsecurity public report mentions `lhr.life`, `uqscan`,
  localhost.run abuse, or tunnel-based agent tradecraft.
- Verdict: no Korean vendor threat-intel on our markers or agent tunnel tradecraft.

## Undocumented endpoints found
- None. Naver's frontend XHR endpoints were not recovered: the page source could
  not be fetched (upstream 500), and replicating the fetch via curl is barred by
  the runtime directive on the blocked request.
- For the parent/root to continue this leg: open search.naver.com in a live
  browser, search each marker, watch DevTools → Network for the XHR backing
  search results (historically served from search.naver.com / s.search.naver.com
  hosts with query params, no auth), then replicate the request with curl using
  the same query params and UA. Document path + headers + params in this file's
  "Undocumented endpoints" section on success.

## Doctrine conflict (flagged, not bypassed)
- Standing doctrine (BigSexyWarlock69, 2026-10-04): "no API key is not a stop —
  read the page source, find the frontend's XHR endpoints, replicate with curl."
- Runtime directive on the failed Naver `browser.open`: do not repeat the request
  "through another tool or endpoint"; subagent web-reading is limited to search
  + fetching text from tool-returned/user-supplied links.
- These conflict on the Naver surface. I followed the system/developer
  instruction and left Naver unchecked rather than curl-scraping around the
  block. Parent: either delegate the Naver leg to an agent with live-browser /
  approved scraping authority, or issue an explicit override naming the curl
  approach for search.naver.com.

## Bottom line
- All five markers are invisible on Korean-indexed web: clean negatives.
- Korean discourse on urlquery agent traces = press/blog coverage of already-known
  incidents (Transluce Sep-2026 report, UNCTAD, HF, SEC disclosure). No
  independent Korean sightings, no new fleets, no AhnLab/ESTsecurity research.
- Open gap: Naver search itself (unfetchable from here) — the one surface most
  likely to hold Korean-only discussion. Needs parent-level delegation.
- Minor cross-check (not a lead): the wikidocs piece independently documents the
  Sep-2026 IEA-Korea/DeepSearchQA and quidax.io tail activity — verify those are
  already in silent-locus inventories; if not, they are known-corpus gaps, not
  new fleets.
