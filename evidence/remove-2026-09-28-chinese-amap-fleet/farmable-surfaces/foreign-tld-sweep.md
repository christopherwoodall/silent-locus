# Foreign-TLD sweep — agent/swarm filter (2026-10-05)

User direction: extend marker/infra sweeps to foreign TLDs (.cn, IDN/punycode, non-Western shorteners/paste services), aimed at finding other AGENT operators' infrastructure. Course correction applied: hunting agent/swarm BEHAVIOR (bursts, tag grammars, self-documenting labels, systematic enumeration), not generic IOCs. Single malware hits = noise; programmatic bursts with grammar = signal.

## .cn + our markers (urlquery htmx)
| Query | Result |
|---|---|
| `uqscan cn` / `uqscan .cn` | 3 hits — all `zh-CN` artifacts in translate.goog URLs (operator's own Amap reports). No actual .cn operator infra. |
| `uqcors cn` | 0 |
| `uqtag cn` | 1 hit (vimeo.com — keyword noise) |
| `xn-- uqscan` (punycode) | 0 |
| `t.cn uqscan`, `url.cn uqscan` | 0 |

## Chinese shorteners (urlquery htmx)
| Shortener | Hits | Agent-shaped? |
|---|---|---|
| `suo.im` | 4 (short links; one adware traffic-diversion page) | No — no grammar, no bursts |
| `985.so` | 2 (2023–2024 plain short links) | No |
| `dwz.cn` | 8 (email-tracking links, parked domains) | No — marketing infra |

## Local corpus (.cn / IDN / shorteners)
- 15 unique .cn domains in corpus: ALL task targets (Chinese POI sites, `beian.miit.gov.cn`, university/gov domains for the scraping tasks) — not operator infrastructure.
- Zero punycode (`xn--`) addresses. Zero foreign-shortener URLs.

## urlscan.io
- `uqscan=` → 0. `amap` → 0. No foreign-TLD agent traces.

## OTX burst analysis (agent-behavior lens)
Applied the filter to OTX's lhr.life (200 URLs) and is.gd (4,000 URLs) lists: looking for programmatic bursts WITH structure, not volume alone.

**SIGNAL — `02e18ab88f2ece.lhr.life` (2026-08-16):** 41 URLs in one hour, all on ONE tunnel with paths `/883120a1824c6dce00679806/c/01` … `/c/20` — systematic numbered-endpoint enumeration within ~15 min. Agent-shaped (task dispatcher / C2 panel pattern). NOT our operator (absent from our corpus; no shared subdomains). Different actor, noted as other-operator lead.

**NOISE — is.gd 2026-01-31T15:** 378 slugs in one hour, all random 6-char alphanumerics (is.gd default). Bulk creation with zero grammar — no agent tells. Filtered out per the user's rule.

## Verdict
- Our operator uses zero foreign-TLD infrastructure: no .cn, no punycode, no Chinese shorteners. Their stack is Western-surface (is.gd, httpbun, lhr.life, webhook.site).
- Foreign shorteners carry no agent-swarm activity with our markers or any other tag grammar.
- One other-operator agent-shaped lead: the `/c/NN` enumerated tunnel (above). Not foreign-TLD, not ours — logged, not tracked.

## Continuation 2026-10-05 — Russian shortener via urlscan (fetch fallback; VM egress down)
- `domain:clck.ru` (Yandex shortener, .ru) → 100 recent scans. Content: Yandex
  Practicum affiliate-marketing links (`utm_source=partners`, `utm_medium=mkb`)
  plus a few directly-scanned shorts returning 406. One cluster of note: the
  same 3 shorts (`3FtCv5`, `3E8tZe`, `3FAxcn`) re-scanned via API on Oct 3–4,
  2 requests each — automated re-scan cadence, but no agent markers, no
  grammar, no bursts with structure.
- Verdict: honest negative for agent-swarm activity on clck.ru in the 30-day
  urlscan window. Foreign-TLD sweep stays negative for agent-shaped behavior;
  the `/c/NN` payload campaign remains the only other-operator lead and it is
  not foreign-TLD.
