# Mode: review-paper

Review the draft the way the venue will, before the venue does, and turn each
weakness into something the loop can act on.

## Contents

- [Two targets](#two-targets)
- [Prepare the inputs](#prepare-the-inputs)
- [Run the review blind](#run-the-review-blind)
- [Audit the source in parallel](#audit-the-source-in-parallel)
- [Triage against the record](#triage-against-the-record)
- [Close the loop](#close-the-loop)

## Two targets

**External** — `/auto-research review-paper external <path>`. Someone else's
paper. Load the `paper-reviews` skill and follow it; this mode adds nothing.
Come back only if the review turns up work worth doing here.

**Self** (the default) — our own draft. Also driven by `paper-reviews`, which
owns the review machinery: evidence format, citation scheme, assumption
extraction, sub-agent partitioning, the quality checklist. Do not restate any
of it. What this mode adds is the input preparation before, and the triage
after, because a self-review that ends at a list of weaknesses has done half
the work.

## Prepare the inputs

`paper-reviews` wants a line-numbered paper, a related-works directory, and a
form. A LaTeX source is none of those.

**Paper.** Build first. Tables and figures are generated, so a review run
against a stale build reviews numbers the paper no longer claims: run the
table, figure, and PDF commands from `research/WORKSPACE.md` before flattening.

Then flatten, keeping a map so a cited line can be traced back to the file that
must actually be edited:

```bash
python3 <skill-dir>/scripts/flatten_tex.py <paper>/main.tex \
    -o <scratch>/paper.txt --map <scratch>/paper.map.tsv
```

Write these to a scratch directory **outside `research/`**. The reviewer must
not see the research state, and a flattened copy sitting inside the directory
it is banned from reading is one careless glob away from defeating the point.

Preamble includes are left unexpanded automatically; `\input` inside a wrapper
such as `\resizebox{...}{\input{table/x}}` is spliced in, so wrapped tables
reach the reviewer. Pass `--keep-comments` when reviewing an early draft, where
`% TODO` notes are part of what needs reading.

The map is what makes the review actionable. Given "Lines 217-219":

```bash
awk -F'\t' '$1>=217 && $1<=219 {print $2":"$3}' <scratch>/paper.map.tsv
```

Expanded files are bracketed by `% >>> name` and `% <<< name` markers, so the
reviewer can see which section a passage belongs to. Tables are expanded too;
the numbers under review should be the ones the build produces.

**Related works.** Prefer real paper text. Any `research/deep/paper-*.md` notes
are a strong supplement because they record what a paper actually assumes
rather than what its abstract says, but they are not a substitute for the
related work itself when novelty is being contested.

**Form.** Use the venue's form. Failing that,
`<skill-dir>/assets/self-review-form.md` is a generic stand-in.

## Run the review blind

The failure mode of self-review is a flattering review. An author knows what a
sentence was meant to convey and reads it as if it conveys that.

Defend against it structurally: run the review in sub-agents that are given
the flattened paper, the related works, and the form, and **are not given
`research/`**. No ledger, no findings, no story spine. They must judge the
paper on what the paper says. A weakness that only survives because the
reviewer lacked context is exactly the weakness a real reviewer will raise.

**Run a panel, not a reviewer.** One review is one sample from a noisy
process; venues assign three reviewers for a reason. Spawn the panel in
parallel, each panelist blind to the others, using the named agents where
they exist (they live in `~/.claude/agents/` and already know the principle
set and output format) — the standing four:

- **`technical-reviewer`** — soundness: notation, methodology, statistical
  rigor, baseline fairness, whether the results support the claims and the
  ablations support the attribution.
- **`logic-reviewer`** — argument and story: the nugget stated in one
  sentence, Goal-Problem-Solution rhythm, transitions, promises versus
  delivery, logical gaps.
- **`writing-reviewer`** — prose: clarity, conciseness, grammar, tone,
  AI-writing tells. Report-only, like the others.
- **`novelty-reviewer`** — novelty and positioning: extracts the claimed
  contributions and actually searches OpenAlex/arXiv per claim, with one
  snowball hop from the closest hits, before ruling on the delta. Give it
  the related-works directory as a starting set; unlike the other panelists
  its searching of the public literature is in scope even in a blind run.
  If it recommends a full `systematic-review` pass (a "first to" claim it
  cannot bound), surface that in the triage rather than absorbing it.

Give each panelist the flattened paper, the related works, and the form —
and state explicitly that this is a blind panel run: judge only the provided
files. Instruct every panelist to argue for rejection where the evidence
permits it, and to calibrate: a first draft that has never been reviewed is
almost never above the venue's acceptance bar, and a panel returning only
minor presentation notes has failed — rerun it with sharper instructions.

**Merge on overlap.** After the panel returns, build the concern list with a
count of how many panelists raised each point independently. A concern raised
by two or three lenses that were not looking for it is close to certain to
appear in the real reviews — triage it first and take it seriously even when
it feels wrong. A singleton is still triaged, but verify it against the paper
before spending a run on it: single-reviewer concerns are where hallucinated
weaknesses live.

**Optional adversarial pass** — before a deadline, add a deliberately
bad-faith reviewer: instructed to mix its legitimate concerns with inflated,
unfalsifiable, or wrong objections and maximum-confidence rhetoric. Its output
is not triaged as findings; it is practice. Sorting its list into "real",
"inflated", and "wrong" is exactly the skill the `rebuttal` mode needs, and a
draft whose weaknesses cannot be inflated convincingly is a robust draft.

## Audit the source in parallel

While the blind panel reads the flattened copy, run the mechanical auditors
on the **real source tree and compiled PDF** — they are not reviewers and are
not blind; their findings are deterministic and need no venue judgment:

- **`consistency-checker`** — terminology drift, promise-versus-delivery
  structure, cross-reference integrity, figure-text-caption alignment,
  float definition order.
- **`bibliography-auditor`** — entry completeness, brace-protection, arXiv
  entries with published versions, author/venue consistency, unresolved
  citations, uncited named models and datasets.
- **`latex-layout-auditor`** — subfigure alignment, isolated float pages,
  sizing, floats far from their first reference, overfull boxes in the log.
  Skip it when the draft has no stable build yet.

Launch all of them and the panel in one parallel batch; the audits are
usually done first. Keep the two streams separate in the report: panel
findings say whether the paper stands, audit findings say whether the
artifact is clean.

## Triage against the record

Now bring the research state back. For each weakness, decide which of four
kinds it is. This is the step that self-review can do and a real reviewer
cannot, because only here does the ledger exist.

| Kind | Test | Action |
|---|---|---|
| Real gap | The run was never done | New ledger entry; `experiment` next |
| Presentation | The run exists, the paper does not show it | `paper-writing` item, cite the EXP id |
| Misread | The paper says it, unclearly enough to miss | `paper-writing` item; the reader is right |
| Accepted | Valid, and out of scope or unaffordable | Limitations section, stated plainly |

Two rules keep the triage honest. A weakness is only "misread" if the passage
can be quoted and it genuinely answers the point; if the defence needs the
ledger, it is a presentation failure. And "accepted" needs a reason a reviewer
would accept, not fatigue — write the reason down, because it goes in the
paper.

Weaknesses that cluster are one structural problem, not five small ones. Say so
rather than filing five items.

Audit-stream findings need no four-kind judgment: nearly all are
"presentation" by construction and go to `paper-writing` as a fix list, with
two exceptions worth promoting — an unresolved citation or a
figure-text-caption contradiction is critical (it can sink a submission on
its own), and a consistency finding that exposes a *claim* mismatch (the
promise-versus-delivery kind) is triaged like a panel weakness.

## Close the loop

Write the review and its triage to `research/reviews/<tag>.md`, tagged by the
latest experiment it reflects, for example `reviews/EXP-0031.md`. If that file
exists, suffix rather than overwrite (`EXP-0031-b.md`): a second review at the
same experiment is usually a rerun after sharpening the instructions, and the
pair is worth comparing. Keep the review verbatim; append the triage table
under it. Old reviews stay: the useful signal next round is which weaknesses
came back.

Then make the actions real, so nothing survives as a note:

```bash
$L add --idea I3 --kind ablation --status planned \
      --config '{"dataset":"ncmapss","seed":0}' \
      --hypothesis "reviewer W2: gain may come from the encoder, not the regime head"
```

`planned`, not `queued`: nothing has been submitted, and `experiment` picks
these up as the work it owes.

Presentation items go into the next `paper-writing` invocation. Accepted
limitations go into the draft now, not later.

Report the review's overall recommendation, the weakness count by kind, the
experiments queued, and whether the draft is submittable. If real gaps remain,
say plainly that it is not, and name the runs that would change that.
