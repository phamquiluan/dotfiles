# Mode: paper-writing

Draft or update the paper so it states the idea as it stands now, supported by
the experiments that survived. The paper is the argument, not the log.

## Contents

- [The rule](#the-rule)
- [What that does not license](#what-that-does-not-license)
- [Fix the story spine first](#fix-the-story-spine-first)
- [Source every claim from state](#source-every-claim-from-state)
- [Figures](#figures)
- [The venue is an ML conference](#the-venue-is-an-ml-conference)
- [Section targets](#section-targets)
- [The staleness sweep](#the-staleness-sweep)
- [Prose and build](#prose-and-build)

## The rule

Write the paper as if the current understanding were known from the start.
A reader wants the shortest path from problem to evidence, not the order in
which things were discovered.

Keep out of the draft:

- The trajectory. No "we initially tried", "in an earlier version", "this led
  us to". The abandoned attempt is not a finding.
- Dropped ideas and superseded framings, however much work they cost.
- Bugs found and fixed. A run that was wrong and was rerun contributes the
  corrected number and nothing else.
- Exploratory probes and calibration runs that only informed the design.
- Hedges inherited from a claim that has since been narrowed. Once the scope is
  known, state it as a boundary, not as an apology.

`IDEAS.md` history, `findings/`, and the ledger hold the trajectory. That is
their job, and it is why the paper does not need to.

## What that does not license

Cutting the chronology is not the same as cutting inconvenient results. The
distinction decides the paper's honesty, so apply it explicitly:

| Belongs in the paper | Stays out |
|---|---|
| An ablation showing a component does not help | The three buggy versions of that ablation |
| The sensitivity cliff bounding the claim | The sweep that was too narrow to see it |
| A dataset where the method loses, if it was in the committed set | A probe run to check a dataloader |
| A baseline that beats the method on one metric | The tuning effort spent on the method |
| The assumption the method needs and cannot verify | The earlier claim that it did not need it |

Every dataset, baseline, and metric committed to in `revise` gets reported,
win or lose. If a result is absent from the paper, the reason must be
methodological and stated, never that it was unflattering. A negative ablation
is a contribution: it tells the reader which part matters.

## Fix the story spine first

Before writing or revising any section, write `research/STORY.md` — or reread
and update it if it exists. It is the paper's argument in one place:

```markdown
# Story (as of EXP-0031)

**Claim.** Observed operating regimes act as weak interventions, identifying
soft-fault latents up to permutation without known intervention targets.
**Why it matters.** Turbomachinery RCA has regimes but never has targets.
**Why it is hard.** Existing identifiability results assume known targets.
**What is new.** The regime-as-weak-intervention construction and its
identifiability condition.
**Evidence.** MCC 0.81 vs 0.62 on synthetic (EXP-0021, 5 seeds); holds on
N-CMAPSS (EXP-0028); degrades below three regimes (EXP-0030).
**Scope.** Requires regime balance within 3:1; untested on multi-fault.
**Contributions.** (1) ... (2) ... (3) ...
```

Every paragraph in the paper serves one line of this spine. A paragraph that
serves none is cut, however good it is. When the spine and the draft disagree,
the spine is right and the draft is stale.

Derive the spine from `IDEAS.md` (the active idea, post-revision), the findings
notes, and the ledger — not from what the paper currently says.

## Source every claim from state

- **Numbers** come from the ledger and the generated tables, never retyped from
  memory or from an older draft. Where the project has a table-generation step,
  run it and let it write the table rather than editing numbers by hand; if it
  has none and numbers are being typed twice, that is worth fixing before the
  next round. `research/WORKSPACE.md` names the command.
- **Every number in prose** — abstract, intro, discussion — must match the
  table it summarises. Check them against the ledger, not against each other.
- **Seed counts and spread** are reported wherever a comparison is drawn.
- **Claims about mechanism** trace to a finding note or an ablation, and the
  paper should say which experiment supports them.
- **Scope statements** come from the sensitivity cliffs, with their numbers.
- **Related-work positioning** comes from the novelty verdict in `IDEAS.md` and
  any `deep/paper-*.md` notes. A paper characterised only from its abstract is
  a citation risk; hand off to `dive-deep paper` before asserting what a rival
  method assumes or cannot do.

## Figures

Half of a results section is figures, and they rot the same way numbers do.

Every figure is **generated, never hand-tweaked**. A plotting script reads the
artefacts in `research/runs/EXP-<id>/` and writes the figure; nothing is
adjusted afterwards in an editor, because the next rerun silently reverts it
and the figure then disagrees with the table beside it.

The craft of making the figure — script structure, venue sizing, style, what
plot type fits which result — is not this mode's job: **load the
`figure-generator` skill** and hand it the run directories and the message the
figure must carry. What this mode still owns:

- Deciding *which* figures the argument needs, and which EXP ids feed each.
- Traceability: every figure traces to the runs that produced it, or it
  cannot be defended in a rebuttal.
- Recording the rebuild command in `research/WORKSPACE.md` so one invocation
  regenerates every figure.
- Regenerating every figure after any rerun, in the same pass as the tables.
  A stale figure is worse than a missing one.

## The venue is an ML conference

Write for NeurIPS, ICLR, or ICML unless `research/WORKSPACE.md` names another
venue. That fixes several things that would otherwise be decisions:

- **The main text is short and the appendix is not.** Eight or nine pages
  carry the argument: claim, method, main comparison, the ablations that do
  attribution, the sensitivity cliffs that bound the claim. Full sweeps, extra
  datasets, proofs, and implementation detail go to the appendix, each
  referenced from the exact sentence it backs — an unreferenced appendix
  section does not exist to a reviewer.
- **The checklist is part of the paper.** NeurIPS and ICML ship a paper
  checklist (reproducibility, compute disclosure, limitations, societal
  impact). Answer it from the record — the ledger has the compute and seeds,
  the sweeps have the scope — and answer it honestly; a checklist answer the
  paper contradicts is a flag reviewers act on.
- **Limitations are a required section, not a courtesy.** The scope boundaries
  from the sensitivity analyses belong there, with numbers.
- **Reproducibility is claimed with specifics**: seeds, spread, compute per
  run, and code availability. The ledger's per-run commit field is what makes
  the code claim true.
- **Reviewers skim, then judge.** Abstract, contributions, Figure 1, and the
  main table decide the initial score; those four get rewritten last, from the
  spine, every round.

## Section targets

The invocation may name one: `/auto-research paper-writing intro`. With no
target, draft or refresh whatever the spine shows is stale, and say which.

- **abstract** — the spine compressed, with the headline number and the scope.
- **intro** — problem, why existing work does not solve it, the claim, the
  contributions as noun phrases. Written last or rewritten last; it is the
  section that goes stale first.
- **method** — the method as it finally is. No variants that were discarded,
  no options nobody used. Define what the experiments actually ran.
- **experiments** — setup, then one subsection per question the runs answer.
  Order by the argument, not by when the runs happened. Ablations and
  sensitivity analyses are sections of the argument, not an appendix dump.
- **related** — organised by how each line of work relates to the claim, not
  chronologically or by venue.
- **limitations** — the scope boundaries the sweeps found, stated plainly.
  This is where honest negatives live, and it strengthens the paper.

## The staleness sweep

Run this after any `revise`, and as its own target
(`/auto-research paper-writing sweep`). A revised claim leaves fossils
throughout a draft, and the abstract is rarely the only survivor.

Grep the draft for each of these against the current spine:

1. The claim sentence in the abstract, intro, and conclusion — three copies
   that drift apart independently.
2. Every number, against the ledger. Old numbers survive reruns.
3. Method and component names that were renamed.
4. Hypotheses phrased as open questions that the runs have since answered.
5. Figure and table captions, which are edited least and go stale most.
6. Contribution list versus what the paper now demonstrates.
7. Scope and hedging language that predates the sensitivity results.
8. After a rebuttal: the Commitments table in `research/reviews/rebuttal-*.md`.
   Every promise is either kept in the draft or explicitly renegotiated with
   the user — a commitment silently dropped at camera-ready is the one
   staleness a reviewer will personally remember.

Report what was stale and what was changed. Fossils are the main way a paper
ends up claiming something the experiments no longer support.

## Prose and build

Delegate the writing craft rather than reinventing it: load the
`academic-writing` skill for venue structure, register, and reviewer
expectations, and `writing-with-style` for clarity at the sentence level. This
mode decides *what* the paper says; those decide how it reads.

These prose rules bind every draft this mode writes, even when those skills
are not loaded. Never write the `<claim>: <elaboration>` sentence shape,
where a colon introduces a clause expanding the claim before it. Reserve
colons for lists, definitions, and math. Rewrite as two sentences, or use
"e.g.," / "i.e.," / "that is" / "namely". Avoid em-dashes and semicolons in
prose too. Never use the words "inert", "headline" (adjective),
"load-bearing", "rungs", or "conflates", even when `STORY.md` or the
findings notes use them internally. Limit hard (at most one per paragraph):
"rather than", the contrast appositive "X, not Y", the connective ", so "
(prefer "therefore", "hence", "thus", "which means"), and negation-heavy
hedging that defines things by what they are not. Prefer stating what IS
true, and keep a negation only when the negative claim is itself the
finding or a scope statement honesty requires.

For a pure polish pass over sections whose content is settled — especially
when working through a `review-paper` or `rebuttal` fix list — hand the edits
to the **`prose-polisher`** agent (in `~/.claude/agents/`) with the polish
level and the findings to fix. It edits under the `academic-writing`
guardrails and reports what it flagged rather than fixed; review its flags,
since those are the content decisions this mode owns.

After editing any paper file, build it with the command in
`research/WORKSPACE.md` (typically `make main 2>&1 | tail -10` in the paper
directory) and read the tail of the log. Fix LaTeX errors before reporting
done, and never leave the draft unbuildable.

Report the sections touched, the spine changes that drove them, anything found
stale in the sweep, and the build result. When a full draft exists and the
sweep is clean, the next useful move is `review-paper`: an author cannot see
what a draft fails to say, and that mode is built to find it.
