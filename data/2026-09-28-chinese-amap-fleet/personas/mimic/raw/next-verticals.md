# Next-Verticals Hunt — Mimic (2026-10-05 ~04:30–05:10 UTC)

**Task**: verify the Mimic's predicted next moves of the Chinese Amap POI fleet against reality.
**Collection status**: urlquery.net UNREACHABLE from this VM for the whole window (2026-10-05 ~04:26–05:10 UTC):
all routes timed out — keyless htmx (`uq_htmx.py`), authenticated `uq.py` API, plain curl to `/` and
`/api/htmx/search/` (http=000). urlscan.io API also unreachable from VM (curl timeout; `browser.open`
→ HTTP 403, not retried per policy). Web search for `"uqscan"` returns no public references (expected —
markers live only in urlquery/urlscan submissions).

Grading below is therefore against the LOCAL corpus: all `20261005`-dated fleet tags already collected
by sibling runs before the outage (fleet dir greps, events/API dumps). Live htmx re-verification of the
vertical/geography predictions remains OPEN. The 24-query paced sweep driver is saved at `raw/nv_hunt.py`
(7s pacing, `--delay 5`, resumes on cached files); the two attempted live queries errored out and are kept
as `raw/nv_01_dated_20261005.json` / `raw/nv_02_dated_20261006.json` for the record.

---

## 1. Grammar drift

### `uqid=` — HIT (via sibling run, cited)
Sibling direct hunt (`raw/uqid_hit.md`, 2026-10-05 ~04:3x UTC) CONFIRMED `uqid=` in the wild:
- 2026-10-04T14:22Z — `postman-echo.com/redirect-to?url=…amap-pc-ssr.amap.com/ssr/place/B0…` (uqid= present)
- 2026-10-04T14:21Z — `nghttp2.org/httpbin/redirect-to?url=…amap-pc-ssr.amap.com/ssr/place/…` (uqid= present)
Shape: operator's redirector tradecraft (redirect-to → Amap place) carrying the NEW `uqid=` param instead
of `uqscan=`. Report IDs not captured — follow-up: re-query `uqid=` with backoff when connectivity returns.
**Novel infra from this hit**: `nghttp2.org/httpbin` as staging host — not in the known set
(httpbun/httpbingo/postman-echo).

### More drift observed TODAY in local corpus (20261005 tags)
- `src=claude20261005jxmuseum` — `57bd6aec`, 2026-10-04T22:39Z — tag grammar migrated into the `src=` param.
- `src=fujianmuseum_top_20261005` / `..._top_20261005a` — `3f4cf1eb` / `a020b0c4`, 22:51Z —
  `src=<word>_top_20261005` on `www.amap.com/service/switchVersion`.
- `uqscan=tianshanzoo-parent-www-20261005a/b` — `d390eeab` / `051e33bf`, 22:08Z — multi-hyphen tag.
- `uqscan=navy971-20261005a/b/c` — `62d1cdbf` / `d6d1dc37` / `be82cecd`, 18:03Z — `<word><digits>-<date><x>`.
- `uqt=` / `uqv=`: **zero** anywhere in the corpus — predicted drift not observed.
- `src=manual0/1/2`: confirmed present (pre-existing grammar, not drift).

---

## 2. Next POI verticals — prediction vs 20261005 evidence

**Clean negatives**: ZERO tags matching `school|gov|mall|food|scenic|pharmacy|bank|estate`, `xuexiao`,
`zhengwu`, `hongkong|macau|taiwan|taipei` anywhere in the full `20261005`-tagged corpus. The fleet did NOT
move to the predicted new verticals today — it expanded WITHIN the known families:

| Family | New words today | Sample report IDs (UTC) |
|---|---|---|
| Museums | `fujianmuseum` | `33ea058d` 22:32Z, `e4280018` 22:32Z |
| Museums | `gxmuseum` (Guangxi) | `0b186149` 2026-10-05T00:16Z |
| Museums | `jxmuseum` (Jiangxi, via `src=`) | `57bd6aec` 22:39Z |
| Museums | `qingdaomuseum` continuing | (known family) |
| Zoos | `tianshanzoo` (Xinjiang) | `bc910254` 21:55Z, `d390eeab`/`051e33bf` 22:08Z |
| Zoos | `wuxizoo` continuing | (known family) |
| Scenic/parks | `zhenbeibao` (Ningxia) | `777ea9db`/`797f174c` 20:15Z |
| Scenic/parks | `gubei` | `89d010cc` 18:05Z |
| Scenic/parks | `hzparadise` | `178f0b8f` 16:38Z, `582b7972` 17:00Z |
| Scenic/parks | `dawugang` (unidentified POI) | `7724da67` 19:21Z |
| Hospitals | `claude20261005hospital2/3`, `gxzyy` family | `cfa0613d` 19:47Z, `d836435e` 19:48Z, `ea16b082` 20:41Z |

Full 20261005 word list in corpus: answer, claude, dawugang, direct, fujianmuseum, gallery, gubei, gxmuseum,
hzparadise, mobileapi, mobilerich, nested, proper, qdmuseum, qingdaomuseum(+api), research, smw, taersi(+api),
taiyuan(+api), target(+api/detail/info/ssr), tianshanzoo, wuxizoo(+api), zhenbeibao. (Tooling words mixed in;
POI signal = the museum/zoo/scenic/hospital words above.)

## 3. Geography — HK/Macau/Taiwan/overseas

**No evidence.** Zero HK/Macau/Taiwan tag words. The actual expansion is domestic-western: Ningxia
(zhenbeibao), Xinjiang (tianshanzoo), Guangxi (gxmuseum, gxzyy), Fujian (fujianmuseum), Jiangxi (jxmuseum),
Shanxi (taiyuan). Direction of travel: filling in inland/western provinces within known verticals.

---

## Infra notes
- `ditu.amap.com` host usage: `d9a5f703` / `9ecbfabe`, 2026-10-04T21:09Z (`dituold`/`ditussr` tags) — new
  host for the fleet alongside www.amap.com / amap-pc-ssr.amap.com.

## Open threads
1. Live re-verification when urlquery.net recovers: run `raw/nv_hunt.py` (24 queries, paced).
   Priority: `uqscan=20261005` catch-all, `uqid=` (capture report IDs + full URLs for the sibling's HIT),
   verticals (`school/gov/mall/...` bare), geography (`hongkong/macau/taiwan/taipei`).
2. urlscan.io is unreachable from this VM by every route tried — needs a parent-side check.
3. Sibling artifacts in this dir left untouched: `uqid_hit.md`, `uqid_hits.json`, `infra-migration.*`,
   `other-operators.md`.
