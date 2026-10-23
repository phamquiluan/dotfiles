# Mode: revise

Update what is being claimed and how it is being tested, so the next round is
better aimed than the last. This mode changes documents, not code.

## Contents

- [Read the record, not the memory](#read-the-record-not-the-memory)
- [Decide the idea's fate](#decide-the-ideas-fate)
- [Rewrite the idea](#rewrite-the-idea)
- [Revise the experimental design](#revise-the-experimental-design)
- [Guard against the usual self-deceptions](#guard-against-the-usual-self-deceptions)
- [Leave the state clean](#leave-the-state-clean)

## Read the record, not the memory

Load `IDEAS.md`, every finding note for the idea, the ledger entries, and any
`research/deep/` notes they reference. The revision must follow from what is
written down. If a belief driving the revision is not in the record, either
find the evidence or mark the belief as an assumption in the revised idea.

A kill or a pivot is expensive to get wrong. If the decision turns on an
unverified assumption — that a baseline was fair, that the labels mean what
they appear to, that the metric was right — send it to `dive-deep` first and
decide next round.

## Decide the idea's fate

Pick one and say why in a sentence:

- **Promote** — the kill test was survived. The idea's next form is a sharper,
  larger claim: more datasets, real data, a stated scope boundary. A promotion
  also changes what the paper says: hand off to `paper-writing` so the spine and
  the draft catch up before the next round buries the change.
- **Narrow** — it works inside a boundary the sweeps found. The revised claim
  carries that boundary in its statement. This is a normal, publishable
  outcome, not a defeat.
- **Repair** — the classification was implementation or optimisation. The idea
  is untouched; hand the fix to `implement`, then rerun. No revision to
  `IDEAS.md` beyond a note.
- **Pivot** — the mechanism failed but the finding is interesting. The pivot
  must be stated as a new idea with its own id and its own kill test, linked to
  the one it came from. A pivot that reuses the old kill test is not a pivot.
- **Park** — sound but not the best use of the next block of compute, and not
  refuted. Set `**Status:** parked` with the reason and what would revive it.
  A parked idea stops driving the routing heuristic without being lost.
- **Kill** — the effect is absent, cheap tests will not rescue it, and no
  interesting pivot exists. Set `**Status:** dropped` and write the reason in
  full. This is what stops the idea being regenerated in a later round.

Two consecutive rounds without a status change means the loop is stuck. Say so
directly and recommend a pivot or a kill rather than a third round.

## Rewrite the idea

Edit the idea's section in place, keeping the id. The revised section states:

- The claim, narrowed or sharpened to exactly what the evidence supports.
- The scope boundary, with the numbers the sweeps produced.
- The new kill test, which must be different from the one already run.
- What the previous round ruled out, in one line, so it is not retried.

Bump `**Status:**` to `revised`, or to `parked` or `dropped` for those fates.
Edit `IDEAS.md` even when the fate is `repair`, if only to note what the round
ruled out: the routing heuristic treats findings written after the last
`IDEAS.md` edit as undecided, so an untouched file keeps suggesting `revise`.

Keep the history: do not delete the superseded claim, strike it through or move
it under a `Previously` heading. The trail is what makes the record
trustworthy later.

## Revise the experimental design

The design usually needs more repair than the idea. Work through:

**Metric.** Did the primary metric measure the thing being claimed? If a
secondary metric turned out to be the informative one, promote it and say
plainly that it was promoted after seeing results — a reader will otherwise
assume it was chosen first.

**Baselines.** Add any method a reviewer would name and the last round lacked.
Remove baselines that turned out not to be comparable, with the reason.

**Data.** If synthetic results did not transfer, the generator is probably
missing a property of the real setting; name it. If real results are noisy,
decide whether the fix is more seeds, more data, or a better-controlled split.

**Ablation set.** Add ablations for components the analysis showed were doing
unexpected work. Drop ablations whose answers are now settled.

**Sweep ranges.** Widen the axes that were flat, refine around the cliffs, and
drop the axes that turned out not to matter.

**Budget.** State the compute the next round needs, from measured use rather
than the last estimate.

## Guard against the usual self-deceptions

- Do not move the claim to fit the numbers while leaving the framing implying
  the original claim was tested.
- Do not add datasets until one is found where the method wins. Choose the next
  datasets before seeing results, and commit to reporting all of them.
- Do not drop a baseline because it is strong. Drop it only for a stated
  methodological reason.
- Do not let effort spent decide the outcome. The right question is whether the
  next round is the best available use of the next block of compute, not
  whether the last round is worth rescuing.
- Do not turn a negative result into a hedge. "Effect absent under these
  conditions" is a clean, reportable finding; write it as one.

## Leave the state clean

- `IDEAS.md` updated, statuses correct, dropped ideas carrying their reasons.
- A short revision note appended to the relevant finding, so the decision and
  its evidence sit together.
- Every run whose finding this round acted on marked decided, which is what
  stops `status` suggesting `revise` again:

  ```bash
  $L update EXP-0007 --decided
  ```
- The next study specified concretely enough that `experiment` can act on it
  without re-deriving anything: idea id, kind, datasets, baselines, metric,
  seeds, and the outcome that would refute.
- If a draft exists and the claim moved, say so and recommend
  `/auto-research paper-writing sweep`. A revised claim leaves stale sentences
  in an abstract, and they are cheapest to catch now.

Report the fate decision, the revised claim in one sentence, the main design
changes, and the exact next invocation to run.
