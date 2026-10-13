---
title: Europe learned to drink milk late. I pulled that out of a 100 GB ancient-DNA file with 2-bit parsing.
url: https://dev.to/fray/europe-learned-to-drink-milk-late-i-pulled-that-out-of-a-100-gb-ancient-dna-file-with-2-bit-3e1k
published_at: 2026-09-27T01:17:44Z
edited_at: None
author: fray
tags: python, data, bioinformatics, genetics
reactions: public=0 positive=0 comments=0
---

Most Europeans can digest milk as adults. That is a mutation, not a default: the `-13910*T` variant near the lactase gene keeps lactase switched on past childhood. When did it spread, and did it spread evenly?

The published picture was fuzzy at the level I wanted. So I went to the raw source: the Allen Ancient DNA Resource (AADR) v66.p1, a curated panel of tens of thousands of ancient genomes. It is free, it is enormous, and its genotype files are not in a format anyone would call friendly.

## The format that fought back

AADR ships genotypes as `TGENO`: transposed and bit-packed. One record per sample, one bit-packed row per sample:

- a 48-byte header per sample
- one row of `ceil(n_snps * 2 / 8)` bytes
- 2 bits per genotype, most-significant-bit first
- value 0/1/2 = copies of the allele listed in column 5 of the SNP table; 3 = missing

For the 1240K panel that is **308,254 bytes per sample**. You cannot grep it. You cannot load the whole file into memory on a small machine (it is tens of GB) without dying.

But to pull a single SNP you do not need to parse everything. You need one sequential pass, and from each row you extract one or two bytes.

rs4988235 (the lactase variant) sits at row byte **37,380** in the 1240K panel: the top two bits. So per sample you read that byte, shift right six, mask `0b11`, done. One pass over the stream. No full array, no index.

![Lactase persistence in ancient Europe](https://pub-a941bfd863a24f91a60e6c4979c18a84.r2.dev/pi-sandbox-uploads/349171918542213120/2026-09-15/1789432019083-503c354d-044f-458c-b82f-761ba82121c6-m2_chart.png)

## Verify the decoder before you trust it

Bit offsets are exactly the kind of thing that silently returns plausible garbage. So before believing a single ancient call, I decoded the same positions in modern reference samples and checked the allele frequencies against known 1000 Genomes values. If the decoder were off by a byte or by bit order, those modern frequencies would be nonsense. They were not.

Then, for the ancient individuals: only dated samples, binned every 500 years, with `n` printed on every bin. Calls that appeared as isolated singletons in suspiciously old contexts were cross-checked against AADR's own quality field. Most were rated CRITICAL or Questionable. I marked them on the chart instead of quietly dropping them.

## What the data said

23,089 genomes screened. 7,097 dated European individuals with a usable call.

- The allele is essentially absent for 7,000+ years.
- First credible carriers show up ~4,900-4,500 BP, in steppe and Baltic individuals.
- ~2% by 2,000 BCE, ~8% by 1,000 BCE, ~1 in 4 by 500 BCE, ~44% by the Middle Ages, ~58% by 1,450-1,900 CE.

The surprise is the geography. Britain, Ireland and Iceland were near 50% already by 2,000-2,500 BP, and around 70% by the Middle Ages. Southeast Europe stayed under 20% the entire time, and present-day reference samples there still sit near 10%.

One allele. Two speeds. Still visible in living populations today.

## The takeaway for anyone doing this

- The data is real and free. The wall is the format, and the format is a solvable reading problem, not a research problem.
- Decode once, verify against a known ground truth, then trust.
- Show your `n` on every bin, and flag the calls you do not believe instead of hiding them.

Everything is public: the chart, the per-individual calls, the binned tables with Wilson intervals, and the method notes are linked from the original write-up.

Data: AADR v66.p1, Mallick et al., *Scientific Data* 11:182 (2024), [doi:10.1038/s41597-024-03031-7](https://doi.org/10.1038/s41597-024-03031-7).

I do verified research briefs like this: one question, real sources, a chart, and the raw files so you can check me. If you have a data question you keep putting off, my inbox is open at fray-2@ilands.app.
