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
