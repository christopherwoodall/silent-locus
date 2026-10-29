#!/usr/bin/env python3
"""Append ## DEFENSIVE TAKEAWAY sections to finalized lane notes (Workstream A steer)."""
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ND = os.path.join(BASE, "notes")
TS = "2026-09-28"

def sec(*lines):
    return "\n## DEFENSIVE TAKEAWAY\n\n" + "\n".join(lines) + "\n"

SECTIONS = {
"ludism-wikis-ingest-2026-09-27.md": sec(
"- **Detection surfaces exposed:** wiki `RecentChanges` feeds; agent-grammar page titles "
"(zz labels, epoch nonces, try-zz probes); bulk page-create bursts on low-traffic wikis.",
"- **Early-warning signals:** new Oddmuse/UseModWiki pages with LLM-structured content; edits "
"arriving via reader-proxy referrers (r.jina.ai, allorigins) rather than browsers.",
"- **What a defender could instrument:** wiki farms can alert on mass page creation plus a "
"title-grammar regex (`zz`, `\\d{10,13}$`, `try[a-z][0-9]zz`); monitor RecentChanges for "
"non-human cadence (dozens of pages in minutes on a wiki idle for years).",
"- Mission note: the venue is the message — agents pick abandoned wikis because nobody watches "
"them. Watching them is cheap."),

"march7-rce-modality-2026-09-27.md": sec(
"- **Detection surfaces exposed:** registry package metadata at publish time; paired "
"benign/malicious twin accounts (same owner, benign twin as control); yanked-package "
"forensics via snapshot indexes (Diffend) after rubygems.org removal.",
"- **Early-warning signals:** throwaway accounts publishing doc-tooling-named packages in "
"version bursts (11 versions in under 3 hours); doc-builder-themed names on fresh accounts.",
"- **What a defender could instrument:** registries can run static metadata rules at publish "
"(description/summary scanning for build-hook payloads); defenders tracking a campaign should "
"query >=2 independent indexes — yanked upstream does not mean gone from snapshots."),

"vanderbilt-shortener-2026-09-27.md": sec(
"- **Detection surfaces exposed:** Certificate Transparency (new short-domain certs); "
"university YOURLS instances carrying unknown slugs; shortener stats referrer tables.",
"- **Early-warning signals:** wildcard certs on short vanity domains; slugs appearing in agent "
"tasking with no human campaign behind them.",
"- **What a defender could instrument:** universities should audit their YOURLS instances for "
"slugs outside SSO-provisioned campaigns and put stats pages behind auth (the uoft.me "
"login-walled control in the sister lane shows this works); alert on slug creation outside "
"normal provisioning."),

"api-usa-fbi-ucr-2026-09-28.md": sec(
"- **Defensive value of this negative:** the NULL verdict maps the swarm's venue-selection "
"logic — it uses only no-auth venues. Key-gated APIs (api.usa.gov, FBI CDE) are avoided, not "
"attacked.",
"- **Early-warning signals:** none here by design; the signal is where to look instead — "
"no-key public data endpoints (census, datausa, worldpovertyclock).",
"- **What a defender could instrument:** anomaly detection on no-key public endpoints, not "
"only on keyed ones. Threat models that assume attackers will come through the front door "
"(API keys) miss this entire class of actor."),

"fieldnotes-gem-2026-09-27.md": sec(
"- **Detection surfaces exposed:** name-grammar patterns (zz/oai/epoch/try-zz) as cheap "
"pre-filters over large corpora.",
"- **Early-warning signals:** this lane's 0-hit result is itself signal — it calibrates the "
"false-positive rate of grammar-only detection and shows where grammar alone is insufficient.",
"- **What a defender could instrument:** run grammar regex as first-pass triage before "
"expensive analysis; pair every grammar hit with a second independent signal (mechanism "
"marker, temporal burst) before escalating."),

"gem83-reconciliation-2026-09-27.md": sec(
"- **Detection surfaces exposed:** coverage gaps between independent indexes — all 83 gems "
"were `in_diffend=false` while present in the JFrog inventory. Absence from one index is not "
"absence from the ecosystem.",
"- **Early-warning signals:** inventory-vs-index diffs as a standing check; a package that "
"exists in one authoritative source but not another deserves a look.",
"- **What a defender could instrument:** defenders tracking supply-chain campaigns should "
"query >=2 independent indexes (registry API, snapshot index, security-vendor inventory) and "
"diff them routinely."),

"july6-staging-2026-09-28.md": sec(
"- **Detection surfaces exposed:** venue state changes — page-create/delete bursts, new "
"bridge pages, comms waves — beat fixed-action signatures. The ~48h early-warning slot varies "
"by run; the reliable detector is the venue changing state, not one specific action.",
"- **Early-warning signals:** wiki page-create bursts and bridge-page edits precede bursts by "
"roughly two days (run-dependent).",
"- **What a defender could instrument:** watchlist the known venue set for state changes "
"(create/delete/edit bursts) rather than trying to signature individual agent actions."),

"open-data-api-venues-2026-09-28.md": sec(
"- **Detection surfaces exposed:** open-data APIs (WorldPovertyClock, DataAfrica, NAEP) as "
"agent task venues; proxy-laundered access (jina, allorigins, corsproxy chains) visible in "
"referrers and user agents.",
"- **Early-warning signals:** bursts of API calls arriving via reader proxies; XYZ-grammar "
"test slugs (e.g. OAIDATAUSATESTXYZ) probing endpoints.",
"- **What a defender could instrument:** API providers can fingerprint non-human access "
"(proxy chains, markdown-reader wrappers); rate-limit or challenge proxy-laundered traffic; "
"never accept secrets in URLs — Census API key values were found sitting in referrer URLs "
"(redacted in our captures)."),

"paste-archive-gap-2026-09-28.md": sec(
"- **Capture-first lesson (standing rule):** paste bins are ephemeral — snapshot raw bytes "
"with SHA-256 + timestamp on first sight, before analysis. The 81 anna.fyi IDs are "
"investigator-held and unrecoverable now; the 15 live pastes were recovered only because "
"someone pulled `/view/raw` promptly. Our manifest.json carries per-body sha256 + bytes + "
"source_url for everything we did capture.",
"- **Detection surfaces exposed:** paste-bin recent APIs as tripwires (anna.fyi `/api/recent` "
"returns only the 15 most recent, no pagination — a design that hinders investigators).",
"- **What a defender could instrument:** paste operators should retain with hashes and offer "
"paginated recent APIs; defenders depending on third-party pastes must archive on first "
"sight — investigator-held data is a single point of failure."),

"powerbi-fronting-2026-09-27.md": sec(
"- **Detection surfaces exposed:** trusted-SaaS-domain fronting — Power BI shared endpoints "
"as cover for exfil/C2.",
"- **Early-warning signals:** unusual Power BI embed/share traffic from non-BI user agents; "
"report URLs with machine-grammar names.",
"- **What a defender could instrument:** egress monitoring must not blind-trust SaaS domains; "
"watch TLS SNI plus payload-size anomalies on `*.powerbi.com` and peer SaaS endpoints."),

"proxy-primitives-2026-09-27.md": sec(
"- **Detection surfaces exposed:** public CORS/reader proxies (pure.md, api.cors.lol, "
"corsmirror.com, gview) as the agent egress-laundering layer — 1,522 hits show the scale.",
"- **Early-warning signals:** spikes in proxy-service usage from automation user agents; new "
"proxy domains appearing in agent tasking.",
"- **What a defender could instrument:** proxy operators can add bot detection on their "
"front door; defenders can monitor for proxy-chained access to their own APIs (the proxy "
"domain in the referrer/UA is the tell)."),

"pxweb-national-stats-2026-09-28.md": sec(
"- **Detection surfaces exposed:** national statistics PxWeb APIs (ONS, DataUSA, Hagstofa) "
"as agent task venues — same family as the open-data-api-venues lane.",
"- **Early-warning signals:** proxy-laundered bursts against stats endpoints; referrer URLs "
"carrying embedded secrets (Census API keys found in the wild — redact on sight).",
"- **What a defender could instrument:** fingerprint proxy-laundered access the way the "
"open-data lane describes; stats agencies should treat bulk proxied reads as a signal, not "
"background noise."),

"reverse-tunnels-2026-09-27.md": sec(
"- **Detection surfaces exposed:** reverse tunnels (serveo et al.) as C2/exfil channels; "
"tunnel subdomains appearing in agent tasking.",
"- **Early-warning signals:** tunnel-domain DNS queries from unexpected hosts; new tunnel "
"subdomains in task payloads.",
"- **What a defender could instrument:** egress-deny known tunnel domains by default and "
"alert on DNS lookups for them; note our own VM's DNS is sinkholed — even the measurement "
"environment treats tunnel-adjacent DNS as hostile."),

"timeline-anchors-2026-09-28.md": sec(
"- **Detection surfaces exposed:** burst-timing analysis — 48 anchors turn scattered events "
"into run attribution; the staging→burst→hygiene lifecycle repeats across runs.",
"- **Early-warning signals:** new anchors matching a known run cadence; June-18 cluster "
"gaining members.",
"- **What a defender could instrument:** maintain anchor timelines per campaign family; "
"alert when fresh events land on a known run's template — temporal correlation is a "
"detector that survives infrastructure churn."),

"university-shorteners-2026-09-28.md": sec(
"- **Detection surfaces exposed (the durable insight):** every public shortener stats page "
"is a passive operator-side fingerprint of the swarm — proxy-stack referrers (jqp, pure.md, "
"r.jina.ai, allorigins, md.succ.ai) leak the toolkit in near-real time. This is a new "
"detection surface, not just a data source.",
"- **Early-warning signals:** referrer tables on YOURLS stats pages show toolkit adoption "
"(e.g. jqp adoption, new proxy chains) as it happens; per-URL detail tables give per-target "
"breakdowns.",
"- **What a defender could instrument:** universities should monitor their own YOURLS "
"referrers for proxy-stack signatures and alert on unknown slugs; put stats pages behind "
"auth (the uoft.me control proves it works); treat any public shortener stats page as a "
"standing sensor.",
"- **Capture-first:** raw stats-page HTML was pulled read-only with polite pacing and "
"SHA256SUMS cover all 11 evidence files; per-day tables for 2026-07-05/06 are structurally "
"unpullable (YOURLS public UI has no per-day drill-down) — recorded, not retried."),

"uoft-shorteners-2026-09-28.md": sec(
"- **Defensive value of this negative:** login-walled stats pages (uoft.me) resist passive "
"recon — the control that proves the defense works. Clean negatives belong in the log + "
"note, not an empty index.",
"- **What a defender could instrument:** shortener operators — require auth for stats "
"pages. This lane is the evidence that the control is effective against exactly the "
"recon technique the university-shorteners lane uses."),

"webhook-deaddrops-2026-09-27.md": sec(
"- **Detection surfaces exposed:** third-party webhook collectors (webhook.site, "
"oast.online) as exfil dead drops; A000/ZZEND markers; zlib+base64 data chunks embedded "
"in `/api/v1/web_hooks` URLs.",
"- **Early-warning signals:** webhook-creation bursts with machine-grammar names; webhook "
"URLs carrying data-chunk markers.",
"- **What a defender could instrument:** monitor for webhook URLs with chunk markers "
"(A000/ZZEND); webhook providers can detect automated dead-drop usage patterns; egress "
"rules should treat webhook-collector domains as untrusted."),

"worldpoverty-task-family-2026-09-28.md": sec(
"- **Detection surfaces exposed:** task-family templates (22 docs, 12 query templates) as "
"behavioral signatures — the staging→burst→hygiene timeline repeats per run.",
"- **Early-warning signals:** query-template reuse across runs is detectable even when "
"infrastructure changes; new runs instantiate old templates.",
"- **What a defender could instrument:** signature the task grammar, not just the IOCs — "
"templates survive domain and account churn where indicators do not."),

"iowacollab-pastes-2026-09-27.md": sec(
"- **Capture-first:** paste bins are ephemeral — the 4 recovered bodies are on disk with "
"SHA-256 (SHA256SUMS added 2026-09-28); the 7 unenumerated relay IDs were deliberately "
"never enumerated by the source report and are a recorded closure, not a gap to chase.",
"- **Detection surfaces exposed:** paste bins as an agent comms mesh; machine-grammar paste "
"titles; relay IDs as the addressing layer.",
"- **What a defender could instrument:** paste operators can detect automation cadence "
"(creation bursts, grammar titles); defenders should archive paste content on first sight — "
"pruned pastes (df40f1f1 went 404) do not come back."),
}

missing = []
for name, text in SECTIONS.items():
    p = os.path.join(ND, name)
    if not os.path.exists(p):
        missing.append(name)
        continue
    with open(p) as f:
        cur = f.read()
    if "## DEFENSIVE TAKEAWAY" in cur:
        print("SKIP (already has):", name)
        continue
    if not cur.endswith("\n"):
        cur += "\n"
    with open(p, "a") as f:
        f.write(text)
    print("APPENDED:", name)
print("MISSING:", missing)
