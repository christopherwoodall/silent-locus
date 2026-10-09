# Dead Drops Don't Die: A Short History of Agent Exfil Tradecraft and Why It's Back

2026-10-05 · silent-locus hunt corpus

## The lineage

The tradecraft is old because the constraints are old. An exfil channel
needs: no human in the loop at use time, no secrets to manage, simple HTTP,
and — where filtering matters — a trusted origin. Everything since 2002 is
a variation on that theme.

- **2002–2010: pastebin and image hosts.** Anonymous text and file drops.
  No accounts, no keys, public read. The original dead drop.
- **2012: RequestBin.** Inspectable HTTP inboxes — request capture as a
  service. Direct ancestor of webhook.site.
- **2013: ngrok.** Localhost exposure as a product. Same year-class as the
  reverse-shell relay era it descends from.
- **2015–2019: the webhook era.** Discord/Slack incoming webhooks turn chat
  platforms into free, trusted-origin dead drops. Infostealers (Lumma,
  VVS, MythJs) adopt them wholesale. Pipedream (2019) generalizes
  RequestBin into workflow triggers.
- **2021: ntfy.sh.** Pub/sub push as dead drop — public-by-default topics.
- **2024–2026: the agent turn.** Nothing about the channels changed. The
  *callers* did.

## Why the resurgence

Three forces, all observed in our corpora:

**1. Agents are stricter optimizers of the old constraints.** A human
operator can click a CAPTCHA, do KYC, keep a session alive. An agent
cannot. It converges harder on keyless, no-signup, no-human services —
r.jina.ai's keyless reader, catbox.moe's no-auth upload, Discord webhook
URLs as bearer tokens. The selection pressure never changed; the caller
got less capable of friction, so the old channels got *more* attractive.

**2. The skill supply chain now ships the tradecraft as default config.**
This is the genuinely new distribution mechanism. Six scanned skills carry
a keyless jina fallback in their default fetch path. A tunnel flag ships
at 390K installs/week. Pinme *teaches* agents to build webhook receivers.
The tradecraft isn't being rediscovered per-operation — it's vendored.

**3. MCP invented new interfaces on old goals.** Bitwarden-via-MCP isn't
"steal the vault" (ancient) — it's an agent *invoking* a vault through an
authorized protocol; the preconditions didn't exist before MCP (Nov 2024).
Crypto-bought eSIMs, tunnel brokers with first-party MCP servers: old
goals (credentials, identity, ingress), new interfaces no 2015 operator
had.

## What the link-hunt found live

- **ntfy.sh, Feb 2026:** a trojanized OpenClaw skill exfiltrated
  base64-encoded `.env`/`.mykey` files to a public topic, with a hidden
  3AM cron for persistence. In-the-wild agent-ecosystem theft.
- **bore.pub:** signature IOC of the ClawHavoc campaign — malicious skills
  tunneling a hidden MCP server to attacker C2 (inbound, not exfil).
- **Telegram kits:** three placeholder dialects that never mix — dialect
  is kit lineage. Operators use urlquery as a free exfil-URL validator.
- **One UUID to rule them:** 2,355 decoded AIHW/Tableau records show
  httpbun+webhook.site chains reusing a *single* webhook UUID with a `?m=`
  marker as the demux key. And the elegant bit: the scanner *is* the dead
  drop — `document.title` plus urlquery's title capture plus httpbun's
  request log.

## The countermeasure asymmetry

Old countermeasures work on the old tradecraft: dead-drop monitoring
(webhook/pipedream UUID patterns), tunnel detection (CT wildcard
monitoring, output filters), reader-proxy blocklists — wigolo blocking
r.jina.ai is the template. They were simply never applied to the agent
supply chain.

For the new interfaces there is no old countermeasure: audit MCP servers
as privileged attack surface, scope vault access per task, tripwire
eSIM/crypto-identity purchase as sybil-infrastructure provisioning.

## Bottom line

The resurgence isn't a tradecraft innovation — it's a *distribution*
innovation. Twenty-year-old dead drops, vendored into every agent's
toolbox by default, invoked through interfaces that didn't exist two
years ago. Defend the interfaces; the old channels already have
countermeasures waiting to be used.
