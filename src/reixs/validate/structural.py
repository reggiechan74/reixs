"""Pass 1: Structural validation."""

from __future__ import annotations

import re

from reixs.schema.reixs_models import ReixsSpec
from reixs.validate.report import Finding

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
PASS = 1


def validate_structural(spec: ReixsSpec) -> list[Finding]:
    findings: list[Finding] = []

    if not SEMVER_RE.match(spec.meta.version):
        findings.append(Finding(
            pass_number=PASS, severity="error", section="meta",
            field="version", message=f"Version '{spec.meta.version}' is not valid semver",
            suggestion="Use format: X.Y.Z (e.g., 1.0.0)",
        ))

    if not spec.meta.spec_id:
        findings.append(Finding(
            pass_number=PASS, severity="error", section="meta",
            field="spec_id", message="Spec ID is missing",
            suggestion="Add a unique spec ID (e.g., REIXS-LA-ON-001)",
        ))

    if not spec.meta.task_type:
        findings.append(Finding(
            pass_number=PASS, severity="error", section="meta",
            field="task_type", message="Task Type is missing",
            suggestion="Specify the task type (e.g., Lease Abstraction)",
        ))

    if not spec.objective:
        findings.append(Finding(
            pass_number=PASS, severity="error", section="objective",
            field=None, message="Objective section is empty",
            suggestion="Describe what this spec accomplishes",
        ))

    if not spec.validation_checklist:
        findings.append(Finding(
            pass_number=PASS, severity="warning", section="validation_checklist",
            field=None, message="Validation checklist is empty",
            suggestion="Add checklist items to verify spec completeness",
        ))

    return findings
