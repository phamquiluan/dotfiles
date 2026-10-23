---
name: figure-generator
description: Generate publication-grade figures for ML papers (NeurIPS, ICLR, ICML) - data figures from experiment artefacts with matplotlib, and method/pipeline diagrams with TikZ - plus the LaTeX side of figures - float placement, subfigure alignment, label wiring, self-sufficient captions. Use when the user or another skill asks to create, fix, or restyle a paper figure, plot experimental results, draw an architecture or pipeline diagram, fix figure placement or alignment in LaTeX, or make figures camera-ready. Produces vector output from committed scripts and sources so every figure is regenerable and traceable.
---

# Figure Generator

Turn run artefacts into figures a reviewer trusts. Every figure comes from a
script; no figure is ever adjusted by hand afterwards.

`assets/paper.mplstyle` below is relative to this skill's directory, given when
the skill loads.

## The contract

Whoever invokes this skill supplies three things; ask for whichever is missing:

1. **The artefacts** — result files, typically `research/runs/EXP-<id>/` from
   the auto-research loop, or any CSV/JSON of results.
2. **The message** — the one sentence the figure must make a skimming reviewer
   believe. A figure without a message is a data dump; refuse to plot until
   the sentence exists.
3. **Where scripts and figures live** — usually `figure/` scripts writing
   `figure/*.pdf` in the paper directory, or wherever the project convention
   (e.g. `research/WORKSPACE.md`) says.

## Non-negotiable rules

- **Script per figure, committed to the project.** The script reads artefacts
  and writes the PDF; rerunning it after new results must reproduce or update
  the figure with no manual step. Never plot inline in a session and paste the
  output.
- **Traceable.** The script header names the EXP ids or artefact paths it
  reads. A figure nobody can trace to a run cannot be defended in a rebuttal.
- **Vector PDF** via `plt.savefig("figure/<name>.pdf")`, included in LaTeX
  with `\includegraphics`. PNG only for genuinely raster content (image
  samples, attention maps), and then at ≥300 dpi.
- **Fixed physical size, never LaTeX scaling.** Set the true column width in
  `figsize` and use `\includegraphics` without `width=`, or text sizes differ
  across figures. Single column: 3.25 in wide. Full width: 6.75 in. Height to
  content, typically 2–2.5 in.
- **Uncertainty is visible or the figure is unfinished.** Seed spread as error
  bars or a shaded band, with n stated in the caption. A mean without spread
  is the plotting equivalent of a single-seed claim.
- **No titles on axes objects** — the caption is the title. Label axes with
  units; legend inside the axes where there is room, above it where not.
- **Style comes from the shared stylesheet**, not per-script settings:

  ```python
  import matplotlib.pyplot as plt
  plt.style.use("<skill-dir>/assets/paper.mplstyle")
  ```

  Copy `paper.mplstyle` into the project the first time (next to the figure
  scripts) so figures build without this skill installed, and use that copy.
  It sets the colorblind-safe palette, 8 pt serif type, hidden top/right
  spines, and TrueType font embedding (`fonttype 42`) — Type 3 fonts fail
  camera-ready checks.

## Choosing the plot

Match the result type; do not invent chart forms:

| Result | Plot |
|---|---|
| Main comparison, few methods × few datasets | Table, not a figure. Plot only if there is a trend to show |
| Sensitivity sweep (one knob) | Line, x = knob (log scale if swept in decades), shaded seed band; mark the cliff |
| Ablation set | Horizontal bars of deltas vs full method, zero line drawn, sorted by effect |
| Scaling / sample-efficiency | Lines per method over n, log x, band per seed spread |
| Distributions per method | Box or strip plot with the raw points overlaid when n is small |
| Training dynamics | Only if the *dynamics* are the claim; otherwise omit |
| Teaser (Figure 1) | Schematic of the mechanism plus one inset result; hand-drawn layout is allowed here, numbers still script-sourced |

Plot raw per-seed points whenever n ≤ 5; a band implying a distribution from
three seeds overstates the evidence.

## Diagrams (TikZ)

Method, architecture, and pipeline figures are drawn in TikZ, not matplotlib,
and follow the same regenerability rule: a standalone `.tex` source per
diagram, compiled into the build, never a screenshot or an exported PNG from
a drawing tool.

- Before drawing, read the project's preamble (`header.tex` or equivalent)
  for available packages, color definitions, and macros, and read one
  existing figure source to match its style — line weights, fonts, palette.
- One figure, one message: a diagram answering two questions is two diagrams.
  The reader should get the mechanism from the diagram plus its caption alone.
- Reuse the data palette (the colorblind-safe cycle in `paper.mplstyle`) for
  semantic colors so diagrams and plots read as one system.
- Text inside diagrams stays ≥ 7 pt at print size; when a diagram needs a
  paragraph to explain, the diagram is wrong, not the caption.

## The LaTeX side

A figure's job is not done until it sits correctly in the paper:

- **Wiring** — every figure gets a `\label`, every label is `\ref`'d in the
  body text, and the reference is interpretive: say what to notice, never a
  bare "see Figure X".
- **Captions are self-sufficient**: what is shown, what the axes/colors/
  groups mean, units, n and spread definition, and the takeaway — readable
  without the body text, since reviewers scan captions first.
- **Placement** — floats defined in source in the order first referenced;
  prefer `[t]`; keep each float within about a page of its first reference;
  flag floats that land isolated on their own page.
- **Subfigure grids** — align rows with `[t]`, and add explicit
  `height=` constraints when a row mixes aspect ratios or raster with
  vector; check that subcaptions align across the row.
- After any figure change, recompile and check the build log for overfull
  boxes and undefined references before reporting done.

## Workflow

1. Read the artefacts; check the numbers against any table that already
   reports them — a figure/table mismatch is a bug to raise, not to plot over.
2. Write or edit the figure script; header comment lists the EXP ids/paths.
3. Run it; view the PDF at 100% scale mentally sized against a two-column
   page — if a label would be under ~7 pt in print, enlarge fonts or simplify,
   never shrink content by scaling.
4. Report: figures written, the script paths, the runs each traces to, and
   the caption sentence proposed for each (message + n + spread definition).

When several figures share data loading, factor a small `figure/common.py`;
resist a framework beyond that.
