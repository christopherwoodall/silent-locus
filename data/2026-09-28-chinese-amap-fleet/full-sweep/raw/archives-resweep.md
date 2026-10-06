# Web-archive resweep — NEW fleet-adjacent tunnel names (2026-10-05)

Lane E resweep. Probed: 2026-10-05 ~07:56–08:50 CDT (12:56–13:50 UTC). Operator: subagent f0bd1b32.
Scope: presence/absence of archived captures for tunnel names from lanes that ran after
`archives.md` / `trick-pastes-archives.md`. No fleet-operator content scraped beyond presence/absence.

## Names swept (20)

| bucket | names |
|---|---|
| ZeroSSL (8, `lead-zerossl-followup.md`) | `a7bfa19dd56391`, `ca990e9a89525d`, `deab0fff603d04`, `0418f1e395a48e`, `92f1f5cd378431`, `efa9eb3bda1df5`, `967f1af7dfd915`, `93ca25e80716ce` |
| tronzap Sep-26 (7, `lead-urlscan-tronzap.md`) | `90667af7b6a9f1`, `d789d4fd5debd8`, `3be663c0dc1827`, `90c6961dd9eba0`, `ba85c283a8f9e0`, `52949a80bf53fc`, `d51842b87c3e80` |
| tronzap Sep-29 (2) | `1881e623217f7c`, `2f102b0544d3b3` |
| June-2026 tunnels (2, `htmx-extended.md`) | `7e7ff6dbbe9824`, `91ef9fc4c82a1b` |
| Radar tunnel (1, `lead-radar-tunnel.md`) | `91b9ec611bbd73` |

All `<name>.lhr.life`. Cross-check: none of the 20 appear in the prior sweep's Wayback
`lhr.life` domain dump (4 hosts) or archive.today's 37 archived subdomains.

## Method & endpoints

1. **Megalodon** — `GET https://megalodon.jp/?url=<urlencoded https://<host>/` (keyless, server-rendered).
   Lookup page title: `魚拓リスト - https://<host>:443/`. Presence of section heading
   `取得済みの魚拓` does NOT mean captures exist: zero-capture pages render
   `取得済みの魚拓 見つかりませんでした。` (not found). Detection rule: CAPTURES only if
   `取得済みの魚拓` present AND `見つかりませんでした` absent. Initial naive grep on the
   heading alone false-positived 20/20 — corrected and re-verified from saved HTML.
   Pacing: ~8s.
2. **Wayback CDX** — `GET https://web.archive.org/cdx/search/cdx?url=<host>&matchType=domain&output=json&limit=100&collapse=urlkey`.
   All 20 returned HTTP 200 with literal `[]`. Pacing: 45s (budget honored; 20 reqs ≈ 29 min
   wall time including fetch latency). No 429/403 encountered.
3. **archive.today** — `GET https://archive.ph/search/?q=<host>` **must use `-L`**: without it the
   endpoint answers bare HTTP 302 (empty body); following the redirect lands on
   `https://archive.ph/<host>`, the host's snapshot page. Detection: page contains
   `No results` (negative) vs snapshot rows (`<d> <Mon> <YYYY> <HH:MM> <title>`).
   Positive control: `6e6d931ed3a4a8.lhr.life` (prior sweep's capture) shows
   `3 Oct 2026 07:17 0100633007D48800 v196608 torrent` — the method has recall on this surface.
   All 20 names: HTTP 200 + `No results`. No 429s. Pacing: ~10s.
4. **Common Crawl** — `GET https://index.commoncrawl.org/CC-MAIN-2026-39-index?url=<host>%2F*&output=json&limit=100`
   (unfiltered prefix; latest collection at sweep: CC-MAIN-2026-39). Pacing: ~8s.
   404 "No Captures found" = clean negative (11/20). HTTP 504 on unfiltered prefix = inconclusive
   (9/20) — same flip-flop seen in `archives.md` on a known-present sanity term; do not read as negative.

## Results matrix (all 20: zero captures everywhere)

| name | Megalodon | Wayback CDX | archive.today | Common Crawl 2026-39 |
|---|---|---|---|---|
| a7bfa19dd56391 | negative | 200, `[]` | No results | 404 clean |
| ca990e9a89525d | negative | 200, `[]` | No results | 404 clean |
| deab0fff603d04 | negative | 200, `[]` | No results | **504 inconclusive** |
| 0418f1e395a48e | negative | 200, `[]` | No results | 404 clean |
| 92f1f5cd378431 | negative | 200, `[]` | No results | **504 inconclusive** |
| efa9eb3bda1df5 | negative | 200, `[]` | No results | **504 inconclusive** |
| 967f1af7dfd915 | negative | 200, `[]` | No results | 404 clean |
| 93ca25e80716ce | negative | 200, `[]` | No results | **504 inconclusive** |
| 90667af7b6a9f1 | negative | 200, `[]` | No results | 404 clean |
| d789d4fd5debd8 | negative | 200, `[]` | No results | **504 inconclusive** |
| 3be663c0dc1827 | negative | 200, `[]` | No results | 404 clean |
| 90c6961dd9eba0 | negative | 200, `[]` | No results | **504 inconclusive** |
| ba85c283a8f9e0 | negative | 200, `[]` | No results | **504 inconclusive** |
| 52949a80bf53fc | negative | 200, `[]` | No results | 404 clean |
| d51842b87c3e80 | negative | 200, `[]` | No results | 404 clean |
| 1881e623217f7c | negative | 200, `[]` | No results | 404 clean |
| 2f102b0544d3b3 | negative | 200, `[]` | No results | 404 clean |
| 7e7ff6dbbe9824 | negative | 200, `[]` | No results | 404 clean |
| 91ef9fc4c82a1b | negative | 200, `[]` | No results | **504 inconclusive** |
| 91b9ec611bbd73 | negative | 200, `[]` | No results | **504 inconclusive** |

## Verdict

**Honest zeros across the board: 20/20 names have zero archived captures on all four surfaces.**
Wayback (200+`[]`) and archive.today (`No results`, recall-verified on a positive control) are
definitive negatives for those two archives. Megalodon is a definitive negative (submission-driven;
the operators' tunnels were never submitted). Common Crawl: 11 definitive negatives (404),
9 inconclusive (504 flip-flop — retryable later, not negatives).

Reading: consistent with the `trick-pastes-archives.md` picture — ephemeral tunnel endpoints are
essentially never web-archived. The tronzap exploit-probing pages (38 urlscan scans, Sep 26) and the
June-2026 uqcors/probe2 lanes exist in urlquery/urlscan but nowhere in web archives. Absence here is
expected for short-lived tunnels, not evidence against the lanes' other findings. No new fleet
signal from web archives on this name set.

## Open / blocked (not negatives)

- 9 Common Crawl 504s (listed above): retry on a later crawl or after cooldown; keep as inconclusive.
- Megalodon keyword (free-word) search endpoint still unrecovered (delegated per `japan-archives.md` §5)
  — would sweep archived titles for `lhr.life`/`uqscan` without knowing names.
- ghostarchive `/search?term=` for the 20 names was out of scope (prior sweep pattern);
  ghostarchive had 1 capture for `lhr.life` total, so expected-negative but unverified per-name.

## Repro

- Scripts: `/tmp/resweep/sweep.sh` (ephemeral) — phases: Megalodon (~8s), archive.today (~10s),
  Common Crawl (~8s), Wayback CDX (45s). `/tmp/resweep/at_rerun.sh` (archive.today `-L` re-run).
- `curl -s -A "<browser UA>" "https://megalodon.jp/?url=<urlencoded https://HOST/>"` → check for
  `見つかりませんでした` (negative) vs capture rows.
- `curl -sL -A "<browser UA>" "https://archive.ph/search/?q=<HOST>"` → `No results` vs snapshot rows
  (`\d{1,2} [A-Z][a-z]{2} 20\d{2} \d{2}:\d{2}`).
- `curl -s "https://web.archive.org/cdx/search/cdx?url=<HOST>&matchType=domain&output=json&limit=100&collapse=urlkey"` → `[]`.
- `curl -s "https://index.commoncrawl.org/CC-MAIN-2026-39-index?url=<HOST>%2F*&output=json&limit=100"` → 404 = clean negative; 504 = inconclusive.
