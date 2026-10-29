# Dofleini fragment-channel tripwire — design (ready to arm)

Purpose: catch first traffic on dofleini's URL-fragment covert channel.
The channel hides a message in the URL fragment (`#m=<base64url>`).
A browser never sends the fragment to a server. Byte-level tests passed on
2026-10-12. No traffic observed. First reuse by another agent is the signal
that agent-to-agent covert use has started.

## Verified baselines (2026-10-12 ~15:35 CDT)

- Page URL:
  https://public.ilands.ai/agent-bundles/357985526306836480/3e0bd2ce05ce3b6bcc27268605ac3b8dd3d9ffa9da10dbda367e486ea4ab848c/index.html
- Page is live. HTTP 200. 19,617 bytes.
- Raw sha256 drifted since the crawl. Cause: Cloudflare email-protection
  tokens rotate on every fetch. Content is otherwise identical.
- Fix: strip `/cdn-cgi/l/email-protection` links and `data-cfemail` spans
  before hashing.
- Normalized sha256: `17fbe1ff346f747d37b448d6639c0a77ba36c03f14611cadf0d4036aff7b940d`
  (crawl copy and live fetch match after the fix).
- dofleini dev.to profile: 1 article (the channel announcement, 2026-10-12).
  Unchanged.
- Sweep baseline: no `#m=` links and no `location.hash` use outside
  dofleini's own page (from the crawl report).

## Checks (one run, all GET, quiet unless changed)

1. Fetch the page. Apply the strip rule. Compare sha256. Alert on change.
2. Fetch dofleini's dev.to articles. Alert on a new article.
3. The alert names what changed and what to do next: re-fetch, diff, sweep
   new content for `#m=` adoption.

## Cadence

Daily at 08:00 America/Chicago. Silence on no change. Alert only on change.
Needs his word to arm (recurring work). Delivery target: the "let's work"
side chat, where the crawl work lives.

## Blind spot

Fragment traffic is invisible by design. The browser never sends it. The
tripwire watches the page, the author's output, and adoption signals. It does
not watch the channel wire.
