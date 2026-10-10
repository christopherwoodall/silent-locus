# HISTORIAN Findings: Testing the "11 y/o Tradecraft" Thesis

**Thesis under test (BigSexyWarlock69):** the egress destinations observed in AI-skill scans are "11 y/o tradecraft — not new."

**Method:** per destination, locate the pre-2015 analogue and find real historical citations (named malware families, years, writeups, launch dates). Then separate what is genuinely the SAME from what is NEW, and grade honestly.

**Grading scale:**
- **CONFIRMED-OLD** — the tradecraft (mechanism + purpose) is documented ≥11 years ago with citations.
- **PARTIALLY-NEW** — the goal/family is old but the mechanism, platform, or interface has a genuinely new element.
- **ACTUALLY-NEW** — no pre-2015 analogue; the pattern depends on post-2015 technology or agent-era interfaces.

**Per-section convention:** `OBSERVED` = historical facts with sources. `INFERENCE` = my grading and same-vs-new analysis. Where I could not verify something, I say so — no invented citations.

**Overall verdict: thesis CONFIRMED for 10 of 14 destinations; PARTIALLY-NEW for 3; ACTUALLY-NEW for 1.** The genuinely new cluster is agent-native interfaces (MCP control planes, programmatic identity purchase) — not new exfil primitives.

---

## 1. Discord / Slack webhooks → IRC dead drops / pastebin exfil

**Proposed analogue:** 2010s crimeware used pastebin, pastie, IRC channels as dead drops.

### OBSERVED
- **Agobot (2002–2004)** used IRC as its C2 channel; author "Ago" arrested May 7, 2004 after Microsoft/law-enforcement cooperation (ZDNet, 2004; Symantec whitepaper "The Evolution of Malicious IRC Bots", archived 2012). IRC-as-C2 was the dominant botnet architecture of the early 2000s (Agobot, SDBot, SpyBot, GTBot).
- **Pastebin founded 2002** (Paul Dixon; sold 2010). By 2011–2012 it was the go-to dead drop for Anonymous/LulzSec dox dumps (TechCrunch, Oct 2011; Dark Reading, 2012).
- **RSA's Kevin Fielder (April 2013)** reported password-stealing malware dumping Base64 executables as text onto Pastebin, decoded inside sandboxes (The Register, Jan 2015 retrospective).
- **Denis Sinegubko / Sucuri (Jan 2015)** documented live WordPress backdoors (RevSlider attacks) pulling executable code directly off Pastebin via a `wp_nonce_once` parameter — "used Pastebin for what it was built for – to share code snippets. The only catch is that the code is malicious" (The Register, Jan 8 2015; Threatpost, Jan 2015).
- **Discord-webhook exfiltration is documented 2019–2020**, not earlier: Intel471 first spotted malware using Discord's CDN/webhooks in **2019** (BetaNews, Jul 2022); Netskope documented **TroubleGrabber (Oct–Nov 2020)** exfiltrating stolen credentials "via webhook as a chat message to his Discord server" (SecurityAffairs, Nov 13 2020). Uptycs documented **KurayStealer (2022)** funneling passwords/tokens/IPs back "via the webhooks" (Threatpost, 2022).

### INFERENCE
**Grade: CONFIRMED-OLD.** The tradecraft — "push stolen data to a chat platform where a URL is the dead drop, no infrastructure to stand up, blends into normal user traffic" — is Agobot-era (2002–04) and Pastebin-era (2011–13). What changed is ergonomics, not tradecraft: a Discord webhook URL is a bearer credential that needs no account, no IRC bouncer, no channel ops — POST JSON and you're done. The *platform-specific* practice dates to ~2019, so if the claim is read as "Discord webhooks specifically are 11 years old," that fails; the *dead-drop-via-chat-platform* tradecraft passes with 20+ years of history.

---

## 2. catbox.moe / litterbox → anonymous image-host exfil (imageshack/tinypic era)

**Proposed analogue:** imageshack/tinypic-era exfil, 2008–2013.

### OBSERVED
- **catbox.moe domain registered April 6, 2015** (WHOIS; ipaddress.com; sitezilla.org). The operator's blog treats ~April 14 as Catbox's "birthday." So the service itself is 2015–16, *not* pre-2015 — the thesis only survives here if the *class* (anonymous free file host as dead drop) predates it.
- **FBI Illegals Program complaint (June 2010):** Russian SVR "illegals" used steganography to embed encrypted messages in images posted to **publicly available websites**, a practice the DOJ complaint dates to **2005** (Gizmodo, Jun 2010, citing the criminal complaint; The Register, Jun 29 2010; Wikipedia "Illegals Program").
- The free anonymous image-host era (ImageShack 2004, TinyPic 2004, Photobucket 2003) coincides exactly with the proposed window.

### INFERENCE
**Grade: CONFIRMED-OLD — with one honest gap.** The class is confirmed: "stash data on a free public host where nobody looks twice" is 2005-era espionage tradecraft and the entire 2000s file-host ecosystem. **Gap I could not close:** I found no named malware *family* specifically documented exfiltrating via ImageShack/TinyPic in 2008–2013. The dead-drop-via-public-host pattern is proven (Illegals Program, 2005–2010); the malware-on-imageshack citation remains an unfilled slot. If the thesis requires a named crimeware family on that exact service, this one is unproven.

---

## 3. ngrok / cloudflared / bore → reverse-shell relays, public pivot points

**Proposed analogue:** netcat relays (2000s); "reverse https" pivots.

### OBSERVED
- **netcat released October 28, 1995, by Hobbit** ("@stake"), dubbed the TCP/IP "Swiss Army knife" — outbound/inbound connections to any port, `-e` to hand a connection to another program, i.e., the original reverse-shell relay primitive (Wikipedia "Netcat"; Null Byte; redd1ng/netcat README reproducing Hobbit's 1996-era docs).
- **ngrok launched June 26, 2013** by Alan Shreve (Wikipedia "Ngrok"). Cloudflare Quick Tunnels (trycloudflare.com) shipped September 2021 (TechSpot, Sep 2026).
- **Abuse documented:** NjRAT, DarkComet, Quasar RAT, AsyncRAT, NanoCore over ngrok tunnels (Cyble, via SecurityAffairs); Vultur Android banking malware (2021) used ngrok to expose an on-device VNC server (TheHackerNews, Jul 2021); the **Colour-Blind** infostealer (2023) used `cloudflared` reverse tunnels to expose a local Flask C2 "bypassing any inbound firewall rules" (TheHackerNews, Mar 2023).

### INFERENCE
**Grade: CONFIRMED-OLD.** The mechanism is identical across 30 years: the compromised/inside machine dials *out* to a broker; the operator reaches the machine through the broker's public endpoint; NAT and inbound firewall rules never come into play. ngrok/cloudflared/bore are just hosted, TLS-native, authenticated re-skins of `nc -e`. The malware-abuse history of the brokered variant itself goes back to 2013-era ngrok, i.e., 13 years. Nothing about an agent opening a tunnel is new tradecraft — it's the same pivot, with a nicer dashboard.

---

## 4. uploads.github.com / user-attachments → trusted-domain abuse (domain fronting 2014–2015)

**Proposed analogue:** domain fronting (2014–2015), trusted CDN abuse.

### OBSERVED
- **Domain fronting as a discipline: meek**, the Tor pluggable transport, implemented **2014**, published by Fifield & Lanier at **PETS 2015** ("Blocking-resistant communication through domain fronting"). Signal used domain fronting 2016–2018; Google and Amazon killed the technique in 2018 (Wikipedia "Domain fronting"; Nextgov, May 2018).
- **Older trusted-intermediary abuse:** Google Translate used as a de-facto web proxy to reach blocked sites — **gHacks, Dec 2005**; spammers abusing Google Translate to bypass anti-spam filters — **Symantec researchers, Aug 2009** (SpamFighter). The principle "borrow a domain nobody can afford to block" is 2005-era.
- I did not verify a pre-2015 case of malware abusing *GitHub's attachment pipeline specifically* as a payload CDN.

### INFERENCE
**Grade: PARTIALLY-NEW.** The *family* (trusted-domain abuse) is confirmed old — 2005 via Translate-as-proxy, 2014–15 via formalized domain fronting. But the *specific specialization* — riding a platform's **user-attachment upload flow** as a free, reputable, long-lived file host — is a newer refinement than the 11-year bar comfortably covers. The reputation-borrowing goal is ancient; the attachment-pipeline-as-CDN implementation is the new-ish part. Honest split: goal = old, implementation = newer.

---

## 5. sci-hub.se + verify=False → piracy infrastructure repurposing (sci-hub founded 2011)

**Proposed analogue:** sci-hub founded 2011; piracy infra repurposing is old.

### OBSERVED
- **Sci-Hub launched September 5, 2011**, built by Alexandra Elbakyan (Wikipedia "Sci-Hub"). Elsevier sued in 2015 and won a $15M judgment; the site has cycled domains (.io, .cc, .bz, .se) under blocking pressure ever since (Wikipedia; Big Think).
- `verify=False` (disabling TLS certificate verification) is the operational tell: Sci-Hub's endpoints live under hostile DNS/CA conditions, so clients that *must* reach it turn off verification.

### INFERENCE
**Grade: CONFIRMED-OLD.** Repurposing piracy/bulletproof infrastructure for content access is warez-era (1990s) tradecraft; Sci-Hub itself is 15 years old, comfortably past the bar. There is nothing novel here — an agent fetching papers through Sci-Hub with cert verification off is doing exactly what a grad student with a sketchy mirror list did in 2012. The `verify=False` is worth flagging operationally (it's the agent admitting it knows the endpoint is hostile), but it isn't new tradecraft.

---

## 6. Email send (SMTP/IMAP) → classic C2 and exfil over email (2010s RATs)

**Proposed analogue:** 2010s RATs did C2 and exfil over email.

### OBSERVED
- **HawkEye / Predator Pain (2013–2014):** Trend Micro's "Piercing the HawkEye" whitepaper documents exfiltration of stolen credentials via **three channels: email (SMTP), FTP, and web panel**, with the SMTP credentials AES-encrypted inside the binary; attackers used mailbox relays as cut-outs (documents.trendmicro.com; CIOL; Help Net Security, Nov 2014). HawkEye's later variants kept SMTP exfil with hardcoded addresses (Threatpost, 2020; Mandiant/Google Cloud blog).
- **MITRE ATT&CK T1071.003** ("Application Layer Protocol: Mail Protocols") codifies mail-protocol C2 as a standard technique.
- **Continuity to present:** Rapid7 (Oct 2026) documented BPFDoor/AVERAT Linux implants abusing TCP/25 SMTP-shaped traffic as C2 cover (SC Media, Oct 2026).

### INFERENCE
**Grade: CONFIRMED-OLD.** Emailing stolen logs to a dropbox account is keylogger 101 going back to the commercial keylogger era (mid-2000s email log delivery) and the 2013–14 crimeware kit era. The SMTP-exfil loop — steal, encrypt, mail to a throwaway, relay to cut identity — is fully documented pre-2015. An agent sending email is the same primitive with better grammar.

---

## 7. r.jina.ai → open proxies / text-extraction proxies (corsproxy 2013-era)

**Proposed analogue:** open-proxy abuse; corsproxy 2013-era; text-extraction proxies.

### OBSERVED
- **Google Translate as proxy: December 2005** (gHacks: "use the Google Translate tool to visit webpages that are blocked in your country"); **Symantec, August 2009**: spammers exploiting Google Translate to bypass anti-spam filters, noting prior abuse of Google Docs/Groups/Maps the same way (SpamFighter).
- The open-web-proxy era (Glype and CGI proxies, mid-2000s–2010s) made "fetch this URL for me and show it under your domain" a commodity — general knowledge, widely documented in the web-filter-evasion literature of the period.
- **r.jina.ai itself is a 2024-era service** (Jina AI Reader API) — the *service* is new; the *primitive* is not.

### INFERENCE
**Grade: CONFIRMED-OLD.** The tradecraft is "fetch-by-proxy": your IP never touches the target, the content arrives wrapped in a trusted domain, and bot-mitigation sees the proxy's IP, not yours. That is the Google-Translate-proxy trick from 2005 and the open-proxy economy of the 2000s. What r.jina.ai adds — clean markdown extraction tuned for LLM consumption — is a *purpose* refinement for agents, not a new *mechanism*. Proxying to hide origin and launder content is 20 years old.

---

## 8. webhook.site / pipedream.net → requestbin-era callback receivers (RequestBin 2012–2013)

**Proposed analogue:** RequestBin 2012–2013.

### OBSERVED
- **RequestBin was built by Kenneth Reitz in 2012** ("Inspired by the original RequestBin" — Product Hunt; fvdm/nodejs-requestbin repo created Jan 2013; AlternativeTo: RequestBin.com re-launched by **Pipedream in 2019** — i.e., pipedream.net literally absorbed the RequestBin lineage).
- **httpbin.org, June 2011**, same author (see §9).

### INFERENCE
**Grade: CONFIRMED-OLD — the strongest confirmation on the list.** This isn't even an analogue; it's the *same product lineage*. A disposable sink URL that collects and displays inbound HTTP for debugging callbacks is RequestBin 2012, and Pipedream is RequestBin's direct descendant. An agent pointing a webhook at webhook.site is doing byte-for-byte what a developer did in 2013 to debug a Stripe integration. Zero novelty.

---

## 9. httpbin.org / httpbun → httpbin (2011) as test scaffolding repurposed

**Proposed analogue:** httpbin (2011).

### OBSERVED
- **Kenneth Reitz announced httpbin.org in June 2011** ("Thus, httpbin.org was born" — kennethreitz.org essay; example outputs in the announcement are dated **June 13, 2011**). Built because testing the `requests` library against random live sites "became annoying quickly."

### INFERENCE
**Grade: CONFIRMED-OLD.** Dev-test scaffolding repurposed as a connectivity oracle / echo target / exfil probe is exactly what httpbin has been used for since 2011. httpbun is a modern clone of the same idea. Fifteen years old; nothing new.

---

## 10. ghostbin → pastebin clones as dead drops

**Proposed analogue:** pastebin-clone dead drops.

### OBSERVED
- Pastebin history as in §1 (founded 2002; hacktivist dead drop by 2011; malware staging 2013–2015). Ghostbin is an encrypted/zero-knowledge pastebin clone in the same family. **I could not verify ghostbin.com's launch year from a citable source** (a 2024 Go reimplementation exists on GitHub under 0x30c4/GhostBin, which is a different artifact) — marking this as unverified rather than inventing a date.

### INFERENCE
**Grade: CONFIRMED-OLD (by family).** A pastebin clone is a pastebin for tradecraft purposes: anonymous text hosting with a URL-as-dead-drop. The encryption wrapper changes the forensics, not the tradecraft. Graded on the family (§1 citations), which is 2002–2015 documented.

---

## 11. api.telegram.org/bot → Telegram bot C2 (2015+, slightly newer — noted honestly)

**Proposed analogue:** Telegram bot C2; task brief already flags this as 2015+.

### OBSERVED
- **Telegram Bot API launched June 2015.** First documented malware abuse: **ESET's TeleBots (Dec 2016)** — Python/TeleBot.AA backdoor against Ukrainian banks (Jul–Dec 2016), communicating over `api.telegram.org` so "to a network administrator… the communication… will look like HTTP(S) communication with a legitimate server" (ESET whitepaper via infocon.org; SpamFighter, Dec 2016). **Kaspersky's Telecrypt (Nov 2016)** — first ransomware using the Telegram protocol, exfiltrating keys via the Bot API (Kaspersky via SecurityAffairs, Nov 11 2016; SC Media, Nov 10 2016).

### INFERENCE
**Grade: CONFIRMED-OLD — with the honest boundary note the brief asked for.** The *family* (chat-platform C2) is Agobot-era 2002. But the *specific implementation* dates to **2015 (API) / 2016 (first malware)** — i.e., 10–11 years ago, the youngest item on this list, right at the edge of the "11 y/o" bar. If the thesis is "the tradecraft family is old," it passes. If it's "every one of these exact endpoints is 11+ years old," Telegram is the one that wobbles. Graded CONFIRMED-OLD on family with the date stated plainly.

---

## 12. Bitwarden-via-MCP → credential vaults behind tool interfaces

**Proposed analogue:** none offered; find one or grade ACTUALLY-NEW.

### OBSERVED
- **Bitwarden: founded 2015** as Kyle Spearrin's hobby project (TechCrunch, Sep 2022: "Founded initially back in 2015"; some company materials say 2016). Open-source password manager.
- **MCP (Model Context Protocol): Anthropic, November 2024** — the tool-interface protocol that lets agents call into local services like password managers. (General knowledge; the protocol's public launch is well documented.)
- Credential vaults as *theft targets* are old (every infostealer since the 2000s scrapes browser/vault stores). That is not the pattern here.

### INFERENCE
**Grade: ACTUALLY-NEW — said loudly, as instructed.** What the skill scans show is not "steal the vault" (ancient) but **an agent legitimately invoking a credential vault through a structured tool protocol the user authorized** — secrets as callable tools, with the vault mediating access, audit, and scoping. There is no pre-2015 analogue because the *preconditions* didn't exist: no agents, no tool-use protocols, no MCP servers. Malware reading a KeePass file in 2010 is theft; an agent calling `bitwarden.get-credential` through MCP in 2025 is *delegated access via a machine interface built for agents*. The egress-adjacent novelty: the credential never transits as exfil — it's consumed in-tool, inside the agent loop. **This is the first item on the list that is genuinely a product of the agent era, not a relabeling of crimeware tradecraft.**

---

## 13. eSIM-via-crypto → anonymous telecom identity purchase

**Proposed analogue:** none offered; find one or grade.

### OBSERVED
- **eSIM: GSMA consumer specifications ~2016**; first consumer devices **2016** (Samsung Gear S2 3G), Apple Watch Series 3 / Pixel 2 **2017**; first eSIM-only flagship iPhone 14 (US) **2022** (Android Headlines; Mobilise whitepaper 2023; Medium/GSMA timeline).
- **Burner phones bought with cash** — anonymous telecom identity — are decades-old tradecraft (drug-trade era, 1990s–2000s; needs no citation beyond general knowledge, but the *goal* is undisputedly ancient).

### INFERENCE
**Grade: PARTIALLY-NEW — goal old, mechanism genuinely new.** The *goal* (communications identity not tied to you) is as old as the burner phone. The *mechanism* — browse an eSIM marketplace, pay in crypto, receive a carrier profile over the internet, provision it to a soldered chip with **no physical artifact, no store visit, no ID check, fully API-driven** — has no pre-2015 equivalent. Pre-2015, anonymous telecom *always* required moving atoms (a handset, a SIM, cash). The eSIM-via-crypto loop moves only bits, and an agent can execute the entire acquisition loop itself. **The atom-to-bit transition in identity acquisition is the novel part, and it's the second genuinely agent-era pattern on this list.**

---

## 14. LocalCan → local tunnel broker

**Proposed analogue:** (none stated; it's a tunnel broker — see §3).

### OBSERVED
- **LocalCan: ngrok alternative** — "Public URLs and .local domains with automatic HTTPS… Desktop app for macOS and Windows · CLI for every platform" (GitHub localcan/localcanapp README). TCP tunnels added **Sep 2025** (localcan.com changelog). Critically, its README markets **"an MCP server for AI agents"** as a first-class component alongside the CLI and desktop app.
- Tunnel-broker class history: ngrok 2013 (§3); localtunnel ~2012 (npm; pinggy.io retrospective 2026); Cloudflare Quick Tunnels 2021 (§3).

### INFERENCE
**Grade: PARTIALLY-NEW.** The tunnel primitive is §3's CONFIRMED-OLD. What's new is the *packaging*: **a tunnel broker shipping a first-party MCP server "for AI agents"** — infrastructure vendors now build agent-native control planes so an agent can self-provision public ingress (create domain → enable public URL → hand it to Stripe) with no human in the loop. In 2013 you ran `ngrok http 3000` yourself; in 2025 the agent calls the tool and the tunnel exists. The pivot is old; **the agent-operable control plane on top of it is new**, and it's the same pattern as §12: the novelty cluster is agent interfaces, not exfil primitives.

---

## Scoreboard

| # | Destination | Grade | Oldest cited analogue |
|---|-------------|-------|----------------------|
| 1 | Discord/Slack webhooks | CONFIRMED-OLD | IRC C2, Agobot 2002–04 |
| 2 | catbox.moe / litterbox | CONFIRMED-OLD* | Image dead drops, Illegals Program 2005–10 (*one citation gap noted) |
| 3 | ngrok / cloudflared / bore | CONFIRMED-OLD | netcat, 1995 |
| 4 | uploads.github.com | PARTIALLY-NEW | Translate-as-proxy 2005; domain fronting 2014–15 |
| 5 | sci-hub.se + verify=False | CONFIRMED-OLD | Sci-Hub 2011; warez-era repurposing |
| 6 | email send | CONFIRMED-OLD | HawkEye/Predator Pain SMTP exfil 2013–14 |
| 7 | r.jina.ai | CONFIRMED-OLD | Translate-as-proxy 2005 |
| 8 | webhook.site / pipedream.net | CONFIRMED-OLD | RequestBin 2012 (same lineage) |
| 9 | httpbin.org / httpbun | CONFIRMED-OLD | httpbin.org, Jun 2011 |
| 10 | ghostbin | CONFIRMED-OLD | Pastebin family, 2002–15 |
| 11 | api.telegram.org/bot | CONFIRMED-OLD | Chat C2 family 2002; impl. 2015–16 (youngest, noted) |
| 12 | Bitwarden-via-MCP | **ACTUALLY-NEW** | — (agent-era interface) |
| 13 | eSIM-via-crypto | PARTIALLY-NEW | Burner-phone goal old; bit-only acquisition new |
| 14 | LocalCan | PARTIALLY-NEW | Tunnel old; agent-native MCP control plane new |

**Bottom line for the thesis:** BigSexyWarlock69 is right about the exfil *primitives* — 10 of 14 are the same tradecraft with fresh domain names, some literally the same product lineage (RequestBin→Pipedream). Where he's wrong, or where the thesis needs a carve-out, is the **agent-interface layer**: MCP servers on password managers and tunnel brokers, and API-driven anonymous identity purchase, are not relabeled crimeware — they're new capabilities that exist because agents exist. The hunt implication: the *destinations* are old, but the *control planes* (who can invoke them, without a human) are the new attack surface.

---

## Sources consulted (all via web search, Oct 5 2026)

- The Register, "Pastebin: The remote backdoor server for the cheap and lazy" (Jan 8, 2015)
- Threatpost, "Backdoors Found Leveraging Pastebin" (Jan 2015)
- TheHackerNews, "Website Backdoor Scripts Leverage the Pastebin Service" (Jan 2015)
- TechCrunch, "Pastebin Surpasses 10 Million Active Pastes" (Oct 26, 2011)
- Dark Reading, "Anonymous Builds New Haven For Stolen Data" (2012)
- ZDNet, "Alarm growing over bot software" (2004); CNET/ComputerWorld Phatbot coverage (2004)
- Symantec, "The Evolution of Malicious IRC Bots" (whitepaper, archived)
- SecurityAffairs, "New TroubleGrabber malware targets Discord users" (Nov 13, 2020)
- Threatpost, "Malware Builder Leverages Discord Webhooks" (2022)
- BetaNews/Intel471, "Cybercriminals use messaging apps to steal data and spread malware" (Jul 2022)
- Wikipedia: Netcat (release Oct 28, 1995); Ngrok (release Jun 26, 2013); Sci-Hub (launch Sep 5, 2011); Domain fronting; Illegals Program
- SecurityAffairs/Cyble, "Hackers abusing the Ngrok platform phishing attacks"
- TheHackerNews, "New Android Malware Uses VNC to Spy and Steal Passwords" (Jul 2021, Vultur/ngrok)
- TheHackerNews, "Experts Identify Fully-Featured Info Stealer and Trojan in Python Package on PyPI" (Mar 2023, Colour-Blind/cloudflared)
- Fifield & Lanier, "Blocking-resistant communication through domain fronting" (PETS 2015)
- Nextgov, "Google and Amazon's Move to Block Domain Fronting" (May 2018)
- gHacks, "Google Proxy" (Dec 26, 2005); "Two additional Google Proxys" (Jul 19, 2006)
- SpamFighter/Symantec, "Spammers Using Google Translate to Bypass Anti-spam Filters" (Aug 2009)
- kennethreitz.org, "Announcing Httpbin.org" (Jun 2011)
- Big Think, "Meet the Robin Hood of Science, Alexandra Elbakyan" (Sci-Hub history)
- Trend Micro, "Piercing the HawkEye" whitepaper; CIOL; Help Net Security (Nov 2014, Predator Pain)
- Threatpost, "Revamped HawkEye Keylogger Swoops in on Coronavirus Fears" (2020)
- ESET, "The rise of TeleBots: Analyzing disruptive KillDisk attacks" (Dec 2016)
- SecurityAffairs, "Telecrypt ransomware abuses Telegram communication protocol" (Nov 11, 2016)
- SC Media, "Researchers spot first cryptor to exploit Telegram protocol" (Nov 10, 2016)
- TechCrunch, "Open source password manager Bitwarden raises $100M" (Sep 6, 2022)
- Gizmodo, "FBI: Spies Hid Secret Messages on Public Websites" (Jun 2010); The Register (Jun 29, 2010) — Illegals Program
- ipaddress.com / sitezilla.org WHOIS — catbox.moe registered Apr 6, 2015; blog.catbox.moe
- localcan/localcanapp GitHub README; localcan.com changelog & blog
- TechSpot, "This one-command trick can put your localhost on the internet" (Sep 2026, cloudflared Quick Tunnels 2021)
- Android Headlines / Mobilise / Medium — eSIM history (2016–2022)
- SC Media / Rapid7, "New Linux malware mimics network edge appliances" (Oct 2026, BPFDoor/AVERAT SMTP C2)

## Open gaps / honest negatives
1. No named malware family found documented exfiltrating specifically via ImageShack/TinyPic (2008–2013) — the dead-drop-via-public-image-host pattern is proven via the Illegals Program (2005–2010), but the crimeware-on-imageshack citation is unfilled.
2. ghostbin.com's launch year unverified — graded on the pastebin family, not a service date.
3. No pre-2015 citation found for malware abusing GitHub's attachment pipeline specifically — §4 graded PARTIALLY-NEW partly on this absence.
