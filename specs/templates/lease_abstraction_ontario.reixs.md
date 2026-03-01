# REIXS: Lease Abstraction — Ontario Commercial

## Meta

- Spec ID: REIXS-LA-ON-001
- Version: 1.0.0
- Task Type: Lease Abstraction
- Tier: standard
- Author: Reggie Chan
- Date: 2026-03-01

## Objective

Extract structured lease terms from a commercial lease document (Ontario jurisdiction)
and produce a normalized term sheet with field-level provenance.

## Domain Context

- Jurisdiction: Ontario, Canada
- Currency: CAD
- Area Unit: sq ft (default), sq m (accepted)
- DDD Reference: re-ddd:lease_core_terms_ontario@0.1.0
- ADR References: ADR-001, ADR-003

## Inputs

- Source document: PDF (scanned or native)
- Document type: Commercial lease agreement
- Expected length: 5-200 pages

## Objective Function Design (OFD)

### Primary Objective
Extract all lease terms defined in DDD with factual accuracy >= 98%.

### Hard Constraints
- NEVER fabricate a term not present in the source document
- NEVER silently resolve conflicting dates — flag as CONFLICT
- ALL extracted values MUST carry provenance (page, clause, verbatim quote)
- Currency MUST be CAD unless explicitly stated otherwise in source

### AutoFail Conditions
- Any fabricated term (not traceable to source text)
- Missing commencement_date without MISSING status flag
- Provenance absent on any FACT-status field

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
- Prefer MISSING over GUESS — an empty field with MISSING status is better than a plausible but unverified value
- Prefer verbatim extraction over normalized form when normalization is lossy

### Scoring Model
- Weighted F1: precision weight 0.7, recall weight 0.3
- Critical fields (commencement, expiry, rent): 2x weight

### Escalation Triggers
- Confidence < 0.6 on any critical field
- More than 3 fields marked CONFLICT in single document
- Document language is not English

### Error Severity Model
- critical: fabricated term, wrong currency, wrong dates
- high: missing critical field without flag, provenance gap
- medium: formatting inconsistency, missing non-critical field
- low: minor normalization differences, whitespace issues

## Constraints

- Processing time: < 120 seconds per document
- Output format: JSON conforming to lease_abstraction_output_v1.json schema
- No external API calls during extraction (offline-capable)

## Output Contract

Each extracted field MUST include:
- `value`: the extracted or derived value
- `status`: FACT | INFERENCE | MISSING | CONFLICT
- `provenance`: { page, clause, verbatim_quote } (required for FACT status)
- `confidence`: 0.0-1.0 (required for INFERENCE status)
- `reasoning`: string (required for INFERENCE and CONFLICT status)

## Evaluation / EDD

- EDD Suite ID: edd:lease_abstraction_core_v1
- Minimum pass rate: 95%
- Zero tolerance: critical-severity errors
- Regression cases: basic_valid_case, conflicting_dates_case, missing_commencement_case

## Behavior Spec (SESF)

```sesf
Lease Term Extraction Rules

Meta: Version 1.0.0 | Date: 2026-03-01 | Domain: Lease Abstraction | Status: active | Tier: micro

Purpose
Define extraction, conflict detection, and provenance rules for commercial lease term extraction.

BEHAVIOR extract_lease_terms: Extract and classify lease terms from source document

  RULE verbatim_extraction:
    WHEN a field value is found verbatim in the source document
    THEN status MUST be FACT
    AND provenance MUST include page number, clause reference, and verbatim quote

  RULE inference_handling:
    WHEN a field value requires interpretation or calculation
    THEN status MUST be INFERENCE
    AND confidence score MUST be provided (0.0 to 1.0)
    AND reasoning MUST explain how the value was derived

  RULE missing_field:
    WHEN a DDD-defined field is not found in the source document
    THEN status MUST be MISSING
    AND the value field MUST be null
    AND the agent MUST NOT fabricate a value

  RULE conflict_detection:
    WHEN multiple conflicting values are found for the same field
    THEN status MUST be CONFLICT
    AND all conflicting values MUST be listed with individual provenance
    AND reasoning MUST explain the nature of the conflict

  RULE currency_default:
    WHEN currency is not explicitly stated in the source document
    THEN assume CAD for Ontario jurisdiction leases

  ERROR fabricated_value:
    WHEN an extracted value cannot be traced to source text
    SEVERITY critical
    ACTION reject the extraction and flag for human review
    MESSAGE "Extracted value has no source provenance — possible fabrication"

  ERROR missing_provenance:
    WHEN a FACT-status field lacks provenance metadata
    SEVERITY critical
    ACTION fail validation for this field
    MESSAGE "FACT-status field requires provenance (page, clause, verbatim quote)"

  EXAMPLE standard_extraction:
    INPUT: lease document with commencement date "January 1, 2026" on page 3, clause 2.1
    EXPECTED: { "value": "2026-01-01", "status": "FACT", "provenance": { "page": 3, "clause": "2.1", "verbatim_quote": "January 1, 2026" } }
    NOTES: Clear verbatim extraction with full provenance

  EXAMPLE conflicting_dates:
    INPUT: lease with "commencing January 1, 2026" in clause 2.1 and "effective March 1, 2026" in clause 5.3
    EXPECTED: { "status": "CONFLICT", "values": ["2026-01-01", "2026-03-01"], "reasoning": "Conflicting commencement dates in clauses 2.1 and 5.3" }
    NOTES: Conflicting dates MUST be flagged, never silently resolved

  EXAMPLE missing_term:
    INPUT: lease document with no operating cost provisions
    EXPECTED: { "value": null, "status": "MISSING" }
    NOTES: Missing field with MISSING status — no fabrication

Constraints
* Extraction MUST process all fields defined in DDD reference before completion
```

## Validation Checklist

- [ ] All DDD-defined fields addressed in output contract
- [ ] Hard constraints are machine-checkable
- [ ] AutoFail conditions have corresponding test fixtures
- [ ] SESF rules cover extraction, conflict, and missing-value scenarios
- [ ] Ontario jurisdiction metadata (currency, units) declared
- [ ] EDD suite ID references at least 3 test cases
