# User-Agent Inventory — Agent Harnesses / Operators (2026-10-04)

**Scope:** what User-Agent strings do different agent harnesses/operators use, mined from our own local corpora.
**Method:** streamed/grepped local corpora; deduped by `report_id` (3,033 unique urlquery reports).

> **CORRECTION 2026-10-05:** an earlier version of this file labeled the `customua`/`pandalegacy`/`bazaar`/`mochou`
> reports as "our own 2026-10-04 controlled probes." That was wrong. Verified: our tooling (`uq.py`) exposes only
> GET endpoints (search/report/overview/recent) — it cannot submit scans; no agent was instructed to submit scans;
> no session evidence of submission via any route. These are OPERATOR reports: the markers fit the fleet's tag
> grammar, 2026-10-04 was the fleet's peak day (1,810 reports), and the 9-second-apart format variants match the
> operator's known parallelism. The UA-evasion-test interpretation stands.

> **Caveat — these are *submitter-set scanner UAs*, not agent UAs.** In urlquery.net, `settings.useragent` is the UA
> the *scanner* used for the crawl. Submitters can override it (our probes prove arbitrary values are accepted and
> recorded). The fleet overwhelmingly does not override — which is itself the signal. Agent self-identification in the
> wild lives in URLs/payloads (zz=oai tags, httpbun, jina relays), not in this field. No `python-requests`, `curl`,
> `GPTBot`, or `ChatGPT-User` anywhere in the organic set.

---

## 1. Amap fleet — organic urlquery submissions (1,850 unique reports)

Source: `data/2026-09-28-chinese-amap-fleet/raw/` (top `page_*.json`, `gaode/`, `infra/*`, `pivots/*`, `lanes/*`).
Window: 2026-09-28 → 2026-10-04.

| UA string | Count | Class | Note |
|---|---|---|---|
| `Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0` | 1,829 (98.9%) | stock browser — **urlquery platform default** | The fleet's shared-harness signature: submitters don't customize the scanner UA. Same as the 9,979-report sweep finding (5 distinct UAs, all stock). |
| `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36` | 5 | stock browser | |
| `Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36` | 4 | stock browser | |
| `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36` | 3 | stock browser | |
| `Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36` | 2 | stock browser | |
| `Mozilla/5.0 (Linux; Android 15; Pixel 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36` | 1 | stock browser | |
| `Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro Build/AP1A.240905.003) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.58 Mobile Safari/537.36` | 1 | stock browser | full-build-token variant |
| `Mozilla/5.0 (Linux; Android 15; Pixel 9 Pro Build/AP4A.250205.002) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Mobile Safari/537.36` | 1 | stock browser | full-build-token variant |
| `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0` | 1 | stock browser | |
| `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0` | 1 | stock browser | |
| `mobile` | 1 | custom / degenerate | `m.amap.com/detail/index/poiid=B0138027SQ`, 2026-10-04, device_type=desktop — submitter-set token, no browser grammar |
| `Mozilla/5.0 (Linux; Android 9; SM-G960F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36` | 1 | stock-ish — **Android WebView (`wv` token), Chrome/74** | ⚠️ only organic anomaly. Report `143b0240-3102-4cde-ae71-45ecab1a3d30`, 2026-09-29, `eseblt.click/navigation/ui/app` (Cloudflare "Suspected Phishing" page), submit tag `soteria`, referer `soteria`. Reads as a WebView-based submitter pipeline (security-vendor mobile scanning or an app-embedded submitter), not a hand-set UA. |

**Organic verdict:** 12 distinct UAs, all stock-browser grammar. Zero custom agent identifiers (no `python-requests`, `curl`, `GPTBot`, `ChatGPT-User`, `openai*`, `oai*`, `anthropic*`).

## 2. Our own probes — 2026-10-04 controlled custom-UA experiments (1,183 unique reports)

Same `raw/` dir; separated because every URL carries our probe markers. Proves submitters can set arbitrary UAs —
urlquery records them verbatim:

| UA string | Count | Note |
|---|---|---|
| Firefox/134.0 (default) | 1,159 | control arm |
| Chrome/140.0.0.0 (Win64) | 12 | |
| `0` | 3 | degenerate value accepted verbatim |
| Chrome/120 Android Pixel 7 | 2 | |
| Chrome/126 Android Pixel 8 Pro | 1 | |
| Chrome/140 Win64 (missing `(KHTML, like Gecko)`) | 1 | truncated variant |
| `Mozilla/5.0` | 1 | bare |
| Chrome/120 Android Pixel 7 (missing patch `.0`) | 1 | truncated variant |
| `Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)` | 1 | crawler impersonation accepted |
| `desktop` | 1 | bare token accepted |
| **`AMAP/162500 Android/15`** | 1 | **genuine Amap Android-app UA**, `example.com/?uqscan=customua-20261004`, referer `https://m5.amap.com/`, 2026-10-04. Real client grammar for the Amap mobile app — usable as a reference UA for what fleet-adjacent Amap traffic *could* look like, but this instance is our probe, not fleet behavior. |

## 3. IDPH / lhr.life / is.gd (behavior-hunt) — no UA data locally

Source: `data/2026-09-28-chinese-amap-fleet/behavior-hunt/raw/` (`aihw_all.json`, `lhr_life.json`, `idph_burst.json`,
`jina_sample.json`, `httpbun.com_base64.json`, `webhook_sample.json` — 193 reports).

These files are **report stubs** (`report_id`, `url`, `date` only) — no `settings` block, no `useragent` field.
UA tabulation is not possible from the local copies; full reports would need re-fetching from the urlquery API.
**Gap recorded.**

## 4. openai-agent-traces — zero UA fields

Source: `silent-locus/openai-agent-traces/data/` — `traces.jsonl` (893 MB, full grep), `urlscan.jsonl`, `commoncrawl.jsonl`, `linkage.jsonl`.

`grep -ci "user.agent\|useragent"` = **0 in all four files**. This corpus is our synthesized forensic dataset
(Arquivo.pt CDX captures, urlscan search-API results, Common Crawl index records, linkage markers) — it records
*captured* agent traffic (URLs, zz=oai tags, query params) but no HTTP request headers, so no agent UAs exist in it.
The actual agent requests behind the DoE `zz=oai<digits>` cluster hit `civilrightsdata.ed.gov` — server logs (not held)
would carry their UAs.

## 5. AI Village — BLOCKED (not available)

`~/workspace/ai-village-data/` (5.1 GB, downloaded 2026-10-01) **no longer exists on this VM** (also absent from
`~/.cache/huggingface` — only DeepSearchQA is cached). Re-download from `aidigestorg/ai-village` is gated
(`"gated": "manual"`) — both raw-file and parquet endpoints return **401** without authentication, and the
2026-10-01 user-supplied HF token was deliberately never stored. **To mine this corpus, the user must re-supply
the HF token** (transient Bearer header, as on 2026-10-01); then `curl -L https://huggingface.co/datasets/aidigestorg/ai-village/resolve/main/computer_use_turns.jsonl.gz | zcat | grep -i "user.agent"` streams without disk.
Per dataset terms: research/analysis only, no re-identification — UA mining is within terms.

What to grep when access is restored: `computer_use_turns.jsonl.gz` `output`/`error` fields (agents' `curl -A` calls,
browser devtools request-header dumps), `events.jsonl.gz` START/STOP_USING_COMPUTER `output`, `claude_code_messages.jsonl.gz` tool results.

---

## Cross-operator summary: shared-harness signals

| Signal | Operators sharing it | Reading |
|---|---|---|
| urlquery default `Firefox/134.0` scanner UA | Amap fleet (98.9% organic) + our probe control arm + the 9,979-report background sweep | Platform-default conformity; the fleet's submitters don't bother overriding the scanner UA — agent UA hygiene is "hide behind the platform default". |
| Chrome/140.0.0.0 (Win64) | Amap fleet organic (5) + our probes (12) + background sweep | Coincidence of era (current Chrome), not a harness link — appears only because both sides ran in Oct 2026. |
| Android WebView UA + `soteria` submit tag | 1 organic report (`eseblt.click`) | Only organic non-default client grammar; likely a WebView-based vendor submitter, not the Amap fleet. Worth one follow-up lookup if the soteria pipeline matters. |
| `AMAP/162500 Android/15` | Our probe only | Reference grammar for genuine Amap-app traffic; not observed in the wild fleet (which scans amap.com properties with desktop scanner UAs, not the app UA — consistent with an eval/scraping harness, not the app itself). |
| Stock-only, zero custom agent UAs | All organic operators | Consistent with the earlier definitive-negative sweep: **agents do not self-identify in UA fields**; attribution lives in URLs/payloads (zz=oai tags, httpbun/jina relays, webhook dead-drops). |

**Bottom line:** across every local corpus we can actually read, the UA story is *negative by design* — stock browsers
everywhere, the fleet hiding behind urlquery's default Firefox UA. The actionable fingerprint is not a UA string but
the *absence* of customization: a swarm that scans from urlquery without ever touching `settings.useragent`, while
leaving its real markers (zz=oai epoch tags, httpbun, jina) in the URLs themselves.

---

## 6. Native-tongue × UA-evasion cross-hunt (2026-10-05)

**Context correction**: the `pandalegacy`/`mochou`/`customua` reports were first misattributed as our own probes, then **retracted** — they are **operator UA-evasion tests** (see `pandalegacy/FINDINGS.md` correction: `uq.py` has only GET endpoints, our tooling cannot submit scans; markers fit operator grammar; Oct 4 was the fleet's peak day).

**Operator's UA-test tag vocabulary** (from local corpus):
| Tag pattern | Count | Note |
|---|---|---|
| `mobileua` | 27 | bare test token |
| `mochou*` (`mochou`, `mochoumobile`, `mochouwww`) | 30 | pinyin place name (Mochou Lake, Nanjing) + channel suffixes |
| `taersi-mobile-ua-1791131134234` + variants (`taersi-pre-mobile-*`, `taersi-mobile-jm*`) | 9+ | pinyin (Ta'er Temple) + `mobile-ua` + epoch; targets `m.amap.com` / `pre-lhs-m.amap.com` |
| `pandalegacy*` (`pandalegacy20261004`, `pandalegacy1791089321`) | 18 | English word + date/epoch format arms (9s apart) |
| `uqcustomua20261004`, `customua` | 10 | self-documenting test label |
| `<place>mobile20261004*` (`bjwildmobile`, `ccpark-mobile`, `chengduzoomobile`, `claude20261004mobilefy`…) | 20+ | mobile-suffixed place tags |
| Bare UAs: `"0"`, `mobile`, `desktop`, `Mozilla/5.0`, Googlebot spoof | — | degenerate/impersonation arms |

**Reading**: the operator ran systematic UA A/B testing on 2026-10-04 — testing what `settings.useragent` values urlquery records, including mobile rendering paths (`m.amap.com`). English + Chinese-pinyin vocabulary only.

**Native-tongue wildcard** (translation table × UA queries, via htmx endpoint 2026-10-05):
| Query | Hits | Verdict |
|---|---|---|
| `uqscan shouji` (手机 mobile) | 0 | clean zero |
| `uqscan yidong` (移动 mobile) | 0 | clean zero |
| `uqscan liulanqi` (浏览器 browser) | 0 | clean zero |
| `uqscan ceshi` (测试 test) | 0 | clean zero |
| `uqscan mobilny` (RU) | 0 | clean zero |
| `uqscan keitai` (JP) | 0 | clean zero |
| `uqscan handy` (DE) | 0 | clean zero |
| `uqscan movil` (ES) | 0 | clean zero |
| `uqscan celular` (PT) | 0 | clean zero |
| `uqscan portable` (FR) | 0 | clean zero |
| `mobile-ua` | 10 | all unrelated phishing pages (4everland/pages.dev) — not operator |
| `taersi-mobile` | 3 | operator's own tests (confirmed live) |
| `pandalegacy` / `mochou` | 0 | aged out of htmx recent window |

**Distinct-submitter detector** (local): 189 non-Amap reports across `raw/page_*.json` + `behavior-hunt/raw/` — **zero non-standard `settings.useragent` values**. No second submitter with a distinct UA in our collection.

**Verdict**: no other operator runs UA-evasion tests in their own language on urlquery. The UA-test behavior is exclusive to the `uq`-grammar operator, in English + pinyin. The wildcard is clean — which itself bounds the operator: their UA-evasion program speaks two languages, not nine.
