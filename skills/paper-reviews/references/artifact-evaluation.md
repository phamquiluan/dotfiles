# Artifact Evaluation Guide

Based on the ACM/SIGSOFT artifact evaluation criteria used at FSE, ICSE, ASE, and ISSTA. When the
venue's call for artifacts is provided, its criteria and thresholds take precedence over this file.

## Badges

Artifacts may qualify for three independent badges:

### Available

- Artifact is placed on a **publicly accessible archival repository** with a DOI or persistent identifier.
- Examples: Zenodo, Figshare, Dryad, institutional repositories. GitHub alone does NOT qualify unless archived (e.g., via Zenodo-GitHub integration).
- Check: Does the artifact have a permanent URL/DOI? Is it on an archival platform?

### Functional

The artifact is **documented, consistent, complete, exercisable**, and includes evidence of verification.

**Checklist:**
- [ ] **Documented** — README describes installation, dependencies, and usage
- [ ] **Consistent** — Artifact matches what the paper describes (same algorithms, same datasets, same parameters)
- [ ] **Complete** — All components needed to reproduce results are present (code, data, configs, scripts)
- [ ] **Exercisable** — Can be executed and produces meaningful output
- [ ] **Verification evidence** — Authors provide expected outputs or test scripts to verify correctness
- [ ] **Installation** — Can be set up within 30 minutes following provided instructions
- [ ] **Requirements** — Dependencies are explicitly listed with version numbers

### Reusable

Exceeds functional requirements; the artifact is **well-structured for reuse and adaptation** by other researchers.

**Checklist (in addition to Functional):**
- [ ] **Modular design** — Code is organized into clear modules/packages with separation of concerns
- [ ] **Parameterized** — Key experimental parameters are configurable (not hardcoded)
- [ ] **Extensible** — New datasets, models, or configurations can be added without modifying core code
- [ ] **Code quality** — Follows language conventions, consistent style, meaningful names
- [ ] **Testing** — Unit tests or integration tests are provided
- [ ] **API documentation** — Public functions/classes have docstrings or API docs
- [ ] **Examples** — Example scripts or notebooks demonstrate usage beyond the paper's experiments
- [ ] **License** — Open-source license is included (e.g., MIT, Apache 2.0, GPL)

## Evaluation Workflow

### 1. Inventory the artifact

List all top-level files and directories. Identify:
- README or documentation files
- Source code directories
- Data files or download scripts
- Configuration files
- Test suites
- License file
- Requirements/dependency files (requirements.txt, environment.yml, Dockerfile, etc.)

### 2. Check documentation quality

- Does the README explain what the artifact is and how it relates to the paper?
- Are installation instructions clear and complete?
- Are reproduction steps documented (which scripts to run, in what order, with what parameters)?
- Are expected outputs or reference results provided?

### 3. Assess consistency with paper

Cross-reference the artifact against the paper:
- Do the implemented algorithms match the paper's description?
- Are the datasets referenced in the paper included or downloadable?
- Do configuration files match the experimental setup described in the paper?
- Are all baselines mentioned in the paper included?

### 4. Evaluate code quality (for Reusable badge)

- **Structure**: Is the code logically organized? Are there clear entry points?
- **Readability**: Can another researcher understand the code without the paper?
- **Configurability**: Are hyperparameters, paths, and settings externalized?
- **Error handling**: Does the code fail gracefully with informative messages?
- **Dependencies**: Are they pinned to specific versions? Is there a lockfile?

### 5. Check reproducibility infrastructure

- Docker/container support for environment isolation?
- Makefile or shell scripts for one-command reproduction?
- CI/CD configuration showing tests pass?
- Seed setting for deterministic results?

## Output Format

When artifact evaluation is included in a review, add an `### Artifact Evaluation` section. Use `####` subheadings for sub-sections, not `**bold**` labels. Do not use em-dashes in the output.

```markdown
### Artifact Evaluation

Artifact location: [URL or description of provided artifact]

#### Badge assessment

| Badge | Recommendation | Justification |
|-------|---------------|---------------|
| Available | Yes/No/Partial | [Specific reason with evidence] |
| Functional | Yes/No/Partial | [Specific reason with evidence] |
| Reusable | Yes/No/Partial | [Specific reason with evidence] |

#### Strengths

1. [One specific positive aspect of the artifact with a file/path reference. 1-2 sentences.]
2. [Second positive aspect with citation. 1-2 sentences.]

#### Weaknesses

1. [Judgement sentence stating what is wrong.] [Evidence sentence with file path or paper `(Lines ...)`.] [Thought sentence on impact and actionable fix.]
2. [Same structure: judgement, then evidence, then thought.]

#### Consistency with paper

- [Specific matches or discrepancies between artifact and paper claims, citing Lines from paper.]
```

## Evidence Format for Artifact Review

Use file path references for artifact citations:
- `README.md` for documentation issues
- `src/model.py:42` for specific code locations
- `configs/experiment.yaml` for configuration references

Combine with paper line references when checking consistency:
- `The paper claims "we use learning rate 0.001" (Line 234), but configs/train.yaml sets lr=0.01.`
