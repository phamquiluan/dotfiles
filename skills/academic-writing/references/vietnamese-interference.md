# Vietnamese-L1 Interference Patterns in Academic English

Checklist for polishing prose written by a Vietnamese L1 author. Vietnamese is
analytic — no articles, no plural or verb inflection, no agreement, time
marked by particles (đã/đang/sẽ), topic-prominent word order — so the
highest-frequency errors are omissions English marks obligatorily. Check the
starred patterns on every pass; they account for most findings.

## Contents

- [P1–P4: The big four (check every pass)](#p1p4-the-big-four-check-every-pass)
- [P5–P9: Verbs and tense](#p5p9-verbs-and-tense)
- [P10–P13: Calqued prepositions and verbs](#p10p13-calqued-prepositions-and-verbs)
- [P14–P17: Word choice and register](#p14p17-word-choice-and-register)
- [P18: Sentence-level habits](#p18-sentence-level-habits)
- [Grep-able self-checks](#grep-able-self-checks)

## P1–P4: The big four (check every pass)

**P1* Article omission.** Vietnamese has no articles. Every singular countable
noun needs a determiner; scan for bare ones.
- ✗ "We propose method that uses transformer." → ✓ "We propose **a** method
  that uses **a** transformer."
- Rules of thumb: first mention of a countable singular → *a/an*; already
  identified or unique in context → *the*; generalizing → bare plural
  ("Transformers dominate...", not "The transformers dominate...").
- Overcorrection also occurs: no *the* before general field names
  (✗ "the machine learning has advanced" → ✓ "machine learning has advanced").

**P2* Plural -s omission.** Vietnamese marks plurality with quantifiers
(các/những), not inflection, so a numeral feels sufficient.
- ✗ "three dataset", "many approach", "one of the method"
- ✓ "three dataset**s**", "many approach**es**", "one of the method**s**"

**P3* Subject–verb agreement.** No agreement exists in Vietnamese; check every
subject–verb pair, especially with intervening phrases.
- ✗ "The results of the ablation **shows**..." → ✓ "The results ... **show**..."
- ✗ "Each of the baselines **were** tuned" → ✓ "**was** tuned"

**P4* Uncountable nouns pluralized.** Vietnamese does not distinguish
countable from mass nouns.
- ✗ "researches", "informations", "evidences", "feedbacks", "trainings",
  "equipments", "knowledges"
- ✓ "research / studies", "information", "evidence", "feedback", "training"

## P5–P9: Verbs and tense

**P5 Tense dropped or flattened.** Vietnamese marks time with particles and
adverbs, so inflection gets forgotten once a time word is present.
- ✗ "We conduct the experiments in the previous section and observe..."
  (when reporting completed work) → ✓ "We conduct**ed** ... and observ**ed**..."
- Academic convention: present for what the paper does ("Section 3
  **describes**"), past for what was done ("we **trained** on..."), present
  perfect for prior-work trends ("recent work **has explored**...").

**P6 "can" overuse.** "Có thể" precedes most Vietnamese claims; in English it
weakens them.
- ✗ "Our method can improve accuracy" → ✓ "Our method **improves** accuracy"
- Keep *can* only for genuine capability or possibility claims.

**P7 Missing dummy subject.** Vietnamese drops subjects freely; English
requires *it/there*.
- ✗ "Is important to note that..." → ✓ "**It** is important to note that..."
- ✗ "Have two reasons for this." → ✓ "**There** are two reasons for this."

**P8 "There is/are" vs "It is" confusion.** Existence takes *there*;
evaluation takes *it*.
- ✗ "It has many studies on this topic" → ✓ "**There are** many studies..."

**P9 Bare verb after modal/to.** ✗ "allows to improve", "helps improving"
→ ✓ "allows **us to** improve" / "allows improv**ing**", "helps improve".

## P10–P13: Calqued prepositions and verbs

**P10 Redundant "about" after transitive verbs.** Calque of "về" (thảo luận
về, đề cập về).
- ✗ "discuss about", "mention about", "describe about", "consider about"
- ✓ drop *about*: "discuss the results", "mention the limitation"
- (But: "talk about", "think about" are correct.)

**P11 Wrong comparison prepositions.** Calques of "khác với", "giống với",
"so với".
- ✗ "different **with**" → ✓ "different **from**"
- ✗ "similar **with**" → ✓ "similar **to**"
- ✗ "compare**d** **with** the accuracy increases" — fine as "compared with/to",
  but check the compared items are parallel.
- ✗ "depend **to**" → ✓ "depend **on**"; ✗ "consist **in**" → ✓ "consist **of**"

**P12 "join/attend/enter" style verb calques.**
- ✗ "join the experiment" (tham gia) → ✓ "participate in the experiment"
- ✗ "open the survey" (mở) for launching → ✓ "launch / conduct the survey"

**P13 "make/do" confusion and light-verb calques.**
- ✗ "do a comparison", "make experiment" → ✓ "compare", "run / conduct
  experiments" — prefer the single verb over the light-verb phrase.

## P14–P17: Word choice and register

**P14 "almost" vs "most".** Calque of "hầu hết"; very common.
- ✗ "**Almost** researchers agree", "**almost of** the cases"
- ✓ "**Most** researchers agree", "**most of** the cases"
- *Almost* modifies adjectives/verbs/numbers ("almost all", "almost 90%").

**P15 "Besides," as a sentence opener.** Reads informal in papers.
- ✗ "Besides, we evaluate..." → ✓ "In addition, we evaluate..." /
  "Moreover, ..."

**P16 Intensifier overuse.** "Rất" maps to *very*; academic prose prefers a
stronger word or a number.
- ✗ "very good performance", "very fast" → ✓ "strong performance (67% Top-1)",
  "fast (8 ms per diagnosis)"

**P17 Politeness hedging imported into claims.** Vietnamese academic register
softens assertions; English venues read it as lack of confidence.
- ✗ "We would like to propose...", "We try to show..." → ✓ "We propose...",
  "We show..."

## P18: Sentence-level habits

- **Comma splices.** Vietnamese tolerates comma-joined clauses; English needs
  a conjunction, semicolon, or period. ✗ "The model converges quickly, it
  needs fewer epochs." → split into two sentences.
- **Topic-fronting.** ✗ "For the accuracy, it increases by 5%." →
  ✓ "Accuracy increases by 5%." Delete the fronted topic and its resumptive
  pronoun.
- **Mixed constructions.** ✗ "As shown in Figure 2 **that** accuracy drops" →
  ✓ "As shown in Figure 2, accuracy drops" or "Figure 2 shows that accuracy
  drops."

## Grep-able self-checks

Run over the LaTeX source after editing; each hit is a candidate, not
automatically an error:

```bash
grep -nE "discuss about|mention about|describe about|consider about" *.tex
grep -nE "researches|informations|evidences|feedbacks|equipments|knowledges" *.tex
grep -nE "different with|similar with|depend to|consist in" *.tex
grep -nE "[Aa]lmost (researchers|methods|studies|papers|of the)" *.tex
grep -nE "^Besides,|\. Besides," *.tex
grep -nE "can (improve|achieve|reduce|increase|solve|help)" *.tex
grep -nE "would like to (propose|present|show)|try to (show|prove)" *.tex
grep -nE "allows to|helps to [a-z]+ing" *.tex
```

Bare-noun and agreement errors (P1–P3) are not grep-able; they need a read.
