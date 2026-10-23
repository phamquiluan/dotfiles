---
name: search-related-works
description: |
  Find related academic papers via OpenAlex (search, citation counts, venues, forward/backward
  citation snowballing) with arXiv as fallback, and optionally download the PDFs and convert
  them to text. Use when the user needs related work for a paper (e.g. one under review), a
  literature review or survey, papers citing or cited by a known work, prior work / baselines /
  competing approaches, or wants a set of papers downloaded to a pdfs/ folder and parsed to txts/.
---

# Search Related Works

Search the literature with OpenAlex, snowball the citation graph from the best hits, and report
what you found. Match the depth to the request: a quick "who cites X?" needs one call, a
related-work set for a paper under review needs several searches plus a snowball round or two.

`<skill>` below is this skill's directory.

## Tools

```bash
# Relevance search (title+abstract+fulltext); --title-abstract for precision
python3 <skill>/scripts/search_openalex.py --search "QUERY" [--title-abstract] [--from-year 2020] \
    [--sort relevance|cited_by_count|publication_date] [--per-page 15] [--format md|md-abstracts|json]

# Forward snowball (who cites W…) / backward snowball (what W… cites)
python3 <skill>/scripts/search_openalex.py --cites W2741809807
python3 <skill>/scripts/search_openalex.py --references W2741809807

# Resolve OpenAlex IDs, DOIs, or arXiv IDs
python3 <skill>/scripts/search_openalex.py --ids 10.1145/3597503.3608128 2401.12345 W2741809807
```

Parallel OpenAlex calls are fine. `--format md-abstracts` shows abstract snippets; `json` adds
`oa_pdf_url`. Filter syntax and API details: `references/openalex-api.md`.

**API key.** OpenAlex requires a key since Feb 2026. The script reads `--api-key`, then
`$OPENALEX_API_KEY`, then `~/.config/openalex/api_key`. If it warns that no key was found, ask
the user for theirs (free at https://openalex.org/settings/api) and save it to that file with
`chmod 600`. Without a key, requests fail with HTTP 409 after a query or two.

## Gotchas

- arXiv papers from before ~2022 often don't resolve by arXiv ID; search the exact title with
  `--title-abstract` instead.
- OpenAlex occasionally merges records, so a title and its authors can disagree. Check any
  surprising row against its DOI or arXiv link before reporting it.
- Preprint and published versions show up as separate works; dedupe by title.
- Citation counts lag Google Scholar. Use them as a relative signal, and don't let them bury
  relevant recent work.
- OpenAlex trails new preprints by weeks. For the last 1–2 months, also use WebSearch or the
  arXiv API. The arXiv API is strictly serial, 1 request per 3 s: read `references/arxiv-api.md`
  before calling it.

## Approach

- Search several distinct facets of the paper or topic: the problem, the method, named
  baselines/benchmarks/datasets (verbatim), and the application domain. Search both full names
  and abbreviations.
- Snowball from the 2–4 most central papers, including key works the manuscript itself cites.
  Stop when new results are mostly duplicates.
- Judge relevance from abstracts, not titles. Don't report a paper you haven't checked.

## Report

Shape the report around what the user is doing (novelty check, related-work section, survey,
quick lookup). By default, group papers by how they relate (same problem / similar method /
broader context), and give each one: title, first author, year, venue, cites, link, and one line
on why it matters. Finish with a short synthesis of the main threads, seminal works, and gaps.
For links, prefer `https://arxiv.org/abs/ID`, then `https://doi.org/DOI`, then
`https://openalex.org/WID`. Also list the queries and snowball seeds you used.

## Downloading and parsing (when the user asks)

Use the folders the prompt names; the usual layout is `pdfs/` and `txts/`. Save the report as
a Markdown file too (path from the prompt, else `OUTPUT.md` next to those folders), so the text
files have an index mapping IDs to titles.

```bash
# arXiv: serial, 5 s spacing, backs off on rate limits, skips existing files and 404s
python3 <skill>/scripts/download_arxiv.py --output-dir pdfs 2408.13729 2405.09330 ...

# Other open-access papers: oa_pdf_url from --format json
curl -sSL -o pdfs/<name>.pdf "<oa_pdf_url>"

# Convert every PDF that doesn't have a .txt yet
mkdir -p txts && for f in pdfs/*.pdf; do t="txts/$(basename "${f%.pdf}").txt"; \
  [ -f "$t" ] || pdftotext -layout "$f" "$t"; done
```

If arXiv rate-limits persist, the cause is usually server-side: wait a few minutes and re-run
(existing files are skipped). Check that each downloaded file is really a PDF (`file pdfs/*`),
since some OA links return HTML landing pages. Papers with no OA copy go in the report as
paywalled, with their DOI. Finish by reporting what was downloaded, converted, skipped, and failed.
