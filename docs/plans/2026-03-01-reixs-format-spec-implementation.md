# REIXS Format Specification & Tutorial — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Write two documents — `docs/REIXS-SPEC.md` (authoritative format reference) and `docs/TUTORIAL.md` (hands-on walkthrough) — that close the authoring gap so anyone can write a valid `.reixs.md` file.

**Architecture:** Documentation-only tasks. Every rule documented must be derived from parser/validator source code, not invented. The spec reference mirrors the 10-section structure of a `.reixs.md` file. The tutorial uses a different domain (property valuation) to prevent copy-paste from the existing lease template.

**Tech Stack:** Markdown only. Validate accuracy by cross-referencing source files listed in the design doc's "Source of Truth" table.

---

### Task 1: REIXS-SPEC.md — Introduction + File Structure Overview

**Files:**
- Create: `docs/REIXS-SPEC.md`

**Context:** This is the first section of the authoritative format reference. It sets up what REIXS is and the overall file structure before diving into individual sections.

**Source files to reference:**
- `src/reixs/parser/markdown_parser.py:20-40` — `SECTION_ALIASES` dict (10 canonical section names)
- `src/reixs/parser/markdown_parser.py:90-112` — heading level detection (H1 ignored, H2 = sections, H3 = subsections)
- `src/reixs/parser/markdown_parser.py:254-264` — `_parse_kv` function (key-value bullet syntax)

**Step 1: Write sections 1-2 of REIXS-SPEC.md**

Write the following content to `docs/REIXS-SPEC.md`:

```markdown
# REIXS Format Specification

> Version 0.1.0 — derived from REIXS v0.1.0 source code

## 1. Introduction

A REIXS spec (`.reixs.md`) is a Markdown file that defines exactly how an AI agent should execute a real estate task — what it must do, what it must never do, and how to evaluate the output. This document is the authoritative reference for the `.reixs.md` format.

**Audience:**
- **Spec authors** writing `.reixs.md` files — see sections 2-3 for format rules and section 5 for validation rules
- **Agent developers** consuming compiled runtime JSON — see section 6 for the output schema

**Related documents:**
- [README](../README.md) — tool overview, CLI commands, architecture
- [Tutorial](TUTORIAL.md) — hands-on walkthrough for first-time authors

## 2. File Structure Overview

A `.reixs.md` file is a standard Markdown document with this structure:

```
# Title (free-form, not validated)

## Meta
(key-value bullet list)

## Objective
(paragraph)

## Domain Context
(key-value bullet list)

## Inputs
(key-value bullet list)

## Objective Function Design (OFD)
### Primary Objective
### Hard Constraints
### AutoFail Conditions
### Optimization Priority Order
### Uncertainty Policy
### Secondary Objectives
### Tradeoff Policies
### Scoring Model
### Escalation Triggers
### Error Severity Model

## Constraints
(bullet list)

## Output Contract
(paragraph + field definitions)

## Evaluation / EDD
(key-value bullet list)

## Behavior Spec (SESF)
(fenced code block with lang=sesf)

## Validation Checklist
(checkbox bullet list)
```

### Structural Rules

| Rule | Detail |
|---|---|
| **Title** | H1 heading. Free-form text, not validated. |
| **Sections** | H2 headings. All 10 sections are mandatory. |
| **Sub-sections** | H3 headings within OFD. Parsed as sub-keys. |
| **Key-value bullets** | `- Key: Value` syntax. Key is normalized to `snake_case`. |
| **Fenced code blocks** | Triple backticks with language tag (e.g., ` ```sesf `). |
| **Checkbox lists** | `- [ ] item` or `- [x] item`. Markers stripped during parsing. |

### Section Ordering

Sections can appear in any order — the parser matches by heading text, not position. However, the conventional order shown above is recommended for readability.
```

**Step 2: Verify accuracy**

Cross-check against source:
- Confirm 10 canonical names match `SECTION_ALIASES` keys in `parser/markdown_parser.py:20-40`
- Confirm H2/H3 behavior matches heading detection at `parser/markdown_parser.py:90-112`
- Confirm key-value syntax matches `_parse_kv` at `parser/markdown_parser.py:254-264`

**Step 3: Commit**

```bash
git add docs/REIXS-SPEC.md
git commit -m "docs: add REIXS-SPEC.md with introduction and file structure overview"
```

---

### Task 2: REIXS-SPEC.md — Section Reference (Meta, Objective, Domain Context, Inputs)

**Files:**
- Modify: `docs/REIXS-SPEC.md`

**Context:** First 4 sections of the 10-section reference. These are the simpler sections.

**Source files to reference:**
- `src/reixs/schema/reixs_models.py:13-19` — `MetaSection` fields
- `src/reixs/schema/enums.py:6-9` — `Tier` enum values
- `src/reixs/parser/section_model.py:62-87` — `_build_meta` (date coercion, tier coercion)
- `src/reixs/validate/structural.py:10-52` — semver regex, spec_id/task_type/objective checks
- `src/reixs/schema/reixs_models.py:22-28` — `DomainContextSection` fields
- `src/reixs/registry/ddd_refs.py:5` — DDD ref regex pattern
- `src/reixs/validate/domain.py:14-72` — jurisdiction, DDD ref validation
- `src/reixs/parser/markdown_parser.py:20-40` — heading aliases for each section

**Step 1: Append section reference for Meta, Objective, Domain Context, and Inputs**

Append the following to `docs/REIXS-SPEC.md`:

```markdown
## 3. Section Reference

### 3.1 Meta

**Heading aliases:** `Meta`

**Format:** Key-value bullet list.

| Field | Required | Format | Validation |
|---|---|---|---|
| `Spec ID` | Yes | Non-empty string | Pass 1 error if empty. Convention: `REIXS-<TYPE>-<JURISDICTION>-<SEQ>` |
| `Version` | Yes | Semver (`X.Y.Z`) | Pass 1 error if not valid semver (regex: `^\d+\.\d+\.\d+$`) |
| `Task Type` | Yes | Non-empty string | Pass 1 error if empty. Pass 3 warning if not in known registry |
| `Tier` | Yes | `micro` \| `standard` \| `complex` | Defaults to `standard` if invalid |
| `Author` | Yes | Non-empty string | Not validated beyond parsing |
| `Date` | Yes | ISO 8601 (`YYYY-MM-DD`) | Defaults to `2000-01-01` if unparseable |

**Example:**

```
## Meta

- Spec ID: REIXS-LA-ON-001
- Version: 1.0.0
- Task Type: Lease Abstraction
- Tier: standard
- Author: Reggie Chan
- Date: 2026-03-01
```

**Known task types:** `Lease Abstraction` (registry is extensible).

---

### 3.2 Objective

**Heading aliases:** `Objective`

**Format:** One or more paragraphs of free text.

| Validation | Severity |
|---|---|
| Empty objective | Pass 1 error |

**Example:**

```
## Objective

Extract structured lease terms from a commercial lease document (Ontario jurisdiction)
and produce a normalized term sheet with field-level provenance.
```

---

### 3.3 Domain Context

**Heading aliases:** `Domain Context`, `Domain`

**Format:** Key-value bullet list.

| Field | Required | Format | Validation |
|---|---|---|---|
| `Jurisdiction` | Yes | Non-empty string | Pass 3 error if empty |
| `Currency` | No | Currency code (e.g., `CAD`) | Pass 5 warning if Ontario jurisdiction and currency not declared |
| `Area Unit` | No | Unit string (e.g., `sq ft`) | Not validated |
| `DDD Reference` | Yes* | `re-ddd:<name>@X.Y.Z` | Pass 3 error if missing or invalid format. Warning if not in known registry |
| `ADR References` | Complex tier only | Comma-separated (e.g., `ADR-001, ADR-003`) | Pass 5 error if complex tier and missing |

*DDD Reference is validated with regex: `^re-ddd:[\w_]+@\d+\.\d+\.\d+$`

**Known DDD references:** `re-ddd:lease_core_terms_ontario@0.1.0` (registry is extensible).

**Known jurisdictions:** `Ontario, Canada`, `Ontario`.

**Example:**

```
## Domain Context

- Jurisdiction: Ontario, Canada
- Currency: CAD
- Area Unit: sq ft (default), sq m (accepted)
- DDD Reference: re-ddd:lease_core_terms_ontario@0.1.0
- ADR References: ADR-001, ADR-003
```

---

### 3.4 Inputs

**Heading aliases:** `Inputs`, `Input`

**Format:** Key-value bullet list. No specific fields are required — contents are domain-dependent.

**Example:**

```
## Inputs

- Source document: PDF (scanned or native)
- Document type: Commercial lease agreement
- Expected length: 5-200 pages
```
```

**Step 2: Verify accuracy**

Cross-check each field, format, and validation rule against the source files listed above. Specifically:
- MetaSection has exactly 6 fields (spec_id, version, task_type, tier, author, date)
- Semver regex is `^\d+\.\d+\.\d+$` from `structural.py:10`
- Tier enum has exactly 3 values from `enums.py:6-9`
- DDD ref regex is `^re-ddd:[\w_]+@\d+\.\d+\.\d+$` from `ddd_refs.py:5`
- Heading aliases match `SECTION_ALIASES` in `markdown_parser.py:20-40`

**Step 3: Commit**

```bash
git add docs/REIXS-SPEC.md
git commit -m "docs: add section reference for Meta, Objective, Domain Context, Inputs"
```

---

### Task 3: REIXS-SPEC.md — Section Reference (OFD)

**Files:**
- Modify: `docs/REIXS-SPEC.md`

**Context:** OFD is the most complex section — 10 sub-sections, tier-dependent requirements. This gets its own task.

**Source files to reference:**
- `src/reixs/schema/reixs_models.py:35-45` — `OFDSection` fields (5 required + 5 optional)
- `src/reixs/validate/ofd.py:12-110` — all OFD validation rules
- `src/reixs/parser/section_model.py:90-118` — `_build_ofd` (how parser output maps to model)
- `src/reixs/parser/section_model.py:297-321` — `_parse_severity_model` (Error Severity Model format)

**Step 1: Append OFD section reference**

Append the following to `docs/REIXS-SPEC.md`:

```markdown
### 3.5 Objective Function Design (OFD)

**Heading aliases:** `Objective Function Design`, `Objective Function Design (OFD)`, `OFD`

**Format:** H3 sub-sections, each containing either paragraph text, bullet lists, or ordered lists.

#### Mandatory Sub-Sections (all tiers)

These 5 sub-sections cause Pass 2 errors if missing or empty:

| Sub-Section | H3 Heading | Format | Notes |
|---|---|---|---|
| Primary Objective | `### Primary Objective` | Paragraph | What the agent must achieve |
| Hard Constraints | `### Hard Constraints` | Bullet list | Rules that must never be broken |
| AutoFail Conditions | `### AutoFail Conditions` | Bullet list | Conditions causing automatic failure |
| Optimization Priority Order | `### Optimization Priority Order` | Ordered list | Priority ranking (should mention "factual", "accuracy", or "correct" — Pass 2 warning if not) |
| Uncertainty Policy | `### Uncertainty Policy` | Paragraph | How to handle ambiguous values |

#### Tier-Dependent Sub-Sections

These 5 sub-sections have severity that depends on the spec's tier:

| Sub-Section | H3 Heading | Format | micro | standard | complex |
|---|---|---|---|---|---|
| Secondary Objectives | `### Secondary Objectives` | Bullet list | info | error | error |
| Tradeoff Policies | `### Tradeoff Policies` | Bullet list | info | error | error |
| Scoring Model | `### Scoring Model` | Bullet list | info | error | error |
| Escalation Triggers | `### Escalation Triggers` | Bullet list | info | error | error |
| Error Severity Model | `### Error Severity Model` | Bullet list (special format) | info | error | error |

#### Error Severity Model Format

Each bullet in the Error Severity Model uses the format:

```
- severity: error_type_1, error_type_2, error_type_3
```

Example:

```
### Error Severity Model

- critical: fabricated term, wrong currency, wrong dates
- high: missing critical field without flag, provenance gap
- medium: formatting inconsistency, missing non-critical field
- low: minor normalization differences, whitespace issues
```

The parser splits on the first `:` and then on `,` to produce `{severity: [error_types]}`.

**Full OFD Example:**

```
## Objective Function Design (OFD)

### Primary Objective
Extract all lease terms defined in DDD with factual accuracy >= 98%.

### Hard Constraints
- NEVER fabricate a term not present in the source document
- NEVER silently resolve conflicting dates — flag as CONFLICT
- ALL extracted values MUST carry provenance (page, clause, verbatim quote)

### AutoFail Conditions
- Any fabricated term (not traceable to source text)
- Missing commencement_date without MISSING status flag

### Optimization Priority Order
1. Factual correctness
2. Completeness of extraction
3. Provenance quality
4. Formatting consistency

### Uncertainty Policy
When a term is ambiguous or requires interpretation, mark as INFERENCE
with confidence score and reasoning. Never present inferences as facts.

### Secondary Objectives
- Identify renewal options and escalation clauses
- Flag unusual or non-standard provisions

### Tradeoff Policies
- Prefer MISSING over GUESS
- Prefer verbatim extraction over normalized form when normalization is lossy

### Scoring Model
- Weighted F1: precision weight 0.7, recall weight 0.3
- Critical fields (commencement, expiry, rent): 2x weight

### Escalation Triggers
- Confidence < 0.6 on any critical field
- More than 3 fields marked CONFLICT in single document

### Error Severity Model
- critical: fabricated term, wrong currency, wrong dates
- high: missing critical field without flag, provenance gap
- medium: formatting inconsistency, missing non-critical field
- low: minor normalization differences, whitespace issues
```
```

**Step 2: Verify accuracy**

- Confirm 5 mandatory fields match first 5 checks in `ofd.py:17-51`
- Confirm 5 tier-dependent fields match tier-gated checks in `ofd.py:64-108`
- Confirm micro=info, standard/complex=error matches `ofd.py:65-68`
- Confirm priority order heuristic matches `ofd.py:54-62`
- Confirm error severity model parsing matches `section_model.py:297-321`

**Step 3: Commit**

```bash
git add docs/REIXS-SPEC.md
git commit -m "docs: add OFD section reference with tier-dependent field requirements"
```

---

### Task 4: REIXS-SPEC.md — Section Reference (Constraints, Output Contract, Evaluation, Behavior Spec, Validation Checklist)

**Files:**
- Modify: `docs/REIXS-SPEC.md`

**Context:** Remaining 5 sections. The Behavior Spec section includes the SESF v3 quick reference (inline summary + link).

**Source files to reference:**
- `src/reixs/parser/section_model.py:164-179` — `_build_constraints`
- `src/reixs/parser/section_model.py:182-201` — `_build_output_contract`
- `src/reixs/validate/domain.py:54-61` — output contract provenance/status check
- `src/reixs/parser/section_model.py:204-228` — `_build_evaluation`
- `src/reixs/validate/domain.py:63-71` — EDD suite requirement for standard/complex
- `src/reixs/parser/sesf_extractor.py:6-16` — SESF block extraction (lang="sesf")
- `src/reixs/sesf/adapter.py:22-88` — SESF validation (empty block error, Meta line check)
- `src/reixs/parser/markdown_parser.py:124-127` — checklist checkbox stripping

**Step 1: Append remaining 5 sections**

Append the following to `docs/REIXS-SPEC.md`:

```markdown
### 3.6 Constraints

**Heading aliases:** `Constraints`

**Format:** Bullet list of operational constraints. Key-value bullets (e.g., `Processing time: < 120 seconds`) are accepted and preserved.

**Example:**

```
## Constraints

- Processing time: < 120 seconds per document
- Output format: JSON conforming to lease_abstraction_output_v1.json schema
- No external API calls during extraction (offline-capable)
```

---

### 3.7 Output Contract

**Heading aliases:** `Output Contract`

**Format:** Description paragraph followed by field definitions. Field names should be wrapped in backticks.

| Validation | Severity |
|---|---|
| Description doesn't mention "provenance" or "status" | Pass 3 warning |
| Provenance in OFD hard constraints but not in output contract | Pass 5 warning |

**Example:**

```
## Output Contract

Each extracted field MUST include:
- `value`: the extracted or derived value
- `status`: FACT | INFERENCE | MISSING | CONFLICT
- `provenance`: { page, clause, verbatim_quote } (required for FACT status)
- `confidence`: 0.0-1.0 (required for INFERENCE status)
- `reasoning`: string (required for INFERENCE and CONFLICT status)
```

---

### 3.8 Evaluation / EDD

**Heading aliases:** `Evaluation`, `Evaluation / EDD`, `Eval`, `EDD`

**Format:** Key-value bullet list.

| Field | Required | Format | Validation |
|---|---|---|---|
| `EDD Suite ID` | standard/complex tiers | String identifier | Pass 3 error if missing for standard/complex |
| `Minimum pass rate` | No | Percentage string (e.g., `95%`) | Not validated |
| `Zero tolerance` | No | String | Not validated |
| `Regression cases` | No | Comma-separated list | Parsed into array |

**Example:**

```
## Evaluation / EDD

- EDD Suite ID: edd:lease_abstraction_core_v1
- Minimum pass rate: 95%
- Zero tolerance: critical-severity errors
- Regression cases: basic_valid_case, conflicting_dates_case, missing_commencement_case
```

---

### 3.9 Behavior Spec (SESF)

**Heading aliases:** `Behavior Spec`, `Behavior Spec (SESF)`, `SESF`, `Behavior`

**Format:** Must contain at least one fenced code block with the language tag `sesf`:

````
```sesf
(SESF v3 content here)
```
````

| Validation | Severity |
|---|---|
| No SESF code block or empty block | Pass 4 error |
| Missing Meta line in SESF block | Pass 4 error |
| SESF structural/consistency failures | Pass 4 error (or warning with `--no-strict-sesf`) |

#### SESF v3 Quick Reference

The SESF block must be a valid [SESF v3](https://github.com/reggiechan74/cc-plugins/tree/main/structured-english) document. Here's the minimum structure:

**Meta line** (required):

```
Meta: Version X.Y.Z | Date: YYYY-MM-DD | Domain: <domain> | Status: active | Tier: micro
```

**BEHAVIOR declaration** — groups related rules:

```
BEHAVIOR <name>: <description>
```

**RULE block** — defines expected behavior:

```
  RULE <name>:
    WHEN <condition>
    THEN <action>
    AND <additional action>
```

**ERROR block** — defines error conditions:

```
  ERROR <name>:
    WHEN <condition>
    SEVERITY <critical|high|medium|low>
    ACTION <what to do>
    MESSAGE "<human-readable message>"
```

**EXAMPLE block** — test cases for rules:

```
  EXAMPLE <name>:
    INPUT: <description of input>
    EXPECTED: <expected output>
    NOTES: <explanation>
```

**Constraints section** — operational limits:

```
Constraints
* <constraint item>
```

**Minimal valid SESF block:**

````
```sesf
Extraction Rules

Meta: Version 1.0.0 | Date: 2026-03-01 | Domain: Lease Abstraction | Status: active | Tier: micro

Purpose
Define extraction rules for lease term extraction.

BEHAVIOR extract_terms: Extract lease terms from source document

  RULE basic_extraction:
    WHEN a field value is found verbatim in the source
    THEN status MUST be FACT
    AND provenance MUST include page number

  ERROR missing_provenance:
    WHEN a FACT-status field lacks provenance
    SEVERITY critical
    ACTION fail validation
    MESSAGE "FACT-status field requires provenance"

  EXAMPLE simple_case:
    INPUT: document with commencement date on page 3
    EXPECTED: { "status": "FACT", "provenance": { "page": 3 } }
    NOTES: Basic extraction with provenance

Constraints
* All fields defined in DDD must be processed
```
````

For the full SESF v3 specification, see the [SESF documentation](https://github.com/reggiechan74/cc-plugins/tree/main/structured-english).

---

### 3.10 Validation Checklist

**Heading aliases:** `Validation Checklist`, `Checklist`

**Format:** Checkbox bullet list. Checkbox markers (`[ ]` or `[x]`) are stripped during parsing — only the text is retained.

| Validation | Severity |
|---|---|
| Empty checklist | Pass 1 warning |

**Example:**

```
## Validation Checklist

- [ ] All DDD-defined fields addressed in output contract
- [ ] Hard constraints are machine-checkable
- [ ] AutoFail conditions have corresponding test fixtures
- [ ] SESF rules cover extraction, conflict, and missing-value scenarios
- [ ] Jurisdiction metadata (currency, units) declared
- [ ] EDD suite ID references at least 3 test cases
```
```

**Step 2: Verify accuracy**

- Confirm output contract validation matches `domain.py:54-61`
- Confirm EDD suite requirement matches `domain.py:63-71`
- Confirm SESF block extraction logic matches `sesf_extractor.py:6-16` (lang="sesf")
- Confirm SESF validation errors match `adapter.py:26-34` (empty block) and `adapter.py:58-66` (missing Meta)
- Confirm checklist parsing matches `markdown_parser.py:124-127`

**Step 3: Commit**

```bash
git add docs/REIXS-SPEC.md
git commit -m "docs: add section reference for Constraints, Output Contract, Evaluation, SESF, Checklist"
```

---

### Task 5: REIXS-SPEC.md — Tier System, Validation Rules Summary, Compiled Output Schema, Heading Aliases

**Files:**
- Modify: `docs/REIXS-SPEC.md`

**Context:** The reference sections after the 10-section reference. These are lookup tables for tiers, validation rules, compiled output, and heading aliases.

**Source files to reference:**
- `src/reixs/validate/ofd.py:64-108` — tier-dependent field requirements
- `src/reixs/validate/structural.py` — Pass 1 rules
- `src/reixs/validate/ofd.py` — Pass 2 rules
- `src/reixs/validate/domain.py` — Pass 3 rules
- `src/reixs/sesf/adapter.py` — Pass 4 rules
- `src/reixs/validate/cross_field.py` — Pass 5 rules
- `src/reixs/compile/compiler.py:34-74` — runtime JSON structure
- `src/reixs/compile/compiler.py:81-88` — manifest JSON structure
- `src/reixs/parser/markdown_parser.py:20-40` — `SECTION_ALIASES`

**Step 1: Append remaining sections**

Append the following to `docs/REIXS-SPEC.md`:

```markdown
## 4. Tier System

Specs declare their complexity tier in the Meta section. The tier determines which OFD fields are required and what additional documentation is expected.

| Requirement | micro | standard | complex |
|---|---|---|---|
| **OFD: 5 mandatory fields** | Required | Required | Required |
| **OFD: 5 additional fields** | Optional (info if missing) | Required (error if missing) | Required (error if missing) |
| **EDD Suite ID** | Optional | Required (Pass 3 error) | Required (Pass 3 error) |
| **ADR References** | Optional | Optional | Required (Pass 5 error) |

**Guidance:**
- Use `micro` for simple, well-understood tasks with few edge cases
- Use `standard` for production tasks that need scoring and evaluation
- Use `complex` for tasks with significant ambiguity requiring documented architectural decisions

## 5. Validation Rules Summary

The validator runs 5 passes in order. Fix errors from earlier passes first — later passes may depend on earlier sections being valid.

### Pass 1: Structural

| Field | Severity | Condition |
|---|---|---|
| `meta.version` | error | Not valid semver (`X.Y.Z`) |
| `meta.spec_id` | error | Empty |
| `meta.task_type` | error | Empty |
| `objective` | error | Empty |
| `validation_checklist` | warning | Empty |

### Pass 2: OFD

| Field | Severity | Condition |
|---|---|---|
| `ofd.primary_objective` | error | Empty |
| `ofd.hard_constraints` | error | Empty list |
| `ofd.autofail_conditions` | error | Empty list |
| `ofd.optimization_priority_order` | error | Empty list |
| `ofd.uncertainty_policy` | error | Empty |
| `ofd.optimization_priority_order` | warning | Doesn't mention "factual", "accuracy", or "correct" |
| `ofd.secondary_objectives` | error (std/complex) / info (micro) | Not defined |
| `ofd.tradeoff_policies` | error (std/complex) / info (micro) | Not defined |
| `ofd.scoring_model` | error (std/complex) / info (micro) | Not defined |
| `ofd.escalation_triggers` | error (std/complex) / info (micro) | Not defined |
| `ofd.error_severity_model` | error (std/complex) / info (micro) | Not defined |

### Pass 3: Domain

| Field | Severity | Condition |
|---|---|---|
| `meta.task_type` | warning | Not in known task type registry |
| `domain_context.jurisdiction` | error | Empty |
| `domain_context.ddd_reference` | error | Missing |
| `domain_context.ddd_reference` | error | Invalid format (not `re-ddd:<name>@X.Y.Z`) |
| `domain_context.ddd_reference` | warning | Valid format but not in known registry |
| `output_contract` | warning | Description doesn't mention "provenance" or "status" |
| `evaluation.edd_suite_id` | error | Missing for standard/complex tier |

### Pass 4: SESF

| Field | Severity | Condition |
|---|---|---|
| `behavior_spec` | error | SESF block is empty |
| `behavior_spec` | error | No Meta line in SESF block |
| `behavior_spec` | error/warning | SESF structural or consistency failures (errors become warnings with `--no-strict-sesf`) |

### Pass 5: Cross-Field

| Field | Severity | Condition |
|---|---|---|
| `domain_context.adr_references` | error | Complex tier and no ADR references |
| `output_contract` | warning | OFD hard constraints mention "provenance" but output contract doesn't |
| `domain_context.currency` | warning | Ontario jurisdiction without currency declaration |

### Validation Status

| Status | Meaning |
|---|---|
| `pass` | No errors, no warnings |
| `warn` | No errors, at least one warning |
| `fail` | At least one error |

## 6. Compiled Output Schema

When `reixs compile` succeeds (validation status is not `fail`), it produces two JSON files.

### `reixs.runtime.json`

This is what a downstream AI agent receives. Structure:

```json
{
  "spec_metadata": {
    "spec_id": "REIXS-LA-ON-001",
    "version": "1.0.0",
    "task_type": "Lease Abstraction",
    "tier": "standard",
    "author": "Reggie Chan",
    "date": "2026-03-01"
  },
  "task_context": {
    "objective": "Extract structured lease terms...",
    "jurisdiction": "Ontario, Canada",
    "currency": "CAD",
    "area_unit": "sq ft"
  },
  "ofd": {
    "primary_objective": "Extract all lease terms...",
    "hard_constraints": ["NEVER fabricate...", "..."],
    "autofail_conditions": ["Any fabricated term...", "..."],
    "optimization_priority_order": ["Factual correctness", "..."],
    "uncertainty_policy": "When a term is ambiguous..."
  },
  "behavior_rules": {
    "raw_sesf": "(full SESF text)",
    "block_count": 1
  },
  "output_contract": {
    "description": "Each extracted field MUST include...",
    "fields": [
      {"name": "value", "description": "the extracted or derived value"},
      {"name": "status", "description": "FACT | INFERENCE | MISSING | CONFLICT"}
    ]
  },
  "eval_config": {
    "edd_suite_id": "edd:lease_abstraction_core_v1",
    "min_pass_rate": "95%",
    "regression_cases": ["basic_valid_case", "conflicting_dates_case"]
  },
  "references": {
    "ddd_reference": "re-ddd:lease_core_terms_ontario@0.1.0",
    "adr_references": ["ADR-001", "ADR-003"]
  },
  "validation_status": "warn"
}
```

### `reixs.manifest.json`

Metadata envelope for reproducibility:

```json
{
  "spec_id": "REIXS-LA-ON-001",
  "version": "1.0.0",
  "source_hash": "sha256:<hex>",
  "compile_timestamp": "2026-03-01T18:30:00+00:00",
  "artifacts": ["reixs.runtime.json", "reixs.manifest.json"]
}
```

The `source_hash` is the SHA-256 of the original `.reixs.md` file, enabling you to verify that a runtime payload matches a specific source spec.

### Optional: `reixs.validation.json`

When compiled with `--include-validation`, a third file contains the full validation report (all findings, pass summaries, and computed status).

## 7. Heading Aliases Reference

The parser accepts these heading variations for each section:

| Canonical Name | Accepted Headings |
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

Heading matching is case-insensitive. Markdown formatting characters (`#`, `*`, `_`, `` ` ``) are stripped before matching.
```

**Step 2: Verify accuracy**

- Confirm tier table matches OFD validation in `ofd.py:64-108` and domain checks in `domain.py:63-71` and cross-field in `cross_field.py:15-21`
- Confirm every validation rule in summary tables matches a check in the corresponding validator module
- Confirm runtime JSON structure matches `compiler.py:34-74`
- Confirm manifest structure matches `compiler.py:81-88`
- Confirm heading aliases match `SECTION_ALIASES` in `markdown_parser.py:20-40`

**Step 3: Commit**

```bash
git add docs/REIXS-SPEC.md
git commit -m "docs: add tier system, validation rules, compiled output schema, heading aliases"
```

---

### Task 6: TUTORIAL.md — Prerequisites + Step-by-Step Authoring (Meta through Inputs)

**Files:**
- Create: `docs/TUTORIAL.md`

**Context:** Hands-on tutorial using a different domain (property valuation) than the Ontario lease template. Walks through writing the first 4 sections with validate-as-you-go.

**Step 1: Write the tutorial introduction and first 4 sections**

Write the following to `docs/TUTORIAL.md`:

```markdown
# Tutorial: Write Your First REIXS Spec

This tutorial walks you through writing a complete `.reixs.md` file from scratch. By the end, you'll have a validated, compilable spec for a **property valuation summary** task.

We use a different domain than the built-in Ontario lease template — so you'll learn the format rather than copy an example.

## Prerequisites

```bash
# Clone and install REIXS
git clone https://github.com/reggiechan74/reixs.git
cd reixs
pip install -e ".[dev]"

# Verify it works
reixs --version
```

## Step 1: Create the File

Create `my_spec.reixs.md` with the title and first section:

```markdown
# REIXS: Property Valuation Summary — British Columbia

## Meta

- Spec ID: REIXS-PV-BC-001
- Version: 0.1.0
- Task Type: Property Valuation
- Tier: micro
- Author: Your Name
- Date: 2026-03-01
```

**Why `micro` tier?** This is a simple task — we want the smallest valid spec. Later you can upgrade to `standard` when you add scoring and evaluation.

Let's validate what we have so far:

```bash
reixs validate my_spec.reixs.md
```

You'll see errors about missing sections — that's expected. We'll fix them one by one.

## Step 2: Add the Objective

```markdown
## Objective

Extract key valuation metrics from a residential appraisal report (BC jurisdiction)
and produce a structured summary with source page references.
```

This is a free-text paragraph. The only rule: it can't be empty.

## Step 3: Add Domain Context

```markdown
## Domain Context

- Jurisdiction: British Columbia, Canada
- Currency: CAD
- DDD Reference: re-ddd:property_valuation_bc@0.1.0
```

**Key rules:**
- `Jurisdiction` is required
- `DDD Reference` must follow the format `re-ddd:<name>@X.Y.Z`
- The DDD reference doesn't need to be in REIXS's built-in registry — you'll get a warning, not an error

## Step 4: Add Inputs

```markdown
## Inputs

- Source document: PDF appraisal report
- Document type: Residential property appraisal (Form 1004 or equivalent)
- Expected length: 10-50 pages
```

Inputs are domain-specific key-value pairs. No particular fields are required.
```

**Step 2: Commit**

```bash
git add docs/TUTORIAL.md
git commit -m "docs: add tutorial with prerequisites and first 4 sections"
```

---

### Task 7: TUTORIAL.md — OFD, Constraints, Output Contract, Evaluation, Checklist

**Files:**
- Modify: `docs/TUTORIAL.md`

**Context:** Continue the tutorial through the remaining non-SESF sections. The SESF block gets its own task because it's the hardest part.

**Step 1: Append sections 5-9**

Append the following to `docs/TUTORIAL.md`:

```markdown
## Step 5: Add the OFD

The Objective Function Design is the heart of the spec — it defines the hard rules your agent must follow. Since we chose `micro` tier, we only need 5 sub-sections:

```markdown
## Objective Function Design (OFD)

### Primary Objective
Extract property valuation metrics with factual accuracy >= 95%.

### Hard Constraints
- NEVER fabricate a value not present in the appraisal report
- NEVER alter assessed values — extract verbatim
- ALL extracted values MUST include the source page number

### AutoFail Conditions
- Any fabricated valuation figure
- Market value extracted without page reference

### Optimization Priority Order
1. Factual correctness
2. Completeness of key metrics
3. Source traceability

### Uncertainty Policy
When a metric requires interpretation (e.g., adjusted vs. unadjusted value),
mark as INFERENCE with reasoning. Never present interpretations as facts.
```

**Why these fields?** The mandatory 5 define *what the agent must optimize for*. The priority order should mention "factual" or "accuracy" — the validator checks for this.

For `standard` or `complex` tiers, you'd also need: Secondary Objectives, Tradeoff Policies, Scoring Model, Escalation Triggers, and Error Severity Model.

## Step 6: Add Constraints

```markdown
## Constraints

- Processing time: < 60 seconds per document
- Output format: JSON
- Offline processing only — no external API calls
```

Operational limits. No specific fields required.

## Step 7: Add Output Contract

```markdown
## Output Contract

Each extracted metric MUST include:
- `value`: the extracted numeric or text value
- `status`: FACT | INFERENCE | MISSING
- `provenance`: { page } (required for FACT status)
```

**Important:** The validator checks that the output contract mentions "provenance" or "status". If it doesn't, you'll get a warning.

## Step 8: Add Evaluation

Since we're using `micro` tier, EDD Suite ID is optional. But let's include the basics:

```markdown
## Evaluation / EDD

- Minimum pass rate: 90%
- Regression cases: basic_appraisal, missing_market_value
```

For `standard` or `complex` tiers, `EDD Suite ID` becomes required.

## Step 9: Add the Validation Checklist

```markdown
## Validation Checklist

- [ ] All key valuation fields addressed in output contract
- [ ] Hard constraints are machine-checkable
- [ ] Jurisdiction metadata (currency) declared
```

This is a self-audit for spec authors. The validator warns if it's empty but doesn't check the content.
```

**Step 2: Commit**

```bash
git add docs/TUTORIAL.md
git commit -m "docs: add tutorial sections for OFD through Validation Checklist"
```

---

### Task 8: TUTORIAL.md — The SESF Block, Compile and Inspect, Common Mistakes

**Files:**
- Modify: `docs/TUTORIAL.md`

**Context:** The hardest part of the tutorial — writing the SESF block. Also includes the final steps (compile + common mistakes).

**Step 1: Append SESF, compile, and common mistakes sections**

Append the following to `docs/TUTORIAL.md`:

```markdown
## Step 10: Add the Behavior Spec (SESF)

This is the trickiest section. You need a fenced code block with the language tag `sesf` containing a valid SESF v3 document.

```markdown
## Behavior Spec (SESF)
```

Then add the fenced SESF block:

````
```sesf
Property Valuation Extraction Rules

Meta: Version 0.1.0 | Date: 2026-03-01 | Domain: Property Valuation | Status: active | Tier: micro

Purpose
Define extraction rules for residential property valuation metrics.

BEHAVIOR extract_valuation_metrics: Extract key valuation data from appraisal reports

  RULE verbatim_value:
    WHEN a valuation figure is found verbatim in the report
    THEN status MUST be FACT
    AND provenance MUST include page number

  RULE derived_value:
    WHEN a metric requires calculation or interpretation
    THEN status MUST be INFERENCE
    AND reasoning MUST explain the derivation

  ERROR fabricated_value:
    WHEN an extracted value cannot be traced to the source report
    SEVERITY critical
    ACTION reject the extraction
    MESSAGE "Value has no source provenance — possible fabrication"

  EXAMPLE basic_extraction:
    INPUT: appraisal with market value "$650,000" on page 2
    EXPECTED: { "value": 650000, "status": "FACT", "provenance": { "page": 2 } }
    NOTES: Simple numeric extraction with provenance

Constraints
* All key valuation fields must be processed before completion
```
````

**Key requirements for the SESF block:**
- Must have a `Meta:` line with Version, Date, Domain, Status, and Tier
- At least one `BEHAVIOR` declaration
- `RULE` blocks use `WHEN`/`THEN`/`AND`
- `ERROR` blocks need `SEVERITY`, `ACTION`, and `MESSAGE`
- `EXAMPLE` blocks need `INPUT:`, `EXPECTED:`, and `NOTES:`

## Step 11: Validate the Complete Spec

Now run validation on the complete file:

```bash
reixs validate my_spec.reixs.md
```

Expected output: **Status: WARN** (not FAIL). You'll see warnings like:
- "Task type 'Property Valuation' not in known registry" — that's fine, the registry is extensible
- "DDD Reference not found in local registry" — also fine for new domains

If you see any **errors**, fix them before proceeding. Common fixes:
- Version not semver → use `X.Y.Z` format
- DDD Reference format invalid → use `re-ddd:<name>@X.Y.Z`
- OFD fields missing → add the required H3 sub-sections

## Step 12: Compile

Once validation passes (status is PASS or WARN):

```bash
reixs compile my_spec.reixs.md -o build/
```

This produces two files in `build/`:

- **`reixs.runtime.json`** — everything an agent needs: objective, constraints, SESF rules, output contract
- **`reixs.manifest.json`** — metadata with source hash for reproducibility

Inspect the runtime payload:

```bash
cat build/reixs.runtime.json | python -m json.tool
```

You'll see your spec transformed into a structured JSON payload ready for an agent prompt.

## Common Mistakes

### 1. Version is not semver

```
Error: Version 'v1.0' is not valid semver
```
**Fix:** Use exactly `X.Y.Z` — three numbers separated by dots. No `v` prefix, no extra segments.

### 2. DDD Reference format invalid

```
Error: DDD Reference 'lease_terms_v1' has invalid format
```
**Fix:** Must be `re-ddd:<name>@X.Y.Z`. Example: `re-ddd:property_valuation_bc@0.1.0`

### 3. EDD Suite ID required for standard/complex tier

```
Error: EDD Suite ID required for standard/complex tier
```
**Fix:** Either add `EDD Suite ID: edd:your_suite_v1` to the Evaluation section, or downgrade to `micro` tier.

### 4. SESF block has no Meta section

```
Error: SESF block has no Meta section — not a valid SESF v3 spec
```
**Fix:** Add a Meta line inside the SESF block: `Meta: Version 1.0.0 | Date: 2026-03-01 | Domain: Your Domain | Status: active | Tier: micro`

### 5. Complex tier requires ADR references

```
Error: Complex tier requires ADR references
```
**Fix:** Add `ADR References: ADR-001` to Domain Context, or downgrade to `standard` tier.

---

**Next steps:**
- Read the full [REIXS Format Specification](REIXS-SPEC.md) for detailed field reference
- Explore the Ontario lease template at `specs/templates/lease_abstraction_ontario.reixs.md`
- Try upgrading your spec to `standard` tier and adding the 5 additional OFD fields
```

**Step 2: Commit**

```bash
git add docs/TUTORIAL.md
git commit -m "docs: add SESF walkthrough, compile instructions, and common mistakes"
```

---

### Task 9: Update README to link to new documents

**Files:**
- Modify: `README.md`

**Context:** The README should link to the new spec reference and tutorial so readers can find them.

**Step 1: Add a Documentation section to README.md**

After the "Quick Start" section and before "Commands", add:

```markdown
## Documentation

| Document | Purpose |
|---|---|
| [Format Specification](docs/REIXS-SPEC.md) | Authoritative reference for the `.reixs.md` format — sections, fields, validation rules |
| [Tutorial](docs/TUTORIAL.md) | Step-by-step guide to writing your first REIXS spec |
| [README](README.md) | Tool overview, CLI commands, architecture (this file) |
```

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add documentation links to README"
```

---

### Task 10: Final verification + push

**Step 1: Verify all links resolve**

```bash
cd /workspaces/reixs
# Check that all referenced files exist
ls docs/REIXS-SPEC.md docs/TUTORIAL.md README.md
```

**Step 2: Verify validation rules count**

Manually count validation rules in REIXS-SPEC.md section 5 and compare against source:
- Pass 1: 5 rules (structural.py has 5 checks)
- Pass 2: 11 rules (ofd.py has 5 mandatory + 1 heuristic + 5 tier-dependent)
- Pass 3: 7 rules (domain.py has 7 checks)
- Pass 4: 3 rules (adapter.py has 3 check categories)
- Pass 5: 3 rules (cross_field.py has 3 checks)

**Step 3: Push**

```bash
git push origin main
```
