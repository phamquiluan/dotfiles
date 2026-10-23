# Mode: analyze

Work out what finished runs actually showed, distinguish broken from
informative, and leave behind hypotheses the next round can test.

## Contents

- [Scope the pass](#scope-the-pass)
- [Rule out the boring explanations first](#rule-out-the-boring-explanations-first)
- [Classify the failure](#classify-the-failure)
- [Read the ablations and sweeps together](#read-the-ablations-and-sweeps-together)
- [Generate hypotheses](#generate-hypotheses)
- [Write the finding note](#write-the-finding-note)

## Reconcile, then scope the pass

Start by making the ledger true. Any record still `queued` or `running` is a
claim about the cluster made at submission time; check each job's real state,
pull the artefacts of anything finished into `research/runs/EXP-<id>/`, and
stamp it:

```bash
$L update EXP-0007 --status done --metrics '{"mcc":0.81}'
$L update EXP-0009 --status failed --notes "walltime kill at epoch 40"
```

Nothing else in the loop does this, and until it happens `status` reports runs
as in flight forever.

Then `ledger.py status` returns `unanalysed`. Analyse those, plus anything the
invocation names.

Analyse negative and positive results with the same care. A result that matched
the hypothesis exactly, on the first try, deserves a bug hunt before it
deserves a celebration.

## Rule out the boring explanations first

Most surprising results are mistakes. Walk this ladder before theorising, and
record which rungs were checked:

1. **Did it run?** Exit code, walltime, whether it was killed. A job that hit
   the walltime produced a partial result, not a negative one.
2. **Did it train?** Loss curve, gradient norms, whether the metric moved off
   its initial value at all.
3. **Is the data what it should be?** Shapes, label alignment, normalisation
   applied consistently to method and baseline, no train/test leakage, no
   all-zero channel.
4. **Is the metric computed right?** Against a case with a known answer.
   Permutation-sensitive metrics such as MCC are a frequent source of silently
   wrong numbers.
5. **Is the baseline handicapped?** Same data, same preprocessing, same tuning
   budget, and its published number reproduced where one exists. A large win
   over a baseline that underperforms its own paper is a bug report.
6. **Is the gap inside noise?** Test it; do not eyeball it. See below.

Only past rung six is the result about the idea.

### Rung 6 properly: test the gap

Eyeballing mean ± spread is where loops fool themselves, in both directions.
Before calling a gap real or absent:

- **Pair the comparison.** Method and baseline share seeds, splits, and data
  by design, so compare per-seed differences, not two independent means. A
  paired test (or just the sign and size of every per-seed difference, listed)
  is far more sensitive than overlapping error bars, which can overlap while
  every paired difference favours one side.
- **Report effect size with the verdict.** "Significant" at a delta of 0.002
  MCC is not a result, and a 0.05 delta at n=3 seeds with wide spread is not a
  null. State the delta, its units, and whether it is big enough to claim.
- **Correct for how many cells were looked at.** A sweep or grid is a
  multiple-comparisons machine: one cell in twenty looks significant by
  chance. A surprising win found while scanning a sweep is a *hypothesis*, not
  a finding — confirm it with fresh seeds at that configuration before it
  enters a finding note as real. Say in the note how many comparisons the
  pass scanned.
- **Respect n=3.** Three seeds cannot certify a distribution; do not dress
  them in a t-test's assumptions. List all the points, and when the call is
  close, the fix is more seeds at the deciding configuration, not a fancier
  test on the seeds already run.

Write the rung-6 verdict in this shape: per-seed deltas, their direction
count, the mean delta against the pooled spread, and the number of
comparisons scanned. That line is what makes the finding auditable later.

Rungs 3, 4, and 5 are exactly what `dive-deep` is for. When one cannot be
cleared by reading the ledger and the logs, stop and dive:
`dive-deep run EXP-0007` for the output, `dive-deep data <name>` for rung 3,
`dive-deep code <repo>` for rung 5. Resume the ladder with the note in hand
rather than guessing past the rung.

## Classify the failure

Name which of these the evidence supports. The classification determines what
`revise` does next, so commit to one rather than hedging across three.

- **Implementation** — the method as coded is not the method as described.
  Hand the fix to `implement` (which also turns the failure into a regression
  test), then rerun; nothing about the idea has been learned.
- **Optimisation** — the method could work but did not converge here. Fixable
  with schedule, initialisation, or capacity changes; still nothing learned
  about the idea.
- **Assumption violated** — the setting does not satisfy what the method needs.
  Either the assumption is unrealistic (an idea problem) or the benchmark is
  unrepresentative (a setup problem). Say which.
- **Effect absent** — the mechanism does not do what the idea claimed. This is
  a real negative result and the most valuable kind.
- **Effect present, insufficient** — it works, but not enough to matter. Ask
  what would have to change by how much, and whether that is reachable.
- **Confounded** — the run cannot distinguish explanations because too much
  varied. Redesign, do not interpret.

## Read the ablations and sweeps together

Individual runs mislead; the pattern across them is the evidence.

- **Ablation with no effect** — the component is not carrying the result.
  Something else is, and the paper's story is currently wrong.
- **Signal-severing ablation with no effect** — the method is not using the
  signal it claims to use. Treat this as fatal until explained.
- **Sensitivity that is flat everywhere** — the knob is not connected, or the
  range was too narrow to matter. Check the code path before concluding
  robustness.
- **Sensitivity with a cliff** — the location of the cliff is the scope of the
  claim. Report the claim with that boundary attached.
- **Result that holds only at the reference configuration** — the finding is
  tuning, not a method.

## Generate hypotheses

For each unexplained observation, write competing explanations, not one. A
single hypothesis is indistinguishable from a rationalisation.

Each hypothesis needs a discriminating test: a run whose outcome differs
depending on which explanation is true. If two hypotheses predict the same
result on every affordable run, they are the same hypothesis for now — say so
and move on.

Prefer probes: small, fast, diagnostic runs on synthetic data with known ground
truth, aimed at one mechanism. A two-minute probe that discriminates beats a
six-hour rerun that does not.

This mode may run probes itself, within one limit: local only. A probe that
fits on the laptop is part of the diagnosis, so run it, log it with
`--kind probe`, and use the answer in the same pass. Anything that needs the
cluster is a study, not a probe, and goes through `experiment` — that is where
sizing, calibration, and sweep design live.

## Write the finding note

One file per analysed run at `research/findings/EXP-<id>.md`, or one shared
note for a group of runs that must be read together, cross-referenced from each
id. Then mark the runs analysed:

```bash
$L update EXP-0007 --analysed --notes "effect absent; regime head unused"
```

The flag is what moves the run out of `unanalysed` and into the queue awaiting
a decision, so set it on every run the pass covered, including the ones whose
answer was "nothing here".

Note structure:

```markdown
# EXP-0007 - regime head ablation (I3)

**Result.** MCC 0.62 +/- 0.04 vs 0.61 +/- 0.05 for the ablated variant, n=3.
**Checks.** Rungs 1-6 clear; baseline reproduces its published 0.58.
**Classification.** Effect absent.

**What the runs license.** Removing the regime head does not change MCC on this
DGP at n=1000.
**What they do not.** Nothing about real data, other regime counts, or whether
the head helps a different metric.

**Hypotheses.**
H1 The head is dead - gradients never reach it. Test: gradient norm probe, 5 min.
H2 Regimes are redundant given the temporal context the encoder already has.
   Test: remove temporal context, keep the head; if MCC drops, H2 holds.
H3 The DGP's regimes are too weak to be informative. Test: raise regime
   separation in the generator and rerun the ablation.

**Recommended next.** H1 first - cheapest, and it invalidates H2 and H3 if true.
```

Report the classification per run, the hypotheses worth testing ranked by cost
to discriminate, and whether `revise` is warranted or the next step is simply
running the probes.
