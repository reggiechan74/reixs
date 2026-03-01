# REIXS Format Specification

> Version 0.1.0 — derived from REIXS v0.1.0 source code

## 1. Introduction

A **REIXS spec** (`.reixs.md` file) is a Markdown document that defines exactly how an AI agent executes a real estate task. It captures the objective, domain context, hard constraints, behavioral rules, evaluation criteria, and output requirements in a single file that is both human-readable and machine-validatable.

The REIXS toolchain parses the Markdown into a typed data model, validates it across five independent passes, and compiles it into runtime JSON that downstream agents consume. The spec file is the single source of truth — the toolchain enforces it, but never invents rules beyond what the spec declares.

### Audience

This document serves two audiences:

- **Spec authors** write `.reixs.md` files. They need to know which sections are required, what syntax the parser expects, and what validation rules will be enforced. Sections 2 through 5 are primarily for this audience.

- **Agent developers** consume the compiled runtime JSON that the REIXS toolchain produces from a validated spec. They need to understand the structure of the source format so they can trace runtime fields back to their spec-level origin. Section 6 (Compiled Output Schema, in a future revision) is primarily for this audience, but the full spec structure is relevant for debugging and provenance.

### Relationship to other documents

| Document | Purpose |
|---|---|
| `README.md` | Tool overview — installation, CLI commands, pipeline diagram, quick start |
| `REIXS-SPEC.md` (this file) | Format reference — every section, field, syntax rule, and validation constraint for `.reixs.md` files |
| `TUTORIAL.md` | Hands-on walkthrough — write, validate, and compile a spec from scratch |

The README tells you *what REIXS does*. This document tells you *how to write a valid spec*. The tutorial walks you through doing it for the first time.

## 2. File Structure Overview

A `.reixs.md` file is a standard Markdown document with a defined heading structure. The parser (built on markdown-it-py) walks the AST to extract sections, key-value pairs, lists, sub-headings, and fenced code blocks. No YAML front matter is used — all metadata lives inside the `## Meta` section.

### 2.1 Title line

The file starts with a single H1 heading. This is a free-form title — the parser does not validate its content. Convention is to prefix it with `REIXS:` followed by a descriptive name:

```markdown
# REIXS: Lease Abstraction — Ontario Commercial
```

### 2.2 The 10 mandatory sections

Every REIXS spec contains exactly 10 H2-level sections. Each section maps to a canonical name used internally by the parser and compiler. The conventional authoring order is:

| # | Heading (conventional) | Canonical name | Purpose |
|---|---|---|---|
| 1 | `## Meta` | `meta` | Spec ID, version, tier, author, date |
| 2 | `## Objective` | `objective` | One sentence: what this task accomplishes |
| 3 | `## Domain Context` | `domain_context` | Jurisdiction, currency, DDD reference |
| 4 | `## Inputs` | `inputs` | What goes into the task |
| 5 | `## Objective Function Design (OFD)` | `ofd` | Hard constraints, priorities, failure conditions |
| 6 | `## Constraints` | `constraints` | Operational limits (time, format, connectivity) |
| 7 | `## Output Contract` | `output_contract` | What comes out, with field-level requirements |
| 8 | `## Evaluation / EDD` | `evaluation` | How to test the output |
| 9 | `## Behavior Spec (SESF)` | `behavior_spec` | Machine-parseable behavioral rules (SESF v3) |
| 10 | `## Validation Checklist` | `validation_checklist` | Self-audit items for spec authors |

**Section order is not enforced.** The parser matches sections by heading text (using an alias lookup table), not by position. You may arrange sections in any order, though the conventional order above is recommended for readability.

**All 10 sections are mandatory.** Validation Pass 1 (structural) reports an error for any missing section.

### 2.3 Heading aliases

Each section can be written with multiple heading variations. The parser normalizes headings by lowercasing and stripping Markdown formatting characters (`#`, `*`, `_`, `` ` ``), then looks up the result in an alias table. For example, all of these resolve to the `behavior_spec` section:

```markdown
## Behavior Spec
## Behavior Spec (SESF)
## SESF
## Behavior
```

The complete alias table (derived from `SECTION_ALIASES` in the parser source):

| Canonical name | Accepted headings |
|---|---|
| `meta` | Meta |
| `objective` | Objective |
| `domain_context` | Domain Context, Domain |
| `inputs` | Inputs, Input |
| `ofd` | Objective Function Design, Objective Function Design (OFD), OFD |
| `constraints` | Constraints |
| `output_contract` | Output Contract |
| `evaluation` | Evaluation, Evaluation / EDD, Eval, EDD |
| `behavior_spec` | Behavior Spec, Behavior Spec (SESF), SESF, Behavior |
| `validation_checklist` | Validation Checklist, Checklist |

Alias matching is case-insensitive.

### 2.4 H3 subsections

Within any H2 section, H3 headings create named subsections. The heading text is normalized to `snake_case` (spaces and hyphens replaced with underscores, lowercased). Content under a subsection is associated with that subsection key in the parsed output.

H3 subsections are most commonly used in the **OFD** section, which defines up to 10 sub-sections:

```markdown
## Objective Function Design (OFD)

### Primary Objective
Extract all lease terms defined in DDD with factual accuracy >= 98%.

### Hard Constraints
- NEVER fabricate a term not present in the source document
- ALL extracted values MUST carry provenance

### Uncertainty Policy
When a term is ambiguous, mark as INFERENCE with confidence score.
```

### 2.5 Key-value bullet syntax

Bullet lists where each item follows the pattern `Key: Value` are parsed into key-value dictionaries. The parser applies a regex (`^([^:]+):\s*(.+)$`) to each bullet item — if it matches, the key is normalized to `snake_case` and the value is stored as a string.

```markdown
## Meta

- Spec ID: REIXS-LA-ON-001
- Version: 1.0.0
- Task Type: Lease Abstraction
- Tier: standard
- Author: Reggie Chan
- Date: 2026-03-01
```

The above parses to:

```json
{
  "spec_id": "REIXS-LA-ON-001",
  "version": "1.0.0",
  "task_type": "Lease Abstraction",
  "tier": "standard",
  "author": "Reggie Chan",
  "date": "2026-03-01"
}
```

Key normalization rules: the key portion (everything before the first colon) is lowercased, and spaces and hyphens are replaced with underscores. The value portion (everything after the colon and whitespace) is kept as-is.

Bullet items that do not match the `Key: Value` pattern are stored as plain list items.

### 2.6 Fenced code blocks

Fenced code blocks are extracted with their language tag. The most important use is the `sesf` language tag in the Behavior Spec section:

````markdown
## Behavior Spec (SESF)

```sesf
Lease Term Extraction Rules

Meta: Version 1.0.0 | Date: 2026-03-01 | Domain: Lease Abstraction | Status: active | Tier: micro

BEHAVIOR extract_lease_terms: Extract and classify lease terms
  RULE verbatim_extraction:
    WHEN a field value is found verbatim in the source document
    THEN status MUST be FACT
```
````

The parser stores each code block as `{"lang": "<tag>", "content": "<text>"}`. The SESF validator (Pass 4) specifically looks for blocks with `lang: "sesf"`.

### 2.7 Checkbox lists

The Validation Checklist section uses Markdown checkbox syntax. During parsing, the checkbox markers (`[ ]` and `[x]`) are stripped, leaving only the item text:

```markdown
## Validation Checklist

- [ ] All DDD-defined fields addressed in output contract
- [ ] Hard constraints are machine-checkable
- [ ] SESF rules cover extraction, conflict, and missing-value scenarios
```

This parses to a flat list of strings:

```json
[
  "All DDD-defined fields addressed in output contract",
  "Hard constraints are machine-checkable",
  "SESF rules cover extraction, conflict, and missing-value scenarios"
]
```

### 2.8 Paragraphs and free text

Sections that contain paragraph text (not bullet lists, not code blocks) are stored as strings. If a section contains only free text, it is stored directly as a string value. The **Objective** section is the most common example:

```markdown
## Objective

Extract structured lease terms from a commercial lease document (Ontario jurisdiction)
and produce a normalized term sheet with field-level provenance.
```

If a section contains both free text and other content (bullet lists, subsections), the text is stored under a `_text` key in the section dictionary.

## 3. Section Reference

This section documents every REIXS section in detail: accepted heading aliases, format expectations, field-level validation rules, and examples. Validation rules reference the pass that enforces them (Pass 1 = structural, Pass 3 = domain, Pass 5 = cross-field).

### 3.1 Meta

**Canonical name:** `meta`
**Heading aliases:** `Meta`

The Meta section declares spec-level metadata as a bullet list of `Key: Value` pairs. All six fields are required.

#### Fields

| Field | Required | Format | Validation |
|---|---|---|---|
| Spec ID | Yes | Non-empty string. Convention: `REIXS-TYPE-JURISDICTION-SEQ` (e.g., `REIXS-LA-ON-001`) | Pass 1 error if empty |
| Version | Yes | Semantic version `X.Y.Z` — must match `^\d+\.\d+\.\d+$` | Pass 1 error if not valid semver |
| Task Type | Yes | Non-empty string | Pass 1 error if empty. Pass 3 warning if not in known task type registry |
| Tier | Yes | One of: `micro`, `standard`, `complex` | Defaults to `standard` if value is unrecognized (no error emitted) |
| Author | Yes | Non-empty string | No validation beyond presence in the data model |
| Date | Yes | ISO 8601 date `YYYY-MM-DD` | Coerced to `2000-01-01` if unparseable (no error emitted) |

**Known task types (v0.1.0):** `Lease Abstraction`

#### Example

```markdown
## Meta

- Spec ID: REIXS-LA-ON-001
- Version: 1.0.0
- Task Type: Lease Abstraction
- Tier: standard
- Author: Reggie Chan
- Date: 2026-03-01
```

#### Notes

- The parser normalizes keys to `snake_case` before mapping to the data model. `Spec ID` becomes `spec_id`, `Task Type` becomes `task_type`, etc.
- Tier matching is case-insensitive and whitespace-trimmed. `Standard`, `STANDARD`, and `standard` all resolve to the `standard` tier.
- The task type registry is checked case-insensitively. `Lease Abstraction` and `lease abstraction` both match.

### 3.2 Objective

**Canonical name:** `objective`
**Heading aliases:** `Objective`

The Objective section is a free-text paragraph describing what this spec accomplishes. It must be non-empty.

#### Fields

This section has no key-value fields. The entire content is stored as a single string.

| Constraint | Validation |
|---|---|
| Non-empty text | Pass 1 error if the section is empty |

#### Example

```markdown
## Objective

Extract structured lease terms from a commercial lease document (Ontario jurisdiction)
and produce a normalized term sheet with field-level provenance.
```

#### Notes

- If the section contains both paragraph text and other elements (bullet lists, code blocks), only the paragraph text is extracted. In practice, keep this section to one or two plain sentences.

### 3.3 Domain Context

**Canonical name:** `domain_context`
**Heading aliases:** `Domain Context`, `Domain`

The Domain Context section declares the jurisdictional and domain framework for the task. It uses `Key: Value` bullet syntax.

#### Fields

| Field | Required | Format | Validation |
|---|---|---|---|
| Jurisdiction | Yes | Free text (e.g., `Ontario, Canada`) | Pass 3 error if empty |
| Currency | No | Currency code (e.g., `CAD`) | Pass 5 warning if jurisdiction contains "Ontario" and currency is not declared |
| Area Unit | No | Unit string (e.g., `sq ft`) | No validation |
| DDD Reference | Yes | `re-ddd:<name>@X.Y.Z` — must match `^re-ddd:[\w_]+@\d+\.\d+\.\d+$` | Pass 3 error if missing. Pass 3 error if present but invalid format. Pass 3 warning if valid format but not in known registry |
| ADR References | No | Comma-separated list (e.g., `ADR-001, ADR-003`) — parsed into an array | Pass 5 error if tier is `complex` and ADR references are absent |

**Known jurisdictions (v0.1.0):** `Ontario, Canada`, `Ontario`
**Known DDD refs (v0.1.0):** `re-ddd:lease_core_terms_ontario@0.1.0`

#### Example

```markdown
## Domain Context

- Jurisdiction: Ontario, Canada
- Currency: CAD
- Area Unit: sq ft
- DDD Reference: re-ddd:lease_core_terms_ontario@0.1.0
- ADR References: ADR-001, ADR-003
```

#### Notes

- The DDD Reference field follows a three-level validation cascade: (1) presence check, (2) format regex, (3) registry lookup. Each level is only reached if the previous level passes.
- ADR References are split on commas and trimmed. The string `ADR-001, ADR-003` becomes the array `["ADR-001", "ADR-003"]`.
- The Ontario currency warning is a cross-field check — it fires only when jurisdiction contains "Ontario" (case-insensitive) and no currency is declared. It is a warning, not an error.
- Known jurisdictions include both `Ontario, Canada` and `Ontario` (matched case-insensitively). Unrecognized jurisdictions are accepted without warning — the registry is advisory, not restrictive.

### 3.4 Inputs

**Canonical name:** `inputs`
**Heading aliases:** `Inputs`, `Input`

The Inputs section lists what goes into the task as a bullet list of `Key: Value` pairs. The content is domain-specific and has no required fields.

#### Fields

No fields are required. Each bullet item is parsed as a key-value pair using the standard `Key: Value` pattern. Items that do not match are stored as plain list entries.

| Constraint | Validation |
|---|---|
| (none) | No structural, domain, or cross-field validation |

#### Example

```markdown
## Inputs

- Source Document: PDF (scanned or native)
- Document Type: Commercial lease agreement
- Expected Page Count: 10-50
```

#### Notes

- The parser produces a list of `{"key": ..., "value": ...}` objects. Bullet items without a colon separator are stored with the full text as the key and an empty string as the value.
- This section is intentionally unconstrained. The spec author defines whatever inputs are relevant for the task. Downstream agents use the compiled input list to understand what they will receive at runtime.

### 3.5 Objective Function Design (OFD)

**Canonical name:** `ofd`
**Heading aliases:** `Objective Function Design`, `Objective Function Design (OFD)`, `OFD`

The OFD section is the heart of a REIXS spec. It defines what the agent optimizes for, what it must never do, how it handles uncertainty, and how outputs are scored. The section uses H3 subsections — up to 10 — each with its own format and validation rules. Five subsections are mandatory for all tiers; five are tier-dependent.

All OFD validation runs in **Pass 2** (OFD validation).

#### 3.5.1 Mandatory sub-sections (all tiers)

These five sub-sections are required regardless of tier. A missing or empty sub-section produces a **Pass 2 error**.

| Sub-Section | H3 Heading | Format | Validation |
|---|---|---|---|
| Primary Objective | `### Primary Objective` | Paragraph (free text) | Pass 2 error if empty |
| Hard Constraints | `### Hard Constraints` | Bullet list | Pass 2 error if empty list |
| AutoFail Conditions | `### AutoFail Conditions` | Bullet list | Pass 2 error if empty list |
| Optimization Priority Order | `### Optimization Priority Order` | Ordered list | Pass 2 error if empty list. Pass 2 warning if the combined text does not contain "factual", "accuracy", or "correct" |
| Uncertainty Policy | `### Uncertainty Policy` | Paragraph (free text) | Pass 2 error if empty |

**Primary Objective** is stored as a string (paragraph text under the H3 heading). It declares the single overarching goal of the spec.

**Hard Constraints** is a bullet list of absolute rules the agent must never violate. Each bullet is stored as a plain string.

**AutoFail Conditions** is a bullet list of conditions that cause automatic failure. Each bullet is stored as a plain string.

**Optimization Priority Order** is an ordered (numbered) list declaring which qualities the agent should prioritize, in rank order. The parser extracts ordered list items into a `list[str]`. A heuristic check warns if the combined text of all priorities does not mention "factual", "accuracy", or "correct" — this is a warning, not an error, and is intended to remind spec authors to include factual correctness as a priority.

**Uncertainty Policy** is stored as a string (paragraph text). It defines how the agent should behave when inputs are ambiguous, incomplete, or contradictory.

#### 3.5.2 Tier-dependent sub-sections

These five sub-sections have severity that varies by tier. The logic is:

- **standard** or **complex** tier: missing sub-section is a **Pass 2 error**
- **micro** tier: missing sub-section is a **Pass 2 info** (informational, does not block validation)

| Sub-Section | H3 Heading | Format | micro | standard | complex |
|---|---|---|---|---|---|
| Secondary Objectives | `### Secondary Objectives` | Bullet list | info | error | error |
| Tradeoff Policies | `### Tradeoff Policies` | Bullet list | info | error | error |
| Scoring Model | `### Scoring Model` | Bullet list (special) | info | error | error |
| Escalation Triggers | `### Escalation Triggers` | Bullet list | info | error | error |
| Error Severity Model | `### Error Severity Model` | Bullet list (special) | info | error | error |

**Secondary Objectives** is a bullet list of goals that complement the primary objective. Each bullet is stored as a plain string.

**Tradeoff Policies** is a bullet list defining how the agent should resolve conflicts between competing objectives or constraints.

**Scoring Model** uses bullet list syntax, but the parser joins all bullet items into a single string with newline separators (see `section_model.py:_build_scoring_model`). The result is stored as `str | dict | None` in the data model, though the most common case is a newline-joined string. This allows spec authors to describe a scoring rubric as a multi-line block without requiring structured key-value format.

**Escalation Triggers** is a bullet list of conditions that should cause the agent to stop and escalate to a human reviewer rather than proceeding autonomously.

**Error Severity Model** uses a special bullet list format. Each bullet must follow the pattern:

```
- severity: error_type_1, error_type_2, ...
```

The parser splits each bullet on the first `:` to extract the severity level, then splits the remainder on `,` to extract individual error types. The result is a dictionary mapping severity levels to lists of error types:

```json
{
  "critical": ["fabricated term", "wrong currency", "wrong dates"],
  "high": ["missing critical field without flag", "provenance gap"],
  "medium": ["formatting inconsistency"],
  "low": ["minor style deviation"]
}
```

This is the only sub-section in OFD with structured parsing beyond plain string/list extraction.

#### Data model

The parsed OFD section maps to the following Pydantic model:

```python
class OFDSection(BaseModel):
    primary_objective: str
    hard_constraints: list[str]
    autofail_conditions: list[str]
    optimization_priority_order: list[str]
    uncertainty_policy: str
    secondary_objectives: list[str] | None = None
    tradeoff_policies: list[str] | None = None
    scoring_model: str | dict | None = None
    escalation_triggers: list[str] | None = None
    error_severity_model: dict[str, list[str]] | None = None
```

Fields that are `None` indicate the sub-section was not present in the spec. This is distinct from an empty list or empty string, which indicates the sub-section heading was present but had no content.

#### Example

A complete OFD section showing all 10 sub-sections:

```markdown
## Objective Function Design (OFD)

### Primary Objective
Extract all lease terms defined in the DDD with factual accuracy >= 98%,
producing a normalized term sheet suitable for portfolio analysis.

### Hard Constraints
- NEVER fabricate a term not present in the source document
- ALL extracted values MUST carry provenance (page, paragraph, or clause reference)
- Currency values MUST use CAD unless the source explicitly states otherwise
- Date values MUST use ISO 8601 format (YYYY-MM-DD)

### AutoFail Conditions
- Any fabricated lease term (value not traceable to source)
- Missing provenance on a critical field (rent, term, tenant name)
- Wrong currency assignment on a financial term
- Misidentified parties (landlord/tenant swapped)

### Optimization Priority Order
1. Factual correctness — no fabricated or hallucinated values
2. Completeness — extract every DDD-defined field present in the source
3. Provenance quality — every value traceable to a specific location
4. Normalization consistency — dates, currencies, and units in standard format
5. Confidence calibration — uncertainty scores reflect actual ambiguity

### Uncertainty Policy
When a term is ambiguous or not explicitly stated, mark the field status as
INFERENCE with a confidence score between 0.0 and 1.0. If confidence is below
0.5, additionally flag the field for human review. Never guess — if the value
cannot be reasonably inferred, mark as NOT_FOUND rather than fabricating.

### Secondary Objectives
- Minimize human review burden by providing clear provenance
- Maintain consistent formatting across all extracted fields
- Flag potential lease anomalies (e.g., unusual escalation clauses)

### Tradeoff Policies
- When completeness conflicts with accuracy, prefer accuracy (skip the field rather than guess)
- When normalization conflicts with source fidelity, preserve the source value and add a normalized alternative
- When confidence is borderline (0.4-0.6), flag for review rather than committing to FACT or NOT_FOUND

### Scoring Model
- Factual accuracy: 40% weight — percentage of extracted values that are correct
- Completeness: 25% weight — percentage of DDD fields successfully extracted
- Provenance coverage: 20% weight — percentage of values with valid source references
- Normalization: 10% weight — percentage of values in standard format
- Confidence calibration: 5% weight — correlation between confidence scores and actual accuracy

### Escalation Triggers
- Document appears to be in a language other than English or French
- More than 30% of DDD-defined fields are NOT_FOUND
- Document page count exceeds 200 pages
- Multiple conflicting values found for the same field with no clear resolution

### Error Severity Model
- critical: fabricated term, wrong currency, wrong dates, misidentified parties
- high: missing critical field without flag, provenance gap on financial term
- medium: formatting inconsistency, low-confidence value not flagged for review
- low: minor style deviation, optional field not extracted
```

#### Notes

- H3 heading text is normalized to `snake_case` for the subsection key. `### Primary Objective` becomes `primary_objective`, `### AutoFail Conditions` becomes `autofail_conditions`, etc.
- The Optimization Priority Order uses an ordered (numbered) Markdown list. The parser strips the leading number and period from each item. Using a bullet list instead will still work (items are stored as strings either way), but an ordered list is recommended to make rank order explicit.
- The "factual/accuracy/correct" heuristic check on Optimization Priority Order is case-insensitive. It joins all list items, lowercases the result, and checks for substring matches. The warning is advisory — it does not prevent validation from passing.
- For micro-tier specs, the five tier-dependent sub-sections can be omitted entirely without affecting validation outcome (info-level findings do not block validation). This allows lightweight specs to focus on the five mandatory sub-sections.
- The Error Severity Model parser is lenient: it strips leading `-` and whitespace from each line before splitting on `:`. Severity levels are not constrained to a fixed set — the spec author defines whatever levels are appropriate (though `critical`, `high`, `medium`, `low` is the conventional set).

### 3.6 Constraints

**Canonical name:** `constraints`
**Heading aliases:** `Constraints`

The Constraints section lists operational limits on how the task executes — time budgets, format restrictions, connectivity requirements, and similar boundaries. It uses a bullet list.

#### Format

Each bullet is stored as a plain string. Bullets that follow the `Key: Value` pattern are accepted and preserved — the parser treats items like `Processing time: < 120 seconds` as key-value pairs, but the section model reconstructs them back into `"key: value"` strings (see `_build_constraints` in `section_model.py`). The net effect is that both plain bullets and key-value bullets appear identically in the compiled output: a flat list of strings.

#### Data model

```python
class ConstraintsSection(BaseModel):
    items: list[str]
```

#### Validation

No structural, domain, or cross-field validation rules apply to this section. It has no required fields and no content checks.

| Constraint | Validation |
|---|---|
| (none) | No validation |

#### Example

```markdown
## Constraints

- Processing time: < 120 seconds per document
- Output format: JSON
- No external API calls during extraction
- Maximum input size: 200 pages
```

#### Notes

- The section model's `_build_constraints` function handles three input shapes: (1) a dict with key-value pairs from the parser — keys and values are re-joined as `"key: value"` strings; (2) a dict with an `_items` key containing plain bullet strings — items are included directly; (3) a plain list of strings — passed through as-is.
- Because key-value bullets are reconstructed into plain strings, the compiled output does not distinguish between `Processing time: < 120 seconds` (parsed as k/v) and `No external API calls during extraction` (parsed as plain text). Both appear as flat string items.

### 3.7 Output Contract

**Canonical name:** `output_contract`
**Heading aliases:** `Output Contract`

The Output Contract section defines what the task produces. It consists of a description paragraph followed by field definitions using backtick-wrapped names in `Key: Value` bullet syntax.

#### Format

The section typically contains:

1. A **description paragraph** — free text explaining the output structure and requirements.
2. A **field definition list** — bullets where the key is a backtick-wrapped field name (e.g., `` `value` ``) and the value describes that field.

The parser stores the paragraph under `_text` and the key-value bullets as regular dict entries. The section model (`_build_output_contract`) strips backticks from field names when constructing the `OutputContractSection`.

#### Data model

```python
class OutputContractSection(BaseModel):
    description: str
    fields: list[dict[str, str]]  # [{"name": "...", "description": "..."}, ...]
```

- `description` holds the paragraph text (from `_text`).
- `fields` is a list of `{"name": ..., "description": ...}` dicts, one per backtick-wrapped field definition. The backticks are stripped from the name.

#### Validation

| Rule | Pass | Severity | Condition |
|---|---|---|---|
| Provenance/status mention | Pass 3 (Domain) | warning | Description does not contain "provenance" or "status" (case-insensitive) |
| Provenance consistency | Pass 5 (Cross-field) | warning | OFD Hard Constraints mention "provenance" but the output contract description does not |

The Pass 3 check (`validate/domain.py:54-61`) lowercases the description and checks for substring matches against both `"provenance"` and `"status"`. If neither is found, a warning is emitted suggesting the author include provenance and fact/inference status.

The Pass 5 check (`validate/cross_field.py:24-32`) joins all OFD hard constraint strings, lowercases them, and checks for `"provenance"`. If found, it then checks the output contract description for the same substring. A warning fires if the hard constraints mention provenance but the output contract does not — indicating a potential gap between what is required and what is delivered.

#### Example

```markdown
## Output Contract

Each extracted field MUST include the following attributes:

- `value`: the extracted or derived value
- `status`: one of FACT, INFERENCE, NOT_FOUND
- `confidence`: float 0.0-1.0 (1.0 for FACT)
- `provenance`: page and clause reference from source document
- `notes`: optional free-text annotation
```

#### Notes

- The backtick-stripping logic uses Python's `str.strip("`")`. Field names like `` `value` `` become `value` in the compiled output.
- Only the `description` (paragraph text) is checked by validation. Field definitions are not individually validated.
- The provenance/status warning is advisory — it does not prevent validation from passing. It is a reminder that real estate extraction specs typically need provenance tracking.

### 3.8 Evaluation / EDD

**Canonical name:** `evaluation`
**Heading aliases:** `Evaluation`, `Evaluation / EDD`, `Eval`, `EDD`

The Evaluation section defines how the task output is tested. It uses `Key: Value` bullet syntax for structured fields, with an optional comma-separated list for regression cases.

#### Fields

| Field | Key in Markdown | Required | Format | Validation |
|---|---|---|---|---|
| EDD Suite ID | `EDD Suite ID` | Tier-dependent | Non-empty string | Pass 3 error if empty and tier is `standard` or `complex` |
| Minimum pass rate | `Minimum pass rate` | No | Free text (e.g., `95%`) | No validation |
| Zero tolerance | `Zero tolerance` | No | Free text | No validation |
| Regression cases | `Regression cases` | No | Comma-separated list | Parsed into `list[str]` |

The EDD Suite ID is the only field with a validation rule. The Pass 3 check (`validate/domain.py:63-71`) requires it for `standard` and `complex` tiers. For `micro` tier, it is optional.

#### Data model

```python
class EvaluationSection(BaseModel):
    edd_suite_id: str | None = None
    min_pass_rate: str | None = None
    zero_tolerance: str | None = None
    regression_cases: list[str] = []
    raw_text: str = ""
```

The `raw_text` field stores a reconstructed `"key: value"` representation of all non-internal fields, joined with newlines. This provides a fallback for sections that are written as free text rather than structured key-value bullets.

#### Parsing details

- The `regression_cases` field is parsed from a comma-separated string. The value `"case-001, case-002, case-003"` becomes `["case-001", "case-002", "case-003"]`.
- The parser also accepts `min_pass_rate` as an alias for `minimum_pass_rate` (the section model checks both keys).
- If the entire section is written as free text (a paragraph rather than bullets), the model stores it in `raw_text` with all structured fields set to `None`.

#### Validation

| Rule | Pass | Severity | Condition |
|---|---|---|---|
| EDD Suite ID required | Pass 3 (Domain) | error | Tier is `standard` or `complex` and `edd_suite_id` is empty or absent |

#### Example

```markdown
## Evaluation / EDD

- EDD Suite ID: EDD-LA-ON-001
- Minimum pass rate: 95%
- Zero tolerance: fabricated term, wrong currency
- Regression cases: case-001, case-002, case-003
```

#### Notes

- The `micro` tier exempts the EDD Suite ID requirement entirely — no error, no warning.
- The `raw_text` field exists because the parser cannot distinguish between a section that was intentionally written as free text and one where the author forgot to use bullet syntax. The raw text provides a safety net for downstream consumers.

### 3.9 Behavior Spec (SESF)

**Canonical name:** `behavior_spec`
**Heading aliases:** `Behavior Spec`, `Behavior Spec (SESF)`, `SESF`, `Behavior`

The Behavior Spec section contains machine-parseable behavioral rules written in the Structured English Specification Format (SESF) v3. The SESF block must appear inside a fenced code block with the language tag `sesf`.

#### Format

The section must contain at least one fenced code block with `lang: "sesf"`. The parser's SESF extractor (`parser/sesf_extractor.py:6-16`) looks specifically in the `behavior_spec` section for code blocks tagged `sesf` and returns their raw text content.

````markdown
## Behavior Spec (SESF)

```sesf
Title Line

Meta: Version 1.0.0 | Date: 2026-03-01 | Domain: Lease Abstraction | Status: active | Tier: micro

BEHAVIOR extract_terms: Extract and classify lease terms
  RULE verbatim_extraction:
    WHEN a field value is found verbatim in the source document
    THEN status MUST be FACT
```
````

If multiple `sesf` code blocks are present, their contents are joined with double newlines (`\n\n`) into a single `raw_sesf` string.

#### Data model

```python
class BehaviorSpecSection(BaseModel):
    raw_sesf: str
    sesf_blocks: list[str]  # individual block contents
```

#### Validation (Pass 4 — SESF)

SESF validation runs as Pass 4 in the pipeline. The adapter (`sesf/adapter.py`) performs a multi-stage check:

| Rule | Severity | Condition |
|---|---|---|
| Empty SESF block | error | `raw_sesf` is empty or whitespace-only |
| Missing Meta line | error | SESF block parses but contains no `Meta:` line |
| Structural/consistency failures | error (or warning with `--no-strict-sesf`) | SESF internal validation detects structural incompleteness, error inconsistency, or example inconsistency |

**Empty SESF block** (`sesf/adapter.py:26-35`): If the `raw_sesf` text is empty or whitespace-only, a Pass 4 error is emitted immediately and no further SESF checks run.

**Missing Meta line** (`sesf/adapter.py:58-66`): If the SESF parser finds no `Meta` section in the block, a Pass 4 error is emitted with a suggestion to add the Meta line.

**Structural/consistency failures**: If the Meta line is present, the adapter runs three SESF validation checks — structural completeness, error consistency, and example consistency. Each SESF `FAIL` result maps to a REIXS `error`; each `WARN` maps to a `warning`; each `PASS` maps to `info`.

**The `--no-strict-sesf` flag**: When passed on the CLI, all SESF errors are downgraded to warnings. This is implemented in the validation runner (`validate/__init__.py:38-43`) — if `strict_sesf` is `False`, any finding with `severity == "error"` from the SESF pass is changed to `"warning"` before being added to the report. This allows compilation to proceed despite SESF issues during early spec development.

#### SESF v3 Quick Reference

The SESF block uses a domain-specific language with these constructs:

| Construct | Syntax | Purpose |
|---|---|---|
| Meta | `Meta: Version X.Y.Z \| Date: YYYY-MM-DD \| Domain: ... \| Status: active \| Tier: micro` | Document metadata (required) |
| BEHAVIOR | `BEHAVIOR name: description` | Named behavior declaration |
| RULE | `RULE name:` then `WHEN` / `THEN` / `AND` clauses | Conditional rule within a behavior |
| ERROR | `ERROR name:` then `WHEN` / `SEVERITY` / `ACTION` / `MESSAGE` clauses | Error handling rule |
| EXAMPLE | `EXAMPLE name:` then `INPUT:` / `EXPECTED:` / `NOTES:` | Test example for validation |
| Constraints | `Constraints` header then `* item` bullets | Operational constraints within SESF |

For the full SESF v3 specification, see: https://github.com/reggiechan74/cc-plugins/tree/main/structured-english

#### Minimal valid SESF block

````markdown
```sesf
Lease Term Extraction Rules

Meta: Version 1.0.0 | Date: 2026-03-01 | Domain: Lease Abstraction | Status: active | Tier: micro

BEHAVIOR extract_lease_terms: Extract and classify lease terms from source documents
  RULE verbatim_extraction:
    WHEN a field value is found verbatim in the source document
    THEN status MUST be FACT
    AND confidence MUST be 1.0
```
````

This block satisfies all Pass 4 checks: it is non-empty, contains a Meta line, and has at least one BEHAVIOR with a RULE.

#### Example (full section)

````markdown
## Behavior Spec (SESF)

```sesf
Lease Term Extraction Rules

Meta: Version 1.0.0 | Date: 2026-03-01 | Domain: Lease Abstraction | Status: active | Tier: micro

BEHAVIOR extract_lease_terms: Extract and classify lease terms from source documents
  RULE verbatim_extraction:
    WHEN a field value is found verbatim in the source document
    THEN status MUST be FACT
    AND confidence MUST be 1.0

  RULE inferred_value:
    WHEN a field value is derived through inference
    THEN status MUST be INFERENCE
    AND confidence MUST be between 0.0 and 1.0

  ERROR missing_critical_field:
    WHEN a DDD-required field is not found in the source
    SEVERITY high
    ACTION flag for human review
    MESSAGE "Required field {field_name} not found in source document"

EXAMPLE basic_extraction:
  INPUT: "The annual base rent is $50,000 CAD"
  EXPECTED: value=$50,000, status=FACT, confidence=1.0, provenance=page 3 clause 4.1
  NOTES: Direct extraction — no inference needed
```
````

#### Notes

- The SESF extractor only looks for code blocks with the exact language tag `sesf`. Other language tags (e.g., `markdown`, `json`, `python`) in the Behavior Spec section are ignored.
- The `raw_sesf` field in the data model is the concatenation of all SESF blocks. If there is exactly one block (the typical case), `raw_sesf` equals that block's content directly.
- SESF validation is the only pass with a strict/lenient toggle. All other passes always enforce their rules at the declared severity level.

### 3.10 Validation Checklist

**Canonical name:** `validation_checklist`
**Heading aliases:** `Validation Checklist`, `Checklist`

The Validation Checklist section is a self-audit tool for spec authors. It uses Markdown checkbox syntax to list items the author should verify before finalizing the spec.

#### Format

Each item uses Markdown checkbox syntax: `- [ ] item text` (unchecked) or `- [x] item text` (checked). During parsing (`markdown_parser.py:124-126`), checkbox markers are stripped using the regex `^\[[ x]\]\s*`, leaving only the item text. The check state is not preserved — both `- [ ] item` and `- [x] item` produce the same output string.

#### Data model

The validation checklist is stored as a flat `list[str]` on the `ReixsSpec` model (not a dedicated section class):

```python
class ReixsSpec(BaseModel):
    ...
    validation_checklist: list[str]
```

#### Validation

| Rule | Pass | Severity | Condition |
|---|---|---|---|
| Empty checklist | Pass 1 (Structural) | warning | The checklist has zero items after parsing |

The Pass 1 check (`validate/structural.py:45-50`) warns if the checklist is empty. This is a warning, not an error — an empty checklist does not block validation.

#### Example

```markdown
## Validation Checklist

- [ ] All DDD-defined fields addressed in output contract
- [ ] Hard constraints are machine-checkable (no subjective language)
- [ ] SESF rules cover extraction, conflict, and missing-value scenarios
- [ ] Provenance requirements consistent between OFD and output contract
- [x] Error severity model covers all AutoFail conditions
```

#### Notes

- Checkbox state is intentionally discarded. The checklist serves as a prompt for the spec author during authoring, not as a runtime input. The compiled output contains only the item text.
- The parser applies checkbox stripping only in the `validation_checklist` section (gated by `current_section == "validation_checklist"` in the parser). Checkbox syntax in other sections is not stripped.
- The empty-checklist warning is one of the lightest validations in the pipeline. It exists to remind authors to include self-audit items, but does not prescribe what those items should be.
