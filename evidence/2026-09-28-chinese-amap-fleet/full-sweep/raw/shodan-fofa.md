# Shodan / FOFA sweep — Chinese Amap fleet IPs
Date: 2026-10-04/05 (UTC+8 Oct 5) | Surface: internet-scan data only | No pushes

## TL;DR verdict
**`106.11.226.79` and `47.246.165.44` are Amap (AutoNavi/高德)'s OWN Alibaba Cloud
ingress gateways — the fleet's TARGETS, not operator infrastructure.** Shodan hostnames,
TLS cert SANs (`*.autonavi.com`), and a leaked internal server name
(`gaode-aserver-ingress033001057226.os30`) all agree. The urlquery "IP/ASN" field is the
*target's* resolved IP (known limitation), so these IPs appearing in the fleet's
urlquery reports means the fleet was probing/scraping Amap's map frontends — consistent
with an Amap map-data-collection operation. Neither IP shows any agent/harness-shaped
traits (no extra ports, no scanning, no proxies, no tunnel exits).

---

## 106.11.226.79 — VERDICT: Amap domestic ingress (Hangzhou)

| Field | Value | Source |
|---|---|---|
| Shodan ports open | 80, 443 only | shodan.io/host/106.11.226.79 (meta + body) |
| Shodan hostname | `ea119-static.wagbridge.ingress.amap.com.gds.` (+ autonavi.com) | Shodan "Hostnames" |
| Country/City | China / Shanghai (ipinfo); Hangzhou (ip-api) | ipinfo.io, ip-api.com |
| Org / ISP / ASN | Zhejiang Taobao Network Co.,Ltd / Hangzhou Alibaba Advertising Co.,Ltd. / **AS37963** | Shodan + ipinfo + ip-api |
| HTTP banner (80+443) | `HTTP/1.1 404 Not Found` / `Server: Tengine/AServer-Ingress/3.0.46` | Shodan banner (scanned 2026-10-03, 2026-10-04); direct curl 2026-10-05 confirms same + `EagleEye-TraceId` |
| TLS cert SANs | `DNS:*.autonavi.com, DNS:*.is.autonavi.com, DNS:autonavi.com` (GlobalSign) | Shodan SSL section |
| GreyNoise | `noise:false, riot:false` — "IP not observed scanning the internet" | api.greynoise.io/v3/community (no key) |
| ip-api flags | hosting:true, proxy:false, mobile:false | ip-api.com (no key) |
| Co-hosted domains | none in HackerTarget reverseiplookup DB | api.hackertarget.com/reverseiplookup |
| urlscan presence | 1 scan (2026-09-23): `denizpeng-maptest.pages.dev` ("地图方案实测 · 手机版", Cloudflare Pages, certstream-suspicious) contacted this IP among 15 uniqIPs — i.e. a Chinese map-test page loading Amap resources from it | urlscan.io/api/v1/search (no key; result-detail API now login-walled) |

`wagbridge` = WAN gateway bridge; `gds` = Alibaba DNS/CDN (alibabadns.com). Tengine is
Alibaba's nginx fork; EagleEye-TraceId is Alibaba's internal distributed-tracing header.
This is Amap's domestic (Hangzhou/Shanghai) map-API ingress.

## 47.246.165.44 — VERDICT: Amap overseas ingress (Singapore)

| Field | Value | Source |
|---|---|---|
| Shodan ports open | 80, 443 only | shodan.io/host/47.246.165.44 |
| Shodan hostname | `os30.wagbridge.ingress.amap.com.gds.` | Shodan "Hostnames" |
| Country/City | Singapore | Shodan + ip-api |
| Org / ISP / ASN | Alibaba Cloud LLC / Alibaba (US) Technology Co., Ltd. / **AS45102** | Shodan + ip-api |
| HTTP banner (80+443) | `HTTP/1.1 404 Not Found` / `Server: Tengine/AServer-Ingress/3.0.46` / `EagleEye-TraceId` | Shodan banner (scanned 2026-10-02); direct curl confirms |
| Leaked server name | **`gaode-aserver-ingress033001057226.os30`** (高德 = Amap's Chinese name; `os30` matches the Shodan hostname) — disclosed in the Tengine 404 error page body served at `http://47.246.165.44/` | direct curl 2026-10-05 |
| TLS cert SANs | `DNS:*.autonavi.com, DNS:*.is.autonavi.com, DNS:autonavi.com` (GlobalSign) | Shodan SSL section |
| GreyNoise | `noise:false, riot:false` — not observed scanning | api.greynoise.io/v3/community |
| ip-api flags | hosting:true, proxy:false | ip-api.com |
| Co-hosted domains | `f.amap.com`, `www.amap.com` | api.hackertarget.com/reverseiplookup |
| urlscan presence | 1 scan (2026-09-11): `ent-dafa.com` (Chinese gambling) contacted this IP among 23 uniqIPs — incidental third-party load (map widget/tracker) | urlscan.io/api/v1/search |

`www.amap.com` currently resolves via `www.amap.com.gds.alibabadns.com` → 47.246.174.241
(same Alibaba SG netblock; CDN IPs rotate) — confirms this netblock is Amap's CDN edge.
This is Amap's overseas (Singapore) map-API ingress.

## "Agent-shaped?" checks — CLEAN NEGATIVE on both IPs
- Ports: only 80/443 per Shodan. Direct light banner probes to 22/3000/8000/8080/8888/3128/1080/3389/5900 returned nothing — **caveat:** this VM egresses through an HTTP proxy (CONNECT seen on 443), so non-80/443 direct probes are unreliable; Shodan's port list is the ground truth here.
- No SSH, no open proxies, no scanner behavior (GreyNoise negative on both).
- No tunnel-exit traits (see localhost.run section below).
- Banners are uniform Alibaba ingress (Tengine/AServer-Ingress/3.0.46), not harness/probe-page banners.

## Tunnel-exit patterns (localhost.run) — LEAD CONFIRMED, IPs EXCLUDED
- localhost.run's SSH endpoint (`ssh.localhost.run` / `localhost.run`) resolves to AWS US-East: **35.171.254.69, 54.161.197.247, 54.82.85.249** (DoH via cloudflare-dns.com). Neither fleet IP matches → **clean negative: the two Amap IPs are NOT localhost.run exits.**
- Confirmed via public docs that **localhost.run issues `*.lhr.life` tunnel URLs** (e.g. `https://<hex>.lhr.life`), matching the fleet's known `<hex>.lhr.life` tunnel pattern — so the fleet's probe pages are exposed through localhost.run exits (the AWS IPs above), while the Alibaba IPs are the scrape targets. Tunnel-exit Shodan fingerprinting (e.g. `ssl:"lhr.life"`) was **blocked, not negative**: Shodan `/search` is login-walled for anonymous users from this VM (see below).

## Agent-harness banner hunts (`uqscan`, `uqcors`, probe-page titles)
- **Web search for `"uqscan" OR "uqcors"`**: zero public hits — these tags exist only inside urlquery report metadata, not indexed anywhere. Clean negative on public indexing.
- **Shodan banner/title search for these strings**: BLOCKED, not negative — Shodan's `/search?query=...` returns a login wall for anonymous requests (6.9KB page, "Log in"). Needs a Shodan account; flag for a follow-up with credentials.
- **FOFA banner search**: BLOCKED — FOFA requires login for all search; API returns `{"error":true,"errmsg":"[-700] 账号无效"}` without credentials (see endpoints below).

## Undocumented / no-key endpoints found (reusable)
Per collection doctrine (no API key is not a stop), probed and documented:
- `GET https://www.shodan.io/host/<ip>` — server-rendered, anonymous OK (intermittent IP rate-limiting: got HTTP 000/timeouts for ~15 min after 3 rapid hits, then recovered). Ports in `<meta name="twitter:description">`; hostnames/ASN/banners/cert SANs in body. **Shodan `/search?query=` is login-walled** — host pages are the only anonymous surface.
- `GET https://api.greynoise.io/v3/community/<ip>` — no key, returns noise/riot/observation status. Both IPs: not observed scanning.
- `GET https://ipinfo.io/<ip>/json` — no key, rate-limited; `http://ip-api.com/json/<ip>?fields=...` — no key, fast, includes `hosting`/`proxy` flags.
- `GET https://api.hackertarget.com/reverseiplookup/?q=<ip>` — no key, co-hosted domains (found f.amap.com/www.amap.com on .44). `reversedns` and `dnslookup` also no-key. **`/nmap/` now requires a key** ("error valid key required").
- `GET https://urlscan.io/api/v1/search/?q=ip%3A<ip>` — no key, finds scans that contacted the IP. **`/api/v1/result/<uuid>/` now requires login** (`{"warning":"You're not logged in!"}`) — can no longer enumerate which request hit the IP anonymously.
- `GET https://cloudflare-dns.com/dns-query?name=<h>&type=A` with `Accept: application/dns-json` — no-key DoH, used to resolve localhost.run infra.
- FOFA (from `https://v5static.fofa.info/_nuxt/<hash>.js` bundle + probes): frontend XHRs include `/api/v1/search/stats`, `/api/v1/search/all` (both → `[-700] 账号无效` without auth), plus app-internal `/search/stats/fid`, `/search`, `/m/assets/update`, `/check`, `/m/message/unread`. **No unauthenticated FOFA query path found** — FOFA is a dead end without credentials.
- `https://crt.sh/?q=%25.amap.com&output=json` — no-key cert transparency (1,223 certs; confirms Amap's `*.amap.com` estate).

## Open leads / follow-ups
1. The real operator infra is upstream of the tunnels: localhost.run exits (35.171.254.69, 54.161.197.247, 54.82.85.249) only forward traffic — the agents sit behind them. The `<hex>.lhr.life` subdomains seen in urlquery reports are the observable operator surface.
2. Shodan/FOFA banner hunts (`uqscan`, `uqcors`, `ssl:"lhr.life"`, `hostname:*.wagbridge.ingress.amap.com.gds`) need credentials — flag for a credentialed follow-up; Shodan anonymous search is login-walled.
3. Sibling Amap ingress nodes (`ea119-static…`, `os30…` naming) suggest a larger `*.wagbridge.ingress.amap.com.gds` fleet mappable via DNS/ASN enumeration — target-surface mapping, not operator infra.
4. urlscan `ip:` hits show Chinese third-party sites loading Amap resources from these exact IPs — the same `ip:` operator can be re-run periodically as a tripwire for new pages embedding Amap endpoints.
