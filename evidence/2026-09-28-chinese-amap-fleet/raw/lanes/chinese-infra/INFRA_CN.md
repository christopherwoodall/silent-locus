# INFRA_CN.md — Chinese-native web infrastructure: agent-fleet inventory (2026-10-05)

Question: do Chinese agent fleets use Chinese-native web utilities, or Western ones? Answer from the Tencent Amap fleet's urlquery traffic plus urlquery-wide checks.

## Headline finding

**The fleet barely uses Chinese-native infra — and the reason is login walls.** Chinese shorteners (t.cn, dwz.cn) and pastebins (yuque, luogu) require accounts; Western equivalents (jina, webhook.site, dpaste.com, LiveCodes) don't. Agents optimize for no-login. The one exception is **`fanyi.baidu.com` (Baidu Translate) as a fetch proxy** — no login needed, and it renders Chinese pages.

## URL shorteners

| Service | Who runs it | Login needed? | urlquery evidence | Verdict |
|---|---|---|---|---|
| `t.cn` | Weibo | Yes (Weibo acct) | 0 as submitted URL; 65 keyword hits all coincidental page text | UNUSED — login-walled |
| `dwz.cn` | Baidu | Yes (Baidu acct) | 4 reports, all Dec 2025, untagged — not the fleet | UNUSED by agents |
| `suo.im` | independent | No | 1 report (Dec 2025, `suo.im/5zVbEL`), untagged — not agent-shaped | UNUSED by agents |
| `m.cn` | unknown | — | 21 keyword hits, coincidental | UNUSED |
| SMS short links (阿里云/火山引擎/云片) | Alibaba/ByteDance/Yunpian | Yes (API key) | — | Enterprise-only, not agent-usable anonymously |

## Pastebins / text-sharing

| Service | Who runs it | Login needed? | Verdict |
|---|---|---|---|
| `yuque.com` (语雀) | Alibaba | Yes | UNUSED — login-walled |
| `luogu.com.cn` cloud clipboard | Luogu | Yes (account) | UNUSED by agents |
| DIY paste tools (V2EX scene) | individuals | No | Fragmented, no dominant service; zero urlquery presence |

The fleet uses `dpaste.com`, `paste.page`, `paste.c-net.org` (Western, no-login) per the swarmcha.se report.

## JS sandboxes / live-code pages

| Service | Who runs it | urlquery evidence | Verdict |
|---|---|---|---|
| `jsrun.net` | independent (CN) | 0 reports | UNUSED |
| `runoob.com` (菜鸟教程 editor) | Runoob | 0 reports | UNUSED |

The fleet stages programs on `livecodes.io` (26 reports) and `httpbun.com/base64` (65 reports) — Western, no-login.

## Dead-drop / request-inspection

| Service | Verdict |
|---|---|
| Chinese webhook.site equivalent | **None found.** Chinese developers use webhook.site itself (well-documented on CSDN, mirrored on gitcode.com). No Chinese-native request-bin with public logs identified. |
| Fleet dead-drops | `webhook.site` inboxes (17 amap-associated reports), created from Tencent Cloud |

## The exception: Baidu Translate as fetch proxy

| Service | Evidence |
|---|---|
| `fanyi.baidu.com/transpage` | Fleet use confirmed: `fanyi.baidu.com/transpage?query=https%3A%2F%2Famap-pc-ssr.amap.com%2Fssr%2Fapi%2FgetPoiInfo%3Fid%3D…` (reports `968009e0`, `a255dfb9`, 2026-10-04). Nested: `href.li/?https://fanyi.baidu.com/transpage?query=…` (redirector → Baidu Translate → Amap API). Baidu-flavored cache-buster `uq=baidu…` observed in the same chain. |

This is the fleet's translate.goog equivalent — and the only Chinese-native service in their kit. 593 total `fanyi.baidu.com` urlquery hits; non-Amap traffic is ordinary human browsing (no other agent-shaped use found in sampled pages).

## Why this matters (watchlist logic)

1. **Login walls are the filter.** Any Chinese web utility requiring an account (Weibo, Baidu, Alibaba) is effectively invisible to anonymous agent fleets. Hunt Chinese agents on no-login services — Western or Chinese.
2. **`fanyi.baidu.com/transpage` is the Chinese fetch-proxy to watch.** Same role as `r.jina.ai` / `translate.goog`. Other Chinese agents doing web tasks will use it.
3. **No Chinese dead-drop service exists with public logs** — webhook.site remains the place to watch, even for Chinese actors.
4. **Shortener absence is itself a signal**: a Chinese agent fleet using t.cn/dwz.cn would imply it holds Chinese platform accounts — a step up in operational maturity from the current anonymous fleet.

## Clean zeros (checked, absent)
`t.cn`, `dwz.cn`, `suo.im`, `m.cn` as agent infrastructure; `jsrun.net`, `runoob.com`; `hysandbox` anywhere on the web; Chinese pastebin dead-drops; `uqscan=` outside the Amap fleet (1,217 hits, all fleet).
