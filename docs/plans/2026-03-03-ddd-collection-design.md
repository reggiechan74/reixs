---
title: CRE Domain Data Dictionary Collection Design
date: 2026-03-03
keywords: [ddd, domain-data-dictionary, cre, property-management, asset-management, leasing, investment, appraisal]
lastUpdated: 2026-03-03
---

# CRE Domain Data Dictionary Collection — Design Document

## 1. Overview

Create a standardized set of domain data dictionaries (DDDs) for commercial real estate (CRE) workflows in North America. The collection follows a hybrid approach: a core shared glossary of cross-role CRE concepts, plus role-specific DDDs for each major CRE function. Task-specific DDDs (like the existing lease abstraction DDD) reference both the core glossary and their relevant role DDD.

### Goals

- Establish a canonical vocabulary for CRE AI workflows
- Enable consistent field definitions across REIXS specs
- Support independent versioning per DDD
- Follow the existing DDD format established by `lease_abstraction_commercial_na_v1_0.md`

### Scope

- **Geography:** North America only
- **Property types:** Commercial office and industrial (primary), retail and multifamily (secondary)
- **Depth:** Full-weight — typed fields, sections, status tracking, semantic versioning

### Relationship to REIXS

Per ADR-001 (Layered Artifact Boundaries), REIXS specs reference DDDs by versioned identifier rather than embedding content. Each DDD in this collection is independently referenceable via `re-ddd:<name>@<semver>`.

## 2. File Structure

```
docs/ddd/
├── core_commercial_re_na_v1_0.md                    # re-ddd:core_commercial_re_na@1.0.0
├── property_management_commercial_na_v1_0.md         # re-ddd:property_management_commercial_na@1.0.0
├── asset_management_commercial_na_v1_0.md            # re-ddd:asset_management_commercial_na@1.0.0
├── leasing_commercial_na_v1_0.md                     # re-ddd:leasing_commercial_na@1.0.0
├── investment_appraisal_commercial_na_v1_0.md        # re-ddd:investment_appraisal_commercial_na@1.0.0
└── lease_abstraction_commercial_na_v1_0.md           # re-ddd:lease_abstraction_commercial_na@1.0.0 (existing)
```

### Naming Convention

`<function>_commercial_na_v<major>_<minor>.md`

- `<function>`: snake_case role or task name
- `commercial`: property sector
- `na`: jurisdiction (North America)
- `v<major>_<minor>`: version

### Reference Format

All DDDs use the established format: `re-ddd:<name>@<semver>`

Role DDDs may cross-reference the core glossary using: "See `core_commercial_re_na@1.0.0 → <section>.<field>`"

## 3. Cross-Cutting Conventions

All DDDs in this collection share:

### Field Status Tracking

| Status | Meaning | Required Metadata |
|---|---|---|
| `FACT` | Value found verbatim in source document | `provenance` (page, clause, verbatim quote) |
| `INFERENCE` | Value derived or interpreted from source | `confidence` (0.0-1.0), `reasoning` |
| `MISSING` | Field not found in source document | value = `null` (JSON) or `"Not specified"` (markdown) |
| `CONFLICT` | Multiple conflicting values found | All values with individual `provenance`, `reasoning` |

### Data Types

| Type | JSON Representation | Notes |
|---|---|---|
| `string` | `"value"` | Text values |
| `string (ISO 8601)` | `"YYYY-MM-DD"` | All dates normalized to ISO 8601 |
| `number` | `45.00` | Numeric values without currency symbols |
| `boolean` | `true` / `false` | Yes/no values |
| `array[string]` | `["item1", "item2"]` | Lists |
| `null` | `null` | Missing or absent values |

### Versioning

Semantic versioning across all DDDs:
- **Patch** (1.0.x): Field description clarifications, no schema changes
- **Minor** (1.x.0): New optional fields added, no existing fields removed
- **Major** (x.0.0): Breaking changes — fields renamed, removed, or restructured

## 4. Core Glossary — `core_commercial_re_na_v1_0.md`

**Reference:** `re-ddd:core_commercial_re_na@1.0.0`

**Scope:** Shared field definitions used across multiple CRE roles. Defines the canonical representation of cross-cutting concepts.

### Sections (~60-80 fields total)

#### 4.1 propertyIdentification

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

#### 4.2 financialFundamentals

Core financial metrics used across roles.

| Field | Type | Description |
|---|---|---|
| `noi` | number | Net Operating Income — revenue minus operating expenses, before debt service and capital |
| `grossRevenue` | number | Total revenue before any deductions |
| `effectiveGrossIncome` | number | Gross revenue minus vacancy and credit loss |
| `operatingExpenses` | number | Total operating expenses (excluding debt service and capital) |
| `capRate` | number | Capitalization rate — NOI / property value (expressed as decimal, e.g., 0.065) |
| `cashOnCashReturn` | number | Annual pre-tax cash flow / total cash invested (expressed as decimal) |
| `irr` | number | Internal rate of return (expressed as decimal) |
| `npv` | number | Net present value at specified discount rate |
| `debtService` | number | Annual debt service (principal + interest) |
| `dscr` | number | Debt service coverage ratio — NOI / debt service |
| `ltv` | number | Loan-to-value ratio — loan balance / property value (expressed as decimal) |
| `equityMultiple` | number | Total distributions / total equity invested |

#### 4.3 areaAndMeasurement

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

#### 4.4 parties

Standard party/entity representation.

| Field | Type | Description |
|---|---|---|
| `entityName` | string | Full legal name of the entity |
| `entityType` | string | Corporation, LLC, LP, REIT, individual, trust, pension fund, etc. |
| `registeredAddress` | string | Registered/principal address |
| `contactName` | string | Primary contact person |
| `contactPhone` | string | Contact phone number |
| `contactEmail` | string | Contact email address |
| `role` | string | Party's role: owner, tenant, manager, broker, lender, appraiser, counsel |
| `taxId` | string | Tax identification number (EIN, BN, etc.) |

#### 4.5 leaseClassifications

Standard lease type definitions.

| Field | Type | Description |
|---|---|---|
| `leaseType` | string | NNN (triple net), modified gross, gross, full-service, ground lease, percentage lease |
| `leaseTypeDescription` | string | Plain-language description of the lease structure |
| `tenantExpenseObligations` | array[string] | Which expenses the tenant pays directly under this structure |
| `landlordExpenseObligations` | array[string] | Which expenses the landlord covers |
| `expenseStopOrBaseYear` | string | Expense stop amount or base year for escalations |

#### 4.6 dateAndTimePeriods

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

#### 4.7 currencyAndUnits

Currency and unit normalization.

| Field | Type | Description |
|---|---|---|
| `currency` | string | ISO 4217 currency code (USD, CAD) |
| `amountUnit` | string | "total", "per-sf", "per-unit", "per-annum", "per-month" |
| `areaUnit` | string | "sq ft", "sq m", "acres", "hectares" |
| `conversionRate` | number | Exchange rate if currency conversion applied |
| `conversionDate` | string (ISO 8601) | Date of exchange rate used |

#### 4.8 documentReferences

Source document tracking for provenance.

| Field | Type | Description |
|---|---|---|
| `documentType` | string | Lease, appraisal, operating statement, rent roll, budget, inspection report, etc. |
| `documentTitle` | string | Title or filename of the source document |
| `documentDate` | string (ISO 8601) | Date of the source document |
| `documentVersion` | string | Version or revision identifier |
| `documentSource` | string | Origin system or provider |
| `pageReference` | string | Page or section reference within the document |

## 5. Property Management — `property_management_commercial_na_v1_0.md`

**Reference:** `re-ddd:property_management_commercial_na@1.0.0`

**Scope:** Field definitions for property management operations across commercial office and industrial properties in North America.

### Sections (~120-150 fields total)

#### 5.1 tenantManagement

Tenant roster and relationship tracking.

- Tenant name, lease reference, unit/suite, contact info
- Move-in/move-out dates, lease status (active/expired/holdover/pending)
- Emergency contacts, after-hours contacts
- Tenant satisfaction score, complaint history count
- Special requirements (e.g., 24/7 access, loading dock priority)

#### 5.2 rentRoll

Unit-level rent and occupancy schedule.

- Unit ID, floor, suite number, rentable SF, usable SF
- Tenant name (or "vacant"), lease start, lease end, WALE contribution
- Base rent (annual, monthly, per-SF), current escalation step
- Market rent comparison (current rent vs. market rent, mark-to-market %)
- Concessions (free rent months, TI allowance, rent abatement)
- Vacancy status, days vacant, last occupancy date

#### 5.3 operatingBudget

Line-item budget and actuals.

- Budget period (fiscal year, calendar year)
- Revenue line items: base rent, percentage rent, recoveries, parking, other income
- Expense categories: utilities, R&M, janitorial, security, insurance, management fees, administrative, landscaping, snow removal
- Budget vs. actual variance ($ and %)
- Year-over-year comparison
- Per-SF and per-unit metrics

#### 5.4 maintenanceAndWorkOrders

Work order lifecycle tracking.

- Work order ID, date opened, date closed, status (open/in-progress/completed/deferred)
- Category (HVAC, plumbing, electrical, janitorial, structural, life safety)
- Priority (emergency, urgent, routine, scheduled)
- Tenant-reported vs. staff-identified
- Assigned vendor, estimated cost, actual cost
- Response time, completion time, tenant satisfaction rating

#### 5.5 vendorManagement

Vendor registry and performance.

- Vendor name, trade/service category, contract start/end
- Contract value (annual, per-service), payment terms
- Insurance certificate status, expiry dates
- Performance rating, response time average
- Licensed/bonded status, diversity certification
- Scope of services description

#### 5.6 buildingOperations

Day-to-day building management.

- Building hours (weekday, weekend, holiday), HVAC schedule
- After-hours HVAC rate (per hour), after-hours access procedures
- Utility accounts (electric, gas, water, sewer) — provider, account number, meter number
- Energy consumption (kWh, therms, gallons) by period
- Elevator service contracts, inspection dates
- Parking inventory (reserved, unreserved, visitor), parking rates
- Life safety systems (fire alarm, sprinkler, emergency generator) — last inspection, next due

#### 5.7 complianceAndInspections

Regulatory compliance tracking.

- Inspection type (fire, elevator, environmental, ADA, structural)
- Inspection date, inspector, result (pass/fail/conditional)
- Violation ID, description, severity, deadline, remediation status
- Certificate of occupancy status, renewal date
- Environmental compliance (asbestos, lead, mold testing)
- Local bylaw compliance items

#### 5.8 tenantBillingAndRecoveries

Additional rent and recovery calculations.

- CAM reconciliation (estimated vs. actual, true-up amount)
- Tax escalation calculations (base year, current year, tenant share)
- Utility billing (sub-metered, allocation method, rates)
- Percentage rent (breakpoint, sales reporting, percentage applied)
- Late fee assessment, NSF charges
- Year-end reconciliation statement fields

#### 5.9 capitalProjects

Capital expenditure tracking.

- Project name, description, category (structural, mechanical, aesthetic, code compliance)
- Budget (approved amount), actual spend, variance
- Contractor, project manager, start date, target completion, actual completion
- Completion percentage, milestone tracking
- Funding source (operating, reserve fund, special assessment)
- Impact on property value, useful life of improvement

#### 5.10 reportingMetrics

KPIs for property management performance.

- Physical occupancy rate, economic occupancy rate
- Collection rate (current month, YTD, arrears aging)
- Tenant retention rate (annual)
- Average work order response time, completion time
- Energy use intensity (EUI — kBTU/sq ft)
- Operating expense ratio (OpEx / gross revenue)
- Rent growth (year-over-year %)
- Tenant satisfaction score (aggregate)
- Deferred maintenance backlog ($)

## 6. Asset Management — `asset_management_commercial_na_v1_0.md`

**Reference:** `re-ddd:asset_management_commercial_na@1.0.0`

**Scope:** Field definitions for asset-level strategy and performance management across commercial portfolios in North America.

### Sections (~100-130 fields total)

#### 6.1 assetProfile

Asset-level summary and ownership context.

- Property reference (link to core propertyIdentification)
- Acquisition date, acquisition price, acquisition cap rate
- Current valuation, valuation date, valuation method
- Ownership structure (JV split, fund allocation, co-investment %)
- Fund/vehicle name, vintage year
- Hold period (actual elapsed, target)
- Asset strategy classification (core, core-plus, value-add, opportunistic)

#### 6.2 financialPerformance

Operating financial results.

- NOI (actual, budget, prior year, variance)
- Revenue breakdown: base rent, recoveries, parking, other
- Expense breakdown by category (mirrors property management budget categories)
- Capital expenditures (routine, non-routine)
- Cash flow before/after debt service
- Distribution amounts, distribution dates, distribution yield
- Unlevered vs. levered returns

#### 6.3 valuationMetrics

Property valuation data points.

- Going-in cap rate, exit cap rate, market cap rate
- Price per SF (acquisition, current)
- Replacement cost per SF
- Assessed value (tax assessment), assessment year
- Most recent appraisal value, appraisal date, appraiser
- Mark-to-market adjustment ($ and %)
- Implied value from NOI / cap rate

#### 6.4 debtAndCapitalStructure

Financing summary.

- Loan ID, lender name, loan type (fixed, floating, construction, mezzanine)
- Original principal, current balance, maturity date
- Interest rate (fixed rate, spread over index, index name)
- IO period end date, amortization schedule
- LTV (current), DSCR (current, covenant)
- Covenant compliance status, covenant thresholds
- Prepayment provisions (yield maintenance, defeasance, open period)
- Refinancing analysis: estimated proceeds, rate assumptions, net benefit

#### 6.5 holdSellAnalysis

Disposition decision support.

- Current market value estimate, basis for estimate
- Projected disposition value (at target exit date)
- Disposition costs (broker commission %, transfer tax, legal)
- Hold IRR (forward-looking), sell IRR, breakeven hold period
- Capital gains estimate, tax implications
- Reinvestment assumptions
- Recommendation (hold/sell/refinance) with supporting rationale

#### 6.6 leasingStrategy

Asset-level leasing direction.

- Current occupancy, target occupancy, stabilized occupancy
- WALE (weighted average lease expiry) in years
- Lease expiry profile (by year, by SF, by revenue)
- Renewal probability by tenant (high/medium/low)
- Estimated downtime between tenants (months)
- Market rent projection (current, 1-yr, 3-yr)
- Tenant credit quality distribution (investment grade %, non-rated %)
- Key tenant concentration (top 5 tenants as % of revenue)

#### 6.7 capitalPlanning

Multi-year capital strategy.

- 5-year capex plan (by year, by category)
- 10-year capex plan (summary)
- Deferred maintenance items, estimated cost, priority
- Reserve fund balance, target reserve, annual contribution
- ROI on planned capital investments (estimated)
- ESG/sustainability upgrades (LED retrofit, HVAC upgrade, solar, EV charging)
- Expected impact on NOI, value, and tenant attraction

#### 6.8 riskAssessment

Risk identification and monitoring.

- Market risk factors (supply pipeline, demand trends, rental rate trajectory)
- Tenant concentration risk (single-tenant exposure %)
- Lease rollover risk (% of revenue expiring within 12/24/36 months)
- Environmental risk (known contamination, flood zone, seismic)
- Regulatory risk (rent control, zoning changes, tax reassessment)
- Obsolescence risk (functional, technological, design)
- Overall risk rating (low/medium/high) with supporting narrative

#### 6.9 portfolioContext

Asset within portfolio.

- Portfolio name, total portfolio value, number of assets
- Asset's share of portfolio (by value, by NOI)
- Peer comparison (vs. similar assets in portfolio)
- Sector allocation (office/industrial/retail %)
- Geographic diversification metrics
- Vintage analysis (acquisition year cohorts)
- Portfolio-level return metrics (gross/net IRR, equity multiple)

#### 6.10 budgetAndForecasting

Forward-looking financial planning.

- Annual budget (revenue, expenses, NOI, capex)
- Reforecast cadence (quarterly, semi-annual)
- Budget vs. actual variance (current period, YTD)
- Key assumptions log (vacancy, market rent growth, expense inflation, cap rate)
- Sensitivity scenarios: base case, upside, downside
- Scenario-specific outputs (NOI, value, IRR for each)

## 7. Leasing — `leasing_commercial_na_v1_0.md`

**Reference:** `re-ddd:leasing_commercial_na@1.0.0`

**Scope:** Field definitions for commercial leasing operations including deal pipeline, market analysis, and transaction execution in North America.

### Sections (~100-120 fields total)

#### 7.1 marketAnalysis

Submarket and competitive intelligence.

- Submarket name, metro area, geographic boundaries
- Vacancy rate (direct, sublease, total), trend (3-quarter direction)
- Net absorption (quarterly, annual) in SF
- Average asking rent (gross, net), trend
- Average concessions (free rent months, TI per SF)
- Competitive set (comparable buildings: name, class, size, occupancy, asking rent)
- Construction pipeline (projects, SF under construction, expected delivery)
- Key demand drivers (employers, infrastructure, regulatory)

#### 7.2 comparableLeases

Lease comparable transactions.

- Property name, address, submarket
- Tenant name, industry/SIC code
- Transaction date, lease execution date
- Suite/floor, area (SF)
- Lease term (years/months), commencement date
- Base rent (per-SF, annual), escalation type and rate
- TI allowance (per-SF), free rent (months)
- Effective rent (calculated, per-SF, per-annum)
- Lease type (new, renewal, expansion, blend-and-extend)
- Net/gross classification
- Broker(s) involved, listing/procuring side

#### 7.3 tenantScreening

Prospect qualification.

- Prospect company name, industry, HQ location
- Space requirement (SF, layout preferences, floor preference)
- Target occupancy date, lease term preference
- Financial statements summary (revenue, assets, net worth)
- Credit rating (S&P/Moody's/Fitch), D&B rating
- Public/private company, parent entity
- Litigation history (material), bankruptcy history
- Current location, reason for move
- References (current landlord, banker)

#### 7.4 dealStructuring

Deal economics and terms.

- Proposed base rent (per-SF, annual, monthly)
- Rent escalation structure (fixed %, CPI, market reset)
- TI allowance (per-SF, total, amortized over term)
- Free rent (months), placement in term (upfront, distributed)
- Expansion option (SF, timing, rent determination)
- Contraction option (SF, timing, penalty)
- Termination right (timing, penalty, notice period)
- Renewal option (number, term, rent determination)
- Parking allocation and rate
- Landlord's total cost (TI + free rent + commissions + legal)
- Net effective rent calculation
- Landlord's ROI on deal (NPV of cash flows)

#### 7.5 loiAndProposal

Letter of intent lifecycle.

- LOI status (draft, issued, countered, accepted, expired, withdrawn)
- Version number, date issued, expiration date
- Issuing party, counterparty
- Key terms summary (rent, term, TI, free rent, commencement)
- Binding provisions (exclusivity, confidentiality, costs)
- Non-binding provisions (business terms)
- Counter history (version, date, key changes)
- Exclusivity period start/end
- Transition to lease drafting date

#### 7.6 commissionAndFees

Brokerage compensation.

- Commission rate (% of aggregate rent)
- Commission structure (flat, tiered, front-loaded)
- Listing broker, listing broker share (%)
- Procuring broker, procuring broker share (%)
- Total commission amount ($)
- Payment schedule (on execution, on occupancy, installments)
- Override provisions (renewals, expansions)
- Referral fee (%, to whom)
- Co-brokerage agreement terms

#### 7.7 spacePlanning

Available space inventory and planning.

- Available spaces list (suite, floor, SF, asking rent, availability date)
- Floor plates (typical SF per floor)
- Test fit feasibility (seats/SF, collaboration ratio, private office count)
- Demising options (can space be subdivided, minimum divisible)
- Building amenities (fitness, conference, rooftop, food service)
- Efficiency ratio (usable/rentable)
- Contiguous block availability
- Sublease availability (tenant, term remaining, asking rent)

#### 7.8 tenantRetention

Renewal and retention tracking.

- Tenant name, current lease expiry, notice deadline
- Renewal probability (high/medium/low), basis for assessment
- Proposed renewal terms (if in discussion)
- Current rent vs. market rent (mark-to-market %)
- Estimated cost of vacancy if tenant leaves (downtime, TI, commissions)
- Competitive threats (buildings tenant is considering)
- Early renewal incentive offered (if any)
- Retention rate (portfolio-level, building-level, annual)

#### 7.9 pipelineTracking

Deal pipeline and forecasting.

- Deal ID, prospect name, space (suite/SF)
- Deal stage: prospect → tour → proposal → LOI → lease negotiation → executed
- Stage entry date, days in current stage
- Probability weighting (% likely to close)
- Expected close date, expected commencement date
- Weighted deal value (annual rent × probability)
- Broker assignment, listing agent
- Next action, next action date
- Lost deal reason (if applicable)

#### 7.10 marketRentOpinion

Concluded market rent with methodology.

- Property address, unit/suite, floor, SF
- Concluded market rent (per-SF, per-annum)
- Rent basis (gross, net, modified gross)
- Effective date of opinion
- Comparable leases used (references to section 7.2 entries)
- Adjustments applied (location, size, condition, floor level, lease term, TI)
- Exposure time estimate
- Supporting narrative / rationale
- Prepared by, date prepared

## 8. Investment & Appraisal — `investment_appraisal_commercial_na_v1_0.md`

**Reference:** `re-ddd:investment_appraisal_commercial_na@1.0.0`

**Scope:** Field definitions for investment analysis and property valuation across commercial real estate in North America.

### Sections (~120-150 fields total)

#### 8.1 propertyDescription

Physical and site characteristics for valuation.

- Property reference (link to core propertyIdentification)
- Site area, frontage, topography, shape, utilities availability
- Building area (GBA, rentable, usable), number of floors
- Construction type (steel frame, concrete, wood), roof type
- Condition rating (excellent/good/fair/poor), basis for rating
- Number of units/suites, average unit size
- Parking (type, spaces, ratio to building area)
- Renovation history (year, scope, cost)
- Highest-and-best-use conclusion (as vacant, as improved)
- Functional utility assessment

#### 8.2 incomeApproach

Direct capitalization.

- Potential gross income (PGI) — base rent at market
- Vacancy and credit loss (%, $)
- Effective gross income (EGI)
- Operating expenses (itemized by category)
- Net operating income (NOI)
- Cap rate selection (source: market extraction, band of investment, survey)
- Comparable cap rate data (property, sale date, cap rate)
- Direct capitalization value (NOI / cap rate)
- Stabilized vs. as-is distinction
- Above/below market lease adjustments

#### 8.3 dcfAnalysis

Discounted cash flow.

- Projection period (years), start date
- Year-by-year revenue projection (base rent, recoveries, other)
- Revenue growth assumptions (by year or blended)
- Year-by-year expense projection (by category or total)
- Expense growth assumptions (inflation rate, fixed vs. variable)
- Capital reserve/replacement allowance (per-SF, per-annum)
- Net cash flow (by year)
- Terminal cap rate, basis for selection
- Reversion value (terminal year NOI / terminal cap rate)
- Selling costs at reversion (%)
- Discount rate, basis for selection (risk-free rate, risk premium, build-up method)
- Present value of cash flows, present value of reversion
- DCF indicated value (sum of PVs)
- IRR (implied by sale price, or target)

#### 8.4 salesComparisonApproach

Comparable sales analysis.

- Comparable sale entries: property name, address, sale date, sale price, property type
- Size (SF, units, acres), price per SF, price per unit
- Cap rate at sale, NOI at time of sale
- Buyer, seller, buyer type (institutional, private, REIT)
- Financing (cash, conventional, assumed, seller-financed)
- Conditions of sale (arm's length, distressed, portfolio, 1031 exchange)
- Adjustment grid: property rights, financing, conditions of sale, market conditions (time), location, physical characteristics, economic characteristics, use
- Adjusted sale price per SF
- Reconciled value from sales comparison

#### 8.5 costApproach

Replacement/reproduction cost analysis.

- Land value (from comparable land sales or allocation)
- Comparable land sales (if used)
- Replacement cost new (per SF, total), source (Marshall & Swift, contractor, etc.)
- Depreciation — physical (age-life, observed condition)
- Depreciation — functional (superadequacy, deficiency)
- Depreciation — external (economic, locational)
- Total depreciation (%, $)
- Depreciated cost of improvements
- Site improvements (paving, landscaping, utilities)
- Cost approach indicated value (land + depreciated improvements + site improvements)

#### 8.6 marketStudy

Market context for valuation/investment.

- Metropolitan statistical area (MSA), submarket definition
- Population, population growth rate (historical, projected)
- Employment (total, by sector), unemployment rate
- Major employers, employer additions/departures
- Median household income, income growth
- Supply metrics: total inventory (SF), vacancy rate, availability rate
- Demand metrics: net absorption (quarterly, annual), pre-leasing activity
- Rental rate trends (asking, effective), concession trends
- Construction pipeline (under construction SF, planned SF, expected deliveries)
- Forecast: vacancy direction, rent growth direction, absorption outlook

#### 8.7 investmentMetrics

Return and risk metrics for investment decisions.

- Equity investment (total equity committed)
- Leveraged IRR, unlevered IRR
- Cash-on-cash return (by year, average)
- Equity multiple (net, gross)
- Payback period (years)
- Modified IRR (if applicable)
- Risk-adjusted return (Sharpe ratio or equivalent)
- Comparison to benchmark (NCREIF, ODCE, custom)
- Vintage-year return comparison

#### 8.8 underwriting

Acquisition/disposition underwriting assumptions.

- Purchase price, price per SF, going-in cap rate
- Financing assumptions (LTV, rate, term, IO period, amortization)
- Closing costs (% or $, itemized)
- Year 1 NOI (in-place vs. stabilized)
- Rent growth assumptions (annual %, basis)
- Expense growth assumptions (annual %, basis)
- Capital expenditure budget (years 1-5)
- Hold period (years)
- Exit cap rate, disposition costs
- Sensitivity analysis: NOI growth ±, cap rate ±, interest rate ±
- Scenario outputs: base case IRR/equity multiple, upside, downside

#### 8.9 dueDiligence

Pre-acquisition/pre-disposition investigation.

- Title review (clear/encumbered, exceptions list)
- Survey (date, surveyor, ALTA items, encroachments noted)
- Environmental Phase I (date, firm, RECs identified, recommendation)
- Environmental Phase II (if triggered — date, firm, findings, remediation estimate)
- Physical condition report (date, firm, immediate repairs $, short-term repairs $, deferred maintenance $)
- Zoning analysis (current zoning, conforming/non-conforming, variance requirements)
- Entitlement status (approved, pending, required)
- Third-party reports list (seismic, wind, flood, ADA, parking study)
- Estoppel certificate summary (tenant confirmations of lease terms)
- SNDA status (obtained/pending for each tenant)

#### 8.10 reconciliationAndConclusion

Final value opinion.

- Income approach indicated value
- Sales comparison indicated value
- Cost approach indicated value (if applicable)
- Weighting applied to each approach (%, rationale)
- Final value conclusion ($)
- Value per SF, value per unit (derived)
- Extraordinary assumptions (if any)
- Hypothetical conditions (if any)
- Effective date of value
- Date of report
- Appraiser name, designation (MAI, AACI, etc.), license number
- Intended use, intended users

## 9. Implementation Priority

| Priority | DDD | Rationale |
|---|---|---|
| 1 | `core_commercial_re_na_v1_0.md` | Foundation — all role DDDs reference it |
| 2 | `property_management_commercial_na_v1_0.md` | Highest operational data volume, most AI task opportunities |
| 3 | `asset_management_commercial_na_v1_0.md` | Closely tied to property management, portfolio-level decisions |
| 4 | `leasing_commercial_na_v1_0.md` | Transaction-oriented, builds on core and asset management |
| 5 | `investment_appraisal_commercial_na_v1_0.md` | Valuation-focused, builds on all prior DDDs |

## 10. DDD Registry Updates

The REIXS DDD reference registry (`src/reixs/registry/ddd_refs.py`) will need to be updated to recognize the new DDD references:

```python
KNOWN_DDD_REFS = [
    "re-ddd:core_commercial_re_na@1.0.0",
    "re-ddd:lease_abstraction_commercial_na@1.0.0",
    "re-ddd:property_management_commercial_na@1.0.0",
    "re-ddd:asset_management_commercial_na@1.0.0",
    "re-ddd:leasing_commercial_na@1.0.0",
    "re-ddd:investment_appraisal_commercial_na@1.0.0",
]
```

## 11. Success Criteria

- All 5 new DDDs pass structural validation (consistent format with existing lease abstraction DDD)
- Core glossary fields are cross-referenced from role DDDs where applicable
- No conflicting field definitions across DDDs (same concept = same field name and type)
- Each DDD is independently referenceable via `re-ddd:<name>@<semver>`
- DDD registry updated to recognize all new references
- Total field count across collection: ~500-600 canonical CRE fields

## 12. Out of Scope (Future Work)

- International/EMEA/APAC variants
- Residential property DDDs
- Retail-specific or multifamily-specific DDDs
- Task-specific DDDs beyond lease abstraction (e.g., property inspection, DCF valuation)
- Import/inheritance mechanism between DDDs (handled by convention for now)
- Automated field conflict detection across DDDs
