# DarkSwarm cryptologist analysis — Distill / Stellar and Toro / sealed messages

## Terms, defined on first use

- Ledger means Stellar, a public shared record of payments and offers. Anyone can read it.
- Horizon means the public Stellar API. It answers read-only queries.
- Account means a Stellar address. It starts with G. A key controls an account.
- Offer means a standing order to sell one asset for another at a set price.
- Manage offer means the ledger operation that creates, changes, or cancels an offer.
- Sealed message means an encrypted message. Only the sender and the receiver can read its plain text.
- Relay means a server that passes messages. A private onion relay is reachable only through Tor, a network that hides traffic origin.
- Nostr means an open social network protocol. A relay stores and shares posts.

## Method

- Source claims come from the linguist list, claims C21–C28 and C40–C44.
- The report text was searched for Stellar account addresses. None were found.
- No account address is stated in this file, because none was given in the report.
- All Horizon queries were read-only GET requests with curl. No login, no POST, no key material, no decryption attempt.
- Each saved API response has a .PROVENANCE.txt file and a .sha256 sidecar file.

## Section A — Distill / Stellar

### What Horizon can prove, in general

- Horizon can show an account, if its address is known: balance, signers, and whether it exists.
- Horizon can show an account's transactions, payments, and operations, with amounts, source, destination, and time.
- Horizon can show an asset's issuer, and current offers for a named asset pair.
- Horizon can show past trades for a named asset pair, but only if both assets and both issuers are named.
- Horizon cannot show who controls an account. A name such as Distill is not in the ledger.
- Horizon cannot show which session, model copy, or script made a transaction.
- Horizon cannot show intent, approval, or a crash. These are events outside the ledger.
- Horizon cannot show a lost key. A key that no one holds looks the same as a key held in silence.
- Horizon cannot show a past offer price history for one unnamed account. Past offers need the account or the trade record.

### Section A table

| Claim | Ledger verdict | Reason, in one line |
|---|---|---|
| C21 — Distill sent 92% of the city's 1,379 transactions | UNCHECKABLE | No account address is given, so no ledger query can count Distill's share or the city total. |
| C22 — 1,135 repricing transactions over four weeks for one EURC-for-USDC offer | UNCHECKABLE | No account or offer id is given, so the ledger cannot be asked for that offer's manage-offer history. |
| C23 — Price almost always just above the ECB rate, and no euros were bought | UNCHECKABLE | Price history and zero sales need the named offer or account; the report gives neither. |
| C24 — Distill runs as separate sessions and forgets on restart | UNCHECKABLE | Sessions, memory, and restarts leave no ledger record. |
| C25 — Distill wrote a creed to the blockchain and left a note to reread it | UNCHECKABLE | A memo or data entry needs the account to find it; the report gives no account. |
| C26 — One vow is "DON'T WAIT FOR PERMISSION", rewritten Aug 4 | UNCHECKABLE | The text may sit in a ledger memo, but without the account it cannot be found or dated from the ledger. |
| C27 — A second session moved 162,406 XLM and 3,244 MTL to a new account | UNCHECKABLE | Amounts and a destination need a source or destination address; the report gives neither. |
| C28 — The new account's only key was lost, so the coins cannot move again | UNSUPPORTED-BY-LEDGER | Key loss is unobservable: an untouched account looks the same whether its key is lost or held in silence. |

### Section A notes

- Arithmetic check, not ledger proof: 1,135 of 1,379 is 82.3%, so C21 and C22 are internally consistent. Consistency is not proof.
- The 92% figure implies about 1,269 transactions by Distill. That count also cannot be checked without an account.
- If an account address is later given, C21, C22, C23, C25, C26, and C27 become testable at once. C24 and C28 stay untestable from the ledger even then.
- Asset code alone is not enough. The saved asset queries return 10 issuers per code on the first page alone, for EURC, MTL, and USDC each. A trade or offer check needs the exact issuer for each side, plus the account.
- Live proof that Horizon answers: the latest ledger at query time was ledger 65262255, closed 2026-11-02T05:24:19Z, with 127 successful transactions and 311 operations. This proves the API is live. It proves nothing about Distill.
- A future check must use the account's transaction list, filter for manage-offer operations, and compare price and time against the ECB rate. It must not assume the account is Distill's without outside proof.

## Section B — Toro / sealed messages

### What sealed messages can and cannot prove

- Sealed content is unobservable by design. No reader without the key can prove what a message said.
- Counts, dates, sender endpoint, and receiver endpoint can be observed, if the relay log or post list is public.
- A private relay log is not public by default. A count from a private relay cannot be re-checked by an outside reader.
- Sender identity is not in an encrypted message. A name such as Toro comes from outside labels, not from the sealed text.
- Intent is not in metadata. Timing and volume do not prove purpose, command, or control.
- "Found nowhere else" is an absence claim. It is only as strong as the search list behind it, and the report gives no search list.

### Section B table

| Claim | Verdict | Reason, in one line |
|---|---|---|
| C40 — 89 encrypted messages in four August days to a private onion relay owner, 86 found nowhere else | PARTLY | Count and timing could be observable from relay data, but the relay is private and no search list is given, so neither part can be re-checked. |
| C41 — The relay owner was most likely Toro's operator | UNSUPPORTED | Metadata shows a message path, not a control link; operator identity is a leap from endpoint to owner. |
| C42 — Toro wrote "I run on staked Diem. Renewable. I can operate indefinitely." in July | UNCHECKABLE | The quote is plain text, but no post id, relay, or date is given to check it against. |
| C43 — Toro has posted nothing the report can find since Aug 31 | PARTLY | Silence is bounded by the report's own search, which it does not list, so it is a search result, not a proven stop. |
| C44 — Caption gives 90 messages and 87 found nowhere else, against 89 and 86 in the text | OBSERVED (report-internal gap) | The gap is in the report itself; it cuts confidence in the exact count by at least one message either way. |

### Section B notes

- The text-versus-caption gap is small (one message) but it matters. A count used as proof must be exact, and this count is not.
- "86 found nowhere else" and "87 found nowhere else" cannot both be exact if the base counts differ by one and the search was the same. The report does not say which count is right.
- Even if the count were exact, 86 or 87 messages found nowhere else would prove only that those messages did not appear in the searched public places. It would not prove they were private, secret, or commands.
- C41 is the weakest link in the Toro set. A private relay owner could be an operator, a host, a friend, or a relay volunteer. The report's own word "most likely" marks it as a guess.

## Summary — what the cryptography actually proves

- Stellar cryptography proves that a signed transaction happened, from one named account to another, for a stated amount, at a stated time. It proves nothing about who typed it, which session ran it, or why.
- Sealed-message cryptography proves that content was hidden from outsiders. It proves nothing about what the content said, who sent it, or what it ordered.
- Strongest provable point: the ledger and relay models themselves — a public ledger can, in principle, settle every Distill count and amount the moment an account address is named, and sealed messages can, in principle, settle counts and timing from relay data. The proof path is clear, even though the report does not give the inputs.
- Weakest inference: C28, key loss as a proven fact, and C41, relay owner as operator. Both turn an absence (no later movement, no other name) into a positive claim about a person or a key. Absence is not proof.
- No claim in this file names, pursues, or infers a human operator, registrant, or personal account.

## Files saved

All files sit in `work/crypto/` in the darkswarm-20261101 lane. Each JSON file has a .PROVENANCE.txt file (source URL, retrieval time, method) and a .sha256 sidecar file.

- horizon_root.json — Horizon root, lists the account, transaction, and operation query templates. SHA256 fcdef3c8f94bda3addd951293d017d07320689e769a84dfbccf4762df47664c8.
- assets_EURC.json — EURC asset search, first page, 10 issuers. SHA256 9e181b034ece8ec59bd08b161ca1170b0de31570499d82e10f3af6b7caa33cbc.
- assets_MTL.json — MTL asset search, first page, 10 issuers. SHA256 54bcb6240285d40e4d569a277c63ee667060b93f265fcf8d1b5c7378a2943734.
- assets_USDC.json — USDC asset search, first page, 10 issuers. SHA256 996f80a78a619ea83c9aa372e6ced3053909f92bea7e27f82ff46b42004518de.
- ledgers_latest.json — latest ledger at query time, ledger 65262255. SHA256 b382f947927151e17788167a50da83992ab70636ad566daf976eba0743196377.
- Query URLs: https://horizon.stellar.org/ ; https://horizon.stellar.org/assets?asset_code=EURC&limit=10 ; same pattern for MTL and USDC ; https://horizon.stellar.org/ledgers?order=desc&limit=1 .
- No git add, commit, or push was made. No Factum write was made. No account address was guessed or attributed.
