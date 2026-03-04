# Domain Data Dictionary: Asset Management — Commercial North America

**Reference:** `re-ddd:asset_management_commercial_na@2.0.0`

**Scope:** Field definitions for asset-level strategy and performance management across commercial portfolios in North America.

**Relationship to REIXS:** This DDD provides canonical definitions for asset management workflows including valuation, financial performance, debt structuring, hold/sell analysis, leasing strategy, capital planning, risk assessment, and portfolio context. Where concepts overlap with the core glossary, this DDD references `core_commercial_re_na@2.0.0` rather than redefining shared terms. Scenario IRR fields are sourced from `investment_commercial_na@2.0.0`.

---

## Sections

The schema defines **10 sections** with **165 fields** total. All sections represent asset-level strategy and performance data used in portfolio management of commercial real estate assets.

### 1. assetProfile

Asset-level summary and ownership context.

Property identity fields use definitions from `core_commercial_re_na@2.0.0 → propertyIdentification`.

| Field | Type | Description |
|---|---|---|
| `propertyReference` | string | Reference to core property identification record (`core_commercial_re_na@2.0.0 → propertyIdentification`) |
| `acquisitionDate` | string (ISO 8601) | → `core@2.0.0 → revenueAndExpenseLineItems.acquisitionDate` |
| `acquisitionPrice` | number | Total acquisition price |
| `acquisitionCapRate` | number | Capitalization rate at acquisition (expressed as decimal, e.g., 0.065) |
| `currentValuation` | number | Current estimated market value of the asset |
| `valuationDate` | string (ISO 8601) | Date of the current valuation |
| `valuationMethod` | string | Method used for current valuation: direct capitalization, DCF, or sales comparison |
| `ownershipStructure` | string | Ownership arrangement: sole, JV, fund, or co-investment |
| `jvSplitPercent` | number | Joint venture ownership split percentage for this entity |
| `fundAllocation` | string | Fund to which the asset is allocated |
| `coInvestmentPercent` | number | Co-investment percentage alongside fund capital |
| `fundVehicleName` | string | Name of the fund vehicle holding the asset |
| `vintageYear` | number | Year the asset was acquired (acquisition vintage) |
| `holdPeriodElapsedYears` | number | Number of years the asset has been held since acquisition |
| `holdPeriodTargetYears` | number | Target hold period in years per the investment plan |
| `assetStrategy` | string | Investment strategy classification: core, core-plus, value-add, or opportunistic |

### 2. financialPerformance

Operating financial results at the asset level.

Financial metrics use definitions from `core_commercial_re_na@2.0.0 → financialFundamentals`.

| Field | Type | Description |
|---|---|---|
| `noiActual` | number | Actual net operating income for the current reporting period |
| `noiBudget` | number | Budgeted net operating income for the current reporting period |
| `noiPriorYear` | number | Net operating income for the same period in the prior year |
| `noiVarianceDollar` | number | Dollar variance between actual and budgeted NOI |
| `noiVariancePercent` | number | Percentage variance between actual and budgeted NOI |
| `revenueBaseRent` | number | → `core@2.0.0 → revenueAndExpenseLineItems.revenueBaseRent` |
| `revenueRecoveries` | number | → `core@2.0.0 → revenueAndExpenseLineItems.revenueRecoveries` |
| `revenueParking` | number | → `core@2.0.0 → revenueAndExpenseLineItems.revenueParking` |
| `revenueOther` | number | → `core@2.0.0 → revenueAndExpenseLineItems.revenueOther` |
| `expensesByCategory` | string | Itemized breakdown of operating expenses by category |
| `capitalExpendituresRoutine` | number | Routine capital expenditures (maintenance, replacements) |
| `capitalExpendituresNonRoutine` | number | Non-routine capital expenditures (major improvements, repositioning) |
| `cashFlowBeforeDebtService` | number | Net cash flow before mortgage and debt service payments |
| `cashFlowAfterDebtService` | number | Net cash flow after all debt service payments |
| `distributionAmount` | number | Distribution amount paid to investors for the period |
| `distributionDate` | string (ISO 8601) | Date the distribution was paid |
| `distributionYield` | number | Distribution yield relative to invested equity (expressed as decimal) |
| `unleveredReturn` | number | Return on the asset before financing effects (expressed as decimal) |
| `leveredReturn` | number | Return on the asset after financing effects (expressed as decimal) |

### 3. valuationMetrics

Property valuation data points and market comparables.

Valuation concepts use definitions from `core_commercial_re_na@2.0.0 → financialFundamentals`.

| Field | Type | Description |
|---|---|---|
| `goingInCapRate` | number | → `core@2.0.0 → capRate` — at acquisition |
| `exitCapRate` | number | → `core@2.0.0 → capRate` — at disposition |
| `marketCapRate` | number | Current market capitalization rate for comparable assets (expressed as decimal) |
| `pricePerSFAcquisition` | number | Price per square foot at acquisition |
| `pricePerSFCurrent` | number | Current value per square foot based on latest valuation |
| `replacementCostPerSF` | number | Estimated replacement cost per square foot |
| `assessedValue` | number | Tax-assessed value of the property |
| `assessmentYear` | number | → `core@2.0.0 → revenueAndExpenseLineItems.assessmentYear` |
| `appraisalValue` | number | Most recent third-party appraised value |
| `appraisalDate` | string (ISO 8601) | Date of the most recent third-party appraisal |
| `appraiserName` | string | Name of the appraiser or appraisal firm |
| `markToMarketDollar` | number | Dollar change from book value to current market value |
| `markToMarketValuePercent` | number | Percentage change from book value to current market value (expressed as decimal) |
| `impliedValue` | number | Implied value derived from NOI divided by market cap rate |

### 4. debtAndCapitalStructure

Financing summary and covenant tracking.

| Field | Type | Description |
|---|---|---|
| `loanId` | string | Unique identifier for the loan |
| `lenderName` | string | Name of the lending institution |
| `loanType` | string | Type of loan: fixed, floating, construction, or mezzanine |
| `originalPrincipal` | number | Original principal amount of the loan |
| `currentBalance` | number | Current outstanding loan balance |
| `maturityDate` | string (ISO 8601) | Loan maturity date |
| `interestRateFixed` | number | Fixed interest rate on the loan (expressed as decimal) |
| `interestRateSpread` | number | Spread over the reference index in basis points |
| `interestRateIndex` | string | Reference rate index (e.g., SOFR, prime) |
| `ioPeriodEndDate` | string (ISO 8601) | End date of the interest-only period |
| `amortizationSchedule` | string | Amortization schedule description (e.g., "25-year") |
| `ltvCurrent` | number | Current loan-to-value ratio (expressed as decimal) |
| `dscrCurrent` | number | Current debt service coverage ratio (NOI / debt service) |
| `dscrCovenant` | number | Minimum debt service coverage ratio required by the loan covenant |
| `covenantComplianceStatus` | string | Current covenant compliance status: compliant, watch, or breach |
| `covenantThresholds` | string | Description of key covenant thresholds and triggers |
| `prepaymentProvisions` | string | Prepayment terms: yield maintenance, defeasance, or open period |
| `refinancingEstimatedProceeds` | number | Estimated net proceeds from a refinancing |
| `refinancingRateAssumptions` | string | Interest rate and term assumptions used in refinancing analysis |
| `refinancingNetBenefit` | number | Estimated net benefit (cost savings or cash-out) from refinancing |

### 5. holdSellAnalysis

Disposition decision support and scenario modeling.

| Field | Type | Description |
|---|---|---|
| `currentMarketValueEstimate` | number | Estimated current market value of the asset |
| `estimateBasis` | string | Basis for the market value estimate: appraisal, broker opinion, or internal model |
| `projectedDispositionValue` | number | Projected gross sale price at the target exit date |
| `targetExitDate` | string (ISO 8601) | Target date for asset disposition |
| `dispositionCostBrokerPercent` | number | Estimated brokerage commission as percentage of sale price |
| `dispositionCostTransferTax` | number | Estimated transfer tax amount |
| `dispositionCostLegal` | number | Estimated legal and closing costs |
| `holdIRR` | number | Forward-looking internal rate of return if the asset is held (expressed as decimal) |
| `sellIRR` | number | Internal rate of return if the asset is sold now (expressed as decimal) |
| `breakevenHoldPeriodYears` | number | Number of additional hold years needed for hold IRR to equal sell IRR |
| `capitalGainsEstimate` | number | Estimated capital gains from disposition |
| `taxImplications` | string | Summary of tax implications from sale (depreciation recapture, 1031 exchange eligibility) |
| `reinvestmentAssumptions` | string | Assumptions for reinvestment of sale proceeds |
| `recommendation` | string | Disposition recommendation: hold, sell, or refinance |
| `recommendationRationale` | string | Narrative rationale supporting the hold/sell/refinance recommendation |

### 6. leasingStrategy

Asset-level leasing direction and tenant mix analysis.

| Field | Type | Description |
|---|---|---|
| `currentOccupancy` | number | Current physical occupancy rate (expressed as decimal, e.g., 0.92) |
| `targetOccupancy` | number | Target occupancy rate per the asset plan (expressed as decimal) |
| `stabilizedOccupancy` | number | Stabilized occupancy rate assumed for underwriting (expressed as decimal) |
| `waleYears` | number | Weighted average lease expiry in years |
| `leaseExpiryProfileByYear` | string | Summary of lease expirations by year (e.g., "2025: 15%, 2026: 22%, 2027: 8%") |
| `leaseExpiryProfileBySF` | string | Lease expiry profile expressed in square footage by year |
| `leaseExpiryProfileByRevenue` | string | Lease expiry profile expressed as percentage of revenue by year |
| `renewalProbabilityByTenant` | string | Tenant-level renewal probability assessment |
| `estimatedDowntimeMonths` | number | Estimated average downtime in months between lease expiry and new lease commencement |
| `marketRentProjectionCurrent` | number | Current market rent per square foot |
| `marketRentProjection1Year` | number | Projected market rent per square foot in one year |
| `marketRentProjection3Year` | number | Projected market rent per square foot in three years |
| `tenantCreditQualityInvestmentGradePercent` | number | Percentage of revenue from investment-grade tenants (expressed as decimal) |
| `tenantCreditQualityNonRatedPercent` | number | Percentage of revenue from non-rated tenants (expressed as decimal) |
| `topTenantConcentrationPercent` | number | Revenue concentration from the top five tenants as percentage of total revenue (expressed as decimal) |

### 7. capitalPlanning

Multi-year capital strategy and reserve management.

| Field | Type | Description |
|---|---|---|
| `capexPlan5YearTotal` | number | Total planned capital expenditures over the five-year horizon |
| `capexPlan5YearByYear` | string | Year-by-year breakdown of planned capital expenditures |
| `capexPlan5YearByCategory` | string | Category breakdown of planned capital expenditures (structural, mechanical, cosmetic, etc.) |
| `capexPlan10YearSummary` | string | Summary of the ten-year capital expenditure outlook |
| `deferredMaintenanceItem` | string | Description of the deferred maintenance item |
| `deferredMaintenanceCost` | number | Estimated cost to address the deferred maintenance item |
| `deferredMaintenancePriority` | string | Priority classification: critical, high, medium, or low |
| `reserveFundBalance` | number | Current balance in the capital reserve fund |
| `targetReserve` | number | Target capital reserve fund balance |
| `annualContribution` | number | Annual contribution to the capital reserve fund |
| `roiOnCapitalInvestments` | number | Estimated return on capital investments (expressed as decimal) |
| `esgUpgradeType` | string | Type of ESG-related capital upgrade: LED retrofit, HVAC upgrade, solar, or EV charging |
| `esgUpgradeDescription` | string | Detailed description of the planned ESG upgrade |
| `expectedImpactOnNOI` | number | Expected annual NOI impact from the capital investment |
| `expectedImpactOnValue` | number | Expected impact on property value from the capital investment |

### 8. riskAssessment

Risk identification, monitoring, and overall risk posture.

| Field | Type | Description |
|---|---|---|
| `marketRiskSupplyPipeline` | string | Assessment of new supply pipeline in the submarket |
| `marketRiskDemandTrends` | string | Assessment of demand trends and absorption in the submarket |
| `marketRiskRentalRateTrajectory` | string | Rental rate trajectory outlook: increasing, stable, or decreasing |
| `tenantConcentrationRiskPercent` | number | Single largest tenant as percentage of total revenue (expressed as decimal) |
| `leaseRolloverRisk12Months` | number | Percentage of revenue from leases expiring within 12 months (expressed as decimal) |
| `leaseRolloverRisk24Months` | number | Percentage of revenue from leases expiring within 24 months (expressed as decimal) |
| `leaseRolloverRisk36Months` | number | Percentage of revenue from leases expiring within 36 months (expressed as decimal) |
| `environmentalRiskContamination` | string | Known contamination status: none, known, or suspected |
| `floodZoneDesignation` | string | → `core@2.0.0 → zoningAndEnvironmental.floodZoneDesignation` |
| `environmentalRiskSeismic` | string | Seismic risk zone designation |
| `regulatoryRiskRentControl` | string | Rent control applicability: applicable or not applicable |
| `regulatoryRiskZoningChanges` | string | Assessment of pending or anticipated zoning changes |
| `regulatoryRiskTaxReassessment` | string | Assessment of tax reassessment risk and timing |
| `obsolescenceRiskFunctional` | string | Functional obsolescence risk level: low, medium, or high |
| `obsolescenceRiskTechnological` | string | Technological obsolescence risk level: low, medium, or high |
| `obsolescenceRiskDesign` | string | Design obsolescence risk level: low, medium, or high |
| `overallRiskRating` | string | Composite risk rating for the asset: low, medium, or high |
| `riskNarrative` | string | Free-text narrative summarizing the overall risk profile and key concerns |

### 9. portfolioContext

Asset positioning within the broader portfolio.

| Field | Type | Description |
|---|---|---|
| `portfolioName` | string | Name of the portfolio or fund containing the asset |
| `totalPortfolioValue` | number | Total market value of the portfolio |
| `numberOfAssets` | number | Total number of assets in the portfolio |
| `assetShareByValuePercent` | number | This asset's share of total portfolio value (expressed as decimal) |
| `assetShareByNOIPercent` | number | This asset's share of total portfolio NOI (expressed as decimal) |
| `peerComparison` | string | Performance comparison versus similar assets in the portfolio |
| `sectorAllocationOfficePercent` | number | Portfolio allocation to office assets (expressed as decimal) |
| `sectorAllocationIndustrialPercent` | number | Portfolio allocation to industrial assets (expressed as decimal) |
| `sectorAllocationRetailPercent` | number | Portfolio allocation to retail assets (expressed as decimal) |
| `geographicDiversification` | string | Summary of portfolio geographic distribution |
| `vintageAnalysis` | string | Acquisition year cohort performance analysis |
| `portfolioGrossIRR` | number | Portfolio-level gross internal rate of return (expressed as decimal) |
| `portfolioNetIRR` | number | Portfolio-level net internal rate of return (expressed as decimal) |
| `portfolioEquityMultiple` | number | Portfolio-level equity multiple (total distributions / total equity invested) |

### 10. budgetAndForecasting

Forward-looking financial planning and scenario analysis.

Temporal concepts use definitions from `core_commercial_re_na@2.0.0 → dateAndTimePeriods`.

| Field | Type | Description |
|---|---|---|
| `annualBudgetRevenue` | number | Budgeted total revenue for the current fiscal year |
| `annualBudgetExpenses` | number | Budgeted total operating expenses for the current fiscal year |
| `annualBudgetNOI` | number | Budgeted net operating income for the current fiscal year |
| `annualBudgetCapex` | number | Budgeted capital expenditures for the current fiscal year |
| `reforecastCadence` | string | Frequency of budget reforecasting: quarterly, semi-annual, or annual |
| `varianceCurrentPeriodDollar` | number | Dollar variance between actual and budget for the current period |
| `varianceCurrentPeriodPercent` | number | Percentage variance between actual and budget for the current period |
| `varianceYTDDollar` | number | Year-to-date dollar variance between actual and budget |
| `varianceYTDPercent` | number | Year-to-date percentage variance between actual and budget |
| `assumptionVacancy` | number | Vacancy rate assumption used in the forecast (expressed as decimal) |
| `assumptionMarketRentGrowth` | number | Market rent growth assumption used in the forecast (expressed as decimal) |
| `assumptionExpenseInflation` | number | Expense inflation assumption used in the forecast (expressed as decimal) |
| `assumptionCapRate` | number | Capitalization rate assumption used in the forecast (expressed as decimal) |
| `scenarioBaseCaseNOI` | number | Base case scenario projected NOI |
| `scenarioBaseCaseIRR` | number | → `investment@2.0.0 → underwriting.scenarioBaseCaseIRR` |
| `scenarioUpsideNOI` | number | Upside scenario projected NOI |
| `scenarioUpsideIRR` | number | → `investment@2.0.0 → underwriting.scenarioUpsideIRR` |
| `scenarioDownsideNOI` | number | Downside scenario projected NOI |
| `scenarioDownsideIRR` | number | → `investment@2.0.0 → underwriting.scenarioDownsideIRR` |

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
