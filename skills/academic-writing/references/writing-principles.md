# Academic Writing Principles (30)

Canonical checklist consulted by the review agents (technical-reviewer,
logic-reviewer, writing-reviewer, consistency-checker, bibliography-auditor,
latex-layout-auditor, prose-polisher) and by any polish pass. Each principle
has an id; findings should cite them (e.g. "violates A2").

Adapted (MIT) from andrehuang/academic-writing-agents, itself drawing on
Michael Black's "Writing a Good Scientific Paper".

## A. Structure & Narrative

- **A1 Recursive consistency.** At every level (chapter, section, subsection):
  the intro's promises, the actual content, and the summary must match. "We
  discuss X, Y, Z" means the subsections cover exactly X, Y, Z in that order.
- **A2 Logical chaining.** No two adjacent paragraphs without a bridge; each
  section's ending motivates the next section's start. Paragraph-to-paragraph
  is the common failure, not section-to-section.
- **A3 Definition order.** Floats are defined in source in the order the text
  first references them; a teaser figure may lead but must be discussed
  promptly.
- **A4 Close every paragraph.** The last sentence concludes, synthesizes, or
  motivates what follows — never trails off into "which we detail below" or a
  bare citation.
- **A5 Claim-first exposition.** State what and why before how. No section
  opens with an equation or procedure before its purpose is stated.
- **A6 Goal–Problem–Solution rhythm.** Every section, down to subsections:
  what are we trying to achieve, what makes it hard, how we address it — in
  that order, so the reader cares before the technical content lands.
- **A7 The nugget.** One key insight per paper, statable in a sentence;
  every section, figure, and experiment serves it. The nugget is the insight,
  not the method.

## B. Prose & Style

- **B1 Non-exhaustive lists say so.** "benchmarks such as X, Y" not
  "benchmarks for X, Y" when the list is illustrative.
- **B2 No negation-contrast.** Rephrase "not X, but Y" positively; state Y.
  A strong AI-writing marker.
- **B3 Colloquial terms stay parenthetical.** Vivid shorthand may appear once
  in parentheses; formal terms carry titles and claims.
- **B4 Analytical prose, not enumeration.** Discussion flows
  claim → evidence → mechanism, in the author's voice (first-person plural,
  active, calibrated hedging) — not bullet-style listing dressed as prose.
- **B5 One idea per sentence.** A sentence needing "while", "unlike", or a
  semicolon to stitch two independent claims is two sentences.
- **B6 Calibrated confidence.** Assertive verbs for empirical facts
  ("achieves", "outperforms"); hedged verbs for causal explanation ("we
  hypothesize", "this suggests"). Never hedge a number; never assert an
  unproven mechanism ("because", "due to" need evidence).
- **B7 Ruthless conciseness.** "in order to"→"to", "due to the fact
  that"→"because", "it is worth noting that"→cut, "utilize"→"use". 100 words
  saying what 60 could is waste, not thoroughness.
- **B8 AI-tell scan.** Eliminate: negation-contrast (B2); "delve",
  "leverage", "landscape", "tapestry", "multifaceted", "paradigm shift";
  consecutive "Moreover/Furthermore/Additionally" openers; "Building on
  this"-style formulaic transitions; interchangeable "crucial/vital/
  essential"; balanced "on one hand / on the other" scaffolds.
- **B9 No fragments under 6 words.** Every sentence carries at least 6
  words. A punchy stub ("Conditioning granularity proves decisive.") merges
  into a neighboring sentence ("Conditioning granularity proves decisive,
  as matching each fault sample...").

## C. Math & Equations

- **C1 Math for clarity.** Notation that adds no precision is dropped; at
  most two new symbols per sentence; a symbol means one thing everywhere.
- **C2 Triple explanation.** The paper's core idea gets all three: intuitive
  text, formal equation, and figure — reinforcing, not repeating. Central
  concepts get at least two.
- **C3 Equation–code correspondence.** Symbols map to the pseudocode/released
  code names, and non-trivial mappings are stated (including dimension-order
  conventions).

## D. Figures & Tables

- **D1 Active figure use.** Hard concepts get a figure; method sections get
  an overview figure; no long dense stretches without visual support.
- **D2 Cross-reference all floats.** Every figure and table is referenced and
  discussed; no orphan floats.
- **D3 Figure–text–caption consistency.** What the figure shows, what the
  caption says, and what the body claims must agree — including spatial
  language ("top-left") matching the actual layout.
- **D4 One figure, one message.** A figure answering two questions is split.
- **D5 Interpret, don't just reference.** Never bare "as shown in Figure X";
  say what to notice and which comparison matters.
- **D6 Row alignment.** Subfigure grids align rows with `[t]`; mixed heights
  (caption on one subfigure only, raster next to vector) get explicit height
  constraints.
- **D7 Caption self-sufficiency.** A caption alone explains what is shown,
  defines the figure's symbols/abbreviations, states the takeaway, and
  carries units. Readers scan captions before deciding to read.

## E. Citations & Bibliography

- **E1 Cite named artifacts.** Every named model, benchmark, and dataset is
  cited at first use *in each chapter/section readers may enter directly*.
- **E2 First-mention completeness.** Foundational methods (Transformer,
  ResNet, ...) are cited at first mention per chapter even when famous.
- **E3 Bibliography hygiene.** Required fields per entry type; brace-protect
  proper nouns in titles (`{ImageNet}`); replace arXiv-only entries whose
  published version exists; one format per author name and one style per
  venue name across the file; no duplicates, no "?" in the compiled PDF, no
  stale "to appear".

## F. Process & Meta

- **F1 Limitation placement.** Papers: after the results build confidence —
  for NeurIPS/ICML/ICLR a limitations section is required, so state
  boundaries plainly, each with context or mitigation, never defensively.
  Thesis/internal documents: at the point the design decision is made.
- **F2 Final negation-contrast audit.** Before finalizing, grep for
  `is not.*but|not to.*but to|not only.*but also` and rephrase positively.
