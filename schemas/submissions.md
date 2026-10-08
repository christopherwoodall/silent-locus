# schemas/submissions.md

Transluce filing drafts under `data/transluce-api/submissions/`.

## Draft files: `NNN-slug.md`

- Numbered `001`, `002`, `003`, … with a short slug
  (e.g. `001-jina-nov2025.md`, `002-glm-turnstile-gsmarena.md`).
- Content: the full form as filed on the Transluce Findings tracker —
  Status, Transluce ID, Evidence pack, Short description, Detailed
  description, and the form sections as filed.
- A family may also get a directory (`003-deaddrop-family/`) holding
  the form plus evidence-pack build notes; the flat `NNN-slug.md`
  remains the filed-form record.

## `LEDGER.md` — submissions ledger

Markdown table with columns:
- `#` — submission number (001, 002, …).
- `Date` — filing/preparation date (YYYY-MM-DD).
- `Transluce ID` — the tracker's finding number once live, `_pending_`
  before.
- `Summary` — one-line description.
- `Status` — one of:
  - `Prepared` — form prefilled, not yet submitted.
  - `ON HOLD` — operator freeze; do not file until reversed.
  - `Submitted` — live on the tracker; Transluce ID recorded.
  - `Withdrawn` — removed or superseded.
