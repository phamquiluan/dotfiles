# arXiv API Reference

The arXiv API allows searching for academic papers without authentication.

## Base URL

```
https://export.arxiv.org/api/query
```

Use `https://` (an `http://` request is 301-redirected). When using `curl`, pass `-L` to follow the redirect.

## Query Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `search_query` | Query string with field prefixes and boolean operators | (required) |
| `start` | Index of first result (0-based) | `0` |
| `max_results` | Number of results to return (max 100) | `10` |
| `sortBy` | Sort field: `relevance`, `lastUpdatedDate`, `submittedDate` | `relevance` |
| `sortOrder` | Sort direction: `ascending`, `descending` | `descending` |

## Field Prefixes

| Prefix | Field | Example |
|--------|-------|---------|
| `ti:` | Title | `ti:transformer` |
| `abs:` | Abstract | `abs:reinforcement+learning` |
| `au:` | Author | `au:vaswani` |
| `cat:` | Category | `cat:cs.CL` |
| `all:` | All fields | `all:attention+mechanism` |

## Boolean Operators

Combine terms with `AND`, `OR`, `ANDNOT` (must be uppercase):

```
ti:transformer AND abs:attention
au:vaswani OR au:devlin
cat:cs.CL AND ti:language+model ANDNOT ti:vision
```

## Multi-Word Queries

- Use `+` for spaces within a field: `ti:language+model`
- Use `%22` for exact phrases: `ti:%22large+language+model%22`
- Parentheses for grouping: `(ti:benchmark OR ti:evaluation) AND abs:agent`

## Relevant CS Categories

| Category | Description |
|----------|-------------|
| `cs.AI` | Artificial Intelligence |
| `cs.CL` | Computation and Language (NLP) |
| `cs.SE` | Software Engineering |
| `cs.LG` | Machine Learning |
| `cs.IR` | Information Retrieval |
| `cs.CV` | Computer Vision |
| `cs.MA` | Multiagent Systems |
| `cs.PL` | Programming Languages |

## Example Queries

**Search for LLM agent benchmarks:**
```
http://export.arxiv.org/api/query?search_query=ti:LLM+agent+benchmark&max_results=10&sortBy=submittedDate&sortOrder=descending
```

**Search for tool use evaluation in NLP:**
```
http://export.arxiv.org/api/query?search_query=(ti:tool+use+OR+ti:function+calling)+AND+cat:cs.CL&max_results=10&sortBy=relevance
```

**Search by author:**
```
http://export.arxiv.org/api/query?search_query=au:vaswani&max_results=5&sortBy=submittedDate&sortOrder=descending
```

**Search for a specific paper by title:**
```
http://export.arxiv.org/api/query?search_query=ti:%22attention+is+all+you+need%22&max_results=5
```

**Combined category and topic search:**
```
http://export.arxiv.org/api/query?search_query=cat:cs.SE+AND+(abs:code+generation+OR+abs:program+synthesis)&max_results=10
```

## Response Format

The API returns Atom XML. When using WebFetch, use a prompt to extract:
- **Title** — paper title
- **Authors** — author list
- **Published** — publication date
- **Summary** — abstract text
- **arXiv ID** — from the `<id>` tag (e.g., `http://arxiv.org/abs/2401.12345v1` → `2401.12345`)
- **Categories** — from `<category>` tags
- **Links** — PDF and abstract page URLs

## WebFetch Extraction Prompt

Use this prompt when calling WebFetch on arXiv API results:

```
Extract all papers from this arXiv API response. For each paper provide:
- Title
- Authors (first author et al. if more than 3)
- Year
- arXiv ID (just the number, e.g., 2401.12345)
- Primary category
- One-sentence summary from the abstract

Format as a markdown table with columns: Title | Authors | Year | arXiv ID | Summary
```

## Rate Limiting (READ BEFORE BATCH QUERYING)

arXiv rate-limits aggressively and the limits differ by host. Violating them gets you
temporarily blocked, which can stall an entire related-works run. The rules below are
precise as of 2026.

### The hard rule (export.arxiv.org API — `tou.html`)

- **One request every 3 seconds, MAXIMUM. Single connection at a time (NO parallelism).**
  This applies across all machines you control — you cannot parallelize to go faster.
- **Prefer GET over POST.** GET responses can be served from arXiv's Fastly/Varnish cache;
  POST bypasses the cache and trips limits sooner.
- `max_results` ≤ **2000 per call**; ≤ **30000 total** per query (page with `start`, 0-based).
  Requesting > 30000 returns **HTTP 400**.
- No `User-Agent` is officially required, but sending a descriptive one with a contact
  email (e.g. `related-works-search/1.0 (you@example.com)`) is good practice and helps
  avoid robot-detection blocks.
- The API caches per query — there is no need to call the same query more than once a day.

### What the error responses mean

| Symptom | Meaning | Action |
|---------|---------|--------|
| HTTP **429** body `Rate exceeded.` (tiny, from Varnish/Fastly) | Usually **server-wide capacity**, NOT necessarily your fault. Can persist for minutes during incidents (a widespread outbreak occurred June 2026). | **Wait and retry later.** Backing off harder won't always help; the only reliable fix is time. |
| HTTP **503** Service Unavailable (sometimes `Retry-After`) | **Genuine individual overuse / throttling**, OR OAI flow control. | Honor `Retry-After` exactly if present; otherwise exponential backoff (3→6→12s…). Never treat 503 as fatal. |
| HTTP **403** (page mentions `denied.html` / "robot detection") | IP-level **robot/abuse block** (separate from rate limiting), triggered by aggressive crawling/prefetch. | Stop, slow down drastically; persistent blocks require emailing arXiv support (plain-text email, include IP + User-Agent). |
| HTTP **301** to `https://` | `http://` is redirected. | Always use `https://` and follow redirects (`curl -L`). |

Empirically, once "Rate exceeded" starts, requests may keep failing for **~3–5 minutes**
(occasionally longer during outages). Waiting is more effective than retrying in a tight loop.

### host differences & robots.txt

- **export.arxiv.org** `robots.txt` = `Disallow: /` (it is the machine-access host; use the
  API/OAI-PMH, don't crawl it).
- **arxiv.org** `robots.txt`: `/abs` and `/pdf` are **Allowed** with `Crawl-delay: 15`;
  `/search` and `/api` are **Disallowed**. So programmatic scraping of the HTML
  `arxiv.org/search/` page is discouraged by robots.txt — use it only as a low-volume
  fallback (see below), never for bulk.

### Fallback when the export API is rate-limited/blocked

If `export.arxiv.org/api` returns `Rate exceeded.` / 503 and waiting a few minutes doesn't
clear it, the metadata can still be obtained from the main site, which is governed
separately and is often reachable when the API is not:

1. Fetch the server-rendered search HTML directly with `curl` (it contains real IDs):
   `curl -sSL "https://arxiv.org/search/?searchtype=all&query=YOUR+TERMS&start=0"`
2. **Parse arXiv IDs locally** (do not trust an LLM summarizer to transcribe IDs — it may
   hallucinate). Extract with: `grep -oE 'arxiv\.org/abs/[0-9]{4}\.[0-9]{4,5}'`.
   Titles/authors live in `<p class="title is-5 mathjax">` and `<p class="authors">`.
3. **Validate every ID** before trusting it — a successful PDF download from
   `https://arxiv.org/pdf/<id>` confirms the ID is real.

Keep this fallback low-volume and serial (respect the 15s crawl-delay spirit). For genuinely
large jobs, use the sanctioned bulk channels instead of scraping: the AWS S3
requester-pays buckets, the Kaggle arXiv dataset, or OAI-PMH for metadata harvesting.

### Official `arxiv` Python package (reliable alternative)

`pip install arxiv` wraps all of this. `arxiv.Client` defaults already comply:
`delay_seconds=3.0`, `page_size=100`, `num_retries=3`. Prefer it when available.
