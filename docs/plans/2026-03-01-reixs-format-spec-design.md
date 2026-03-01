# REIXS Format Specification & Tutorial — Design Document

**Goal:** Create two documents that close the "authoring gap" — a complete format reference (`docs/REIXS-SPEC.md`) and a hands-on tutorial (`docs/TUTORIAL.md`) so that someone with zero context can write, validate, and compile a `.reixs.md` file.

**Audience:** Spec authors (writing `.reixs.md` files) and agent developers (consuming compiled runtime JSON). Both audiences served by the same reference document, with clearly marked sections.

---

## Document 1: `docs/REIXS-SPEC.md` — Format Reference

The authoritative reference for the `.reixs.md` format. Every rule documented here is derived from the parser and validator source code — not invented.

### Structure

1. **Introduction**
   - What a REIXS spec is
   - Who this document is for (spec authors + agent developers)
   - Relationship to README (README = tool overview, this = format reference)

2. **File Structure Overview**
   - H1 title line (free-form, not validated)
   - 10 mandatory H2 sections
   - H3 subsections within OFD
   - Fenced code blocks for SESF (```sesf)
   - Key-value bullet syntax (`- Key: Value`)

3. **Section Reference** — one subsection per section (10 total):

   **3.1 Meta**
   - 6 required fields: `Spec ID`, `Version`, `Task Type`, `Tier`, `Author`, `Date`
   - Version: must be semver (`X.Y.Z`)
   - Tier: one of `micro`, `standard`, `complex`
   - Date: ISO 8601 (`YYYY-MM-DD`)
   - Spec ID: non-empty string (convention: `REIXS-<TYPE>-<JURISDICTION>-<SEQ>`)
   - Accepted heading aliases: `Meta`

   **3.2 Objective**
   - Free-text paragraph
   - Must be non-empty (Pass 1 error if empty)
   - Accepted aliases: `Objective`

   **3.3 Domain Context**
   - Required: `Jurisdiction`
   - Optional: `Currency`, `Area Unit`, `DDD Reference`, `ADR References`
   - DDD Reference format: `re-ddd:<name>@X.Y.Z` (regex validated)
   - ADR References: comma-separated list (e.g., `ADR-001, ADR-003`)
   - Complex tier requires ADR References (Pass 5 error)
   - Ontario jurisdiction should declare CAD currency (Pass 5 warning)
   - Accepted aliases: `Domain Context`, `Domain`

   **3.4 Inputs**
   - Bullet list of `Key: Value` pairs
   - No specific field requirements — domain-dependent
   - Accepted aliases: `Inputs`, `Input`

   **3.5 Objective Function Design (OFD)**
   - 10 sub-sections under H3 headings
   - 5 mandatory (all tiers): Primary Objective, Hard Constraints, AutoFail Conditions, Optimization Priority Order, Uncertainty Policy
   - 5 tier-dependent: Secondary Objectives, Tradeoff Policies, Scoring Model, Escalation Triggers, Error Severity Model
     - micro: info if missing
     - standard/complex: error if missing
   - Hard Constraints: bullet list
   - AutoFail Conditions: bullet list
   - Optimization Priority Order: ordered list (heuristic: should mention factual/accuracy/correct)
   - Uncertainty Policy: paragraph text
   - Error Severity Model: bullet list in format `severity: error1, error2, error3`
   - Accepted aliases: `Objective Function Design`, `Objective Function Design (OFD)`, `OFD`

   **3.6 Constraints**
   - Bullet list of operational constraints
   - No specific field requirements
   - Accepted aliases: `Constraints`

   **3.7 Output Contract**
   - Description paragraph (should mention `provenance` or `status` — Pass 3 warning if not)
   - Field definitions using backtick-wrapped names: `` `field_name` ``: description
   - Accepted aliases: `Output Contract`

   **3.8 Evaluation / EDD**
   - Fields: `EDD Suite ID`, `Minimum pass rate`, `Zero tolerance`, `Regression cases`
   - EDD Suite ID required for standard/complex tiers (Pass 3 error)
   - Regression cases: comma-separated list
   - Accepted aliases: `Evaluation`, `Evaluation / EDD`, `Eval`, `EDD`

   **3.9 Behavior Spec (SESF)**
   - Must contain a fenced code block with language tag `sesf`
   - Empty SESF block = Pass 4 error
   - SESF v3 Quick Reference (inline summary):
     - Meta line format: `Version X.Y.Z | Date: YYYY-MM-DD | Domain: ... | Status: active | Tier: micro`
     - BEHAVIOR declarations: `BEHAVIOR name: description`
     - RULE blocks: `RULE name:` → `WHEN` → `THEN` → optional `AND`
     - ERROR blocks: `ERROR name:` → `WHEN` → `SEVERITY` → `ACTION` → `MESSAGE`
     - EXAMPLE blocks: `EXAMPLE name:` → `INPUT:` → `EXPECTED:` → `NOTES:`
     - Constraints section: `Constraints` followed by `*` bullet items
   - Link to full SESF v3 specification
   - Accepted aliases: `Behavior Spec`, `Behavior Spec (SESF)`, `SESF`, `Behavior`

   **3.10 Validation Checklist**
   - Checkbox bullet list: `- [ ] item`
   - Checkbox markers are stripped during parsing
   - Empty checklist = Pass 1 warning
   - Accepted aliases: `Validation Checklist`, `Checklist`

4. **Tier System**
   - Table: tier × field requirements (mandatory/required/optional)
   - micro: 5 mandatory OFD fields only, no ADR, no EDD suite
   - standard: 5 mandatory + 5 recommended OFD fields, EDD suite required
   - complex: all 10 OFD fields, ADR required, EDD suite required

5. **Validation Rules Summary**
   - Table organized by pass number (1-5)
   - Columns: Pass | Field | Severity | Condition | Suggestion
   - Complete list derived from all 5 validator modules

6. **Compiled Output Schema**
   - `reixs.runtime.json` structure (for agent developers)
   - `reixs.manifest.json` structure (for reproducibility)
   - Only emitted when validation status ≠ fail

7. **Heading Aliases Reference**
   - Complete lookup table: canonical name → all accepted heading strings

---

## Document 2: `docs/TUTORIAL.md` — Write Your First Spec

Hands-on walkthrough for first-time authors. Uses a different domain than the Ontario lease template to force understanding rather than copying.

### Structure

1. **Prerequisites**
   - Install REIXS (`pip install -e ".[dev]"`)
   - Verify CLI works (`reixs --version`)

2. **Choose Your Task**
   - Example: "Property Valuation Summary" — extract key valuation metrics from an appraisal report
   - Simpler than lease abstraction, different enough to avoid copy-paste

3. **Step-by-Step Authoring** (one section at a time)
   - Each step: write the section → run `reixs validate` → interpret output → fix errors
   - Sections in authoring order: Meta → Objective → Domain Context → Inputs → OFD → Constraints → Output Contract → Evaluation → Behavior Spec → Validation Checklist

4. **The SESF Block** (dedicated section — hardest part)
   - Walk through writing one BEHAVIOR, two RULEs, one ERROR, one EXAMPLE
   - Show common SESF mistakes and their error messages

5. **Compile and Inspect**
   - Run `reixs compile`
   - Walk through runtime.json and manifest.json
   - Show what an agent developer receives

6. **Common Mistakes**
   - Top 5 validation failures with exact error messages and fixes
   - "Version not semver", "DDD Reference format invalid", "EDD Suite ID required for standard tier", etc.

---

## Source of Truth

Every rule in REIXS-SPEC.md MUST be traceable to source code:

| Rule | Source |
|---|---|
| Section names + aliases | `parser/markdown_parser.py:SECTION_ALIASES` |
| Meta field names + types | `schema/reixs_models.py:MetaSection` + `parser/section_model.py:_build_meta` |
| Tier enum values | `schema/enums.py:Tier` |
| Field status enum values | `schema/enums.py:FieldStatus` |
| Semver regex | `validate/structural.py:SEMVER_RE` |
| DDD ref regex | `registry/ddd_refs.py:DDD_REF_PATTERN` |
| Known task types | `registry/task_types.py:KNOWN_TASK_TYPES` |
| Known jurisdictions | `registry/jurisdictions.py:KNOWN_JURISDICTIONS` |
| OFD mandatory fields | `validate/ofd.py:validate_ofd` (first 5 checks) |
| OFD tier-dependent fields | `validate/ofd.py:validate_ofd` (tier-gated checks) |
| SESF block extraction | `parser/sesf_extractor.py:extract_sesf_blocks` (lang="sesf") |
| Cross-field rules | `validate/cross_field.py:validate_cross_field` |
| Runtime JSON schema | `schema/runtime_payload.py:RuntimePayload` |
| Manifest schema | `schema/runtime_payload.py:Manifest` |

---

## Decisions

- **Two documents, not one:** Reference (REIXS-SPEC.md) for lookup, Tutorial for learning. Different purposes, different structures.
- **SESF inline summary + link:** Enough to author a basic SESF block without leaving the doc, link to full spec for advanced usage.
- **Validation rules as lookup table:** Organized by pass number so authors can fix errors in order (structural → OFD → domain → SESF → cross-field).
- **Tutorial uses different domain:** Prevents copy-paste learning from the Ontario lease template.
