# Coordinator adversarial review — RubyGems July spike CSV review

This is the coordinator's attack pass on the review's own synthesis. The
lane adversarial review lives at
`working/adversarial/ADVERSARIAL-REVIEW.md`; this note attacks the
synthesis built from all five lanes, not just the dashboard.

## Attacks attempted

1. **"82 payload rows" double-counting.** Gross payload mentions sum
   above 82 (OAST 29 + webhook 19 + SSRF homepages 24 + XSS 10 + SSTI 4
   + payload authors 9). The cryptologist lane reports 82 as a union
   over rows, with overlapping sets. The union logic is stated in
   REPORT.md section 3, and the dashboard's own "oob url" token count
   (also 48) is explicitly not counted as evidence. The coincidence of
   the two 48s is flagged, not hidden. Attack fails, with one residual:
   the verifier lane must recompute the union from the lane inventory,
   not from the lane's prose.
2. **"203 known" set-equality claim.** The corroboration lane asserts
   the v2 set, the events.jsonl set, and the raw JFrog CSV set are
   exactly the same 203 names. That claim is load-bearing for the
   "corroborates the JFrog list, not independent observation"
   conclusion. It was verified by set equality in the lane's script.
   The verifier lane must re-run that equality check independently.
3. **"No verdict change" without re-reading the standing verdict.**
   The adversarial lane states its July-7 no-change answer rests on the
   file adding no new observation type, and notes the standing verdict
   was not re-read in that lane. REPORT.md says "no change forced,"
   which is the correct weaker claim: nothing in this file forces a
   change. Mapping the file's rows onto the standing July-7 verdict
   document remains a parent confirmation step. This is a residual
   caveat, not a hole in the file analysis.
4. **Live-state generalization.** Live checks covered 20 RubyGems API
   names and 10 Diffend names. REPORT.md qualifies batch-removal claims
   to sampled names and states per-name results. No claim in the report
   generalizes live state to all 533 rows. Attack fails.
5. **Factum sampling.** Factum matching covered a stated 30-name
   sample, not all 533 names. REPORT.md states this and rests the
   exhaustive classification on local sources (v2 + lane files + notes),
   which do classify all 533. The sample's role is cross-check only.
   Attack fails.
6. **Credential handling.** Three lanes ran keyword scans with
   method-dependent counts (5–7 cells). REPORT.md reports the range and
   the method dependence, copies no value, and confirms zero key-shaped
   patterns. The count-only rule is honored. Attack fails.
7. **Empty-field rows.** REPORT.md refuses to read the 49 empty rows as
   safe and lists them as a coverage hole. The 6 monib110 batch rows
   inside the 49 are called out. Attack fails.
8. **Score claims.** REPORT.md states Haiku score exists on 20 rows
   only and refuses any score claim for v1 rows. The v1/v2 calibration
   shift is reported with matched-shape inconsistencies. Attack fails.

## Kills confirmed from the lane review

Dashboard critical/high as risk; Haiku high on 385 rows as high risk;
Haiku score as a calibrated scale; version 2 superseding version 1;
"possible"/"likely" as agent evidence; MFA/publisher assertions;
exact reason batch sizes for tester and monib110; withdrawn as
malicious or as risk gone; empty as safe; out-of-band or metadata
homepage as SSRF success or exfiltration; markup string as XSS
execution; mass-generated as agent-generated; July spike as one
campaign or actor from this file alone; placeholder, short, numbered,
test, or burst shapes as malicious intent.

## Surviving claims, graded

See findings.json (F01–F23). Nothing survives as agent attribution,
severity grading, or impact. The file's durable value is: a shape-sorted
inventory of 533 July rows; 330 names new to our corpus (three mass
batches plus 20 ordinary-looking gems); a July-7 mechanism-family match
on metadata strings; and a live-state snapshot for 20 sampled names.

## Residual caveats for the parent

- Verdict-change mapping to the standing July-7 verdict document needs
  parent confirmation (see attack 3).
- Gem code behavior and callback receipts were never fetched; both stay
  open questions, not findings.
- The 851 third-party-only rows in v2 are untouched by this review;
  this file does not corroborate or kill them.
