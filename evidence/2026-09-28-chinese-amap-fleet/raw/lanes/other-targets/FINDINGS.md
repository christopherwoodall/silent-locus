# FINDINGS - other-Chinese-targets lane (Amap fleet hunt)

Sweep date: 2026-10-04. Window: 2026-09-28 to 2026-10-05 on all queries.
Raw JSON in raw/ (q1_baidu.json, q2_qqmap.json, q3_uqscan page files x13,
q4_ditu.json, q5_lbsqq.json, full report files x2, clusters.json).
A naive 429 guard tripped once on a content match ("429" inside report bodies);
a real 429 was never hit. No pushes to git.

## Queries and counts

| # | Query | Hits | Verdict |
|---|---|---|---|
| q1 | url.domain:map.baidu.com, in-window | 0 | Honest zero - fleet does not touch Baidu Maps |
| q2 | url.domain:map.qq.com, in-window | 0 | Honest zero - fleet does not touch Tencent Maps (web) |
| q3 | keyword uqscan, in-window, all domains | 1208 total, 1205 retrieved | Fleet grammar sweep - see cluster table |
| q4 | keyword ditu, in-window | 40 | 6 fleet (ditu.amap.com), 34 unrelated |
| q5 | lbs.qq.com, in-window | 0 | Honest zero - fleet does not touch Tencent Maps API |

## Headline verdict

**The fleet tag grammar hits NO non-Amap targets in-window.** Zero reports target
map.baidu.com, map.qq.com, lbs.qq.com, tianditu.gov.cn, meituan, dianping, or ctrip -
in submitted or final URLs across all 1,245 reports. The operation is Amap-exclusive
(amap.com / gaode.com / ditu.amap.com plus relay and carrier infra).

## q3 uqscan sweep - cluster verdicts (1,205 reports)

| Domain | n | Verdict |
|---|---|---|
| amap.com | 1010 | Known fleet target |
| httpbin.org | 112 | Known fleet carrier |
| gaode.com | 18 | Amap own alt domain - same fleet |
| example.com | 16 | Fleet self-tests (claude20261004test, testnohx, ctrl20261004, customua-20261004) - tag-plumbing calibration, not a target |
| httpbun.com | 10 | Known fleet carrier |
| postman-echo.com | 5 | NEW fleet redirector: redirect-to to Amap SSR place and getPoiInfo URLs (tags orangeisle20261004e, stadium-postman-1791125549, cdzoo20261004redir1, mf-api-1791105341) |
| livecodes.io | 4 | Known fleet carrier |
| ceshiren.com | 4 | NEW Chinese-infra carrier |
| kennethreitz.org | 2 | NEW fleet redirector via httpbin-style redirect-to endpoint |
| google.com | 2 | NEW fleet redirector via google url redirect endpoint |
| urlquery.net | 2 | Fleet self-surveillance: search for its own place ID B00190BC3W with tag target-search-1791120942 |
| tinyurl.com | 1 | Confirmed fleet: full report shows short link resolves to Amap SSR place page with tag short-1791125822 |
| 59.82.121.95 and 203.119.204.85 | 2 | IP-direct Amap tests: both Hangzhou Alibaba Advertising Co., Ltd. (CN), Amap edge; getPoiInfo API path with sequential tags ls17911058006 and ls17911058007 |
| spoo.me | 3 | NEW fleet redirector: shortener to Amap place URLs (tags hppopup1, hplaunch4) |
| httpbingo.org | 3 | NEW fleet carrier/redirector: base64 programs titled Amap top-level redirect 1790824679 and NAV (tag yipenghtmlnav6), plus redirect-to to Amap (tag zhaolin-page-redirect-20261004f) |
| href.li | 3 | Known fleet redirector |
| amap-pc-ssr.amap.com. | 3 | Trailing-dot variant of Amap SSR host - same fleet |
| nghttp2.org | 2 | NEW fleet redirector: nghttp2 httpbin-style redirect-to to Amap (tags orangeisle20261004d, www20261004r) |
| da.gd | 1 | Shortener stub, target dead; 0 uqscan even in full report - ambiguous, likely expired fleet probe |
| translate.goog relays | 2 | Known fleet relays of Amap pages |

## New findings beyond the verdict

- New tag params uqtarget and uqhost seen on 4 reports, all on the Amap ditu subdomain.
  Examples: uqtarget=pd-ditu-9674e8e9-a631-4aeb-9b6d-a3a4771d80f3,
  uqtarget=api-ditu-8b1c40ad-4505-4b27-afeb-e05f2e34e0ae,
  uqtarget=laoshan-ditu-20261004a, uqhost=ditu-1791116586.
  PATTERN.md lists only uqscan and uq - the param set is wider.
- The Amap ditu subdomain is itself a fleet target surface.
- Redirector diversification on 4 Oct: postman-echo, kennethreitz.org, nghttp2.org,
  google url-redirect, spoo.me, and httpbingo.org join the previously known href.li -
  same redirect-to-Amap shape, same tag grammar.
- Chinese infra adoption: the ceshiren.com httpbin mirror is the first China-hosted
  carrier observed (prior carriers were httpbin.org and httpbun.com).
- Fleet watches its own traces: urlquery.net self-search on place ID B00190BC3W.

## Constraints honored

No human or operator identity pursued (analysis on submitted URLs, tags, and program
shapes only). Nothing pushed to git. No news, blog, or social coverage searched - traces only.
