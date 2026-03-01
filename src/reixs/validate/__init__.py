"""REIXS validation — 5-pass validator pipeline."""

from __future__ import annotations

from reixs.schema.reixs_models import ReixsSpec
from reixs.validate.cross_field import validate_cross_field
from reixs.validate.domain import validate_domain
from reixs.validate.ofd import validate_ofd
from reixs.validate.report import Finding, ValidationReport, PassSummary
from reixs.validate.structural import validate_structural


PASS_NAMES = {
    1: "Structural",
    2: "OFD",
    3: "Domain",
    4: "SESF",
    5: "Cross-field",
}


def run_validation(spec: ReixsSpec, strict_sesf: bool = True) -> ValidationReport:
    """Run all 5 validation passes and return a report."""
    all_findings: list[Finding] = []

    # Pass 1: Structural
    all_findings.extend(validate_structural(spec))

    # Pass 2: OFD
    all_findings.extend(validate_ofd(spec))

    # Pass 3: Domain
    all_findings.extend(validate_domain(spec))

    # Pass 4: SESF (lazy import to avoid circular dependency)
    from reixs.sesf.adapter import validate_sesf_block
    sesf_findings = validate_sesf_block(spec.behavior_spec.raw_sesf)
    if not strict_sesf:
        for f in sesf_findings:
            if f.severity == "error":
                f = f.model_copy(update={"severity": "warning"})
            all_findings.append(f)
    else:
        all_findings.extend(sesf_findings)

    # Pass 5: Cross-field
    all_findings.extend(validate_cross_field(spec))

    # Build pass summaries
    summaries = {}
    for pn, name in PASS_NAMES.items():
        pf = [f for f in all_findings if f.pass_number == pn]
        summaries[pn] = PassSummary(
            pass_number=pn,
            name=name,
            errors=sum(1 for f in pf if f.severity == "error"),
            warnings=sum(1 for f in pf if f.severity == "warning"),
            infos=sum(1 for f in pf if f.severity == "info"),
        )

    return ValidationReport(
        spec_id=spec.meta.spec_id,
        spec_version=spec.meta.version,
        findings=all_findings,
        pass_summaries=summaries,
        sesf_findings=[],
    )
