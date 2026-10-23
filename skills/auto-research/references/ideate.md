# Mode: ideate

Produce a small number of ideas that are specific enough to run, and honest
about what already exists.

## Contents

- [Gather the ground truth](#gather-the-ground-truth)
- [Generation moves](#generation-moves)
- [Novelty check](#novelty-check)
- [Triage](#triage)
- [Write to IDEAS.md](#write-to-ideasmd)

## Gather the ground truth

Read before generating. Ideas invented ahead of the reading are almost always
either already published or unrunnable.

1. **Existing state.** `ledger.py status` plus `IDEAS.md`. Dropped ideas carry
   the reason they were dropped; do not regenerate them.
2. **Findings.** Everything in `research/findings/`. Failure analyses are the
   richest idea source in the project because they are specific to this setup.
3. **Code that exists.** If the project keeps a catalogue of downloaded
   research code, read its index and then the entries for candidate repos; a
   good entry lists reusable components with exact paths and signatures,
   synthetic generators, and gotchas. An idea whose components already exist
   and are catalogued is worth several that are not. An entry is still a
   summary: if an idea will rest on a component, hand off to `dive-deep code`
   before treating it as fact.
4. **Literature.** `search-related-works` on the closest known paper, and the
   review notes already in the repo.

## Generation moves

Work through these deliberately rather than free-associating. Each move should
yield candidates; most will die in triage, which is the point.

**Transfer.** A mechanism that works in a neighbouring setting, moved here.
Name the assumption that breaks in transit — that is the contribution.

**Compose.** Two catalogued components that have never been combined, where the
first supplies what the second assumes. Check the cards for whether the
interfaces actually meet.

**Relax.** Take a published method's strongest assumption (known graph, hard
interventions, observed regime labels, stationarity) and ask what survives
without it. Weakening an assumption is a contribution only if the guarantee or
the empirical result survives in some form; say which.

**Invert the failure.** Read a finding note and ask what method would not have
failed that way. This is the highest-yield move once experiments exist.

**Change the object.** Same method, different target: point estimate to
set-valued, single fault to multi-fault, detection to attribution.

## Novelty check

An idea that survives triage without a literature check is not an idea, it is a
guess. For each surviving candidate:

1. `search-related-works` with the idea's own terms, not the parent paper's.
2. Read the titles and abstracts of the top hits, and follow citations from any
   that look close.
3. Record the verdict in the idea: **novel** (nothing does this), **delta**
   (published work is close, and here is the specific difference), or
   **published** (drop it, and say where it was published).

"Delta" is the common and acceptable outcome. State the delta in one sentence.
If the sentence needs a "but also", the delta is too thin.

A delta claimed against an abstract is not a delta. Before an idea's novelty
rests on how it differs from the nearest paper, read that paper properly:
`/auto-research dive-deep paper <name>`. Papers routinely claim less than the
field repeats about them, which either kills the delta or widens it.

**Escalate when targeted search cannot settle it.** A few queries and a
citation hop are enough for most candidates, but not when the verdict hinges
on coverage: the idea claims to be *first* to do something, the delta sits in
a crowded or fast-moving area where one missed paper kills it, or the idea is
about to anchor months of work. For those, hand off to the
`systematic-review` skill (protocolled search, dedup, screening, PRISMA
counts) instead of stretching a spot check into a coverage claim. It is a
multi-session pipeline with its own `review/` state, so do not run it inline:
record the verdict as **delta (provisional — systematic check pending)** in
`IDEAS.md`, and treat the systematic pass as a prerequisite the idea must
clear before `experiment` spends real compute on it. Its `synthesis.md` then
replaces the provisional verdict — and doubles as the related-work backbone
at `paper-writing` time.

## Triage

Score each candidate on four axes, briefly:

- **Falsifiable** — is there a run that would show it is wrong? If not, drop it.
- **Feasible** — components, data, and compute available now. Cite the card or
  dataset path.
- **Load-bearing** — if it works, does anything downstream change?
- **Cheap to kill** — what is the smallest run that would refute it, and how
  long does it take?

Rank by cheapest-to-kill among those that pass the first three. Carry forward
three to five ideas, not fifteen.

## Write to IDEAS.md

Append a section per surviving idea, using the next free `I<n>`:

```markdown
## I4 Regime labels as weak interventions for soft-fault attribution

**Status:** proposed
**Novelty:** delta - CITRIS assumes known intervention targets; here the regime
label is observed but the target is not.
**Feasible:** CITRIS encoder (see its catalogue entry); N-CMAPSS regimes.

**Claim.** Observed operating regimes act as weak interventions, enough to
identify soft-fault latents up to permutation without knowing which variable
each regime touches.

**Kill test.** Synthetic DGP with three regimes and one soft fault. If MCC does
not separate from the regime-blind baseline at n=3 seeds, the claim is dead.
Roughly two GPU-hours.

**Open questions.** Does it need regime balance? What happens at one regime?
```

The **Kill test** field is what `experiment` mode reads first, so make it
concrete: dataset, metric, baseline, and the threshold that would refute.

Finish by reporting the ideas added, the ones dropped and why, and which idea
`experiment` should take first.
