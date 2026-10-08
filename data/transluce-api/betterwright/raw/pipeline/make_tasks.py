"""Synthesize real-web browser tasks with the local Qwen server, grounded on a live
excerpt of each site. Appends to tasks/pool.jsonl until --target tasks exist.

  python3 make_tasks.py --target 4000 --concurrency 6
"""
import argparse, json, os, re, random, hashlib, html, threading, time, datetime, urllib.request

W = "/job/work"
POOL = f"{W}/tasks/pool.jsonl"
API = "http://127.0.0.1:30010/v1/chat/completions"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"

# (url, category, mode, hint)  mode: read = read-only public site; sandbox = practice site built for automation; tool = interactive web app without accounts
SITES = [
 ("https://en.wikipedia.org", "reference", "read", "encyclopedia; infoboxes, tables, history, categories, language links"),
 ("https://www.wikidata.org", "reference", "read", "structured entities, statements, identifiers"),
 ("https://en.wikivoyage.org", "travel", "read", "travel guides: get in, see, do, eat, sleep sections"),
 ("https://en.wiktionary.org", "reference", "read", "definitions, etymology, translations"),
 ("https://commons.wikimedia.org", "reference", "read", "media files, categories, licensing info"),
 ("https://openlibrary.org", "books", "read", "book search, editions, authors, subjects"),
 ("https://www.gutenberg.org", "books", "read", "public-domain ebooks, top lists, bookshelves, formats"),
 ("https://archive.org", "reference", "read", "collections search, metadata, Wayback Machine"),
 ("https://arxiv.org", "science", "read", "paper search, listings by category, abstracts, versions"),
 ("https://pubmed.ncbi.nlm.nih.gov", "science", "read", "biomedical literature search with filters"),
 ("https://www.semanticscholar.org", "science", "read", "paper search, citations, authors"),
 ("https://dblp.org", "science", "read", "CS bibliography, author pages, venues"),
 ("https://www.biorxiv.org", "science", "read", "preprints by subject, search"),
 ("https://journals.plos.org/plosone/", "science", "read", "open-access articles, search and filters"),
 ("https://clinicaltrials.gov", "health", "read", "trial search with status/phase/location filters"),
 ("https://github.com", "dev", "read", "repos, releases, issues, PRs, code search limited without login, trending"),
 ("https://pypi.org", "dev", "read", "python packages, release history, metadata, classifiers"),
 ("https://www.npmjs.com", "dev", "read", "packages, versions, dependencies, weekly downloads"),
 ("https://crates.io", "dev", "read", "rust crates, versions, downloads, dependencies"),
 ("https://pkg.go.dev", "dev", "read", "go packages docs, versions, imports"),
 ("https://rubygems.org", "dev", "read", "gems, versions, dependencies"),
 ("https://packagist.org", "dev", "read", "php packages, stats"),
 ("https://hub.docker.com", "dev", "read", "images, tags, pulls, official images"),
 ("https://huggingface.co", "dev", "read", "models, datasets, spaces; filters, model cards, files"),
 ("https://docs.python.org/3/", "dev", "read", "python docs, library reference, changelog"),
 ("https://developer.mozilla.org", "dev", "read", "web docs, browser compatibility tables"),
 ("https://caniuse.com", "dev", "read", "browser support tables"),
 ("https://stackoverflow.com", "dev", "read", "questions, tags, votes, accepted answers"),
 ("https://news.ycombinator.com", "news", "read", "front page, past, ask/show, comments, user pages"),
 ("https://lobste.rs", "news", "read", "stories by tag, comments"),
 ("https://hn.algolia.com", "news", "read", "HN search with date/points filters"),
 ("https://www.sqlite.org", "dev", "read", "docs, release history, changelog"),
 ("https://www.postgresql.org/docs/", "dev", "read", "manuals by version, release notes"),
 ("https://nodejs.org", "dev", "read", "releases, docs, changelogs"),
 ("https://go.dev", "dev", "read", "release notes, docs, blog"),
 ("https://www.rust-lang.org", "dev", "read", "blog, releases, docs links"),
 ("https://kernel.org", "dev", "read", "kernel versions and release dates"),
 ("https://codeberg.org/explore/repos", "dev", "read", "explore repositories, sort, topics"),
 ("https://gitlab.com/explore", "dev", "read", "explore projects, stars, topics"),
 ("https://www.weather.gov", "gov", "read", "US forecasts by city, alerts, hourly tables"),
 ("https://earthquake.usgs.gov/earthquakes/map/", "gov", "read", "recent earthquakes list, magnitude filters, event pages"),
 ("https://www.nasa.gov", "gov", "read", "missions, news, image of the day"),
 ("https://data.gov", "gov", "read", "dataset catalog search with filters"),
 ("https://www.census.gov", "gov", "read", "quickfacts, population data"),
 ("https://www.bls.gov", "gov", "read", "CPI, unemployment, data tables"),
 ("https://www.federalregister.gov", "gov", "read", "document search with agency/type/date filters"),
 ("https://www.congress.gov", "gov", "read", "bills search, status, sponsors"),
 ("https://www.loc.gov", "gov", "read", "digital collections search"),
 ("https://www.nps.gov", "gov", "read", "parks finder, fees, alerts, hours"),
 ("https://www.cdc.gov", "health", "read", "health topics, data"),
 ("https://www.who.int", "health", "read", "fact sheets, news, data"),
 ("https://ourworldindata.org", "data", "read", "charts, data explorers, articles"),
 ("https://data.worldbank.org", "data", "read", "indicators by country, tables"),
 ("https://fred.stlouisfed.org", "data", "read", "economic series search, latest observations"),
 ("https://fiscaldata.treasury.gov", "data", "read", "debt to the penny, datasets"),
 ("https://www.eia.gov", "data", "read", "energy prices, state profiles"),
 ("https://www.usa.gov", "gov", "read", "government services directory"),
 ("https://www.gov.uk", "gov", "read", "services, guidance, bank holidays, visas"),
 ("https://www.ons.gov.uk", "data", "read", "UK statistics releases"),
 ("https://ec.europa.eu/eurostat", "data", "read", "EU statistics, news releases"),
 ("https://www.usajobs.gov", "jobs", "read", "federal job search with filters"),
 ("https://www.recalls.gov", "gov", "read", "recall listings links"),
 ("https://www.fda.gov", "health", "read", "recalls, drug approvals, press"),
 ("https://www.bbc.com/news", "news", "read", "news sections, articles"),
 ("https://www.npr.org", "news", "read", "news sections, programs"),
 ("https://apnews.com", "news", "read", "top news, topics"),
 ("https://www.theguardian.com/international", "news", "read", "sections, articles, live"),
 ("https://www.aljazeera.com", "news", "read", "news by region"),
 ("https://www.dw.com/en/", "news", "read", "news by topic/region"),
 ("https://arstechnica.com", "news", "read", "tech articles by section, authors"),
 ("https://www.theverge.com", "news", "read", "tech news, reviews"),
 ("https://techcrunch.com", "news", "read", "startup news, categories"),
 ("https://phys.org", "science", "read", "science news by topic"),
 ("https://www.sciencedaily.com", "science", "read", "research news by topic"),
 ("https://www.quantamagazine.org", "science", "read", "long-form science articles"),
 ("https://www.smithsonianmag.com", "reference", "read", "history/science articles"),
 ("https://www.propublica.org", "news", "read", "investigations, data tools"),
 ("https://www.ebay.com", "shopping", "read", "search, filters (condition, price, buy it now), sort, item specifics"),
 ("https://www.ikea.com/us/en/", "shopping", "read", "product search, filters, dimensions, prices"),
 ("https://www.newegg.com", "shopping", "read", "PC components search, specs filters, sort"),
 ("https://www.adafruit.com", "shopping", "read", "electronics catalog, stock, prices, categories"),
 ("https://www.sparkfun.com", "shopping", "read", "electronics catalog, specs, prices"),
 ("https://www.thriftbooks.com", "shopping", "read", "used books search, conditions, prices"),
 ("https://www.abebooks.com", "shopping", "read", "rare/used book search with filters"),
 ("https://bookshop.org", "shopping", "read", "books, lists, prices"),
 ("https://www.goodreads.com", "books", "read", "ratings, lists, editions, quotes"),
 ("https://www.lego.com/en-us", "shopping", "read", "sets by theme, piece counts, prices, age"),
 ("https://www.rei.com", "shopping", "read", "outdoor gear filters, specs, reviews"),
 ("https://www.bhphotovideo.com", "shopping", "read", "camera gear specs and filters"),
 ("https://www.microcenter.com", "shopping", "read", "PC parts, store availability"),
 ("https://www.decathlon.com", "shopping", "read", "sports gear, filters"),
 ("https://craigslist.org", "shopping", "read", "classifieds by city/category, filters"),
 ("https://www.openstreetmap.org", "maps", "read", "place search, directions, map features"),
 ("https://www.timeanddate.com", "reference", "read", "world clock, time zones, sun/moon, holidays, date calculators"),
 ("https://www.flightaware.com", "travel", "read", "flight status, airport boards"),
 ("https://www.seat61.com", "travel", "read", "train travel guides by route"),
 ("https://www.rome2rio.com", "travel", "read", "route options between places"),
 ("https://www.nationalrail.co.uk", "travel", "read", "UK train journey planner"),
 ("https://www.sbb.ch/en", "travel", "read", "Swiss timetable planner"),
 ("https://www.bahn.com/en", "travel", "read", "German rail journey planner"),
 ("https://www.booking.com", "travel", "read", "hotel search with dates, filters, sort (no booking)"),
 ("https://www.hostelworld.com", "travel", "read", "hostel search, ratings, prices"),
 ("https://www.google.com/travel/flights", "travel", "read", "flight search, date grid, filters (no booking)"),
 ("https://www.imdb.com", "entertainment", "read", "titles, cast, ratings, charts, advanced search"),
 ("https://www.themoviedb.org", "entertainment", "read", "movies/TV, cast, release dates, discover filters"),
 ("https://www.rottentomatoes.com", "entertainment", "read", "tomatometer, audience scores, lists"),
 ("https://www.metacritic.com", "entertainment", "read", "metascores, best-of lists by platform/year"),
 ("https://musicbrainz.org", "entertainment", "read", "artists, releases, recordings, relationships"),
 ("https://www.discogs.com", "entertainment", "read", "releases, labels, marketplace stats"),
 ("https://www.last.fm", "entertainment", "read", "artist stats, top tracks, tags"),
 ("https://bandcamp.com", "entertainment", "read", "discover by genre/tag, album pages"),
 ("https://boardgamegeek.com", "entertainment", "read", "game ranks, weights, player counts, advanced search"),
 ("https://store.steampowered.com", "entertainment", "read", "game search, tags, reviews summary, prices"),
 ("https://itch.io", "entertainment", "read", "indie games browse by tag/price/platform"),
 ("https://myanimelist.net", "entertainment", "read", "anime/manga rankings, seasons, details"),
 ("https://letterboxd.com", "entertainment", "read", "film pages, lists, ratings"),
 ("https://www.speedrun.com", "entertainment", "read", "leaderboards by game/category"),
 ("https://lichess.org", "games", "tool", "play vs computer anonymously, puzzles, opening explorer, analysis board, tournaments list"),
 ("https://www.allrecipes.com", "food", "read", "recipes search, ratings, ingredients, nutrition"),
 ("https://www.bbcgoodfood.com", "food", "read", "recipes, collections, filters"),
 ("https://www.seriouseats.com", "food", "read", "recipes and techniques"),
 ("https://world.openfoodfacts.org", "food", "read", "product search, nutri-score, ingredients"),
 ("https://fdc.nal.usda.gov", "food", "read", "USDA food nutrient search"),
 ("https://www.espn.com", "sports", "read", "scores, standings, schedules, stats"),
 ("https://www.transfermarkt.com", "sports", "read", "football player values, transfers, squads"),
 ("https://www.olympics.com", "sports", "read", "results, medal tables, athletes"),
 ("https://www.formula1.com", "sports", "read", "standings, race results, schedule"),
 ("https://www.nba.com", "sports", "read", "standings, stats leaders, schedule"),
 ("https://finance.yahoo.com", "finance", "read", "quotes, historical data tables, statistics"),
 ("https://www.coingecko.com", "finance", "read", "crypto prices, market cap ranks, categories, historical"),
 ("https://www.xe.com", "finance", "read", "currency converter and charts"),
 ("https://tradingeconomics.com", "finance", "read", "indicators by country, tables"),
 ("https://www.marketwatch.com", "finance", "read", "markets data, quotes"),
 ("https://www.khanacademy.org", "education", "read", "course catalog, units, lessons"),
 ("https://ocw.mit.edu", "education", "read", "course search by topic/level, syllabi, materials"),
 ("https://www.classcentral.com", "education", "read", "MOOC search, filters, rankings"),
 ("https://www.coursera.org", "education", "read", "course search, filters, syllabi (no enrollment)"),
 ("https://www.edx.org", "education", "read", "course search and details (no enrollment)"),
 ("https://remoteok.com", "jobs", "read", "remote jobs by tag, salary filters"),
 ("https://weworkremotely.com", "jobs", "read", "remote job listings by category"),
 ("https://duckduckgo.com", "search", "read", "web search, instant answers; use to discover sources then open first-party pages"),
 ("https://search.brave.com", "search", "read", "web search; discover then verify on source pages"),
 ("https://www.bing.com", "search", "read", "web search; discover then verify on source pages"),
 ("https://www.saucedemo.com", "sandbox-shop", "sandbox", "demo store; public logins standard_user / problem_user / performance_glitch_user, password secret_sauce; sort, cart, checkout with fake info"),
 ("https://www.demoblaze.com", "sandbox-shop", "sandbox", "demo electronics store; categories, product pages, cart, place order with fake data; sign-up allowed with throwaway fake credentials"),
 ("https://automationexercise.com", "sandbox-shop", "sandbox", "practice e-commerce: products, search, brands, cart, contact form, subscription, test cases; fake sign-up allowed"),
 ("https://the-internet.herokuapp.com", "sandbox-ui", "sandbox", "UI challenges: login (tomsmith / SuperSecretPassword!), dropdown, checkboxes, dynamic loading, tables, drag and drop, iframes, hovers, key presses, file download list, infinite scroll, shadow DOM, sortable tables, JS alerts, nested frames"),
 ("https://demoqa.com", "sandbox-ui", "sandbox", "practice forms, web tables, widgets (date picker, slider, tabs, tooltips), interactions (sortable, droppable), book store app"),
 ("https://practice.expandtesting.com", "sandbox-ui", "sandbox", "many practice pages: login, forms, tables, drag-drop, dynamic content, notes app, OTP, shadow DOM, locators"),
 ("https://books.toscrape.com", "sandbox-scrape", "sandbox", "1000 fake books over 50 pages and ~50 categories; price, rating, stock, UPC on detail pages"),
 ("https://quotes.toscrape.com", "sandbox-scrape", "sandbox", "quotes with authors/tags, pagination, author bio pages, login (any user/pass), JS/infinite-scroll/table variants under /js /scroll /tableful"),
 ("https://webscraper.io/test-sites", "sandbox-scrape", "sandbox", "e-commerce test sites with pagination, AJAX, load-more and scroll variants; laptops/tablets/phones with specs and prices"),
 ("https://www.scrapethissite.com/pages/", "sandbox-scrape", "sandbox", "countries list, hockey team stats with search+pagination, Oscar films AJAX, frames, advanced topics"),
 ("http://uitestingplayground.com", "sandbox-ui", "sandbox", "tricky UI: dynamic IDs, class attribute, hidden layers, load delay, AJAX data, client delay, click, text input, scrollbars, dynamic table, verify text, progress bar, visibility, sample app, mouse over, shadow DOM, overlapped element"),
 ("https://todomvc.com/examples/react/dist/", "sandbox-app", "sandbox", "todo app: add, edit (double click), complete, filter, clear completed"),
 ("https://www.selenium.dev/selenium/web/web-form.html", "sandbox-ui", "sandbox", "single web form with text, password, textarea, select, datalist, file, checkbox, radio, color, date, range"),
 ("https://practicetestautomation.com/practice/", "sandbox-ui", "sandbox", "test login page (student / Password123), exceptions page with dynamic rows, table practice"),
 ("https://parabank.parasoft.com", "sandbox-bank", "sandbox", "demo bank: register a fake customer, open accounts, transfer funds, bill pay, find transactions, request loan"),
 ("https://opensource-demo.orangehrmlive.com", "sandbox-app", "sandbox", "OrangeHRM demo (Admin / admin123): PIM employees, leave, recruitment, directory, admin users, search and filters; demo data resets"),
 ("https://ecommerce-playground.lambdatest.io", "sandbox-shop", "sandbox", "OpenCart demo store: categories, filters, compare, wishlist, cart, guest checkout with fake data, blog"),
 ("https://magento.softwaretestingboard.com", "sandbox-shop", "sandbox", "Magento demo store: layered navigation filters, size/color options, cart, compare, guest checkout with fake data"),
 ("https://demo.realworld.show", "sandbox-app", "sandbox", "Conduit blogging demo: global feed, tags, article pages, profiles; fake sign-up allowed"),
 ("https://testpages.eviltester.com/styled/index.html", "sandbox-ui", "sandbox", "many test pages: forms, tables, dynamic tables, alerts, frames, drag drop, calculators, basic apps, redirects, cookies"),
 ("https://qa-practice.netlify.app", "sandbox-ui", "sandbox", "practice: forms, dynamic tables, e-commerce login flow, file upload, iframes, pagination, date pickers, spot-the-bugs"),
 ("https://letcode.in/test", "sandbox-ui", "sandbox", "practice widgets: inputs, buttons, select, alerts, frames, radio, windows, elements (github user lookup), drag, drop, sort, multi-select, slider, tables, calendar, forms"),
 ("https://www.globalsqa.com/demo-site/", "sandbox-ui", "sandbox", "demo widgets: tabs, sliders, tooltips, dialogs, datepicker, sorting, drag and drop, progress bar, frames, dropdown menus, banking project (AngularJS)"),
 ("https://www.globalsqa.com/angularJs-protractor/BankingProject/", "sandbox-bank", "sandbox", "XYZ Bank demo: customer login by name, deposit, withdraw, transactions; manager adds customers/opens accounts"),
 ("https://jqueryui.com/demos/", "sandbox-ui", "sandbox", "widget demos inside iframes: draggable, droppable, resizable, selectable, sortable, accordion, autocomplete, datepicker, slider, spinner, tabs"),
 ("https://datatables.net/examples/index", "sandbox-ui", "sandbox", "table examples: search, sort, paginate, column filters, child rows"),
 ("https://www.ag-grid.com/example/", "sandbox-ui", "sandbox", "big data grid demo: filter, sort, group, column tools"),
 ("https://httpbin.org/forms/post", "sandbox-ui", "sandbox", "pizza order form that echoes submitted data as JSON"),
 ("https://excalidraw.com", "tool", "tool", "whiteboard: shapes, arrows, text, keyboard shortcuts; verify via DOM/localStorage scene data"),
 ("https://play2048.co", "games", "tool", "2048 game: arrow keys; read tile grid from DOM; report score/max tile"),
 ("https://sudoku.com", "games", "tool", "sudoku boards; easier alternative sites acceptable if blocked"),
 ("https://minesweeperonline.com", "games", "tool", "classic minesweeper; read board from DOM"),
 ("https://www.desmos.com/calculator", "tool", "tool", "graphing calculator: enter expressions, read intersections/values"),
 ("https://www.calculator.net", "tool", "tool", "many calculators: mortgage, BMI, date, loan, percentage; fill forms and read results"),
 ("https://www.omnicalculator.com", "tool", "tool", "thousands of calculators; fill fields, read outputs"),
 ("https://regex101.com", "tool", "tool", "regex tester: enter pattern/test string, read matches and explanation"),
 ("https://www.wolframalpha.com", "tool", "tool", "computational queries; read result pods (some limits without login)"),
 ("https://app.diagrams.net", "tool", "tool", "diagram editor (choose device storage / decide later); add shapes and labels"),
 ("https://monkeytype.com", "tool", "tool", "typing test; settings; read results"),
 ("https://jsonformatter.org", "tool", "tool", "format/validate/convert JSON in the browser"),
 ("https://crontab.guru", "tool", "tool", "cron expression explainer"),
 ("https://www.epochconverter.com", "tool", "tool", "timestamp conversion forms"),
]

TIERS = {
 "short": "SHORT: 1-4 browser tool calls. One page or one simple search; a single fact, value, or one simple interaction.",
 "medium": "MEDIUM: roughly 5-12 browser tool calls. Needs search/filter/sort, pagination, a multi-field form, or comparing 2-4 items across a few pages.",
 "long": "LONG: roughly 12-30 browser tool calls. Multi-page extraction (8-15 items with details), a complete multi-stage flow, or cross-checking facts across 2-3 different websites, ending in a structured deliverable.",
 "very_long": "VERY LONG: 30-100+ browser tool calls, typically 45-120 minutes of work. Exhaustive multi-page crawls with aggregation, research dossiers across 4-8 websites with a source-cited table, long multi-stage workflows in a demo app with verification after each stage, or long interactive sessions (games, editors). Must clearly require sustained work; state the full deliverable format precisely.",
}
TIER_WEIGHTS = [("short", 0.28), ("medium", 0.34), ("long", 0.26), ("very_long", 0.12)]
STYLES = [
 "a terse power user (one or two short sentences)", "a friendly non-technical person writing casually", "a busy professional who specifies the exact output format (table/JSON/bullets)",
 "a student doing research who explains the purpose briefly", "someone typing quickly on a phone with a typo or two and lowercase", "a QA engineer writing precise numbered acceptance criteria",
 "a data analyst who wants numbers with units and the source URL for each", "a non-native English speaker writing simply", "a detail-oriented planner listing constraints explicitly",
]
KINDS = {
 "read": ["fact lookup", "filtered search and extraction", "comparison of several items", "ranking / top-N with sort order taken from the site", "aggregation (count, sum, average) over listed items", "timeline or changelog extraction", "cross-site verification of a fact", "find the item matching several constraints", "navigate deep into a site section and summarise a specific page", "table extraction into a structured format"],
 "sandbox": ["complete an end-to-end flow and report the confirmation details", "fill a complex form and verify the submitted values", "solve tricky UI challenges and report what happened", "scrape and aggregate data across paginated pages", "stateful multi-step workflow with verification of the resulting state", "find an item by constraints, act on it, verify the cart/table/result", "exercise several widgets and report their final values"],
 "tool": ["use the web app to produce a concrete result and report it", "play/solve as far as possible under explicit rules and report the final state", "compute several values with the tool and report them in a table", "build a small artifact in the editor and verify it via the page state"],
}

def fetch_excerpt(url, cache={}):
    if url in cache: return cache[url]
    text = ""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*", "Accept-Language": "en-US,en;q=0.9"})
        raw = urllib.request.urlopen(req, timeout=20).read(600000).decode("utf-8", "ignore")
        raw = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", raw)
        title = re.search(r"(?is)<title[^>]*>(.*?)</title>", raw)
        links = re.findall(r'(?is)<a[^>]+href="([^"#]{2,120})"[^>]*>(.*?)</a>', raw)
        body = html.unescape(re.sub(r"\s+", " ", re.sub(r"(?s)<[^>]+>", " ", raw))).strip()
        nav = "; ".join(dict.fromkeys(f"{html.unescape(re.sub(r'<[^>]+>', '', t)).strip()[:40]} -> {h}" for h, t in links if re.sub(r"<[^>]+>", "", t).strip())) [:1500]
        text = f"TITLE: {html.unescape(title.group(1)).strip() if title else ''}\nTEXT: {body[:2200]}\nLINKS: {nav}"
    except Exception as e:
        text = f"(homepage excerpt unavailable: {type(e).__name__}; rely on widely known, stable features of the site)"
    cache[url] = text
    return text

def chat(prompt, max_tokens=7000):
    body = {"model": "qwen3.8-flash-next", "messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens,
            "chat_template_kwargs": {"enable_thinking": True, "reasoning_effort": "low"}, "temperature": 1.0, "top_p": 0.95}
    req = urllib.request.Request(API, data=json.dumps(body).encode(), headers={"content-type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=1200))["choices"][0]["message"].get("content") or ""

def build_prompt(rnd, tier):
    primary = rnd.choice(SITES)
    sites = [primary]
    if tier in ("long", "very_long") and primary[2] == "read" and rnd.random() < (0.55 if tier == "long" else 0.85):
        extra = rnd.sample([s for s in SITES if s[2] == "read" and s[0] != primary[0]], rnd.choice([1, 2] if tier == "long" else [2, 3, 4]))
        sites += extra
    mode = primary[2]
    kinds = rnd.sample(KINDS[mode], min(3, len(KINDS[mode])))
    style = rnd.sample(STYLES, 3)
    feature = rnd.random()
    special = ""
    if feature < 0.12:
        special = 'SPECIAL: make task #1 deliberately under-specified in ONE important detail (e.g. which city, which size, which date range) so that a careful agent must ask the user a clarifying question. For that task add "ask_profile": {"<detail name>": "<the user\'s private answer>", ...} with 2-4 private facts.'
    elif feature < 0.26:
        special = 'SPECIAL: for task #1 add a "followup" field: a natural second request the same user sends after the first one is done, which builds on the results of the first task in the same browser session (roughly medium effort).'
    today = datetime.date.today().isoformat()
    blocks = []
    for url, cat, m, hint in sites:
        blocks.append(f"SITE: {url}\nCATEGORY: {cat} | MODE: {m}\nKNOWN FEATURES: {hint}\nLIVE HOMEPAGE EXCERPT:\n{fetch_excerpt(url)}")
    rules_mode = {
        "read": "These are live public websites: tasks must be READ-ONLY (search, filter, sort, navigate, extract, compare). Never require login, sign-up, purchases, bookings, posting, messaging, or submitting contact forms.",
        "sandbox": "This is a practice/demo site built for automation: tasks SHOULD involve real interaction (forms, carts, fake checkout, demo logins, widgets) using obviously fake personal data that you specify in the task (e.g. name 'Test User', address '123 Test St'). Use the public demo credentials from KNOWN FEATURES when needed.",
        "tool": "This is an account-free interactive web app: tasks should use it to produce a concrete, checkable result. No sign-in.",
    }[mode]
    return primary, sites, f"""You write realistic tasks that a user would give to an autonomous web-browsing agent. Today is {today}.

{chr(10).join(blocks)}

DIFFICULTY TIER: {TIERS[tier]}
{rules_mode}
{'The task should genuinely need ALL the listed sites (e.g. gather on one, verify/enrich on the others).' if len(sites) > 1 else ''}

Write 4 DIFFERENT tasks of this tier. Requirements:
- Self-contained and unambiguous (unless SPECIAL says otherwise); answerable purely with what is visible on the live site(s) today; robust to content changing (ask for "current"/"latest" values or give concrete stable targets you can see in the excerpt or that certainly exist).
- Do not depend on features you are not confident exist. Prefer the features listed above. No CAPTCHAs, no file uploads from disk, no downloads, no email/phone verification.
- State precisely what the agent must report back (exact fields, units, ordering, format) so success is checkable from the final answer.
- Vary the task kinds, e.g.: {'; '.join(kinds)}.
- Write each task in the voice of a different user: (1) {style[0]}; (2) {style[1]}; (3) {style[2]}; (4) any.
- Mention the website by name or URL naturally inside the task text.
{special}

Reply with ONLY a JSON array of 4 objects: {{"text": "<the task as the user would type it>", "expected_steps": <int>, "kind": "<short label>", "answer_format": "<what the final answer must contain>"}} (plus "ask_profile" or "followup" only where SPECIAL requires)."""

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--target", type=int, default=4000); ap.add_argument("--concurrency", type=int, default=6); ap.add_argument("--seed", type=int, default=20260921)
    a = ap.parse_args()
    os.makedirs(f"{W}/tasks", exist_ok=True)
    seen = set(); count = {"n": 0}
    if os.path.exists(POOL):
        for line in open(POOL):
            try: t = json.loads(line); seen.add(t["id"]); count["n"] += 1
            except Exception: pass
    lock = threading.Lock(); tiers = [t for t, _ in TIER_WEIGHTS]; weights = [w for _, w in TIER_WEIGHTS]
    def worker(i):
        rnd = random.Random(a.seed * 1000 + i + int(time.time()))
        while True:
            with lock:
                if count["n"] >= a.target: return
            if os.path.exists(f"{W}/control/STOP_TASKGEN"): return
            tier = rnd.choices(tiers, weights)[0]
            try:
                primary, sites, prompt = build_prompt(rnd, tier)
                text = chat(prompt)
                arr = json.loads(re.search(r"\[.*\]", text, re.S).group(0))
            except Exception as e:
                print("gen error", repr(e)[:200], flush=True); time.sleep(5); continue
            rows = []
            for t in arr:
                if not isinstance(t, dict) or not isinstance(t.get("text"), str) or len(t["text"]) < 25 or len(t["text"]) > 4000: continue
                tid = hashlib.sha1(re.sub(r"\W+", " ", t["text"].lower()).encode()).hexdigest()[:10]
                row = {"id": tid, "tier": tier, "text": t["text"].strip(), "sites": [s[0] for s in sites], "site_mode": primary[2], "category": primary[1],
                       "kind": str(t.get("kind", ""))[:80], "expected_steps": t.get("expected_steps"), "answer_format": str(t.get("answer_format", ""))[:600], "source": "synthetic-qwen3.8-flash-next", "created": datetime.date.today().isoformat()}
                if isinstance(t.get("ask_profile"), dict) and t["ask_profile"]: row["ask_profile"] = {str(k)[:80]: str(v)[:300] for k, v in t["ask_profile"].items()}
                if isinstance(t.get("followup"), str) and len(t["followup"]) > 15: row["followup"] = t["followup"].strip()
                if primary[2] == "sandbox": row["guardrails"] = {"forbidPurchases": False, "extraRules": ["This is a practice/demo website built for automation testing: fake checkouts, fake sign-ups and form submissions with obviously fake data are allowed here. Never enter real personal or payment data."]}
                rows.append(row)
            with lock:
                with open(POOL, "a") as f:
                    for row in rows:
                        if row["id"] in seen: continue
                        seen.add(row["id"]); count["n"] += 1; f.write(json.dumps(row, ensure_ascii=False) + "\n")
                print(f"pool={count['n']} (+{len(rows)} {tier} {primary[0]})", flush=True)
    th = [threading.Thread(target=worker, args=(i,), daemon=True) for i in range(a.concurrency)]
    [t.start() for t in th]; [t.join() for t in th]

if __name__ == "__main__":
    main()
