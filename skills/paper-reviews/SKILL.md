---
name: paper-reviews
description: "Write evidence-backed peer reviews of conference and journal submissions (ML venues such as ICML, NeurIPS, ICLR, IJCAI; SE venues such as ICSE, FSE, ASE, EASE, ESEM; journals such as TOSEM, TSE, EMSE), filling in the venue's review form. Use when the user asks to review a paper or manuscript, write or revise a referee report, fill out a review form, review a survey or a revised submission, or evaluate a paper's artifact for ACM/SIGSOFT badges. Every point cites page and line coordinates the authors can find, related work is checked against the literature, and the draft is adversarially audited before delivery."
---

# Paper Reviews

The goal is a review the authors cannot dismiss. Every point is anchored to text they can
find, quoted fairly, and has survived an adversarial re-read. The content rules and house
style below are the user's standing preferences and are hard rules unless the user overrides
them for a specific review.

`<skill>` below is this skill's directory.

## Inputs

A review folder usually holds the paper (`paper.pdf` and/or `paper.txt`), the venue's review
form, and sometimes related works (`txts/`), the CFP or reviewer guidelines, an appendix, and
an artifact. Work with what is there.

- PDF only: `pdftotext -layout paper.pdf paper.txt`. Layout mode keeps the margin line numbers
  and form feeds the coordinate script relies on.
- No related works: find them with the `search-related-works` skill or the `novelty-reviewer` agent.
- Artifact: evaluate it when it is provided. When the paper links one but the user did not
  mention it, ask once whether to include artifact evaluation.
- The form defines the output. Fill it in its own format (e.g., `[x]` checkboxes in a `.txt`
  form) and save under the name the user gives.

## Workflow

1. Fix the citation coordinates before reading. Run
   `python3 <skill>/scripts/map_paper_lines.py paper.txt --detect`. Most submissions print
   margin line numbers that reset on every page, and the authors never saw your `.txt`, so a
   flat offset like "Line 759" is useless to them. With per-page numbering cite
   `(p. 11, line 40)` or `(p. 11, lines 37-38)`. Without it, cite `(Line 42)` / `(Lines 42-45)`
   from the extracted text, or `(p. 11, Sec. 3.2)` for journal manuscripts without line
   numbers. State the convention once at the top of the review. Drafting with flat offsets and
   running `--convert` at the end is fine. Spot-check table rows with `--lookup`, because
   conversion cannot fix a citation that points at the wrong row.

2. Read the whole paper, recording a location and a short quote for each notable point as you
   go. Pay particular attention to load-bearing assumptions (methodological, task, evaluation,
   modeling), which are often implicit. For each, note where it is stated or revealed, whether
   it holds in the claimed setting, and whether the authors verify it. Unverified assumptions
   are often the strongest weaknesses and questions.

3. Check the claims against related work. Scale the effort to the material. Read a handful of
   papers directly. For a larger set, split them into thematic clusters and give each cluster
   to a parallel sub-agent along with the paper's claimed contributions. Ask what the related
   work does that the paper does not, which baselines or datasets are missing, and whether
   anything contradicts the paper, with quotes from both sides. The `novelty-reviewer`,
   `technical-reviewer`, and `logic-reviewer` agents are available for a fuller panel. For
   double-blind venues, do not web-search the submission's own title or distinctive phrases.

   Before drafting, tag each related work. If it is in the paper's bibliography, cite it by the
   paper's own number, `[9]`. If not, it is reviewer-introduced and gets a letter, `[A]`, `[B]`,
   in order of first appearance. Never both (`Prather et al. [A] (cited as [9])`), and no
   author-name prefix by default. A one-clause gloss on first mention is fine when `[9]` alone
   is ambiguous.

4. Draft the review in the form's structure, following the content rules and house style below.
   See `references/evidence-format.md` for good and bad examples.

5. Audit the draft. This step is never skipped. Read `references/self-audit.md` and run its
   three auditor sub-agents in parallel. Audit hardest the claims you are most confident in.
   Keep the legitimate residue of an overstatement and drop the overstatement. Change a rating
   if its basis goes. Tell the user which claims were withdrawn or weakened.

6. Finalize.
   - Verify every reviewer-introduced reference exists with the right title, authors, and year,
     via its arXiv page, its DOI, or `search-related-works` (`--ids`, `--title-abstract`). Many
     SE and journal papers are not on arXiv, which does not make them fake. Drop anything you
     cannot verify and rewrite the sentences that relied on it.
   - The References section lists only letter-labelled works, each cited at least once. Use
     the venue's requested format (journal forms often want all authors, full title, venue,
     year, and URL).
   - Ratings must follow from the surviving weaknesses, each justification cites at least two
     pieces of evidence, and the recommendation follows from the ratings.
   - Run `python3 <skill>/scripts/lint_review.py review.md --paper paper.txt` and fix what it
     reports. It checks the house style, sentence-count limits, letter labels, and coordinates.

## Content rules

- Summary: exactly one paragraph of 5 to 7 sentences, in near-layman language that an
  SE-literate non-specialist can follow without the paper. Gloss any unavoidable
  paper-specific term on first use. Cover what the paper is, the problem, how the approach
  works, what it is evaluated on, and the main result. Keep it neutral, with no judgement, lists,
  or subheadings. Citations are optional here.
- Strengths: numbered, 1 to 2 sentences each, with an inline citation.
- Weaknesses (and journal major comments): numbered, 3 to 5 sentences each. Sentence 1 is the
  judgement. The rest give the evidence (a quote with its coordinate, or `[9]` / `[A]`) and the
  actionable thought, i.e., why it matters and what would fix it. If it needs more than 5
  sentences, split it in two.
- Questions: each cites the paper and says what the reviewer would update if the authors
  answer convincingly.
- Every strength, weakness, and question carries at least one citation.

## House style

The review should read like a careful human reviewer wrote it. Banned:

- `**bold**`, including bolded item titles like `**W1 — Weak evaluation.**`. Use `###` and
  `####` headings for structure.
- Em-dashes (`—`) and semicolons in prose.
- The `<claim>: <elaboration>` colon. It is the usual substitute for a banned em-dash, so it
  reads as a fix but is the same tic. Use colons only before lists, definitions, and ratios.
  ✗ "This paper asks a practical question: does thinking mode help?"
  ✓ "This paper asks whether thinking mode helps an agent diagnose an outage."
- The word "headline". Name the thing meant: main, central, reported, abstract, lead with.
- Decorative emoji or symbols.

Allowed: headings, numbered and `-` lists, verbatim quotes in double quotes, and tables only
where the form asks for one.

Math in OpenReview fields uses `$...$` and `$$...$$` with double-escaped backslashes. See
`references/openreview-math.md`. For plain-text forms, or when the user asks for plain text,
drop all Markdown emphasis, write headings as uppercase lines, flatten tables into
`Label: value` lines, and write math in ASCII (`lambda`, `Q_hat_theta`).

## Venue types

- Conference (OpenReview, HotCRP, EasyChair): summary, strengths, weaknesses, questions, and
  ratings, as the form asks. Grouping weaknesses under topic headings with labels such as
  `E1.` or `N2.` is fine.
- Journal (TOSEM, TSE, EMSE, ...): usually a recommendation (accept, minor revision, major
  revision, reject) and comments to the authors. Use the summary rule above, then major
  comments (built like weaknesses) and minor comments (1 to 2 sentences each, still cited),
  and end with what a revision must address for you to recommend acceptance.
- Survey: judge coverage (search for missed work), the soundness of the taxonomy, and whether
  the literature-collection method (search strings, inclusion criteria) is reproducible.
- Revision round: check each earlier concern against the response letter and the changed text,
  and say whether it is resolved, partially resolved, or unresolved, with coordinates in the
  revised manuscript.
- Generative-AI disclosure fields: answer truthfully. Ask the user if you are unsure of their
  preferred wording.

## Artifact evaluation

When evaluating an artifact, follow `references/artifact-evaluation.md` (ACM/SIGSOFT
Available, Functional, Reusable). If the venue's call for artifacts is provided, its criteria
take precedence.

## Resources

- `scripts/map_paper_lines.py`: flat `.txt` offsets to printed page and margin-line
  coordinates. Modes `--detect`, `--lookup N ...`, `--convert REVIEW`, `--check REVIEW`.
- `scripts/lint_review.py`: mechanical checks for house style, length limits, letter labels,
  and (with `--paper`) coordinates.
- `references/self-audit.md`: the six failure modes and the three auditor prompts (step 5).
- `references/evidence-format.md`: citation formats with good and bad examples.
- `references/openreview-math.md`: TeX delimiters and escaping for OpenReview.
- `references/artifact-evaluation.md`: badge criteria and output format.
