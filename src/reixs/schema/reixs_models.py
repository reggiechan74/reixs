"""REIXS specification data models."""

from __future__ import annotations

from datetime import date
from typing import Any

from pydantic import BaseModel

from reixs.schema.enums import Tier


class MetaSection(BaseModel):
    spec_id: str
    version: str
    task_type: str
    tier: Tier
    author: str
    date: date


class DomainContextSection(BaseModel):
    jurisdiction: str
    currency: str | None = None
    area_unit: str | None = None
    ddd_reference: str | None = None
    adr_references: list[str] | None = None
    extra: dict[str, str] = {}


class InputsSection(BaseModel):
    items: list[dict[str, str]]


class OFDSection(BaseModel):
    primary_objective: str
    hard_constraints: list[str]
    autofail_conditions: list[str]
    optimization_priority_order: list[str]
    uncertainty_policy: str
    secondary_objectives: list[str] | None = None
    tradeoff_policies: list[str] | None = None
    scoring_model: str | dict | None = None
    escalation_triggers: list[str] | None = None
    error_severity_model: dict[str, list[str]] | None = None


class ConstraintsSection(BaseModel):
    items: list[str]


class OutputContractSection(BaseModel):
    description: str
    fields: list[dict[str, str]] = []


class EvaluationSection(BaseModel):
    edd_suite_id: str | None = None
    min_pass_rate: str | None = None
    zero_tolerance: str | None = None
    regression_cases: list[str] = []
    raw_text: str = ""


class BehaviorSpecSection(BaseModel):
    raw_sesf: str
    sesf_blocks: list[str] = []


class ReixsSpec(BaseModel):
    meta: MetaSection
    objective: str
    domain_context: DomainContextSection
    inputs: InputsSection
    ofd: OFDSection
    constraints: ConstraintsSection
    output_contract: OutputContractSection
    evaluation: EvaluationSection
    behavior_spec: BehaviorSpecSection
    validation_checklist: list[str]
    source_hash: str
