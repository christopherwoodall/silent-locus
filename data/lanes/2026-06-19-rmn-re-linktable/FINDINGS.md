# Findings

One shortlink observation, grade OBSERVED throughout.

## The shortlink

- Short URL: `https://rmn.re/masscounty1781813461d`
- Destination: `https://cors.bwa.workers.dev/www.sec.gov/files/county.json`
- Clicks recorded: 53
- Link status: preserved
- Slug grammar: epoch (`masscounty1781813461d` follows the
  `<word>county<digits>d` epoch grammar shape)

OBSERVED: the shortlink and destination exist in the source document.
Record: `observation_a35b28355da349c79ffc0bacd8fe282a`.

## The slug marker

- Term: `masscounty1781813461d`
- Category: marker. Status: active.
- The slug is a searchable marker term. It is not an internal ID.

OBSERVED: the slug is the actual shortlink identifier from the source.
Record: `observation_6c986b60dd8d4eaa8862f8b34ead0c9a`.

## Proxy wrapper

The destination routes through the `cors.bwa.workers.dev` CORS proxy
wrapper. This is recorded as a tag on the shortcut record, not as a
separate proxy observation: no agent traffic through the proxy was
observed, only the wrapped target URL.

## What is not claimed

No claim is made about who created the shortlink, when it was created
beyond the ES `@timestamp`, or whether the destination was live. The
`creator_ip16` value `4.255` is a truncated /16 kept as a tag only.
