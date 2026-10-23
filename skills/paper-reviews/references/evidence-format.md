# Evidence Format: Examples

Worked examples of the citation scheme and the content rules in SKILL.md. The examples use
flat `(Lines ...)` coordinates. Substitute `(p. 11, lines 37-38)` when the manuscript prints
per-page margin numbers.

## Citations

Paper under review, with the quote inline:
- `"we introduce ComplexMCP, a benchmark designed to evaluate agents" (Lines 11-12)`
- `"even top-tier models fail to exceed a 60% success rate" (Line 30)`

Related work the paper already cites (here as [9] and [44]):
- `[9] reports the distraction as caused by AI suggestions, not by verbalization.`
- `[44] uses fixed pre-segmented intervals tied to GitHub Copilot.`

Reviewer-introduced related work (not in the paper's bibliography):
- `MCP-Bench covers 250 tools across 28 servers [A].`
- `tau-Bench is limited to retail and airline domains [B].`

Comparing the paper with related work:
- `The paper claims its design "minimizes distraction" relative to refs [9-11] (Lines 113-116), but [9] reports the distraction as caused by AI suggestions, not by verbalization.`

Artifact:
- `The paper claims "we use learning rate 0.001" (Line 234), but configs/train.yaml sets lr=0.01.`

Anti-patterns:
- `Prather et al. [A] (cited as [9]) reports ...` (the paper already numbers this work)
- `Mozannar et al. [B] introduced CUPS ...` when the paper lists Mozannar et al. as [44]

## Strengths

Bad (generic, no evidence):
> The paper presents a comprehensive benchmark with thorough experiments.

Bad (bolded title, em-dash, three sentences when one would do):
> **S1 — Comprehensive benchmark.** The benchmark covers many tools. It also addresses a gap. The seed-driven architecture is novel.

Good (one sentence):
> Unlike prior MCP benchmarks that treat tools as isolated units [A], ComplexMCP models cross-tool state through a "seed-driven architecture to simulate dynamic environment states and unpredictable API failures" (Lines 24-26).

Good (two sentences):
> The 84-developer deployment (Lines 285-289) is unusually strong evidence of in-the-wild use for a 4-page tool paper. The same JSON outputs supported the sequential-pattern mining and thematic analysis reported in the companion FSE study (Lines 336-340).

## Weaknesses

Bad (vague, not actionable):
> The experimental evaluation could be more thorough.

Bad (bolded title, em-dash, no evidence):
> **W3 — Weak evaluation.** Only 7 models tested. More are needed.

Good (judgement, evidence, thought, 4 sentences):
> The evaluation does not exercise the latest frontier models, so the reported ceiling cannot be attributed to a fundamental limit of the benchmark. The paper evaluates only 7 LLMs (Line 245, Table 2) and omits Gemini 2.5 and DeepSeek-R1-0528. Given the paper's own finding that "top-tier models fail to exceed a 60% success rate" (Line 30), the ceiling may be model-specific rather than task-intrinsic. Adding 2-3 recent frontier models would let Section 4 separate these two explanations.

Good (with OpenReview math, 4 sentences):
> The training objective has no explicit regularization, which leaves the small-data regime exposed to overfitting. The loss is $\\mathcal{L} = \\sum_{i=1}^{N} \\ell(f(x_i), y_i)$ (Line 142) with no $\\lambda \\|\\theta\\|_2^2$ term. The training set is only 500 samples (Lines 198-200), so the Table 3 gains may reflect memorization rather than generalization. Reporting results with $\\lambda \\in \\{10^{-3}, 10^{-4}, 10^{-5}\\}$ would clarify whether the improvements are robust.

## Questions

Bad (generic):
> How do you handle edge cases?

Good (specific, states the impact):
> The seed-driven evaluation claims "deterministic yet diverse evaluation" (Lines 26-27), but it is unclear how many seeds were used per task and whether results are stable across seeds. If the variance across seeds is high ( $> 5\\%$ absolute), the reported scores in Table 2 may not be reliable. Could the authors report per-seed variance? A positive answer showing low variance would raise my Soundness rating from 2 to 3.

Good (with math):
> The convergence guarantee assumes $\\mathbb{E}[\\nabla f(x)]$ is $L$-Lipschitz (Lines 112-114), but Theorem 1 requires $L < \\frac{1}{\\eta}$ where $\\eta$ is the learning rate. The experiments use $\\eta = 0.01$ (Line 230), implying $L < 100$, but no empirical estimate of $L$ is provided. Could the authors verify this bound on the datasets in Table 1? If $L \\geq 100$ in practice, the convergence rate in Theorem 1 would not apply, and my Soundness rating would drop from 3 to 2.

## Journal minor comments

> The y-axis of Figure 4 (p. 14) is unlabeled, so readers cannot tell whether it shows latency or throughput.

> Section 5.2 (p. 19) cites [112] for the claim that "most incidents are change-induced", but [112] studies only one cloud provider.

## References section

Conference style:

```
### References

[A] Mo et al., "LiveMCPBench: Can Agents Navigate an Ocean of MCP Tools?," 2025. arXiv:2508.01780
[B] Yao et al., "tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains," 2024. arXiv:2406.12045
```

Journal forms often ask for all authors, the full venue name, and a URL. Follow the form.
