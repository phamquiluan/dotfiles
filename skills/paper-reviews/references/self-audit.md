# Self-Audit Guide

How to adversarially audit a DRAFT review before delivering it. Run this after the review
is written and before the references are verified (SKILL.md step 5).

## Contents

- [Why this step exists](#why-this-step-exists)
- [The six failure modes](#the-six-failure-modes)
- [Auditor sub-agent prompts](#auditor-sub-agent-prompts)
- [Mechanical checks to run yourself](#mechanical-checks-to-run-yourself)
- [Applying the results](#applying-the-results)

## Why this step exists

A review that is confidently wrong on one point loses the authors' trust on all the others.
Every failure mode below has been observed in practice on real submissions, usually caught by
the user rather than by the reviewer. The cost of catching them yourself is one parallel
sub-agent pass; the cost of not catching them is a rebuttal that legitimately embarrasses you.

The strongest criticisms are the most dangerous, because they get the least scrutiny. Audit
the claims you are most confident about first.

## The six failure modes

### 1. Overstated absence claims

The single highest-frequency error. Any sentence of the form "the paper never", "is silent
on", "X is absent", "never defined", "no ablation exists", "never discussed" is a universal
claim over a document you have read once. Authors routinely address the point in the Limitations
section, a table note, a figure caption, or one clause of a sentence three pages away.

Rule: never ship an absence claim you have not verified with an exhaustive search using at
least three phrasings plus synonyms, including the Limitations and Discussion sections.

Typical corrections: "never defined" becomes "glossed but never given an equation";
"the paper is silent on X" becomes false outright when the preceding sentence makes that
very argument.

### 2. Quote-stops-before-the-concession

Quoting up to the point where the authors concede, and stopping. This is the error that reads
as bad faith even when it was an accident.

Rule: for every quote, read three sentences before and three after. If the surrounding text
hedges, qualifies, or concedes, either quote the hedge too or drop the criticism.

Watch particularly for sections that disclaim their own status in an opening or closing
paragraph. Attacking a section for overclaiming, when it opens by declining the claim, is a
guaranteed rebuttal.

### 3. Convention shopping in statistics

Computing a statistic two defensible ways and reporting the one that favours your narrative,
often without noticing you did it. This is the same defect reviewers criticize papers for.

Rule: state your convention once, apply it to every table identically, and report a
sensitivity check. If the conclusion flips under a different weighting, estimator, or unit of
analysis, say so and lower your confidence rather than picking a side.

Specific traps: series-weighted versus unweighted aggregation; recomputed versus printed
deltas; cluster-robust variance at small cluster counts, where G below roughly 30 makes t
approximations unreliable and a wild bootstrap has a p-value floor of 2 / 2^G.

### 4. Internal contradiction between review sections

Claiming X in one weakness and not-X in another. Reviews are written in pieces over a long
context and are not automatically self-consistent.

Rule: extract every numeric claim and every superlative ("the strongest baseline", "the
weakest entry", "above every other method") and check them against each other and against the
paper's tables.

### 5. Wrong or drifting citations

Two distinct problems. First, coordinates the authors cannot use: see the citation section in
SKILL.md and `scripts/map_paper_lines.py`. Second, citations that point a row or two off,
which is common in tables and makes a correct claim look fabricated.

Rule: verify that each cited coordinate resolves to the text you are quoting, especially for
table rows.

### 6. Unverified related-work claims

Numbers and quotes taken from an earlier analysis pass, or from memory, and never rechecked
against the source before becoming load-bearing.

Rule: every number attributed to a related work must be traced to a verbatim quote in that
work's text. Comparisons between differently-defined quantities (an absolute noise level
versus one scaled by a local standard deviation, for example) must either be made comparable
or explicitly flagged as not comparable.

## Auditor sub-agent prompts

Launch these three in parallel, in a single message. Give each the absolute path to the draft
review and the paper. Adapt the numbered items to the actual claims in the draft.

### Auditor A: absence claims

```
You are adversarially auditing a peer review I wrote, hunting for one failure mode:
claims that the paper never does X, is silent on X, or that X is absent.

REVIEW: <path>   PAPER: <path>

Extract EVERY negative/absence claim in the review. For each, search the paper
exhaustively (multiple phrasings, synonyms, the Limitations and Discussion sections,
all table notes and figure captions) and rule it TRUE, FALSE, or PARTIALLY TRUE.

Assume each claim is wrong until the text proves otherwise. Do not defend the review.
If the paper partially addresses something, quote the hedge and tell me the honest
residue of the criticism after accounting for it.

Also flag any place where the review quotes the paper but the surrounding sentences
materially change the meaning, especially where a quote stops just before a concession.

Return: one entry per claim with verdict, evidence quote plus line number, and the
corrected wording I should use.
```

### Auditor B: quotes, arithmetic, and internal consistency

```
You are auditing a peer review for QUOTE FIDELITY, ARITHMETIC, and SELF-CONSISTENCY.

REVIEW: <path>   PAPER: <path>

TASK 1. For every double-quoted passage attributed to the paper: confirm it is verbatim,
confirm the cited coordinate is correct (report the correct one if not), and read three
sentences either side reporting any context that changes the meaning.

TASK 2. Recompute every number in the review, showing your work with python3. Before
trusting any statistic derived from a table, verify the table's own rows and totals sum
correctly. Where the review computes a statistic that admits more than one defensible
convention, compute it BOTH ways and tell me whether the conclusion is convention-dependent.

TASK 3. Check the review against itself. List every superlative and numeric claim and
report any pair that contradicts.

Report every discrepancy however small. Where the review is correct, say so briefly.
```

### Auditor C: related-work claims

```
You are re-verifying claims about RELATED WORK in a peer review. Each is now
load-bearing, so each must be checked directly against the source. Assume each is
wrong until the source proves it.

REVIEW: <path>   SOURCES: <txts dir>

For each claim listed below, give a verbatim quote and its location, and mark
TRUE / FALSE / OVERSTATED: <enumerate the specific claims>

Flag any comparison between quantities that are not actually commensurable. For
anything you cannot verify from the sources provided, say so and tell me to soften
or drop it.
```

## Mechanical checks to run yourself

```bash
# house style, length limits, letter labels, and coordinates in one pass
python3 <skill>/scripts/lint_review.py review.md --paper paper.txt
```

## Applying the results

Fix everything the auditors confirm, then say plainly in your reply to the user which claims
were withdrawn or weakened and why. Do not quietly drop a criticism.

Weakening a criticism is not the same as deleting it. Most overstatements have a legitimate
residue: "never defined" weakens to "defined without a window", "the paper ignores X" weakens
to "the paper hedges X in one clause but does not act on it". Keep the residue, drop the
overstatement.

If an audit removes the basis for a rating or a recommendation, change the rating. A
recommendation that no longer follows from the surviving evidence is itself a defect.
