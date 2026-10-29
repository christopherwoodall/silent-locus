# EVALHUNT — Hunt Queries (W4-HUNT-BRIEF)

Built 2026-10-05 from `collections/eval-questions/all-questions.jsonl` (10,201 records, 11 evals).
Ranking: corpus-uniqueness (low n-gram df) × entity rarity × phrase length 5–8 words × trace-likelihood
(SimpleQA/FRAMES/SealQA/WebWalkerQA/AssistantBench = browse-heavy; tau-bench/mle-bench/webarena/facts-grounding = down-weighted or skipped).
Precedent: DeepSearchQA dsqa_250 verbatim-matched the June-17 DoE incident task — one verbatim hit is gold.

Conventions: `q=` on urlquery.net keyword-matches **submitted URLs** (so the token-pair variant targets
search-engine URLs like `google.com/search?q=piatetski+shapiro+wolf+prize`); the full-phrase variant targets
verbatim URL/title capture. `url.domain:` scopes to the expected-source domain.
On urlscan.io, `page.title:` / `task.url:` / `domain:` are the operative fields.

## 1. TOP 50 ranked fingerprint phrases

### 1. "1990 wolf prize with ilya iosifovich piatetski shapiro"
- **openai-simpleqa:simpleqa-01554** — What is the full name of the individual who shared the 1990 Wolf Prize with Ilya Iosifovich Piatetski-Shapiro?
- why: Rare person (Ilya Iosifovich Piatetski-Shapiro) + rare award (Wolf Prize) + year 1990 — a three-part collocation no one types by accident; agents fetching the MacTutor biography page leak it.
- urlquery: `q="1990 wolf prize with ilya iosifovich piatetski shapiro"` · tokens: `q="1990 wolf prize"` · domain: `url.domain:mathshistory.st-andrews.ac.uk`
- urlscan: `page.title:"1990 wolf prize with ilya iosifovich piatetski shapiro"` · `task.url:"1990 wolf prize"` · `domain:mathshistory.st-andrews.ac.uk`
- google: `"1990 wolf prize with ilya iosifovich piatetski shapiro"`

### 2. "2003 sigplan john c reynolds doctoral dissertation award"
- **openai-simpleqa:simpleqa-03048** — Who won the 2003 SIGPLAN John C. Reynolds Doctoral Dissertation Award?
- why: Niche CS award (SIGPLAN John C. Reynolds Doctoral Dissertation Award) + year — only appears in award-listing contexts; agent visits sigplan.org/awards to answer.
- urlquery: `q="2003 sigplan john c reynolds doctoral dissertation award"` · tokens: `q="2003 sigplan john"` · domain: `url.domain:sigplan.org`
- urlscan: `page.title:"2003 sigplan john c reynolds doctoral dissertation award"` · `task.url:"2003 sigplan john"` · `domain:sigplan.org`
- google: `"2003 sigplan john c reynolds doctoral dissertation award"`

### 3. "2015 wickham skinner teaching innovation award"
- **webwalkerqa:webwalkerqa-0021** — Who won the 2015 Wickham Skinner Teaching Innovation Award?
- why: Rare named award (Wickham Skinner Teaching Innovation Award) + year — poms.org is the expected source; a burst of poms.org visits is itself the trace.
- urlquery: `q="2015 wickham skinner teaching innovation award"` · tokens: `q="2015 wickham skinner"` · domain: `url.domain:poms.org`
- urlscan: `page.title:"2015 wickham skinner teaching innovation award"` · `task.url:"2015 wickham skinner"` · `domain:poms.org`
- google: `"2015 wickham skinner teaching innovation award"`

### 4. "tribunal that nullified chris ngige s 2003 anambra"
- **openai-simpleqa:simpleqa-03553** — What is the surname of the judge who led the Election Tribunal that nullified Chris Ngige's 2003 Anambra governorship victory in August 2006?
- why: Rare person (Chris Ngige) + specific event (2003 Anambra governorship nullification) — Nigerian political trivia with near-zero organic overlap.
- urlquery: `q="tribunal that nullified chris ngige s 2003 anambra"` · tokens: `q="tribunal that nullified"` · domain: `url.domain:vanguardngr.com`
- urlscan: `page.title:"tribunal that nullified chris ngige s 2003 anambra"` · `task.url:"tribunal that nullified"` · `domain:vanguardngr.com`
- google: `"tribunal that nullified chris ngige s 2003 anambra"`

### 5. "july 2018 by ramadan badry hussein"
- **openai-simpleqa:simpleqa-00325** — What item was found in a damaged wooden coffin in July 2018 by Ramadan Badry Hussein?
- why: Rare person (Ramadan Badry Hussein) + month-year — Saqqara archaeology story; the name is the fingerprint.
- urlquery: `q="july 2018 by ramadan badry hussein"` · tokens: `q="july 2018 ramadan"` · domain: `url.domain:livescience.com`
- urlscan: `page.title:"july 2018 by ramadan badry hussein"` · `task.url:"july 2018 ramadan"` · `domain:livescience.com`
- google: `"july 2018 by ramadan badry hussein"`

### 6. "first transistor-based computer philco transac s-2000"
- **openai-simpleqa:simpleqa-02760** — Who designed the software for the first transistor-based computer, Philco Transac S-2000?
- why: First transistor-based computer (Philco Transac S-2000) — computing-history collocation that survives paraphrase ('transistor-based', 'Philco', 'S-2000').
- urlquery: `q="first transistor-based computer philco transac s-2000"` · tokens: `q="first transistor-based computer"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"first transistor-based computer philco transac s-2000"` · `task.url:"first transistor-based computer"` · `domain:en.wikipedia.org`
- google: `"first transistor-based computer philco transac s-2000"`

### 7. "galler kulturpreis der st gallischen kulturstiftung"
- **openai-simpleqa:simpleqa-00612** — In what year was Pipilotti Rist first awarded the 'St. Galler Kulturpreis der St. Gallischen Kulturstiftung'?
- why: German award name verbatim ('St. Galler Kulturpreis der St. Gallischen Kulturstiftung') — non-English proper noun string, extremely high verbatim survival.
- urlquery: `q="galler kulturpreis der st gallischen kulturstiftung"` · tokens: `q="galler kulturpreis gallischen"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"galler kulturpreis der st gallischen kulturstiftung"` · `task.url:"galler kulturpreis gallischen"` · `domain:en.wikipedia.org`
- google: `"galler kulturpreis der st gallischen kulturstiftung"`

### 8. "bikini atoll eschscholtz atoll"
- **openai-simpleqa:simpleqa-02566** — What is the name of the person who explored and named Bikini Atoll "Eschscholtz Atoll"?
- why: Obsolete place-name ('Eschscholtz Atoll' for Bikini Atoll) — historical naming trivia; the archaic name is the fingerprint.
- urlquery: `q="bikini atoll eschscholtz atoll"` · tokens: `q="bikini atoll eschscholtz"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"bikini atoll eschscholtz atoll"` · `task.url:"bikini atoll eschscholtz"` · `domain:en.wikipedia.org`
- google: `"bikini atoll eschscholtz atoll"`

### 9. "asantehene otumfuo opoku ware ii"
- **openai-simpleqa:simpleqa-01870** — In which year was the stool "Nkosuostool" (Development stool) created by Asantehene, Otumfuo Opoku Ware II?
- why: Rare royal title + name (Asantehene Otumfuo Opoku Ware II) — Ghanaian chieftaincy collocation, near-zero background rate.
- urlquery: `q="asantehene otumfuo opoku ware ii"` · tokens: `q="asantehene otumfuo opoku"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"asantehene otumfuo opoku ware ii"` · `task.url:"asantehene otumfuo opoku"` · `domain:en.wikipedia.org`
- google: `"asantehene otumfuo opoku ware ii"`

### 10. "pornographic drawings 1997 cornelia parker"
- **openai-simpleqa:simpleqa-00549** — What item did Cornelia Parker dissolve to create ink for her work "Pornographic Drawings (1997)"?
- why: Artist + titled work + year (Cornelia Parker, 'Pornographic Drawings', 1997) — the unusual title survives any paraphrase of the question.
- urlquery: `q="pornographic drawings 1997 cornelia parker"` · tokens: `q="pornographic drawings 1997"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"pornographic drawings 1997 cornelia parker"` · `task.url:"pornographic drawings 1997"` · `domain:en.wikipedia.org`
- google: `"pornographic drawings 1997 cornelia parker"`

### 11. "1938 with tadashi nakayama"
- **openai-simpleqa:simpleqa-02169** — What Toronto doctoral student coauthored "Note on Symmetric Algebras (1938)" with Tadashi Nakayama?
- why: Rare mathematician (Tadashi Nakayama) + paper title ('Note on Symmetric Algebras') + year 1938 — pairs with mathshistory.st-andrews.ac.uk.
- urlquery: `q="1938 with tadashi nakayama"` · tokens: `q="1938 with tadashi"` · domain: `url.domain:mathshistory.st-andrews.ac.uk`
- urlscan: `page.title:"1938 with tadashi nakayama"` · `task.url:"1938 with tadashi"` · `domain:mathshistory.st-andrews.ac.uk`
- google: `"1938 with tadashi nakayama"`

### 12. "sigmod edgar f codd innovations award in 1995"
- **openai-simpleqa:simpleqa-04223** — Who received the SIGMOD Edgar F. Codd Innovations Award in 1995?
- why: Niche CS award (SIGMOD Edgar F. Codd Innovations Award) + year 1995 — award-listing context only.
- urlquery: `q="sigmod edgar f codd innovations award in 1995"` · tokens: `q="sigmod edgar codd"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"sigmod edgar f codd innovations award in 1995"` · `task.url:"sigmod edgar codd"` · `domain:en.wikipedia.org`
- google: `"sigmod edgar f codd innovations award in 1995"`

### 13. "leopoldo luis cabo penna franca marry ana cristina"
- **openai-simpleqa:simpleqa-02599** — On what day, month, and year did the Brazilian mathematician Leopoldo Luis Cabo Penna Franca marry Ana Cristina Leonardos?
- why: Rare Brazilian mathematician's full name (Leopoldo Luis Cabo Penna Franca) — four-part name no one reproduces by chance; pairs with MacTutor.
- urlquery: `q="leopoldo luis cabo penna franca marry ana cristina"` · tokens: `q="leopoldo luis cabo"` · domain: `url.domain:mathshistory.st-andrews.ac.uk`
- urlscan: `page.title:"leopoldo luis cabo penna franca marry ana cristina"` · `task.url:"leopoldo luis cabo"` · `domain:mathshistory.st-andrews.ac.uk`
- google: `"leopoldo luis cabo penna franca marry ana cristina"`

### 14. "received the worcester reed warner medal in 1934"
- **openai-simpleqa:simpleqa-02865** — Which engineer received the Worcester Reed Warner Medal in 1934?
- why: Niche engineering award (Worcester Reed Warner Medal) + year 1934 — ASME award-listing context; pairs with asme.org.
- urlquery: `q="received the worcester reed warner medal in 1934"` · tokens: `q="received worcester reed"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"received the worcester reed warner medal in 1934"` · `task.url:"received worcester reed"` · `domain:en.wikipedia.org`
- google: `"received the worcester reed warner medal in 1934"`

### 15. "mufti sayed contest the 2019 lok sabha elections"
- **openai-simpleqa:simpleqa-00009** — To whom did Mehbooba Mufti Sayed contest the 2019 Lok Sabha elections and lose?
- why: Rare person (Mehbooba Mufti Sayed) + event (2019 Lok Sabha elections) — Indian political trivia, distinctive name.
- urlquery: `q="mufti sayed contest the 2019 lok sabha elections"` · tokens: `q="mufti sayed contest"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"mufti sayed contest the 2019 lok sabha elections"` · `task.url:"mufti sayed contest"` · `domain:en.wikipedia.org`
- google: `"mufti sayed contest the 2019 lok sabha elections"`

### 16. "british linguist bernard comrie married in 1985"
- **openai-simpleqa:simpleqa-00037** — What is the first and last name of the woman whom the British linguist Bernard Comrie married in 1985?
- why: Rare person (British linguist Bernard Comrie) + year 1985 — the name + marriage-year combo is the fingerprint.
- urlquery: `q="british linguist bernard comrie married in 1985"` · tokens: `q="british linguist bernard"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"british linguist bernard comrie married in 1985"` · `task.url:"british linguist bernard"` · `domain:en.wikipedia.org`
- google: `"british linguist bernard comrie married in 1985"`

### 17. "manila bulletin in may 2021 succeeding dr crispulo"
- **openai-simpleqa:simpleqa-01723** — Who was named the new editor-in-chief of The Manila Bulletin in May 2021, succeeding Dr. Crispulo Icban?
- why: Rare org + person + month-year (Manila Bulletin, Dr. Crispulo Icban, May 2021) — pairs with mb.com.ph; a burst of mb.com.ph visits is the trace.
- urlquery: `q="manila bulletin in may 2021 succeeding dr crispulo"` · tokens: `q="manila bulletin 2021"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"manila bulletin in may 2021 succeeding dr crispulo"` · `task.url:"manila bulletin 2021"` · `domain:en.wikipedia.org`
- google: `"manila bulletin in may 2021 succeeding dr crispulo"`

### 18. "2018 acm eugene l lawler award recipient"
- **openai-simpleqa:simpleqa-02622** — Who was the 2018 ACM Eugene L. Lawler Award recipient?
- why: Niche CS award (ACM Eugene L. Lawler Award) + year 2018 — pairs with awards.acm.org.
- urlquery: `q="2018 acm eugene l lawler award recipient"` · tokens: `q="2018 eugene lawler"` · domain: `url.domain:awards.acm.org`
- urlscan: `page.title:"2018 acm eugene l lawler award recipient"` · `task.url:"2018 eugene lawler"` · `domain:awards.acm.org`
- google: `"2018 acm eugene l lawler award recipient"`

### 19. "1881 edward s morse of salem massachusetts patented"
- **openai-simpleqa:simpleqa-01952** — In 1881, Edward S. Morse of Salem, Massachusetts, patented a way of warming and ventilating apartments using what?
- why: Rare person + place + year (Edward S. Morse, Salem Massachusetts, 1881) + patent context — pairs with patents.google.com.
- urlquery: `q="1881 edward s morse of salem massachusetts patented"` · tokens: `q="1881 edward morse"` · domain: `url.domain:patents.google.com`
- urlscan: `page.title:"1881 edward s morse of salem massachusetts patented"` · `task.url:"1881 edward morse"` · `domain:patents.google.com`
- google: `"1881 edward s morse of salem massachusetts patented"`

### 20. "1981 judith feist hemmendinger received her ph d"
- **openai-simpleqa:simpleqa-01208** — In 1981, Judith Feist Hemmendinger received her Ph.D. from which French university?
- why: Rare person (Judith Feist Hemmendinger) + Ph.D. + year 1981 — Holocaust-research context; pairs with the1939society.org.
- urlquery: `q="1981 judith feist hemmendinger received her ph d"` · tokens: `q="1981 judith feist"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"1981 judith feist hemmendinger received her ph d"` · `task.url:"1981 judith feist"` · `domain:en.wikipedia.org`
- google: `"1981 judith feist hemmendinger received her ph d"`

### 21. "marcel baschet 1883 grand prix de rome"
- **openai-simpleqa:simpleqa-01248** — What is the English translation of the title of the painting for which Marcel Baschet won the 1883 Grand Prix de Rome?
- why: Rare painter (Marcel Baschet) + Grand Prix de Rome + year 1883 — French art-history collocation.
- urlquery: `q="marcel baschet 1883 grand prix de rome"` · tokens: `q="marcel baschet 1883"` · domain: `url.domain:hellenicaworld.com`
- urlscan: `page.title:"marcel baschet 1883 grand prix de rome"` · `task.url:"marcel baschet 1883"` · `domain:hellenicaworld.com`
- google: `"marcel baschet 1883 grand prix de rome"`

### 22. "loukia vassilopoulou michail matalliotakis maria zervou"
- **openai-simpleqa:simpleqa-01077** — A 2019 genome-wide association study review published by Loukia Vassilopoulou, Michail Matalliotakis, Maria I. Zervou, Charoula Matalliotaki, Konstantinos Krithinakis, Ioannis Matalliotakis, Demetrios A. Spandidos, and G
- why: Four rare author surnames in one GWAS-review citation (Vassilopoulou, Matalliotakis, Zervou) — citation-string fingerprint; pairs with ncbi.nlm.nih.gov.
- urlquery: `q="loukia vassilopoulou michail matalliotakis maria zervou"` · tokens: `q="loukia vassilopoulou michail"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"loukia vassilopoulou michail matalliotakis maria zervou"` · `task.url:"loukia vassilopoulou michail"` · `domain:en.wikipedia.org`
- google: `"loukia vassilopoulou michail matalliotakis maria zervou"`

### 23. "dregling merchant in demon s souls 2009"
- **openai-simpleqa:simpleqa-01466** — What is the soul price of the Short Spear sold by the Dregling Merchant in Demon's Souls (2009)?
- why: Game-specific entity (Dregling Merchant) + game + year (Demon's Souls, 2009) — pairs with demonssouls.wikidot.com; wiki.gg-style fan wikis are agent favorites.
- urlquery: `q="dregling merchant in demon s souls 2009"` · tokens: `q="dregling merchant demon"` · domain: `url.domain:demonssouls.wikidot.com`
- urlscan: `page.title:"dregling merchant in demon s souls 2009"` · `task.url:"dregling merchant demon"` · `domain:demonssouls.wikidot.com`
- google: `"dregling merchant in demon s souls 2009"`

### 24. "former mla ashok veer vikram singh"
- **openai-simpleqa:simpleqa-03189** — What was the name of the maid who committed suicide by setting herself on fire on May 21, 2007, because the former MLA Ashok Veer Vikram Singh exploited her physically, while his wife, a sitting MLA from Bijawar, used to
- why: Rare person (Ashok Veer Vikram Singh) + title (former MLA) — Indian crime-politics story with a distinctive name.
- urlquery: `q="former mla ashok veer vikram singh"` · tokens: `q="former ashok veer"` · domain: `url.domain:dailypioneer.com`
- urlscan: `page.title:"former mla ashok veer vikram singh"` · `task.url:"former ashok veer"` · `domain:dailypioneer.com`
- google: `"former mla ashok veer vikram singh"`

### 25. "women s asian individual squash championships aisc 2017"
- **openai-simpleqa:simpleqa-00889** — Who won the 19th edition of the Women’s Asian Individual Squash Championships (AISC)-2017?
- why: Rare event (Women's Asian Individual Squash Championships, AISC 2017) — sports-trivia collocation; pairs with asiansquash.org.
- urlquery: `q="women s asian individual squash championships aisc 2017"` · tokens: `q="women asian individual"` · domain: `url.domain:gktoday.in`
- urlscan: `page.title:"women s asian individual squash championships aisc 2017"` · `task.url:"women asian individual"` · `domain:gktoday.in`
- google: `"women s asian individual squash championships aisc 2017"`

### 26. "2019 video game sekiro shadows die twice"
- **openai-simpleqa:simpleqa-01683** — What was the name of Lord Takeru's partner in the 2019 video game Sekiro: Shadows Die Twice?
- why: Game + year + character (Sekiro: Shadows Die Twice, 2019, Lord Takeru) — pairs with sekiroshadowsdietwice.wiki.fextralife.com.
- urlquery: `q="2019 video game sekiro shadows die twice"` · tokens: `q="2019 video game"` · domain: `url.domain:sekiroshadowsdietwice.wiki.fextralife.com`
- urlscan: `page.title:"2019 video game sekiro shadows die twice"` · `task.url:"2019 video game"` · `domain:sekiroshadowsdietwice.wiki.fextralife.com`
- google: `"2019 video game sekiro shadows die twice"`

### 27. "2015 maine state pumpkin and squash weigh off"
- **openai-simpleqa:simpleqa-00514** — Who won the 2015 Maine State Pumpkin and Squash Weigh-Off, held at the Cumberland Fair?
- why: Hyper-specific local event (2015 Maine State Pumpkin and Squash Weigh-Off) — small-town trivia with near-zero background.
- urlquery: `q="2015 maine state pumpkin and squash weigh off"` · tokens: `q="2015 maine state"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"2015 maine state pumpkin and squash weigh off"` · `task.url:"2015 maine state"` · `domain:en.wikipedia.org`
- google: `"2015 maine state pumpkin and squash weigh off"`

### 28. "cape argus cycle tour in september 1978"
- **openai-simpleqa:simpleqa-01371** — What time (hours, minutes, and seconds) did Lawrence Whittaker finish in when he won the first Cape Town Cycle Tour, formerly known as the Cape Argus Cycle Tour, in September 1978?
- why: Rare event + month-year (Cape Argus Cycle Tour, September 1978) — South African sports history; pairs with capetowncycletour.com.
- urlquery: `q="cape argus cycle tour in september 1978"` · tokens: `q="cape argus cycle"` · domain: `url.domain:capetowncycletour.com`
- urlscan: `page.title:"cape argus cycle tour in september 1978"` · `task.url:"cape argus cycle"` · `domain:capetowncycletour.com`
- google: `"cape argus cycle tour in september 1978"`

### 29. "shri hari om ashram prerit vikram sarabhai award"
- **openai-simpleqa:simpleqa-01199** — In which year did Pramod Kale (an Indian engineer) win the Shri Hari Om Ashram Prerit Vikram Sarabhai Award for System Analysis and Management Problems?
- why: Rare Indian award name (Shri Hari Om Ashram Prerit Vikram Sarabhai Award) — multi-word proper-noun string, high verbatim survival.
- urlquery: `q="shri hari om ashram prerit vikram sarabhai award"` · tokens: `q="shri hari ashram"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"shri hari om ashram prerit vikram sarabhai award"` · `task.url:"shri hari ashram"` · `domain:en.wikipedia.org`
- google: `"shri hari om ashram prerit vikram sarabhai award"`

### 30. "american heart association s 1958 heart fund campaign"
- **openai-simpleqa:simpleqa-03822** — What was the name of the painting that Norman Rockwell dedicated to the American Heart Association's 1958 "Heart Fund" campaign?
- why: Org + campaign + year (American Heart Association, 1958 Heart Fund campaign) — pairs with heart.org history PDF.
- urlquery: `q="american heart association s 1958 heart fund campaign"` · tokens: `q="american heart association"` · domain: `url.domain:heart.org 4
https:`
- urlscan: `page.title:"american heart association s 1958 heart fund campaign"` · `task.url:"american heart association"` · `domain:heart.org`
- google: `"american heart association s 1958 heart fund campaign"`

### 31. "1863 george bentham renamed cyanothamnus ramosus"
- **openai-simpleqa:simpleqa-03944** — In 1863, George Bentham renamed *Cyanothamnus ramosus* to what binomial name?
- why: Rare botanist + taxon rename + year (George Bentham, Cyanothamnus ramosus, 1863) — taxonomy-history collocation.
- urlquery: `q="1863 george bentham renamed cyanothamnus ramosus"` · tokens: `q="1863 george bentham"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"1863 george bentham renamed cyanothamnus ramosus"` · `task.url:"1863 george bentham"` · `domain:en.wikipedia.org`
- google: `"1863 george bentham renamed cyanothamnus ramosus"`

### 32. "war of 1812 edward william mcbride"
- **openai-simpleqa:simpleqa-00217** — After the War of 1812, Edward William McBride (1791-1834) worked as what for the king's printer, John Cameron, on the York Gazette until April 1815?
- why: Rare person (Edward William McBride) + War of 1812 — pairs with biographi.ca (Dictionary of Canadian Biography).
- urlquery: `q="war of 1812 edward william mcbride"` · tokens: `q="1812 edward william"` · domain: `url.domain:biographi.ca`
- urlscan: `page.title:"war of 1812 edward william mcbride"` · `task.url:"1812 edward william"` · `domain:biographi.ca`
- google: `"war of 1812 edward william mcbride"`

### 33. "james blasius williams in 1873"
- **openai-simpleqa:simpleqa-03108** — What is the name of the photography partnership that photographed Charles James Blasius Williams in 1873?
- why: Rare person (Charles James Blasius Williams) + year 1873 — pairs with wellcomecollection.org.
- urlquery: `q="james blasius williams in 1873"` · tokens: `q="james blasius williams"` · domain: `url.domain:wellcomecollection.org`
- urlscan: `page.title:"james blasius williams in 1873"` · `task.url:"james blasius williams"` · `domain:wellcomecollection.org`
- google: `"james blasius williams in 1873"`

### 34. "1992 at ieperfest hardcore"
- **openai-simpleqa:simpleqa-01978** — What band opened on Sunday, September 6, 1992, at Ieperfest Hardcore '92 festival?
- why: Rare event (Ieperfest, 1992, hardcore) — Belgian hardcore-punk festival trivia; near-zero background.
- urlquery: `q="1992 at ieperfest hardcore"` · tokens: `q="1992 ieperfest hardcore"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"1992 at ieperfest hardcore"` · `task.url:"1992 ieperfest hardcore"` · `domain:en.wikipedia.org`
- google: `"1992 at ieperfest hardcore"`

### 35. "jamia millia islamia new delhi in 1978"
- **openai-simpleqa:simpleqa-03603** — Name the person appointed as the Vice-Chancellor of Jamia Millia Islamia, New Delhi, in 1978.
- why: Rare org + place + year (Jamia Millia Islamia, New Delhi, 1978) — pairs with jmi.ac.in.
- urlquery: `q="jamia millia islamia new delhi in 1978"` · tokens: `q="jamia millia islamia"` · domain: `url.domain:jmi.ac.in`
- urlscan: `page.title:"jamia millia islamia new delhi in 1978"` · `task.url:"jamia millia islamia"` · `domain:jmi.ac.in`
- google: `"jamia millia islamia new delhi in 1978"`

### 36. "ravel s alborada del gracioso"
- **openai-simpleqa:simpleqa-02159** — On what month, day, and year did Emil Oberhoffer conduct the first performance by the LA Philharmonic of Maurice Ravel's "Alborada del Gracioso"?
- why: Composer + work title (Ravel, Alborada del Gracioso) — classical-music collocation that survives paraphrase.
- urlquery: `q="ravel s alborada del gracioso"` · tokens: `q="ravel alborada gracioso"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"ravel s alborada del gracioso"` · `task.url:"ravel alborada gracioso"` · `domain:en.wikipedia.org`
- google: `"ravel s alborada del gracioso"`

### 37. "kow nkensen arkaah"
- **openai-simpleqa:simpleqa-01821** — Which day, month, and year did former Vice President of Ghana Kow Nkensen Arkaah die?
- why: Rare person (Kow Nkensen Arkaah) — Ghanaian vice-president; the name alone is the fingerprint.
- urlquery: `q="kow nkensen arkaah"` · tokens: `q="nkensen arkaah"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"kow nkensen arkaah"` · `task.url:"nkensen arkaah"` · `domain:en.wikipedia.org`
- google: `"kow nkensen arkaah"`

### 38. "detecting driver mental fatigue eeg alpha power"
- **openai-simpleqa:simpleqa-02997** — What are the four classifications of techniques and methodologies for mental fatigue measurement mentioned in Faramarz Gharagozlou et al.'s 2015 research paper, "Detecting Driver Mental Fatigue Based on EEG Alpha Power C
- why: Paper topic + method (driver mental fatigue, EEG alpha power) — research-paper fingerprint; pairs with ncbi.nlm.nih.gov / researchgate.net.
- urlquery: `q="detecting driver mental fatigue eeg alpha power"` · tokens: `q="detecting driver mental"` · domain: `url.domain:ncbi.nlm.nih.gov`
- urlscan: `page.title:"detecting driver mental fatigue eeg alpha power"` · `task.url:"detecting driver mental"` · `domain:ncbi.nlm.nih.gov`
- google: `"detecting driver mental fatigue eeg alpha power"`

### 39. "edmonton oilers captain connor mcdavid"
- **google-frames:frames-0672** — Which Colombian cyclist was born on the same day as Edmonton Oilers captain Connor McDavid?
- why: Multi-hop combo: Colombian cyclist + Edmonton Oilers captain Connor McDavid — the FRAMES-style cross-entity join is itself the signal; agents fetch both pages.
- urlquery: `q="edmonton oilers captain connor mcdavid"` · tokens: `q="edmonton oilers captain"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"edmonton oilers captain connor mcdavid"` · `task.url:"edmonton oilers captain"` · `domain:en.wikipedia.org`
- google: `"edmonton oilers captain connor mcdavid"`

### 40. "1988 world indoor bowls championship"
- **google-frames:frames-0731** — How old were the winners of the Men's Pairs division at the 1988 World Indoor Bowls Championship?
- why: Rare event (1988 World Indoor Bowls Championship, Men's Pairs) — niche sports trivia, year-anchored.
- urlquery: `q="1988 world indoor bowls championship"` · tokens: `q="1988 world indoor"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"1988 world indoor bowls championship"` · `task.url:"1988 world indoor"` · `domain:en.wikipedia.org`
- google: `"1988 world indoor bowls championship"`

### 41. "eagle awards favourite specialist comics publication"
- **google-frames:frames-0536** — What was the pseudonym of one of the co-founders of the Eagle Awards that won Favourite Specialist Comics Publication/Trade Publication 1977 and 1978?
- why: Eagle Awards + 'Favourite Specialist Comics Publication' — UK comics-history collocation.
- urlquery: `q="eagle awards favourite specialist comics publication"` · tokens: `q="eagle awards favourite"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"eagle awards favourite specialist comics publication"` · `task.url:"eagle awards favourite"` · `domain:en.wikipedia.org`
- google: `"eagle awards favourite specialist comics publication"`

### 42. "lower klamath national wildlife refuge"
- **google-frames:frames-0667** — In 1966, the Lower Klamath National Wildlife Refuge became part of the U.S. National Register of Historic Places (NRHP). What is another natural site with water added during that year, also located in California?
- why: Place name (Lower Klamath National Wildlife Refuge) + year 1966 — US conservation-history collocation.
- urlquery: `q="lower klamath national wildlife refuge"` · tokens: `q="lower klamath national"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"lower klamath national wildlife refuge"` · `task.url:"lower klamath national"` · `domain:en.wikipedia.org`
- google: `"lower klamath national wildlife refuge"`

### 43. "1994 linus roache starred in priest"
- **google-frames:frames-0563** — In 1994, Linus Roache starred in Priest. Who composed the music on his next film?
- why: Actor + film + year (Linus Roache, Priest, 1994) — filmography collocation.
- urlquery: `q="1994 linus roache starred in priest"` · tokens: `q="1994 linus roache"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"1994 linus roache starred in priest"` · `task.url:"1994 linus roache"` · `domain:en.wikipedia.org`
- google: `"1994 linus roache starred in priest"`

### 44. "2025 according to petrovietnam oil corporation pvoil"
- **sealqa:seal-0-0063** — What was the official retail price per liter (in VND, inclusive of VAT and environmental tax) of RON 92-III gasoline on April 24, 2025, according to PetroVietnam Oil Corporation (PVOIL)?
- why: Rare org + product + date (PetroVietnam/PVOIL, RON 92-III gasoline, April 24 2025) — Vietnamese fuel-price trivia; pairs with pvoil.com.vn. SealQA long-tail style.
- urlquery: `q="2025 according to petrovietnam oil corporation pvoil"` · tokens: `q="2025 according petrovietnam"` · domain: `url.domain:pvoil.com.vn`
- urlscan: `page.title:"2025 according to petrovietnam oil corporation pvoil"` · `task.url:"2025 according petrovietnam"` · `domain:pvoil.com.vn`
- google: `"2025 according to petrovietnam oil corporation pvoil"`

### 45. "meta quest models released after 2023 use touch"
- **sealqa:seal-hard-0027** — Which Meta Quest models released after 2023 use Touch Plus controllers and have 6 cameras?
- why: Product line + feature constraint (Meta Quest models after 2023, Touch Plus, 6 cameras) — spec-sheet fingerprint; agents hit spec pages.
- urlquery: `q="meta quest models released after 2023 use touch"` · tokens: `q="meta quest models"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"meta quest models released after 2023 use touch"` · `task.url:"meta quest models"` · `domain:en.wikipedia.org`
- google: `"meta quest models released after 2023 use touch"`

### 46. "ict development index idi 2024 how many countries"
- **sealqa:seal-0-0051** — According to the ICT Development Index (IDI) 2024, how many countries scored below 25?
- why: Index + year + threshold (ICT Development Index IDI 2024, countries below 25) — UN/ITU data-trivia fingerprint.
- urlquery: `q="ict development index idi 2024 how many countries"` · tokens: `q="development index 2024"` · domain: `url.domain:worldpopulationreview.com`
- urlscan: `page.title:"ict development index idi 2024 how many countries"` · `task.url:"development index 2024"` · `domain:worldpopulationreview.com`
- google: `"ict development index idi 2024 how many countries"`

### 47. "icse 2003 program committee meeting held"
- **webwalkerqa:webwalkerqa-0265** — Where and when was the ICSE 2003 Program Committee Meeting held?
- why: Conference + year + artifact (ICSE 2003 Program Committee meeting) — pairs with icse-conferences.org; academic archaeology no one browses casually.
- urlquery: `q="icse 2003 program committee meeting held"` · tokens: `q="icse 2003 program"` · domain: `url.domain:icse-conferences.org`
- urlscan: `page.title:"icse 2003 program committee meeting held"` · `task.url:"icse 2003 program"` · `domain:icse-conferences.org`
- google: `"icse 2003 program committee meeting held"`

### 48. "玻利维亚乌尤尼碳酸锂工厂项目"
- **webwalkerqa:webwalkerqa-0156** — 玻利维亚乌尤尼碳酸锂工厂项目是在何年何月获得了临时移交证书，并预计在何时出产品？
- why: CJK verbatim: 玻利维亚乌尤尼碳酸锂工厂项目 (Bolivia Uyuni lithium carbonate plant project) — spaceless CJK is highly verbatim-stable; pairs with sinomach.com.cn.
- urlquery: `q="玻利维亚乌尤尼碳酸锂工厂项目"` · tokens: `q="玻利维亚乌尤尼碳酸锂工厂项目"` · domain: `url.domain:sinomach.com.cn`
- urlscan: `page.title:"玻利维亚乌尤尼碳酸锂工厂项目"` · `task.url:"玻利维亚乌尤尼碳酸锂工厂项目"` · `domain:sinomach.com.cn`
- google: `"玻利维亚乌尤尼碳酸锂工厂项目"`

### 49. "drug risperidone when administered as an intramuscular injection"
- **assistantbench:6689e6704ab8ed0342f743ff39cde31b5f0a4e5c2b3bb2433297d4dc98f68740** — Find the mean terminal elimination half-life of the drug "Risperidone" when administered as an intramuscular injection.
- why: Drug + administration route (Risperidone, intramuscular injection, terminal elimination half-life) — pharmacology collocation; assistantbench-style deep research.
- urlquery: `q="drug risperidone when administered as an intramuscular injection"` · tokens: `q="drug risperidone when"` · domain: `—`
- urlscan: `page.title:"drug risperidone when administered as an intramuscular injection"` · `task.url:"drug risperidone when"` · `—`
- google: `"drug risperidone when administered as an intramuscular injection"`

### 50. "league baseball after fernandomania the craze surrounding"
- **assistantbench:2bedecc055920566a97e6f049dc9c722d7a8d46adff62bcb096904e7e3783c04** — Which players also from Navojoa, Mexico played in Major League Baseball after “Fernandomania”, the craze surrounding Los Angeles Dodgers’ pitcher Fernando Valenzuela? (Format the answer as a list of jsons with the keys: 
- why: Event nickname + person (Fernandomania, Fernando Valenzuela, Navojoa Mexico) — baseball-history collocation that survives paraphrase.
- urlquery: `q="league baseball after fernandomania the craze surrounding"` · tokens: `q="league baseball after"` · domain: `url.domain:en.wikipedia.org`
- urlscan: `page.title:"league baseball after fernandomania the craze surrounding"` · `task.url:"league baseball after"` · `domain:en.wikipedia.org`
- google: `"league baseball after fernandomania the craze surrounding"`

## 2. PREDICTED-DOMAIN WATCHLIST (top 30, obscurity × frequency)

Question-count per domain (one count per question even with multiple URLs on the domain).
A burst of urlquery/urlscan submissions to any of these — especially the non-.com academic,
niche-reference, and non-English ones — is itself the trace, no phrase needed.

1. **mathshistory.st-andrews.ac.uk** — 97 questions [openai-simpleqa] — `url.domain:mathshistory.st-andrews.ac.uk`
2. **familysearch.org** — 48 questions [openai-simpleqa] — `url.domain:familysearch.org`
3. **storage.googleapis.com** — 46 questions [openai-mle-bench, openai-simpleqa] — `url.domain:storage.googleapis.com`
4. **allrecipes.com** — 45 questions [webvoyager] — `url.domain:allrecipes.com`
5. **rsc.org** — 43 questions [openai-simpleqa] — `url.domain:rsc.org`
6. **alchetron.com** — 33 questions [openai-simpleqa] — `url.domain:alchetron.com`
7. **discogs.com** — 33 questions [mind2web, openai-simpleqa] — `url.domain:discogs.com`
8. **last.fm** — 31 questions [mind2web, openai-simpleqa] — `url.domain:last.fm`
9. **vgmdb.net** — 30 questions [openai-simpleqa] — `url.domain:vgmdb.net`
10. **findagrave.com** — 28 questions [openai-simpleqa] — `url.domain:findagrave.com`
11. **encyclopedia.com** — 28 questions [openai-simpleqa] — `url.domain:encyclopedia.com`
12. **wikiroulette.co** — 27 questions [openai-simpleqa] — `url.domain:wikiroulette.co`
13. **ncbi.nlm.nih.gov** — 27 questions [openai-mle-bench, openai-simpleqa] — `url.domain:ncbi.nlm.nih.gov`
14. **archives.nypl.org** — 25 questions [openai-simpleqa] — `url.domain:archives.nypl.org`
15. **budget.com** — 24 questions [mind2web] — `url.domain:budget.com`
16. **puebliandoporantioquia.com.co** — 23 questions [openai-simpleqa] — `url.domain:puebliandoporantioquia.com.co`
17. **supremecourt.gov** — 23 questions [assistantbench, openai-simpleqa] — `url.domain:supremecourt.gov`
18. **cs.swust.edu.cn** — 23 questions [webwalkerqa] — `url.domain:cs.swust.edu.cn`
19. **degruyter.com** — 22 questions [openai-simpleqa] — `url.domain:degruyter.com`
20. **ticketcenter.com** — 22 questions [mind2web] — `url.domain:ticketcenter.com`
21. **timesofindia.indiatimes.com** — 21 questions [openai-simpleqa] — `url.domain:timesofindia.indiatimes.com`
22. **newegg.com** — 21 questions [mind2web] — `url.domain:newegg.com`
23. **spothero.com** — 21 questions [mind2web] — `url.domain:spothero.com`
24. **riotgames.com** — 21 questions [webwalkerqa] — `url.domain:riotgames.com`
25. **cs.zju.edu.cn** — 21 questions [webwalkerqa] — `url.domain:cs.zju.edu.cn`
26. **geni.com** — 20 questions [openai-simpleqa] — `url.domain:geni.com`
27. **military-history.fandom.com** — 20 questions [openai-simpleqa] — `url.domain:military-history.fandom.com`
28. **espncricinfo.com** — 19 questions [openai-simpleqa] — `url.domain:espncricinfo.com`
29. **olympedia.org** — 19 questions [openai-simpleqa] — `url.domain:olympedia.org`
30. **gamestop.com** — 19 questions [mind2web] — `url.domain:gamestop.com`

Notable low-frequency / high-obscurity domains (covered in §3 multi-signal rather than ranked here):
`sigplan.org`, `poms.org`, `pvoil.com.vn`, `sinomach.com.cn`, `mb.com.ph`, `asme.org`, `awards.acm.org`,
`demonssouls.wikidot.com`, `sekiroshadowsdietwice.wiki.fextralife.com`, `the1939society.org`, `biographi.ca`,
`wellcomecollection.org`, `jmi.ac.in`, `yili.com`, `icse-conferences.org`, `hellenicaworld.com`, `heart.org`.

## 3. MULTI-SIGNAL QUERIES (phrase + expected domain, strongest joint fingerprints)

How to run: execute the phrase query and the domain query separately on the same surface,
then intersect submitter / timestamp. A joint hit (same submitter, same session window) is
the strongest possible fingerprint — phrase proves the question, domain proves the execution.

1. "1990 wolf prize with ilya iosifovich piatetski shapiro" **AND** `openai-simpleqa:simpleqa-01554` expected domain `mathshistory.st-andrews.ac.uk`
   - urlquery: `q="1990 wolf prize with ilya iosifovich piatetski shapiro"` then `url.domain:mathshistory.st-andrews.ac.uk` — also try token form `q="1990 wolf prize"` before intersecting by date/submitter.
   - urlscan: `page.title:"1990 wolf prize with ilya iosifovich piatetski shapiro"` then `domain:mathshistory.st-andrews.ac.uk` — correlate scan timestamps.

2. "2003 sigplan john c reynolds doctoral dissertation award" **AND** `openai-simpleqa:simpleqa-03048` expected domain `sigplan.org`
   - urlquery: `q="2003 sigplan john c reynolds doctoral dissertation award"` then `url.domain:sigplan.org` — also try token form `q="2003 sigplan john"` before intersecting by date/submitter.
   - urlscan: `page.title:"2003 sigplan john c reynolds doctoral dissertation award"` then `domain:sigplan.org` — correlate scan timestamps.

3. "2015 wickham skinner teaching innovation award" **AND** `webwalkerqa:webwalkerqa-0021` expected domain `poms.org`
   - urlquery: `q="2015 wickham skinner teaching innovation award"` then `url.domain:poms.org` — also try token form `q="2015 wickham skinner"` before intersecting by date/submitter.
   - urlscan: `page.title:"2015 wickham skinner teaching innovation award"` then `domain:poms.org` — correlate scan timestamps.

4. "2025 according to petrovietnam oil corporation pvoil" **AND** `sealqa:seal-0-0063` expected domain `pvoil.com.vn`
   - urlquery: `q="2025 according to petrovietnam oil corporation pvoil"` then `url.domain:pvoil.com.vn` — also try token form `q="2025 according to"` before intersecting by date/submitter.
   - urlscan: `page.title:"2025 according to petrovietnam oil corporation pvoil"` then `domain:pvoil.com.vn` — correlate scan timestamps.

5. "玻利维亚乌尤尼碳酸锂工厂项目" **AND** `webwalkerqa:webwalkerqa-0156` expected domain `sinomach.com.cn`
   - urlquery: `q="玻利维亚乌尤尼碳酸锂工厂项目"` then `url.domain:sinomach.com.cn` — also try token form `q="玻利维亚乌尤尼碳"` before intersecting by date/submitter.
   - urlscan: `page.title:"玻利维亚乌尤尼碳酸锂工厂项目"` then `domain:sinomach.com.cn` — correlate scan timestamps.

6. "worcester reed warner medal in 1934" **AND** `openai-simpleqa:simpleqa-02865` expected domain `asme.org`
   - urlquery: `q="worcester reed warner medal in 1934"` then `url.domain:asme.org` — also try token form `q="worcester reed warner"` before intersecting by date/submitter.
   - urlscan: `page.title:"worcester reed warner medal in 1934"` then `domain:asme.org` — correlate scan timestamps.

7. "2018 acm eugene l lawler award" **AND** `openai-simpleqa:simpleqa-02622` expected domain `awards.acm.org`
   - urlquery: `q="2018 acm eugene l lawler award"` then `url.domain:awards.acm.org` — also try token form `q="2018 acm eugene"` before intersecting by date/submitter.
   - urlscan: `page.title:"2018 acm eugene l lawler award"` then `domain:awards.acm.org` — correlate scan timestamps.

8. "manila bulletin in may 2021 succeeding dr crispulo" **AND** `openai-simpleqa:simpleqa-01723` expected domain `mb.com.ph`
   - urlquery: `q="manila bulletin in may 2021 succeeding dr crispulo"` then `url.domain:mb.com.ph` — also try token form `q="manila bulletin in"` before intersecting by date/submitter.
   - urlscan: `page.title:"manila bulletin in may 2021 succeeding dr crispulo"` then `domain:mb.com.ph` — correlate scan timestamps.

9. "dregling merchant in demon s souls 2009" **AND** `openai-simpleqa:simpleqa-01466` expected domain `demonssouls.wikidot.com`
   - urlquery: `q="dregling merchant in demon s souls 2009"` then `url.domain:demonssouls.wikidot.com` — also try token form `q="dregling merchant in"` before intersecting by date/submitter.
   - urlscan: `page.title:"dregling merchant in demon s souls 2009"` then `domain:demonssouls.wikidot.com` — correlate scan timestamps.

10. "1938 with tadashi nakayama" **AND** `openai-simpleqa:simpleqa-02169` expected domain `mathshistory.st-andrews.ac.uk`
   - urlquery: `q="1938 with tadashi nakayama"` then `url.domain:mathshistory.st-andrews.ac.uk` — also try token form `q="1938 with tadashi"` before intersecting by date/submitter.
   - urlscan: `page.title:"1938 with tadashi nakayama"` then `domain:mathshistory.st-andrews.ac.uk` — correlate scan timestamps.

## 4. SKIP LIST — evals/questions NOT worth hunting (and why)

- **tau-bench (165)** — synthetic airline/retail policy templates, zero live web (`synthetic-policy-no-live-web` marker on all 165). Agents talk to fake tools; there is no public-surface footprint. Skip entirely.
- **openai-mle-bench (82)** — Kaggle competition boilerplate executed in containers. Any web footprint lands on `kaggle.com` (generic, unhuntable at phrase level) and the text is templated ("Overview / Description / Problem Statement"). Skip phrases; keep `kaggle.com` competition-URL monitoring only as background noise.
- **webarena (812)** — all tasks run against six self-hosted environments (`selfhosted:shopping`, `:shopping_admin`, `:gitlab`, `:reddit`, `:map`, `:wikipedia`). No live-web footprints exist by construction. Skip entirely.
- **google-facts-grounding (860)** — 553/860 carry `context-provided-no-web-needed`: the grounding document ships with the question, so a competent agent never browses. The remaining ~307 are long-form explain/compare prompts with weak fingerprints. Skip (lowest priority if anything).
- **mind2web (1009) / webvoyager (643) — phrases skip, DOMAINS watch.** Their fingerprint phrases are templated navigation instructions ("find the cheapest one-way flight…", "find climbing gear and sort by price") — paraphrase-fragile and generic. The trace here is domain bursts on the task sites (`budget.com`, `ticketcenter.com`, `newegg.com`, `spothero.com`, `rei.com`, `allrecipes.com`, `wolframalpha.com`) — covered in §2, not §1.
- **High-df boilerplate anywhere** — the enrichment already penalized it via n-gram df (tau-bench instruction templates, mle-bench Kaggle headers, webarena task templates all scored ~0). If a "fingerprint" reads like instructions rather than content, it's not a fingerprint.

## 5. SURFACE NOTES — how an EXECUTED (not pasted) question appears per surface

The core insight: agents don't paste eval questions into urlquery — they *execute* them, and execution leaks sideways.

- **urlquery.net submissions.** What lands: (a) the agent's **search-engine URLs** — `google.com/search?q=…` / `bing.com/search?q=…` with the agent's query terms, so `q=` token-pair queries (§1 "tokens" variant) catch paraphrased searches; (b) **expected-source page visits** — `url.domain:` bursts on §2 domains (e.g. five submissions to `mathshistory.st-andrews.ac.uk` biography pages in ten minutes = a SimpleQA math run); (c) **title capture** — urlquery records the visited page's title on the report page, so an agent query like "1990 Wolf Prize Piatetski-Shapiro" typed into a search box can surface in the report's title field even when the URL doesn't contain it. Scope with `date:[YYYY-MM-DD TO YYYY-MM-DD]` and `tags:` once a candidate cluster is found.
- **urlscan.io.** Same two channels: `task.url:` for search-engine/agent query URLs, `page.title:` for verbatim question fragments in page titles (agents that open a search results page or a "questions" page leak the query into the title), and `domain:` for expected-source bursts. urlscan also captures the scan's **source / submitter context** — correlate timestamps across the §3 multi-signal pairs.
- **Google verbatim (`"…"`).** Pre-flight validation, not the hunt itself: a clean phrase should return ~0 results or only the eval repo. If it returns forum posts or "cheat" mirrors, the phrase is contaminated — demote it. (dsqa_250 precedent: the verbatim question existed in exactly one incident-relevant place.)
- **Web archives (Wayback CDX, Arquivo.pt, Megalodon).** Agents don't create captures by fetching, but two patterns matter: (a) agents that use `web.archive.org` *as a source* leave timestamped snapshot fetches in CDX logs — a burst of fetches for the same snapshot URL is agent-shaped; (b) passive captures of expected-source pages (e.g. a `pvoil.com.vn` fuel-price page captured days after the SealQA question's reference date) corroborate timing.
- **Request-logging endpoints (httpbun-style dead drops).** Per our own prior work, agents use request-logging endpoints as scratchpads — query parameters and echoed bodies can contain verbatim question fragments. On urlquery, `q=httpbun` / `q=webhook.site` style searches find the submissions; the fragment then appears in the logged request data on the endpoint's own page.
- **CJK note.** WebWalkerQA's 433 CJK questions tokenize per-character and are rejoined spaceless — search them spaceless and verbatim (e.g. `q="玻利维亚乌尤尼碳酸锂"`). Spaceless CJK has extremely low collision rates; even short fragments are strong.

## 6. CROSS-REFERENCE RESULT — silent-locus tree sweep (2026-10-05)

Method: top 200 ranked fingerprint phrases (lowest df, entity-bearing, incl. spaceless CJK) literal-matched with `rg -F -f patterns` across the whole `~/workspace/silent-locus` tree, excluding `collections/eval-questions/` (the corpus itself) and `.git/**`. 7,498 files searched.

**Result: ZERO hits.** No top-200 fingerprint phrase appears anywhere else in the tree — not in notes, corpora, assessments, or incident-discovery material. (Sanity-checked: the same patterns match 2/2 in `all-questions.jsonl`, so the patterns and the search are valid.)

Interpretation: unlike dsqa_250 (which verbatim-matched the June-17 DoE incident task), none of these 200 fingerprints have been previously observed in our holdings. The hunt queries in §1–§3 are therefore greenfield — any future hit is novel signal, not a re-find.
