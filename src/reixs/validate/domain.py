"""Pass 3: Domain validation."""

from __future__ import annotations

from reixs.schema.enums import Tier
from reixs.schema.reixs_models import ReixsSpec
from reixs.registry.task_types import is_known_task_type
from reixs.registry.ddd_refs import is_valid_ddd_format, is_known_ddd_ref
from reixs.validate.report import Finding

PASS = 3


def validate_domain(spec: ReixsSpec) -> list[Finding]:
    findings: list[Finding] = []

    if not is_known_task_type(spec.meta.task_type):
        findings.append(Finding(
            pass_number=PASS, severity="warning", section="meta",
            field="task_type",
            message=f"Task type '{spec.meta.task_type}' not in known registry",
            suggestion="Known types: Lease Abstraction",
        ))

    if not spec.domain_context.jurisdiction:
        findings.append(Finding(
            pass_number=PASS, severity="error", section="domain_context",
            field="jurisdiction", message="Jurisdiction not declared",
            suggestion="Add jurisdiction (e.g., Ontario, Canada)",
        ))

    ddd = spec.domain_context.ddd_reference
    if not ddd:
        findings.append(Finding(
            pass_number=PASS, severity="error", section="domain_context",
            field="ddd_reference", message="DDD Reference is missing",
            suggestion="Add DDD ref (format: re-ddd:<name>@<semver>)",
        ))
    elif not is_valid_ddd_format(ddd):
        findings.append(Finding(
            pass_number=PASS, severity="error", section="domain_context",
            field="ddd_reference",
            message=f"DDD Reference '{ddd}' has invalid format",
            suggestion="Use format: re-ddd:<name>@X.Y.Z",
        ))
    elif not is_known_ddd_ref(ddd):
        findings.append(Finding(
            pass_number=PASS, severity="warning", section="domain_context",
            field="ddd_reference",
            message=f"DDD Reference '{ddd}' not found in local registry",
            suggestion="Verify the DDD reference exists",
        ))

    oc_text = spec.output_contract.description.lower()
    if "provenance" not in oc_text and "status" not in oc_text:
        findings.append(Finding(
            pass_number=PASS, severity="warning", section="output_contract",
            field=None,
            message="Output contract does not mention provenance or status fields",
            suggestion="Include provenance and fact/inference status in output contract",
        ))

    if spec.meta.tier in (Tier.STANDARD, Tier.COMPLEX):
        if not spec.evaluation.edd_suite_id:
            findings.append(Finding(
                pass_number=PASS, severity="error", section="evaluation",
                field="edd_suite_id",
                message="EDD Suite ID required for standard/complex tier",
                suggestion="Add an EDD Suite ID referencing test cases",
            ))

    return findings
