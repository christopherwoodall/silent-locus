# LINGUIST (CHINESE) — how Chinese-speaking agents write

Persona: specialist in agent-written Chinese. Not humans. Agents.

## Headline: the agent thinks in ASCII

Across 1,243 unique `uq*` tag values in the corpus, there are **zero CJK characters** — in
`raw/`, in `events.jsonl`, everywhere. A Chinese-speaking *human* operator labels things
with hanzi constantly (file names, comments, test labels). This agent never does. Its
Chinese exists only as toneless, separator-less, lowercase pinyin. That is the single
strongest classifier feature: **agent-written Chinese here is pinyin-only, always.**

The only actual Chinese words in the entire corpus are two, transliterated inside
payload markers (Codebreaker lane): `gucheng` (古城, "old city") and `ceshiren`
(测试人, "test person") — `data-marker="gucheng-ceshiren-delay-20261004r"`.

## The pinyin conventions (corpus inventory)

Tag grammar: `<label><YYYYMMDD>[letter|digit]>`, e.g. `uqscan=qingdaomuseum20261005b`.
37 distinct `uq*` param names; `uqscan` dominates (1,068 of 1,243 tags).

Place-name pinyin (toneless, no separators, no apostrophes):
`bailuzhou` 白鹭洲, `dazhou` 达州, `mianyang` 绵阳, `nanshan` 南山, `tongren` 铜仁,
`wangshan` 望山, `sijiqing` 四季青, `jinniu` 金牛, `jinyuan` 锦源, `baoan` 宝安,
`qinghai` 青海, `shenzhen` 深圳, `wuhan` 武汉, `nanjing` 南京, `taersi` 塔尔寺
(Kumbum Monastery), `xiangshan` 香山, `zhaolin` 兆麟, `zishui` 紫水, `longyuan` 龙源,
`weiyang` 未央, `xiaogang` 小岗, `songjiang` 松江, `shuncheng` 顺城, `qingxiushan` 青秀山,
`zhijiang` ?, `jincheng` 晋城, `haizhu` 海珠, `beihai` 北海, `gubei` 古北, `litchi` 荔枝,
`deming` ?, `xian` 西安 (see below)

Pinyin + English hybrids: `fujianmuseum`, `henanmuseum`, `qingdaomuseum`,
`gansumuseum`, `qdmuseum` (青岛), `wzmuseum` (温州), `gxmuseum` (广西), `fjmuseum` (福建),
`chaoyangpark`, `hainanwildlife`, `tianshanzoo`, `wuhanbotanical`, `botgarden`,
`shaanxihistory`, `worldpark`, `worldwindowold`, `hspark`, `szcec`, `njzwy`, `njxzgz`,
`fzmd`, `srh`, `cdhv`/`cdhvm`, `th`, `xg`, `shbg`, `xzsty`, `wfjxy`

## Machine tells (the classifier)

1. **Zero hanzi, 1,243 tags.** Humans writing Chinese labels use hanzi. The agent never
   does — not in tags, not in payloads, not in file names. Pinyin is its entire Chinese.

2. **English exonyms where a Chinese speaker uses pinyin.** `summerpalace` for 颐和园.
   A Chinese writer produces `yiheyuan`; "summer palace" is the English Wikipedia name.
   This is an English-dominant model reaching for the English label. Same for `worldpark`,
   `botgarden`, `hainanwildlife` — descriptive English compounds, not transliterations.

3. **Lost disambiguation: `xian`.** 西安 (Xi'an) without the apostrophe collides with 县
   (xiàn, county). Pinyin input methods and human writers both preserve the apostrophe
   or use hanzi. Dropping it is what a model does when it never learned the distinction
   matters.

4. **Opaque initialisms.** `njxzgz`, `fzmd`, `srh`, `cdhv`, `xzsty`, `th`, `xg`, `shbg`.
   Human Chinese abbreviations are conventional (京, 沪, BJ, SH) or readable. These are
   machine shorthand — consistent within the harness, meaningless outside it.

5. **Translationese in the one real Chinese word.** `ceshiren` 测试人 = "test person."
   A human QA label is 测试 (test) or test. 测试人 is what a model writes when it
   translates "test person" word by word — literal, grammatical, and slightly off.

6. **Machine timestamping as grammar.** `<label><YYYYMMDD>[letter]>` — `20261004a`,
   `20261005b` — plus raw epoch nonces (`uq=1791089794`). Humans date things
   10-04 or 1004; YYYYMMDD+run-letter is harness bookkeeping.

7. **Abstract-word labels.** `research` ×103, `answer20261005`, `target`, `zhuoyue` 卓越
   ("excellence") as a place label. The agent labels by *function*, not by name —
   task-oriented rather than referential.

8. **The `claude` self-label — 182 tags.** `uqscan=claude20261004bailuzhou`,
   `uqscan=claude20261001summerpalace`, `uqresearch=claude20261004xzs1`,
   `uqdirect=claude20261004v5`, `claude-bootstrap`, `claude-ssr-place`, `claude-test-1791099600`.
   No gpt/deepseek/gemini/qwen tags exist. The agent (or harness) names its runs after
   the model family driving them. Whether this is honest self-identification or a decoy
   is open — but it is a *model-attribution artifact*, and it is consistent across
   20261001–20261005.

## The Dream parallel (reported, not in our bytes)

Dream's Taiwan swarm showed Simplified Chinese in internal/status logs and Traditional
Chinese in target analysis — the internal voice vs. the target-facing voice. Our corpus
shows the same structural split one level down: the internal voice is ASCII pinyin +
English (`gucheng-ceshiren`, `claude20261004*`), and there is no target-facing Chinese
at all — the targets are Chinese sites addressed entirely in ASCII. Same shape:
**the agent's private language is not the target's language.**

## Classifier summary: agent vs human Chinese

| Feature | Agent (this corpus) | Human |
|---|---|---|
| Hanzi in labels | 0 / 1,243 | frequent |
| Pinyin style | toneless, no separators | tone marks or separators, or hanzi |
| Exonyms | English (`summerpalace`) | pinyin (`yiheyuan`) or hanzi |
| Ambiguity | `xian` unmarked | 西安 or xi'an |
| Abbreviations | opaque (`njxzgz`) | conventional (京/BJ) |
| Test labels | `ceshiren` (translationese) | 测试 / test |
| Dates | `YYYYMMDD`+letter, epochs | 10-4, 1004 |
| Self-reference | model name as run label | project/task name |

Confidence: high for the pinyin-only and exonym features (corpus-wide, hundreds of
samples). Medium for translationese (n=1 word). The `claude` self-label is
descriptive, not diagnostic of model family — treat as harness convention.

## Huntable grammar for other personas

- `uq[a-z]*=<pinyin-word><YYYYMMDD>[a-z0-9]>` — the tag grammar itself
- `gucheng-` / `ceshiren` / `data-marker="gucheng-` — payload markers
- `claude<YYYYMMDD>` as run prefix — model self-labels; hunt other model names in
  the same position (`gpt<date>`, `deepseek<date>`, `qwen<date>`) on urlquery/urlscan
- Toneless-pinyin-only labeling on non-Chinese targets — an agent working Brazil or
  India in ASCII transliteration would show the same shape

## What I did not do

- urlquery htmx external checks for `ceshiren`/`gucheng` were throttled this session
  (proxy tunnel failures under persona-swarm load) — retry on a calm window.
- Gist/paste sweeps for the grammar deferred to Grammarian/Codebreaker.
- No CJK found in `openai-agent-traces` or `collusion-wiki` corpora either — the
  pinyin-only convention appears consistent across our agent corpora, which strengthens
  the classifier but means cross-corpus hanzi comparison wasn't possible.
