---
name: academic-writing
description: Write and edit academic papers for top-tier CS venues (ICSE, FSE, ASE, ICML, NeurIPS). Provides rigorous writing style guidance for peer review.
---

# Academic Writing Skill

Use this skill when writing or editing academic content for software engineering and machine learning conferences. Follow these patterns rigorously.

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
- Longer sentences for technical explanations with embedded clauses
- Avoid run-on sentences. Split into separate sentences instead

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

**Examples:**
- "This suggests that structural knowledge may not be necessary..."
- "The performance degradation likely results from..."
- "These findings indicate that..."

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

**Never orphan equations** — always embed in narrative flow.

**Displayed equations:** Use for important formulas that will be referenced or that define key quantities.

## Citations

**Integrate naturally:**
- "Recent work on causal discovery~\cite{pearl2009} has shown..."
- "Following~\cite{budhathoki2022}, we define..."

**Group by topic:**
- "...has been explored in microservices~\cite{a,b,c} and cloud systems~\cite{d,e}."

**With evaluation:**
- "As demonstrated in~\cite{hardt2024}, this approach struggles with..."

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
- Em-dashes (`---`) for parenthetical statements. Use commas or separate sentences instead
- Semicolons (`;`) in prose. Split into separate sentences instead
- Colons (`:`) in prose for introducing clauses. Reserve for lists, definitions, and mathematical notation

## Common Revision Patterns

| Before | After |
|--------|-------|
| Run-on sentence with multiple clauses | Split into 2-3 shorter sentences |
| "which better assists..." | "This helps... more effectively" |
| "This formulation follows..." | "[Method] performs..." (active voice) |
| "A recent work has theoretically proved" | "Recent theoretical work proves" |
| "are consolidated to yield" | "we aggregate... to obtain" |
| "may be significantly affected" | "can degrade" (specific effect) |
| Long parenthetical "(i.e., the time series data corresponding to each metric, log template, or trace)" | Short "(i.e., metric, log template, or trace)" |
| Repeating "time series $x$" multiple times | "let $x$ denote its time series" then use $x$ |
