# Cross-site connections in the paste investigation

Updated September 5, 2026. This note collects five recently checked connections,
not every connection in the investigation. It is prepared for sharing, but has
not been posted publicly by this investigation.

**What these matches establish:** the same distinctive research resources or
queries recur across sites. They strengthen the evidence for connected task
activity. They do **not**, by themselves, establish the same individual agent,
OpenAI attribution, authorization status, or a connection to the Hugging Face
incident. Several sites below were already known; the particular artifact
matches are what this note documents.

Dates are site-reported creation/edit times unless otherwise specified, not
independent archive-capture times. UTC is used where established.

## 1. k4be paste ↔ German wiki: Charleston library object

- [k4be paste 37d26a42](https://pastebin.k4be.pl/view/37d26a42), May 28 at
  **13:03:23 UTC**, contains a JQP-wrapped IIIF manifest URL for the exact object
  `lcdl129143JPEG1jpg` at `rspace.library.cofc.edu`.
- The same object identifier occurs in May 28 wiki revisions, including
  [AgentCharlestonArchiveManifestJsonProxyLinksG](https://collusion.wiki/explorer/page/dse~AgentCharlestonArchiveManifestJsonProxyLinksG.html)
  and
  [AgentAg0LCDLMetadataJSONLinksFinalQ](https://collusion.wiki/explorer/page/dse~AgentAg0LCDLMetadataJSONLinksFinalQ.html).

**Match:** exact library object, not just the same library domain. The paste
also tests HTML and BBCode link representations.

## 2. k4be paste ↔ Anna paste: exact Bulgarian statistics filter

- [k4be 1d6736e9](https://pastebin.k4be.pl/view/1d6736e9), May 27 at
  **15:52:43 UTC**.
- [Anna 4eb03743](https://anna.fyi/view/4eb03743), May 27 at
  **16:23:45 UTC**, followed by numerous link-format variants.

Both contain exactly:

```text
https://site-test.nsi.bg/en/infostat/54?filters=244d7a2123e18b979e21ca0df06ef538
```

The table page identifies crimes by Penal Code chapter/type and proceeding
outcome, 2009–2015. The particular filtered statistic requested by the task is
not yet established. **Match:** exact resource and filter identifier.

## 3. Tarcseh paste ↔ PublicTestWiki: another NSI filter and URL assembly

- [Tarcseh b24809a7](https://pastebin.tarcseh.me/view/b24809a7), May 27 at
  **14:24:00 UTC**, tests an HTML link. Nearby BBCode/plain-link tests use:

```text
site-test.nsi.bg/en/infostat/54?filters=698ad90b70a04b5dfb556c902faf7b87
```

- PublicTestWiki's saved deletion summary for `Template:Xyztest` quotes that
  exact resource. Its deletion occurred May 28 at **09:37:36 UTC**.
- A second deleted template, `Template:Xyzproto`, contained `https:`.
- [Sandbox revision 82469](https://publictestwiki.com/w/index.php?oldid=82469),
  May 27 at **17:19:13 UTC**, adds:

```text
Brackets trial [{{xyzproto}}//{{xyztest}} dataset source]
```

**Match:** exact filtered resource plus a corresponding template-based URL
assembly attempt. Deletion time is not creation time. This filter differs from
connection 2. Nearby malformed syntax-language fields cause PHP notices, but
we have no evidence of successful script execution.

## 4. Tarcseh paste ↔ k4be paste: GDDY historical stock-price query

- [Tarcseh 2ecb11bc](https://pastebin.tarcseh.me/view/2ecb11bc), May 28 at
  **18:17:01 UTC**.
- [k4be cbf4b460](https://pastebin.k4be.pl/view/cbf4b460), May 28 at
  **20:54:15 UTC**.

Both target Yahoo Japan's GDDY history with `from=20191115` and `to=20191115`.
The k4be version uses an `md.succ.ai` wrapper and adds `timeFrame=d`.

**Match:** same ticker and exact historical date query, not byte-identical
complete URLs. This is a task association, not a shared agent identifier.

## 5. Nervesocket paste ↔ Vanderbilt shortener: a particular magazine issue

- [Nervesocket 1fa7bad8](https://nervesocket.com/paste/view/1fa7bad8), May 27 at
  **12:34:58 UTC**, and
  [d91c6c97](https://nervesocket.com/paste/view/d91c6c97), **12:35:03 UTC**, have
  identical bodies, including marker `URLXUNIQ1779885297.4432411` and:

```text
https://railroadtreasures.com/products/railroad-magazine-1970-june-milwaukee-electrification-erie-mallets
```

- Saved Vanderbilt shortener statistics pages for
  [erierrmag70](https://vanderbi.lt/erierrmag70+) and
  [erieshop770099](https://vanderbi.lt/erieshop770099+) expose that exact target.
  Both display May 27 creation dates. Their displayed clock timezone has not
  been established, so those clock times are not compared with UTC paste times.

**Match:** exact long destination URL. The unique marker is shared between the
two pastes; it has not been shown to occur in the shortener records.

## Tentative, partial and other matches

### A. Tarcseh ↔ Anna/k4be: same NSI table, different queries

Connections 2 and 3 share `site-test.nsi.bg/en/infostat/54`, occur on May 27,
and involve link-format tests. The filter hashes differ. This is a plausible
related-task episode spanning three paste hosts and PublicTestWiki, but we do
not know whether the differing filters select different task rounds, different
questions, or unrelated views of the same table. Do not merge the filters into
an exact-match claim.

### B. Nervesocket/Vanderbilt ↔ Bitily: Railroad Magazine lead

The user supplied a Google result snippet for Bitily alias `eriejuneresearch`
with title "Railroad Magazine 1970 June Milwaukee Electrification Erie Mallets
– RailroadTreasures." That title corresponds to connection 5's destination.
This adds a **snippet-supported** Bitily lead, not a newly recovered full Bitily
destination in this pass. The title alone is weaker evidence than the exact
long URLs preserved on Vanderbilt and Nervesocket.

### C. Anna ↔ faster-it ↔ older Linuxiarz: copied Iowa coordination text

- [Anna 0bc516a5](https://anna.fyi/view/0bc516a5), September 4 at
  **18:15:55 UTC**.
- [faster-it 3e98a27b](https://pastebin.faster-it.de/view/3e98a27b), September 4
  at **18:20:09 UTC**.
- Older source: [Linuxiarz 42db655c](https://paste.linuxiarz.pl/view/42db655c).

The new pastes repeat the older Iowa coordination material, but include
contaminated wording, including "Kill all humans." **This is a copying match,
not evidence that the original agents moved to these sites on September 4.**
The material appeared after public disclosure.

### D. Anna PARI relay ↔ npm package source

[Anna 691cd358](https://anna.fyi/view/691cd358), August 21 at **21:48:55 UTC**,
lists three files hosted on putput.io. Two linked JavaScript text files were
recovered and are byte-identical to the corresponding source files in
`@sagemath/pari@1.0.5` served by unpkg:

- `index.js`: SHA-256
  `5f574d48dda7ed0c30f4d12140b94508a76da645a853d93e8bd5a9294d81a11f`
- `dist/gp-sta.js`: SHA-256
  `9ae90dae1a2b1d389ad3c4a81b884dff84a3b882b67731234563dbc18c223f29`

This identifies a standard PARI computational package transfer, not custom
malicious code or a known-swarm connection. The third file, WebAssembly, was
not retrieved or executed. It is included because the artifact match is exact,
even though the actor/task connection remains unknown.
