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

## Validation Checklist

- [ ] All DDD-defined fields addressed in output contract
- [ ] Hard constraints are machine-checkable
- [ ] AutoFail conditions have corresponding test fixtures
- [ ] SESF rules cover extraction, conflict, and missing-value scenarios
- [ ] Ontario jurisdiction metadata (currency, units) declared
- [ ] EDD suite ID references at least 3 test cases
