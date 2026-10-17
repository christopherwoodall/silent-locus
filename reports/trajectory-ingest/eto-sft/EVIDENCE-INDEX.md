# ETO-SFT Evidence Index

Dataset: `agent-eto/eto-sft-trajectory`, rev
`a8f745ef799a5201d2288b9c2a47e40a0ff70a4c`.
All quotes byte-verified against the raw files below.

| Finding | Trajectory | File (sha256) | Turns |
|---|---|---|---|
| F-A01 | alfworld_133 (exemplar; 70 others) | `data/lanes/eto-sft-trajectories/raw/data/alfworld_sft.json` (9bc9720466cdbae9da26f60ab61ccdd34ae2d1e8c9f1b2ca5a1acb6606f66972) | [9,9] |
| F-A02 | alfworld_3436 (also alfworld_919 t13, alfworld_2464 t13, alfworld_1263 t43, alfworld_1270 t15) | alfworld_sft.json (9bc9720466cdbae9da26f60ab61ccdd34ae2d1e8c9f1b2ca5a1acb6606f66972) | [13,14] |
| F-A03 | alfworld_1270 | alfworld_sft.json (9bc9720466cdbae9da26f60ab61ccdd34ae2d1e8c9f1b2ca5a1acb6606f66972) | [15,17] |
| F-A04 | alfworld_3319 (also alfworld_797 t9) | alfworld_sft.json (9bc9720466cdbae9da26f60ab61ccdd34ae2d1e8c9f1b2ca5a1acb6606f66972) | [11,12] |
| F-A05 | alfworld_797 | alfworld_sft.json (9bc9720466cdbae9da26f60ab61ccdd34ae2d1e8c9f1b2ca5a1acb6606f66972) | [9,11] |
| F-A06 | alfworld_2087 | alfworld_sft.json (9bc9720466cdbae9da26f60ab61ccdd34ae2d1e8c9f1b2ca5a1acb6606f66972) | [3,99] |
| RB-W-001 | 282 | `data/lanes/eto-sft-trajectories/raw/data/webshop_sft.json` (3fd1ff38f28dccaf4448cc5fa8609f2a3d3100bed303d66b6d748cff5a49601b) | [9,9] |
| RB-W-002 | 1298 | webshop_sft.json (3fd1ff38f28dccaf4448cc5fa8609f2a3d3100bed303d66b6d748cff5a49601b) | [9,9] |
| RB-W-003 | 272 | webshop_sft.json (3fd1ff38f28dccaf4448cc5fa8609f2a3d3100bed303d66b6d748cff5a49601b) | [11,11] |
| RB-W-004 | 1961 | webshop_sft.json (3fd1ff38f28dccaf4448cc5fa8609f2a3d3100bed303d66b6d748cff5a49601b) | [7,7] |
| RB-W-005 | 116 | webshop_sft.json (3fd1ff38f28dccaf4448cc5fa8609f2a3d3100bed303d66b6d748cff5a49601b) | [7,7] |
| RB-W-006 | 1948 | webshop_sft.json (3fd1ff38f28dccaf4448cc5fa8609f2a3d3100bed303d66b6d748cff5a49601b) | [5,9] |
| RB-W-007 | 2319 | webshop_sft.json (3fd1ff38f28dccaf4448cc5fa8609f2a3d3100bed303d66b6d748cff5a49601b) | [9,9] |
| RB-S-001 | 15_53 | `data/lanes/eto-sft-trajectories/raw/data/sciworld_sft.json` (7079f08068ec4c526628857695231b97939472e697c3a87b4f75f682829f0ee5) | [88,89] |
| RB-S-002 | 4_79 | sciworld_sft.json (7079f08068ec4c526628857695231b97939472e697c3a87b4f75f682829f0ee5) | [21,199] |

Turn numbers are 0-based indexes into the record's `conversations`
list. `from` roles are exactly `human` (environment/observation)
and `gpt` (agent thought + action).

Corpus-level claims (F-A01 counts, RB-S-001 326/326, F-A04 2 in
20,132, RB-W-001 47 over-budget buys) derive from full-file scans
of the three raw JSON files above. Retrieval provenance:
`raw/data/<file>.PROVENANCE.txt`.
