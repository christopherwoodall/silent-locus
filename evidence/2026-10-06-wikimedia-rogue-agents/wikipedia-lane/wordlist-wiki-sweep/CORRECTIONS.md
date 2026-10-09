# CORRECTIONS — wordlist wiki sweep, query-mangling artifacts

## 2026-10-07 ~01:55 UTC — CirrusSearch special-char mangling (coordinator)

Three search terms contain regex/special characters that CirrusSearch's
`insource:"..."` PHRASE mode mangles into wildcard-ish queries, producing
giant false-positive hit counts:

| term | phrase-mode result (enwiki) | correct query | correct result (enwiki) |
|---|---|---|---|
| `${7*7}` | 168,354 hits (mangled) | `insource:/\$\{7\*7\}/` | 0 |
| `oai[0-9]+` | phrase-mode untested (would match literal text) | `insource:/oai[0-9]+/` | 68, all noise* |
| `zz=oai[0-9]+` | phrase-mode untested | `insource:/zz=oai[0-9]+/` | 0 |

\* The 68 `oai[0-9]+` hits are coincidental `oai`+digits substrings inside
random URL slugs (`...sbdaoai43dd4`), ref names (`woai1` = WOAI TV,
`Soai2001` = chemist Soai) — none is the `zz=oai<digits>` agent grammar.
Graded NOISE.

Remediation: `sweep_resume.py` carries a SPECIAL_REGEX map — these three
terms are searched as `insource:/.../` regex on all 9 wikis. Their bogus
phrase-mode rows were removed from run logs (enwiki run-log 492→489 rows)
and cached files deleted so they re-run correctly. No other terms are
affected (only 8/1,148 terms contain special chars; the other 5 are
harmless literal phrases).
