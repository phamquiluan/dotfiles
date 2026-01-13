---
name: icml-intro-writer
description: >
  Revise ICML/NeurIPS/ICLR paper introductions to match oral-quality writing patterns.
  Use when writing or revising a machine learning paper introduction, when user mentions
  ICML/NeurIPS/ICLR paper writing, when user asks to improve introduction structure or flow,
  or when user wants to make introduction more compelling for top ML venues.
---

# ICML Introduction Writer

Revise introductions to match patterns from ICML 2025 oral papers. Based on analysis of 10 accepted oral papers spanning theory, methods, benchmarks, and applications.

## Revision Workflow

### Step 1: Analyze Current Introduction

Read the introduction and identify:
- Current opening strategy
- How problem motivation is established
- How gap is identified
- How solution is previewed
- How contributions are presented
- Citation integration style

### Step 2: Select Appropriate Patterns

Based on paper type, select patterns from [references/patterns.md](references/patterns.md):

| Paper Type | Opening | Motivation | Gap Style |
|------------|---------|------------|-----------|
| New method | Contrast or Challenge-first | Applications-based | Technical barriers |
| Benchmark | Historical progression | Proxy-metric mismatch | Empirical demonstration |
| Theory | Universal importance | Resistance-based | Comparative refinement |
| Application | Crisis-driven or Systems | Multi-stakeholder | Practical limitations |

### Step 3: Apply Revision Checklist

**Opening (Para 1)**
- [ ] Does NOT start with "In this paper, we..."
- [ ] Establishes context before narrowing to problem
- [ ] Uses one of 7 opening strategies

**Motivation (Para 2-3)**
- [ ] Concrete applications or importance stated
- [ ] Scale/urgency established
- [ ] Citations support claims

**Gap (Para 3-4)**
- [ ] Specific limitation, not vague "insufficient"
- [ ] Prior work acknowledged before criticizing
- [ ] Gap flows naturally to solution

**Solution Preview (Para 4-5)**
- [ ] Method named clearly
- [ ] Key insight or reframing stated
- [ ] Scope clarified if needed

**Contributions (Final Para)**
- [ ] Clearly signaled ("Our contributions are:")
- [ ] Action verbs start each item
- [ ] Quantified when possible
- [ ] 3-4 items typical

### Step 4: Polish Transitions

Use transition phrases from [references/phrases.md](references/phrases.md):
- Paragraph connections should flow logically
- Avoid abrupt topic shifts
- Use contrast phrases for gap identification
- Use causal phrases for solution justification

### Step 5: Verify Citation Integration

- Definitions have citations
- Limitations cite specific prior work
- No orphan citation clusters at paragraph ends
- Use "Following~\citet{}, we..." pattern when building on prior work

## Quick Reference

### Never Do
- Open with "In this paper, we propose..."
- Use vague gap: "existing methods are insufficient"
- List contributions without action verbs
- Cluster citations at paragraph ends without integration

### Always Do
- Establish context before narrowing
- Acknowledge prior work before criticizing
- Quantify improvements when available
- Use hedging appropriately (may, suggests, indicates)

### Sentence Length
- Short sentences for key claims
- Longer sentences for technical explanations
- No run-on sentences

## Resources

- **[references/patterns.md](references/patterns.md)**: Detailed patterns with examples from 10 oral papers
- **[references/phrases.md](references/phrases.md)**: Ready-to-use phrases organized by function
