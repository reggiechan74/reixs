# ADR-001: Layered Artifact Boundaries

## Status
Accepted

## Context
REIXS specs reference multiple supporting artifacts: domain data dictionaries (DDD), architecture decision records (ADR), and evaluation datasets (EDD). The question is whether to embed these fully in the REIXS spec or reference them externally.

## Decision
REIXS runtime specs REFERENCE supporting artifacts (DDD, ADR, EDD) by versioned identifier rather than embedding their full content.

## Consequences
- REIXS specs stay focused on task execution, not domain definitions
- DDD/ADR/EDD can evolve independently with their own versioning
- Validator checks that references exist and are well-formatted
- Downstream consumers must resolve references to access full content
