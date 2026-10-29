# Correction note — 2026-10-23 (coordinator)

Section 5's line "No JS-bundle API routes were fetched or enumerated" is true of THIS probe run only and is misleading against the corpus. The discovery lane (earlier, pre-override) already fetched the full 1.02MB client bundle — `data/lanes/india-cert-in/raw/discovery/pentest_wb_161.248.63.110_bundle.js` (1,022,724 bytes) — and enumerated its internal routes: `/api/v1/projects`, `/api/auth/balance`, `/api/auth/billing`, X-Cairn-Project headers. A follow-up pass (2026-10-23, under the 09:10 CDT override) issued plain unauthenticated GETs to those already-enumerated routes. See `log-review-161.248.63.110.md` in `reports/india-cert-in-lead/` for the full outcome.

The §5 "not fetched" line describes this probe's scope, not the corpus state. Do not read it as "the bundle was never acquired" — it was, by the discovery lane.
