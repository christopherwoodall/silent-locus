# Cultural Anthropologist (East Asia) — FINDINGS

**Date:** 2026-10-05
**Lens:** East Asian work culture, public-holiday calendars, naming/script conventions.
**Scope:** AGENTS, not operators. No human attribution.

## Verdict

The agent corpora carry **Chinese public-holiday fingerprints**. The strongest: near-zero agent activity across the May 1–5 Labour Day holiday followed by a 293,898-capture burst on May 6 (first workday back), and a Golden Week trough (Oct 1–3) inside the Amap corpus. The workday rhythm is 996-shaped, not 955. Naming is pinyin + English task words in ASCII — zero Chinese script anywhere in 1,272 tag values — and the agent self-labels runs with the model name `claude` (174 values, the single most common label word).

## 1. Holiday-calendar matches (2026 official State Council calendar)

| Holiday (2026) | Dates | Agent-corpus match |
|---|---|---|
| Labour Day (劳动节) | May 1–5 (Fri–Tue); May 9 (Sat) make-up workday | **Strong.** Arquivo.pt-sourced agent traffic: 11 events May 1, **zero May 2–5**, then a **293,898-capture burst on May 6** — Maryland education-data URLs, first workday after the holiday. |
| Dragon Boat (端午节) | Jun 19–21 (Fri–Sun) | AIHW June R&D strand (`uqtag=AGEDATA23`, vizprod.aihw.gov.au) ran **Sat Jun 20 — inside the holiday**. Weekend work during a festival break. |
| Mid-Autumn (中秋节) | Sep 25–27 (Fri–Sun) | Amap corpus begins Sep 28 (Mon, first workday after): 20 reports, ramping to 144 by Sep 30. Post-holiday ramp-up shape. |
| National Day / Golden Week (国庆节) | Oct 1–7 (Thu–Wed) | **Trough.** True submission dates: Sep 30 (last pre-holiday workday) 144 → Oct 1: 59 → **Oct 2: 0** → Oct 3: 4 → Oct 4: 1,722 → Oct 5: 18. |
| Spring Festival (春节) | Feb 15–23 (9 days, longest ever) | No corpus coverage — **open hunt window.** If any agent corpus spans Feb 2026, expect a 9-day silence. |

**Caveats (read before citing):**
- The May 6 burst timestamp is Arquivo.pt's **CDX capture time**, a proxy for the agent's request time. The Labour Day silence → May 6 burst is consistent with holiday observance, but capture scheduling could contribute.
- The Oct 4 count (1,722) is inflated: it's the htmx collection day. The Oct 1–3 trough (59 / 0 / 4) vs the Sep 30 ramp (144) is the real signal — the collection window covered those days equally.
- The jmail.world auditor (Oct 2–5, 872 reports, unbroken 24/7) ran **straight through Golden Week** — no holiday observance, consistent with its "human's script/cron" grading rather than a human-gated swarm.

### Jul 1–4 (Dream swarm) — date symbolism note
Jul 1 is the **CPC founding anniversary** (1921 → 105th in 2026) and Hong Kong SAR Establishment Day. The Dream offensive ran Jul 1–4, launching *on* Jul 1 and ending on US Independence Day. No Taiwan public holiday falls in that window (Taiwan does not observe mainland Golden Week). Whether Jul 1 was chosen or coincidental is unknowable from metadata — recorded as a date to cross-check if sibling campaigns surface.

## 2. Work-rhythm shape: 996, not 955 (Beijing hours, n=1,970 true submission dates)

```
00 28 | 01 60 | 02 72 | 03 18  <- sleep floor
04 71 | 05 61 | 06 44 | 07 36
08 65 | 09 46 | 10 31          <- slow morning ramp
11 84 | 12 108| 13 150| 14 136| <- afternoon peak (no lunch dip)
15 105| 16 127| 17 63          <- 17:00 dinner dip
18 181| 19 151| 20 122| 21 143 <- evening overtime peak
22 30 | 23 38                  <- wind-down
```

- **No lunch dip.** 12:00 (108) → 13:00 (150) rises straight through the standard 12:00–13:30 lunch. Machines don't eat lunch.
- **Dinner dip at 17:00** (63 vs 181 at 18:00) and **sleep floor at 03:00** (18) — the two human tells in an otherwise machine curve.
- **Evening overtime peak 18:00–21:00** with a slow morning ramp is the classic **996 curve** (9am–9pm), not 955. A 955-shaped agent would fall off a cliff at 18:00; this one peaks there.
- No weekend dip anywhere in the June strands (IDPH Sat/Sun Jun 20–21, AIHW Sat Jun 20).

Reading: a human-scheduled machine — lunch is skipped (automation), but dinner/sleep/holiday rhythms leak through the schedule. Consistent with Night Owl's UTC+8 fit.

## 3. Naming conventions: pinyin + English, ASCII-only

From 1,272 `uq*` parameter values (distinct label words, dates stripped):

- **Zero CJK characters in any value.** A Chinese-attributed agent that never writes Chinese script in its tags — pinyin transliteration instead. This is a technical choice (ASCII-safe, no URL-encoding breakage) that also makes the tags grep-friendly for us.
- **Model self-label: `claude` ×174** — the single most common label word, and the *only* model name present (no gpt/deepseek/gemini/qwen/kimi/doubao/glm). The agent names its runs after its model: `uqscan=claude20261004target1`. (Flag for Model Whisperer.)
- **Pinyin place names:** taiyuan, zhenbeibao (镇北堡), taersi (塔尔寺, Ta'er Monastery), longyuan, zishui, jincheng, mianyang, xiangshan, shuncheng, beihai, haizhu, gubei, nanjing, wuhan, deming, zhijiang, xiaogang, zhuoyue, lingfeng, qinghai, hainan, gansu, henan, fujian, wenzhou, qingdao (qd).
- **Bureaucratic acronyms** (pinyin initials, Chinese admin style): `njxzgz` ×16, `fzmd` ×9, `cdhv` ×7, `srh` ×7, `njzwy`, `xzsty`, `wfjxy`, `szcec`, `cdhvm`, `shbg`, `xg`, `th`. These read like Chinese institutional abbreviations (cf. university-shorteners lane).
- **English task words:** research, target, api, detail, place, deep, answer, direct, verify, proper, mobiletarget, targetdetail, poidetail.
- **Date format: compact `YYYYMMDD`** (`20261004`), no separators — Chinese convention. Mixed with epoch nonces (`uqscan=1791077647`).
- **Notable labels:** `navy971-20261005{a,b,c}` (military-adjacent, Oct 5 — *during* Golden Week), `xian-olympic-arrival-20261004{a–d}` (event-shaped), `gucheng-*` with `ceshiren` (测试人, "test person") inside a payload per Codebreaker.

## 4. Script policy vs the Dream swarm

- **Dream swarm archive:** Simplified Chinese internal/status logs, Traditional Chinese target analysis — the script split *is* the attribution-relevant metadata there.
- **Our agent:** no Chinese script anywhere in 1,272 tag values. Different agents, different script policies. If a new cluster shows Traditional-script tags hitting Simplified-script targets (or vice versa), that's a Dream-swarm-shaped lead; pinyin-ASCII tags are our agent's shape.

## 5. Open questions / hunt leads

1. **Spring Festival Feb 15–23, 2026 (9 days)** — no corpus covers it. Any agent corpus spanning Feb 2026 should show a 9-day silence; absence of the silence would be as informative as presence.
2. **Make-up workdays (调休):** Sep 20 (Sun) and Oct 10 (Sat) 2026 were official workdays. Agent activity on a Sunday make-up workday would be a strong cultural tell — hunt urlquery for Sep 20 / Oct 10 bursts with Chinese-grammar tags.
3. **`navy971` labels during Golden Week** — military-adjacent naming + holiday-period activity deserves a Grammarian/Cartographer cross-check (what targets did those three reports hit?).
4. **The lunch test generalizes:** any new cluster with a 12:00–13:30 Beijing dip is more human-driven; no dip + 03:00 floor = scheduled machine. Apply as a quick classifier.
5. **Taiwan/Japan/Korea calendars** showed no matches in current corpora — expected, since current corpora are mainland-shaped. Revisit if Global South Scout / Polyglot surface non-mainland clusters (e.g., Chuseok Sep 24–26 for Korean-shaped agents).

## Sources
- Official 2026 PRC holiday calendar: State Council General Office notice (Nov 4, 2025) via msadvisory.com, slasify.com, humanresourcesonline.net — Labour Day May 1–5, Dragon Boat Jun 19–21, Mid-Autumn Sep 25–27, National Day Oct 1–7, Spring Festival Feb 15–23.
- Corpus bytes: `raw/page_*.json` (1,970 reports, true `date` fields), `data/2026-10-03-openai-agent-traces/events.jsonl` (589,972 events; May 6 burst = `arquivo_pt_capture` records from `data/2026-10-01-arquivo-pt/raw/maryland-edstats.cdx.jsonl.gz`).
- Cross-read: Night Owl (`personas/night-owl/FINDINGS.md`), Codebreaker (`personas/codebreaker/FINDINGS.md`), cachedview (`cachedview/FINDINGS.md`).
