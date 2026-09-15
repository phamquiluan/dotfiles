---
name: academic-writing
description: Write, edit, and polish academic papers for top-tier CS venues (ICSE, FSE, ASE, ICML, NeurIPS). Provides rigorous writing style guidance for peer review, polish passes over LaTeX sources at light/moderate/strict levels with strict preservation guardrails (citations, math, numbers untouched), and a Vietnamese-L1 interference checklist for grammar passes. Use when writing paper prose, when asked to polish, proofread, or fix the English of a draft, or when editing any LaTeX manuscript text.
---

# Academic Writing Skill

Use this skill when writing or editing academic content for software engineering and machine learning conferences.

The 30 numbered writing principles (A1–F2: structure, prose, math, figures,
citations, process) live in
[references/writing-principles.md](references/writing-principles.md), the
canonical checklist shared with the review agents. Read it for any full-paper
review or strict-level polish, and cite principle ids in findings.

**Punctuation, in one line, because it is the most frequently broken rule
here:** no em-dashes, no semicolons, and no `<claim>: <elaboration>` colons in
prose. Removing an em-dash by substituting a colon is the usual failure and
recreates the banned shape. Use two sentences, or "e.g.," / "i.e.," / "that
is," / "namely". Full rule and worked examples in
[Punctuation Guidelines](#punctuation-guidelines) below.

## Conservative Editing Philosophy

**Principle: Minimal intervention.** Only change what is actually problematic. The author's voice and intentional choices take precedence over style preferences.

**Before making any change, ask:**
1. Is this actually wrong, or just different from my preference?
2. Could this be an intentional stylistic choice?
3. Does this change improve clarity, or just impose a different style?

**Preserve author intent:**
- Keep word choices the author uses consistently (e.g., "merely", "significantly")
- Keep structural patterns the author has established
- Keep rhetorical devices like strategic repetition

**Strategic repetition is valid.** Repetition for emphasis differs from redundancy:
- **Keep:** Repeating a key thesis statement in both the response intro and the quoted paper text (reinforces the main point)
- **Keep:** Parallel structure that repeats phrases for rhetorical effect
- **Remove:** Saying the same thing twice with no added emphasis or clarity

## Workflow Behavior

1. **Scope the request:** Identify what specific issues exist in the text. Do not invent problems.
2. **Categorize issues:** Separate actual errors (grammar, unclear meaning) from style preferences
3. **Present minimal changes:** Only propose changes for actual issues, not style preferences
4. **Preserve author choices:** If something could be intentional, assume it is
5. **Ask before restructuring:** For structural changes, ask: "Would you like me to restructure X, or keep the current structure?"
6. **Apply edits only when approved**

## Polish Levels

Scope every polish request to one of three levels before touching the text,
and say which level is being applied. When the request does not name one,
default to **moderate**; never escalate a level without asking.

| Level | License | Typical request |
|-------|---------|-----------------|
| **light** | Grammar, articles, agreement, typos, punctuation only. No rephrasing, no reordering. | "fix my English", "proofread this" |
| **moderate** | Light, plus clarity edits within a sentence: cut filler, replace vague words, repair flow between adjacent sentences. Sentence order and paragraph structure stay. | "polish this section" |
| **strict** | Moderate, plus restructuring toward top-venue standards: reorder sentences, merge or split paragraphs, rewrite topic sentences. Each structural change still needs approval per the workflow above. | "make this publication-ready" |

A "fix my grammar" request handled at strict level is the classic failure
mode: the author gets back a paper that is no longer theirs.

## Polish Guardrails

A polish pass edits prose. It must never alter, in any level:

- `\cite{...}` keys, `\ref`/`\label`/`\autoref` names, and BibTeX entries
- Math: inline `$...$`, display environments, macro definitions
- **Numbers and units** in text — a reported metric is data, not prose
- Named entities: method names, dataset names, system names, author names
- Verbatim quotations and anything inside `verbatim`/`lstlisting` blocks
- LaTeX comments (`% ...`) — they are notes to the authors, not prose
- Technical terms the paper defines, even when a synonym reads better

If any of these looks wrong — a citation that seems misplaced, a number that
contradicts a nearby table, an undefined reference — **flag it separately;
never fix it silently.** A substantive issue disguised as a copy-edit is how
wrong numbers enter camera-ready papers.

After editing a LaTeX source, recompile it (the project's build command, or
`pdflatex` twice) and confirm no new errors or warnings were introduced
before reporting done.

Report changes as a numbered before/after list with a one-line justification
each, and list the flagged substantive issues separately at the end.

## Vietnamese-L1 Grammar Pass

The author's first language is Vietnamese. On every light-or-above polish
pass, additionally check the draft against
[references/vietnamese-interference.md](references/vietnamese-interference.md) —
a checklist of interference patterns (articles, plural marking, agreement,
tense, calques such as "discuss about") with fixes and grep-able self-checks.
Read it whenever polishing prose the author wrote; skip it when generating
fresh text.

## Voice and Sentence Structure

**Use active voice (80%+ of sentences):**
- "We propose..." / "We show..." / "We evaluate..."
- "Our method achieves..." / "[METHOD] identifies..."

**Reserve passive voice for:**
- Established facts: "Root cause analysis is widely used..."
- Method descriptions: "The anomaly score is computed as..."
- Emphasizing results over actors: "A 15% improvement was observed..."

**Sentence length:**
- Short sentences for key claims: "This approach fails when the graph is unknown."
- Every sentence must have at least 6 words. Never write punchy fragments
  like "Conditioning granularity proves decisive." Merge a short key-claim
  sentence into a neighboring sentence instead ("Conditioning granularity
  proves decisive, as matching each fault sample...").
- Longer sentences for technical explanations with embedded clauses
- Split run-on sentences only when they impede comprehension

## Abstract Structure (6 Parts)

1. **Problem importance** (1-2 sentences): Why this matters
2. **Current limitations** (1-2 sentences): What existing methods lack
3. **Key insight** (1 sentence): Core observation or reformulation
4. **Proposed solution** (1-2 sentences): Method name and approach
5. **Results** (1-2 sentences): Specific metrics (percentages, speedups)
6. **Availability** (optional): Code/data links

## Introduction Structure (10 Paragraphs)

1. **Motivation**: Why the problem matters, broad applications
2. **Current state**: What exists, with citations
3. **Gap identification**: Limitations of existing work
4. **Deeper analysis**: Why the gap exists (technical reasons)
5. **Related approaches**: What others have tried, why insufficient
6. **Proposed direction**: High-level idea before technical details
7. **Technical solution**: Method introduction with key components
8. **Challenges addressed**: Specific improvements over prior work
9. **Results summary**: Key metrics and comparisons
10. **Contributions**: Bulleted list (3-4 items), each starting with action verb

## Claim Presentation

**For contributions:**
- "To the best of our knowledge, this is the first..."
- "We make the following contributions:"
- "Our key insight is that..."

**For results (use specific numbers):**
- "[METHOD] achieves 67% Top-1 accuracy, a 253% improvement over..."
- "Our method requires only 8ms per diagnosis, 9,700x faster than..."

**For theoretical claims:**
- "We show that..." / "We prove that..." / "We demonstrate that..."

## Hedging Language (Calibrated Uncertainty)

| Certainty Level | Words to Use |
|-----------------|--------------|
| **Strong** | demonstrates, achieves, proves, establishes, shows |
| **Moderate** | indicates, reveals, suggests, implies |
| **Cautious** | may, might, appears to, potentially, likely, can |

**Use hedging for:**
- Speculation beyond direct evidence
- Generalizations beyond experimental scope
- Theoretical implications not fully proven

## Transition Phrases

| Function | Phrases |
|----------|---------|
| **Contrast** | However, In contrast, Nevertheless, Unlike, While |
| **Addition** | Furthermore, Moreover, Additionally, In addition |
| **Sequence** | First, Second, Third, Finally, Subsequently |
| **Cause/Effect** | Therefore, Thus, Consequently, As a result, Hence |
| **Evidence** | Specifically, In particular, For instance, As shown in |
| **Emphasis** | Importantly, Notably, Crucially, Interestingly |

## Mathematical Writing

**Before equations:** Provide context
- "The anomaly score is defined as:"
- "We compute the ranking function using:"

**After equations:** Define variables immediately
- "where $S^I_c$ denotes the internal score and $S^E_c$ the external score."

**References:** Use `Eq.~\ref{eq:name}` or `Equation~\ref{eq:name}`

**Displayed equations:** Use for important formulas that will be referenced.

## Citations

**Integrate naturally:**
- "Recent work on causal discovery~\cite{pearl2009} has shown..."
- "Following~\cite{budhathoki2022}, we define..."

**Group by topic:**
- "...has been explored in microservices~\cite{a,b,c} and cloud systems~\cite{d,e}."

**Citation placement:** Make clear what is being cited
- Good: "Prior work using mean and standard deviation~\cite{Li2022Circa} can degrade..."
- Bad: "We prefer median over mean~\cite{Li2022Circa}..." (unclear if citing or critiquing)

## Figures and Tables

**Pre-reference:** Explain what to look for
- "To evaluate scalability, we measure runtime across dataset sizes."

**Reference format:**
- "Table~\ref{tab:results}" / "Figure~\ref{fig:overview}"
- "As shown in Figure~\ref{fig:overview}..."

**Post-reference:** Interpret the data
- "From Table~\ref{tab:results}, we observe that [METHOD] consistently outperforms..."

**Captions:** Self-contained, describe what is shown and key takeaway

## Terminology Conventions

- **Acronyms:** Introduce once with full form: "Root Cause Analysis (RCA)"
- **After introduction:** Use acronym only: "RCA"
- **Novel concepts:** Use quotes on first use: 'internal properties', 'external properties'
- **Consistency:** Choose one term and use it throughout (not alternating synonyms)
- **Variable introduction:** "Let $x$ denote..." then use $x$ consistently

## Phrases to Use

- "We propose..." / "We introduce..."
- "Our key observation is that..." / "Our key insight is that..."
- "To address this challenge, we..."
- "We evaluate on..." / "We conduct experiments on..."
- "Results demonstrate that..." / "Our findings show that..."
- "Compared to [baseline], our method..."
- "Let $x$ denote..." (for variable introduction)

## Phrases to Avoid

- "Obviously" / "Clearly" / "It is easy to see" (condescending)
- "Very" / "Really" / "Extremely" (vague intensifiers)
- "We believe" (use "We hypothesize" or "We conjecture" for speculation)
- "Proves" for empirical results (use "demonstrates" or "shows")
- "Novel" / "Innovative" without substantiation
- First person singular "I" (use "we" even for single author)

## Punctuation Guidelines

- Em-dashes (`---`): avoid in prose; use commas or separate sentences
- Semicolons: avoid in prose; split into separate sentences
- Colons in prose: NEVER write the `<claim>: <elaboration>` sentence shape,
  where a colon introduces a clause that explains or expands the claim
  before it. Reserve colons for lists, definitions, and mathematical
  notation only. Rewrite the shape as two sentences, or fold the
  elaboration in with "e.g.," "i.e.," "that is," or "namely".

  ✗ "RCA asks a single question after a failure: which part of the system caused it."
  ✓ "After a failure, RCA asks which part of the system caused it."
  ✗ "The central finding concerns granularity: matching each sample at its own operating point beats a pooled reference."
  ✓ "The central finding concerns granularity. Matching each sample at its own operating point beats a pooled reference."
  ✗ "We report reusable negative results: the win does not transfer, and the leak does not diagnose topology error."
  ✓ "We report reusable negative results, e.g., the win does not transfer, and the leak does not diagnose topology error."

## Overused Constructions (limit hard)

Each of these reads fine once and becomes a tic when repeated. Keep each
to a handful of uses per paper, at most one per paragraph:
- "rather than" — prefer "instead of", or restructure to state only the chosen thing
- the contrast appositive "X, not Y" — state X; drop ", not Y" unless the contrast is itself the point
- ", so " as a connective — prefer "therefore", "hence", "thus", "which means", or start a new sentence
- Negation-heavy hedging that defines things by what they are not ("does
  not", "is not", "we do not claim"). Prefer stating what IS true, e.g.,
  "the win does not transfer" → "the win is specific to N-CMAPSS". Keep a
  negation only when the negative claim is itself the finding (a
  retraction, a null result) or a scope statement honesty requires.

## Forbidden Words

Never use these words in prose: "inert", "headline" (as adjective),
"load-bearing", "rungs", "conflates". Substitutes, e.g., "has no effect" /
"statistically indistinguishable from no effect" (inert), "main" /
"central" (headline), "essential" / "carries most of the accuracy"
(load-bearing), "steps" / "levels" (rungs), "mistakes X for Y" /
"confuses X with Y" (conflates).

Also never (added 2026-08-27): "probe", "readout", "episode",
"asserted", "unasserted", "concede", "lever". For probe/readout, pick
by sense: "sensor" (physical device), "investigates" (verb; avoid
"tests" here, which reads as test set in ML), or name the specific
diagnostic (e.g., "the encoder diagnostic"); "case" for episode; "declared" / "undeclared" for asserted / unasserted; state
the loss plainly instead of conceding it; name the mechanism directly
("conditioning", "topology") or use "ingredient" / "factor" / "effect"
/ "design choice" for lever.

## No Self-Deprecating Scope Disclaimers

Never write sentences that talk the paper down: "this is not a claim of
state-of-the-art", "an empirical account, not a method paper", "we make
no claim of...". State what the results show and where the method
loses, precisely, and frame losses as design targets. Honest scope
statements are specific ("the win is specific to N-CMAPSS, seed spread
0.500"), never apologetic.

## Common Revision Patterns

Apply these only when they improve clarity, not mechanically:

| Pattern | When to Apply |
|---------|---------------|
| Split long sentences | Only if comprehension is impeded |
| Convert passive to active | Only if the actor matters for understanding |
| Shorten parentheticals | Only if they interrupt flow significantly |
| Introduce variables | Only if the same term appears 3+ times in close proximity |
