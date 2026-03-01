# ADR-004: Dual Output Contracts in a Single Spec

## Status
Accepted

## Context
The lease abstraction workflow produces two output formats: JSON (for data integration and programmatic analysis) and Markdown (for executive review and human consumption). When designing the REIXS spec, we had to decide whether to create separate specs for each output format or combine both output contracts into a single spec.

Options considered:
1. **Separate specs** — one `.reixs.md` for JSON output, one for Markdown output. Each spec has a single, simple output contract.
2. **Single spec, dual contracts** — one `.reixs.md` with both JSON and Markdown output contracts defined in the Output Contract section. The caller specifies which format at invocation time.
3. **Single spec, abstract contract** — one `.reixs.md` with a format-neutral output contract. The orchestrator interprets the contract into the appropriate format.

## Decision
Use a single REIXS spec with dual output contracts (Option 2). The Output Contract section describes requirements for both JSON and Markdown formats. The caller (slash command) specifies which format to produce via a flag (`-json`).

## Consequences
- One spec to maintain instead of two — extraction rules, hard constraints, SESF behaviors, and OFD are defined once
- The Output Contract section is longer but self-contained — both contracts share the same field-level status/provenance requirements
- The orchestrator (slash command) owns format selection, not the spec
- Format-specific differences (e.g., `null` vs `"Not specified"` for missing values, inline status indicators vs structured metadata) are documented in the Output Contract rather than split across files
- Validation checklist must verify both output contracts are consistent
- Future formats (e.g., CSV, Excel) can be added to the same spec without forking
