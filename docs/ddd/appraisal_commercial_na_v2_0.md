# Domain Data Dictionary: Appraisal — Commercial North America

**Reference:** `re-ddd:appraisal_commercial_na@2.0.0`

**Scope:** Field definitions for USPAP-compliant commercial real estate property valuation reports in North America, covering engagement metadata, property and site description, three approaches to value, market analysis, highest and best use, stabilization, and reconciliation with multiple valuation premises.

**Relationship to REIXS:** This DDD provides canonical definitions for appraisal report production workflows. It references `core_commercial_re_na@2.0.0` for shared property identification, financial fundamentals, area measurement, market context, revenue/expense line items, and zoning/environmental fields. For rent comparable analysis infrastructure, see also `leasing_commercial_na@1.0.0 → comparableLeases`. Investment analysis workflows (DCF projections, underwriting, due diligence) are defined in the separate `investment_commercial_na@1.0.0`.

---

## Sections

The schema defines **12 sections** with **240 fields** total (including 14 cross-referenced pointer fields and 1 section fully delegated to core). All sections represent data found in or derived from formal commercial real estate appraisal reports.

### 1. engagementMetadata

Appraisal engagement details, compliance standards, and appraiser credentials.

| Field | Type | Description |
|---|---|---|
| `appraisalFirm` | string | Name of the appraisal firm |
| `appraisalFirmAddress` | string | Address of the appraisal firm |
| `clientName` | string | Name of the client who engaged the appraisal |
| `clientAddress` | string | Address of the client |
| `intendedUse` | string | Intended use of the appraisal (mortgage lending, acquisition, financial reporting, litigation, etc.) |
| `intendedUsers` | string | Intended users of the appraisal report |
| `typeOfValue` | string | Type of value opinion: market value, liquidation value, investment value, insurable value |
| `propertyInterestAppraised` | string | Property interest appraised: fee simple, leased fee, leasehold |
| `effectiveDateOfValue` | string (ISO 8601) | Effective date of the value opinion |
| `dateOfReport` | string (ISO 8601) | Date the appraisal report was issued |
| `dateOfInspection` | string (ISO 8601) | Date of the most recent property inspection |
| `inspectionScope` | string | Scope of inspection: interior and exterior, exterior only, or desktop |
| `complianceStandards` | array[string] | Applicable standards: USPAP, FIRREA, IVS, CUSPAP |
| `reportFormat` | string | Report format: appraisal report, restricted appraisal report |
| `approachesUsed` | array[string] | Valuation approaches applied: income capitalization, sales comparison, cost |
| `extraordinaryAssumptions` | array[string] | Extraordinary assumptions affecting the value conclusion |
| `hypotheticalConditions` | array[string] | Hypothetical conditions affecting the value conclusion |
| `leadAppraiserName` | string | Name of the lead/signing appraiser |
| `leadAppraiserDesignation` | string | Lead appraiser professional designation (MAI, SRA, AACI, etc.) |
| `leadAppraiserLicenseNumber` | string | Lead appraiser license or certification number |
| `leadAppraiserLicenseState` | string | State or province of lead appraiser licensure |
| `secondAppraiserName` | string | Name of the second/co-signing appraiser, if applicable |
| `secondAppraiserDesignation` | string | Second appraiser professional designation |
| `secondAppraiserLicenseNumber` | string | Second appraiser license or certification number |

### 2. propertyDescription

Physical building characteristics for valuation. Property identity fields reference `core_commercial_re_na@2.0.0 → propertyIdentification`.

| Field | Type | Description |
|---|---|---|
| `propertyReference` | string | Reference to core property identification record (`core_commercial_re_na@2.0.0 → propertyIdentification`) |
| `grossBuildingArea` | number | → `core@2.0.0 → areaAndMeasurement.grossBuildingArea` |
| `rentableArea` | number | → `core@2.0.0 → areaAndMeasurement.rentableArea` |
| `usableArea` | number | → `core@2.0.0 → areaAndMeasurement.usableArea` |
| `numberOfFloors` | number | Total number of above-grade floors |
| `numberOfBelowGradeFloors` | number | Number of below-grade floors |
| `numberOfUnits` | number | Total number of rentable units |
| `unitMix` | string | Unit mix breakdown by type, count, and square footage |
| `averageUnitSizeSF` | number | Average unit size in square feet |
| `constructionType` | string | Construction type: steel frame, concrete, wood frame, masonry, or mixed |
| `foundationType` | string | Foundation type: spread footing, mat/raft, pier, or slab-on-grade |
| `structuralSystem` | string | Primary structural system description |
| `exteriorWalls` | string | Exterior wall materials and finish |
| `roofType` | string | Roof type: flat, pitched, membrane, metal, or built-up |
| `roofAge` | number | Approximate age of the current roof in years |
| `windowType` | string | Window type and glazing description |
| `hvacSystem` | string | HVAC system type and description |
| `hvacAge` | number | Approximate age of the HVAC system in years |
| `electricalSystem` | string | Electrical service description (amps, phase, voltage) |
| `plumbingSystem` | string | Plumbing system description |
| `elevators` | string | Elevator count, type, and capacity |
| `fireProtection` | string | Fire protection system: sprinklered, smoke detection, fire alarm |
| `interiorFinish` | string | General interior finish quality and description |
| `parkingType` | string | Parking type: surface, structured, underground, or combination |
| `parkingSpaces` | number | Total number of parking spaces |
| `parkingRatio` | number | Parking ratio expressed as spaces per 1,000 square feet |
| `conditionRating` | string | Overall condition rating: excellent, good, fair, or poor |
| `conditionBasis` | string | Basis for condition rating: inspection, report, or assumption |
| `effectiveAge` | number | Effective age of the improvements in years |
| `remainingEconomicLife` | number | Estimated remaining economic life in years |
| `totalEconomicLife` | number | Total estimated economic life in years |
| `renovationYear` | number | Year of most recent renovation |
| `renovationScope` | string | Description of renovation scope and work performed |
| `renovationCost` | number | Total cost of renovation |
| `deferredMaintenanceItems` | string | Description of deferred maintenance items observed |
| `functionalUtilityAssessment` | string | Assessment of the property's functional utility and layout efficiency |
| `adaCompliance` | string | ADA compliance status: compliant, partially compliant, non-compliant |

### 3. siteDescription

Land and site characteristics. Area measurement references `core_commercial_re_na@2.0.0 → areaAndMeasurement`.

| Field | Type | Description |
|---|---|---|
| `siteAreaSF` | number | Total site area in square feet |
| `siteAreaAcres` | number | Total site area in acres |
| `siteFrontage` | number | Site frontage in linear feet |
| `siteFrontageStreet` | string | Name of the street providing primary frontage |
| `siteDepth` | number | Site depth in linear feet |
| `siteShape` | string | Site shape: regular, irregular, rectangular, or triangular |
| `siteTopography` | string | Site topography: level, gently sloping, sloping, or steep |
| `soilCondition` | string | Known soil conditions or geotechnical considerations |
| `floodZoneDesignation` | string | FEMA flood zone designation (e.g., Zone X, Zone AE) |
| `floodMapNumber` | string | FEMA flood insurance rate map panel number |
| `floodMapDate` | string (ISO 8601) | Effective date of the flood map |
| `wetlandsPresent` | boolean | Whether wetlands are present on the site |
| `wetlandsDescription` | string | Description of wetland areas and restrictions |
| `utilitiesWater` | string | Water service: public, well, or none |
| `utilitiesSewer` | string | Sewer service: public, septic, or none |
| `utilitiesGas` | string | Gas service: natural gas, propane, or none |
| `utilitiesElectric` | string | Electric service provider and capacity |
| `utilitiesStormDrainage` | string | Storm drainage description |
| `streetImprovements` | string | Description of street improvements: paved, curb, gutter, sidewalk |
| `easements` | string | Description of known easements affecting the site |
| `environmentalHazards` | string | Known or suspected environmental hazards |
| `accessIngress` | string | Description of site access and ingress/egress points |

### 4. taxAndAssessment

Real property tax and assessment data.

| Field | Type | Description |
|---|---|---|
| `assessorParcelNumber` | string | Assessor's parcel number (APN) |
| `taxingAuthority` | string | Primary taxing authority or jurisdiction |
| `assessedValueLand` | number | Assessed value of land |
| `assessedValueImprovements` | number | Assessed value of improvements |
| `assessedValueTotal` | number | Total assessed value |
| `assessmentYear` | number | → `core@2.0.0 → revenueAndExpenseLineItems.assessmentYear` |
| `assessmentRatio` | number | Assessment ratio to market value (expressed as decimal, e.g., 0.40) |
| `taxRateMills` | number | Tax rate in mills or per dollar of assessed value |
| `annualTaxes` | number | Current annual real property taxes |
| `specialAssessments` | string | Description of any special assessments or tax districts |
| `specialAssessmentAmount` | number | Annual amount of special assessments |
| `taxExemptions` | string | Any tax exemptions or abatements in effect |
| `taxExemptionExpiration` | string (ISO 8601) | Expiration date of tax exemption or abatement |
| `phaseInStatus` | string | Whether assessed value is being phased in over multiple years |
| `taxGrievanceStatus` | string | Status of any pending tax grievance or appeal |
| `taxGrievanceYear` | number | Year of pending tax grievance |
| `taxComparableAssessments` | string | Comparable property assessment data supporting tax analysis |

### 5. zoning

Zoning classification, conformance, and permitted uses.

| Field | Type | Description |
|---|---|---|
| `zoningClassification` | string | → `core@2.0.0 → propertyIdentification.zoningClassification` |
| `zoningDescription` | string | Description of the zoning district |
| `zoningAuthority` | string | Municipal or county zoning authority |
| `permittedUsesPrincipal` | array[string] | Principal permitted uses under current zoning |
| `permittedUsesAccessory` | array[string] | Accessory permitted uses under current zoning |
| `conditionalUses` | array[string] | Conditional or special exception uses available |
| `maxBuildingHeight` | string | Maximum permitted building height |
| `maxFloorAreaRatio` | number | Maximum permitted floor area ratio |
| `maxLotCoverage` | number | Maximum lot coverage (expressed as decimal, e.g., 0.60) |
| `minSetbacks` | string | Minimum setback requirements: front, side, rear |
| `minParkingRequired` | string | Minimum parking requirements for the current use |
| `zoningConformance` | string | → `core@2.0.0 → zoningAndEnvironmental.zoningConformance` |
| `nonConformingDetails` | string | Details of non-conforming status and grandfathering provisions |
| `varianceRequired` | boolean | → `core@2.0.0 → zoningAndEnvironmental.varianceRequired` |
| `varianceDescription` | string | Description of required or granted variance |
| `overlayDistricts` | string | Any applicable overlay or special zoning districts |

### 6. marketAnalysis

> **Shared fields:** Uses `re-ddd:core_commercial_re_na@2.0.0 → marketContext` for all market analysis fields.

This section contains no domain-specific fields beyond core. Reference the core marketContext section for the complete field list.

### 7. highestAndBestUse

Highest and best use analysis for both vacant site and as-improved scenarios.

| Field | Type | Description |
|---|---|---|
| `vacantLegallyPermissible` | string | Legally permissible uses for the vacant site |
| `vacantPhysicallyPossible` | string | Physically possible uses for the vacant site |
| `vacantFinanciallyFeasible` | string | Financially feasible uses for the vacant site |
| `vacantMaximallyProductive` | string | Maximally productive use of the vacant site |
| `vacantConclusion` | string | Highest and best use conclusion assuming the site is vacant |
| `improvedLegallyPermissible` | string | Legally permissible uses as improved |
| `improvedPhysicallyPossible` | string | Physically possible uses as improved |
| `improvedFinanciallyFeasible` | string | Financially feasible uses as improved |
| `improvedMaximallyProductive` | string | Maximally productive use as improved |
| `improvedConclusion` | string | Highest and best use conclusion as improved |
| `demolitionFeasibilityAnalysis` | string | Analysis of whether demolition is financially feasible |
| `mostLikelyBuyer` | string | Most likely buyer profile for the subject property |

### 8. incomeCapitalizationApproach

Direct capitalization and income-based valuation with rent comparables, itemized expenses, and vacancy analysis.

Financial metrics reference `core_commercial_re_na@2.0.0 → financialFundamentals`.

| Field | Type | Description |
|---|---|---|
| `rentComparableCount` | number | Number of rent comparables analyzed |
| `rentCompPropertyName` | string | Name of the rent comparable property (per comparable) |
| `rentCompAddress` | string | Address of the rent comparable (per comparable) |
| `rentCompUnitType` | string | Unit type of the rent comparable: office, retail, apartment, industrial |
| `rentCompAreaSF` | number | Area of the comparable unit in square feet |
| `rentCompRentPerSF` | number | Rent per square foot per annum of the comparable |
| `rentCompRentMonthly` | number | Monthly rent of the comparable unit |
| `rentCompLeaseType` | string | Lease type: gross, modified gross, NNN, full-service |
| `rentCompTIAllowance` | number | Tenant improvement allowance per square foot |
| `rentCompFreeRentMonths` | number | Free rent concession in months |
| `rentCompEffectiveRent` | number | Effective rent after concession adjustments |
| `rentCompLeaseDate` | string (ISO 8601) | Date of the comparable lease |
| `rentCompAdjustments` | string | Summary of adjustments applied to the comparable |
| `marketRentPerSF` | number | → `core@2.0.0 → revenueAndExpenseLineItems.marketRentPerSF` — appraisal-concluded context |
| `concludedMarketRentMonthly` | number | Concluded market rent per month per unit |
| `potentialGrossIncome` | number | Total potential gross income assuming full occupancy at market rents |
| `vacancyRatePercent` | number | Vacancy allowance as a percentage (expressed as decimal, e.g., 0.05) |
| `vacancyLossDollar` | number | Vacancy loss in dollars |
| `collectionLossPercent` | number | Collection loss allowance as a percentage (expressed as decimal) |
| `collectionLossDollar` | number | Collection loss in dollars |
| `otherIncome` | number | Other income (parking, laundry, storage, etc.) |
| `otherIncomeDetail` | string | Breakdown of other income sources |
| `effectiveGrossIncome` | number | → `core@2.0.0 → financialFundamentals.effectiveGrossIncome` |
| `expenseRealEstateTaxes` | number | Real estate tax expense |
| `expenseInsurance` | number | → `core@2.0.0 → revenueAndExpenseLineItems.expenseInsurance` |
| `expenseManagement` | number | Management fee expense |
| `expenseManagementPercent` | number | Management fee as percentage of EGI (expressed as decimal) |
| `expenseUtilities` | number | → `core@2.0.0 → revenueAndExpenseLineItems.expenseUtilities` |
| `expenseRepairsMaintenance` | number | → `core@2.0.0 → revenueAndExpenseLineItems.expenseRepairsMaintenance` |
| `expenseReserves` | number | Replacement reserves expense |
| `expenseOther` | number | Other operating expenses |
| `expenseOtherDetail` | string | Breakdown of other operating expenses |
| `totalOperatingExpenses` | number | Total operating expenses |
| `operatingExpenseRatio` | number | → `core@2.0.0 → revenueAndExpenseLineItems.operatingExpenseRatio` |
| `noi` | number | → `core@2.0.0 → financialFundamentals.noi` |
| `capRateSource` | string | Source of capitalization rate: market extraction, band of investment, or survey |
| `capRateSelected` | number | Selected capitalization rate (expressed as decimal, e.g., 0.065) |
| `capRateMarketExtractionData` | string | Supporting comparable property capitalization rate data |
| `directCapitalizationValue` | number | Value indicated by direct capitalization (NOI / cap rate) |
| `stabilizedVsAsIs` | string | Basis of income analysis: stabilized or as-is |
| `aboveBelowMarketLeaseAdjustment` | number | Dollar adjustment for above- or below-market lease terms |
| `aboveBelowMarketLeaseDetail` | string | Explanation of above- or below-market lease adjustment |
| `incomeApproachIndicatedValue` | number | Final value indicated by the income approach |

### 9. salesComparisonApproach

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

### 10. costApproach

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
| `insurableReplacementCostTotal` | number | Insurable replacement cost (excluding land, foundation, underground) |
| `insurableReplacementCostBasis` | string | Basis for insurable replacement cost estimate |
| `costApproachIndicatedValue` | number | Value indicated by the cost approach (land value + depreciated improvements + site improvements) |

### 11. stabilizationAnalysis

Lease-up and stabilization adjustments for properties not at stabilized occupancy.

| Field | Type | Description |
|---|---|---|
| `currentOccupancyPercent` | number | Current occupancy rate (expressed as decimal, e.g., 0.75) |
| `stabilizedOccupancyPercent` | number | Stabilized occupancy rate assumed (expressed as decimal, e.g., 0.95) |
| `leaseUpPeriodMonths` | number | Estimated lease-up period in months to reach stabilized occupancy |
| `stabilizationDate` | string (ISO 8601) | Projected date of stabilization |
| `leaseUpRentLoss` | number | Rent loss during lease-up period |
| `leaseUpConcessions` | number | Concession costs during lease-up (free rent, reduced rent) |
| `tenantImprovementCosts` | number | Tenant improvement costs for new leases during lease-up |
| `leasingCommissions` | number | Leasing commission costs during lease-up |
| `entrepreneurialIncentive` | number | Entrepreneurial incentive or developer's profit allowance |
| `totalLeaseUpCosts` | number | Total lease-up costs (rent loss + concessions + TI + commissions) |
| `stabilizedValueBeforeDeductions` | number | Stabilized value before deducting lease-up costs |
| `asIsValueAfterDeductions` | number | As-is value after deducting lease-up costs from stabilized value |
| `absorptionRateUnitsPerMonth` | number | Assumed absorption rate in units per month |

### 12. reconciliationAndConclusion

Final value opinion, reconciliation of approaches, and multiple valuation premises.

| Field | Type | Description |
|---|---|---|
| `incomeApproachValue` | number | Value indicated by the income approach |
| `salesComparisonValue` | number | Value indicated by the sales comparison approach |
| `costApproachValue` | number | Value indicated by the cost approach |
| `incomeApproachWeightPercent` | number | Weight assigned to the income approach in reconciliation (as whole number, e.g., 50) |
| `salesComparisonWeightPercent` | number | Weight assigned to the sales comparison approach in reconciliation (as whole number, e.g., 35) |
| `costApproachWeightPercent` | number | Weight assigned to the cost approach in reconciliation (as whole number, e.g., 15) |
| `weightingRationale` | string | Rationale for the weighting of each valuation approach |
| `marketValueAsIs` | number | Concluded market value under as-is conditions |
| `marketValueAsIsPerSF` | number | As-is market value per square foot |
| `marketValueAsIsPerUnit` | number | As-is market value per unit |
| `marketValueStabilized` | number | Concluded market value upon stabilization |
| `marketValueStabilizedPerSF` | number | Stabilized market value per square foot |
| `marketValueStabilizedDate` | string (ISO 8601) | Prospective date for stabilized value opinion |
| `marketValueAsComplete` | number | Concluded prospective market value upon completion (if applicable) |
| `marketValueAsCompleteDate` | string (ISO 8601) | Prospective date for as-complete value opinion |
| `insuredValue` | number | Insurable value conclusion, if applicable |
| `liquidationValue` | number | Liquidation value conclusion, if applicable |
| `exposureTimeDays` | number | Estimated exposure time in days for market value |
| `marketingTimeDays` | number | Estimated marketing time in days for market value |
| `finalValueConclusion` | number | Primary concluded market value (typically as-is or stabilized per engagement) |
| `valuePerSF` | number | Primary concluded value per square foot |
| `valuePerUnit` | number | Primary concluded value per unit |
| `valuationPremiseOfFinalConclusion` | string | Valuation premise of the primary conclusion: as-is, stabilized, as-complete |

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
