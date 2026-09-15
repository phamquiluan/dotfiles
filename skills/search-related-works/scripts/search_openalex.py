#!/usr/bin/env python3
"""Search OpenAlex for academic works: keyword search, citation snowballing, batch lookup.

Usage:
    # Keyword search (title + abstract + fulltext relevance)
    python3 search_openalex.py --search "root cause analysis turbomachinery" --per-page 15

    # Restrict search to title+abstract only (higher precision)
    python3 search_openalex.py --search "graceful degradation" --title-abstract --from-year 2020

    # Forward snowball: works that CITE a given work
    python3 search_openalex.py --cites W2741809807 --per-page 25

    # Backward snowball: works a given work REFERENCES
    python3 search_openalex.py --references W2741809807

    # Batch lookup by OpenAlex IDs, DOIs, or arXiv IDs
    python3 search_openalex.py --ids W2741809807 10.1145/3597503 2401.12345

Output: markdown table (default) or JSON lines (--format json).
Each result includes: title, first author, year, venue, citation count,
OpenAlex ID, DOI, arXiv ID (when available), OA PDF URL, abstract snippet.
"""

import argparse
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://api.openalex.org/works"
# Required since 2026-02-13. Free key: https://openalex.org/settings/api
# Keyless requests get ~100 trial credits/day, then HTTP 409.
# Resolution order: --api-key flag > OPENALEX_API_KEY env var > key file.
KEY_FILE = os.path.expanduser("~/.config/openalex/api_key")
API_KEY = os.environ.get("OPENALEX_API_KEY", "")
if not API_KEY:
    try:
        with open(KEY_FILE) as f:
            API_KEY = f.read().strip()
    except OSError:
        pass
ARXIV_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5})", re.I)


def _ssl_context() -> ssl.SSLContext:
    try:
        ctx = ssl.create_default_context()
        urllib.request.urlopen("https://api.openalex.org", context=ctx, timeout=5)
        return ctx
    except (ssl.SSLCertVerificationError, urllib.error.URLError):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx


def _get(url: str, ctx: ssl.SSLContext, max_retries: int = 3) -> dict:
    headers = {"User-Agent": "search-related-works/2.0"}
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            if e.code == 404:
                return {}
            if e.code in (401, 402, 403, 409):
                sys.exit(
                    f"HTTP {e.code}: out of API credits or invalid/missing key.\n"
                    "Get a free key at https://openalex.org/settings/api and set "
                    "OPENALEX_API_KEY (or pass --api-key)."
                )
            raise
        except (urllib.error.URLError, TimeoutError):
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise
    return {}


def reconstruct_abstract(inverted: dict, max_words: int = 60) -> str:
    """OpenAlex stores abstracts as {word: [positions]}; rebuild the text."""
    if not inverted:
        return ""
    positions = []
    for word, idxs in inverted.items():
        for i in idxs:
            positions.append((i, word))
    positions.sort()
    words = [w for _, w in positions[:max_words]]
    suffix = "..." if len(positions) > max_words else ""
    return " ".join(words) + suffix


def extract_arxiv_id(work: dict) -> str:
    for loc in work.get("locations") or []:
        for key in ("landing_page_url", "pdf_url"):
            m = ARXIV_RE.search(loc.get(key) or "")
            if m:
                return m.group(1)
    return ""


def simplify(work: dict) -> dict:
    authorships = work.get("authorships") or []
    first = authorships[0]["author"]["display_name"] if authorships else "?"
    authors = first + (" et al." if len(authorships) > 3 else
                       "" if len(authorships) <= 1 else
                       ", " + ", ".join(a["author"]["display_name"] for a in authorships[1:]))
    loc = work.get("primary_location") or {}
    source = loc.get("source") or {}
    oa = work.get("best_oa_location") or {}
    doi = (work.get("doi") or "").replace("https://doi.org/", "")
    return {
        "id": (work.get("id") or "").replace("https://openalex.org/", ""),
        "title": work.get("display_name") or "(untitled)",
        "authors": authors,
        "year": work.get("publication_year"),
        "venue": source.get("display_name") or "",
        "cited_by_count": work.get("cited_by_count", 0),
        "doi": doi,
        "arxiv_id": extract_arxiv_id(work),
        "oa_pdf_url": oa.get("pdf_url") or "",
        "abstract": reconstruct_abstract(work.get("abstract_inverted_index") or {}),
    }


SELECT = ("id,doi,display_name,publication_year,cited_by_count,authorships,"
          "primary_location,best_oa_location,locations,abstract_inverted_index,"
          "referenced_works")


def build_url(params: dict) -> str:
    params = dict(params)
    if API_KEY:
        params["api_key"] = API_KEY
    return API_BASE + "?" + urllib.parse.urlencode(params)


def resolve_id(raw: str) -> str:
    """Map a raw ID (OpenAlex ID, DOI, arXiv ID) to an OpenAlex works URL."""
    raw = raw.strip()
    key = ("?api_key=" + urllib.parse.quote(API_KEY)) if API_KEY else ""
    if re.fullmatch(r"[Ww]\d+", raw):
        return API_BASE + "/" + raw.upper() + key
    if re.fullmatch(r"[0-9]{4}\.[0-9]{4,5}(v\d+)?", raw):
        doi = "10.48550/arXiv." + re.sub(r"v\d+$", "", raw)
        return API_BASE + "/doi:" + doi + key
    if raw.startswith("10."):
        return API_BASE + "/doi:" + raw + key
    raise ValueError(f"Unrecognized ID format: {raw}")


def fetch_batch(ids: list, ctx: ssl.SSLContext) -> list:
    """Fetch up to 50 OpenAlex work IDs per request via the OR filter."""
    works = []
    for i in range(0, len(ids), 50):
        chunk = [w.replace("https://openalex.org/", "") for w in ids[i:i + 50]]
        url = build_url({
            "filter": "ids.openalex:" + "|".join(chunk),
            "select": SELECT,
            "per-page": 50,
        })
        works.extend(_get(url, ctx).get("results") or [])
    return works


def print_results(works: list, fmt: str, resort: bool = False) -> None:
    rows = [simplify(w) for w in works if w]
    if resort:
        rows.sort(key=lambda r: r["cited_by_count"] or 0, reverse=True)
    if fmt == "json":
        for r in rows:
            print(json.dumps(r, ensure_ascii=False))
        return
    print("| Title | Authors | Year | Venue | Cites | OpenAlex | arXiv | DOI |")
    print("|-------|---------|------|-------|-------|----------|-------|-----|")
    for r in rows:
        title = r["title"].replace("|", "\\|")[:90]
        venue = r["venue"].replace("|", "\\|")[:40]
        print(f"| {title} | {r['authors']} | {r['year']} | {venue} "
              f"| {r['cited_by_count']} | {r['id']} | {r['arxiv_id']} | {r['doi']} |")
    print(f"\n{len(rows)} results.")
    if fmt == "md-abstracts":
        print()
        for r in rows:
            if r["abstract"]:
                print(f"**{r['id']}** — {r['abstract']}\n")


def main():
    p = argparse.ArgumentParser(description="Search OpenAlex for academic works")
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--search", help="Keyword search query")
    mode.add_argument("--cites", metavar="WID", help="Works citing this OpenAlex ID (forward snowball)")
    mode.add_argument("--references", metavar="WID", help="Works this OpenAlex ID references (backward snowball)")
    mode.add_argument("--ids", nargs="+", help="Fetch specific works (OpenAlex IDs, DOIs, or arXiv IDs)")
    p.add_argument("--title-abstract", action="store_true",
                   help="Restrict --search to title+abstract (higher precision)")
    p.add_argument("--from-year", type=int, help="Earliest publication year")
    p.add_argument("--to-year", type=int, help="Latest publication year")
    p.add_argument("--per-page", type=int, default=15, help="Results per query (max 200)")
    p.add_argument("--sort", choices=["relevance", "cited_by_count", "publication_date"],
                   default="relevance")
    p.add_argument("--format", choices=["md", "md-abstracts", "json"], default="md")
    p.add_argument("--api-key", help="OpenAlex API key (default: $OPENALEX_API_KEY)")
    args = p.parse_args()

    global API_KEY
    if args.api_key:
        API_KEY = args.api_key
    if not API_KEY:
        print("Warning: no OpenAlex API key found — keyless requests get ~100 trial "
              "credits/day. Get a free key at https://openalex.org/settings/api and "
              f"save it to {KEY_FILE} (or set OPENALEX_API_KEY).", file=sys.stderr)

    ctx = _ssl_context()
    filters = []
    if args.from_year:
        filters.append(f"from_publication_date:{args.from_year}-01-01")
    if args.to_year:
        filters.append(f"to_publication_date:{args.to_year}-12-31")

    if args.search:
        params = {"per-page": args.per_page, "select": SELECT}
        if args.title_abstract:
            filters.append("title_and_abstract.search:" + args.search)
        else:
            params["search"] = args.search
        if filters:
            params["filter"] = ",".join(filters)
        if args.sort != "relevance":
            params["sort"] = args.sort + ":desc"
        works = _get(build_url(params), ctx).get("results") or []
    elif args.cites:
        filters.append("cites:" + args.cites.upper())
        params = {"filter": ",".join(filters), "per-page": args.per_page,
                  "select": SELECT, "sort": "cited_by_count:desc"}
        works = _get(build_url(params), ctx).get("results") or []
    elif args.references:
        seed = _get(resolve_id(args.references), ctx)
        if not seed:
            sys.exit(f"Work not found: {args.references}")
        refs = seed.get("referenced_works") or []
        print(f"Seed work references {len(refs)} works; fetching...", file=sys.stderr)
        works = fetch_batch(refs, ctx)
    else:
        works = []
        openalex_ids, singles = [], []
        for raw in args.ids:
            if re.fullmatch(r"[Ww]\d+", raw.strip()):
                openalex_ids.append(raw.strip().upper())
            else:
                singles.append(raw)
        if openalex_ids:
            works.extend(fetch_batch(openalex_ids, ctx))
        for raw in singles:
            w = _get(resolve_id(raw), ctx)
            if w:
                works.append(w)
            else:
                print(f"Not found: {raw}", file=sys.stderr)

    # Preserve API relevance order for searches; sort snowball/batch results by citations.
    resort = bool(args.cites or args.references or args.ids)
    print_results(works, args.format, resort=resort)


if __name__ == "__main__":
    main()
