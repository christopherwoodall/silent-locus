# Paste-archive recovery — 2026-09-27

Lane 3 of the archive-recovery fan-out. Scope: paste hosts from the
investigators' `site-coverage.csv` other than paste.linuxiarz.pl (separate lane).

## Headline: nothing was dead — all three hosts are live

No archive recovery was needed. `pastebin.k4be.pl`, `anna.fyi`, and
`infinitypaste.club` all serve normally as of 2026-09-28. `swarm.termina.digital`
does not appear in `site-coverage.csv` at all (0 rows) — it was in the lane
brief but not in the investigators' coverage, so it was not pursued.

## pastebin.k4be.pl — 20/20 live (Stikked)

- **6 full bodies recovered**: EPL relegation tables — `EPL 2000/01`, `2001/02`,
  `2002/03`, `2003/04`, `2004/05`, and `EPL 1995-00 home-away relegation data`
  (cites the official Premier League Pulselive API). Clean task data, zero
  tradecraft on the battery.
- **11 ROIETA-series pastes** (metadata only): `ROIETA1..8` + three year-range
  pastes — Roi Et province (TH45, Thailand) health-study data extracts with
  numeric values in titles (35083, 36227, 46308…). Authors are adjective–animal
  generated pseudonyms: Perl Rhinoceros, Abrupt Armadillo, Morose Tortoise,
  Baby Curlew, Diminutive Peafowl, Chartreuse Sheep, Whipped Pig, Paltry
  Meerkat, Lousy Shama, Queen Meerkat, Perl Dormouse. View counts 186–248.
  Bodies sit behind raw/download endpoints that the text fetch renders as `x` —
  need a live-browser render. **Time-sensitive**: pages show
  `[paste_expire] 4 miesiące` (expire in 4 months).
- **3 reply-form-only**: `stats reference link`, `Roi Et province (TH45) male
  studies Q2 2013-2021`, and `linktry97976` — the last uses campaign grammar
  (`link`+`try`+digits).

## anna.fyi — 53/55 titles verified live

All "Statistical reference N" series (N = 1–48 observed), plus `ReplyLink0/1/2`,
`NSI table reference 2009-2015` (×2), and `Official data link`. Bodies are
JS-gated in text fetch — titles only, need a live-browser render for bodies.
2 URLs unchecked (rate-limited mid-census, not retried per instruction):
`e3b8ac8c`, `e88e8449`.

Notable: `93811d8c` ("Official data link") threw a PHP/GeSHi deprecation error
leaking the server path `/home/things/domains/anna.fyi/public_html/`
(CodeIgniter: `controllers/Main.php`, `models/Pastes.php`). Infrastructure fact
only.

## infinitypaste.club — 1 paste, body recovered

`Gf4nRzww` ("LinkNSIDataMay27Final", created 2026-05-27, 676 views): a single
official-statistics reference link to `site-test.nsi.bg` (Bulgarian NSI
infostat). Same statistics-reference task family as the anna.fyi series.

## Task-family read

The three hosts converge on one task family: **official-statistics reference
work** — EPL standings via the Pulselive API, Thai provincial health studies,
Bulgarian NSI tables. Same family as the wiki agents' statistics tasks; the
pastes are agent working notes / shared reference links, not tradecraft
carriers (zero hits on the full IOC battery).

## Dataset & index

- `data/paste-archive/` — bodies, metadata, titles, `manifest.json`,
  `PROVENANCE.md` (separate dataset, out of collusion-wiki).
- Elastic index **`paste-archive`** (own index per standing rule), shared schema,
  `event.dataset=paste-archive`.

## Follow-ups for the parent

1. Live-browser render lane for the 11 ROIETA bodies + 55 anna.fyi bodies before
   the k4be 4-month expiry window closes.
2. The 2 unchecked anna.fyi URLs (`e3b8ac8c`, `e88e8449`) still need title checks.
3. `linktry97976` (k4be) deserves a grammar-battery note — `link`+`try`+digits
   matches the campaign's generative naming.
