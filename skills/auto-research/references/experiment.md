# Mode: experiment

Turn one idea into runs that can only come back interpretable, launch them, and
leave the ledger accurate.

## Contents

- [Pick the study](#pick-the-study)
- [Design the main comparison](#design-the-main-comparison)
- [Ablations](#ablations)
- [Sensitivity analyses](#sensitivity-analyses)
- [Calibrate, then fan out](#calibrate-then-fan-out)
- [Record and report](#record-and-report)

## Pick the study

The invocation may name one: `/auto-research experiment ablation I3`. If not,
derive it from state — an idea with no runs needs its kill test; an idea whose
main result landed needs ablations; a result that holds needs sensitivity.

Read the idea's **Kill test** field. If it is vague, sharpen it into a concrete
comparison before writing any code, and update `IDEAS.md` with the sharpened
version.

Never launch a study whose outcomes are all compatible with the claim. Write
down, before submitting, what each possible result would mean. If one of the
outcomes has no interpretation, the design is wrong.

Check early that the code the study needs exists: the method with its ablation
flags wired, the baseline integrated, the harness able to run the sweep from
config alone. Anything missing beyond a trivial fix is a handoff to
`implement`; record the study's runs as `--status planned` so the work owed is
in the ledger, and resume here once the commit lands.

## Design the main comparison

Fix these explicitly and put them in the ledger `config`:

- **Datasets** — real and synthetic. A synthetic DGP with known ground truth is
  what makes a negative result diagnosable, and published repos often ship one,
  so grep the code catalogue for a generator before writing another. A dataset carrying a
  headline number for the first time needs `dive-deep data <name>` first — label
  semantics and split leakage are cheaper to find now than after the result.
- **Baselines** — at least one tuned published method, not just a naive control.
  Use the authors' implementation from `artifacts/` where it exists, and give it
  the same tuning budget as the proposed method. An untuned baseline invalidates
  the comparison. Run `dive-deep code <repo>` on a repo the first time it is used
  as a baseline: config defaults that differ from the paper, and undocumented
  training tricks, are common enough that an unchecked baseline number is not
  worth reporting.
- **Metrics** — one primary, decided now, plus secondaries. Choosing the primary
  after seeing results is the most common way a research loop fools itself.
- **Seeds** — three minimum, five preferred. Report mean and spread.
- **Compute budget** — matched across methods, and stated.

## Ablations

An ablation removes one component of the proposed method and changes nothing
else. Its purpose is attribution: which part carries the gain.

Build the list from the method's own components, one run each:

- Remove the component entirely.
- Replace it with the obvious simpler alternative.
- Keep it but sever what it is supposed to exploit (shuffle the regime labels,
  randomise the graph, break the temporal order).

That last form is the strongest and the most often skipped. If shuffling the
signal the method claims to use does not hurt it, the method is not using it,
and the headline result has another explanation.

Expected outcomes go in the hypothesis field of each ledger entry. An ablation
that does not hurt is a finding, not a failure — it usually means the component
can be cut.

## Sensitivity analyses

A sensitivity analysis varies a knob across a range and asks how the result
moves. Its purpose is scope: where the claim holds.

Cover three families:

- **Data regime** — sample size, noise level, class or fault balance, sequence
  length. Sweep until the method breaks; the breaking point is the result.
- **Assumption strength** — the assumption the idea relaxes, varied from fully
  satisfied to badly violated. This is the sensitivity that matters most for a
  relaxation idea.
- **Hyperparameters** — the two or three the method is most likely accused of
  being tuned to. Show the result survives an order of magnitude either side.

Sweep one dimension at a time from a fixed reference configuration. Grids over
three dimensions produce runs nobody reads. Prefer wide-and-shallow: seven
values on one axis beats a 3x3 with two seeds.

## Calibrate, then fan out

Use the `katana` skill for anything beyond a laptop-sized run; it holds the
cluster conventions, PBS templates, and sizing guidance. Load it before
submitting rather than writing PBS by hand.

The sequence that avoids wasting a queue slot:

1. Smoke-test one configuration locally on tiny data. Most failures are import
   errors, path mistakes, and shape bugs, and they cost nothing to catch here.
2. Submit a single full configuration and read its measured resource use.
3. Size the sweep from that measurement, then submit the rest as one array job.

**Chunk within a run, not just across configs.** A single evaluation over many
independent cases is itself a sweep: a method on a 500-case benchmark goes up
as an array of 50 subjobs of 10 cases each, mapped through the harness's
case-range flag, not as one job that walks all 500 serially. Size chunks so
each subjob runs minutes-to-hours — large enough not to spam the scheduler,
small enough that the study finishes in roughly one subjob's walltime. Each
subjob writes its own result file and its own log
(`results/chunk_${PBS_ARRAY_INDEX}.json`, `logs/chunk_${PBS_ARRAY_INDEX}.log`);
never append to a shared file, which concurrent subjobs would interleave.
Per-chunk files mean a partially failed array still yields usable data, and
only the failed indices get resubmitted.

**Wall-clock budget: the whole study lands inside ~5 hours**, queue time
included, unless the user grants more. Size the array from the measured
per-case cost: shards = ceil(total case-cost / 30 min per subjob), with a
floor of 8 shards — extra shards are free for deterministic CPU work, and
short-walltime subjobs schedule faster. For per-case-trained methods near
an hour per case, split down to one or two cases per subjob rather than
multi-case shards on a long walltime: a walltime kill on a 10-hour shard
costs a full resubmission cycle, and three such cycles is how a study
turns into a day. Request walltime at roughly twice the worst shard's
estimate, never a round maximum. Known slow or timeout-prone cases get
their own shards so the tail never holds the study.

A sweep large enough to matter — hundreds of jobs, or many GPU-hours — is worth
confirming with the user before submitting, even though this mode is otherwise
autonomous.

## Record and report

Add a ledger entry per run **at submission**, with the hypothesis and the job
id, as `--status running`. Batch entries for an array job individually if their
configs differ; that is what makes them comparable later. When this is an
idea's first run, set its `**Status:**` in `IDEAS.md` from `proposed` to
`active`.

Runs designed but not yet submitted — a study `revise` specified, or a run
queued by `review-paper` triage — are `--status planned` with no job id. Move
them to `running` when they actually reach the scheduler. Keeping the two apart
is what lets `status` tell "waiting on the cluster" from "waiting on us".

```bash
$L add --idea I3 --kind sensitivity --hypothesis "MCC degrades gracefully below n=500" \
      --config '{"n":500,"seed":1,"noise":0.1}' --status running --job 4812345[3]
```

Update with metrics as results land; `--status done` stamps the finish time.
Leave failed runs in the ledger as `failed` with a note on how they failed.

Fetch artefacts into `research/runs/EXP-<id>/`, one directory per run. Logs,
checkpoints, and predictions are what `analyze` and `dive-deep run` read, and
a flat dump of everything into `runs/` becomes unusable within a few rounds.
Fetch logs for failed runs especially — the log is what `analyze` diagnoses
from, and a failure whose log was never pulled back gets rerun blind.

Report: what was submitted, what it tests, what each outcome would mean, and
where the results will appear. If runs are still in flight, say so plainly —
this mode ends at submission, and `analyze` picks them up once they finish.
