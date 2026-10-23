#!/usr/bin/env python3
"""Flatten a LaTeX paper into one line-numbered text file for review.

The paper-reviews skill expects a paper as "NNN  content" lines. LaTeX sources
are split across \\input files, so a review citing "Line 217" is useless unless
the line can be traced back to a real file. This expands the includes, numbers
the result, and writes a sidecar map from flattened line to source file:line.

    flatten_tex.py main.tex -o review/paper.txt --map review/paper.map.tsv
    grep -P '^217\\t' review/paper.map.tsv     # -> section/70evaluation.tex 43
"""

import argparse
import os
import re
import sys

INPUT_RE = re.compile(r"^\s*\\(?:input|include|subfile)\s*\{([^}]+)\}\s*$")
ANY_INPUT_RE = re.compile(r"\\(?:input|include|subfile)\s*\{([^}]+)\}")
BEGIN_DOC_RE = re.compile(r"\\begin\s*\{document\}")
COMMENT_RE = re.compile(r"(?<!\\)%.*$")


def resolve(name, base):
    for cand in (name, name + ".tex"):
        path = os.path.join(base, cand)
        if os.path.isfile(path):
            return path
    return None


def flatten(path, base, skip, seen, out, state):
    """Append (source_path, source_lineno, text, is_marker) tuples to out.

    Includes appearing before \\begin{document} are preamble (style files,
    macro definitions) and are left unexpanded: a reviewer wants the paper,
    not its class options. That rule replaces any per-project skip list.
    """
    real = os.path.realpath(path)
    if real in seen:
        print("warning: skipping recursive input %s" % path, file=sys.stderr)
        return
    seen.add(real)
    rel = os.path.relpath(path, base)
    with open(path, errors="replace") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.rstrip("\n")
            code = COMMENT_RE.sub("", line)
            if BEGIN_DOC_RE.search(code):
                state["in_body"] = True
            if state["in_body"] and ANY_INPUT_RE.search(code):
                # Splice every \input on the line, wherever it sits. Tables are
                # routinely wrapped, as in \resizebox{...}{\input{table/x}},
                # and dropping them would silently gut the paper under review.
                rest, spliced = code, False
                while True:
                    m = ANY_INPUT_RE.search(rest)
                    if not m:
                        break
                    name = m.group(1)
                    if os.path.splitext(os.path.basename(name))[0] in skip:
                        break
                    child = resolve(name, base)
                    if not child:
                        print("warning: unresolved \\input{%s} in %s:%d"
                              % (name, rel, lineno), file=sys.stderr)
                        break
                    head = rest[:m.start()]
                    if head.strip():
                        out.append((rel, lineno, head.rstrip(), False))
                    out.append((rel, lineno, "%% >>> %s" % name, True))
                    flatten(child, base, skip, seen, out, state)
                    out.append((rel, lineno, "%% <<< %s" % name, True))
                    rest, spliced = rest[m.end():], True
                if spliced:
                    if rest.strip():
                        out.append((rel, lineno, rest.strip(), False))
                    continue
            out.append((rel, lineno, line, False))
    seen.discard(real)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("main_tex", help="entry point, e.g. iclr-2027/main.tex")
    p.add_argument("-o", "--out", required=True, help="line-numbered output file")
    p.add_argument("--map", dest="mapfile", help="TSV of flatline -> source file, line")
    p.add_argument("--skip", default="",
                   help="extra comma-separated basenames not to expand; "
                        "preamble includes are skipped automatically")
    p.add_argument("--keep-comments", action="store_true",
                   help="keep %%-comments; useful when reviewing your own draft, "
                        "where TODO notes are part of what needs reading")
    args = p.parse_args()

    if not os.path.isfile(args.main_tex):
        sys.exit("no such file: %s" % args.main_tex)
    base = os.path.dirname(os.path.abspath(args.main_tex)) or "."
    skip = {s.strip() for s in args.skip.split(",") if s.strip()}

    rows = []
    flatten(os.path.abspath(args.main_tex), base, skip, set(), rows,
            {"in_body": False})

    kept, blank_run = [], 0
    for src, lineno, text, is_marker in rows:
        if not args.keep_comments and not is_marker:
            stripped = COMMENT_RE.sub("", text)
            # a whole-line comment vanishes entirely; an inline one leaves code
            if not stripped.strip() and text.strip().startswith("%"):
                continue
            text = stripped.rstrip()
        if not text.strip():
            blank_run += 1
            if blank_run > 1:
                continue
        else:
            blank_run = 0
        kept.append((src, lineno, text, is_marker))

    outdir = os.path.dirname(os.path.abspath(args.out))
    if outdir and not os.path.isdir(outdir):
        os.makedirs(outdir)
    width = max(3, len(str(len(kept))))
    with open(args.out, "w") as fh:
        for i, (_, _, text, _m) in enumerate(kept, 1):
            fh.write("%s  %s\n" % (str(i).rjust(width), text))

    if args.mapfile:
        with open(args.mapfile, "w") as fh:
            fh.write("flatline\tsource\tsrcline\n")
            for i, (src, lineno, _t, _m) in enumerate(kept, 1):
                fh.write("%d\t%s\t%d\n" % (i, src, lineno))

    files = sorted({src for src, _, _, _ in kept})
    print("wrote %s: %d lines from %d file(s)" % (args.out, len(kept), len(files)))
    for f in files:
        print("  %s" % f)


if __name__ == "__main__":
    main()
