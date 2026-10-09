# French hunt — Findings 2: agentness words, time blasts, cross-swarm slice (2026-10-05)

Follow-up to FINDINGS.md, closing two gaps plus a cross-swarm slice.
**Caveat: urlquery.net rate-limited this task (HTTP 429) mid-sweep — per policy no further
API calls were made. Hit counts and completed samples below are final; items marked
NOT EXAMINED need a follow-up run.**

## 1. French agentness words

Raw keyword hit counts (urlquery matches submitted-URL text AND page content):

| Word | Hits | Note |
|---|---|---|
| `agent` | 6,776,335 | Useless alone — matches "user agent", "agent immobilier", etc. |
| `recherche` | 2,598 | French for "search" — high-frequency ordinary vocabulary |
| `analyse` | 20,535 | Ordinary |
| `donnees` / `donn%C3%A9es` | 15,147 / 153 | ASCII-normalized search; accented form adds nothing |
| `extraction` | 2,131 | |
| `collecte` | 1,554 | |
| `robot` | 24,950 | robots.txt, robotics — ordinary |
| `automatique` | 2,235 | |
| `tache` | 2,493 | |
| `mission` | 20,841 | Ordinary (space missions, etc.) |
| `resultat` | 968 | |

Combined with program infrastructure:

| Pivot | Hits | Verdict |
|---|---|---|
| `httpbin recherche` | 126 | NOT EXAMINED (rate limit before sampling) |
| `httpbun recherche` | 0 | Zero — no httpbun programs with French "recherche" |
| `httpbin collecte` | 4 | Sampled: all `report.error-report.com` — noise, not agent-shaped |
| `httpbun collecte` | 0 | Zero |
| `webhook.site recherche` | 14 | Sampled: lavazza.co.za / lavazza.it / lavazzaofficial.ma / diasporam.com — coffee-brand and diaspora pages where "recherche" = ordinary French "search" text. Not agent programs. |
| `webhook.site collecte` | 11 | Sampled: goodchange.app / cory4judge.org / becky4countycommission.com / chris4nlv.com — US political donation pages with French-language "collecte de fonds" text. Not agents. |
| `livecodes recherche` | 0 | Zero |
| `base64 collecte` | 767 | NOT EXAMINED (rate limit before sampling) |

**French tag-grammar params** — `?recherche=` / `?tache=` / `?mission=` / `?resultat=` /
`?collecte=` / `?analyse=` returned counts IDENTICAL to the bare words (2,598 / 2,493 /
20,841 / 967 / 1,554 / 20,534), meaning urlquery's search strips `?`/`=` punctuation —
param-shape pivoting does not work through this API. `uqscan=fr` = 0, `uqtag=fr` = 0:
no French uqscan/uqtag tags exist.

**Interpretation:** French agentness words are high-frequency ordinary French vocabulary.
Keyword search matches page content, not program structure, so these words cannot
discriminate agents from humans. The discriminating pivots remain URL-structural
(program hosts + French content in paths) or tag grammars — both empty so far.
A stronger next attempt: `httpbun.com/` + French city names in path segments
(`httpbun paris`, `httpbun lyon` were noise because keyword matched page text, not URL —
needs report-body inspection, not keyword search).

## 2. Time blasts — NOT COMPLETED (rate-limited)

Methodology staged for a follow-up run once the 429 clears:

1. Pull reports (with timestamps) for every French-domain pivot with >5 hits:
   data.gouv.fr (19), zerobin.net (12), frama.link (20), `mistral` keyword (1,235 —
   sample ~300), `itineraire` (2,129 — sample ~500), qwant.com (3), geoportail.gouv.fr (3).
2. Histogram timestamps by hour and by day per target.
3. Flag bursts: >10 reports in one hour on a single target, or >30 in a day —
   the Amap fleet's signature was 1,810 reports in one day.
4. Re-examine `itineraire` for burst clustering: the first pass dismissed all 2,129 as
   tourism from keyword matches, but a fleet scraping French itineraries would hide
   inside exactly that keyword — only the time distribution can separate it.

Nothing about the French targets' time distribution is established yet. This is the
highest-value open item from this follow-up.

## 3. Cross-swarm shared vocabulary — French slice

Checking whether other swarms' markers appear in French contexts
(shared marker in a new language = shared toolkit evidence):

| Pivot | Hits | Verdict |
|---|---|---|
| `claude paris` | 1,479 | Count only — NOT EXAMINED (rate limit). Likely noise: Claude (name) × Paris (city) are both high-frequency. |
| `claude recherche` | 627 | Count only — NOT EXAMINED |
| `claude francais` | 969 | Count only — NOT EXAMINED |
| `claude httpbin` | 71 | Sampling failed (429). NOT EXAMINED |
| `ltzh paris` | 1 | Sampled: `www.wexbusinesspayments.com/` (2025-11-09) — "ltzh" matching a random hex substring, not a program. Noise. |
| `ltzh france` | 4 | Sampled: eoob.no, fumamx.com, wexbusinesspayments.com, 17.magic88.cc — all "ltzh" inside unrelated hex/UUIDs. Confirms the Zhipu hunt's warning: raw `ltzh` keyword is 99% noise. |
| `zz=oai paris` | 493 | Count only — NOT EXAMINED |
| `uqscan le` | 258 | "le" matches inside arbitrary words — not pursued. |

**Verdict:** no cross-swarm marker (`uqscan=`/`uqtag=`/`zz=oai`/`claude`-labels/`ltzh`
families) was observed in a French context. The one fully checkable slice (`ltzh` +
French) was hex-substring noise. The `claude` + French counts are large enough to
deserve sampling in a follow-up run, but the base rate of "Claude" × "Paris" as
ordinary words is high.

## Summary

- French agentness words: searched, no agent-shaped results; ordinary French vocabulary
  defeats keyword pivots — need URL-structural or report-body analysis instead.
- Time blasts: not completed, rate-limited; methodology staged, highest-value open item.
- Cross-swarm French slice: no shared markers observed; `ltzh`+French fully ruled out
  as hex noise; `claude`+French counts need sampling later.
- Net new traces from this follow-up: **zero**. The French zero stands, now with the
  vocabulary and cross-swarm angles checked as far as the rate limit allowed.

Nothing pushed, per instructions.
