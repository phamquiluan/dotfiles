# Mode: implement

Write the code a study needs — the method, a baseline integration, the
experiment harness, tests — and leave it committed to the code repo, so every
ledger entry's `commit` field points at code that actually existed.

This mode changes code, not claims. What is being claimed lives in `IDEAS.md`
and is `revise`'s to change; what the paper says is `paper-writing`'s. Here the
question is only: does the code that the next study needs exist, run, and do
what the record says it does.

## Contents

- [When to run it](#when-to-run-it)
- [Ground rules](#ground-rules)
- [Target: method](#target-method)
- [Target: baseline](#target-baseline)
- [Target: experiment harness](#target-experiment-harness)
- [Target: tests](#target-tests)
- [Commit and record](#commit-and-record)

## When to run it

The invocation names a target: `/auto-research implement method I3`,
`implement baseline CITRIS`, `implement experiment I3-sensitivity`,
`implement tests metrics`. Other modes hand off here:

- `experiment` designs a study and finds the code for it does not exist —
  the method variant, an unintegrated baseline, the sweep harness.
- `analyze` classifies a failure as **implementation**: the method as coded is
  not the method as described. The fix happens here, then the rerun goes back
  through `experiment`.
- `review-paper` triage queues a run that needs a baseline or an ablation
  switch nobody has written.

`status` never suggests this mode; missing code is invisible to the file
heuristic. It is entered by name or by handoff.

## Ground rules

**Work in the code repo.** `research/` holds state *about* the code — never
the code itself. New source, baselines, tests, and configs all belong in the
project tree, at the paths `WORKSPACE.md`'s code catalogue describes.

**Reuse before writing.** Read the code catalogue first. A catalogued
component with a checked signature beats a fresh implementation; if the study
rests on one that has never been verified, that is a `dive-deep code` handoff,
not a reason to rewrite it.

**Smallest diff that makes the study runnable.** This mode exists to unblock a
specific study, not to build a framework. Generality that no queued run needs
is scope creep here exactly as it is in a paper.

**Match the project's idiom.** New code should read like the code around it —
same config style, same logging, same layout — or the next pass through it
costs more than it should.

**Smoke-test before handing back.** Nothing leaves this mode untested: run it
on tiny data end to end. Import errors and shape bugs caught here cost
nothing; caught after submission they cost a queue slot and a round.

## Target: method

New source code implementing an idea's mechanism.

- **Implement the claim as written.** The spec is the idea's **Claim** and
  **Kill test** in `IDEAS.md`. Where the code forces a choice the idea does
  not specify — an architecture detail, an initialisation, a discretisation —
  make it, and record it in the idea's **Open questions**. Silent decisions
  resurface later as unexplained results.
- **Flag-gate every component the ablations will remove.** Design the ablation
  switches now: an ablation that requires editing source produces runs no one
  can compare, because the ledger `config` no longer determines the run. Each
  switch is a config key, defaulting to the full method.
- **Share the harness with the baselines.** Same dataloader, same splits, same
  preprocessing, same metric code. A method with a private input pipeline
  makes every comparison suspect.
- **Expose the seed** and thread it through everything stochastic —
  initialisation, dataloader order, augmentation.

## Target: baseline

Integrating a published method so its numbers can sit in the same table.

- **Wrap the authors' implementation; do not reimplement it.** A
  reimplementation's numbers are yours, not theirs, and reviewers know the
  difference. If the repo has never been read, `dive-deep code <repo>` comes
  first — its config defaults and undocumented tricks change what "the
  baseline" even is.
- **Write an adapter, not a fork.** The wrapper feeds the shared splits and
  preprocessing in, and emits predictions in the same format the method emits,
  so the same metric code scores both. Patch the vendored code as little as
  possible, and record every patch in the code catalogue entry.
- **Reproduce a published number before trusting the integration.** Run the
  baseline in a configuration its own paper reports and compare. Until that
  matches, a gap between the method and the baseline is a bug report on the
  wrapper, not a result.
- **Give it the same tuning hooks as the method.** The comparison rule —
  equal tuning budgets — is decided in `experiment`, but it is only possible
  if the wrapper exposes the knobs.

## Target: experiment harness

The runner that turns a ledger `config` into artefacts `analyze` can read.

- **One entry point, fully config-driven.** Dataset, seed, method, baseline,
  every ablation flag and sweep knob — all arrive by flags or a config file.
  If a run requires editing source, the ledger no longer determines the run,
  and rung checks in `analyze` stop meaning anything.
- **Write what the downstream modes read.** Each run emits, under its output
  directory: metrics as JSON, **raw predictions**, training curves or logs,
  and the resolved config it actually ran with. Predictions are not optional —
  recomputing the headline number from them is how metric bugs get caught,
  and `dive-deep run` is built around them.
- **Log the environment.** Seed, git commit, dataset version, device. The
  ledger records these too; the run's own copy is what survives when the two
  disagree.
- **Make the sweep an array over configs**, not a shell loop over edits, so
  submission through the `katana` skill maps one array index to one ledger
  entry.
- **Support case-range chunking.** The harness takes a case subset — an index
  range or an explicit list — as a flag, so `experiment` can split a 500-case
  evaluation into an array of 50 subjobs of 10 cases each instead of one
  serial job. One chunk emits one result file and one log, named by chunk
  index; aggregation happens after fetch, never by concurrent append to a
  shared file.
- **Log so a failure is diagnosable from the file alone.** Every run and
  every chunk writes a log under its output directory: resolved config at the
  top, a progress line per case, timings, and the full traceback on error,
  with stdout/stderr captured rather than left to the scheduler's buffer.
  When chunk 12 dies on case 7, the log must say which case and why —
  otherwise the diagnosis costs a resubmission.

## Target: tests

Test what would silently corrupt results, not what would loudly crash.

- **Metrics against hand-computed cases.** Especially permutation-sensitive
  ones like MCC: a tiny input with a known answer, worked by hand. Wrong
  metrics survive precisely because nobody recomputes.
- **Dataloader shapes, dtypes, and alignment** at the point the model consumes
  them, and label alignment against a case where the answer is known.
- **Split integrity.** No entity or time overlap between train and test on
  grouped or temporal data. This is the leak that random-split code introduces
  by construction.
- **Flags reach their component.** For every ablation switch: two configs that
  differ only in that flag must produce different outputs. A flag that is not
  wired through turns a whole ablation into noise.
- **Regressions from the bug ladder.** When `analyze` finds a bug and it gets
  fixed here, the failing case becomes a test, so the same bug cannot cost a
  second round.

Run the suite as part of the smoke test, and note the command in
`WORKSPACE.md` so every later pass runs it too.

## Commit and record

- Run the tests and the tiny-data smoke test; fix what they catch.
- Commit to the **code repo** with a message naming the idea or study:
  `implement: I3 regime head + ablation flags`. The hash is what
  `experiment` will stamp into the ledger entries.
- If this pass fixed an implementation-classified failure, note it on the
  affected ledger entry so the old number cannot be quoted innocently:

  ```bash
  $L update EXP-0007 --notes "regime head was detached from the loss; fixed at <hash>, rerun needed"
  ```

- Update the code catalogue entry for any repo that was patched or wrapped.
- Commit the research repo as every mode does.

Report: what exists now and where, the code commit hash, what the tests cover,
and whether `experiment` can submit — or what still blocks it.
