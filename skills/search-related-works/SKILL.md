---
name: search-related-works
description: |
  Search OpenAlex (primary) and arXiv (fallback/PDFs) for related works given an academic paper,
  and conduct literature reviews with citation snowballing. Extracts key terms from a paper,
  searches for related publications with citation counts and venues, and traverses the citation
  graph (forward/backward snowballing) from key papers.
  Use when the user needs to: (1) Find related work for a paper under review, (2) Conduct a
  literature review or survey on a topic, (3) Find papers citing or cited by a known work,
  (4) Find prior work, baselines, or competing approaches mentioned in a paper,
  (5) Search academic literature based on a manuscript's key concepts,
  or any other task involving finding related academic papers.
---

# Search Related Works

Extract key terms from an academic paper (or topic), search OpenAlex for related publications,
snowball the citation graph, and present results organized by relevance with citation counts.

OpenAlex is the primary search engine: no meaningful rate limits, citation counts, venue
metadata, and citation-graph traversal. arXiv is kept for PDF downloads and as a search fallback.

## Workflow

### Step 1: Read the Paper

Read the paper the user provides (file path via Read tool — PDFs supported — or pasted text).
If the user gives a topic instead of a paper, skip to Step 2 using the topic directly.

Extract information from these sections (in priority order):
1. Title and abstract
2. Introduction (contributions, problem statement)
3. Related work section
4. Method/approach names
5. Experiments (baselines, datasets, benchmarks)

### Step 2: Extract Search Terms

Identify **5–8 search term groups**, each targeting a different facet:

| Category | What to extract | Example terms |
|----------|----------------|---------------|
| **Core topic** | Main research problem or area | `root cause analysis time series` |
| **Methods/techniques** | Specific approaches or frameworks | `causal discovery`, `graph neural network diagnosis` |
| **Baselines/comparisons** | Named systems, benchmarks, datasets | `PRISM`, `C-MAPSS`, `tau-bench` |
| **Application domain** | Specific application area | `gas turbine fault diagnosis` |
| **Seed papers** | Key cited works for snowballing | The 2–3 most central references |

Guidelines:
- Prefer specific terms over generic ones (`function calling LLM` over `language model`)
- Include both full names and abbreviations (`MCP` and `Model Context Protocol`)
- Extract named benchmarks and datasets verbatim

### Step 3: Search OpenAlex

**API key check (required since Feb 2026):** the script finds the key automatically via
`--api-key` flag → `OPENALEX_API_KEY` env var → `~/.config/openalex/api_key` file.
If it prints a "no OpenAlex API key found" warning, ask the user for their key — free
from https://openalex.org/settings/api after creating an account — and save it to
`~/.config/openalex/api_key` with `chmod 600`. Keyless requests get only ~100 trial
credits/day (one or two test queries), then HTTP 409. A free key covers ~1,000
searches/day — far more than a full run needs.

Run `scripts/search_openalex.py` for each search term group. Unlike arXiv, **parallel
execution is fine** — run several searches in one Bash call or in parallel calls.

```bash
# Relevance search (title + abstract + fulltext)
python3 <skill_path>/scripts/search_openalex.py --search "QUERY" --per-page 15

# Higher precision: title + abstract only, with year filter
python3 <skill_path>/scripts/search_openalex.py --search "QUERY" --title-abstract --from-year 2020

# Include abstract snippets in output (for judging relevance)
python3 <skill_path>/scripts/search_openalex.py --search "QUERY" --format md-abstracts
```

Output is a markdown table: Title | Authors | Year | Venue | Cites | OpenAlex ID | arXiv ID | DOI.
Use `--format json` when results need programmatic processing.
See `references/openalex-api.md` for filter syntax and API details.

**Fallback:** if OpenAlex is unreachable or coverage seems poor for very recent preprints
(last 1–2 months), search arXiv directly — see `references/arxiv-api.md` and **obey its
strict serial rate-limit rules** (1 request / 3s, no parallelism).

### Step 4: Snowball the Citation Graph (literature review)

For the 2–4 most relevant/seminal papers found (or seed papers named in the manuscript):

```bash
# Forward: who cites this work? (finds newer follow-ups and competitors)
python3 <skill_path>/scripts/search_openalex.py --cites W2741809807 --per-page 25

# Backward: what does this work cite? (finds foundations and shared baselines)
python3 <skill_path>/scripts/search_openalex.py --references W2741809807
```

Look up a work's OpenAlex ID from Step 3 output, or resolve a DOI/arXiv ID:

```bash
python3 <skill_path>/scripts/search_openalex.py --ids 10.1145/3597503.3608128 2401.12345
```

Note: arXiv papers from before ~2022 often can't be resolved by arXiv ID — look them up by
title with `--search "exact title" --title-abstract` instead.

For a thorough literature review, do one more snowball round on the best papers surfaced
by the first round. Stop when new results are mostly duplicates.

### Step 5: Deduplicate and Organize

1. **Remove duplicates** — same OpenAlex ID / DOI across queries; preprint vs published
   versions of the same title
2. **Sanity-check surprising rows** — OpenAlex has occasional merged-record glitches where
   title and authors disagree; verify against the DOI/arXiv link before including
3. **Categorize** each paper:
   - **Directly related** — same problem or competing approaches
   - **Methodologically similar** — similar techniques, different problems
   - **Same domain** — same broader area, different focus
4. **Rank** within each category by relevance, using citation counts as a signal
   (but don't let raw counts bury highly relevant recent work)
5. **Add relevance notes** — briefly explain why each paper is relevant

### Step 6: Present Results

```markdown
## Related Works for "[Paper Title]"

### Search Terms Used
- Core topic: [terms]
- Methods: [terms]
- Baselines: [terms]
- Domain: [terms]
- Snowball seeds: [papers]

### Directly Related Papers
| Title | Authors | Year | Venue | Cites | Link | Relevance |
|-------|---------|------|-------|-------|------|-----------|

### Methodologically Similar Papers
(same columns)

### Same Domain / Broader Context
(same columns)

### Summary
[2-3 sentences on the landscape: major threads, seminal works, apparent gaps]
```

Link each paper: prefer `[arXiv](https://arxiv.org/abs/ID)` when an arXiv ID exists,
else `[DOI](https://doi.org/...)`, else `[OpenAlex](https://openalex.org/WID)`.

### Step 7: Ask for Output Paths

Use AskUserQuestion to ask for all three paths in a single prompt:
1. **OUTPUT.md file path** — the structured report (e.g., `./OUTPUT.md`)
2. **PDF download folder** — (e.g., `./pdfs`)
3. **Text output folder** — converted `.txt` files (e.g., `./txts`)

### Step 8: Save OUTPUT.md

Write the full Step 6 report to the user-specified path.

### Step 9: Download Papers

**arXiv papers** — use the download script (serial, rate-limit aware):

```bash
python3 <skill_path>/scripts/download_arxiv.py --output-dir <pdf_folder> <id1> <id2> ...
```

It downloads serially with 5s delays, backs off on `Rate exceeded` (HTTP 429/503 and the
tiny 200-body variant), and skips 404s and already-downloaded files. If errors persist,
it is usually server-side — wait several minutes and re-run.

**Non-arXiv open-access papers** — use the `oa_pdf_url` from `--format json` output:

```bash
curl -sSL -o <pdf_folder>/<name>.pdf "<oa_pdf_url>"
```

Papers with no OA location cannot be downloaded — list them in the report as
"paywalled" with their DOI so the user can retrieve them via institutional access.

Report which papers were downloaded, skipped, and failed.

### Step 10: Convert to Text

```bash
pdftotext -layout <pdf_folder>/<file>.pdf <txt_folder>/<file>.txt
```

One command per PDF. Report which files were converted.

## Tips

- No results → broaden terms or drop `--title-abstract`; too noisy → add `--title-abstract`
  or more specific terms
- For very recent work, add `--sort publication_date`; for foundational work,
  `--sort cited_by_count`
- OpenAlex citation counts lag Google Scholar — treat as relative signal, not ground truth
- The user may ask to drill into a sub-area — run additional targeted queries or another
  snowball round
- If the paper names specific prior works, resolve them directly with `--ids` or a title search

## Resources

### references/
- `openalex-api.md` — OpenAlex API: search/filter syntax, snowballing, external-ID lookup, caveats
- `arxiv-api.md` — arXiv API syntax and **strict rate-limit rules** (fallback search only)

### scripts/
- `search_openalex.py` — OpenAlex search/snowball/lookup. Modes: `--search`, `--cites WID`,
  `--references WID`, `--ids <doi|arxiv|WID>...`. Output: `md` (default), `md-abstracts`, `json`
- `download_arxiv.py` — Downloads arXiv PDFs by ID, serially with backoff
