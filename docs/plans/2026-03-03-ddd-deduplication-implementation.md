# DDD Deduplication v2.0.0 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Eliminate 48 exact-name field duplicates and 19 semantic duplicate groups across 7 DDDs by expanding core and adding pointer-row cross-references.

**Architecture:** Core-first, top-down. Build complete `core@2.0.0` with 4 new sections (marketContext, occupancyAndVacancy, revenueAndExpenseLineItems, zoningAndEnvironmental) and restructured parties (Option A dot notation). Then update each domain DDD to v2.0.0 replacing duplicates with pointer rows. Finally update registry and tests.

**Tech Stack:** Markdown DDDs, Python registry (`ddd_refs.py`), pytest

**Design doc:** `docs/plans/2026-03-03-ddd-deduplication-design.md`

---

### Task 1: Write failing test for v2.0.0 registry

**Files:**
- Modify: `tests/test_ddd_refs.py`

**Step 1: Write the failing test**

Add a new test class at the end of the file (before the closing line) that asserts v2.0.0 refs exist:

```python
class TestV2DDDRefs:
    """Tests for v2.0.0 DDD references after deduplication migration."""

    @pytest.mark.parametrize("ref", [
        "re-ddd:core_commercial_re_na@2.0.0",
        "re-ddd:lease_abstraction_commercial_na@2.0.0",
        "re-ddd:property_management_commercial_na@2.0.0",
        "re-ddd:asset_management_commercial_na@2.0.0",
        "re-ddd:leasing_commercial_na@2.0.0",
        "re-ddd:appraisal_commercial_na@2.0.0",
        "re-ddd:investment_commercial_na@2.0.0",
    ])
    def test_v2_refs_are_known(self, ref):
        assert is_known_ddd_ref(ref)

    def test_v2_refs_are_valid_format(self):
        assert is_valid_ddd_format("re-ddd:core_commercial_re_na@2.0.0")

    def test_old_v1_refs_removed(self):
        """v1 refs should no longer be in registry after migration."""
        assert not is_known_ddd_ref("re-ddd:core_commercial_re_na@1.0.0")
        assert not is_known_ddd_ref("re-ddd:lease_abstraction_commercial_na@1.0.0")
        assert not is_known_ddd_ref("re-ddd:lease_abstraction_commercial_na@1.1.0")
        assert not is_known_ddd_ref("re-ddd:investment_commercial_na@1.0.0")

    def test_registry_count_after_migration(self):
        """Still 8 DDDs (same count — versions changed, not added/removed)."""
        from reixs.registry.ddd_refs import KNOWN_DDD_REFS
        assert len(KNOWN_DDD_REFS) == 8
```

Also update the existing `TestDDDRefFormat.test_valid_ddd_format` parametrize list to include a v2 example:

```python
"re-ddd:core_commercial_re_na@2.0.0",
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_ddd_refs.py::TestV2DDDRefs -v`
Expected: FAIL — v2 refs not in registry yet

**Step 3: Commit failing test**

```bash
git add tests/test_ddd_refs.py
git commit -m "test: add failing tests for DDD v2.0.0 registry migration"
```

---

### Task 2: Create core v2.0.0 — copy and restructure

**Files:**
- Create: `docs/ddd/core_commercial_re_na_v2_0.md`
- Reference: `docs/ddd/core_commercial_re_na_v1_0.md` (read only, do not modify)
- Reference: `docs/plans/2026-03-03-ddd-deduplication-design.md` (read for design decisions)

**Step 1: Create core v2.0.0**

Copy the structure from `core_commercial_re_na_v1_0.md` and apply these changes:

1. **Line 3**: Change reference to `re-ddd:core_commercial_re_na@2.0.0`
2. **Line 5**: Update scope to mention new sections
3. **Line 13**: Update field count: "The schema defines **12 sections** with **113 fields** total."
4. **Section 2 (financialFundamentals)**: Update `effectiveGrossIncome` description to USPAP standard: "Potential gross income minus vacancy and credit loss plus other income"
5. **Section 4 (parties)**: Restructure to role-qualified dot notation:

```markdown
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
```

6. **Add Section 9: marketContext** — All 22 fields from design doc (MSA/submarket, demographics, employment, supply, demand, rental trends, construction, forecasts). Copy field names and descriptions exactly from `investment_commercial_na_v1_0.md` lines 148-178 (section 6: marketStudy) since those are the canonical definitions.

7. **Add Section 10: occupancyAndVacancy**:

```markdown
### 10. occupancyAndVacancy

Occupancy and vacancy metrics used across appraisal, asset management, and property management.

| Field | Type | Description |
|---|---|---|
| `occupancyRatePhysical` | number | Physically occupied space / total rentable space (expressed as decimal) |
| `occupancyRateEconomic` | number | Actual revenue / potential gross revenue at full occupancy (expressed as decimal) |
| `occupancyStabilized` | number | Expected occupancy at stabilization (expressed as decimal) |
| `vacancyRatePercent` | number | Vacant space / total rentable space (expressed as decimal) |
| `vacancyAndCreditLossPercent` | number | Combined vacancy and credit loss as percentage of potential gross income (expressed as decimal) |
```

8. **Add Section 11: revenueAndExpenseLineItems**:

```markdown
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
```

9. **Add Section 12: zoningAndEnvironmental**:

```markdown
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
```

**Step 2: Verify the file is well-formed**

Manually check: 12 section headers, ~113 fields total, reference string is `@2.0.0`.

**Step 3: Commit**

```bash
git add docs/ddd/core_commercial_re_na_v2_0.md
git commit -m "feat: create core DDD v2.0.0 with 4 new shared sections and parties restructure"
```

---

### Task 3: Update investment DDD to v2.0.0

**Files:**
- Create: `docs/ddd/investment_commercial_na_v2_0.md`
- Reference: `docs/ddd/investment_commercial_na_v1_0.md` (lines 1-233)
- Reference: `docs/ddd/core_commercial_re_na_v2_0.md`

**Step 1: Create investment v2.0.0**

Copy from v1.0 and apply these changes:

1. **Line 3**: Reference → `re-ddd:investment_commercial_na@2.0.0`
2. **Line 7**: Update relationship text to reference `core@2.0.0`
3. **Section 6 (marketStudy, lines 146-178)**: Replace the entire field table with a section-level pointer:

```markdown
### 6. marketStudy

> **Shared fields:** Uses `re-ddd:core_commercial_re_na@2.0.0 → marketContext` for all market study fields (MSA, demographics, employment, supply, demand, rental trends, construction pipeline, forecasts).

This section contains no domain-specific fields beyond core. Reference the core marketContext section for the complete field list.
```

4. **Section 5 (dueDiligence)**: Replace duplicated zoning fields with pointer rows:
   - `zoningCurrent` → `| \`zoningClassification\` | string | → \`core@2.0.0 → propertyIdentification.zoningClassification\` |`
   - `zoningConformance` → `| \`zoningConformance\` | string | → \`core@2.0.0 → zoningAndEnvironmental.zoningConformance\` |`
   - `zoningVarianceRequired` → `| \`varianceRequired\` | boolean | → \`core@2.0.0 → zoningAndEnvironmental.varianceRequired\` |`

5. **Section 7 (dispositionAnalysis)**: Fix intra-file duplicates:
   - `exitCapRate` → `| \`exitCapRate\` | number | → \`core@2.0.0 → capRate\` — at disposition. See also underwriting §4. |`
   - `dispositionCostsPercent` → `| \`dispositionCostsPercent\` | number | → underwriting §4 for canonical definition |`

6. **Section 4 (underwriting)**: Add core capRate back-references to existing fields:
   - `exitCapRate` description: append " → `core@2.0.0 → capRate` — at disposition"
   - `terminalCapRate` description: append " → `core@2.0.0 → capRate` — terminal year of DCF"

7. **Section 1 (acquisitionSummary)**: `goingInCapRate` description: append " → `core@2.0.0 → capRate` — at acquisition"

8. Update section count in header to reflect that marketStudy is now a pointer section (still 7 sections, fewer total fields — update field count accordingly).

**Step 2: Verify pointer rows reference correct core sections**

Grep the new file for `core@2.0.0` — should have references to: `marketContext`, `propertyIdentification.zoningClassification`, `zoningAndEnvironmental`, `capRate`.

**Step 3: Commit**

```bash
git add docs/ddd/investment_commercial_na_v2_0.md
git commit -m "feat: create investment DDD v2.0.0 with core cross-references"
```

---

### Task 4: Update appraisal DDD to v2.0.0

**Files:**
- Create: `docs/ddd/appraisal_commercial_na_v2_0.md`
- Reference: `docs/ddd/appraisal_commercial_na_v1_0.md` (lines 1-413)
- Reference: `docs/ddd/core_commercial_re_na_v2_0.md`

**Step 1: Create appraisal v2.0.0**

Copy from v1.0 and apply these changes:

1. **Line 3**: Reference → `re-ddd:appraisal_commercial_na@2.0.0`
2. **Line 7**: Update relationship text to reference `core@2.0.0`
3. **Section 6 (marketAnalysis, lines 166-199)**: Replace entire field table with section-level pointer (same pattern as investment):

```markdown
### 6. marketAnalysis

> **Shared fields:** Uses `re-ddd:core_commercial_re_na@2.0.0 → marketContext` for all market analysis fields.

This section contains no domain-specific fields beyond core. Reference the core marketContext section for the complete field list.
```

4. **Section 5 (zoning, lines 143-164)**: Replace duplicated fields with pointers:
   - `zoningClassification` → pointer to `core@2.0.0 → propertyIdentification.zoningClassification`
   - `zoningConformance` → pointer to `core@2.0.0 → zoningAndEnvironmental.zoningConformance`
   - `varianceRequired` → pointer to `core@2.0.0 → zoningAndEnvironmental.varianceRequired`
   - Keep appraisal-specific fields: `zoningDescription`, `permittedUses`, `conditionalUses`, `setbacks`, `parkingRequirements`, `overlayDistricts`

5. **Section 2 (propertyDescription)**: Replace area fields with pointers:
   - `buildingAreaGBA` → `| \`grossBuildingArea\` | number | → \`core@2.0.0 → areaAndMeasurement.grossBuildingArea\` |`
   - `buildingAreaRentable` → `| \`rentableArea\` | number | → \`core@2.0.0 → areaAndMeasurement.rentableArea\` |`
   - `buildingAreaUsable` → `| \`usableArea\` | number | → \`core@2.0.0 → areaAndMeasurement.usableArea\` |`

6. **Section 8 (incomeCapitalizationApproach)**: Replace duplicated fields:
   - `effectiveGrossIncome` → pointer to `core@2.0.0 → financialFundamentals.effectiveGrossIncome`
   - `netOperatingIncome` → `| \`noi\` | number | → \`core@2.0.0 → financialFundamentals.noi\` |`
   - `expenseUtilities` → pointer to `core@2.0.0 → revenueAndExpenseLineItems.expenseUtilities`
   - `expenseRepairsMaintenance` → pointer to `core@2.0.0 → revenueAndExpenseLineItems.expenseRepairsMaintenance`
   - `expenseInsurance` → pointer to `core@2.0.0 → revenueAndExpenseLineItems.expenseInsurance`
   - `operatingExpenseRatio` → pointer to `core@2.0.0 → revenueAndExpenseLineItems.operatingExpenseRatio`
   - `concludedMarketRentPerSF` → pointer to `core@2.0.0 → revenueAndExpenseLineItems.marketRentPerSF` (appraisal-concluded context)
   - Keep appraisal-specific fields: `potentialGrossIncome`, `capRateSelected`, `capRateSource`, `directCapitalizationValue`, rent comparable fields, DCF projection fields

7. **Section 4 (taxAndAssessment)**: `assessmentYear` → pointer to `core@2.0.0 → revenueAndExpenseLineItems.assessmentYear`

8. Update field count in header.

**Step 2: Verify all pointer rows**

Grep for `core@2.0.0` — should have references to: `marketContext`, `propertyIdentification`, `zoningAndEnvironmental`, `areaAndMeasurement`, `financialFundamentals`, `revenueAndExpenseLineItems`.

**Step 3: Commit**

```bash
git add docs/ddd/appraisal_commercial_na_v2_0.md
git commit -m "feat: create appraisal DDD v2.0.0 with core cross-references"
```

---

### Task 5: Update asset management DDD to v2.0.0

**Files:**
- Create: `docs/ddd/asset_management_commercial_na_v2_0.md`
- Reference: `docs/ddd/asset_management_commercial_na_v1_0.md` (lines 1-287)
- Reference: `docs/ddd/core_commercial_re_na_v2_0.md`

**Step 1: Create asset management v2.0.0**

Copy from v1.0 and apply:

1. **Line 3**: Reference → `re-ddd:asset_management_commercial_na@2.0.0`
2. **Section 2 (financialPerformance, lines 40-66)**: Replace duplicated revenue fields with pointers:
   - `revenueBaseRent` → pointer to `core@2.0.0 → revenueAndExpenseLineItems.revenueBaseRent`
   - `revenueRecoveries` → pointer to `core@2.0.0 → revenueAndExpenseLineItems.revenueRecoveries`
   - `revenueParking` → pointer to `core@2.0.0 → revenueAndExpenseLineItems.revenueParking`
   - `revenueOther` → pointer to `core@2.0.0 → revenueAndExpenseLineItems.revenueOther`
   - Keep asset-mgmt-specific fields: `noiActual`, `noiBudget`, `noiPriorYear`, `budgetVariancePercent`, etc.

3. **Section 3 (valuationMetrics, lines 68-89)**:
   - `goingInCapRate` → `| \`goingInCapRate\` | number | → \`core@2.0.0 → capRate\` — at acquisition |`
   - `exitCapRate` → `| \`exitCapRate\` | number | → \`core@2.0.0 → capRate\` — at disposition |`
   - `markToMarketPercent` → **rename** to `markToMarketValuePercent` with description: "Percentage change from book value to current market value (expressed as decimal)"
   - `assessmentYear` → pointer to `core@2.0.0 → revenueAndExpenseLineItems.assessmentYear`

4. **Section 1 (assetProfile, lines 15-38)**:
   - `acquisitionDate` → pointer to `core@2.0.0 → revenueAndExpenseLineItems.acquisitionDate`

5. **Section 8 (riskAssessment, lines 184-207)**:
   - `environmentalRiskFloodZone` → `| \`floodZoneDesignation\` | string | → \`core@2.0.0 → zoningAndEnvironmental.floodZoneDesignation\` |`

6. **Section 10 (budgetAndForecasting, lines 230-258)**:
   - `scenarioBaseCaseIRR` → `| \`scenarioBaseCaseIRR\` | number | → \`investment@2.0.0 → underwriting.scenarioBaseCaseIRR\` |`
   - `scenarioUpsideIRR` → `| \`scenarioUpsideIRR\` | number | → \`investment@2.0.0 → underwriting.scenarioUpsideIRR\` |`
   - `scenarioDownsideIRR` → `| \`scenarioDownsideIRR\` | number | → \`investment@2.0.0 → underwriting.scenarioDownsideIRR\` |`

7. Update field count in header.

**Step 2: Verify**

Grep for `core@2.0.0` and `investment@2.0.0`. Verify `markToMarketPercent` no longer exists (renamed to `markToMarketValuePercent`).

**Step 3: Commit**

```bash
git add docs/ddd/asset_management_commercial_na_v2_0.md
git commit -m "feat: create asset management DDD v2.0.0 with core cross-references"
```

---

### Task 6: Update property management DDD to v2.0.0

**Files:**
- Create: `docs/ddd/property_management_commercial_na_v2_0.md`
- Reference: `docs/ddd/property_management_commercial_na_v1_0.md` (lines 1-290)
- Reference: `docs/ddd/core_commercial_re_na_v2_0.md`

**Step 1: Create property management v2.0.0**

Copy from v1.0 and apply:

1. **Line 3**: Reference → `re-ddd:property_management_commercial_na@2.0.0`
2. **Section 1 (tenantManagement, lines 15-38)**: Replace party fields with pointers:
   - `tenantName` → `| \`party.tenant.name\` | string | → \`core@2.0.0 → parties\` with role=tenant |`
   - `contactName` → `| \`party.tenant.contactName\` | string | → \`core@2.0.0 → parties\` with role=tenant |`
   - `contactPhone` → `| \`party.tenant.contactPhone\` | string | → \`core@2.0.0 → parties\` with role=tenant |`
   - `contactEmail` → `| \`party.tenant.contactEmail\` | string | → \`core@2.0.0 → parties\` with role=tenant |`
   - Keep PM-specific fields: `leaseId`, `moveInDate`, `moveOutDate`, `tenantType`, etc.

3. **Section 2 (rentRoll, lines 40-68)**:
   - `tenantName` → `| \`party.tenant.name\` | string | → \`core@2.0.0 → parties\` with role=tenant |`
   - `freeRentMonths` → pointer to `core@2.0.0 → revenueAndExpenseLineItems.freeRentMonths`
   - `tiAllowance` → `| \`tiAllowancePerSF\` | number | → \`core@2.0.0 → revenueAndExpenseLineItems.tiAllowancePerSF\` |`
   - `rentableSF` → `| \`rentableArea\` | number | → \`core@2.0.0 → areaAndMeasurement.rentableArea\` |`
   - `usableSF` → `| \`usableArea\` | number | → \`core@2.0.0 → areaAndMeasurement.usableArea\` |`
   - `markToMarketPercent` — **keep as-is** (rent-based meaning is correct in PM context)

4. **Section 3 (operatingBudget, lines 70-100)**: Replace revenue/expense fields with pointers:
   - `revenueBaseRent` → pointer to `core@2.0.0 → revenueAndExpenseLineItems.revenueBaseRent`
   - `revenueRecoveries` → pointer to `core@2.0.0 → revenueAndExpenseLineItems.revenueRecoveries`
   - `revenueParking` → pointer to `core@2.0.0 → revenueAndExpenseLineItems.revenueParking`
   - `revenueOther` → pointer to `core@2.0.0 → revenueAndExpenseLineItems.revenueOther`
   - `expenseUtilities` → pointer to `core@2.0.0 → revenueAndExpenseLineItems.expenseUtilities`
   - `expenseRepairsMaintenance` → pointer to `core@2.0.0 → revenueAndExpenseLineItems.expenseRepairsMaintenance`
   - `expenseInsurance` → pointer to `core@2.0.0 → revenueAndExpenseLineItems.expenseInsurance`
   - Keep PM-specific budget fields: `budgetTotalRevenue`, `budgetTotalExpense`, `varianceActualVsBudget`, etc.

5. **Section 10 (reportingMetrics, lines 236-261)**:
   - `operatingExpenseRatio` → pointer to `core@2.0.0 → revenueAndExpenseLineItems.operatingExpenseRatio`
   - Add note: "PM convention: denominator is effective gross income per core standard"

6. Update field count in header.

**Step 2: Verify**

Grep for `core@2.0.0` and `party.tenant`. Verify `contactName` as flat field no longer exists (replaced by `party.tenant.contactName`).

**Step 3: Commit**

```bash
git add docs/ddd/property_management_commercial_na_v2_0.md
git commit -m "feat: create property management DDD v2.0.0 with core cross-references"
```

---

### Task 7: Update leasing DDD to v2.0.0

**Files:**
- Create: `docs/ddd/leasing_commercial_na_v2_0.md`
- Reference: `docs/ddd/leasing_commercial_na_v1_0.md` (lines 1-305)
- Reference: `docs/ddd/core_commercial_re_na_v2_0.md`

**Step 1: Create leasing v2.0.0**

Copy from v1.0 and apply:

1. **Line 3**: Reference → `re-ddd:leasing_commercial_na@2.0.0`
2. **Section 3 (tenantScreening, lines 70-97)**:
   - `prospectName` → `| \`party.prospect.name\` | string | → \`core@2.0.0 → parties\` with role=prospect |`
   - Keep leasing-specific screening fields: `prospectIndustry`, `spaceRequirementSF`, `creditRating`, etc.

3. **Section 7 (spacePlanning, lines 180-203)**:
   - `efficiencyRatio` → `| \`efficiencyRatio\` | number | → \`core@2.0.0 → areaAndMeasurement.efficiencyRatio\` |` (replace the inline "See also" note with proper pointer row)

4. **Section 10 (marketRentOpinion, lines 250-276)**:
   - `concludedMarketRentPerSF` → `| \`marketRentPerSF\` | number | → \`core@2.0.0 → revenueAndExpenseLineItems.marketRentPerSF\` — leasing-concluded context |`

5. **Section 4 (dealStructuring, lines 99-131)**:
   - `tiAllowancePerSF` — already correctly named; add pointer: `→ core@2.0.0 → revenueAndExpenseLineItems.tiAllowancePerSF`
   - `freeRentMonths` — add pointer: `→ core@2.0.0 → revenueAndExpenseLineItems.freeRentMonths`

6. **Section 1 (marketAnalysis)**: These are leasing-specific submarket fields (different scope than the macro market context in core). Keep as-is but add a note:

```markdown
> **Note:** For macro-level MSA and demographic data, see `re-ddd:core_commercial_re_na@2.0.0 → marketContext`. This section covers submarket-level competitive intelligence specific to leasing.
```

7. Update field count in header.

**Step 2: Verify**

Grep for `core@2.0.0` and `party.prospect`. Verify `efficiencyRatio` uses pointer row syntax (not inline "See also").

**Step 3: Commit**

```bash
git add docs/ddd/leasing_commercial_na_v2_0.md
git commit -m "feat: create leasing DDD v2.0.0 with core cross-references"
```

---

### Task 8: Update lease abstraction DDD to v2.0.0

**Files:**
- Create: `docs/ddd/lease_abstraction_commercial_na_v2_0.md`
- Reference: `docs/ddd/lease_abstraction_commercial_na_v1_1.md` (lines 1-640)
- Reference: `docs/ddd/core_commercial_re_na_v2_0.md`

**Step 1: Create lease abstraction v2.0.0**

Copy from v1.1 and apply:

1. **Line 3**: Reference → `re-ddd:lease_abstraction_commercial_na@2.0.0`
2. **Section 1 (documentInformation, lines 15-26)**:
   - `leaseType` → `| \`leaseType\` | string | → \`core@2.0.0 → leaseClassifications.leaseType\` |`

3. **Section 2 (parties, lines 28-49)**: Replace all party fields with pointer rows:
   - `landlord.name` → `| \`party.landlord.name\` | string | → \`core@2.0.0 → parties\` with role=landlord |`
   - `landlord.address` → `| \`party.landlord.address\` | string | → \`core@2.0.0 → parties\` with role=landlord |`
   - `landlord.entityType` → `| \`party.landlord.entityType\` | string | → \`core@2.0.0 → parties\` with role=landlord |`
   - `tenant.name` → `| \`party.tenant.name\` | string | → \`core@2.0.0 → parties\` with role=tenant |`
   - `tenant.address` → `| \`party.tenant.address\` | string | → \`core@2.0.0 → parties\` with role=tenant |`
   - `tenant.entityType` → `| \`party.tenant.entityType\` | string | → \`core@2.0.0 → parties\` with role=tenant |`
   - `tenant.contact` → `| \`party.tenant.contactName\` | string | → \`core@2.0.0 → parties\` with role=tenant |`
   - Keep lease-abstraction-specific fields: `guarantor.*`, `additionalParties`

4. **Section 3 (premises, lines 51-72)**:
   - `area.rentableAreaSqFt` → `| \`rentableArea\` | number | → \`core@2.0.0 → areaAndMeasurement.rentableArea\` |`
   - `area.measurementStandard` → `| \`measurementStandard\` | string | → \`core@2.0.0 → areaAndMeasurement.measurementStandard\` |`
   - Keep lease-specific: `suiteNumber`, `floor`, `area.usableAreaSqFt`, `area.parkingSpaces`

5. **Section 5 (rent, lines 108-151)**:
   - `paymentTerms.currency` → `| \`currency\` | string | → \`core@2.0.0 → currencyAndUnits.currency\` |`

6. **Section 7 (operatingCostsAndTaxes, lines 178-201)**:
   - `netLeaseProvisions.leaseType` → `| \`leaseType\` | string | → \`core@2.0.0 → leaseClassifications.leaseType\` (duplicate removed — see documentInformation) |`

7. Update field count in header.

**Step 2: Verify**

Grep for `core@2.0.0`, `party.landlord`, and `party.tenant`. Verify no flat `landlord.name` or `tenant.name` fields remain.

**Step 3: Commit**

```bash
git add docs/ddd/lease_abstraction_commercial_na_v2_0.md
git commit -m "feat: create lease abstraction DDD v2.0.0 with core cross-references"
```

---

### Task 9: Update registry and tests to v2.0.0

**Files:**
- Modify: `src/reixs/registry/ddd_refs.py`
- Modify: `tests/test_ddd_refs.py`

**Step 1: Update registry**

Replace the `KNOWN_DDD_REFS` set in `ddd_refs.py` (lines 7-16):

```python
KNOWN_DDD_REFS = {
    "re-ddd:lease_core_terms_ontario@0.1.0",
    "re-ddd:lease_abstraction_commercial_na@2.0.0",
    "re-ddd:core_commercial_re_na@2.0.0",
    "re-ddd:property_management_commercial_na@2.0.0",
    "re-ddd:asset_management_commercial_na@2.0.0",
    "re-ddd:leasing_commercial_na@2.0.0",
    "re-ddd:appraisal_commercial_na@2.0.0",
    "re-ddd:investment_commercial_na@2.0.0",
}
```

**Step 2: Update existing tests**

In `tests/test_ddd_refs.py`, update the `TestDDDRefFormat.test_valid_ddd_format` parametrize list (lines 9-18) to use v2.0.0 versions:

```python
@pytest.mark.parametrize("ref", [
    "re-ddd:lease_core_terms_ontario@0.1.0",
    "re-ddd:lease_abstraction_commercial_na@2.0.0",
    "re-ddd:core_commercial_re_na@2.0.0",
    "re-ddd:property_management_commercial_na@2.0.0",
    "re-ddd:asset_management_commercial_na@2.0.0",
    "re-ddd:leasing_commercial_na@2.0.0",
    "re-ddd:appraisal_commercial_na@2.0.0",
    "re-ddd:investment_commercial_na@2.0.0",
])
```

Update the `TestKnownDDDRefs.test_known_ddd_refs` parametrize list (lines 35-44) similarly.

Remove the `TestV2DDDRefs` class added in Task 1 — its assertions are now covered by the updated existing tests. Or keep it as a migration-specific regression test. Either way, all v1.0.0 refs in the test assertions must be changed to v2.0.0.

**Step 3: Run all tests**

Run: `pytest tests/test_ddd_refs.py -v`
Expected: ALL PASS

**Step 4: Commit**

```bash
git add src/reixs/registry/ddd_refs.py tests/test_ddd_refs.py
git commit -m "feat: migrate DDD registry and tests to v2.0.0"
```

---

### Task 10: Update spec template reference and clean up old files

**Files:**
- Modify: `specs/templates/lease_abstraction_commercial_na.reixs.md` (line 20, line 276)
- Delete: `docs/ddd/core_commercial_re_na_v1_0.md`
- Delete: `docs/ddd/investment_commercial_na_v1_0.md` (already deleted per git status, confirm)
- Delete: `docs/ddd/appraisal_commercial_na_v1_0.md`
- Delete: `docs/ddd/asset_management_commercial_na_v1_0.md`
- Delete: `docs/ddd/property_management_commercial_na_v1_0.md`
- Delete: `docs/ddd/leasing_commercial_na_v1_0.md`
- Delete: `docs/ddd/lease_abstraction_commercial_na_v1_1.md`
- Delete: `docs/ddd/investment_appraisal_commercial_na_v1_0.md` (already deleted per git status)
- Delete: `docs/ddd/lease_abstraction_commercial_na_v1_0.md` (already deleted per git status)

**Step 1: Update spec template**

In `specs/templates/lease_abstraction_commercial_na.reixs.md`:
- Line 20: Change `re-ddd:lease_abstraction_commercial_na@1.0.0` → `re-ddd:lease_abstraction_commercial_na@2.0.0`
- Line 276 (or wherever the second reference is): Same change

**Step 2: Delete old v1 DDD files**

```bash
git rm docs/ddd/core_commercial_re_na_v1_0.md
git rm docs/ddd/asset_management_commercial_na_v1_0.md
git rm docs/ddd/property_management_commercial_na_v1_0.md
git rm docs/ddd/leasing_commercial_na_v1_0.md
git rm docs/ddd/lease_abstraction_commercial_na_v1_1.md
```

Note: `investment_appraisal_commercial_na_v1_0.md` and `lease_abstraction_commercial_na_v1_0.md` are already deleted per git status. `investment_commercial_na_v1_0.md` and `appraisal_commercial_na_v1_0.md` may also already be deleted — check git status first and only `git rm` files that still exist.

**Step 3: Run full test suite**

Run: `pytest -v`
Expected: ALL PASS

**Step 4: Commit**

```bash
git add -A specs/templates/lease_abstraction_commercial_na.reixs.md
git commit -m "chore: remove v1 DDD files and update spec template to v2.0.0"
```

---

### Task 11: Final validation — cross-reference audit

**Files:**
- Read: All v2.0.0 DDD files in `docs/ddd/`

**Step 1: Run cross-reference validation**

Grep all v2.0.0 DDD files for pointer rows (`→ \`core@2.0.0`) and verify each referenced section and field actually exists in `core_commercial_re_na_v2_0.md`.

```bash
grep -n "core@2.0.0" docs/ddd/*_v2_0.md
```

For each match, confirm the target section (`parties`, `marketContext`, `areaAndMeasurement`, etc.) and field exist in core v2.0.0.

**Step 2: Verify no remaining v1 references**

```bash
grep -rn "@1.0.0\|@1.1.0" docs/ddd/*_v2_0.md
```

Expected: No matches (all v2.0.0 files should only reference `@2.0.0`).

**Step 3: Verify no duplicate field names across domain DDDs**

For the previously duplicated fields (`revenueBaseRent`, `msaName`, `exitCapRate`, etc.), grep across domain v2.0.0 files to confirm they either:
- Appear as pointer rows (not standalone definitions), OR
- Appear in exactly one domain DDD as the canonical owner

**Step 4: Run full test suite one final time**

Run: `pytest -v`
Expected: ALL PASS

**Step 5: Final commit if any fixes needed**

```bash
git add -A
git commit -m "fix: resolve cross-reference audit findings in v2.0.0 DDDs"
```

(Only if step 1-3 revealed issues that needed fixing.)
