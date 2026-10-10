# Findings

Grade claims OBSERVED, UPSTREAM, or INFERENCE.

- corpus_record_counts (OBSERVED): payload 91,037 / recovered_text 75,534 /
  response 23,008 = 189,579 total. IDs R0000001–R0189579, zero gaps.
- record_field_stats (OBSERVED): uniform 7-field records; parent_id null on
  all 91,037 payloads; time_utc null on all 189,579 records. No timestamps
  anywhere in the corpus.
- redaction_marker_counts (OBSERVED): 116,646 destination redactions;
  100,215 numbered encoded blobs; 15,335 bare encoded blobs;
  42,790 credential markers; 24,777 opaque markers; 25,420 runtime
  identifiers; 22,866 source identifiers; 15,254 sensitive-content markers;
  81 URL fragments.
- parentage_topology (OBSERVED): 61,124 parents point at payload records,
  1 at a recovered_text record, 0 dangling. Payloads are chain roots.
  parent_id is the only ordering signal.
- cite_token_semantics (OBSERVED): 163,849 distinct 8-hex tokens; 19,036
  reused; max 1,094 records on one token. Token is a template/cluster key,
  not a content hash.

Cite Factum IDs claim_0f678d8ac3ce4d37bc6f9a7198b752c7,
claim_08e6843885804190924955557d33f931,
claim_e8e6fb2bd77d4f039d53e4f05e8bf1bf,
claim_fe2ec61e4d464e2eb6ba6bbf2ce2a1c4,
claim_9a1e858de5084dc2b49ed146ee6e8703.
