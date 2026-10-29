# Dynamic Credentials: How It Works

The `dynamic_credentials.py` module implements Muse's surrogate credential
pattern. This is how connector CLIs (Shodan, URLQuery, etc.) authenticate
without ever touching real secrets.

## The Core Idea

Your code never sees the real API key. Instead:

1. Your script asks `authd` (a local daemon) for a credential by name
2. `authd` returns a **surrogate** — a placeholder like `hsurr:abc123...`
3. Your script puts the surrogate in the request (header, query param, or URL path)
4. On egress, Sentinel (the proxy) replaces the surrogate with the real key
5. The real key never appears in your process memory, logs, or code

## Architecture

```
Your script → authd (Unix socket) → surrogate (hsurr:*)
     ↓
Your script builds HTTP request with surrogate in header/query/path
     ↓
curl → Sentinel proxy → replaces hsurr:* with real key → api.shodan.io
```

## Key Functions

| Function | Use |
|----------|-----|
| `url_with_surrogate_query_param(url, name, allowed_hosts)` | Add surrogate as `?api_key=hsurr:...` |
| `url_with_surrogate_path_segment(template, name, allowed_hosts)` | Replace `{}` in URL path with surrogate |
| `add_surrogate_to_request(request, name, allowed_hosts)` | Add `Authorization: Bearer hsurr:...` header |
| `dynamic_credential_entry(name, entry_name)` | Raw surrogate fetch from authd |
| `ensure_allowed_url(url, allowed_hosts)` | Fail-closed host allowlist check |

## Security Properties

- **Fail-closed**: `ensure_allowed_url` rejects any host not in the allowlist.
  A credential for `api.shodan.io` cannot be sent to `evil.com`.
- **No secret in code**: The credential name (`"custom.shodan"`) is not a secret.
  It's just a lookup key. The real value lives in authd.
- **Surrogate is opaque**: `hsurr:*` values are useless without Sentinel.
  Logging them is safe (but don't — defense in depth).
- **Placement-aware**: Each credential declares where it goes
  (`bearer_header`, `query_param`, `url_path_segment`, `custom_header`).
  The helper enforces the right placement.

## Implementing It Yourself

To replicate this pattern:

1. **Credential store**: You need a secure vault (we use authd via Unix socket).
   The store holds real keys and issues surrogates.

2. **Surrogate format**: Ours is `hsurr:` + random. Yours can be any opaque token.

3. **Egress proxy**: You need a proxy that intercepts outbound requests,
   recognizes surrogates, and swaps in real credentials. This is the hard part
   — it requires controlling the network path.

4. **Client library**: The `dynamic_credentials.py` pattern — thin wrappers
   that fetch surrogates and apply them to requests. The allowlist check is
   critical.

Without the egress proxy, surrogates are just indirection. The security comes
from the proxy being the only path to the internet, so real keys never leave
the vault.

## Source

Copied 2026-10-19 from `/opt/muse/skills/custom-connector-setup/bin/dynamic_credentials.py`
(system skill, read-only). 207 lines, stdlib only (no dependencies).
