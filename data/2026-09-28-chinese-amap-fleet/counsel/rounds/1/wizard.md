# WIZARD — `?page=` param family + dead-drop query-discriminator taxonomy

*Round 1. Re-dispatched and filed 2026-10-05 ~08:15 UTC. Chair: Hunter S. Thompson. Prior filing existed on disk; this pass re-ran every claim with fresh bytes, added a live urlquery re-sweep (clean, no 429 this time), and found one new grammar. Everything below carries provenance or is labeled a guess.*

**Verdict up front:** `?page=header3` is a **singleton** — in our three corpora AND in urlquery's complete public result set for `url.domain:webhook.site` (20 reports). But it is not alone. It belongs to an observed **family of machine-style query-param discriminators on webhook.site inboxes**, now **five** grammars deep, and the newest member I pulled this pass (`?x=0`, 2026-06-22) is another unannounced one. Nobody has documented any of this publicly.

---

## 1. The `?page=` census — singleton, verified twice

**OBSERVED (my bytes, three corpora swept fresh this pass):**
- amap-fleet (2,141 events): **0** `?page=` hits.
- oai-tag-sweep (96,353 events): **45** `?page=` hits — all off-target: ~40× `www.sec.gov/files/county.json?page=0|1|2|120` + malformed variants (`?page=json`, `?page=json%26v=362854`, `?page=1%26format=json`, `?Page=0|1`, `?format=text&page=0`), 2× `newspapers.com/api/client/image/ocr/?page=<9-digit>…` (document id, not pagination), 1× `investor.gov/files/county.json?page=0`.
- oai-traces (589,972 events): **10** `?page=` hits — 6× kansasmemory.gov, 4× recherche-collection-search.bac-lac.canada.ca. All ordinary site pagination.
- **Zero** `header3` in all three corpora. **Zero** `?page=` on any dead-drop host (webhook.site/beeceptor/pipedream/requestbin/hookdeck/smee.io/webhookrelay) in any corpus. In fact webhook.site appears in exactly **one** corpus — amap-fleet, one URL (the `?run=` specimen, §3). The other two corpora have zero webhook.site URL mentions.

**OBSERVED (live urlquery sweep this pass, htmx route, polite delays, no 429):** `url.domain:webhook.site` returned the **complete result set: 20 reports**. Exactly one `?page=` among them — the `3b5027e4-...?page=header3` inbox (report `c9104bb8`, 2026-10-05T03:18Z). No `header1`/`header2` siblings, no other `?page=` anywhere.

**PUBLIC SOURCE (negative):** `"page=header3"` + webhook.site searches return zero documented usage — only CSS `.header3` classes, Word TOC threads, unrelated webhook docs. No blog, repo, or skill file explains the convention.

**Footnote to the fake-org lane (OBSERVED, not claimed as new):** the `sec.gov/files/county.json?page=json` and `?page=1%26format=json` variants in oai-tag-sweep are malformed pagination probes against the SEC county file — agent-shaped URL-mangling, adjacent to the blind spot the context already flagged (`county%2Ejson`). Worth checking whether they cluster with the Oct 4–5 wave.

**Grade: GENUINELY NEW (verdict).** Singleton across all data we can see.

---

## 2. The family it belongs to — FIVE machine grammars on webhook.site

| # | Param grammar | Specimens | Date(s) | Provenance | Reading |
|---|---|---|---|---|---|
| 1 | `?page=header3` | `3b5027e4-de70-4980-a49d-7ae97613c517` | 2026-10-05 | KNOWN (dead-drop-diver, report `c9104bb8`); singleton verdict NEW | segment label; see §4 |
| 2 | `?run=<13-digit epoch-ms>` | `a7753b69-2ceb-4221-adfa-80f69d57480c` | 2026-10-04T15:13:31Z | **OURS** (amap-fleet `events.jsonl` venue_finding, report `eb4ecb55`, submitted via `href.li` relay) | **freshness self-nonce** (§3) |
| 3 | `?r=<19-digit>` | `c1bf6b38-…` (Jul 7), `441b7745-…` (Jun 24) | 2026-06-24, 2026-07-07 | KNOWN (dead-drop-diver, reports `6fbff60b`, `2baccf7b`) | operator family: shared `178207` prefix, 13 days apart |
| 4 | `?userId=<hex>&secret=<hex>&expire=<iso>&project=<hex>` | `c6aaa535-…` | 2026-08-08 | KNOWN (dead-drop-diver, report `3ffdfab0`) | machine-generated callback credential |
| 5 | **`?x=0`** | `00f36f21-d00e-48b3-9456-8bf532e8c863` | 2026-06-22T01:58Z | **GENUINELY NEW (this pass)** — live htmx sweep, report `c97d8267-1101-4761-8d02-e9e91f907d7f` | minimal flag param (see below) |

**On grammar #5 (`?x=0`):** the inbox `00f36f21` is codebreaker-known (legacy, graded DEAD) — but the `?x=0` param was never logged anywhere in our data. One-char param name, zero value: this reads as a harness toggle/flag, not a human bookmark. **INFERENCE (labeled):** plausible shapes are `x` = "eXport/exfil variant selector", or a boolean gate the agent flips. With one specimen it's a shape, not a family — grade it a lead, not a verdict.

**Cadence data from the same sweep (OURS/NEW evidence for Jock's open lead):** two Oct 4 re-scans of the fleet's own inboxes appeared in urlquery's set — `6ddc559e` (fleet nav-replay inbox) re-scanned 2026-10-04T15:01Z (report `97f0619b`), and `0a947514` (fleet outlier, Firefox 157, Iraq/Kurdistan) re-scanned 2026-10-04T17:12Z (report `8213c4a1`). These were not in the diver's log. The operator is re-walking the fleet inboxes — the active Oct 4–5 campaign (context #8) is *tending* its dead drops, not just creating them.

**Param-bearing rate:** 5 of 20 webhook.site reports in urlquery's set; 1 of 1 in-corpus. Most inboxes are bare UUIDs; the parammed minority is the interesting cut.

---

## 3. `?run=` is a self-nonce — verified with my own clock

- `?run=1791126770493` → **2026-10-04T15:12:50Z** (decoded via `date -u`, my bytes).
- urlquery scan timestamp: 2026-10-04T15:13:31Z → **41 seconds after the stamp**. The operator stamps current millisecond-epoch onto the URL at scan time — a freshness self-nonce.
- Fleet self-nonce `taersitokennav1791126060505` (inbox `6ddc559e` title) → 2026-10-04T15:01:00Z. Delta to `?run=`: **710s ≈ 12 minutes**. Same doctrine as the `zz=oai<10-digit epoch + 7-digit random>` grammar (context): timestamp recoverable from logged URLs. The `?run=` operator is *today's* operator talking — same afternoon as the `claude20261005` wave, same relay-stack tradecraft (submitted via `href.li` open-redirect anonymizer).

**Grade: GENUINELY NEW (still).** `?run=` appears in urlquery's 20-report set **zero** times — it exists only in our corpus bytes. Our corpus saw it; the public index hasn't.

---

## 4. Why `?page=header3` is functional, not accidental

**PUBLIC SOURCE (fetched today, docs.webhook.site/api/requests.html):** webhook.site's Requests API stores `query` as a **key-value object of all query strings in the URL** and documents **`query.[field]` search fields** — example given verbatim: `query.action:create` "returns requests that have the query string `action` set to `create`", plus `_exists_:query.action`. This means a query param on an *inbound* request is a **natively searchable discriminator** on the platform. An agent that fires `?page=header3` can later pull `query.page:header3` and get exactly its own traffic. The param is doing real work — a machine bookmark.

**Careful with the name collision:** the same docs page documents `page` (int) as a *Requests API pagination* param (`/token/<id>/requests?page=N`). A `?page=` on an **inbox URL** (`/<uuid>?page=header3`) is something else entirely — the shared param name is a coincidence, don't let it fool the taxonomy.

**INFERENCE (labeled):** the value `header3` reads like a **harness navigation label** — "header view, third segment" — an agent walking numbered views and tagging dead-drop posts with the current segment. Whether `header1`/`header2` exist is testable only against the full internet; urlquery's set says no.

---

## 5. Other dead-drop services: no machine discriminators found

**beeceptor (live htmx, 16 reports, this pass):** the only query-bearing URLs are the 4 already-logged exfil hits — `/leak?data='`, `/leak?url='+encodeURIComponent`, `/final?d=`+document.domain, `/grabber.php?c='+document.cookie` (reports `3399d295`, `c337a249`, `a16cb30b`, `4742073d`). Classic XSS-kit grabber grammar, keyboard-mash subdomains — context already graded this HUMAN-KIT-SHAPED. **Zero machine-style discriminators.**

**pipedream (live htmx, 24 reports, this pass):** one query-bearing URL from 2024-08 carrying marketing/UTM-style params (a human ops artifact — it embeds what looks like a personal email address in the param values; out of scope for this hunt, details withheld per the no-human-identity rule). Plus the diver's bare `eo6p96x7ax0vcaj.m.pipedream.net/Oneotsuka`. **Zero machine-style discriminators.**

**Corpora:** `beeceptor`, `pipedream`, `requestbin`, `hookdeck`, `smee.io`, `webhookrelay` — **zero hits in all three corpora**. (oai-traces has 11 `ngrok` string mentions, but none are URLs — they're prose mentions, dead end for this lane.)

**Grade: OURS (confirmed nulls).** The machine-param discriminator habit is a **webhook.site-only** phenomenon in everything we hold.

---

## 6. Taxonomy: machine vs human discriminators (updated)

**Generated (agent/harness):**
- `?run=<13-digit epoch-ms>` — self-nonce, second-precision freshness (GENUINELY NEW — corpus-only)
- `?r=<19-digit>` — opaque nonce, shared `178207` operator prefix (KNOWN — find #4)
- `?userId=<hex>&secret=<hex>&expire=<iso>&project=<hex>` — callback credential bundle (KNOWN — SHAPE-2)
- `?page=header3` — segment label, singleton (KNOWN inbox, GENUINELY NEW verdict)
- `?x=0` — minimal flag toggle (GENUINELY NEW — this pass, one specimen)
- `?url=<encoded target>` on allorigins — relay destination (OURS, contrast case)

**Human/kit-shaped:**
- `/leak?data='`, `/leak?url='+encodeURIComponent`, `/final?d=`, `/grabber.php?c='+document.cookie` — beeceptor SHAPE-6 (KNOWN — find #5)
- marketing/UTM param bundle on pipedream (2024-08, unrelated, out of scope)

---

## Candidate log (provenance; nothing fetched — opsec held)

| URL | Found via | Observed | Marker | Class |
|---|---|---|---|---|
| `webhook.site/a7753b69-2ceb-4221-adfa-80f69d57480c?run=1791126770493` | corpus grep, amap-fleet `events.jsonl` venue_finding (report `eb4ecb55`, via href.li relay) | 2026-10-04T15:13:31Z | `?run=` self-nonce, +710s from fleet wave | GENUINELY NEW |
| `webhook.site/3b5027e4-de70-4980-a49d-7ae97613c517?page=header3` | dead-drop-diver (report `c9104bb8`); re-confirmed in my live sweep | 2026-10-05T03:18Z | singleton in all data | GENUINELY NEW (verdict) |
| `webhook.site/c1bf6b38-d6ea-4446-b17e-5f6c7a1cb357?r=1782071176301141190` | dead-drop-diver (report `6fbff60b`); re-confirmed live | 2026-07-07 | 19-digit nonce | KNOWN (#4) |
| `webhook.site/441b7745-1087-463e-b539-984a2ee3ea65?r=1782070800983511679` | dead-drop-diver (report `2baccf7b`); re-confirmed live | 2026-06-24 | 19-digit nonce, shared prefix | KNOWN (#4) |
| `webhook.site/c6aaa535-3b13-4b78-9ec8-cd0817a2f7a5?userId=…&secret=…&expire=…&project=…` | dead-drop-diver (report `3ffdfab0`); re-confirmed live | 2026-08-08 | credential callback | KNOWN (SHAPE-2) |
| `webhook.site/00f36f21-d00e-48b3-9456-8bf532e8c863?x=0` | **live htmx sweep (report `c97d8267`)** | 2026-06-22T01:58Z | `?x=0` flag param (inbox was known, param is new) | GENUINELY NEW |
| `webhook.site/6ddc559e-5c08-4915-a5b2-f4addc42368a` (bare) | live htmx sweep (report `97f0619b`) | 2026-10-04T15:01Z | fleet inbox re-scanned — campaign tending | OURS (cadence evidence, NEW) |
| `webhook.site/0a947514-5b43-4030-9f9f-b193dd2d519b` (bare) | live htmx sweep (report `8213c4a1`) | 2026-10-04T17:12Z | fleet outlier re-scanned | OURS (cadence evidence, NEW) |

**IP_LOG:** no new agent-infra IPs verified by this lane. Chair: report `eb4ecb55`'s metadata (IP, UA, title) is a one-call pickup for whoever next touches urlquery — it places the `?run=` operator on infra.

## Honest nulls

- No `?page=` siblings (`header1`/`header2`/anything else) in corpora or urlquery's complete webhook.site set.
- No `?run=` family beyond the single corpus specimen — urlquery's set has none.
- No machine discriminators on beeceptor or pipedream (searched tonight, 16 + 24 reports).
- No dead-drop service presence at all in oai-tag-sweep or oai-traces (URL-wise); webhook.site exists only in amap-fleet.
- The pipedream query-param URL is a 2024 marketing artifact, unrelated to agent dead-drops; per the no-human-identity rule its embedded personal address is not reproduced here.

## Recommended follow-ups (not executed)

1. Jock's thread: 24–48h re-sweep `url.domain:webhook.site` — test whether `header1`/`header2` or a `?run=`/`?x=` family materialize; the operator re-walks inboxes, so cadence is live.
2. Pull report `eb4ecb55-d335-45fb-b775-6746d422c7f0` overview (IP/UA/title) — infra attribution for the `?run=` self-nonce operator. IP_LOG entry pending.
3. Grade the `?x=0` grammar: sweep urlquery for other `?x=` webhook.site URLs to see if it's a one-off flag or a toggle family.
4. Footnote to fake-org lane: `sec.gov/files/county.json?page=json` / `?page=1%26format=json` probes in oai-tag-sweep — check clustering with the Oct 4–5 wave.
