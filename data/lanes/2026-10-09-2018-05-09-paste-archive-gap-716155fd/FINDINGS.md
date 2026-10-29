# Findings

Grade claims OBSERVED, UPSTREAM, or INFERENCE.

## Body-save normalization (OBSERVED)

10 of the 54 new paste bodies were saved to disk with LF changed to CRLF.
The on-disk bytes did not match the manifest-recorded live-capture sha256.

Root cause: the save step wrote text with newline conversion. Proof: for
each of the 10, changing CRLF back to LF reproduces the recorded sha256
and size exactly. The records carry the reconstructed bytes, marked
`body_integrity: RECONSTRUCTED`. One paste (027713a7) recorded its hash
over CRLF bytes and went in as-is. One paste (d266bdde) has no recorded
hash, so its body was withheld and marked UNVERIFIED.

The same normalization hit pastes ingested by the transfer-test-family
lane (example: 6c3cbe0b, 691cd358). Their records still carry the
MISMATCH tag with the body withheld. A follow-up could rebuild those
bodies with the same verified method.

## Proxy-ladder split (OBSERVED)

The 89 ladder URLs are not all proxies. 79 are laundering-service
invocations (md.succ.ai x30, jqp.vercel.app x28, proxymule x7, and
others). 10 are direct www.sec.gov county.json fetches. They are the
ladder's final target, so they went in as `infra.ioc`, not
`infra.proxy_chain`.

## Skipped overlap (OBSERVED)

13 paste IDs were already in the corpus from the transfer-test-family
lane (006e1456, 01cfebfb, 3e9a2b38, 41e058fe, 691cd358, 6c3cbe0b,
875a96d0, 87e9328e, a26c0940, b3c39392, c1218392, c1d62d70, c40f39f3).
No duplicates were made.

## Records submitted

- 54 `infra.message` (anna.fyi pastes; 53 with verbatim body, 1 withheld)
- 79 `infra.proxy_chain` (laundering-service URLs)
- 10 `infra.ioc` (SEC fetch targets)
- 2 `source`, 1 `artifact` + 1 `web.capture` (joshuadavid revisions corpus)
