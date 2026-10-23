---
name: auto-research
description: Run one phase of a research loop per invocation - ideate, implement, experiment, analyze, revise, dive-deep, paper-writing, review-paper, rebuttal - with state in a research/ directory (its own local git repo) so the phases compound across sessions. Use when the user types /auto-research with or without a mode, or asks to generate or novelty-check research ideas, implement a method or integrate a new baseline, write tests or an experiment harness for research code, design or launch an ablation or sensitivity study, diagnose why an experiment underperformed, decide what to run next, read a paper or repository properly, verify a dataset or a baseline implementation, audit a run's logs and predictions, draft or update a paper from experimental results, strip stale claims out of a draft, red-team a draft before submission, or triage venue reviews and write a point-by-point rebuttal or response letter.
---

# Auto Research

Run one phase of a research loop per invocation, reading and writing shared
state so the phases compound instead of restarting.

`scripts/` and `assets/` below are relative to this skill's own directory,
which is given when the skill loads. The project being researched is a
different directory, passed to the script as `--project`. Write
`python3 <skill-dir>/scripts/ledger.py --project <project-root> ...`.

## Modes

| Mode | Does | Guide |
|---|---|---|
| `ideate` | Mine papers, artifact cards, and code for candidate ideas; novelty-check; write them to `IDEAS.md` | [references/ideate.md](references/ideate.md) |
| `implement` | Write the code a study needs — method, baseline integration, experiment harness, tests — and commit it to the code repo | [references/implement.md](references/implement.md) |
| `experiment` | Turn an idea into a run plan (main, ablation, sensitivity), submit it, record it | [references/experiment.md](references/experiment.md) |
| `analyze` | Diagnose finished runs, separate bugs from real negatives, emit hypotheses | [references/analyze.md](references/analyze.md) |
| `revise` | Rewrite idea and experimental design from the evidence; kill or promote | [references/revise.md](references/revise.md) |
| `dive-deep` | Inspect a paper, repo, dataset, or run output first-hand; check claims against the artifact | [references/dive-deep.md](references/dive-deep.md) |
| `paper-writing` | Draft or refresh the paper to state the current idea and surviving results; sweep out stale claims | [references/paper-writing.md](references/paper-writing.md) |
| `review-paper` | Review the draft blind, as the venue would, then triage each weakness into a run or an edit | [references/review-paper.md](references/review-paper.md) |
| `rebuttal` | Triage real venue reviews, run what the window allows, write the point-by-point response, record camera-ready commitments | [references/rebuttal.md](references/rebuttal.md) |

Read only the guide for the mode being run.

## Routing

The mode is the first argument: `/auto-research experiment sensitivity`.
Anything after the mode is a free-text focus — an idea id, a metric, a
constraint — and should shape the work.

With no argument, run:

```bash
python3 <skill-dir>/scripts/ledger.py --project <project-root> status
```

`suggested_mode` and `why` come back in the JSON. Say which mode is being
entered and why in one line, then run it. Override the suggestion when the
conversation clearly points elsewhere; the heuristic only sees the files.

**Reconcile before anything else.** If `in_flight` is non-empty, the ledger is
describing the cluster as it was at submission. Check each job's real state
first, and for every one that has finished, pull its artefacts into
`research/runs/EXP-<id>/` and stamp the ledger:

```bash
$L update EXP-0007 --status done --metrics '{"mcc":0.81}'   # or --status failed
```

Then re-run `status`, because harvesting is usually what turns "still in
flight" into "runs to analyse". This step belongs to whichever mode is about to
run, not to a mode of its own; skipping it is how the loop stalls.

`implement`, `dive-deep`, `paper-writing`, `review-paper`, and `rebuttal` are
never inferred. Each takes a target the file state cannot guess, or a moment
only the user knows: `implement baseline CITRIS`, `dive-deep code CITRIS`,
`paper-writing intro`, `paper-writing sweep`, `review-paper external <path>`,
`rebuttal <path-to-reviews>`. Missing code in particular is invisible to the
heuristic, so `implement` is entered by name or by handoff.

Handoffs between modes: the loop modes call `dive-deep` when a step depends on
something nobody has checked; `experiment` hands to `implement` when the study
it designed needs code that does not exist, and `analyze` failures classified
as implementation come back through `implement` before the rerun; `revise`
calls `paper-writing` when it promotes an idea or moves a claim the draft
already states; `review-paper` feeds weaknesses back to `experiment` as queued
runs and to `paper-writing` as edits; `rebuttal` does the same for real venue
reviews, and its commitments table is what `paper-writing` must honour at
camera-ready time.

Run exactly one mode. At the end, state the next mode and what it would do, but
do not enter it. Two exceptions, both narrow:

- A run that fails on submission: fix and resubmit inside `experiment` rather
  than handing back a broken launch. The same license covers a study blocked
  only by a trivial missing piece of code — a flag, a wrapper line. Anything
  larger — a method, a baseline integration, a harness — is `implement`'s job
  and a handoff.
- A dive that unblocks the mode in progress: `analyze` may run `dive-deep`
  inline when a bug-ladder rung cannot be cleared, because the diagnosis cannot
  finish without it. Everywhere else a dive is a handoff — `revise` in
  particular defers, since a fate decision can wait a round.

## State

Everything lives under `<project-root>/research/`, created by
`python3 <skill-dir>/scripts/ledger.py --project <root> init`. Read
`WORKSPACE.md` before running any mode: it records the project's build command,
compute, data locations, and code catalogue, and what it says overrides the
generic guidance in this skill. `init` writes it as a template with empty
slots; fill them in on first use, and `status` warns while it is missing.

```
research/
├── WORKSPACE.md    project specifics; read first, overrides generic guidance
├── IDEAS.md        one "## I<n> <title>" section per idea, with **Status:**
├── STORY.md        the paper's argument in one place; what the draft must match
├── LEDGER.jsonl    one JSON record per run; only the script edits it
├── findings/       EXP-<id>.md, one failure-analysis note per analysed run
├── deep/           dive-deep notes: paper-, code-, data-, run-<slug>.md
├── reviews/        self-reviews plus triage; rebuttal files with commitments
└── runs/EXP-<id>/  raw artefacts pulled back, one directory per run
```

A run can have a note in both `findings/` and `deep/`, and they are not
duplicates: `findings/EXP-7.md` is what the run means, written by `analyze`;
`deep/run-EXP-7.md` is what its raw output contains, written by `dive-deep`.
Interpretation and inspection, in that order.

The project spans **three git repositories**, kept separate on purpose:

- **code** — the project root. `implement` commits here, and every ledger
  entry's `commit` field points into this history.
- **paper** — the paper directory, with whatever remote the venue workflow
  uses.
- **research** — `research/` itself, its own **local-only** repo that `init`
  creates with `git init`. No remote: it is the progress track. Every mode
  ends by committing the state it changed, message named after the mode —
  `git -C research add -A && git commit -m "analyze: EXP-0007 effect absent"`.
  `init` writes a `.gitignore` keeping `runs/` and the lock file out, so
  large artefacts never enter the history.

Add `research/` to the code repo's `.gitignore` so the histories do not
tangle. Because the research repo is local, it does not travel when the
`katana` skill syncs the code repo to the cluster — that is fine: runs happen
on the cluster, state stays here, and artefacts are pulled back into
`research/runs/`.

Never hand-edit `LEDGER.jsonl`. Records are rewritten in place by `update`, so
the file is script-managed rather than an immutable log:

```bash
L="python3 <skill-dir>/scripts/ledger.py --project <root>"
$L add --idea I2 --kind ablation --hypothesis "regime head carries the gain" \
      --config '{"dataset":"ncmapss","seed":0,"lr":1e-3}' \
      --status running --job 4812345
$L update EXP-0007 --status done --metrics '{"mcc":0.81,"f1":0.62}'
$L update EXP-0007 --analysed --notes "dataloader was the bottleneck"
$L update EXP-0007 --decided        # revise acted on that finding
$L update EXP-0004 --kind sensitivity --config '{...}'   # fix a bad add
$L list --idea I2 --kind ablation
$L status
```

`kind` is one of `main`, `ablation`, `sensitivity`, `baseline`, `probe`. Every
kind but `probe` must pin `dataset` and `seed` in `--config`, because those are
the runs that get compared. Each record also captures the project's git commit,
so a number traces back to the code that produced it; pass `--data-version`
when the dataset version matters.

`--status` distinguishes work that exists only on paper from work the scheduler
has: `planned` (designed, not submitted, no job id), `queued` and `running`
(submitted, has a job id), then `done` or `failed`. Only `queued` and `running`
count as in flight and trigger reconciliation.

Two flags carry the loop's memory, and they are durable rather than inferred
from file times, so they survive a clone: `--analysed` means `analyze` wrote a
finding for the run, `--decided` means `revise` acted on that finding. An
undecided finding is what makes `status` keep suggesting `revise`.

Idea `**Status:**` is edited directly in `IDEAS.md`, and every mode owns
specific transitions:

| Status | Set by | When |
|---|---|---|
| `proposed` | `ideate` | the idea survives triage and a novelty check |
| `active` | `experiment` | its first run is submitted |
| `revised` | `revise` | promote or narrow, after evidence lands |
| `parked` | `revise` | deprioritised but not refuted; reason recorded |
| `dropped` | `revise` | killed, with the reason in full |

`proposed`, `active`, and `revised` all count as live; `parked` and `dropped`
do not, and an idea set to either stops driving the routing heuristic.

If the project root is ambiguous, use the working directory and say so.

## Rules that hold in every mode

**Prose punctuation.** Every mode that writes text for a human reader is bound
by this, not only `paper-writing`. That includes `review-paper`, `rebuttal`,
`analyze`, and any summary written into `STORY.md` or a findings note. Never
write the `<claim>: <elaboration>` sentence shape, where a colon introduces a
clause expanding the claim before it. Reserve colons for lists, definitions,
and math. Rewrite as two sentences, or use "e.g.," / "i.e.," / "that is" /
"namely". Avoid em-dashes and semicolons in prose. When removing an em-dash,
do not reach for a colon, which recreates the banned shape. `paper-writing`
carries the full prose contract, including banned diction; see
`references/paper-writing.md`.

**One claim per run.** A run that varies two things answers neither question.
If a configuration change is unavoidable, log it in `notes` and treat the
comparison as suggestive.

**Seeds before conclusions.** No claim of an improvement from a single seed.
Three seeds minimum for a headline number, and report spread, not just the
mean. A gap inside seed noise is not a result.

**Record before interpreting.** Write the ledger entry when a run is submitted,
not after the numbers look good. Runs that are abandoned or crash stay in the
ledger with `--status failed`; a ledger that only holds successes cannot
support a failure analysis.

**Fan out; never queue serially.** Wall-clock is the loop's real bottleneck,
so independent work is split into parallel jobs. A study over many independent
cases — one method on a benchmark of 500 cases, a grid of datasets and seeds —
is submitted as a chunked array job (e.g. 50 subjobs of 10 cases each), never
as one job that crawls through all 500. The `katana` skill holds the array
mechanics; `implement` builds the harness so it can be chunked.

**Every job leaves a log.** The harness `implement` builds writes a per-run
(and per-chunk) log — resolved config, per-case progress, full tracebacks —
and `experiment` pulls logs back with the other artefacts, for failed runs
above all. A failure with no log costs a resubmission just to see the error.

**Baselines are load-bearing.** An idea beats a tuned baseline or it does not
beat anything, and a baseline given less tuning than the method proves nothing.
Reuse the authors' own implementation rather than reimplementing it.

**Say what the evidence does not cover.** Every summary ends with the claim the
runs actually license, and the ones they do not.

**No calendar estimates.** Never cost work in human time — "a week for the
baseline" is meaningless when the loop executes as fast as it runs. The only
durations worth writing down are compute: GPU-hours, walltime, queue time.
Plan in runs and dependencies, not in days or weeks.

**Commit the state every pass.** The research repo is the progress track: end
every mode by committing `research/` with a message naming the mode and what
changed. An uncommitted pass is invisible to the history later rounds rely on.

**The record keeps the trajectory; the paper does not.** Dropped ideas, fixed
bugs, and abandoned runs live in the state files so they are never
re-litigated, which is also why they stay out of the draft — with the
in/out line drawn in [references/paper-writing.md](references/paper-writing.md).

## Project specifics

This skill is project-agnostic. Everything particular to a project — paper
directory and build command, where jobs run, dataset locations, the code
catalogue, literature tools — belongs in that project's
`research/WORKSPACE.md`, not here. Read it at the start of every mode and
prefer it wherever it contradicts a default.

## A first pass through the loop

```
/auto-research ideate              -> research/ created (with its own git),
                                      WORKSPACE.md filled in, I1-I3 written
/auto-research implement method I1 -> method, harness, and tests committed
                                      to the code repo
/auto-research experiment I1       -> kill test submitted, EXP-0001..3 queued
/auto-research analyze             -> findings/EXP-0001.md, classification, hypotheses
/auto-research revise              -> I1 narrowed, next study specified
/auto-research experiment          -> the study revise specified
/auto-research paper-writing       -> STORY.md, then sections
/auto-research review-paper        -> blind review, weaknesses triaged into runs
```

`/auto-research` with no mode reads the state and picks the next of these.
