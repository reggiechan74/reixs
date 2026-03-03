# CRE Domain Data Dictionary Collection — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create 5 new domain data dictionaries (core glossary + 4 role DDDs) following the established format from `lease_abstraction_commercial_na_v1_0.md`.

**Architecture:** Each DDD is a standalone Markdown file in `docs/ddd/` with typed field tables, section descriptions, field status tracking, data types, and versioning boilerplate. The core glossary defines shared CRE terms; role DDDs define role-specific fields and cross-reference core where applicable. The DDD registry in `src/reixs/registry/ddd_refs.py` is updated to recognize all new references.

**Tech Stack:** Markdown (field tables), Python (registry update), pytest (registry tests)

**Design doc:** `docs/plans/2026-03-03-ddd-collection-design.md`

**Format reference:** `docs/ddd/lease_abstraction_commercial_na_v1_0.md` — every new DDD must match this file's structure:
- H1 title: `# Domain Data Dictionary: <Name>`
- Header block: `**Reference:**`, `**Scope:**`, `**Relationship to REIXS:**`
- `---` separator
- `## Sections` with count summary
- Numbered `### N. sectionName` subsections with description + field table
- Each field table: `| Field | Type | Description |` with `|---|---|---|` separator
- `## Field Status Tracking` section (FACT/INFERENCE/MISSING/CONFLICT table)
- `## Data Types` section (type → JSON representation table)
- `## Versioning` section (semver rules)

---

### Task 1: Core Commercial RE Glossary

**Files:**
- Create: `docs/ddd/core_commercial_re_na_v1_0.md`

**Step 1: Create the core glossary DDD**

Write `docs/ddd/core_commercial_re_na_v1_0.md` with all 8 sections and full field tables as specified in the design doc (sections 4.1–4.8). The file must follow the exact format of the existing lease abstraction DDD.

Sections to include (from design doc section 4):
1. `propertyIdentification` — 13 fields (propertyName, streetAddress, city, stateProvince, postalCode, country, legalDescription, propertyType, assetClass, yearBuilt, yearRenovated, zoningClassification, parcelId)
2. `financialFundamentals` — 12 fields (noi, grossRevenue, effectiveGrossIncome, operatingExpenses, capRate, cashOnCashReturn, irr, npv, debtService, dscr, ltv, equityMultiple)
3. `areaAndMeasurement` — 12 fields (grossBuildingArea, rentableArea, usableArea, grossLeasableArea, netRentableArea, floorAreaRatio, measurementStandard, commonAreaFactor, loadFactor, efficiencyRatio, siteArea, siteAreaUnit)
4. `parties` — 8 fields (entityName, entityType, registeredAddress, contactName, contactPhone, contactEmail, role, taxId)
5. `leaseClassifications` — 5 fields (leaseType, leaseTypeDescription, tenantExpenseObligations, landlordExpenseObligations, expenseStopOrBaseYear)
6. `dateAndTimePeriods` — 7 fields (asOfDate, fiscalYearEnd, reportingPeriod, reportingPeriodStart, reportingPeriodEnd, holdingPeriod, projectionPeriod)
7. `currencyAndUnits` — 5 fields (currency, amountUnit, areaUnit, conversionRate, conversionDate)
8. `documentReferences` — 6 fields (documentType, documentTitle, documentDate, documentVersion, documentSource, pageReference)

Total: 68 fields.

Include the standard boilerplate sections at the end: Field Status Tracking, Data Types, Versioning (copy from lease abstraction DDD, these are identical across all DDDs).

**Step 2: Verify format consistency**

Manually verify:
- H1 title matches pattern: `# Domain Data Dictionary: Commercial Real Estate Core Glossary — North America`
- Reference line: `**Reference:** \`re-ddd:core_commercial_re_na@1.0.0\``
- All field tables have exactly 3 columns: Field, Type, Description
- All field names use backtick formatting
- All types match the canonical set: string, string (ISO 8601), number, boolean, array[string]
- Section numbering is sequential (1–8)

**Step 3: Commit**

```bash
git add docs/ddd/core_commercial_re_na_v1_0.md
git commit -m "feat: add core CRE glossary domain data dictionary (NA v1.0)"
```

---

### Task 2: Property Management DDD

**Files:**
- Create: `docs/ddd/property_management_commercial_na_v1_0.md`

**Step 1: Create the property management DDD**

Write `docs/ddd/property_management_commercial_na_v1_0.md` with all 10 sections and full field tables. The design doc (section 5) provides bullet-point field lists — expand each bullet into a proper `| Field | Type | Description |` table row.

Sections to include (from design doc section 5):
1. `tenantManagement` — fields: tenantName, leaseReference, unitSuite, contactInfo, moveInDate, moveOutDate, leaseStatus, emergencyContact, afterHoursContact, satisfactionScore, complaintCount, specialRequirements (~12 fields)
2. `rentRoll` — fields: unitId, floor, suiteNumber, rentableSF, usableSF, tenantName, leaseStart, leaseEnd, waleContribution, baseRentAnnual, baseRentMonthly, baseRentPerSF, currentEscalationStep, marketRent, markToMarketPercent, freeRentMonths, tiAllowance, rentAbatement, vacancyStatus, daysVacant, lastOccupancyDate (~21 fields)
3. `operatingBudget` — fields: budgetPeriod, budgetType, revenueBaseRent, revenuePercentageRent, revenueRecoveries, revenueParking, revenueOther, expenseUtilities, expenseRepairsMaintenance, expenseJanitorial, expenseSecurity, expenseInsurance, expenseManagementFee, expenseAdministrative, expenseLandscaping, expenseSnowRemoval, budgetAmount, actualAmount, varianceDollar, variancePercent, priorYearActual, perSFMetric, perUnitMetric (~23 fields)
4. `maintenanceAndWorkOrders` — fields: workOrderId, dateOpened, dateClosed, status, category, priority, reportedBy, assignedVendor, estimatedCost, actualCost, responseTimeHours, completionTimeHours, tenantSatisfactionRating (~13 fields)
5. `vendorManagement` — fields: vendorName, tradeCategory, contractStart, contractEnd, contractValueAnnual, paymentTerms, insuranceCertificateStatus, insuranceExpiryDate, performanceRating, responseTimeAverage, licensedBondedStatus, diversityCertification, scopeOfServices (~13 fields)
6. `buildingOperations` — fields: buildingHoursWeekday, buildingHoursWeekend, buildingHoursHoliday, hvacSchedule, afterHoursHVACRate, afterHoursAccessProcedure, utilityProvider, utilityAccountNumber, utilityMeterNumber, energyConsumptionKWH, energyConsumptionTherms, energyConsumptionGallons, elevatorServiceContract, elevatorInspectionDate, parkingReserved, parkingUnreserved, parkingVisitor, parkingRate, lifeSafetySystem, lifeSafetyLastInspection, lifeSafetyNextDue (~21 fields)
7. `complianceAndInspections` — fields: inspectionType, inspectionDate, inspector, inspectionResult, violationId, violationDescription, violationSeverity, violationDeadline, remediationStatus, certificateOfOccupancyStatus, certificateRenewalDate, environmentalComplianceItem, localBylawComplianceItem (~13 fields)
8. `tenantBillingAndRecoveries` — fields: camEstimated, camActual, camTrueUp, taxBaseYear, taxCurrentYear, taxTenantShare, taxEscalationAmount, utilityBillingMethod, utilityRate, percentageRentBreakpoint, percentageRentSalesReported, percentageRentPercentage, lateFeeAmount, nsfChargeAmount, reconciliationStatementDate (~15 fields)
9. `capitalProjects` — fields: projectName, projectDescription, projectCategory, budgetApproved, actualSpend, budgetVariance, contractor, projectManager, startDate, targetCompletion, actualCompletion, completionPercentage, fundingSource, impactOnPropertyValue, usefulLife (~15 fields)
10. `reportingMetrics` — fields: physicalOccupancyRate, economicOccupancyRate, collectionRateCurrentMonth, collectionRateYTD, arrearsAging, tenantRetentionRate, avgWorkOrderResponseTime, avgWorkOrderCompletionTime, energyUseIntensity, operatingExpenseRatio, rentGrowthYoY, tenantSatisfactionScoreAggregate, deferredMaintenanceBacklog (~13 fields)

Total: ~159 fields.

Cross-reference core glossary where applicable. For example, in the section description for `rentRoll`, note: "Financial metrics use definitions from `core_commercial_re_na@1.0.0 → financialFundamentals`."

Include the standard boilerplate sections at the end (Field Status Tracking, Data Types, Versioning).

**Step 2: Verify format consistency**

Same checks as Task 1. Additionally verify:
- Core cross-references use the format: "See `core_commercial_re_na@1.0.0 → <section>.<field>`"
- Field names don't conflict with core glossary fields (same name = same definition)
- Section count summary in the `## Sections` line is correct

**Step 3: Commit**

```bash
git add docs/ddd/property_management_commercial_na_v1_0.md
git commit -m "feat: add property management domain data dictionary (NA v1.0)"
```

---

### Task 3: Asset Management DDD

**Files:**
- Create: `docs/ddd/asset_management_commercial_na_v1_0.md`

**Step 1: Create the asset management DDD**

Write `docs/ddd/asset_management_commercial_na_v1_0.md` with all 10 sections and full field tables. Expand design doc section 6 bullets into proper field tables.

Sections to include (from design doc section 6):
1. `assetProfile` — fields: propertyReference, acquisitionDate, acquisitionPrice, acquisitionCapRate, currentValuation, valuationDate, valuationMethod, ownershipStructure, jvSplitPercent, fundAllocation, coInvestmentPercent, fundVehicleName, vintageYear, holdPeriodElapsed, holdPeriodTarget, assetStrategy (~16 fields)
2. `financialPerformance` — fields: noiActual, noiBudget, noiPriorYear, noiVariance, revenueBaseRent, revenueRecoveries, revenueParking, revenueOther, expenseBreakdown, capitalExpendituresRoutine, capitalExpendituresNonRoutine, cashFlowBeforeDebtService, cashFlowAfterDebtService, distributionAmount, distributionDate, distributionYield, unleveredReturn, leveredReturn (~18 fields)
3. `valuationMetrics` — fields: goingInCapRate, exitCapRate, marketCapRate, pricePerSFAcquisition, pricePerSFCurrent, replacementCostPerSF, assessedValue, assessmentYear, appraisalValue, appraisalDate, appraiserName, markToMarketDollar, markToMarketPercent, impliedValue (~14 fields)
4. `debtAndCapitalStructure` — fields: loanId, lenderName, loanType, originalPrincipal, currentBalance, maturityDate, interestRateFixed, interestRateSpread, interestRateIndex, ioPeriodEndDate, amortizationSchedule, ltvCurrent, dscrCurrent, dscrCovenant, covenantComplianceStatus, covenantThresholds, prepaymentProvisions, refinancingEstimatedProceeds, refinancingRateAssumptions, refinancingNetBenefit (~20 fields)
5. `holdSellAnalysis` — fields: currentMarketValueEstimate, estimateBasis, projectedDispositionValue, targetExitDate, dispositionCostBrokerPercent, dispositionCostTransferTax, dispositionCostLegal, holdIRR, sellIRR, breakevenHoldPeriod, capitalGainsEstimate, taxImplications, reinvestmentAssumptions, recommendation, recommendationRationale (~15 fields)
6. `leasingStrategy` — fields: currentOccupancy, targetOccupancy, stabilizedOccupancy, waleYears, leaseExpiryProfileByYear, leaseExpiryProfileBySF, leaseExpiryProfileByRevenue, renewalProbabilityByTenant, estimatedDowntimeMonths, marketRentProjectionCurrent, marketRentProjection1Yr, marketRentProjection3Yr, tenantCreditQualityInvestmentGradePercent, tenantCreditQualityNonRatedPercent, topTenantConcentrationPercent (~15 fields)
7. `capitalPlanning` — fields: capexPlan5YearByYear, capexPlan5YearByCategory, capexPlan10YearSummary, deferredMaintenanceItem, deferredMaintenanceCost, deferredMaintenancePriority, reserveFundBalance, targetReserve, annualContribution, roiOnCapitalInvestments, esgUpgradeType, esgUpgradeDescription, expectedImpactOnNOI, expectedImpactOnValue, expectedImpactOnTenantAttraction (~15 fields)
8. `riskAssessment` — fields: marketRiskSupplyPipeline, marketRiskDemandTrends, marketRiskRentalRateTrajectory, tenantConcentrationRiskPercent, leaseRolloverRisk12Months, leaseRolloverRisk24Months, leaseRolloverRisk36Months, environmentalRiskContamination, environmentalRiskFloodZone, environmentalRiskSeismic, regulatoryRiskRentControl, regulatoryRiskZoningChanges, regulatoryRiskTaxReassessment, obsolescenceRiskFunctional, obsolescenceRiskTechnological, obsolescenceRiskDesign, overallRiskRating, riskNarrative (~18 fields)
9. `portfolioContext` — fields: portfolioName, totalPortfolioValue, numberOfAssets, assetShareByValue, assetShareByNOI, peerComparison, sectorAllocationOffice, sectorAllocationIndustrial, sectorAllocationRetail, geographicDiversification, vintageAnalysis, portfolioGrossIRR, portfolioNetIRR, portfolioEquityMultiple (~14 fields)
10. `budgetAndForecasting` — fields: annualBudgetRevenue, annualBudgetExpenses, annualBudgetNOI, annualBudgetCapex, reforecastCadence, varianceCurrentPeriod, varianceYTD, assumptionVacancy, assumptionMarketRentGrowth, assumptionExpenseInflation, assumptionCapRate, scenarioBaseCase, scenarioUpside, scenarioDownside (~14 fields)

Total: ~159 fields.

Include the standard boilerplate sections at the end.

**Step 2: Verify format consistency**

Same checks as Tasks 1-2.

**Step 3: Commit**

```bash
git add docs/ddd/asset_management_commercial_na_v1_0.md
git commit -m "feat: add asset management domain data dictionary (NA v1.0)"
```

---

### Task 4: Leasing DDD

**Files:**
- Create: `docs/ddd/leasing_commercial_na_v1_0.md`

**Step 1: Create the leasing DDD**

Write `docs/ddd/leasing_commercial_na_v1_0.md` with all 10 sections and full field tables. Expand design doc section 7 bullets into proper field tables.

Sections to include (from design doc section 7):
1. `marketAnalysis` — fields: submarketName, metroArea, geographicBoundaries, vacancyRateDirect, vacancyRateSublease, vacancyRateTotal, vacancyTrend, netAbsorptionQuarterly, netAbsorptionAnnual, averageAskingRentGross, averageAskingRentNet, askingRentTrend, averageFreeRentMonths, averageTIPerSF, competitiveSetProperties, constructionPipelineSF, constructionExpectedDelivery, keyDemandDrivers (~18 fields)
2. `comparableLeases` — fields: compPropertyName, compAddress, compSubmarket, compTenantName, compTenantIndustry, compTransactionDate, compLeaseExecutionDate, compSuiteFloor, compAreaSF, compLeaseTermYears, compLeaseTermMonths, compCommencementDate, compBaseRentPerSF, compBaseRentAnnual, compEscalationType, compEscalationRate, compTIAllowancePerSF, compFreeRentMonths, compEffectiveRentPerSF, compEffectiveRentAnnual, compLeaseType, compNetGrossClassification, compBrokers, compListingProcuringSide (~24 fields)
3. `tenantScreening` — fields: prospectName, prospectIndustry, prospectHQLocation, spaceRequirementSF, layoutPreference, floorPreference, targetOccupancyDate, leaseTermPreference, financialRevenue, financialAssets, financialNetWorth, creditRating, dnbRating, publicPrivate, parentEntity, litigationHistory, bankruptcyHistory, currentLocation, reasonForMove, referenceLandlord, referenceBanker (~21 fields)
4. `dealStructuring` — fields: proposedBaseRentPerSF, proposedBaseRentAnnual, proposedBaseRentMonthly, escalationStructure, escalationRate, tiAllowancePerSF, tiAllowanceTotal, tiAmortization, freeRentMonths, freeRentPlacement, expansionOptionSF, expansionOptionTiming, expansionOptionRentDetermination, contractionOptionSF, contractionOptionTiming, contractionOptionPenalty, terminationRightTiming, terminationRightPenalty, terminationRightNoticePeriod, renewalOptionCount, renewalOptionTerm, renewalOptionRentDetermination, parkingAllocation, parkingRate, landlordTotalCost, netEffectiveRent, landlordROI (~27 fields)
5. `loiAndProposal` — fields: loiStatus, loiVersionNumber, loiDateIssued, loiExpirationDate, loiIssuingParty, loiCounterparty, loiKeyTermsRent, loiKeyTermsTerm, loiKeyTermsTI, loiKeyTermsFreeRent, loiKeyTermsCommencement, bindingExclusivity, bindingConfidentiality, bindingCosts, nonBindingBusinessTerms, counterVersion, counterDate, counterKeyChanges, exclusivityPeriodStart, exclusivityPeriodEnd, transitionToLeaseDraftingDate (~21 fields)
6. `commissionAndFees` — fields: commissionRatePercent, commissionStructure, listingBroker, listingBrokerSharePercent, procuringBroker, procuringBrokerSharePercent, totalCommissionAmount, paymentSchedule, overrideProvisions, referralFeePercent, referralFeeTo, coBrokerageTerms (~12 fields)
7. `spacePlanning` — fields: availableSuite, availableFloor, availableSF, availableAskingRent, availabilityDate, typicalFloorPlateSF, testFitSeatsSF, testFitCollaborationRatio, testFitPrivateOfficeCount, canSubdivide, minimumDivisibleSF, buildingAmenities, efficiencyRatio, contiguousBlockSF, subleaseAvailableTenant, subleaseTermRemaining, subleaseAskingRent (~17 fields)
8. `tenantRetention` — fields: retentionTenantName, currentLeaseExpiry, noticeDeadline, renewalProbability, renewalProbabilityBasis, proposedRenewalTerms, currentRent, marketRent, markToMarketPercent, estimatedVacancyCost, competitiveThreats, earlyRenewalIncentive, retentionRatePortfolio, retentionRateBuilding, retentionRateAnnual (~15 fields)
9. `pipelineTracking` — fields: dealId, prospectName, dealSpace, dealSF, dealStage, stageEntryDate, daysInStage, probabilityPercent, expectedCloseDate, expectedCommencementDate, weightedDealValue, brokerAssignment, listingAgent, nextAction, nextActionDate, lostDealReason (~16 fields)
10. `marketRentOpinion` — fields: mroPropertyAddress, mroUnitSuite, mroFloor, mroSF, concludedMarketRentPerSF, concludedMarketRentPerAnnum, rentBasis, effectiveDate, comparableLeasesUsed, adjustmentLocation, adjustmentSize, adjustmentCondition, adjustmentFloorLevel, adjustmentLeaseTerm, adjustmentTI, exposureTimeEstimate, supportingNarrative, preparedBy, datePrepared (~19 fields)

Total: ~190 fields.

Include the standard boilerplate sections at the end.

**Step 2: Verify format consistency**

Same checks as Tasks 1-3.

**Step 3: Commit**

```bash
git add docs/ddd/leasing_commercial_na_v1_0.md
git commit -m "feat: add leasing domain data dictionary (NA v1.0)"
```

---

### Task 5: Investment & Appraisal DDD

**Files:**
- Create: `docs/ddd/investment_appraisal_commercial_na_v1_0.md`

**Step 1: Create the investment & appraisal DDD**

Write `docs/ddd/investment_appraisal_commercial_na_v1_0.md` with all 10 sections and full field tables. Expand design doc section 8 bullets into proper field tables.

Sections to include (from design doc section 8):
1. `propertyDescription` — fields: propertyReference, siteArea, siteFrontage, siteTopography, siteShape, utilitiesAvailability, buildingAreaGBA, buildingAreaRentable, buildingAreaUsable, numberOfFloors, constructionType, roofType, conditionRating, conditionBasis, numberOfUnits, averageUnitSize, parkingType, parkingSpaces, parkingRatio, renovationYear, renovationScope, renovationCost, highestBestUseVacant, highestBestUseImproved, functionalUtilityAssessment (~25 fields)
2. `incomeApproach` — fields: potentialGrossIncome, vacancyAndCreditLossPercent, vacancyAndCreditLossDollar, effectiveGrossIncome, operatingExpensesItemized, netOperatingIncome, capRateSource, capRateSelected, comparableCapRateProperty, comparableCapRateSaleDate, comparableCapRateValue, directCapitalizationValue, stabilizedVsAsIs, aboveBelowMarketLeaseAdjustment (~14 fields)
3. `dcfAnalysis` — fields: projectionPeriodYears, projectionStartDate, revenueProjectionByYear, revenueGrowthAssumptions, expenseProjectionByYear, expenseGrowthRate, expenseFixedVsVariable, capitalReservePerSF, capitalReservePerAnnum, netCashFlowByYear, terminalCapRate, terminalCapRateBasis, reversionValue, sellingCostsPercent, discountRate, discountRateBasis, presentValueCashFlows, presentValueReversion, dcfIndicatedValue, impliedIRR (~20 fields)
4. `salesComparisonApproach` — fields: compSalePropertyName, compSaleAddress, compSaleSaleDate, compSalePrice, compSalePropertyType, compSaleSizeSF, compSaleSizeUnits, compSaleSizeAcres, compSalePricePerSF, compSalePricePerUnit, compSaleCapRate, compSaleNOI, compSaleBuyer, compSaleSeller, compSaleBuyerType, compSaleFinancing, compSaleConditionsOfSale, adjustmentPropertyRights, adjustmentFinancing, adjustmentConditionsOfSale, adjustmentMarketConditions, adjustmentLocation, adjustmentPhysical, adjustmentEconomic, adjustmentUse, adjustedSalePricePerSF, reconciledValueSalesComparison (~27 fields)
5. `costApproach` — fields: landValue, landValueSource, comparableLandSales, replacementCostNewPerSF, replacementCostNewTotal, replacementCostSource, depreciationPhysicalPercent, depreciationPhysicalMethod, depreciationFunctionalPercent, depreciationFunctionalDescription, depreciationExternalPercent, depreciationExternalDescription, totalDepreciationPercent, totalDepreciationDollar, depreciatedCostOfImprovements, siteImprovementsPaving, siteImprovementsLandscaping, siteImprovementsUtilities, costApproachIndicatedValue (~19 fields)
6. `marketStudy` — fields: msaName, submarketDefinition, population, populationGrowthHistorical, populationGrowthProjected, employmentTotal, employmentBySector, unemploymentRate, majorEmployers, employerChanges, medianHouseholdIncome, incomeGrowth, supplyTotalInventorySF, supplyVacancyRate, supplyAvailabilityRate, demandNetAbsorptionQuarterly, demandNetAbsorptionAnnual, demandPreLeasingActivity, rentalRateTrendAsking, rentalRateTrendEffective, concessionTrends, constructionUnderConstructionSF, constructionPlannedSF, constructionExpectedDeliveries, forecastVacancy, forecastRentGrowth, forecastAbsorption (~27 fields)
7. `investmentMetrics` — fields: equityInvestment, leveragedIRR, unleveragedIRR, cashOnCashReturnByYear, cashOnCashReturnAverage, equityMultipleNet, equityMultipleGross, paybackPeriodYears, modifiedIRR, riskAdjustedReturn, benchmarkName, benchmarkReturn, vintageYearReturnComparison (~13 fields)
8. `underwriting` — fields: purchasePrice, purchasePricePerSF, goingInCapRate, financingLTV, financingRate, financingTerm, financingIOPeriod, financingAmortization, closingCostsPercent, closingCostsItemized, year1NOIInPlace, year1NOIStabilized, rentGrowthAssumption, expenseGrowthAssumption, capitalExpenditureBudget, holdPeriodYears, exitCapRate, dispositionCosts, sensitivityNOIGrowth, sensitivityCapRate, sensitivityInterestRate, scenarioBaseCaseIRR, scenarioBaseCaseEquityMultiple, scenarioUpsideIRR, scenarioDownsideIRR (~25 fields)
9. `dueDiligence` — fields: titleReviewStatus, titleExceptions, surveyDate, surveyor, surveyALTAItems, surveyEncroachments, envPhase1Date, envPhase1Firm, envPhase1RECs, envPhase1Recommendation, envPhase2Date, envPhase2Firm, envPhase2Findings, envPhase2RemediationEstimate, physicalConditionDate, physicalConditionFirm, physicalConditionImmediateRepairs, physicalConditionShortTermRepairs, physicalConditionDeferredMaintenance, zoningCurrent, zoningConformance, zoningVarianceRequired, entitlementStatus, thirdPartyReportsList, estoppelCertificateSummary, sndaStatus (~26 fields)
10. `reconciliationAndConclusion` — fields: incomeApproachValue, salesComparisonValue, costApproachValue, incomeApproachWeight, salesComparisonWeight, costApproachWeight, weightingRationale, finalValueConclusion, valuePerSF, valuePerUnit, extraordinaryAssumptions, hypotheticalConditions, effectiveDateOfValue, dateOfReport, appraiserName, appraiserDesignation, appraiserLicenseNumber, intendedUse, intendedUsers (~19 fields)

Total: ~215 fields.

Include the standard boilerplate sections at the end.

**Step 2: Verify format consistency**

Same checks as Tasks 1-4.

**Step 3: Commit**

```bash
git add docs/ddd/investment_appraisal_commercial_na_v1_0.md
git commit -m "feat: add investment & appraisal domain data dictionary (NA v1.0)"
```

---

### Task 6: Update DDD Registry

**Files:**
- Modify: `src/reixs/registry/ddd_refs.py:7-10`
- Modify: test file that covers `ddd_refs.py` (find via grep)

**Step 1: Find the existing test file**

Run: `grep -r "ddd_refs\|KNOWN_DDD_REFS\|is_known_ddd_ref\|is_valid_ddd_format" tests/`

**Step 2: Write a failing test for new DDD refs**

Add test cases that assert the 5 new DDD references are recognized by `is_known_ddd_ref()`:

```python
@pytest.mark.parametrize("ref", [
    "re-ddd:core_commercial_re_na@1.0.0",
    "re-ddd:property_management_commercial_na@1.0.0",
    "re-ddd:asset_management_commercial_na@1.0.0",
    "re-ddd:leasing_commercial_na@1.0.0",
    "re-ddd:investment_appraisal_commercial_na@1.0.0",
])
def test_new_ddd_refs_are_known(ref):
    assert is_known_ddd_ref(ref)
```

**Step 3: Run test to verify it fails**

Run: `pytest tests/<test_file>::test_new_ddd_refs_are_known -v`
Expected: FAIL — refs not in KNOWN_DDD_REFS yet.

**Step 4: Update the registry**

Edit `src/reixs/registry/ddd_refs.py` to add the 5 new references to `KNOWN_DDD_REFS`:

```python
KNOWN_DDD_REFS = {
    "re-ddd:lease_core_terms_ontario@0.1.0",
    "re-ddd:lease_abstraction_commercial_na@1.0.0",
    "re-ddd:core_commercial_re_na@1.0.0",
    "re-ddd:property_management_commercial_na@1.0.0",
    "re-ddd:asset_management_commercial_na@1.0.0",
    "re-ddd:leasing_commercial_na@1.0.0",
    "re-ddd:investment_appraisal_commercial_na@1.0.0",
}
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/<test_file>::test_new_ddd_refs_are_known -v`
Expected: PASS

**Step 6: Run full test suite**

Run: `pytest tests/ -v`
Expected: All tests pass (no regressions).

**Step 7: Commit**

```bash
git add src/reixs/registry/ddd_refs.py tests/<test_file>
git commit -m "feat: register 5 new CRE domain data dictionaries in DDD registry"
```

---

### Task 7: Cross-DDD Consistency Check

**Files:**
- No new files — this is a verification task

**Step 1: Check for field name conflicts**

Search across all DDDs for any field name that appears in multiple DDDs with different types or descriptions. Fields with identical names should have identical types and compatible descriptions.

Run: `grep -h '| \`' docs/ddd/*.md | sort | uniq -d`

Review any duplicates to ensure they're intentionally shared (same definition) rather than conflicting.

**Step 2: Verify all boilerplate sections are identical**

The "Field Status Tracking", "Data Types", and "Versioning" sections should be character-identical across all 6 DDDs. Compare:

Run: `diff <(sed -n '/^## Field Status Tracking/,/^## [^#]/p' docs/ddd/core_commercial_re_na_v1_0.md) <(sed -n '/^## Field Status Tracking/,/^## [^#]/p' docs/ddd/lease_abstraction_commercial_na_v1_0.md)`

Repeat for all pairs.

**Step 3: Verify reference format**

Check that every DDD's `**Reference:**` line matches the `re-ddd:` format and is parseable by `is_valid_ddd_format()`:

```bash
grep '^\*\*Reference:\*\*' docs/ddd/*.md
```

Verify each extracted reference passes `DDD_REF_PATTERN`.

**Step 4: Commit (if fixes needed)**

Only commit if fixes were needed in steps 1-3. Otherwise, this task is complete.

---

### Summary

| Task | DDD | Est. Fields | Commit |
|---|---|---|---|
| 1 | Core CRE Glossary | 68 | `feat: add core CRE glossary domain data dictionary (NA v1.0)` |
| 2 | Property Management | ~159 | `feat: add property management domain data dictionary (NA v1.0)` |
| 3 | Asset Management | ~159 | `feat: add asset management domain data dictionary (NA v1.0)` |
| 4 | Leasing | ~190 | `feat: add leasing domain data dictionary (NA v1.0)` |
| 5 | Investment & Appraisal | ~215 | `feat: add investment & appraisal domain data dictionary (NA v1.0)` |
| 6 | DDD Registry Update | — | `feat: register 5 new CRE domain data dictionaries in DDD registry` |
| 7 | Consistency Check | — | (fix commit if needed) |

**Total new fields:** ~791 across 5 DDDs (plus existing 200+ in lease abstraction = ~1000 total CRE vocabulary).
