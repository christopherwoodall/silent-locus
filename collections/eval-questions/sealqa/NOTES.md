# NOTES — sealqa

- Source URL: https://huggingface.co/datasets/vtllms/sealqa/resolve/main/{seal-0,seal-hard,longseal}.parquet
- Homepage: https://huggingface.co/datasets/vtllms/sealqa
- Eval org: Academic (Virginia Tech, vtllms)
- License: apache-2.0
- Retrieved: 2026-10-05
- Raw files: raw/seal-0.parquet (27KB), raw/seal-hard.parquet (49KB), raw/longseal.parquet (73MB — carries a large `search_results` column) — all byte-identical
- Banked questions: 619 / expected 619 (111 seal_0 + 254 seal_hard + 254 longseal, datasets-server) — MATCH
- Included: yes — fact-seeking questions over noisy/conflicting web search; has per-question `urls`, `topic`, `freshness` columns (trace gold)
- QUIRK (parquet parsing): no pyarrow/fastparquet/duckdb on the VM and no installs allowed, so a minimal stdlib-only parquet reader was written (_tools/pqread.py = thrift-compact footer parser, _tools/snappy.py = raw-block snappy decompressor, _tools/pqdec.py = page decoder). Verified: footer num_rows match on all three files; decoded questions cross-checked against data-page statistics min/max. Empirical findings encoded in the reader: (1) SchemaElement/ColumnMetaData field ids per parquet.thrift (type=1..name=4, NOT name-first); (2) compact list header = single byte, size in HIGH nibble; (3) pages are SNAPPY-compressed — must decompress even when compressed==uncompressed size; (4) data-page header `encoding` enum is unreliable in these files (claims BYTE_STREAM_SPLIT for structurally RLE_DICTIONARY data; level encodings claim BIT_PACKED for RLE levels) — decoder works off structure (dictionary page present => RLE_DICTIONARY layout).
- Normalization: question_id = {seal-0|seal-hard|longseal}-{i:04d}; question = `question`; topic = `topic`. `search_results` column skipped (bulk, not needed for question banking).
