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
