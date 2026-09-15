# OpenAlex API Reference

OpenAlex indexes ~250M scholarly works with citation links, no authentication required.
Prefer it over arXiv for search: friendlier rate limits, citation counts, venue metadata,
citation-graph traversal, and coverage beyond arXiv (journals, conference proceedings).

## Base URL

```
https://api.openalex.org/works
```

## Authentication (API key REQUIRED since 2026-02-13)

OpenAlex switched to keyed, credit-based access on February 13, 2026. The old
`mailto=` polite-pool parameter is no longer supported.

- **Get a free key** (~30 seconds): create an account at openalex.org, copy the key
  from https://openalex.org/settings/api
- **Pass it as a query parameter**: `?api_key=YOUR_KEY`
- `scripts/search_openalex.py` resolves the key in order: `--api-key` flag →
  `OPENALEX_API_KEY` env var → `~/.config/openalex/api_key` file. If none is found,
  ask the user for their key and save it to the key file (`chmod 600`).
- **Without a key**: ~100 trial credits/day, then HTTP 409 errors. Enough for one or
  two test queries only — not a full related-works run.

## Rate Limits (credit-based)

A free key includes **$1 of usage per day**, which covers per day:
- Unlimited single-work lookups by ID/DOI (free)
- ~10,000 list/filter calls ($0.0001 each)
- ~1,000 search calls ($0.001 each)
- ~100 PDF/XML downloads ($0.01 each)

Hard cap of 100 requests/second. This is far more than a related-works run needs
(typically <30 calls). Parallel queries are fine (unlike arXiv). On HTTP 429, back
off a second and retry; HTTP 409/402 means credits are exhausted for the day.
Responses include headers showing spend.

## Search

| Approach | URL | Notes |
|----------|-----|-------|
| Relevance search | `?search=QUERY` | Searches title, abstract, fulltext. Results ranked by relevance. |
| Title+abstract only | `?filter=title_and_abstract.search:QUERY` | Higher precision, less noise. |
| Title only | `?filter=title.search:QUERY` | For finding a specific known paper. |

Search is not case-sensitive; stemming is applied. Quote phrases with `%22...%22` for exact match.

## Filters (comma = AND, pipe = OR within a filter)

```
?filter=from_publication_date:2020-01-01,to_publication_date:2025-12-31
?filter=cites:W2741809807                  # works CITING W274... (forward snowball)
?filter=ids.openalex:W123|W456|W789        # batch fetch (max ~50 per pipe list)
?filter=type:article
?filter=cited_by_count:>100
?filter=primary_location.source.id:S4306420609   # specific venue
```

## Other Parameters

| Param | Notes |
|-------|-------|
| `per-page` | Max 200 (default 25) |
| `page` | Basic pagination; use `cursor=*` for deep paging |
| `sort` | `cited_by_count:desc`, `publication_date:desc`, `relevance_score:desc` (search only) |
| `select` | Comma list of fields — always use it to keep responses small |

## Single-Work Lookup by External ID

```
/works/W2741809807                      # OpenAlex ID
/works/doi:10.1145/3597503.3608128      # DOI
/works/doi:10.48550/arXiv.2401.12345    # arXiv ID via its auto-registered DOI
```

**Caveat:** arXiv papers first posted before ~2022 often lack the `10.48550` DOI in
OpenAlex (e.g. `1706.03762` 404s). Fall back to a title search:
`?filter=title.search:attention is all you need`.

## Key Response Fields

- `display_name` — title (occasionally null → "(untitled)")
- `authorships[].author.display_name`
- `publication_year`, `cited_by_count`
- `primary_location.source.display_name` — venue
- `best_oa_location.pdf_url` — open-access PDF when available
- `referenced_works` — list of OpenAlex IDs this work cites (backward snowball)
- `abstract_inverted_index` — abstract as `{word: [positions]}`; must be reconstructed
  by sorting positions (the script does this)

## Citation Snowballing

- **Forward** (who cites X): `?filter=cites:WID&sort=cited_by_count:desc`
- **Backward** (what X cites): fetch the work, read `referenced_works`, batch-fetch
  via `?filter=ids.openalex:W1|W2|...` (≤50 per request)

## Data Quality Caveats

- Some records are merged/mislinked: title, DOI, and authors can occasionally disagree
  (e.g. a record showing BERT's authors under an unrelated title). Cross-check any
  surprising row against its DOI or arXiv link before citing it.
- Citation counts lag and differ from Google Scholar (OpenAlex counts indexed works only).
- Preprint + published versions may appear as separate works — dedupe by title.
