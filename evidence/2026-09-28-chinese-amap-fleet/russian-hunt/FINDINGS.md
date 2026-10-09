# Russian Hunt — Findings (2026-10-05)

Question: is there a Russian-ecosystem agent fleet on urlquery.net comparable to the Chinese Amap fleet? Ran the same TTP playbook: map-target scanning, native infra, relay stack, language n-grams, lab fingerprints.

## Verdict: no Russian fleet on urlquery — honest zeros across all five lanes

The detection net that caught the 2,000-report Chinese fleet catches nothing Russian. Either Russian agent operations don't use urlquery-visible infrastructure, or nothing operates at this scale/loudness.

## Lane 1 — Yandex Maps as target: ZERO

- `url.domain:yandex.ru`: **90 total hits**, all routine — homepage (24), Metrica (20), yandsearch (7), disk shares (6), forms, video, radio, calendar. Zero maps-place systematic scanning, zero API bursts, zero cache-busting tag grammar.
- `url.domain:2gis.ru` (Russia's dominant maps/POI service, the closer Amap analog): **0 hits**.
- Keyword `yandex.ru/maps` / `2gis`: thousands of hits, but all Russian business sites embedding map widgets — the exact keyword-noise shape, no agent programs.

## Lane 2 — Russian native infra: ZERO agent use

| Service | Hits | Verdict |
|---|---|---|
| `clck.ru` (Yandex shortener) | 216 keyword / 7 actual short-link submissions | All 7 resolve to phishing/spam (fake Correos login `nus.nbt.mybluehost.me/.../login.php`, casino `cas-black.asia`, sneaker scam `sneakers90off.click`). Cybercrime, not agents. |
| `vk.cc` (VK shortener) | 548 | Spam/phishing noise only. |
| `paste.org.ru` (Russian-language paste service) | **0** | No urlquery presence at all. |
| `translate.yandex` as fetch proxy | 78 | Noise (redirect referrers). Zero proxy use. |
| `turbopages` (Yandex translate-proxy) | 7,089 | Ad-tracking noise. Zero fetch-proxy use — unlike the Chinese fleet's `fanyi.baidu.com/transpage`. |

Note the asymmetry with the Chinese finding: the Chinese fleet avoided native infra because of login walls and used Western no-login services. Here there is no fleet at all to make that choice — the negative is one level deeper.

## Lane 3 — Relay stack with Russian targets: ZERO

- `r.jina.ai` (1,088 hits): zero Russian targets in 60-report sample. Traffic is researcher-adjacent (`dantheduck.tech` ×15, `collusion.wiki`, `transluce.org`) — hunt infrastructure, not Russian ops.
- `href.li` (4,824 hits): 1 RU-flavored (`play.runicwin.com`, a game site).

## Lane 4 — Russian-language n-grams: ZERO

- 60 `httpbin.org/base64` programs sampled, regex for transliterated Russian geo terms (mosk, peter, kazan, novosib, ekaterin, krem, arbat, nevsk, tvers, lenin, krasn, .ru): **0 hits**.
- No Cyrillic-comment programs, no Russian place-name program titles found.

## Lane 5 — Russian lab fingerprints: ZERO

- `yandexgpt` (187): noise — Webflow previews mentioning YandexGPT, unofficial `yandex-gpt.ru/`.
- `gigachat` (84): noise — `nika-agent.ru/` (Russian agent *product* site, Sep 27 — a company page, not fleet traffic), `elhacker.net` mentions.
- `url.domain:sberbank.ru`: **0**. `gigachat.devices` (actual GigaChat API host): **0**.
- `83.222.10.102` (surfaced in both yandexgpt and gigachat searches) → redirects to `sitebolit.ru`, a Russian website-malware scanner. Security-tooling IP, not agent infra.

## The meta-finding (why this negative matters)

Three OPSEC postures now on the table:

| Actor | urlquery footprint | Posture |
|---|---|---|
| Tencent Amap fleet | 2,000+ reports | Loud — uses urlquery *as a browser* |
| DeepSeek+Hermes (knaithe) | Zero under own identifiers | Quiet — avoids urlquery |
| Russian ecosystem | Zero everywhere checked | **Absent** — no loud fleet, no native-infra agent use |

The Chinese fleet was found because it was loud on Western no-login infra. The Russian hunt shows the complementary blind spot: if Russian agent ops exist, they are not on this surface at all. The detection net needs a different shape for them.

## Suggested next surfaces (not urlquery)

- **Telegram Bot API as C2/dead-drop** — the DeepSeek+Hermes op already used Telegram C2; Russian actors live on Telegram, not webhook.site.
- **Yandex Cloud IP ranges** — the Tencent fleet gave itself away via AS132203; a Yandex Cloud ASN pivot is the equivalent fingerprint.
- **urlscan.io** for yandex.ru/2gis.ru place-scan bursts.
- **Russian-language GitHub** — agent program repos, `uqscan`-style tag generators.
- **VK infra** (`vk.cc`, VK API) as the native dead-drop/relay surface.

Nothing pushed, per instructions. All zeros logged as results above.
