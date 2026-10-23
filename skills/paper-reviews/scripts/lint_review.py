#!/usr/bin/env python3
"""Mechanical checks for a draft review, so SKILL.md does not need a long checklist.

Errors (hard rules):    **bold**, em-dash, "headline", letter labels [A] used but not
                        listed in References (or listed but never used).
Warnings (heuristic):   semicolons and <claim>: <elaboration> colons in prose, sentence
                        counts outside the limits (summary 5-7, strengths 1-2,
                        weaknesses / major comments 3-5, minor comments 1-2).
With --paper:           runs map_paper_lines.py --check on the review as well.

Sections are found from Markdown headings (#..####) and plain-text uppercase heading
lines. Items are numbered paragraphs such as "1.", "2)", "E1.", "N2.".

Usage:
  lint_review.py review.md [--paper paper.txt]
Exit status is 1 if any error is found.
"""
import argparse
import os
import re
import subprocess
import sys

HEADING = re.compile(r"^\s*(#{1,6})\s+(.*\S)\s*$")
CAPS_HEADING = re.compile(r"^\s*([A-Z][A-Z0-9 /&,()'-]{3,})\s*$")
ITEM = re.compile(r"^\s*(?:[A-Z]{1,2})?\d{1,2}[.)]\s+")
LETTER = re.compile(r"\[([A-Z](?:\s*,\s*[A-Z])*)\]")
REF_ENTRY = re.compile(r"^\s*(?:[-*]\s+)?\[([A-Z])\]\s")
REF_HEADING = re.compile(r"^[#\s]*(?:missing\s+)?references?\b", re.I)
CHECKBOX = re.compile(r"^\s*\[[ xX]\]\s")
RULE = re.compile(r"^\s*(?:-{3,}|={3,}|\*{3,})\s*$")
QUOTED = re.compile(r"\"[^\"\n]*\"|\u201c[^\u201d\n]*\u201d")
MATH = re.compile(r"\$\$.*?\$\$|\$[^$\n]*\$", re.S)
CODE = re.compile(r"`[^`\n]*`")
URL = re.compile(r"https?://\S+")

# Abbreviations that end in a period but do not end a sentence.
ABBREV = re.compile(
    r"\b(e\.g|i\.e|et al|etc|vs|cf|Fig|Figs|Sec|Secs|Eq|Eqs|Tab|Ref|No|approx|resp|"
    r"p|pp|ca|Dr|Mr|Ms|al|St|Inc|Jr)\.",
    re.I,
)
# Section kinds, matched against lowercased heading text.
KINDS = [
    ("summary", re.compile(r"summary"), (5, 7)),
    ("strength", re.compile(r"strength"), (1, 2)),
    ("minor", re.compile(r"minor"), (1, 2)),
    ("weakness", re.compile(r"weakness|major|concern"), (3, 5)),
]


def strip_inline(s):
    return URL.sub("URL", CODE.sub("CODE", MATH.sub("MATH", s)))


def reviewer_prose(s):
    """Inline text with verbatim quotes removed, since their punctuation is the paper's."""
    return QUOTED.sub("QUOTE", strip_inline(s))


def sentences(text):
    t = strip_inline(text)
    t = ABBREV.sub(lambda m: m.group(0).replace(".", "<dot>"), t)
    t = re.sub(r"(\d)\.(\d)", r"\1<dot>\2", t)
    t = ITEM.sub("", t, count=1)
    parts = re.split(r'(?<=[.!?])["\')\]]?\s+(?=["(\[]?[A-Z0-9$`])', t.strip())
    return [p for p in parts if re.search(r"[A-Za-z]", p)]


def heading_of(line):
    m = HEADING.match(line)
    if m:
        return m.group(2)
    m = CAPS_HEADING.match(line)
    if m and len(m.group(1).split()) <= 8:
        return m.group(1)
    return None


def parse(lines):
    """Yield (kind, start_line, text) blocks: section paragraphs and numbered items."""
    kind, buf, start = None, [], 0
    blocks = []

    def flush():
        if buf:
            blocks.append((kind, start, " ".join(s.strip() for s in buf)))
        buf.clear()

    for i, line in enumerate(lines, 1):
        h = heading_of(line)
        if h is not None:
            flush()
            low = h.lower()
            new = next((k for k, rx, _ in KINDS if rx.search(low)), None)
            if new is not None:
                kind = new
            elif re.search(r"reference|rating|confidence|question|artifact|justification|"
                           r"recommend|title|ethic|feedback|score", low):
                kind = None
            # Any other heading (e.g. "## Novelty" under Weaknesses) is a topic
            # sub-heading and keeps the parent kind.
            continue
        if not line.strip() or RULE.match(line):
            flush()
            continue
        if ITEM.match(line):
            flush()
        if not buf:
            start = i
        buf.append(line)
    flush()
    return blocks


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("review")
    ap.add_argument("--paper")
    args = ap.parse_args()

    raw = open(args.review, encoding="utf-8").read()
    lines = raw.split("\n")
    errors, warns = [], []

    # References section: everything after a heading containing "reference".
    ref_start = None
    for i, line in enumerate(lines):
        if REF_HEADING.match(line) and len(line.split()) <= 8:
            ref_start = i
    body = lines[:ref_start] if ref_start is not None else lines
    refs = lines[ref_start:] if ref_start is not None else []

    for n, line in enumerate(body, 1):
        if "**" in line:
            errors.append(f"{n}: bold marker '**'")
        if "—" in line:
            errors.append(f"{n}: em-dash")
        if re.search(r"headlin", line, re.I):
            errors.append(f"{n}: the word 'headline'")
        prose = reviewer_prose(line)
        if heading_of(line) or RULE.match(line) or prose.lstrip().startswith(("|", "[")):
            continue
        if ";" in prose:
            warns.append(f"{n}: semicolon in prose")
        for m in re.finditer(r"(\w[\w)\"']*): ([a-z]\w*)", prose):
            before = prose[: m.start()].strip()
            # "Label: value" lines and list lead-ins are fine.
            if len(before.split()) >= 3 and not prose.rstrip().endswith(":") and m.group(1) != "QUOTE":
                warns.append(f"{n}: possible <claim>: <elaboration> colon near '{m.group(0)}'")

    used = set()
    for line in body:
        for m in LETTER.finditer(CHECKBOX.sub("", line)):
            used.update(x.strip() for x in m.group(1).split(","))
    listed = {m.group(1) for line in refs if not CHECKBOX.match(line) for m in [REF_ENTRY.match(line)] if m}
    for x in sorted(used - listed):
        errors.append(f"[{x}] cited in the body but missing from References")
    for x in sorted(listed - used):
        errors.append(f"[{x}] listed in References but never cited")

    limits = {k: lim for k, _, lim in KINDS}
    for kind, start, text in parse(body):
        if kind is None:
            continue
        is_item = bool(ITEM.match(text))
        if kind != "summary" and not is_item:
            continue
        n = len(sentences(text))
        lo, hi = limits[kind]
        if not lo <= n <= hi:
            warns.append(f"{start}: {kind} has {n} sentences (limit {lo}-{hi})")

    summary_paras = [b for b in parse(body) if b[0] == "summary"]
    if len(summary_paras) > 1:
        warns.append(f"{summary_paras[0][1]}: summary spans {len(summary_paras)} paragraphs (must be one)")

    for e in errors:
        print(f"ERROR  {e}")
    for w in warns:
        print(f"WARN   {w}")
    print(f"\n{len(errors)} errors, {len(warns)} warnings "
          f"(sentence counts are heuristic; check flagged items by eye)", flush=True)

    if args.paper:
        here = os.path.dirname(os.path.abspath(__file__))
        print("\n--- coordinates (map_paper_lines.py --check)", flush=True)
        subprocess.run([sys.executable, os.path.join(here, "map_paper_lines.py"), args.paper, "--check", args.review])

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
