# ICML Introduction Patterns

Patterns extracted from 10 ICML 2025 oral papers. Use these as templates when revising introductions.

## Table of Contents
1. [Opening Strategies](#opening-strategies)
2. [Problem Motivation](#problem-motivation)
3. [Gap Identification](#gap-identification)
4. [Solution Preview](#solution-preview)
5. [Contributions Format](#contributions-format)
6. [Citation Integration](#citation-integration)
7. [Sentence Structures](#sentence-structures)

---

## Opening Strategies

**Never open with "In this paper, we propose..."** All 10 oral papers avoid this. Instead use:

### 1. Contrast Opening
Position work against established paradigm.
```
In contrast to model-centric learning, data-centric learning focuses on...
```
**When to use**: Method challenges conventional approach or reframes problem.

### 2. Universal Importance
Establish fundamental value before narrowing.
```
The discovery of mathematical constructions is fundamental to theoretical mathematics.
```
**When to use**: Theoretical contributions, foundational methods.

### 3. Systems Phenomenon
Frame as emergent behavior in complex systems.
```
The dynamic interaction among agents and algorithms creates a complex ecosystem where unanticipated individual and collective behavior can emerge.
```
**When to use**: Multi-agent systems, platform dynamics, sociotechnical systems.

### 4. Challenge-First
State dual/multiple challenges upfront.
```
A crucial requirement for such systems is the ability to interact effectively with external environments... However, two challenges hinder the development...
```
**When to use**: When solving multiple interrelated problems.

### 5. Historical Progression
Show field evolution leading to current gap.
```
Language models traditionally have been evaluated on language reasoning and understanding tasks like MMLU. However, state-of-the-art models have outgrown the usefulness of many of these benchmarks...
```
**When to use**: Benchmark papers, capability evaluations.

### 6. Capability-First
Position as advancing established successful approach.
```
As machine learning systems grow in scale, accurate predictive models of their training dynamics become increasingly valuable...
```
**When to use**: Scaling work, improvements to established methods.

### 7. Crisis-Driven
Real-world catastrophe establishing urgency.
```
Modern IT systems are driving many facets of our economy... The recent CrowdStrike outage highlighted these challenges as it brought down our society's most critical systems from hospital services to air travel, costing an estimated $5.4 billion.
```
**When to use**: Applied systems, safety-critical domains.

---

## Problem Motivation

### 1. Applications-Based (Breadth)
List concrete applications to show importance.
```
...holds significant potential in many areas such as model interpretation, subset training set selection, noisy label detection, and active learning.
```

### 2. Resistance-Based (Temporal)
Emphasize problem's historical difficulty.
```
Despite its simple statement, this problem combines discrete choices, continuous geometry, and hard constraints in a way that has resisted resolution for over seventy years.
```

### 3. Multi-Stakeholder (Societal)
Connect to broader societal implications.
```
The study of such behavior is crucial for understanding how to design systems that are robust, fair, and aligned with societal values.
```

### 4. Proxy-Metric Mismatch
Show gap between measured and desired outcomes.
```
However, the MLIP literature has mostly focused on assessing models based on energy and force predictions over static DFT test sets rather than directly assessing their performance in complex simulations. This approach has limitations, as improved accuracy on test sets does not always lead to better predictions of physical properties.
```

### 5. Paradox/Counterintuitive
Frame as unexplained phenomenon.
```
Why do deep learning systems sometimes develop proper computational algorithms, instead of simply interpolating the data? Understanding this is crucial for the safe application of machine learning models.
```

---

## Gap Identification

### 1. Technical Barriers
Identify specific computational/methodological constraints.
```
...their applicability to deep models is constrained by the strong convexity assumption and the computational cost linked to calculating the inverse of the Hessian matrix.
```

### 2. Historical Resistance
Frame as long-standing unsolved problem.
```
Despite... this problem has resisted resolution for over seventy years.
```

### 3. Practical Limitations
Show prior work fails in real conditions.
```
Unfortunately, several of the strategies studied by \citet{prior} are not available in practice to the collective.
```

### 4. Empirical Demonstration
Show gap through data contrast.
```
On a 24-defense subset... 75% success rate. But on real world defenses... only 13% of the time.
```

### 5. Comparative Refinement
Position as improvement on specific prior work.
```
While Kaplan et al. (2020) found the loss curves roughly follow a sum of power laws, we identify that loss curves follow a universal shape with far greater precision.
```

---

## Solution Preview

### 1. Problem Reframing
```
We present a framework that reformulates this geometric coloring problem as a continuous optimization task.
```

### 2. Question-Driven
```
In this paper, we address two questions: Why does higher test accuracy sometimes fail to enhance a model's ability to predict physical properties, and how can we improve MLIPs to excel in this area?
```

### 3. Framework Introduction
```
In this paper, we introduce a new framework to enable members of the collective to learn strategies efficiently and to infer the parameters that determine their success.
```

### 4. Bridge Metaphor
```
We build a bridge between identifying detrimental training samples via influence functions and outlier detection on the gradient space.
```

---

## Contributions Format

### 1. Bulleted List with Action Verbs
Most common format. Each bullet starts with "We".
```
Our major contributions are as follows:
\begin{itemize}
\item We build a bridge between...
\item We demonstrate empirically that...
\item We achieve state-of-the-art performance on...
\end{itemize}
```

### 2. Enumerated with Forward References
Link to paper sections.
```
Our main contributions are as follows:
\begin{itemize}
\item In Section~\ref{sec:theory}, we provide a local interaction theory...
\item In Section~\ref{sec:analysis}, we explain how...
\item In Section~\ref{sec:experiments}, we demonstrate...
\end{itemize}
```

### 3. Threefold Structure
```
Our contributions are threefold:
(1) Proposing a comprehensive benchmark suite...
(2) Development of an efficient agent framework...
(3) Conducting extensive evaluations providing valuable insights...
```

### 4. Quantified Improvements
Include specific numbers when available.
```
We obtained a 5-coloring covering all but 3.74\% of the plane, improving on the previous best of 4.01\%.
```
```
MICA achieves 67\% Top-1 accuracy, a 253\% improvement over the best baseline.
```

---

## Citation Integration

### 1. Definition with Citation
```
\textit{Data-centric} learning focuses on improving the data rather than the model~\citep{oala2023dmlr}.
```

### 2. Topic Clustering
Group related methods.
```
...has been explored in microservices~\citep{a,b,c} and cloud systems~\citep{d,e}.
```

### 3. Problem Citation at Weakness
Place citation where limitation is stated.
```
...incur significant computational costs, especially for large-scale data analysis~\citep{schioppa2022scaling}.
```

### 4. Following Pattern
```
Following~\citet{rafailov2024direct}, we apply a sequential variant of Direct Preference Optimization.
```

### 5. Specific Comparison
```
Our lower bounds are tighter than those from~\citet{hardt2023collectiveaction}.
```

### 6. Historical Grounding
```
First posed in 1950; for a comprehensive treatment, see~\citet{soifer2009mathematical}.
```

---

## Sentence Structures

### Short Punchy Claims
One idea per sentence for key claims.
```
This approach fails when the graph is unknown.
```
```
The network is not penalized for breaking after a certain length.
```

### Multi-Clause Technical
For complex ideas with clear punctuation.
```
While the complexity of modern architectures, optimizers, and datasets often renders exact analyses intractable for any individual model, recent work shows that some key aspects of training are predictable when we focus on their scaling behavior.
```

### Contrast Structure
```
Our work differs from this notion of curiosity in that we do not leverage intrinsic motivation. Instead, we train our agents to explore and interact with an entirely unseen environment.
```

### Concession-Advancement
```
While these efforts significantly contribute to understanding LLM-based agent design, the evaluation of MLLM embodied agents remains underexplored.
```

### Rhetorical Questions
For engaging reader (use sparingly).
```
Why do deep learning systems sometimes develop proper computational algorithms, instead of simply interpolating the data?
```
