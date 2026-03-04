# Domain Data Dictionary: Leasing — Commercial North America

**Reference:** `re-ddd:leasing_commercial_na@2.0.0`

**Scope:** Field definitions for commercial leasing operations including deal pipeline, market analysis, and transaction execution in North America.

**Relationship to REIXS:** This DDD defines leasing-specific fields for market intelligence, deal structuring, and transaction management. It references the core glossary (`re-ddd:core_commercial_re_na@2.0.0`) for shared property identification, financial fundamentals, party representation, area measurement, revenue/expense line items, market context, and lease classification concepts rather than redefining them.

---

## Sections

The schema defines **10 sections** with **191 fields** total (5 cross-referenced from `core@2.0.0`). Sections cover the full leasing lifecycle from market analysis through deal execution and tenant retention.

### 1. marketAnalysis

Submarket and competitive intelligence.

> **Note:** For macro-level MSA and demographic data, see `re-ddd:core_commercial_re_na@2.0.0 → marketContext`. This section covers submarket-level competitive intelligence specific to leasing.

| Field | Type | Description |
|---|---|---|
| `submarketName` | string | Name of the submarket area |
| `metroArea` | string | Metropolitan statistical area |
| `geographicBoundaries` | string | Description of submarket geographic boundaries |
| `vacancyRateDirect` | number | Direct vacancy rate (expressed as decimal, e.g., 0.08) |
| `vacancyRateSublease` | number | Sublease vacancy rate (expressed as decimal, e.g., 0.02) |
| `vacancyRateTotal` | number | Total vacancy rate combining direct and sublease (expressed as decimal) |
| `vacancyTrend` | string | Direction of vacancy movement: increasing, stable, decreasing |
| `netAbsorptionQuarterlySF` | number | Net absorption for the quarter (sq ft) |
| `netAbsorptionAnnualSF` | number | Net absorption for the trailing twelve months (sq ft) |
| `averageAskingRentGross` | number | Average gross asking rent in the submarket (per SF per annum) |
| `averageAskingRentNet` | number | Average net asking rent in the submarket (per SF per annum) |
| `askingRentTrend` | string | Direction of asking rent movement: increasing, stable, decreasing |
| `averageFreeRentMonths` | number | Average free rent concession in the submarket (months) |
| `averageTIPerSF` | number | Average tenant improvement allowance in the submarket (per SF) |
| `competitiveSetProperties` | array[string] | Comparable buildings in the competitive set |
| `constructionPipelineSF` | number | Square footage currently under construction in the submarket |
| `constructionExpectedDelivery` | string | Expected delivery timeline for construction pipeline |
| `keyDemandDrivers` | array[string] | Primary demand drivers in the submarket (e.g., tech expansion, government) |

### 2. comparableLeases

Lease comparable transactions. Each entry represents one comparable lease used to support market rent conclusions and deal structuring.

| Field | Type | Description |
|---|---|---|
| `compPropertyName` | string | Property name of the comparable lease |
| `compAddress` | string | Street address of the comparable property |
| `compSubmarket` | string | Submarket of the comparable property |
| `compTenantName` | string | Tenant name in the comparable lease |
| `compTenantIndustry` | string | Industry classification of the comparable tenant |
| `compTransactionDate` | string (ISO 8601) | Date the comparable transaction was reported or recorded |
| `compLeaseExecutionDate` | string (ISO 8601) | Date the comparable lease was executed |
| `compSuiteFloor` | string | Suite number or floor of the comparable lease |
| `compAreaSF` | number | Leased area of the comparable (sq ft) |
| `compLeaseTermYears` | number | Lease term in years |
| `compLeaseTermMonths` | number | Lease term in months (for precision or short-term leases) |
| `compCommencementDate` | string (ISO 8601) | Lease commencement date |
| `compBaseRentPerSF` | number | Starting base rent (per SF per annum) |
| `compBaseRentAnnual` | number | Starting base rent (total annual) |
| `compEscalationType` | string | Escalation structure: fixed, CPI, market reset |
| `compEscalationRate` | number | Annual escalation rate (expressed as decimal, e.g., 0.03) |
| `compTIAllowancePerSF` | number | Tenant improvement allowance (per SF) |
| `compFreeRentMonths` | number | Free rent concession (months) |
| `compEffectiveRentPerSF` | number | Effective rent after concessions (per SF per annum) |
| `compEffectiveRentAnnual` | number | Effective rent after concessions (total annual) |
| `compLeaseTransactionType` | string | Transaction type: new, renewal, expansion, blend-and-extend |
| `compNetGrossClassification` | string | Lease structure: net, gross, modified gross |
| `compBrokers` | array[string] | Brokers involved in the comparable transaction |
| `compListingProcuringSide` | string | Side of the transaction: listing, procuring |

### 3. tenantScreening

Prospect qualification and credit analysis for potential tenants.

| Field | Type | Description |
|---|---|---|
| `party.prospect.name` | string | → `core@2.0.0 → parties` with role=prospect |
| `prospectIndustry` | string | Industry classification of the prospect |
| `prospectHQLocation` | string | Headquarters location of the prospect |
| `spaceRequirementSF` | number | Total space requirement (sq ft) |
| `layoutPreference` | string | Preferred layout type (e.g., open plan, private offices, hybrid) |
| `floorPreference` | string | Preferred floor or floor range |
| `targetOccupancyDate` | string (ISO 8601) | Desired occupancy date |
| `leaseTermPreferenceYears` | number | Desired lease term (years) |
| `financialRevenue` | number | Prospect's annual revenue |
| `financialAssets` | number | Prospect's total assets |
| `financialNetWorth` | number | Prospect's net worth |
| `creditRatingAgency` | string | Rating agency: S&P, Moody's, Fitch |
| `creditRating` | string | Credit rating from the specified agency |
| `dnbRating` | string | Dun & Bradstreet rating |
| `publicPrivate` | string | Entity status: public, private |
| `parentEntity` | string | Parent company or guarantor entity name |
| `litigationHistoryMaterial` | boolean | Whether the prospect has material litigation history |
| `bankruptcyHistory` | boolean | Whether the prospect has prior bankruptcy filings |
| `currentLocation` | string | Prospect's current office location |
| `reasonForMove` | string | Primary reason for relocation or expansion |
| `references` | array[string] | References such as current landlord, banker, trade references |

### 4. dealStructuring

Deal economics, concessions, and option terms.

| Field | Type | Description |
|---|---|---|
| `proposedBaseRentPerSF` | number | Proposed starting base rent (per SF per annum) |
| `proposedBaseRentAnnual` | number | Proposed starting base rent (total annual) |
| `proposedBaseRentMonthly` | number | Proposed starting base rent (total monthly) |
| `escalationStructure` | string | Escalation method: fixed %, CPI, market reset |
| `escalationRatePercent` | number | Annual escalation rate (expressed as decimal, e.g., 0.03) |
| `tiAllowancePerSF` | number | → `core@2.0.0 → revenueAndExpenseLineItems.tiAllowancePerSF` |
| `tiAllowanceTotal` | number | Total tenant improvement allowance |
| `tiAmortizationTermYears` | number | Amortization period for unamortized TI if tenant vacates early (years) |
| `freeRentMonths` | number | → `core@2.0.0 → revenueAndExpenseLineItems.freeRentMonths` |
| `freeRentPlacement` | string | Timing of free rent: upfront, distributed, end-of-term |
| `expansionOptionSF` | number | Square footage available under expansion option |
| `expansionOptionTiming` | string | Exercise window or conditions for expansion option |
| `expansionOptionRentDetermination` | string | Method for determining rent on expansion space |
| `contractionOptionSF` | number | Square footage that may be surrendered under contraction option |
| `contractionOptionTiming` | string | Exercise window or conditions for contraction option |
| `contractionOptionPenalty` | number | Penalty amount for exercising contraction option |
| `terminationRightTiming` | string | Exercise window or conditions for early termination right |
| `terminationRightPenalty` | number | Penalty amount for exercising early termination |
| `terminationRightNoticePeriod` | string | Required notice period for early termination |
| `renewalOptionCount` | number | Number of renewal options |
| `renewalOptionTermYears` | number | Term length of each renewal option (years) |
| `renewalOptionRentDetermination` | string | Method for determining rent at renewal (e.g., fair market value, fixed increase) |
| `parkingAllocation` | number | Number of parking spaces allocated |
| `parkingRate` | number | Parking rate (per space per month) |
| `landlordTotalCost` | number | Total landlord cost including TI, free rent, commissions, and legal |
| `netEffectiveRent` | number | Net effective rent after all concessions (per SF per annum) |
| `landlordROI` | number | Landlord return on investment — NPV of deal cash flows |

### 5. loiAndProposal

Letter of intent lifecycle and proposal tracking.

| Field | Type | Description |
|---|---|---|
| `loiStatus` | string | Current LOI status: draft, issued, countered, accepted, expired, withdrawn |
| `loiVersionNumber` | number | Version number of the current LOI |
| `loiDateIssued` | string (ISO 8601) | Date the LOI was issued |
| `loiExpirationDate` | string (ISO 8601) | Date the LOI expires |
| `loiIssuingParty` | string | Entity that issued the LOI |
| `loiCounterparty` | string | Entity receiving the LOI |
| `loiKeyTermsRent` | string | Proposed rent terms summarized in the LOI |
| `loiKeyTermsTerm` | string | Proposed lease term summarized in the LOI |
| `loiKeyTermsTI` | string | Proposed TI allowance summarized in the LOI |
| `loiKeyTermsFreeRent` | string | Proposed free rent summarized in the LOI |
| `loiKeyTermsCommencement` | string | Proposed commencement date summarized in the LOI |
| `bindingExclusivity` | boolean | Whether the exclusivity provision is binding |
| `bindingConfidentiality` | boolean | Whether the confidentiality provision is binding |
| `bindingCosts` | string | Description of binding cost-sharing provisions |
| `nonBindingBusinessTerms` | string | Summary of non-binding business terms in the LOI |
| `counterVersion` | number | Counter-offer version number |
| `counterDate` | string (ISO 8601) | Date the counter-offer was issued |
| `counterKeyChanges` | string | Summary of key changes in the counter-offer |
| `exclusivityPeriodStart` | string (ISO 8601) | Start date of exclusivity period |
| `exclusivityPeriodEnd` | string (ISO 8601) | End date of exclusivity period |
| `transitionToLeaseDraftingDate` | string (ISO 8601) | Date the deal transitioned from LOI to lease drafting |

### 6. commissionAndFees

Brokerage compensation and fee structures.

| Field | Type | Description |
|---|---|---|
| `commissionRatePercent` | number | Commission rate as percentage of aggregate rent (expressed as decimal, e.g., 0.04) |
| `commissionStructure` | string | Commission payment structure: flat, tiered, front-loaded |
| `listingBroker` | string | Name of the listing broker or brokerage firm |
| `listingBrokerSharePercent` | number | Listing broker's share of total commission (expressed as decimal) |
| `procuringBroker` | string | Name of the procuring (tenant-side) broker or brokerage firm |
| `procuringBrokerSharePercent` | number | Procuring broker's share of total commission (expressed as decimal) |
| `totalCommissionAmount` | number | Total commission amount |
| `paymentSchedule` | string | Commission payment timing: on execution, on occupancy, installments |
| `overrideProvisions` | string | Commission provisions for renewals, expansions, or other override events |
| `referralFeePercent` | number | Referral fee as percentage of commission (expressed as decimal) |
| `referralFeeTo` | string | Entity or individual receiving the referral fee |
| `coBrokerageTerms` | string | Terms of co-brokerage arrangement if applicable |

### 7. spacePlanning

Available space inventory, test fits, and planning metrics.

| Field | Type | Description |
|---|---|---|
| `availableSuite` | string | Suite identifier for available space |
| `availableFloor` | number | Floor number of available space |
| `availableSF` | number | Square footage of available space |
| `availableAskingRent` | number | Asking rent for available space (per SF per annum) |
| `availabilityDate` | string (ISO 8601) | Date the space becomes available |
| `typicalFloorPlateSF` | number | Typical floor plate size (sq ft) |
| `testFitSeatCount` | number | Number of seats in the test fit layout |
| `testFitSFPerSeat` | number | Square footage per seat in the test fit |
| `testFitCollaborationRatio` | number | Ratio of collaboration space to total space (expressed as decimal) |
| `testFitPrivateOfficeCount` | number | Number of private offices in the test fit layout |
| `canSubdivide` | boolean | Whether the space can be subdivided |
| `minimumDivisibleSF` | number | Minimum divisible unit of the space (sq ft) |
| `buildingAmenities` | array[string] | Building amenities available to tenants |
| `efficiencyRatio` | number | → `core@2.0.0 → areaAndMeasurement.efficiencyRatio` |
| `contiguousBlockSF` | number | Largest contiguous block of available space (sq ft) |
| `subleaseAvailableTenant` | string | Current tenant offering sublease space |
| `subleaseTermRemainingMonths` | number | Remaining term on the sublease (months) |
| `subleaseAskingRent` | number | Asking rent for sublease space (per SF per annum) |

### 8. tenantRetention

Renewal probability assessment and retention tracking.

| Field | Type | Description |
|---|---|---|
| `retentionTenantName` | string | Name of the tenant being evaluated for retention |
| `currentLeaseExpiry` | string (ISO 8601) | Current lease expiration date |
| `noticeDeadline` | string (ISO 8601) | Deadline for tenant to provide renewal or termination notice |
| `renewalProbability` | string | Assessed renewal probability: high, medium, low |
| `renewalProbabilityBasis` | string | Basis for renewal probability assessment |
| `proposedRenewalTerms` | string | Summary of proposed renewal terms offered to tenant |
| `currentRentPerSF` | number | Tenant's current rent (per SF per annum) |
| `marketRentPerSF` | number | Current market rent for comparable space (per SF per annum) |
| `markToMarketPercent` | number | Percentage change from current rent to market rent (expressed as decimal) |
| `estimatedVacancyCostDowntime` | number | Estimated downtime if tenant vacates (months) |
| `estimatedVacancyCostTI` | number | Estimated TI cost to re-tenant the space |
| `estimatedVacancyCostCommissions` | number | Estimated leasing commission cost to re-tenant the space |
| `competitiveThreats` | array[string] | Buildings the tenant is considering as alternatives |
| `earlyRenewalIncentive` | string | Description of incentive offered for early renewal commitment |
| `retentionRateAnnual` | number | Annual tenant retention rate for the property (expressed as decimal) |

### 9. pipelineTracking

Deal pipeline stages and forecasting metrics.

| Field | Type | Description |
|---|---|---|
| `dealId` | string | Unique identifier for the deal |
| `prospectName` | string | Name of the prospective tenant |
| `dealSpace` | string | Description of the space (suite/floor) associated with the deal |
| `dealSF` | number | Square footage of the deal (sq ft) |
| `dealStage` | string | Current pipeline stage: prospect, tour, proposal, LOI, lease-negotiation, executed |
| `stageEntryDate` | string (ISO 8601) | Date the deal entered its current stage |
| `daysInStage` | number | Number of days the deal has been in its current stage |
| `probabilityPercent` | number | Estimated probability of closing (expressed as decimal, e.g., 0.75) |
| `expectedCloseDate` | string (ISO 8601) | Expected date of lease execution |
| `expectedCommencementDate` | string (ISO 8601) | Expected lease commencement date |
| `weightedDealValue` | number | Weighted deal value — annual rent multiplied by probability |
| `brokerAssignment` | string | Broker or team assigned to the deal |
| `listingAgent` | string | Listing agent responsible for the space |
| `nextAction` | string | Next action required to advance the deal |
| `nextActionDate` | string (ISO 8601) | Target date for the next action |
| `lostDealReason` | string | Reason the deal was lost if applicable |

### 10. marketRentOpinion

Concluded market rent with supporting methodology and adjustments.

| Field | Type | Description |
|---|---|---|
| `mroPropertyAddress` | string | Address of the subject property |
| `mroUnitSuite` | string | Unit or suite being evaluated |
| `mroFloor` | number | Floor number of the subject space |
| `mroSF` | number | Square footage of the subject space (sq ft) |
| `marketRentPerSF` | number | → `core@2.0.0 → revenueAndExpenseLineItems.marketRentPerSF` — leasing-concluded context |
| `concludedMarketRentPerAnnum` | number | Concluded market rent (total annual) |
| `rentBasis` | string | Rent structure basis: gross, net, modified gross |
| `effectiveDate` | string (ISO 8601) | Effective date of the market rent opinion |
| `comparableLeasesUsed` | array[string] | References to comparable lease entries used in the analysis |
| `adjustmentLocation` | string | Description of location adjustment applied to comparables |
| `adjustmentSize` | string | Description of size adjustment applied to comparables |
| `adjustmentCondition` | string | Description of condition adjustment applied to comparables |
| `adjustmentFloorLevel` | string | Description of floor level adjustment applied to comparables |
| `adjustmentLeaseTerm` | string | Description of lease term adjustment applied to comparables |
| `adjustmentTI` | string | Description of TI adjustment applied to comparables |
| `exposureTimeEstimate` | string | Estimated exposure time for the space (e.g., "3-6 months") |
| `supportingNarrative` | string | Narrative supporting the concluded market rent |
| `preparedBy` | string | Person or entity that prepared the market rent opinion |
| `datePrepared` | string (ISO 8601) | Date the market rent opinion was prepared |

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
