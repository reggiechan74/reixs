"""Pass 5: Cross-field consistency checks."""

from __future__ import annotations

from reixs.schema.enums import Tier
from reixs.schema.reixs_models import ReixsSpec
from reixs.validate.report import Finding

PASS = 5


def validate_cross_field(spec: ReixsSpec) -> list[Finding]:
    findings: list[Finding] = []

    if spec.meta.tier == Tier.COMPLEX:
        if not spec.domain_context.adr_references:
            findings.append(Finding(
                pass_number=PASS, severity="error", section="domain_context",
                field="adr_references",
                message="Complex tier requires ADR references",
                suggestion="Add ADR References to Domain Context",
            ))

    hc_text = " ".join(spec.ofd.hard_constraints).lower()
    oc_text = spec.output_contract.description.lower()
    if "provenance" in hc_text and "provenance" not in oc_text:
        findings.append(Finding(
            pass_number=PASS, severity="warning", section="output_contract",
            field=None,
            message="OFD hard constraints mention provenance but output contract does not",
            suggestion="Ensure output contract enforces provenance requirements",
        ))

    jurisdiction = spec.domain_context.jurisdiction.lower()
    if "ontario" in jurisdiction and not spec.domain_context.currency:
        findings.append(Finding(
            pass_number=PASS, severity="warning", section="domain_context",
            field="currency",
            message="Ontario jurisdiction should declare currency (CAD)",
            suggestion="Add 'Currency: CAD' to Domain Context",
        ))

    return findings
