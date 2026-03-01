# Tutorial: Write Your First REIXS Spec

You're about to write a complete `.reixs.md` file from scratch. By the end of this tutorial, you'll have a validated, compilable spec for a **property valuation summary** task — and you'll understand every section well enough to write specs for your own tasks.

We're deliberately using a different domain than the built-in lease abstraction template. If we used the same domain, you'd be tempted to copy and tweak. Writing a spec for a new domain forces you to think through each section yourself, which is how you actually learn the format.

**What you'll build:** A REIXS spec that tells an AI agent how to extract key valuation metrics from a residential appraisal report (British Columbia jurisdiction) and produce a structured summary with source page references.

## Prerequisites

You need Python 3.10+ and git. That's it.

```bash
git clone https://github.com/reggiechan74/reixs.git
cd reixs
pip install -e ".[dev]"
reixs --version
```

You should see a version number (e.g., `0.1.0`). If `reixs --version` fails, check that the `pip install` completed without errors and that the `reixs` entry point is on your `PATH`.

Now create a working file:

```bash
touch my_spec.reixs.md
```

We'll build this file section by section. After each step, you'll run `reixs validate my_spec.reixs.md` to see what the validator thinks. Expect errors early on — that's the point. The validator gives you actionable feedback, and watching the error count drop as you add sections is the fastest way to internalize the format.

## Step 1: Create the File — Meta Section

Open `my_spec.reixs.md` in your editor and add:

```markdown
# REIXS: Property Valuation Summary — British Columbia

## Meta

- Spec ID: REIXS-PV-BC-001
- Version: 0.1.0
- Task Type: Property Valuation
- Tier: micro
- Author: Your Name
- Date: 2026-03-01
```

Let's unpack what each field does:

- **Spec ID** — A unique identifier for this spec. The convention is `REIXS-TYPE-JURISDICTION-SEQ` (so `PV` for Property Valuation, `BC` for British Columbia, `001` for the first version), but any non-empty string works.
- **Version** — Semantic versioning (`X.Y.Z`). We're starting at `0.1.0` because this is a draft.
- **Task Type** — What kind of real estate task this is. `Property Valuation` isn't in the built-in registry (only `Lease Abstraction` is, as of v0.1.0), so you'll see a warning — that's expected and harmless.
- **Tier** — One of `micro`, `standard`, or `complex`. We're using `micro` because this is a simple, self-contained task. The tier controls how strict the OFD section validation is: `micro` only requires 5 mandatory OFD sub-sections, while `standard` and `complex` require all 10. Start small.
- **Author** — Your name. No validation beyond "not empty."
- **Date** — ISO 8601 format (`YYYY-MM-DD`).

Now run the validator:

```bash
reixs validate my_spec.reixs.md
```

You'll see errors about missing sections — something like "missing required section: objective", "missing required section: domain_context", and so on for all 9 sections we haven't written yet. That's exactly right. A REIXS spec has 10 mandatory sections, and we've only written one. The validator is telling you what to do next.

## Step 2: Objective

Add this after the Meta section:

```markdown
## Objective

Extract key valuation metrics from a residential appraisal report (BC jurisdiction)
and produce a structured summary with source page references.
```

The Objective section is the simplest one in the spec. It's a free-text paragraph — no bullet lists, no key-value pairs, no special syntax. The only rule is that it can't be empty. Write one or two sentences that describe what the task accomplishes.

Think of it as the "elevator pitch" for the spec. If someone reads only this section, they should understand the task at a high level.

Run `reixs validate my_spec.reixs.md` again. You should see one fewer error now — the "missing required section: objective" message is gone.

## Step 3: Domain Context

Add this next:

```markdown
## Domain Context

- Jurisdiction: British Columbia, Canada
- Currency: CAD
- DDD Reference: re-ddd:property_valuation_bc@0.1.0
```

This section uses the `Key: Value` bullet syntax that you already saw in Meta. Three things to note:

- **Jurisdiction** is required. It's free text — the validator accepts any non-empty string, though it knows about some jurisdictions (like `Ontario, Canada`) for cross-field checks. `British Columbia, Canada` isn't in the known registry, but that's fine. The registry is advisory, not restrictive.

- **Currency** is optional but good practice. If you were writing a spec for Ontario and omitted the currency, the validator would emit a cross-field warning reminding you. For BC, no such warning exists, but declaring the currency explicitly is clearer.

- **DDD Reference** is required and must follow the format `re-ddd:<name>@X.Y.Z`. That regex is enforced — if you write something like `property_valuation_bc` without the `re-ddd:` prefix and version suffix, the validator will reject it. Our reference `re-ddd:property_valuation_bc@0.1.0` has valid format, but it's not in the built-in registry (which only knows about `re-ddd:lease_core_terms_ontario@0.1.0`). You'll get a warning about that — a warning, not an error. The validator is saying "I don't recognize this DDD reference, make sure it's correct" rather than "this is invalid."

Run the validator again. The missing-section errors for `domain_context` should be gone, possibly replaced by a warning about the unrecognized DDD reference.

## Step 4: Inputs

Add this:

```markdown
## Inputs

- Source document: PDF appraisal report
- Document type: Residential property appraisal (Form 1004 or equivalent)
- Expected length: 10-50 pages
```

The Inputs section is the most free-form section in a REIXS spec. There are no required fields — the content is entirely domain-specific. You define whatever inputs are relevant for your task, and the validator won't complain about missing fields.

Each bullet follows the same `Key: Value` syntax. The parser normalizes the key to `snake_case` (so `Source document` becomes `source_document`) and stores the value as a string. If you write a bullet without a colon (like `- The original scanned PDF`), it gets stored as a plain list item instead of a key-value pair. Both forms are valid.

This section tells downstream agents what they'll receive at runtime. Be specific enough that an agent knows what format to expect, but don't over-specify — details about how to process the input belong in the OFD and Behavior Spec sections.

Run `reixs validate my_spec.reixs.md` once more. You've now written 4 of 10 sections. The validator should report 6 missing sections remaining.

## Step 5: Objective Function Design (OFD)

This is the heart of the spec. The OFD tells the agent what to optimize for, what never to do, and how to handle ambiguity. The number of sub-sections depends on your tier: `micro` requires 5, `standard` requires all 10, and `complex` requires all 10 plus additional depth. Since we chose `micro` in Step 1, we only need the 5 mandatory sub-sections.

Add this:

```markdown
## Objective Function Design (OFD)

### Primary Objective
Extract property valuation metrics with factual accuracy >= 95%.

### Hard Constraints
- NEVER fabricate a value not present in the appraisal report
- NEVER alter assessed values — extract verbatim
- ALL extracted values MUST include the source page number

### AutoFail Conditions
- Any fabricated valuation figure
- Market value extracted without page reference

### Optimization Priority Order
1. Factual correctness
2. Completeness of key metrics
3. Source traceability

### Uncertainty Policy
When a metric requires interpretation (e.g., adjusted vs. unadjusted value),
mark as INFERENCE with reasoning. Never present interpretations as facts.
```

Let's walk through each sub-section:

- **Primary Objective** — A single sentence stating the top-level goal and a measurable threshold. The validator checks for words like "factual" or "accuracy" in this sub-section (it's a soft heuristic, not a hard regex, but including them avoids a warning). This is what the agent optimizes for above all else.

- **Hard Constraints** — Absolute rules the agent must never violate. Think of these as the "guardrails." They should be machine-checkable where possible — "NEVER fabricate a value" is clear enough that a downstream evaluator can flag violations.

- **AutoFail Conditions** — Specific scenarios that constitute immediate failure. The difference from Hard Constraints is granularity: constraints are general rules, AutoFail conditions are concrete test cases. If an evaluator detects any of these, the entire run is scored as a failure regardless of how well everything else went.

- **Optimization Priority Order** — A ranked list that tells the agent what to prioritize when trade-offs are necessary. If the agent can extract all metrics with perfect accuracy but it takes longer, is that okay? This list says yes — factual correctness comes first, completeness second, speed isn't even in the list.

- **Uncertainty Policy** — How the agent should handle ambiguous or missing data. This is where you prevent the "confidently wrong" failure mode. Our policy says: label it as INFERENCE, show your reasoning, and never present an interpretation as a fact.

These 5 mandatory sub-sections define the agent's optimization landscape. If you were writing a `standard` or `complex` tier spec, you'd also need 5 additional sub-sections (Soft Preferences, Scope Boundaries, Interaction with Jurisdiction, Conflict Resolution, and Success Metrics). For `micro`, the 5 above are sufficient.

Run `reixs validate my_spec.reixs.md`. The "missing required section: ofd" error should be gone. If you misspelled a sub-section heading, you'll see a warning about a missing mandatory OFD sub-section — the validator matches headings by normalized name, so `Primary Objective`, `primary_objective`, and `Primary objective` all resolve to the same thing.

## Step 6: Constraints

Add this:

```markdown
## Constraints

- Processing time: < 60 seconds per document
- Output format: JSON
- Offline processing only — no external API calls
```

The Constraints section captures operational limits — things that don't affect what the agent does, but how it's allowed to do it. Processing time, output format, network access, memory limits, that kind of thing.

Like the Inputs section, there are no required fields here. The content is entirely domain-specific. The validator only checks that the section exists and isn't empty. You could have one constraint or twenty — whatever is relevant for your task.

The distinction between Constraints (here) and Hard Constraints (in the OFD) is important: OFD Hard Constraints are about correctness ("never fabricate data"), while this section is about operational boundaries ("must finish in 60 seconds"). One is about the quality of the output, the other is about the conditions of execution.

Run the validator. One more section checked off.

## Step 7: Output Contract

Add this:

```markdown
## Output Contract

Each extracted metric MUST include:
- `value`: the extracted numeric or text value
- `status`: FACT | INFERENCE | MISSING
- `provenance`: { page } (required for FACT status)
```

The Output Contract defines the structure of what the agent produces. This is where you specify the shape of the output — what fields are present, what values they can take, and what invariants hold.

Two things matter for validation:

1. The section must not be empty.
2. The validator checks for the presence of words like "provenance" or "status" as a heuristic signal that you've thought about traceability. This isn't a hard requirement — the validator won't reject a spec that omits these words — but it will emit a warning nudging you to consider them. Our Output Contract mentions both, so no warnings here.

Notice how the Output Contract connects back to the OFD's Uncertainty Policy: we defined three status values (`FACT`, `INFERENCE`, `MISSING`) and the Uncertainty Policy explained when to use `INFERENCE`. This kind of cross-section coherence is what separates a good spec from a collection of disconnected sections.

Run the validator again. You should be down to just 2 missing sections now.

## Step 8: Evaluation / EDD

Add this:

```markdown
## Evaluation / EDD

- Minimum pass rate: 90%
- Regression cases: basic_appraisal, missing_market_value
```

The Evaluation section (also called EDD, for Evaluation-Driven Design) defines how you'll know whether the agent is working correctly. At minimum, you need a pass rate threshold and some regression test cases.

For `micro` tier, an EDD Suite ID is optional. If you were writing a `standard` or `complex` spec, you'd need to provide one — a reference to a formal test suite that evaluators can run. At `micro` tier, listing a few regression case names is sufficient. These names don't have to resolve to actual test files right now; they serve as documentation of what scenarios you intend to test.

The `Minimum pass rate: 90%` line means that if you run the agent against a test suite, at least 90% of cases must pass for the spec to be considered "met." The regression cases tell future-you (or a teammate) which specific scenarios to include in that suite.

Run the validator. One section to go.

## Step 9: Validation Checklist

Add this:

```markdown
## Validation Checklist

- [ ] All key valuation fields addressed in output contract
- [ ] Hard constraints are machine-checkable
- [ ] Jurisdiction metadata (currency) declared
```

The Validation Checklist is a self-audit. Before you finalize a spec, you walk through this list and check each item. It's a forcing function to make sure you didn't miss something obvious.

The validator checks that this section exists and isn't empty, but it doesn't inspect the content of individual checklist items. It will emit a warning if the section is empty (zero items), but won't tell you whether your checklist items are good or bad — that's your judgment call.

Use the `- [ ]` Markdown checkbox syntax so the checklist is interactive if you view the spec in an editor that supports it (like GitHub or Obsidian). You can check items off as you verify them:

```markdown
- [x] All key valuation fields addressed in output contract
- [x] Hard constraints are machine-checkable
- [x] Jurisdiction metadata (currency) declared
```

Run the validator one final time:

```bash
reixs validate my_spec.reixs.md
```

If you've followed every step, you should see zero errors. You may still see warnings — about the unrecognized Task Type, the unrecognized DDD Reference, or similar advisory messages — but no errors. Warnings are informational; errors are blockers. A spec with zero errors and a few warnings is perfectly valid.

---

**What we've built so far:** A 9-section spec covering Meta, Objective, Domain Context, Inputs, OFD, Constraints, Output Contract, Evaluation, and Validation Checklist. That's 9 of 10 mandatory sections. The remaining section — the Behavior Spec (SESF) — is where you define the agent's step-by-step behavior, and it gets its own dedicated chapter next.

## Step 10: Behavior Spec (SESF)

This is the trickiest part of a REIXS spec — and the most powerful. The Behavior Spec uses SESF (Structured English Specification Format) to define extraction rules, error handling, and worked examples in a way that's readable by humans and parseable by machines.

The SESF block lives inside a fenced code block with the `sesf` language tag. Add this to your spec:

````markdown
## Behavior Spec (SESF)

```sesf
Property Valuation Extraction Rules

Meta: Version 0.1.0 | Date: 2026-03-01 | Domain: Property Valuation | Status: active | Tier: micro

Purpose
Define extraction rules for residential property valuation metrics.

BEHAVIOR extract_valuation_metrics: Extract key valuation data from appraisal reports

  RULE verbatim_value:
    WHEN a valuation figure is found verbatim in the report
    THEN status MUST be FACT
    AND provenance MUST include page number

  RULE derived_value:
    WHEN a metric requires calculation or interpretation
    THEN status MUST be INFERENCE
    AND reasoning MUST explain the derivation

  ERROR fabricated_value:
    WHEN an extracted value cannot be traced to the source report
    SEVERITY critical
    ACTION reject the extraction
    MESSAGE "Value has no source provenance — possible fabrication"

  EXAMPLE basic_extraction:
    INPUT: appraisal with market value "$650,000" on page 2
    EXPECTED: { "value": 650000, "status": "FACT", "provenance": { "page": 2 } }
    NOTES: Simple numeric extraction with provenance

Constraints
* All key valuation fields must be processed before completion
```
````

That's a lot of new syntax. Let's break it down piece by piece.

**The `Meta:` line** is required inside every SESF block. It uses a pipe-delimited format to declare Version, Date, Domain, Status, and Tier — all on a single line. The validator will reject an SESF block that's missing the Meta line entirely. Version must be semver (`X.Y.Z`), Status must be one of `active`, `draft`, or `deprecated`, and Tier must match one of `micro`, `standard`, or `complex`.

**`BEHAVIOR` declarations** are the top-level containers for your rules. Each BEHAVIOR gets a name (like `extract_valuation_metrics`) and a one-line description after the colon. You need at least one BEHAVIOR in every SESF block. Think of a BEHAVIOR as a function definition — it groups related rules together.

**`RULE` blocks** define the conditional logic inside a BEHAVIOR. The structure is always `WHEN` (the condition), `THEN` (the primary action), and optionally `AND` for additional requirements. Rules are the core of SESF — they tell the agent what to do in specific situations. Each RULE needs a name (like `verbatim_value`) so it can be referenced in error messages and test results.

**`ERROR` blocks** define what happens when something goes wrong. They require three fields: `SEVERITY` (one of `critical`, `high`, `medium`, `low`), `ACTION` (what the agent should do), and `MESSAGE` (a human-readable explanation). Critical severity means the agent must stop and report the error; lower severities allow the agent to continue with a warning.

**`EXAMPLE` blocks** are worked examples that serve as both documentation and test cases. They require `INPUT` (what goes in), `EXPECTED` (what should come out), and `NOTES` (why this example matters). The validator checks that EXAMPLE blocks have all three fields, but it doesn't execute the example — that's the job of the EDD test suite.

**The `Constraints` section** at the end of the SESF block uses `*` bullet items to declare operational constraints specific to the behavior. This is distinct from the top-level Constraints section in the REIXS spec — the SESF Constraints are scoped to this particular behavior, while the REIXS Constraints apply to the entire task.

One thing that trips people up: the SESF block has its own Meta line that's separate from the REIXS Meta section at the top of the file. They can have different versions (e.g., you might update the SESF rules without bumping the overall spec version), but the Domain and Tier should be consistent. The validator will warn if they diverge.

## Step 11: Validate the Complete Spec

You've now written all 10 mandatory sections. Run the validator one more time:

```bash
reixs validate my_spec.reixs.md
```

Expected result: **Status: WARN** (not FAIL). You should see zero errors and a handful of warnings. The warnings you'll see are expected:

- **"Task type 'Property Valuation' not in known registry"** — This is fine. The registry currently only knows about `Lease Abstraction`, and it's designed to be extensible. Your task type is valid; the validator is just telling you it hasn't seen it before.

- **"DDD Reference not found in local registry"** — Also fine. Our `re-ddd:property_valuation_bc@0.1.0` reference has correct format but points to a domain dictionary that doesn't ship with the default registry. When you (or your team) create that dictionary, this warning will disappear.

If you see any **ERRORS** instead of warnings, here are quick fixes for the most common ones:

- **Version not semver** — Make sure both the REIXS Meta `Version` and the SESF Meta `Version` use the `X.Y.Z` format. Not `v1.0`, not `1.0`, not `version 1` — exactly three numbers separated by dots.

- **DDD Reference format invalid** — The format must be `re-ddd:<name>@X.Y.Z`. Check for typos: missing `re-ddd:` prefix, missing `@` separator, or a version that isn't semver.

- **OFD fields missing** — If you're on `micro` tier, you need the 5 mandatory OFD sub-sections (Primary Objective, Hard Constraints, AutoFail Conditions, Optimization Priority Order, Uncertainty Policy). Check that your H3 headings match these names exactly. The validator normalizes casing and whitespace, but the heading text must be recognizable.

## Step 12: Compile

Once validation passes (status WARN or PASS — anything except FAIL), you can compile the spec into runtime artifacts:

```bash
reixs compile my_spec.reixs.md -o build/
```

This produces two files in the `build/` directory:

- **`reixs.runtime.json`** — The machine-readable version of your spec. This is what agent developers actually consume.
- **`reixs.manifest.json`** — A lightweight manifest with metadata (spec ID, version, tier, task type) for registry and discovery purposes.

Inspect the runtime JSON to see what an agent developer receives:

```bash
cat build/reixs.runtime.json | python -m json.tool
```

The runtime JSON contains everything from your `.reixs.md` file, parsed and structured: the meta fields, the OFD sub-sections as keyed objects, the SESF rules decomposed into condition/action pairs, the examples as input/expected tuples. An agent developer doesn't need to parse Markdown — they load this JSON file and get a structured representation of every rule, constraint, and example you defined.

The manifest JSON is much smaller — just the metadata needed to register this spec in a catalog or check compatibility between specs. Think of the runtime JSON as the "full build" and the manifest as the "package.json."

---

## Common Mistakes

These are the top 5 validation failures we see, with exact error messages and fixes.

### 1. Version is not semver

```
Error: Version 'v1.0' is not valid semver
```

**Fix:** Use the `X.Y.Z` format — three integers separated by dots. No `v` prefix, no two-part versions, no text. `0.1.0` is valid. `v1.0` is not. `1.0` is not. `1.0.0-beta` is not (pre-release tags aren't supported yet).

### 2. DDD Reference format invalid

```
Error: DDD Reference 'lease_terms_v1' has invalid format
```

**Fix:** The required format is `re-ddd:<name>@X.Y.Z`. The reference `lease_terms_v1` is missing the `re-ddd:` prefix and the `@` version separator. The correct form would be `re-ddd:lease_terms@1.0.0`.

### 3. EDD Suite ID required for standard/complex tier

```
Error: EDD Suite ID is required for standard tier
```

**Fix:** If your spec declares `Tier: standard` or `Tier: complex`, the Evaluation / EDD section must include an `EDD Suite ID` field pointing to a formal test suite. Either add the suite ID (e.g., `EDD Suite ID: edd-pv-bc-001`) or downgrade to `Tier: micro` if you don't have a test suite yet. Starting at micro and upgrading later is a perfectly valid workflow.

### 4. SESF block has no Meta section

```
Error: SESF block missing required Meta line
```

**Fix:** Add a `Meta:` line inside the SESF fenced block. It must be a single line with pipe-delimited fields: `Meta: Version X.Y.Z | Date YYYY-MM-DD | Domain <name> | Status active | Tier micro`. This is separate from the REIXS-level Meta section — the SESF block needs its own.

### 5. Complex tier requires ADR references

```
Error: Complex tier spec must include ADR References
```

**Fix:** If your spec declares `Tier: complex`, you must include an `ADR References` field in the Meta section (or a dedicated ADR section) linking to Architecture Decision Records that justify design choices. If you don't have ADRs, downgrade to `Tier: standard` or `Tier: micro`. Tier complexity is meant to be earned — don't declare complex unless the spec genuinely needs it.

---

## Next Steps

You've written, validated, and compiled a complete REIXS spec from scratch. Here's where to go from here:

- **Read the full specification:** [`REIXS-SPEC.md`](REIXS-SPEC.md) covers every section, field, and validation rule in detail. The tutorial showed you the "what" — the spec explains the "why."

- **Study the lease template:** The built-in lease abstraction template (`templates/lease_abstraction_ontario.reixs.md`) is a production-grade `standard` tier spec. Compare it to the `micro` spec you just wrote — notice how it includes the 5 additional OFD sub-sections, an EDD Suite ID, and more detailed SESF rules.

- **Upgrade to standard tier:** Change `Tier: micro` to `Tier: standard` in your spec and run `reixs validate` again. The validator will tell you exactly which additional sub-sections are required. Adding them is a good exercise to deepen your understanding of the format.
