# SESF v3→v4 Migration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace the vendored SESF v3 validator with v4, update the adapter to call all 11 validation checks with configurable selection, promote the commercial NA spec's SESF block to standard tier, and update all v3 references across docs.

**Architecture:** Drop-in replacement — the v4 validator is a strict superset of v3 with identical function signatures for all 6 existing checks plus 5 new ones. The adapter gains a `checks` parameter (defaults to all 11) so callers can opt out of specific checks. Existing specs continue to validate because v4 is backward-compatible.

**Tech Stack:** Python 3.10+, pytest, Pydantic (for Finding model), markdown

---

### Task 1: Replace vendored v3 validator with v4

**Files:**
- Replace: `src/reixs/sesf/validate_sesf.py`
- Source: `/home/codespace/.claude/plugins/cache/cc-plugins/structured-english/5.1.0/skills/structured-english/scripts/validate_sesf.py`

**Step 1: Copy the v4 validator over the v3 file**

```bash
cp /home/codespace/.claude/plugins/cache/cc-plugins/structured-english/5.1.0/skills/structured-english/scripts/validate_sesf.py \
   src/reixs/sesf/validate_sesf.py
```

**Step 2: Verify the v4 validator imports work**

```bash
python -c "from reixs.sesf.validate_sesf import parse_sesf, check_structural_completeness, check_error_consistency, check_example_consistency, check_type_consistency, check_rule_integrity, check_cross_behavior, check_config_references, check_variable_threading, check_route_completeness, check_error_table_structure, check_notation_section; print('All 12 imports OK')"
```

Expected: `All 12 imports OK`

**Step 3: Run existing tests to verify backward compatibility**

```bash
pytest tests/test_sesf_adapter.py -v
```

Expected: All 3 existing tests PASS (v4 validator handles v3 specs)

**Step 4: Commit**

```bash
git add src/reixs/sesf/validate_sesf.py
git commit -m "feat: replace vendored SESF v3 validator with v4

v4 adds support for @config, @route, \$variable threading, compact
error/example tables, and Notation section validation. All v3
function signatures preserved for backward compatibility."
```

---

### Task 2: Update adapter to call all 11 checks with configurable selection

**Files:**
- Modify: `src/reixs/sesf/adapter.py`
- Test: `tests/test_sesf_adapter.py`

**Step 1: Write the failing tests**

Add to `tests/test_sesf_adapter.py`:

```python
VALID_SESF_V4 = """\
Standard Tier Spec

Meta
* Version: 1.0.0
* Date: 2026-03-03
* Domain: Test
* Status: active
* Tier: standard

Notation
* $ -- references a variable or config value
* @ -- marks a structured block
* -> -- means "produces" or "routes to"
* MUST/SHOULD/MAY/CAN -- requirement strength keywords

Purpose
Test spec for v4 validation.

Scope
* IN SCOPE: testing v4 features
* OUT OF SCOPE: production use

Inputs
* document: string - the source document - required

Outputs
* result: string - the extracted result

@config
  max_retries: 3

Types
-- none: all data structures are inline

Functions
-- none: all logic is expressed directly in behavior rules

BEHAVIOR test_behavior: Test behavior for v4 validation

  RULE basic_rule:
    WHEN input is provided
    THEN output MUST be produced

  @route classify_input [first_match_wins]
    input is type A   -> handler_a
    input is type B   -> handler_b
    input is type C   -> handler_c
    *                 -> default_handler

  ERRORS:
  | name | when | severity | action | message |
  |------|------|----------|--------|---------|
  | no_input | input is missing | critical | halt | "Input required" |

  EXAMPLES:
    valid_input: input="hello" -> output produced
    missing_input: input=null -> rejected with "Input required"

Constraints
* Output MUST be non-empty

Dependencies
* None
"""


class TestConfigurableChecks:
    def test_default_runs_all_checks(self):
        """Default (no checks param) runs all available checks."""
        findings = validate_sesf_block(VALID_SESF, pass_number=4)
        # Should have findings from structural, error, and example checks at minimum
        categories = {f.field for f in findings}
        assert "meta" in categories or "sections" in categories

    def test_custom_checks_subset(self):
        """Passing a subset of check names limits which checks run."""
        findings = validate_sesf_block(
            VALID_SESF, pass_number=4,
            checks=["check_structural_completeness"],
        )
        # Should have structural findings but no error/example findings
        error_findings = [f for f in findings if f.field == "error_consistency"]
        assert len(error_findings) == 0

    def test_empty_checks_returns_no_validation_findings(self):
        """Empty checks list means no SESF validation runs (only parse)."""
        findings = validate_sesf_block(VALID_SESF, pass_number=4, checks=[])
        # Only the parse succeeds, no check findings
        assert len(findings) == 0

    def test_v4_features_validated(self):
        """v4 spec with @config, @route, compact tables passes validation."""
        findings = validate_sesf_block(VALID_SESF_V4, pass_number=4)
        errors = [f for f in findings if f.severity == "error"]
        assert len(errors) == 0, (
            f"Unexpected errors: {[e.message for e in errors]}"
        )

    def test_v3_message_updated(self):
        """Empty SESF block message references v4 not v3."""
        findings = validate_sesf_block("", pass_number=4)
        error_msgs = [f.message for f in findings if f.severity == "error"]
        assert any("v4" in m or "SESF" in m for m in error_msgs)
        assert not any("v3" in m for m in error_msgs)
```

**Step 2: Run tests to verify they fail**

```bash
pytest tests/test_sesf_adapter.py::TestConfigurableChecks -v
```

Expected: FAIL — `validate_sesf_block` does not accept `checks` parameter yet

**Step 3: Implement the adapter update**

Replace the full content of `src/reixs/sesf/adapter.py`:

```python
"""SESF validator adapter — maps SESF validation results to REIXS findings."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Sequence

from reixs.validate.report import Finding

try:
    from reixs.sesf.validate_sesf import (
        parse_sesf,
        check_structural_completeness,
        check_error_consistency,
        check_example_consistency,
        check_type_consistency,
        check_rule_integrity,
        check_cross_behavior,
        check_config_references,
        check_variable_threading,
        check_route_completeness,
        check_error_table_structure,
        check_notation_section,
    )
    SESF_AVAILABLE = True
except ImportError:
    SESF_AVAILABLE = False

# Registry of all available SESF check functions, keyed by name.
# Order matters — structural checks run first, then consistency, then v4.
ALL_CHECKS: dict[str, object] = {}
if SESF_AVAILABLE:
    ALL_CHECKS = {
        "check_structural_completeness": check_structural_completeness,
        "check_type_consistency": check_type_consistency,
        "check_rule_integrity": check_rule_integrity,
        "check_error_consistency": check_error_consistency,
        "check_example_consistency": check_example_consistency,
        "check_cross_behavior": check_cross_behavior,
        "check_config_references": check_config_references,
        "check_variable_threading": check_variable_threading,
        "check_route_completeness": check_route_completeness,
        "check_error_table_structure": check_error_table_structure,
        "check_notation_section": check_notation_section,
    }


def validate_sesf_block(
    sesf_text: str,
    pass_number: int = 4,
    checks: Sequence[str] | None = None,
) -> list[Finding]:
    """Validate a SESF text block and return REIXS findings.

    Args:
        sesf_text: The raw SESF specification text.
        pass_number: The REIXS validation pass number (default 4).
        checks: Optional list of check function names to run.
                Defaults to all available checks. Pass an empty list
                to skip all SESF validation (parse only).
    """
    findings: list[Finding] = []

    if not sesf_text or not sesf_text.strip():
        findings.append(Finding(
            pass_number=pass_number,
            severity="error",
            section="behavior_spec",
            field=None,
            message="SESF block is empty",
            suggestion="Add SESF v4 behavior rules in the ```sesf fenced block",
        ))
        return findings

    if not SESF_AVAILABLE:
        findings.append(Finding(
            pass_number=pass_number,
            severity="warning",
            section="behavior_spec",
            field=None,
            message="SESF validator not available — skipping deep validation",
            suggestion=None,
        ))
        return findings

    # Resolve which checks to run
    if checks is None:
        selected = list(ALL_CHECKS.values())
    else:
        selected = [ALL_CHECKS[name] for name in checks if name in ALL_CHECKS]

    # Write to temp file for the SESF parser
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    ) as f:
        f.write(sesf_text)
        tmp_path = f.name

    try:
        doc = parse_sesf(tmp_path)

        if not doc.meta:
            findings.append(Finding(
                pass_number=pass_number,
                severity="error",
                section="behavior_spec",
                field=None,
                message="SESF block has no Meta section — not a valid SESF v4 spec",
                suggestion="Add Meta line: Version X.Y.Z | Date: YYYY-MM-DD | Domain: ... | Status: active | Tier: micro",
            ))
            return findings

        # Run selected SESF validation checks
        sesf_results = []
        for check_fn in selected:
            sesf_results.extend(check_fn(doc))

        # Map SESF ValidationResult → REIXS Finding
        for r in sesf_results:
            severity = _map_sesf_status(r.status)
            findings.append(Finding(
                pass_number=pass_number,
                severity=severity,
                section="behavior_spec",
                field=r.category,
                message=f"[SESF] {r.message}",
                suggestion=None,
            ))
    finally:
        Path(tmp_path).unlink(missing_ok=True)

    return findings


def _map_sesf_status(status: str) -> str:
    """Map SESF status (PASS/WARN/FAIL) to REIXS severity."""
    return {
        "PASS": "info",
        "WARN": "warning",
        "FAIL": "error",
    }.get(status, "info")
```

**Step 4: Run tests to verify they pass**

```bash
pytest tests/test_sesf_adapter.py -v
```

Expected: All tests PASS (both original TestSESFAdapter and new TestConfigurableChecks)

**Step 5: Commit**

```bash
git add src/reixs/sesf/adapter.py tests/test_sesf_adapter.py
git commit -m "feat: update SESF adapter with all 11 v4 checks and configurable selection

- Import all 11 check functions (6 v3 + 5 v4)
- Add checks parameter for configurable check selection
- Default runs all 11 checks
- Update v3 references to v4 in messages"
```

---

### Task 3: Promote commercial NA SESF block to standard tier

**Files:**
- Modify: `specs/templates/lease_abstraction_commercial_na.reixs.md` (lines 122-252, the SESF fenced block)

**Step 1: Update the SESF block**

Replace the existing SESF block (everything between the ` ```sesf ` and closing ` ``` ` fences) with the standard-tier version. Key changes:

1. Change pipe-delimited Meta to multi-line bullet format
2. Change `Tier: micro` to `Tier: standard`
3. Add Notation section after Meta
4. Add Scope section (IN SCOPE / OUT OF SCOPE)
5. Add Inputs section
6. Add Outputs section
7. Add Types section (`-- none` stub)
8. Add Functions section (`-- none` stub)
9. Add Dependencies section
10. Convert the 6 ERROR blocks into a compact ERRORS: table in `validate_extraction`

The existing BEHAVIOR blocks, RULEs, and EXAMPLEs remain unchanged in content — only the structural wrapper changes.

Here is what the SESF block should look like (inside the fences):

```
Commercial Lease Abstraction Extraction Rules

Meta
* Version: 1.0.0
* Date: 2026-03-01
* Domain: Lease Abstraction
* Status: active
* Tier: standard

Notation
* $ -- references a variable or config value (e.g., $config.threshold)
* @ -- marks a structured block (@config for parameters, @route for decision tables)
* -> -- means "produces", "routes to", or "yields"
* MUST/SHOULD/MAY/CAN -- requirement strength keywords

Purpose
Define extraction, conflict detection, provenance, and normalization rules for North American commercial lease term extraction across 25 standardized sections with dual output format support.

Scope
* IN SCOPE: financial value extraction, date normalization, conflict detection, schedule override handling, provenance tracking, currency inference, completeness validation
* OUT OF SCOPE: lease classification, tenant creditworthiness assessment, market rent comparison, lease negotiation advice

Inputs
* source_document: PDF or image - the commercial lease document to extract terms from - required
* output_format: enum [json, markdown] - the desired output format - required
* ddd_reference: string - the DDD reference defining the 25 extraction sections - required

Outputs
* extraction_result: object - structured extraction with status, provenance, and normalized values per field across all 25 sections

@config
  completeness_escalation_threshold: 0.30
  confidence_review_threshold: 0.5

Types
-- none: all data structures are inline within behavior blocks

Functions
-- none: all logic is expressed directly in behavior rules

BEHAVIOR extract_lease_terms: Extract and classify lease terms from source document across all 25 DDD-defined sections

  RULE verbatim_financial:
    WHEN a financial value (rent, deposit, operating cost, tax amount) is found verbatim in the source document
    THEN status MUST be FACT
    AND provenance MUST include page number, clause reference, and verbatim quote
    AND the value MUST be extracted exactly as written in the source
    AND a normalized numeric form MUST be provided as a separate field
    AND the currency code MUST be included with every financial value

  RULE inferred_term:
    WHEN a lease term requires interpretation, calculation, or derivation from other terms
    THEN status MUST be INFERENCE
    AND confidence score MUST be provided between 0.0 and 1.0
    AND reasoning MUST explain how the value was derived
    AND if confidence < $config.confidence_review_threshold the field MUST be flagged for human review

  RULE missing_term:
    WHEN a DDD-defined field is not found anywhere in the source document
    THEN status MUST be MISSING
    AND the value field MUST be null (JSON) or "Not specified" (markdown)
    AND the agent MUST NOT fabricate a plausible value

  RULE conflict_detection:
    WHEN multiple conflicting values are found for the same field across different sections of the lease
    THEN status MUST be CONFLICT
    AND all conflicting values MUST be listed with individual provenance for each
    AND reasoning MUST explain the nature of the conflict and identify the source sections
    AND the conflict MUST NOT be silently resolved

  RULE schedule_override:
    WHEN a Schedule G (or equivalent special provisions schedule) contains a term that contradicts the main body of the lease
    THEN the Schedule G value MUST be used as the primary extracted value
    AND the main body value MUST be preserved in a separate override_note field
    AND status MUST be FACT with provenance pointing to the Schedule G reference
    AND a flag MUST indicate that a schedule override occurred

  RULE currency_detection:
    WHEN currency is not explicitly stated alongside a financial value in the source document
    THEN the agent MUST infer currency from jurisdiction clues in the document (address, governing law, province/state references)
    AND status MUST be INFERENCE with confidence score and reasoning
    AND the agent MUST NOT assume a default currency

  RULE date_normalization:
    WHEN a date is found in any format in the source document (written, numeric, partial)
    THEN the date MUST be normalized to ISO 8601 format (YYYY-MM-DD)
    AND the original date text MUST be preserved in the provenance verbatim_quote field
    AND status MUST be FACT if the date is unambiguous or INFERENCE if interpretation was required

  ERRORS:
  | name | when | severity | action | message |
  |------|------|----------|--------|---------|
  | fabricated_value | an extracted value cannot be traced to any text in the source document | critical | reject the extraction and flag for human review | "Extracted value has no source provenance — possible fabrication detected" |
  | parties_swapped | the landlord and tenant identities are reversed or misassigned in the output | critical | reject the extraction and require re-processing | "Landlord and tenant parties are misidentified or swapped — critical data integrity failure" |

  EXAMPLE standard_rent_extraction:
    INPUT: Lease document with clause 5.1 on page 12 stating "The Tenant shall pay base rent of $45.00 per square foot per annum"
    EXPECTED: value="$45.00 per square foot per annum", status=FACT, provenance={"page": 12, "section": "5.1", "verbatim_quote": "$45.00 per square foot per annum"}, normalized_value=45.00, normalized_unit="psf/annum"
    NOTES: Verbatim financial extraction with full provenance and normalized numeric form

  EXAMPLE conflicting_commencement:
    INPUT: Lease with "The Term shall commence on January 1, 2026" in clause 3.1 (page 8) and "Effective Date: March 1, 2026" in clause 1.2 (page 2)
    EXPECTED: status=CONFLICT, values=["2026-01-01", "2026-03-01"], provenance=[{"page": 8, "section": "3.1"}, {"page": 2, "section": "1.2"}], reasoning="Conflicting commencement dates found in clause 3.1 (January 1, 2026) and clause 1.2 (March 1, 2026)"
    NOTES: Conflicting dates across sections MUST be flagged as CONFLICT and never silently resolved

  EXAMPLE missing_renewal:
    INPUT: Lease document with no renewal clause, renewal option, or extension provision anywhere in the document
    EXPECTED: value=null, status=MISSING
    NOTES: Absent term produces MISSING status with null value — no fabrication of a plausible renewal term

  EXAMPLE schedule_g_rent_override:
    INPUT: Lease main body clause 5.1 states base rent of "$40.00 psf" but Schedule G item 3 states "Notwithstanding Section 5.1, the base rent for the first 24 months shall be $35.00 psf"
    EXPECTED: value="$35.00 psf", status=FACT, provenance={"page": 45, "section": "Schedule G, Item 3"}, override_note="Schedule G overrides clause 5.1 base rent from $40.00 psf to $35.00 psf for first 24 months", override_flag=true
    NOTES: Schedule G provisions take precedence over main body terms — the override MUST be flagged and both values preserved

BEHAVIOR validate_extraction: Validate extracted data for completeness, consistency, and compliance with hard constraints

  RULE completeness_check:
    WHEN extraction is complete for a document
    THEN all 25 DDD-defined sections MUST be present in the output
    AND each section MUST contain at least one field with a non-null status
    AND if more than $config.completeness_escalation_threshold of fields are MISSING the document MUST be flagged for escalation

  RULE provenance_integrity:
    WHEN a field has status FACT
    THEN provenance MUST NOT be null or empty
    AND provenance MUST include page number as an integer
    AND provenance MUST include section or clause reference as a string
    AND provenance MUST include a verbatim quote from the source text

  ERRORS:
  | name | when | severity | action | message |
  |------|------|----------|--------|---------|
  | missing_provenance | a FACT-status field lacks provenance metadata (page, clause, or verbatim quote) | critical | fail validation for this field and flag for correction | "FACT-status field requires complete provenance (page, clause, verbatim quote)" |
  | wrong_currency | a financial value is assigned an incorrect currency code that does not match the source document | critical | reject the financial extraction and flag for human review | "Financial value assigned wrong currency — source document currency does not match extracted currency" |
  | template_placeholder | the output contains an unresolved template placeholder such as "[Insert value]", "[TBD]", or "[PLACEHOLDER]" | critical | reject the output and require re-processing | "Template placeholder detected in output — all placeholders MUST be replaced with extracted values or null" |

  EXAMPLES:
    complete_extraction: all 25 sections present with non-null status -> valid
    incomplete_extraction: 10 of 25 sections MISSING (40%) -> flagged for escalation
    valid_provenance: FACT field with page=5, clause="3.1", quote="..." -> valid
    missing_provenance: FACT field with provenance=null -> critical error

Constraints
* Extraction MUST process all 25 DDD-defined sections before completion
* Every FACT-status field MUST carry provenance with page, clause, and verbatim quote
* Financial values MUST NOT be altered from source — extract verbatim with separate normalized field
* Currency MUST be determined from source document context, never assumed
* Dates MUST be normalized to ISO 8601 while preserving original text in provenance
* Output MUST conform to either JSON or Markdown contract as specified by caller
* Schedule G (or equivalent) overrides MUST be detected and flagged

Dependencies
* DDD reference: re-ddd:lease_abstraction_commercial_na@1.0.0
```

**Step 2: Run SESF validation on the updated spec**

```bash
reixs validate specs/templates/lease_abstraction_commercial_na.reixs.md --json 2>&1 | python -m json.tool | head -50
```

Expected: No SESF errors (warnings acceptable)

**Step 3: Commit**

```bash
git add specs/templates/lease_abstraction_commercial_na.reixs.md
git commit -m "feat: promote commercial NA SESF block from micro to standard tier

Add Notation, Scope, Inputs, Outputs, Types, Functions, Dependencies,
and @config sections. Convert ERROR blocks to compact ERRORS tables.
Thread \$config references for escalation and review thresholds."
```

---

### Task 4: Update README.md

**Files:**
- Modify: `README.md`

**Step 1: Update all v3 references**

Make these replacements in `README.md`:

1. Line 66: `SESF v3 rules` → `SESF v4 rules`
2. Line 73: `[SESF v3](https://github.com/reggiechan74/cc-plugins/tree/main/structured-english)` → `[SESF v4](https://github.com/reggiechan74/cc-plugins/tree/main/structured-english)`
3. Line 119: `standalone SESF v3 document` → `standalone SESF v4 document`
4. Line 121: `SESF v3 validator (~1,480 lines of pure Python)` → `SESF v4 validator (~2,140 lines of pure Python)`
5. Line 152: `SESF v3 behavior rules` → `SESF v4 behavior rules`

**Step 2: Commit**

```bash
git add README.md
git commit -m "docs: update README SESF references from v3 to v4"
```

---

### Task 5: Update REIXS-SPEC.md

**Files:**
- Modify: `docs/REIXS-SPEC.md`

**Step 1: Update v3 references**

1. Line 55: `Machine-parseable behavioral rules (SESF v3)` → `Machine-parseable behavioral rules (SESF v4)`
2. Lines 718-731: Replace "SESF v3 Quick Reference" section with expanded v4 version:

```markdown
#### SESF v4 Quick Reference

The SESF block uses a domain-specific language with these constructs:

| Construct | Syntax | Purpose |
|---|---|---|
| Meta (micro) | `Meta: Version X.Y.Z \| Date: YYYY-MM-DD \| Domain: ... \| Status: active \| Tier: micro` | Document metadata — pipe-delimited for micro tier |
| Meta (standard+) | Multi-line bullet format with `* Version:`, `* Date:`, etc. | Document metadata — multi-line for standard/complex tier |
| Notation | `Notation` section with `*` bullets defining `$`, `@`, `->`, keywords | Symbol glossary (required for standard/complex tier) |
| BEHAVIOR | `BEHAVIOR name: description` | Named behavior declaration |
| RULE | `RULE name:` then `WHEN` / `THEN` / `AND` clauses | Conditional rule within a behavior |
| ERROR | `ERROR name:` then `WHEN` / `SEVERITY` / `ACTION` / `MESSAGE` clauses | Error handling rule |
| ERRORS: table | Compact 5-column table: name, when, severity, action, message | Compact error table (2+ error cases) |
| EXAMPLE | `EXAMPLE name:` then `INPUT:` / `EXPECTED:` / `NOTES:` | Test example for validation |
| EXAMPLES: | `name: input_description -> expected_outcome` | Compact example format |
| @config | `@config` block with `key: value` entries | Centralized static parameters |
| @route | `@route name [mode]` with `condition -> outcome` rows | Decision table (3+ branches) |
| $variable | `STEP name -> $var` / `$config.key` | Variable threading and config references |
| Constraints | `Constraints` header then `* item` bullets | Operational constraints within SESF |

For the full SESF v4 specification, see: https://github.com/reggiechan74/cc-plugins/tree/main/structured-english
```

**Step 2: Commit**

```bash
git add docs/REIXS-SPEC.md
git commit -m "docs: update REIXS-SPEC SESF references from v3 to v4

Expand Quick Reference table with v4 constructs: @config, @route,
\$variable threading, compact ERRORS/EXAMPLES tables, Notation section,
and multi-line Meta format."
```

---

### Task 6: Update TUTORIAL.md

**Files:**
- Modify: `docs/TUTORIAL.md`

**Step 1: Check and update v3 references**

The tutorial doesn't explicitly mention "v3" but references SESF concepts. No text changes needed — the tutorial describes SESF constructs generically (BEHAVIOR, RULE, ERROR, EXAMPLE, Meta) which are valid in both v3 and v4.

Verify by searching:

```bash
grep -n "v3\|v4" docs/TUTORIAL.md
```

Expected: No matches (tutorial doesn't mention version numbers)

**Step 2: Skip commit if no changes needed**

---

### Task 7: Update historical plan docs

**Files:**
- Modify: `docs/plans/2026-03-01_REIXS.md`
- Modify: `docs/plans/2026-03-01-reixs-design.md`
- Modify: `docs/plans/2026-03-01-reixs-implementation.md`
- Modify: `docs/plans/2026-03-01-reixs-format-spec-design.md`
- Modify: `docs/plans/2026-03-01-reixs-format-spec-implementation.md`

**Step 1: Find and replace all SESF v3 references**

For each file, replace:
- `SESF v3` → `SESF v4`
- `sesf v3` → `sesf v4` (case-insensitive check, but keep original casing pattern)

Use `sed` for batch replacement across all plan docs:

```bash
sed -i 's/SESF v3/SESF v4/g' docs/plans/2026-03-01_REIXS.md docs/plans/2026-03-01-reixs-design.md docs/plans/2026-03-01-reixs-implementation.md docs/plans/2026-03-01-reixs-format-spec-design.md docs/plans/2026-03-01-reixs-format-spec-implementation.md
```

**Step 2: Verify replacements**

```bash
grep -r "SESF v3" docs/plans/
```

Expected: No matches

**Step 3: Commit**

```bash
git add docs/plans/
git commit -m "docs: update SESF v3 references to v4 across plan documents"
```

---

### Task 8: Regenerate golden test files

**Files:**
- Regenerate: `tests/golden/valid_report.json`
- Regenerate: `tests/golden/valid_runtime.json` (if affected)

**Step 1: Run the full test suite to identify failures**

```bash
pytest tests/ -v 2>&1 | tail -30
```

Expected: Golden file comparison tests may fail because the v4 validator produces additional findings (notation checks, type consistency, rule integrity, cross-behavior checks, config references, variable threading, route completeness, error table structure).

**Step 2: Regenerate golden files**

Run the validation on the Ontario spec (which the golden file is based on) and capture the new output:

```bash
reixs validate specs/templates/lease_abstraction_ontario.reixs.md --json > tests/golden/valid_report.json
```

For the runtime JSON:
```bash
reixs compile specs/templates/lease_abstraction_ontario.reixs.md -o /tmp/golden_regen/ --include-validation && cp /tmp/golden_regen/reixs.runtime.json tests/golden/valid_runtime.json
```

**Step 3: Review the diff to confirm changes are expected**

```bash
git diff tests/golden/
```

Expected: New SESF findings from the additional checks (type_consistency, rule_integrity, cross_behavior, and v4 checks). No findings should change from info/warning to error for the existing micro-tier Ontario spec.

**Step 4: Run the full test suite**

```bash
pytest tests/ -v
```

Expected: All tests PASS

**Step 5: Commit**

```bash
git add tests/golden/
git commit -m "test: regenerate golden files for SESF v4 validator output"
```

---

### Task 9: Final verification

**Step 1: Run full test suite**

```bash
pytest tests/ -v
```

Expected: All tests PASS

**Step 2: Validate both spec templates**

```bash
reixs validate specs/templates/lease_abstraction_ontario.reixs.md
reixs validate specs/templates/lease_abstraction_commercial_na.reixs.md
```

Expected: Both pass validation (warnings acceptable, no errors)

**Step 3: Verify no stale v3 references remain in source code**

```bash
grep -rn "SESF v3\|sesf v3" src/ tests/ README.md docs/REIXS-SPEC.md docs/TUTORIAL.md
```

Expected: No matches

**Step 4: Verify v3 references are gone from plan docs**

```bash
grep -rn "SESF v3" docs/plans/
```

Expected: No matches
