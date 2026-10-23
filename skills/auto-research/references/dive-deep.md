# Mode: dive-deep

Go to the primary source and check it. Every other mode runs on secondhand
knowledge — an abstract, a card, a summary metric, a filename — and this mode
exists because that knowledge is wrong often enough to sink a project quietly.

## Contents

- [When to run it](#when-to-run-it)
- [Method](#method)
- [Target: paper](#target-paper)
- [Target: source code](#target-source-code)
- [Target: dataset](#target-dataset)
- [Target: output](#target-output)
- [Write the note](#write-the-note)

## When to run it

The invocation names the target: `/auto-research dive-deep code CITRIS`,
`/auto-research dive-deep data ncmapss`. Other modes hand off here at the points
where being wrong is expensive: before a novelty verdict rests on a paper's
abstract, before a repo becomes a baseline, before a dataset carries a headline
number, and whenever the bug ladder in `analyze` cannot clear a rung.

A dive that finds nothing wrong is still worth its cost — it converts an
assumption into a checked fact, and the note stops it being re-checked.

## Method

Four rules hold across all targets.

**Read the thing, not the description of the thing.** The card, the abstract,
the docstring, and the plot are summaries written by someone with a reason to
simplify. Open the source.

**Check claims against artifacts, one at a time.** Take each claim the summary
makes, find the specific line, cell, or number that supports it, and record
whether it holds. A claim nobody can locate evidence for is a finding.

**Chase the discrepancy.** When the artifact disagrees with its description,
that gap is the whole point of the dive. Do not smooth it over; run it to
ground and write down which one is right.

**Bound the dive.** Thorough is not unbounded. State up front which questions
the dive must answer, work those, and record what was left unexamined. An
unbounded read of a large repo burns hours and returns atmosphere.

## Target: paper

Beyond the abstract and results table:

- **The claim as stated versus as cited.** What the paper proves is usually
  narrower than what the field repeats about it. Quote the actual theorem or
  headline sentence.
- **Assumptions, including the unstated.** List every condition the result
  needs. Check the theorem's preconditions against the experimental setup — it
  is common for the experiments to violate the theory's assumptions.
- **What the numbers were measured on.** Dataset version, split protocol,
  tuning budget, seed count, whether variance is reported. A single-seed table
  changes how much weight the paper can bear.
- **The appendix.** Preprocessing, hyperparameters, and negative results live
  there. So do the caveats the main text drops.
- **Baselines as run by these authors.** Were they tuned? Do their numbers
  match the baselines' own papers?
- **What the paper does not claim.** Write this explicitly; it is where the
  open problems are.

## Target: source code

The question is whether the code is the method the paper describes.

- **Entry point to loss.** Trace one full path: data loading, preprocessing,
  model forward, objective, update, metric. Read it, do not skim for names.
- **Defaults versus the paper.** Compare the config defaults against the values
  the paper reports. Divergences are common and material.
- **Undocumented tricks.** Gradient clipping, warmup, EMA, label smoothing,
  early stopping on the test set, clamping, magic epsilons. Anything that
  affects results and is absent from the paper goes in the note.
- **The evaluation path.** How is the metric computed, and on what? Look for
  test-set leakage, tuning on test, metrics computed over the wrong axis, and
  permutation handling in metrics like MCC.
- **What is actually reusable.** Exact paths and signatures for the components
  worth importing, and what they assume about their inputs. If the project keeps
  a code catalogue, correct that repo's entry when the dive shows it is wrong or
  thin: a dive that improves the catalogue pays for itself twice.
- **Does it run?** Smoke-test the authors' own example on tiny data before
  trusting anything above. A repo that does not run is a card correction, not a
  baseline.

## Target: dataset

Never trust a loader you have not watched produce a batch.

- **Shapes and dtypes** at the point the model consumes them, printed, not
  inferred from documentation.
- **Label semantics.** What does the ground truth actually mean, who produced
  it, and how? For fault or anomaly data: what counts as an event, how are
  onsets defined, is the label at the right timestamp.
- **Distributions.** Per-channel statistics, missingness, constant or dead
  channels, class balance, outliers. Plot a few series and look at them.
- **Splits.** How train, validation, and test are separated, and whether the
  separation survives the temporal or entity structure. Random splits over time
  series and grouped data leak by construction.
- **Preprocessing order.** Normalisation fitted on train only, applied
  identically to every method being compared.
- **Scale versus the claim.** Is there enough data to detect the effect size
  the idea predicts? Answer this before running, not after a null result.

## Target: output

The summary metric is one number out of a run that produced thousands.

- **Logs first.** Warnings, silent fallbacks (CPU when GPU was requested),
  NaNs, restarts, truncated epochs. Read the head and tail of stderr.
- **Curves, not endpoints.** Training and validation loss over time. Diverged,
  plateaued at initialisation, still improving at the cutoff, or overfitting —
  each implies a different next step.
- **Predictions, not just scores.** Look at actual outputs on specific examples.
  Where does it fail: a subset, a regime, a fault type, the boundaries? Aggregate
  metrics hide structure that predictions show immediately.
- **Recompute the headline number** from the raw predictions, independently of
  the training script. Metric bugs survive because nobody recomputes.
- **Resource telemetry.** Idle GPU, memory near the cap, walltime near the
  limit — each changes what the run means and what the next one should request.
- **Compare against a run that should differ.** If two configurations produce
  identical outputs, a flag is not wired through.

## Write the note

One file at `research/deep/<type>-<slug>.md`, where type is `paper`, `code`,
`data`, or `run`:

```markdown
# code-CITRIS - does the implementation match the paper?

**Scope.** Encoder and objective only; the visualisation code was not read.
**Verdict.** Matches, with two undocumented deviations.

**Checked.**
- Objective matches Eq. 4. (models/citris_vae.py:118)
- Intervention targets are read from the dataloader, not inferred, as claimed.

**Discrepancies.**
- Default beta is 0.01; the paper reports 1.0 in Table 6. Results below were
  produced with the config default, not the reported value.
- Gradient clipping at 5.0 is applied and is not mentioned in the paper.

**Reusable.** CITRISVAE.encode(x) -> (mu, logvar), expects float32 NCHW in
[0,1]; assumes fixed sequence length 2. (models/citris_vae.py:64)

**Left unexamined.** The normalising-flow variant, and the ablation scripts.

**Consequences.** Rerun the I3 baseline with beta=1.0 before comparing; the
current EXP-0004 number is not the paper's configuration.
```

The **Consequences** section is what makes the dive useful — state what changes
in the ledger, the ideas, or the next run. If a ledger entry is now known to be
wrong, append a note to it:

```bash
$L update EXP-0004 --notes "beta was 0.01, not the paper's 1.0; see deep/code-CITRIS.md"
```

Report the verdict, the discrepancies that matter, what was left unexamined,
and the mode that should act on the consequences.
