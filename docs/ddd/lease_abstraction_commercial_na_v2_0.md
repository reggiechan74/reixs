# Domain Data Dictionary: Commercial Lease Abstraction — North America

**Reference:** `re-ddd:lease_abstraction_commercial_na@2.0.0`

**Scope:** Field definitions for commercial lease abstraction across office and industrial lease types in North American jurisdictions.

**Relationship to REIXS:** This DDD is referenced by REIXS spec `REIXS-LA-NA-001` (Lease Abstraction — North American Commercial). The REIXS spec defines *how* to extract these fields (provenance, status tracking, conflict handling). This DDD defines *what* each field means and its data type. This DDD declares a dependency on `re-ddd:core_commercial_re_na@2.0.0` and uses pointer rows (`->`) to reference shared definitions from the core glossary rather than redefining them.

---

## Sections

The schema defines **28 sections**. Sections 1-24 are extracted from the lease document. Sections 25-28 are derived/analytical.

### 1. documentInformation

Abstract metadata — not extracted from the lease, created by the abstraction process.

| Field | Type | Description |
|---|---|---|
| `abstractDate` | string (ISO 8601) | Date the abstraction was performed |
| `abstractedBy` | string | Person or system that performed the abstraction |
| `sourceDocument` | string | Filename or identifier of the source lease document |
| `lastUpdated` | string (ISO 8601) | Date the abstraction was last updated |
| `leaseDate` | string (ISO 8601) | Date the lease was executed |
| `leaseType` | string | → `core@2.0.0 → leaseClassifications.leaseType` |

### 2. parties

The legal entities bound by the lease.

| Field | Type | Description |
|---|---|---|
| `party.landlord.name` | string | → `core@2.0.0 → parties` with role=landlord |
| `party.landlord.address` | string | → `core@2.0.0 → parties` with role=landlord |
| `party.landlord.entityType` | string | → `core@2.0.0 → parties` with role=landlord |
| `landlord.contact` | string | Contact information (name, phone, email) |
| `landlord.signatories` | array[string] | Names and titles of landlord signatories |
| `party.tenant.name` | string | → `core@2.0.0 → parties` with role=tenant |
| `party.tenant.address` | string | → `core@2.0.0 → parties` with role=tenant |
| `party.tenant.entityType` | string | → `core@2.0.0 → parties` with role=tenant |
| `party.tenant.contactName` | string | → `core@2.0.0 → parties` with role=tenant |
| `tenant.signatories` | array[string] | Names and titles of tenant signatories |
| `tenant.incorporationJurisdiction` | string | Province/state of tenant's incorporation |
| `indemnifier.name` | string | Full legal name of guarantor/indemnifier |
| `indemnifier.address` | string | Registered address of the indemnifier |
| `indemnifier.relationshipToTenant` | string | Legal relationship (e.g., parent company, principal) |
| `indemnifier.contact` | string | Contact information for the indemnifier |
| `indemnifier.signatories` | array[string] | Names and titles of indemnifier signatories |

**Critical section** — 2x scoring weight. Misidentification of landlord/tenant is an AutoFail condition.

### 3. premises

Physical description of the leased space.

| Field | Type | Description |
|---|---|---|
| `propertyInformation.projectName` | string | Name of the building, complex, or project |
| `propertyInformation.buildingAddress` | string | Street address of the building |
| `propertyInformation.unitNumber` | string | Suite or unit number within the building |
| `propertyInformation.legalDescription` | string | Legal description (lot, plan, municipal reference) |
| `propertyInformation.buildingType` | string | Single-tenant or multi-tenant |
| `rentableArea` | number | → `core@2.0.0 → areaAndMeasurement.rentableArea` |
| `measurementStandard` | string | → `core@2.0.0 → areaAndMeasurement.measurementStandard` |
| `area.commonFacilities` | string | Description of shared/common areas |
| `area.parkingSpaces` | number | Number of allocated parking spaces |
| `area.storage` | string | Storage space description and allocation |
| `area.floorLoadLimitPsf` | number | Maximum floor load capacity in pounds per square foot |
| `permittedUse.primaryUse` | string | Primary permitted use of the premises |
| `permittedUse.restrictions` | array[string] | Use restrictions imposed by the lease |
| `permittedUse.prohibitedUses` | array[string] | Explicitly prohibited uses |

**Critical section** — 2x scoring weight.

### 4. term

Duration and timing of the lease.

| Field | Type | Description |
|---|---|---|
| `leaseTerm.commencementDate` | string (ISO 8601) | Date the lease term begins |
| `leaseTerm.deliveryDate` | string (ISO 8601) | Date premises are delivered to tenant (may differ from commencement) |
| `leaseTerm.expiryDate` | string (ISO 8601) | Date the lease term ends |
| `leaseTerm.termLengthYears` | number | Length of the lease term in years |
| `leaseTerm.termLengthMonths` | number | Length of the lease term in months (if not whole years) |
| `leaseTerm.fixturingPeriod` | string | Duration and terms of any fixturing/build-out period |
| `leaseTerm.deliveryConditions` | array[string] | Conditions for premises delivery (insurance, deposit, cheques) |
| `leaseTerm.acceptanceType` | string | How premises are accepted (as-is, with/without landlord work) |
| `renewalOptions.numberOfOptions` | number | Number of renewal options available to tenant |
| `renewalOptions.lengthOfEachOption` | string | Duration of each renewal option period |
| `renewalOptions.noticePeriodRequired` | string | Notice period to exercise renewal (e.g., "12 months prior to expiry") |
| `renewalOptions.rentDeterminationMethod` | string | How renewal rent is determined (e.g., fair market, fixed increase) |
| `renewalOptions.rentBasis` | string | Basis for renewal rent (e.g., greater of market rent or last year's rent) |
| `renewalOptions.noAllowanceOrIncentive` | boolean | Whether renewal excludes allowances or incentives |
| `renewalOptions.premisesAsIs` | boolean | Whether renewal is on as-is basis |
| `renewalOptions.earliestNoticeMonths` | number | Earliest month before expiry to give renewal notice |
| `renewalOptions.latestNoticeMonths` | number | Latest month before expiry to give renewal notice |
| `marketRentDetermination.factors` | array[string] | Factors used to determine market rent |
| `marketRentDetermination.agreementDeadlineMonths` | number | Months before expiry to agree on market rent |
| `marketRentDetermination.interimRatePct` | number | Interim rent rate as percentage of prior rent during determination |
| `marketRentDetermination.expertProcess` | string | Expert determination process (qualification, timeline, cost split, binding) |
| `earlyTermination.terminationRights` | boolean | Whether the tenant has early termination rights |
| `earlyTermination.conditions` | string | Conditions that must be met for early termination |
| `earlyTermination.noticePeriod` | string | Required notice period for early termination |
| `earlyTermination.penalties` | string | Financial penalties for early termination |

**Critical section** — 2x scoring weight. Commencement/expiry dates without provenance is an AutoFail condition.

### 5. rent

Financial obligations for base rent and escalations.

| Field | Type | Description |
|---|---|---|
| `basicRent[].period` | string | Period label (e.g., "Year 1", "Months 1-12") |
| `basicRent[].annualRent` | number | Annual base rent amount |
| `basicRent[].monthlyRent` | number | Monthly base rent amount |
| `basicRent[].ratePerSqFt` | number | Rent rate per square foot |
| `rentEscalations.escalationType` | string | Type of escalation (fixed, CPI, market) |
| `rentEscalations.frequency` | string | How often escalations occur |
| `rentEscalations.baseYearOrIndex` | string | Base year or index used for escalation calculation |
| `rentEscalations.capPercentage` | number | Maximum annual increase percentage |
| `rentEscalations.floorPercentage` | number | Minimum annual increase percentage |
| `additionalRent.operatingCosts.tenantShare` | string | Tenant's share of operating costs |
| `additionalRent.operatingCosts.method` | string | Calculation method for operating cost share |
| `additionalRent.realtyTaxes.tenantShare` | string | Tenant's share of realty taxes |
| `additionalRent.realtyTaxes.method` | string | Calculation method for tax share |
| `additionalRent.managementFee.percentage` | number | Management fee as percentage |
| `additionalRent.managementFee.basis` | string | What the management fee is calculated on |
| `additionalRent.utilities.separatelyMetered` | boolean | Whether utilities are separately metered |
| `additionalRent.utilities.tenantResponsibility` | string | Which utilities tenant pays directly |
| `additionalRent.camCharges` | string | Common area maintenance charges |
| `proportionateShare.calculationMethod` | string | How proportionate share is calculated |
| `proportionateShare.percentage` | number | Tenant's proportionate share percentage |
| `proportionateShare.adjustmentProvisions` | string | How the share is adjusted over time |
| `paymentTerms.dueDate` | string | When rent payments are due |
| `paymentTerms.paymentMethod` | string | Accepted payment methods |
| `paymentTerms.latePaymentPenalty` | string | Penalty for late payment |
| `paymentTerms.nsfFee` | number | Fee for insufficient funds / bounced payment |
| `currency` | string | → `core@2.0.0 → currencyAndUnits.currency` |
| `estimatedAdditionalRent.perSqFt` | number | Estimated additional rent per square foot |
| `estimatedAdditionalRent.year` | number | Year of the additional rent estimate |
| `estimatedAdditionalRent.total` | number | Total estimated additional rent amount |
| `padAuthorizationRequired` | boolean | Whether pre-authorized debit is required |
| `auditRights.tenantHasAuditRight` | boolean | Whether tenant can audit operating cost statements |
| `auditRights.requestDeadlineDays` | number | Days after final statement to request audit |
| `auditRights.contingencyFeeProhibited` | boolean | Whether auditor contingency fees are prohibited |
| `auditRights.ndaRequired` | boolean | Whether NDA is required for audit |
| `auditRights.claimDeadlineMonths` | number | Months after final statement to make claims |
| `finalStatement.deliveryDeadlineDays` | number | Days after fiscal period for landlord to deliver final statement |

**Critical section** — 2x scoring weight. Financial values must be extracted verbatim with normalized form as a separate field. Wrong currency is an AutoFail condition.

### 6. depositsAndSecurity

Security deposits and credit instruments.

| Field | Type | Description |
|---|---|---|
| `rentDeposit.amount` | number | Deposit amount |
| `rentDeposit.heldAs` | string | How the deposit is held (e.g., trust, general account) |
| `rentDeposit.interest` | boolean | Whether interest accrues on the deposit |
| `rentDeposit.interestRate` | number | Interest rate applied to deposit |
| `rentDeposit.application` | string | When/how the deposit may be applied |
| `rentDeposit.returnConditions` | string | Conditions for return of deposit |
| `rentDeposit.restorationDays` | number | Days to restore deposit after draw-down |
| `rentDeposit.restorationInterestPremium` | string | Interest premium on unrestored deposit (e.g., "3% above Prime") |
| `rentDeposit.returnDaysAfterExpiry` | number | Days after lease expiry to return deposit |
| `rentDeposit.securedItems` | array[string] | Items secured by the deposit |
| `letterOfCredit.required` | boolean | Whether an LOC is required |
| `letterOfCredit.amount` | number | LOC face amount |
| `letterOfCredit.beneficiary` | string | Named beneficiary of the LOC |
| `letterOfCredit.expiry` | string | LOC expiry date or terms |
| `letterOfCredit.reductionProvisions` | string | How the LOC amount may be reduced over time |
| `otherSecurity.type` | string | Type of additional security |
| `otherSecurity.amount` | number | Amount of additional security |
| `otherSecurity.terms` | string | Terms governing additional security |

### 7. operatingCostsAndTaxes

Lease structure and cost allocation.

| Field | Type | Description |
|---|---|---|
| `leaseType` | string | → `core@2.0.0 → leaseClassifications.leaseType` — see also documentInformation §1 |
| `netLeaseProvisions.tenantObligations` | array[string] | Specific cost obligations assigned to tenant |
| `operatingCosts.includedItems` | array[string] | Items included in operating cost calculations |
| `operatingCosts.excludedItems` | array[string] | Items excluded from operating cost calculations |
| `operatingCosts.baseYear` | string | Base year for operating cost calculations |
| `operatingCosts.grossUpProvisions` | string | Gross-up provisions for occupancy adjustments |
| `operatingCosts.cap` | number | Cap on operating cost increases (percentage or amount) |
| `operatingCosts.amortizationInterestRate` | string | Interest rate for amortizing capital items in operating costs |
| `excessCosts.premiumPct` | number | Premium percentage charged on excess/above-standard costs |
| `excessCosts.triggers` | array[string] | Events triggering excess cost charges |
| `realtyTaxes.paymentMethod` | string | How tenant pays its tax share |
| `realtyTaxes.tenantShare` | string | Tenant's proportionate share of taxes |
| `realtyTaxes.contestRights` | string | Tenant's right to contest tax assessments |
| `realtyTaxes.taxIncreaseLimitations` | string | Limitations on tax increase pass-throughs |
| `realtyTaxes.vacancyCreditsRetainedByLandlord` | boolean | Whether tax vacancy credits are retained by landlord |
| `businessAndSalesTaxes.responsibility` | string | Which party is responsible for business/sales taxes |
| `businessAndSalesTaxes.hstGst` | string | HST/GST applicability and responsibility |
| `capitalAndCarbonTaxes.applicable` | boolean | Whether capital or carbon taxes apply |

### 8. useAndOperations

Permitted activities and operating requirements.

| Field | Type | Description |
|---|---|---|
| `permittedUse.specificUsesAllowed` | array[string] | Specific uses permitted |
| `permittedUse.buildingStandard` | string | Building standard applicable to the premises |
| `permittedUse.complianceRequirements` | array[string] | Compliance requirements for the permitted use |
| `prohibitedUses.specificProhibitions` | array[string] | Explicitly prohibited uses |
| `prohibitedUses.hazardousSubstances` | string | Restrictions on hazardous substances |
| `prohibitedUses.bioMedicalWaste` | string | Restrictions on biomedical waste |
| `operatingHours.businessHours` | string | Standard business hours for the building |
| `operatingHours.access` | string | Tenant access hours (may differ from business hours) |
| `operatingHours.afterHoursHVAC` | string | Availability and cost of after-hours HVAC |
| `signage.exteriorSignageRights` | string | Tenant's rights for exterior signage |
| `signage.interiorSignage` | string | Interior signage provisions |
| `signage.approvalRequirements` | string | Required approvals for signage |
| `signage.costResponsibility` | string | Who pays for signage installation and maintenance |
| `exclusiveCovenants.grantedToOthers` | boolean | Whether exclusive use covenants have been granted to other tenants |
| `continuousOperationsRequired` | boolean | Whether tenant must continuously operate business |
| `telecomAndWireless.landlordConsentRequired` | boolean | Whether landlord consent required for telecom/wireless installations |
| `wasteRemoval.tenantResponsibility` | string | Waste removal obligations and responsibility |

### 9. maintenanceAndRepairs

Maintenance responsibilities allocated between parties.

| Field | Type | Description |
|---|---|---|
| `landlordObligations.structural` | string | Structural maintenance responsibility |
| `landlordObligations.roof` | string | Roof maintenance responsibility |
| `landlordObligations.commonAreas` | string | Common area maintenance responsibility |
| `landlordObligations.buildingSystems` | string | Building systems (electrical, plumbing) maintenance |
| `landlordObligations.hvac` | string | HVAC system maintenance responsibility |
| `tenantObligations.interiorMaintenance` | string | Interior maintenance responsibility |
| `tenantObligations.equipment` | string | Equipment maintenance responsibility |
| `tenantObligations.janitorial` | string | Janitorial services responsibility |
| `tenantObligations.repairsUnderThreshold` | number | Dollar threshold below which tenant pays for repairs |
| `tenantObligations.snowRemoval` | boolean | Whether tenant is responsible for snow removal |
| `exclusiveSupplier.landlordRight` | boolean | Whether landlord has right to designate exclusive suppliers for certain services |
| `capitalImprovements.landlordsRights` | string | Landlord's rights regarding capital improvements |
| `capitalImprovements.tenantObligations` | string | Tenant's obligations for capital improvements |
| `capitalImprovements.amortization` | string | How capital improvement costs are amortized |

### 10. alterationsAndImprovements

Modifications to the premises.

| Field | Type | Description |
|---|---|---|
| `landlordWork.description` | string | Description of landlord's initial work/build-out |
| `landlordWork.completionDate` | string (ISO 8601) | Date landlord's work must be completed |
| `landlordWork.allowance` | number | Tenant improvement allowance from landlord |
| `tenantWork.preApprovalRequired` | boolean | Whether landlord approval is required for tenant work |
| `tenantWork.approvalThreshold` | number | Dollar threshold above which approval is required |
| `tenantWork.architectEngineerRequirements` | string | Professional requirements for tenant's work |
| `tenantWork.insuranceDuringConstruction` | string | Insurance requirements during construction |
| `tenantWork.permitsResponsibility` | string | Who is responsible for obtaining permits |
| `tenantWork.constructionInsuranceMinimum` | number | Minimum CGL coverage for construction work |
| `tenantWork.overheadPct` | number | Landlord's overhead/supervision percentage on tenant work |
| `tenantWork.plansReviewLeadTimeWeeks` | number | Minimum weeks for landlord to review plans |
| `tenantWork.constructionHours` | string | Permitted hours for construction work |
| `constructionLiens.dischargeDays` | number | Days to discharge a construction lien |
| `constructionLiens.adminFeePct` | number | Administrative fee percentage on lien-related costs |
| `leaseholdImprovements.ownership` | string | Who owns leasehold improvements during the term |
| `leaseholdImprovements.removalAtEndOfTerm` | string | Requirements for removal at end of term |
| `leaseholdImprovements.restorationObligations` | string | Restoration obligations at end of term |
| `leaseholdImprovementAllowance.perSqFt` | number | Allowance per square foot |
| `leaseholdImprovementAllowance.conditions` | array[string] | Conditions to receive allowance |
| `leaseholdImprovementAllowance.clawbackOnDefault` | boolean | Whether allowance is clawed back on default |
| `tradeFixtures.definition` | string | How trade fixtures are defined in the lease |
| `tradeFixtures.removalRights` | string | Tenant's rights to remove trade fixtures |
| `tradeFixtures.restoration` | string | Restoration requirements after fixture removal |

### 11. insuranceAndIndemnity

Insurance requirements and indemnification provisions.

| Field | Type | Description |
|---|---|---|
| `landlordInsurance.propertyInsurance` | string | Landlord's property insurance coverage |
| `landlordInsurance.liabilityInsurance` | string | Landlord's liability insurance coverage |
| `landlordInsurance.other` | string | Other insurance carried by landlord |
| `landlordInsurance.rentalIncomeInsurance` | boolean | Whether landlord carries rental income insurance |
| `tenantInsuranceRequirements.commercialGeneralLiability.minimumCoverage` | number | Minimum CGL coverage amount |
| `tenantInsuranceRequirements.commercialGeneralLiability.namedInsured` | string | Who must be named as additional insured |
| `tenantInsuranceRequirements.propertyInsurance.allRiskCoverage` | number | All-risk property coverage amount |
| `tenantInsuranceRequirements.propertyInsurance.businessInterruption` | number | Business interruption coverage amount |
| `tenantInsuranceRequirements.otherRequiredCoverage` | array[string] | Other insurance coverages tenant must maintain |
| `tenantInsuranceRequirements.certificateRequirements` | string | When/how insurance certificates must be provided |
| `tenantInsuranceRequirements.renewalNotice` | string | Notice requirements for insurance renewal |
| `tenantInsuranceRequirements.cglExtensions` | array[string] | Required CGL policy extensions |
| `tenantInsuranceRequirements.boilerMachineryInsurance` | boolean | Whether boiler/machinery insurance is required |
| `tenantInsuranceRequirements.plateGlassInsurance` | boolean | Whether plate glass insurance is required |
| `tenantInsuranceRequirements.cancellationNoticeDays` | number | Days notice required for insurance cancellation |
| `waiverOfSubrogation.appliesTo` | array[string] | Parties to whom waiver of subrogation applies |
| `indemnification.tenantIndemnifiesLandlordFor` | array[string] | Events for which tenant indemnifies landlord |
| `indemnification.landlordIndemnifiesTenantFor` | array[string] | Events for which landlord indemnifies tenant |
| `indemnification.exceptions` | array[string] | Exceptions to indemnification provisions |
| `consequentialDamagesExcluded` | boolean | Whether consequential damages are mutually excluded |

### 12. damageAndDestruction

Casualty provisions.

| Field | Type | Description |
|---|---|---|
| `casualtyProvisions.landlordRepairObligation` | string | Landlord's obligation to repair after damage |
| `casualtyProvisions.timeToRepair` | string | Timeframe for landlord to complete repairs |
| `casualtyProvisions.substantialDamageDefinition` | string | How "substantial damage" is defined |
| `casualtyProvisions.substantialDamageRights` | string | Rights of parties when damage is substantial |
| `casualtyProvisions.damageOpinionDeliveryDays` | number | Days for landlord to deliver damage/repair opinion |
| `casualtyProvisions.tenantReconstructionDeadlineDays` | number | Days for tenant to complete its reconstruction after landlord finishes |
| `casualtyProvisions.terminationCostThresholdPct` | number | Cost threshold (% over insurance) triggering termination right |
| `casualtyProvisions.terminationElectionDays` | number | Days to elect termination after receiving damage opinion |
| `rentAbatement.duringRepairs` | string | Rent abatement provisions during repairs |
| `rentAbatement.conditions` | string | Conditions for rent abatement |
| `rentAbatement.tenantAccess` | string | Tenant access provisions during repairs |
| `rentAbatement.endTriggerDays` | number | Days after premises ready that rent abatement ends |
| `uninsuredCasualty.landlordObligations` | string | Landlord's obligations for uninsured damage |
| `uninsuredCasualty.terminationRights` | string | Termination rights for uninsured damage |
| `projectDamage.terminationThresholdPct` | number | Project damage threshold (% of rentable area) for termination |
| `projectDamage.terminationNoticeDays` | number | Days after project damage to give termination notice |

### 13. assignmentAndSubletting

Transfer and subletting restrictions.

| Field | Type | Description |
|---|---|---|
| `transferRestrictions.assignmentAllowed` | string | Whether and under what conditions assignment is permitted |
| `transferRestrictions.sublettingAllowed` | string | Whether and under what conditions subletting is permitted |
| `transferRestrictions.consentStandard` | string | Standard for landlord consent (e.g., "not to be unreasonably withheld") |
| `transferRestrictions.consentDeemedRefusedDays` | number | Days after which no response is deemed refusal |
| `transferRestrictions.consentWithholdReasons` | array[string] | Enumerated reasons landlord may withhold consent |
| `landlordRights.recaptureRight` | boolean | Whether landlord has right to recapture space |
| `landlordRights.profitSharing` | number | Percentage of subletting profit shared with landlord |
| `landlordRights.processingFee` | number | Administrative fee for processing transfer requests |
| `landlordRights.takeoverRight` | boolean | Whether landlord can take over the proposed transfer on same terms |
| `landlordRights.recaptureExerciseDays` | number | Days for landlord to exercise recapture/takeover right |
| `permittedTransfers.affiliateTransfers` | string | Rules for transfers to affiliates |
| `permittedTransfers.changeOfControl` | string | Whether change of control triggers consent requirement |
| `permittedTransfers.conditions` | array[string] | Conditions for permitted transfers |
| `transferRequirements.noticePeriod` | string | Required notice period for transfer requests |
| `transferRequirements.informationRequired` | array[string] | Information that must be provided with transfer request |
| `transferRequirements.financialCovenant` | string | Financial requirements for proposed transferee |
| `transferRequirements.ongoingLiability` | string | Whether original tenant remains liable after transfer |
| `transferRequirements.processingDeposit` | number | Non-refundable deposit for processing transfer request |

### 14. defaultAndRemedies

Default events and remedial provisions.

| Field | Type | Description |
|---|---|---|
| `eventsOfDefault.nonPayment.gracePeriod` | string | Grace period for non-payment of rent |
| `eventsOfDefault.nonPayment.curePeriodBusinessDays` | number | Business days to cure non-payment default |
| `eventsOfDefault.breachOfCovenants.curePeriod` | string | Cure period for breach of lease covenants |
| `eventsOfDefault.breachOfCovenants.curePeriodBusinessDays` | number | Business days to cure non-monetary default |
| `eventsOfDefault.insuranceFailure.curePeriodHours` | number | Hours to cure insurance default |
| `eventsOfDefault.bankruptcyInsolvency` | string | Default triggered by bankruptcy or insolvency |
| `eventsOfDefault.abandonment` | string | Default triggered by abandonment of premises |
| `eventsOfDefault.other` | array[string] | Other events constituting default |
| `landlordRemedies.termination` | string | Landlord's right to terminate upon default |
| `landlordRemedies.reEntry` | string | Landlord's right of re-entry |
| `landlordRemedies.damages` | string | Landlord's right to claim damages |
| `landlordRemedies.distress` | string | Landlord's right of distress (seizure of property) |
| `landlordRemedies.rentAccelerationMonths` | number | Months of accelerated rent on default |
| `landlordRemedies.overheadPct` | number | Landlord's overhead percentage on default remedy costs |
| `landlordRemedies.other` | array[string] | Other remedies available to landlord |
| `interestOnLatePayments.rate` | string | Interest rate on overdue payments |
| `interestOnLatePayments.calculationMethod` | string | How interest on late payments is calculated |
| `costs.legalFeesResponsibility` | string | Responsibility for legal fees in default proceedings |
| `costs.collectionCosts` | string | Responsibility for collection costs |

### 15. servicesAndUtilities

Building services and utility arrangements.

| Field | Type | Description |
|---|---|---|
| `utilitiesProvidedByLandlord.electricity` | string | Electricity provisions by landlord |
| `utilitiesProvidedByLandlord.waterSewer` | string | Water/sewer provisions by landlord |
| `utilitiesProvidedByLandlord.gas` | string | Gas provisions by landlord |
| `utilitiesProvidedByLandlord.hvac` | string | HVAC provisions by landlord |
| `utilitiesProvidedByLandlord.other` | array[string] | Other services provided by landlord |
| `utilitiesTenantResponsibility.separatelyMetered` | array[string] | Utilities separately metered to tenant |
| `utilitiesTenantResponsibility.paymentMethod` | string | How tenant pays for separately metered utilities |
| `utilitiesTenantResponsibility.afterHoursHVAC` | string | After-hours HVAC availability and cost |
| `serviceInterruptions.landlordLiability` | string | Landlord's liability for service interruptions |
| `serviceInterruptions.rentAbatement` | string | Rent abatement for prolonged service interruption |
| `serviceInterruptions.forceMajeure` | string | Force majeure provisions for service interruptions |

### 16. environmental

Environmental compliance and remediation.

| Field | Type | Description |
|---|---|---|
| `environmentalCompliance.tenantObligations` | array[string] | Tenant's environmental compliance obligations |
| `environmentalCompliance.hazardousSubstances` | string | Restrictions on hazardous substances |
| `environmentalCompliance.phaseRequirements` | string | Environmental assessment phase requirements |
| `environmentalIndemnity.scope` | string | Scope of environmental indemnification |
| `environmentalIndemnity.survival` | string | Whether environmental indemnity survives lease termination |
| `remediation.responsibility` | string | Responsibility for environmental remediation |
| `remediation.costAllocation` | string | How remediation costs are allocated |
| `remediation.accessForTesting` | string | Access provisions for environmental testing |

### 17. subordinationAndAttornment

Priority and registration provisions.

| Field | Type | Description |
|---|---|---|
| `subordination.leaseSubordinateTo` | string | Instruments to which the lease is subordinate |
| `subordination.sndaRequired` | boolean | Whether an SNDA is required |
| `subordination.sndaProvided` | boolean | Whether an SNDA has been provided |
| `subordination.conditions` | array[string] | Conditions for subordination |
| `subordination.nonDisturbanceAdminFee` | number | Administrative fee for non-disturbance agreement |
| `statusStatement.deliveryDays` | number | Days to deliver status/estoppel certificate |
| `statusStatement.financialStatementsRequired` | boolean | Whether landlord can require tenant financial statements |
| `registration.leaseRegistration` | string | Whether/how the lease is registered on title |
| `registration.noticeOfLease` | string | Whether a notice or caveat is registered |

### 18. notices

Notice delivery requirements.

| Field | Type | Description |
|---|---|---|
| `noticeRequirements.form` | string | Required form of notice (written, electronic) |
| `noticeRequirements.deliveryMethod` | array[string] | Acceptable delivery methods (personal, registered mail, courier) |
| `noticeRequirements.deemedReceived` | string | When notice is deemed received after sending |
| `noticeAddresses.landlord.address` | string | Landlord's notice address |
| `noticeAddresses.landlord.attention` | string | Attention line for landlord notices |
| `noticeAddresses.landlord.email` | string | Landlord's email for notices (if permitted) |
| `noticeAddresses.tenant.address` | string | Tenant's notice address |
| `noticeAddresses.tenant.attention` | string | Attention line for tenant notices |
| `noticeAddresses.tenant.email` | string | Tenant's email for notices (if permitted) |
| `noticeAddresses.copyTo` | array[string] | Additional parties who receive copies of notices |

### 19. endOfTerm

Lease expiration provisions.

| Field | Type | Description |
|---|---|---|
| `surrenderRequirements.condition` | string | Required condition of premises upon surrender |
| `surrenderRequirements.removalOfImprovements` | array[string] | Improvements tenant must remove |
| `surrenderRequirements.removalOfEquipment` | string | Equipment removal requirements |
| `surrenderRequirements.cleaning` | string | Cleaning requirements upon surrender |
| `overholding.permitted` | boolean | Whether overholding is permitted |
| `overholding.rentDuringOverholding` | string | Rent rate during overholding (e.g., "150% of last month's rent") |
| `overholding.consequences` | string | Other consequences of overholding |
| `overholding.rateWithConsentPct` | number | Overholding rent as percentage of last year's rent (with consent) |
| `overholding.rateWithoutConsentPct` | number | Overholding rent as percentage (without consent) |
| `finalStatement.reconciliation` | string | Final cost reconciliation provisions |
| `finalStatement.timing` | string | Timing for final statement and reconciliation |

### 20. landlordControlOfProject

Landlord's rights over the project, tenant relocation, and landlord-initiated termination.

| Field | Type | Description |
|---|---|---|
| `projectControl.exclusiveControlByLandlord` | boolean | Whether landlord has exclusive control of the project |
| `projectControl.rightToAlterProject` | boolean | Landlord's right to make alterations to the project |
| `relocation.landlordRightToRelocate` | boolean | Whether landlord can relocate tenant within the project |
| `relocation.conditions` | string | Conditions for relocation (e.g., substantially same size) |
| `relocation.movingCostResponsibility` | string | Who pays moving costs |
| `tenantAccess.twentyFourSeven` | boolean | Whether tenant has 24/7 access to premises |
| `tenantAccess.conditions` | string | Conditions on after-hours access |
| `landlordTermination.noticePeriod` | string | Notice period for landlord-initiated termination |
| `landlordTermination.triggers` | array[string] | Events triggering landlord termination right (sale, demolition, substantial alteration) |
| `forRentSigns.noticePeriodMonths` | number | Months before expiry landlord may post for-rent signs |
| `noiseAndVibration.landlordLiabilityExcluded` | boolean | Whether landlord is not liable for noise/vibration from nearby operations |

### 21. expropriation

Compulsory acquisition/eminent domain provisions.

| Field | Type | Description |
|---|---|---|
| `tenantCompensationScope` | string | Scope of tenant's compensation rights (e.g., relocation costs and business interruption only) |
| `compensationAssignmentToLandlord` | boolean | Whether tenant must assign other compensation to landlord |
| `assignmentExecutionDays` | number | Days to execute compensation assignment documents |

### 22. governingLawAndMiscellaneous

Jurisdiction, boilerplate, and general provisions.

| Field | Type | Description |
|---|---|---|
| `governingLaw.jurisdiction` | string | Governing law jurisdiction (e.g., Province of Ontario) |
| `governingLaw.courts` | string | Courts with jurisdiction |
| `jointAndSeveralLiability` | boolean | Whether multiple tenants/indemnifiers are jointly and severally liable |
| `timeOfTheEssence` | boolean | Whether time is of the essence |
| `entireAgreement` | boolean | Whether lease constitutes the entire agreement |
| `landlordEntityType.isTrust` | boolean | Whether landlord entity is a REIT or trust |
| `landlordEntityType.liabilityLimitedToProjectInterest` | boolean | Whether landlord liability is limited to its interest in the project |
| `planningActCompliance` | string | Planning Act compliance provisions (Ontario-specific) |
| `privacyConsent` | boolean | Whether tenant consents to privacy policy |
| `forceMajeure.applies` | boolean | Whether force majeure clause exists |
| `forceMajeure.excludesPaymentObligations` | boolean | Whether force majeure excludes rent/payment obligations |

### 23. specialProvisions

Custom terms, typically from Schedule G or equivalent.

| Field | Type | Description |
|---|---|---|
| `fixturingPeriod.startDate` | string (ISO 8601) | Start date of fixturing period |
| `fixturingPeriod.endDate` | string (ISO 8601) | End date of fixturing period |
| `fixturingPeriod.rentExemptions` | array[string] | Which rent components are exempt during fixturing |
| `rentFreePeriod.duration` | string | Duration of basic rent-free period |
| `rentFreePeriod.startDate` | string (ISO 8601) | Start of rent-free period |
| `rentFreePeriod.endDate` | string (ISO 8601) | End of rent-free period |
| `rentFreePeriod.obligationsStillPayable` | array[string] | Obligations that remain payable during rent-free period |
| `earlyOccupancy.startDate` | string (ISO 8601) | Start of early occupancy period |
| `earlyOccupancy.endDate` | string (ISO 8601) | End of early occupancy period |
| `earlyOccupancy.rentExemptions` | array[string] | Which rent components are exempt during early occupancy |
| `requiredConditions` | array[string] | Preconditions for special provisions (e.g., original tenant, no default) |
| `customTerms` | array[string] | Other special provisions not captured in structured fields above |

Schedule G provisions that contradict main body terms trigger the `schedule_override` SESF rule — the Schedule G value takes precedence and the override must be flagged.

### 24. schedulesAndExhibits

Attached schedules (A through J, or as applicable).

| Field | Type | Description |
|---|---|---|
| `attachedSchedules.schedule{X}.title` | string | Title of the schedule |
| `attachedSchedules.schedule{X}.attached` | boolean | Whether the schedule is attached to the lease |
| `attachedSchedules.schedule{X}.summary` | string | Summary of key contents |
| `keyItemsFromSchedules` | array[string] | Key items extracted from attached schedules |
| `indemnityAgreement.isAbsoluteUnconditional` | boolean | Whether indemnity is absolute and unconditional |
| `indemnityAgreement.coversExtensionsRenewals` | boolean | Whether indemnity covers extensions and renewals |
| `indemnityAgreement.financialReportingRequired` | boolean | Whether indemnifier must provide financial statements |
| `indemnityAgreement.assetDepletionConsentRequired` | boolean | Whether indemnifier needs consent for material asset depletion |

Standard schedule mapping (varies by lease):

| Schedule | Typical Title |
|---|---|
| A | Legal Description of Project |
| B | Outline Plan of Premises |
| C | Landlord's and Tenant's Work |
| D | Rent Deposit Agreement |
| E | Environmental Questionnaire |
| F | Rules and Regulations |
| G | Special Provisions |
| H | Indemnity Agreement |
| I | Pre-Authorized Debit (PAD) Authorization |
| J | Letter of Credit Agreement |

### 25. criticalDates

*Derived section* — compiled from extracted dates across all sections.

| Field | Type | Description |
|---|---|---|
| `criticalDates[].event` | string | Description of the date event |
| `criticalDates[].date` | string (ISO 8601) | The date |
| `criticalDates[].noticeRequired` | string | Notice requirements associated with this date |
| `criticalDates[].actionRequired` | string | Action required by this date |

Standard events include: Lease Commencement, First Rent Payment, Renewal Option Notice, Lease Expiry. Additional events are derived from the lease.

### 26. financialObligations

*Derived section* — calculated from extracted financial data.

| Field | Type | Description |
|---|---|---|
| `initialCosts.firstMonthRent` | number | First month's rent payment |
| `initialCosts.rentDeposit` | number | Required rent deposit |
| `initialCosts.letterOfCredit` | number | Letter of credit amount |
| `initialCosts.other` | number | Other initial costs |
| `initialCosts.total` | number | Total initial costs |
| `ongoingMonthlyCosts.basicRent` | number | Monthly base rent |
| `ongoingMonthlyCosts.operatingCosts` | number | Monthly operating cost share |
| `ongoingMonthlyCosts.realtyTaxes` | number | Monthly realty tax share |
| `ongoingMonthlyCosts.managementFee` | number | Monthly management fee |
| `ongoingMonthlyCosts.utilities` | number | Monthly utility costs |
| `ongoingMonthlyCosts.estimatedTotal` | number | Estimated total monthly cost |

### 27. keyIssuesAndRisks

*Derived section* — analytical assessment of the lease terms.

| Field | Type | Description |
|---|---|---|
| `favorableTerms` | array[string] | Terms that are favorable to the tenant |
| `unfavorableTermsRisks` | array[string] | Terms that are unfavorable or create risk for the tenant |
| `itemsRequiringFurtherReview` | array[string] | Items that require legal or business review |

For markdown output: limit to top 5 critical red flags, top 5-7 favorable, top 5-7 unfavorable, top 10 review items.

### 28. notesAndComments

*Optional section* — free-form notes and observations not captured in the structured sections above.

| Field | Type | Description |
|---|---|---|
| `notesAndComments` | string | Free-text notes, observations, or commentary from the abstraction process |

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
