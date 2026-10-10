# Findings — anyrun-scan

Grade claims OBSERVED, UPSTREAM, or INFERENCE.

## Friction findings (OBSERVED)
- any.run TI Lookup and task submission both require a registered account.
  Unauthenticated API access returns 401.
- Registration rejects personal email addresses. Business email only, with
  manual human-in-the-loop verification for others.

## Viability (INFERENCE)
- any.run is not a viable hunt surface for rogue-agent eval traces. Ruled out
  on friction, not on content.
- The observed agent pattern favors zero-friction public surfaces (urlquery.net
  and arquivo.pt need no account to submit). A scale-optimizing eval harness
  would not route through a business-email gate plus manual approval when
  account-free alternatives are already in use.
- Not proof of absence: a motivated operator with a business email could still
  submit. The scan cannot proceed without an account we do not have.
