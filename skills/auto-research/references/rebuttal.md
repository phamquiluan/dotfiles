# Mode: rebuttal

Real venue reviews came back. Triage them, run what must be run, and write the
point-by-point response — without promising the camera-ready anything the loop
cannot deliver.

This mode is never inferred: reviews arriving is a moment only the user knows.
The invocation names them: `/auto-research rebuttal <path-to-reviews>`, or the
reviews are pasted into the conversation.

## Contents

- [Ingest the reviews verbatim](#ingest-the-reviews-verbatim)
- [Triage every point](#triage-every-point)
- [Separate legitimate from inflated](#separate-legitimate-from-inflated)
- [Run what the window allows](#run-what-the-window-allows)
- [Write the response](#write-the-response)
- [Record the commitments](#record-the-commitments)
- [Stress-test the response](#stress-test-the-response)

## Ingest the reviews verbatim

Copy the reviews unedited into `research/reviews/rebuttal-<venue><year>.md`
(e.g. `rebuttal-neurips2026.md`), one section per reviewer, keeping their ids
(R1, R2, ...) and scores. Everything else this mode writes appends below the
verbatim text, so the response and its evidence live with what they answer.
A second round at the same venue suffixes: `rebuttal-neurips2026-b.md`.

Number every distinct point (`R1.1`, `R1.2`, `R2.1`, ...). A reviewer paragraph
often packs three objections; split them, because they may triage differently.

## Triage every point

Use `review-paper`'s four kinds, which shift meaning when the reviewer is real:

| Kind | Test | Action |
|---|---|---|
| Real gap | The run was never done | Ledger entry `--status planned`; run it if the window allows |
| Presentation | The run exists, the paper does not show it | Answer with the number now; commit the edit for camera-ready |
| Misread | The paper says it, unclearly enough to miss | The reader is right about the writing: quote the passage, restate it plainly, commit a clarification |
| Accepted | Valid, and out of scope or unaffordable | Concede in the response; goes to limitations |

Two rules carry over unchanged: "misread" only if the passage can be quoted and
genuinely answers the point — a defence that needs the ledger is a presentation
failure; "accepted" needs a reason a reviewer would accept, written down.

One rule is new: **a misread is never argued as the reviewer's fault.** The
response thanks, quotes, clarifies, and commits the edit. Winning the point
while irritating the reviewer loses the paper.

Points that recur across reviewers are one structural problem and get one
coordinated answer, cross-referenced from each reviewer's section — reviewers
read each other's reviews, and inconsistent answers to the same point are
noticed.

## Separate legitimate from inflated

Real review sets mix sound objections with inflated, unfalsifiable, or simply
wrong ones, and the two need different handling. For each point, ask: what
evidence would satisfy this reviewer? If a concrete run or edit would, the
point is legitimate — triage it above. If nothing affordable would — "evaluate
on all modalities", "compare against the entire field", a demand that amounts
to a new research program — say so internally, and respond by doing the
*bounded* version: one discriminating experiment, plus a sentence on why it
answers the spirit of the objection.

A factually wrong objection is corrected with a citation or a number, once,
politely, without dwelling. Never concede a wrong point to seem agreeable; the
meta-reviewer reads concessions as admissions.

## Run what the window allows

Rebuttal windows are short and the queue does not care. Order the queued runs
by leverage, not by reviewer:

- First, anything a score hinge names explicitly ("would raise my score if...").
- Then the cheapest run that removes the most-repeated objection.
- Last, nice-to-haves that only pad the response.

Submit through the normal machinery — ledger entry at submission, `katana` for
the cluster — and fan out; a rebuttal week is exactly when serial queuing kills.
Anything that cannot land in the window is not promised as a result, only as a
camera-ready commitment, and only if it is genuinely affordable.

**Never cite a number from a run that has not finished.** A rebuttal claim that
a rerun later contradicts is worse than the original weakness.

## Write the response

Point-by-point, under the verbatim reviews. For each numbered point:

1. Quote or faithfully compress the point.
2. Answer with evidence: the number, the EXP id behind it, the quoted passage,
   or the concession. New results are labelled as new ("we ran X during the
   rebuttal period: ...").
3. State the change committed for camera-ready, if any, in one sentence.

Tone: grateful, direct, unhedged. No "we believe the reviewer may have
missed" — just the quote and the clarification. Every reviewer point gets a
response, including the kind ones; an ignored point reads as an evaded one.
Respect the venue's length limit; when squeezed, cut the padding from strong
answers before cutting weak answers entirely — an unanswered point costs more
than a terse answer.

## Record the commitments

Every "we will add/clarify/fix X" in the response goes into a **Commitments**
table at the bottom of the rebuttal file:

```markdown
## Commitments
| Id | Point | Promise | Where | Status |
|---|---|---|---|---|
| C1 | R2.3 | Add CITRIS baseline, 3 seeds | Table 2 | planned (EXP-0041) |
| C2 | R1.1 | Clarify assumption A2 scope | Sec 3.1 | pending |
```

This table is what `paper-writing` reads at camera-ready time: a promise made
in a rebuttal and silently dropped is the failure mode this file exists to
prevent. Runs promised get `--status planned` ledger entries at the moment the
promise is made, so `status` counts them as work owed.

## Stress-test the response

Before it ships, run the draft response past an adversarial reader in a
sub-agent: give it the reviews and the response only — no `research/`, no
goodwill — and instruct it to find, for each point, how a hostile reviewer
would dismiss the answer, reinterpret a concession as an admission, or claim
the new experiment misses the point. Fix what that surfaces; ignore what would
require bad faith to sustain, and say so in one line each.

The response itself ships however the venue wants (OpenReview, PDF); this mode
ends with the rebuttal file complete and committed. Report: points by kind,
runs submitted and in flight, commitments made, score hinges and whether they
were addressed, and anything deliberately conceded.
