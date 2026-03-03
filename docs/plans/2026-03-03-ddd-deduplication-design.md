# DDD Deduplication Design — v2.0.0 Migration

**Date:** 2026-03-03
**Status:** Approved
**Scope:** Eliminate 48 exact-name field duplicates and 19 semantic duplicate groups across 7 DDD files.

---

## Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Party representation | Option A: `party.{role}.fieldName` dot notation | Domain DDDs reference specific roles (landlord, tenant, broker) with full traceability to core |
| Shared market fields | Add to core (not a separate DDD) | Simpler — one shared DDD to reference |
| Cross-reference syntax | Pointer rows in domain tables | Domain DDDs remain self-contained and readable; each field row shows `→ core@2.0.0 → section.field` |
| Contextual variants | Domain variants reference core base field | e.g., `goingInCapRate` → `core@2.0.0 → capRate` — at acquisition |
| Versioning | Major bump all DDDs to 2.0.0 | Field renames and restructuring = breaking change |
| Execution approach | Core-first, top-down | Build complete core v2.0.0 first, then update domains |

---

## Core v2.0.0 Changes

### Existing Sections (updated)

**Section 4: parties** — Restructured to role-qualified dot notation:

```
| Field                     | Type   | Description                                         |
|---------------------------|--------|-----------------------------------------------------|
| party.{role}.name         | string | Full legal name of the entity                       |
| party.{role}.entityType   | string | Corporation, LLC, LP, REIT, individual, trust, etc. |
| party.{role}.address      | string | Registered/principal address                        |
| party.{role}.contactName  | string | Primary contact person                              |
| party.{role}.contactPhone | string | Contact phone number                                |
| party.{role}.contactEmail | string | Contact email address                               |
| party.{role}.taxId        | string | Tax identification number (EIN, BN, etc.)           |

Standard roles: owner, landlord, tenant, manager, broker, lender, appraiser, counsel
```

**Section 2: financialFundamentals** — `effectiveGrossIncome` definition updated to USPAP standard: "Potential gross income minus vacancy and credit loss plus other income."

### New Sections

**Section 9: marketContext** (~22 fields)

Shared market study fields previously duplicated between Investment and Appraisal:

- MSA/submarket: `msaName`, `submarketDefinition`
- Demographics: `population`, `populationGrowthHistoricalPercent`, `populationGrowthProjectedPercent`, `medianHouseholdIncome`
- Employment: `employmentTotal`, `employmentBySector`, `unemploymentRatePercent`, `majorEmployers`
- Supply: `supplyTotalInventorySF`, `supplyVacancyRatePercent`, `supplyAvailabilityRatePercent`
- Demand: `demandNetAbsorptionAnnualSF`
- Rental trends: `rentalRateTrendAsking`, `rentalRateTrendEffective`, `concessionTrends`
- Construction: `constructionUnderConstructionSF`, `constructionPlannedSF`
- Forecasts: `forecastVacancy`, `forecastRentGrowth`

**Section 10: occupancyAndVacancy** (~5 fields)

- `occupancyRatePhysical`, `occupancyRateEconomic`, `occupancyStabilized`
- `vacancyRatePercent`, `vacancyAndCreditLossPercent`

**Section 11: revenueAndExpenseLineItems** (~15 fields)

- Revenue: `revenueBaseRent`, `revenueRecoveries`, `revenueParking`, `revenueOther`
- Expenses: `expenseUtilities`, `expenseRepairsMaintenance`, `expenseInsurance`, `expenseManagementFee`, `expenseRealEstateTaxes`
- Ratios: `operatingExpenseRatio`
- Deal-level: `marketRentPerSF`, `tiAllowancePerSF`, `freeRentMonths`
- Metrics: `assessmentYear`
- Acquisition: `acquisitionDate`

**Section 12: zoningAndEnvironmental** (~6 fields)

- `zoningConformance`, `varianceRequired`, `floodZoneDesignation`
- `floodMapNumber`, `environmentalPhaseI`, `environmentalPhaseII`

**Core field count:** 68 → ~113 fields across 12 sections.

---

## Domain DDD Updates (all to v2.0.0)

### Cross-Reference Syntax

Pointer row format used throughout:

```
| `party.landlord.name` | string | → `core@2.0.0 → parties` with role=landlord |
| `goingInCapRate`       | number | → `core@2.0.0 → capRate` — at acquisition    |
```

### Lease Abstraction (`lease_abstraction_commercial_na@2.0.0`)

| Change | Fields |
|---|---|
| → core parties | `landlord.name/address`, `tenant.name/address/contact` → `party.{role}.*` pointers |
| → core leaseClassifications | `leaseType` (both occurrences) → pointer |
| → core areaAndMeasurement | `area.rentableAreaSqFt` → `rentableArea`, `measurementStandard` → pointer |
| → core currencyAndUnits | `currency` → pointer |

### Leasing (`leasing_commercial_na@2.0.0`)

| Change | Fields |
|---|---|
| → core parties | `prospectName` context → `party.prospect.*` pointers |
| → core areaAndMeasurement | `efficiencyRatio` → proper pointer row (replacing inline note) |
| → core revenueAndExpenseLineItems | `concludedMarketRentPerSF` → `marketRentPerSF` pointer (leasing-concluded context) |

### Investment (`investment_commercial_na@2.0.0`)

| Change | Fields |
|---|---|
| → core marketContext | Remove `marketStudy` section entirely → section-level pointer to core |
| → core zoningAndEnvironmental | `zoningCurrent` → `zoningClassification` pointer; `zoningConformance`, `zoningVarianceRequired` → pointers |
| Fix intra-file dup | `exitCapRate` in dispositionAnalysis → pointer to underwriting's definition |
| Fix intra-file dup | `dispositionCostsPercent` in dispositionAnalysis → pointer to underwriting's definition |

### Appraisal (`appraisal_commercial_na@2.0.0`)

| Change | Fields |
|---|---|
| → core marketContext | Remove `marketAnalysis` section → section-level pointer to core |
| → core financialFundamentals | `netOperatingIncome` → `noi` pointer; `effectiveGrossIncome` → pointer |
| → core areaAndMeasurement | `buildingAreaGBA/Rentable/Usable` → `grossBuildingArea/rentableArea/usableArea` pointers |
| → core zoningAndEnvironmental | `zoningClassification`, `zoningConformance` → pointers |
| → core revenueAndExpenseLineItems | `expenseUtilities/RepairsMaintenance/Insurance`, `operatingExpenseRatio`, `concludedMarketRentPerSF` → pointers |

### Asset Management (`asset_management_commercial_na@2.0.0`)

| Change | Fields |
|---|---|
| → core revenueAndExpenseLineItems | `revenueBaseRent/Recoveries/Parking/Other` → pointers |
| → investment underwriting | `scenarioBaseCaseIRR/UpsideIRR/DownsideIRR` → pointer to `investment@2.0.0` |
| → core capRate variants | `exitCapRate`, `goingInCapRate` → core capRate pointers with context |
| Rename | `markToMarketPercent` → `markToMarketValuePercent` (book value vs. market value context) |
| → core zoningAndEnvironmental | `environmentalRiskFloodZone` → `floodZoneDesignation` pointer |
| → core revenueAndExpenseLineItems | `assessmentYear` → pointer |

### Property Management (`property_management_commercial_na@2.0.0`)

| Change | Fields |
|---|---|
| → core parties | `tenantName`, `contactName/Phone/Email` → `party.tenant.*` pointers |
| → core revenueAndExpenseLineItems | Revenue/expense fields, `operatingExpenseRatio`, `freeRentMonths`, `tiAllowance` → pointers |
| → core areaAndMeasurement | `rentableSF` → `rentableArea`, `usableSF` → `usableArea` pointers |
| Stays as-is | `markToMarketPercent` (rent-based meaning is correct in PM context) |

---

## Semantic Collision Fixes

| Field | Problem | Fix |
|---|---|---|
| `markToMarketPercent` | Means "contract rent vs. market rent" in Leasing/PM but "book value vs. market value" in Asset Mgmt | Rename to `markToMarketValuePercent` in Asset Mgmt only |
| `effectiveGrossIncome` | Core excludes other income; Appraisal includes it (USPAP) | Update core definition to USPAP standard |
| `operatingExpenseRatio` | Appraisal uses EGI denominator; PM uses gross revenue | Standardize to EGI denominator in core; PM adds clarifying note |

---

## Registry and File Changes

- All DDD refs bumped to `@2.0.0` in `ddd_refs.py`
- All filenames change: `*_v1_0.md` / `*_v1_1.md` → `*_v2_0.md`
- Old v1 files deleted (git history preserves them)
- `test_ddd_refs.py` updated for new version strings
