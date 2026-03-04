# Domain Data Dictionary: Commercial Real Estate Core Glossary — North America

**Reference:** `re-ddd:core_commercial_re_na@2.0.0`

**Scope:** Shared field definitions used across multiple CRE roles — property identification, financial fundamentals, area measurement, party representation, lease classifications, temporal concepts, currency conventions, document references, market context, occupancy, revenue/expense, and zoning/environmental. Organized into 12 sections.

**Relationship to REIXS:** This DDD provides canonical definitions for cross-cutting CRE concepts. Role-specific DDDs (lease abstraction, underwriting, asset management, appraisal) reference these shared definitions rather than redefining them, ensuring consistency across the REIXS ecosystem. Domain DDDs declare a dependency on `re-ddd:core_commercial_re_na@2.0.0`.

---

## Sections

The schema defines **12 sections** with **114 fields** total. All sections represent shared concepts used across multiple CRE roles and workflows.

### 1. propertyIdentification

Property-level identifiers and classification.

| Field | Type | Description |
|---|---|---|
| `propertyName` | string | Common name of the property |
| `streetAddress` | string | Street address |
| `city` | string | City |
| `stateProvince` | string | State or province |
| `postalCode` | string | ZIP or postal code |
| `country` | string | Country (ISO 3166-1 alpha-2) |
| `legalDescription` | string | Legal description (lot, plan, municipal reference) |
| `propertyType` | string | Classification: office, industrial, retail, multifamily, mixed-use |
| `assetClass` | string | Class A, B, or C designation |
| `yearBuilt` | number | Year of original construction |
| `yearRenovated` | number | Year of most recent major renovation |
| `zoningClassification` | string | Current zoning designation |
| `parcelId` | string | Tax assessor parcel number |

### 2. financialFundamentals

Core financial metrics used across roles.

| Field | Type | Description |
|---|---|---|
| `noi` | number | Net Operating Income — revenue minus operating expenses, before debt service and capital |
| `grossRevenue` | number | Total revenue before any deductions |
| `effectiveGrossIncome` | number | Potential gross income minus vacancy and credit loss plus other income |
| `operatingExpenses` | number | Total operating expenses (excluding debt service and capital) |
| `capRate` | number | Capitalization rate — NOI / property value (expressed as decimal, e.g., 0.065) |
| `cashOnCashReturn` | number | Annual pre-tax cash flow / total cash invested (expressed as decimal) |
| `irr` | number | Internal rate of return (expressed as decimal) |
| `npv` | number | Net present value at specified discount rate |
| `debtService` | number | Annual debt service (principal + interest) |
| `dscr` | number | Debt service coverage ratio — NOI / debt service |
| `ltv` | number | Loan-to-value ratio — loan balance / property value (expressed as decimal) |
| `equityMultiple` | number | Total distributions / total equity invested |

### 3. areaAndMeasurement

Standardized area metrics and measurement conventions.

| Field | Type | Description |
|---|---|---|
| `grossBuildingArea` | number | Total building area including all enclosed spaces (sq ft) |
| `rentableArea` | number | Rentable square footage per BOMA standards (sq ft) |
| `usableArea` | number | Usable square footage per BOMA standards (sq ft) |
| `grossLeasableArea` | number | Total leasable area in retail properties (sq ft) |
| `netRentableArea` | number | Net rentable area after exclusions (sq ft) |
| `floorAreaRatio` | number | Building area / site area (decimal) |
| `measurementStandard` | string | Standard used (e.g., ANSI/BOMA Z65.1-2017, ANSI/BOMA Z65.2-2012) |
| `commonAreaFactor` | number | Ratio of rentable to usable area (e.g., 1.15) |
| `loadFactor` | number | Common area allocation factor (expressed as decimal) |
| `efficiencyRatio` | number | Usable area / rentable area (expressed as decimal) |
| `siteArea` | number | Total land area (sq ft or acres) |
| `siteAreaUnit` | string | Unit for site area: "sq ft" or "acres" |

### 4. parties

Standard party/entity representation using role-qualified dot notation. Domain DDDs reference specific roles (e.g., `party.landlord.name`, `party.tenant.name`).

| Field | Type | Description |
|---|---|---|
| `party.{role}.name` | string | Full legal name of the entity |
| `party.{role}.entityType` | string | Corporation, LLC, LP, REIT, individual, trust, pension fund, etc. |
| `party.{role}.address` | string | Registered/principal address |
| `party.{role}.contactName` | string | Primary contact person |
| `party.{role}.contactPhone` | string | Contact phone number |
| `party.{role}.contactEmail` | string | Contact email address |
| `party.{role}.taxId` | string | Tax identification number (EIN, BN, etc.) |

**Standard roles:** owner, landlord, tenant, manager, broker, lender, appraiser, counsel, prospect

### 5. leaseClassifications

Standard lease type definitions.

| Field | Type | Description |
|---|---|---|
| `leaseType` | string | NNN (triple net), modified gross, gross, full-service, ground lease, percentage lease |
| `leaseTypeDescription` | string | Plain-language description of the lease structure |
| `tenantExpenseObligations` | array[string] | Which expenses the tenant pays directly under this structure |
| `landlordExpenseObligations` | array[string] | Which expenses the landlord covers |
| `expenseStopOrBaseYear` | string | Expense stop amount or base year for escalations |

### 6. dateAndTimePeriods

Temporal concepts and period definitions.

| Field | Type | Description |
|---|---|---|
| `asOfDate` | string (ISO 8601) | Effective date for the data or analysis |
| `fiscalYearEnd` | string | Month/day of fiscal year end (e.g., "12-31", "03-31") |
| `reportingPeriod` | string | Period covered: "monthly", "quarterly", "annually" |
| `reportingPeriodStart` | string (ISO 8601) | Start date of the reporting period |
| `reportingPeriodEnd` | string (ISO 8601) | End date of the reporting period |
| `holdingPeriod` | number | Investment holding period in years |
| `projectionPeriod` | number | Number of years in forward projection/DCF |

### 7. currencyAndUnits

Currency and unit normalization.

| Field | Type | Description |
|---|---|---|
| `currency` | string | ISO 4217 currency code (USD, CAD) |
| `amountUnit` | string | "total", "per-sf", "per-unit", "per-annum", "per-month" |
| `areaUnit` | string | "sq ft", "sq m", "acres", "hectares" |
| `conversionRate` | number | Exchange rate if currency conversion applied |
| `conversionDate` | string (ISO 8601) | Date of exchange rate used |

### 8. documentReferences

Source document tracking for provenance.

| Field | Type | Description |
|---|---|---|
| `documentType` | string | Lease, appraisal, operating statement, rent roll, budget, inspection report, etc. |
| `documentTitle` | string | Title or filename of the source document |
| `documentDate` | string (ISO 8601) | Date of the source document |
| `documentVersion` | string | Version or revision identifier |
| `documentSource` | string | Origin system or provider |
| `pageReference` | string | Page or section reference within the document |

### 9. marketContext

Market study fields shared across investment, appraisal, and leasing analysis. Covers MSA/submarket identification, demographics, employment, supply and demand metrics, rental trends, construction pipeline, and forecasts.

| Field | Type | Description |
|---|---|---|
| `msaName` | string | Metropolitan Statistical Area name |
| `submarketDefinition` | string | Definition and boundaries of the submarket |
| `population` | number | Current population of the MSA or submarket |
| `populationGrowthHistoricalPercent` | number | Historical population growth rate (expressed as decimal, e.g., 0.02) |
| `populationGrowthProjectedPercent` | number | Projected population growth rate (expressed as decimal, e.g., 0.015) |
| `medianHouseholdIncome` | number | Median household income in the market area |
| `employmentTotal` | number | Total employment in the MSA or submarket |
| `employmentBySector` | string | Employment breakdown by sector |
| `unemploymentRatePercent` | number | Unemployment rate (expressed as decimal, e.g., 0.04) |
| `majorEmployers` | array[string] | List of major employers in the market area |
| `supplyTotalInventorySF` | number | Total competitive inventory in square feet |
| `supplyVacancyRatePercent` | number | Market vacancy rate (expressed as decimal, e.g., 0.08) |
| `supplyAvailabilityRatePercent` | number | Market availability rate including sublease space (expressed as decimal, e.g., 0.12) |
| `demandNetAbsorptionAnnualSF` | number | Annual net absorption in square feet |
| `rentalRateTrendAsking` | string | Asking rental rate trend: increasing, stable, or decreasing |
| `rentalRateTrendEffective` | string | Effective rental rate trend: increasing, stable, or decreasing |
| `concessionTrends` | string | Description of current concession trends (free rent, TI allowances) |
| `constructionUnderConstructionSF` | number | Square footage currently under construction |
| `constructionPlannedSF` | number | Square footage in planned pipeline |
| `forecastVacancy` | string | Vacancy rate forecast: increasing, stable, or decreasing |
| `forecastRentGrowth` | string | Rent growth forecast: increasing, stable, or decreasing |

### 10. occupancyAndVacancy

Occupancy and vacancy metrics used across appraisal, asset management, and property management.

| Field | Type | Description |
|---|---|---|
| `occupancyRatePhysical` | number | Physically occupied space / total rentable space (expressed as decimal) |
| `occupancyRateEconomic` | number | Actual revenue / potential gross revenue at full occupancy (expressed as decimal) |
| `occupancyStabilized` | number | Expected occupancy at stabilization (expressed as decimal) |
| `vacancyRatePercent` | number | Vacant space / total rentable space (expressed as decimal) |
| `vacancyAndCreditLossPercent` | number | Combined vacancy and credit loss as percentage of potential gross income (expressed as decimal) |

### 11. revenueAndExpenseLineItems

Standardized revenue and expense line items, deal-level metrics, and ratios used across property management, asset management, and appraisal.

| Field | Type | Description |
|---|---|---|
| `revenueBaseRent` | number | Base rental revenue |
| `revenueRecoveries` | number | Expense recovery revenue from tenants |
| `revenueParking` | number | Parking revenue |
| `revenueOther` | number | Other miscellaneous revenue |
| `expenseUtilities` | number | Utility expenses |
| `expenseRepairsMaintenance` | number | Repair and maintenance expenses |
| `expenseInsurance` | number | Insurance expenses |
| `expenseManagementFee` | number | Property management fee |
| `expenseRealEstateTaxes` | number | Real estate tax expenses |
| `operatingExpenseRatio` | number | Total operating expenses / effective gross income (expressed as decimal) |
| `marketRentPerSF` | number | Current market rent per square foot per annum |
| `tiAllowancePerSF` | number | Tenant improvement allowance per square foot |
| `freeRentMonths` | number | Free rent concession period in months |
| `assessmentYear` | number | Year of the most recent tax assessment |
| `acquisitionDate` | string (ISO 8601) | Date the property was acquired |

### 12. zoningAndEnvironmental

Zoning compliance and environmental assessment fields used across appraisal, investment, and asset management.

| Field | Type | Description |
|---|---|---|
| `zoningConformance` | string | Conformance status: conforming, non-conforming, or legal non-conforming |
| `varianceRequired` | boolean | Whether a zoning variance is required for intended use |
| `floodZoneDesignation` | string | FEMA flood zone designation (e.g., Zone X, Zone AE) |
| `floodMapNumber` | string | FEMA flood insurance rate map panel number |
| `environmentalPhaseI` | string | Phase I ESA status and date |
| `environmentalPhaseII` | string | Phase II ESA status and date (if applicable) |

---

## Field Status Tracking

Every field in this DDD, when extracted, MUST carry a status indicator:

| Status | Meaning | Required Metadata |
|---|---|---|
| `FACT` | Value found verbatim in source document | `provenance` (page, clause, verbatim quote) |
| `INFERENCE` | Value derived or interpreted from source | `confidence` (0.0-1.0), `reasoning` |
| `MISSING` | Field not found in source document | value = `null` (JSON) or `"Not specified"` (markdown) |
| `CONFLICT` | Multiple conflicting values found | All values with individual `provenance`, `reasoning` |

## Data Types

| Type | JSON Representation | Notes |
|---|---|---|
| `string` | `"value"` | Text values |
| `string (ISO 8601)` | `"YYYY-MM-DD"` | All dates normalized to ISO 8601 |
| `number` | `45.00` | Numeric values without currency symbols |
| `boolean` | `true` / `false` | Yes/no values |
| `array[string]` | `["item1", "item2"]` | Lists |
| `null` | `null` | Missing or absent values |

## Versioning

This DDD follows semantic versioning:
- **Patch** (2.0.x): Field description clarifications, no schema changes
- **Minor** (2.x.0): New optional fields added, no existing fields removed
- **Major** (x.0.0): Breaking changes — fields renamed, removed, or restructured
