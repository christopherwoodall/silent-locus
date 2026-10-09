# Linguist (Multilingual) — FINDINGS
## Agent writing in every language except English and Chinese

**Run:** 2026-10-05 ~00:12–01:30 CDT (resumed after VM restart; prior round file was empty — no prior results lost, all work is new).
**Baseline from sibling (linguist-chinese):** the Amap fleet agent thinks in ASCII. Zero CJK across 1,243 `uq*` tag values; Chinese exists only as toneless separator-less lowercase pinyin; `summerpalace` for 颐和园 (English-exonym tell); `ceshiren` translationese; 182 `claude` self-labels, no other model names.
**This run's question:** does the agent write in Hindi, Portuguese, Arabic, Bahasa, Russian, Spanish, or any other language — in tags, URLs, payloads?

## Headline: the agent is multilingual in TARGETS, monolingual in WRITING

The fleet reads Indonesian, Brazilian, Vietnamese, and Indian government content, navigates Vietnamese-locale UIs, and walks through Google-Translate wrappers. Its marker grammar — the part it authors — stays ASCII English + pinyin in every case observed. **Locale-fluid browsing, marker-monolingual writing.**

## Confirmed features

### F1. ASCII-only agent writing, all scripts (STRONG — confirmed across ~40 corpora)
- 943 unique fleet tags in `2026-09-28-chinese-amap-fleet/events.jsonl`: **zero non-ASCII**.
- Agent-authored fields (matched_string, fleet_tag, uq*/test/probe/marker URL params) across 40 `data/*/events.jsonl` corpora: only hits were Latin-with-diacritics (Vietnamese target content) and investigator notes (em-dashes, arrows).
- 40,000 sampled events from `2026-10-03-openai-agent-traces/events.jsonl` (589,972 total): **zero Devanagari, zero Arabic, zero Cyrillic, zero Thai, zero Hangul, zero Greek/Hebrew**.
- No agent-authored CJK anywhere — even when the target is a Chinese site, even when a human Chinese operator would use hanzi reflexively.
- **Classifier feature:** any non-Latin script in an agent marker/tag is evidence AGAINST Amap-fleet lineage, or of a different build.

### F2. English-exonym preference over endonym/transliteration (MEDIUM — new this run)
- `uqscan=bazaar20261004a`, `uqscan=claude20261005bazaar…` on POI `B03DF05V5I` (Xinjiang International Grand Bazaar, Ürümqi) — the agent reaches for the **English Wikipedia word** "bazaar", not pinyin `daba扎`/`erdaoqiao` and not Uyghur `بۇغرا`.
- Same pattern as sibling's `summerpalace` (not `yiheyuan`).
- **Classifier feature:** exonym-vs-endonym test for place-name tags. A Chinese-human-built or Chinese-model-dominant agent produces `yiheyuan`, `wulumuqi`; an English-dominant model produces `summerpalace`, `bazaar`.

### F3. Locale navigation without marker-language change (MEDIUM)
- Vietnamese pxweb referrers in BOTH locales: `https://pxweb.nso.gov.vn/api/v1/en/National Accounts and State budget/…` AND `https://pxweb.nso.gov.vn/pxweb/vi/Tài khoản quốc gia/Tài khoản quốc gia/V03.14.px/?action=` — the agent walks the Vietnamese UI path while its referrer/relay grammar stays English.
- Google-Translate wrappers on agent-laundered URLs: `_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en` on Indonesian (`jdih.balikpapan.go.id`) and Indian (`indiascienceandtechnology.gov.in`) government content — the agent consumes foreign-language pages via machine translation, never by writing in the target language.
- `?utm_source=chatgpt.com` on Indonesian gov URLs (Balikpapan, Egyptian Drug Authority) — URLs copied out of a ChatGPT answer, i.e. the research step happened in a chat UI, the submission step stayed ASCII.

### F4. Machine shorthand has no transliteration vowel patterns (MEDIUM)
- Opaque initialisms in tags: `njxzgz`, `fzmd`, `cdhv`, `srh`, `wfjxy`, `ltzh`, `shbg`, `qdmuseum`, `cdtyzx` — consonant-cluster compression.
- A human transliterating in any language keeps vowel skeletons (e.g. `ujian`, `teste`); these don't. This is machine ID-compression, and its shape is identical across the Chinese corpus and the global-south targets.

## Honest negatives

- **`ujian` / `coba` / `teste` htmx hits are target content, not agent writing.** `q=ujian` → 12 reports on `peminjamanruangan.appwrite.network` (Bahasa Indonesia "room booking" Appwrite deployment — exploitgym-family branch deployments). `q=teste` → Brazilian `.com.br` targets and `branch-codex-teste-mesa-…appwrite.network` (Portuguese branch names). The matched word is in the *target's* name, not in agent-authored text.
- **No non-English translationese found in markers.** Sibling found English-only translationese (`ceshiren`); no equivalent found for Hindi, Arabic, Portuguese, Spanish, Bahasa, Russian in any agent-authored field sampled.
- **No non-English test/probe grammar.** No `prueba=`, `teste=`, `ujian=`, `اختبار` markers; the fleet's test vocabulary is `test`, `default`, `TESTDEFAULT999` — all English.
- `q=coba` and `q=prueba` failed on transport (IncompleteRead under post-restart flakiness); retry pending — these are the two remaining open queries.

## Discriminator vs Dream swarm
- Dream: Simplified-Chinese internal / Traditional-Chinese target-facing — script policy splits by audience.
- Amap fleet: ASCII-only everywhere — internal tags, marker grammar, place-name references. No script split because there is no non-ASCII script at all.
- **Script policy is a usable cluster discriminator:** a new cluster writing hanzi, Devanagari, or Arabic in its markers is not this fleet's build.

## Caveats / open
1. openai-agent-traces sample was 40k of 589,972 events (head-biased); a full sweep is open.
2. `q=coba` and `q=prueba` htmx retries pending.
3. Percent-encoded script-range queries (`%D8%`, `%E0%A4`) proved non-discriminative on the htmx endpoint (matches report internals, not just submitted URLs) — do not use that method.
4. Vietnam `vi`-locale URL is from the frozen `2026-05-12-university-shorteners-events` corpus (archived capture, not live).

## Steps taken (audit trail)
1. Read sibling baseline; checked prior `raw/htmx_round1.jsonl` (empty — fresh run).
2. Tested egress: `curl https://urlquery.net/` → 200 (recovered).
3. Extracted 943 fleet tags from amap-fleet events.jsonl — zero non-ASCII; token analysis surfaced `bazaar` exonym cluster on POI B03DF05V5I.
4. Swept 40 corpora for non-ASCII in agent-authored fields; sampled 40k openai-agent-traces events for 7 non-Latin scripts — zero.
5. htmx round (≤1 req/5s, `--delay 6`, retry wrapper around IncompleteRead): `%D8%`, `ujian`, `coba`(fail), `teste`, `prueba`(fail). Results in `raw/htmx_round1.jsonl`.
6. Wrote this report. No commits/pushes.

## APPENDIX — All observed URLs
- https://urlquery.net/ (egress test, 200)
- https://pxweb.nso.gov.vn/pxweb/vi/Tài khoản quốc gia/Tài khoản quốc gia/V03.14.px/?action= (Vietnamese-locale pxweb URL, university-shorteners corpus)
- https://pxweb.nso.gov.vn/api/v1/en/National Accounts and State budget/ (English-locale pxweb, same task family)
- https://goto.unm.edu/7t6-o+ (YOURLS stats source)
- jdih.balikpapan.go.id/dokumen/610/detail?utm_source=chatgpt.com (Indonesian legal-docs, ChatGPT-copied URL)
- pa-gresik.go.id/index.php?option=com_media (Indonesian religious court)
- dinkes.acehprov.go.id/detailpost/abcde-cegah-stunting (Aceh health office)
- https://proxy.cors.sh/https://www.indiascienceandtechnology.gov.in/res… (Indian gov via CORS proxy + Google Translate params)
- anatel.gov.br/ (Brazilian telecom regulator)
- esporte.gov.br/ (Brazilian Ministry of Sport)
- edaegypt.gov.eg/en/media-center/news/during-the-fifth-edition-of-africa-health-excon-2026-eda-supports-strategic-partnerships-to-localize-vaccine-manufacturing-and-strengthen-health-security-across-africa/?utm_source=chatgpt.com (Egyptian Drug Authority)
- peminjamanruangan.appwrite.network (Bahasa Indonesia Appwrite target; report https://urlquery.net/report/6bd6882b-7c6c-4bf1-bcb2-35c754273b87)
- branch-codex-teste-mesa-df4072a-8aae00f.appwrite.network (Portuguese-named Appwrite branch; report https://urlquery.net/report/4c7bcaa8-1ce0-436e-bc49-e8c954036fda)
- https://urlquery.net/report/4eeb5d12-fedb-4b7f-b8cf-4c9b138f85ad (ujian report)
- https://urlquery.net/report/a0b2a16d-ed8d-43ce-8056-e2bc0b34bf0f (teste report: www.codigodiviino.link)
- https://urlquery.net/report/d75538f1-78da-46c9-8f6f-99620659934f (teste report: bwmequipamentos.com.br)
- https://urlquery.net/report/95382df1-6556-46c5-8a02-2abffe36b9532 (teste report: opescadordeofertas.com.br)
