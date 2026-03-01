"""Validation report models."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, computed_field


class Finding(BaseModel):
    pass_number: int
    severity: Literal["error", "warning", "info"]
    section: str | None = None
    field: str | None = None
    message: str
    suggestion: str | None = None


class PassSummary(BaseModel):
    pass_number: int
    name: str
    errors: int = 0
    warnings: int = 0
    infos: int = 0


class ValidationReport(BaseModel):
    spec_id: str
    spec_version: str
    findings: list[Finding]
    pass_summaries: dict[int, PassSummary] = {}
    sesf_findings: list[dict[str, Any]] = []

    @computed_field
    @property
    def status(self) -> str:
        if any(f.severity == "error" for f in self.findings):
            return "fail"
        if any(f.severity == "warning" for f in self.findings):
            return "warn"
        return "pass"

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "error"]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "warning"]
