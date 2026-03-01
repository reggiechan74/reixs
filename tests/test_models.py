"""Tests for REIXS data models."""

import pytest
from datetime import date
from pydantic import ValidationError

from reixs.schema.enums import Tier, FieldStatus
from reixs.schema.reixs_models import (
    MetaSection,
    OFDSection,
    DomainContextSection,
    InputsSection,
    ConstraintsSection,
    OutputContractSection,
    EvaluationSection,
    BehaviorSpecSection,
    ReixsSpec,
)
from reixs.schema.runtime_payload import RuntimePayload, Manifest
from reixs.validate.report import Finding, ValidationReport


class TestEnums:
    def test_tier_values(self):
        assert Tier.MICRO == "micro"
        assert Tier.STANDARD == "standard"
        assert Tier.COMPLEX == "complex"

    def test_field_status_values(self):
        assert FieldStatus.FACT == "fact"
        assert FieldStatus.INFERENCE == "inference"
        assert FieldStatus.MISSING == "missing"
        assert FieldStatus.CONFLICT == "conflict"


class TestMetaSection:
    def test_valid_meta(self):
        meta = MetaSection(
            spec_id="REIXS-LA-ON-001",
            version="1.0.0",
            task_type="Lease Abstraction",
            tier=Tier.STANDARD,
            author="Reggie Chan",
            date=date(2026, 3, 1),
        )
        assert meta.spec_id == "REIXS-LA-ON-001"
        assert meta.tier == Tier.STANDARD

    def test_invalid_tier_rejected(self):
        with pytest.raises(ValidationError):
            MetaSection(
                spec_id="X",
                version="1.0.0",
                task_type="X",
                tier="invalid",
                author="X",
                date=date(2026, 1, 1),
            )


class TestOFDSection:
    def test_required_fields_only(self):
        ofd = OFDSection(
            primary_objective="Extract lease terms",
            hard_constraints=["No fabrication"],
            autofail_conditions=["Fabricated term"],
            optimization_priority_order=["Factual correctness"],
            uncertainty_policy="Mark as INFERENCE",
        )
        assert ofd.secondary_objectives is None
        assert ofd.scoring_model is None

    def test_all_fields(self):
        ofd = OFDSection(
            primary_objective="Extract lease terms",
            hard_constraints=["No fabrication"],
            autofail_conditions=["Fabricated term"],
            optimization_priority_order=["Factual correctness"],
            uncertainty_policy="Mark as INFERENCE",
            secondary_objectives=["Find renewals"],
            tradeoff_policies=["Prefer MISSING over GUESS"],
            scoring_model="Weighted F1",
            escalation_triggers=["Low confidence"],
            error_severity_model={"critical": ["fabricated term"]},
        )
        assert ofd.secondary_objectives == ["Find renewals"]

    def test_empty_hard_constraints_accepted_by_pydantic(self):
        ofd = OFDSection(
            primary_objective="X",
            hard_constraints=[],
            autofail_conditions=["X"],
            optimization_priority_order=["X"],
            uncertainty_policy="X",
        )
        assert ofd.hard_constraints == []


class TestFinding:
    def test_finding_creation(self):
        f = Finding(
            pass_number=1,
            severity="error",
            section="meta",
            field="version",
            message="Version format invalid",
            suggestion="Use semver format: X.Y.Z",
        )
        assert f.severity == "error"
        assert f.pass_number == 1

    def test_finding_minimal(self):
        f = Finding(
            pass_number=2,
            severity="warning",
            section=None,
            field=None,
            message="OFD scoring model missing",
            suggestion=None,
        )
        assert f.section is None


class TestValidationReport:
    def test_status_derived_from_findings(self):
        report = ValidationReport(
            spec_id="TEST-001",
            spec_version="1.0.0",
            findings=[
                Finding(pass_number=1, severity="info", section="meta",
                        field=None, message="OK", suggestion=None),
            ],
            pass_summaries={},
            sesf_findings=[],
        )
        assert report.status == "pass"

    def test_status_fail_on_error(self):
        report = ValidationReport(
            spec_id="TEST-001",
            spec_version="1.0.0",
            findings=[
                Finding(pass_number=1, severity="error", section="meta",
                        field=None, message="Missing", suggestion=None),
            ],
            pass_summaries={},
            sesf_findings=[],
        )
        assert report.status == "fail"

    def test_status_warn_on_warnings_only(self):
        report = ValidationReport(
            spec_id="TEST-001",
            spec_version="1.0.0",
            findings=[
                Finding(pass_number=1, severity="warning", section="ofd",
                        field=None, message="Missing scoring", suggestion=None),
            ],
            pass_summaries={},
            sesf_findings=[],
        )
        assert report.status == "warn"
