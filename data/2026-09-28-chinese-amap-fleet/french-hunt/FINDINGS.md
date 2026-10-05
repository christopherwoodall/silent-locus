# French hunt — Findings (2026-10-05)

## Verdict: no French agent fleet found on urlquery — clean sweep

Applied the Amap-fleet TTP playbook (systematic place/API scans, cache-busting tags,
relay-stack pivots, native-infra checks, language n-grams) to the French web ecosystem.
Every pivot is an honest zero or ordinary human traffic. There is no French-language
equivalent of the Amap operation visible on urlquery.net.

## French map/POI targets

| Pivot | Hits | Verdict |
|---|---|---|
| `url.domain:pagesjaunes.fr` | 0 | Zero. No PagesJaunes place/API scanning at all. |
| `url.domain:mappy.com` | 0 | Zero. |
| `url.domain:viamichelin.fr` | 0 | Zero. |
| `url.domain:openstreetmap.fr` | 0 | Zero. |
| `url.domain:geoportail.gouv.fr` | 3 | Ordinary browsing (`/`, `/carte?c=...`), no agent markers. |

No Amap-style systematic place/API scanning exists for any French mapping service.

## French government / open-data APIs

| Pivot | Hits | Verdict |
|---|---|---|
| `url.domain:data.gouv.fr` | 19 | All ordinary: dataset pages, annuaire-entreprises lookups. No API scraping, no tags, no bursts. |
| `url.domain:api.gouv.fr` | 1 | Single hit, not agent-shaped. |
| `url.domain:adresse.data.gouv.fr` | 0 | The French national address API — untouched. |
| `url.domain:geo.api.gouv.fr` | 0 | The French geo API (communes/départements) — untouched. |

## French native infra

| Pivot | Hits | Verdict |
|---|---|---|
| `url.domain:zerobin.net` | 12 | French encrypted pastebin (Sébastien Sauvage). Links are `?hex#base64key` — normal ZeroBin usage; content is client-encrypted so agent dead-drop use is unknowable from metadata. No agent markers on the URLs themselves. |
| `url.domain:lstu.fr` | 1 | Framasoft shortener. Single hit. |
| `url.domain:frama.link` | 20 | **Abused for bank phishing, not agents**: `snsbank-bevestiging`, `vasco-psd2`, `Netfix`, `rabo-bankmail`, `HSBCwarnings` — Dutch/French bank-phishing lures on a French shortener. Human cybercrime; worth noting as the French shortener's actual abuse profile. |
| `url.domain:pastebin.fr` | 1 | Single hit. |
| `url.domain:framapad.org` | 1 | Single hit (Framasoft collaborative pad). |
| `url.domain:u.nu` | 0 | |

## French AI labs / agent infra

| Pivot | Hits | Verdict |
|---|---|---|
| `url.domain:mistral.ai` | 5 | Ordinary `chat.mistral.ai` usage. No fleet. |
| `url.domain:api.mistral.ai` | 0 | No agents calling Mistral's API via urlquery-visible URLs. |
| `url.domain:console.mistral.ai` | 0 | |
| `url.domain:lechat.mistral.ai` | 0 | |
| `mistral` keyword | 1,235 | All noise — pages merely mentioning Mistral, phishing, spam. Zero agent programs. |
| `url.domain:lighton.ai` | 0 | French LLM lab, no footprint. |
| `url.domain:dust.tt` | 1 | French agent-infra company (Dust). Single hit: a sign-up page, ordinary. |

## Relay stack with French targets

| Pivot | Hits | Verdict |
|---|---|---|
| `jina.ai/https://www.lemonde.fr` | 0 | No jina fetching of Le Monde. |
| `jina.ai/https://www.lefigaro.fr` | 0 | No jina fetching of Le Figaro. |
| `jina.ai/https://fr.wikipedia.org` | 0 | No jina fetching of French Wikipedia. |
| `translate.goog` French targets | 0/40 | 4,216 total translate.goog hits; 40-report sample contained zero French targets. |

## French-language n-grams / program pivots

| Pivot | Hits | Verdict |
|---|---|---|
| `itineraire` keyword | 2,129 | All ordinary: French tourism sites, Le Monde, transport pages. Keyword matches page content, not agent programs. |
| `httpbin paris` | 1,176 | Noise — pages mentioning both terms; zero actual httpbin/httpbun program URLs in sample. |
| `livecodes paris` | 0 | |
| `httpbun paris` | 0 | |

## Misc French web

| Pivot | Hits | Verdict |
|---|---|---|
| `url.domain:qwant.com` | 3 | Ordinary image-search usage. |
| `url.domain:fr.wikipedia.org` | 0 | Nobody submits French Wikipedia to urlquery. |
| `url.domain:api.sncf.com` | 0 | French rail API untouched. |

## Interpretation

1. **No French Amap-equivalent.** French mapping/POI services show zero systematic scanning. Either no French-language place-scraping fleet exists, or it doesn't use urlquery-visible infrastructure.
2. **French open-data APIs are pristine.** adresse.data.gouv.fr and geo.api.gouv.fr — exactly the structured-data APIs an agent fleet would love — have zero urlquery footprint.
3. **No French-lab agent infra on urlquery.** Mistral, LightOn, Dust: no agent-shaped traffic. (Caveat: API calls are server-side and wouldn't appear as submitted URLs anyway; this only rules out urlquery-visible fleet behavior, same limitation as the DeepSeek finding.)
4. **French native infra's abuse profile is phishing, not agents.** frama.link's observable abuse is bank-phishing lures — consistent with the Chinese-infra finding that agents optimize for no-login Western services regardless of origin.
5. **The relay stack shows no French targeting.** jina and translate.goog carry no French-target traffic in the samples checked.

## Open follow-ups

- If a French fleet exists, it likely uses the same Western no-login stack (jina, webhook.site, httpbun) — hunt it via French *task* markers (French place names in program titles, `uq*`-style tag grammars) rather than French *infrastructure*.
- `zerobin.net` is the one French-native service where encrypted agent dead-drops would be invisible by design — worth remembering as a blind spot, not a lead.
- Russian and German lanes remain open per the user's direction.

Nothing pushed, per instructions.
