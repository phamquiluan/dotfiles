# Plan: Create writing-with-style Skill

## Problem with PDF Reading
- The PDF has 171 pages
- Reading pages accumulates context in conversation
- After ~15-20 pages, context exceeds max request size (413 error)

## Solution: Use Task Agents
- Spawn Task agents to read batches of pages (e.g., pages 1-30, 31-60, etc.)
- Each agent reads pages, extracts key principles, appends to NOTE.md
- Agent returns short summary; detailed PDF content stays in agent's context
- Main conversation stays small

## Progress So Far
- [x] Split PDF into 171 individual pages at `temp_pages/`
- [x] Created NOTE.md with initial notes (pages 1-10)
- [x] Read remaining pages using Task agents (151 agents, 1 per page)
- [x] Created SKILL.md with consolidated Pinker principles
- [x] Cleaned up temp_pages directory

## Reading Plan (6 batches)
1. Pages 1-30: Prologue + Chapter 1 (Good Writing)
2. Pages 31-60: Chapter 2 (A Window onto the World)
3. Pages 61-90: Chapter 3 (The Curse of Knowledge)
4. Pages 91-120: Chapter 4 (The Web, The Tree, and The String)
5. Pages 121-150: Chapter 5 (Arcs of Coherence)
6. Pages 151-171: Chapter 6 (Telling Right from Wrong)

## Skill Creation Steps
1. Complete reading all 171 pages via Task agents
2. Consolidate NOTE.md into actionable style rules
3. Create skill using skill-creator pattern:
   - instructions.md: Main style guidelines
   - examples/: Good and bad writing examples
   - Optional: checklist.md for style review

## Skill Structure (based on skill-creator)
```
skills/writing-with-style/
├── instructions.md      # Main skill prompt with Pinker's principles
├── NOTE.md             # Reading notes (working file)
├── PLAN.md             # This file
├── examples/           # Writing examples
│   ├── good-style.md
│   └── bad-style.md
└── temp_pages/         # Split PDF pages (cleanup after)
```

## Key Principles Identified So Far
1. Classic style: prose as window onto world
2. Show, don't tell - use concrete imagery
3. Fresh wording over clichés
4. Phonesthetics - words should sound like meaning
5. Strong endings
6. Language is a wiki, not a protocol (evolving, not fixed rules)
7. Replace dogma with reason and evidence

## Next Steps
1. Start fresh session
2. Read this PLAN.md
3. Use Task agents to read page batches and update NOTE.md
4. Create the skill files
