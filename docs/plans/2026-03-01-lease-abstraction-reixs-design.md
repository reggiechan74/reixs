# REIXS Lease Abstraction Spec — Design Document

**Goal:** Convert the existing slash command at `reggiechan74/vp-real-estate/.claude/commands/Abstraction/abstract-lease.md` into a REIXS-compliant execution specification for commercial lease abstraction.

**Approach:** Hybrid — the REIXS spec governs extraction behavior (what to extract, provenance requirements, conflict handling, field status). The slash command remains the orchestrator (file I/O, lease type detection, output formatting, file saving). This separates *what the agent must do* (spec) from *how the workflow runs* (command).

**Key decisions:**
- Tier: complex (24 sections, dual output, provenance, conflict detection)
- Jurisdiction: North America (agnostic — DDD defines jurisdiction-neutral field set)
- Output: Dual contracts (JSON data extraction + markdown summary) in a single spec
- Scope boundary: REIXS spec covers extraction rules; slash command covers orchestration

---

## Spec Structure

### Meta

```
Spec ID: REIXS-LA-NA-001
Version: 1.0.0
Task Type: Lease Abstraction
Tier: complex
Author: Reggie Chan
Date: 2026-03-01
```

### Objective

Extract structured lease terms from a commercial lease document (any North American jurisdiction) across 24 standardized sections, producing field-level output with provenance and status tracking in both JSON and markdown formats.

### Domain Context

- Jurisdiction: North America
- Currency: determined from source document (no default)
- Area Unit: sq ft (default), sq m (accepted)
- DDD Reference: `re-ddd:lease_abstraction_commercial_na@1.0.0`
- ADR References: ADR-001, ADR-003, ADR-004

ADR-004 (new): Documents the decision to use dual output contracts in a single spec rather than separate specs per format.

### Inputs

- Source document: PDF, DOCX, or Markdown (scanned or native)
- Document type: Commercial lease agreement (office or industrial)
- Expected length: 5-200 pages
- Output format preference: JSON (default) or Markdown (specified by caller)

### OFD

#### 5 Mandatory (all tiers)

**Primary Objective:**
Extract all 24 lease sections defined in the DDD with factual accuracy >= 95%, provenance on every FACT-status field, and explicit status tracking on every extracted value.

**Hard Constraints:**
- NEVER fabricate a term not present in the source document
- NEVER silently resolve conflicting provisions — flag as CONFLICT with all sources cited
- ALL FACT-status fields MUST carry provenance (page number, clause/section reference)
- NEVER alter financial figures — extract verbatim, add normalized form as separate field
- Quote specific section/article numbers when referencing lease provisions
- Use "Not specified" (markdown) or null (JSON) for absent terms, never leave template placeholders

**AutoFail Conditions:**
- Any fabricated lease term (value not traceable to source text)
- Parties (landlord/tenant) misidentified or swapped
- Commencement or expiry date extracted without provenance
- Financial term assigned wrong currency
- Template placeholder left in output (e.g., "[Insert value]")

**Optimization Priority Order:**
1. Factual correctness — no fabricated or hallucinated values
2. Completeness — extract every DDD-defined field present in the source
3. Provenance quality — every FACT value traceable to specific page and clause
4. Normalization consistency — dates (ISO 8601), currencies, units in standard format
5. Formatting — consistent style across output

**Uncertainty Policy:**
When a term is ambiguous or not explicitly stated, mark as INFERENCE with confidence 0.0-1.0 and reasoning. If confidence < 0.5, flag for human review. For terms that are absent from the source document, mark as MISSING with null value. Never guess — prefer MISSING over a plausible but unverified value.

#### 5 Tier-Dependent (required for complex)

**Secondary Objectives:**
- Identify unusual or non-standard lease provisions
- Flag Schedule G (or equivalent special provisions) overrides of main body terms
- Detect related-party transactions (landlord/tenant at same address, shared officers)
- Calculate derived values where requested (proportionate share, total cost over term)

**Tradeoff Policies:**
- Accuracy over completeness: skip a field rather than guess its value
- Verbatim over normalized: when normalization loses information, preserve source form and add normalized alternative
- MISSING over INFERENCE: when confidence < 0.3, use MISSING rather than low-confidence INFERENCE
- Conciseness over exhaustiveness (markdown): top 5-7 items per risk category, not comprehensive lists

**Scoring Model:**
- Critical sections (Parties, Premises, Term, Rent): 2x weight
- Factual accuracy: 40% — percentage of extracted values that are correct
- Completeness: 25% — percentage of DDD fields successfully extracted
- Provenance coverage: 20% — percentage of FACT values with valid source references
- Normalization: 10% — percentage of values in standard format
- Confidence calibration: 5% — correlation between confidence scores and actual accuracy

**Escalation Triggers:**
- Document language is not English or French
- More than 30% of DDD fields marked MISSING
- Document exceeds 200 pages
- More than 3 fields marked CONFLICT in a single document
- Confidence < 0.5 on any critical field (commencement, expiry, rent, parties)

**Error Severity Model:**
- critical: fabricated term, wrong currency, wrong dates, misidentified parties, template placeholder in output
- high: missing critical field without MISSING flag, provenance gap on financial term, Schedule G override not flagged
- medium: formatting inconsistency, low-confidence INFERENCE not flagged for review, missing non-critical field
- low: minor normalization differences, whitespace issues, optional field not extracted

### Constraints

- Processing time: < 120 seconds per document (< 60 for documents under 50 pages)
- Output format: JSON or Markdown (determined by caller, not by spec)
- Offline processing: no external API calls during extraction
- File size targets: 50-60KB for JSON, 30-40KB for Markdown

### Output Contract

#### JSON Output

The output is a JSON object with 24 top-level section keys. Each extracted field within a section includes:

- `value`: the extracted or derived value (proper JSON types: numbers, strings, booleans, arrays, null)
- `status`: FACT | INFERENCE | MISSING | CONFLICT
- `provenance`: `{ "page": int, "section": string, "verbatim_quote": string }` — required for FACT status
- `confidence`: 0.0-1.0 — required for INFERENCE status
- `reasoning`: string — required for INFERENCE and CONFLICT status

Top-level sections follow the 24-section DDD schema:
1. documentInformation, 2. parties, 3. premises, 4. term, 5. rent,
6. depositsAndSecurity, 7. operatingCostsAndTaxes, 8. useAndOperations,
9. maintenanceAndRepairs, 10. alterationsAndImprovements, 11. insuranceAndIndemnity,
12. damageAndDestruction, 13. assignmentAndSubletting, 14. defaultAndRemedies,
15. servicesAndUtilities, 16. environmental, 17. subordinationAndAttornment,
18. notices, 19. endOfTerm, 20. specialProvisions, 21. schedulesAndExhibits,
22. criticalDatesSummary, 23. financialObligationsSummary, 24. keyIssuesAndRisks

Numeric values stored as numbers (not strings). Dates as ISO 8601 strings. Booleans as true/false. Missing values as null (not ""). Lists as arrays.

#### Markdown Output

Structured markdown document containing:
- Executive Summary (3-5 sentences: property, parties, term, rent, key provisions)
- Key Terms at a Glance (critical facts as concise bullets)
- 24 sections as concise bullet points with inline status indicators: `[FACT]`, `[INFERRED]`, `[MISSING]`
- Critical Dates Summary (table format)
- Financial Obligations Summary (table format)
- Key Issues & Risks (top 5 critical, top 5-7 favorable, top 5-7 unfavorable, top 10 review items)

Status indicators appear after each extracted value so the reader knows what's verified versus inferred.

### Evaluation / EDD

- EDD Suite ID: edd:lease_abstraction_commercial_v1
- Minimum pass rate: 95%
- Zero tolerance: critical-severity errors
- Regression cases: basic_office_lease, basic_industrial_lease, conflicting_provisions, missing_sections, schedule_g_override, related_party_transaction, multi_currency_lease

### Behavior Spec (SESF)

The SESF block defines rules for:

**Extraction behaviors:**
- verbatim_financial: financial values found verbatim → FACT + provenance
- inferred_term: terms requiring interpretation → INFERENCE + confidence + reasoning
- missing_term: DDD field not in source → MISSING + null value
- conflict_detection: multiple conflicting values → CONFLICT + all sources + reasoning
- schedule_override: Schedule G contradicts main body → flag, use Schedule G value
- currency_detection: currency not explicit → INFERENCE based on jurisdiction clues
- date_normalization: dates in any format → normalize to ISO 8601, preserve original in provenance

**Error conditions:**
- fabricated_value: SEVERITY critical
- parties_swapped: SEVERITY critical
- missing_provenance: SEVERITY critical (FACT without provenance)
- wrong_currency: SEVERITY critical
- template_placeholder: SEVERITY critical

**Test examples:**
- standard_rent_extraction: rent on page 5 → FACT with provenance
- conflicting_commencement: two dates in different sections → CONFLICT
- missing_renewal: no renewal clause → MISSING
- schedule_g_rent_override: Schedule G modifies base rent → use Schedule G, flag override

### Validation Checklist

- [ ] All 24 DDD-defined sections addressed in output contract
- [ ] Hard constraints are machine-checkable (no subjective rules)
- [ ] AutoFail conditions have corresponding SESF ERROR blocks
- [ ] SESF rules cover extraction, conflict, missing-value, and override scenarios
- [ ] Both output contracts (JSON and Markdown) define status/provenance requirements
- [ ] Escalation triggers have clear thresholds
- [ ] Critical sections (parties, premises, term, rent) identified for scoring weight
- [ ] EDD suite references at least 5 regression cases
- [ ] ADR-004 documents dual output format decision

---

## What Changes in the Slash Command

After the REIXS spec is written, the slash command would be updated to:

1. **Load the compiled REIXS runtime JSON** at startup (objective, hard constraints, SESF rules)
2. **Inject the runtime payload** into the agent prompt alongside the document
3. **Keep ownership of:** file I/O, lease type detection (industrial/office template selection), DOCX→MD conversion, output file naming and saving
4. **Delegate to the spec:** extraction rules, provenance requirements, status tracking, conflict detection, quality thresholds

The slash command becomes a ~50-line orchestrator instead of a ~300-line monolith.

## Scope Boundary

| Concern | Owned by REIXS spec | Owned by slash command |
|---|---|---|
| What 24 sections to extract | Yes | No |
| Field-level provenance rules | Yes | No |
| FACT/INFERENCE/MISSING/CONFLICT status | Yes | No |
| Hard constraints and autofail | Yes | No |
| File loading (PDF/DOCX/URL) | No | Yes |
| Lease type detection (office/industrial) | No | Yes |
| Template selection | No | Yes |
| Output file naming and saving | No | Yes |
| `-json` flag parsing | No | Yes |
| DOCX to Markdown conversion | No | Yes |
