"""Pass 2: OFD validation."""

from __future__ import annotations

from reixs.schema.enums import Tier
from reixs.schema.reixs_models import ReixsSpec
from reixs.validate.report import Finding

PASS = 2


def validate_ofd(spec: ReixsSpec) -> list[Finding]:
    findings: list[Finding] = []
    ofd = spec.ofd
    tier = spec.meta.tier

    if not ofd.primary_objective:
        findings.append(Finding(
            pass_number=PASS, severity="error", section="ofd",
            field="primary_objective", message="Primary Objective is missing",
            suggestion="Define the primary goal of this spec",
        ))

    if not ofd.hard_constraints:
        findings.append(Finding(
            pass_number=PASS, severity="error", section="ofd",
            field="hard_constraints", message="Hard Constraints list is empty",
            suggestion="Add at least one hard constraint",
        ))

    if not ofd.autofail_conditions:
        findings.append(Finding(
            pass_number=PASS, severity="error", section="ofd",
            field="autofail_conditions", message="AutoFail Conditions list is empty",
            suggestion="Define conditions that should cause automatic failure",
        ))

    if not ofd.optimization_priority_order:
        findings.append(Finding(
            pass_number=PASS, severity="error", section="ofd",
            field="optimization_priority_order",
            message="Optimization Priority Order is empty",
            suggestion="List priorities in order (e.g., factual correctness first)",
        ))

    if not ofd.uncertainty_policy:
        findings.append(Finding(
            pass_number=PASS, severity="error", section="ofd",
            field="uncertainty_policy", message="Uncertainty Policy is missing",
            suggestion="Define how to handle ambiguous or uncertain values",
        ))

    # Heuristic: priority order should mention accuracy/factual
    if ofd.optimization_priority_order:
        combined = " ".join(ofd.optimization_priority_order).lower()
        if "factual" not in combined and "accuracy" not in combined and "correct" not in combined:
            findings.append(Finding(
                pass_number=PASS, severity="warning", section="ofd",
                field="optimization_priority_order",
                message="Priority order does not mention factual accuracy",
                suggestion="Consider including 'Factual correctness' as a priority",
            ))

    # Required for standard/complex tiers
    if tier in (Tier.STANDARD, Tier.COMPLEX):
        sev = "error"
    else:
        sev = "warning"

    if not ofd.secondary_objectives:
        findings.append(Finding(
            pass_number=PASS, severity=sev if tier != Tier.MICRO else "info",
            section="ofd", field="secondary_objectives",
            message="Secondary Objectives not defined",
            suggestion="Add secondary goals for standard/complex tiers",
        ))

    if not ofd.tradeoff_policies:
        findings.append(Finding(
            pass_number=PASS, severity=sev if tier != Tier.MICRO else "info",
            section="ofd", field="tradeoff_policies",
            message="Tradeoff Policies not defined",
            suggestion=None,
        ))

    if not ofd.scoring_model:
        findings.append(Finding(
            pass_number=PASS, severity=sev if tier != Tier.MICRO else "info",
            section="ofd", field="scoring_model",
            message="Scoring Model not defined",
            suggestion=None,
        ))

    if not ofd.escalation_triggers:
        findings.append(Finding(
            pass_number=PASS, severity=sev if tier != Tier.MICRO else "info",
            section="ofd", field="escalation_triggers",
            message="Escalation Triggers not defined",
            suggestion=None,
        ))

    if not ofd.error_severity_model:
        findings.append(Finding(
            pass_number=PASS, severity=sev if tier != Tier.MICRO else "info",
            section="ofd", field="error_severity_model",
            message="Error Severity Model not defined",
            suggestion="Define severity levels: critical, high, medium, low",
        ))

    return findings
