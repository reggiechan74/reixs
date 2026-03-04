# Domain Data Dictionary: Investment — Commercial North America

**Reference:** `re-ddd:investment_commercial_na@2.0.0`

**Scope:** Field definitions for commercial real estate investment analysis in North America, covering acquisition, DCF projections, underwriting, due diligence, investment metrics, market context, and disposition analysis.

**Relationship to REIXS:** This DDD provides canonical definitions for investment analysis and acquisition/disposition workflows. It references `core_commercial_re_na@2.0.0` for shared property identification, financial fundamentals, area measurement, market context, and zoning/environmental fields. For property valuation (appraisal) workflows, see `appraisal_commercial_na@1.0.0` — the investment DDD can reference appraised values as inputs to underwriting assumptions.

---

## Sections

The schema defines **7 sections** with **119 fields** total (plus shared fields via core pointers). All sections represent data used in commercial real estate investment analysis, acquisition underwriting, and disposition planning.

### 1. acquisitionSummary

Property identification and key acquisition parameters.

Property identity fields reference `core_commercial_re_na@2.0.0 → propertyIdentification`.

| Field | Type | Description |
|---|---|---|
| `propertyReference` | string | Reference to core property identification record (`core_commercial_re_na@2.0.0 → propertyIdentification`) |
| `purchasePrice` | number | Proposed or actual purchase price |
| `purchasePricePerSF` | number | Purchase price per square foot |
| `purchasePricePerUnit` | number | Purchase price per unit |
| `goingInCapRate` | number | Going-in capitalization rate at acquisition (expressed as decimal, e.g., 0.06) → `core@2.0.0 → capRate` — at acquisition |
| `acquisitionDate` | string (ISO 8601) | Actual or expected acquisition closing date |
| `acquisitionBasis` | string | Basis for acquisition: off-market, marketed, auction, portfolio |
| `appraiserValueReference` | string | Reference to appraised value (`appraisal_commercial_na@1.0.0 → reconciliationAndConclusion → finalValueConclusion`) |
| `priceToAppraiserValueRatio` | number | Purchase price as a ratio to appraised value (e.g., 0.95 = 5% below appraised value) |
| `investmentThesis` | string | Summary of the investment thesis and value creation strategy |
| `investmentStrategy` | string | Strategy type: core, core-plus, value-add, opportunistic, development |

### 2. dcfAnalysis

Discounted cash flow analysis and multi-year projections.

| Field | Type | Description |
|---|---|---|
| `projectionPeriodYears` | number | Number of years in the DCF projection period |
| `projectionStartDate` | string (ISO 8601) | Start date of the DCF projection |
| `revenueProjectionByYear` | string | Year-by-year revenue projection summary |
| `revenueGrowthAssumptions` | string | Assumptions underlying revenue growth projections |
| `expenseProjectionByYear` | string | Year-by-year expense projection summary |
| `expenseGrowthRatePercent` | number | Annual expense growth rate (expressed as decimal, e.g., 0.03) |
| `expenseFixedVsVariable` | string | Breakdown of expenses into fixed and variable categories |
| `capitalReservePerSF` | number | Capital reserve allocation per square foot per annum |
| `capitalReservePerAnnum` | number | Total annual capital reserve allocation |
| `netCashFlowByYear` | string | Year-by-year net cash flow summary |
| `terminalCapRate` | number | Terminal capitalization rate applied to reversion (expressed as decimal, e.g., 0.07) → `core@2.0.0 → capRate` — terminal year |
| `terminalCapRateBasis` | string | Rationale for selected terminal capitalization rate |
| `reversionValue` | number | Estimated reversion (sale) value at end of projection period |
| `sellingCostsPercent` | number | Selling costs as a percentage of reversion value (expressed as decimal, e.g., 0.03) |
| `discountRate` | number | Discount rate applied to future cash flows (expressed as decimal, e.g., 0.08) |
| `discountRateBasis` | string | Basis for discount rate selection (risk-free rate + risk premium build-up) |
| `presentValueCashFlows` | number | Present value of projected periodic cash flows |
| `presentValueReversion` | number | Present value of reversion proceeds |
| `dcfIndicatedValue` | number | DCF indicated value (sum of present value of cash flows and reversion) |
| `impliedIRR` | number | Implied internal rate of return from DCF analysis (expressed as decimal) |

### 3. investmentMetrics

Return and risk metrics for investment analysis.

Financial metrics reference `core_commercial_re_na@2.0.0 → financialFundamentals`.

| Field | Type | Description |
|---|---|---|
| `equityInvestment` | number | Total equity capital committed to the investment |
| `leveragedIRR` | number | Leveraged internal rate of return (expressed as decimal, e.g., 0.12) |
| `unleveragedIRR` | number | Unleveraged internal rate of return (expressed as decimal, e.g., 0.08) |
| `cashOnCashReturnByYear` | string | Year-by-year cash-on-cash return summary |
| `cashOnCashReturnAverage` | number | Average cash-on-cash return over hold period (expressed as decimal) |
| `equityMultipleNet` | number | Net equity multiple (total net distributions / total equity invested) |
| `equityMultipleGross` | number | Gross equity multiple (total gross distributions / total equity invested) |
| `paybackPeriodYears` | number | Number of years to recover initial equity investment |
| `modifiedIRR` | number | Modified internal rate of return, if applicable (expressed as decimal) |
| `riskAdjustedReturn` | number | Risk-adjusted return metric (Sharpe ratio or equivalent) |
| `benchmarkName` | string | Benchmark index name: NCREIF, ODCE, or custom benchmark |
| `benchmarkReturn` | number | Benchmark return for comparison (expressed as decimal) |
| `vintageYearReturnComparison` | string | Return comparison against vintage year peer group |

### 4. underwriting

Acquisition underwriting assumptions including financing, growth, and scenario analysis.

| Field | Type | Description |
|---|---|---|
| `financingLTV` | number | Loan-to-value ratio (expressed as decimal, e.g., 0.65) |
| `financingRate` | number | Loan interest rate (expressed as decimal, e.g., 0.045) |
| `financingTermYears` | number | Loan term in years |
| `financingIOPeriodYears` | number | Interest-only period in years |
| `financingAmortizationYears` | number | Loan amortization period in years |
| `closingCostsPercent` | number | Closing costs as a percentage of purchase price (expressed as decimal, e.g., 0.02) |
| `closingCostsItemized` | string | Itemized breakdown of closing costs |
| `year1NOIInPlace` | number | Year 1 net operating income based on in-place rents and occupancy |
| `year1NOIStabilized` | number | Year 1 net operating income assuming stabilized occupancy |
| `rentGrowthAssumptionPercent` | number | Annual rent growth assumption (expressed as decimal, e.g., 0.03) |
| `expenseGrowthAssumptionPercent` | number | Annual expense growth assumption (expressed as decimal, e.g., 0.025) |
| `capitalExpenditureBudgetYear1to5` | string | Year-by-year capital expenditure budget summary for years 1 through 5 |
| `holdPeriodYears` | number | Planned investment hold period in years |
| `exitCapRate` | number | Assumed exit capitalization rate at disposition (expressed as decimal, e.g., 0.07) → `core@2.0.0 → capRate` — at disposition |
| `dispositionCostsPercent` | number | Disposition costs as a percentage of sale price (expressed as decimal, e.g., 0.02) |
| `sensitivityNOIGrowthRange` | string | NOI growth sensitivity range (e.g., "+/-1.0%") |
| `sensitivityCapRateRange` | string | Capitalization rate sensitivity range (e.g., "+/-25 bps") |
| `sensitivityInterestRateRange` | string | Interest rate sensitivity range (e.g., "+/-50 bps") |
| `scenarioBaseCaseIRR` | number | Base case scenario IRR (expressed as decimal) |
| `scenarioBaseCaseEquityMultiple` | number | Base case scenario equity multiple |
| `scenarioUpsideIRR` | number | Upside scenario IRR (expressed as decimal) |
| `scenarioDownsideIRR` | number | Downside scenario IRR (expressed as decimal) |

### 5. dueDiligence

Pre-acquisition and pre-disposition investigation items.

| Field | Type | Description |
|---|---|---|
| `titleReviewStatus` | string | Title review status: clear or encumbered |
| `titleExceptions` | array[string] | List of title exceptions and encumbrances |
| `surveyDate` | string (ISO 8601) | Date of the ALTA/NSPS survey |
| `surveyor` | string | Name of the surveying firm |
| `surveyALTAItems` | array[string] | ALTA/NSPS survey optional Table A items requested |
| `surveyEncroachments` | string | Description of any encroachments identified in the survey |
| `envPhase1Date` | string (ISO 8601) | Date of the Phase I Environmental Site Assessment |
| `envPhase1Firm` | string | Name of the Phase I ESA consulting firm |
| `envPhase1RECs` | string | Recognized environmental conditions identified in Phase I |
| `envPhase1Recommendation` | string | Phase I ESA recommendation (no further action, Phase II recommended, etc.) |
| `envPhase2Date` | string (ISO 8601) | Date of the Phase II Environmental Site Assessment |
| `envPhase2Firm` | string | Name of the Phase II ESA consulting firm |
| `envPhase2Findings` | string | Phase II ESA findings and contamination details |
| `envPhase2RemediationEstimate` | number | Estimated cost of environmental remediation |
| `physicalConditionDate` | string (ISO 8601) | Date of the property condition assessment |
| `physicalConditionFirm` | string | Name of the property condition assessment firm |
| `physicalConditionImmediateRepairs` | number | Estimated cost of immediate repairs identified |
| `physicalConditionShortTermRepairs` | number | Estimated cost of short-term repairs (1-2 years) |
| `physicalConditionDeferredMaintenance` | number | Estimated cost of deferred maintenance items |
| `zoningClassification` | string | → `core@2.0.0 → propertyIdentification.zoningClassification` |
| `zoningConformance` | string | → `core@2.0.0 → zoningAndEnvironmental.zoningConformance` |
| `varianceRequired` | boolean | → `core@2.0.0 → zoningAndEnvironmental.varianceRequired` |
| `entitlementStatus` | string | Entitlement status: approved, pending, or required |
| `thirdPartyReports` | array[string] | List of third-party reports obtained (seismic, wind, flood, ADA, parking study) |
| `estoppelCertificateSummary` | string | Summary of tenant estoppel certificate findings |
| `sndaStatus` | string | Subordination, non-disturbance, and attornment agreement status (obtained or pending for each tenant) |

### 6. marketStudy

> **Shared fields:** Uses `re-ddd:core_commercial_re_na@2.0.0 → marketContext` for all market study fields (MSA, demographics, employment, supply, demand, rental trends, construction pipeline, forecasts).

This section contains no domain-specific fields beyond core. Reference the core marketContext section for the complete field list.

### 7. dispositionAnalysis

Exit planning and disposition analysis.

| Field | Type | Description |
|---|---|---|
| `exitStrategy` | string | Planned exit strategy: sale, refinance, recapitalization, or hold |
| `targetDispositionDate` | string (ISO 8601) | Target date for disposition |
| `projectedSalePrice` | number | Projected sale price at disposition |
| `projectedSalePricePerSF` | number | Projected sale price per square foot |
| `exitCapRate` | number | → `core@2.0.0 → capRate` — at disposition. See also underwriting §4. |
| `exitCapRateBasis` | string | Rationale for the selected exit cap rate |
| `projectedNOIAtExit` | number | Projected NOI at time of disposition |
| `dispositionCostsPercent` | number | → underwriting §4 for canonical definition |
| `dispositionCostsDollar` | number | Total disposition costs in dollars (brokerage, legal, transfer tax) |
| `brokerageCommissionPercent` | number | Brokerage commission as a percentage of sale price (expressed as decimal) |
| `transferTax` | number | Estimated transfer or conveyance tax |
| `prepaymentPenalty` | number | Loan prepayment penalty, if applicable |
| `netSaleProceeds` | number | Net sale proceeds after all disposition costs |
| `equityProceeds` | number | Equity proceeds after loan payoff and costs |
| `holdVsSellAnalysis` | string | Analysis comparing holding vs. selling at the projected date |
| `buyerPoolAssessment` | string | Assessment of the likely buyer pool and market demand |
| `marketingStrategy` | string | Recommended marketing strategy for disposition |

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
