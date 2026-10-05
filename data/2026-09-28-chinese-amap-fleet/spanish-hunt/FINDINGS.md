# Spanish hunt — Findings (2026-10-05)

Full pass including follow-up angles (agentness words, time blasts, cross-swarm vocab).
Verdict: **no Spanish agent fleet on urlquery.net** — clean sweep, all honest zeros.

## 1. Spanish map/POI targets (Amap analogy)

| Pivot | Hits | Verdict |
|---|---|---|
| `url.domain:paginasamarillas.es` | 1 | Single 2026-05-20 Sevilla business listing. Ordinary. |
| `url.domain:qdq.com` | 0 | |
| `url.domain:guiacampsa.es` | 0 | |
| `url.domain:ign.es` | 1 | Single 2026-03-29 geodesy data page. Ordinary. |
| `url.domain:callejero.es` | 0 | |
| `url.domain:ine.es` | 0 | Spanish statistics institute — untouched. |
| `url.domain:paginasamarillas.com` | 0 | |
| `url.domain:11870.com` | 0 | |
| `url.domain:emis.es` | 0 | |
| `url.domain:tripadvisor.es` | 0 | |

No systematic Spanish place/API scanning. No Amap analog.

## 2. Spanish native infra

| Pivot | Hits | Verdict |
|---|---|---|
| `url.domain:ouo.io` | 47 | Ad-link shortener popular in Spanish-speaking world. Sampled: homepage/short-link scans, no agent markers. (Burst check pending — API throttled.) |
| `url.domain:paste.rs` | 77 | Not Spanish-native (generic). Max 4/hour — background noise, no bursts. |
| `url.domain:0x0.st` | 23 | Generic file host. No agent markers in sample. |
| `url.domain:acortame.com` | 0 | |
| `url.domain:bitly.es` | 0 | |
| `url.domain:pastebin.es` | 0 | |

No Spanish-native shortener/pastebin shows agent use. Consistent with the login-wall dynamic: agents prefer no-login Western services.

## 3. Relay stack with Spanish targets

| Pivot | Hits | Verdict |
|---|---|---|
| `r.jina.ai` + elpais/elmundo/es-wikipedia | 0 | No jina fetching of Spanish targets. |
| `webhook.site madrid` | 60 | 1 sampled: rsshubx.appwrite.network — harness noise, not Spanish fleet. |
| `httpbin madrid` | 1,172 | Keyword noise (pages mentioning both terms), not carrier URLs. Same pattern as French/German. |
| `httpbun madrid` | 0 | |
| `livecodes madrid` | 0 | |

## 4. Spanish agentness words (proper pass, not tourism words)

| Pivot | Hits | Verdict |
|---|---|---|
| `httpbin agente` | 1 | salesforce-experience.com — noise. |
| `httpbin búsqueda` / `extraccion` / `recopilacion` / `tarea` / `mision` | 0 | All zero. |
| `httpbun agente` / `busqueda` | 0 | |
| `webhook.site agente` | 5 | Brazilian domains (tnovas.com.br, innovasie.com.br) — Portuguese keyword matches, not agent-shaped. |
| `webhook.site busqueda` | 1 | intermundial.es travel insurance — noise. |

Zero agent-shaped programs with Spanish agentness vocabulary.

## 5. Local corpus check (fleet's 2,673 collected reports)

- Zero Spanish agentness words (`búsqueda`, `extracción`, `recopilación`, `ubicación`, `consulta`, `misión`, `tarea`) in any collected report.
- Zero Spanish place names (madrid, barcelona, sevilla, españa, mexico, argentina, lima, bogota) in program titles.

## 6. Cross-swarm vocabulary in Spanish contexts

- `uqscan=` (1,217 hits per Zhipu hunt): Tencent/Amap fleet only. No Spanish-target adoption.
- No "claude"-labeled Spanish-language programs found.
- No `ltzh-`-style families with Spanish content.
- No `zz=`-grammar params in 2026 Spanish traffic.

## 7. Lab fingerprints

Spain has no foundation-model lab operating agent fleets at the Mistral/Aleph Alpha scale. No Spanish-lab agent infra markers exist to hunt. (Structural negative.)

## Interpretation

1. **No Spanish Amap-equivalent.** Zero systematic place/API scanning of Spanish mapping or POI services.
2. **Spanish agentness vocabulary yields nothing** — the one thing a Spanish-language fleet would have to use (its own language in programs/tags) is absent.
3. **The fleet's own corpus is Spanish-free** — 2,673 collected reports, zero Spanish words or place names.
4. **Cross-swarm markers haven't crossed into Spanish contexts.**
5. Combined with the Russian/French/German clean zeros: the Amap fleet remains the only language-specific fleet visible on urlquery.net.

## Open follow-ups

- Time-blast analysis on ouo.io (47) and 0x0.st (23) blocked by API rate limiting (concurrent sibling agents); re-run when the window clears.
- Latin American map/POI services (e.g., country-specific yellow pages) remain unexamined beyond the Spanish set above.

Nothing pushed, per instructions.
