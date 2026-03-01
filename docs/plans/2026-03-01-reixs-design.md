---
title: REIXS Design Document
date: 2026-03-01
keywords: [reixs, real-estate, ai-workflows, specification, validation]
lastUpdated: 2026-03-01
---

# REIXS Design Document

**Real Estate Intelligence Execution Specification — Implementation Design**

## 1. Overview

REIXS is a versioned, testable execution specification for real estate AI workflows. It lets authors define what an AI task must accomplish (objective + hard constraints), what domain terms mean (DDD references), what behaviors are required (SESF v3 rules), and what "good" looks like (evaluation fixtures) — all in a single Markdown file.

The system parses, validates, and compiles REIXS specs into machine-readable JSON, catching errors in the spec itself before any AI agent runs.

**First vertical slice:** Lease abstraction for Ontario commercial leases.

## 2. Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Repo | Standalone `reggiechan74/reixs` | Clean separation, own CI, publishable to PyPI later |
| SESF integration | Vendor `validate_sesf.py` | Self-contained, no external path deps. Re-copy when SESF evolves |
| CLI framework | Click | Battle-tested, good subcommand support, minimal learning curve |
| SESF block format | Full SESF v3 required | More rigorous — catches real issues. §6.6 example needs updating |
| Markdown parser | markdown-it-py | Full CommonMark AST, well-maintained, used by MyST/Sphinx |
| Python version | 3.11+ | Matches Codespace environment |

## 3. Architecture

### Pipeline

```
REIXS.md → [markdown-it-py Parser] → ReixsSpec (Pydantic)
                                          ↓
                                    [5-Pass Validator]
                                     ├─ Pass 1: Structural
                                     ├─ Pass 2: OFD
                                     ├─ Pass 3: Domain
                                     ├─ Pass 4: SESF (vendored validator)
                                     └─ Pass 5: Cross-field
                                          ↓
                                    [Compiler] → reixs.runtime.json
                                               → reixs.manifest.json
                                               → reixs.validation.json
```

Each stage is independent and testable. The compiler refuses to compile if validation status is `fail`.

### Module Layout

```
reixs/
├── pyproject.toml
├── README.md
├── src/reixs/
│   ├── __init__.py
│   ├── cli.py                   # Click commands: validate, compile, init
│   ├── parser/
│   │   ├── __init__.py
│   │   ├── markdown_parser.py   # markdown-it-py → section tree
│   │   ├── section_model.py     # intermediate section objects → Pydantic
│   │   └── sesf_extractor.py    # extract ```sesf fenced blocks
│   ├── schema/
│   │   ├── __init__.py
│   │   ├── reixs_models.py      # ReixsSpec, MetaSection, OFDSection, etc.
│   │   ├── enums.py             # Tier, TaskType, FieldStatus
│   │   └── runtime_payload.py   # RuntimePayload, Manifest
│   ├── validate/
│   │   ├── __init__.py
│   │   ├── structural.py        # Pass 1
│   │   ├── ofd.py               # Pass 2
│   │   ├── domain.py            # Pass 3
│   │   ├── cross_field.py       # Pass 5
│   │   └── report.py            # ValidationReport model + formatters
│   ├── sesf/
│   │   ├── __init__.py
│   │   ├── validate_sesf.py     # vendored from cc-plugins/structured-english
│   │   └── adapter.py           # Pass 4: maps SESF ValidationResult → Finding
│   ├── compile/
│   │   ├── __init__.py
│   │   └── compiler.py          # ReixsSpec → runtime JSON + manifest
│   ├── registry/
│   │   ├── __init__.py
│   │   ├── task_types.py        # known task type registry
│   │   ├── jurisdictions.py     # known jurisdiction profiles
│   │   └── ddd_refs.py          # DDD reference registry + format validator
│   └── utils/
│       ├── __init__.py
│       └── hashing.py           # source hash for manifest
├── specs/
│   ├── templates/
│   │   └── lease_abstraction_ontario.reixs.md
│   ├── examples/
│   │   └── lease_abstraction_sample.reixs.md
│   ├── invalid/
│   │   ├── missing_ofd.reixs.md
│   │   ├── missing_sesf.reixs.md
│   │   ├── missing_ddd_ref.reixs.md
│   │   └── complex_no_adr.reixs.md
│   └── schemas/
│       ├── reixs_v1.json
│       └── lease_abstraction_output_v1.json
├── tests/
│   ├── test_parser.py
│   ├── test_validator.py
│   ├── test_compiler.py
│   ├── test_sesf_adapter.py
│   └── golden/
│       ├── valid_report.json
│       └── valid_runtime.json
└── docs/
    ├── REIXS_SPEC.md
    └── ADR/
        ├── ADR-001-layered-artifacts.md
        └── ADR-003-hard-constraints-before-scoring.md
```

## 4. Data Models

### Enums

```python
class Tier(str, Enum):
    MICRO = "micro"
    STANDARD = "standard"
    COMPLEX = "complex"

class FieldStatus(str, Enum):
    FACT = "fact"
    INFERENCE = "inference"
    MISSING = "missing"
    CONFLICT = "conflict"
```

### Core Spec Model

```python
class MetaSection(BaseModel):
    spec_id: str
    version: str               # semver
    task_type: str
    tier: Tier
    author: str
    date: date

class OFDSection(BaseModel):
    # Required (all tiers)
    primary_objective: str
    hard_constraints: list[str]
    autofail_conditions: list[str]
    optimization_priority_order: list[str]
    uncertainty_policy: str
    # Required for standard/complex only
    secondary_objectives: list[str] | None = None
    tradeoff_policies: list[str] | None = None
    scoring_model: str | dict | None = None
    escalation_triggers: list[str] | None = None
    error_severity_model: dict[str, list[str]] | None = None

class ReixsSpec(BaseModel):
    meta: MetaSection
    objective: str
    domain_context: DomainContextSection
    inputs: InputsSection
    ofd: OFDSection
    constraints: ConstraintsSection
    output_contract: OutputContractSection
    evaluation: EvaluationSection
    behavior_spec: BehaviorSpecSection  # raw SESF text + parsed SESFDocument
    validation_checklist: list[str]
    source_hash: str
```

### Compiler Output Models

```python
class RuntimePayload(BaseModel):
    spec_metadata: dict
    task_context: dict
    ofd: dict
    behavior_rules: dict       # raw SESF + parsed references
    output_contract: dict
    eval_config: dict
    references: dict
    validation_status: str     # pass | warn | fail

class Manifest(BaseModel):
    spec_id: str
    version: str
    source_hash: str
    compile_timestamp: str
    artifacts: list[str]
```

## 5. Parser Design

Two-stage pipeline:

### Stage 1: Markdown → Section Tree

Using `markdown-it-py`:
1. Parse full document into AST
2. Walk AST, grouping content by `##` heading level
3. Normalize heading text to canonical names via alias map
4. Extract: bullet lists → `list[str]`, key-value pairs → `dict`, sub-headings → nested dicts, fenced code blocks → tagged by language, free text → string

Heading alias map:

```python
SECTION_ALIASES = {
    "meta": ["meta"],
    "objective": ["objective"],
    "domain_context": ["domain context", "domain"],
    "inputs": ["inputs", "input"],
    "ofd": ["objective function design", "objective function design (ofd)", "ofd"],
    "constraints": ["constraints"],
    "output_contract": ["output contract"],
    "evaluation": ["evaluation", "evaluation / edd", "eval", "edd"],
    "behavior_spec": ["behavior spec", "behavior spec (sesf)", "sesf", "behavior"],
    "validation_checklist": ["validation checklist", "checklist"],
}
```

### Stage 2: Section Tree → ReixsSpec

Map parsed sections into Pydantic models. Type coercion and initial structural errors surface here as Pydantic ValidationErrors.

### SESF Extraction

- Find all fenced code blocks with language tag `sesf`
- Concatenate if multiple blocks exist
- Write to temp file for vendored validator
- Return both raw text and temp file path

## 6. Validator Design (5-Pass)

Each pass returns `list[Finding]`:

```python
class Finding(BaseModel):
    pass_number: int
    severity: Literal["error", "warning", "info"]
    section: str | None
    field: str | None
    message: str
    suggestion: str | None
```

### Pass 1 — Structural

- All 10 required sections present
- Meta fields present and valid (spec_id, version as semver, tier as enum)
- No duplicate required sections
- Version format: `^\d+\.\d+\.\d+$`

### Pass 2 — OFD

- 5 mandatory fields present for all tiers
- 5 additional fields: warn for micro if missing, error for standard/complex
- hard_constraints and autofail_conditions non-empty
- optimization_priority_order contains factual accuracy concept (heuristic)

### Pass 3 — Domain

- task_type in known registry
- Jurisdiction declared in domain_context
- DDD reference present, matches format `re-ddd:<name>@<semver>`
- DDD reference exists in local registry
- Output contract mentions provenance / fact-inference requirement
- EDD suite ID present for standard/complex tiers

### Pass 4 — SESF

- At least one `sesf` fenced block exists
- Write block to temp file, call `parse_sesf()` from vendored validator
- Run `check_structural_completeness()`, `check_error_consistency()`, `check_example_consistency()`
- Map each SESF `ValidationResult` → REIXS `Finding`
- SESF FAIL → REIXS error (controlled by `--strict-sesf`, default ON)

### Pass 5 — Cross-field

- If task_type = lease_abstraction → output contract must include normalized lease terms
- If tier = complex → ADR references required
- If OFD hard constraints mention "provenance" → output contract must enforce provenance fields
- If jurisdiction is Ontario → currency/unit fields should be present

### Validation Report

```python
class ValidationReport(BaseModel):
    status: Literal["pass", "warn", "fail"]
    spec_id: str
    spec_version: str
    findings: list[Finding]
    pass_summaries: dict[int, PassSummary]
    sesf_findings: list[dict]
```

Output as CLI (Rich-formatted) and JSON (`validation_report.json`).

## 7. Compiler Design

Takes validated `ReixsSpec`, produces:

1. **`reixs.runtime.json`** — Normalized runtime payload for downstream agents
2. **`reixs.manifest.json`** — Metadata envelope (spec_id, source_hash, compile_timestamp, artifacts)
3. **`reixs.validation.json`** (optional) — Full validation report

Refuses to compile if validation status is `fail`. Compiles with warnings and includes them in manifest.

## 8. CLI Design

```bash
reixs validate <spec.md>                    # validate, CLI output
reixs validate <spec.md> --json             # validate, JSON output
reixs validate <spec.md> --no-strict-sesf   # SESF failures as warnings
reixs compile <spec.md> -o <dir>            # validate + compile
reixs compile <spec.md> -o <dir> --include-validation
reixs init --template lease-abstraction-ontario -o my_spec.reixs.md
reixs init --list-templates
```

Exit codes: `0` success, `1` validation failure, `2` parse error, `3` SESF failure.

## 9. Testing Strategy

| Test file | Coverage |
|---|---|
| `test_parser.py` | Heading detection, alias mapping, SESF extraction, key-value parsing, malformed inputs |
| `test_validator.py` | Each pass independently, tier-specific field requirements, cross-field rules |
| `test_sesf_adapter.py` | SESF block → temp file → validation → Finding mapping |
| `test_compiler.py` | Valid spec → runtime JSON schema compliance, manifest fields, refuse-on-fail |
| `golden/` | Regression baselines for validation report and runtime payload JSON |

Invalid specs in `specs/invalid/` provide negative test cases: missing_ofd, missing_sesf, missing_ddd_ref, complex_no_adr.

## 10. Dependencies

| Package | Purpose | Type |
|---|---|---|
| `pydantic>=2.0` | Schema models, validation, JSON serialization | Runtime |
| `click>=8.0` | CLI framework | Runtime |
| `markdown-it-py>=3.0` | Markdown parsing / AST | Runtime |
| `rich>=13.0` | CLI formatting (colored output, tables) | Runtime |
| `pytest>=8.0` | Testing | Dev |
| `pytest-cov` | Coverage | Dev |

Vendored: `validate_sesf.py` from `cc-plugins/structured-english` (zero external deps).

## 11. Day 1 Success Criteria

- `reixs validate <valid-template>` returns pass
- `reixs validate <invalid-template>` fails with actionable errors (3+ failure modes)
- `reixs compile` emits `reixs.runtime.json` and `reixs.manifest.json`
- SESF block extraction + real validation works
- `reixs init --template lease-abstraction-ontario` scaffolds a valid spec
- All tests pass locally
- README explains usage in under 5 minutes
- ADR-001 and ADR-003 exist

## 12. What This Design Does NOT Cover (Day 2+)

- EDD fixture runner / `reixs eval` command
- Multi-task support (market rent opinion, comp screening)
- Jurisdiction modules beyond Ontario
- DDD registry expansion
- SESF transpilation to executable policy graph
- Agent runtime integration
- CI pipeline with regression gates
