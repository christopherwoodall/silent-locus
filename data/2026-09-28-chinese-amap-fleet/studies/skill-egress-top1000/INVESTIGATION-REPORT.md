# The Skill Supply Chain Is the Tradecraft — Integrated Investigation Report

**2026-10-05 · silent-locus · BigSexyWarlock69's hunt**
**Scope:** agents and agent infrastructure only. Passive/public OSINT throughout.

This report integrates four completed investigations: the **top-1000 skill-egress scan**, the **why-these-sites** thesis test, the **deep link-hunt** (with corrections), and the **usemod.org ClipBoard** follow-up — plus the new **eval-questions corpus** built to feed future hunts.

---

## 1. The top-1000 scan

**Method:** exact replication of the top-500 study — same 16 GitHub Search queries (pages 2–10), same 7 marketplace lanes extended, same `egress_scan.py` unmodified, same taxonomy. Static scans of shallow clones; nothing installed or executed.

| | Top-500 | Extension (501–1000) | Combined |
|---|---|---|---|
| Skill identities | 358 | 655 | **1,013** |
| Repos/packages fetched | 177 | 260 | **437** |
| Skill units scanned | 3,853 | 2,490 | **6,343** |
| Units with egress hits | 800 | 741 | **1,541** |
| Raw hits (ext.) | — | 57,352 | — |

**Known-URL hunt (28 items): 17 confirmed, 11 absent.** The confirmations that matter:
- **whale-alert-monitor** ships the *complete runtime dead-drop grammar* — Discord + Slack + Telegram notifiers in one skill.
- **r.jina.ai runtime** in 2 more skills (6 total now) — keyless-fallback crawler, exact corpus tradecraft.
- **uploads.github.com runtime** release-asset upload code in 2 skills.
- **sci-hub.se runtime** as MCP tools (`download_scihub`) — the scanner *missed* it because the unit was scoped to a subdirectory. **Methodological finding: subdirectory-scoped units undercount.**

**New primitives (genuinely new to the taxonomy):** zread.ai (first jina-cousin relay, 3 skills); loca.lt taught as webhook-receiver path; R2 public buckets as no-auth asset hosts; Kleros IPFS gateway — **$0.01 USDC crypto-micropayment upload as a skill's canonical path**; YaoApp-yao's 8-provider messenger matrix (mailgun novel); **mcpagentmail.com — agent-to-agent email, 34 MCP tools**; API-key reseller routing with affiliate links; Tailscale tailnet endpoints. 6,088 novel domains total (volume-driven by mega-catalogs — multi-skill spread is the real signal).

**Consistent zeros:** webhook.site (docs only, no runtime POST code — twice now), httpbun, catbox.moe, epoch nonces, zz labels, A000-ZZEND. The corpus toolkit and the skill supply chain overlap *selectively*, not wholesale.

---

## 2. Why these sites — the thesis verdict

**BigSexyWarlock69's thesis: "11-year-old tradecraft — not new." Verdict: right about the exfil primitives, wrong about the interfaces.**

10 of 14 destinations grade **CONFIRMED-OLD** with real citations — some literally the same product lineage (RequestBin 2012 → Pipedream 2019). Agents converge on these sites for the same invariant reasons crimeware did: **no human in the loop at use time, keyless-or-preprovisioned credentials, simple HTTP, trusted origin where filtering matters.** An agent is a stricter optimizer of these constraints than a human operator — it can't click a CAPTCHA or do KYC. The selection pressure never changed; only the caller did.

**The carve-outs — all in the agent-invokable control plane:**
- **Bitwarden-via-MCP: ACTUALLY-NEW.** Not "steal the vault" (ancient) — an agent *invoking* a credential vault through an authorized tool protocol. Preconditions didn't exist before MCP (Nov 2024).
- **eSIM-via-crypto: PARTIALLY-NEW.** Burner-phone goal ancient; bit-only acquisition loop (crypto checkout → remote provisioning, no atoms moved) has no pre-2015 equivalent.
- **LocalCan: PARTIALLY-NEW.** Tunnels are 1995-old; a tunnel broker shipping a first-party MCP server "for AI agents" is not.
- **uploads.github.com: PARTIALLY-NEW.** Trusted-domain abuse is 2005-era; the attachment-pipeline-as-CDN specialization is newer.

**The resurgence isn't a tradecraft innovation — it's a distribution innovation.** Twenty-year-old dead drops, vendored into every agent's toolbox by default config, invoked through interfaces that didn't exist two years ago. (See `why-these-sites/TRADECRAFT-RESURGENCE.md` for the short version.)

---

## 3. The deep link-hunt — live material and honest corrections

**Confirmed live:**
- **ntfy.sh, Feb 2026:** trojanized OpenClaw skill exfiltrated base64 `.env`/`.mykey` files to a public topic, with a hidden 3AM cron for persistence. In-the-wild agent-ecosystem theft.
- **bore.pub:** signature IOC of the ClawHavoc campaign — malicious skills tunneling a hidden MCP server to attacker C2.
- **Telegram kits:** three placeholder dialects that never mix — dialect is kit lineage. Operators use urlquery as a free exfil-URL validator.
- **One UUID to rule them:** 2,355 decoded AIHW/Tableau records show httpbun+webhook.site chains reusing a *single* webhook UUID with a `?m=` marker as the demux key. The elegant bit: the scanner *is* the dead drop — `document.title` + urlquery's title capture + httpbun's request log.

**Four corrections applied 2026-10-05** (logged in `why-these-sites/CORRECTIONS-LOG.md`; original claims preserved verbatim inside the retractions):
1. **trycloudflare/DSQA attribution: WITHDRAWN.** False positive — "WHO" from a question collided case-insensitively with "who-visits" in a Facebook phishing path. Crimeware, not agent infrastructure.
2. **Pipedream `/ssh_` repetition: REFRAMED as observer-side.** Nine urlscan observations were rescans (incl. two urlhaus auto-submissions), endpoint answered HTTP 400. Watchlist-grade, not evidence-grade.
3. **`oai-` ngrok tunnel: investigator artifact,** not incident attribution — from a cloned wiki-agent demo, shallow-cloned into our own tree.
4. **Discord webhooks: six token-bearing records, not three.** The "evaluator corpus" file is a dead-drop hunt inventory, not benchmark output. Five were bare GET probes; one crimeware-shaped. No eval-run connection; tokens never validated or used.

---

## 4. The ClipBoard burst — verdict: LEAD, narrowed

usemod.org `WikiPatches/ClipBoard`: 6,848 anonymous edits from five OVH hosts over nine days (May 23–31, 2026), blank summaries, revisions purged, page reverted to the 2009 stub two minutes after the last edit.

The surviving revert diff showed the final content was **commodity pharma spam** (`mnsmiles.com/prednisone/`). Spam-bot is now the leading hypothesis — but the geometry (nine-day burst, five hosts, purge + revert) stays agent-shaped enough to hold as a LEAD. Wayback, Arquivo.pt, Common Crawl, and Wikiwix are exhausted: Wikiwix holds exactly one capture, created on demand 2026-10-05. Nobody outside our own notes has written about the burst. Full report: `german-french-swarm-hunt/clipboard-followup/CLIPBOARD-REPORT.md`.

---

## 5. New hunt surface: the eval-questions corpus

10,201 public eval questions banked from 11 evals (SimpleQA 4,326 → MLE-bench 82), each with topic tags, the domains an agent would likely visit answering it, and verbatim fingerprint phrases. 50 ranked hunt queries with concrete search strings per surface. **Greenfield:** the top-200 most distinctive fingerprints match zero files in our existing holdings — any future hit is novel signal. Corrections to prior notes: GAIA is now fully gated (not just test), HLE needs a terms click, BrowseComp/xbench-DeepSearch encrypted by design. (`collections/eval-questions/`)

---

## 6. Honest negatives (first-class)

- **EUROSWARM:** no German/French-locale swarm found; P(observing zero) ≈ 0.55–0.67 at DE/FR's AI share — zero was modal, not anomalous. DE/FR-operated English-task swarm on server-side APIs not ruled out.
- **Evaluator corpus:** no benchmark-output connection; dead-drop inventory, not eval data.
- **webhook.site/httpbun/catbox:** absent from the skill supply chain's runtime code twice running — the corpus toolkit and the skill chain overlap selectively.
- **Bitwarden-via-MCP / eSIM-via-crypto in the wild:** zero incident-corpus sightings. That absence is itself the tripwire.
- **ClipBoard archives:** all four public archives exhausted; the May 2026 revisions are unrecoverable from public sources.

---

## 7. What this means for defense

**Old countermeasures work for the old tradecraft** — they were just never applied to the agent supply chain: dead-drop monitoring (webhook/pipedream UUID patterns, webhook-URL entropy scanning in code), tunnel detection (CT-log wildcard monitoring, output filters), reader-proxy blocklists (copy the wigolo counter-pattern).

**For the new stuff there is no old countermeasure:** audit MCP servers as privileged attack surface, scope vault access per task, tripwire eSIM/crypto-identity purchase as sybil-infrastructure provisioning.

---

## 8. Still open

- **AI Village join:** the 2025-rows-vs-our-corpus URL overlap analysis. Dataset re-downloading now (gated HF access restored 2026-10-05); join runs when it lands. Prep (reference URL set, 2025 cutoff plan) is complete.
- **Pipedream `/ssh_` lead:** passive 7-day re-scan suggested, not executed; submitter identity unknown.
- **153 signal-positive repos** sit below the fetch cap — a third wave if warranted.
- **ua-burst-retry** collector still 429-bound; next run retries.

*Evidence rule held throughout: full observed values, never redacted; OBSERVED/INFERENCE separated. Corrections logged, not erased.*
