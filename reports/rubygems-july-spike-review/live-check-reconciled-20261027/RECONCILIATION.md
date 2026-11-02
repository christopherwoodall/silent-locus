# Reconciliation: two independent July-spike live censuses, 2026-10-27

Sources: first census (live-check-20261027, commit 7e5d41bd) and helper-fleet
census (live-check-help-20261027, commit 607afd08). Both covered all 533 names.
Name sets identical. RubyGems API verdicts identical (23 live / 510 gone).

## Differences found (5) and adjudication by fresh re-fetch

1. Diffend pages for apex-black-test-011, apex-oidc-probe, apex-blk-test-final,
   minitest-hashdiff: first census said full, helper said stub.
   Fresh fetch 2026-10-27: each page ~5.7 KB with no diff content, vs an
   agreed-full page (sportdb-parser, 23.6 KB, 168 version patterns) and an
   agreed-stub page (mini-sharp-hub, 5.6 KB, stub marker present).
   Adjudication: STUB-class. Helper was right; the 4 URLs are NOT artifacts.
2. klondikemarlen-jira-api Diffend: first said stub, helper said gone.
   Fresh fetch redirects to the Diffend index. Adjudication: GONE.
   No artifact either way.
3. edoxen source repo: first counted github.com/metanorma/edoxen live;
   helper counted it 301, not live. Fresh check: it 301s to
   github.com/edoxen/edoxen, which answers 200. Adjudication: artifact at
   the NEW URL, not the old one.
4. OAST callback endpoints (2): helper counted them as source artifacts;
   first excluded them. Adjudication: EXCLUDED. A collector answering 200
   is not a package artifact, and both gems are API-404. Listed here only:
   http://d966sooa8p5umhpheccg6tnm9at8ix9kh.oast.online/source_code
   https://d96977lq1pkct8do7pn0dh1nbhzygujby.oast.online/ssrf

## Reconciled totals

- RubyGems API live: 23. Diffend full: 18. Artifact URLs: see live-urls.txt.
- Live on both: 18. Live on RubyGems only: 5. Live on Diffend only: 0.
- Tombstone/not-hosted RubyGems pages (510) remain viewable but are NOT
  artifacts; see the first census's yanked-tombstone-pages.txt.
