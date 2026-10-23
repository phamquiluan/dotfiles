#!/usr/bin/env python3
"""Map flat .txt line offsets to the page/line coordinates an author actually sees.

Manuscripts submitted through Editorial Manager, and most conference templates with
`\\linenumbers`, print line numbers in the left margin that RESET on every page.
A citation like "(Lines 759-761)" taken from `pdftotext` output is meaningless to an
author: they have no way to find line 759 of a file they never saw.

This script builds the fileline -> (page, margin-line) map and rewrites citations.

Modes:
  --detect                 report whether the paper uses per-page margin numbering
  --lookup N [N ...]       print page/line for one or more flat file lines
  --check REVIEW           verify every "p. P, line L" citation in REVIEW resolves
  --convert REVIEW         rewrite "(Lines N-M)" -> "(p. P, lines L1-L2)" in REVIEW

Examples:
  map_paper_lines.py paper.txt --detect
  map_paper_lines.py paper.txt --lookup 759 1105
  map_paper_lines.py paper.txt --convert reviews.md --out reviews.md
  map_paper_lines.py paper.txt --check reviews.md
"""
import argparse
import re
import sys

MARGIN = re.compile(r"^\s*(\d{1,3})(?:\s|$)")
# A row carrying only numbers: a margin number, a printed page number, or both.
NUMERIC_ROW = re.compile(r"^[\s\d]+$")


def build_map(path, max_margin=99):
    """Return (mapping, meta). mapping: fileline(1-based) -> (page, margin_line)."""
    raw = open(path, encoding="utf-8", errors="replace").read()
    lines = raw.split("\n")

    # Page blocks are delimited by form feeds. Fall back to one block if absent.
    breaks = [i for i, l in enumerate(lines) if l.startswith("\x0c")]
    if not breaks:
        return {i + 1: (1, i + 1) for i in range(len(lines))}, {
            "per_page_numbering": False,
            "pages": 1,
            "reason": "no form-feed page breaks found",
        }

    bounds = []
    start = 0
    for b in breaks:
        if b > start:
            bounds.append((start, b - 1))
        start = b
    bounds.append((start, len(lines) - 1))

    # Does each block carry margin numbers that restart near 1?
    restarts = 0
    for lo, hi in bounds:
        nums = []
        for i in range(lo, hi + 1):
            m = MARGIN.match(lines[i].lstrip("\x0c"))
            if m and 1 <= int(m.group(1)) <= max_margin:
                nums.append(int(m.group(1)))
        if len(nums) >= 5 and min(nums[:5]) <= 3:
            restarts += 1
    per_page = restarts >= max(2, len(bounds) // 2)

    # Recover the PRINTED page number. Numeric-only rows are ambiguous: a row may hold
    # a margin number, a page number, or both. Disambiguate with the one property a
    # page number has and a margin number does not - it increases by exactly one per
    # block. Score every candidate offset k and keep the k that fits the most blocks.
    # This also tolerates unnumbered cover sheets, which simply match no k.
    candidates = {}
    for idx, (lo, hi) in enumerate(bounds):
        vals = set()
        for i in range(lo, hi + 1):
            body = lines[i].lstrip("\x0c")
            if body.strip() and NUMERIC_ROW.match(body):
                vals.update(int(t) for t in body.split() if t.isdigit() and 1 <= int(t) <= 999)
        candidates[idx] = vals

    best_k, best_hits = 1, 0
    for k in range(-len(bounds), 1000):
        hits = sum(1 for idx, vals in candidates.items() if (idx + k) in vals)
        if hits > best_hits:
            best_k, best_hits = k, hits
    offset = best_k
    printed = {idx: idx + offset for idx, vals in candidates.items() if (idx + offset) in vals}

    mapping = {}
    for idx, (lo, hi) in enumerate(bounds):
        page = printed.get(idx, idx + offset)
        margin = 1
        for i in range(lo, hi + 1):
            m = MARGIN.match(lines[i].lstrip("\x0c"))
            if m and 1 <= int(m.group(1)) <= max_margin:
                margin = int(m.group(1))
            mapping[i + 1] = (page, margin)

    meta = {
        "per_page_numbering": per_page,
        "pages": len(bounds),
        "page_offset": offset,
        "printed_page_numbers": bool(printed),
    }
    return mapping, meta


def fmt(mapping, a, b=None):
    pa, la = mapping.get(a, (None, None))
    if pa is None:
        return None
    if b is None or b == a:
        return f"p. {pa}, line {la}"
    pb, lb = mapping.get(b, (pa, la))
    if pb == pa:
        return f"p. {pa}, lines {la}-{lb}" if lb != la else f"p. {pa}, line {la}"
    return f"p. {pa}, line {la} to p. {pb}, line {lb}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paper")
    ap.add_argument("--detect", action="store_true")
    ap.add_argument("--lookup", nargs="+", type=int)
    ap.add_argument("--convert")
    ap.add_argument("--check")
    ap.add_argument("--out")
    args = ap.parse_args()

    mapping, meta = build_map(args.paper)

    if args.detect or not (args.lookup or args.convert or args.check):
        print(f"per-page margin numbering : {meta['per_page_numbering']}")
        print(f"page blocks               : {meta['pages']}")
        print(f"printed page numbers found: {meta.get('printed_page_numbers')}")
        print(f"page offset applied       : {meta.get('page_offset')}")
        if meta["per_page_numbering"]:
            print("\nCite as 'p. P, line L'. Flat .txt offsets are NOT usable by the authors.")
        else:
            print("\nNo per-page numbering detected. Flat line numbers are acceptable;")
            print("state the convention in the review so the authors can follow it.")
        return

    if args.lookup:
        for n in args.lookup:
            print(f"{n:6d} -> {fmt(mapping, n) or 'OUT OF RANGE'}")
        return

    if args.check:
        text = open(args.check, encoding="utf-8").read()
        rev = {}
        for fl, pl in sorted(mapping.items()):
            rev.setdefault(pl, fl)
        cites = set(re.findall(r"p\.\s*(\d{1,3}),\s*lines?\s*(\d{1,3})", text))
        bad = [(p, l) for p, l in cites if (int(p), int(l)) not in rev]
        print(f"distinct page/line citations: {len(cites)}")
        print(f"unresolvable                : {bad if bad else 'none'}")
        stale = len(re.findall(r"\(Lines?\s+\d{2,4}", text))
        if stale and meta["per_page_numbering"]:
            print(f"WARNING: {stale} flat-offset citations still present; run --convert")
        return

    if args.convert:
        text = open(args.convert, encoding="utf-8").read()
        n = [0]

        def sub(m):
            a = int(m.group(1))
            b = int(m.group(2)) if m.group(2) else None
            s = fmt(mapping, a, b)
            if not s:
                return m.group(0)
            n[0] += 1
            return f"({s})"

        out = re.sub(r"\(Lines?\s+(\d{1,4})(?:\s*[-–]\s*(\d{1,4}))?\)", sub, text)
        dest = args.out or args.convert
        open(dest, "w", encoding="utf-8").write(out)
        print(f"converted {n[0]} citations -> {dest}")
        print("NOTE: verify a sample with --lookup; a citation pointing at the wrong")
        print("table row is still wrong after conversion.")
        return


if __name__ == "__main__":
    sys.exit(main())
