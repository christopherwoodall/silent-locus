# Cross-swarm shared vocabulary hunt — Findings (2026-10-05)

**Question**: do marker words/n-grams from one agent swarm appear in another swarm's
traffic — in any language? A shared marker across languages = shared toolkit evidence.

**Method**: built a vocabulary from four corpora (Tencent Amap fleet Oct 2026, OpenAI
incidents May–Jun 2026, ltzh family Oct 2026, DeepSeek+Hermes Jul–Aug 2026), then
searched each marker on urlquery.net for non-origin-language contexts
(Russian, French, German, Spanish, Portuguese, Arabic, Japanese, Korean targets/content).

**Verdict: no marker has crossed swarm boundaries. Every fleet's vocabulary is
fleet-exclusive. The shared layer is commodity infrastructure (jina, webhook.site,
httpbun) — not marker grammar.**

## Vocabulary table

| Marker | Origin swarm | urlquery hits | Cross-language verdict |
|---|---|---|---|
| `uqscan=` | Tencent Amap fleet | 1,220 | **Exclusive**: all amap.com + fleet's own httpbin.org programs. The one `baidu` hit is `m-amap-com.translate.goog` — still Amap. Zero Russian/French/German/any non-Amap. |
| `uqtag=` | ltzh family (beacon exfil) | 92 | Fleet + noise (breached.st, carousell.com, gambling). No second actor. |
| `uqtarget=` / `uqhost=` | Tencent (subdomain A/B test) | 23 / 7 | Amap-only. One `example.com/?uqtarget=1791135441` = fleet self-testing its own grammar, not cross-swarm. |
| `uq=` epoch | Tencent | (in `uqscan` set) | Amap-only. |
| `sub_poi_navi` | Amap API field | 24 | **Perfect fingerprint**: 21 httpbin.org + 2 amap.com + 1 httpbun.com, all fleet. Zero web hits outside. |
| `clk_ratio` | Amap API field | 6 | All fleet httpbin.org programs. |
| `hysandbox` | Tencent proxy Via | 0 | Zero urlquery hits, zero web hits. Tencent-only by construction. |
| `zzbulk` | OpenAI Jun 2026 | 0 | **Gone**: zero in current urlquery index. |
| `prepnonce` | OpenAI Jun 2026 | 0 | **Gone**: zero in current urlquery index. |
| `zz=oai<digits>` | OpenAI Jun 2026 | — | Rate-limited during hunt (429); grammar confirmed in local June corpora (arquivo-pt, re-hunt-patterns). Survival in 2026 index unverified — needs recheck. |
| `claude2026…` labels | Tencent (false-flag) | 1 | `freegpt.tech` (free AI-chat aggregator, 2026-10-04) — not agent-shaped. No cross-swarm claude labels. |
| `ltzh-` prefix | Unattributed Oct 2026 | 207 | 99% noise; 6 signal (the Oct 4 httpbin family). No other-language adoption. |
| `injectPageScript` | ltzh TTP (jina API) | 6 | Unrelated sites (graphy.com, Indian tutorial pages, Feb–Jul 2026). The ltzh use is inside base64 blobs — not keyword-searchable. No cross-swarm. |
| `research2026` / `target2026` tags | Tencent tag grammar | 3 / 1 | Ordinary sites (bajaexpo.com, shrooomz.com, ifyoucare.com). Noise. |
| Telegram Bot C2 (`api.telegram.org bot`) | Hermes/DeepSeek | 13,590 | All phishing noise (Vercel/Replit credential lures). No agent-shaped Telegram C2 on urlquery. |
| FOFA `"claude code web ui"` | DeepSeek+Hermes recon | 1 (May 16) | Single report; no second actor reusing the query. |

## What this bounds

1. **The `uq*` grammar has not spread.** 1,220 `uqscan=` hits and not one outside the
   Amap operation. If a shared launcher/toolkit existed across Chinese labs, its tag
   grammar would leak across fleets — it hasn't.
2. **The OpenAI June grammar is dead on this surface.** `zzbulk` and `prepnonce` return
   zero; the June toolkit's markers don't appear in current urlquery at all (aged out
   or never indexed). No 2026 actor has picked them up.
3. **False-flag "claude" labels don't travel.** The only `claude2026` hit is an unrelated
   free-GPT site. The claude-labeling quirk is Tencent-fleet-specific, not a shared
   deception pattern.
4. **The ltzh family is unattributed and isolated.** Distinct TTP (jina POST +
   injectPageScript + image beacons) with no adoption elsewhere — either private
   alternate tooling or a one-off copycat.
5. **Commodity infra is the only shared layer.** jina, webhook.site, httpbun, LiveCodes,
   translate.goog appear across contexts — but they're public utilities, not toolkit
   fingerprints. Shared infra ≠ shared operator (established in earlier lanes).

## Negative space worth keeping

- `fanyi.baidu.com/transpage` (Baidu Translate fetch proxy): fleet-exclusive, 6 URLs.
  No `translate.yandex`, no DeepL-as-proxy — the fetch-proxy trick hasn't generalized.
- `example.com/?uqtarget=`: the fleet tests its own grammar on example.com — a
  self-survey behavior also seen in the other-targets lane (fleet searching its own
  place IDs on urlquery). Worth watching: example.com probes may precede new grammar.
- `zzb3-start` / `zzb4-start` httpbin programs (Oct 4, in `uqtag=` results): `zz`-prefixed
  but not `zz=oai` — possibly unrelated; flagged, not claimed.

## Follow-ups

- Recheck `zz=oai` in the urlquery index after rate-limit cooldown — the one unverified cell.
- Watch `uqscan=` for first non-Amap appearance: that would be the shared-toolkit tripwire.
- Watch `example.com` + `uq*` params: fleet grammar proving ground.
- `openclaw` (1,026 hits) still unexamined — Hermes-adjacent framework, may hold agent traffic.

- Recheck `zz=oai` in the urlquery index after rate-limit cooldown — the one unverified cell.
- Watch `uqscan=` for first non-Amap appearance: that would be the shared-toolkit tripwire.
- Watch `example.com` + `uq*` params: fleet grammar proving ground.
- `openclaw` (1,026 hits) still unexamined — Hermes-adjacent framework, may hold agent traffic.

---

# Part 2 — Native-tongue agent vocabulary (predictive, not observed)

The user: don't just hunt shared words from swarms we've seen — hunt what agents
WOULD say in their native tongue, even if never observed. Below: agent-framework
vocabulary (the words agents emit in loop traces, program comments, tag params) for
9 languages. Transliterations are Latin-script forms agents would plausibly put in
URLs/params (native script is usually percent-encoded or avoided).

## Russian

| Category | Native (translit) |
|---|---|
| Core loop | zadacha/zadanie (task), shag (step), plan (plan), deistvie (action), nablyudenie (observation), mysl (thought), instrument (tool), rezultat (result), oshibka (error), povtor (retry), vypolnit (execute), zavershit (complete) |
| Collection | issledovanie (research), poisk (search), sbor (collect), izvlech (extract), parsing (scrape), poluchit (fetch), skachat (download), sokhranit (save), dannye (data) |
| Infra | skanirovanie (scan), zondirovanie (probe), test (test), proverka (check), proksi (proxy), rele (relay), vebkhuk (webhook), mayak (beacon), eksfiltratsiya (exfiltrate) |
| Tag params | `?zadacha=`, `?zadanie=`, `?shag=`, `?rezultat=` |

## French

| Category | Native |
|---|---|
| Core loop | tâche/mission (task), étape (step), plan (plan), action (action), observation (observation), pensée/réflexion (thought), outil (tool), résultat (result), erreur (error), réessayer (retry), exécuter (execute), terminer (complete) |
| Collection | recherche (research/search), collecte (collect), extraction (extract), scraper/moissonner (scrape), récupérer (fetch), télécharger (download), sauvegarder (save), données (data) |
| Infra | scanner/analyse (scan), sonder (probe), tester (test), vérifier (check), proxy (proxy), relais (relay), webhook (webhook), balise (beacon), exfiltrer (exfiltrate) |
| Tag params | `?tache=`, `?mission=`, `?etape=`, `?resultat=` |

## German

| Category | Native |
|---|---|
| Core loop | Aufgabe/Auftrag (task), Schritt (step), Plan (plan), Aktion (action), Beobachtung (observation), Gedanke (thought), Werkzeug/Tool (tool), Ergebnis (result), Fehler (error), Wiederholung (retry), ausführen (execute), abschließen (complete) |
| Collection | Recherche/Forschung (research), Suche (search), sammeln/erfassen (collect), extrahieren (extract), scrapen/auslesen (scrape), abrufen (fetch), herunterladen (download), speichern (save), Daten (data) |
| Infra | scannen (scan), sondieren (probe), testen (test), prüfen (check), Proxy (proxy), Relais (relay), Webhook (webhook), Beacon (beacon), exfiltrieren (exfiltrate) |
| Tag params | `?aufgabe=`, `?auftrag=`, `?schritt=`, `?ergebnis=` |

## Spanish

| Category | Native |
|---|---|
| Core loop | tarea/misión (task), paso (step), plan (plan), acción (action), observación (observation), pensamiento (thought), herramienta (tool), resultado (result), error (error), reintentar (retry), ejecutar (execute), completar (complete) |
| Collection | investigación (research), búsqueda (search), recopilar (collect), extraer (extract), raspado (scrape), obtener (fetch), descargar (download), guardar (save), datos (data) |
| Infra | escanear (scan), sondear (probe), probar (test), verificar (check), proxy (proxy), relé (relay), webhook (webhook), baliza (beacon), exfiltrar (exfiltrate) |
| Tag params | `?tarea=`, `?mision=`, `?paso=`, `?resultado=` |

## Portuguese

| Category | Native |
|---|---|
| Core loop | tarefa/missão (task), passo/etapa (step), plano (plan), ação (action), observação (observation), pensamento (thought), ferramenta (tool), resultado (result), erro (error), tentar novamente (retry), executar (execute), concluir (complete) |
| Collection | pesquisa (research), busca (search), coletar (collect), extrair (extract), raspagem (scrape), obter (fetch), baixar (download), salvar (save), dados (data) |
| Infra | varredura (scan), sonda (probe), teste (test), verificar (check), proxy (proxy), relé (relay), webhook (webhook), farol (beacon), exfiltrar (exfiltrate) |
| Tag params | `?tarefa=`, `?missao=`, `?passo=`, `?resultado=` |

## Arabic

| Category | Native (translit) |
|---|---|
| Core loop | muhimma (task), khutwa (step), khitta (plan), ijra (action), mulahaza (observation), fikra (thought), ada (tool), natija (result), khata (error), i'adat al-muhawala (retry), tanfidh (execute), ikmal (complete) |
| Collection | bahth (research/search), jam' (collect), istikhraj (extract), scraping (scrape — loanword), jalb (fetch), tahmil (download), hifz (save), bayanat (data) |
| Infra | mash (scan), misbar (probe), ikhtibar (test), tahaqquq (check), wakil (proxy), murahhal (relay), webhook (loanword), manara (beacon), tasrib al-bayanat (exfiltrate) |
| Tag params | transliterated: `?mohimma=`, `?khotwa=`, `?natija=` (native script percent-encodes in URLs) |

## Japanese

| Category | Native (romaji) |
|---|---|
| Core loop | tasuku/kadai (task), suteppu/dankai (step), keikaku/puran (plan), akushon/koudou (action), kansatsu (observation), shikou (thought), tsuuru/dougu (tool), kekka (result), eraa (error), ritorai (retry), jikkou (execute), kanryou (complete) |
| Collection | chousa/risaachi (research), kensaku (search), shuushuu (collect), chuushutsu (extract), sukureipingu (scrape), shutoku (fetch), daunroodo (download), hozon (save), deeta (data) |
| Infra | sukyan (scan), puroobu (probe), tesuto (test), chekku/kakunin (check), purokishi (proxy), riree (relay), webufukku (webhook), biikon (beacon), mochidashi/rouei (exfiltrate) |
| Tag params | romaji: `?tasuku=`, `?kekka=`, `?shutoku=` |

## Korean

| Category | Native (romaji) |
|---|---|
| Core loop | jageop/taeseukeu (task), dangye (step), gyehoek (plan), haengdong/aeksyeon (action), gwanchal (observation), saenggak (thought), dogu/tul (tool), gyeolgwa (result), oryu/ereo (error), jaesido (retry), silhaeng (execute), wallyo (complete) |
| Collection | yeongu/riseochi (research), geomsaek (search), sujip (collect), chuchul (extract), seukeuraeping (scrape), gajyeoogi (fetch), daunrodeu (download), jeojang (save), deiteo (data) |
| Infra | seukaen (scan), peurobeu (probe), teseuteu (test), hwagin (check), peuroksi (proxy), rillei (relay), wephuk (webhook), bikon (beacon), yuchul (exfiltrate) |
| Tag params | romaji: `?jageop=`, `?gyeolgwa=`, `?sujip=` |

## Chinese

| Category | Native (pinyin) |
|---|---|
| Core loop | renwu (task), buzhou (step), jihua (plan), xingdong (action), guancha (observation), sikao (thought), gongju (tool), jieguo (result), cuowu (error), chongshi (retry), zhixing (execute), wancheng (complete) |
| Collection | yanjiu (research), sousuo (search), shouji (collect), tiqu (extract), paqu/zhuaqu (scrape), huoqu (fetch), xiazai (download), baocun (save), shuju (data) |
| Infra | saomiao (scan), tance (probe), ceshi (test), jiancha (check), daili (proxy), zhongji (relay), webhook (loanword), xinbiao (beacon), shuju waixie (exfiltrate) |
| Tag params | pinyin: `?renwu=`, `?jieguo=`, `?shouji=` |

## Hunt results (native-tongue candidates × program patterns)

**BLOCKED by rate limiting.** All 25 prioritized queries returned HTTP 429 despite
65s spacing and a 5-minute cooldown — the urlquery API quota is exhausted after
today's collection + lane hunts. Per provider hard-stop rules, no further requests
were made. The queries are defined and ready to rerun (script: `/tmp/native_vocab_hunt.py`):

Tier 1 (tag-grammar param candidates): `zadacha=`, `tache=`, `aufgabe=`, `tarea=`,
`tarefa=`, `renwu=`, `tasuku=`, `jageop=`, `mission=`, `ergebnis=`

Tier 2 (native words × program patterns): `zadacha httpbin`, `issledovanie`,
`recherche httpbin`, `collecte httpbin`, `aufgabe httpbin`, `datenerfassung`,
`tarea httpbin`, `recopilacion`, `tarefa httpbin`, `coleta httpbin`,
`shouji httpbin`, `paqu`, `shuushuu`, `sujip`, `bahth`

Rerun when the quota resets; each is a clean hit-or-zero cell for the table above.
The highest-signal bets: `?zadacha=` / `?tache=` / `?aufgabe=` (a native-tongue
cache-buster param would be the strongest possible "swarm speaking its own language"
signal), and `paqu` (爬取 — the Chinese word for scraping; if any Chinese agent
program titles/descriptions use it on httpbun/httpbin, that's a new marker).

Nothing pushed, per instructions.
