# Domain Data Dictionary: Property Management — Commercial North America

**Reference:** `re-ddd:property_management_commercial_na@2.0.0`

**Scope:** Field definitions for property management operations across commercial office and industrial properties in North America.

**Relationship to REIXS:** This DDD provides canonical definitions for property management workflows including tenant relations, rent collection, maintenance, vendor oversight, budgeting, compliance, and performance reporting. It references `core_commercial_re_na@2.0.0` for shared party representation, area measurement, and revenue/expense line item fields. Where concepts overlap with the core glossary, this DDD uses cross-reference pointers rather than redefining shared terms.

---

## Sections

The schema defines **10 sections** with **166 fields** total (including 17 cross-referenced pointer fields). All sections represent operational data used in day-to-day property management of commercial office and industrial assets.

### 1. tenantManagement

Tenant roster and relationship tracking.

Tenant identity fields reference `core_commercial_re_na@2.0.0 → parties` with role=tenant.

| Field | Type | Description |
|---|---|---|
| `party.tenant.name` | string | → `core@2.0.0 → parties` with role=tenant |
| `leaseReference` | string | Internal lease identifier or reference number |
| `unitSuite` | string | Unit or suite number occupied by the tenant |
| `party.tenant.contactName` | string | → `core@2.0.0 → parties` with role=tenant |
| `party.tenant.contactPhone` | string | → `core@2.0.0 → parties` with role=tenant |
| `party.tenant.contactEmail` | string | → `core@2.0.0 → parties` with role=tenant |
| `moveInDate` | string (ISO 8601) | Date the tenant took physical occupancy |
| `moveOutDate` | string (ISO 8601) | Date the tenant vacated or is scheduled to vacate |
| `leaseStatus` | string | Current lease status: active, expired, holdover, pending |
| `emergencyContactName` | string | Name of the tenant's designated emergency contact |
| `emergencyContactPhone` | string | Phone number for the tenant's emergency contact |
| `afterHoursContactName` | string | Name of the tenant's after-hours contact person |
| `afterHoursContactPhone` | string | Phone number for after-hours contact |
| `satisfactionScore` | number | Tenant satisfaction rating on a 1-10 scale |
| `complaintCount` | number | Total number of formal complaints filed by the tenant in the current period |
| `specialRequirements` | array[string] | Special operational requirements (e.g., 24/7 access, dedicated HVAC, loading dock priority) |

### 2. rentRoll

Unit-level rent and occupancy schedule.

Financial metrics use definitions from `core_commercial_re_na@2.0.0 → financialFundamentals`. Area metrics reference `core_commercial_re_na@2.0.0 → areaAndMeasurement`.

| Field | Type | Description |
|---|---|---|
| `unitId` | string | Unique identifier for the rentable unit |
| `floor` | number | Floor number where the unit is located |
| `suiteNumber` | string | Suite or unit number |
| `rentableArea` | number | → `core@2.0.0 → areaAndMeasurement.rentableArea` |
| `usableArea` | number | → `core@2.0.0 → areaAndMeasurement.usableArea` |
| `party.tenant.name` | string | → `core@2.0.0 → parties` with role=tenant |
| `leaseStartDate` | string (ISO 8601) | Commencement date of the current lease |
| `leaseEndDate` | string (ISO 8601) | Expiry date of the current lease |
| `waleContributionYears` | number | This unit's contribution to the weighted average lease expiry in years |
| `baseRentAnnual` | number | Annual base rent amount |
| `baseRentMonthly` | number | Monthly base rent amount |
| `baseRentPerSF` | number | Base rent per rentable square foot per annum |
| `currentEscalationStep` | string | Current position in the rent escalation schedule (e.g., "Year 3 of 5") |
| `marketRent` | number | Current market rent per rentable square foot per annum |
| `markToMarketPercent` | number | Current contract rent as a percentage of market rent (e.g., 0.95 means 5% below market) |
| `freeRentMonths` | number | → `core@2.0.0 → revenueAndExpenseLineItems.freeRentMonths` |
| `tiAllowancePerSF` | number | → `core@2.0.0 → revenueAndExpenseLineItems.tiAllowancePerSF` |
| `rentAbatement` | string | Description of any rent abatement provisions and their terms |
| `vacancyStatus` | string | Current occupancy status: occupied, vacant, subleased |
| `daysVacant` | number | Number of days the unit has been continuously vacant (0 if occupied) |
| `lastOccupancyDate` | string (ISO 8601) | Date the unit was last occupied (relevant for vacant units) |

### 3. operatingBudget

Line-item budget and actuals.

Financial metrics use definitions from `core_commercial_re_na@2.0.0 → financialFundamentals`. Period definitions use `core_commercial_re_na@2.0.0 → dateAndTimePeriods`. Revenue and expense line items reference `core_commercial_re_na@2.0.0 → revenueAndExpenseLineItems`.

| Field | Type | Description |
|---|---|---|
| `budgetPeriod` | string | Budget period label (e.g., "FY 2025", "CY 2025") |
| `budgetType` | string | Period basis: fiscal year, calendar year |
| `revenueBaseRent` | number | → `core@2.0.0 → revenueAndExpenseLineItems.revenueBaseRent` |
| `revenuePercentageRent` | number | Total budgeted or actual percentage rent revenue |
| `revenueRecoveries` | number | → `core@2.0.0 → revenueAndExpenseLineItems.revenueRecoveries` |
| `revenueParking` | number | → `core@2.0.0 → revenueAndExpenseLineItems.revenueParking` |
| `revenueOther` | number | → `core@2.0.0 → revenueAndExpenseLineItems.revenueOther` |
| `expenseUtilities` | number | → `core@2.0.0 → revenueAndExpenseLineItems.expenseUtilities` |
| `expenseRepairsMaintenance` | number | → `core@2.0.0 → revenueAndExpenseLineItems.expenseRepairsMaintenance` |
| `expenseJanitorial` | number | Total budgeted or actual janitorial and cleaning expense |
| `expenseSecurity` | number | Total budgeted or actual security services expense |
| `expenseInsurance` | number | → `core@2.0.0 → revenueAndExpenseLineItems.expenseInsurance` |
| `expenseManagementFee` | number | Total budgeted or actual property management fee |
| `expenseAdministrative` | number | Total budgeted or actual administrative and general expense |
| `expenseLandscaping` | number | Total budgeted or actual landscaping and grounds maintenance expense |
| `expenseSnowRemoval` | number | Total budgeted or actual snow and ice removal expense |
| `budgetAmount` | number | Total budgeted amount for the period (all line items) |
| `actualAmount` | number | Total actual amount for the period (all line items) |
| `varianceDollar` | number | Dollar variance between budget and actual (actual minus budget) |
| `variancePercent` | number | Percentage variance between budget and actual (expressed as decimal, e.g., 0.05 = 5% over budget) |
| `priorYearActual` | number | Prior year actual total for comparison |
| `perSFMetric` | number | Total operating cost per rentable square foot |
| `perUnitMetric` | number | Total operating cost per rentable unit |

### 4. maintenanceAndWorkOrders

Work order lifecycle tracking.

| Field | Type | Description |
|---|---|---|
| `workOrderId` | string | Unique identifier for the work order |
| `dateOpened` | string (ISO 8601) | Date the work order was created |
| `dateClosed` | string (ISO 8601) | Date the work order was completed and closed |
| `status` | string | Current work order status: open, in-progress, completed, deferred |
| `category` | string | Work category: HVAC, plumbing, electrical, janitorial, structural, life-safety |
| `priority` | string | Priority level: emergency, urgent, routine, scheduled |
| `reportedBy` | string | Source of the work order: tenant-reported, staff-identified |
| `assignedVendor` | string | Name of the vendor or contractor assigned to the work order |
| `estimatedCost` | number | Estimated cost to complete the work |
| `actualCost` | number | Actual cost upon completion |
| `responseTimeHours` | number | Hours elapsed from work order creation to first response |
| `completionTimeHours` | number | Hours elapsed from work order creation to completion |
| `tenantSatisfactionRating` | number | Tenant satisfaction rating for the completed work on a 1-5 scale |

### 5. vendorManagement

Vendor registry and performance tracking.

| Field | Type | Description |
|---|---|---|
| `vendorName` | string | Full legal name of the vendor or contractor |
| `tradeCategory` | string | Trade or service category (e.g., HVAC, janitorial, landscaping, elevator, fire protection) |
| `contractStartDate` | string (ISO 8601) | Start date of the current service contract |
| `contractEndDate` | string (ISO 8601) | End date of the current service contract |
| `contractValueAnnual` | number | Annual contract value in dollars |
| `paymentTerms` | string | Payment terms (e.g., "Net 30", "Net 60", "Upon completion") |
| `insuranceCertificateStatus` | string | Status of the vendor's certificate of insurance: current, expired, pending |
| `insuranceExpiryDate` | string (ISO 8601) | Expiry date of the vendor's insurance certificate |
| `performanceRating` | number | Vendor performance rating on a 1-5 scale |
| `responseTimeAverage` | number | Average response time in hours across completed work orders |
| `licensedBondedStatus` | string | Licensing and bonding status: licensed, bonded, both, neither |
| `diversityCertification` | string | Diversity or minority business certification (e.g., MBE, WBE, DVBE, or "none") |
| `scopeOfServices` | string | Description of the contracted scope of services |

### 6. buildingOperations

Day-to-day building management.

| Field | Type | Description |
|---|---|---|
| `buildingHoursWeekday` | string | Standard building operating hours on weekdays (e.g., "7:00-19:00") |
| `buildingHoursWeekend` | string | Standard building operating hours on weekends (e.g., "8:00-13:00" or "Closed") |
| `buildingHoursHoliday` | string | Building operating hours on statutory holidays |
| `hvacSchedule` | string | Standard HVAC operating schedule (e.g., "Weekdays 6:00-20:00") |
| `afterHoursHVACRate` | number | Charge per hour for after-hours HVAC service |
| `afterHoursAccessProcedure` | string | Procedure for tenants to access the building after hours |
| `utilityProvider` | string | Name of the primary utility provider |
| `utilityAccountNumber` | string | Building utility account number |
| `utilityMeterNumber` | string | Primary utility meter number |
| `energyConsumptionKWH` | number | Electricity consumption in kilowatt-hours for the reporting period |
| `energyConsumptionTherms` | number | Natural gas consumption in therms for the reporting period |
| `energyConsumptionGallons` | number | Water consumption in gallons for the reporting period |
| `elevatorServiceContractor` | string | Name of the elevator service and maintenance contractor |
| `elevatorInspectionDate` | string (ISO 8601) | Date of the most recent elevator inspection |
| `parkingSpacesReserved` | number | Number of reserved parking spaces |
| `parkingSpacesUnreserved` | number | Number of unreserved parking spaces |
| `parkingSpacesVisitor` | number | Number of visitor parking spaces |
| `parkingMonthlyRate` | number | Monthly rate per reserved parking space |
| `lifeSafetySystemType` | string | Life safety systems installed: fire alarm, sprinkler, emergency generator |
| `lifeSafetyLastInspection` | string (ISO 8601) | Date of the most recent life safety system inspection |
| `lifeSafetyNextDue` | string (ISO 8601) | Date the next life safety system inspection is due |

### 7. complianceAndInspections

Regulatory compliance tracking.

| Field | Type | Description |
|---|---|---|
| `inspectionType` | string | Type of inspection: fire, elevator, environmental, ADA, structural |
| `inspectionDate` | string (ISO 8601) | Date the inspection was conducted |
| `inspector` | string | Name of the inspector or inspection firm |
| `inspectionResult` | string | Inspection outcome: pass, fail, conditional |
| `violationId` | string | Unique identifier for a cited violation |
| `violationDescription` | string | Description of the violation or deficiency |
| `violationSeverity` | string | Severity classification: critical, major, minor |
| `violationDeadline` | string (ISO 8601) | Deadline for remediation of the violation |
| `remediationStatus` | string | Current remediation status: open, in-progress, resolved |
| `certificateOfOccupancyStatus` | string | Certificate of occupancy status: active, expired, pending |
| `certificateRenewalDate` | string (ISO 8601) | Date the certificate of occupancy is due for renewal |
| `environmentalComplianceItems` | array[string] | Environmental compliance items tracked (e.g., asbestos abatement, mold remediation, stormwater management) |
| `localBylawComplianceItems` | array[string] | Local bylaw and ordinance compliance items tracked (e.g., noise ordinance, signage codes, occupancy limits) |

### 8. tenantBillingAndRecoveries

Additional rent and recovery calculations.

Financial metrics use definitions from `core_commercial_re_na@2.0.0 → financialFundamentals`.

| Field | Type | Description |
|---|---|---|
| `camEstimated` | number | Estimated annual common area maintenance charge |
| `camActual` | number | Actual annual common area maintenance charge |
| `camTrueUpAmount` | number | Year-end CAM reconciliation true-up amount (positive = tenant owes, negative = credit) |
| `taxBaseYear` | string | Base year used for real estate tax escalation calculations (e.g., "2023") |
| `taxCurrentYear` | string | Current tax year for escalation comparison (e.g., "2025") |
| `taxTenantSharePercent` | number | Tenant's proportionate share of real estate taxes (expressed as decimal, e.g., 0.12 = 12%) |
| `taxEscalationAmount` | number | Dollar amount of tax escalation above the base year owed by the tenant |
| `utilityBillingMethod` | string | Method for billing utilities to tenants: sub-metered, allocated, included |
| `utilityRate` | number | Utility rate charged to tenant per unit of consumption |
| `percentageRentBreakpoint` | number | Sales breakpoint above which percentage rent is due |
| `percentageRentSalesReported` | number | Tenant-reported gross sales for the percentage rent calculation period |
| `percentageRentPercentage` | number | Percentage rate applied to sales above the breakpoint (expressed as decimal, e.g., 0.06 = 6%) |
| `lateFeeAmount` | number | Late payment fee amount |
| `nsfChargeAmount` | number | Non-sufficient funds / returned payment charge amount |
| `reconciliationStatementDate` | string (ISO 8601) | Date the annual reconciliation statement was issued |

### 9. capitalProjects

Capital expenditure tracking.

| Field | Type | Description |
|---|---|---|
| `projectName` | string | Name or title of the capital project |
| `projectDescription` | string | Detailed description of the capital project scope |
| `projectCategory` | string | Project category: structural, mechanical, aesthetic, code-compliance |
| `budgetApproved` | number | Approved budget amount for the project |
| `actualSpend` | number | Actual expenditure to date |
| `budgetVariance` | number | Variance between approved budget and actual spend (actual minus budget) |
| `contractor` | string | Name of the general contractor or primary vendor |
| `projectManager` | string | Name of the assigned project manager |
| `startDate` | string (ISO 8601) | Project start date |
| `targetCompletionDate` | string (ISO 8601) | Targeted project completion date |
| `actualCompletionDate` | string (ISO 8601) | Actual project completion date |
| `completionPercentage` | number | Current completion percentage (expressed as decimal, e.g., 0.75 = 75%) |
| `fundingSource` | string | Source of project funding: operating, reserve-fund, special-assessment |
| `impactOnPropertyValue` | string | Description of the project's expected impact on property value |
| `usefulLifeYears` | number | Estimated useful life of the improvement in years |

### 10. reportingMetrics

KPIs for property management performance.

Financial metrics use definitions from `core_commercial_re_na@2.0.0 → financialFundamentals`. Area metrics use definitions from `core_commercial_re_na@2.0.0 → areaAndMeasurement`.

| Field | Type | Description |
|---|---|---|
| `physicalOccupancyRate` | number | Percentage of rentable area physically occupied (expressed as decimal, e.g., 0.92 = 92%) |
| `economicOccupancyRate` | number | Percentage of potential gross revenue actually collected (expressed as decimal) |
| `collectionRateCurrentMonth` | number | Rent collection rate for the current month (expressed as decimal) |
| `collectionRateYTD` | number | Rent collection rate year-to-date (expressed as decimal) |
| `arrearsAgingCurrent` | number | Dollar amount of receivables in the current (0-30 day) aging bucket |
| `arrearsAging30Days` | number | Dollar amount of receivables in the 31-60 day aging bucket |
| `arrearsAging60Days` | number | Dollar amount of receivables in the 61-90 day aging bucket |
| `arrearsAging90Plus` | number | Dollar amount of receivables aged over 90 days |
| `tenantRetentionRate` | number | Annual tenant retention rate (expressed as decimal, e.g., 0.85 = 85%) |
| `avgWorkOrderResponseTimeHours` | number | Average response time for work orders in hours |
| `avgWorkOrderCompletionTimeHours` | number | Average time to complete work orders in hours |
| `energyUseIntensity` | number | Energy use intensity in kBTU per square foot |
| `operatingExpenseRatio` | number | → `core@2.0.0 → revenueAndExpenseLineItems.operatingExpenseRatio`. PM convention: denominator is effective gross income per core standard. |
| `rentGrowthYoYPercent` | number | Year-over-year rent growth (expressed as decimal, e.g., 0.03 = 3%) |
| `tenantSatisfactionScoreAggregate` | number | Aggregate tenant satisfaction score across all tenants on a 1-10 scale |
| `deferredMaintenanceBacklog` | number | Dollar amount of deferred maintenance items in the backlog |

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
