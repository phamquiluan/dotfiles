# arXiv API (fallback search)

Use it only for very recent preprints that OpenAlex hasn't indexed yet, or when OpenAlex is down.
The endpoint is `https://export.arxiv.org/api/query` (GET, https). It takes the usual
`search_query` field prefixes (`ti:`, `abs:`, `au:`, `cat:`, `all:`) with `AND`/`OR`/`ANDNOT`,
`+` for spaces, and `%22…%22` for phrases, plus `start`, `max_results`, `sortBy`
(`relevance|lastUpdatedDate|submittedDate`), and `sortOrder`. The response is Atom XML. Parse
IDs from the `<id>` tags yourself.

## Rate limits (strict)

- **One request every 3 s, one connection at a time, no parallelism**, counted across all your
  machines. Prefer GET (it can be cached); POST trips limits sooner.
- `max_results` ≤ 2000 per call and ≤ 30000 per query (above that you get HTTP 400).
- Send a descriptive User-Agent. Don't repeat the same query within a day (responses are cached).
- The `pip install arxiv` client complies by default (3 s delay, retries). Prefer it when it's available.

| Symptom | Meaning | Action |
|---|---|---|
| HTTP 429 or HTTP 200 with a tiny `Rate exceeded.` body | Usually server-wide capacity, not you | Wait 3–5+ min; tight retries don't help |
| HTTP 503 (maybe `Retry-After`) | Individual throttling | Honor `Retry-After`, else back off 3→6→12 s |
| HTTP 403 mentioning `denied.html` / robot detection | IP-level block | Stop and slow down drastically; persistent blocks need an email to arXiv support |

## When the API is blocked

`arxiv.org/search/` is a separate service and often still answers. Use it at low volume and
serially (robots.txt sets a 15 s crawl-delay for `/abs` and `/pdf`):

```bash
curl -sSL "https://arxiv.org/search/?searchtype=all&query=YOUR+TERMS&start=0" \
  | grep -oE 'arxiv\.org/abs/[0-9]{4}\.[0-9]{4,5}' | sort -u
```

Extract IDs locally with grep; an LLM summarizer may hallucinate them. Before trusting an ID,
validate it, e.g. by resolving it with `search_openalex.py --ids` or fetching its `/abs` page.
