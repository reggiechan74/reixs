# Design: SESF v3→v4 Migration

**Date:** 2026-03-03
**Status:** approved
**Approach:** Drop-In Replacement (Approach A)

## Context

The structured-english plugin has been updated from SESF v3 to SESF v4. The reixs-specification repo vendors a copy of the v3 validator and references "SESF v3" throughout documentation, adapter code, and embedded SESF blocks. This design covers migrating everything to v4.

### What changed in SESF v4

**New data models:** `SESFConfig`, `SESFConfigEntry`, `SESFRoute`, `SESFRouteRow`, `SESFCompactError`, `SESFCompactExample`.

**New fields on existing models:** `routes`, `compact_errors`, `compact_examples` on `SESFBehavior`; `output_variables` on `SESFStep`; `config` and `has_notation_section` on `SESFDocument`.

**New KNOWN_SECTIONS:** `notation`, `procedures` added.

**5 new validation functions:**
1. `check_config_references()` — validates `@config` / `$config.key` consistency
2. `check_variable_threading()` — validates `$variable` produce-before-use
3. `check_route_completeness()` — validates `@route` tables (wildcard default, min branches)
4. `check_error_table_structure()` — validates compact `ERRORS:` tables (5 mandatory columns)
5. `check_notation_section()` — warns if standard/complex tier missing Notation section

All 6 v3 functions are preserved with identical signatures.

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Migration approach | Drop-in replacement | v4 is a strict superset of v3 with identical function signatures |
| Check selection | Configurable with all-by-default | Users can opt out of specific checks without forking the adapter |
| Ontario SESF tier | Keep micro | 1 behavior = micro per v4 tier rules |
| Commercial NA SESF tier | Promote to standard | 2 behaviors, 9 rules = standard per v4 tier rules |
| Historical plan docs | Update all v3 references | User preference for consistency over historical accuracy |

## Section 1: Validator Replacement

Replace `src/reixs/sesf/validate_sesf.py` (1,482 lines, v3-only) with the v4 validator from the structured-english plugin (2,141 lines, v3/v4 compatible).

The v4 validator is backward-compatible: it handles v3-format specs without errors. The file is a strict superset — same function signatures for all 6 v3 functions plus 5 new ones.

No other source files import from `validate_sesf.py` directly — only the adapter does.

## Section 2: Adapter Update

Update `src/reixs/sesf/adapter.py`:

1. **Imports** — Add all 11 check functions:
   - v3: `check_structural_completeness`, `check_error_consistency`, `check_example_consistency`, `check_type_consistency`, `check_rule_integrity`, `check_cross_behavior`
   - v4: `check_config_references`, `check_variable_threading`, `check_route_completeness`, `check_error_table_structure`, `check_notation_section`

2. **Configurable check selection** — Add a `checks` parameter to `validate_sesf_block()` that accepts a list of check function references. Defaults to all 11. Callers can pass a subset to opt out.

3. **Message strings** — Update "SESF v3" → "SESF v4" in error messages and suggestions.

4. **Default behavior** — All 11 checks run by default. The orchestrator in `validate/__init__.py` calls the adapter without specifying checks (gets all 11).

## Section 3: Spec Tier Promotion

### Ontario spec (keep micro)

`specs/templates/lease_abstraction_ontario.reixs.md` — 1 behavior, 5 rules. Stays micro per v4 tier rules. No structural changes needed to the SESF block.

### Commercial NA spec (promote to standard)

`specs/templates/lease_abstraction_commercial_na.reixs.md` — 2 behaviors, 9 rules. Promote SESF block from micro to standard tier.

**Required additions for standard tier:**
- Change Meta from pipe-delimited single-line to multi-line bullet format
- Change `Tier: micro` to `Tier: standard`
- Add Notation section (after Meta)
- Add Scope section (IN SCOPE / OUT OF SCOPE)
- Add Inputs section
- Add Outputs section
- Add Types section (or `-- none` stub)
- Add Functions section (or `-- none` stub)
- Add Dependencies section

## Section 4: Documentation Updates

### README.md
- Update all "SESF v3" → "SESF v4" (lines 66, 73, 119, 121, 152)
- Update validator line count from ~1,480 to ~2,140

### REIXS-SPEC.md
- Update "SESF v3" → "SESF v4" (lines 55, 718, 731)
- Expand "SESF v3 Quick Reference" to "SESF v4 Quick Reference" — add v4 constructs: @config, @route, $variable threading, compact error/example tables, Notation section requirement

### TUTORIAL.md
- Check and update any v3 references

### docs/plans/*.md
- Find/replace all "SESF v3" → "SESF v4" across all plan documents

## Section 5: Test Updates

### Golden files
Regenerate `tests/golden/valid_report.json` and `tests/golden/valid_runtime.json` after the validator update. The v4 validator produces additional findings (notation checks, etc.).

### Adapter tests
- Update `tests/test_sesf_adapter.py`:
  - Add test for configurable `checks` parameter
  - Add test fixture with v4 features (@config, @route, $variable, compact tables)
  - Add test verifying v4 checks produce expected findings

### Regression
- Run full test suite to verify no regressions from the validator swap
