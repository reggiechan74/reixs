# ADR-003: Hard Constraints Before Scoring

## Status
Accepted

## Context
The OFD section defines both hard constraints (absolute requirements) and a scoring model (weighted optimization). When evaluating AI outputs, the system must decide whether to score first and then check constraints, or vice versa.

## Decision
Hard constraint violations cause AUTOMATIC FAILURE before any weighted scoring is applied. An output that violates a hard constraint receives no score — it is rejected.

## Consequences
- AutoFail conditions are checked first in all evaluation paths
- The scoring model only applies to outputs that pass all hard constraints
- This prevents "high-scoring but factually wrong" results from passing
- Constraint checking is computationally cheaper than scoring, so this is also more efficient
