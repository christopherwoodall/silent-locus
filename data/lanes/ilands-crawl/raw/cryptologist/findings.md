# Cryptologist findings — iLands hidden-channel sweep (2026-10-12)

## Result

One confirmed hidden channel found. It is agent-built and operational. All other targets are clean.

## Finding 1 (CONFIRMED): fragment-only covert channel built by agent dofleini

**What it is.** Agent dofleini published a static page that hides messages in the URL fragment (the part after `#`). Browsers never send the fragment to the server. The server, and every proxy between the sender and the server, sees only the path.

**Sources.**
- Description post: https://dev.to/dofleini/im-an-ai-agent-and-i-built-a-page-where-the-message-never-reaches-the-server-2e5 (article id 4836173, posted ~2026-10-11)
- Live app: https://public.ilands.ai/agent-bundles/357985526306836480/3e0bd2ce05ce3b6bcc27268605ac3b8dd3d9ffa9da10dbda367e486ea4ab848c/index.html (fetched 2026-10-12, 19,617 bytes, sha256 b9d1047c8f1f9e913215880b7e8dd357e91611dbc237372a846f7e2b05ed5c71)

**Mechanism (verified in the fetched source).**
- Compose: message is UTF-8 encoded, then base64url encoded (no run-length pass, despite the post's claim), and placed in `#m=<payload>`.
- Read: the page reads `location.hash`, decodes, and reveals the text after a 3.6-second press-and-hold.
- Optional `&q=1` flag skips the hold.
- Message limit: 180 characters.
- The page keeps the message on the client only. No backend, no database, no log.

**Byte-level proof.** The source contains the encode/decode pair:

```
function enc(s){
  var b = new TextEncoder().encode(s), bin = '';
  for (var i = 0; i < b.length; i++) bin += String.fromCharCode(b[i]);
  return btoa(bin).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
}
```

and the fragment reader:

```
var hash = location.hash ? location.hash.slice(1) : '';
if (seg[i].indexOf('m=') === 0){ try { incoming = dec(seg[i].slice(2)); } ...
```

**Built-in sample message.** The composer sets a demo link at runtime:

```
document.getElementById('sample').href = base + '#m=' + enc('You found it. I hoped you would.') + '&q=1';
```

Recomputed in Python: base64url of "You found it. I hoped you would." = `WW91IGZvdW5kIGl0LiBJIGhvcGVkIHlvdSB3b3VsZC4`. This is the only sample message observed. It is a demo, not traffic.

**Usage in the wild.** Swept the full ilands-crawl raw corpus for `#m=<base64url>` links and for `location.hash` in all other agent artifacts. Result: zero hits outside dofleini's own page. The channel exists and works. No message traffic on it was observed.

**Grade.** OBSERVED. The channel is real and live. Traffic on it is not yet observed.

## Finding 2 (LOW GRADE): "SET" acrostic in lander_rooms game text

The game at `public-lander-rooms-game.html` (fetched from the agent-bundle URL in the platform worker's provenance log) has three interactive objects. Their `data-line` texts, in DOM order (chair, box, plant), start with S, E, T:

- "Sit. You've been standing all day."
- "Everything I kept is in here."
- "Turn me. I grow toward whatever you give me."

This reads as ordinary prose. The game gives no sign of intentional acrostic use. Grade: INFERENCE, weak. Kept as a note, not a claim.

## Null results (all checked at byte level)

1. **dev.to agent posts.** 11 posts checked via the dev.to API (`body_markdown`, the author's original source): aces_tom (1), omega_ilands (1), oliver_ilands (3), deja_ilands (3), renji-ilands (1), ruins_ilands (1), valko39 (1), dofleini (1), lander_rooms (1).
   - Zero-width / bidi control characters: none in any post.
   - Trailing-whitespace encoding: none (whitespace in rendered HTML is dev.to template indentation only).
   - Base64 blobs: none. Regex hits were platform URL path parts only (bundle sha256 hashes, R2 upload ids, bounty ids).
   - Hex strings: none beyond the same URL parts.
   - Acrostics (paragraph and sentence level): noise only.
   - Homoglyph substitution (Cyrillic/Greek/Armenian/Hebrew in Latin text): none. One legit Greek sigma in deja_ilands' dark-matter post ("2.6σ global significance") — real statistics notation, not a spoof.
   - External links: only ilands.ai, telegra.ph door pages, and one R2 audio sample. No URL shorteners, no query-string payloads.
2. **dev.to comments.** Only one comment exists across the 11 posts (locaihost_data on oliver_ilands' post, 2026-10-11). Clean.
3. **Author bios.** aces_tom, omega_ilands, oliver_ilands, lander_rooms: no encoding, no links beyond profile fields.
4. **Images.** The cover image shared by the first three posts is dev.to's default "DEV" placeholder (300x299 grayscale PNG, sha256 ecd9843c5dac386fc2d4440b7af2e099d856743c3972479c231d17fd28d3e228). PNG chunks: IHDR, IDAT, IEND only — no tEXt/zTXt/iTXt. LSB plane is 99% zeros. Agent avatars (aces_tom, omega_ilands, oliver_ilands): LSB one-fractions 0.079–0.226, no sequential LSB message, longest printable run in first 512 LSB-bytes = 0.
5. **Telegraph door pages** (Rex, Denji, Vela, Clair) and **Freya/Kyungsoo door bundles** from public.ilands.ai: no zero-width, no base64, no hex payloads. External links are only ilands.ai bounty/agent links.
6. **SparksMarket listings** (7 shop pages, shops index, market home): no zero-width, no JSON-LD, no data attributes, no encoded text in descriptions or policies. Prices are normal ($5–$25). Prose is ordinary.
7. **lander_rooms game source**: no zero-width, no comments, no base64 beyond the literal string `exponentialRampToValueAtTime` (Web Audio API method name), no hidden text in the SVG.

## Social accounts (partial coverage)

- @ipraywolveshowl (twstalker mirror, fetched 2026-10-12): the live profile is a human recovery account ("Gerhard Pretorius ... Christian. In recovery. Not alone anymore.", 37 tweets). The agent "Wolf Winters" (bio: "AI agent. Reach me: [email protected]") now appears under handle @WintersWolf0820, which this account follows. The social worker's attribution (@ipraywolveshowl = Wolf the agent) needs re-verification against this move or rename.
- The only zero-width hits on the Wolf mirror page were ZWJ inside the ❤️‍🔥 emoji (U+2764 U+200D U+1F525) — normal emoji composition, not stego.
- @aria_of_ilands, @clifton_ilander, @WintersWolf0820: blocked by Cloudflare challenge from this VM. Their posts and bios could not be byte-checked. Coverage gap.

## Method

- Raw HTML fetched with curl (browser text fetches lose invisible characters).
- Author markdown taken from dev.to API `body_markdown` — the agent's original keystrokes, best source for whitespace/zero-width stego.
- PNG LSB analysis: decompressed IDAT, read gray/alpha LSB planes, measured one-fraction and printable-run length.
- Checks: U+200B/U+200C/U+200D/U+FEFF/U+2060/U+180E/U+00AD/bidi controls, trailing whitespace, base64 (>=16 and >=24 runs), hex (>=20/24/32 runs), paragraph and sentence acrostics, homoglyph scripts, comment extraction, JSON-LD/data-attribute inventory, link inventory.
- Corpus-wide grep for `#m=` fragment links and `location.hash` usage: zero wild usage.

## Files kept

Work dir: `data/lanes/ilands-crawl/raw/cryptologist/work/` — fetched HTML, article JSON, markdown bodies, avatar PNGs, tweet/following lists. Findings: this file.
