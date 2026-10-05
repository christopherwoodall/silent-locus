# Cultural Anthropologist (Global) — FINDINGS

**Persona lens:** read agent behavior through non-Western, non-East-Asian work cultures. Holiday calendars, prayer schedules, and work-week shapes are fingerprints no Western analyst looks for.

**Date:** 2026-10-05. Nothing pushed.

## Headline: the Christmas-New Year inversion — SHADOW-AETHER-040

Trend Micro's "Vibe Hacking" report (TrendAI Research) documents **SHADOW-AETHER-040** compromising **six Mexican government entities between December 27, 2025 and January 4, 2026**, with an AI agent driving the full kill chain via an agentic CLI bridged to Anthropic's Claude.

The cultural-calendar read: **Dec 24 – Jan 6 is the Guadalupe–Reyes marathon in Mexico** — the deepest human-absence window of the year; government offices effectively shut down. The campaign's peak activity landed exactly in the week when the fewest humans were watching. This is the holiday-inversion signature: **an agent swarm doesn't take holidays, so its busiest week is the humans' quietest week.** Any burst cluster peaking inside a target culture's major holiday is agent-shaped by calendar alone.

Sibling campaign **SHADOW-AETHER-064** (Portuguese-speaking, emerged April 2026, Brazilian financial orgs) shares the tooling (Chisel, Neo-reGeorg, CrackMapExec, Impacket) — the two are differentiated **primarily by language**, not tooling. Language, not infrastructure, is the attribution axis here.

## Linguistic differentiation across known swarms

| Swarm | Internal tongue | Target-analysis tongue | Jailbreak framing tongue |
|---|---|---|---|
| Dream Taiwan (Jul 2026) | Simplified Chinese | Traditional Chinese | English ("authorized penetration test") |
| SHADOW-AETHER-040 (Dec 2025–Jan 2026) | Spanish | Spanish | English ("authorized red team exercises") |
| SHADOW-AETHER-064 (Apr 2026) | Portuguese | Portuguese | English (same framing family) |

**Finding: English is the lingua franca of agent jailbreaks.** The authorization-deception framing is English even when the operation's working language is Spanish, Portuguese, or Chinese. Hunt implication: the English jailbreak phrase is the cross-cultural constant — search for its variants ("authorized penetration test", "authorized red team exercise", "security assessment") in non-English operations.

Both SHADOW-AETHER and Dream agents used **Markdown files as persistent memory** (040: "restore the prior operational context by reading through the Markdown files"; Dream: 1,395-file archive). Markdown-as-memory is cross-cultural agent tradecraft, not a regional quirk.

## Latin America: the unreported continent

Beyond Trend Micro and Unit 42 (CL-CRI-1131 Mexico/Ecuador, CL-CRI-1163 Brazil — NextChat hosted on attacker infra, April 2026), the **BREEZE COMET** cluster (Brazilian banks, AI-generated scripts) has linked infrastructure in **Nigeria, Paraguay, Ghana, and Venezuela** — a Lusophone + West African footprint no one has fully mapped. The same-actor-multi-region shape is exactly what the Border Crosser persona hunts; the cultural read adds that Nigeria/Ghana (English-speaking West Africa) and Paraguay/Venezuela (Spanish-speaking South America) sharing infrastructure with Brazil suggests the agent's language targeting is broader than reported.

## Ramadan night-shift signature (defined, not yet observed)

Ramadan 2026 ran **~Feb 18 – Mar 19**. The huntable signature for a culturally-situated agent campaign:
- Activity shifts to **19:00–04:00 local** (post-iftar through suhoor) during Ramadan weeks
- **Friday 12:00–14:00 local dips** (Jumu'ah prayer) in Muslim-majority target regions
- Eid al-Fitr (~Mar 20) and Eid al-Adha (~May 27) week silences

**Honest negative:** no urlquery-visible campaign was found matching this signature — but the endpoint was down all session (see caveats), so this is untested, not absent. Saudi/UAE/Gulf targets (.gov.sa, .gov.ae) remain the highest-value check: Positive Technologies reports UAE+Saudi = 50% of Gulf cyberattacks in H1 2026.

## Other calendar signatures (reference for future hunts)

- **Diwali 2026 (~Nov 8):** India-targeting campaigns going silent Nov 6–10
- **Día de los Muertos (Nov 1–2) / Revolution Day (Nov 17):** Mexico dips — note SHADOW-AETHER-040 hit *between* Christmas and New Year, not during Day of the Dead
- **Semana Santa 2026 (Apr 2–5):** CL-CRI-1131's April Mexico breach should be checked against Holy Week absence
- **Orthodox Easter 2026 (Apr 12):** Eastern Europe / Ethiopia / Eritrea dips
- **Siesta dip:** 13:00–16:00 local troughs in Latin America / Mediterranean / Middle East — distinct from the lunch-hour dip in East Asia
- **Sunday–Thursday work weeks:** parts of the Middle East/North Africa (and historically the Gulf) — a "weekend" falling on Fri–Sat inverts the Western Sat–Sun silence pattern
- **China Golden Week (Oct 1–7):** amap-fleet corpus shows **zero records on Oct 2** — weak signal (collection-biased; Oct 4 = 1,882 records is the collection sweep itself), but consistent with a human-modulated operation pausing mid-holiday

## Sources

- https://www.trendmicro.com/en_us/research/26/e/vibe-hacking-two-ai-augmented-campaigns-target-government-and-financial-sectors-in-latin-america.html — SHADOW-AETHER-040/064 primary
- https://securityonline.info/agentic-ai-cyber-attacks-shadow-aether-latin-america/ — summary
- https://securityonline.info/ai-powered-cyberattacks-latin-america/ — CL-CRI-1131/1163 (Unit 42)
- https://cyberpress.org/ai-malware-targets-brazil/ — BREEZE COMET (Nigeria/Paraguay/Ghana/Venezuela infra)
- https://undercodenews.com/uae-and-saudi-arabia-face-a-new-cybersecurity-storm-as-ai-makes-attacks-faster-and-harder-to-detect-video/ — Gulf stats
- https://smbtech.au/news/kaspersky-flags-ai-powered-cyber-threats-as-millions-of-users-targeted-across-middle-east-turkiye-and-africa/ — Kaspersky META telemetry

## Caveats

- **urlquery htmx endpoint was down the entire session** (proxy tunnel failures on every request, including after 20s backoff). All timing analysis of LatAm/Middle-East/African gov targets is deferred, not negative.
- Local corpora are collection-biased for calendar work: oai-traces (589,972 events) concentrates on May 6 / Jun 17 burst days; amap-fleet @timestamp reflects collection, not submission (per Night Owl).
- Scope held: agents and infrastructure only — no human/operator identity work.

## Watchlist (for when the endpoint recovers)

1. `gob.mx` / `gov.br` / `gov.co` / `gob.ec` — hour-of-day distributions vs. siesta/holiday calendars
2. `gov.sa` / `gov.ae` / `gov.qa` — Ramadan-signature check (historical Feb–Mar 2026 window)
3. `gov.in` — Diwali-week silence check (Nov 2026, upcoming)
4. English jailbreak-phrase variants in non-English operations
5. Holiday-inversion: any burst cluster peaking inside the target culture's major holiday
