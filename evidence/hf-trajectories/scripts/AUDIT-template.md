# Audit: {{DS}}

- Source: `https://huggingface.co/datasets/{{DS}}` (raw under `raw/{{SLUG}}/`, provenance in `raw/{{SLUG}}/PROVENANCE.md`)
- Audited: {{DATE}}
- Rows/files: {{N}}
- Method: per-row text scan for CAPTCHA/Turnstile/Cloudflare/bot-check encounters and challenge-solved strings; byte-verification discipline (template-default flag ≠ defeat; challenge must appear in tool output/observations, not docstrings); marker grammar hunt (oai* tags, zz= params, epoch nonces, httpbun/httpbin carriers, webhook.site/ntfy.sh dead-drops).

## Grading legend
- **OBSERVED**: we saw this in the data.
- **INFERENCE**: we think this is true, but we did not see it directly.
- **UPSTREAM**: documented by the dataset/publisher or a cited finding elsewhere.

## Headline
{{HEADLINE}}

## Evidence
{{EVIDENCE}}

## Marker grammar
{{MARKERS}}

## Verdict: **{{VERDICT}}**
