# REIXS: Lease Abstraction — North American Commercial

## Meta

- Spec ID: REIXS-LA-NA-001
- Version: 1.0.0
- Task Type: Lease Abstraction
- Tier: complex
- Author: Reggie Chan
- Date: 2026-03-01

## Objective

Extract structured lease terms from a commercial lease document (any North American jurisdiction) across 25 standardized sections, producing field-level output with provenance and status tracking in both JSON and markdown formats.

## Domain Context

- Jurisdiction: North America
- Area Unit: sq ft (default), sq m (accepted)
- DDD Reference: re-ddd:lease_abstraction_commercial_na@2.0.0
- ADR References: ADR-001, ADR-003, ADR-004

## Inputs

- Source document: PDF, DOCX, or Markdown (scanned or native)
- Document type: Commercial lease agreement (office or industrial)
- Expected length: 5-200 pages
- Output format preference: JSON (default) or Markdown (specified by caller)

## Objective Function Design (OFD)

### Primary Objective
Extract all 25 lease sections defined in the DDD with factual accuracy >= 95%, provenance on every FACT-status field, and explicit status tracking on every extracted value.

### Hard Constraints
- NEVER fabricate a term not present in the source document
- NEVER silently resolve conflicting provisions — flag as CONFLICT with all sources cited
- ALL FACT-status fields MUST carry provenance (page number, clause/section reference)
- NEVER alter financial figures — extract verbatim, add normalized form as separate field
- Quote specific section/article numbers when referencing lease provisions
- Use "Not specified" (markdown) or null (JSON) for absent terms, never leave template placeholders
- Currency MUST be determined from the source document — no default currency assumed

### AutoFail Conditions
- Any fabricated lease term (value not traceable to source text)
- Parties (landlord/tenant) misidentified or swapped
- Commencement or expiry date extracted without provenance
- Financial term assigned wrong currency
- Template placeholder left in output (e.g., "[Insert value]")

### Optimization Priority Order
1. Factual correctness — no fabricated or hallucinated values
2. Completeness — extract every DDD-defined field present in the source
3. Provenance quality — every FACT value traceable to specific page and clause
4. Normalization consistency — dates (ISO 8601), currencies, units in standard format
5. Formatting — consistent style across output

### Uncertainty Policy
When a term is ambiguous or not explicitly stated, mark as INFERENCE with confidence 0.0-1.0 and reasoning. If confidence < 0.5, flag for human review. For terms that are absent from the source document, mark as MISSING with null value. Never guess — prefer MISSING over a plausible but unverified value. When confidence < 0.3, use MISSING rather than low-confidence INFERENCE.

### Secondary Objectives
- Identify unusual or non-standard lease provisions
- Flag Schedule G (or equivalent special provisions) overrides of main body terms
- Detect related-party transactions (landlord/tenant at same address, shared officers)
- Calculate derived values where requested (proportionate share, total cost over term)

### Tradeoff Policies
- Accuracy over completeness: skip a field rather than guess its value
- Verbatim over normalized: when normalization loses information, preserve source form and add normalized alternative
- MISSING over INFERENCE: when confidence < 0.3, use MISSING rather than low-confidence INFERENCE
- Conciseness over exhaustiveness (markdown): top 5-7 items per risk category, not comprehensive lists

### Scoring Model
- Critical sections (Parties, Premises, Term, Rent): 2x weight
- Factual accuracy: 40% — percentage of extracted values that are correct
- Completeness: 25% — percentage of DDD fields successfully extracted
- Provenance coverage: 20% — percentage of FACT values with valid source references
- Normalization: 10% — percentage of values in standard format
- Confidence calibration: 5% — correlation between confidence scores and actual accuracy

### Escalation Triggers
- Document language is not English or French
- More than 30% of DDD fields marked MISSING
- Document exceeds 200 pages
- More than 3 fields marked CONFLICT in a single document
- Confidence < 0.5 on any critical field (commencement, expiry, rent, parties)

### Error Severity Model
- critical: fabricated term, wrong currency, wrong dates, misidentified parties, template placeholder in output
- high: missing critical field without MISSING flag, provenance gap on financial term, Schedule G override not flagged
- medium: formatting inconsistency, low-confidence INFERENCE not flagged for review, missing non-critical field
- low: minor normalization differences, whitespace issues, optional field not extracted

## Constraints

- Processing time: < 120 seconds per document (< 60 for documents under 50 pages)
- Output format: JSON or Markdown (determined by caller, not by spec)
- Offline processing: no external API calls during extraction
- File size targets: 50-60KB for JSON, 30-40KB for Markdown

## Output Contract

Each extracted field MUST include the following attributes with provenance and status tracking. The output is structured across 25 top-level sections following the DDD schema: (1) documentInformation, (2) parties, (3) premises, (4) term, (5) rent, (6) depositsAndSecurity, (7) operatingCostsAndTaxes, (8) useAndOperations, (9) maintenanceAndRepairs, (10) alterationsAndImprovements, (11) insuranceAndIndemnity, (12) damageAndDestruction, (13) assignmentAndSubletting, (14) defaultAndRemedies, (15) servicesAndUtilities, (16) environmental, (17) subordinationAndAttornment, (18) notices, (19) endOfTerm, (20) specialProvisions, (21) schedulesAndExhibits, (22) criticalDates, (23) financialObligations, (24) keyIssuesAndRisks, (25) notesAndComments.

JSON output uses proper JSON types: numbers for numeric values, strings for text and ISO 8601 dates, booleans for true/false, arrays for lists, null for missing values. Markdown output uses inline status indicators [FACT], [INFERRED], [MISSING] after each extracted value, with an Executive Summary, Key Terms at a Glance, 25 section bullet points, Critical Dates table, Financial Obligations table, and Key Issues & Risks section.

- `value`: the extracted or derived value (proper JSON types or markdown text)
- `status`: FACT | INFERENCE | MISSING | CONFLICT
- `provenance`: { "page": int, "section": string, "verbatim_quote": string } — required for FACT status
- `confidence`: 0.0-1.0 — required for INFERENCE status
- `reasoning`: string — required for INFERENCE and CONFLICT status

## Evaluation / EDD

- EDD Suite ID: edd:lease_abstraction_commercial_v1
- Minimum pass rate: 95%
- Zero tolerance: critical-severity errors
- Regression cases: basic_office_lease, basic_industrial_lease, conflicting_provisions, missing_sections, schedule_g_override, related_party_transaction, multi_currency_lease

## Behavior Spec (SESF)

```sesf
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
* DDD reference: re-ddd:lease_abstraction_commercial_na@2.0.0
```

## Validation Checklist

- [ ] All 25 DDD-defined sections addressed in output contract
- [ ] Hard constraints are machine-checkable (no subjective rules)
- [ ] AutoFail conditions have corresponding SESF ERROR blocks
- [ ] SESF rules cover extraction, conflict, missing-value, and override scenarios
- [ ] Both output contracts (JSON and Markdown) define status/provenance requirements
- [ ] Escalation triggers have clear thresholds
- [ ] Critical sections (parties, premises, term, rent) identified for scoring weight
- [ ] EDD suite references at least 5 regression cases
- [ ] ADR-004 documents dual output format decision
