# Domain Data Dictionary: Investment & Appraisal — Commercial North America

**Reference:** `re-ddd:investment_appraisal_commercial_na@1.0.0`

**Scope:** Field definitions for investment analysis and property valuation across commercial real estate in North America.

**Relationship to REIXS:** This DDD provides canonical definitions for investment and appraisal workflows including property description for valuation, income capitalization, discounted cash flow analysis, sales comparison, cost approach, market studies, investment metrics, underwriting, due diligence, and reconciliation. Where concepts overlap with the core glossary, this DDD references `core_commercial_re_na@1.0.0` rather than redefining shared terms.

---

## Sections

The schema defines **10 sections** with **216 fields** total. All sections represent investment analysis and property valuation data used in commercial real estate appraisal and acquisition/disposition workflows.

### 1. propertyDescription

Physical and site characteristics for valuation.

Property identity fields use definitions from `core_commercial_re_na@1.0.0 → propertyIdentification`.

| Field | Type | Description |
|---|---|---|
| `propertyReference` | string | Reference to core property identification record (`core_commercial_re_na@1.0.0 → propertyIdentification`) |
| `siteAreaSF` | number | Total site area in square feet |
| `siteAreaAcres` | number | Total site area in acres |
| `siteFrontage` | number | Site frontage in linear feet |
| `siteTopography` | string | Site topography: level, sloping, or irregular |
| `siteShape` | string | Site shape: regular or irregular |
| `utilitiesAvailability` | array[string] | Available utilities: water, sewer, gas, electric |
| `buildingAreaGBA` | number | Gross building area in square feet |
| `buildingAreaRentable` | number | Rentable building area in square feet |
| `buildingAreaUsable` | number | Usable building area in square feet |
| `numberOfFloors` | number | Total number of above-grade floors |
| `constructionType` | string | Construction type: steel frame, concrete, wood frame, or masonry |
| `roofType` | string | Roof type: flat, pitched, or membrane |
| `conditionRating` | string | Overall condition rating: excellent, good, fair, or poor |
| `conditionBasis` | string | Basis for condition rating: inspection, report, or assumption |
| `numberOfUnits` | number | Total number of rentable units |
| `averageUnitSizeSF` | number | Average unit size in square feet |
| `parkingType` | string | Parking type: surface, structured, or underground |
| `parkingSpaces` | number | Total number of parking spaces |
| `parkingRatio` | number | Parking ratio expressed as spaces per 1,000 square feet |
| `renovationYear` | number | Year of most recent renovation |
| `renovationScope` | string | Description of renovation scope and work performed |
| `renovationCost` | number | Total cost of renovation |
| `highestBestUseVacant` | string | Highest and best use conclusion assuming the site is vacant |
| `highestBestUseImproved` | string | Highest and best use conclusion as improved |
| `functionalUtilityAssessment` | string | Assessment of the property's functional utility and layout efficiency |

### 2. incomeApproach

Direct capitalization and income-based valuation.

Financial metrics reference `core_commercial_re_na@1.0.0 → financialFundamentals`.

| Field | Type | Description |
|---|---|---|
| `potentialGrossIncome` | number | Total potential gross income assuming full occupancy at market rents |
| `vacancyAndCreditLossPercent` | number | Vacancy and credit loss allowance as a percentage (expressed as decimal, e.g., 0.05) |
| `vacancyAndCreditLossDollar` | number | Vacancy and credit loss allowance in dollars |
| `effectiveGrossIncome` | number | Potential gross income minus vacancy and credit loss |
| `operatingExpensesItemized` | string | Itemized breakdown of operating expenses by category |
| `netOperatingIncome` | number | Effective gross income minus total operating expenses |
| `capRateSource` | string | Source of capitalization rate: market extraction, band of investment, or survey |
| `capRateSelected` | number | Selected capitalization rate (expressed as decimal, e.g., 0.065) |
| `comparableCapRateData` | string | Supporting comparable property capitalization rate data |
| `directCapitalizationValue` | number | Value indicated by direct capitalization (NOI / cap rate) |
| `stabilizedVsAsIs` | string | Basis of income analysis: stabilized or as-is |
| `aboveBelowMarketLeaseAdjustment` | number | Dollar adjustment for above- or below-market lease terms |
| `aboveBelowMarketLeaseDetail` | string | Explanation of above- or below-market lease adjustment |
| `incomeApproachIndicatedValue` | number | Final value indicated by the income approach |

### 3. dcfAnalysis

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
| `terminalCapRate` | number | Terminal capitalization rate applied to reversion (expressed as decimal, e.g., 0.07) |
| `terminalCapRateBasis` | string | Rationale for selected terminal capitalization rate |
| `reversionValue` | number | Estimated reversion (sale) value at end of projection period |
| `sellingCostsPercent` | number | Selling costs as a percentage of reversion value (expressed as decimal, e.g., 0.03) |
| `discountRate` | number | Discount rate applied to future cash flows (expressed as decimal, e.g., 0.08) |
| `discountRateBasis` | string | Basis for discount rate selection (risk-free rate + risk premium build-up) |
| `presentValueCashFlows` | number | Present value of projected periodic cash flows |
| `presentValueReversion` | number | Present value of reversion proceeds |
| `dcfIndicatedValue` | number | DCF indicated value (sum of present value of cash flows and reversion) |
| `impliedIRR` | number | Implied internal rate of return from DCF analysis (expressed as decimal) |

### 4. salesComparisonApproach

Comparable sales analysis and market-derived valuation adjustments. Each entry represents one comparable sale.

| Field | Type | Description |
|---|---|---|
| `compSalePropertyName` | string | Name of the comparable sale property |
| `compSaleAddress` | string | Address of the comparable sale property |
| `compSaleSaleDate` | string (ISO 8601) | Date of the comparable sale transaction |
| `compSalePrice` | number | Total sale price of the comparable property |
| `compSalePropertyType` | string | Property type of the comparable sale |
| `compSaleSizeSF` | number | Size of the comparable sale property in square feet |
| `compSaleSizeUnits` | number | Number of units in the comparable sale property |
| `compSaleSizeAcres` | number | Land area of the comparable sale property in acres |
| `compSalePricePerSF` | number | Sale price per square foot of the comparable property |
| `compSalePricePerUnit` | number | Sale price per unit of the comparable property |
| `compSaleCapRate` | number | Capitalization rate of the comparable sale (expressed as decimal) |
| `compSaleNOI` | number | Net operating income of the comparable sale property |
| `compSaleBuyer` | string | Buyer name or entity for the comparable sale |
| `compSaleSeller` | string | Seller name or entity for the comparable sale |
| `compSaleBuyerType` | string | Buyer type: institutional, private, or REIT |
| `compSaleFinancing` | string | Financing terms: cash, conventional, assumed, or seller-financed |
| `compSaleConditionsOfSale` | string | Conditions of sale: arm's length, distressed, portfolio, or 1031 exchange |
| `adjustmentPropertyRights` | string | Adjustment for differences in property rights conveyed |
| `adjustmentFinancing` | string | Adjustment for differences in financing terms |
| `adjustmentConditionsOfSale` | string | Adjustment for atypical conditions of sale |
| `adjustmentMarketConditions` | string | Adjustment for market conditions (time adjustment) |
| `adjustmentLocation` | string | Adjustment for location differences |
| `adjustmentPhysical` | string | Adjustment for physical characteristic differences |
| `adjustmentEconomic` | string | Adjustment for economic characteristic differences |
| `adjustmentUse` | string | Adjustment for differences in use or zoning |
| `adjustedSalePricePerSF` | number | Adjusted sale price per square foot after all adjustments |
| `salesComparisonIndicatedValue` | number | Final value indicated by the sales comparison approach |

### 5. costApproach

Replacement/reproduction cost analysis and depreciation.

| Field | Type | Description |
|---|---|---|
| `landValue` | number | Estimated land value |
| `landValueSource` | string | Source of land value estimate: comparable sales, allocation, or extraction |
| `comparableLandSales` | string | Supporting comparable land sale data |
| `replacementCostNewPerSF` | number | Replacement cost new per square foot |
| `replacementCostNewTotal` | number | Total replacement cost new for all improvements |
| `replacementCostSource` | string | Source of replacement cost data: Marshall & Swift, contractor estimate, or published data |
| `depreciationPhysicalPercent` | number | Physical depreciation as a percentage (expressed as decimal, e.g., 0.15) |
| `depreciationPhysicalMethod` | string | Method used for physical depreciation: age-life or observed condition |
| `depreciationFunctionalPercent` | number | Functional depreciation as a percentage (expressed as decimal, e.g., 0.05) |
| `depreciationFunctionalDescription` | string | Description of functional depreciation (superadequacy or deficiency details) |
| `depreciationExternalPercent` | number | External depreciation as a percentage (expressed as decimal, e.g., 0.03) |
| `depreciationExternalDescription` | string | Description of external depreciation (economic or locational factors) |
| `totalDepreciationPercent` | number | Total depreciation as a percentage (expressed as decimal) |
| `totalDepreciationDollar` | number | Total depreciation in dollars |
| `depreciatedCostOfImprovements` | number | Depreciated cost of improvements (replacement cost new minus total depreciation) |
| `siteImprovementsPaving` | number | Cost of site paving improvements |
| `siteImprovementsLandscaping` | number | Cost of site landscaping improvements |
| `siteImprovementsUtilities` | number | Cost of site utility improvements |
| `costApproachIndicatedValue` | number | Value indicated by the cost approach (land value + depreciated improvements + site improvements) |

### 6. marketStudy

Market context for valuation and investment analysis.

| Field | Type | Description |
|---|---|---|
| `msaName` | string | Metropolitan Statistical Area name |
| `submarketDefinition` | string | Definition and boundaries of the submarket |
| `population` | number | Current population of the MSA or submarket |
| `populationGrowthHistoricalPercent` | number | Historical population growth rate (expressed as decimal, e.g., 0.02) |
| `populationGrowthProjectedPercent` | number | Projected population growth rate (expressed as decimal, e.g., 0.015) |
| `employmentTotal` | number | Total employment in the MSA or submarket |
| `employmentBySector` | string | Employment breakdown by sector |
| `unemploymentRatePercent` | number | Unemployment rate (expressed as decimal, e.g., 0.04) |
| `majorEmployers` | array[string] | List of major employers in the market area |
| `employerChanges` | string | Notable employer additions or departures affecting the market |
| `medianHouseholdIncome` | number | Median household income in the market area |
| `incomeGrowthPercent` | number | Income growth rate (expressed as decimal, e.g., 0.03) |
| `supplyTotalInventorySF` | number | Total competitive inventory in square feet |
| `supplyVacancyRatePercent` | number | Market vacancy rate (expressed as decimal, e.g., 0.08) |
| `supplyAvailabilityRatePercent` | number | Market availability rate including sublease space (expressed as decimal, e.g., 0.12) |
| `demandNetAbsorptionQuarterlySF` | number | Quarterly net absorption in square feet |
| `demandNetAbsorptionAnnualSF` | number | Annual net absorption in square feet |
| `demandPreLeasingActivity` | string | Description of pre-leasing activity for new construction |
| `rentalRateTrendAsking` | string | Asking rental rate trend: increasing, stable, or decreasing |
| `rentalRateTrendEffective` | string | Effective rental rate trend: increasing, stable, or decreasing |
| `concessionTrends` | string | Description of current concession trends (free rent, TI allowances) |
| `constructionUnderConstructionSF` | number | Square footage currently under construction |
| `constructionPlannedSF` | number | Square footage in planned pipeline |
| `constructionExpectedDeliveries` | string | Description of expected construction deliveries and timing |
| `forecastVacancy` | string | Vacancy rate forecast: increasing, stable, or decreasing |
| `forecastRentGrowth` | string | Rent growth forecast: increasing, stable, or decreasing |
| `forecastAbsorption` | string | Absorption forecast: positive, neutral, or negative |

### 7. investmentMetrics

Return and risk metrics for investment analysis.

Financial metrics reference `core_commercial_re_na@1.0.0 → financialFundamentals`.

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

### 8. underwriting

Acquisition and disposition underwriting assumptions.

| Field | Type | Description |
|---|---|---|
| `purchasePrice` | number | Proposed or actual purchase price |
| `purchasePricePerSF` | number | Purchase price per square foot |
| `goingInCapRate` | number | Going-in capitalization rate at acquisition (expressed as decimal, e.g., 0.06) |
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
| `exitCapRate` | number | Assumed exit capitalization rate at disposition (expressed as decimal, e.g., 0.07) |
| `dispositionCostsPercent` | number | Disposition costs as a percentage of sale price (expressed as decimal, e.g., 0.02) |
| `sensitivityNOIGrowthRange` | string | NOI growth sensitivity range (e.g., "+/-1.0%") |
| `sensitivityCapRateRange` | string | Capitalization rate sensitivity range (e.g., "+/-25 bps") |
| `sensitivityInterestRateRange` | string | Interest rate sensitivity range (e.g., "+/-50 bps") |
| `scenarioBaseCaseIRR` | number | Base case scenario IRR (expressed as decimal) |
| `scenarioBaseCaseEquityMultiple` | number | Base case scenario equity multiple |
| `scenarioUpsideIRR` | number | Upside scenario IRR (expressed as decimal) |
| `scenarioDownsideIRR` | number | Downside scenario IRR (expressed as decimal) |

### 9. dueDiligence

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
| `zoningCurrent` | string | Current zoning classification |
| `zoningConformance` | string | Zoning conformance status: conforming, non-conforming, or legal non-conforming |
| `zoningVarianceRequired` | boolean | Whether a zoning variance is required for intended use |
| `entitlementStatus` | string | Entitlement status: approved, pending, or required |
| `thirdPartyReports` | array[string] | List of third-party reports obtained (seismic, wind, flood, ADA, parking study) |
| `estoppelCertificateSummary` | string | Summary of tenant estoppel certificate findings |
| `sndaStatus` | string | Subordination, non-disturbance, and attornment agreement status (obtained or pending for each tenant) |

### 10. reconciliationAndConclusion

Final value opinion and reconciliation of valuation approaches.

| Field | Type | Description |
|---|---|---|
| `incomeApproachValue` | number | Value indicated by the income approach |
| `salesComparisonValue` | number | Value indicated by the sales comparison approach |
| `costApproachValue` | number | Value indicated by the cost approach |
| `incomeApproachWeightPercent` | number | Weight assigned to the income approach in reconciliation (as whole number, e.g., 50) |
| `salesComparisonWeightPercent` | number | Weight assigned to the sales comparison approach in reconciliation (as whole number, e.g., 35) |
| `costApproachWeightPercent` | number | Weight assigned to the cost approach in reconciliation (as whole number, e.g., 15) |
| `weightingRationale` | string | Rationale for the weighting of each valuation approach |
| `finalValueConclusion` | number | Final concluded market value |
| `valuePerSF` | number | Final concluded value per square foot |
| `valuePerUnit` | number | Final concluded value per unit |
| `extraordinaryAssumptions` | array[string] | Extraordinary assumptions affecting the value conclusion |
| `hypotheticalConditions` | array[string] | Hypothetical conditions affecting the value conclusion |
| `effectiveDateOfValue` | string (ISO 8601) | Effective date of the value opinion |
| `dateOfReport` | string (ISO 8601) | Date the appraisal report was issued |
| `appraiserName` | string | Name of the appraiser |
| `appraiserDesignation` | string | Appraiser professional designation (MAI, AACI, etc.) |
| `appraiserLicenseNumber` | string | Appraiser license or certification number |
| `intendedUse` | string | Intended use of the appraisal (mortgage lending, acquisition, financial reporting, etc.) |
| `intendedUsers` | string | Intended users of the appraisal report |

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
- **Patch** (1.0.x): Field description clarifications, no schema changes
- **Minor** (1.x.0): New optional fields added, no existing fields removed
- **Major** (x.0.0): Breaking changes — fields renamed, removed, or restructured
